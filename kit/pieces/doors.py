"""Doors: the inn's front door, back door, cellar doors, the gabled porch that
shelters the main door, and the stone doorstep in front of it.

Measured off the reference crops (ref1:door, ref1:arch_door, ref3/ref2:porch):
  ref1 front door  -- round-arched boarded leaf, six boards over 1.1m tenoned
      into an arched head rail, DARK grooves between boards, and an arched
      amber-lit diamond-lattice light in the upper leaf (light ~0.5 of the leaf
      width, three diamonds across, sill just above mid height). Strap hinges
      lie ON the ledges; ring pull on the far stile.
  ref1 cellar arch -- wide round head, twin boarded leaves, diagonal ledge
      braces, a narrow lattice light on the meeting stile.
  ref2 back door   -- flat head, ledge-and-brace: five boards, two ledges and
      one diagonal, dark oak, plain iron.
  ref3 porch       -- the clearest form reference in the set. The porch is a
      BOX, not four legs: boarded dado to ~1.0m, diamond-lattice panel above it
      to the head, chunky corner posts, a carved name board, a boarded gable
      tympanum, wide barge boards with a run of cusped teeth off their inner
      edge, a pendant-dentil fascia under each eave, a pinnacle finial, and
      small shingles (~4 courses/m). Stone steps with a raking timber handrail
      on turned newels lead up to it.

Three of the leaves have a hand-worked sibling -- SM_Door_ArchPlank_1m_A_Rough,
SM_Door_ArchPlank_1m_B_Rough, SM_Door_FlatPlank_1m_Rough and
SM_Door_CellarDouble_1m_Rough -- with plank widths that vary hard, cupped and
bowed boards, ledges that are not parallel, wandering nails and worn edges. The
regular leaves are untouched and stay the family's default; see the section
headed THE ROUGH HALF OF THE FAMILY near the bottom of this file.

Conventions: door leaves are INSERTS -- footprint centred in X, Z=0 at the
bottom, outer face on Y=0, body to +Y, ironwork proud to -Y. Each is built
INSERT_CLEAR smaller than its OPENINGS entry; a level artist pushes it +REVEAL
into the wall (the demo does exactly that).

THE DEPTH LADDER OF A LEAF. Two opaque faces that land on the SAME plane and
overlap are what makes a renderer flicker (check_zfight.py measures the area),
and a boarded door is a stack of thin members so it is easy to do by accident.
Every solid in a leaf therefore sits on this ladder, and no two rungs share a
boundary: each member is either clear of its neighbour or buried several mm
inside it. Y grows INTO the door; -Y is towards the viewer.

    -0.078 .. -0.014   hinge pin / strap plate / ring pull        (ironwork)
    -0.035 .. +0.011   ledge            (46 mm, back buried in the boarding)
    -0.033 .. +0.022   THE BEAD: the light's frame, and the same 55 mm band bent
                       round an arched head. Part.glazing() lays it -- see below
    -0.029 .. +0.005   brace            (34 mm, set back 6 mm behind the ledges)
     0.000 .. +0.044   the boarding itself (thickness jitters, backs .038-.048).
                       A ROUGH leaf's boards bow out of that plane, and they now
                       bow ONE WAY ONLY -- proud, towards the viewer -- because
                       everything above this line on the ladder is buried BEHIND
                       the board face by 5-8 mm, and a board bowing inward
                       surfaced through it. Measured: 83 cm2 of the wicket bars'
                       backs against the boarding on SM_Door_ArchPlank_1m_B_Rough
    +0.012 .. +0.030   arch spandrel fill -- the wedge between an arched light's
                       ring and the square top of the hole cut for it. It used to
                       sit ON the boarding's own two planes (0.000 .. +0.044) and
                       it necessarily LAPS the boards, because each board's cut
                       is a rectangle of its own height: 50 cm2 of coincident
                       surface on SM_Door_ArchPlank_1m_A, front face and back
                       face both. Recessed 12 mm it reads as a rebate behind the
                       boards, which is what a fill piece looks like anyway
    +0.008 .. +0.050   springing rail -- behind the boards everywhere they
                       exist, and on a GLAZED leaf it stops inside the bead
                       instead of carrying on across the glass
    +0.038 .. +0.050   leading, one diagonal family -- struck over the WHOLE
                       light and clipped to the pane, so every quarry meets the
                       edge as a partial quarry
    +0.036 .. +0.048   leading, the OTHER diagonal family. Two rungs, not one,
                       because Part.glazing() lays both families on a single
                       plane and every crossing then puts two identical faces
                       0.000 mm apart: 1.59 cm2 a crossing, 152 cm2 across the
                       five glazed leaves, all of it ray-reachable. Stepped
                       2 mm by _lead_relief -- see it for the arithmetic
    +0.052 .. +0.064   glass (1.70 mm clear of the leading -- see LEAD_W)
    +0.074 .. +0.086   the fanlight pane, in an arched head only
    +0.100 .. +0.138   dark backing slab -- its FRONT face is 36 mm behind the
                       deepest thing in front of it, so slab and boarding never
                       share a plane. It used to sit exactly on the plane of the
                       board backs, which was the family's single biggest source
                       of z-fighting. The clearance is generous and not 3 mm
                       because this face is a metre-wide quad and p.wobble()
                       tilts it: a big panel's plane wanders far more than a
                       plank's does.

THE GLAZING IS NOT BUILT IN THIS FILE ANY MORE. util.Part.glazing() builds
frame + glass + leading in ONE call, and it makes the three faults five families
kept re-reporting impossible by construction: the pane is cut OVERSIZE and the
bead laps its edge, so glass can never stop short of its opening; the leading is
struck over the WHOLE opening and clipped to the pane, so every diamond meets
the edge as a partial diamond instead of floating in mid-pane; and the bead
oversails what it sits in rather than butting to it, so no line can open round
it. Read its docstring -- it is the contract. The local pane / light-frame /
_lattice ladder that used to live here is GONE from every glazed leaf, and with
it the reason five families diverged: each had forked the same code and re-grown
the same bugs.

AND IT IS LAID AFTER p.wobble(). Every glazed leaf calls its _light_* function
BELOW its wobble call, so the glazing stack alone is not warped. This is the
other half of the same argument: glazing() builds a nine-rung ladder inside 100
mm of depth -- pane 12 mm, leading 12.6 mm, 1.7 mm of air between them -- and a
7 mm coherent noise field warps a metre-wide pane +/-2 mm across the bars sitting
on it, which is more than the air gap. Measured before: 302 cm2 of glass against
its own leading over three leaves. The unit cannot come loose from the leaf by
being left rigid, because the bead LAPS 44 mm onto the boarding rather than
butting to it -- that lap is the joint, and it absorbs the leaf's wobble.

WHY THE BEAD STANDS 33 mm PROUD, which is arithmetic and not taste.
glazing() lays its whole stack relative to the pane and its frame is 55 mm deep,
so from the bead's front face to the back of the glass is 55 + 2.6*lead + 6 mm
= 97 mm. A leaf's boarding is only 44 mm thick, and the dark backing slab has to
stay clear BEHIND the glass or the pane is built inside an opaque panel and
never shows (which is exactly what happened to the cellar light once). So either
the bead stands proud or the slab goes back; both, here. The bead's BACK face is
the number that pins it: at +0.022 it is 18 mm clear of the shallowest board
back (the boarding jitters 38-48 mm thick), and the bead LAPS 44 mm onto that
boarding all round, so those two faces really do overlap and really would fight
if they met. Nothing between +0.030 and +0.056 is available to it.

The porch is a projecting piece: one 2m bay of POSTS in X, standing on the
ground at Z=0 -- but its ROOF is much bigger than that, because in ref3 the
porch is nearly all overhang. The roof reaches out to Y=-1.78 (0.385 past the
front post face) and sideways to X=+/-1.20 (0.405 past the side post faces),
with exposed rafter tails under the eaves and purlin ends up the gable filling
the gap that opens under it. So it oversails its 2m bay by 0.3 either side and
declares its X bounds as the roof, not the grid. At the kit's 52 deg pitch that
makes it top out near 3.6m plus finial, so it wants a bay whose wall carries on
well above H_GROUND (ref2's tall stone entrance bay) rather than a jettied
storey directly over it.

The steps' TOP TREAD IS THE FLOOR PLANE: sink the piece 0.42, or stand the
building on a 0.42 plinth as the demo does.
"""
import bpy
from math import pi, sin, cos, tan, sqrt, radians, floor, asin, acos, ceil
from mathutils import Matrix, Vector

from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "doors"
COLLECTION = "08_Doors"

CL = S.INSERT_CLEAR
TAN_P = S.SIN_P / S.COS_P

# ---- the glazed light: ONE ladder, and Part.glazing() lays all of it --------
# See "THE GLAZING IS NOT BUILT IN THIS FILE ANY MORE" in the module docstring.
# These are the numbers every glazed leaf hands the primitive; the asserts below
# are the two inequalities the last several rounds kept rediscovering.
LEAD_W = .014            # lead section: 12.6 mm across the pane, near square.
                         #   ref1 measures the leads at ~12 mm, and it is also
                         #   what keeps the stack shallow enough to fit a leaf.
                         #   THIS NUMBER SETS THE GLASS-TO-LEAD AIR GAP, which is
                         #   arithmetic: glazing() centres the leading `lead` in
                         #   front of the pane and makes it lead*0.9 thick against
                         #   a 12 mm pane, so the gap between the lead's BACK face
                         #   and the glass FRONT face is 0.55*lead - 6 mm. At 13 mm
                         #   that is 1.15 mm, and the whole leaded net of three
                         #   leaves measured as coincident surface at 0.5 mm
                         #   (SM_Door_CellarDouble_1m 135 cm2, _Rough 92,
                         #   SM_Door_ArchPlank_1m_A 75) because p.wobble() then
                         #   warped the metre-wide pane +/-2 mm across the bars.
                         #   14 mm gives 1.70 mm, and the glazing is now laid
                         #   AFTER wobble (see the leaves) so nothing warps it.
D_GLAZE = .058           # the `depth` every glazed light in this file passes.
                         #   It fixes the whole ladder:
                         #     bead      -0.033 .. +0.022
                         #     leading   +0.038 .. +0.050
                         #     glass     +0.052 .. +0.064
FR = .040                # bead face width
OV = .004                # bead oversail term
REACH = FR + OV / 2      # .042: how far the bead really reaches past its own
                         #   aperture edge -- the number every call site needs
LAP = REACH + .002       # .044: how far the bead laps onto the BOARDING, i.e.
                         #   past the edge of the hole cut for the light. The
                         #   bead's inner edge lands exactly on that cut edge, so
                         #   no strip of board shows between bead and glass and
                         #   no line can open between bead and boarding.
REB = .032               # pane rebate -- two inequalities pin it, both asserted
Y_SLAB = .119            # centre of the dark backing slab -> 0.100 .. 0.138
# (1) the pane's lip must out-run glazing()'s own reveal (glass front to bead
#     back = lead*2.6 - 6 mm) or an oblique view finds bead where glass should be;
# (2) it must stay UNDER the bead, or the lip shows past the bead's outer edge
#     instead of being buried in it.
assert REB >= LEAD_W * 2.6 - .006, "pane rebate must out-run glazing()'s reveal"
assert REB <= REACH - .001, "pane lip must stay buried under the bead"

# Ledge lines that BOTH halves of the family share, regular and rough, because
# they are the ones a member above them has to be measured against: B's top
# ledge must stay clear of its barred wicket at 1.74, and C's deep mid rail must
# stay clear of the bead under its light at 1.256.
Z_LEDGE_B = (.38, 1.08, 1.44)
Z_RAIL_C = 1.15
# The rough leaves' springing rail sits deeper than the regular ones' 0.008,
# because a hand-worked board BOWS up to 7 mm out of the leaf plane and a rail
# only 8 mm behind the board face then surfaces through it.
Y_RAIL_R = .016


def _ap(light):
    """Aperture to hand glazing() for a light of size `light` (width or height).

    glazing() laps its bead `REACH` past the aperture and 2 mm INTO it, so an
    aperture of light + 4 mm shows exactly `light` of glass and puts the bead's
    inner edge dead on the edge of the hole cut in the boarding."""
    return light + .004


# ============================================================ small helpers ==
def _ins(key):
    o = S.OPENINGS[key]
    return o["w"] - 2 * CL, o["h"] - 2 * CL


def _arch_geo(W, H):
    r = W / 2.0
    return r, H - r


def _arch_z(x, r, spring):
    d = r * r - x * x
    return spring + (sqrt(d) if d > 1e-9 else 0.0)


def _arch_outline(W, H, segs=15):
    """CCW (x,z) outline of a round-arched leaf."""
    r, spring = _arch_geo(W, H)
    pts = [(-r, 0.0), (r, 0.0), (r, spring)]
    for i in range(1, segs):
        a = pi * i / segs
        pts.append((r * cos(a), spring + r * sin(a)))
    pts.append((-r, spring))
    return pts


def _arc_band(p, y, thick, r_out, r_in, spring, mat, segs=14, tint=.05,
              shade=1.0, bevel=0.0):
    """A smooth half-annulus board: the arched head RAIL the boards die into,
    and the ring round an arched light. One prism, so the arch silhouette does
    not read as a ziggurat of voussoirs."""
    outer = [(r_out * cos(pi * i / segs), spring + r_out * sin(pi * i / segs))
             for i in range(segs + 1)]
    inner = [(r_in * cos(pi * i / segs), spring + r_in * sin(pi * i / segs))
             for i in range(segs + 1)]
    p.prism(outer + inner[::-1], thick, mat, axis='Y', at=(0, y, 0),
            bevel=bevel, seg=1, tint=tint, shade=shade)


def _spandrel(p, lr, lsp, zt, y0, thick, mat, ring_out=.050, side=.010,
              segs=7, tint=.075, shade=.94):
    """The two corners between an ARCHED light's ring and the square corner of
    the hole cut in the boarding for it.

    `_boards`' hole is a z-SPAN per board -- a rectangle -- so above an arched
    light the boarding is always cut higher than the arc, and the void between
    the arc and that cut opened onto the dark backing slab. On the front door it
    measured as two black wedges either side of the light's crown, and beside the
    stiles it was a slot down the whole height of the light. This fills the wedge
    with the same board material at the same depth, so the boarding reads as
    continuous right up to the ring.

    `lr` light half-width / arc radius, `lsp` its spring height, `zt` the top of
    the rectangular cut, `ring_out` how far under the ring's outer arc to sit."""
    R = lr + ring_out
    dz = clamp(zt - lsp, 0.0, R)
    t_top = pi / 2 if dz >= R else asin(dz / R)
    for sgn in (-1, 1):
        xe = sgn * (lr + side)
        if abs(xe) >= R:
            continue
        t_side = acos(abs(xe) / R)
        if t_top - t_side < radians(2.0):
            continue
        pts = [(xe, zt)]
        for i in range(segs + 1):
            t = lerp(t_top, t_side, i / segs)
            pts.append((sgn * R * cos(t), lsp + R * sin(t)))
        p.prism(pts, thick, mat, axis='Y', at=(0, y0 + thick / 2, 0), bevel=0,
                tint=tint, shade=shade)


# ------------------------------------------------------------ glazed lights --
Y_LEAD_LAP = .0020       # depth step between the two diagonal came families


