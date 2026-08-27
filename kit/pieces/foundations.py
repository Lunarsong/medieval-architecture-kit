"""Foundations -- the modular base layer the whole inn stands on.

Shanee: "the entrance comes out of the inn a bit with its cover and steps, and the
entire inn is on foundations that elevate it slightly ... foundations and
terraced/layered levels".  Both references have it: ref3:stone_arch draws the
stone storey standing on a low course of big squared blocks with a capping band
that oversails it, and ref1:barrels has the whole yard terraced, the terrace edge
retained by a heavy capped kerb with moss in the joint.  Neither building sits on
the dirt.

===========================================================================
WHAT THIS FAMILY IS
===========================================================================
A course of masonry, spec.H_FOUND (0.45) tall, that goes UNDER a storey and
stands spec.FOUND_OUT (0.11) PROUD of the wall it carries.  Everything follows
the WALL convention exactly -- outer face on y = 0, body to +y, x in
[-GRID/2, +GRID/2] -- so a wall bay dropped at z = H_FOUND lands on it with no
arithmetic, and the 110 mm step at the top of the foundation is what reads, from
across the street, as "the building is on a base".

    SM_Found_Plinth_2m_A/_B   the standard course
    SM_Found_Corner           the T x T outside corner (outward="xy")
    SM_Found_CornerInner      the T x T RE-ENTRANT corner, for a base that comes
                              forward for a porch: two outside corners at the
                              front angles and two of these at the returns
    SM_Found_Step_2m          the top steps DOWN by FOUND_STEP: the terrace piece
    SM_Found_Batter_2m        battered base course for the tallest exposed side
    SM_Found_Vent             cellar vent, so the base is not blank
    SM_Found_Riser_2m         extra H_FOUND/2 course for fine adjustment

===========================================================================
HOW A TERRACED RUN IS ASSEMBLED  (this is the "layered levels" part)
===========================================================================
The TOP of the foundation is the datum -- it is the floor line, and it must be
level along a run because a wall sits on it.  The GROUND is not level.  So:

  * on a slope the foundation is simply buried deeper uphill;
  * where the ground falls away far enough that the course would run out, slide
    SM_Found_Riser_2m UNDER the bay (place it at z = -H_FOUND/2).  The top stays
    where it was and the visible face gets half a course taller;
  * where the FLOOR LEVEL itself has to change -- a lower entrance terrace, a
    wing stepped down the hill -- use SM_Found_Step_2m.  Its top is at H_FOUND at
    the -x end and at H_FOUND - FOUND_STEP at the +x end, so the next bay is
    placed at z = -FOUND_STEP and its cap lands exactly on the step's low cap.
    The ground drops with it, at the step piece's low seam.

demo() builds precisely that, around a base that PROJECTS: an entrance 2.72 m
across and coming 2.36 m forward of the main wall face on an upper terrace,
dressed with all four corners a projection needs, then the main elevation
stepping down a terrace, turning an outside corner into a battered side run and
picking up a riser where the ground falls away. A stand-in wall band sits on the
coping throughout so the FOUND_OUT setback is visible as a shadow line the whole
way round -- and it is drawn from the SAME arithmetic that places the pieces, so
a wall face and the face of the foundation under it cannot drift apart. See
_projection(): it is the pattern assemble_inn.py follows, and the reason the
projection's depth is deep*GRID + T while its width is wide*GRID + 2T.

===========================================================================
THE STONE: THE SAME MASON, ONE GRADE HEAVIER
===========================================================================
stone_walls' round 8 is the standard here and this family holds to it: a stone is
NOT a box.  Its face is a 4- to 7-sided polygon inscribed in the bed it is
allotted, with corners knocked off asymmetrically, one long edge dished, the
whole thing tapered and rolled a degree or two; it is extruded off the bed plane
through three rings so it keeps a 45-degree arris all round its face (the bright
cut edge, for 6n-4 tris); and the joints are a real mortar SURFACE 30 mm behind
the stone faces, patched so its tone varies, not a black slot.

What is different, because a footing is not a wall:
  * ONE course, 315 mm tall, where the walling above runs seven of 265.  Blocks
    are 0.26-0.50 long, i.e. 0.83-1.6:1 against the walling's 1.05-1.7:1 -- so
    they are SQUARER, and about a third bigger in area, which is what "one grade
    heavier" means on a base course.  (Longer is NOT heavier: the first cut ran
    them to 0.76, which is four half-metre slabs to a bay, and 2 m of that reads
    as a bench.)  Every bay is GUARANTEED at least one split cell -- a full-height
    closer beside two smaller stones stacked in one bed, ref1's "big stones at the
    bottom, smaller ones packed into the gaps" -- because left to an independent
    die per block it came up empty across three bays running, and a bay with no
    split cell in it is six squared blocks in a row.
  * JOINT .030 against the walling's .036: tighter, as dressed footings are.
  * fewer knocked corners, less taper, less roll: these blocks were squared. The
    ARRIS carries the detail instead -- a 45-degree cut ~20 mm wide all round
    every face, which on a 400 mm block is the thing that reads.
  * the course is bedded 30 mm below the coping, on an open BED JOINT, and capped
    by a coping with a SQUARE arris: a 15-degree weathered ledge, a 75-degree
    top-outer edge, a 67 mm vertical fascia and a 26 mm drip chamfer under the
    nose, whose nose oversails the mean block face by 37 mm. Ledge, bed joint and
    the shadow the nose casts into it are the family's signature line -- see the
    coping section for what was measured and why the chamfer moved.

===========================================================================
THE DEPTH LADDER  (no two solids in this module share a boundary plane)
===========================================================================
y is measured from the WALL face above, so every number here is negative =
standing proud.  Nothing in this module butts anything: each solid either stands
clear or bites LAP into its neighbour, so along any view ray the frontmost
surface is unambiguous (the bug stone_walls invented and documented).

    -.148  NOSE     the coping nose -- the proudest thing in the family
    -.126  FACE     the proudest block faces
    -.111           ... the MEAN block face, against the -.110 FOUND_OUT promises
                    the rest of the kit. Measured over a bay, the faces spread
                    -.101 to -.124: 23 mm of relief, which is what makes a
                    coursed face shade itself instead of reading as cladding.
                    The nose therefore oversails the mean face by 37 mm and the
                    PROUDEST face by 22 mm, and that oversail is the shadow.
    -.122           ... the inner foot of the coping's 26 mm drip chamfer, the
                    down-facing band that is dark in every shading mode
    -.106  WASH_Y   the back of the coping's weathered ledge: where the nose
                    block dies into the continuous bearing slab, and the plane
                    the slab's front face stands on.
    -.102           ... the back of the nose blocks, lapping BITE onto that slab
    -.060  BLK_Y    block BACKS, bedded INSIDE the mortar layer
    -.078/-.042     the mortar layer: block backs sit 18 mm inside it either way
    -.028  BED      the core's front face, buried behind the mortar
    +.360  T        the inner face; the core owns it

SM_Found_Batter_2m runs its own ladder (see BAT_*) because its faces lean out
45 mm over the course: a battered bay meeting a vertical one shows that step at
the joint, which is what a batter is.  Battered bays run with each other.

===========================================================================
THE COURSE GRID, top down
===========================================================================
    .450  H          the flat BEARING plane. A wall corner lands anywhere on
                     y in [WASH_Y, T] of it and finds dressed stone.
    .345  CAP_Z0     the coping's bed
    .315  BLK_TOP    the level top of the BLOCK course: cut there, not clamped,
                     so the 30 mm between it and the coping is an open bed joint
                     -- and so no block face can saw through the coping's soffit,
                     which is what serrated the family's strongest horizontal.
    .000             grade

Verified with check_zfight.py: 0 coincident surfaces in the family. Every piece
reports EMPTY, nothing is clamped -- the bearing planes that could have been (the
riser's top, the coping's bed, the bay seams) are CUT by _clip at build time --
and the seam planes are bit-identical between variants: A's +x seam and B's -x
seam are the same 23 vertices, measured, so a run of A B A shows one stone across
every bay edge and not a joint.
"""
import bpy
from math import sqrt, sin, cos, pi, radians
from mathutils import noise as _nz, Vector
from kit import spec as S
from kit.util import Part, rng, lerp, clamp, smoothstep

FAMILY = "foundations"
COLLECTION = "14_Foundations"

# --------------------------------------------------------------------- cell --
T = S.T_STONE            # .36  body depth: a footing is at least as thick as
                         #      the stone wall it carries
H = S.H_FOUND            # .45  one course
G = S.GRID
HX = G / 2
OUT = S.FOUND_OUT        # .11  how far the course stands proud of the wall
STEP = S.FOUND_STEP      # .30  terrace step
PROUD = OUT + .05        # .16  declared allowance, per the spec note
SEAMS = dict(x=(-HX, HX), y=(0, T), z=(0, H))

# --------------------------------------------------------------- face ladder --
NOSE = -(OUT + .038)     # -.148  coping nose. Out as far as the family's declared
                         # allowance safely permits (PROUD .16, and _wob moves a
                         # vertex up to WOB past it), because the ONLY thing that
                         # puts a dark line the length of the base is the coping
                         # oversailing the block faces far enough to cast one.
CAP_CD = .012            # THE ARRIS, and the round-9 change. This is no longer a
                         # 50-degree wash -- it is the FALL of a weathered LEDGE,
                         # 12 mm over the 46 mm between the nose and WASH_Y, i.e.
                         # 15 degrees. That makes the top-outer edge a 75-degree
                         # dihedral instead of a 43-degree one.
                         #
                         # WHY, measured. Round 8 put a 49.6-degree chamfer there,
                         # which IS over spec.SMOOTH_ANG and did shade as its own
                         # facet -- three hard bands, no bullnose. It still read as
                         # nothing: on a raked-sun elevation render the flat top
                         # measured L=168, the chamfer L=157 and the vertical nose
                         # L=147. An 11 L step is not a line. A 90-degree turn
                         # between the SAME two surfaces is worth 21 L, and the
                         # only thing worth more than that is a shadow. So the
                         # chamfer is spent where it earns: the top edge goes
                         # square (75 deg), the ledge sheds water at 15 deg, and
                         # the whole 105 mm of coping height goes into a 67 mm
                         # vertical fascia over a 26 mm down-facing drip.
CAP_CH = .042            # the ledge run: NOSE to WASH_Y. 12 over 42 = 16 deg.
DRIP = .026              # the drip chamfer under the nose, at 45 degrees, and now
                         # half as deep again as round 8's 17 mm. A face at 45
                         # degrees BELOW horizontal takes no sun at any elevation
                         # and no matcap light in Solid shading either, so this is
                         # 26 mm of guaranteed dark immediately above the ~25 mm
                         # the nose casts onto the blocks. Together they are the
                         # continuous 50 mm shadow line the base did not have.
WASH_Y = NOSE + CAP_CH   # -.106  the back of the weathered ledge, unchanged from
                         # round 8 so the bearing slab, the corner's bearing box
                         # and everything that lands on them keep their planes.
                         # 106 mm OUTSIDE y=0, so the wall above lands on flat
                         # stone with a 106 mm dressed ledge to spare.
FACE = -(OUT + .016)     # -.126  proudest block faces. Set by MEASUREMENT: the
                         # relief ramp and the tilt bias put the MEAN face 16 mm
                         # behind this, and at -.122 that landed the mean at -.105
                         # -- the family 5 mm short of the FOUND_OUT it promises
                         # the rest of the kit. (Moving BLK_Y instead does
                         # nothing: DEPTH is derived from the pair, so the face
                         # plane stays exactly where it was.)
BLK_Y = -.060            # block backs
DEPTH = BLK_Y - FACE     # .062  nominal relief
MORT_Y = -.078           # the joint plane
MORT_T = .036            # thick enough to swallow every block back
MORT_STEP = .006         # alternating patch parity
MORT_SHADE = .72
BED = -.028              # core front
LAP = .016               # how far one solid bites into the next
BITE = .004              # ...between two big plates whose corners are pinned
WOB = .005
NOISE_SEED = 20240823    # the kit-wide pinned noise seed (see stone_walls)

