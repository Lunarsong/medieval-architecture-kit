r"""THREE MORE BUILDINGS OUT OF THE SAME KIT -- the proof that it is modular.

    blender -b --python assemble_layouts.py

assemble_inn.py assembles ONE building.  One building assembled from a kit is a
building; three buildings that differ in PLAN and MASSING and still read as one
street are a kit.  So this file models nothing at all either: it imports
assemble_inn as a library (its __main__ guard means importing it builds nothing)
and re-uses Blk / put / storey / gable_face / foundation / corners / lay_roof /
lay_ridge / gable / chimney / valley_run wholesale.  What is new here is PLAN.

  1  MARKET ROW   16.7 x 4.7, eaves to the street, TWO storeys under a roof
                  bigger than the wall under it.  Its whole ground floor is an
                  OPEN ARCADE -- six arches between two responds -- with the
                  half-timber storey standing straight on the piers and an
                  external TIMBER GALLERY on posts along the eastern third of
                  the front, turning the south-east corner onto the flank and
                  reached by an outside stair.  refs r9 / r10 / r11.  This is
                  the layout that finally uses SM_Wall_StoneArcade_2m_A/B,
                  SM_Wall_StoneArcadePier, SM_Corner_GalleryBay_2m,
                  SM_Corner_GalleryCorner and SM_Corner_GalleryStair -- six
                  pieces nothing in the kit used.

  2  COTTAGE      4.7 x 2.7, TWO BAYS, one stone storey, a half-timber attic
                  band, one dormer, one chimney, a plain gable each end.  The
                  hard direction: a kit that only makes showpieces is not a kit.

  3  L-PLAN       a 12.7 m range running west out of a taller cross-wing that
                  projects 6 m south at its east end.  Two ridges at right
                  angles, TWO VALLEYS down one side of the wing, and a
                  re-entrant armpit dressed with SM_Corner_StoneInner and
                  SM_Found_CornerInner -- none of which the inn exercises (its
                  cross gable is a symmetrical four-valley crossing and it never
                  places an inner corner at all).

===========================================================================
THE FIVE THINGS THAT HAD TO BE SOLVED, AND WHERE
===========================================================================
1. THE ARCADE RUN DOES NOT LAND ON THE BAY GRID.  SM_Wall_StoneArcadePier is
0.46 m wide and stands OUTSIDE the last arch's seam (its docstring: centre it at
bay_centre +/- 1.23), so an arcade of n bays plus two responds is 2n + 0.92 long
and can never fill a whole number of modules.  Solved the way a mason solves it:
the two bays at the ends of the run are cut to 1.54 m (x-scale 0.77) and the
responds take up the remaining 0.46 each, so the run closes on the corner cells
exactly:  0.36 |1.54| 0.46 |6 x 2.00| 0.46 |1.54| 0.36 = 16.72.

2. THE GALLERY AND THE JETTY CANNOT SHARE AN ELEVATION, so the market row has
no jetty.  Both features own the same band of air: the jetty's bressumer sits at
z = 2.52..3.00 in y = -0.45..0 and its soffit closes y = -0.45..0 just under the
storey line, while the gallery's deck boards run y = -1.20..0 at z = 2.956..2.994
and its ledger is bolted to the wall at z = 2.59..2.78.  Laid over each other the
sill beam comes straight up through the deck boards (measured: 441 intersecting
face pairs, 477 mm).  An arcaded market hall does not need a jetty anyway -- r6,
r7 and r11 all stand the upper wall straight on the piers -- so the front carries
a bressumer STRING COURSE at the storey line instead, 60 mm proud of the stone,
and the depth in the elevation comes from the arcade below and the gallery in
front.  See the note handed back with this file.

3. THE GALLERY HANGS ON THE STOREY LINE, NOT ON A FOUNDATION.  Its deck top is
authored at GA_DKT = H_GROUND - 6 mm and the stair is exactly fifteen 0.20 m
risers of H_GROUND, so a gallery only lands on the floor inside if the ground
storey starts at z = 0.  The market row therefore sits straight on the paving
with no foundation course -- which is also what r9 shows, arcade piers rising out
of the cobbles -- while the cottage and the L-plan keep the inn's foundation.
The gallery corner is snapped at the SE corner spot of the STONE storey,
(x1, y0 + T_STONE) rotated 90, which puts its two butt planes at x = 16.48
(south run) and y = 0.24 (east run); the bays and the stair's top module line
tile off those.

4. THE L-PLAN'S ARMPIT IS THE ONE JOINT THE INN NEVER MAKES, and both pieces for
it are HANDED.  foundations.py states the convention exactly: cell x in [-T, 0],
y in [0, T]; y = 0 is the only EXPOSED plane; x = -T is the CREASE, where the
returning run's body carries straight on; x = 0 is the BUTT, where the main run's
next bay lands.  Our armpit is at (8.00, 0.00) with the range's south face on
y = 0 and the wing's west face on x = 8.00, so the piece goes in at rz = -90:
its exposed face becomes the WING's west elevation, its crease becomes the
range's south face plane y = 0, and its butt plane is y = -0.36, which is where
the wing's west run has to stop.  Get that 0.36 wrong and the piece's dressed
jamb ends up buried inside the wing's wall -- which is exactly what the first
build of this file did, and check_collisions found it at 874 face pairs.

5. THE L-PLAN'S VALLEY APEX IS A CHOSEN NUMBER, NOT AN ACCIDENT.  Two ridges at
right angles meet where the lower one dies into the higher one's slope, at
    apex = wing_ridge_x - (wing_datum - range_datum) / (ZK * tan(PITCH_F))
and if that lands mid-bay the range's ridge run stops short of it and leaves a
notch.  So the wing is set 1.16 m above the range -- not 0.70 like the inn's
hero -- because that puts the apex at x = 9.82, exactly five 2 m bays from the
range's roof run start at -0.18.  The ridge cap then ends ON the apex and the
two valleys close on it.  The range's dormers are kept west of x = 6.4 for the
same reason: the wing's west eave line is x = 7.40, and a 2 m dormer centred on
the bay at 7.36 is sliced in half by it.

===========================================================================
RE-SYNCED WITH assemble_inn.  FOUR FAULTS THIS FILE HAD INHERITED FROM IT
===========================================================================
This file was written while assemble_inn was still being corrected, so it copied
that file's conventions as they were THEN.  Four of them have since been fixed in
the inn and were still standing here.  Measured with check_layouts.py, before and
after, on all three layouts:

    THROUGH-ROOF   1814 verts on 9 objects, worst 2.007 m   ->  0
    WALL-RUN GAPS  the arcade (12.00), the crossing, and TWO
                   holes of exactly 0.240 m = T_TIMBER      ->  the arcade and
                                                                the crossing only

1. THE JETTY IS TAKEN FROM THE ASSEMBLER NOW (A.JT = 0.0), not from spec.JETTY.
   See the note by the imports: 0.45 is not a multiple of GRID, so it walks a
   corner post out of the T x T void it fills and a gable face past the verge its
   own roof stops at.  Both of those were measurable here.  jetty_underside(),
   jetty_returns() and every jetty= argument are gone with it.

2. THE NARROW GABLE ENDS ARE LAID BY A.gable_face(), which this file had never
   called once.  A gable end here is an EVEN number of bays, so no bay centre
   lands on the wall's centre line and a window in a bay sits off to one side
   under a symmetrical gable.  gable_face() lays the face out from the centre --
   one window bay on the centre line, the rest split into two equal fillers --
   and gable_band() below carries the plate band it does not.  Six faces: the
   market row's two ends, the range's west end, the wing's two ends.  (The
   cottage's ends are ONE bay, so their window is already on the centre line and
   gable_face() correctly declines to touch them.)

3. THE LOCAL COPY OF A.corners() IS DELETED.  It existed for one flag that
   A.corners() now takes (joint=), and while it sat here A.corners() learned to
   scale posts and braces by the storey's own zs -- which is why four 2.60 m
   corner posts stood 1.49 m through the cottage's 1.30 m attic band.

4. THE COTTAGE'S "TWO ROOF LINES" WERE ITS ATTIC BAND.  SM_Wall_TimberGable_2m is
   gable-end infill -- a cream TRIANGLE with its own rakes -- and run round four
   faces as a band it drew a second rake under the real one at both ends.  The
   band is ordinary walling now, the way every other band in this file and in the
   inn is built.

WHAT IS STILL WRONG, AND IS NOT OURS.  A.gable() places SM_Gable_Barge_* at the
wall face and the piece projects 0.513 m past it, while the roof run it has to
meet is built on spec.VERGE_OVER = 0.30 -- so the barge stands 0.213 m proud of
the verge in plan, and its foot scroll, which turns UP off the rake, ends up as
much as 1.194 m clear of the swept eave beneath it.  That is Shanee's "gable
facade/barge mismatching the roof line".  It is not a market row fault: the inn's
own 2-bay gables measure 0.213 m and 1.194 m at the identical local coordinates,
and the numbers cannot be moved from a layout, because the roof's across-extent
is nseg * SLOPE_SEG * cos(PITCH) and no integer nseg lands on the barge's foot.
The gable END matches the roof plane exactly (0 verts through, all six of them);
it is the BARGE and the FINIAL that overhang.  See the notes handed back.
"""
import bpy, sys, os, json
from math import radians
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kit import spec as S, util as U, render as R, finalize as F
import assemble_inn as A                      # __main__ guard: builds nothing

