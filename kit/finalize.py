"""Make the kit texturable, and hand it over cleanly.

Called by build_kit.py / assemble_inn.py / kit_sheet.py -- never by a piece module.

Two UV sets go on every piece, because the two things you might want to do are
different jobs:

  "UVMap"    world-scale box projection: 1 UV unit = 1 metre. This is the one you
             want for TILING textures (planks, plaster, rubble, shingle). Islands
             overlap on purpose -- a 2 m wall gets two repeats of a 1 m wood tile,
             and texel density is identical on every piece in the kit, which is
             exactly what stops a kit looking like it was made by 13 people.

  "UVPacked" smart-projected and packed into 0-1 with no overlap. This is the one
             you want for BAKING, hand-painting, lightmaps or atlasing.

Materials also get a texture slot wired in and switched off (Mix factor 0), so
"texture this kit" is: load an image, set the factor to 1. No re-wiring.
"""
import bpy
from math import radians
from . import spec as S


# -------------------------------------------------------------------- UVs -----
def uv_object(ob, cube_size=1.0, packed=True):
    """Give one mesh object both UV sets. Safe to call twice."""
    if ob.type != 'MESH' or not ob.data.polygons:
        return False
    me = ob.data
    for name in ("UVMap", "UVPacked"):
        if name not in [l.name for l in me.uv_layers]:
            me.uv_layers.new(name=name)
    prev_mode = bpy.context.mode
    prev_active = bpy.context.view_layer.objects.active
    for o in list(bpy.context.selected_objects):
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    try:
        # 1. world-scale box projection for tiling textures
        me.uv_layers.active = me.uv_layers["UVMap"]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.cube_project(cube_size=cube_size, correct_aspect=True,
                                scale_to_bounds=False)
        # 2. packed non-overlapping set for baking / painting
        if packed:
            bpy.ops.object.mode_set(mode='OBJECT')
            me.uv_layers.active = me.uv_layers["UVPacked"]
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project(angle_limit=radians(66), island_margin=0.006,
                                     correct_aspect=True, scale_to_bounds=True)
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception as e:
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass
        print(f"UV FAIL {ob.name}: {e}")
        return False
    finally:
        me.uv_layers.active = me.uv_layers["UVMap"]      # tiling set is the default
        ob.select_set(False)
        bpy.context.view_layer.objects.active = prev_active
    return True


def uv_all(objs=None, cube_size=1.0, packed=True):
    objs = objs or [o for o in bpy.data.objects if o.type == 'MESH']
    ok = sum(1 for o in objs if uv_object(o, cube_size, packed))
    print(f"UV {ok}/{len(objs)} objects unwrapped (UVMap world-scale + UVPacked 0-1)")
    return ok


# ----------------------------------------------------------- texture slots ----
def texturize_material(m, uv_name="UVMap"):
    """Wire a switched-off texture slot into a kit material.

    The palette colour x vertex-colour chain stays exactly as it was. An Image
    Texture feeds the B side of a Mix whose factor is 0, so nothing changes until
    you load an image and raise the factor. Named nodes so it is obvious:
      TEX_image / TEX_uv / TEX_mix
    """
    if not m or not m.use_nodes:
        return False
    nt = m.node_tree
    if nt.nodes.get("TEX_mix"):
        return True                     # already done
    bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bsdf:
        return False
    base_in = bsdf.inputs.get("Base Color")
    src = base_in.links[0].from_socket if base_in.links else None
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.name = tex.label = "TEX_image"
    tex.location = (-420, -300)
    uvn = nt.nodes.new("ShaderNodeUVMap"); uvn.name = uvn.label = "TEX_uv"
    uvn.location = (-640, -300); uvn.uv_map = uv_name
    nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix"); mix.name = mix.label = "TEX_mix"
    mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.location = (10, -120)
    mix.inputs[0].default_value = 0.0            # <-- off until you load an image
    if src:
        nt.links.new(src, mix.inputs[6])
    else:
        mix.inputs[6].default_value = tuple(base_in.default_value)
    nt.links.new(tex.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], base_in)
    fr = nt.nodes.new("NodeFrame")
    fr.label = "TEXTURE SLOT — load an image into TEX_image, set TEX_mix factor to 1"
    for n in (tex, uvn, mix):
        n.parent = fr
    return True


def texturize_all(uv_name="UVMap"):
    n = sum(1 for m in bpy.data.materials if texturize_material(m, uv_name))
    print(f"TEXTURE SLOTS added to {n} materials (off by default)")
    return n


def finalize(objs=None, cube_size=1.0, packed=True, textures=True, tone=0.65,
             use_bundled_textures=True):
    """Everything a hand-off needs. Call right before saving/exporting."""
    if tone:
        harmonize(objs, strength=tone)
    uv_all(objs, cube_size, packed)
    if textures:
        texturize_all()
        if use_bundled_textures:
            apply_textures()