# ------------------------------------------------------------- course grid ----
CAP_H = .095             # the coping. 105 mm read as a lid on the first cut:
                         # nearly a quarter of the piece's height, in one pale
                         # unbroken tone, with a rolled nose.
CAP_Z0 = H - CAP_H       # .345  bed of the coping
BEDJ = .030              # THE BED JOINT, and the other half of the round-9 shadow
                         # line. The coping is bedded on a deep recessed joint
                         # rather than straight onto the block faces, so between
                         # the blocks' level top and the coping's soffit there is
                         # 30 mm of open recess 45 mm deep. That matters because a
                         # 450 mm base is ALWAYS looked down on from a street, and
                         # a downward view cannot see the drip chamfer, cannot see
                         # the soffit and gets only however much shadow the nose
                         # casts -- which measured 14 px of a 100 px band. A recess
                         # is dark from above by construction: the eye looks into
                         # a hole whose ceiling faces down and whose back is 45 mm
                         # in. It also fixes a real artefact: the blocks used to be
                         # laid LAP past CAP_Z0 with faces 4 mm PROUDER than the
                         # coping's drip chamfer, so every block sawed a visible
                         # serrated line through the coping's underside.
BLK_TOP = CAP_Z0 - BEDJ  # .315  level top of the block course: the bed the coping
                         #       sits on. Cut, not clamped -- see course(ceil=).
LOW_TOP = H - STEP       # .150  the step piece's low level
LOW_Z0 = LOW_TOP - CAP_H # .045  ...and its coping bed
RH = H / 2               # .225  the riser course

JOINT = .030             # a footing's joint. NOT the walling's .036, and not
                         # the .026 the first cut of this used either: at .026
                         # less overfill the joints closed to 8-15 mm and a
                         # 2 m bay read as one flat panel with lines drawn on it.
CHAMF = .014             # the arris knocked off a face all round
BLK_LO, BLK_HI = .26, .50   # SQUARER than the walling, which is what "one grade
                         # heavier" means on a 345 mm course: 0.64-1.45:1, mean
                         # 1.03:1. The first cut ran .30-.76, i.e. up to 2.2:1 --
                         # four half-metre slabs to a bay, which is a bench, not
                         # masonry. Bigger than the wall above in AREA (a .36
                         # square against its .36 x .265), not in length.
OV = (.005, .004)        # overfill: hand back the area a polygon gives up at
                         # every knocked corner, but no more -- see JOINT        # overfill: a polygon gives area back at every corner it
                         # knocks off, and the joints double if it is not handed
                         # back. Same lesson as stone_walls' OVER.

# --------------------------------------------------------- batter's own ladder -
BAT_BED = -.045
BAT_DEPTH = .070
BAT_MORT = -.062
BAT_BUILD = -.012        # core front
BAT_SLOPE = .128         # face lean, per metre of height: 44 mm over the course


# =========================================================== stone toolkit ===
# A stone is a polygon extruded off its bed with a 45-degree arris, not a box.
# stone_walls round 8 proved the point: `taper` and `skew` on a p.box() give you a
# slightly irregular QUADRILATERAL -- four sides, two of them still parallel --
# so an elevation built of them is ONE SHAPE SCALED, which is what reads as a
# pattern however wide you spread the sizes.  Footing blocks are squarer than
# walling, but square is not rectangular: these are dressed by hand, every corner
# is off, and the reference has no rectangles in it either.


def _unit(du, dv):
    m = sqrt(du * du + dv * dv)
    return (du / m, dv / m) if m > 1e-9 else (1.0, 0.0)


def _dedupe(poly, eps=8e-4):
    """Drop vertices that landed on their neighbour. A zero-length edge makes
    bmesh refuse the whole face and _emit swallows the error, so the stone would
    simply come out missing a side with nobody told."""
    out = []
    for q in poly:
        if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > eps:
            out.append(q)
    while len(out) > 3 and (abs(out[0][0] - out[-1][0])
                            + abs(out[0][1] - out[-1][1])) <= eps:
        out.pop()
    return out


def _outline(r, u0, u1, v0, v1, clips=(.34, .44, .20, .02), mid=.26, taper=0.0,
             flip=False, lean=0.0, roll=0.0, dish=.07, ju=.009, jv=.007):
    """The FACE of one squared footing block: a CCW polygon in absolute (u, v),
    drawn inside the rectangle its bed allots it.

    clips   distribution over HOW MANY of the four corners get knocked off. A
            knocked corner is the cheapest thing there is that says "cut by
            hand"; a footing gets fewer of them than a rubble wall, and never
            three, because these blocks were squared before they were laid.
    taper   narrows one end into a shallow wedge
    lean    shears the outline into a parallelogram
    mid     chance the longest edge gains a mid-point, so the block has an odd
            number of sides and its two long edges are not parallel
    dish    how far that mid-point dents in, as a fraction of the short side
    roll    roll in the plane of the elevation, radians
    """
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    hu, hv = (u1 - u0) / 2, (v1 - v0) / 2
    tu = hu * (1.0 - clamp(taper, 0.0, .26))
    if flip:
        base = [(-tu + lean, -hv), (tu + lean, -hv), (hu, hv), (-hu, hv)]
    else:
        base = [(-hu, -hv), (hu, -hv), (tu + lean, hv), (-tu + lean, hv)]
    ju, jv = min(ju, (u1 - u0) * .07), min(jv, (v1 - v0) * .08)
    pts = [(bu - (1.0 if bu > 0 else -1.0) * r.uniform(-.45, 1.0) * ju,
            bv - (1.0 if bv > 0 else -1.0) * r.uniform(-.45, 1.0) * jv)
           for (bu, bv) in base]
    q, acc, k = r.random(), 0.0, len(clips) - 1
    for i, wgt in enumerate(clips):
        acc += wgt
        if q < acc:
            k = i
            break
    order = [0, 1, 2, 3]
    r.shuffle(order)
    knock = set(order[:k])
    # NEVER BOTH ENDS OF A SHORT EDGE on anything elongated: cutting the two
    # corners that share a 200 mm end off a 700 mm block turns it into an
    # arrowhead, and a column of those is the most artificial thing a wall of
    # polygons can contain (stone_walls measured exactly that).
    lo_, hi_ = sorted((u1 - u0, v1 - v0))
    if hi_ > lo_ * 1.30:
        pairs = ((1, 2), (3, 0)) if (u1 - u0) > (v1 - v0) else ((0, 1), (2, 3))
        for (i, j) in pairs:
            if i in knock and j in knock:
                knock.discard(j if order.index(j) > order.index(i) else i)
    # KNOCK SIZES ARE CAPPED IN MILLIMETRES, not only as a fraction of the block.
    # Scaled purely off the short side, a corner cut ran to .50 * 371 mm = 185 mm
    # on a full-height footing block -- a slice off half its face, which is not a
    # dressed corner, it is a broken stone -- and on the SMALL blocks a split cell
    # puts in (160-180 mm tall) the same rule cut 80 mm off a 240 mm stone from two
    # corners at once and left a wedge with a hole round it. That is the "split
    # cells lose their upper block" the critic reported: the block was there, it
    # had just been dressed away. A knock is a knock: 40-80 mm of stone.
    m = min(u1 - u0, v1 - v0)
    # ...and capped as a FRACTION of the short side as well, which the millimetre
    # cap alone does not do. On the 220 x 180 packers a split cell puts in, an
    # 80 mm knock off two corners at once is 36 % of the face gone and the stone
    # stops reading as a stone -- which is half of "the split cells lose their
    # upper block". A knock is a knock: a third of the short side, 75 mm at most.
    mk = min(m * .34, .075)           # corner knocks
    md = min(m, .110)                 # the dished long edge
    out = []
    for i in range(4):
        c = pts[i]
        if i not in knock:
            out.append(c)
            continue
        prv, nxt = pts[i - 1], pts[(i + 1) % 4]
        din = _unit(c[0] - prv[0], c[1] - prv[1])
        dout = _unit(nxt[0] - c[0], nxt[1] - c[1])
        li = sqrt((c[0] - prv[0]) ** 2 + (c[1] - prv[1]) ** 2)
        lo = sqrt((nxt[0] - c[0]) ** 2 + (nxt[1] - c[1]) ** 2)
        # ASYMMETRIC. Two equal cuts make a 45-degree corner, and a field of
        # blocks each with one clean 45-degree corner is just another repeating
        # shape. So the legs are drawn independently and one is often cut right
        # back: "the corner came off when they dressed it", not "chamfered box".
        s_i, s_o = r.uniform(.14, .50) * mk, r.uniform(.14, .50) * mk
        if r.random() < .45:
            s_i, s_o = ((s_i * r.uniform(.25, .55), s_o) if r.random() < .5
                        else (s_i, s_o * r.uniform(.25, .55)))
        s_i, s_o = min(s_i, li * .38), min(s_o, lo * .38)
        out.append((c[0] - din[0] * s_i, c[1] - din[1] * s_i))
        out.append((c[0] + dout[0] * s_o, c[1] + dout[1] * s_o))
    out = _dedupe(out)
    if mid > 0.0 and len(out) <= 6 and r.random() < mid:
        n = len(out)
        j = max(range(n), key=lambda i: (out[(i + 1) % n][0] - out[i][0]) ** 2
                                        + (out[(i + 1) % n][1] - out[i][1]) ** 2)
        a, b = out[j], out[(j + 1) % n]
        du, dv = b[0] - a[0], b[1] - a[1]
        nu, nv = _unit(-dv, du)
        s = r.uniform(-.20, 1.0) * dish * md
        t = r.uniform(.38, .62)
        out.insert(j + 1, (a[0] + du * t + nu * s, a[1] + dv * t + nv * s))
    if roll:
        ca, sa = cos(roll), sin(roll)
        out = [(u * ca - v * sa, u * sa + v * ca) for (u, v) in out]
    return _dedupe([(u + cu, v + cv) for (u, v) in out])


def _clip(poly, plane, keep_lo, i=0):
    """The part of an outline on one side of plane `u = plane` (or v, with i=1).

    THE SEAM RULE, by construction rather than by clamp_to_seams. Two pieces
    meeting at a bay edge build the same polygon in the same seam-relative
    coordinates and cut it here on the same plane, so the vertices ON the cut are
    bit-identical between the two meshes and the stone reads as ONE stone across
    the joint. Clamping cannot do that: it snaps a stray vertex onto the plane
    and brings that vertex's own v and face depth with it, which is a step."""
    out, n = [], len(poly)
    j = 1 - i
    for k in range(n):
        a, b = poly[k], poly[(k + 1) % n]
        ia = (a[i] <= plane) if keep_lo else (a[i] >= plane)
        ib = (b[i] <= plane) if keep_lo else (b[i] >= plane)
        if ia:
            out.append(a)
        if ia != ib and abs(b[i] - a[i]) > 1e-9:
            t = (plane - a[i]) / (b[i] - a[i])
            q = [0.0, 0.0]
            q[i] = plane
            q[j] = a[j] + (b[j] - a[j]) * t
            out.append(tuple(q))
    return _dedupe(out)