def _lead_relief(p, faces, dy=-Y_LEAD_LAP):
    """Break the coplanar lap where two diagonal CAMES CROSS each other.

    Part.glazing() lays BOTH diagonal families of the leaded net on ONE plane
    (y = depth - lead) with one section, so at every crossing the two bars
    present the SAME front face and the SAME back face to each other. Measured
    at 0.5 mm with a ray-reachability harness (separation taken across the
    clipped overlap, controls in both directions): 12.6 x 12.6 mm = 1.59 cm2 per
    crossing, 0.000 mm apart -- exact coincidence, not a near miss -- 36
    crossings on SM_Door_CellarDouble_1m alone, and 152 cm2 over the five glazed
    leaves, ALL of it ray-reachable on the viewer's side of the light. That was
    91% of everything reachable in this family; the leaves' own depth ladder was
    clean.

    It cannot be fixed from glazing()'s parameters -- nothing in the signature
    separates the two directions, and "square" leading crosses the same way --
    and the primitive is shared by five families, so it is not a piece module's
    to fork. The lap is therefore broken HERE, on the faces glazing() hands
    back: one diagonal family is lifted `dy` towards the viewer, which is what a
    soldered came lap looks like anyway. It is the same fix _light_arched
    already makes for its fan bars with a boss, and it costs ZERO triangles
    because it only moves vertices that already exist.

    The two families are told apart by their own GEOMETRY, never by glazing()'s
    construction order: each came is one box, so its two long side faces carry
    the bar's direction in their normals -- sign(n.x * n.z) is negative for a
    came running (1,1) and positive for one running (1,-1). Anything
    axis-aligned (the pane, the bead, a mullion) has a zero product and is
    skipped, and so is any face off the leading plane. An END CAP is told from a
    side face by its longest edge -- a cap is one came width square, a side face
    is a came long -- and NOT by area: an area gate set at (3 * lead) ** 2 reads
    as "shorter than 140 mm", which quietly left the short cames round the edge
    of every light unmoved and 5.2 cm2 of them still fighting.

    DEPTH: the moved family runs 0.0357 .. 0.0483 against the other's
    0.0377 .. 0.0503 -- 2.0 mm apart, which is the same air gap this file already
    accepts between the leading and the pane it lies on (1.70 mm, see LEAD_W),
    14.1 mm behind the bead's back face (+0.0216) and 3.7 mm clear of the glass
    (+0.052). Nothing else on the depth ladder lives between 0.030 and 0.056.

    AND THE STEP IS 2 mm BECAUSE 2 mm MEASURED BEST, not because it is pretty.
    glazing() strikes the leading over the OVERSIZE pane, so every came runs REB
    (32 mm) past the aperture and its ends lap the BOARDING under the bead --
    where the boards' own back faces sit at 0.0396 .. 0.0475 before p.wobble
    warps them another +/-7 mm. A came plane landed in that band is a fresh
    coincidence, of exactly the kind this fix exists to remove, so the step was
    swept and measured rather than guessed:
        step   all pairs / cm2   RAY-REACHABLE
        2.0 mm      61 / 646        0.0 cm2      <- this
        3.0 mm      63 / 653        3.1 cm2      came back 0.0473 on a board back
        3.5 mm      65 / 653        3.8 cm2
        4.5 mm      67 / 663        7.2 cm2      came back 0.0458, worst of all
    2.0 mm puts the moved family's back face at 0.0483, clear above the boards'
    thickest nominal back, and it is the only value of the four that leaves the
    whole family at zero reachable coincident surface.
    """
    y0 = D_GLAZE - LEAD_W                  # glazing()'s leading plane, derived
    mv = set()
    for f in faces:
        n = f.normal
        if abs(n.y) > .30 or n.x * n.z <= 0:
            continue                       # a front/back face, or not diagonal
        if max(e.calc_length() for e in f.edges) < LEAD_W * 2:
            continue                       # an end cap, not a side face
        if any(abs(v.co.y - y0) > LEAD_W for v in f.verts):
            continue                       # not on the leading plane
        mv.update(f.verts)
    for v in mv:
        v.co.y += dy
    return len(mv) // 8                    # cames moved


def _light_rect(p, cz, lw, lh, gm, gl, cell, pattern="diamond", tint=.05):
    """A SQUARE-HEADED glazed light: one Part.glazing() call and nothing else.

    `lw` x `lh` is the hole cut in the boarding, centred on x = 0 at z = `cz`.
    The bead lands with its inner edge on that cut and laps LAP onto the boards
    all round, so the joint is an overlap and not a butt."""
    _lead_relief(p, p.glazing(
        (0.0, 0.0, cz), (_ap(lw), _ap(lh)), depth=D_GLAZE, frame=FR,
        overlap=OV, rebate=REB, lead=LEAD_W, cell=cell, pattern=pattern,
        mullions=0, mat_glass=gm, mat_lead=gl, tint=tint))


def _light_arched(p, lr, lz0, lsp, gm, gl, cell, rough=None, bars=3, tint=.05):
    """A ROUND-HEADED glazed light -- the only way Part.glazing() allows one.

    The primitive strikes RECTANGULAR openings, and rather than fork it (which is
    how five families grew five different glazing bugs) the light is joined the
    way a real arched glazed door is, and the way windows.arch_stone already
    does it: ONE glazing() unit for the square-headed light up to the SPRINGING,
    a fanlight in the head above it, and the bead carried round the arch as a
    single bent band. The leaded net therefore comes from the shared primitive --
    struck over the whole opening and clipped to an oversize pane, so it strikes
    the corners -- and the arch is joinery, which is what it is anyway.

    `lr` light half-width (= the arc radius), `lz0` its sill, `lsp` the height
    the arc springs from. `rough` is an rng: pass one and the bent head is
    hand-cut instead of struck true."""
    gz0, gz1 = lz0 - .002, lsp - REACH     # bead head's top edge lands ON lsp
    # _lead_relief steps the two diagonal came families 2 mm apart in depth --
    # see its docstring: crossing cames share one plane in the primitive.
    _lead_relief(p, p.glazing(
        (0.0, 0.0, (gz0 + gz1) / 2), (_ap(2 * lr), gz1 - gz0),
        depth=D_GLAZE, frame=FR, overlap=OV, rebate=REB, lead=LEAD_W,
        cell=cell, pattern="diamond", mullions=0,
        mat_glass=gm, mat_lead=gl, tint=tint))
    r_i, r_o = lr, lr + LAP                # the bead, bent: same band, same faces
    # ---- the fanlight pane. It sits 22 mm BEHIND the leaded pane AND its flat
    # bottom edge starts 6 mm above that pane's top, so the two sheets of glass
    # can neither share a plane nor overlap -- two overlapping panes 2 mm apart
    # is a flicker the width of the light -- and the bead's head member, which
    # runs from 43 mm below the spring line to it, covers the 6 mm anyway.
    rg = r_i + REB
    seg = [(rg * cos(radians(4.0)), lsp - .004)]
    for i in range(9):
        a = radians(lerp(4.0, 176.0, i / 8.0))
        seg.append((rg * cos(a), lsp + rg * sin(a)))
    seg.append((-rg * cos(radians(4.0)), lsp - .004))
    p.prism(seg, .012, gm, axis='Y', at=(0, D_GLAZE + .022, 0), bevel=0,
            tint=.03)
    # ---- radiating bars on the leading's own plane, dying into a boss at the
    # spring line. Without the boss three bars meet at a point and present three
    # coplanar front faces to each other; the boss stands 11 mm proud of them and
    # swallows their inner ends instead.
    y_bar = D_GLAZE - LEAD_W
    for i in range(bars):
        a = radians(lerp(28.0, 152.0, i / max(bars - 1.0, 1.0)))
        p.beam((.030 * cos(a), y_bar, lsp + .030 * sin(a)),
               ((r_i + .012) * cos(a), y_bar, lsp + (r_i + .012) * sin(a)),
               LEAD_W * 1.1, LEAD_W * 1.1, gl, bevel=0, tint=tint)
    p.cyl((0, y_bar - .001, lsp), .038, .034, gl, sides=8, axis='Y', tint=tint)
    # ---- the bent head. Struck on the bead's own depth so head and jambs are
    # one member: y_ring is glazing()'s frame plane, derived, never guessed.
    y_ring = D_GLAZE - LEAD_W * 2.6 - .0275
    if rough is None:
        _arc_band(p, y_ring, .055, r_o, r_i, lsp, "oak_dark", segs=12, tint=tint,
                  shade=.90)
    else:
        _arc_band_rough(p, rough, y_ring, .055, r_o, r_i, lsp, "oak_dark",
                        segs=12, tint=tint, shade=.90)


def _band_top(R_in, R_out, spring, frac=0.45, floor=0.0):
    """The line a boarded leaf's boards are cut to under an ARCHED HEAD BAND:
    `frac` of the way THROUGH the band, between its inner and its outer arc.

    "SM_Door_CellarDouble_1m is strange in how the beams end low from the arch
    instead of getting to the top and tapering/being cut to fit." It was: every
    board was a flat-topped box cut to the LOWEST height the arch reached across
    its own width, so under the curve there was a staircase of voids -- 220 mm
    deep at the haunches -- opening onto the dark backing slab. In a real board-
    and-ledge door in an arched opening the boards run right up and are cut to
    the curve, each one a little shorter than its neighbour.

    Cutting them to the arch line exactly is not enough either: board top and
    band bottom would then share one curve, and p.wobble displaces the two
    independently, so the joint opens again (and this family wobbles 7 mm). So
    the boards are cut to a line INSIDE the band and buried in it. What you see
    as the boards' top edge is then the band's own inner arc -- which is what it
    should have been all along."""
    def f(x):
        ax = abs(x)
        z_in = spring + (sqrt(R_in * R_in - ax * ax) if ax < R_in else 0.0)
        z_out = spring + (sqrt(R_out * R_out - ax * ax) if ax < R_out else 0.0)
        return max(z_in + (z_out - z_in) * frac, floor)
    return f


def _boards(p, x0, x1, n, z_bot, top_fn, y0, thick, mat, seed=0, gap=0.006,
            hole=None, tint=.075, bevel=.005, curve=0):
    """Vertical boards of uneven width filling x0..x1, each cut to top_fn(x) and
    stepping around an optional hole(x, w) -> (z0, z1). Deep grooves + a dark
    slab behind = the shadowed joints the refs show; the bevel is kept small so
    the groove reads as shadow, not as a pale highlight line.

    `gap` was 20 mm, then 10 mm, and it STILL read off the model as "gaps between
    the vertical wooden beams" rather than as joints -- because behind the joint
    is the dark backing slab, so 10 mm of gap plus a 5 mm bevel each side reads
    as a 20 mm black slot, not a shadow line. Boards in a ledged door are tight:
    6 mm plus the bevel is a joint you can see and not a hole you can see
    through, and it is the number to keep.

    `curve` > 0 cuts the board's TOP EDGE to top_fn with that many segments,
    building the board as a prism instead of a box. Use it on any leaf whose
    head is an arch -- see _band_top for why a square-cut board under a curve is
    the wrong shape."""
    # A right-to-left range (as the left leaf of a double door naturally gives)
    # used to poison everything downstream: w came out negative, so `w - gap`
    # made every board 20 mm WIDER instead of narrower -- the boards overlapped
    # each other instead of leaving a groove, which put two coplanar board faces
    # on the visible face of the leaf -- and hole() was handed a negative width,
    # so the glazing was never cut out of that leaf at all.
    if x1 < x0:
        x0, x1 = x1, x0
    r = rng(f"{p.name}/boards/{seed}")
    ws = [r.uniform(.82, 1.20) for _ in range(n)]
    k = (x1 - x0) / sum(ws)
    ws = [w * k for w in ws]
    # THE WHOLE RUN LEANS TOGETHER. Each board used to draw its own skew, so two
    # neighbours could lean 5 mm towards each other and close the groove at the
    # top; a run that racks as one is what a nailed-up boarded leaf does anyway,
    # and it keeps every pair of cheeks exactly parallel.
    sk = r.uniform(-1, 1) * .005
    MIN_AIR = .0025          # see below: the narrowest the groove may ever get
    u, prev_r = x0, None
    for w in ws:
        cu, u = u + w / 2, u + w
        ea, eb = cu - (w - gap) / 2, cu + (w - gap) / 2      # the board's edges
        # ONE BOARD IS ONE BOARD. jx, thickness and shade used to be drawn INSIDE
        # the span loop below, so a board split either side of a light came out
        # with a different offset, a different thickness and a different tone
        # above and below the glass.
        jx = r.uniform(-1, 1) * .003
        th = thick * r.uniform(.90, 1.08)
        sh = 1.0 + r.uniform(-.11, .09)
        # ...AND THE OFFSET MAY NEVER CLOSE THE GROOVE. This is the bug that
        # measured 647 cm2 on SM_Door_ArchPlank_1m_B and made doors the worst
        # z-fighting family in the kit: `gap` is 6 mm and jx was +/-3 mm drawn
        # independently per board, so a +3 board next to a -3 board put two full
        # -height cheeks, 1.85 m x 38 mm, in the SAME plane. (They were welded
        # together by finish(), which is how sure the coincidence was.) The
        # offset is now clamped against the board before it, so the groove can
        # never be narrower than MIN_AIR -- twelve times the 0.2 mm tolerance --
        # and because the clamp can only ever raise jx towards its neighbour's
        # value it cannot ratchet the run sideways either.
        if prev_r is not None and ea + jx < prev_r + MIN_AIR:
            jx = prev_r + MIN_AIR - ea
        prev_r = eb + jx
        # A curve-cut board runs to the HIGH corner of the arch over its own
        # width; a square-cut one can only stop at the low corner.
        zt = (max(top_fn(ea), top_fn(eb)) if curve
              else min(top_fn(cu - w / 2 + .01), top_fn(cu + w / 2 - .01)))
        spans = [(z_bot, zt)]
        if hole:
            h = hole(cu, w - gap)
            if h and h[0] < zt:
                spans = []
                if h[0] - z_bot > 0.06:
                    spans.append((z_bot, h[0]))
                if zt - h[1] > 0.05:
                    spans.append((h[1], zt))
        for (za, zb) in spans:
            if zb - za < 0.02:
                continue
            if curve and zb >= zt - 1e-9:
                pts = [(ea + jx, za), (eb + jx, za)]
                for i in range(curve + 1):
                    x = lerp(eb, ea, i / curve)
                    pts.append((x + jx, max(top_fn(x), za + .012)))
                p.prism(pts, th, mat, axis='Y', at=(0, y0 + th / 2, 0),
                        bevel=bevel, seg=1, tint=tint, shade=sh)
            else:
                p.box((cu + jx, y0 + th / 2, (za + zb) / 2),
                      (w - gap, th, zb - za), mat,
                      bevel=bevel, seg=1, tint=tint,
                      skew=(sk, 0), shade=sh)


def _edge_s(f, s_out, s_in, iters=22):
    """Bisect the patch boundary between an `s` that is outside it and one that
    is inside, and return the inside-most s that is still on the boundary."""
    for _ in range(iters):
        m = (s_out + s_in) / 2
        if f(m):
            s_in = m
        else:
            s_out = m
    return s_in