G, TS, TT = S.GRID, S.T_STONE, S.T_TIMBER
HG, HU = S.H_GROUND, S.H_UPPER
# NO `JT`.  The jetty is taken from the ASSEMBLER (assemble_inn.JT, now 0.0)
# and not from spec, and on this file that means it is off everywhere.  JETTY is
# 0.45, which is not a multiple of GRID, so offsetting a wall plane by it takes
# that run out of alignment with its flanks and moves the corner piece OUT of
# the T x T void it exists to fill.  Measured here before it went: two wall-run
# holes of exactly 0.240 m -- T_TIMBER, i.e. one corner cell -- on the L-plan
# wing's west and east runs, and the wing's own proud plate standing 2.007 m
# through its roof, because the jettied face had walked 0.45 m past the verge
# line the roof stops at.  Same signature, same cause and same remedy as the
# inn: see assemble_inn's note over `JT = 0.0`.
BASE, INSET, VO = S.H_FOUND, TS - TT, S.VERGE_OVER

LAYOUTS = []            # (name, [objects], summary dict)


# ---------------------------------------------------------------------------
# MODULE STATE IN assemble_inn THAT IS BOUND TO THE INN, AND HOW IT IS RESET
# ---------------------------------------------------------------------------
# put() counts into A.placed and links into A.INN; find() reports into
# A.missing; the clutter pass reads A.OBSTACLES; and -- the one that actually
# matters -- lay_roof() and lay_ridge() take the OTHER masses to trim against
# from the module global A.ALL, which is the inn's own (MAIN, HERO).  All five
# are rebound here per layout rather than edited in assemble_inn.py, because
# they are a scene's state and not the library's.  A proper refactor would pass
# them in; see the notes handed back with this file.
def begin(name):
    A.placed, A.missing, A.OBSTACLES = 0, [], []
    A.INN = U.get_collection(name)
    return A.INN


def end(name, coll):
    objs = [o for o in coll.objects if o.type == 'MESH']
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in objs)
    rec = dict(name=name, placed=A.placed, missing=sorted(set(A.missing)),
               tris=tris)
    LAYOUTS.append((name, objs, rec))
    print("LAYOUT_JSON " + json.dumps(rec))
    return objs


def part(nm, at, rz, length, zs=1.0):
    """One wall piece cut to `length` along its own tiling axis.  A part bay is
    ordinary kit practice -- assemble_inn cuts roof courses and jetty returns
    the same way -- and it is what lets a run close on a plane that is not a
    whole number of modules away."""
    return A.put(A.P(nm), at, rz, scale=(length / G, 1.0, zs))


# THE LOCAL COPY OF A.corners() IS GONE.  It existed because A.corners()
# hardcoded SM_Corner_JettyJoint -- the sill course of a jetty transition, which
# on a building with no jetty is a beam stub in mid air and, at the market row's
# south-east corner, a beam stub inside the gallery deck.  A.corners() takes
# `joint=` now, so the copy had nothing left to add -- and it had quietly lost
# the one thing it could not do: A.corners() scales its posts and arch braces by
# the STOREY's own `zs`.  Without that a 2.60 m corner post in the cottage's
# 1.30 m attic band stood 1.49 m through the roof, four times over.  Every local
# copy is a fault waiting to be fixed twice; this one was.


# A corner post BULGES 0.15 m past BOTH of its wall planes -- spec.py allows it
# ("Corner geometry may bulge outward") and every SM_Corner_TimberPost measures
# 0.390 across a 0.240 cell.  On an EAVE face the roof plane meets the wall plane
# exactly AT the datum, so a post whose head is at the datum stands that bulge
# 0.15 * tan(65) = 0.32 m out on the shingles: measured 0.19-0.26 m of post
# through the roof at every band corner of all three layouts.  assemble_inn never
# hits it because its top corner post stops at a STOREY head with a band above
# it; a band that is itself the top of the wall has to tuck its own corner.
POST_BULGE = 0.15
POST_TUCK = POST_BULGE * A.TANF                    # 0.322


def gable_band(blk, side, z, band_h, win="b", fill="a", plate=True):
    """The plate band over an A.gable_face(), and its projecting head plate.

    A.storey() drives the band off the same bay loop it drives the walls off and
    skips both for a None bay, so a face handed to A.gable_face() has to carry
    its own -- gable_face()'s docstring says exactly that.  A band is plain
    walling, so it is one more centred face with the window spec set to a panel;
    the head plate is the projecting course ref3 draws under every gable, laid on
    the block's own bay grid exactly as A.storey() lays it (the plate is a
    horizontal course, so its seams need not follow the centred face below it)."""
    A.gable_face(blk, side, z, zs=band_h / HU, win=win, fill=fill)
    if not plate:
        return
    n = blk.nx if side in "SN" else blk.ny
    for (cx, cy), rz in A.side_bays(blk, blk.tb, TT, side, n):
        A.put(A.P(A.SILLS[2]), (cx, cy, z + band_h - 0.48), rz)