# ---------------------------------------------------------- harmonisation -----
def harmonize(objs=None, strength=0.65, report=True):
    """Pull every piece's vertex-colour tone toward the kit-wide mean FOR THAT
    MATERIAL, so thirteen families stop disagreeing about how dark oak is.

    Thirteen agents built thirteen families and each picked its own vertex-colour
    `shade` values -- some ran to 1.7, some sat under 0.8. Same material, wildly
    different apparent tone, which is instantly obvious once two families sit on
    the same building. This measures the actual mean per material across the whole
    kit and scales each piece toward it.

    strength 0 = leave alone, 1 = force every piece to the mean. 0.65 keeps local
    stone-to-stone and shingle-to-shingle variation while killing the family-level
    drift, which is the part that reads as a mistake.
    """
    objs = objs or [o for o in bpy.data.objects if o.type == 'MESH']
    # 1. per (material, object) mean of the loop colours
    sums = {}      # mat_name -> [total, count]
    per = {}       # (obj, mat_name) -> [total, count]
    for ob in objs:
        me = ob.data
        ca = me.color_attributes.get("Col")
        if not ca or ca.domain != 'CORNER':
            continue
        mats = [m.name if m else "" for m in me.materials]
        for poly in me.polygons:
            mn = mats[poly.material_index] if poly.material_index < len(mats) else ""
            if not mn:
                continue
            for li in poly.loop_indices:
                c = ca.data[li].color
                v = (c[0] + c[1] + c[2]) / 3.0
                s = sums.setdefault(mn, [0.0, 0])
                s[0] += v; s[1] += 1
                k = per.setdefault((ob.name, mn), [0.0, 0])
                k[0] += v; k[1] += 1
    if not sums:
        return 0
    target = {m: (t / n) for m, (t, n) in sums.items() if n}
    # 2. scale each piece's loops for that material toward the kit-wide mean
    moved = []
    for ob in objs:
        me = ob.data
        ca = me.color_attributes.get("Col")
        if not ca or ca.domain != 'CORNER':
            continue
        mats = [m.name if m else "" for m in me.materials]
        factors = {}
        for mn in set(mats):
            if not mn or mn not in target:
                continue
            k = per.get((ob.name, mn))
            if not k or not k[1] or k[0] <= 1e-6:
                continue
            own = k[0] / k[1]
            f = 1.0 + strength * ((target[mn] / own) - 1.0)
            f = max(0.55, min(1.8, f))
            factors[mn] = f
            if abs(f - 1.0) > 0.06:
                moved.append((ob.name, mn, round(f, 2)))
        if not factors:
            continue
        for poly in me.polygons:
            mn = mats[poly.material_index] if poly.material_index < len(mats) else ""
            f = factors.get(mn)
            if not f or abs(f - 1.0) < 1e-4:
                continue
            for li in poly.loop_indices:
                c = ca.data[li].color
                ca.data[li].color = (min(c[0] * f, 4.0), min(c[1] * f, 4.0),
                                     min(c[2] * f, 4.0), c[3])
    if report:
        print(f"HARMONIZE adjusted {len(moved)} piece/material pairs "
              f"(strength {strength})")
        for row in sorted(moved, key=lambda r: -abs(r[2] - 1.0))[:12]:
            print(f"   {row[0]:34s} {row[1]:16s} x{row[2]}")
    return len(moved)


# ------------------------------------------------------- default texturing ----
# Which bundled texture goes on which material, and how strongly. Grain goes on
# things already MODELLED as separate pieces (stones, timbers); cell patterns are
# reserved for flat surfaces, or you get two competing stone patterns.
# Strength is the TEX_mix factor. Plaster gets the most because a critic measured
# our plaster panels at a luminance sd of 2 across 19% of the facade -- a blank
# card -- against 25-35 in the reference.
TEXTURE_DEFAULTS = {
    "plaster":      ("plaster",     0.55),
    "plaster_dim":  ("plaster",     0.55),
    "stone":        ("stone_grain", 0.45),
    "stone_dark":   ("stone_grain", 0.40),
    "stone_pale":   ("stone_grain", 0.45),
    "stone_warm":   ("stone_grain", 0.45),
    "oak_dark":     ("wood_grain",  0.40),
    "oak_mid":      ("wood_grain",  0.40),
    "oak_pale":     ("wood_grain",  0.35),
    "shingle":      ("shingle",     0.45),
    "shingle_moss": ("shingle",     0.45),
    "thatch":       ("wood_planks", 0.45),
}


def apply_textures(tex_dir=None, table=None, enable=True):
    """Load the bundled tiling textures into the slots texturize_all() wired up,
    and switch them on. The kit then ships WITH surface variation instead of
    shipping the ability to add some later; a viewer can still zero TEX_mix.
    Images are packed into the .glb by the exporter, so this travels."""
    import os as _os
    tex_dir = tex_dir or _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "textures")
    table = table or TEXTURE_DEFAULTS
    loaded, applied = {}, 0
    for mat_key, (tex_name, strength) in table.items():
        m = bpy.data.materials.get("M_" + mat_key)
        if not m or not m.use_nodes:
            continue
        node = m.node_tree.nodes.get("TEX_image")
        mix = m.node_tree.nodes.get("TEX_mix")
        if not node or not mix:
            continue
        path = _os.path.join(tex_dir, tex_name + ".png")
        if not _os.path.exists(path):
            print(f"  texture missing: {path}")
            continue
        if tex_name not in loaded:
            loaded[tex_name] = bpy.data.images.load(path, check_existing=True)
        node.image = loaded[tex_name]
        mix.inputs[0].default_value = strength if enable else 0.0
        applied += 1
    print(f"TEXTURES applied to {applied} materials from {len(loaded)} images")
    return applied