def _lattice(p, mapfn, u0, u1, v0, v1, pitch, mat, up, w=.028, t=.020,
             top_fn=None, tint=.06, seed=0, shade=1.0, lap=.008, over=.026,
             min_len=.024):
    """Diamond lattice of crossing laths STRUCK OVER THE WHOLE PANEL, then cut
    to it. mapfn(u,v) -> 3D; `up` is the patch normal so lath width lies in the
    patch.

    THE ONE THING LEFT IN THIS FILE THAT THIS BUILDS is the porch's two side
    SCREENS, and they are not glazing: an open trellis in a frame the posts, the
    mid rail and the head beam already make. None of the three faults
    Part.glazing() exists to prevent can happen to one -- there is no pane to
    fall short of its opening, and no frame of its own to open a line against
    what surrounds it. Every actual glazed light in this family now comes from
    Part.glazing() (see _light_rect / _light_arched); this is deliberately NOT
    a fifth fork of it, and it must not grow a pane and a frame and become one.

    It stays here for a measured reason as well as a formal one: the porch runs
    at 2564 tris of a 2800 budget (roof 1272, body 788, this 336, barges 168),
    and glazing()'s frame alone is 432 tris a call because it lays four bevelled
    boxes -- two calls could not be afforded even with the leading turned off.
    A porch that fails its tri budget is a failed piece.

    They lay a plane in the YZ plane, which glazing() also cannot express: its
    `rot` turns each primitive about its own centre rather than the assembly.

    TWO FAULTS OFF THE MODEL, both fixed here ("the window crosses are shaped
    weird and don't reach the edges properly"):

      * THE ENDS WERE QUANTISED. Each lath was clipped by walking 64 samples
        along it and keeping the first and last that landed inside the patch, so
        its ends were rounded to 2D/64 of its length -- 17 mm on the cellar
        door's little light -- and every lath stopped short of the frame by a
        different random amount. That is the ragged, floating pattern that reads
        as "shaped weird". The clip is now analytic: a coarse pass finds the span
        (the patch is convex, so `inside` is one interval) and both ends are then
        BISECTED onto the boundary to well under a tenth of a millimetre.
      * NOTHING REACHED THE EDGE. Even clipped exactly, a 45 deg lath meeting a
        horizontal or vertical edge square leaves half its width short of it, so
        the border was a saw-tooth of notches. Each lath now RUNS ON `over` past
        the clip at both ends and dies INSIDE the post, rail or head beam round
        the panel, so every quarry meets the border as a partial quarry and no
        lath end sits on a visible face. `over` is the caller's responsibility:
        it must be smaller than the member the lath dies into is deep, or the
        ends lie ACROSS that member instead of inside it, which is the fault
        that was measured on the cellar light before Part.glazing() took it.
      * AND THE CORNER LATHS WERE THROWN AWAY: the old cull dropped anything
        spanning under 110 mm, i.e. exactly the short laths that make the half
        quarries round the border, which is why the pattern floated in the middle
        of the light. The cull is now `min_len`, 24 mm, so only slivers go.

    The two diagonal sets are LAPPED: one of them stands `lap` proud of the
    other along -`up`, the way one direction of real leading crosses over the
    other. Laid in a single plane the two sets share a front and a back face at
    every crossing, and every crossing then flickers -- which is exactly the
    "artifacts in the window pattern" reported on the glazed doors."""
    r = rng(f"{p.name}/lat/{seed}")
    un = Vector(up).normalized()
    H = 0.70710678

    # the patch's real top: with an arched top_fn it stands well above v1, and
    # the old code sized its sample sweep off v1 alone
    v_hi = v1
    if top_fn:
        v_hi = max(v1, max(top_fn(lerp(u0, u1, i / 24.0)) for i in range(25)))
    D = ((u1 - u0) + (v_hi - v0)) * 1.6      # both ends of the sweep are OUTSIDE
    marg = (v_hi - v0) + pitch
    vm = (v0 + v1) / 2
    for sgn in (1, -1):
        off = un * (-lap if sgn < 0 else 0.0)
        k = int(floor((u0 - marg) / pitch))
        while True:
            a = (k + .5) * pitch
            k += 1
            if a > u1 + marg:
                break

            def inside(sv, a=a, sgn=sgn):
                u = a + sv * H
                v = vm + sgn * sv * H
                if u < u0 or u > u1 or v < v0:
                    return False
                return v <= (top_fn(u) if top_fn else v1)

            N, lo_i, hi_i = 48, None, None
            for i in range(N + 1):
                if inside(lerp(-D, D, i / N)):
                    if lo_i is None:
                        lo_i = i
                    hi_i = i
            if lo_i is None:
                continue
            sa = _edge_s(inside, lerp(-D, D, (lo_i - 1) / N),
                         lerp(-D, D, lo_i / N))
            sb = _edge_s(inside, lerp(-D, D, (hi_i + 1) / N),
                         lerp(-D, D, hi_i / N))
            if sb - sa < min_len:
                continue
            sa -= over
            sb += over
            pa = (a + sa * H, vm + sgn * sa * H)
            pb = (a + sb * H, vm + sgn * sb * H)
            p.beam(tuple(Vector(mapfn(*pa)) + off),
                   tuple(Vector(mapfn(*pb)) + off), w, t, mat, bevel=0,
                   tint=tint, up=up, shade=shade * (1 + r.uniform(-.07, .07)))


def _ring(p, at, R, tube, mat="iron", sides=8, prof=5, axis='Y', tint=.04):
    pr = [(R + tube * cos(2 * pi * i / prof), tube * sin(2 * pi * i / prof))
          for i in range(prof)]
    pr.append(pr[0])
    p.lathe(pr, mat, at=at, sides=sides, axis=axis, tint=tint, close=False)


def _strap(p, x_root, z, length, sign, y=-.046, h=.070, mat="iron"):
    """Iron strap hinge, lying ON the ledge: pin at the leaf edge, tapered strap
    running inward, spear tip on the end."""
    # the pin stands clear IN FRONT of the boarding: at its old radius one flat
    # of the hexagon came to rest in the board face plane and fought it.
    p.cyl((x_root, y + .008, z), .030, h + .060, mat, sides=6, axis='Z',
          bevel=0, tint=.03)
    xa, xb = x_root, x_root + sign * length
    p.box(((xa + xb) / 2, y + .012, z), (length, .026, h), mat, bevel=0,
          tint=.03, shade=.95)
    tip = [(0, -h * .36), (sign * .105, 0), (0, h * .36)]
    p.prism([(xb + u, z + v) for (u, v) in tip], .024, mat, axis='Y',
            at=(0, y + .012, 0), bevel=0, tint=.03)


def _pull(p, x, z, mat="iron"):
    """Ring pull on a cone-shaped rose. z is HAND HEIGHT: every leaf in this
    family puts it at 0.95-1.05 m off its own bottom edge, on the leaf's opening
    edge. The rose flares INTO the leaf and ends 5 mm inside the boarding, so it
    can neither hover off the face nor land its back cap on it."""
    p.cyl((x, -.016, z), .040, .042, mat, sides=8, axis='Y', bevel=0,
          r_top=.044, tint=.03)
    _ring(p, (x, -.046, z - .014), .064, .015, mat)


def _studs(p, xs, zs, y=-.030, mat="iron", r=.019, seed=0):
    rr = rng(f"{p.name}/studs/{seed}")
    for x in xs:
        for z in zs:
            p.cyl((x, y, z), r * rr.uniform(.85, 1.15), .026, mat, sides=5,
                  axis='Y', bevel=0, r_top=r * .55, tint=.03)


# ============================================================ door leaves ====
def arch_door(variant="A"):
    """Round-arched boarded door for OPENINGS['door_main'] -- ref1's front door.
    A: amber lattice light in the head, two ledges, hinges left.
    B: heavy studded door, iron-barred wicket, brace, hinges right.
    C: half-glazed -- wide lattice head over a deep mid rail (ref2's own front
       door), paler boards, knocker plate.
    """
    W, H = _ins("door_main")
    r, spring = _arch_geo(W, H)
    p = Part(f"SM_Door_ArchPlank_1m_{variant}", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(0, .24), z=(0, H)))
    RAIL = .105                          # arched head rail the boards die into
    R_IN, R_OUT = r - RAIL - .004, r - .002   # the head band's two arcs
    # EVERY BOARD RUNS TO THE ARCH AND IS CUT TO IT -- see _band_top. Cut square
    # to the lowest point the curve reached across their own width (which is what
    # they were) they leave a staircase of voids under the head, worst at the
    # haunches, opening onto the dark backing slab.
    top = _band_top(R_IN, R_OUT, spring, frac=.45)
    # dark slab behind everything: closes the leaf, is the shadow in every
    # groove. Its front face is at Y_SLAB - .019 = .100, clear BEHIND the
    # deepest board back AND behind the glass -- see the depth ladder at the top
    # of this file. It used to sit at .062, which is inside the glazed stack.
    p.prism(_arch_outline(W, H), .038, "oak_dark", axis='Y', at=(0, Y_SLAB, 0),
            bevel=.008, seg=1, tint=.04, shade=.52)

    if variant == "A":
        nb, mat, sgn = 6, "oak_mid", -1
        lw, lz0, lz1 = .54, 1.20, 1.90
    elif variant == "B":
        nb, mat, sgn = 7, "oak_mid", 1
        lw, lz0, lz1 = 0.0, 0.0, 0.0
    else:
        nb, mat, sgn = 5, "oak_pale", -1
        lw, lz0, lz1 = .76, 1.30, 1.99

    hole = None
    lr = lw / 2
    lsp = lz1 - lr
    ltop = lambda x: (lsp + sqrt(max(lr * lr - x * x, 0.0))) if abs(x) < lr else lsp
    if lw > 0:
        def hole(cx, wid):
            if cx - wid / 2 > lr - .01 or cx + wid / 2 < -lr + .01:
                return None
            xs = (cx - wid / 2, cx, cx + wid / 2)
            return (lz0 - .014, max(ltop(clamp(x, -lr, lr)) for x in xs) + .014)

    # arched head rail, flush with the boards, then the boards into it. The
    # springing rail is set 8 mm back so it does not share the board face plane.
    # proud of the boarding by 21 mm: the boards now run up UNDER it (curve=4),
    # so their front plane has to be buried inside it rather than level with it
    _arc_band(p, .002, .046, R_OUT, R_IN, spring, mat, segs=14,
              tint=.06, shade=.97)
    # SPRINGING RAIL. On the glazed leaves the door's arch springs INSIDE the
    # light (A: light 1.20-1.90 and spring 1.63; C: 1.30-1.99 and spring 1.63),
    # so a rail spanning the full width crossed the glazing -- and sitting 18 mm
    # in FRONT of the glass it read as a bar straight across the window. It now
    # DIES INTO THE LIGHT FRAME: one stub per side, from the leaf edge to 16 mm
    # inside the stile's outer face, so the boards are still tied at the
    # springing line, the stub end is buried in the stile rather than sharing a
    # plane with it, and nothing crosses the glass. Unglazed B keeps its rail.
    if lw > 0:
        for s in (-1, 1):
            # the stub's inner end DIES INSIDE the bead's head member, which runs
            # to lr + REACH. lr + .040 left only 6 mm of lap, and the glazing is
            # now rigid while the leaf wobbles 7 mm, so 6 mm could open into a
            # slot; lr + .022 laps it by 24 mm, which 7 mm cannot open.
            xa, xb = s * (W / 2 - .002), s * (lr + .022)
            p.box(((xa + xb) / 2, .029, spring), (abs(xa - xb), .042, .030),
                  mat, bevel=.005, seg=1, tint=.05, shade=.95)
    else:
        p.box((0, .029, spring), (W - .004, .042, .030), mat, bevel=.005, seg=1,
              tint=.05, shade=.95)
    # BOARD THE LEAF IN THREE RUNS ON A GLAZED LEAF. `hole` is a z-span per
    # BOARD, so whichever board happened to straddle the light's edge was cut
    # over its whole width -- up to 176 mm on this leaf against a 56 mm stile,
    # which left an open slot down both sides of the light, 25 mm of dark backing
    # slab, the full height of the glass. Boarding the two side panels
    # separately puts the joint at the light's edge, where the stile covers it.
    xa, xb = -W / 2 + .008, W / 2 - .008
    if lw > 0:
        e = lr + .004
        nl = max(1, int(round(nb * (-e - xa) / (xb - xa))))
        nm = max(2, nb - 2 * nl)
        _boards(p, xa, -e, nl, .012, top, 0.0, .044, mat, seed=f"{variant}L",
                curve=4)
        _boards(p, -e, e, nm, .012, top, 0.0, .044, mat, seed=variant,
                hole=hole, curve=4)
        _boards(p, e, xb, nl, .012, top, 0.0, .044, mat, seed=f"{variant}R",
                curve=4)
        # ...and the wedge between the light's arc and the square top of that
        # cut, which is the other half of the same fault.
        # ITS ARC HAS TO LAND UNDER THE BENT HEAD. The head runs from lr to
        # lr + LAP; a spandrel struck outside lr + LAP leaves a crescent of the
        # dark backing slab following the arch, 6 mm wide and the whole length of
        # it, which is the same "gap between the timber frame and what surrounds
        # it" in polar coordinates. LAP - 14 mm puts the fill's edge squarely in
        # the middle of the head's own width.
        # ...AND IT SITS ON ITS OWN RUNG OF THE DEPTH LADDER, 0.012 .. 0.030.
        # It used to be handed (0.0, .044) -- the boarding's own two planes -- and
        # a fill bounded by the ARC cannot avoid lapping boards cut to a
        # RECTANGLE: measured 25 cm2 of lap against the outermost middle board on
        # this leaf, on the front face and again on the back. Recessed 12 mm that
        # lap is a rebate instead of a fight, and the fill is under the bent head
        # for most of its area anyway.
        _spandrel(p, lr, lsp, lz1 + .016, .012, .018, mat, ring_out=LAP - .014,
                  tint=.075)
    else:
        _boards(p, xa, xb, nb, .012, top, 0.0, .044, mat, seed=variant, curve=4)

    # ---- ledges / braces on the face
    if variant == "A":
        for z in (.42, 1.04):
            p.box((0, -.012, z), (W - .040, .046, .116), "oak_dark", bevel=.008,
                  seg=1, tint=.05, shade=.86)
    elif variant == "B":
        # THE TOP LEDGE USED TO RUN STRAIGHT THROUGH THE WICKET. It sat at 1.76
        # and the barred wicket at 1.74, so the three iron bars passed through a
        # solid rail and their back faces landed on its back face -- measured on
        # the rough twin, whose thickness jitter closed the last 5 mm of it. A
        # ledge belongs UNDER a wicket, framing it, not across it: 1.44 puts the
        # rail 86 mm below the lowest bar and ties the boards where the arch
        # starts to narrow them.
        for z in Z_LEDGE_B:
            p.box((0, -.012, z), (W - .040, .046, .108), "oak_dark", bevel=.008,
                  seg=1, tint=.05, shade=.86)
        # A BRACE ENDS ON THE CENTRELINE OF THE LEDGE IT LANDS ON, not 20 mm off
        # it. This brace is 100 mm wide and rises at 36 deg, so its end face is
        # 82 mm tall in z; aimed at 0.40 against a 108 mm ledge centred on 0.38,
        # the top 7 mm of that end face stood out above the ledge, and the same
        # 7 mm stood below the upper one -- a diagonal cut end floating on the
        # boarding at both ends. On the ledge centres the whole end face is
        # buried, which is what a housed brace looks like. Same fault, measured
        # bigger, on flat_door (28 mm out at each end) and on both rough twins.
        p.beam((-W / 2 + .07, -.012, Z_LEDGE_B[0]),
               (W / 2 - .07, -.012, Z_LEDGE_B[1]), .100,
               .034, "oak_dark", bevel=.008, seg=1, tint=.05, up=(0, 1, 0),
               shade=.88)
        p.box((0, .035, 1.74), (.32, .034, .32), "oak_dark", bevel=.006, seg=1,
              tint=.04, shade=.45)
        for x in (-.086, 0, .086):
            p.box((x, -.012, 1.74), (.026, .036, .32), "iron", bevel=0, tint=.03)
    else:
        # the deep mid rail sits clear BELOW the light's bead: the bead stands
        # 33 mm proud and the rail 35 mm, i.e. 1.6 mm apart in depth, so the two
        # must NEVER overlap in z or that sliver is a coincident patch the width
        # of the leaf. 1.15 leaves 36 mm of air under the bead's sill (measured:
        # the bead's sill member's bottom face is at z = 1.256, the rail's top at
        # 1.220), and that clearance is the only thing keeping them apart.
        p.box((0, -.012, Z_RAIL_C), (W - .030, .046, .140), "oak_dark",
              bevel=.008, seg=1, tint=.05, shade=.86)
        p.box((0, -.012, .30), (W - .040, .046, .104), "oak_dark", bevel=.008,
              seg=1, tint=.05, shade=.86)

    # ---- iron
    xe = sgn * (W / 2 - .038)
    hz = (.42, 1.04) if variant != "C" else (.30, Z_RAIL_C)
    for z in hz:
        _strap(p, xe, z, W * .66, -sgn)
    if variant == "B":
        _studs(p, [-W / 2 + .11 + i * (W - .22) / 4 for i in range(5)],
               Z_LEDGE_B, seed="B")
    # ring pull on the OPENING edge (hinges are at xe), at hand height. C used
    # to carry its pull at 0.88 m, which read as a door built for a child.
    hx = -sgn * (W / 2 - .140)
    _pull(p, hx, 1.00)
    if variant == "C":
        # KNOCKER PLATE. It used to sit at (hx, 1.44), which on this leaf is
        # INSIDE the glazed light: half of it hung over the glass and half was
        # swallowed by the light frame's stile, so it read as a loose iron tab
        # floating in the window. A knocker is fixed to something solid, so it
        # now sits on the deep mid rail -- above the ring pull, clear of the
        # strap's spear tip -- standing 16 mm proud of the rail face with its
        # back 8 mm inside it, the same rung of the depth ladder as the rose.
        p.box((W / 2 - .110, -.039, Z_RAIL_C), (.100, .024, .105), "iron",
              bevel=.006, seg=1, tint=.03)
    p.wobble(.007, freq=1.8, respect_seams=False)
    if lw > 0:
        # ONE Part.glazing() call plus the fanlight that a round head needs --
        # see _light_arched. Bead, pane and leading all come from the primitive,
        # so the pane is oversize and lapped by the bead, and the leaded net is
        # struck over the whole light and clipped to the pane instead of being
        # generated inside an inset rectangle. That is the corner-diagonal fault
        # closed by construction rather than by tuning a margin.
        #
        # BELOW THE WOBBLE ON PURPOSE. The stack's tightest air gap is the 1.70
        # mm between the leading and the pane it lies on, and a 7 mm noise field
        # warps a 0.6 m pane by +/-2 mm across the bars: measured 75 cm2 of glass
        # against its own leading on this leaf. The unit stays rigid; the joint
        # to the leaf is the bead's 44 mm LAP onto the boarding, which is what
        # absorbs the leaf's wobble.
        _light_arched(p, lr, lz0, lsp, "glass", "oak_dark", .132)
    return p.finish()