def valley_pair(low, high, s_hi):
    """The two valleys where `low`'s roof dies into ONE side of `high`'s.

    A.cross_valleys() lays all FOUR valleys of a symmetrical crossing, which is
    right for the inn (its hero cuts the range on both sides) and wrong for an
    L, where the wing has a roof on one side only and the other two valleys
    would be laid in mid-air off the end of the building.  Same arithmetic,
    restricted to one side; A.valley_run() does the actual laying."""
    e_across = high.ridge_pos + s_hi * high.nseg * A.STEPY
    z_e = high.r52 - high.nseg * A.STEPZ
    d = (low.r52 - z_e) / A.TANP                  # down low's slope to that z
    top = (high.r52 - low.r52) / A.TANP           # where low's ridge dies
    for s_lo in (-1, 1):
        a0 = low.ridge_pos + s_lo * d
        if low.axis == 'X':
            p0, p1 = (e_across, a0), (high.ridge_pos + s_hi * top, low.ridge_pos)
        else:
            p0, p1 = (a0, e_across), (low.ridge_pos, high.ridge_pos + s_hi * top)
        A.valley_run(p0, p1, z_e)


def foundations(blk, spec):
    """A foundation course with SKIPPABLE bays.

    A.foundation() lays all four sides of a mass whole, which is right for a
    single rectangle and wrong for two masses that share a wall: on the L-plan
    the range's east course and the wing's west course would land on top of
    each other on an elevation you can see.  Same pieces, same convention, one
    spec list per side ('p' plinth, 'v' vent, None skip)."""
    for side, keep in spec.items():
        for i, ((cx, cy), rz) in enumerate(
                A.side_bays(blk, blk.st, TS, side,
                            blk.nx if side in "SN" else blk.ny)):
            if i >= len(keep) or keep[i] is None:
                continue
            nm = ("SM_Found_Vent" if keep[i] == "v"
                  else A.vpick(A.FOUND, cx, cy))
            A.put(A.P(nm), (cx, cy, 0.0), rz)


def dormer_run(blk, sgn, poss, s=1.0, inb=0.95, nm=None, flower=True):
    """A.dormer(), generalised to either slope of either ridge direction and to
    a scale.

    A.dormer() is hardcoded to the -Y slope of a ridge-along-X mass at the inn's
    own 6.3 m roof depth, and both of those bite here: the cottage's roof
    triangle is 2.66 m, so an unscaled dormer's finial stands half a metre over
    its ridge, and the L-plan's wing has its slopes facing -X.  The control
    point is the piece's own (D_YWALL, D_ZROOF) and it is scaled with the piece,
    which keeps it self-consistent -- a dormer is not a roof-family piece and
    takes no part in the Z stretch."""
    wall = ((blk.y0 if sgn < 0 else blk.y1) if blk.axis == 'X'
            else (blk.x0 if sgn < 0 else blk.x1))
    across = wall - sgn * inb                     # inboard of the wall face
    zd = (blk.ridge - (abs(across - blk.ridge_pos) - A.D_YWALL * s) * A.TANF
          - A.D_ZROOF * s)
    rz = blk.rz(sgn)
    # STEP THE INDEX, do not hash the position. A.vpick() hashes (u, zd) into a
    # 4-entry table, and a 4-entry table picked by hash lands on one entry about
    # one run in sixteen: the market row's three dormers all came out
    # SM_Dormer_Gabled_1m5 -- one shared mesh datablock, same scale, same flower
    # box -- and the L-plan's two both came out _1m2_C. The user reported exactly
    # this class on the inn ("Dormers were literally the same object three
    # times") and assemble_inn.py was fixed to step the index; dormer_run never
    # was, and it has collided on both buildings that place more than one.
    off = int(abs(across) * 7 + abs(poss[0] if poss else 0) * 3) % len(A.DORMERS)
    for i, u in enumerate(poss):
        x, y = (u, across) if blk.axis == 'X' else (across, u)
        A.put(A.P(nm or A.DORMERS[(off + i) % len(A.DORMERS)]),
              (x, y, zd), rz, scale=(s, s, s))
        if flower:
            A.put(A.P("SM_Win_FlowerBox"), (x, y, zd + 0.26 * s), rz,
                  scale=(s, s, s))
    return zd


_PAV = {}


def cobbles(x0, x1, y0, y1, keep=8, seed=0, fray=True):
    """Paving on the walls' own grid, top face pinned to z = 0 so props stand ON
    it (assemble_inn's rule, and the reason for the per-piece drop), laid 10 %
    oversize so a patch's cut border stones are buried under its neighbour's,
    and quarter-turned only so no diamond gaps open at the grid corners.

    `fray` thins the outer ring: a rectangle of cobble with four straight sides
    is a decal however well it tiles."""
    cob = ("SM_Ground_Cobble_2m_A", "SM_Ground_Cobble_2m_B")
    r = U.rng(f"pav/{seed}/{x0}/{y0}")
    nx = int(round((x1 - x0) / G))
    ny = int(round((y1 - y0) / G))
    for j in range(ny):
        for i in range(nx):
            x, y = x0 + G * i, y0 + G * j
            # NOT the row against the building: that one is the apron at the
            # door and a hole in it reads as a hole, not as a frayed edge.  The
            # buildings all stand on the +y side of their paving, so the row to
            # keep solid is j == ny - 1.
            edge = fray and (i in (0, nx - 1) or j == 0)
            # THE CORE STAYS SOLID. A first pass thinned the whole field at
            # `keep` and the street came out moth-eaten, which reads far worse
            # than a straight edge -- assemble_inn found the same thing. Only
            # the outer ring is nibbled, and that is what frays the rectangle.
            if edge and r.randrange(10) >= keep - 5:
                continue
            nm = A.vpick(cob, x, y)
            if nm not in _PAV:
                ob = A.P(nm)
                lo, hi = R.bbox_of([ob]) if ob else (None, None)
                _PAV[nm] = -hi.z if ob else 0.0
            A.put(A.P(nm), (x + G / 2, y + G / 2,
                            _PAV[nm] - (0.004 if edge else 0.0)),
                  90 * r.randrange(4), scale=(1.10, 1.10, 1.0))


def tufts(spots, big=1.05):
    names = ("SM_Prop_WeedTuft_A", "SM_Prop_WeedTuft_B", "SM_Prop_MossPatch")
    for x, y in spots:
        r = U.rng(f"tuft/{x:.2f}/{y:.2f}")
        for i in range(3):
            sc = big * r.uniform(0.9, 1.4)
            A.put(A.P(names[r.randrange(3)]),
                  (x + r.uniform(-.34, .34), y + r.uniform(-.28, .28), 0.0),
                  r.uniform(0, 360), scale=(sc, sc, sc * 0.9))


def clutter(items):
    for nm, x, y, rz in items:
        A.put(A.P(nm), (x, y, 0.0), rz)


