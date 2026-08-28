"""Rendering + presentation. Builders use lineup()/turntable() to see their work;
the hero cameras exist so our renders can be put NEXT TO the reference paintings
at matching angle and light, which is the whole point of the comparison.

CAM_REF1  low 3/4 street view, warm afternoon sun, blue sky   -> matches fantasy_inn.jpg
CAM_REF2  elevated 3/4 long-lens view, soft light, grey void  -> matches Inn.jpg
"""
import bpy, math, os
from math import radians, tan, sqrt
from mathutils import Vector, Euler
from . import spec as S
from . import mats as M


# ------------------------------------------------------------------ engines --
def _set_transform(*names):
    """Set the view transform by assignment, verified by read-back.

    bl_rna enum introspection returns nothing in background mode, so testing
    membership before assigning silently picks the fallback forever. Assign, then
    check what actually stuck.
    """
    vs = bpy.context.scene.view_settings
    for n in names:
        try:
            vs.view_transform = n
        except TypeError:
            continue
        if vs.view_transform == n:
            return n
    print(f"TRANSFORM_FAILED {names}; left at {vs.view_transform!r}")
    return vs.view_transform


def engine(eevee=True, samples=64, res=(1200, 800), transparent=False):
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE' if eevee else 'CYCLES'
    if eevee:
        try:
            sc.eevee.taa_render_samples = samples
            sc.eevee.use_raytracing = True
            sc.eevee.use_shadows = True
            # a 17 m building with a hard sun needs more than the default
            # shadow budget, or eave and chimney shadows go blotchy
            sc.eevee.shadow_ray_count = 4
            sc.eevee.shadow_step_count = 8
            sc.eevee.shadow_resolution_scale = 2.0
            sc.eevee.shadow_pool_size = '512'
        except Exception:
            pass
    else:
        sc.cycles.samples = samples
        sc.cycles.use_denoising = True
        sc.cycles.max_bounces = 6
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = 'PNG'
    # NOT by enum introspection. bl_rna enum_items for view_transform comes back
    # EMPTY in background mode, so the old `'AgX' if 'AgX' in [...] else 'Filmic'`
    # test was always False and every headless render this project ever made used
    # FILMIC -- while look_ref1's comments reasoned at length about how "AgX
    # compresses the top three stops". They were describing a transform that was
    # never active. Filmic is far flatter at the top, which is exactly why the
    # frame measured max 229 with 0.000% of pixels above 230 and three blind
    # critics all said nothing reads as struck by sunlight.
    # Assignment works even where introspection does not, so try and read back.
    _set_transform('AgX', 'Filmic')
    sc.view_settings.look = 'None'
    return sc