def flat_door():
    """Ledge-and-brace back door for OPENINGS['door_side'] -- ref2's kitchen
    door: five boards, two ledges, one diagonal, dark oak, plain iron."""
    W, H = _ins("door_side")
    p = Part("SM_Door_FlatPlank_1m", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(0, .24), z=(0, H)))
    # backing slab on Y_SLAB, clear behind the board backs (see the depth ladder
    # at the top of this file) instead of level with them.
    p.plate((0, Y_SLAB, H / 2), (W - .006, .038, H - .004), "oak_dark", tint=.04,
            shade=.52)
    _boards(p, -W / 2, W / 2, 5, .012, lambda x: H - .008, 0.0, .044, "oak_mid",
            seed="side", tint=.085)
    Z_LEDGE_F = (.32, 1.60)
    for z in Z_LEDGE_F:
        p.box((0, -.012, z), (W - .024, .046, .122), "oak_dark", bevel=.008,
              seg=1, tint=.05, shade=.85)
    # brace ends ON the ledge centrelines -- see arch_door("B"). At 0.38 / 1.54
    # the end faces (58 mm tall in z) stuck 28 mm clear of a ledge only 122 mm
    # tall, so the diagonal's cut end sat on the boarding in plain view at both
    # ends of the brace.
    p.beam((-W / 2 + .06, -.012, Z_LEDGE_F[0]),
           (W / 2 - .06, -.012, Z_LEDGE_F[1]), .106, .034,
           "oak_dark", bevel=.008, seg=1, tint=.05, up=(0, 1, 0), shade=.88)
    # boarded top rail with an iron-barred slot, as on the ref
    p.box((0, .035, 1.86), (.36, .034, .17), "oak_dark", bevel=.006, seg=1,
          tint=.04, shade=.45)
    for x in (-.10, 0, .10):
        p.box((x, -.008, 1.86), (.024, .032, .17), "iron", bevel=0, tint=.03)
    for z in Z_LEDGE_F:
        _strap(p, -(W / 2 - .036), z, W * .68, 1)
    _pull(p, W / 2 - .130, .96)
    p.box((W / 2 - .130, -.003, 1.20), (.095, .022, .130), "iron", bevel=.005,
          seg=1, tint=.03)
    p.wobble(.007, freq=1.8, respect_seams=False)
    return p.finish()


def cellar_door():
    """Twin boarded leaves under a round head -- ref1's big cellar arch.
    Ledged and braced, with a narrow lattice light over the meeting stiles.

    Three faults were found by eye on this piece and fixed here. They were
    joinery mistakes, not styling, so the look is deliberately unchanged:

    1. THE BRACES RAN THE WRONG WAY. Each leaf hangs on the OUTER jamb, so its
       free edge is the inner (meeting) one. A brace has to rise from the hinge
       stile at the bottom to the free stile at the top, or it carries nothing --
       it used to do the opposite, which is the beam that "made no sense".
    2. THE TOP LEDGE RAN STRAIGHT THROUGH THE GLAZING. The light sat at
       0.94-1.56 m and the ledge at 1.30 m, so a solid rail crossed the glazed
       panel. The light is now a HIGH vision slot (1.42-1.74 m, about eye level,
       which is where you want it on a cellar door anyway) and the top ledge has
       come down to 1.26 m, clear below it.
    3. THE RING PULLS SAT AT 0.66 m -- knee height, and they were the only thing
       in the family not at hand height. They are now at 1.00 m, still one on
       each meeting leaf either side of the central joint, which is where the
       light used to be in the way.
    """
    W, H = _ins("door_cellar")
    r, spring = _arch_geo(W, H)
    p = Part("SM_Door_CellarDouble_1m", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(0, .24), z=(0, H)))
    RAIL = .115
    R_IN, R_OUT = r - RAIL - .004, r - .002    # the head band's two arcs
    # EVERY BOARD RUNS TO THE ARCH AND IS CUT TO IT (see _band_top). It used to
    # stop at the lowest point the arch reached across its own width, which left
    # the staircase of voids under the curve that was reported on this piece.
    top = _band_top(R_IN, R_OUT, spring, frac=.45)
    # front face on Y_SLAB - .019: clear BEHIND the board backs AND behind the
    # glass, never level with either
    p.prism(_arch_outline(W, H), .038, "oak_dark", axis='Y', at=(0, Y_SLAB, 0),
            bevel=.008, seg=1, tint=.04, shade=.52)

    lw, lz0, lz1 = .22, 1.42, 1.74          # high vision slot, above the ledges
    lr = lw / 2
    Z_LEDGE = (.36, 1.26)
    Z_PULL = 1.00

    def hole(cx, wid):
        if abs(cx) > lr + wid / 2 - .01:
            return None
        return (lz0 - .014, lz1 + .014)

    # THE HEAD BAND NOW STANDS PROUD OF THE BOARDING -- 21 mm, spanning
    # y = -0.021 .. +0.025 instead of 0.000 .. +0.050. Two reasons, and the first
    # is a bug: at y = 0 its front face and the board faces were THE SAME PLANE,
    # so once the boards run up under it (which is the whole fix) the overlap
    # would be a large coplanar patch, i.e. flicker. Proud, the boards' front
    # face is buried 21 mm inside the band -- five times what this piece's 7 mm
    # wobble can move it -- and a head rail standing slightly proud of the
    # boarding it carries is what the joint looks like anyway.
    _arc_band(p, .002, .046, R_OUT, R_IN, spring, "oak_mid",
              segs=15, tint=.06, shade=.97)
    for s in (-1, 1):
        # springing rail, one per leaf so the two leaves stay separate things:
        # out towards the jamb the boards die below the arch band and used to
        # leave a slot open onto the backing slab.
        p.box((s * (W / 4 + .008), .029, spring), (W / 2 - .026, .042, .030),
              "oak_mid", bevel=.005, seg=1, tint=.05, shade=.95)
        # THE MEETING JOINT. Each leaf's boarding used to start 18 mm off centre
        # and then inset half a gap on top of that, so between the two leaves
        # there was a 46 mm slot open onto the dark backing slab down the whole
        # height of the door -- by far the widest of the "gaps between the
        # vertical wooden beams", and the one the eye goes to because it is dead
        # centre. 5 mm off centre plus the 6 mm board gap leaves a 16 mm shadow
        # line, which is what a pair of leaves meeting actually looks like.
        #
        # BOARD IT IN TWO RUNS, with the joint under the light's bead -- the same
        # trick arch_door uses, and for the same reason. `hole` is a z-span per
        # BOARD, so whichever board straddled the light's edge was cut over its
        # WHOLE width: 155 mm of board against a bead that laps 44 mm, which left
        # a slot of the light standing open past its own frame down both sides.
        # Splitting the run at the light's edge puts the cut exactly where the
        # bead covers it.
        e = s * (lr + .012)
        _boards(p, s * .005, e, 1, .012, top, 0.0, .042, "oak_mid",
                seed=f"cellarL{s}", hole=hole, tint=.085, curve=4)
        _boards(p, e, s * (W / 2 - .008), 3, .012, top, 0.0, .042, "oak_mid",
                seed=f"cellar{s}", tint=.085, curve=4)
    for s in (-1, 1):
        for z in Z_LEDGE:
            p.box((s * (W / 4 + .012), -.012, z), (W / 2 - .05, .046, .110),
                  "oak_dark", bevel=.008, seg=1, tint=.05, shade=.85)
        # brace: bottom end at the HINGE stile, top end at the meeting stile,
        # both ends dying into a ledge rather than stopping in mid air.
        p.beam((s * (W / 2 - .07), -.012, Z_LEDGE[0]),
               (s * .10, -.012, Z_LEDGE[1]), .094, .034, "oak_dark", bevel=.008,
               seg=1, tint=.05, up=(0, 1, 0), shade=.88)
        for z in Z_LEDGE:
            _strap(p, s * (W / 2 - .034), z, W * .34, -s)
        _pull(p, s * .120, Z_PULL)
    p.box((0, -.012, Z_PULL), (.062, .036, .20), "iron", bevel=.005, seg=1,
          tint=.03)
    p.wobble(.007, freq=1.8, respect_seams=False)
    # THE LIGHT IS ONE Part.glazing() CALL, LAID AFTER THE WOBBLE. It used to be
    # four frame members, a glass plate and a local diamond lattice, and the last
    # fault left in it was that the laths OVERLAY THE RAILS: the leading sat 1 mm
    # in front of the head and sill rails and ran 30 mm past the light, so every
    # lath end lay across the frame it was supposed to die inside. glazing() puts
    # the leading BEHIND the bead by construction (lead * 2.6 back from its front
    # face) and clips the net to an oversize pane, so the laths cannot reach the
    # rails' faces and every quarry still meets the edge as a partial quarry.
    #
    # It is built below p.wobble() because the ladder inside it is finer than the
    # wobble: 1.70 mm of air between the leading and the pane against a 7 mm
    # noise field. This piece measured 135 cm2 of glass against its own leading,
    # the family's second worst entry, purely from that warp. The bead's 44 mm
    # lap onto the boarding is the joint, so nothing can come loose.
    _light_rect(p, (lz0 + lz1) / 2, lw, lz1 - lz0, "glass", "oak_dark", .058)
    return p.finish()


# ================================================================== porch ====
# The porch is ALL OVERHANG. ref3's porch roof floats well clear of the box it
# shelters -- roughly 0.4 m past the posts on every side -- and the gap between
# the roof and the walls is filled with structure you can read: a run of rafter
# tails at each eave, purlin ends stepping up the gable, a scallop-toothed barge
# board. The numbers below are what make that happen; keep them proportional if
# you touch them.
P_POST = 0.70               # side planes / front post centres in X
P_SEC = 0.190               # post section  (post faces at 0.795 / -1.395)
P_FRONT = -1.30             # front post centre plane in Y
P_VERGE = -1.78             # gable verge plane: 0.385 past the front post face
P_BACK = 0.05               # roof runs this far into the wall face
P_EAVE = 2.30               # roof plane height at the eave line
P_HW = 1.20                 # roof half-width: 0.405 past the side post faces
SW_LEN = 0.50               # bell-cast (swept) bottom section, along the slope
SW_DEG = 32.0
P_HEAD = 2.42               # top of the door head / bottom of the tympanum
P_RAIL = 1.04               # top of the boarded dado on the sides
P_PLATE = 2.452             # eaves plate centre: the rafter tails bear on it
SLAB = 0.048                # roof slab thickness (see _courses)
BARGE = 0.162               # how far the barge board hangs below the rake
RAFT = 0.150                # rafter-tail depth: deep enough to hang clear
                            # below the eaves fascia and read from outside
# HOW FAR EACH ROOF PATCH IS PULLED IN FROM THE VERGE AND THE WALL, in the order
# _porch_frames() yields them: left bell-cast, left main, right bell-cast, right
# main. All four used to be struck to the same width, so their sheathing plates'
# end faces -- 630 cm2 on a main patch, 250 on a bell-cast one -- landed on ONE
# plane at each end (y = P_VERGE at the verge, y = P_BACK at the wall), and the
# patches OVERLAP in projection exactly where they meet: the two segments of a
# slope lap at the kink, and the two slopes lap at the apex. Measured at 0.5 mm:
# 3.1 cm2 at the verge, 100% ray-reachable, plus 23.5 + 3.1 + 3.1 cm2 at the wall
# end. Nominally those faces are coincident to 0.000 and what the tool reads is
# only whatever p.wobble() happens to leave -- the verge pair came out 0.07 mm
# apart. A coincidence that survives on a noise lottery is not sealed, it is
# lucky. Stepped 0 / 3 / 3 / 6 mm every lapping pair is at least 3 mm apart by
# construction (the two bell-cast patches never overlap each other, so they can
# share), and 6 mm of inset still leaves the sheathing edge 11 mm proud of the
# barge board's outer face, so nothing opens at the verge.
PATCH_IN = (0.0, .003, .003, .006)


def _kink():
    cs, ss = cos(radians(SW_DEG)), sin(radians(SW_DEG))
    return P_HW - SW_LEN * cs, P_EAVE + SW_LEN * ss


def _porch_apex():
    kx, kz = _kink()
    return kz + kx * TAN_P


def _rake_z(x):
    """Height of the roof plane at |x| on the gable."""
    kx, kz = _kink()
    x = abs(x)
    if x >= kx:
        return P_EAVE + (P_HW - x) * tan(radians(SW_DEG))
    return kz + (kx - x) * TAN_P


def _bell_z(x):
    """The bell-cast (lowest, flattest) roof plane, extended INBOARD past the
    kink. Rafter tails run on this line, so a straight tail tucks under the
    steeper part of the slope instead of stabbing up through it."""
    return P_EAVE + (P_HW - abs(x)) * tan(radians(SW_DEG))


def _slope_cos(x):
    """cos of the roof's angle at |x| -- the bell-cast section is flatter."""
    return cos(radians(SW_DEG) if abs(x) >= _kink()[0] else S.PITCH)


def _soffit_drop(x):
    """Vertical distance from the roof plane down to its underside at |x|."""
    return SLAB / _slope_cos(x)


def _under_roof(x, perp):
    """Height at |x| that is `perp` metres PERPENDICULARLY under the roof plane.

    PERPENDICULAR is the measurement that matters and a vertical drop is not it.
    Everything the roof slab contains is stacked normal to its own plane: the
    sheathing plate fills 0 .. 48 mm under it, and _courses pushes each shingle
    tab's underside 14 mm (even courses) or 24 mm (odd) inside that plate. So a
    member cut to a fixed VERTICAL drop d lands at d * cos(pitch) perpendicular,
    which at the kit's 52 deg is 0.62 d -- and the tympanum's 22 mm vertical drop
    put its raking top edge 13.5 mm under the plane, i.e. 0.5 mm off the even
    courses' tab undersides. That measured 336 cm2, by far the biggest single
    entry in the doors family: two 170 cm2 patches of board against shingle.
    Anything dying into the slab should say what perpendicular depth it wants."""
    return _rake_z(x) - perp / _slope_cos(x)


# How deep into the roof slab the boarded tympanum's raking top edge dies. The
# slab is 48 mm thick perpendicular and the shingle tabs' undersides are buried
# 14-24 mm inside it, so 34 mm is the middle of the only clear band: 10 mm below
# the shallowest tab underside and 14 mm above the slab's own soffit.
TYMP_PERP = 0.034


def _rake_pts(s):
    """Rake polyline of one slope, eave -> kink -> apex, as (x, z)."""
    kx, kz = _kink()
    return [(s * P_HW, P_EAVE), (s * kx, kz), (0.0, _porch_apex())]


def _porch_frames():
    """(rotation, patch origin, patch length) for the four roof patches: a
    bell-cast bottom section and a main section on each slope."""
    out = []
    kx, kz = _kink()
    apex = _porch_apex()
    for s in (-1, 1):
        e = Vector((s * P_HW, 0.0, P_EAVE))
        k = Vector((s * kx, 0.0, kz))
        for (a, b) in ((e, k), (k, Vector((0.0, 0.0, apex)))):
            d = b - a
            up = d.normalized()
            ex = Vector((0.0, s, 0.0))
            n = ex.cross(up)
            M = Matrix(((ex.x, up.x, n.x), (ex.y, up.y, n.y),
                        (ex.z, up.z, n.z))).to_4x4()
            out.append((M, a, d.length))
    return out