# ===========================================================================
# 1.  MARKET ROW -- arcade, string course, gallery, outside stair
# ===========================================================================
# WHY IT SITS ON THE GROUND AND THE OTHER TWO DO NOT: see the header.  The
# gallery family derives every height it has from spec.H_GROUND (deck top
# GA_DKT = 2.994, stair 15 x 0.200 = 3.000, handrail 3.95), so a foundation
# course under this mass would put the deck 0.45 m below the floor it is
# supposed to be an extension of, and the stair would climb to nowhere.
#
# TWO storeys, not three, and a datum of only 6.80 over a 16.7 m front: the
# reference market rows (r9, r11) are LOW and their roofs are enormous.  Ours
# runs 6.34 m of roof over 5.27 m of visible wall, where the inn runs 6.34 over
# 7.30.  That inversion, plus the arcade, is what stops this reading as the inn
# again -- it is a roof with a market under it rather than a wall with a hat on.
def market_row():
    coll = begin("L1_MarketRow")
    D = 6.80                            # 3.00 stone + 2.60 timber + 1.20 band
    B = A.Blk(0.00, 0.00, 16.72, 4.72, 'X', D, 3)
    A.ALL = (B,)
    ARC_BAYS = (3.36, 5.36, 7.36, 9.36, 11.36, 13.36)
    DORM_X = (3.36, 7.36, 11.36)

    # ---- ground storey: SIX OPEN ARCHES between two responds ---------------
    # The south face is laid by hand because the run does not fit the bay grid
    # (header note 1).  Everything else about it is the family's own: the arcade
    # bays carry the same wall head, plinth, string course and bed lines as the
    # rubble bays they butt, so the storey above lands flat on all of them.
    A.storey(B, 0.0, "stone",
             dict(S=[None] * 8,
                  N=["b", "c", "win", "a", "b", "win", "a", "c"],
                  W=["a", "c"], E=["b", "a"]))
    part("SM_Wall_StoneRubble_2m_A", (1.13, 0.0, 0.0), 0, 1.54)
    A.put(A.P("SM_Wall_StoneArcadePier"), (2.13, 0.0, 0.0), 0)
    ARC = ("SM_Wall_StoneArcade_2m_A", "SM_Wall_StoneArcade_2m_B")
    for i, x in enumerate(ARC_BAYS):
        A.put(A.P(ARC[i % 2]), (x, 0.0, 0.0), 0)
    A.put(A.P("SM_Wall_StoneArcadePier"), (14.59, 0.0, 0.0), 0)
    part("SM_Wall_StoneRubble_2m_B", (15.59, 0.0, 0.0), 0, 1.54)
    A.corners(B, "stone", "SWSENENW", z=0.0)

    # ---- the half-timber storey, standing straight on the piers ------------
    # W and E ARE THE GABLE ENDS, and they are an EVEN number of bays wide, so
    # no bay centre lands on the wall's centre line: a window in a bay is
    # necessarily off to one side under a symmetrical gable, which is Shanee's
    # "windows not centered with half walls on the sides on the narrow walls".
    # A.gable_face() lays those two faces out from the CENTRE instead -- one
    # window bay on the centre line, the remainder split into two equal fillers
    # -- and gable_band() carries the plate band gable_face() does not.
    BH = D - HG - HU                                   # 1.20, the plate band
    A.storey(B, HG, "timber",
             dict(S=["a", "win", "b", "win", "a", "win", "b", "win"],
                  N=["c", "a", "win", "b", "a", "c", "b", "a"]),
             flower="S", band_sides="SN", band_h=BH)
    for side in "WE":
        A.gable_face(B, side, HG)
        gable_band(B, side, HG + HU, BH)
    # ...and its BRESSUMER STRING COURSE, at the storey line and 60 mm proud of
    # the stone, which is what r9 and r11 run over an arcade in place of a
    # jetty.  60 mm, not 0: laid on the wall face plane its own face would be
    # coplanar with the rubble field's and flicker.
    #
    # IT STOPS AT x = 10.36, where the stair's top flight and then the gallery
    # take the line over.  SM_Beam_JettySill is 0.48 deep and sits at
    # z = 2.52..3.00, and that is exactly the band the gallery's deck boards
    # (2.956..2.994) and the stair's top four treads occupy -- run the whole
    # length it comes through the deck.  The gallery's own bressumer carries the
    # line from there, 0.30 deep at 2.66..2.96, which is the same line.
    for cx in (1.13, 3.36, 5.36, 7.36, 9.36):
        A.put(A.P(A.vpick(A.SILLS, cx, 0.0)), (cx, -0.06, HG - 0.48), 0)
    A.corners(B, "timber", "SWSENENW", brace=True, z=HG, joint=False)
    # ...and the band's own corner cells.  A 1.20 m band left a 0.24 x 0.24 x
    # 1.20 notch at each corner of the elevation with nothing in it.
    A.corners(B, "timber", "SWSENENW", brace=False, z=HG + HU,
              zs=(BH - POST_TUCK) / HU, joint=False)

    # ---- roof -------------------------------------------------------------
    A.lay_roof(B)
    A.lay_ridge(B)
    A.gable(B, 'W', var="B")
    A.gable(B, 'E', var="A")
    dormer_run(B, -1, DORM_X)
    # chimneys clear of every dormer in x -- 1.10 sits between the west gable
    # and the first dormer, 14.36 between the last dormer and the gallery
    A.chimney(B, 1.10, 1.05, "C")
    A.chimney(B, 14.36, 0.95, "A")
    for sgn, along, up, n, sc, sd in ((-1, .22, .07, 16, .95, 1),
                                      (-1, .70, .10, 14, .88, 2),
                                      (1, .45, .08, 14, .92, 3)):
        A.roof_drift(B, sgn, along, up, n=n, sc=sc, spread=(1.6, .40), seed=sd)

    # ---- THE GALLERY ------------------------------------------------------
    # Snapped at the SE corner spot of the STONE storey, (x1, y0 + T) rotated
    # 90, i.e. the same origin arithmetic A.corners() uses.  Its butt planes are
    # then x = 16.48 for the south run and y = 0.24 for the east run, and every
    # bay and the stair's top module line tile off those.
    A.put(A.P("SM_Corner_GalleryCorner"), (16.72, 0.24, 0.0), 90)
    for x in (15.48, 13.48):                       # south run, over the arcade
        A.put(A.P("SM_Corner_GalleryBay_2m"), (x, 0.0, 0.0), 0)
    for y in (1.24, 3.24):                         # and round onto the flank
        A.put(A.P("SM_Corner_GalleryBay_2m"), (16.72, y, 0.0), 90)
    # two bays long, so its top tread lands on the deck at the module line
    # x = 12.48 where the south run begins
    A.put(A.P("SM_Corner_GalleryStair"), (10.48, 0.0, 0.0), 0)

    # ---- the market under the arches --------------------------------------
    cobbles(-4.0, 22.0, -6.0, 0.0, keep=8, seed=1)
    cobbles(0.36, 16.36, 0.36, 4.36, keep=10, seed=2, fray=False)
    # on the two piers the gallery does NOT stand over: a bracket lantern at
    # z = 2.30 reaches z = 3.0, which is the gallery's bressumer and deck
    for x in (2.13, 12.36):
        A.put(A.P("SM_Light_WallLantern_A"), (x, 0.0, 2.30), 0)
    A.put(A.P("SM_Sign_InnBoard_B"), (4.36, 0.0, 2.30), 0)
    A.put(A.P("SM_Sign_NoticeBoard"), (6.36, 0.0, 1.20), 0)
    # ...and two on the INNER face of the north wall (y = 4.36, the lining
    # plane), because an arcade is only an arcade if you can see it has a depth:
    # through an open arch the eye needs something lit 4 m back or the opening
    # reads as a recess with a panel in it.
    for x in (5.36, 11.36):
        A.put(A.P("SM_Light_WallLantern_B"), (x, 4.36, 2.30), 0)
    clutter([("SM_Prop_Barrel_Large_A", 3.95, 1.35, 15),
             ("SM_Prop_Barrel_Large_B", 5.05, 0.95, 40),
             ("SM_Prop_Crate_A", 6.05, 1.55, 20),
             ("SM_Prop_Crate_B", 6.70, 0.95, -14),
             ("SM_Prop_Sacks", 8.10, 1.55, 25),
             ("SM_Prop_Barrel_Lying_Large", 10.20, 1.20, 84),
             ("SM_Prop_Barrel_Small_C", 12.30, 1.00, 0),
             ("SM_Prop_Trough", 3.20, -1.15, 0),
             ("SM_Prop_Barrel_Large_A", 7.40, -1.30, 30),
             ("SM_Prop_Crate_A", 13.90, 1.35, 8),
             ("SM_Prop_Bucket", 9.10, 1.60, 0),
             ("SM_Prop_Planter", 2.60, -0.62, 0),
             ("SM_Prop_Planter", 16.20, -0.75, 0),
             # stacked against the back wall, for the same reason as the
             # lanterns: depth read through the arches
             ("SM_Prop_Crate_A", 4.60, 3.30, 12),
             ("SM_Prop_Barrel_Lying_Large", 7.15, 3.45, 8),
             ("SM_Prop_Barrel_Large_B", 9.90, 3.35, 30),
             ("SM_Prop_Sacks", 12.60, 3.20, 18)])
    A.put(A.P("SM_Prop_Creeper_2m"), (12.48, -0.28, 3.95), 0)
    A.put(A.P("SM_Prop_Ladder"), (0.90, -0.62, 0.0), 6, rx=-9)
    tufts([(-0.35, 1.20), (-0.33, 3.40), (17.05, 1.10), (17.07, 3.60),
           (0.60, -0.30), (5.10, -0.32), (12.60, -0.30), (16.30, -0.34)])
    return end("MarketRow", coll)


