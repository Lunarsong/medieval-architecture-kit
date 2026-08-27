"""Dormers -- the run of little gabled boxes along ref2's roof, plus the shed
dormer that sits mid-slope on its left wing, plus the cheek/flashing bits that
tuck either of them into a 52 degree roof.

WHAT WAS MEASURED OFF THE REFERENCE (Inn.jpg, dormer run + the lone shed
dormer on the left wing, both cropped at 5x):

* The gabled dormers are WALL dormers, and -- this is the whole point -- they
  are BOXES, not gables painted on a roof. Measured off ref3 the box projects
  about one window-width in front of the wall/roof plane behind it
  (Y_WALL = 0.68), so every one has deep vertical-boarded CHEEKS down each
  side, its own two-plane shingled roof standing 0.16 proud of the face on the
  rake, a corbelled/canted soffit under the sill and diagonal braces under it.
  One piece = ONE 2m BAY of the top storey: the projecting dormer box in the
  middle, a RECESSED plaster panel each side of it (set back the full 0.68 --
  that recess is what makes the box read), and the boxed jetty along the
  bottom. Drop three in a row at GRID spacing and you get the reference run.
* Dormer gables are much steeper than the main roof: measured 61-67 deg off the
  bargeboards, against 52 for the field. DORMER_PITCH = 61. They only ever meet
  the main roof in a valley, which this family builds itself, so nothing in the
  kit has to bend to it.
* Measured off the greyscale linework (ref3, the clearest form reference):
  face 110px wide by 205px tall, window opening 90px tall, gable span 190px,
  gable rise 165px, dormer spacing 195px. Scaled on the 0.78 opening that is
  face 0.95 x 1.78, span 1.73x the face width, spacing ~1.7. So: a NARROW tall
  face (window nearly fills it), a HUGE bargeboard overhang that all but closes
  the gap to the next dormer at GRID spacing, and 60-61 deg rakes.
* Bargeboard is a WIDE flat plank (0.19 across the face, 0.07 thick) whose
  outer edge is the roof edge, and it overhangs the box by 0.28-0.32 each side.
  Its lower edge is SCALLOPED with a run of pendant lobes the whole way up
  (ref3 draws them plainly), its foot kicks out and down, and a second thinner
  verge plank is tucked behind it.
* Tooth trim: a dentil course under the head beam, running BETWEEN the corner
  posts (not out over the cheeks), and a canted corbel under each projecting end
  of the head beam. The corbel used to be an arched bracket, but there is nothing
  outboard of the box for an arch to span to, so it bulged out past the cheek and
  crossed the post -- see the note where it is built.
* The dentil course and the carved window crest are ALTERNATIVES per variant:
  there are only 170 mm between the window head and the head beam, and the two of
  them plus the head casing cannot share it without standing inside each other.
* Gable infill is VERTICAL boarding, nearly black in shadow, with a pierced
  trefoil/quatrefoil right under the apex. Variant C swaps it for a plaster
  tympanum with timber framing, which is how ref1 does its gables.
* Face bands, bottom up (measured off ref3 at 0.0052 m/px): box soffit 0.055,
  floor beam 0.13, plank apron 0.24, chunky sill beam with peg ends 0.13,
  window (frame casing lapping the plaster panel each side of it), crest or
  dentil course on the window head, head beam 0.20. The window sill
  lands at 0.55 = OPENINGS.win_dormer["sill"]. Under the soffit the box is
  jettied out over the wall behind, so its underside is canted and ribbed.
* The shed dormer (left wing, ref2) is squat: face a bit wider than it is tall,
  single window with bright cream reveals, one shallow ~22 deg roof with a big
  overhang all round, upturned fascia ends, three peg dowels showing under the
  sill plank, and deep dark vertical-boarded cheeks. NO SHINGLE ON ITS FACE: the
  assembler sinks it so the roof surface crosses its front plane at Z_ROOF_SHED,
  and the slope falls AWAY in front of that, so everything above 0.30 on the
  front face is in plain view -- roofing put there reads as shingles stuck on the
  wall beside the window.
  NO SOAKERS ALONG ITS CHEEKS EITHER, for the same reason: a soaker laps the main
  roof field, and on this piece the field is 0.9 m outboard of the box and not
  part of the piece, so eight of them climbed the outside of the face past the
  window with nothing under them. SM_Dormer_Flash_Valley is the piece that
  dresses that junction. (Verified this round by measurement, not by reading the
  code: the only shingle_moss left on the shed piece runs z 1.476-2.252, which is
  its roof, 146 mm above the window head. Nothing shingled comes near the window.)

* THE CHEEK BOARDING LAPS THE CHEEK SLAB -- it does not butt it. On both the
  gabled and the shed dormer the slab's outer face is on x = hf and the boarding
  used to START outboard of it, so a 12-14 mm SLOT ran the full height of the
  box's corner beside the window. That is "a gap between the plaster and the
  brickwork making it show roof in-between": on the gabled dormer a front-on ray
  cast into it hit the recessed backing 0.72 m behind; on the shed, which has no
  recessed panel behind it, it hit NOTHING -- 283 cm2 of hole clean through the
  piece, which on an assembled roof shows the main roof field. Both boards are now
  cut thicker on their INBOARD side so they overlap the slab by 20 mm, with the
  outer faces unmoved (the relief reads the same and SM_Dormer_Cheek_Board still
  lands on the shed's) and the new inner faces landing on no existing plane. An
  overlap cannot open a slot; a butt joint always can. The shed's boards are also
  prisms cut on the field and the shed plane rather than upright boxes taking one
  height for their whole run -- as boxes their bottoms stopped 0.34 m above the
  roof line at the front of the piece and their tops stood 84 mm up through its
  own shingles.

PLACEMENT (this family's convention, built on the wall-family one)
    origin (0,0,0) = front face, centre of the bay, base of the piece.
    X in [-GRID/2, GRID/2]   -> tiles along X at exactly GRID.
    Y: front face of the BOX on Y=0, body runs +Y into the roof; the barge /
       roof rake edge stands proud to -0.148 (PROUD_MAX is 0.16 and
       Part.finish() silently CLAMPS anything past it -- never exceed -0.155).
       The SHED dormer declares proud=0.30 instead, because its eaves overhang
       all round is 0.20 plus a 35 mm starter-course drip, and inside 0.16 there
       was no overhang left at all -- the roof edge fell behind its own head
       beam. spec.py provides for exactly that, and nothing in the kit abuts a
       roof dormer's front: it is planted mid-slope with clear roof below it.
    Z in [0, apex].
    Z_ROOF (a module constant) is the height at which the 52 deg main-roof
    surface crosses the RECESSED WALL PLANE of the piece:
        gabled dormers  Z_ROOF = 1.70 at Y = Y_WALL = 0.68.  The box stands
                        0.68 in FRONT of that plane, so a bay of top-storey
                        wall butts the flanking panels at Y_WALL, and the main
                        roof field starts there:  z = Z_ROOF + (y-Y_WALL)*tan52
        shed dormer     Z_ROOF = 0.30 at Y = 0  (roof dormer: plant it anywhere
                        on a slope, bottom 0.30 buried/flashed)
    Line that up with the roof and the valleys, cheeks and flashing all close.

Openings are OPENINGS["win_dormer"] exactly (0.62 x 0.78, sill 0.55, flat), and
the frame and the pane are util.Part.glazing() -- NOT hand-rolled here. See the
WIN_* block above _window(): the primitive cuts the pane oversize and laps it,
and oversails the plaster instead of butting it, which is the three-fault fork
five families each grew their own copy of. A lit pane sits at the BACK of the
reveal so the piece reads on its own.

THE DIAMOND LEADING IS THE ONE EXCEPTION, and only since this round's
measurement. The primitive strikes both diagonal families of bars at ONE
standoff, so every crossing is two 27 mm bars overlapping in plan with their
front faces in one plane and their back faces in another. Ray-sampled, that was
ALL 78 cm2 of this family's reachable coincidence -- 36 pairs, 140 cm2, dead
centre of the window -- while the 341 cm2 the area gate reports is frame
joinery buried inside solid timber and 0.0 % reachable. So _leading() strikes
the two families 12 mm apart, reproducing the primitive's clip-to-glass-rect
rule verbatim so the diamonds still meet the edge. The proper fix is in
util.Part.glazing(), which five families call; this is the piece-local one.

Flowers, moss and creeper are deliberately absent -- props' job, per the brief.
demo() adds a little context roof/wall/window scaffolding named CTX_* so the
arrangement reads as a building; those are NOT kit pieces and build() never
returns them.
"""
import bpy
from math import radians, tan, cos, sin, hypot, atan2, pi
from mathutils import Matrix, Vector
from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "dormers"
COLLECTION = "06_Dormers"

G = S.GRID
HB = G / 2.0

# main roof, and this family's own steeper gable
TAN_R = S.SIN_P / S.COS_P                      # 52 deg field pitch
DORMER_PITCH = radians(61.0)
COS_D, SIN_D, TAN_D = cos(DORMER_PITCH), sin(DORMER_PITCH), tan(DORMER_PITCH)
SHED_PITCH = radians(22.0)
TAN_S = tan(SHED_PITCH)

Z_ROOF = 1.70          # gabled dormers: main roof crosses Y=0 here
Z_ROOF_SHED = 0.30     # shed dormer: ditto

# horizontal bands of the face (metres above the piece base)
Z_SOF = 0.055          # underside of the projecting box at its front face
Z_RAIL = 0.185         # top of the box floor beam
Z_APRON = 0.42         # plank apron top
OP = S.OPENINGS["win_dormer"]
Z_SILL = OP["sill"]                  # 0.55  sill beam top / opening sill
Z_HEAD = Z_SILL + OP["h"]            # 1.33  opening head
Z_CREST = Z_HEAD + 0.17              # 1.50  top of the carved crest
OW = OP["w"]

# depths. front face on Y=0, trim proud to Y_TRIM (PROUD_MAX = 0.16, and
# util.Part.finish() CLAMPS anything past it -- do not exceed -0.155)
Y_BARGE = -0.150       # outer face of the bargeboard / roof rake edge
Y_TRIM = -0.100        # head beam / sill / floor beam fronts
Y_POST = -0.088        # corner posts. THE POST HAS TO STAND PROUD OF THE ARCHED
                       # BRACES: what hides the end of a housed brace is the
                       # timber of the member it dies into, and at -0.070 the
                       # braces stood 48 mm in FRONT of the post, so their ends
                       # crossed it and came out the other side.
Y_FACE = 0.020         # plaster face (slightly recessed behind the frame)
Y_BACK = 0.20          # back of the dormer box front panel
Y_WALL = 0.68          # THE RECESS: wall + main-roof plane behind the box.
                       # One window-width, so the box is a box.
Y_FLANK = Y_WALL       # recessed flanking panel face
Y_FLANK_B = Y_WALL + 0.26
CHEEK_T = 0.055        # cheek board thickness

MOSS = "shingle_moss"

# ===========================================================================
# SHINGLE COURSES -- A DORMER ROOF AND THE MAIN ROOF IT SITS IN ARE THE SAME
# MATERIAL, so this is roofs.py's course treatment, at roofs.py's numbers.
# ---------------------------------------------------------------------------
# An integrator called these roofs "flat dark plates", and they were, for one
# reason: the tabs lay FLAT on the boarding. A course lapped the one below it at
# the same height, so its butt was buried inside the course under it, there was
# no step to catch light or throw a shadow, and the two lapping surfaces were
# coplanar over the whole lap (which was also a third of this family's measured
# z-fighting -- 100 cm2 of it on the sunlit face of the roof).
#
# So, exactly as roofs.py does it:
#   * EVERY TAB IS TILTED about the course axis by atan(RELIEF/gauge), so its
#     butt end rides RELIEF out of the course below and its head end lies back
#     down on the boarding. The step at every butt line is RELIEF, nothing
#     accumulates up the rake, and it costs no tris at all.
#   * THE STEP IS ALSO PAINTED, in the direction the light falls: lit along the
#     proud butt edge, dark in the crevice under the course above, with one
#     extra edge loop across the tab so the dark band lands inside the strip you
#     can actually see. A 38 mm riser is 1-2 px on a building seen whole and it
#     faces DOWN-slope; the painted band is what reads at any distance.
#   * PER-TAB TILT AND YAW, so no two tabs in a field share a plane.
#   * REAL SLOTS between the tabs in a course (GAP), so the vertical joint reads
#     too -- ref3's shingles are separated on all four sides.
#   * ONE MATERIAL. Moss is a tone: age is per-course and per-blotch VALUE, not
#     a green tab dropped in at 1.5 %, which reads as confetti (brief, and the
#     same call roofs.py made).
#
# GAUGE. Wall dormers are NOT stretched by assemble_inn (their flanking panels
# are vertical wall, so the roof-world Z stretch never touches them), while the
# main roof is: roofs.py authors ROW 0.125 and the stretch takes it to a 0.183
# gauge with a 0.165 rise and a 42 mm step. This family therefore authors the
# FINISHED numbers, and they have to satisfy both the brief's 6-8 courses per
# metre AS AUTHORED and the main roof's assembled rhythm:
#     ROW 0.165 -> 6.1 courses per metre of rake, rise 0.144 (7.0 per vertical
#                  metre) against the main roof's assembled 0.165. Inside the
#                  brief at both ends, and within 10 % of the roof it abuts.
#     TAB 0.1429 -> roofs.py's tab, to the millimetre. X is never stretched in
#                  either family, so this is the one shingle dimension that is
#                  DIRECTLY comparable on the finished building -- and at 0.180
#                  it was the mismatch you could see: the dormer's tabs were
#                  1.09x their own gauge where the main roof's are 0.78x its
#                  assembled gauge, so a dormer roof read as long slabs sitting
#                  in a field of fine courses. Same tab width, same lap, same
#                  painted ramp, same per-tab tilt: same material.
#     RELIEF 0.040 -> inside the 30-40 mm the critics asked for, and within 2 mm
#                  of the main roof's assembled 42 mm step.
ROW = 0.165            # course depth (the GAUGE) along this roof's own rake
TAB = G / 14.0         # 0.1429 -- ROOFS.PY'S TAB WIDTH, EXACTLY. X is never
                       # stretched by the assembler in either family, so this
                       # number is directly comparable on the finished building,
                       # and it was the mismatch you could actually see: the
                       # dormer used to run 0.180 against the main roof's 0.1429,
                       # so its tabs were 26 % wider than the field they sit in
                       # and read as long slabs beside a fine-coursed roof.
OV = 1.45              # shingle length / gauge, i.e. the lap. Sets how far a
                       # tab reaches past the next course's butt; the TILT is
                       # RELIEF/gauge and is what makes the step.
THICK = 0.042          # tab thickness. MUST be >= RELIEF or the butt step opens
                       # a gap you can see the boarding through.
RELIEF = 0.040         # <<< THE COURSE STEP: how far each course's butt rides
                       # out of the course below. roofs.py authors 0.032 and the
                       # assembler stretches it to a 0.042 step; 0.040 lands
                       # between, and inside the 30-40 mm the critics asked for.
GAP = 0.007            # the slot between tabs in a course
LIFT = OV * RELIEF * .5   # 0.0276 -- butt underside above the boarding. The
                       # tilt is centred on the boarding plane, so the MEAN roof
                       # surface stays where the cheeks and valleys expect it;
                       # only the butts stand higher.
BUILD = LIFT + THICK   # outer face of a course butt above the boarding --
                       # everything that laps the field (ridge, valley) sits off
                       # this number, so it follows RELIEF if RELIEF changes.
SLAB_T = 0.045         # boarding under the shingles
STAG = (0.00, 0.50, 0.25, 0.75)   # 4-phase stagger. A half-tab alternation
                       # makes a two-course checkerboard cell, and that cell,
                       # not the tab, is what reads as a toy roof.
# The painted relief. Same ramp as roofs.py: display gamma flattens albedo
# ratios by about the 1/2.2 power, so a 3:1 painted ramp lands as roughly 1.6:1
# on screen, which is what the reference roof measures.
SH_BUTT = 1.26         # multiplier at the proud, lit butt edge
SH_BAND = 0.42         # at the band line: the course shadow
SH_HEAD = 0.16         # at the head, buried under the lap
SH_BAND_AT = 0.58      # where the band sits along the tab (exposure = 1/OV)
SH_RISER = 0.20        # the butt riser itself: the darkest line on a roof
SH_ROLL = 0.095        # ACROSS the tab: a touch lighter on one side than the
                       # other, in alternating directions, like a split shake
                       # that has cupped. It puts a value step at every vertical
                       # joint, which is how the reference's shingles read as
                       # separate shingles without a dark outline all round.
QA, QB = 1.37, 4.11    # blotch phases, FIXED (not from the piece's own rng) so
                       # the weathering pattern is continuous between two
                       # different dormer variants standing side by side.

# ===========================================================================
# NO TWO OPAQUE FACES IN A PIECE MAY SHARE A PLANE.
# ---------------------------------------------------------------------------
# That is what Shanee's "a lot of z-fighting on the inside/backside" is: two
# coplanar overlapping faces, which the renderer cannot order, so it flickers.
# In this family it came from layers that ABUTTED -- the recessed panel's dark
# backing started exactly on the back face of the plaster skim in front of it
# (4400 cm2 of coincident wall per dormer, the worst single offender in the
# kit after the walls), the box back landed on the soffit's back plane, the
# front backing plates shared the beams' z planes, and the cheek boarding, the
# corner post and the cheek slab all had a face on x = +/-hf.
#
# THE RULE: two solids that overlap in plan either INTERPENETRATE by >= 12 mm
# or clear each other by >= 12 mm. Never abut. check_zfight.py buckets planes
# 2.5 mm apart together and wobble() is coherent (neighbours move together), so
# 12 mm survives both -- 20 mm on long faces, which wobble blurs more.
#
# Re-measure after touching any of it:
#   blender -b --python check_zfight.py -- dormers
# ===========================================================================
ZF = 0.014             # the standard clearance used throughout this module