def _courses(p, width, length, at, rot, seed, row=.235, tab=.33, thick=.042,
             mat="shingle_moss", mat_alt="shingle"):
    """Shingle courses on a flat patch: rows along local X climbing +Y, tabs
    standing +Z. Built in a sub-Part so the whole patch can be rotated onto the
    slope (util.shingles only rotates the individual shingles, not the layout).
    Tabs are unbeveled -- at this size the row rhythm is what reads."""
    sub = p.sub(f"{p.name}_sh{seed}")
    r = rng(f"{p.name}/courses/{seed}")
    # the butt line's wander gets its OWN stream, so changing it does not shift
    # every tab's size, shade and material behind it
    rb = rng(f"{p.name}/butt/{seed}")
    sub.plate((0, length / 2, -.024), (width, length, .048), "oak_dark",
              tint=.03, shade=.55)
    nr = max(1, int(round(length / row)))
    for ri in range(nr):
        v = row * ri
        n = max(2, int(round(width / tab)))
        tw = width / n
        # EVERY PATCH GETS ITS OWN COLUMN PHASE. The four patches of this roof
        # meet each other -- the two segments of a slope lap at the kink, and the
        # two slopes lap at the apex -- and each patch laid its tab boundaries on
        # exactly the same grid, so two lapping tabs from different patches put
        # their cut side faces in ONE plane. Measured at the kink: 76 cm2 at 0.47
        # mm, invisible to check_zfight (>400 faces in that bucket). The phases
        # are deliberately not fractions of each other, so no pair of patches
        # lines up, and a shingle roof whose columns break at the kink is what
        # every real one does anyway.
        ph = tw * (0.0, 0.23, 0.37, 0.11)[int(seed) % 4]
        off = (ri % 2) * tw * .5 - ph
        # Consecutive courses LAP by ~46% of a row, so if they sat at one height
        # every lap would be two coplanar faces fighting over the same pixels --
        # the single biggest flicker on this piece. Odd courses stand a clear
        # 12 mm proud, which is also how a shingle laps the course below it. And
        # a tab's underside is pushed 14-24 mm INSIDE the sheathing plate rather
        # than resting exactly on its top face, for the same reason. The gaps
        # have to be that big: p.wobble() below warps a patch-sized quad by up
        # to 6 mm, so anything tighter closes up again.
        lift = (ri % 2) * .012
        z_bot = -.014 - (ri % 2) * .010
        # THE BUTT LINE WANDERS. Every tab in a course used to start at the
        # same v, so two tabs whose skew made them overlap laterally by a few mm
        # presented two faces in one plane -- the only TRUE coincidence left on
        # this piece (measured 2.2 cm2 between two tabs in the same course; the
        # rest of what check_zfight.py reports here is mirror-symmetric
        # geometry -- see MEASURING COINCIDENT SURFACE above). Stepping the butt
        # by index means
        # neighbouring tabs are always at least 1 mm apart in v, and both refs
        # draw an uneven butt line anyway.
        # AND THE TWO CUT EDGES STEP COURSE BY COURSE. Every course has one tab
        # cut short at each end of the patch, and consecutive courses LAP by 46%
        # of a row -- so the cut faces of two lapping tabs sat in one plane and
        # overlapped, which is a genuine coincidence and a large one: 55 cm2 at
        # 0.17 mm at the wall end of one patch. check_zfight cannot see it (this
        # piece puts more than 400 faces in that normal's bucket and the bucket
        # is skipped), so it was found with a brute-force pass instead. Stepping
        # the cut 0, 4, 8 mm on a 3-cycle puts every lapping pair at least 4 mm
        # apart, and courses 3 apart do not lap at all (a tab is 1.46 rows long).
        # Both ends are covered anyway -- the barge board stands 24 mm proud of
        # the verge and the far end dies into the wall.
        e0 = -width / 2 + .004 * (ri % 3)
        e1 = width / 2 - .004 * ((ri + 1) % 3)
        for i in range(n + 1):
            # A tab that runs off the edge of the patch is CUT SHORT, which is
            # what a shingler does with the first tab of a staggered course. It
            # used to be slid back inside the patch instead, which dropped it
            # half on top of its neighbour -- two identical faces in one plane,
            # and the biggest single flicker left on this piece.
            lo = -width / 2 + tw * i - off
            hi = min(lo + tw, e1)
            lo = max(lo, e0)
            if hi - lo < tw * .28:
                continue
            cu = (lo + hi) / 2
            hh = row * 1.46 * (1 + r.uniform(-.06, .05))
            butt = -.005 * (i % 3) - rb.uniform(0, .004)  # never 0 vs 0
            z_top = thick + lift + r.uniform(0, .003)
            # a WHISPER of the warm shingle, not confetti: at one in eight the
            # brown tabs read as damage on a mossy roof rather than as age.
            m = mat if r.random() > .05 else mat_alt
            # THE SKEW MAY NOT CLOSE THE GAP TO THE NEXT TAB. 13 mm of gap
            # against a skew of +/-16 mm means the top edge of a tab can lean
            # straight through its neighbour, and two tabs leaning the same way
            # then present one plane: measured 16 cm2 between two tabs of one
            # course near the apex. 18 mm of gap against +/-8 mm of skew leaves
            # 2 mm in the worst case and still reads as a hand-laid course.
            sub.box((cu, v + butt + hh / 2 - row * .23, (z_top + z_bot) / 2),
                    (hi - lo - .018, hh, z_top - z_bot), m, bevel=0, tint=.07,
                    skew=(r.uniform(-1, 1) * .008, 0),
                    shade=.92 + r.uniform(-.12, .10))
    p.merge(sub, at=at, rot=rot)
    sub.bm.free()


def _barge(p, s, y, thick, depth, tooth, n, mat, tint=.05, shade=.84):
    """One barge board: the wide raking plank of the verge with a run of dagged
    (cusped) teeth cut along its lower edge -- ref3's carved trim, and most of
    what makes the roofline read as crafted rather than extruded. Built as ONE
    prism, the way a real scalloped bargeboard is one carved plank, instead of a
    plank plus a row of loose blocks: cheaper AND it cannot come apart."""
    pts = _rake_pts(s)
    segs = []
    for a, b in zip(pts, pts[1:]):
        d = Vector((b[0] - a[0], 0.0, b[1] - a[1]))
        L = d.length
        u = d / L
        nrm = Vector((u.z, 0.0, -u.x))          # perpendicular, in the gable
        if nrm.z > 0:                           # ... pointing DOWN under the roof
            nrm = -nrm
        segs.append((Vector((a[0], 0.0, a[1])), u, nrm, L))
    total = sum(sg[3] for sg in segs)

    def at(t, off):
        # NOT clamped at 0: the eave end deliberately runs OUT past the start of
        # the rake -- see EAVE_RUN below -- and clamping killed that.
        t = min(t, total)
        for i, (a, u, nrm, L) in enumerate(segs):
            if t <= L or i == len(segs) - 1:
                q = a + u * min(t, L) + nrm * off
                return (q.x, q.z)
            t -= L

    # THE EAVE END RUNS 30 mm PAST THE RAKE. Cut dead on t = 0 its end face sat
    # in exactly the plane of the roof patch's own sheathing edge -- both are
    # struck perpendicular to the rake through the eave point -- which measured
    # 42 cm2 of oak_dark against oak_dark at 0.10 mm, the third entry on this
    # piece. A bargeboard that oversails the eave corner by a hair is also what
    # ref3 draws; a bargeboard whose tip stops exactly level with the sheathing
    # is not something anyone builds.
    EAVE_RUN = -.030
    out = [at(EAVE_RUN, -.024)]                 # eave end, a shade proud
    acc = 0.0
    for (a, u, nrm, L) in segs[:-1]:
        acc += L
        out.append(at(acc, -.024))
    out.append(at(total, -.024))                # apex
    out.append(at(total, depth))
    step = total / n
    for i in range(n):
        # teeth hang STRAIGHT DOWN off the board's lower edge, not square to the
        # rake: square to the rake they read as a flight of stairs, straight
        # down they read as the row of pendant cusps ref3 actually carves.
        q = at(total - (i + .5) * step, depth)
        out.append((q[0], q[1] - tooth))
        out.append(at(total - (i + 1) * step if i < n - 1 else EAVE_RUN, depth))
    p.prism(out, thick, mat, axis='Y', at=(0, y, 0), bevel=0, seg=1, tint=tint,
            shade=shade)


def porch():
    """Gabled entrance porch + door surround (ref3/ref2). Boarded dado with
    lattice panels over it, chunky posts, carved name board, boarded tympanum --
    and the thing that makes the silhouette: a DEEP overhang. The roof oversails
    the front posts by 0.39 and the side posts by 0.41 (ref3's porch is nearly
    all roof), and the gap that opens up under it is filled with real structure:
    four exposed rafter tails bearing on the eaves plate at each eave, purlin
    ends stepping up the gable under the barge boards, a scallop-toothed barge
    board on each rake, a pinnacle finial, and mossy shingles flicking out over
    a long bell-cast eave.

    Because the roof oversails its 2 m bay by 0.3 either side, this piece
    declares its X bounds as the ROOF, not the grid. That is honest -- a porch
    projects, it does not tile -- but it means the bay next door should not carry
    relief above 2.2 m on the wall face.

    BEVELS: slot 0 of this mesh is oak_dark deliberately. util.Part._emit loses
    a bevelled primitive's original faces (bmesh.ops.bevel rebuilds them and
    they fall back to material slot 0), so ONLY oak_dark primitives are bevelled
    here -- otherwise the posts and head beams come out the colour of whatever
    was registered first, which is how they ended up looking like stone. Fix
    _emit and the bevels can go back everywhere.
    """
    apex = _porch_apex()
    inner = P_POST - P_SEC / 2                      # inside face of the sides
    kx, _kz = _kink()
    p = Part("SM_Door_PorchGable_2m", budget="door",
             seams=dict(x=(-(P_HW + .10), P_HW + .10), y=(P_VERGE, .12),
                        z=(0, apex + .50)))

    # ---- corner posts (front pair chunkier, on stone pads) + rear jamb posts.
    #      oak_dark first, so it owns material slot 0 -- see the docstring.
    for s in (-1, 1):
        x = s * P_POST
        p.box((x, P_FRONT, 1.30), (P_SEC, P_SEC, 2.28), "oak_dark", bevel=.018,
              seg=1, tint=.05, taper=.94)
        p.box((x, .015, 1.24), (P_SEC - .02, P_SEC - .02, 2.36), "oak_dark",
              bevel=0, tint=.05, taper=.96)
        p.box((x, P_FRONT, .112), (P_SEC + .075, P_SEC + .075, .165),
              "stone", bevel=0, tint=.06, shade=.78)
        # spandrel bracket into the head beam. ITS BACK EDGE LIVES INSIDE THE
        # POST, 20 mm in. At x -/+ P_SEC/2 (0.095) it was struck exactly on the
        # post's nominal inner face -- and the post is TAPERED (taper=.94), so at
        # the bracket's own height the post face has already drawn back to
        # 0.6103 while the bracket stood at 0.6050: a 5 mm slot, 320 mm long, up
        # the inside of both front posts, with nothing behind it. A brace that
        # does not touch what it braces is the fault Shanee keeps catching by
        # eye, and it is measurable: 5.3 mm at z = 2.06, 4.6 mm at z = 2.38.
        p.prism([(0, 0), (0, .32), (-s * .32, .32)], .10, "oak_dark", axis='Y',
                at=(x - s * .070, P_FRONT, 2.06), bevel=0, tint=.05, shade=.94)
        # eaves plate: the rafter tails sit on top of this
        p.beam((x, P_FRONT - .06, P_PLATE), (x, .06, P_PLATE), .150, .145,
               "oak_dark", bevel=0, tint=.05, up=(0, 0, 1), shade=.92)

    # ---- flagged floor
    p.plate((0, (P_FRONT + .06) / 2, .034), (P_POST * 2 + .20, -P_FRONT + .16,
                                             .068), "stone", tint=.07, shade=.74)

    # ---- door surround at the wall: head and plaster cheeks
    p.box((0, .030, P_HEAD - .09), (P_POST * 2 - .06, .120, .175), "oak_dark",
          bevel=0, tint=.05)

    # ---- front head + carved name board
    p.box((0, P_FRONT - .024, 2.375), (P_POST * 2 + .13, .090, .140), "oak_dark",
          bevel=0, tint=.05)
    p.box((0, P_FRONT - .042, 2.225), (P_POST * 2 + .06, .062, .190),
          "oak_pale", bevel=0, tint=.045, shade=.82)
    rr = rng("porch/runes")
    for i in range(3):
        # 20 mm deep at P_FRONT - .070, so the back of each letter is 13 mm
        # INSIDE the name board and 7 mm of it stands proud. At (P_FRONT - .078,
        # 12 mm) the letters lapped the board by exactly 1 mm: two 26 cm2
        # patches of gold against oak_pale, 0.38 mm apart. A letter fixed to a
        # board is bedded in it, not laid on its face.
        p.box((lerp(-.34, .34, (i + .5) / 3), P_FRONT - .070,
               2.225 + rr.uniform(-.012, .012)),
              (.036, .020, .086 * rr.uniform(.72, 1.15)), "flower_gold",
              bevel=0, tint=.09)

    # ---- sides: boarded dado, mid rail, lattice panel
    for s in (-1, 1):
        x = s * (inner + .026)
        rb = rng(f"porch/dado{s}")
        y0, y1 = P_FRONT + P_SEC / 2, -P_SEC / 2 + .01
        nbd = 4
        ws = [rb.uniform(.85, 1.15) for _ in range(nbd)]
        k = (y1 - y0) / sum(ws)
        u = y0
        for w in (v * k for v in ws):
            cy, u = u + w / 2, u + w
            p.box((x, cy, (P_RAIL + .06) / 2), (.052, w - .018, P_RAIL - .06),
                  "oak_mid", bevel=0, tint=.085,
                  shade=.92 + rb.uniform(-.09, .07))
        p.beam((x, y0 - .02, P_RAIL + .045), (x, y1 + .02, P_RAIL + .045), .070,
               .090, "oak_dark", bevel=0, tint=.05, up=(1, 0, 0), shade=.92)
        _lattice(p, lambda u, v, x=x: (x, u, v), y0 + .02, y1 - .02,
                 P_RAIL + .10, 2.36, .30, "oak_mid", up=(1, 0, 0), w=.046,
                 t=.030, seed=f"scr{s}", shade=.86, lap=.016)

    # ---- gable: boarded tympanum (ref3 BOARDS it, vertically), sign, barges
    gb = P_VERGE + .060
    rb = rng("porch/tymp")
    nt = 7
    tw2 = inner + .17
    # THE TYMPANUM WAS A ROW OF BOARDS WITH NOTHING BEHIND IT AND 16 mm BETWEEN
    # THEM, so the gable leaked four bright slots of daylight from the head beam
    # to the ridge -- straight through the piece, and obvious the moment the
    # porch is looked at square on. Same fault the leaves fixed twice and the
    # same two-part fix: a dark board behind the boarding, and joints tight
    # enough to read as shadow (6 mm now, not 16). With something dark behind it
    # a 6 mm joint is a line; with the sky behind it a 16 mm joint is a hole.
    # The backing's own top edge dies 41 mm perpendicular under the roof plane,
    # 7 mm deeper than the boards in front of it and 7 mm clear of the slab's
    # soffit, so it is inside the slab without sharing a plane with either.
    bk_perp = TYMP_PERP + .007
    p.prism([(-tw2, P_HEAD), (tw2, P_HEAD), (tw2, _under_roof(tw2, bk_perp)),
             (0.0, apex - bk_perp / cos(S.PITCH)),
             (-tw2, _under_roof(-tw2, bk_perp))],
            .020, "oak_dark", axis='Y', at=(0, P_FRONT - .002, 0), bevel=0,
            tint=.03, shade=.50)
    for i in range(nt):
        # each board is a PRISM with a raking top edge, not a box cut square:
        # square-cut boards turned the tympanum into a flight of stairs, and
        # cutting them to the high corner instead pushed them through the roof.
        x0 = lerp(-tw2, tw2, i / nt) + .003
        x1 = lerp(-tw2, tw2, (i + 1) / nt) - .003
        top = [(x1, _under_roof(x1, TYMP_PERP))]
        if x0 < 0.0 < x1:
            top.append((0.0, apex - TYMP_PERP / cos(S.PITCH)))
        top.append((x0, _under_roof(x0, TYMP_PERP)))
        if min(t[1] for t in top) - P_HEAD < .05:
            continue
        p.prism([(x0, P_HEAD), (x1, P_HEAD)] + top, .058, "oak_mid", axis='Y',
                at=(0, P_FRONT - .046, 0), bevel=0, tint=.085,
                shade=1.04 + rb.uniform(-.09, .07))
    for (zz, ss) in ((apex - .40, .150), (apex - .70, .105)):
        p.box((0, P_FRONT - .082, zz), (ss, .038, ss), "oak_pale", bevel=0,
              tint=.05, rot=(0, 45, 0), shade=.94)

    for s in (-1, 1):
        # scallop-toothed barge board on the rake
        _barge(p, s, gb, .086, BARGE, .102, 9, "oak_dark", tint=.05, shade=.86)
        # dark raking board where the roof dies into the wall (follows the kink).
        # The four boards STEP 3 mm in depth. Each beam's end cap is square to
        # its own rake, so the two upper boards overshoot x=0 and lap each other
        # at the apex, and each rake's two segments lap at the kink -- laid at one
        # depth those laps put two opaque faces on the same plane (measured 7.3
        # cm2 at the apex, the last true coincidence on this piece). Stepped, the
        # lapping face is always unambiguous, and 3 mm on a board tucked behind
        # the tympanum is invisible. The step goes to -Y on purpose: +Y would
        # walk the boards' back faces up towards the y=+0.12 seam, where
        # wobble() could push them over and clamp_to_seams() would flatten them
        # onto it.
        pts = _rake_pts(s)
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            y_rk = .035 - .003 * (i + (0 if s < 0 else 2))
            p.beam((a[0], y_rk, a[1]), (b[0], y_rk, b[1]), .150, .058,
                   "oak_dark", bevel=0, tint=.04)
        # eaves fascia: kept SHALLOW so the rafter tails hang below it. Its
        # inboard end runs 4 mm PAST P_BACK: cut dead on P_BACK its end cap sat
        # in the same plane as the roof patch's sheathing edge (12 cm2 of
        # coincident surface), and 4 mm deeper into the wall buries it.
        p.beam((s * (P_HW - .014), P_VERGE - .01, P_EAVE - .036),
               (s * (P_HW - .014), P_BACK + .004, P_EAVE - .036), .062, .072,
               "oak_dark", bevel=0, tint=.05, up=(0, 0, 1), shade=.86)
        # EXPOSED RAFTER TAILS: four per eave, bearing on the eaves plate and
        # running out to the fascia. This is the kit's signature and the reason
        # a 0.4 m overhang reads as a roof and not as a lid.
        # MEASURED, and both numbers were wrong. The tails are 86 mm wide and the
        # eaves plate they bear on runs y = -1.36 .. +0.06; the front tail sat at
        # y = -1.38, so 63 of its 86 mm hung off the FRONT END of the plate and
        # it bore on nothing but air. They now run P_FRONT .. P_BACK - 0.21, i.e.
        # -1.30 .. -0.16, so every one of the four sits wholly on the plate.
        # Their inboard ends were also cut at |x| = 0.595, which is 30 mm PAST
        # the plate's inner face (0.625): four square-cut ends hanging in the
        # soffit void with 97 mm of air above them. Ending at P_POST - 0.035
        # buries the lower 74 mm of each end inside the plate and tucks the rest
        # directly behind it. The tails stay PARALLEL to the bell-cast plane --
        # that is what keeps their top faces 21 mm inside the roof slab for their
        # whole length, and any tail steeper than the plane grazes the slab
        # underside at the eave.
        dz = _soffit_drop(P_HW) + RAFT * .5 * cos(radians(SW_DEG))
        x_in = P_POST - .035
        for i in range(4):
            y = lerp(P_FRONT, P_BACK - .21, i / 3.0)
            p.beam((s * x_in, y, _bell_z(x_in) - dz),
                   (s * (P_HW + .050), y, _bell_z(P_HW + .050) - dz),
                   RAFT, .086, "oak_dark", bevel=0, tint=.05, up=(0, 1, 0),
                   shade=1.14)
        # EXPOSED PURLIN ENDS: blocks stepping up the gable, tucked under the
        # toothed edge of the barge board, projecting out of the boarded
        # tympanum into the verge overhang.
        # 0.27 / 0.585, not 0.30 / 0.60: each block is 96 mm wide, so its side
        # faces landed at 0.348 and 0.552 -- and the tympanum's board joints fall
        # at 0.340 and 0.553. That put a 105 x 58 mm patch of board edge 1.0 mm
        # from a purlin's cheek, parallel and overlapping: under the 0.5 mm gate
        # only by luck. Moved, the nearest pair is 16 mm apart.
        for xf in (0.27, 0.585, 0.90):
            x = s * xf
            zt = _rake_z(x) - BARGE / _slope_cos(x)
            p.beam((x, P_FRONT + .03, zt - .058), (x, P_VERGE + .135, zt - .058),
                   .096, .112, "oak_dark", bevel=0, tint=.05, up=(0, 0, 1),
                   shade=1.12)

    # ridge board -- its front end is the ridge purlin poking out at the apex.
    # Shifted 3 mm into the wall for the fascia's reason: its back end was cut
    # dead on P_BACK, in the roof patches' own plane.
    p.box((0, (P_VERGE + .04 + P_BACK) / 2 + .003, apex + .026),
          (.125, P_BACK - P_VERGE - .04, .082), "oak_dark", bevel=0, tint=.04)
    # pinnacle finial
    fy = P_VERGE + .140
    p.box((0, fy, apex + .100), (.105, .105, .150), "oak_dark", bevel=0,
          tint=.05, shade=.90)
    p.box((0, fy, apex + .208), (.128, .128, .090), "oak_dark", bevel=0,
          tint=.05, rot=(0, 45, 0), shade=.90)
    p.cyl((0, fy, apex + .330), .044, .180, "oak_dark", sides=6, axis='Z',
          bevel=0, r_top=.005, tint=.05, shade=.90)

    # ---- roof
    width = (P_BACK - P_VERGE)
    ymid = (P_VERGE + P_BACK) / 2
    for i, (M, org, L) in enumerate(_porch_frames()):
        # width stepped per patch -- see PATCH_IN: all four sheathing plates
        # used to end on one plane at each end and they lap each other there.
        _courses(p, width - 2 * PATCH_IN[i], L + .015, (org.x, ymid, org.z), M,
                 seed=i, row=.190 if i % 2 == 0 else .232, tab=.30, thick=.042)
    p.wobble(.006, freq=1.5)
    return p.finish()