# ===========================================================================
# 2.  THE COTTAGE -- two bays, one storey, an attic and a dormer
# ===========================================================================
# THE HARD DIRECTION.  Everything the kit is good at pushes a building UP: the
# pitch is 65 degrees and not negotiable, so a mass two bays DEEP has a 4.80 m
# roof triangle whatever else you do, and two bays deep by two bays long comes
# out 9.6 m tall on a 4.7 m square -- a tower, not a cottage.  So the cottage is
# ONE bay deep (2.72 m), which halves the triangle to 2.66 m and drops nseg to
# 2, and the attic is a band rather than a storey.  Two decisions follow:
#
#   the band is SM_Wall_TimberGable_2m, not a squashed wall.  The gable-end
#   infill piece is authored 1.28 m tall, which is what an attic knee wall
#   actually is; stretching a 2.6 m panel down to 1.3 would have halved the
#   height of every stud and brace in it.
#
#   the dormer is scaled 0.72.  At full size its finial stands 0.5 m over a
#   7.4 m ridge.  A small building gets small carpentry.
def cottage():
    coll = begin("L2_Cottage")
    D = BASE + HG + 1.30                                   # 4.75
    B = A.Blk(0.00, 0.00, 4.72, 2.72, 'X', D, 2)
    A.ALL = (B,)

    A.foundation(B, vent_bays=(("S", 1),))
    A.storey(B, BASE, "stone",
             dict(S=["win", "arch"], N=["b", "c"], W=["a"], E=["win"]))
    A.corners(B, "stone", "SWSENENW", z=BASE)

    # THE ATTIC BAND IS A KNEE WALL, AND IT IS PLAIN WALLING.
    # It used to be SM_Wall_TimberGable_2m run round all four faces "at its
    # authored height", and that piece is exactly what its own docstring says it
    # is: "Gable-end infill: a CREAM triangle framed the way ref3 frames its big
    # gable ... Bargeboard and tooth trim lap the rakes".  It is a TRIANGLE with
    # its own rakes, authored to sit under an apex.  Used as a band it painted a
    # small gable on every elevation of this cottage, and at the two gable ends
    # its apex landed exactly on the real gable's base line, so the west end read
    # as two nested triangles -- one rake line under another.  That is Shanee's
    # "the cottage looks like it has 2 roof lines in some places"; measured, the
    # inner rake ran from (0.36, 3.45) and (2.36, 3.45) up to (1.36, 4.75), and
    # the real gable's rake started from (0.12, 4.75) and (2.60, 4.75).
    #
    # So the band is what a band is everywhere else in this file and in the inn:
    # ordinary half-timber walling squashed to the band height, laid by A.storey.
    # It costs the studs their full length, which is the reason the gable piece
    # was reached for in the first place -- but a band 1.30 m tall on a 4.72 m
    # cottage carries one panel and two posts, and a false rake line across the
    # hero elevation is not a price worth paying for their proportion.
    #
    # Two calls, because the two pairs of faces meet the roof differently.  On an
    # EAVE face the roof plane arrives AT the wall plane exactly at the datum and
    # the swept eave course dips below it, so a band built to the full datum
    # stands its head out on the shingles -- measured here at 0.087-0.129 m over
    # four bays before this tuck, which is assemble_inn's BAND_TUCK fault word
    # for word, so it takes assemble_inn's BAND_TUCK.  What it loses is inside
    # the roof space under a 0.73 m overhang.  The GABLE faces are exposed, the
    # gable end sits on them, and nothing is over them to poke through.
    BH = D - BASE - HG                                 # 1.30
    A.storey(B, BASE + HG, "timber", dict(W=["a"], E=["b"]), zs=BH / HU)
    A.storey(B, BASE + HG, "timber", dict(S=["a", "b"], N=["b", "c"]),
             zs=(BH - A.BAND_TUCK) / HU)
    # zs -- the one thing the local copy of A.corners() could not do.  A 2.60 m
    # corner post in a 1.30 m band stood 1.49 m through this roof at all four
    # corners (1602 verts on eight objects), and those four posts breaking the
    # rake at the west end are the "2 roof lines" Shanee read off the render.
    A.corners(B, "timber", "SWSENENW", brace=False, z=BASE + HG,
              zs=(BH - POST_TUCK) / HU, joint=False)

    A.lay_roof(B)
    A.lay_ridge(B)
    A.gable(B, 'W', var="C", win=False)
    A.gable(B, 'E', var="A")
    dormer_run(B, -1, [3.36], s=0.72, inb=0.25)
    A.chimney(B, 0.90, 0.80, "A")
    A.roof_drift(B, -1, 0.30, 0.10, n=10, sc=0.80, spread=(1.0, .34), seed=1)

    # a doorstep, a water butt and five minutes of yard.  The flight is 1.04 m
    # deep and climbs exactly H_FOUND, and its top tread is at its +y end, so it
    # goes at y = -1.42: its nosing then lands 48 mm inside the threshold slab's
    # far edge and the landing is continuous from the street to the door.
    # assemble_inn's own -1.92 is 0.5 m further out because its porch floor
    # bridges the gap; a cottage with no porch would be left with a step up to
    # nothing.
    A.put(A.P("SM_Ground_StepsFlight_2m"), (3.36, -1.42, 0.0), 0)
    A.put(A.P("SM_Ground_ThresholdSlab"), (3.36, -0.50, BASE - 0.192), 0)
    A.put(A.P("SM_Light_WallLantern_B"), (2.42, 0.0, 2.60), 0)
    cobbles(-4.0, 8.0, -6.0, 0.0, keep=8, seed=3)
    clutter([("SM_Prop_Barrel_Large_B", 0.95, -0.72, 22),
             ("SM_Prop_Barrel_Small_C", 1.70, -0.60, 0),
             ("SM_Prop_Crate_B", 0.30, -1.45, 34),
             ("SM_Prop_Planter", 4.45, -0.62, 10),
             ("SM_Prop_Bucket", 1.62, -1.30, 0)])
    for i in range(2):
        A.put(A.P("SM_Ground_Fence_2m"), (6.10, -0.40 + G * i, 0.0), 90)
    A.put(A.P("SM_Prop_Creeper_2m"), (0.90, -0.05, 2.62), 0)
    tufts([(-0.35, 1.10), (5.05, 1.10), (0.40, -0.35), (4.30, -0.34)])
    return end("Cottage", coll)