def _stone(p, poly, bed, d, mat, tint, shade, at=(0.0, 0.0), axis='Y',
           grad=(0.0, 0.0), chamf=CHAMF, rings=3, pin=None, extent=None):
    """Extrude one block outline off its bed plane, toward the viewer.

    Three rings, and the middle one is the whole point: ring 0 is the outline on
    the bed plane (buried inside the mortar layer, where nothing can see it),
    ring 1 carries the same outline out to `chamf` short of the face, ring 2 is
    the face itself, inset by `chamf`. So the block has a square flank and then a
    45-degree arris all the way round its face -- the bright cut edge, for 6n-4
    tris where a beveled box spends 44.

    axis  'Y' -> u is x, the face grows -y (a wall-convention elevation)
          'X' -> u is y, the face grows -x (a corner's return elevation)
    grad  (gu, gv) tilt of the face plane. gv > 0 is a BATTER: the face leans
          back as it climbs. The bed stays flat, so the block is a wedge, thicker
          at the bottom -- which is what a battered footing block is.
    pin   a u the face inset must not move off (a seam plane), so a block cut at
          a bay edge still meets its other half face to face.
    """
    poly = _dedupe(poly)
    n = len(poly)
    if n < 3 or d <= .004:
        return []
    cu = sum(q[0] for q in poly) / n
    cv = sum(q[1] for q in poly) / n
    yf = lambda u, v: bed - d + grad[0] * (u - cu) + grad[1] * (v - cv)
    if extent is None:
        extent = ((max(q[0] for q in poly) - min(q[0] for q in poly)) / 2,
                  (max(q[1] for q in poly) - min(q[1] for q in poly)) / 2)
    dmin = min(bed - yf(u, v) for (u, v) in poly)
    # .55 of the shallowest depth, not .34: at .34 a 20 mm chamfer on a stone
    # bedded 60 mm deep was being cut back to 10 mm, and a 400 mm dressed block
    # whose arris is 10 mm has no arris -- which is most of why the first cuts of
    # this family read as soap bars. The ring still lands at .45 d, well in front
    # of the bed, so nothing inverts.
    c = min(chamf, max(dmin, .002) * .55, extent[0] * .20, extent[1] * .20)
    ins = []
    for (u, v) in poly:
        du = 0.0 if (pin is not None and abs(u - pin) < 1e-6) else \
            (-1.0 if u > cu else 1.0) * min(c, abs(u - cu) * .45)
        dv = (-1.0 if v > cv else 1.0) * min(c, abs(v - cv) * .45)
        ins.append((u + du, v + dv))
    a0, a1 = at
    if axis == 'Y':
        w = lambda u, y, v: (a0 + u, y, a1 + v)
    else:
        w = lambda u, y, v: (y, a0 + u, a1 + v)
    vs = [w(u, bed, v) for (u, v) in poly]
    F = []
    if rings >= 3:
        vs += [w(u, yf(u, v) + c, v) for (u, v) in poly]
        vs += [w(u, yf(u, v), v) for (u, v) in ins]
        for i in range(n):
            j = (i + 1) % n
            F.append((i, j, j + n, i + n))                    # flank
            F.append((i + n, j + n, j + 2 * n, i + 2 * n))    # the arris
        F.append(tuple(range(2 * n, 3 * n)))                  # the face
    else:
        vs += [w(u, yf(u, v), v) for (u, v) in ins]
        for i in range(n):
            j = (i + 1) % n
            F.append((i, j, j + n, i + n))
        F.append(tuple(range(n, 2 * n)))
    F.append(tuple(range(n))[::-1])                           # bed face
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _wob(p, amount=WOB, **kw):
    """p.wobble() with the noise field PINNED first. mathutils.noise is seeded
    per Blender PROCESS and Part.wobble displaces by noise_vector, so without
    this "same code, same mesh" is simply false: two builds of identical code
    come out millimetres apart and a rebuild does not reproduce the .blend
    anybody is looking at. Same seed as stone_walls, timber_walls and corners --
    it is one kit-wide bug whose proper home is util, which a piece may not
    edit. Nothing in this module calls p.wobble() directly."""
    _nz.seed_set(NOISE_SEED)
    p.wobble(amount, **kw)


def _blotch(u, v, seed=1, f=.62):
    """Smooth -1..1 field. Real masonry varies in PATCHES -- a run of warm
    blocks, a damp dark corner at grade -- not block by block like confetti."""
    return _nz.noise((u * f + seed * 3.7, v * f + seed * 1.3, seed * .41))


def _tone(r, b, warm=.22, pale=.05, dark=.38, var=.05, damp=0.0, force=None):
    """Block material + shade.

    `force` overrides which material comes out WITHOUT skipping the draw, so the
    caller's random stream stays exactly where it was and the shade still gets the
    +.15 lift a stone_dark block needs to stay readable. It is how the two packers
    in one split cell are made to come out of the same batch of stone.

    WEIGHTS RETUNED (24 Aug): the intent below was right but the numbers were not
    delivering it. Measured against stone_walls, this family was using an almost
    IDENTICAL material mix (dark 11-17%, pale 13%), so at building scale the base
    read as more of the same wall rather than as a footing, and the whole foundation
    course became invisible in the hero render even though its stones genuinely stand
    85 mm proud of each other. Both references make the base the darkest, heaviest
    band in the elevation. dark is now the dominant draw and pale is nearly gone.

    A FOOTING IS WET: it is the thing standing in the
    mud, so the mix is pulled toward `stone` and `stone_dark` where the walling
    above is pulled toward pale ashlar, and `damp` (0 at the cap, 1 at grade)
    darkens it further. Value comes mostly from the patch field and only a
    little from the die -- the other way round is confetti, which averages back
    to one flat tone at any distance and reads as sample tiles up close."""
    q = r.random()
    d = dark + max(-b, 0.0) * .05 + damp * .10
    w = warm + max(b, 0.0) * .14
    pl = max(pale + max(b, 0.0) * .08 - damp * .07, 0.0)
    if q < d:
        m = "stone_dark"
    elif q < d + w:
        m = "stone_warm"
    elif q < d + w + pl:
        m = "stone_pale"
    else:
        m = "stone"
    if force is not None:
        m = force
    sd = (1.0 + b * .10 + r.uniform(-var, var) - damp * .07
          + (.15 if m == "stone_dark" else 0.0))
    return m, clamp(sd, .62, 1.12)


# ============================================================== the course ===
class Bed:
    """Everything a course needs to know about how its blocks are cut, bedded and
    coloured. One object rather than fifteen keyword arguments, because the
    plinth, the corner, the riser and the batter differ in exactly these numbers
    and every one of them has to be able to say which."""

    def __init__(self, y=BLK_Y, depth=DEPTH, mort=MORT_Y, mort_t=MORT_T,
                 joint=JOINT, bat=0.0, vmid=None, lo=BLK_LO, hi=BLK_HI,
                 long=.20, small=.14, split=.24, warm=.24, pale=.05, dark=.40,
                 var=.075, tint=.05, tilt=.014, damp=.45, axis='Y'):
        self.y, self.depth, self.mort, self.mort_t = y, depth, mort, mort_t
        self.joint, self.bat, self.vmid = joint, bat, vmid
        self.lo, self.hi = lo, hi
        self.long, self.small, self.split = long, small, split
        self.warm, self.pale, self.dark, self.var = warm, pale, dark, var
        self.tint, self.tilt, self.damp, self.axis = tint, tilt, damp, axis


PLINTH = Bed(split=.52, long=.22)
BATTER = Bed(y=BAT_BED, depth=BAT_DEPTH, mort=BAT_MORT, bat=BAT_SLOPE,
             vmid=CAP_Z0 / 2, lo=.26, hi=.56, long=.26, small=.10, split=.16,
             tilt=.008, warm=.28, pale=.14, dark=.15)
RISERB = Bed(y=-.068, mort=-.086, lo=.22, hi=.44, long=.16, small=.18,
             split=.16, warm=.26, dark=.20, pale=.10, damp=.85)
CORNERB = Bed(joint=.020, tilt=.007, long=0.0, small=0.0, split=0.0, pale=.24,
               warm=.32, dark=.06, damp=.30)

# THE BAND'S OWN BED. A "band" is the name of a continuous RUN of masonry -- every
# piece that can sit next to another piece at a bay seam and has to look like the
# same wall. The stone that STRADDLES that seam is therefore a property of the
# band, not of whichever piece is drawing its half: it has to be cut, bedded,
# toned and shaded off one set of numbers or the two halves disagree and the run
# grows a seam every 2 m. (SM_Found_Plinth_2m_B is the only piece in the family
# that varies its Bed, and it is exactly the piece the artefact showed up on.)
# `steplow` is added below, where LOWB is defined.
BAND_BED = {"plinth": PLINTH, "batter": BATTER, "riser": RISERB}


def _relief(bd, l):
    """How far a block stands out of its bed. Longer stones sit prouder. The
    SPAN of this is the difference between masonry and stone-tile cladding: with
    every face inside a 9 mm band the joints never fall into shadow and no block
    ever casts onto its neighbour. A footing's spread is narrower than a rubble
    wall's -- these are squared blocks on a tight joint -- but it is not zero."""
    t = clamp((l - bd.lo) / max(bd.hi - bd.lo, 1e-6))
    return bd.depth * lerp(.72, 1.00, t)


def _one(p, r, u0, u1, v0, v1, bd, at=(0.0, 0.0), key="", pin=None,
         clips=None, floor=None, ceil=None, cut=(), relief_l=None,
         mat_lock=None, deep=1.0):
    """ONE BLOCK. Three shape families are drawn for every one of them, because
    what the eye picks up is not the range of SIZES but the fact that every stone
    is the same SHAPE: a wedge frankly narrower at one end, a polygonal boulder
    with most of its corners knocked off, and an ordinary squared block -- which
    is still never a rectangle, because its corners are pulled in unequally, one
    long edge is dished and the whole thing is rolled a degree in the plane.

    `relief_l` overrides the length _relief() is measured on, `deep` scales the
    result, and `mat_lock` forces the material. All three exist for ONE bug, the
    critic's "split cells lose their upper block", and the last round declared
    relief_l in the signature and then never read it, so nothing was fixed.

    MEASURED, on SM_Found_Plinth_2m_A. The two packers in a split cell came out at
    face y = -.101 with their full-height neighbours at -.117: 16 mm behind, most
    of a joint's worth of setback, because _relief() beds a stone on its OWN width
    and a packer is half a block wide. Put a stone_dark packer 16 mm back with a
    stone_pale one under it and what the eye gets is not two stones filling one
    bed, it is a bright stone with a hole over it. So:
      * both packers are bedded on `relief_l` = the length of the SLOT they share,
        which is the length their neighbours are bedded on, and set `deep` a
        little proud of it -- packers are driven in last and stand slightly out;
      * both take the same `mat_lock`, so they are two stones off the same cart
        rather than a pale one and a dark one, and the pair reads as a pair."""
    l, h = u1 - u0, v1 - v0
    if l < .05 or h < .04:
        return
    # A block need not fill its bed to the last millimetre: a few sit low or
    # high with a wedge of mortar over or under them, which is how you get a bed
    # line you can follow without getting one you can measure.
    if h > .13 and r.random() < .30:
        nick = min(r.uniform(.014, .038), h * .14)
        if r.random() < .5:
            v1 -= nick
        else:
            v0 += nick
        h = v1 - v0
    cv = (v0 + v1) / 2
    b = _blotch(u0 + at[0], cv + at[1])
    # wettest at grade, dry by the coping: the bottom of a footing stands in the
    # mud and both references have the base course darker than the wall above it
    damp = bd.damp * (1.0 - clamp(cv / max(CAP_Z0, 1e-6))) ** .7
    m, sd = _tone(r, b, bd.warm, bd.pale, bd.dark, bd.var, damp, force=mat_lock)
    q = r.random()
    if q < .14:            # a WEDGE
        cl, mid, tp, dish = (.30, .48, .20, .02), .18, r.uniform(.07, .17), .04
    elif q < .30:          # a polygonal BOULDER, most corners off
        cl, mid, tp, dish = (.02, .18, .48, .32), .34, r.uniform(0.0, .06), .08
    else:                  # an ordinary squared BLOCK -- still not a rectangle
        cl, mid, tp, dish = (.36, .44, .18, .02), .26, r.uniform(0.0, .05), .06
    poly = _outline(r, u0 - OV[0] / 2, u1 + OV[0] / 2, v0 - OV[1] / 2,
                    v1 + OV[1] / 2, clips=cl if clips is None else clips,
                    mid=mid, taper=tp, flip=r.random() < .5,
                    lean=r.uniform(-1, 1) * .006, dish=dish,
                    roll=r.uniform(-1, 1) * .022)
    if floor is not None:
        poly = _clip(poly, floor, False, i=1)
    if ceil is not None:
        poly = _clip(poly, ceil, True, i=1)     # a bearing plane, cut not clamped
    for (pl, keep_lo, i) in cut:
        poly = _clip(poly, pl, keep_lo, i)      # butt planes, cut not clamped
    d = _relief(bd, l if relief_l is None else relief_l) * deep * r.uniform(.92, 1.06)
    if bd.bat and bd.vmid is not None:
        d += bd.bat * (bd.vmid - cv)          # the batter, block to block
    # THE TILT, and it may only ever take the face BACK. A tilted face is what
    # stops the elevation being perfectly flush; the bias is what makes it safe.
    # The coping nose is 18 mm in front of the proudest block face, and a block
    # that tipped out past it would read as a broken plinth (and would foul the
    # ground family's steps and threshold slabs, which sit on the y = 0 plane).
    t = bd.tilt * r.uniform(.15, 1.0)
    ang = r.uniform(0.0, 2 * pi)
    ca, sa = cos(ang), sin(ang)
    cu0 = sum(q[0] for q in poly) / len(poly)
    cv0 = sum(q[1] for q in poly) / len(poly)
    span = max([abs((q[0] - cu0) * ca + (q[1] - cv0) * sa) for q in poly] + [1e-4])
    gu, gv = t / span * ca, t / span * sa
    d -= t              # ...so the tilt is EXACTLY t deep and takes only one side
    _stone(p, poly, bd.y + r.uniform(-.002, .005), d, m, bd.tint, sd,
           at=at, axis=bd.axis, grad=(gu, gv + bd.bat), pin=pin,
           chamf=clamp(bd.joint * .62, .012, .022),
           rings=2 if (l < .22 or h < .11) else 3)