# =================================================================== steps ===
def threshold():
    """Doorstep: three dressed stone treads with raking timber handrails, exactly
    the flight ref3 puts in front of the porch. THE TOP TREAD IS THE FLOOR PLANE
    -- sink the piece 0.42, or stand the building on a 0.42 plinth as demo()
    does. A longer flight is the ground family's job."""
    W, D, RISE = 1.58, 0.94, 0.14
    p = Part("SM_Door_ThresholdSteps_2m", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(-D / 2, D / 2), z=(0, 1.44)))
    r = rng("steps")
    # "stone" goes in first so it owns material slot 0: the bevelled treads and
    # cheeks lose their own material to slot 0 (see porch()'s docstring), and
    # stone is the right average for them. shade drops it to a shadow tone.
    p.plate((0, .06, .18), (W - .06, D - .34, .36), "stone", tint=.03,
            shade=.42)
    # Everything above the base slab starts at z=+.008. Treads and cheeks used to
    # be modelled hanging BELOW the piece's floor plane, so finish() clamped a
    # hundred verts flat onto z=0 -- straight onto the slab's own underside, two
    # opaque faces in one plane. That single mistake was most of this piece's
    # z-fighting.
    treads = ((-D / 2, -D / 2 + .36), (-D / 2 + .32, -D / 2 + .68),
              (-D / 2 + .64, D / 2))
    for i, (y0, y1) in enumerate(treads):
        zt = RISE * (i + 1)
        zb = max(.008, zt - .17)
        n = 4 - (i // 2)
        wid = (W - .05) / n
        for j in range(n):
            cx = -W / 2 + .025 + wid * (j + .5)
            m = "stone_pale" if r.random() > .72 else (
                "stone" if r.random() > .28 else "stone_warm")
            p.box((cx + r.uniform(-1, 1) * .004, (y0 + y1) / 2 + r.uniform(-1, 1) * .005,
                   (zt + zb) / 2), (wid - .016, y1 - y0, zt - zb), m,
                  bevel=.022, seg=1,
                  tint=.085, taper=.985, skew=(0, r.uniform(-1, 1) * .006),
                  shade=1.0 + r.uniform(-.12, .10))
    # raking stone cheek walls, and the handrail on top of them. The blocks are
    # kept inside the y seams (they used to overhang the back one and get cut
    # flat onto the top tread's face) and each is a different width, so two
    # blocks that lap never present the same side plane twice.
    for s in (-1, 1):
        x = s * (W / 2 - .085)
        for i in range(3):
            ztop = RISE * (i + 1) + .05
            zbot = max(.016, ztop - .24)      # treads bottom out at .008
            p.box((x, lerp(-.255, .255, i / 2.0), (ztop + zbot) / 2),
                  (.145 + i * .010, .40, ztop - zbot), "stone", bevel=.020,
                  seg=1, tint=.07, shade=.90 + r.uniform(-.07, .05))
        # newels: front (low) and back (on the landing). The cap swallows the
        # post top and the knop's foot instead of butting onto them.
        for (yy, zz) in ((-D / 2 + .10, RISE), (D / 2 - .12, RISE * 3)):
            # THE FOOT IS SUNK 14 mm INTO THE STONE, not stood on it. zz is
            # exactly a tread's top face (RISE * i), so a newel whose bottom face
            # sits at zz puts a 104 x 104 mm face in the same plane as the tread
            # top -- 100 cm2 of coincidence, and the only reason it never
            # measured is that p.wobble tilts the tread's much larger quad a
            # couple of mm at that spot. The foot is inside the raking cheek wall
            # (which rises to RISE*(i+1) + .05) either way, so sinking it costs
            # nothing visually and closes the pair by construction. The top stays
            # exactly where it was, so the cap and knop above are unchanged.
            p.box((x, yy, zz + .423), (.104, .104, .874), "oak_mid", bevel=0,
                  tint=.05, taper=.93, shade=.86)
            p.box((x, yy, zz + .870), (.126, .126, .052), "oak_mid", bevel=0,
                  tint=.05, shade=.86)
            p.cyl((x, yy, zz + .940), .054, .100, "oak_mid", sides=6, axis='Z',
                  bevel=0, r_top=.008, tint=.05, shade=.86)
        a = Vector((x, -D / 2 + .10, RISE + .80))
        b = Vector((x, D / 2 - .12, RISE * 3 + .80))
        p.beam(tuple(a), tuple(b), .058, .076, "oak_dark", bevel=0,
               tint=.05, up=(1, 0, 0), shade=.95)
        lo_a = a - Vector((0, 0, .40))
        lo_b = b - Vector((0, 0, .40))
        p.beam(tuple(lo_a), tuple(lo_b), .042, .060, "oak_dark", bevel=0,
               tint=.05, shade=.9)
        for t in (.28, .58, .84):
            # A BALUSTER IS THINNER THAN THE RAIL IT STANDS IN. p.beam puts the
            # lower rail's 42 mm across X (up=(0,0,1) on a rake that runs in YZ),
            # so its cheeks are at x -/+ 0.021 -- and a 40 mm baluster's cheeks
            # landed 1 mm inside them, parallel and overlapping. Measured 8.3 cm2
            # at 0.175 mm once p.wobble had closed the last of it, 100%
            # ray-reachable from the flight, and the only coincidence left on
            # this piece. 28 mm buries each cheek 7 mm inside the rail (and 24 mm
            # inside the 76 mm top rail), which is what a housed baluster is.
            p.box((x, lerp(a.y, b.y, t), lerp(a.z, b.z, t) - .19),
                  (.028, .040, .40), "oak_dark", bevel=0, tint=.05, shade=.92)
    p.wobble(.006, freq=2.0)
    return p.finish()


# =============================================================================
# ============= THE ROUGH HALF OF THE FAMILY -- "_Rough" door leaves ==========
# =============================================================================
# "Similarly the wood on the walls and doors is too regular, let's add more
# irregular versions as well (but keep the regular ones as options just in case)."
#
# ADDITIVE. Every leaf above keeps its name and its mesh byte for byte; three of
# them gain a hand-worked sibling with _Rough on the end, so a level artist can
# put a crisp door on the front of the inn and a beaten one on the cellar.
#
# WHAT IS ACTUALLY DIFFERENT, and all of it is FORM, because these get judged in
# Solid shading where one material is one flat colour:
#
#   PLANK WIDTHS VARY MUCH MORE. The regular leaves draw board widths from
#   0.82-1.20 of the mean; these draw 0.66-1.42, and the groove between boards
#   varies with them instead of being a constant 20 mm. A hand-riven board is
#   whatever width the log gave.
#
#   BOARDS ARE CUPPED AND BOWED. `_swept` builds a board as a swept section
#   rather than a box, so its front face has a middle vertex: positive cup dishes
#   the board (the middle sits back, the arrises catch the light), negative cup
#   crowns it. Along its length the board BOWS out of the leaf plane, and it
#   leans a few mm off plumb. This is the change that carries the whole read --
#   in Solid shading a cupped board is two tones where a flat one is one.
#
#   EDGES ARE WORN. Every board is pulled back and narrowed at both ends, so its
#   corners are rounded off rather than cut dead square, and the arched head
#   band's outer edge wanders INWARD off the leaf's silhouette (never outward:
#   that edge is the x seam of an insert).
#
#   LEDGES ARE NOT PARALLEL. Each ledge gets its own tilt (15-25 mm across the
#   leaf), its own taper, and a bow, and the strap hinges FOLLOW them -- a strap
#   lies on its ledge, so a tilted ledge with a level strap would be worse than
#   no tilt at all.
#
#   NAILS AND PEGS WANDER. `_studs_rough` moves every nail off its grid, tilts
#   the heads, and varies their size; the ring pull and the knocker move with the
#   ledge they are fixed to.
#
# WHAT DOES NOT MOVE: the leaf is an INSERT. Its outline stays inside
# spec.OPENINGS minus INSERT_CLEAR, Z = 0 stays the bottom edge, the outer face
# stays on Y = 0 with the ironwork proud to -Y, and the depth ladder at the top
# of this file is obeyed rung for rung -- a rough leaf must drop into the same
# reveal as its regular twin and must not flicker doing it.


def _swept(p, a, b, w, thick, mat, seed=0, y=0.0, k=3, cup=0.0, bow=0.0,
           lean=0.0, taper=1.0, worn=0.0, dj=0.02, tint=.075, shade=1.0,
           mid=0.5):
    """ONE HAND-WORKED BOARD, from (x, z) to (x, z): swept, not extruded.

    A board is not a box. This walks k + 1 sections along the member's own axis
    with a FIVE vertex section -- three across the front face, two across the
    back -- which is what lets it be:

      cup     the middle of the front face set back (dished, the way a board
              cups as it dries) or forward (crowned). In flat light this is the
              difference between one tone and two
      bow     bent out of the leaf plane, deepest at mid-length
      lean     off plumb / off level end to end
      taper   narrower at the far end, the way a riven board is
      worn    both ENDS pulled back and narrowed, so the corners are rounded off
              instead of cut dead square
      dj      per-station jitter of width and thickness
      mid     WHERE the cup's crease runs, as a fraction of the width. Dead
              centre on every board is itself a regular pattern -- a crease down
              the exact middle of six boards in a row is a machined look -- so
              the caller wanders it

    10k + 6 tris, which is cheaper than the beveled box it replaces.
    """
    r = rng(f"{p.name}/swept/{seed}")
    ax, az = b[0] - a[0], b[1] - a[1]
    L = sqrt(ax * ax + az * az)
    if L < 1e-6:
        return []
    ux, uz = ax / L, az / L
    nx, nz = -uz, ux                      # perpendicular, in the leaf plane
    vs, F = [], []
    for i in range(k + 1):
        t = i / k
        end = (i == 0 or i == k)
        cx = a[0] + ax * t + nx * lean * (t - .5)
        cz = a[1] + az * t + nz * lean * (t - .5)
        hw = (w / 2) * lerp(1.0, taper, t) * (1 + r.uniform(-dj, dj))
        if end:
            hw -= worn * .9               # worn corners
        yf = y + bow * sin(pi * t) + (worn if end else 0.0)
        yb = yf + thick * (1 + r.uniform(-dj, dj))
        cupd = cup * (1 + r.uniform(-.25, .25))
        mo = hw * (2 * mid - 1)
        vs += [(cx - nx * hw, yf, cz - nz * hw),
               (cx + nx * mo, yf + cupd, cz + nz * mo),
               (cx + nx * hw, yf, cz + nz * hw),
               (cx + nx * hw, yb, cz + nz * hw),
               (cx - nx * hw, yb, cz - nz * hw)]
    for i in range(k):
        q, s = 5 * i, 5 * (i + 1)
        F += [(q, q + 1, s + 1, s), (q + 1, q + 2, s + 2, s + 1),
              (q + 2, q + 3, s + 3, s + 2), (q + 3, q + 4, s + 4, s + 3),
              (q + 4, q, s, s + 4)]
    F += [(0, 1, 2, 3, 4), (5 * k + 4, 5 * k + 3, 5 * k + 2, 5 * k + 1, 5 * k)]
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _boards_rough(p, x0, x1, n, z_bot, top_fn, y0, thick, mat, seed=0,
                  hole=None, tint=.085, cup=.009, bow=.007, lean=.007,
                  wide=(.66, 1.42), groove=(.030, .062), curve=0):
    """The rough leaf's boarding. Same contract as `_boards` -- fill x0..x1 with
    n boards cut to top_fn(x), stepping round an optional glazed hole -- but the
    widths and the grooves between them vary hard, and each board is a cupped,
    bowed, worn `_swept` instead of a box.

    The cup ALTERNATES in sign down the run: boards cupped the same way read as
    corrugation, boards cupped alternately read as a plank door that has been
    out in the weather for fifty years.

    TWO FAULTS OFF THE MODEL WERE BOTH IN HERE, and this is the leaf the reviewer
    was actually looking at (SM_Door_CellarDouble_1m_Rough):

      * `groove` was 8.5-15.5% of the board's own width, i.e. 14-25 mm on a
        160 mm board, with the dark backing slab behind it. That is not a joint,
        it is a hole -- "gaps between the vertical wooden beams". 3.0-6.2% now,
        so 5-10 mm: still visibly uneven board to board, which is the whole point
        of the rough leaf, but tight.
      * every board was cut SQUARE to the LOWEST height the arch reached across
        its own width (`min` of the two edges), so under a curved head the tops
        stepped down away from the arch and left a staircase of voids opening
        onto the backing slab -- "the beams end low from the arch instead of
        getting to the top and tapering/being cut to fit". `curve` > 0 now cuts
        the board's top edge TO the curve, the same way `_boards` does, so every
        board runs right up and each is a little shorter than its neighbour.

    AND THE BOW NOW ONLY EVER GOES ONE WAY: PROUD, towards the viewer. It used to
    be signed, so a board could bow up to 5.6 mm INTO the leaf -- and the depth
    ladder at the top of this file puts five things just behind the board face,
    each buried by 5-8 mm: the wicket bars' backs at +0.006, the ring pull's rose
    cap at +0.005, the barred slot's bars at +0.008. A board bowing inward
    surfaces through all of them. Measured on SM_Door_ArchPlank_1m_B_Rough: 83
    cm2 of one board's front face against the back of a wicket bar, 0.43 mm
    apart, the worst single pair on any leaf in the family. A board that bows
    proud is exactly as hand-made to look at and cannot reach anything, because
    everything in front of the boarding is ironwork standing 20 mm clear."""
    if x1 < x0:
        x0, x1 = x1, x0
    r = rng(f"{p.name}/rboards/{seed}")
    ws = [r.uniform(*wide) for _ in range(n)]
    k = (x1 - x0) / sum(ws)
    ws = [w * k for w in ws]
    u = x0
    for i, w in enumerate(ws):
        g = w * r.uniform(*groove)
        a, b = u + g / 2, u + w - g / 2
        u += w
        cu = (a + b) / 2
        # a curve-cut board runs to the HIGH corner of the arch over its own
        # width; a square-cut one can only stop at the low corner
        zt = (max(top_fn(a), top_fn(b)) if curve
              else min(top_fn(a + .01), top_fn(b - .01)))
        spans = [(z_bot, zt)]
        if hole:
            h = hole(cu, b - a)
            if h and h[0] < zt:
                spans = []
                if h[0] - z_bot > 0.06:
                    spans.append((z_bot, h[0]))
                if zt - h[1] > 0.05:
                    spans.append((h[1], zt))
        sgn = (1.0 if i % 2 else -0.75) * r.uniform(.30, 1.25)
        mid = r.uniform(.34, .66)
        for (za, zb) in spans:
            if zb - za < 0.02:
                continue
            if curve and zb >= zt - 1e-9:
                # The top board of a run under a curved head: a prism whose top
                # edge IS the curve, not a swept box with a flat top. A prism
                # cannot cup the way _swept does, so the hand-worked variation
                # it does keep is carried the other three ways -- it stands a
                # little in or out of the leaf plane, it tapers, and its foot
                # and its top edge both wander.
                th = thick * r.uniform(.90, 1.06)
                jx = r.uniform(-1, 1) * .003
                tp = r.uniform(0.0, .007)          # riven taper up the board
                # OUT of the leaf plane ONLY -- never in. See the note below.
                dy = -r.uniform(.15, 1.0) * bow * .8
                pts = [(a + jx, za), (b + jx, za)]
                for q in range(curve + 1):
                    x = lerp(b - tp, a + tp, q / curve)
                    pts.append((x + jx, max(top_fn(x), za + .012)))
                p.prism(pts, th, mat, axis='Y', at=(0, y0 + dy + th / 2, 0),
                        bevel=.004, seg=1, tint=tint,
                        shade=1.0 + r.uniform(-.13, .10))
                continue
            _swept(p, (cu, za), (cu, zb), b - a, thick * r.uniform(.90, 1.06),
                   mat, seed=f"{seed}/{i}/{za:.2f}", y=y0, k=3, mid=mid,
                   cup=cup * sgn, bow=-bow * r.uniform(.15, 1.0),
                   lean=lean * r.uniform(-1, 1), taper=r.uniform(.94, 1.0),
                   worn=.005, tint=tint, shade=1.0 + r.uniform(-.12, .09))


def _ledge_rough(p, r, W, zc, tilt, h, y=-.035, thick=.046, mat="oak_dark",
                 seed=0, inset=.018, shade=.86):
    """One ledge, out of level by `tilt` across the leaf, tapered, bowed and worn
    at both ends. Returns (za, zb) so the strap hinge and the ring pull can be
    hung off the ledge's ACTUAL line instead of the level one it used to be."""
    za, zb = zc - tilt / 2, zc + tilt / 2
    _swept(p, (-W / 2 + inset, za), (W / 2 - inset, zb), h, thick, mat,
           seed=f"ledge{seed}", y=y, k=3, cup=-.005, bow=-.004,
           taper=r.uniform(.90, 1.00), worn=.006, dj=.03, tint=.05,
           shade=shade)
    return za, zb


def _ledge_z(W, za, zb, x):
    """Height of a tilted ledge at x, so ironwork can sit ON it."""
    return lerp(za, zb, clamp((x + W / 2) / W))


def _studs_rough(p, r, xs, zs, y=-.030, mat="iron", rad=.019, seed=0):
    """Nail heads that were driven by hand: off the grid in both axes, tilted,
    and not one of them the same size."""
    for i, x in enumerate(xs):
        for k, z in enumerate(zs):
            p.cyl((x + r.uniform(-.016, .016), y + r.uniform(-.004, .004),
                   z + r.uniform(-.014, .014)),
                  rad * r.uniform(.78, 1.22), .026, mat, sides=5, axis='Y',
                  bevel=0, r_top=rad * .55, tint=.03,
                  rot=(r.uniform(-9, 9), 0, r.uniform(-9, 9)))


def _arc_band_rough(p, r, y, thick, r_out, r_in, spring, mat, segs=14, tint=.06,
                    shade=.97):
    """`_arc_band`, hand-cut: the band's width swells and shrinks round the arch
    and its outer edge wanders. INWARD ONLY -- that edge is the leaf's own
    silhouette, i.e. the x seam of an insert, and a board standing outside it
    would be clamped flat by finish() and rattle in its frame."""
    outer, inner = [], []
    for i in range(segs + 1):
        aa = pi * i / segs
        ro = r_out - r.uniform(0, .004)
        wi = (r_out - r_in) * (1 + r.uniform(-.12, .12))
        outer.append((ro * cos(aa), spring + ro * sin(aa)))
        inner.append(((ro - wi) * cos(aa), spring + (ro - wi) * sin(aa)))
    p.prism(outer + inner[::-1], thick, mat, axis='Y', at=(0, y, 0), bevel=0,
            seg=1, tint=tint, shade=shade)


# ------------------------------------------------------------- rough leaves ---
def arch_door_rough(variant="A"):
    """`arch_door`'s hand-worked twin, for OPENINGS['door_main'].
    A: amber lattice light in the head, two ledges out of level, hinges left.
    B: heavy studded leaf, iron-barred wicket, braced, nails all over the place.
    """
    W, H = _ins("door_main")
    r, spring = _arch_geo(W, H)
    p = Part(f"SM_Door_ArchPlank_1m_{variant}_Rough", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(0, .24), z=(0, H)))
    rr = rng(f"{p.name}/hand")
    RAIL = .105
    R_IN, R_OUT = r - RAIL - .006, r - .006   # the hand-cut band's two arcs
    top = _band_top(R_IN, R_OUT, spring, frac=.45)
    # A WORN LEAF IS A HAIR SMALLER than a new one, and it has to be:
    # p.wobble(respect_seams=False) moves the outline and x = +/-W/2 is this
    # insert's own seam, so an outline built dead on it gets cut back by
    # finish() -- reported as 5 mm of clamping on the first build of this piece.
    # 4 mm off the outline is free, honest, and leaves the report clean.
    p.prism(_arch_outline(W - .008, H - .006), .038, "oak_dark", axis='Y',
            at=(0, Y_SLAB, 0), bevel=.008, seg=1, tint=.04, shade=.52)

    if variant == "A":
        nb, mat, sgn = 6, "oak_mid", -1
        lw, lz0, lz1 = .54, 1.20, 1.90
    else:
        nb, mat, sgn = 7, "oak_mid", 1
        lw, lz0, lz1 = 0.0, 0.0, 0.0

    hole = None
    lr = lw / 2
    lsp = lz1 - lr
    ltop = lambda x: (lsp + sqrt(max(lr * lr - x * x, 0.0))) if abs(x) < lr else lsp
    if lw > 0:
        def hole(cx, wid):
            if cx - wid / 2 > lr - .01 or cx + wid / 2 < -lr + .01:
                return None
            xs = (cx - wid / 2, cx, cx + wid / 2)
            return (lz0 - .014, max(ltop(clamp(x, -lr, lr)) for x in xs) + .014)

    _arc_band_rough(p, rr, .002, .046, R_OUT, r - RAIL - .004, spring, mat,
                    segs=14, tint=.06, shade=.97)
    # springing rail: stubs each side on a glazed leaf so nothing crosses the
    # glass, one rail on the unglazed one -- and out of level either way.
    # Y_RAIL_R, not the regular leaf's 0.008: a rough board BOWS out of the leaf
    # plane by up to 7 mm, so a rail whose front face sits 8 mm behind the board
    # faces surfaces through the middle of any board that bowed inward -- visible
    # on the unglazed rough leaf as a pale rail lying across its own boarding.
    if lw > 0:
        for s in (-1, 1):
            # lr + .022, not lr + .040: the stub has to die INSIDE the bead's
            # head member (which reaches lr + REACH), and the glazing is laid
            # rigid after the wobble, so 6 mm of lap could open into a slot while
            # 24 mm cannot. Same change as the regular leaf.
            xa, xb = s * (W / 2 - .002), s * (lr + .022)
            _swept(p, (xa, spring + rr.uniform(-.008, .008)),
                   (xb, spring + rr.uniform(-.008, .008)), .030, .042, mat,
                   seed=f"spring{s}", y=Y_RAIL_R, k=2, cup=-.004, worn=.004,
                   tint=.05, shade=.95)
    else:
        _swept(p, (-W / 2 + .002, spring - .007), (W / 2 - .002, spring + .009),
               .030, .042, mat, seed="spring", y=Y_RAIL_R, k=3, cup=-.004,
               bow=-.003, worn=.004, tint=.05, shade=.95)
    xa, xb = -W / 2 + .013, W / 2 - .013
    if lw > 0:
        # three runs plus a spandrel fill, exactly as on the regular leaf: see
        # the note there. The rough leaf's boards vary in width even harder, so
        # the slot beside the light was wider still.
        e = lr + .004
        nl = max(1, int(round(nb * (-e - xa) / (xb - xa))))
        nm = max(2, nb - 2 * nl)
        _boards_rough(p, xa, -e, nl, .012, top, 0.0, .044, mat,
                      seed=f"{variant}L", curve=4)
        _boards_rough(p, -e, e, nm, .012, top, 0.0, .044, mat, seed=variant,
                      hole=hole, curve=4)
        _boards_rough(p, e, xb, nl, .012, top, 0.0, .044, mat,
                      seed=f"{variant}R", curve=4)
        # ring_out as on the regular leaf: the fill's arc has to die under the
        # bent head, not outside it -- see the note there.
        # own rung of the depth ladder, 0.012 .. 0.030 -- see the regular leaf
        _spandrel(p, lr, lsp, lz1 + .016, .012, .018, mat, ring_out=LAP - .014,
                  tint=.085, shade=.97)
    else:
        _boards_rough(p, xa, xb, nb, .012, top, 0.0, .044, mat, seed=variant,
                      curve=4)

    # ---- ledges, none of them level, and the ironwork follows them
    if variant == "A":
        lz = [_ledge_rough(p, rr, W, .420, +.019, .118, seed=0),
              _ledge_rough(p, rr, W, 1.045, -.024, .112, seed=1)]
    else:
        # the top ledge comes UNDER the wicket, not across it -- see the regular
        # leaf. Here it was measurable: this leaf's ledge thickness jitter put
        # its back face within 0.9 mm of the three wicket bars' back faces.
        lz = [_ledge_rough(p, rr, W, Z_LEDGE_B[0], -.021, .110, seed=0),
              _ledge_rough(p, rr, W, Z_LEDGE_B[1], +.017, .106, seed=1),
              _ledge_rough(p, rr, W, Z_LEDGE_B[2], -.014, .104, seed=2)]
        # both ends land on the ACTUAL line of the ledge they die into -- these
        # ledges are deliberately out of level, so a brace aimed at the nominal
        # height misses by the tilt as well as by the 20 mm the regular leaf was
        # out. Measured before: 6 mm of the lower end face proud of the ledge.
        xb0, xb1 = -W / 2 + .07, W / 2 - .07
        _swept(p, (xb0, _ledge_z(W, lz[0][0], lz[0][1], xb0)),
               (xb1, _ledge_z(W, lz[1][0], lz[1][1], xb1)), .100, .034,
               "oak_dark", seed="brace", y=-.029, k=3, cup=-.005, bow=-.004,
               taper=.90, worn=.006, tint=.05, shade=.88)
        p.box((0, .035, 1.74), (.32, .034, .32), "oak_dark", bevel=.006, seg=1,
              tint=.04, shade=.45)
        for x in (-.086, 0, .086):
            p.box((x + rr.uniform(-.008, .008), -.012, 1.74),
                  (.026, .036, .32 * rr.uniform(.94, 1.0)), "iron", bevel=0,
                  tint=.03, rot=(0, rr.uniform(-2.5, 2.5), 0))

    # ---- iron: the straps sit ON their ledges, so they take the ledge's line
    xe = sgn * (W / 2 - .038)
    for (za, zb) in lz[:2]:
        _strap(p, xe, _ledge_z(W, za, zb, xe), W * .66, -sgn)
    if variant == "B":
        _studs_rough(p, rr, [-W / 2 + .11 + i * (W - .22) / 4 for i in range(5)],
                     [(_ledge_z(W, a, b, 0.0)) for (a, b) in lz], seed="B")
    hx = -sgn * (W / 2 - .140)
    _pull(p, hx, _ledge_z(W, lz[1][0], lz[1][1], hx) - .045)
    p.wobble(.007, freq=1.8, respect_seams=False)
    if lw > 0:
        # SAME ONE CALL AS THE REGULAR LEAF, and below the wobble for the same
        # reason (see arch_door). The rough twin used to fork the glazing as well
        # as the joinery -- its own pane, its own hand-swept stiles and sill, its
        # own lattice -- which is exactly how five families ended up with five
        # different glazing bugs. The bead comes from Part.glazing() here too;
        # only the BENT HEAD is hand-cut, because that is joinery and not glazing
        # (`rough=rr`), and being hand-cut it does not need the noise field.
        _light_arched(p, lr, lz0, lsp, "glass", "oak_dark", .132, rough=rr)
    return p.finish()