# ===========================================================================
# 3.  THE L-PLAN -- two wings, two valleys, one armpit
# ===========================================================================
# PLAN.  Range x 0..12.72 (6 bays) by y 0..4.72 (2 bays), ridge along X, gable
# at its west end.  Wing x 8.00..12.72 (2 bays) by y -6.00..4.72 (5 bays),
# ridge along Y, gable at each end, PROJECTING 6 m south past the range.  The
# wing spans the range's full depth, so the north elevation and the east
# elevation are each one continuous run and the only junction in plan is the
# re-entrant at (8.00, 0.00).
#
# WHY THE WING SITS 1.16 M HIGHER, and where the armpit's two handed pieces go:
# header notes 4 and 5.
#
# THE RUNS AT THE ARMPIT.  The range's south run reaches the wing's face plane
# x = 8.00 (a 1.64 m part bay closing 6.36..8.00) and the wing's west run stops
# on the inner corner's butt plane y = -0.36 (a 1.28 m part bay closing
# -1.64..-0.36).  The T x T cell between them, x 8.00..8.36 by y -0.36..0, is
# SM_Corner_StoneInner, with SM_Found_CornerInner under it.  One bay short or
# long anywhere in that chain and the armpit either doubles up or opens a slot,
# which is why every one of those four numbers is written down.
def l_plan():
    coll = begin("L3_LPlan")
    DR = BASE + HG + HU + 1.20                    # 7.25
    DW = DR + 1.16                                # 8.41 -- see the header
    RG = A.Blk(0.00, 0.00, 12.72, 4.72, 'X', DR, 3, run=(-0.18, 9.82))
    WG = A.Blk(8.00, -6.00, 12.72, 4.72, 'Y', DW, 3)
    A.ALL = (RG, WG)
    ARM = (8.00, -0.36)                           # the inner corner's origin

    # ---- foundations, skipping every bay buried in the other mass ---------
    foundations(RG, dict(S=["p", "p", "p", None, None, None],
                         N=["p", "p", "v", "p", None, None],
                         W=["p", "p"], E=[None, None]))
    foundations(WG, dict(S=["p", "v"], N=["p", "p"],
                         W=["p", "p", None, None, None],
                         E=["p", "p", "p", "p", "p"]))
    part("SM_Found_Plinth_2m_A", (7.18, 0.0, 0.0), 0, 1.64)      # 6.36..8.00
    part("SM_Found_Plinth_2m_B", (8.00, -1.00, 0.0), -90, 1.28)  # -1.64..-0.36
    for (px, py), rz in (((0.36, 0.00), 0), ((0.00, 4.36), 270),
                         ((8.36, -6.00), 0), ((12.72, -5.64), 90),
                         ((12.36, 4.72), 180)):
        A.put(A.P("SM_Found_Corner"), (px, py, 0.0), rz)
    A.put(A.P("SM_Found_CornerInner"), (ARM[0], ARM[1], 0.0), -90)

    # ---- stone ground storey ----------------------------------------------
    A.storey(RG, BASE, "stone",
             dict(S=["b", "win", "a", None, None, None],
                  N=["c", "a", "win", "b", None, None],
                  W=["win", "win"], E=[None, None]))
    A.storey(WG, BASE, "stone",
             dict(S=["win", "arch"], N=["b", "c"],
                  W=["c", "a", None, None, None],
                  E=["b", "win", "a", "c", "win"]))
    part("SM_Wall_StoneRubble_2m_C", (7.18, 0.0, BASE), 0, 1.64)
    part("SM_Wall_StoneRubble_2m_A", (8.00, -1.00, BASE), -90, 1.28)
    A.corners(RG, "stone", "SWNW", z=BASE)
    A.corners(WG, "stone", "SWSENE", z=BASE)
    A.put(A.P("SM_Corner_StoneInner"), (ARM[0], ARM[1], BASE), -90)

    # ---- half-timber upper storey; only the wing's street gable jetties ----
    # The timber arris stands 0.12 inside the stone one on both faces, so the
    # armpit's two part bays are 0.12 longer up here than they are below.
    BHR = DR - BASE - HG - HU                     # 1.20
    A.storey(RG, BASE + HG, "timber",
             dict(S=["a", "win", "b", None, None, None],
                  N=["b", "c", "a", "win", None, None],
                  E=[None, None]),
             flower="S", band_sides="SN", band_h=BHR)
    # W is the range's gable end and two bays wide -- laid from the centre, so
    # its window is on the wall's centre line with a half-width filler each side
    A.gable_face(RG, 'W', BASE + HG)
    gable_band(RG, 'W', BASE + HG + HU, BHR)
    BHW = DW - BASE - HG - HU                     # 2.36
    A.storey(WG, BASE + HG, "timber",
             dict(W=["a", "b", None, None, None],
                  E=["win", "a", "win", "b", "a"]),
             flower="E", band_sides="WE", band_h=BHW)
    # S and N are the wing's two GABLE ENDS, both two bays wide, so both are
    # laid from the centre and carry their own band.
    # ...and the NORTH one takes NO head plate.  That gable rises out of the
    # RANGE's roof, and a plate is a projecting bressumer: 0.48 m deep against a
    # verge that oversails 0.30, its outer 0.18 m cleared the wing's own roof
    # altogether and came down 2.007 m clear of the range's shingles -- 212 verts,
    # the single worst object in this file before this round.  Where a roof abuts
    # a wall the joint is a valley, not a bressumer.
    for side, plate in (('S', True), ('N', False)):
        A.gable_face(WG, side, BASE + HG)
        gable_band(WG, side, BASE + HG + HU, BHW, plate=plate)
    # NO JETTY, HERE OR ANYWHERE ELSE IN THIS FILE -- see the note by the
    # imports.  What stood here was jetty_returns() + jetty_underside() on
    # S.JETTY = 0.45: it opened a 0.240 m hole (one corner cell) at both ends of
    # the wing's south wall, because the corner post had been carried 0.45 m out
    # of the void it fills, and it carried the south face's proud plate 0.45 m
    # past the verge the roof stops at, leaving it 2.007 m clear of any roof.
    part("SM_Wall_Timber_2m_C", (7.24, 0.12, BASE + HG), 0, 1.76)   # 6.36..8.12
    part("SM_Wall_Timber_2m_A", (8.12, -0.76, BASE + HG), -90, 1.76)  # -1.64..0.12
    A.corners(RG, "timber", "SWNW", brace=True, z=BASE + HG)
    A.corners(WG, "timber", "SWSENE", brace=True, z=BASE + HG)
    A.corners(RG, "timber", "SWNW", brace=False, z=BASE + HG + HU,
              zs=(BHR - POST_TUCK) / HU)
    A.corners(WG, "timber", "SWSENE", brace=False, z=BASE + HG + HU,
              zs=(BHW - POST_TUCK) / HU)
    # the internal angle post, filling the timber cell the two runs leave.  It
    # is an OUTSIDE corner post used at a re-entrant, because the corners family
    # has a stone inner corner and no timber one -- see the notes handed back.
    A.put(A.P("SM_Corner_TimberPost_B"), (8.36, 0.12, BASE + HG), 0)
    # ---- and the PLATE BAND over those two part bays ----------------------
    # A.storey() drives the band off the SAME bay list as the walls and skips
    # both for a None bay, so the two bays it skips here -- RG's S bay 7.36 and
    # WG's W bay -0.64 -- got a hand-laid wall above (the two part() calls) and
    # no band at all.  Measured in the built file: the range's south band ran
    # x 0.36..6.36 and the wing's west band y -5.64..-1.64, leaving a hole of
    #     1.76 x 1.05 m at y = 0.12, x 6.36..8.12, z 6.05..7.10   (range, south)
    #     1.76 x 2.21 m at x = 8.12, y -1.64..0.12, z 6.05..8.26  (wing,  west)
    # and the second of those is the ONE place in this building where
    # M_plaster_dim -- the material on the BACK of every timber panel -- is
    # visible from outside.  Traced with a ray: from the south-west the sight
    # line crosses the wing's west plane at (8.12, -1.25, 6.23), i.e. inside
    # that hole, and its first surface is the inside face of the wing's east
    # wall 4.2 m further on.  Nothing is in the way; it is a hole, not a leak.
    #
    # NOT A.compose_band(): it places FULL 2 m pieces and takes no width.  So
    # its stack is reproduced here at part width, 1.76 / 2.00 = 0.88, with the
    # same pieces and the same z scales the neighbouring bays measure --
    #   RG south  band_h BHR 1.20, non-proud -> 1.20 - BAND_TUCK = 1.05
    #             -> BandGable 1.00 + 0.05 residue,  z 6.05..7.10, zs 1.05
    #   WG west   band_h BHW 2.36, non-proud -> 2.36 - BAND_TUCK = 2.21
    #             -> Knee 1.30,                      z 6.05..7.35, zs 1.00
    #             -> BandEave 0.85 + 0.06 residue,   z 7.35..8.26, zs 0.91/0.85
    # NO head plate on either: neither A.storey() call passes band_proud, so
    # both of storey()'s plate branches are off for these faces and the
    # neighbouring bays carry none.  A projecting bressumer under an eave is
    # the fault the note over the wing's north gable describes.
    ZB = BASE + HG + HU                            # 6.05
    part("SM_Wall_TimberBandGable_2m", (7.24, 0.12, ZB), 0, 1.76, zs=1.05)
    part("SM_Wall_TimberKnee_2m", (8.12, -0.76, ZB), -90, 1.76)
    part("SM_Wall_TimberBandEave_2m", (8.12, -0.76, ZB + 1.30), -90, 1.76,
         zs=0.91 / 0.85)
    # NO fourth piece at the arris, and no post over it.  The band's corner
    # cell (x 8.12..8.36, y -0.12..0.12, T_TIMBER square) is already closed in
    # plan by the wing's west band bay, which runs to y = 0.12 exactly as the
    # wall below it does -- the same reason no timber inner-corner piece is
    # needed at the storey below, and there is none in the kit.  A
    # SM_Corner_TimberPost here would be dressing only, and it costs: the
    # storey post at this arris measures 603 and 593 intersecting face pairs
    # against the two runs it stands between, at 0.15 m -- its own bulge.
    # Overhead there is no room for a second one either.  The first roof
    # surface above the arris is the west valley at z 7.94 and the range's own
    # eave sweep dips to 7.05 at x = 7.60, against a band head of 8.26.

    # ---- the two roofs, and the valleys where they meet --------------------
    A.lay_roof(RG)
    A.lay_ridge(RG)
    A.lay_roof(WG)
    A.lay_ridge(WG)
    A.gable(RG, 'W', var="A")
    A.gable(WG, 'S', var="B")
    A.gable(WG, 'N', var="C", win=False)
    valley_pair(RG, WG, -1)                # the wing's WEST side only
    # WEST of the valley only: the wing's west eave line is x = 7.40, so a 2 m
    # dormer on the bay at 7.36 is cut in half by it
    dormer_run(RG, -1, [1.36, 5.36])
    A.chimney(RG, 3.36, 1.05, "B")
    A.chimney(WG, -4.20, 1.15, "C")
    A.roof_drift(RG, -1, 0.30, 0.09, n=14, sc=0.90, spread=(1.4, .40), seed=1)
    A.roof_drift(RG, 1, 0.62, 0.12, n=12, sc=0.86, spread=(1.4, .40), seed=2)
    A.roof_drift(WG, -1, 0.22, 0.08, n=14, sc=0.92, spread=(1.4, .40), seed=3)

    # ---- the yard in the armpit -------------------------------------------
    # ON THE DOOR BAY, x = 11.36, not on the wall's centre line at 10.36.  The
    # stone bays of this face are at 9.36 and 11.36 and the arched door is in
    # the second of them, so a 2 m porch centred at 10.36 covered the right half
    # of the window AND the left half of the door and stood against solid wall
    # between them.  The sign moves to the far bay to keep off its cheek.
    A.put(A.P("SM_Door_PorchGable_2m"), (11.36, -6.00, BASE), 0)
    A.put(A.P("SM_Ground_StepsFlight_2m"), (11.36, -7.42, 0.0), 0)
    A.put(A.P("SM_Ground_ThresholdSlab"), (11.36, -6.50, BASE - 0.192), 0)
    A.put(A.P("SM_Light_LanternHanging"), (11.36, -7.10, 2.44 + BASE), 0)
    A.put(A.P("SM_Sign_InnBoard_C"), (8.90, -6.00, 2.20), 0)
    A.put(A.P("SM_Ground_Well"), (2.40, -4.30, 0.0), 0)
    cobbles(-4.0, 16.0, -10.0, 0.0, keep=8, seed=4)
    for i in range(2):
        A.put(A.P("SM_Ground_GardenWall_2m"), (1.20 + G * i, -2.40, 0.0), 0)
    # EVERY ONE OF THESE IS WEST OF x = 7.5.  The wing's west wall face is
    # x = 8.00 and its foundation stands 0.11 proud of that, so a 0.42 m barrel
    # centred anywhere east of 7.45 is standing inside the building -- which is
    # where two of them were.
    clutter([("SM_Prop_Barrel_Large_A", 7.42, -1.10, 18),
             ("SM_Prop_Barrel_Large_B", 7.36, -2.10, 44),
             ("SM_Prop_Barrel_Lying_Large", 6.30, -1.15, 86),
             ("SM_Prop_Crate_A", 6.45, -2.05, 12),
             ("SM_Prop_Sacks", 5.45, -1.00, 30),
             ("SM_Prop_Planter", 10.22, -6.62, 0),
             ("SM_Prop_Planter", 12.50, -6.62, 0),
             ("SM_Prop_Trough", 4.20, -0.95, 0),
             ("SM_Prop_Bucket", 5.60, -1.60, 0),
             ("SM_Prop_Crate_B", 13.45, -4.35, 22)])
    A.put(A.P("SM_Prop_Ladder"), (2.60, -0.62, 0.0), 4, rx=-9)
    A.put(A.P("SM_Prop_Creeper_2m"), (1.36, -0.05, 2.90), 0)
    tufts([(-0.35, 1.20), (-0.33, 3.60), (8.35, -0.42), (7.60, -0.40),
           (13.05, -3.20), (13.03, 1.30), (9.40, -6.40), (12.70, -6.42),
           (2.40, -0.34), (5.20, -0.36)])
    return end("LPlan", coll)