def _lengths(r, span, bd):
    """The width distribution for one course, normalised to fill `span` exactly.
    Deliberately three-humped -- genuinely big blocks, a plain middle, and real
    packers -- rather than one narrow band around the mean: a course of stones
    all one size is a pattern by construction however irregular their shapes."""
    mid = (lerp(bd.lo, bd.hi, .28), lerp(bd.lo, bd.hi, .62))
    lens, tot = [], 0.0
    while tot < span:
        q = r.random()
        if q < bd.long:
            L = r.uniform(mid[1], bd.hi)
        elif q < bd.long + bd.small:
            L = r.uniform(bd.lo, mid[0])
        else:
            L = r.uniform(*mid)
        lens.append(L)
        tot += L
    if len(lens) > 1 and tot - lens[-1] > span * .72:
        lens.pop()              # drop the overshoot rather than squeeze them all
    k = span / sum(lens)
    return [L * k for L in lens]


def _fill(p, u0, u1, v0, v1, key, bd, at=(0.0, 0.0), floor=None, ceil=None):
    """Lay one course between two fixed edges. JOINT WIDTHS vary per joint as
    well as block widths: all-one-width joints put a regular grid back over
    however irregular the stones are, and the joint is the line the eye follows.
    A wide slot is sometimes filled with one full-height block and a stack of two
    smaller squarish ones beside it -- ref1's "big stones at the bottom, smaller
    ones packed into the gaps", and the one thing that stops a single-course
    footing reading as a row of identical slabs."""
    span = u1 - u0
    if span < .07:
        return
    r = rng(f"fd/fill/{key}/{u0:.3f}")
    lens = _lengths(r, span, bd)
    edges = [u0]
    for L in lens:
        edges.append(edges[-1] + L)
    js = [bd.joint * r.uniform(.72, 1.50) for _ in range(len(lens) + 1)]
    last = len(lens) - 1
    slots = []
    for i in range(len(lens)):
        slots.append((edges[i] + (0.0 if i == 0 else js[i] / 2),
                      edges[i + 1] - (0.0 if i == last else js[i + 1] / 2)))
    # WHICH CELLS SPLIT is decided up front, and a bay with room for one always
    # gets one. Left to an independent die per block it came up empty across three
    # bays running -- four fill blocks a bay, two of them wide enough, .52 each --
    # and with no split cell anywhere a 2 m bay is six squared blocks in a row,
    # which is the "7 flat panels a bay" the critic reported. It is also ref1's
    # detail ("big stones at the bottom, smaller ones packed into the gaps") and
    # the only vertical joint in the family that is not full height.
    wide = [i for i, (a, b) in enumerate(slots)
            if b - a > lerp(bd.lo, bd.hi, .38)]
    hit = set(i for i in wide if r.random() < bd.split) if bd.split > 0 else set()
    if bd.split > 0 and wide and not hit:
        hit.add(max(wide, key=lambda i: slots[i][1] - slots[i][0]))
    for i, L in enumerate(lens):
        a, b = slots[i]
        ln = b - a
        if i in hit:
            f = r.uniform(.34, .45)              # the CLOSER's share
            g = bd.joint * r.uniform(.8, 1.2)
            if r.random() < .5:
                (xa0, xa1), (xb0, xb1) = (a, a + ln * f), (a + ln * f + g, b)
            else:
                (xb0, xb1), (xa0, xa1) = (a, b - ln * f - g), (b - ln * f, b)
            # the CLOSER is a block of its own width, but it is bedded with the
            # cell, not behind it: a narrow closer set back on its own width is
            # the same fault as the packers, one stone further along.
            _one(p, r, xa0, xa1, v0, v1, bd, at, key, floor=floor, ceil=ceil,
                 relief_l=lerp(xa1 - xa0, ln, .70))
            mid = lerp(v0, v1, r.uniform(.42, .58))
            # ONE material for the pair, drawn off the cell rather than off each
            # stone, so the upper packer can never come out dark over a pale lower
            # one -- which is what read as a hole where the upper block should be.
            pm, _ = _tone(rng(f"fd/split/{key}/{a:.3f}"),
                          _blotch(a + at[0], (v0 + v1) / 2 + at[1]),
                          bd.warm, bd.pale, bd.dark, bd.var,
                          bd.damp * .45)
            # ...and the packers are driven in LAST, so they stand a shade proud
            # of the bed rather than sunk into it.
            for w0, w1 in ((v0, mid - bd.joint / 2), (mid + bd.joint / 2, v1)):
                _one(p, r, xb0 + r.uniform(0, .008), xb1 - r.uniform(0, .008),
                     w0, w1, bd, at, key, floor=floor, ceil=ceil,
                     relief_l=ln, deep=1.05, mat_lock=pm)
            continue
        _one(p, r, a, b, v0, v1, bd, at, key, floor=floor, ceil=ceil)


def _seam_stone(p, side, v0, v1, bd, band, max_reach=9.9, at=(0.0, 0.0),
                ceil=None):
    """The block that STRADDLES a bay seam -- and the reason a run of these does
    not show a line every 2 m.

    The notional block spans [seam - a, seam + b] and everything about it --
    width, split point, shape, relief, material, shade -- comes from an rng keyed
    on the BAND ALONE, with tint 0 so _paint's per-primitive jitter (which
    depends on how many primitives the piece happened to emit first) cannot pull
    the two halves apart. The piece on the left keeps [seam - a, seam], the piece
    on the right keeps [seam, seam + b], and together they are ONE stone: same
    width, same relief, same tone, cut on the same plane by _clip so the
    vertices on the cut are bit-identical in both meshes. Returns how far it
    reaches INTO this piece.

    It never crosses the seam, so a corner piece butting this run meets a flat
    cut face, not an overhang buried in its own quoin.

    THE BED COMES FROM THE BAND, NOT FROM THE PIECE, and that is the round-9 fix
    for "a mortar hole every 2 m at the bay seam". Everything above was true of
    the SHAPE and false of the SURFACE: `bd` was whatever Bed the calling piece
    happened to hold, and SM_Found_Plinth_2m_B holds a different one from _A
    (warm .34 / pale .17 / dark .13 against .24 / .05 / .40, and blocks .30-.62
    against .26-.50). So _tone drew a different material on each side of the joint
    and _relief bedded the two halves at different depths: an A|B seam rendered as
    one stone with a hard vertical tone break and a depth step straight down its
    middle, every 2 m, exactly where the piece promised there would be none. A
    band is a property of the RUN, so the bed a seam stone is cut from has to be
    too."""
    bd = BAND_BED.get(band, bd)
    r = rng(f"fd/seam/{band}/{v0:.4f}/{v1:.4f}")
    w = r.uniform(.42, .66)
    u = r.uniform(.40, .60)
    a, b = w * u, w * (1.0 - u)
    reach = min(a if side > 0 else b, max_reach)
    m, sd = _tone(r, 0.0, bd.warm, bd.pale, bd.dark, .04, bd.damp * .5)
    d = _relief(bd, w)
    if bd.bat and bd.vmid is not None:
        d += bd.bat * (bd.vmid - (v0 + v1) / 2)
    # no mid-point and no roll on this one: _clip wants a convex outline, and a
    # dished edge is not worth a special case on the one block per course that
    # has to come out identical on two different meshes. Knocked corners are.
    poly = _outline(r, -a - OV[0] / 2, b + OV[0] / 2, v0 - OV[1] / 2,
                    v1 + OV[1] / 2, clips=(.34, .46, .20, .0), mid=0.0,
                    taper=r.uniform(0.0, .12), flip=r.random() < .5,
                    lean=r.uniform(-1, 1) * .005, roll=0.0)
    ext = ((max(q[0] for q in poly) - min(q[0] for q in poly)) / 2,
           (max(q[1] for q in poly) - min(q[1] for q in poly)) / 2)
    poly = _clip(poly, 0.0, side > 0)
    poly = _clip(poly, -reach if side > 0 else reach, side < 0)
    poly = _clip(poly, max(v0 - OV[1] / 2, 0.0), False, i=1)
    if ceil is not None:
        poly = _clip(poly, ceil, True, i=1)
    _stone(p, poly, bd.y + .002, d, m, 0.0, sd, at=(at[0] + side * HX, at[1]),
           axis=bd.axis, grad=(0.0, bd.bat), pin=0.0, extent=ext,
           chamf=clamp(bd.joint * .58, .010, .020),
           rings=2 if v1 - v0 < .11 else 3)
    return reach + OV[0] / 2


def course(p, u0, u1, v0, v1, key, bd, band=None, seam_lo=False, seam_hi=False,
           at=(0.0, 0.0), floor=None, ceil=None, mort_hi=LAP):
    """One coursed run: the mortar behind it, a seam block at each bay edge that
    asks for one, and the field between them.

    The MORTAR is keyed on the band, not on the piece key -- which is what the
    _mortar docstring always claimed and what this call never did. Keyed on "a"
    and "b" the two plinth variants laid a different batch of lime behind the same
    joint, so a run of A B A showed the joint tone change at every bay edge."""
    _nz.seed_set(NOISE_SEED)
    _mortar(p, u0, u1, max(v0 + .004, .004), v1 + mort_hi, band or key, bd, at)
    a0, a1 = u0, u1
    sbd = BAND_BED.get(band, bd)
    if seam_lo:
        a0 = u0 + sbd.joint + _seam_stone(p, -1, v0, v1, bd, band, u1 - u0 - .12,
                                          at, ceil)
    if seam_hi:
        a1 = u1 - sbd.joint - _seam_stone(p, +1, v0, v1, bd, band, u1 - u0 - .12,
                                          at, ceil)
    _fill(p, a0, a1, v0, v1, key, bd, at, floor=floor, ceil=ceil)