def flat_door_rough():
    """`flat_door`'s hand-worked twin: five wildly uneven boards with a wandering
    top edge, two ledges out of level, a bowed brace, and nails driven by eye."""
    W, H = _ins("door_side")
    p = Part("SM_Door_FlatPlank_1m_Rough", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(0, .24), z=(0, H)))
    rr = rng(f"{p.name}/hand")
    p.plate((0, Y_SLAB, H / 2), (W - .014, .038, H - .010), "oak_dark", tint=.04,
            shade=.52)
    # THE TOP EDGE WANDERS. On a flat-headed leaf the board tops are the
    # silhouette, so this is the cheapest irregularity on the piece -- and it
    # only ever wanders DOWN, into the 20 mm the insert clearance already gives.
    top = lambda x: H - .008 - .010 * (1 + sin(2.6 * x + 1.1)) / 2
    _boards_rough(p, -W / 2 + .005, W / 2 - .005, 5, .012, top, 0.0, .044,
                  "oak_mid", seed="side", tint=.085)
    lz = [_ledge_rough(p, rr, W, .320, +.022, .124, inset=.012),
          _ledge_rough(p, rr, W, 1.600, -.018, .118, inset=.012, seed=1)]
    # ends on the tilted ledges' own lines: aimed at 0.38 / 1.54 against ledges
    # centred on 0.320 / 1.600 and tilted +/-22 mm, 37 mm of the lower end face
    # stood proud of the ledge it was supposed to be housed in.
    xb0, xb1 = -W / 2 + .06, W / 2 - .06
    _swept(p, (xb0, _ledge_z(W, lz[0][0], lz[0][1], xb0)),
           (xb1, _ledge_z(W, lz[1][0], lz[1][1], xb1)), .106, .034, "oak_dark",
           seed="brace", y=-.029, k=3, cup=-.005, bow=-.005, taper=.91,
           worn=.006, tint=.05, shade=.88)
    p.box((0, .035, 1.86), (.36, .034, .17), "oak_dark", bevel=.006, seg=1,
          tint=.04, shade=.45)
    for x in (-.10, 0, .10):
        p.box((x + rr.uniform(-.007, .007), -.008, 1.86), (.024, .032, .17),
              "iron", bevel=0, tint=.03, rot=(0, rr.uniform(-3, 3), 0))
    for (za, zb) in lz:
        _strap(p, -(W / 2 - .036), _ledge_z(W, za, zb, -(W / 2 - .036)),
               W * .68, 1)
    _pull(p, W / 2 - .130, _ledge_z(W, lz[0][0], lz[0][1], W / 2 - .130) + .64)
    p.box((W / 2 - .130, -.003, 1.20), (.095, .022, .130), "iron", bevel=.005,
          seg=1, tint=.03, rot=(0, rr.uniform(-3, 3), 0))
    p.wobble(.007, freq=1.8, respect_seams=False)
    return p.finish()