# ===========================================================================
# LOOK + CAMERAS
# ===========================================================================
# The two fills, stated as OFFSETS from the building they light (see below).
FILL_SKY = dict(off=(11.0, -17.0, 15.0), tgt=(0.0, 0.0, 5.0), energy=3600,
                size=20, color=(0.66, 0.78, 1.0))
# The WEST fill.  The sun sits in the SOUTH-EAST, so every -X face in the kit --
# the L-plan's wing slope, the market row's west gable, the cottage's gable end
# -- is a shadow side, and at 26 W over 20 m it was a silhouette.
FILL_WEST = dict(off=(-14.0, -12.0, 7.0), tgt=(-1.0, -1.0, 6.5), energy=6200,
                 size=22, color=(1.0, 0.76, 0.50))


def look_street(res=(1600, 1000), samples=64, ctrs=((0.0, 0.0),)):
    """One light rig for all four frames, half way between the two hero looks:
    ref1's raking sun (so eaves, the arcade and the gallery throw real shadows
    and the undercroft goes properly dark) on ref2's calmer sky, because these
    are kit frames rather than a match to a painting.

    THE TWO FILLS ARE PLACED RELATIVE TO EACH BUILDING, not in world space.
    The three layouts stand 22 and 32 m apart on the street so the combined
    sheet can be one photograph, and a fill light fixed at the origin therefore
    lit the market row properly, the cottage weakly and the L-plan not at all --
    its whole west elevation and the wing's west roof slope went to black, which
    is the elevation the armpit and the valley are on.  The sun is shared (it is
    the same sun over the whole street); the fills follow the subject."""
    R.engine(eevee=True, samples=samples, res=res)
    R.world(top=(0.36, 0.50, 0.78), bottom=(0.50, 0.47, 0.42), strength=1.05)
    R.sun(energy=15.0, angle_deg=(56, 0, 34), softness=1.6,
          color=(1.0, 0.93, 0.78))
    for cx, cy in ctrs:
        for f in (FILL_SKY, FILL_WEST):
            ox, oy, oz = f["off"]
            tx, ty, tz = f["tgt"]
            R.area((cx + ox, cy + oy, oz), energy=f["energy"], size=f["size"],
                   color=f["color"], target=(cx + tx, cy + ty, tz))
    R._set_look('High Contrast')
    bpy.context.scene.view_settings.exposure = -0.62
    R.ground(color="stone_dark", z=-0.02, size=240)