# ------------------------------------------------------------------ mortar ----
def _mortar(p, u0, u1, v0, v1, key, bd, at=(0.0, 0.0), n=None):
    """THE JOINT PLANE, laid as patches 30 mm behind the block faces.

    Not a black slot: a surface of its own, at a tone that CATCHES LIGHT out of
    the recess, and patched -- each patch takes its own value off its own rng and
    some of them sit on `stone_warm` rather than stone_dark, so the joints in one
    run are a different batch of lime from the joints in the next. Keyed on the
    band and the span, never on the piece, so two variants meeting at a bay seam
    show the same mortar behind the same joint.

    Adjacent patches sit at different depths so the LAP where they overlap has an
    unambiguous front face -- the whole module's rule, applied to itself. The
    patches at the two ENDS of a run are always at the base depth, though, and the
    run is cut into an odd number of them: with two patches per bay the parity
    landed a -.078 patch against a -.072 one across every seam, so the joint plane
    stepped 6 mm at exactly the place a joint plane must not do anything at all."""
    w = u1 - u0
    if w < .05:
        return
    n = n or max(1, 2 * int(round(w / 1.40)) + 1)
    for i in range(n):
        a = max(lerp(u0, u1, i / n) - (LAP if i else 0.0), u0)
        b = min(lerp(u0, u1, (i + 1) / n) + (LAP if i < n - 1 else 0.0), u1)
        r = rng(f"fd/mortar/{key}/{a:.3f}")
        yy = bd.mort + (MORT_STEP if (0 < i < n - 1 and i % 2) else 0.0)
        warm = r.random() < .18
        m = "stone_warm" if warm else "stone_dark"
        sd = (.66 if warm else MORT_SHADE) * (1.0 + r.uniform(-.22, .22))
        c = ((a + b) / 2 + at[0], yy + bd.mort_t / 2, (v0 + v1) / 2 + at[1])
        sz = (b - a, bd.mort_t, v1 - v0)
        if bd.axis == 'X':
            c = (c[1], c[0], c[2])
            sz = (sz[1], sz[0], sz[2])
        p.plate(c, sz, m, tint=.06, shade=sd)