def cellar_door_rough():
    """`cellar_door`'s hand-worked twin: the two leaves are boarded to different
    widths, the four ledges all run out of level, and the braces are bowed. Same
    joinery logic as the regular leaf -- braces rise from the hinge stile to the
    free stile, the vision slot sits clear above the top ledges, pulls at hand
    height -- because those were bugs, not styling."""
    W, H = _ins("door_cellar")
    r, spring = _arch_geo(W, H)
    p = Part("SM_Door_CellarDouble_1m_Rough", budget="door",
             seams=dict(x=(-W / 2, W / 2), y=(0, .24), z=(0, H)))
    rr = rng(f"{p.name}/hand")
    RAIL = .115
    # THIS IS THE LEAF THE FAULT WAS REPORTED ON. It kept the old square cut --
    # every board stopped at the LOWEST height the arch reached across its own
    # width, so under the curve there was a stepped run of voids opening onto the
    # backing slab, 200 mm deep at the haunches. `_band_top` plus curve=4 runs
    # every board up to the arch and cuts it to the curve, each one a little
    # shorter than its neighbour, with the top edge buried inside the head band.
    R_IN, R_OUT = r - RAIL - .006, r - .010
    top = _band_top(R_IN, R_OUT, spring, frac=.45)
    p.prism(_arch_outline(W - .008, H - .006), .038, "oak_dark", axis='Y',
            at=(0, Y_SLAB, 0), bevel=.008, seg=1, tint=.04, shade=.52)
    lw, lz0, lz1 = .22, 1.42, 1.74
    lr = lw / 2
    Z_LEDGE = (.36, 1.26)
    Z_PULL = 1.00

    def hole(cx, wid):
        if abs(cx) > lr + wid / 2 - .01:
            return None
        return (lz0 - .014, lz1 + .014)

    # THE BAND STANDS PROUD OF THE BOARDING, 21 mm, the same way the regular
    # leaf's does and for the same reason: once the boards run up UNDER it their
    # front faces have to be buried inside it. Level with them (which is where it
    # was, y = 0.000) the overlap is a large coplanar patch, i.e. flicker.
    _arc_band_rough(p, rr, .002, .046, r - .006, r - RAIL - .004, spring,
                    "oak_mid", segs=15, tint=.06, shade=.97)
    for s in (-1, 1):
        _swept(p, (s * .014, spring + rr.uniform(-.007, .007)),
               (s * (W / 2 - .012), spring + rr.uniform(-.007, .007)),
               .030, .042, "oak_mid", seed=f"spring{s}", y=Y_RAIL_R, k=2,
               cup=-.004, worn=.004, tint=.05, shade=.95)
        # 5 mm off centre, not 18: see the note on the regular leaf's meeting
        # joint. 46 mm of open slot down the middle of the door was the widest
        # of the "gaps between the vertical wooden beams".
        # Two runs, split at the light's edge so the cut lands under the bead --
        # see the regular leaf. The rough boards vary in width even harder, so
        # the slot a straddling board left beside the light was wider still.
        e = s * (lr + .012)
        _boards_rough(p, s * .005, e, 1, .012, top, 0.0, .042, "oak_mid",
                      seed=f"cellarL{s}", hole=hole, tint=.085,
                      wide=(.70, 1.36), curve=4)
        _boards_rough(p, e, s * (W / 2 - .013), 3, .012, top, 0.0, .042,
                      "oak_mid", seed=f"cellar{s}", tint=.085,
                      wide=(.70, 1.36), curve=4)
    for s in (-1, 1):
        lz = []
        for i, z in enumerate(Z_LEDGE):
            tilt = rr.uniform(.014, .026) * (1 if (i + (s > 0)) % 2 else -1)
            za, zb = z - tilt / 2, z + tilt / 2
            _swept(p, (s * .026, za), (s * (W / 2 - .024), zb), .112, .046,
                   "oak_dark", seed=f"led{s}{i}", y=-.035, k=3, cup=-.005,
                   bow=-.004, taper=rr.uniform(.90, 1.0), worn=.006, dj=.03,
                   tint=.05, shade=.85)
            lz.append((za, zb))
        _swept(p, (s * (W / 2 - .07), Z_LEDGE[0]), (s * .10, Z_LEDGE[1]),
               .094, .034, "oak_dark", seed=f"brace{s}", y=-.029, k=3,
               cup=-.005, bow=-.004, taper=.92, worn=.006, tint=.05, shade=.88)
        for (za, zb) in lz:
            xr = s * (W / 2 - .034)
            _strap(p, xr, lerp(za, zb, .93), W * .34, -s)
        _pull(p, s * .120, Z_PULL + rr.uniform(-.02, .02))
    p.box((0, -.012, Z_PULL), (.062, .036, .20), "iron", bevel=.005, seg=1,
          tint=.03, rot=(0, rr.uniform(-2, 2), 0))
    p.wobble(.007, freq=1.8, respect_seams=False)
    # THE ONE FAULT LEFT ON THIS LEAF WAS THAT ITS LATHS OVERLAY THE RAILS.
    # The local lattice ran 30 mm past the light at both ends of every lath, and
    # it sat 1 mm in FRONT of the head and sill rails' own front faces, so the
    # ends that were supposed to die inside the frame lay across it instead --
    # visible as a fringe of lath ends on the rails, and the rails wobble 7 mm
    # so no margin could have fixed it. Part.glazing() cannot do that: it puts
    # the leading lead*2.6 BEHIND the bead's front face and clips the net to an
    # oversize pane, so the laths are buried by construction and every quarry
    # still meets the pane edge as a partial quarry. Same call as the regular
    # leaf -- the rough twin does not fork its glazing any more.
    #
    # Laid AFTER the wobble, like every other glazed light in this file: the
    # leading lies 1.70 mm off the pane and the noise field is 7 mm, which
    # measured 92 cm2 of glass against its own leading here.
    _light_rect(p, (lz0 + lz1) / 2, lw, lz1 - lz0, "glass", "oak_dark", .058)
    return p.finish()

# =================================================================== build ===
# MEASURING COINCIDENT SURFACE IN THIS FAMILY -- READ BEFORE CHASING A NUMBER.
# check_zfight.py buckets a face by n.dot(centre) and calls two faces coincident
# when min(|di-dj|, |di+dj|) is under tolerance. For a face at x=-0.78 with
# normal -X and its MIRROR TWIN at x=+0.78 with normal +X, both offsets come out
# the same, and the two faces project onto each other in the shared plane's
# tangent basis -- so a symmetric piece reports its own left half fighting its
# right half. That is most of what this family measures: the biggest single entry
# is SM_Door_ThresholdSteps_2m's 2155 cm2 "pair" at [0.76, 0.06, 0.18], which is
# the -X and +X faces of ONE p.plate() 1.52 m apart. A single box cannot fight
# itself. The same effect makes the family total swing 2x between runs, because
# whether a mirror pair slips under the 0.2 mm test depends on the sub-millimetre
# vertex jitter bmesh leaves in each Blender process.
#
# So: judge a fix by whether two faces are at the SAME coordinate, i.e. compare
# |n_i . (c_j - c_i)|, not |n.c| against |n.c|. Measured that way this family
# holds well under 40 cm2 in total, none of it visible, and the porch holds zero.
def build():
    """The seven regular pieces first -- they keep their exact names and are the
    family's default -- then the three hand-worked leaves."""
    return [arch_door("A"), arch_door("B"), arch_door("C"), flat_door(),
            cellar_door(), porch(), threshold(),
            arch_door_rough("A"), arch_door_rough("B"), flat_door_rough(),
            cellar_door_rough()]


# ==================================================================== demo ===
Z0 = 0.42            # demo plinth height = the building's floor plane


def _ashlar(p, x0, x1, z0, z1, seed, depth=.095, course=.34, mask=None,
            plinth=False):
    """Coursed stone facing for the demo backdrop only: rectangular dressed
    blocks, since ref2/ref3's entrance bay is dressed stone, not rubble."""
    if x1 - x0 < .04 or z1 - z0 < .04:
        return
    r = rng(f"ctx/{seed}")
    rows = max(1, int(round((z1 - z0) / course)))
    ch = (z1 - z0) / rows
    for i in range(rows):
        cz = z0 + ch * (i + .5)
        u = x0 - (0.0 if i % 2 else ch * .55)
        while u < x1 - .03:
            w = ch * r.uniform(1.15, 2.25) * (1.35 if plinth else 1.0)
            w = min(w, x1 - u)
            if x1 - (u + w) < ch * .5:
                w = x1 - u
            cx = u + w / 2
            u += w
            if mask and not mask(cx, cz, w, ch):
                continue
            m = "stone"
            q = r.random()
            if q < .22:
                m = "stone_pale"
            elif q < .34:
                m = "stone_warm"
            elif q < .42:
                m = "stone_dark"
            p.box((cx, -depth / 2 + .004, cz), (w - .024, depth, ch - .024), m,
                  bevel=.016, seg=1, tint=.075, taper=.97,
                  skew=(r.uniform(-1, 1) * .006, 0),
                  shade=1.0 + r.uniform(-.13, .11))


def _ctx_wall():
    """DEMO SCENERY, not a kit piece: a plain dressed-stone frontage with the
    three door openings plus the raised plinth ref2's entrance sits on, so the
    inserts are judged in a real reveal instead of floating in space."""
    T, HW = S.T_STONE, 4.55 + Z0
    p = Part("_DEMO_ContextWall", smooth=True)
    bays = ((-2.0, "door_cellar"), (0.0, "door_main"), (2.0, "door_side"))
    holes = []
    for (bx, key) in bays:
        o = S.OPENINGS[key]
        w, h = o["w"], o["h"]
        ar = o["head"] == "arch"
        r = w / 2
        holes.append((bx, w, h, (h - r) if ar else h, r, ar))

    xs = [-3.0]
    for (bx, w, h, sp, r, ar) in holes:
        xs += [bx - w / 2, bx + w / 2]
    xs += [3.0]
    for i in range(0, len(xs) - 1, 2):
        a, b = xs[i], xs[i + 1]
        if b - a > .02:
            p.plate(((a + b) / 2, T / 2, Z0 + (HW - Z0) / 2),
                    (b - a, T, HW - Z0), "stone_dark", tint=.03, shade=.5)
    for (bx, w, h, sp, r, ar) in holes:
        z = Z0 + h + (.02 if ar else .0)
        p.plate((bx, T / 2, (z + HW) / 2), (w, T, HW - z), "stone_dark",
                tint=.03, shade=.5)
        p.plate((bx, T - .09, Z0 + h / 2), (w + .02, .18, h), "stone_dark",
                tint=.03, shade=.22)
        for s in (-1, 1):
            p.plate((bx + s * (w / 2 - .045), .18, Z0 + h / 2), (.09, .36, h),
                    "stone_pale", tint=.05, shade=.85)
        if ar:
            p.arch((bx, .10, Z0 + sp), r + .215, .28, "stone_pale",
                   thickness=.215, segs=10, span=180, tint=.06,
                   tint_seed=f"a{bx}", bevel=.014)
        else:
            p.box((bx, .11, Z0 + h + .095), (w + .40, .30, .19), "oak_dark",
                  bevel=.018, seg=1, tint=.05)

    def mask(cx, cz, w, ch):
        for (bx, ow, h, sp, r, ar) in holes:
            if ar:
                if abs(cx - bx) < ow / 2 + w / 2 and cz < Z0 + sp + .02:
                    return False
                d = ((cx - bx) ** 2 + (cz - Z0 - sp) ** 2) ** .5
                if d < r + .245 + max(w, ch) * .38 and cz > Z0 + sp - .02:
                    return False
            elif (abs(cx - bx) < ow / 2 + w / 2 + .18
                    and cz < Z0 + h + .21 + ch * .35):
                return False
        return True

    _ashlar(p, -3.0, 3.0, Z0, Z0 + .42, seed="pl", depth=.125, course=.42,
            plinth=True)
    _ashlar(p, -3.0, 3.0, Z0 + .42, HW - .26, seed="f", mask=mask)
    _ashlar(p, -3.0, 3.0, HW - .26, HW, seed="cap", depth=.15, course=.26)
    # the plinth / platform the building stands on
    p.box((0, (T - .62) / 2, Z0 / 2), (6.0, T + .62, Z0), "stone", bevel=.02,
          seg=1, tint=.06, shade=.94)
    p.box((0, (-.58 - 1.60) / 2, Z0 / 2), (2.02, 1.02, Z0), "stone", bevel=.02,
          seg=1, tint=.06, shade=.94)
    p.wobble(.008)
    return p.finish()


def demo():
    """One inn frontage: cellar doors in the left bay, the porch and front door
    in the centre with its stone steps, the kitchen door on the right, and a
    spare leaf leaning by the corner."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = [_ctx_wall()]

    def put(nm, loc, rot=(0, 0, 0)):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = [radians(a) for a in rot]
        out.append(o)
        return o

    R_ = S.REVEAL
    # the rough leaves are in the openings, the regular ones leaning by the
    # corner, so demo.png shows both halves of the family in one frame and in
    # the same light: same silhouette, same reveal, different surface
    put("SM_Door_CellarDouble_1m_Rough", (-2.0, R_, Z0))
    put("SM_Door_ArchPlank_1m_A_Rough", (0.0, R_, Z0))
    put("SM_Door_FlatPlank_1m_Rough", (2.0, R_, Z0))
    put("SM_Door_PorchGable_2m", (0.0, 0.0, Z0))
    put("SM_Door_ThresholdSteps_2m", (0.0, -2.06, 0.0))
    put("SM_Door_ThresholdSteps_2m", (2.0, -1.06, 0.0))
    put("SM_Door_ArchPlank_1m_C", (2.94, -0.34, Z0), rot=(0, 12, 0))
    put("SM_Door_ArchPlank_1m_B_Rough", (4.22, -0.16, Z0), rot=(0, 15, 0))
    for nm in src:
        src[nm].location = (0, 40, 0)
    return out