def show_only(objs):
    keep = {o.name for o in objs}
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.startswith("SM_"):
            o.hide_render = o.name not in keep


def massing(objs):
    return [o for o in objs
            if not o.name.startswith(("SM_Ground_", "SM_Prop_", "SM_Sign_"))
            ] or objs


def hero(name, objs, yaw, out, pitch=80, lens=48, fill=(0.94, 0.90), z=0.44):
    """A STREET three-quarter, not a drone shot.  render.camera()'s pitch is 90
    at the horizon, so these sit 8-12 degrees above it: enough to read the plan
    of an L and the deck of a gallery, low enough that the arcade is a row of
    holes you look through rather than a row of shadows you look down on."""
    R.clear_stage()
    show_only(objs)
    build = massing(objs)
    lo, hi = R.bbox_of(build)
    tgt = (lo + hi) / 2
    look_street(ctrs=((tgt.x, tgt.y),))
    tgt.z = lo.z + (hi.z - lo.z) * z
    cam = R.camera(build, yaw=yaw, pitch=pitch, lens=lens, margin=1.0,
                   target=tgt)
    R.fit(cam, build, tgt, fill=fill, centre=(0.50, 0.50))
    R.save(out)


def street_sheet(out):
    """The three side by side AT THE SAME SCALE.  Orthographic, so that is true
    by construction rather than by luck of where the camera stood -- one metre
    is the same number of pixels on the cottage as on the market row, which is
    the whole point of putting them in one frame."""
    R.clear_stage()
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.hide_render = False
    allo = [o for name, objs, rec in LAYOUTS for o in objs]
    build = massing(allo)
    # one pair of fills per building, so all three are lit the way their own
    # hero frame lights them
    ctrs = []
    for name, objs, rec in LAYOUTS:
        lo_, hi_ = R.bbox_of(massing(objs))
        ctrs.append(((lo_.x + hi_.x) / 2, (lo_.y + hi_.y) / 2))
    look_street(res=(2600, 900), samples=48, ctrs=ctrs)
    lo, hi = R.bbox_of(build)
    tgt = (lo + hi) / 2
    cam = R.camera(build, yaw=-34, pitch=76, lens=50, margin=1.0, ortho=True,
                   target=tgt)
    cam.data.ortho_scale = 62.0
    bpy.context.view_layer.update()
    R.fit(cam, build, tgt, fill=(0.965, 0.92), centre=(0.50, 0.50))
    R.save(out)


# ===========================================================================
if __name__ == "__main__":
    A.load_library()
    A.texture_plaster()
    A.texture_roof(z0=3.0, z1=13.5)
    A.texture_stone()
    MB = ("shingle_moss", "shingle", "plaster", "plaster_dim", "oak_dark",
          "oak_mid", "oak_pale", "stone", "stone_pale", "stone_warm",
          "stone_dark", "terracotta", "thatch")
    A.occlude(MB, dist=0.85, floor=0.22)
    A.saturate(MB + ("moss",), 1.40)

    market_row()
    cottage()
    l_plan()
    # onto one street, in one scene, so the combined sheet is a photograph of
    # three buildings rather than three photographs pasted together
    for name, dx in (("Cottage", 22.0), ("LPlan", 32.0)):
        for n2, objs, rec in LAYOUTS:
            if n2 == name:
                for o in objs:
                    o.location.x += dx

    objs = [o for name, o_, r in LAYOUTS for o in o_]
    seen, reps = set(), []
    for o in objs:
        if o.data.name not in seen:
            seen.add(o.data.name)
            reps.append(o)
    F.finalize(objs=reps, tone=0.85, packed=False)

    out = os.path.join(ROOT, "renders", "layouts")
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    hero("MarketRow", LAYOUTS[0][1], 34, os.path.join(out, "market_row.png"),
         pitch=81, lens=46, z=0.40)
    hero("Cottage", LAYOUTS[1][1], -40, os.path.join(out, "cottage.png"),
         pitch=81, lens=52, z=0.46)
    hero("LPlan", LAYOUTS[2][1], -44, os.path.join(out, "l_plan.png"),
         pitch=78, lens=46, z=0.44)
    street_sheet(os.path.join(out, "all.png"))

    for name, o_, rec in LAYOUTS:
        print("LAYOUT_JSON " + json.dumps(rec))
    print("LAYOUTS_TOTAL " + json.dumps(dict(
        placed=sum(r["placed"] for _, _, r in LAYOUTS),
        missing=sorted({m for _, _, r in LAYOUTS for m in r["missing"]}),
        tris=sum(r["tris"] for _, _, r in LAYOUTS))))
    bpy.ops.wm.save_as_mainfile(
        filepath=os.path.join(ROOT, "out", "layouts.blend"))