# -------------------------------------------------------------------- core ----
def _core(p, u0, u1, z0, z1, y0=BED, y1=T, shade=.30):
    """The solid mass behind the facing. Nothing ever sees its front face -- the
    mortar layer owns the surface the joints show -- so it stays the dark bulk it
    is, and its back owns the y = T inner plane on its own."""
    p.plate(((u0 + u1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
            (u1 - u0, y1 - y0, z1 - z0), "stone_dark", tint=.03, shade=shade)


# ------------------------------------------------------------------ coping ----
# The one horizontal in the family, and the thing that makes a foundation read as
# a foundation rather than as a short wall: a band of dressed stone whose nose
# oversails the block faces by 37 mm and whose top-OUTER edge is a SQUARE ARRIS --
# a 75-degree dihedral between a 15-degree weathered ledge and a 67 mm vertical
# fascia. ref3:stone_arch draws exactly this band under its stone storey, and
# ref1's yard terrace is capped with the same thing.
#
# ROUND 9, and this is the fault that survived every previous fix. The band has
# been through a 30-degree wash (under spec.SMOOTH_ANG: it shaded as one
# continuous bullnose) and then a 49.6-degree chamfer (over the smooth angle, so
# genuinely three hard-edged facets) -- and BOTH read as nothing, because a
# raked-sun elevation measured the three facets at L=168 / 157 / 147. Hard edges
# are necessary and not sufficient: what makes a line is CONTRAST, and there are
# only two sources of it on a 105 mm band.
#   1. the biggest normal break available. A 90-degree turn between the ledge and
#      the fascia is worth the full 21 L, where the 49.6-degree chamfer split the
#      same turn into two steps of 11 and 10.
#   2. surfaces that face DOWN, which take no light from anything above them: the
#      26 mm drip chamfer under the nose, plus the ~25 mm of block face the nose
#      keeps the sun off. That is 50 mm of near-black, continuous, the whole way
#      along -- and unlike the chamfer it survives being looked at from above,
#      which is how a 450 mm base is always seen from a street.
#
# It is built as TWO kinds of solid, and both faults the critic found in the old
# single-prism slab are fixed by that split rather than by tuning a number:
#   _cap_bear   ONE continuous bearing slab per run. Flat top at z1, front face on
#               WASH_Y. Walls sit on this; no joint crosses it.
#   _cap_slab   the NOSE BLOCKS in front of it, cut into slabs with real joints.
#               Their ledges meet the bearing slab's flat top along one line --
#               two separate surfaces, so no smoothing can cross it -- and their
#               joints are 42 mm notches, not holes through the base.
def _cap_nose_sec(z0, z1, nose=NOSE, wash_y=WASH_Y, cd=CAP_CD, drip=DRIP,
                  tail=BITE):
    """Section, in (y, z), of ONE coping NOSE BLOCK -- not of the whole coping.

    Five points, and from the bottom out they are: the 45-degree DRIP chamfer, the
    vertical FASCIA, the square ARRIS, the weathered LEDGE, and a short tail that
    dies BITE deep into the continuous bearing slab behind it. The tail's top is
    the last of the ledge, so the block reaches z1 along one line only and shares
    no plane with the slab's flat top.

    Every edge in it is over spec.SMOOTH_ANG by a margin no jitter can close:
    ledge/fascia 75 deg, fascia/drip 45 deg, drip/underside 45 deg.

    Why the coping is two solids (this, and _cap_bear) rather than one prism:
      * the ledge/top edge is an edge between two SEPARATE surfaces, which cannot
        be smoothed across whatever spec.SMOOTH_ANG says. Under the original
        one-prism section that edge was a 30-degree wash under a 34-degree smooth
        angle, and the whole coping shaded as one bullnose;
      * the joints between nose blocks are 42 mm deep notches with dressed stone
        at the back of them. Under that section every joint ran the full 500 mm
        depth of the piece: backlit, a 6 m run showed nine slots clean through the
        base, one of them beside every bay seam."""
    d = min(drip, (z1 - z0) * .30)
    return [(nose + d, z0), (nose, z0 + d), (nose, z1 - cd),
            (wash_y + tail, z1), (wash_y + tail, z0)]


def _cap_split():
    """How a coping slab straddling a bay seam divides between the two pieces.
    Keyed on nothing but this function, so it is a CONSTANT of the family: every
    piece knows exactly how far its neighbour's half reaches, and a corner can
    stop its own coping on the butt plane knowing nothing will overlap it."""
    r = rng("fd/cap/seam")
    w = r.uniform(.52, .68)
    u = r.uniform(.42, .58)
    return w * u, w * (1.0 - u)


CAP_A, CAP_B = _cap_split()      # the -x half and the +x half of a seam slab


def _cap_bear(p, x0, x1, z0, z1, key, front=WASH_Y, back=T):
    """THE BEARING SLAB: one continuous solid per run, from the arris line back to
    the inner face, whose top face IS the flat bearing plane at z1. A wall sits on
    it, so nothing here is ever jittered in z and the run carries no joint through
    it -- that is what stopped the nose joints being holes through the base, and
    it is also simply what a wall wants to be bedded on.

    Its front face (the plane at `front`) is what shows at the back of every nose
    joint: dressed stone in shadow, 34 mm in, instead of daylight."""
    r = rng(f"fd/cap/bear/{key}")
    p.box(((x0 + x1) / 2, (front + back) / 2, (z0 + z1) / 2),
          (x1 - x0, back - front, z1 - z0), "stone_pale", bevel=0,
          tint=.045, shade=.94 + r.uniform(-.03, .03))


def _cap_slab(p, x0, x1, z0, z1, key, back=T, drip=DRIP):
    """One coping NOSE BLOCK. Its nose line, the fall of its ledge and how far the
    arris has weathered back are all jittered -- weathering is the only variation a
    dressed slab gets -- but the ledge never falls more than CAP_CD * 1.4 over its
    42 mm run, i.e. the arris is never shallower than 68 degrees, so no slab in any
    run can slip back under spec.SMOOTH_ANG and go bullnose again. bevel=0 on
    purpose: a 1-segment bevel halves every dihedral in the section.

    The two jitters are one-sided ON PURPOSE:
      * `nose` may only come BACK from NOSE, which is set at the family's declared
        proud allowance less the wobble amplitude. Jittering it outward would put
        vertices past that allowance and get them clamped flat by finish().
      * `wy` may only go BACK from WASH_Y, so the tail always ends behind the
        bearing slab's front plane and laps into it. Jittering it forward opens a
        3 mm gap between the nose block and the slab, straight through the band."""
    r = rng(f"fd/cap/{key}")
    nose = NOSE + r.uniform(0.0, .006)
    wy = WASH_Y + r.uniform(0.0, .008)
    cd = CAP_CD * r.uniform(.85, 1.25)
    if r.random() < .26:                      # a worn one: the arris eaten back
        cd *= 1.15
        nose += .007
    q = r.random()
    m = "stone_pale" if q < .54 else ("stone_warm" if q < .86 else "stone")
    # the nose block starts BITE below the bearing slab, never level with it. Both
    # are bedded on z0, and the tail laps BITE of the slab's y range, so level
    # bottoms put 4 mm x the slab's length of coincident surface under every run --
    # measured at 76 cm2 on SM_Found_Step_2m before this line existed.
    p.prism(_cap_nose_sec(z0 - BITE, z1, nose, wy, min(cd, (z1 - z0) * .55), drip),
            x1 - x0, m, axis='X', at=((x0 + x1) / 2, 0, 0), bevel=0,
            tint=.05, shade=.92 + r.uniform(-.07, .07))


def coping(p, x0, x1, z0, z1, band, seam_lo=True, seam_hi=True, per_m=1.45,
           joint=.026, back=T, front=None, drip=DRIP):
    """A run of coping: ONE bearing slab, and a row of nose blocks in front of it.

    The nose block at each bay seam is the SAME block on both sides of it -- same
    length, same nose, same chamfer, same tone, keyed on the band -- with each
    piece building only its own half up to the seam plane. So a run reads as one
    continuous band of dressed stone with a hairline joint every 2 m rather than
    the 16 mm dark nick stone_walls' round 7 had to go back and kill on the three
    strongest horizontals of its elevation.

    `drip` is a knob because the drip chamfer is only safe over a course that is
    bedded BEDJ below the coping: it brings the soffit's inner foot 26 mm back
    from the nose, and any block face prouder than that saws a serrated line
    through it. SM_Found_Step_2m's low level has only 45 mm of masonry under its
    coping and no room for a bed joint, so it caps with drip near zero instead."""
    _cap_bear(p, x0, x1, z0, z1, band,
              front=WASH_Y if front is None else front, back=back)
    a0, a1 = x0, x1
    if seam_lo:
        _cap_slab(p, x0, x0 + CAP_B, z0, z1, "seam", back, drip)
        a0 = x0 + CAP_B + joint / 2
    if seam_hi:
        _cap_slab(p, x1 - CAP_A, x1, z0, z1, "seam", back, drip)
        a1 = x1 - CAP_A - joint / 2
    w = a1 - a0
    if w < .05:
        return
    n = max(1, int(round(w * per_m)))
    r = rng(f"fd/cap/run/{band}")
    # jittered, never sorted-random: two random cuts land 20 mm apart often
    # enough that a run grows a sliver slab, and a sliver in a dressed band is
    # the one thing that reads as a mistake rather than as masonry
    cuts = ([0.0] + [i / n + r.uniform(-.34, .34) / n for i in range(1, n)]
            + [1.0])
    for i in range(n):
        a = lerp(a0, a1, cuts[i]) + (joint / 2 if i else 0.0)
        b = lerp(a0, a1, cuts[i + 1]) - (joint / 2 if i < n - 1 else 0.0)
        if b - a > .06:
            _cap_slab(p, a, b, z0, z1, f"{band}/{i}", back, drip)


# ==================================================================== pieces ==
def _plinth(name, key, bd=PLINTH, core_y=BED, seed=0):
    """The standard course: heavy squared footing blocks on a tight joint,
    standing FOUND_OUT proud of the wall above, closed by the washed coping.
    Two variants so a long run does not repeat -- same course, same bed line,
    same coping band, same seam blocks, DIFFERENT stones."""
    p = Part(name, budget="found", seams=SEAMS, proud=PROUD)
    _core(p, -HX, HX, .006, CAP_Z0 + BITE, core_y)
    # ceil=BLK_TOP: the coping's bed is a LEVEL plane, cut at build time rather
    # than clamped, and the 30 mm between it and CAP_Z0 is the open bed joint the
    # coping's shadow line lives in.
    course(p, -HX, HX, 0.0, BLK_TOP + LAP, key, bd, band="plinth",
           seam_lo=True, seam_hi=True, floor=0.0, ceil=BLK_TOP,
           mort_hi=CAP_Z0 + BITE - (BLK_TOP + LAP))
    coping(p, -HX, HX, CAP_Z0, H, "plinth")
    _wob(p)
    return p.finish()


def plinth_a():
    return _plinth("SM_Found_Plinth_2m_A", "a", PLINTH)


def plinth_b():
    """The same course laid by a mason with a bigger cart: a quarter of the
    blocks are boulders, fewer of them are split, and the mix runs warmer."""
    return _plinth("SM_Found_Plinth_2m_B", "b",
                   Bed(long=.34, small=.09, split=.34, warm=.34, pale=.17,
                       dark=.13, lo=.30, hi=.62))


def riser():
    """The extra half-height course, for where the ground falls away and the
    coping has to stay level. It has no coping of its own -- it goes UNDER a
    plinth, so its top is a flat bearing bed -- and its blocks stand 8 mm
    prouder than the course above, because a footing course that stood BACK from
    the one it carries would read as an overhang."""
    p = Part("SM_Found_Riser_2m", budget="found",
             seams=dict(x=(-HX, HX), y=(0, T), z=(0, RH)), proud=PROUD)
    # THE CORE REACHES RH, and that is a fix, not a copy of the plinth. Every
    # other piece in the family tops its core at CAP_Z0 + BITE because the coping
    # buries it; the riser has NO coping, so z = RH is its bearing plane -- the
    # plinth above lands its whole body depth on it -- and a core stopped BITE
    # short of it left 220 mm of that bearing surface, everything behind the
    # joint plane, 4 mm hollow. The blocks are cut on RH and the core now ends on
    # it, and the two cannot z-fight because they share no depth: the core's
    # front is at -.036 and the blocks' backs are at RISERB.y = -.068.
    _core(p, -HX, HX, .006, RH, -.036)
    # ceil: the riser's top is a BEARING plane -- a plinth sits on it -- so the
    # blocks are cut on it by construction rather than clamped there by util.
    # The MORTAR still stops BITE short, and must: it is the one layer the blocks
    # are bedded INTO (backs -.068 inside a plate spanning -.086 to -.050), so a
    # mortar top on RH would be coincident with the cut block tops over 18 mm of
    # depth. It is 30 mm behind the faces and under the plinth, where nothing
    # sees it; the core is not.
    course(p, -HX, HX, 0.0, RH, "r", RISERB, band="riser", seam_lo=True,
           seam_hi=True, floor=0.0, ceil=RH, mort_hi=-BITE)
    _wob(p)
    return p.finish()


def batter():
    """A battered base course for the tallest exposed side: the faces lean out
    44 mm from the coping down to grade, so the base is frankly heavier at the
    bottom. The bed plane stays flat, so every block is a wedge -- which is what
    a battered footing block is -- and the coping's nose stops oversailing it by
    the bottom of the course, exactly as it should on a batter.

    It runs with itself. Where a battered bay meets a vertical one the joint
    shows the batter's step, because that is what a batter is; a corner or a
    riser is the place to change from one to the other."""
    p = Part("SM_Found_Batter_2m", budget="found", seams=SEAMS, proud=PROUD)
    _core(p, -HX, HX, .006, CAP_Z0 + BITE, BAT_BUILD)
    course(p, -HX, HX, 0.0, BLK_TOP + LAP, "bt", BATTER, band="batter",
           seam_lo=True, seam_hi=True, floor=0.0, ceil=BLK_TOP,
           mort_hi=CAP_Z0 + BITE - (BLK_TOP + LAP))
    coping(p, -HX, HX, CAP_Z0, H, "batter")
    _wob(p)
    return p.finish()


# =============================================================== the corner ==
CORNER_SEAMS = dict(x=(-T, 0.0), y=(0.0, T), z=(0.0, H))
CBED_X = Bed(y=-T + BLK_Y, mort=-T + MORT_Y, joint=.020, tilt=.007, pale=.24,
             warm=.32, dark=.06, damp=.30, axis='X')


def _wob_corner(p, amount=WOB, freq=1.7):
    """Hand-hewn wobble on a corner, fading ONLY at the planes that have to stay
    flat: the two BUTT planes where the wall runs land (x = 0, y = T) and the two
    z planes. Part.wobble's own fade is two-sided per axis, so asking it to keep
    x flat would also flatten x = -T -- one of the two elevations anybody ever
    looks at. corners.py had to write this for the same reason."""
    _nz.seed_set(NOISE_SEED)
    for v in p.bm.verts:
        f = min(smoothstep(0, .11, -v.co.x), smoothstep(0, .11, T - v.co.y),
                smoothstep(0, .10, v.co.z), smoothstep(0, .10, H - v.co.z))
        if f <= 0.0:
            continue
        v.co += Vector(_nz.noise_vector(v.co * freq)) * amount * f


def corner():
    """The T x T outside corner, on the corners family's convention: the cell
    that sits in the void where two perpendicular runs meet, faces out on TWO
    sides (outward="xy"), so an outer rectangle of n x m bays measures
    (n*GRID + 2T) x (m*GRID + 2T) with zero gap by construction.

    ONE massive block per elevation, long-and-short round the arris: the long one
    wraps out to the return face and shows its end there, the short one closes
    the return behind it. That is what a footing corner is -- the heaviest stone
    in the building goes where the two walls have to hold each other up -- and
    with a 345 mm course there is no room for it to be anything else.

    Both blocks are CUT on their butt planes rather than clamped, so the seam
    block the adjacent run lays against the same plane meets them face to face,
    and the coping stops dead on the butt plane so the run's own coping half
    (a known constant, CAP_A/CAP_B) lands beside it with nothing overlapping."""
    p = Part("SM_Found_Corner", budget="found", seams=CORNER_SEAMS,
             proud=PROUD, outward="xy")
    _core(p, -T + BED, 0.0, .006, CAP_Z0 + BITE, BED)
    _mortar(p, -T - .02, 0.0, .004, CAP_Z0 + BITE, "cy", CORNERB)
    _mortar(p, -.02, T, .004, CAP_Z0 + BITE, "cx", CBED_X)
    r = rng("fd/corner/blocks")
    CL = (.46, .40, .14, .0)
    zt = BLK_TOP + LAP            # ...cut back to BLK_TOP: the corner is bedded
    j = CORNERB.joint             #    on the same open joint as every run
    # ---- the y = 0 elevation: the LONG block, wrapping past the arris until its
    # end IS the return elevation's face, then a narrow CLOSER up to the butt
    # plane. One stone per elevation was true to a footing and read as a blank
    # panel: 360 mm of dressed masonry with not one joint in it.
    _one(p, r, -T - .118, -.155, 0.0, zt, CORNERB, key="cq0", clips=CL,
         floor=0.0, ceil=BLK_TOP)
    _one(p, r, -.155 + j, 0.0, 0.0, zt, CORNERB, key="cq1", pin=0.0, clips=CL,
         floor=0.0, ceil=BLK_TOP, cut=((0.0, True, 0),))
    # ---- the x = -T elevation: two blocks, the first butting the long one's bed
    # so the joint between them lands on the arris
    _one(p, r, BLK_Y + j, .175, 0.0, zt, CBED_X, key="cq2", clips=CL,
         floor=0.0, ceil=BLK_TOP)
    _one(p, r, .175 + j, T, 0.0, zt, CBED_X, key="cq3", pin=T, clips=CL,
         floor=0.0, ceil=BLK_TOP, cut=((T, True, 0),))
    # ---- the coping, mitred: the flat bearing body, and a NOSE WEDGE on each
    # elevation carrying the same drip / fascia / square arris as a run's nose
    # block. The two wedges overlap in the nose square and each slopes its own
    # way, so their union is a hip along the diagonal -- a mitred ledge, for
    # nothing, and with no two faces sharing a plane. Each wedge's ledge reaches
    # z=H along ONE LINE (y = WASH_Y + BITE), which is where the arris is: the
    # bearing body's flat top and the wedge's ledge are separate surfaces, so the
    # corner's arris cannot smooth away either.
    r2 = rng("fd/corner/cap")
    m = "stone_pale" if r2.random() < .60 else "stone_warm"
    sh = .95 + r2.uniform(-.04, .04)
    # the flat bearing top: x from -T+WASH_Y to 0, y from WASH_Y to T -- i.e. the
    # rectangle the wall corner above lands on, and not one millimetre of chamfer
    # inside it
    p.box(((-T + WASH_Y) / 2, (WASH_Y + T) / 2, (CAP_Z0 + H) / 2),
          (T - WASH_Y, T - WASH_Y, CAP_H),
          m, bevel=0, tint=.05, shade=sh)
    wedge = [(NOSE + DRIP, CAP_Z0 - BITE), (NOSE, CAP_Z0 - BITE + DRIP),
             (NOSE, H - CAP_CD), (WASH_Y + BITE, H), (WASH_Y + BITE, CAP_Z0 - BITE)]
    p.prism(wedge, T - NOSE, m, axis='X', at=((-T + NOSE) / 2, 0, 0),
            bevel=0, tint=.05, shade=sh)
    p.prism([(-T + a, b) for (a, b) in wedge], T - NOSE, m, axis='Y',
            at=(0, (NOSE + T) / 2, 0), bevel=0, tint=.05, shade=sh)
    _wob_corner(p)
    return p.finish()


# =========================================================== the inner corner ==
# A base that PROJECTS -- and Shanee's entrance does -- turns four corners, not
# two: two outside ones at the front angles of the projection, and two RE-ENTRANT
# ones where it returns into the main elevation. Without a piece for the
# re-entrant pair those two joints are the raw cut ends of two bays butting at 90
# degrees, which is the one place on a coursed base where a mistake has nowhere to
# hide -- and it is the piece this family's own author flagged as missing.
#
# THE CELL is the corners family's cell, unrotated: x in [-T, 0], y in [0, T].
# What differs from SM_Found_Corner is which planes are AIR:
#     y = 0     EXPOSED, and the ONLY exposed plane. It carries the main run's
#               elevation the last T to the crease.
#     x = -T    the CREASE. Beyond it the returning run's body carries straight
#               on -- solid on both sides -- so nothing crosses it and the blocks
#               are cut on it, exactly as they are cut on x = 0.
#     x = 0     BUTT, where the main run's next bay lands.
#     y = T     the inner face.
# That is SM_Found_Corner with wrap=False: no block turns the arris, because at a
# re-entrant corner there is no arris to turn. outward="y" -- one exposed face is
# one direction relief may stand proud in, and the crease plane has to stay dead
# flat or the returning run's own quoin fouls it.
#
# IT IS HANDED, like every re-entrant corner in every modular kit: the crease is
# at the -x end of its elevation. The four rotations give a piece whose face looks
# -Y with the crease to its west, +X with the crease to its south, and so on -- so
# a projecting bay is dressed with this piece at BOTH its returns, once on the
# main elevation and once mirrored (scale x = -1). demo() does exactly that, and
# the plan closes on the grid with no gap and no overlap.
#
# THE COPING IS NOTCHED, and that is the whole reason this is not just a short
# plinth. Two coping bands meeting at a re-entrant corner mitre, and the mitre
# square -- |NOSE| x |NOSE| at the crease -- can belong to only ONE of them. The
# returning run's bays carry their coping right up to their bay seam on y = 0, so
# the square is already theirs; this piece keeps its front edge on y = 0 across
# that strip and lets it through. Anything else is either a 148 mm hole in the
# band or two slabs fighting over the same 148 mm of bearing surface at exactly
# z = H_FOUND, on the one horizontal plane in the kit that has to be clean.
CIN_SEAMS = dict(x=(-T, 0.0), y=(0.0, T), z=(0.0, H))
CIN_NOTCH = -NOSE                 # .148  the coping's mitre square
CIN_STONE = -FACE                 # .126  the COURSE mitres closer than the coping
                                  # does, because a block face only reaches FACE
                                  # where the coping's nose reaches NOSE. Cut the
                                  # course back on the coping's line instead and
                                  # the two courses stop 22 mm apart, which at a
                                  # re-entrant angle reads as a slot, not a joint.
CINB = Bed(joint=.022, tilt=.008, long=0.0, small=0.0, split=0.0, lo=.16, hi=.34,
           pale=.22, warm=.30, dark=.10, damp=.30)


def _wob_inner(p, amount=WOB, freq=1.7):
    """Hand-hewn wobble fading at the FOUR planes that must stay flat -- the
    crease x=-T, the butt x=0, the inner face y=T and the two z planes -- and
    nowhere else, so the y=0 elevation, which is the only thing anybody looks at,
    keeps its irregularity. Part.wobble fades two-sided per axis and cannot
    express "flat on y=T, free on y=0"."""
    _nz.seed_set(NOISE_SEED)
    for v in p.bm.verts:
        f = min(smoothstep(0, .11, v.co.x + T), smoothstep(0, .11, -v.co.x),
                smoothstep(0, .11, T - v.co.y),
                smoothstep(0, .10, v.co.z), smoothstep(0, .10, H - v.co.z))
        if f <= 0.0:
            continue
        v.co += Vector(_nz.noise_vector(v.co * freq)) * amount * f


def corner_inner():
    """The re-entrant (270 degree) corner: the armpit where a projecting porch
    bay returns into the main base. See the block comment above for the cell, the
    handedness and why the coping is notched.

    The elevation it owns is CIN_STONE short of the full cell -- 226 mm of dressed
    face, laid as a TOOTHED JAMB of two stones one above the other rather than one
    blank panel, which is the traditional way a corner is closed and the only way
    to get a joint into 226 mm of a single-course footing. Both stones are cut on
    the mitre plane and on the butt plane rather than clamped there, so the
    returning run's quoin and the main run's seam block meet them face to face."""
    p = Part("SM_Found_CornerInner", budget="found", seams=CIN_SEAMS,
             proud=PROUD, outward="y")
    xj = -T + CIN_NOTCH                                   # -.212, the coping line
    xs = -T + CIN_STONE                                   # -.234, the course line
    # THE CORE, in two plates. The one under the notch keeps its face on y = 0 so
    # nothing of this piece enters the mitre square; the one under the elevation
    # sits at the family's BED. They lap LAP in x and differ on every plane they
    # could otherwise have shared -- front (0 vs BED), top (+.006) and bottom
    # (+.004) -- which is the vent's lesson applied to a second piece.
    # ...and it is toned as STONE IN SHADOW, not as buried core. In use nothing
    # sees it -- the returning run's body stands in front of it -- but in a lineup
    # it is a third of the piece's face, and at the core's .30 it read as a hole.
    _core(p, -T, xs + LAP, .006, CAP_Z0 + BITE, 0.0, T, .74)
    _core(p, xs, 0.0, .010, CAP_Z0 + BITE + .006, BED)
    _mortar(p, xs - .02, 0.0, .004, CAP_Z0 + BITE, "in", CINB)
    r = rng("fd/inner/blocks")
    CL = (.44, .42, .14, .0)
    j = CINB.joint
    zm = lerp(0.0, BLK_TOP, r.uniform(.46, .56))
    for (w0, w1, k) in ((0.0, zm - j / 2, "in0"), (zm + j / 2, BLK_TOP + LAP, "in1")):
        _one(p, r, xs, 0.0, w0, w1, CINB, key=k, pin=0.0, clips=CL,
             floor=0.0 if w0 <= 0.0 else None, ceil=BLK_TOP,
             cut=((xs, False, 0), (0.0, True, 0)))
    # THE COPING. The bearing body is ONE L-shaped prism in plan rather than two
    # boxes: two boxes lapping anywhere inside the cell would put their flat tops
    # on the same z = H plane over the lap, and that plane is the bearing surface.
    r2 = rng("fd/inner/cap")
    m = "stone_pale" if r2.random() < .58 else "stone_warm"
    plan = [(-T, T), (-T, 0.0), (xj, 0.0), (xj, WASH_Y), (0.0, WASH_Y), (0.0, T)]
    p.prism(plan, CAP_H, m, axis='Z', at=(0, 0, (CAP_Z0 + H) / 2), bevel=0,
            tint=.045, shade=.94 + r2.uniform(-.03, .03))
    # ...and the nose blocks in front of it, over the elevation only. Two of them,
    # so the 212 mm of band carries the same joint rhythm as a run's 1.45/m.
    xm = lerp(xj, 0.0, r2.uniform(.44, .56))
    _cap_slab(p, xj, xm - .013, CAP_Z0, H, "inner/0")
    _cap_slab(p, xm + .013, 0.0, CAP_Z0, H, "inner/1")
    _wob_inner(p)
    return p.finish()


# ================================================================= the step ==
XS = .10                 # where the top steps down
LOWB = Bed(mort=MORT_Y + .009, lo=.22, hi=.46, long=.14, small=.18, split=0.0,
           damp=1.0)
BAND_BED["steplow"] = LOWB


def step():
    """The terrace piece, and the answer to "terraced/layered levels": the top
    steps DOWN by FOUND_STEP across the bay, so a run can follow the ground
    instead of pretending the site is flat.

    The high end's coping is at H_FOUND and the low end's at H_FOUND - FOUND_STEP,
    with 195 mm of masonry showing in the riser between the two bands -- which is
    what a stepped coping looks like, and it is why the step is not just a
    chamfer. Place the next bay at z = -FOUND_STEP and its coping seam half lands
    exactly on this one's (same "seam" key, so it is literally the same slab)."""
    p = Part("SM_Found_Step_2m", budget="found", seams=SEAMS, proud=PROUD)
    _core(p, -HX, XS + LAP, .006, CAP_Z0 + BITE, BED)
    _core(p, XS, HX, .011, LOW_Z0 + BITE, BED + .008)   # see the vent: not .006
    course(p, -HX, XS, 0.0, BLK_TOP + LAP, "sh", PLINTH, band="plinth",
           seam_lo=True, floor=0.0, ceil=BLK_TOP,
           mort_hi=CAP_Z0 + BITE - (BLK_TOP + LAP))
    coping(p, -HX, XS, CAP_Z0, H, "steph", seam_hi=False)
    # the dressed stone that closes the riser, and covers the cut ends of the
    # high course's blocks
    r = rng("fd/step")
    # ...and it reaches all the way back to the inner face, because the riser is
    # a FACE: stopped at y = .10 it left the core's dark end showing over half the
    # step, which is the one thing a stepped coping must not do. It stops at the
    # high course's own bed line, so it dies into the bed joint instead of sawing
    # through the coping's soffit 18 mm in front of it.
    p.box((XS + .007, (-.132 + T) / 2, (LOW_TOP - .004 + BLK_TOP + LAP) / 2),
          (.026, T + .132, BLK_TOP + LAP - LOW_TOP + .004), "stone_pale",
          bevel=.012, seg=1, tint=.05, skew=(.004, 0),
          shade=.97 + r.uniform(-.04, .04))
    # THE LOW LEVEL has 45 mm of masonry under its coping and no room for a bed
    # joint, so it caps with a 6 mm drip instead of 26: at 26 the soffit's inner
    # foot lands 24 mm behind the nose, in front of the low course's own faces.
    course(p, XS + .020, HX, 0.0, LOW_Z0 + LAP, "sl", LOWB, band="steplow",
           seam_hi=True, floor=0.0)
    coping(p, XS + .020, HX, LOW_Z0, LOW_TOP, "stepl", seam_lo=False, drip=.006)
    _wob(p)
    return p.finish()


# ================================================================= the vent ==
V_W2 = .22               # half the void
V_JAMB = .09
V_Z0, V_Z1 = .105, .275


def vent():
    """A cellar vent set into a plinth course, so 2 m of base is not blank.

    ref1 has a grille and a hatch at grade under the barrels; a base course with
    nothing in it reads as a kerb rather than as a building. The masonry owns the
    opening: a heavy squared sill block, dressed jambs, a lintel bedded up into
    the coping, and a wrought grille set 55 mm back in the reveal so the whole
    thing is a hole with shadow in it -- FORM, which is what survives the Solid
    shading the .blend is judged in."""
    p = Part("SM_Found_Vent", budget="found", seams=SEAMS, proud=PROUD)
    e = V_W2 + V_JAMB                                     # .31
    _core(p, -HX, -e + .01, .006, CAP_Z0 + BITE, BED)
    _core(p, e - .01, HX, .006, CAP_Z0 + BITE, BED)
    # THE FOUR BOXES OVERLAP EACH OTHER BY 10 mm OF x, so every plane they could
    # share is a coincident pair over that strip: not the bottom (.011 vs .006),
    # not the front (BED+.006 vs BED), not the top (.365 vs .359, both buried in
    # the coping). Measured, not guessed -- check_zfight found all three.
    _core(p, -e - .01, e + .01, .011, V_Z0 + .004, BED + .006)
    _core(p, -e - .01, e + .01, V_Z1 - .004, CAP_Z0 + BITE + .006, BED + .006)
    course(p, -HX, -e - .012, 0.0, BLK_TOP + LAP, "vl", PLINTH, band="plinth",
           seam_lo=True, floor=0.0, ceil=BLK_TOP,
           mort_hi=CAP_Z0 + BITE - (BLK_TOP + LAP))
    course(p, e + .012, HX, 0.0, BLK_TOP + LAP, "vr", PLINTH, band="plinth",
           seam_hi=True, floor=0.0, ceil=BLK_TOP,
           mort_hi=CAP_Z0 + BITE - (BLK_TOP + LAP))
    r = rng("fd/vent")
    # the void: a dark blank, bitten 5 mm into the reveal so it shares no plane
    p.plate((0, .075, (V_Z0 + V_Z1) / 2), (2 * V_W2 + .02, .040,
            V_Z1 - V_Z0 + .02), "stone_dark", tint=.02, shade=.12)
    # sill block: one squared stone, its top washed forward to throw the water
    p.box((0, (-.134 + .06) / 2, (.004 + V_Z0) / 2), (2 * (V_W2 + .06), .194,
          V_Z0 - .004), "stone_warm", bevel=.013, seg=1, tint=.05, taper=.97,
          taper_axis='Y', skew=(0, .008), shade=.94 + r.uniform(-.04, .04))
    for sx in (-1, 1):                                    # jambs
        p.box((sx * (V_W2 + V_JAMB / 2), (-.128 + .06) / 2, (V_Z0 + V_Z1) / 2),
              (V_JAMB, .188, V_Z1 - V_Z0 + .008),
              "stone_pale" if sx > 0 else "stone_warm", bevel=.010,
              seg=1, tint=.05, shade=.92 + r.uniform(-.05, .05))
    # the lintel stops on the course's own bed line, like every block beside it:
    # carried LAP into the coping its front face at -.132 stood 18 mm proud of the
    # coping's soffit and cut a line through it, and stopped at CAP_Z0 its top
    # would have been coplanar with that soffit. Here it is simply the head stone
    # of the opening, bedded under the same open joint as the rest of the course.
    p.box((0, (-.132 + .06) / 2, (V_Z1 + BLK_TOP + LAP) / 2),               # lintel
          (2 * e, .192, BLK_TOP + LAP - V_Z1), "stone_pale", bevel=.011, seg=1,
          tint=.05, shade=.95 + r.uniform(-.04, .04))
    for bx in (-.105, 0.0, .105):                         # the grille
        p.box((bx, -.047, (V_Z0 + V_Z1) / 2), (.024, .022, V_Z1 - V_Z0 + .012),
              "iron", bevel=.004, seg=1, tint=.05, shade=.92)
    p.box((0, -.041, (V_Z0 + V_Z1) / 2), (2 * V_W2 + .012, .022, .022),
          "iron", bevel=.004, seg=1, tint=.05, shade=1.0)
    coping(p, -HX, HX, CAP_Z0, H, "vent")
    _wob(p)
    return p.finish()


def build():
    return [plinth_a(), plinth_b(), corner(), corner_inner(), step(), batter(),
            vent(), riser()]


# ==================================================================== demo ====
# The demo has to prove the two things a lineup cannot: that these pieces make a
# TERRACED base, and that they turn the FOUR corners a base with a projecting
# entrance has to turn. That needs ground at more than one level and a plan with
# a re-entrant angle in it, so the demo builds two context objects of its own --
# a stepped earth platform and a stand-in wall band above the coping. Neither is
# a kit piece (they are not in build(), they are not named SM_, and nothing else
# may use them); they are the site and the building, which is what a foundation
# is only legible against. The wall band is a plain mass on purpose: its only job
# is to sit its face on the wall plane so the FOUND_OUT setback reads as the
# shadow line it is meant to be.
#
# ===========================================================================
# THE PROJECTING ENTRANCE: THE PATTERN, AND THE ARITHMETIC THAT CLOSES IT
# ===========================================================================
# This is the part assemble_inn.py copies, so it is stated ONCE, as numbers, in
# _projection() -- which returns the piece placements AND the footprint of the
# storey they carry, out of the same two lines of arithmetic. It has to: the bug
# this replaced was a hand-written wall band disagreeing with a hand-written
# plan by exactly T. It stood the porch's wall 360 mm in front of the base meant
# to carry it -- overhanging the coping nose by 214 mm, with three quarters of
# its underside over air -- while every piece in the plan was correct and every
# other elevation lined up. Two plans of one thing is the defect; one plan with
# two readers is the fix, and it is why nothing below is typed twice.
#
# Measured from the main run's FACE plane (y = 0, where every wall face in the
# kit lies), a projection of `wide` front bays and `deep` return bays is:
#
#     w2 = wide * GRID / 2 + T      half-width, outside face to centre
#     d  = deep * GRID + T          depth, main face plane -> porch front face
#
# WIDTH AND DEPTH ARE NOT SYMMETRICAL, and that is the whole trick:
#   * the two FRONT angles are OUTSIDE corners. SM_Found_Corner's cell sits in
#     the void outside BOTH runs, so it adds T at each end -- spec.py's outer
#     rectangle rule, (n*GRID + 2T) x (m*GRID + 2T), applied to the front;
#   * the two REAR angles are RE-ENTRANT. SM_Found_CornerInner's cell is cut OUT
#     OF THE MAIN ELEVATION (it occupies x in [w2, w2 + T] of it) and takes
#     nothing from the return -- so the return is `deep` WHOLE bays and its last
#     bay seam lands exactly ON y = 0.
#
# That last line is not a convenience, it is what the inner corner is CUT FOR.
# The return's face plane IS the crease plane, so the return's coping nose
# oversails it by |NOSE| INTO the inner corner's cell, and CIN_NOTCH is the
# |NOSE| x |NOSE| hole the piece holds open for exactly that nose. Land the
# return anywhere else and the notch is either a 148 mm gap in the coping band
# or two slabs fighting over the bearing plane at z = H_FOUND. Land it here and
# the plan closes on the grid at all four corners with zero gap and zero overlap.
#
#  PLAN of the demo's entrance -- wide = deep = 1, so 2.72 m across the outside
#  and 2.36 m forward -- with the main elevation running along y = 0 and the
#  porch coming forward into -y. Every number on it is on the grid:
#
#         x  -3.72        -1.72 -1.36 -1.00          1.00  1.36 1.72       3.72
#  y=+0.36     +--- A ------+-CI-+.....:.............:.....+-CI-+--- step ---+
#  y= 0.00     +------------+----+     |             |     +----+------------+
#                            crease| pw |  interior  | pe |crease
#  y=-2.00                        +-----+------------+-----+
#                                 |  C  |    vent    |  C  |
#  y=-2.36                        +-----+------------+-----+
#
#     CI = SM_Found_CornerInner    C = SM_Found_Corner    pw/pe = the returns
#     The west inner corner is the same mesh MIRRORED: the piece is handed, its
#     crease being at the -x end of its own elevation. The dotted line is the
#     building's inside; no foundation runs there.
#
# The T x T square behind each return's last bay (x in [1.00, 1.36], y in
# [0, 0.36] on the east) belongs to no piece, by construction: the inner
# corner's cell comes out of the main elevation, not out of the return. It is
# inside the building, in the porch's inner angle, with the storey's own floor
# over it -- nothing bears on it and nothing sees it.
UZ, MZ, LZ = .60, .30, .075           # the three ground levels in the demo

PJ_BAYS_W = 1                         # the demo's entrance: bays across the front
PJ_BAYS_D = 1                         # ...and bays down each return
PJ_W2 = PJ_BAYS_W * G / 2 + T         # 1.36  outside half-width
PJ_D = PJ_BAYS_D * G + T              # 2.36  main face plane -> porch front face


def _projection(cx=0.0, z=UZ, wide=PJ_BAYS_W, deep=PJ_BAYS_D,
                front=("SM_Found_Vent",), side="SM_Found_Plinth_2m_B"):
    """ONE PROJECTING ENTRANCE, laid out from one number: cx, its centre on the
    main elevation. The block comment above is the derivation; this is the only
    place the numbers exist.

    Returns (pieces, band):
      pieces  (name, (x, y, z), rot_z_deg, mirror_x) -- the same row the demo's
              main-elevation entries use, so a caller just concatenates lists.
      band    (x0, x1, y0, y1) rectangles of the STOREY footprint this base
              carries: the wall bodies, whose FACES therefore land on the same
              planes the pieces' faces do and stand FOUND_OUT back from the
              stone. The main elevation's own band is the caller's to draw and
              runs straight past both inner corners -- it OWNS those two cells --
              so it stops at cx -/+ w2, where the returns take over.
    """
    w2 = wide * G / 2 + T
    d = deep * G + T
    pieces = [
        # ---- the two re-entrant joints, where the projection returns into the
        # main run. Handed, so the west one is the same mesh mirrored on x; both
        # butt the main elevation's next bay on their outer plane (cx -/+ w2+T)
        # and put their crease on the return's face plane (cx -/+ w2).
        ("SM_Found_CornerInner", (cx - w2 - T, 0.0, z), 0, -1),
        ("SM_Found_CornerInner", (cx + w2 + T, 0.0, z), 0, +1),
        # ---- the two outside corners at the front angles, each filling the T x T
        # void where the front run's face plane crosses its return's
        ("SM_Found_Corner", (cx - w2 + T, -d, z), 0, +1),
        ("SM_Found_Corner", (cx + w2, -d + T, z), 90, +1),
    ]
    for i in range(deep):             # the returns: whole bays, ending on y = 0
        y = -(i + .5) * G
        pieces.append((side, (cx - w2, y, z), 270, +1))   # faces -X
        pieces.append((side, (cx + w2, y, z), 90, +1))    # faces +X
    for j in range(wide):             # the front, between the two corner cells
        pieces.append((front[j % len(front)],
                       (cx + (j + .5 - wide / 2) * G, -d, z), 0, +1))
    band = [(cx - w2, cx - w2 + T, -d, 0.0),                 # west return + corner
            (cx - w2 + T, cx + w2 - T, -d, -d + T),          # the front
            (cx + w2 - T, cx + w2, -d, 0.0)]                 # east return + corner
    return pieces, band


def _ctx_terrace():
    """The site: three plateaus, stepping down FOUND_STEP where the coping steps
    and another H_FOUND/2 along the side run where the ground falls away.

    Each plateau tops out 2 mm ABOVE the pieces standing on it, so the masonry
    bites into the earth rather than sharing a plane with it, and each one
    reaches DOWN to the top of the plateau below, so the bank between two
    terraces is a real 300 mm face and the run in front of the building is
    standing on ground rather than floating over it."""
    p = Part("_ctx_terrace", smooth=False)
    for (x0, x1, y0, y1, zb, zt, sh) in (
            (-4.20, 3.70, -2.90, 2.60, MZ, UZ + .002, .46),      # upper terrace
            (3.68, 6.60, -2.90, 0.38, LZ, MZ + .002, .40),       # main level
            (3.68, 6.60, 0.36, 2.60, LZ - .12, LZ + .002, .34)):  # falling away
        p.box(((x0 + x1) / 2, (y0 + y1) / 2, (zb + zt) / 2),
              (x1 - x0, y1 - y0, zt - zb), "stone_dark", bevel=0, tint=.05,
              shade=sh)
    return p.finish()


def _ctx_walls(band, h=.44):
    """The stand-in storey: a plain mass whose face sits on the wall plane, so the
    110 mm the foundation stands proud of it is visible as one shadow line all the
    way round -- round the entrance's four corners, and where it steps down
    300 mm with the terrace.

    It draws whatever footprint it is HANDED, and it is handed the rectangles the
    plan itself computed. Nothing about the projection is typed here; that is the
    fix, not a style note."""
    p = Part("_ctx_walls", smooth=False)
    for (x0, x1, y0, y1, z0) in band:
        p.box(((x0 + x1) / 2, (y0 + y1) / 2, z0 - .004 + h / 2),
              (x1 - x0, y1 - y0, h), "stone", bevel=.014, seg=1, tint=.04,
              shade=.82)
    return p.finish()


def demo():
    """The inn's base: a projecting entrance bay dressed with all four corners it
    needs, and the ground then falling away east so the coping has to step a
    terrace and pick up a riser to stay level.

    Everything a level artist has to know about this family is in this one
    picture: the coping is the datum, the ground is not, the pieces make up the
    difference, and a base that comes forward needs the re-entrant corner as much
    as it needs the outside one. The entrance and the storey standing on it both
    come out of _projection(), so the wall faces and the foundation faces are on
    the same planes by construction rather than by agreement."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_Found")}
    A = "SM_Found_Plinth_2m_A"
    pj, pj_band = _projection(0.0, UZ)
    xw = -(PJ_W2 + T)                 # -1.72  the west inner corner's butt plane
    xe = PJ_W2 + T                    #  1.72  the east one's
    xs = xe + G                       #  3.72  where the step piece hands over
    xc = xs + G                       #  5.72  the far corner's cell, and the
    plan = ([                         #        outside face of the side run
        # ---- main elevation west of the entrance: faces -Y, tiles along X ----
        (A, (xw - G / 2, 0.0, UZ), 0, 1),
    ] + pj + [
        # ---- main elevation east of it, then down a terrace ------------------
        ("SM_Found_Step_2m", (xe + G / 2, 0.0, UZ), 0, 1),   # the level change
        (A, (xs + G / 2, 0.0, MZ), 0, 1),
        # the outside corner: its cell is x in [xc, xc+T], y in [0, T]
        ("SM_Found_Corner", (xc + T, T, MZ), 90, 1),
        # side run, faces +X, tiles along Y -- the tallest exposed side, so
        # battered, with a riser slid under it where the ground drops away and
        # the coping still has to come out level
        ("SM_Found_Riser_2m", (xc + T, T + G / 2, LZ), 90, 1),
        ("SM_Found_Batter_2m", (xc + T, T + G / 2, MZ), 90, 1),
    ])
    # THE STOREY, on the same arithmetic as the plan. The main elevation's band
    # runs past both inner corners -- their cells are its, not the returns' --
    # so it stops where the returns' outside faces are, at -/+ PJ_W2.
    band = ([(xw - G, -PJ_W2, 0.0, T, UZ + H)]
            + [(x0, x1, y0, y1, UZ + H) for (x0, x1, y0, y1) in pj_band]
            + [(PJ_W2, xe + G / 2 + XS, 0.0, T, UZ + H),   # up to the step's fall
               (xe + G / 2 + XS, xc, 0.0, T, MZ + H),      # ...and down a terrace
               (xc, xc + T, 0.0, T, MZ + H),               # the corner cell
               (xc, xc + T, T, T + G, MZ + H)])            # the side run
    out = [_ctx_terrace(), _ctx_walls(band)]
    for nm, loc, rz, mx in plan:
        s = src.get(nm)
        if not s:
            continue
        o = s.copy()
        o.data = s.data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (0.0, 0.0, radians(rz))
        o.scale = (mx, 1.0, 1.0)
        out.append(o)
    for nm in src:
        src[nm].location = (0, 60, 0)      # park the originals out of frame
    return out