# -------------------------------------------------------------------- world --
def world(top=(0.35, 0.50, 0.78), bottom=(0.55, 0.52, 0.48), strength=1.0,
          sky_gain=1.0):
    """Gradient sky. `sky_gain` brightens what the CAMERA sees without touching
    what the scene is LIT by.

    The two are normally the same number, which is a trap: the painting has a sky
    at luminance 98-124 and a roof mass at 52, while ours had sky 70 and roof 78 --
    the roof was LIGHTER than the sky, so the top third of the silhouette had no
    edge at all. Raising world strength fixes the sky and simultaneously lifts every
    shadow, flattening the contrast the same critics asked for. Splitting on
    Light Path > Is Camera Ray gives the backdrop its own exposure while the ambient
    fill stays where it was.
    """
    w = bpy.data.worlds.get("KitWorld") or bpy.data.worlds.new("KitWorld")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld"); out.location = (400, 0)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.location = (200, 0)
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.location = (-60, 0)
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (*bottom, 1)
    ramp.color_ramp.elements[1].position = 0.62
    ramp.color_ramp.elements[1].color = (*top, 1)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-260, 0)
    tex = nt.nodes.new("ShaderNodeTexCoord"); tex.location = (-440, 0)
    m = nt.nodes.new("ShaderNodeMath"); m.location = (-160, -140)
    m.operation = 'MULTIPLY_ADD'; m.inputs[1].default_value = 0.5; m.inputs[2].default_value = 0.5
    nt.links.new(tex.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], m.inputs[0])
    nt.links.new(m.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    if abs(sky_gain - 1.0) < 1e-6:
        nt.links.new(bg.outputs[0], out.inputs["Surface"])
        return w
    bg2 = nt.nodes.new("ShaderNodeBackground"); bg2.location = (200, 180)
    bg2.inputs["Strength"].default_value = strength * sky_gain
    nt.links.new(ramp.outputs["Color"], bg2.inputs["Color"])
    lp = nt.nodes.new("ShaderNodeLightPath"); lp.location = (200, 380)
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.location = (330, 90)
    nt.links.new(bg.outputs[0], mix.inputs[1])      # fac 0 -> ambient
    nt.links.new(bg2.outputs[0], mix.inputs[2])     # fac 1 -> what the camera sees
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return w


def sun(energy=3.0, angle_deg=(52, 0, 34), softness=2.5, color=(1.0, 0.94, 0.84)):
    """ONE key sun, replacing any existing one.

    This used to call lights.new() unconditionally and never remove the previous
    object, so every invocation added another sun -- which made `sun(energy=0)` a
    no-op in any scene that already had one, and turned three separate "sun off"
    control renders on this project into sunlit renders presented as controls.

    area() is deliberately NOT given the same treatment: look_ref1 places two
    independent fills and assemble_layouts' street look places six, and
    collapsing them to one reinstates a documented lighting fault.
    """
    for _o in list(bpy.data.objects):
        if _o.type == 'LIGHT' and _o.data.type == 'SUN':
            bpy.data.objects.remove(_o, do_unlink=True)
    l = bpy.data.lights.new("KeySun", 'SUN')
    l.energy = energy
    l.angle = radians(softness)
    l.color = color
    ob = bpy.data.objects.new("KeySun", l)
    bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = [radians(a) for a in angle_deg]
    return ob


def area(loc, energy=200, size=6, color=(0.75, 0.85, 1.0), target=(0, 0, 1.5)):
    l = bpy.data.lights.new("Fill", 'AREA')
    l.energy = energy; l.size = size; l.color = color
    ob = bpy.data.objects.new("Fill", l)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob


def ground(size=60, color="stone_dark", z=-0.02):
    """The studio/hero backdrop floor. Sits slightly BELOW z=0 on purpose: kit
    ground pieces (cobbles, thresholds, steps) sit at z=0, and a backdrop at exactly
    z=0 z-fights them into a flickering near-black mess.
    """
    me = bpy.data.meshes.new("Ground")
    h = size / 2
    me.from_pydata([(-h, -h, z), (h, -h, z), (h, h, z), (-h, h, z)], [], [(0, 1, 2, 3)])
    me.update()
    ca = me.color_attributes.new(name="Col", type='FLOAT_COLOR', domain='CORNER')
    for i in range(len(me.loops)):
        ca.data[i].color = (1, 1, 1, 1)
    me.materials.append(M.get(color))
    ob = bpy.data.objects.new("Ground", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


# ------------------------------------------------------------------- camera --
def bbox_of(objs):
    bpy.context.view_layer.update()          # matrices must not be stale
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in objs:
        if o.type != 'MESH':
            continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    if lo.x > 1e8:
        return Vector((0, 0, 0)), Vector((1, 1, 1))
    return lo, hi


def camera(objs, yaw=48, pitch=68, lens=50, margin=1.18, ortho=False, target=None,
           shift=(0, 0)):
    """Frame `objs`. yaw/pitch in degrees; pitch 90 = horizontal, <90 looks down."""
    lo, hi = bbox_of(objs)
    ctr = target or ((lo + hi) / 2)
    rad = max((hi - lo).length / 2, 0.5)
    cd = bpy.data.cameras.new("Cam")
    cd.lens = lens
    cd.shift_x, cd.shift_y = shift
    if ortho:
        cd.type = 'ORTHO'
        cd.ortho_scale = rad * 2 * margin
        dist = rad * 4
    else:
        fov = 2 * math.atan(18.0 / lens)   # half-sensor 18mm (36mm sensor)
        dist = rad * margin / max(tan(fov / 2), 1e-3)
    ob = bpy.data.objects.new("Cam", cd)
    bpy.context.scene.collection.objects.link(ob)
    eul = Euler((radians(pitch), 0.0, radians(yaw)), 'XYZ')
    ob.rotation_euler = eul
    # camera looks down its local -Z, so back it off along +Z. Derive the
    # direction from the euler directly -- matrix_world is not evaluated yet.
    d = eul.to_matrix() @ Vector((0.0, 0.0, 1.0))
    ob.location = Vector(ctr) + d * dist
    bpy.context.view_layer.update()
    bpy.context.scene.camera = ob
    return ob


# ---------------------------------------------------------------- presets ----
def studio(objs, res=(1400, 900), samples=48, eevee=True, bg="mid"):
    """Neutral turnaround lighting for judging a single piece or a lineup."""
    engine(eevee=eevee, samples=samples, res=res)
    if bg == "mid":
        world(top=(0.42, 0.45, 0.50), bottom=(0.30, 0.30, 0.31), strength=1.25)
    else:
        world(top=(0.75, 0.78, 0.82), bottom=(0.60, 0.60, 0.62), strength=1.6)
    sun(energy=3.4, angle_deg=(50, 0, 38), softness=6.0)
    area((-9, -7, 7), energy=420, size=9, color=(0.72, 0.82, 1.0))
    ground(color="stone_dark")
    return objs


def _set_look(name):
    """Set the view-transform look, tolerating the two naming conventions.

    Blender has shipped these as both 'High Contrast' and 'AgX - High Contrast'
    depending on the OCIO config, and assigning an unknown one raises TypeError
    mid-render. Worse, a try/except around a bare assignment fails SILENTLY, which
    is how a whole tone-mapping sweep of mine produced numbers for a look that was
    never actually applied. So this reads the value back and says what it got.
    """
    vs = bpy.context.scene.view_settings
    for cand in (name, f"AgX - {name}", name.replace("AgX - ", "")):
        try:
            vs.look = cand
        except TypeError:
            continue
        if vs.look in (cand, f"AgX - {cand}"):
            return vs.look
    print(f"LOOK_FAILED {name!r}; left at {vs.look!r}")
    return vs.look


def look_ref1():
    """Warm afternoon, strong blue sky bounce, hard sun from upper left.
    Matches fantasy_inn.jpg. The ambient is deliberately LOW: the painting's
    stone base is a dark mass and its jetty throws a real shadow band, and a
    bright sky fill is what flattened round 1 into one even value."""
    # clear_stage FIRST. sun() and area() call bpy.data.lights.new on every
    # invocation and never remove the previous object, so lights ACCUMULATE:
    # a caller that set this look and then asked for sun(energy=0) got
    # "KeySun 22.0 W" sitting next to "KeySun.001 0.0 W", and its "sun off"
    # control render came back 56.5% bit-identical to the lit one. That voided
    # the control in three separate investigations on this project, including
    # one of mine that I reported to the user as evidence.
    clear_stage()
    engine(eevee=True, samples=96, res=(1440, 810))
    # sky_gain, measured. The ambient stays at 0.40 -- it is deliberately low and
    # raising it flattens the shadow side -- but the BACKDROP the camera sees is
    # lifted, because the roof was reading LIGHTER than the sky:
    #     gain 1.0   sky  70  roof 78   gap  -8.8   <- no silhouette at all
    #     gain 2.0   sky 115  roof 88   gap +27
    #     gain 2.8   sky 142  roof 94   gap +48     (sky past the painting's 124)
    # The painting runs sky 98-124 against a roof mass of 52. 2.0 puts the sky in
    # that band; the rest of the gap is the shingle albedo, not the lighting.
    world(top=(0.21, 0.37, 0.74), bottom=(0.46, 0.38, 0.28), strength=0.40,
          sky_gain=2.0)
    # SUN AZIMUTH. (52, 0, -58) put the light behind the camera's own shoulder,
    # so both visible elevations were lit head-on at 0.7 and 0.85 and the whole
    # facade came out one value -- flat lighting cannot be rescued by exposure.
    # At (58, 0, 40) it comes over the far shoulder instead: the long street
    # front takes 0.65, the near west end takes NOTHING and the hero's near roof
    # slope takes nothing either, so the frame gets the paintings' arrangement --
    # one big shaded mass nearest the camera, the lit range running away behind
    # it. That single change is worth more to the value structure than any
    # exposure tweak, because it is what creates the darks in the first place.
    sun(energy=22.0, angle_deg=(56, 0, 32), softness=1.1, color=(1.0, 0.88, 0.64))
    area((14, -12, 10), energy=30, size=16, color=(0.52, 0.70, 1.0))
    # warm ground bounce: what makes the shaded side of a sunlit stone building
    # glow instead of going blue-grey, and both paintings have it
    area((-8, -14, 1.2), energy=38, size=22, color=(1.0, 0.72, 0.42),
         target=(2, 0, 5.0))
    # EXPOSURE. fantasy_inn.jpg spans L=60 in its shaded stone to L=141 on its
    # lit plaster. At the old exposure our whole facade sat inside L=80..100 --
    # every material landed on the same mid grey, so no amount of palette work
    # could separate stone from timber. AgX lifts darks and compresses lights,
    # so the fix is to open up rather than to keep darkening the albedos.
    # ... but spec.PALETTE has since been corrected (timber L=48 against plaster
    # L=217) and assemble_inn.py no longer re-tones the scene darker, so the
    # +0.10 stop that was propping up a near-black facade now overexposes a
    # correct one: the whole frame measured median L=146 against the painting's
    # 56. Back off, and put the building on a MID ground instead of a cream one
    # -- a bright plaster floor filling the bottom third bounced the value
    # structure flat and left the stone base with nothing to sit against.
    # CONTRAST, measured. fantasy_inn.jpg runs median L=47 with a p95 of 190:
    # a dark picture with a few blazing sunlit faces. Round 5's first pass
    # measured median 97 and p95 151 -- our lit plaster was barely brighter than
    # our shaded stone, which is the definition of a flat render, and no palette
    # or surface field can fix it because the fault is in the RATIO of sun to
    # ambient. So the sky fill comes down by two thirds and the sun goes up by
    # two thirds: the shaded side falls into real shadow and the lit side clips
    # toward the painting's highlights. AgX handles the top end.
    # HIGHLIGHTS. With the ambient down and the sun raked, p05 finally matched
    # (14 against the painting's 15) but p95 stopped at 119 where
    # fantasy_inn.jpg reaches 205: we had the darks and no lights, which is
    # still a flat picture. AgX compresses the top three stops hard, so the only
    # way to reach a painting's highlights is to put a LOT more light on the lit
    # faces and take the whole frame back down with exposure -- sun x2.5,
    # exposure -0.6 stops. The sunlit plaster and the sunlit shingle then sit
    # near the top of the transform where it rolls off, and everything the sun
    # does not reach falls away.
    # THE TRANSFORM, measured. Three blind critics judged this render against the
    # paintings and two picked the painting. Their headline was the same number:
    # "the roof measures 89 against sky 92 -- three levels apart, the top third of
    # the silhouette has no edge against the background", and "only 0.01% of pixels
    # exceed 230, so nothing reads as actually struck by sunlight". Both were true:
    # the shipped frame measured max 229 and 0.000% above 230.
    #
    # The cause was not the lights -- previous rounds had already pushed the sun to
    # 22 and then pulled exposure back to compensate, which is the two fighting each
    # other. It was AgX with look='None', whose soft S-curve rolls off long before
    # white. Sweeping transforms and looks against fantasy_inn.jpg (median 55,
    # p95 205, 2.18% above 230):
    #     AgX None        -0.72   p95 183   >230 0.33%   sky/roof gap 23.6
    #     AgX Punchy      -0.72   p95 160   >230 0.00%   gap 24.5
    #     AgX MedHighCon  -0.90   p95 185   >230 2.58%   gap 28.6
    #     AgX HighCon     -1.00   p95 189   >230 2.98%   gap 33.4   <-- this
    #     Khronos PBR     -0.40   p95 219   >230 2.96%   gap 39.3   (too hot)
    # High Contrast at -1.00 puts the median within 5 of the painting's, restores
    # the highlights, and widens the roof-against-sky separation by half again.
    # AgX BASE LOOK, not High Contrast. Measured on the hero frame against the
    # reference crop: High Contrast at exposure -0.72 put 19.9% of BUILDING pixels
    # below L=10 against the reference's 0.01% -- every stud, brace, bargeboard and
    # the whole west gable end reading as a black shape with no material in it --
    # and clipped 3.4% of the frame above L230 where the reference clips 0.045%.
    # Dropping it holds the mean (0.4241 -> 0.4271), halves the crushed blacks
    # (10.02% -> 5.33% of frame, 10.27% -> 7.67% on the shadowed gable crop) and
    # clips nothing. look_ref2 never called this and lands within 2 levels of ITS
    # own reference's p95, so the control was already in the repo.
    # To restore it: _set_look('High Contrast').
    _set_look('None')
    # Re-measured on the real pipeline once AgX was ACTUALLY being applied
    # (painting: median 55, p95 205, 2.18% over 230):
    #     High Contrast  -1.00  med 60  p95 158  >230 0.14%
    #     High Contrast  -0.72  med 70  p95 172  >230 1.62%   <-- this
    #     High Contrast  -0.40  med 84  p95 187  >230 3.04%
    #     None           -0.72  med 82  p95 158  >230 0.00%
    # -0.72 keeps the median nearest the painting while restoring highlights.
    # NOTE the spread (p95 - median) is ~100 at every exposure against the
    # painting's 150: the transform cannot manufacture contrast the scene does not
    # have. Closing the rest is a sun-to-ambient RATIO and albedo job, not a
    # tone-mapping one.
    bpy.context.scene.view_settings.exposure = -0.72
    # z=-0.02, NOT 0.0. assemble_inn pins the paving's TOP vertex to z=0 so props
    # stand on it, so a backdrop at 0.0 sits exactly in that plane and buries all 83
    # cobble patches -- two separate agents measured the ref1 hero as containing the
    # entire cobbled street with zero stones visible, and no geometry change could
    # fix it. Every other preset already uses -0.02.
    ground(color="stone_dark", z=-0.02, size=170)


def look_ref2():
    """Soft high light, flat grey void backdrop. Matches Inn.jpg -- which is a
    DARKER picture than it looks: its median value is L=114 and its roof L=71.
    Ambient dropped and the sun tightened so the eaves, the jetty and the
    dormer cheeks all carry a shadow instead of reading as flat paint."""
    # clear_stage FIRST. sun() and area() call bpy.data.lights.new on every
    # invocation and never remove the previous object, so lights ACCUMULATE:
    # a caller that set this look and then asked for sun(energy=0) got
    # "KeySun 22.0 W" sitting next to "KeySun.001 0.0 W", and its "sun off"
    # control render came back 56.5% bit-identical to the lit one. That voided
    # the control in three separate investigations on this project, including
    # one of mine that I reported to the user as evidence.
    clear_stage()
    engine(eevee=True, samples=96, res=(1500, 1060))
    world(top=(0.54, 0.54, 0.53), bottom=(0.40, 0.40, 0.39), strength=0.66)
    sun(energy=15.0, angle_deg=(53, 0, 30), softness=3.2, color=(1.0, 0.96, 0.90))
    # Fill down from 150: Inn.jpg's shadow side runs to L=27 at its 5th
    # percentile where ours stopped at 56, and a 22 m fill card is what was
    # lifting every eave soffit and every recess back to mid grey.
    area((16, -14, 16), energy=26, size=20, color=(0.90, 0.92, 0.95))
    # Inn.jpg is a HIGHER-key picture than it looks: stone L=126, plaster L=144,
    # roof L=93. Ours was landing 40 L under all three.
    # Inn.jpg: mean 106, p05 26, p95 183. Ours measured p05 51 and p95 160 -- the
    # whole frame living inside one stop and a half. Same fix as ref1: ambient
    # down, sun up, so the valleys and the eave soffits go dark and the lit
    # slopes come up.
    bpy.context.scene.view_settings.exposure = -0.58
    g = ground(color="stone", size=64)
    return g


def _building(objs):
    """The MASSING, without its yard.

    camera() frames a bbox DIAGONAL, so every barrel, cobble and fence panel
    placed outside the walls used to push the building further away and shrink
    it in frame -- laying a cobbled street in front of the door zoomed the whole
    inn out by a third. The hero cameras therefore frame the building and let
    the clutter fall where it falls, which is also what the paintings do: both
    crop straight through their foreground props.
    """
    keep = [o for o in objs if not o.name.startswith(("SM_Ground_", "SM_Prop_",
                                                      "SM_Sign_", "Ground"))]
    return keep or objs


def fit(cam, objs, target, fill=(0.94, 0.92), centre=(0.5, 0.5), iters=8):
    """Pull `cam` along its own view axis until `objs` FILL the frame, then
    shift the frame so the silhouette lands where `centre` says.

    camera() can only frame a bbox by its DIAGONAL, which is the radius of the
    sphere around it -- a safe bound and a poor composition: it left this inn on
    60 % of the frame width with a third of the picture empty, and it moved every
    time a barrel was added outside the walls. This measures where the mass
    actually projects and solves for the distance, so the crop is a decision
    rather than a side effect of the bbox.

    fill   fraction of frame width / height the silhouette should span
    centre where its middle sits, in normalised frame coords (0.5, 0.5 = middle)
    """
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    # PER-PIECE bounds, not the whole-scene bbox. The scene bbox's top face is
    # at ridge height across the WHOLE footprint and its corners are empty air
    # above the eaves, so fitting it frames a phantom box half again too big --
    # which is exactly how the first version of this managed to shrink the inn.
    # Each piece's own 8 corners is a tight hull and costs nothing.
    pts = [o.matrix_world @ Vector(c) for o in objs if o.type == 'MESH'
           for c in o.bound_box]
    if not pts:
        return cam
    tgt = Vector(target)
    ry = sc.render.resolution_y / sc.render.resolution_x
    for _ in range(iters):
        bpy.context.view_layer.update()
        co = [world_to_camera_view(sc, cam, p) for p in pts]
        xs = [c.x for c in co]; ys = [c.y for c in co]
        k = max((max(xs) - min(xs)) / fill[0], (max(ys) - min(ys)) / fill[1])
        if abs(k - 1.0) < 0.004:
            break
        cam.location = tgt + (cam.location - tgt) * k
    bpy.context.view_layer.update()
    co = [world_to_camera_view(sc, cam, p) for p in pts]
    xs = [c.x for c in co]; ys = [c.y for c in co]
    cam.data.shift_x += (max(xs) + min(xs)) / 2 - centre[0]
    cam.data.shift_y += ((max(ys) + min(ys)) / 2 - centre[1]) * ry
    bpy.context.view_layer.update()
    return cam


def hero_ref1(objs, out):
    """Low street view. The inn's hero gable faces -Y and its long range runs
    +X, so the camera has to sit FRONT-LEFT (-X,-Y) to get the paintings'
    viewpoint: big gable centre frame, range receding to the right.

    ref1 is shot from about eye height, looking very slightly UP, with a lens
    shift keeping the ridge in frame -- the way the painting does it. Framing
    on the bbox centre put the camera 10 m in the air, which is exactly what
    made round 1's massing read as a model on a table."""
    look_ref1()
    build = _building(objs)
    lo, hi = bbox_of(build)
    ctr = (lo + hi) / 2
    # FRAMING. Round 3 put the building on 62 % of the frame width and 78 % of
    # its height, with empty sky above and empty ground below; the painting
    # CROPS its inn at the top and both sides. camera() frames the bbox
    # DIAGONAL, which for a 20.7 x 14.2 x 14.3 m mass is 28.6 m -- so a margin
    # of 1.0 leaves a third of the frame empty before anything is composed. A
    # small building in a big frame is the single loudest "this is a model on a
    # table" signal there is, so the margin does the zooming the painting does.
    # The numbers are derived, not hunted: at 34 mm the frame's half height is
    # 0.2978*dist, so 16 m of content (a 14.25 m ridge plus a metre of street)
    # needs dist 26.9 m, i.e. margin 0.95 against camera()'s 28.6 m bbox
    # diagonal. The camera stays at eye height (target z 2.5, axis level, so
    # verticals stay vertical) and a shift_y of 0.17 sensor widths lifts the
    # frame the 4.6 m needed to put the street at the bottom edge and the ridge
    # just under the top -- which is how the painting is cropped.
    # Eye height, level axis (so verticals stay vertical), and the crop the
    # painting uses: the inn across 96 % of the frame width, its base a little
    # below centre so the street shows and the ridge nearly touches the top.
    tgt = Vector((ctr.x, ctr.y, 2.5))
    cam = camera(objs, yaw=-36, pitch=90, lens=34, margin=1.0, target=tgt)
    fit(cam, build, tgt, fill=(0.98, 0.95), centre=(0.50, 0.52))
    save(out)


def hero_ref2(objs, out):
    """Elevated 3/4, long lens -- Inn.jpg's viewpoint, ~20 deg above the
    horizon rather than the 26 of round 1, which flattened the roof pitch."""
    look_ref2()
    build = _building(objs)
    lo, hi = bbox_of(build)
    tgt = (lo + hi) / 2
    cam = camera(build, yaw=-43, pitch=71, lens=85, margin=1.0, target=tgt)
    fit(cam, build, tgt, fill=(0.95, 0.93), centre=(0.50, 0.50))
    save(out)


# ----------------------------------------------------------------- lineups ---
def lineup(objs, gap=0.5, axis='X'):
    """Space objects out in a row so nothing overlaps. Returns them."""
    cur = 0.0
    for o in objs:
        lo, hi = bbox_of([o])
        w = (hi - lo)[0 if axis == 'X' else 1]
        o.location[0 if axis == 'X' else 1] += cur - lo[0 if axis == 'X' else 1]
        cur += w + gap
    # recentre the row on the origin
    lo, hi = bbox_of(objs)
    mid = (lo + hi) / 2
    for o in objs:
        o.location.x -= mid.x
        o.location.y -= mid.y
    return objs


def tile_copies(ob, n=3, step=None, axis='X'):
    """Linked copies at exact grid spacing -- the visual proof that a wall
    piece tiles with no gap and no seam."""
    step = S.GRID if step is None else step
    out = [ob]
    for i in range(1, n):
        c = ob.copy()
        c.data = ob.data
        bpy.context.scene.collection.objects.link(c)
        c.location[0 if axis == 'X' else 1] += step * i
        out.append(c)
    return out


def save(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDERED", path)
    return path


def clear_stage():
    """Remove lights/camera/ground so a second look_*() can be set up cleanly."""
    for o in list(bpy.data.objects):
        if o.type in ('LIGHT', 'CAMERA') or o.name.startswith("Ground"):
            bpy.data.objects.remove(o, do_unlink=True)