class _Part(Part):
    """util.Part with one local repair.

    util.Part._emit bevels a primitive and then keeps `[f for f in fs if
    f.is_valid]` -- but bmesh.ops.bevel INVALIDATES the six original faces of a
    box and returns replacements in res["faces"] only partially, so a beveled
    primitive loses its six big flat faces from the paint list. They keep
    material_index 0 and the vertex colour of whatever they interpolated from,
    i.e. every beveled timber in the kit renders in the piece's first material.
    That is a shared-library bug (see `needs`); until it is fixed there, tag
    every face as it is created and paint anything still untagged.
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._tag = self.bm.faces.layers.int.new("_pt")

    def _emit(self, verts, faces_idx, mat, tint, bevel, seg, shade=1.0):
        fs = super()._emit(verts, faces_idx, mat, tint, bevel, seg, shade)
        new = [f for f in self.bm.faces if f[self._tag] == 0]
        for f in new:
            f[self._tag] = 1
        return self._paint(new, mat, tint, shade) if new else fs

    def sub(self, name=None):
        return _Part(name or (self.name + "_sub"), smooth=self.smooth)

    def finish(self, *a, **kw):
        self.bm.faces.layers.int.remove(self._tag)
        return super().finish(*a, **kw)

    def tab(self, center, size, mat, rot=None, tint=.07, taper=.94, shade=1.0,
            skew=(0, 0), head=False, butt=SH_RISER,
            grad=(SH_BUTT, SH_BAND, SH_HEAD), roll=0.0):
        """ONE SHINGLE TAB, 10 tris. Local frame is the surface frame: X along
        the course, Y up the slope, Z out of the roof.

        Two of a box's six quads can never be seen on a shingle -- the one lying
        on the boarding, and (in every course but the last) the head under the
        next course's lap -- so they are left out: 8 tris instead of 12. Leaving
        the base out also means a tab sitting on the boarding has no face
        coplanar with it. The band loop across the outer face (see SH_BAND_AT)
        puts it back to 10, and that is the cheapest two tris in the piece: it
        is what turns the painted course relief from a soft ramp into a dark
        BAND with an edge, tight under every course.

        The tab is placed tilted (see _field): its butt end rides RELIEF out of
        the course below. The same relief is PAINTED along the tab -- lit at the
        proud butt edge, dark where it disappears under the course above, with
        the riser itself darkest -- because a 38 mm step is one or two pixels on
        a building seen whole and it faces down-slope, away from any camera
        looking at the roof.

        This mirrors roofs.py's tab so the two roofs match; the two families are
        edited independently, so it is duplicated rather than imported.
        """
        sx, sy, sz = size[0] / 2, size[1] / 2, size[2] / 2
        ty = sy * taper
        kx, ky = skew
        vs = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
              (-sx + kx, -ty + ky, sz), (sx + kx, -ty + ky, sz),
              (sx + kx, ty + ky, sz), (-sx + kx, ty + ky, sz)]
        yb = lerp(-ty + ky, ty + ky, SH_BAND_AT)     # the band loop
        vs += [(-sx + kx, yb, sz), (sx + kx, yb, sz)]
        M = rot if isinstance(rot, Matrix) else Matrix.Identity(4)
        vs = [tuple(M @ Vector(v) + Vector(center)) for v in vs]
        F = [(7, 6, 9, 8), (8, 9, 5, 4),      # outer face, split at the band
             (0, 4, 5, 1),                    # butt -- draws the course line
             (1, 5, 6, 2), (3, 7, 4, 0)]      # the two sides
        if head:
            F.append((2, 6, 7, 3))
        fs = self._emit(vs, F, mat, tint, 0, None, shade)
        if abs(sy) > 1e-6 and (butt < 1.0 or grad):
            # Work in the tab's own frame. Winding is not a reliable guide to
            # which face is the butt (finish() recalculates normals), so test
            # the axis of the normal and the side of the centroid.
            inv = M.inverted()
            inv3 = inv.to_3x3()
            ctr = Vector(center)
            grad = grad or (1.0, 1.0, 1.0)
            for f in fs:
                loc = [inv @ (l.vert.co - ctr) for l in f.loops]
                mid = sum(loc, Vector((0, 0, 0))) / len(loc)
                if butt < 1.0 and abs((inv3 @ f.normal).y) > 0.45 and mid.y < 0.0:
                    for l in f.loops:         # the riser: one dark line
                        c = l[self.clay]
                        l[self.clay] = (c[0] * butt, c[1] * butt, c[2] * butt, 1.0)
                    continue
                for l, v in zip(f.loops, loc):    # butt -> band -> head
                    m = _course_shade(clamp((v.y + sy) / (2.0 * sy)), *grad)
                    if roll:                      # ... and across the tab
                        m *= 1.0 + roll * clamp(v.x / sx, -1.0, 1.0)
                    c = l[self.clay]
                    l[self.clay] = (c[0] * m, c[1] * m, c[2] * m, 1.0)
        return fs


# --------------------------------------------------------------- helpers -----
def _basis(ex, ey):
    """Rotation matrix whose columns are ex, ey, ex x ey (all unit)."""
    ex = Vector(ex).normalized()
    ey = Vector(ey).normalized()
    return Matrix((ex, ey, ex.cross(ey))).transposed().to_4x4()


def _course_shade(t, g0=SH_BUTT, gb=SH_BAND, g1=SH_HEAD, fb=SH_BAND_AT):
    """Vertex-colour multiplier along a tab: t = 0 at the butt, 1 at the head."""
    if t <= fb:
        return lerp(g0, gb, t / fb)
    return lerp(gb, g1, (t - fb) / (1.0 - fb))


def _shmat(r, moss=0.0, warm=0.0):
    """THE FIELD IS ONE MATERIAL. moss and warm default to zero: a green or a
    warm-brown tab dropped through a shingle_moss field at 1-2 % reads as
    confetti, not as age, and the brief says so outright. Age is carried by the
    per-course and per-blotch VALUE drift in _field instead. (This family used to
    run moss at 1.5 % and warm at 2.2 %, and before that mat_alt="moss" at 13 %.)
    Non-zero moss is passed in exactly one place: the valley soakers, which is
    where the brief allows a few green shingles."""
    q = r.random()
    if moss and q < moss:
        return "moss"
    if warm and q < moss + warm:
        return "shingle"
    return MOSS


def _slab(p, org, ex, ey, poly, mat=MOSS, t=SLAB_T, tint=.04, shade=.88):
    """Roof boarding under the shingles, on the plane (org, ex, ey). `poly` is
    in (along ex, up ey) coordinates. Its top face is the plane the tabs sit
    on: SLAB_T/2 out along ex x ey."""
    return p.prism(poly, t, mat, axis='Z', at=org, rot=_basis(ex, ey), bevel=0,
                   tint=tint, shade=shade)


def _field(p, org, ex, ey, u0, u1_at, v0, v1, seed, row=ROW, tab=TAB,
           thick=THICK, relief=RELIEF, t0=SLAB_T / 2, moss=0.0, warm=0.0,
           phase=0.0, taper=.97, shade=1.0, wander=1.0, hang=0.035, gap=GAP,
           shade_var=.135, course_var=.150, clump=.130, curl=.055, tint=.090,
           mirror=False):
    """COURSED SHINGLE TABS on an arbitrary plane -- every roof surface in this
    family, and the demo's context roof, so the two cannot read as different
    materials. Courses run along `ex` and climb `ey`; ex x ey points out of the
    roof. Courses are placed by HEAD, so the top course's head lands on v1 and
    the bottom course's butt hangs `hang` below v0. `u1_at(v)` is the up-slope
    end of the course, which is how a dormer roof plane widens as it climbs to
    its valley.

    THE COURSE STEP is what makes this read as a roof instead of a painted
    plane, and it is roofs.py's mechanism exactly: every tab is TILTED about the
    course axis by th = atan(relief/gauge), so the surface it presents drops by
    exactly `relief` over one course. The butt of each course therefore stands
    `relief` out of the course below it and draws a shadow line, while nothing
    accumulates up the rake, so the roof plane still lands on its valley and its
    ridge where the cheeks and the barge expect it. It costs no tris at all.

    Everything else here exists to make the COURSE, and not the tab, the thing
    the eye picks up at the distance a dormer is actually seen from:
      * a tab is placed by its BUTT, so the wander ragged-edges the course
        without breaking the step line;
      * the stagger is 4-phase, so there is no two-course checkerboard cell to
        be mistaken for one coarse course;
      * value is mostly PER COURSE, over soft blotches a few tabs across, so
        what varies reads as weathering along the courses rather than confetti;
      * one material -- see _shmat.

    And two things stop it fighting, which is what the old flat-laid version did
    over every lap: the tilt means two lapping courses are no longer parallel,
    and each tab carries its own small extra tilt and yaw, so no two tabs in a
    field share a plane at all.

    HANDEDNESS, and pass `mirror` OR THE WHOLE FIELD IS BUILT INSIDE THE DECK.
    The tab frame is X along the course, Y up the slope, Z OUT OF THE ROOF, and
    Z here is whatever ex x ey happens to be -- so (ex, ey) must be right-handed
    about the surface's real outward normal. On a mirrored slope it is not. The
    gabled dormer's two roof planes were authored as ex = +Y on BOTH sides with
    only ey flipped by sx, and on the -X side that makes ex x ey point DOWN into
    the deck: every tab was placed at -(SLAB_T/2 + relief) instead of +, i.e.
    buried under its own boarding, and the per-course tilt stepped inward too.
    Half of every gabled dormer roof rendered as a flat bare plate -- correct
    from +X, bare from -X, which is how it survived four rounds of renders taken
    from one side. (Measured: 21-30 verts standing proud of the -X plane against
    653-660 on the +X plane.)
    So `mirror` says "this frame is the mirror image": the u axis and every u
    coordinate stay exactly as passed (u is still measured along `ex`, which for
    the dormer gable is +Y on both slopes, front to valley), but the tab frame is
    rebuilt right-handed -- course axis reversed, outward normal flipped back --
    so the relief steps PROUD, away from the deck, on both slopes. Fixing it here
    rather than at the caller is what keeps u0/u1_at readable as world y.
    The sign only matters for the TABS: `_slab` extrudes symmetrically about its
    plane and finish() recalculates its normals, so the deck is unaffected.
    """
    r = rng(f"{p.name}/field/{seed}")
    eu, ey = Vector(ex).normalized(), Vector(ey).normalized()
    ez = eu.cross(ey).normalized()
    ex = eu
    if mirror:
        # right-handed again about the TRUE outward normal: ey x (-ez) = -eu
        ez, ex = -ez, -eu
    M = _basis(ex, ey)
    n = max(1, int(round((v1 - v0) / row)))
    ra = (v1 - v0) / n
    th = atan2(relief, ra)                 # the course tilt
    ct, st = cos(th), sin(th)
    hz = thick * 0.5
    lift = OV * relief * 0.5
    # PER-TAB TILT AND YAW -- what a hand-laid shingle does, and what keeps any
    # two tabs off one plane (the yaw separates the SIDE faces, the tilt the
    # OUTER ones). Indexed on the course as well as the tab: indexed on the tab
    # alone, every course got the same alternating pattern and with the half-tab
    # stagger that makes a two-course cell you can mistake for one course.
    ROT = []
    for i in range(48):
        dth = radians(1.80 * (1 if i % 2 else -1) * (.55 + .45 * ((i * 3) % 7) / 6.))
        yaw = radians(0.90 * (1 if (i // 2) % 2 else -1) * (.60 + .40 * ((i * 5) % 7) / 6.))
        ROT.append(Matrix.Rotation(-th + dth, 4, 'X')
                   @ Matrix.Rotation(yaw, 4, 'Z'))
    ph = [(r.uniform(0, 6.283), r.uniform(0, 6.283)) for _ in range(n)]
    amp = [(ra * r.uniform(.07, .18) * wander, ra * r.uniform(.03, .09) * wander)
           for _ in range(n)]
    out = []
    for k in range(n):
        head = v0 + (k + 1) * ra
        u1 = u1_at(head - ra * .5)
        if u1 - u0 < .06:
            continue
        nt = max(1, int(round((u1 - u0) / tab)))
        tw = (u1 - u0) / nt
        off = (STAG[k % 4] + phase) * tw
        a1p, a2p = amp[k]
        p1, p2 = ph[k]
        # ONE butt height and ONE base tone for the whole course
        cl = t0 + lift + r.uniform(0, relief * .22)
        csh = shade * (1.0 + r.uniform(-course_var, course_var * .8))
        for i in range(nt + 1):
            cu = u0 + tw * (i + 0.5) - off
            lo, hi = max(cu - tw / 2, u0), min(cu + tw / 2, u1)
            if hi - lo < tw * .18:
                continue
            # THE JOINT: pull each end in by half a slot, but never at the roof
            # edge itself, where the barge or the valley covers the tab end
            lo += 0.0 if lo <= u0 + 1e-6 else gap * .5
            hi -= 0.0 if hi >= u1 - 1e-6 else gap * .5
            if hi - lo < tw * .12:
                continue
            cu = (lo + hi) / 2
            hd = head + (a1p * sin(2 * pi * cu / G + p1)
                         + a2p * sin(4 * pi * cu / G + p2)
                         + r.uniform(-1, 1) * ra * .045 * wander)
            bt = hd - ra * OV * (1 + r.uniform(-.05, .04) * wander)
            if k == 0:
                # starter course: a full-length bottom course hangs 0.45 of a
                # gauge below the roof edge, and on a dormer rake that is that
                # much further OUTBOARD -- straight through the bay's tiling seam
                bt = max(bt, v0 - hang)
            sy = (hd - bt) * 0.5 / ct       # half length along the tilted tab
            # a few tabs sit proud of their course -- a thicker shake, or one
            # that has curled. They catch the sun and shadow the tab beside them.
            pl = r.uniform(.18, .40) * thick if r.random() < curl else 0.0
            # place by the BUTT: its underside lands on `cl` whatever the wander
            # did to this tab's length, so the course step line holds
            tc = cl + pl - sy * st + hz * ct + r.uniform(-1, 1) * thick * .05
            # weathering blotches: two harmonics a few tabs across whose phase
            # walks with the course, so damp patches drift diagonally instead of
            # striping. Grey-green VALUE on the one field material.
            bl = 1.0 + clump * (.62 * sin(2 * pi * cu / G + QA + k * .83)
                                + .38 * sin(4 * pi * cu / G + QB - k * 1.27))
            if bl < 1.0 - clump * .30 and r.random() < .34:
                bl *= .74               # dark weathered shakes, inside a blotch
            # eu, not ex: u is measured on the axis the CALLER passed, whichever
            # way the tab frame had to be handed to keep ez pointing out
            c = (Vector(org) + eu * cu + ey * ((hd + bt) * 0.5) + ez * tc)
            out += p.tab(tuple(c), (hi - lo, sy * 2.0, thick),
                         _shmat(r, moss, warm), rot=M @ ROT[(k * 5 + i) % 48],
                         tint=tint, taper=taper,
                         skew=(r.uniform(-1, 1) * .007 * wander, 0.0),
                         head=(k >= n - 1),
                         roll=SH_ROLL * (1 if (k * 3 + i * 5) % 3 else -1)
                              * (.7 + .3 * ((i * 7 + k) % 4) / 3.),
                         shade=csh * bl * (1.0 + r.uniform(-shade_var,
                                                           shade_var * .8)))
    return out


def _boards(p, x0, x1, z0, z1_at, y, t, mat, n, seed, tint=.07, shade=1.0,
            gap=.012, jit=.25, rake=False, peak=None):
    """Vertical boarding. z1_at(x) lets the top edge follow a rake.

    `gap` is the slot between two boards, and it is a REAL HOLE unless something
    solid sits directly behind it -- which is what "gaps between the vertical
    wooden beams under the window" was: the plank apron ran 12 mm slots over an
    empty box, so every joint showed black. Boarding laid on a dark backer wants
    a joint line (4-6 mm); boarding with nothing behind it wants none. `jit` is
    the per-board depth variation, which has to stay inside whatever backer the
    caller put behind the run.

    `rake` CUTS EACH BOARD TO z1_at INSTEAD OF SQUARING IT OFF UNDER IT, and on
    a steep rake that is the difference between boarding and a staircase. A
    square board can only take ONE height for its whole width, and the only safe
    one is its LOW edge -- so under a 61 deg barge every board stopped
    (w/2)*tan61 below the plank at its own centreline: 171 mm on the 1m2 gable,
    a stepped triangle of dark backing showing between the boarding and the
    barge all the way up both rakes and a dark V of it at the apex. Cut as a
    prism on the real line instead, each board meets the plank at its own x, for
    4 extra tris on the one board that straddles `peak` and none on the others.
    `peak` is where z1_at turns over (the gable apex), so the centre board gets
    the tent vertex rather than a chord across the top of the gable.
    """
    r = rng(f"{p.name}/boards/{seed}")
    w = (x1 - x0) / n
    out = []
    for i in range(n):
        cx = x0 + w * (i + 0.5)
        d = t * (1 + r.uniform(-jit, jit))
        sh = shade * (1 + r.uniform(-.10, .08))
        if rake:
            xa, xb = cx - (w - gap) / 2, cx + (w - gap) / 2
            za, zb = max(z1_at(xa), z0 + .015), max(z1_at(xb), z0 + .015)
            if max(za, zb) - z0 < 0.04:
                continue
            poly = [(xa, z0), (xb, z0), (xb, zb)]
            if peak is not None and xa < peak < xb:
                poly.append((peak, z1_at(peak)))
            poly.append((xa, za))
            out += p.prism(poly, d, mat, axis='Y', at=(0, y + d / 2, 0),
                           bevel=0, tint=tint, shade=sh)
            continue
        top = min(z1_at(cx - w / 2), z1_at(cx + w / 2))
        if top - z0 < 0.03:
            continue
        out += p.box((cx, y + d / 2, (z0 + top) / 2), (w - gap, d, top - z0),
                     mat, bevel=0, tint=tint, shade=sh)
    return out


def _arc(p, a, b, rise, w, y, t, mat, segs=6, bury=0.055, tint=.06, shade=1.0,
         flip=False, taper_w=1.0):
    """ONE CONTINUOUS ARCHED BRACE -- the "broad shallow arc of timber" the brief
    reads off ref3, under every dormer window and every gable apex.

    THE OLD VERSION WAS THE "BROKEN ARCS" BUG. It drew a crescent between two
    free points: the ends stopped in mid-air on the plaster face, landing on
    nothing, and a pair of them either side of a window read as two fragments of
    an arch that never met. So:

      * `a` and `b` are SPRINGING POINTS INSIDE the members the arc lands on --
        a post, a beam, a rail -- not points on their surface. Both ends are then
        extended a further `bury` along their own tangent, so the arc dies inside
        solid timber at both ends and there is no end face to see and no butt
        seam to open up.
      * it is ONE solid, one continuous curve from springing to springing, so an
        arch spanning a whole face is a single member rather than two halves
        butted at the crown.
      * the band is offset PERPENDICULAR to the local tangent, so its depth is
        constant round the curve instead of pinching at the springing.

    a, b     (x, z) springing points, inside the members being landed on
    rise     peak bulge of the centre line off the chord (parabolic, 4t(1-t))
    w        depth of the timber band, measured on the concave side
    flip     bulge to the other side of a -> b
    taper_w  band depth multiplier at the b end (a haunched brace tapers)
    """
    ax, az = a
    bx, bz = b
    dx, dz = bx - ax, bz - az
    L = hypot(dx, dz) or 1.0
    ux, uz = dx / L, dz / L
    sgn = -1.0 if flip else 1.0
    nx, nz = -uz * sgn, ux * sgn
    out = []
    for i in range(segs + 1):
        s = i / segs
        bl = rise * 4.0 * s * (1.0 - s)
        out.append((ax + ux * L * s + nx * bl, az + uz * L * s + nz * bl))

    def _ext(q0, q1, d):
        vx, vz = q0[0] - q1[0], q0[1] - q1[1]
        m = hypot(vx, vz) or 1.0
        return (q0[0] + vx / m * d, q0[1] + vz / m * d)

    out[0] = _ext(out[0], out[1], bury)
    out[-1] = _ext(out[-1], out[-2], bury)
    inn = []
    n = len(out)
    for i, q in enumerate(out):
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        tx, tz = out[j1][0] - out[j0][0], out[j1][1] - out[j0][1]
        m = hypot(tx, tz) or 1.0
        ww = w * lerp(1.0, taper_w, i / (n - 1.0))
        inn.append((q[0] + (tz / m) * sgn * ww, q[1] - (tx / m) * sgn * ww))
    return p.prism(out + inn[::-1], t, mat, axis='Y', at=(0, y, 0), bevel=0,
                   tint=tint, shade=shade)


def _barge(p, hs, apex, bw, y, t=.085, teeth=11, seed=0, mat="oak_dark",
           tint=.05, shade=1.0):
    """THE WHOLE GABLE'S BARGEBOARD, AS ONE SOLID.

    Left kicked foot -> up the left rake -> over the apex -> down the right rake
    -> right kicked foot, with the dagged (scalloped) lower edge cut into the
    same polygon. It is a plank, so it is a prism: profile in (x, z), extruded
    `t` in y.

    WHY IT IS ONE PIECE. It used to be four butted beams -- a kicked foot and a
    rake on each side -- plus eighteen loose scallop lobes stuck on afterwards.
    That gave the two seams "at the bottom and the tops of their eaves/rafters":
    the kick met the rake in a mid-rake butt joint where both members lay in the
    SAME two y planes and overlapped (156 cm2 of coincident face, measured), and
    the two rakes met head-on at the apex. A bargeboard is a single sawn plank
    following the whole rake, so build it as one, and the joints cannot show.

    Distances along the rake are `s` (0 at the eave line, +up); depths are `off`,
    measured INWARD from the roof edge, so a negative `off` is outboard.
    """
    base = bw * .76            # plank depth at a notch between two dags
    dag = bw * .24             # extra depth at a dag tip
    foot = bw * 1.25           # the flare on the kicked foot
    # outer edge: (s, outboard flare). The foot runs 0.11 PAST the eave line and
    # flicks out, which is the reference's kick, and stays 28 mm inside the bay's
    # tiling seam so finish() never has to cut it.
    S_OUT = ((-.11, .022), (-.01, .012), (.15, .003), (.50, .0))

    def P(sx, s, off):
        return (sx * (hs - COS_D * s - SIN_D * off),
                Z_ROOF + SIN_D * s - COS_D * off)

    s_in = (hs - SIN_D * base) / COS_D     # inner edge reaches x = 0 here
    s0, s1 = .10, s_in - .20               # the dagged run, stopped short of the
    out, inn = {}, {}                      # apex so the two sides cannot cross
    # SCALLOPS, NOT A SAW. The lower edge used to alternate `base` and
    # `base + dag` at half-tooth steps, i.e. a pure TRIANGLE WAVE -- and a
    # triangle wave running up both rakes and meeting at the apex is read as a
    # ZIG-ZAG CHEVRON across the gable, not as cut joinery. ("the gable has a
    # strange zig zag pattern".) A dagged bargeboard is a run of ROUND pendant
    # lobes parted by a cusp, so each lobe is sampled round: the cusp sits on
    # `base`, the belly swells to base+dag and comes back. Fewer, rounder,
    # shallower lobes than the old teeth, which also stops the pattern competing
    # with the shingle courses right behind it.
    LOBE = ((0.00, 0.00), (0.22, 0.80), (0.50, 1.00), (0.78, 0.80))
    lobes = max(6, int(round(teeth * .78)))
    for sx in (-1, 1):
        out[sx] = [P(sx, s, -o) for (s, o) in S_OUT]
        q = [P(sx, -.11, foot), P(sx, -.01, base * 1.34)]
        for i in range(lobes):
            for (t_, d_) in LOBE:
                q.append(P(sx, lerp(s0, s1, (i + t_) / lobes), base + dag * d_))
        q.append(P(sx, s1, base))
        inn[sx] = q
    poly = (out[-1] + [(0.0, apex)] + out[1][::-1]
            + inn[1] + [(0.0, apex - base / COS_D)] + inn[-1][::-1])
    p.prism(poly, t, mat, axis='Y', at=(0, y, 0), bevel=0, tint=tint,
            shade=shade)
    return abs(out[1][0][0])


def _teeth(p, u_range, v, y, mat, step=0.16, size=(.058, .09, .085), seed=0,
           tint=.05, rot=None):
    """A tooth/dentil course. Same rhythm as util.dentil() but unbevelled: at
    58 mm a bevel is invisible and costs 36 tris a tooth, and this family spends
    those tris on shingle courses instead."""
    r = rng(f"{p.name}/teeth/{seed}")
    u0, u1 = u_range
    n = max(1, int(round((u1 - u0) / step)))
    for i in range(n):
        p.box((lerp(u0, u1, (i + .5) / n), y, v), size, mat, bevel=0, tint=tint,
              rot=rot, shade=1.0 + r.uniform(-.07, .07))


def _peg(p, x, y, z, mat="oak_pale", r=0.026, l=0.075):
    return p.cyl((x, y, z), r, l, mat, sides=5, axis='Y', tint=.06,
                 shade=1.06)


# ===========================================================================
# THE GLAZED OPENING IS util.Part.glazing(). IT IS NOT HAND-ROLLED HERE.
# ---------------------------------------------------------------------------
# This module used to build its own casing (three boxes), its own pane (one box
# cut to the reveal) and its own diamond leading (a local _lead(), now deleted).
# Five families each grew their own version of that, and each grew the same
# three faults with it -- a pane that stops short of its opening, leading struck
# INSIDE the pane so the diamonds float in an inset rectangle instead of meeting
# the edge, and a frame that butts the plaster so a line opens between them.
# util.Part.glazing() makes all three impossible by construction (oversize pane
# lapped by the frame; leading struck across the whole opening and clipped to the
# pane; frame oversailing onto the plaster), so this family calls it and keeps
# only the numbers that are genuinely this piece's.
CAS_H = .052           # the band above the opening head that the carved crest or
                       # the boarded head panel STANDS ON. The frame's head laps
                       # 15 mm up over it, which houses the crest's foot; keeping
                       # this number is what keeps a 133 mm finial clear of the
                       # head beam's soffit at Z_CREST.
WIN_FRAME = .055       # frame face width
WIN_LAP   = .024       # how far the frame OVERSAILS onto the plaster panel
WIN_LEAD  = .030       # leading standoff. NOT the primitive's 0.015 default: at
                       # 0.015 the bars' back faces land 2.2 mm off the pane, and
                       # this module wobbles by 0.007 -- which tilts both planes
                       # enough that check_zfight measured 126 cm2 of M_glass
                       # against M_iron on the C variant. 0.030 puts 10.5 mm of
                       # clear air between bar and pane, which no wobble closes.
WIN_DEEP  = .114        # glass set-back from Y = 0. Follows WIN_LEAD: it is set so
                       # the frame's front face still lands on y = -0.019, i.e.
                       # 39 mm proud of the plaster face and 69 mm behind the
                       # corner posts -- the order the reference reads front to
                       # back: post, casing, plaster. The pane therefore sits at
                       # the BACK of the REVEAL (y 0.108-0.120 against
                       # Y_FACE + REVEAL = 0.12), which is where it belongs.
WIN_REB   = .034       # pane oversize all round. Bigger than the primitive's
                       # 0.020 because the reveal is deep: the frame laps the pane
                       # by 46 mm, so the pane still covers the whole aperture at
                       # 33 degrees off axis instead of 24.
WIN_CELL  = .205       # diamond pitch, the figure the old local _lead() used, so
                       # the lattice reads exactly as it did before.
WIN_FO    = WIN_FRAME + WIN_LAP        # 0.079: frame reach past the opening edge
WIN_TOP   = WIN_FRAME + WIN_LAP / 2    # 0.067: how far the frame's head rises
                       # above the opening head, i.e. z 1.397 on this opening.
WIN_IN    = OW / 2 + .045              # where the plaster panel's edge runs: 22 mm
                       # UNDER the frame's outer edge (0.377), never a butt joint.
WIN_LEAD2 = WIN_LEAD + ZF   # 0.042: standoff of the SECOND diagonal family of
                       # lead bars. See _leading() -- this is the whole reason
                       # the lattice is struck here rather than by the primitive.


def _leading(p, cx, cz, gw, gh, cell=WIN_CELL, mat="iron", tint=.06):
    """The diamond leading. THE PANE AND THE FRAME ARE STILL util.Part.glazing()
    -- this takes over the lattice ALONE, for one measured reason.

    THE PRIMITIVE STRIKES BOTH DIAGONAL FAMILIES AT THE SAME STANDOFF
    (`zb = cy + depth - lead`, one plane, both directions), so at EVERY crossing
    two 27 mm bars overlap in plan with their front faces in one plane and their
    back faces in another -- nominally 0.0 mm apart, and 27x27 mm each, i.e.
    7.29 cm2 a crossing on the front and the same again on the back.
    Measured on this family at 0.5 mm before this change:

        64 coincident pairs, 616 cm2 in total, of which RAY-REACHABLE 78 cm2
        -- and all 78 of it was these crossings. Nothing else in the family
        was reachable at all. 36 pairs / 140 cm2 of the total is bar-on-bar.

    That is the worst place in the piece to put a flicker: it is dead centre of
    the window, the one thing a player looks at, and the two faces are the same
    material with independent per-primitive tint, so it reads as a twinkle on
    every diamond junction rather than as an obvious seam. It also breaks this
    module's own rule 200 lines up -- two solids that overlap in plan either
    interpenetrate by >= 12 mm or clear each other by >= 12 mm, never abut.

    It cannot be fixed in a piece module through the primitive: `lead` is one
    scalar for both directions and `pattern` only selects diamond/square/none.
    The real fix belongs in util.Part.glazing() -- offset one direction's bars by
    their own thickness -- and five families call it, so it is worth doing there.
    Until then this piece strikes its own two families 12 mm apart in Y (ZF, the
    module's standard clearance, against a 7 mm wobble), which is also how a
    half-lapped lattice is actually made and gives each crossing a shadow.

    THE PRIMITIVE'S CLIP RULE IS REPRODUCED VERBATIM, because it is the fault
    the shared version exists to foreclose: bars are generated across the WHOLE
    opening and clipped to the OVERSIZE GLASS RECT (gw x gh), never inside an
    inset rectangle, so every diamond still meets the edge as a partial diamond.
    Same bar width (lead * 0.9), same pitch, same iteration order, so the lattice
    reads exactly as it did -- only the crossings are no longer coplanar.
    """
    def clip(a, b, c):
        """Clip a*u + b*v = c to the glass rect; the two endpoints or None."""
        pts = []
        if abs(b) > 1e-9:
            for u in (-gw / 2, gw / 2):
                v = (c - a * u) / b
                if -gh / 2 - 1e-9 <= v <= gh / 2 + 1e-9:
                    pts.append((u, v))
        if abs(a) > 1e-9:
            for v in (-gh / 2, gh / 2):
                u = (c - b * v) / a
                if -gw / 2 - 1e-9 <= u <= gw / 2 + 1e-9:
                    pts.append((u, v))
        uniq = []
        for q in pts:
            if not any(abs(q[0] - r[0]) < 1e-6 and abs(q[1] - r[1]) < 1e-6
                       for r in uniq):
                uniq.append(q)
        return uniq[:2] if len(uniq) >= 2 else None

    bw = WIN_LEAD * .9                      # the primitive's bar, to the mm
    step = cell * 2 ** 0.5
    reach = gw + gh
    stand = (WIN_LEAD, WIN_LEAD2)           # "/" family in front, "\" behind
    k = -reach
    while k <= reach:
        for i, (a, b) in enumerate(((1.0, 1.0), (1.0, -1.0))):
            seg = clip(a, b, k)
            if seg:
                (u0, v0), (u1, v1) = seg
                if (u1 - u0) ** 2 + (v1 - v0) ** 2 > 1e-6:
                    yb = WIN_DEEP - stand[i]
                    p.beam((cx + u0, yb, cz + v0), (cx + u1, yb, cz + v1),
                           bw, bw, mat, bevel=0, tint=tint)
        k += step


def _window(p, cx=0.0, y_face=Y_FACE, y_back=Y_BACK, z_sill=Z_SILL,
            z_head=Z_HEAD, lit=True, seed=0, sill=True, sill_hw=OW / 2 + .090):
    """The frame for OPENINGS['win_dormer'], a leaded pane filling it, and a real
    projecting sill under it. THIS IS NOW THE ONLY WINDOW IN THE PIECE -- the
    assembler no longer drops SM_Win_Dormer in front of it (the insert was
    landing 323 mm inside this one), so it has to be complete on its own.

    THE FRAME, THE PANE AND THE LEADING ARE util.Part.glazing(). They used to be
    hand-rolled here, and this family caught every fault that fork was written to
    end: "there are gaps between the window beams and the plasterboard/render
    (white area)" was a lining standing clear of the plaster panel's edge, and the
    leading was struck inside the pane so the lattice floated in an inset
    rectangle. The primitive laps the plaster (WIN_LAP), cuts the pane oversize
    and clips the leading to it, so none of the three can come back. An overlap
    cannot open a gap; a butt joint always can.

    "the window bottom seems a bit weird, missing the sill maybe?" It was. The
    opening simply stopped on the top face of the apron rail: a flush line with
    nothing standing out of the wall, so the window had no visible bottom edge
    and nothing for a casement to sit on. Now there is a chunky sill BOARD whose
    top is exactly OPENINGS["win_dormer"]["sill"] (so the windows family's
    casement still lands on it), projecting 125 mm in front of the plaster with
    an undercut front and a bed mould beneath -- and the callers drop the apron
    rail behind and below it, so the sill reads as the thing that sticks out.
    """
    rv = y_face + S.REVEAL                       # back of the reveal
    if sill:
        # THE SILL. A prism, not a box, because the shape matters: its top face
        # is on z_sill at the BACK -- that is the plane OPENINGS["win_dormer"]
        # gives and the plane a casement has to sit on -- and WASHES DOWN 26 mm
        # to the nose, so weather runs off it and, more to the point, the top is
        # not one flat lit shelf. (Built as a flat box it read as a bookshelf
        # bolted under the window; the reference's sill is a modest weathered
        # band standing about 35 mm out past the apron rail.)
        p.prism([(y_face - .155, z_sill - .064), (rv + .030, z_sill - .048),
                 (rv + .030, z_sill), (y_face - .155, z_sill - .026)],
                sill_hw * 2, "oak_mid", axis='X', at=(cx, 0, 0), bevel=0,
                tint=.06, shade=1.12)
    # FRAME + PANE + LEADING, IN ONE SHARED CALL. Everything that used to be
    # hand-rolled here is now the primitive's job, and the three faults it
    # forecloses are exactly the three that were reported on this window:
    #   * the pane is cut OVERSIZE (opening + rebate all round) and every frame
    #     member laps its edge by 32 mm, so the glass cannot stop short of its
    #     opening and no dark slot can run round it inside its own frame;
    #   * the leading is struck across the WHOLE opening and clipped to the pane,
    #     so every diamond meets the edge as a partial diamond instead of the
    #     lattice floating in an inset rectangle;
    #   * the frame reaches WIN_FO = 79 mm past the opening on all four sides and
    #     so laps 32 mm over the plaster panel's edge (WIN_IN) -- an overlap
    #     cannot open a line the way the old butt joint could.
    # It also holds the leading clear of the pane's plane, so bars and glass are
    # never coplanar.
    # pattern="none" takes ONLY the lattice off the primitive -- the pane is still
    # cut oversize by it, the frame still laps that pane and oversails the plaster,
    # and `lead` is still passed so the frame lands on exactly the same y as before
    # (yf follows lead * 2.6). _leading() then strikes the diamonds itself, two
    # families 12 mm apart, because the primitive puts both in one plane and every
    # crossing was a fully ray-reachable coincidence -- see _leading().
    p.glazing((cx, 0.0, (z_sill + z_head) / 2), (OW, z_head - z_sill),
              depth=WIN_DEEP, frame=WIN_FRAME, overlap=WIN_LAP, rebate=WIN_REB,
              lead=WIN_LEAD, cell=WIN_CELL, pattern="none", mat_frame="oak_mid",
              mat_glass="glass" if lit else "plaster_dim", tint=.06)
    _leading(p, cx, (z_sill + z_head) / 2,
             OW + 2 * WIN_REB, (z_head - z_sill) + 2 * WIN_REB)


def _crest(p, cx, z, y, kind=0):
    """The little carved crown that STANDS ON the window head in ref2. `z` is the
    top of the head casing, i.e. the surface it sits on -- it used to be the head
    of the opening, which buried the whole crest inside the head trim, and left
    its tip poking through the head beam above.
    Bevels dropped on the small blocks: 36 tris each at 70 mm across, spent on
    shingle courses instead."""
    m = "oak_pale"
    p.box((cx, y + .035, z + .0275), (.30, .07, .055), "oak_mid", bevel=0, tint=.05)
    # every carved block sits at the SAME depth, 10 mm proud of the base block's
    # face and 35 mm inside its back -- they used to share the base's back plane
    # exactly, which is 19 cm2 of coincident face right on the window head
    # ... AND THE "10 mm PROUD" WAS NEVER TRUE. yb = y + .0275 with a 55 mm block
    # puts the carved block's FRONT face on y exactly, which is the base block's
    # own front face: 17-19 cm2 a dormer, dead centre on the window head, and
    # ray-sampled 100% REACHABLE -- it is the most-looked-at 20 cm2 of the piece.
    # Measured at 0.63-0.95 mm (wobble is all that keeps it off the 0.5 mm gate;
    # nominally it is 0.0 mm). y + .0155 is what the comment always described,
    # at this module's own 12 mm clearance: front 12 mm proud of the base, back
    # 27 mm inside it, and the blocks are 12 mm DEEPER so the back plane does
    # not move with the front: at 55 mm deep, standing the front 12 mm proud put
    # the BACK on y = 0.053, which is 3 mm off the plaster head plate's front face
    # (Y_FACE + .024 + .030 - .024 = 0.050) -- measured, 113 cm2 of it. 67 mm deep
    # keeps the back on 0.065, 15 mm clear of that plate, where it always was.
    # NOT y + .0175, which puts the front on y = 0.000 EXACTLY -- and y = 0 is a
    # declared seam of every piece in this family, which check_zfight excludes by
    # design (seam_planes/on_seam). Landing a face there would have moved the pair
    # out of the measurement instead of out of the mesh. -0.002 is measurable.
    yb = y + .0215
    if kind == 0:
        p.box((cx, yb, z + .086), (.085, .067, .080), m, bevel=0, tint=.05)
        for sx in (-1, 1):
            p.box((cx + sx * .095, yb, z + .062), (.075, .067, .058), m,
                  bevel=0, tint=.05, rot=(0, sx * 16, 0))
    elif kind == 1:
        p.box((cx, yb, z + .082), (.072, .067, .072), m, bevel=0, tint=.05,
              rot=(0, 45, 0))
        for sx in (-1, 1):
            p.box((cx + sx * .10, yb, z + .052), (.058, .067, .058), m,
                  bevel=0, tint=.05, rot=(0, 45, 0))
    else:
        p.box((cx, yb, z + .072), (.20, .067, .070), m, bevel=0,
              tint=.05, taper=.55, taper_axis='X')
        p.box((cx, yb, z + .122), (.05, .067, .055), m, bevel=0, tint=.05,
              rot=(0, 45, 0))


def _pierce(p, cx, z, y, kind=0, mat="oak_mid"):
    """Pierced trefoil / quatrefoil under the gable apex."""
    r = .044
    if kind == 0:
        for dx, dz in ((0, .062), (-.058, -.028), (.058, -.028)):
            p.cyl((cx + dx, y, z + dz), r, .05, mat, sides=7, axis='Y',
                  tint=.05, shade=.86)
        p.box((cx, y, z - .10), (.04, .048, .12), mat, bevel=0, tint=.05, shade=.86)
    elif kind == 1:
        for dx, dz in ((0, .07), (0, -.07), (-.07, 0), (.07, 0)):
            p.cyl((cx + dx, y, z + dz), r * .95, .05, mat, sides=7, axis='Y',
                  tint=.05, shade=.86)
    else:
        p.cyl((cx, y, z), r * 1.25, .05, mat, sides=9, axis='Y', tint=.05)
        p.box((cx, y, z - .11), (.045, .048, .13), mat, bevel=0, tint=.05)
        p.box((cx, y, z + .10), (.045, .048, .10), mat, bevel=0, tint=.05)


# ------------------------------------------------------- gabled dormer -------
def _gabled(name, wf, over, var, seed):
    """One 2m bay: a 0.68 m deep dormer BOX standing proud of the recessed wall
    plane, boarded cheeks down both sides, its own two-plane shingled roof over
    it, and the recessed flanking wall panels each side."""
    # Gable half span. A course butt now stands SLAB_T/2 + BUILD = 0.092 out of
    # the roof plane and the starter course hangs below its edge, and on a 61 deg
    # rake both of those go OUTBOARD in x -- so the roof edge itself has to sit
    # far enough inside the bay that the finished roof still fits. Past HB (the
    # tiling seam) finish() clamps everything flat onto the seam, which deforms
    # the shingles AND leaves a stack of coincident faces there. The margin is
    # (SLAB_T/2 + BUILD) * sin(61) + hang * cos(61) = 0.098; the overhang is what
    # gives, because a 1.48 m box in a 2.0 m bay has only 0.26 either side.
    hs = min(wf / 2 + over, HB - .112)     # gable half span
    apex = Z_ROOF + hs * TAN_D
    d_roof = (apex - Z_ROOF) / TAN_R        # where the ridge dies into the field
    D = Y_WALL + d_roof + 0.13
    hf = wf / 2
    # THE OVERHANG IS hs - hf, NOT `over`. hs is CLAMPED to HB - 0.112 so the
    # finished roof fits inside the bay, and on the 1m5 that clamp bites hard:
    # `over` asks for 0.26 and the rake edge actually lands 0.148 outside the
    # cheek. z_ck/y_ck were computed from the ASKED-FOR figure, so the whole top
    # of the cheek -- its slab, its boarding and the wall plate along it -- was
    # built 0.20 m too high on the 1m5 (0.09 on the 1m2s) and stood UP THROUGH
    # the dormer's own shingles. Ray-cast straight down onto the roof and the
    # wall plate was the first thing hit over a 0.16 x 0.85 m strip of it: that is
    # the beam lying across the roof that makes no sense. Take the overhang from
    # the geometry that was actually built.
    ov = hs - hf                            # the real rake overhang past the cheek
    z_ck = Z_ROOF + ov * TAN_D              # roof underside over the cheek
    y_ck = Y_WALL + ov * TAN_D / TAN_R      # ... where that meets the field
    # z-max has to contain the apex spike: declared at apex+0.02 it was 0.10 m
    # short, and finish() CRUSHED the spike flat onto that plane -- a clamp is
    # not just lost detail, the flattened faces are all coplanar and fight.
    p = _Part(name, budget="dormer",
             seams=dict(x=(-HB, HB), y=(0, D), z=(0, apex + .15)))
    r = rng(name)
    barge_w = var.get("barge", .20)

    # ---------------- recessed flanking wall panels ------------------------
    # Set back the FULL box depth: this recess is what makes the dormer read as
    # a box instead of a gable painted on the roof.
    for sx in (-1, 1):
        x0, x1 = sx * hf, sx * HB
        lo, hi = min(x0, x1), max(x0, x1)
        # The dark backing starts 42 mm INSIDE the plaster face in front of it
        # (it used to start exactly on the plaster's back plane), and its inner
        # x edge runs on behind the cheek instead of dying on the framing plane.
        # ... and it now runs 60 mm PAST the eave line at the top: its top face
        # used to sit on z = Z_ROOF, which is also the top face of the head plate
        # in front of it -- 119 cm2 of coincident wall per dormer. Above Z_ROOF
        # at this y the main roof field has not arrived yet (it crosses Z_ROOF at
        # Y_WALL and climbs from there), so the overrun is buried.
        p.plate(((lo + hi) / 2 - sx * .008, (Y_FLANK + .042 + Y_FLANK_B) / 2,
                 (Z_ROOF + .060) / 2),
                (hi - lo + .016, Y_FLANK_B - Y_FLANK - .042, Z_ROOF + .060),
                "plaster_dim", tint=.03, shade=.60)
        # plaster face, inset from the framing all round -- the reference panels
        # are recessed anyway, and now no panel edge lies on a frame plane
        p.plate(((lo + hi) / 2, Y_FLANK + .024, (Z_APRON + .030 + 1.576) / 2),
                (hi - lo - .024, .05, 1.576 - Z_APRON - .030), "plaster",
                tint=.05, shade=.86)
        # framing: post beside the cheek, top plate, apron rail.
        # THE POST IS DEEPER THAN THE RAILS ON BOTH SIDES. It used to be exactly
        # as deep and at exactly the same y as them, so post and rails shared
        # BOTH y planes and fought wherever they crossed (2 x 159 cm2 a dormer).
        # A post standing 27 mm proud of the infill it frames is also what the
        # reference shows, so the fix is the better read as well. Bevel dropped:
        # 64 tris a dormer, at 0.68 m back in a recess.
        # ... and its head, like the box's corner posts, dies 30 mm INSIDE the
        # top plate rather than level with it. Both used to top out on z = Z_ROOF
        # and the post is deeper than the plate on both sides, so the 0.15 x 0.085
        # patch where they cross put two top faces on one plane: 129 cm2 on the B
        # variant, and the same joint on every variant. Sealed (ray-sampled 0%
        # reachable -- the dormer's own roof and the backing plate cover it), so
        # this is a number change and nothing else: no triangles, no visible move.
        p.box((sx * (hf + .10), Y_FLANK + .0175, (Z_ROOF - .030) / 2),
              (.15, .140, Z_ROOF - .030),
              "oak_dark", bevel=0, tint=.05, shade=.84)
        p.box(((lo + hi) / 2, Y_FLANK + .03, (Z_APRON + Z_SILL) / 2),
              (hi - lo, .085, Z_SILL - Z_APRON), "oak_dark", bevel=0,
              tint=.05, shade=.84)
        p.box(((lo + hi) / 2, Y_FLANK + .03, (1.56 + Z_ROOF) / 2),
              (hi - lo, .085, Z_ROOF - 1.56), "oak_dark", bevel=0,
              tint=.05, shade=.84)
        # boarding: its head runs up INTO the apron rail rather than stopping on
        # the rail's underside
        # recessed 18 mm behind the framing's face (that is where boarding
        # sits) and thick enough that its back is buried in the dark backing
        # ... and thick enough that its back comes out at least 15 mm BEHIND
        # the post's back plane whatever the per-board depth jitter does. At
        # 0.070 the deepest board landed 0.75 mm off that plane, which
        # remove_doubles (0.6 mm) then welded into an exact coincidence: 294 cm2
        # on the B variant, the biggest single pair left in the family.
        # ... and the joints are 6 mm, not 12: this run is boarding, and a 12 mm
        # slot over a backer 30 mm behind it reads as a hole rather than a joint
        # ... and the run starts on z = 0, the piece's own base plane, not on
        # 0.010. A 10 mm strip of nothing along the foot of both flanking panels
        # is a slot at the joint with the wall course below: a front-on ray at
        # z = 0.004 missed the boarding (front face y = 0.692) altogether and
        # struck the dark backing plate at y = 0.722 instead. The post beside it
        # and the backing behind it both already run to 0, so this run was the
        # one that was short.
        _boards(p, lo + .01, hi - .01, 0.0, lambda x: Z_APRON + .016,
                Y_FLANK + .012, .110, "oak_mid", var.get("flank_boards", 3),
                seed=seed * 7 + 1, shade=.80, gap=.006)

    # back of the box, so the roof void never shows daylight. 22 mm behind the
    # canted soffit's own back plane, cut narrower than the cheeks, and stopped
    # short of the cheeks' top plane.
    p.plate((0, Y_WALL + .092, (z_ck - .02) / 2), (wf - .06, .14, z_ck - .02),
            "plaster_dim", tint=.03, shade=.42)

    # ---------------- dormer box: front panel ------------------------------
    # ONE BACKING PLATE, and this is the single biggest z-fighting fix in the
    # family. It used to be four plates threaded AROUND the window opening, and
    # they cost 1041 cm2 of coincident surface on the 1m5 alone: they overlapped
    # each other by 14 mm in z, so two of them shared a front face and a back
    # face wherever they lapped, and the bottom band's top face landed exactly on
    # the apron rail's top face at Z_SILL.
    #
    # It only needed threading around the opening because it sat at y = 0.13,
    # in front of the glass. Put it BEHIND everything instead -- y 0.22..0.34,
    # clear of the posts, the beams, the reveal and the pane, which all stop by
    # y = 0.19 -- and it can be one solid sheet with no hole and no laps. The
    # glass is emissive and opaque, so nothing shows through the reveal.
    hbk = hf - .03
    p.plate((0, .280, (.120 + Z_ROOF - .035) / 2),
            (hbk * 2, .12, Z_ROOF - .035 - .120), "plaster_dim",
            tint=.03, shade=.80)
    # Plaster face, four plates around the opening. Each carries its own face
    # depth -- a hand-floated panel is not one flat sheet -- and the head and
    # apron plates lap 14 mm over the jamb plates, so neither the joints nor the
    # faces are ever coplanar.
    # EVERY EDGE OF EVERY PLATE IS NOW LAPPED BY THE MEMBER NEXT TO IT. "a gap
    # between the plaster and the brickwork making it show roof in-between" was
    # two BUTT JOINTS that had opened into slots, measured at 8 mm on z
    # 0.512-0.520 and 14 mm on z 1.330-1.344 beside every window:
    #   * the jamb plates' feet sat on Z_SILL - 0.030 = 0.520 and the apron rail's
    #     top face is Z_SILL - 0.038 = 0.512, so an 8 mm band of nothing ran
    #     between them and you saw the dark backing plate through it. The feet now
    #     run to Z_SILL - 0.060, i.e. 22 mm DOWN INSIDE the rail;
    #   * the head plate's foot sat at Z_HEAD + 0.014 and the jamb plates stopped
    #     dead on Z_HEAD, so despite the comment that used to be here they did not
    #     lap at all -- they missed each other by 14 mm. The jamb heads now run to
    #     Z_HEAD + 0.056 and the head plate's foot drops to Z_HEAD + 0.040, so the
    #     head plate laps 16 mm OVER them, 30 mm behind their face (dy) so no two
    #     faces are coplanar, and the joint itself is hidden behind the glazing
    #     frame's head (z 1.318-1.397) and, further out, inside the corner post.
    # Their inner edges run 32 mm under the glazing frame's outer edge (WIN_IN),
    # which is what closes the slot down each side of the window. The apron plate
    # is GONE: the plank apron and its backer fill that band, and a plaster plate
    # behind boarding was a member doing another member's job.
    for (z0, z1, x0, x1, dy) in ((Z_SILL - .060, Z_HEAD + .056, -hf + .146, -WIN_IN, 0.0),
                                 (Z_SILL - .060, Z_HEAD + .056, WIN_IN, hf - .146, 0.0),
                                 (Z_HEAD + .040, Z_CREST + .04, -hf + .13, hf - .13, .030)):
        p.plate(((x0 + x1) / 2, Y_FACE + .024 + dy, (z0 + z1) / 2),
                (x1 - x0, .048, z1 - z0), "plaster", tint=.05, shade=1.03)
    _window(p, lit=True)
    # THE BOARDED HEAD PANEL AND THE CREST ARE ALTERNATIVES, NOT A STACK. The
    # boarding sat at y = -0.028 and the crest behind it at y = +0.010, so on the
    # boarded variant the crest was walled up behind its own head panel -- carved
    # timber doing nothing, which is the kind of doubling-up that makes a face
    # read as a pile of parts. Whichever the variant picks now starts on the top
    # of the window's head casing and dies up under the head beam.
    if var.get("face_boarded"):
        # y = Y_FACE - .044, not -.028: the boarding laps the top 11 mm of the
        # glazing frame's head, and at -.028 its back face ran 4 mm off the
        # frame's front face over that lap -- the separation that measured as
        # coincident once wobble tilted both planes. 10 mm of clear air instead.
        _boards(p, -hf + .13, hf - .13, Z_HEAD + CAS_H + .004, lambda x: 1.53,
                Y_FACE - .044, .03, "oak_mid", 6, seed=seed * 3 + 5, shade=1.02,
                gap=.007)
    elif var.get("crest") is not None:
        _crest(p, 0.0, Z_HEAD + CAS_H, Y_FACE - .01, kind=var["crest"])

    # corner posts. Set 12 mm in from the box corner so the post's outer face is
    # buried in the cheek slab instead of sharing a plane with the cheek slab and
    # the cheek boarding.
    # AND THE HEAD DIES 30 mm INSIDE THE HEAD BEAM INSTEAD OF LEVEL WITH IT.
    # The post used to stop dead on z = Z_ROOF, which is also the head beam's TOP
    # face, and the post is entirely inside that beam in y (-0.088..0.112 against
    # -0.1025..0.1325) -- so its 0.121 x 0.170 top quad lay exactly on the beam's
    # own top quad. Measured at 0.5 mm this round: 202 cm2 on the C variant and
    # 196 on the 1m5, and ray-sampled 20% and 70% REACHABLE, i.e. the largest
    # thing on this family a camera can actually watch flicker. It is the same
    # construction on all four variants; which of them the gate reports is
    # decided by which way p.wobble tilts the beam's top quad, so all four were
    # one wobble away from it. A post carrying a beam runs UP INTO the beam, so
    # this one now stops 70 mm short of its top: 130 mm of housing, no new
    # triangles, and nothing that was visible moves.
    # 0.070, NOT 0.030, and this is measured rather than chosen: at Z_ROOF-0.030
    # the head landed on z = 1.670, which is the base plane of the GABLE BOARDING
    # (_boards from Z_ROOF - 0.03) and inside the boards' own y band -- so the fix
    # simply moved 130 cm2 from one coplanar pair to another, four smaller ones.
    # The horizontal planes it has to miss above the beam soffit are 1.655 (the
    # infill prism's foot, Z_ROOF-0.045), 1.670 (the boarding's foot) and 1.700
    # (the beam's top). 1.630 is 25 mm clear of the nearest.
    z_post_top = Z_ROOF - .070
    for sx in (-1, 1):
        p.box((sx * (hf - .087), Y_POST + .10, (Z_SOF + .018 + z_post_top) / 2),
              (.15, .20, z_post_top - Z_SOF - .018), "oak_dark", bevel=.016,
              seg=1, tint=.05, shade=1.0 + r.uniform(-.04, .04))
    # APRON RAIL. Its top is now 38 mm BELOW Z_SILL, so _window's projecting sill
    # sits on it and stands out of it -- the rail used to run all the way up to
    # Z_SILL, which is why the window had no visible bottom edge at all, and its
    # top face was coplanar with the backing behind it (1041 cm2, the worst pair
    # in the kit).
    p.box((0, Y_TRIM + .12, (Z_APRON + Z_SILL - .038) / 2),
          (wf + .07, .24, Z_SILL - .038 - Z_APRON),
          "oak_mid", bevel=.016, seg=1, tint=.06, shade=1.04)
    # peg ends under the sill, out where the arched brace springs and the arc is
    # low -- they used to sit at mid-apron, which is where that brace now is, and
    # read as nubs pushed through it
    for sx in (-1, 1):
        _peg(p, sx * (hf - .17), Y_TRIM + .012, Z_SILL - .115)
    # PLANK APRON, ON A SOLID BACKER, WITH THE JOINTS CLOSED. "there are ... gaps
    # between the vertical wooden beams under the window": the boards ran 12 mm
    # slots over an empty box, so every joint was a hole straight through to the
    # dark of the interior, and the depth jitter widened some of them. Now the run
    # sits on a dark oak backer whose front face is INSIDE the boards' own depth
    # range whatever the jitter does (so a joint shows shadowed timber, not
    # daylight), and the joint itself is 5 mm -- a plank line, not a gap.
    p.plate((0, .0225, (Z_RAIL - .020 + Z_APRON + .040) / 2),
            ((hf - .03) * 2, .045, Z_APRON + .040 - Z_RAIL + .020),
            "oak_dark", tint=.03, shade=.46)
    # ... and the boards run 45 mm DOWN INSIDE the floor beam rather than butting
    # its top face. They used to start exactly on z = Z_RAIL, which IS that face,
    # so the whole run met its bearer in a butt joint: measured on the built mesh
    # the two coincided to 0.0 mm and finish()'s 0.6 mm weld fused them, which is
    # the one joint in the piece that could not be checked for daylight because
    # there was nothing between the two faces to check. An overlap cannot open.
    # 0.045, not 0.030: the canted soffit's top face is Z_SOF + 0.10 = 0.155, so
    # a 30 mm lap put every board's underside exactly on it (77 cm2 a board,
    # which check_zfight duly caught). 0.140 clears the soffit by 15 mm, the
    # backer's own foot by 25 mm and the beam's top face by 45 mm.
    _boards(p, -hf + .02, hf - .02, Z_RAIL - .045, lambda x: Z_APRON + .018,
            -.020, .045,
            "oak_mid", var.get("apron_boards", 7), seed=seed * 11, shade=1.02,
            gap=.005, jit=.22)
    p.box((0, Y_TRIM + .115, (Z_SOF + Z_RAIL) / 2), (wf + .10, .25, Z_RAIL - Z_SOF),
          "oak_dark", bevel=.016, seg=1, tint=.05, shade=.95)
    # (The two blocks that used to sit here are GONE. They were described as the
    # floor beam's ends reading as corbels, but the floor beam stops at x = 0.79
    # and the box's own cheek face is at 0.798, so a block centred on 0.815 stood
    # entirely OUTBOARD of both: a lump stuck on the corner, landing on nothing,
    # doubling up on the three joists that already read as the box's bearers.)

    # ---------------- canted soffit + diagonal braces under the sill -------
    # The box is jettied out over the wall behind it, so its underside rakes
    # back and down onto that wall, with exposed joists under it.
    # the soffit's back edge stops 22 mm SHORT of the wall plane: it used to sit
    # on y = Y_WALL, and so does the back edge of both cheeks, which put three
    # faces of three solids on one plane (2 x 74 cm2). The box back plate covers
    # the 22 mm.
    p.prism([(Y_TRIM + .01, Z_SOF + .006), (Y_WALL - .022, .004),
             (Y_WALL - .022, Z_SOF + .10),
             (Y_TRIM + .01, Z_SOF + .10)], wf - .01, "oak_dark", axis='X',
            bevel=0, tint=.04, shade=.62)
    for i in range(3):        # joists across the soffit
        jx = lerp(-hf + .16, hf - .16, i / 2.0)
        # start z 0.050, not 0.026: the end cap's lower corners hang h/2 below
        # the axis, and at 0.026 six of them sat at z = -0.014, so finish() cut
        # them flat onto the piece's own floor plane every build.
        # BACK END AT Y_WALL - .052, NOT Y_WALL - .02. The soffit prism's back
        # face is on Y_WALL - .022, so a joist ending at Y_WALL - .02 poked its
        # 0.085 x 0.080 end cap 2 mm out through it: 68 cm2 a dormer of end grain
        # 2 mm off a face it is parallel to, and ray-sampled 100% REACHABLE from
        # behind the box. A joist is a rib IN this soffit, not a member spanning
        # to the wall, so its end is now buried 30 mm inside the soffit. The
        # exposed part -- the ribs standing below the canted underside at the
        # front -- is untouched.
        p.beam((jx, Y_WALL - .052, .050), (jx, Y_TRIM + .04, Z_SOF + .010),
               .085, .080, "oak_dark", bevel=0, tint=.05, shade=.70)
    # THE ARCHED BRACE UNDER THE WINDOW -- one member, not two crescents.
    # The brief reads "a broad shallow arc of timber spanning ... under each
    # dormer window" off ref3, and what was here instead was a pair of separate
    # curved wedges, one each side, each floating with both ends on nothing. That
    # is what "the arcs on the dormer are broken" is: two fragments that never
    # meet and never land. Now it is a single arc springing from INSIDE both
    # corner posts and dying INSIDE the apron rail at the crown.
    # ... AND IT IS NOW HOUSED, NOT LAID ON TOP. Its springings used to sit at
    # x = +/-(hf - 0.05) with the band standing 48 mm PROUD of the corner post's
    # own front face, so each end crossed the post's outer plane and came out the
    # far side into open air beside the cheek -- an arc passing THROUGH a post,
    # which is exactly what reads as a modelling error. The springings are pulled
    # 135 mm inboard (well inside the post's 150 mm width) and the band is set
    # BEHIND the post face, so the post's own timber covers the end: an arc that
    # springs from a member and dies into one.
    _arc(p, (-(hf - .135), Z_RAIL + .030), (hf - .135, Z_RAIL + .030),
         Z_APRON + .010 - (Z_RAIL + .030), .085, -.062, .058,
         "oak_dark", segs=6, bury=.055, shade=.94)

    # ---------------- head beam + tooth trim -------------------------------
    p.box((0, Y_TRIM + .115, (Z_CREST + Z_ROOF) / 2), (wf + .19, .235, Z_ROOF - Z_CREST),
          "oak_dark", bevel=.018, seg=1, tint=.05)
    # TOOTH COURSE UNDER THE HEAD BEAM, RUNNING BETWEEN THE POSTS. It used to run
    # to +/-(hf + 0.04), i.e. 40 mm outboard of the box's own corner, so the last
    # tooth at each end stood inside the cheek boarding and the corner bracket
    # crossed the run -- teeth passing through timber. Ending it on the posts'
    # inner faces makes it a course carried between two members instead.
    # Unbevelled: util.dentil() bevels every block, which is 48 tris a tooth and
    # invisible at 58 mm -- 290 tris a dormer, which is what pays for the shingle
    # courses below.
    # AND IT IS AN ALTERNATIVE TO THE CARVED CREST, NOT A SECOND LAYER OVER IT.
    # The band between the window head and the head beam is only 170 mm, and the
    # casing, the crest and this course all wanted it: the crest ended up standing
    # inside the tooth course, two carved details in one 90 mm strip fighting for
    # the same read. Each variant now takes one -- a crest, a boarded head panel,
    # or this course running the full face the way ref3 draws it.
    # AND THE COURSE IS FIXED TO THE BEAM IT HANGS FROM. Struck at
    # v = Z_CREST - 0.045 its tops landed on z = 1.4975 against a soffit at
    # Z_CREST = 1.500, and its face on y = -0.100 against a beam face at -0.1025:
    # a whole dentil course held 2.5 mm clear of the member it belongs to, on
    # both axes -- measured on the built mesh at 4.4 mm once wobble is in. Teeth
    # are cut out of the beam's underside, so they run UP INTO it: 14.5 mm now,
    # and 12.5 mm back behind its face so the beam oversails them the way a
    # fascia oversails a dentil course instead of sitting flush with it.
    if var.get("head_teeth", True):
        # DEPTH 0.120, NOT 0.090. At 0.090 the tooth's BACK face landed on
        # y = 0.000 and the boarded head panel's boards -- which cross the same
        # 85 mm of z -- have their backs at 0.0015..0.0135 once the per-board
        # depth jitter is in. So on the one variant that carries both (C: teeth
        # plus face_boarded) the two back faces sat 1.5 mm apart and measured
        # 28.9 cm2 at 0.47 mm. Sealed (ray-sampled 0% reachable: it is between the
        # boarding and the beam), so this is a number, not a rebuild -- the tooth
        # runs 30 mm past the boarding's deepest back instead of stopping level
        # with it, and its back is still 20 mm clear of the plaster head plate's
        # front face at y = 0.050. The FRONT of the course does not move.
        _teeth(p, (-hf + .19, hf - .19), Z_CREST - .028, Y_TRIM + .070, "oak_dark",
               step=var.get("dentil", .185), size=(.058, .120, .085), seed=seed)

    # ---------------- gable: roof planes, barge, infill ---------------------
    # THE BARGEBOARD IS NOW ONE SOLID FOR THE WHOLE GABLE -- see _barge. It used
    # to be four butted beams (a kick and a rake each side) plus eighteen loose
    # scallop lobes, which is exactly the fault: a seam across the middle of each
    # rake where the kick met it (156 cm2 of coincident face there, since both
    # halves lay in the same two y planes) and another seam where the two rakes
    # met head-on at the apex.
    _barge(p, hs, apex, barge_w, y=-.105, t=.085,
           teeth=var.get("dags", 11), seed=seed * 13)
    # THE RIDGE RUNS THE WHOLE RIDGE. It used to stop at 0.62 of the way back,
    # which is nowhere: a capping timber ending in the middle of its own roof
    # reads as a stick lying on the shingles. It now runs to where the dormer
    # ridge actually dies into the main roof field -- the same point the two
    # valley beams converge on -- so all three members meet at one junction.
    # (The back end is solved against the field plane at the cap itself, below;
    # only the front end is a number.)
    ridge_y0 = Y_BARGE + .02
    for sx in (-1, 1):
        # THE TWO SLOPES ARE MIRROR IMAGES OF EACH OTHER. The course axis is +Y
        # (front edge to valley) on both, and only ey flips with sx -- which
        # means the frame's implied normal, ex x ey, points out of the roof on
        # +X and INTO THE DECK on -X. That is the sign that has to reach the tab
        # OFFSET as well as the tab position, so _field takes `mirror` and rehands
        # the tab frame; without it the -X slope's ~210 tabs are built under the
        # boarding and that whole slope renders as a flat bare plate.
        ex = (0, 1, 0)
        ey = (-sx * COS_D, 0, SIN_D)
        org = (sx * hs, 0, Z_ROOF)
        mirrored = sx < 0                   # ex x ey = (SIN_D, 0, sx*COS_D)
        rake = hs / COS_D
        # boarding under the shingles: front edge overhangs the face on the
        # rake, back edge follows the valley down into the field.
        # THE DECK IS ROOF MATERIAL, NOT TIMBER. It was oak_dark, and the deck is
        # what you see in every slot between the tabs, along the whole front edge
        # under the starter course and in the ridge gap -- so a shingle_moss roof
        # read as green shingles over brown ones, which is the "green and brown
        # shingles" fault. A roof deck seen between shingle butts should read as
        # roof; dark shading does the rest.
        valley = lambda v: Y_WALL + (SIN_D / TAN_R) * v + .09
        _slab(p, org, ex, ey, [(Y_BARGE + .015, 0), (Y_WALL + .09, 0),
                               (valley(rake), rake), (Y_BARGE + .015, rake)],
              mat=MOSS, shade=.40, tint=.03)
        # real coursed shingle, roofs.py's tab width exactly (see TAB above).
        # The field stops 55 mm short of the apex along the rake: both planes'
        # top courses used to run right onto x = 0, where the two sides' tabs
        # interpenetrate and some pairs land coplanar (101 cm2 on the 1m5). The
        # 53 mm gap in x is under the ridge cap.
        _field(p, org, ex, ey, Y_BARGE + .03, valley, 0.0, rake - .055,
               seed=seed * 5 + (sx > 0), phase=.25 * (sx > 0), mirror=mirrored)
        # CORBEL UNDER THE PROJECTING END OF THE HEAD BEAM.
        # THIS IS THE ARC SHANEE IS LOOKING AT ("the side has strange arcs that
        # make no sense going through beams the way they do"). It was an _arc in
        # the face plane from x = hf-0.02 to hf+0.06 that BULGED 0.10 further out
        # still: its belly reached x = 0.857 on the 1m5, which is outboard of the
        # corner post (0.728), outboard of the cheek's own outer face (0.798) and
        # outboard of the head beam's end (0.835) -- a curved timber hanging in
        # the air beside the cheek, crossing the post's outer plane and cutting
        # through the tooth course on its way. An arch has to span between two
        # members; there is nothing out there to span to.
        # What belongs under a beam end that projects 95 mm past the box is a
        # CORBEL, so it is one: a canted console, deep at the front and cut away
        # behind, housed 18 mm into the post and through the cheek boarding,
        # stopping 20 mm inside the beam's own end so no two faces line up.
        # AND IT NOW SITS ENTIRELY UNDER THE PROJECTING PART OF THE BEAM.
        # It used to run x = hf-0.030 .. hf+0.075, i.e. 30 mm of it lapped back
        # INSIDE the box, and its front face (Y_TRIM+0.008 = -0.092) was then 2 mm
        # off the cheek slab's front face (Y_TRIM+0.010 = -0.090) and 4 mm off the
        # corner post's (-0.088) over that lap. Measured this round: 69 cm2 at
        # 0.31 mm on the B variant, and ray-sampled 90% REACHABLE -- it is on the
        # front of the box beside the window, the most visible fight in the family.
        # There is no y to fix it in: the 40 mm between the head beam's face
        # (-0.1025) and the cheek boarding's (-0.070) already holds four planes, so
        # anything proud enough to read as a corbel is within 12 mm of one of them.
        # Fix it in X instead. The beam projects hf..hf+0.095; a corbel under a
        # beam END belongs under the projection, so it starts at hf+0.016 -- 16 mm
        # clear of the slab's outer plane, 28 mm clear of the post's -- and is
        # housed 42 mm into the cheek boarding, which is a member, not air. Same
        # tri count (a prism is a prism), and the read is better, not worse: the
        # console now stands under the beam end instead of half-buried in the box.
        zc = Z_CREST
        p.prism([(Y_TRIM + .010, zc + .020), (Y_TRIM + .010, zc - .235),
                 (Y_TRIM + .110, zc - .235), (Y_TRIM + .175, zc - .075),
                 (Y_TRIM + .175, zc + .020)],
                .059, "oak_dark", axis='X', at=(sx * (hf + .0455), 0, 0),
                bevel=0, tint=.05, shade=.90)
        # ------- CHEEK: the deep boarded side of the box ------------------
        # front-bottom -> back along the canted soffit -> up the wall plane ->
        # up the field to where the roof edge dies into it -> back along the
        # roof underside.
        prof = [(Y_TRIM + .01, Z_SOF + .01), (Y_WALL, .004), (Y_WALL, Z_ROOF),
                (y_ck, z_ck), (Y_TRIM + .01, z_ck)]
        # the slab's outer face is ON x = hf: the corner post is buried 12 mm
        # inside it and the boarding stands 14 mm outside it, so the three of
        # them no longer share one plane
        p.prism(prof, CHEEK_T, "oak_dark", axis='X',
                at=(sx * (hf - CHEEK_T / 2), 0, 0), bevel=0, tint=.04,
                shade=.72)
        # vertical cheek boarding (boards stand in Z, divided along Y). This is
        # the read the reference gives every dormer side: dark deep boarding.
        rb = rng(f"{name}/cheek/{sx}")
        nb = var.get("cheek_boards", 5)
        # THE BOARD HEADS STOP ON THE ROOF PLANE AT THEIR OUTER FACE, NOT AT
        # z_ck. Same fault as the wall plate above, at half the amplitude: the
        # boards run x = hf - 0.020 .. hf + 0.058 and took the height of the roof
        # plane where it crosses the CHEEK, so over their outboard 58 mm the deck
        # fell 0.058 * tan61 = 105 mm while they stayed level. Measured: the
        # outer top corner stood 18.5 mm perpendicular above the deck's TOP face
        # -- under the shingle butts (42-70 mm out) but proud of the deck itself,
        # so in the 7 mm slots between tabs the board WAS the topmost surface:
        # 7-22 cm2 of oak per dormer, dashed along both cheek lines.
        # Struck on the plane at the board's OUTER face instead, the top lands
        # dead centre of the 45 mm deck there -- 22 mm of timber under the deck's
        # top face and 22 mm over its soffit, so it can neither show through the
        # slots nor sit close enough to any deck face to fight. Inboard of that
        # the head runs under the roof by up to 28 mm, which is a shadow reveal
        # along the top of the boarding, backed by the cheek slab: raking the top
        # to close it turns the board's end cap into a trapezoid, and the tilt
        # that gives its normal was enough to bring it into the same plane bucket
        # as the head beam's back face 5 mm away -- 131 cm2 of coincident surface
        # that check_zfight had not been reporting before. A flat head keeps the
        # cap rectangular and the family back at zero.
        z_top = Z_ROOF + (hs - hf - .058) * TAN_D
        for i in range(nb):
            y0 = lerp(Y_TRIM + .02, y_ck - .01, i / nb)
            y1 = lerp(Y_TRIM + .02, y_ck - .01, (i + 1) / nb)
            # below the wall plane the boards run right down to the canted
            # soffit; behind it they stop on the roof field
            zb = (lerp(Z_SOF, .01, clamp((y1 - Y_TRIM) / (Y_WALL - Y_TRIM)))
                  if y1 <= Y_WALL else Z_ROOF + (y1 - Y_WALL) * TAN_R)
            if z_top - zb < .06:
                continue
            # THE BOARDING LAPS THE CHEEK SLAB -- IT DOES NOT BUTT IT.
            # "a gap between the plaster and the brickwork making it show roof
            # in-between", measured again this round: the slab's outer face is on
            # x = hf and the boarding used to start at hf + 0.014, so a 14 mm SLOT
            # ran the full height of the box's corner, from below the sill to the
            # window head, with nothing in it -- ray-casting the front of the piece
            # at x = 0.616 hit the recessed backing 0.72 m behind (and on the shed,
            # which has no recessed panel behind it, hit NOTHING AT ALL: 283 cm2
            # of straight-through hole beside the window, which is the roof
            # showing between the plaster and the framing). The board is 78 mm
            # thick instead of 44 and set 20 mm INBOARD of the slab's outer face,
            # so the two overlap by 20 mm and the joint cannot open. It shows
            # exactly the same 58 mm of relief as before (outer face unmoved at
            # hf + 0.058), costs no extra tris -- a box is a box -- and the new
            # inner face is buried inside the slab, 8 mm clear of the corner post's
            # outer plane and 10 mm clear of the corbel's, so it lands on no
            # existing plane. An overlap cannot open a slot; a butt joint always can.
            p.box((sx * (hf + .019), (y0 + y1) / 2, (zb + z_top) / 2),
                  (.078, y1 - y0 - .020, z_top - zb),
                  "oak_mid" if i % 2 else "oak_dark", bevel=0,
                  tint=.08, shade=.88 + rb.uniform(-.10, .10))
        # the floor beam and sill beam return along the cheek, as they do in
        # ref3 -- two strong horizontals across an otherwise blank side
        for (zc, hh) in ((Z_RAIL - (Z_RAIL - Z_SOF) / 2, Z_RAIL - Z_SOF),
                         ((Z_APRON + Z_SILL - .038) / 2, Z_SILL - .038 - Z_APRON)):
            p.box((sx * (hf + .055), (Y_TRIM + Y_WALL) / 2 - .04, zc),
                  (.055, Y_WALL - Y_TRIM - .08, hh), "oak_dark", bevel=0,
                  tint=.05, shade=.88)
        # NO WALL PLATE ALONG THE TOP OF THE CHEEK. THERE IS NO ROOM FOR ONE.
        # This was "a dark dashed line 0.83 m up the shingles", and it is the last
        # member on this piece that stood out of its own roof. A 0.16 x 0.10 beam
        # lay along the cheek plane with its top at z_ck - 0.005, i.e. 5 mm under
        # the roof plane WHERE THAT PLANE CROSSES x = hf -- but the plane rakes at
        # 61 deg, so over the beam's outboard half it fell 0.08 * tan61 = 144 mm
        # while the beam stayed level. Measured on the built mesh: the outer top
        # corner stood 45 mm PERPENDICULAR above the deck's top face, which is
        # inside the shingle layer (butt faces sit 42-70 mm out), so the beam broke
        # the surface wherever a tab lay low -- 132 cm2 of oak_dark on the A
        # variant and 269 on C was the topmost thing a ray from above could hit,
        # in dashes, up both slopes of every dormer.
        # It cannot be rescued by cutting or sinking it. Anything projecting past
        # the boarding's own face (hf + 0.058) has to clear the deck underside
        # there, which is 151 mm below z_ck: a "wall plate" 130-220 mm under the
        # roof line is a frieze rail, not a plate. The cheek needs no such member
        # anyway -- ref3's dormer cheeks are plain vertical boarding running up
        # under the barge, the slab's top edge already lies on the roof plane (see
        # `prof`), and the floor and sill beams already return along the side as
        # the two horizontals. So the plate is gone: 24 tris back, and the roof is
        # roof all the way to the barge.
        # VALLEY COVER, ON THE VALLEY, FOR THE WHOLE LENGTH OF IT.
        # It used to run from the top of the cheek (x = hf) to x = 0.13, which is
        # neither end of anything: the valley -- the line where this roof plane
        # cuts the 52 deg field -- starts out at the rake edge (x = hs) and runs
        # to the ridge, so a strip starting 150 mm inboard of it and stopping
        # short at both ends read as a dark plank lying across the middle of the
        # shingles. That is the "beams that make no sense" on the roof. Now it is
        # struck along the real intersection: solve the two planes for each rake
        # position v, and run from just inside the rake edge up UNDER the ridge
        # cap (they must not meet head-on at x = 0, mirrored, or their long faces
        # coincide under it).
        # THE TOP END NOW ACTUALLY REACHES THE CAP. It stopped at x = 0.130 on a
        # cap that is 0.17 across, i.e. reaches x = 0.085 -- so the two covers
        # ended 45 mm out from under it and 147 mm below its soffit, and their end
        # faces were in the open on the shingles: the same "stick lying on the
        # roof" the ridge itself was fixed for. At x = 0.060 the end is 25 mm
        # inside the cap's edge and its outer face runs into the cap's underside,
        # and the two sides still stay 120 mm apart.
        v_lo, v_hi = .10, (hs - .060) / COS_D
        pv = lambda v: (sx * (hs - v * COS_D),
                        Y_WALL + v * (SIN_D / TAN_R) + .010,
                        Z_ROOF + v * SIN_D + .015)
        p.beam(pv(v_lo), pv(v_hi), .26, .05, MOSS,
               bevel=0, tint=.05, up=(sx * SIN_D, 0, COS_D), shade=.42)
        # NO SOAKER COURSE AT THE CHEEK BASE. There is no room for one and there
        # never was: the wedge between the 52 deg field and this roof's own rake
        # overhang is only ~0.1 m high at the cheek and closes to nothing at the
        # valley, so two 0.17 m tabs lying on the field at 52 deg came straight up
        # THROUGH the dormer's own shingles and hung out past the rake edge -- two
        # green nubs sticking out of the roof on each side. The cheek's top edge
        # already runs exactly along the field's surface (see `prof` above), so the
        # junction closes by construction, the main roof's own courses lap over it,
        # and SM_Dormer_Flash_Valley is the piece that dresses it if a level artist
        # wants it dressed.

    # ridge cap + apex block. The cap is 0.17 across, so it covers the 53 mm the
    # two shingle fields now stop short of the ridge, and the 0.26 gap between
    # the two valley beams. Bevel dropped: 32 tris, at the top of the piece.
    # front end at -0.138, not -0.170: at -0.170 it was 10 mm past PROUD_MAX and
    # finish() flattened the cap's whole front end onto y = -0.16 -- four verts
    # crushed onto one plane, on the most visible line of the piece.
    # AND THE BACK END IS CUT ON THE 52 DEG FIELD, NOT SQUARED OFF IN MID-AIR.
    # ridge_y1 = Y_WALL + d_roof - 0.10 stopped the cap at y = 1.832 when the
    # dormer ridge dies into the field at y = 1.932: 100 mm short, and because
    # the cap is a level timber and the field climbs at 52 deg, its blunt end
    # face floated 55 mm above that plane -- the same "stick lying on the roof"
    # the cap was lengthened to cure, moved to the other end. A ridge that dies
    # into a field is CUT ON the field, so solve the plane for the cap's own
    # underside and top (z = Z_ROOF + (y - Y_WALL) * TAN_R) and rake the end
    # between them, 25 mm past the plane so the end grain is buried inside the
    # main roof's own deck instead of touching it. Same 12 tris as the beam.
    z_cap0, z_cap1 = apex - .0725, apex + .0125
    y_of = lambda z: Y_WALL + (z - Z_ROOF) / TAN_R + .025
    p.prism([(ridge_y0 - .008, z_cap1), (ridge_y0 - .008, z_cap0),
             (y_of(z_cap0), z_cap0), (y_of(z_cap1), z_cap1)],
            .17, "oak_mid", axis='X', bevel=0, tint=.06, shade=.98)
    # THE APEX BLOCK IS ALSO THE KING POST'S HEAD BEARING, so it has to reach
    # back far enough for the king post to land IN it. At 0.155 deep it ran
    # y -0.1425..0.0125, i.e. it stopped 12 mm in FRONT of the king post's own
    # front face (0.025) -- so the one member in the gable that has to die into
    # the apex had nothing at the apex to die into, and stopped 100 mm short of
    # the bargeboard's inner apex instead, leaving a bare plaster V above it
    # (see the king post below). Its face is unmoved at y = -0.1425, so the
    # silhouette and its grip on the barge are exactly as before; it now runs
    # back to y = 0.0825, which is 57 mm of overlap with the post, 22 mm clear
    # of the tympanum's back face and 20 mm behind the deepest gable board.
    p.box((0, Y_BARGE + .120, apex - .055), (.15, .225, .19), "oak_dark",
          bevel=0, tint=.05)
    p.box((0, Y_BARGE + .085, apex + .075), (.055, .08, .075), "oak_pale", bevel=0,
          tint=.05, rot=(0, 45, 0))

    # GABLE INFILL, CUT TO THE BARGEBOARD'S ACTUAL INNER EDGE.
    # x_t/z_t used to be guessed as barge_w/SIN_D in from the rake, which on the
    # 1m5 is 69 mm short in x and 124 mm short in z of where the plank's inner
    # edge really runs -- so the tympanum and its boarding stopped short of the
    # barge all the way up both rakes and left a raking dark wedge, plus a dark
    # V of it at the apex, reading as a gap in the gable. The barge's inner edge
    # is just its own roof-edge line shifted in by its plank depth (see _barge),
    # so solve that line properly and lap the infill 20-30 mm UNDER the plank.
    bb = barge_w * .76                            # _barge's plank depth at a notch
    dxb, dzb = SIN_D * bb, COS_D * bb
    x_t = hs - dxb - dzb / TAN_D                  # inner edge, at the eave line
    z_t = Z_ROOF + (hs - dxb) * TAN_D - dzb       # ... and at x = 0
    barge_in = lambda x: Z_ROOF + (hs - dxb - abs(x)) * TAN_D - dzb
    # the infill's base runs 45 mm BELOW the eave line, buried behind the head
    # beam: it used to sit exactly on z = Z_ROOF, along with the head beam's top
    # face and the backing plate's top face -- three coplanar faces on one line
    if var.get("plaster_gable"):
        p.prism([(-x_t - .03, Z_ROOF - .045), (x_t + .03, Z_ROOF - .045),
                 (0, apex - .03)],
                .07, "plaster", axis='Y', at=(0, Y_FACE + .05, 0), bevel=0,
                tint=.05)
        # KING POST -- IT LANDS AT BOTH ENDS NOW.
        # "the vertical wood beam in the center doesn't reach the top leaving an
        # empty white gap": it ran Z_ROOF..z_t - 0.100, i.e. from the head beam's
        # top FACE to 100 mm under the bargeboard's inner apex, so
        #   * its head stopped 100 mm below the apex and 383 mm below the apex
        #     block's foot, and what filled that 110 x 100 mm triangle -- 52 cm2
        #     of it, dead centre at the top of the gable -- was bare plaster
        #     tympanum. A front-on ray at x = 0 struck M_plaster at z 2.990;
        #   * its foot sat exactly ON z = Z_ROOF, which is the head beam's top
        #     plane: a butt joint, not a housing, on a post that carries the apex.
        # A king post runs from the tie beam to the ridge, so this one now does:
        # its foot is housed 60 mm down inside the head beam and its head 95 mm
        # up inside the apex block (which was deepened to receive it, above) and
        # on into the ridge cap. Everything above the barge's inner apex is
        # covered by the barge itself up to z = apex - 0.099 and by the apex
        # block from z = apex - 0.150, so the two overlap and no part of the
        # added length is ever in open air. Set BEHIND the apex arch (it used to
        # stand 40 mm proud of it, so the arch read as something threaded behind
        # a post rather than the member spanning the gable). The two raking
        # struts that used to flank it are gone: with the arch in place they made
        # three overlapping trusses in one small tympanum, which is what made
        # this variant's gable read as a tangle of broken curves.
        z_kp0, z_kp1 = Z_ROOF - .060, apex - .055
        p.box((0, Y_FACE + .055, (z_kp0 + z_kp1) / 2), (.11, .10, z_kp1 - z_kp0),
              "oak_dark", bevel=0, tint=.05)
    else:
        p.prism([(-x_t - .03, Z_ROOF - .045), (x_t + .03, Z_ROOF - .045),
                 (0, apex - .03)],
                .06, "oak_dark", axis='Y', at=(0, Y_FACE + .055, 0), bevel=0,
                tint=.04, shade=.55)
        # RAKED, so every board dies under the plank at its own x -- see _boards.
        # Squared off, each one stopped at its LOW edge and the run sat 171 mm
        # below the barge's inner edge at its own centreline (centre board 2.833
        # against an inner apex at 3.004), which showed as a stepped triangle of
        # dark backing under the whole rake. The two end boards used to be
        # dropped entirely for being too short square, leaving the corners of the
        # gable bare as well; cut on the line they are wedges and they stay.
        _boards(p, -x_t - .02, x_t + .02, Z_ROOF - .03,
                lambda x: min(z_t + .02, barge_in(x) + .02),
                Y_FACE + .002, .032, "oak_dark", 7, seed=seed * 17,
                tint=.05, shade=.72, gap=.008, rake=True, peak=0.0)
    # THE ARCHED BRACE UNDER THE GABLE APEX -- the other half of the brief's
    # "broad shallow arc of timber spanning under each gable apex and under each
    # dormer window". Springs from behind the bargeboard on both rakes (the
    # springing x is set on the barge's own inner edge, so each end runs in
    # behind the plank rather than stopping in open tympanum), crown low enough
    # that the pierced motif still sits above it.
    zs = Z_ROOF + .10
    xs = hs - COS_D * ((zs - Z_ROOF + COS_D * barge_w * .66) / SIN_D) \
            - SIN_D * barge_w * .66
    _arc(p, (-xs - .032, zs), (xs + .032, zs), .40, .090, Y_FACE + .020, .070,
         "oak_dark", segs=5, bury=.055, shade=.88)
    # ... and the pierced motif only where there is bare infill for it to be cut
    # into. On the plaster-tympanum variant the king post stands exactly where it
    # goes, so the two were stacked on the same 100 mm of gable: post, arch and
    # motif all fighting for the apex. That variant gets the framed tympanum ref1
    # draws, and nothing else.
    if not var.get("plaster_gable"):
        _pierce(p, 0.0, z_t - .30, Y_FACE - .02, kind=var.get("pierce", 0))

    p.wobble(.007)
    return p.finish()


def gabled_a():
    return _gabled("SM_Dormer_Gabled_1m2_A", 1.22, .33,
                   dict(crest=0, head_teeth=False, pierce=0, apron_boards=7,
                        pegs=3, dentil=.185, barge=.19, dags=12,
                        flank_boards=3),
                   seed=1)


def gabled_b():
    return _gabled("SM_Dormer_Gabled_1m2_B", 1.22, .33,
                   dict(crest=1, head_teeth=False, pierce=1, apron_boards=6,
                        pegs=4, dentil=.20, barge=.205, flank_boards=4,
                        dags=10),
                   seed=2)


def gabled_c():
    return _gabled("SM_Dormer_Gabled_1m2_C", 1.22, .33,
                   dict(crest=None, pierce=2, plaster_gable=True, apron_boards=8,
                        pegs=2, dentil=.175, barge=.18, face_boarded=True,
                        dags=13, flank_boards=3),
                   seed=3)


def gabled_large():
    return _gabled("SM_Dormer_Gabled_1m5", 1.48, .26,
                   dict(crest=None, pierce=1, apron_boards=7, pegs=4,
                        dentil=.19, barge=.215, flank_boards=3, cheek_boards=5,
                        dags=11),
                   seed=4)


# --------------------------------------------------------- shed dormer -------
def shed():
    """Roof dormer: plant it mid-slope. Squat, one shallow swept roof, deep
    boarded cheeks -- ref2's left wing."""
    wf = 1.60
    hf = wf / 2
    # THE EAVES OVERHANG NEEDS MORE THAN PROUD_MAX, SO THE PIECE DECLARES ITS
    # OWN. At over_y = 0.075 (all the default 0.16 allowance can carry, once the
    # starter course's 35 mm drip is counted) the roof edge landed BEHIND the
    # head beam's own front face, so there was no overhang at all: the fascia had
    # to sit outboard of the roof to be seen, which is why it read as two beams
    # lying on top of the roof rather than as an eave. spec.py explicitly allows
    # a piece to declare a bigger allowance and be validated against it, and
    # nothing in the kit abuts this piece's front -- it is planted mid-slope --
    # so it declares proud=0.30 and gets the reference's "big overhang all round".
    over_x, over_y = .17, .20
    hs = hf + over_x
    # z_eave 1.58, not 1.52. The band between the window head (1.33) and the
    # roof plane has to hold the window's head casing, the head beam and a
    # fascia deep enough to read as one -- at 1.52 it held 190 mm and the
    # fascia had to hang over the glass to be seen at all. 60 mm more, and the
    # window keeps a visible head trim, the beam keeps its depth and the eave
    # clears both. The piece stays squat (1.60 wide, eave at 1.58).
    z_eave = 1.58                       # head beam top = shed roof at Y=0
    d_roof = (z_eave - Z_ROOF_SHED) / (TAN_R - TAN_S)
    D = d_roof + .10
    top = z_eave + TAN_S * D
    # z-max has to clear the shingle relief standing off the boarding, or
    # finish() flattens the top course onto the seam
    p = _Part("SM_Dormer_Shed_1m6", budget="dormer", proud=.30,
             seams=dict(x=(-HB, HB), y=(0, D), z=(0, top + .12)))
    r = rng(p.name)

    # BASE OF THE FACE. NO SHINGLES ON IT.
    # "SM_Dormer_Shed_1m6.001 is showing shingles by the window": this band is
    # why. There used to be a row of seven shingle_moss tabs across the FRONT
    # FACE at z 0.15-0.31, standing 12 mm proud of it, called apron flashing and
    # meant to be buried. They are not buried: the assembler sinks this piece so
    # that Z_ROOF_SHED lands on the roof surface AT THE FRONT PLANE, and in front
    # of that plane the slope falls away downhill -- so everything from z = 0.30
    # up is in clear view, and what showed was a course of roof shingles stuck on
    # the wall a few hundred mm under the sill. Roof shingles belong to the roof.
    # The band now reads as the bottom of the dormer's own wall: a WATER-TABLE
    # BOARD at the junction with the plaster carried down behind it, which is the
    # honest detail and cannot be mistaken for roofing.
    p.plate((0, (Y_FACE + Y_BACK) / 2, Z_ROOF_SHED / 2 + .02),
            (wf, Y_BACK - Y_FACE, Z_ROOF_SHED + .04), "oak_dark", tint=.03, shade=.6)
    # The apron board runs from below the roof line right up into the sill rail,
    # so there is no recessed strip between them to read as a slot, and it sits
    # 30 mm behind the rail's face and 18 mm behind the posts' -- never level with
    # either, which is what would fight.
    p.box((0, .015, (Z_ROOF_SHED - .060 + Z_APRON + .020) / 2),
          (wf + .05, .170, Z_APRON + .020 - Z_ROOF_SHED + .060),
          "oak_mid", bevel=.012, seg=1, tint=.06, shade=.94)

    # ONE BACKING PLATE, behind everything, exactly as the gabled dormer now
    # does it -- the four laced plates it replaces put 632 cm2 of coincident
    # surface into this piece on their own (the apron plaster plate's top face
    # landed on the sill rail's underside, and the bands shared faces where they
    # lapped).
    hbk = hf - .03
    p.plate((0, .280, (.10 + z_eave - .035) / 2),
            (hbk * 2, .12, z_eave - .035 - .10), "plaster_dim",
            tint=.03, shade=.80)
    # THE SAME TWO SLOTS AS THE GABLED DORMER, CLOSED THE SAME WAY (see the long
    # note there): the jamb plates' feet run 22 mm down inside the sill rail
    # instead of stopping 8 mm above it, and their heads run 76 mm past the opening
    # head, which buries them inside the head beam -- so neither end of either
    # plate faces open air with the backing behind it. Their inner edges run 22 mm
    # under the glazing frame's outer edge (WIN_IN). The plaster
    # apron plate that used to sit below the sill is gone: the apron board above
    # covers that whole band and covers it wider, so the plate was a panel behind
    # a panel.
    # ... and the plate that used to sit ABOVE the opening head is gone with them.
    # On a piece this squat the head beam's soffit is at Z_HEAD + 0.040 and the
    # glazing frame's head reaches Z_HEAD + WIN_TOP = 1.397, so the two overlap and
    # there is no band left for a plate to fill: it was a panel buried inside a
    # beam, and its foot was the 14 mm slot.
    for (z0, z1, x0, x1, dy) in ((Z_SILL - .060, Z_HEAD + .076, -hf + .156, -WIN_IN, 0.0),
                                 (Z_SILL - .060, Z_HEAD + .076, WIN_IN, hf - .156, 0.0)):
        if z1 - z0 > .02:
            p.plate(((x0 + x1) / 2, Y_FACE + .024 + dy, (z0 + z1) / 2),
                    (x1 - x0, .048, z1 - z0), "plaster", tint=.05, shade=1.03)
    _window(p, lit=True)
    # corner posts + sill + head beam
    for sx in (-1, 1):
        # 12 mm in from the box corner, so the post's outer face is buried in
        # the cheek slab instead of sharing its plane
        # ... and its head dies 70 mm INSIDE the head beam, exactly as the gabled
        # dormer's posts now do and for exactly the same measured reason: post top
        # and beam top were both on z = z_eave = 1.580, with the post entirely
        # inside the beam in y (-0.088..0.122 against -0.105..0.145), so the
        # post's 0.128 x 0.178 top quad lay on the beam's own. 226 cm2 -- the
        # biggest single pair anywhere in the family -- at 0.55 mm, i.e. ONE
        # wobble outside the 0.5 mm gate, and ray-sampled 20% reachable. 140 mm
        # of housing instead, no new triangles, nothing visible moved.
        z_top_post = z_eave - .070
        p.box((sx * (hf - .092), Y_POST + .105, (Z_ROOF_SHED + z_top_post) / 2 - .05),
              (.16, .21, z_top_post - Z_ROOF_SHED + .10), "oak_dark", bevel=.016,
              seg=1, tint=.05)
    # sill rail: top 38 mm below Z_SILL so _window's projecting sill sits on it
    p.box((0, Y_TRIM + .155, (Z_APRON + Z_SILL - .038) / 2),
          (wf + .10, .26, Z_SILL - .038 - Z_APRON),
          "oak_mid", bevel=.014, seg=1, tint=.06, shade=1.05)
    for i in range(3):
        _peg(p, lerp(-.34, .34, i / 2.0), Y_TRIM + .008, Z_APRON - .05, r=.03, l=.085)
    # head beam soffit 40 mm above the window head, so the head casing shows as
    # a frame band under it instead of being swallowed whole
    z_hb = Z_HEAD + .040
    p.box((0, Y_TRIM + .12, (z_hb + z_eave) / 2), (wf + .13, .25, z_eave - z_hb),
          "oak_dark", bevel=.018, seg=2, tint=.05)
    # NO TOOTH COURSE HERE. On this piece the head beam lands 10 mm above the
    # window head, so there is no band for one: the course used to sit at
    # z 1.335-1.415 with its front 68 mm proud of the window's head trim, which
    # put a row of blocks hanging DOWN OVER THE GLASS -- you could see the lit
    # pane between the teeth. Its ends also stood inside the cheek boarding. The
    # piece already has a tooth course where a tooth course belongs, under the
    # roof fascia, so this was a second one doing the same job in a place that
    # could not hold it.
    # SPANDREL BRACES either side of the window: each springs from INSIDE the
    # corner post and dies INSIDE the head beam above. These were the two
    # floating crescents -- both ends on nothing, reading as two halves of a
    # broken arch -- and they are the most visible instance of "the arcs on the
    # dormer are broken" in the whole family.
    # THE SPRINGING IS THE CENTRE LINE, NOT THE EDGE OF THE TIMBER. At
    # hf - 0.085 = 0.715 the springing itself was inside the post (0.628..0.788),
    # but _arc lays its 105 mm band on the CONVEX side of that line and extends
    # the end 55 mm further along its own tangent -- and at the foot both of those
    # go outboard, so the corner of the band landed at x = 0.828: 40 mm past the
    # post's outer face, with 45 mm of it also in front of the cheek boarding
    # (which starts at y = 0.012) and therefore hanging against sky. A brace foot
    # showing outside the post it springs from is the same fault as the arcs that
    # crossed the gabled dormer's posts. Pull the springing 60 mm further in: the
    # band's outer corner comes back to x = 0.770, 18 mm inside the post's face
    # and 26 mm inside the boarding's, and the whole foot is buried in timber.
    for sx in (-1, 1):
        _arc(p, (sx * (hf - .145), Z_SILL + .045),
             (sx * (OW / 2 + .085), Z_HEAD + .115),
             .130, .105, Y_FACE - .022, .062, "oak_dark", segs=5, bury=.055,
             flip=(sx < 0), shade=.95)

    # cheeks: bounded below by the field, above by the shed plane
    for sx in (-1, 1):
        prof = [(-.02, Z_ROOF_SHED), (d_roof, Z_ROOF_SHED + d_roof * TAN_R),
                (-.02, z_eave - .02 * TAN_S)]
        p.prism(prof, CHEEK_T, "oak_dark", axis='X',
                at=(sx * (hf - CHEEK_T / 2), 0, 0), bevel=0, tint=.04, shade=.75)
        nb = 5
        # THE BOARDS ARE WEDGES THAT RIDE THE TWO PLANES, NOT UPRIGHT BOXES.
        # Every board used to take ONE height for its whole length -- the field at
        # its BACK edge for the bottom, the shed plane at its BACK edge for the
        # top -- and both of those are wrong at the FRONT by the run of the board:
        #   * the bottom of the front board sat at z 0.644 when the field at the
        #     front of the piece is at Z_ROOF_SHED = 0.30, so the boarding stopped
        #     0.34 m short of the roof line and left a stepped notch out of the
        #     corner of the dormer -- 127 cm2 of open sky beside the sill, which is
        #     the rest of "it shows roof in-between";
        #   * the top overshot the shed plane by TAN_S * (y1-y0) = 84 mm at the
        #     front, so the front board stood up THROUGH the piece's own roof deck
        #     and into its shingles -- the same fault the gabled dormer's wall
        #     plate had.
        # Cut as a prism on the two real planes, each board meets the roof at its
        # own y. Same four corners, same six faces, no extra tris.
        zf = lambda yy: Z_ROOF_SHED + (yy + .02) * d_roof * TAN_R / (d_roof + .02)
        for i in range(nb):
            y0 = lerp(0, d_roof * .92, i / nb) + .012
            y1 = lerp(0, d_roof * .92, (i + 1) / nb) - .012
            # 10 mm above the slab's own raked lower edge, so the slab shows as a
            # thin reveal under the boarding instead of the two sharing a plane
            zb0, zb1 = zf(y0) + .010, zf(y1) + .010
            zt0, zt1 = (z_eave + TAN_S * y0 - .022, z_eave + TAN_S * y1 - .022)
            if zt1 - zb1 < .05:
                continue
            # THE BOARDING LAPS THE CHEEK SLAB. This is where "a gap between the
            # plaster and the brickwork making it show roof in-between" actually
            # was on this piece, and on this piece it was a hole clean through:
            # the slab's outer face is on x = hf = 0.800 and the boarding started
            # at 0.815, so a 14 mm slot ran from z 0.53 to z 1.40 -- from below the
            # sill to above the window head, down BOTH sides of the window -- with
            # no geometry in it at any depth. A front-on ray cast at x = 0.806 came
            # out the back of the piece, 283 cm2 of it, and on an assembled roof
            # what you see through it is the main roof field. The board is 65 mm
            # thick instead of 30 and starts 20 mm INBOARD of the slab's outer
            # face, so slab and boarding overlap by 20 mm; the outer face is
            # unmoved at hf + 0.045 (SM_Dormer_Cheek_Board still lands on it in
            # demo()) and the inner face at hf - 0.020 sits 8 mm clear of the
            # corner post's outer plane and 10 mm clear of the backing plate's
            # edge, so it lands on no existing plane and adds no tris.
            p.prism([(y0, zb0), (y1, zb1), (y1, zt1), (y0, zt0)], .065,
                    "oak_dark", axis='X', at=(sx * (hf + .0125), 0, 0),
                    bevel=0, tint=.07, shade=.82 + r.uniform(-.05, .05))
        # NO SOAKERS ON THIS PIECE. "SM_Dormer_Shed_1m6.001 is showing shingles by
        # the window" survived the last round because of these: eight
        # shingle_moss tabs at x = +/-0.895, outboard of the cheek's own face at
        # 0.80, climbing z 0.62-1.52 -- straight up the outside of the piece past
        # the window (sill 0.55, head 1.33). They were struck on the 52 deg field
        # plane, so on the assembled roof they would lap the field beside the
        # cheek; but the field is not part of this piece, so as built they
        # cantilever into open air and land on nothing, and they are the only
        # shingles anywhere near the window. A soaker course is a JOINT dressing,
        # and this family already ships the piece whose whole job that is:
        # SM_Dormer_Flash_Valley, which a level artist lays along the junction
        # when they want it dressed. The cheek's own top edge already runs on the
        # field surface (see `prof` above), so the junction closes without them.

    # shed roof: boarding, coursed shingle, fascia planks with upturned ends
    ex, ey = (1, 0, 0), (0, cos(SHED_PITCH), sin(SHED_PITCH))
    org = (0, -over_y, z_eave - TAN_S * over_y)
    rake = (D + over_y) / cos(SHED_PITCH)
    # THE DECK IS ROOF MATERIAL, NOT TIMBER -- see the same change on the gabled
    # dormer. A brown deck showing in every slot between grey-green tabs, and
    # right along the front edge under the starter course, is most of what "the
    # green and brown shingles" was.
    # the deck's head stops 20 mm short of `rake`: its own 50 mm thickness tips
    # 9 mm further in y than its mid-plane, which put it 10 mm past the declared
    # y bound and got the two back corners cut flat
    _slab(p, org, ex, ey, [(-hs, 0), (hs, 0), (hs, rake - .020), (-hs, rake - .020)],
          mat=MOSS, t=.05, shade=.40, tint=.03)
    # v1 stops 35 mm short of the boarding's head, so the top course's jitter
    # and its lap skew stay inside the piece's declared y bound instead of being
    # clamped flat onto it
    _field(p, org, ex, ey, -hs + .01, lambda v: hs - .01, 0.0, rake - .035,
           seed=32, t0=.025)
    z0f = z_eave - TAN_S * over_y
    # VERGE BOARDS, AT THE ROOF EDGE, UNDER IT -- NOT TWO BATTENS LYING ON IT.
    # These used to run 85 mm INBOARD of the roof edge with their axis 55 mm ABOVE
    # the roof plane, so a 0.16 x 0.10 timber stood 105 mm out of the middle of
    # the shingle field on each side: in the demo they read as two sticks left
    # lying on the roof, which is exactly the "beams/rafters that make no sense".
    # A verge board caps the EDGE: outer face on the rake, top tucked under the
    # shingle butts that overhang it, body hanging below as a fascia -- the same
    # relationship the front fascia already has, so the three meet as one eaves
    # line all round.
    nz = (0.0, -sin(SHED_PITCH), cos(SHED_PITCH))     # roof plane normal
    for sx in (-1, 1):
        def _ax(yy, off=-.035):
            # 0.905 not 0.92: at 0.92 the board's outer face landed exactly on the
            # deck's own edge plane at x = hs, and two coincident faces 891 cm2
            # across is the single worst z-fighting pair the checker found in the
            # family. 15 mm inside it, so the deck and its starter course overhang
            # the verge the way they overhang the front fascia.
            return (sx * (hs - .065), yy + off * nz[1],
                    z_eave + TAN_S * yy + off * nz[2])
        p.beam(_ax(-over_y + .050), _ax(D - .060), .10, .19, "oak_dark",
               bevel=0, tint=.05, up=nz, shade=.96)
    # FRONT FASCIA: ONE CONTINUOUS CURVED MEMBER.
    # "the 2 beams at the top with the seam in the middle. Maybe it should
    # connect better as one piece and curve?" -- it was two straight beams
    # running out from x = 0 to each end, so they met in a butt joint dead centre
    # with a visible kink and a seam, and both halves lay in the same two y
    # planes so the joint fought as well. A swept fascia is one sawn plank, bent:
    # so it is one prism whose top and bottom edges are both curves, deepest at
    # the centre and flicking up at both ends. No joint exists to show.
    # It also now sits UNDER the roof edge instead of outboard of it: the deck
    # and the starter course overhang it by 35 mm, which is what makes it read as
    # a fascia. Both edges flick up at the ends -- the kit's swept eave.
    # AND IT NO LONGER HANGS OVER THE WINDOW. This is the other half of what
    # Shanee is seeing at this window: the plank was 185 mm deep, so its lower
    # edge sat at z = 1.254 -- 86 mm BELOW the window head at 1.33 and below the
    # head beam's own soffit at 1.34 -- and a tooth course hung 67 mm below that
    # again, straight across the glass. Ray-casting the front of the piece showed
    # the top 140 mm of the pane behind a picket fence of dentil blocks, which is
    # what read as a crenellated top to the window. There are only 190 mm between
    # the window head and the roof plane on a piece this squat, so the fascia is
    # cut to fit inside them: a 110 mm plank whose lower edge sits 11 mm above the
    # head beam's soffit at the centre and flicks 75 mm further up at each end
    # (the kit's swept eave, and it uncovers the head beam toward the corners) --
    # and the tooth course under it is gone, because there is no band left for one
    # to hang in and this piece is not short of trim.
    xe = hs + .005
    fbot = lambda x: z0f - .118 + .075 * (abs(x) / xe) ** 2.4
    prof_t, prof_b = [], []
    for i in range(12):
        u = (-1.0 + 2.0 * i / 11.0) * xe
        prof_t.append((u, z0f - .008 + .062 * (abs(u) / xe) ** 2.2))
        prof_b.append((u, fbot(u)))
    p.prism(prof_t + prof_b[::-1], .12, "oak_dark", axis='Y',
            at=(0, -over_y + .095, 0), bevel=0, tint=.05, shade=1.0)

    p.wobble(.007)
    return p.finish()


# -------------------------------------------------- cheek / flashing ---------
def cheek():
    """Boarded cheek extension: butt it behind a dormer to make a deeper one,
    or use two to build a custom-width dormer. Cheek plane on X=0, boards face
    +X. Bottom edge rides the 52 deg field, top edge rides the shed dormer's own
    22 deg roof, so the piece is a WEDGE that closes as the field climbs.
    Mirror in X for the other side.

    It used to be drawn as a quad from the field up to a HORIZONTAL top at
    Z=TOP -- but over 0.66 m the 52 deg field climbs 0.845, well past TOP, so
    that quad turned itself inside out and finish() then crushed 24 verts onto
    the declared z bound. Both faults are one fault: the declared shape and the
    declared bound did not describe the real piece.
    """
    L, TOP = 0.66, 0.60
    z_top = TOP + L * TAN_S                     # 0.867 -- the back of the wedge
    p = _Part("SM_Dormer_Cheek_Board", budget="dormer",
             seams=dict(x=(-.06, .34), y=(0, L), z=(0, z_top + .10)))
    r = rng(p.name)
    # back edge 12 mm short of L, and the top plate 30 mm short of it: wobble
    # does not fade on y, so geometry sitting exactly ON the y bound gets cut.
    p.prism([(0, .02), (L - .012, (L - .012) * TAN_R), (L - .012, z_top), (0, TOP)], CHEEK_T,
            "oak_dark", axis='X', at=(CHEEK_T / 2, 0, 0), bevel=0, tint=.04,
            shade=.8)
    nb = 5
    # THE BOARDS ARE WEDGES CUT ON THE SLAB'S OWN TWO EDGES, NOT UPRIGHT BOXES --
    # the same fault the shed dormer's cheek had, and it survived here.
    # Every board took ONE height for its whole run: its bottom from the slab's
    # raking lower edge at its BACK corner and its top from the upper edge at its
    # FRONT corner. Both are wrong at the other end by the run of the board, so
    # measured on the built mesh the front board's underside sat at z 0.172 where
    # the slab's lower edge under it is 0.027 -- 145 mm of open notch, 153 mm on
    # the next board -- and a staircase of four of them ran up the piece with the
    # slab (and, in place, the roof field) showing through underneath. The tops
    # stopped 53 mm under the slab's upper edge at the back the same way.
    # Cut as a prism on the two real edges, each board meets both at its own y:
    # same four corners, same six faces, no extra tris.
    yb = L - .012
    z_lo = lambda yy: lerp(.02, yb * TAN_R, yy / yb)      # slab's raking foot
    z_hi = lambda yy: lerp(TOP, z_top, yy / yb)           # ... and its head
    for i in range(nb):
        y0, y1 = lerp(0, L, i / nb) + .005, lerp(0, L, (i + 1) / nb) - .005
        zb0, zb1 = z_lo(y0) + .010, z_lo(y1) + .010       # 10 mm reveal of slab
        zt0, zt1 = z_hi(y0) - .012, z_hi(y1) - .012
        if zt1 - zb1 < .05:
            continue
        # AND IT LAPS THE SLAB INSTEAD OF STANDING 14 mm OFF IT. The slab's outer
        # face is x = 0.055 and the boarding used to start at 0.069, so the joint
        # down the whole piece was an open butt -- the fault both dormers were
        # fixed for and this piece kept. The board is 64 mm thick instead of 30
        # and starts 20 mm INBOARD of that face, so the two overlap by 20 mm; the
        # outer face is unmoved at 0.099 and the new inner face at 0.035 lands on
        # no existing plane. Costs no tris -- a prism is a prism.
        p.prism([(y0, zb0), (y1, zb1), (y1, zt1), (y0, zt0)], .064, "oak_dark",
                axis='X', at=(.067, 0, 0), bevel=0, tint=.07,
                shade=.85 + r.uniform(-.05, .05))
    # top plate following the shed plane, + a rafter end poking out at the front
    p.beam((CHEEK_T / 2, 0, TOP - .045),
           (CHEEK_T / 2, L - .030, z_top - .045 - .030 * TAN_S), .11, .09,
           "oak_mid", bevel=.012, seg=1, tint=.06)
    p.box((CHEEK_T / 2, .06, .10), (.028, .14, .13), "oak_dark", bevel=.012,
          seg=1, tint=.05)
    # soaker/flashing skirt lapping onto the field
    for i in range(4):
        yy = lerp(.08, L - .12, (i + .5) / 4)
        p.box((.115, yy, yy * TAN_R + .022), (.19, .20, .036), MOSS,
              bevel=0, tint=.09, rot=(-52, 0, 4),
              shade=.9 + r.uniform(-.06, .06))
    p.wobble(.006)
    return p.finish()


def flashing():
    """Dressed valley flashing for the +X cheek of any dormer: a lead-look
    upstand against the cheek and two laps of shingle soakers over the field.
    Origin at the front-bottom of the junction; roof rises +Y. Mirror in X."""
    L = 1.05
    # z-max has to contain an upstand that rides a 52 deg field for 1.05 m: it
    # was declared at 0.60 and finish() was crushing 0.97 m of geometry onto
    # that plane, which both destroyed the upstand and left a stack of
    # coincident faces there -- every one of this piece's reported pairs.
    p = _Part("SM_Dormer_Flash_Valley", budget="dormer",
             seams=dict(x=(-.02, .40), y=(0, L), z=(0, L * TAN_R + .30)))
    r = rng(p.name)
    # upstand against the cheek
    # far edge 12 mm short of L -- wobble does not fade on y, so an upstand
    # standing exactly on the y bound gets cut flat
    p.prism([(0, .015), (L - .012, (L - .012) * TAN_R + .015),
             (L - .012, (L - .012) * TAN_R + .225), (0, .225)],
            # MOSS at a dark shade, not `iron`: iron is #26241F, so a 1.05 m
            # upstand standing 0.21 out of a grey-green roof read as a black
            # blade laid across the shingles -- and the brief puts every roof
            # surface, flashing included, on shingle_moss. Dressed lead over
            # shingle is a dark grey-green, which is what this now is.
            .035, MOSS, axis='X', at=(.02, 0, 0), bevel=0, tint=.05, shade=.55)
    # Two laps of soakers. The upper lap stands 30 mm higher, not 12: the two
    # laps overlap in plan, and at 12 mm their faces measured as one plane.
    for lap in range(2):
        n = 4 - lap
        for i in range(n):
            yy = lerp(.06, L - .08, (i + .5) / n)
            p.box((.10 + lap * .155, yy, yy * TAN_R + .022 + lap * .030),
                  (.20, .215 - lap * .02, .038), MOSS, bevel=0,
                  tint=.10, rot=(-52, r.uniform(-2, 2), lap * 4),
                  shade=.88 + r.uniform(-.07, .07))
    # front apron end, turned down over the course below
    p.box((.14, .02, .068), (.30, .10, .10), MOSS, bevel=.010, seg=1, tint=.08,
          rot=(-18, 0, 0), shade=.86)
    # the fixing clip stays iron -- one small dark accent, not a black blade.
    # AND IT IS NOW WHOLLY ON THE UPSTAND IT CLIPS. At 0.24 tall, centred on
    # z = 0.28, it ran z 0.160..0.400 while the upstand's top edge at its own y
    # is 0.263: 137 mm of it stood clear above the only member it touches, an
    # iron blade cantilevered into open air over the shingles. A clip is a clip,
    # so it is 0.15 tall inside the upstand, 33 mm clear of its head and 27 mm
    # clear of its foot.
    p.box((.03, .03, .155), (.05, .11, .15), "iron", bevel=.008, seg=1, tint=.05,
          shade=1.05)
    p.wobble(.005)
    return p.finish()


# ------------------------------------------------------------------ build ----
def build():
    return [gabled_a(), gabled_b(), gabled_c(), gabled_large(), shed(),
            cheek(), flashing()]


# ------------------------------------------------------------------- demo ----
def _ctx_roof(x0, x1, y0, y1, z_roof=Z_ROOF, name="CTX_RoofField", zup=0.0,
              y_ref=Y_WALL):
    """Demo-only context: a patch of 52 deg shingle field. NOT a kit piece.
    The field crosses z_roof at y = y_ref (the recessed wall plane)."""
    p = _Part(name)
    ex, ey = (1, 0, 0), (0, S.COS_P, S.SIN_P)
    org = (0, y0, z_roof + (y0 - y_ref) * TAN_R)
    rake = (y1 - y0) / S.COS_P
    _slab(p, org, ex, ey, [(x0, 0), (x1, 0), (x1, rake), (x0, rake)],
          mat=MOSS, t=.06, shade=.40, tint=.03)
    # the context field is coursed exactly like the dormer roofs, which is the
    # point of the demo: the two must not read as different materials
    _field(p, org, ex, ey, x0, lambda v: x1, 0.0, rake, seed=91, t0=.03,
           shade=.94)
    # eave fascia + teeth along the front edge: only shows in the narrow gaps
    # between the dormer boxes, which is exactly where the reference shows it
    z0 = z_roof + (y0 - y_ref) * TAN_R
    p.beam((x0, y0 - .07, z0 - .09), (x1, y0 - .07, z0 - .09), .13, .18,
           "oak_dark", bevel=.014, seg=1, tint=.05)
    p.dentil((x0 + .06, x1 - .06), z0 - .235, y0 - .01, "oak_dark", step=.19,
             size=(.055, .08, .075), seed=93)
    ob = p.finish()
    ob.location.z += zup
    return ob


def _ctx_base(x0, x1, zup=0.0, y_st=0.82):
    """Demo-only: the stone storey the boxes jetty out over, the boxed jetty
    band under them, and the run of raking braces the reference shows under it.
    NOT kit pieces (the beams family owns the real jetty sill + braces)."""
    p = _Part("CTX_StoneBase")
    p.plate(((x0 + x1) / 2, y_st + .55, -1.30), (x1 - x0, 1.1, 2.4),
            "stone_dark", tint=.03)
    p.stones((x0, x1), (-2.5, -.30), y=y_st, depth=.10, mat="stone",
             mat_alt="stone_pale", mat_warm="stone_warm", course=.36, seed=5,
             wobble=.26, mortar=.022, r_bevel=.045, big=.22)
    # the boxed-out jetty the dormer boxes stand on
    p.box(((x0 + x1) / 2, (y_st - .13) / 2, -.13), (x1 - x0, y_st + .13, .26),
          "oak_dark", bevel=.016, seg=1, tint=.05, shade=.92)
    p.box(((x0 + x1) / 2, -.055, -.30), (x1 - x0, .17, .16), "oak_mid",
          bevel=.014, seg=1, tint=.06, shade=1.02)
    # raking braces from the stone face up to the jetty -- ref3 draws a whole
    # run of them, roughly one every 0.6 m
    n = max(1, int((x1 - x0) / 0.62))
    for i in range(n + 1):
        cx = lerp(x0 + .28, x1 - .28, i / max(1, n))
        p.beam((cx, y_st - .04, -1.05), (cx, .02, -.27), .11, .15, "oak_dark",
               bevel=.012, seg=1, tint=.05, shade=.88)
    ob = p.finish()
    ob.location.z += zup
    return ob


def demo():
    """Four gabled dormers stepping away along a wall head, a shed dormer
    planted higher up the slope behind them with its flashing pieces, all
    against a patch of context roof and stone. Compose it like the reference:
    the run reads as a rhythm, the shed dormer breaks the line."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []

    ZUP = 2.7                       # stand the assembly on the ground plane

    def place(nm, at, mirror=False):
        at = (at[0], at[1], at[2] + ZUP)
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = at
        if mirror:
            o.scale.x = -1
        out.append(o)
        return o

    run = ["SM_Dormer_Gabled_1m5", "SM_Dormer_Gabled_1m2_C",
           "SM_Dormer_Gabled_1m2_A", "SM_Dormer_Gabled_1m2_B"]
    xs = [3.0, 1.0, -1.0, -3.0]
    for nm, x in zip(run, xs):
        place(nm, (x, 0, 0))

    # shed dormer planted higher up the slope behind the run, with its flashing
    # and a deeper cheek on its uphill side
    sx0, sy = 0.0, 2.05
    sz = Z_ROOF + (sy - Y_WALL) * TAN_R - Z_ROOF_SHED
    place("SM_Dormer_Shed_1m6", (sx0, sy, sz))
    # The cheek board is a WEDGE: its bottom edge rides the 52 deg field and its
    # top edge the shed dormer's 22 deg roof, so it only fits where the gap
    # between those two planes is its own 0.60 -- solve for that y instead of
    # guessing 1.02, which stood it 0.21 PROUD of the shed roof and poked two
    # boards up through the dormer's own shingles in every demo render.
    y_cb = (1.58 - Z_ROOF_SHED - 0.60) / (TAN_R - TAN_S)
    for m in (False, True):
        sgn = -1 if m else 1
        place("SM_Dormer_Flash_Valley", (sx0 + sgn * .81, sy, sz + Z_ROOF_SHED), m)
        place("SM_Dormer_Cheek_Board", (sx0 + sgn * .845, sy + y_cb,
                                        sz + Z_ROOF_SHED + y_cb * TAN_R), m)

    # the field starts at the recessed wall plane, so the boxes stand clear of
    # it -- that gap IS the point of this family
    out.append(_ctx_roof(-4.15, 4.15, Y_WALL + .01, 3.60, zup=ZUP))
    out.append(_ctx_base(-4.5, 4.5, zup=ZUP))

    for nm in src:
        src[nm].location = (0, 40, 0)          # park the originals out of shot
    return out
