"""Ground-floor stone walling -- the heavy base course both references sit on.

===========================================================================
ROUND 6, PART 1: THE DEPTH LADDER  (this family INVENTED the z-fighting bug)
===========================================================================
The old `_backing()` helper here spanned y 0..T and the inner plaster skim's
back face ALSO landed on y = T, so the wall's VISIBLE inner surface was two
opaque coplanar faces and the renderer flickered between them.  Several other
families copied the pattern.  check_zfight measured 558525 cm2 on this family
alone -- the worst in the kit.

The fix is not "move the backing 26 mm forward so the pair is buried" (that
still leaves 6 m2 of coincident faces per piece, merely hidden).  It is: NO TWO
SOLIDS IN THIS MODULE SHARE A BOUNDARY PLANE, EVER.  Every solid either stands
clear of its neighbour or bites 4 mm INTO it, so along any view ray the
frontmost surface is unambiguous.  That is what these constants are (the face
half of the ladder was retuned in round 7 -- see the note further down):

    y = -.050/-.030   band / capping-slab noses  (relief, stands proud)
    y = -.032         the plinth blocks' MEAN face, 32 mm prouder (the batter)
    y = -.010  FACE   the wall FACE: front of the biggest coursed blocks
    y =  .000         ... their MEAN face: the kit's wall plane
    y = +.020         ... and a small packer's, sat back in its socket
    y =  .044  SKIRT_Y the plane a stone is WIDEST on (round 9)
    y =  .050  MORT_Y the JOINT PLANE: front of the mortar layer
    y =  .066  BLK_Y  block BEDS -- bedded INSIDE the mortar layer, .050-.092
    y =  .140  BED    the core's front face, buried behind the mortar
    y =  .200/.215    backs of band / plinth-cap slabs, buried in the core
    y =  .166  REV_D  back of the dressed reveal liner (>> spec.REVEAL = .10)
    y =  .286/.312    the dark blank that plugs the back of an opening
    y =  .330  CAP_Y1 (unused as a shared plane -- kept for reference)
    y =  .334  SKIM_Y front of the plaster lining
    y =  .338  CORE_Y1 the core's BACK: 4 mm INSIDE the lining, not on its face
    y =  .360  T      the visible inner surface -- the lining and NOTHING else

Horizontal boundaries follow the same rule: a block course bites 4 mm into the
slab above or below it (so no dark stripe AND no shared plane), the core's top
is 4 mm inside the wall-head slab, the skim's top is 4 mm below it.

===========================================================================
ROUND 6, PART 2: ONE COURSE GRID FOR THE WHOLE FAMILY  (the visible seam)
===========================================================================
Shanee: "SM_Wall_StoneWindow_2m next to SM_Wall_StoneArch_2m shows seams in the
connection."  Three separate causes, all of them real:

  1. every piece invented its own course height (.164 / .172 / .176 / .178 /
     .192) and its own field boundaries, so bed lines did not line up across a
     bay seam;
  2. the window wall carried ref3's projecting sill band at 1.05 and the arch
     wall did not, so a 150 mm course simply STOPPED at the seam; and the arch
     wall had NO PLINTH AT ALL while every other piece had one -- a 585 mm tall,
     32 mm deep step that died in mid-air;
  3. blocks lapped the seam and were then cut flat by clamp_to_seams, so each
     seam got TWO half stones with independently jittered tone and relief: a
     continuous vertical line of tonal steps, full height.

So now: ROWS_P / ROWS_A / ROWS_B are computed ONCE, from the range only, and
every piece walls those same courses (masked around its opening).  The plinth
(top .585, cap .085), the sill band (.90-1.05) and the wall head (2.905-3.0)
are on EVERY piece at identical z, identical projection and identical depth --
including the half-height wall, whose coping now lands on a course line.  And
each course lays a SEAM STONE straddling the bay seam, keyed on the course
alone with tint 0: the two halves either side of the seam are the same stone,
same width, same relief, same tone, so they read as one and the seam vanishes.

===========================================================================
ROUND 6, PART 3: THE WINDOW REVEAL
===========================================================================
SM_Win_ArchStone duplicated this wall's arch because the wall's opening was a
flat black plate 30 mm behind the face with a stepped core behind it -- nothing
for an insert to sit in, so the insert brought its own surround.  The WALL owns
the masonry: dressed jambs, a voussoir ring whose inner CHORD (not its corner
radius) is exactly OPENINGS.win_ground/2 so the polygon never eats into the
opening, an oversized keystone, and a sill.  All of it is REV_D = .166 deep --
well past spec.REVEAL -- and the void behind it stays clear to y = .286, so any
insert depth fits.  The window family builds frame + glazing only.

===========================================================================
ROUND 7: STONE SCALE, THE MORTAR JOINT, AND THE CORNER INTERFACE
===========================================================================
Shanee, looking at the assembled inn: seam lines across wall connections, the
corner/end pieces not connecting nicely, "some bricks in walls are a bit too
small at times ... at times there's almost a pattern to it", and "do we need
some texture or colour for the mortar in between?".

  1. STONE SCALE.  0.170 courses with blocks .30-.45 is an aspect ratio of
     1.8:1 to 2.6:1 -- that is a BRICK, and a field of bricks is a pattern by
     construction.  Both references run roughly 1.0-1.5:1 (ref2's corner quoins
     measure ~0.45 long by 0.29 tall).  So COURSE is now .265, which makes the
     ordinary block .28-.44 long, i.e. 1.05-1.7:1, and gives 7 courses from the
     sill band to the wall head instead of 11.  The distribution is WIDER at
     both ends as well -- genuinely big blocks up to .72, real packers down to
     .165 -- and _tall_plan lays blocks that span TWO courses, which is the
     one thing that stops a coursed wall reading as rows at all.
  2. THE MORTAR.  It used to be the dark backing plate showing through a 20 mm
     slot at shade .46: black, flat, and the same black everywhere.  Now the
     joint plane is its own thin layer (MORT_Y / MORT_T) at a shade that
     CATCHES LIGHT, laid as patches whose tone varies course by course, with
     per-joint width variation (JOINT * .70-1.55).  A recessed joint you can
     see the colour of, not a void.
  3. THE SEAM.  Round 6 made the courses continuous and put a seam stone across
     every bay edge, but the dressed HORIZONTALS -- plinth cap, sill band, wall
     head -- still took half a joint each side of the seam, so the three
     strongest lines in the piece were nicked by a dark 16 mm slot every 2 m.
     They now lay a SEAM SLAB straddling the bay edge on exactly the same rule
     as the seam stone.  The mortar patches are keyed on the course and the span
     alone, so they too are the same solid either side of the seam.
  4. THE CORNER.  See corners.py: SM_Corner_StoneQuoin_A/B and
     SM_Corner_StoneInner import this module's course grid, face ladder and
     course_run(), because a quoin that invents its own bed lines and its own
     projection is a different wall stuck on the end of this one.  Everything
     they need is public: BEDS, FACE, PROUD, PLINTH_Z, BAND_Z0, SILL_Z, HEAD_Z,
     SLAB_CAP_Y / SLAB_BAND_Y / SLAB_HEAD_Y, course_run(), mortar_field().

===========================================================================
ROUND 8: THE STONES WERE RECTANGLES
===========================================================================
Shanee: "Let's try and improve the brickwork to be more detailed. It's currently
very much squares of different sizes. I think we need to add some shaping."

Rounds 6 and 7 fixed the SEAMS and the SIZES and never touched the SHAPES, and
that is why the complaint came back. Every stone in the field came out of _one(),
which emitted a p.box(); taper and skew made that box a slightly irregular
QUADRILATERAL, which is as far as a box goes -- four sides, two still parallel,
every corner still 90-ish degrees. So the elevation was one shape scaled, and no
amount of widening BLK_MIN/BLK_MAX could hide it. ref1:stone_base has no
rectangles in it at all. Textures are not available to us, so this is FORM, which
is better anyway: it survives the Solid viewport shading the .blend is judged in.

  1. OUTLINES. `_outline()` draws a stone's FACE as a 4- to 7-sided jittered
     polygon inscribed in the rectangle its bed allots it: corners pulled in
     unequally, one to three of them KNOCKED CLEAN OFF at an asymmetric angle,
     the longest edge often dished by a mid-point, the whole thing tapered or
     sheared and rolled a degree or two. Three shape families are drawn per
     stone (wedge / polygonal boulder / ordinary block) so the eye cannot find
     one silhouette being scaled.
  2. THE ARRIS. `_stone()` extrudes that outline off the bed plane through THREE
     rings, the middle one `chamf` short of the face, so every stone keeps a
     45-degree cut edge all the way round -- the bright arris the old bevel
     bought for 44 tris, now for 6n-4 (32 at n = 6). The whole family came out
     ~14% CHEAPER than the boxes it replaced.
  3. OVERFILL. A polygon gives area back at every corner it cuts, and the first
     cut of this doubled the joints and read as pebbles on tarmac. OVER hands
     that area back, so the wall is TIGHTLY PACKED as the brief asks.
  4. TILT. `_face_plane()` tips two fifths of the stones slightly out of the wall
     plane, half of them forward and half back, so the field is not flush and the
     MEAN FACE IS STILL y = 0. The recess is capped on the run's own shallowest
     relief, so every clearance in the depth ladder above is exactly what it was.
  5. THE SEAM, AGAIN. A polygon cannot be cut by clamp_to_seams (it snaps a
     stray vertex onto the plane and keeps its z and its face depth, which is a
     step, not a cut), so `_clip_u()` cuts the seam stone analytically in
     seam-relative coordinates before it is extruded. Measured after: every
     variant's x = +GRID/2 vertex profile is bit-identical to every variant's
     x = -GRID/2 profile, in front of the mortar layer. The clamp count fell from
     ~330 verts a piece to ~120 (the dressed seam slabs, which are still boxes,
     as dressed ashlar should be), and check_zfight went from 25 cm2 to 0.
  6. AND THE SPLIT STONE. `_fill`'s wide-slot split used to halve the slot's
     HEIGHT and keep its full length, i.e. turn a 400 x 230 slot into two 4:1
     SLATS -- invisible while they were boxes and glaring once they had outlines.
     It now splits the slot's LENGTH first: one full-height stone and a stack of
     two small squarish ones wedged beside it, which is ref1's "big stones at the
     bottom, smaller ones packed into the gaps".

===========================================================================
ROUND 9: THREE STYLES, A DOMED STONE, AND A JOINT THAT PACKS AT 10%
===========================================================================
Shanee, on the assembled .blend: "Brickwork still needs work (although it is
better, but I think sometimes the stones look bulky/square/polygonal and have a
lot of gap in-between at times which might not make much sense?)"  And, given
that ref1's stones are rounded cobbles: "some are rounded/cobbles, not all. It'd
be good to have variation of wall styles for different masonry styles."

  1. THREE STYLES, NOT ONE (see STYLES). Rounds 7 and 8 each read the complaint
     as "the one style is wrong" and re-tuned the one style. The kit needs
     several: cobble (ref1's rounded, near-equant, tightly packed river stone --
     the one that was missing), rubble (what this family has always built), and
     dressed ashlar (ref3's squared blocks, where REGULARITY IS THE MATERIAL, not
     the round-7 pattern defect). SM_Wall_StoneCobble_2m_A/B and
     SM_Wall_StoneAshlar_2m_A are new; every existing piece keeps its name.
     What no style may change: the course grid, the plinth, the sill band, the
     wall head, the face ladder and the seam rule. A style is a stone SHAPE, a
     joint width, a size distribution and a tone mix -- so any two of them stand
     side by side with no step, which the demo now deliberately shows.
  2. THE STONE IS A CUSHION, NOT A PLATE (see _stone). Round 8's stone was an
     outline extruded to a FLAT face with a 45-degree arris: measured on the
     render, the median stone's whole front relief was 6.3% of its width and the
     face was one plane by construction. It is now a SKIRT (the outline carried
     out to SKIRT_Y, in front of the mortar), a SHOULDER and an off-centre CROWN
     on the face ladder: median dome rise 16.5% of the stone's width, p90 25%,
     and not one stone in the family holds 85% of its face in a single plane.
     Two triangles a stone more than the plate it replaces.
  3. THE JOINT IS THE CELL'S JOINT, AND NOTHING ELSE (see SKIRT_Y and _one).
     What the eye read as the edge of a stone used to be neither its cell nor its
     outline: the arris cut 14 mm in from the outline, the outline was drawn
     14 mm OVERSIZE to win that area back, the roll was paid for with another
     5 mm a side, and the bedding jitter with 5 more. Measured, the drawn joint
     was 14-21% of a stone width against the reference's 10, AND the oversize
     still bought 7-9 interpenetrating pairs a piece (found with a BVH, worst
     30 mm, 45 mm of it in front of the joint plane). Now the widest section of
     every stone is its cell, in front of the mortar; the joint is JOINT and the
     concavities a hand-cut outline gives back. Measured after: 11-15% on the
     rubble, 15-16% on the cobble (a rounded stone's median chord is narrower
     than its width, so that number flatters the joint), 7% on the ashlar,
     coverage .94-.97, and ZERO overlapping pairs -- by a BVH self-overlap test
     and by slicing every stone at the joint plane and in front of it.
  4. AND THE STONES ARE FINER. COURSE .265 -> .232: "bulky" is a size complaint
     as well as a shape one, the reference's stones are nearer 250 mm than 360,
     and a dome is a fraction of the stone it sits on. The median stone measures
     ~285 x 210 (cobble ~215 x 195) against the chimney's ~190, so the stack
     still reads FINER than the wall it rises from, which is the way round it
     has to be.

===========================================================================
ROUND 10/11: THE JOINT AT 10%, A ROUND COBBLE, AND THE Z-FIGHT FINISHED
===========================================================================
Three measured faults came back off the assembled .blend, and two of them are
the same decision seen twice.

  1. THE COBBLE READ AS "squared octagonal tiles, not rounded", and its BED
     joints drew 14.4% of a stone height where the reference packs at 10. Those
     pull opposite ways only while the outline ring is INSCRIBED in its cell: a
     rounder corner hands its area to the joint, so round 10 bought its packing
     by squaring the curve into a squircle. `infl` (see _round_outline) breaks
     the trade -- the ring is scaled PAST circumscription, the clamp turns the
     overshoot at the four axes into the short flats a bedded stone beds on, and
     the corners keep whatever curve `e` draws. So `e` went ROUNDER (.56-.74 ->
     .78-.98, i.e. |u|^2.0-2.6, an ellipse to a hair) and the give-back still
     halved: measured over 400 outlines, 5.7% -> 3.2% of a half-extent, coverage
     .869 -> .90. Eleven chords instead of nine were the other half of the bed
     joint, and 10 with `infl` 1.16 is where it settled.
  2. THE STONE WAS STILL A PLATE WITH A CHAMFER, because two rings can only give
     two slope zones and in flat-shaded Solid viewport a face's tone IS its
     slope. `_stone` takes `rings` now: the cobble carries two shoulder rings on
     a spherical profile (three zones -- a rolled rim, a shoulder, a small cap,
     consecutive zones 28 and 11 degrees apart, both inside spec.SMOOTH_ANG), and
     it is PAID FOR by ring 0 becoming a POINT. That back cone closes the shell
     -- which round 9's open bed ring never was -- for n FEWER triangles than the
     open version cost, so the rubble and the ashlar came out ~15% cheaper than
     they were while the cobble got its dome.
  3. AND THE Z-FIGHT REGRESSION IS FINISHED. 3104 -> 437 -> 22 -> 0 cm2. The
     last pair was a stone's skirt underside -- a dead-horizontal facet wherever
     an outline had been clamped flat -- 6.5 mm above the top face of the plinth
     cap it beds on. check_zfight buckets a face by its normal ROUNDED TO TWO
     DECIMALS and then compares n.centre, so two +Z faces whose normals differ by
     the .01 p.wobble puts on a 95 mm facet can differ by a centimetre of
     n.centre over a 1 m lever arm and read as coincident 6.5 mm apart. Widening
     the bed joint would have cleared it and would have put the wall's first
     course 10 mm off the bed line corners.py lays its quoins on. The bed POINT
     clears it instead: every facet of a back cone rakes, so none of them is in
     the same bucket as a dressed slab's top face at all.

===========================================================================
ROUND 12: THE COBBLE IS ROUND BECAUSE IT IS BUILT ROUND, NOT TUNED ROUND
===========================================================================
"Cobble style reads as squared octagonal tiles, not rounded -- the cobble style
is the one that should be roundest, per ref1", for the third round running. It
kept coming back because rounds 9, 10 and 11 all drew the outline the SAME WAY
-- a superellipse ring, `sides` vertices spread evenly round it, every vertex
clamped into the cell -- and then fought the packing/roundness trade with `e`
(corner sharpness) and `infl` (how far past circumscription the ring is scaled).
The arithmetic says that fight cannot be won. At sides = 10, e = .88 and
infl = 1.16 the ring is scaled 1.219, so the vertex at 0 deg lands at 1.219 bu
AND the vertex at 36 deg lands at 1.011 bu: BOTH clamp to u = bu, and the
outline between them is a dead straight vertical edge running 76% of the
half-height. Same at all four axes. That is an octagon -- not because the curve
drawn was square, but because the clamp ate three quarters of it, and the clamp
is not optional (it is what makes overlap impossible).

So `_round_outline` stops drawing a curve that has to be clamped and draws the
CELL WITH ITS CORNERS TAKEN ROUND instead -- flats first, arcs second, which is
what a bedded cobble is: flat where it beds against its neighbour, round where
three stones meet and there is nowhere to bed. Each corner is a quarter ELLIPSE
of radii (f*bu, f*bv) with `arc` interior points; `f` is drawn per corner, so
one stone comes out nearly round and the next keeps a squarer shoulder; one
corner in five is a single chord (split, not worn) and one in five is left
nearly square. The give-back is then exactly (1 - pi/4) f^2 = .2146 f^2 of the
cell whatever the aspect ratio, so PACKING IS ARITHMETIC rather than a tuning
problem:  f = .53 keeps 94% of the cell, f = .80 keeps 86%, f = 1.0 is a full
ellipse at 78.5%. `fill` sets it directly and roundness costs what it costs.

Measured, cobble A: fill (.66, .96) drew a wall of pebbles scattered in lime --
coverage 75.6%, joint 22% -- and fill (.44, .74) lands on coverage 84.9% and
9.0/10.4%, i.e. THE SAME PACKING round 11's clamped superellipse managed (85.3%,
9.2/9.6) with a two-chord arc on every corner instead of a 45 deg chamfer. Cost:
12-vertex outlines against 10, and the cobble pieces run 4794/4918 tris of the
5200 budget.

The chimney family's _cobble was rebuilt on exactly the same construction in the
same round, at its own scale -- one quarry, one mason, and one place to look
when the next note about the stones arrives.

A NOTE ON HOW THE JOINT IS MEASURED, because two rounds have now been spent
chasing a number that was an artefact of the gauge. Raycast each piece's face on
a 1.5 mm grid, split every scanline into stone runs and joint runs, and compare
median against median. What a hit is CLASSIFIED by decides the answer: a depth
threshold set anywhere in front of the mortar plane counts the outer few
millimetres of every stone's shoulder as joint and reads ~19% on a wall that
draws 9. So classify by the MATERIAL of the face the ray lands on, with the
mortar body tagged for the measurement -- then the geometry can stay exactly as
it ships, p.wobble and all, and "joint" means "you can see lime here".

Measured that way, as shipped:
    rubble A  9.0% across / 11.0% up  cover 85.2%   cobble A 9.0 / 10.4  84.9%
    rubble B 11.8 / 9.9  84.9%                      cobble B 8.8 / 11.8  84.5%
    rubble C 11.3 / 8.5  80.3%                      ashlar A 8.8 / 8.4   86.9%
    window   10.7 / 9.4  87.5%   arch 10.5 / 8.5    plinth  11.3 / 8.2   89.4%
    check_zfight: 0 cm2, every piece
    stone-vs-stone volume overlap (a BVH per stone, every pair): 0, every piece
    drawn stone 201 x 202 mm (cobble) / 250 x 204 (rubble), against the chimney
    family's 144-234 x 159-182 -- the stack still reads finer than the wall.

What survives from earlier rounds, because the reference has it too:
  * value variation in PATCHES (`_blotch`), damp at grade, bleached in the sun
  * greenery lives in props/, so a level artist chooses where the moss goes
"""
import bpy
from math import sqrt, sin, cos, pi, atan2, acos, degrees, radians
from mathutils import noise as _nz
from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "stone_walls"
COLLECTION = "01_Walls_Stone"

T = S.T_STONE
H = S.H_GROUND
G = S.GRID
HX = G / 2
SEAMS = dict(x=(-HX, HX), y=(0, T), z=(0, H))

# ------------------------------------------------------------ depth ladder ---
BITE = .004           # how far one solid buries into the next. Never 0: two
                      # solids that BUTT share a plane, and a shared plane is
                      # exactly what the renderer cannot order. 4 mm is enough
                      # only between two big plates whose corners sit ON the snap
                      # planes, where p.wobble() fades to nothing.
LAP = .016            # ...and this is the bite for everything else. A small
                      # solid in the middle of the wall samples the wobble field
                      # at its own corners, so its planes drift several mm
                      # against the big plate it is buried in; 4 mm there closes
                      # and the pair fights again. Measured, not guessed.
SPLIT_Y = .012        # y offset between the two halves of a split core
SKIM_T = .026         # plaster lining thickness
SKIM_Y = T - SKIM_T   # .334  front of the lining
CORE_Y1 = SKIM_Y + BITE       # .338  core back, 4 mm INSIDE the lining
CORE_Y2 = CORE_Y1 + SPLIT_Y   # .350  the second half of a split core
# ------------------------------------------------------------- face ladder ---
# THE FOUR PLANES THE WHOLE FAMILY SHARES, and corners.py with it. A piece that
# invents its own number here is a piece that shows a step where it meets its
# neighbour, which is the whole of Shanee's "seam lines across wall connections".
PROUD = .076          # a wall block's relief at _relief's top of range. ROUND 9
                      # deepened it BY EXACTLY what it deepened the joint plane
                      # by, so FACE is the number it always was: what the extra
                      # 16 mm buys is DOME (see _stone), not a prouder wall.
BLK_Y = .066          # block BEDS -- every block, every piece, every course.
                      # The bed is buried in the mortar layer; what the eye reads
                      # as the edge of a stone is its WIDEST SECTION, which
                      # _stone now stands at SKIRT_Y, in front of the mortar.
FACE = BLK_Y - PROUD  # -.010  UNCHANGED ACROSS ROUNDS 7-9, and it must be:
                      # corners.py stands its quoins Q_PROUD in front of this
                      # number, so a millimetre here is a step at every quoin in
                      # the kit. _relief spreads the crowns from here back to
                      # about +.011, so the MEAN crown is still y = 0.
PROUD_PL = .108       # plinth relief: mean crown -.036 (the batter), proudest
                      # -.048, i.e. just inside the plinth cap's own -.050 nose.
                      # (Not BLK_Y + .048: RL_PLINTH's mean factor is ~.935, so
                      # the nominal depth has to be divided by it or the whole
                      # plinth sits back out of its cap.)
MORT_Y = .050         # THE JOINT PLANE: the front of the mortar layer.
                      # ROUND 9 MOVED IT BACK 20 MM, and that one number is what
                      # pays for the dome. A stone's crown is pinned by the face
                      # ladder (FACE = -.010); its WIDEST section has to sit in
                      # FRONT of the mortar, or the joint opens up by however
                      # much the flank has already tapered by the time it crosses
                      # the mortar plane (see _stone). The gap between those two
                      # planes IS the dome -- so at MORT_Y = .030 the deepest
                      # dome the ladder could hold was 35 mm on a 360 mm stone,
                      # i.e. 10%, which is a plate with a lip, which is what
                      # Shanee is looking at. At .050 it is 54 mm on a 290 mm
                      # stone: 19%, the same figure the chimney measures, and the
                      # joint reads as the SHADOW where two shoulders meet rather
                      # than as a gap with a lit floor at the bottom of it.
MORT_T = .042         # mortar layer thickness -- thick enough to SWALLOW every
                      # block bed (BLK_Y = .062 lands inside .050-.096, and
                      # inside .054-.096 on the deeper parity, so a block bed at
                      # .066-.072 has 12 mm of clear lime in front of it and 20
                      # behind. THOSE TWO MARGINS ARE MEASURED, NOT CHOSEN: the
                      # first cut of round 9 left 2 mm in front, and check_zfight
                      # found 900 cm2 of the mortar front against the block beds
                      # on one piece -- p.wobble displaces a 1 m mortar patch by
                      # up to 5 mm at its corners and a 200 mm stone by 5 mm at
                      # its own position, so anything under ~10 mm of designed
                      # separation is inside the noise. Round 7 measured the same
                      # threshold from the other side (568 cm2 at 4 mm, clean at
                      # 10).
MORT_CLR = .012       # ROUND 10, AND THIS IS THE Z-FIGHT REGRESSION, MEASURED.
                      # How far a mortar patch's own faces must stand clear of
                      # the nearest STONE face, in the plane of the wall.
                      #   Round 9 ran the patch LAP*.55 = 8.8 mm past its course's
                      # bed lines while the course above started its stones at
                      # joint/2 = 8.0 mm past the same line. That is 0.8 mm of
                      # designed separation between the patch's horizontal top
                      # face and the underside of the skirt of every stone in the
                      # course above -- and a stone's skirt IS a horizontal face
                      # wherever its outline was clamped flat, which is most
                      # stones. check_zfight duly found it: 437 cm2 over six
                      # pieces, worst pair 60, every one of them at y = .043-.069,
                      # i.e. between SKIRT_Y and the block beds. The same
                      # arithmetic at a SPAN edge put the patch's side face on
                      # exactly the plane of the first stone's clamped flank
                      # (both at x = +-hw), which is the arch bay's three pairs.
                      #   12 mm is the number this family already measured twice
                      # for a stone against the lime it is bedded in (see MORT_T);
                      # p.wobble displaces a 1 m patch and a 200 mm stone by up to
                      # 5 mm each, so anything under ~10 is inside the noise.
MORT_XPAD = .024      # ...and how far it runs past a SPAN edge, where 12 mm is
                      # not available: the patch would land 5.6 mm inside the
                      # dressed jamb's own outer face, which is the same fault
                      # again one solid further in. At 24 the patch's side face is
                      # 17.6 mm inside the jamb, and the jamb is 155-205 mm thick,
                      # so it cannot reach the reveal. Capped at half the distance
                      # to the bay centre so the two spans of one course can never
                      # meet (an opening's crown course leaves only ~50 mm of hw).
MORT_STEP = .004      # ...and how much the alternating patch parity sinks by.
                      # Was .006: the parity comes straight off the block's own
                      # burial, and 8 mm is the least this family has ever run.
MORT_SHADE = .68      # ...and its tone. Lifted from .70 along with the recess:
                      # the joint is 60 mm deep now and self-shadowing, so the
                      # surface at the bottom of it has to be a lighter grey than
                      # before to read as lime rather than as a void. (The
                      # chimney reaches the same place from the other side --
                      # `stone` at .60 behind a shallower recess.)
WOB = .005            # hand-hewn wobble amplitude, family-wide
NOISE_SEED = 20240823 # ...and the seed the noise field it rides on is PINNED to.
                      # THE SAME NUMBER timber_walls uses, deliberately: this is
                      # a kit-wide bug, not a family one. mathutils.noise is
                      # seeded PER BLENDER PROCESS, and both Part.wobble (which
                      # displaces by noise_vector) and _blotch (which picks the
                      # tone patches) read it -- so "same code, same mesh" was
                      # false for this family in the loudest possible way:
                      # measured, two builds of identical code differed by up to
                      # 289 mm and did not even agree on the vertex count, and a
                      # rebuild would not reproduce the .blend Shanee is looking
                      # at. Seeded, every piece here is byte-for-byte
                      # reproducible across processes. The proper home for this
                      # is util.Part.wobble, which a piece module may not edit.
BED = .140            # core FRONT. IT MOVED BACK 60 MM IN ROUND 9, and the two
                      # dressed slabs moved with it (see SLAB_BAND_Y), because
                      # the mortar layer in front of it got 20 mm thicker and the
                      # separations here are not free: p.wobble displaces a 2 m
                      # core plate by up to 5 mm AT ITS FOUR CORNERS, which is a
                      # rigid plane, while it displaces a 1 m mortar patch by the
                      # local field -- so two big parallel plates need ~20 mm of
                      # designed separation, not the 8 mm that is plenty between
                      # a stone and the lime it is bedded in. Measured: at 8 mm
                      # check_zfight found 2600 cm2 of core against mortar on one
                      # piece. The ladder now reads mortar .050-.092, block beds
                      # .066-.072, core .140-.338, and the slab backs at .200 and
                      # .215, i.e. 12 / 20 / 48 / 60 mm apart. Nothing sees the
                      # core; it can be anywhere that is clear of its neighbours.
BED2 = BED + SPLIT_Y  # .092  ditto, second half of a split core
REV_D = .166          # back of the dressed reveal liner (spec.REVEAL = .10)
BLANK_Y = (.286, .312)   # the dark blank plugging the back of an opening
CLR = .016            # how far the core's void is inflated past the liner, so
                      # the liner owns the reveal surface on its own
CORE_SHADE = .30      # the deep core. Nothing ever sees it; the mortar does.

SKIRT_Y = MORT_Y - .006   # .044 THE PLANE A STONE IS WIDEST ON, and this is
                      # round 9's answer to "a lot of gap in-between at times".
                      # A stone is a skirt, a shoulder and a crown: the skirt
                      # carries its outline -- the whole cell, undiminished --
                      # from the bed plane out to HERE, 6 mm in front of the
                      # shallowest mortar patch, and only then does the shoulder
                      # begin to draw in. So the section the eye reads as the
                      # edge of the stone IS its cell, and the drawn joint is the
                      # joint the course laid out and nothing else. Before this,
                      # the widest VISIBLE section was wherever the flank
                      # happened to cross the mortar plane, which cost 15-20 mm a
                      # side and so doubled every joint in the family.

JOINT = .0105         # MEAN joint between two CELLS in a course -- and now that
                      # a stone fills its cell out to SKIRT_Y, very nearly what
                      # gets drawn. Every joint is this x .72-1.44, because a
                      # wall whose joints are all one width is a grid however
                      # irregular the stones are.
                      # THE SIZE: ref1's cobbles pack at roughly a tenth of a
                      # stone width. ROUND 10 measured what actually gets DRAWN,
                      # by raycasting the face on a 1.5 mm grid and splitting
                      # every scanline into stone runs and joint runs: the rubble
                      # drew 33-34 mm against a 285 mm stone (12%) and 28 mm
                      # between beds (14%), so the nominal 16 was already only
                      # half of it -- the rest is what a hand-cut outline gives
                      # back at its corners. 12 mm nominal, with the corner
                      # knocks and the bedding jitters trimmed to match, draws
                      # 25-28 mm: 9-10% across and 11-12% up.
JOINT_PL = .0105      # the plinth's blocks are bigger and tighter
JOINT_BEV = .26       # PUBLIC (corners.py cuts its quoin arris with it). It used
                      # to size this family's chamfer too; the chamfer is gone --
                      # a stone's arris is its shoulder now.
COURSE = .232         # THE course height. ROUND 9 brought it down from .265:
                      # Shanee reads the stones as "bulky", the reference's are
                      # nearer 250 mm than 360, and a dome is a fraction of the
                      # stone it sits on -- the same 50 mm of relief that is 19%
                      # of a 290 mm stone is 14% of a 360 mm one. Blocks run
                      # 1.0-1.6:1 on the course, eight courses from the sill band
                      # to the wall head, and the median stone measures about
                      # 290 x 210 against the chimney's 190 x 175 -- so the stack
                      # still reads FINER than the wall it rises from, which is
                      # the way round it has to be.
BLK_MIN, BLK_MAX = .140, .620     # the bulk of the blocks run .23-.38, with
                                  # real outliers at both ends

# How far the crowns in a run spread, as (lo, hi) of _relief's ramp and (lo, hi)
# of the per-block die on top of it. NARROWER than round 8's (.55, 1.12, .86,
# 1.14): the facing used to have to shade itself out of the spread between one
# stone's bedding depth and the next's, because every face was flat. Every stone
# now carries 40-54 mm of dome, which shades far harder than a 30 mm step between
# two plates ever did -- so the spread comes in to 23 mm, which keeps every crown
# inside the ladder (proudest -.012, mean 0) and leaves the shading to the shape.
RL_WALL = (.70, .98, .94, 1.05)
RL_PLINTH = (.86, 1.02, .96, 1.03)

# ---------------------------------------------------------- the course grid --
PLINTH_Z = .585       # top of the plinth -- IDENTICAL on every piece
PLINTH_CAP = .085     # its chamfered cap
BAND_H = .150         # the sill string course
SILL_Z = S.OPENINGS["win_ground"]["sill"]      # 1.05 -- band top = window sill
BAND_Z0 = SILL_Z - BAND_H                      # .90
HEAD_H = .095
HEAD_Z = H - HEAD_H                            # 2.905 -- wall-head course

# The three dressed horizontals, as (nose, back). PUBLIC: corners.py returns the
# same projection round the corner, or the string course visibly steps at it.
# ROUND 9 MADE THEM DEEPER (the backs, never the noses): the core's front face
# had to move back to clear the thicker mortar layer, and at .110 / .140 the two
# slab backs were the planes it collided with. A dressed slab's back is buried in
# the core either way -- what matters is the NOSE, which is what corners.py
# matches to turn the string course round an arris, and those are unchanged.
SLAB_CAP_Y = (-.050, .215)     # plinth cap
SLAB_BAND_Y = (-.030, .200)    # sill string course
SLAB_HEAD_Y = (-.040, T)       # wall head


def _grid(z0, z1, course=COURSE, jitter=.075):
    """Course boundaries for a band of walling. Deterministic on the RANGE
    ALONE -- never on the piece -- so every piece in the family that walls the
    same band gets the same bed lines and two variants can sit side by side."""
    r = rng(f"sw/grid/{z0:.4f}/{z1:.4f}/{course:.3f}")
    n = max(1, int(round((z1 - z0) / course)))
    hs = [1.0 + r.uniform(-jitter, jitter) for _ in range(n)]
    k = (z1 - z0) / sum(hs)
    out, z = [], z0
    for h in hs:
        out.append((z, z + h * k))
        z += h * k
    return out


ROWS_P = _grid(0.0, PLINTH_Z - PLINTH_CAP, .250)   # 2 big plinth courses
ROWS_A = _grid(PLINTH_Z, BAND_Z0, .315)            # 1 course under the band
ROWS_B = _grid(SILL_Z, HEAD_Z)                     # 7 courses to the head

# Every bed joint in the family, bottom to top. PUBLIC: this is the list a
# corner piece has to land its blocks on, and the only way to be sure it does is
# to read it from here rather than to divide a storey by a course height of its
# own. (PLINTH_Z and SILL_Z are the tops of the cap and the band.)
BEDS = tuple(sorted({0.0}
                    | {z for r in ROWS_P for z in r}
                    | {PLINTH_Z}
                    | {z for r in ROWS_A for z in r}
                    | {BAND_Z0, SILL_Z}
                    | {z for r in ROWS_B for z in r}
                    | {HEAD_Z, H}))


# --------------------------------------------------------------- ingredients --
def _relief(l, depth, rl=RL_WALL):
    """How far a block stands out of the bed. Longer stones sit prouder and land
    on (or just past) the FACE plane; a small packer sits back in its socket.

    THE SPAN OF THIS IS THE WHOLE DIFFERENCE between a rubble wall and stone
    tile cladding. At lerp(.68, 1.0) every face in the piece landed inside a
    9 mm band, so the facing was one plane with lines drawn on it, the joints
    never fell into shadow, and no stone ever cast onto its neighbour. .55-1.12
    spreads the faces over ~30 mm -- still nothing like a boulder heap, but
    enough that the wall shades itself. See RL_WALL / RL_PLINTH."""
    return depth * lerp(rl[0], rl[1], clamp((l - .17) / .36))


# ------------------------------------------------------- stone silhouettes ----
# ROUND 8: THE STONES WERE RECTANGLES.
#
# Shanee: "Let's try and improve the brickwork to be more detailed. It's
# currently very much squares of different sizes. I think we need to add some
# shaping." He is right, and it was structural rather than a matter of dice: the
# whole field came out of _one(), which emitted a p.box(). `taper` and `skew`
# turned that box into a slightly irregular QUADRILATERAL, which is as far as a
# box goes -- four sides, two of them still parallel, every corner still 90-ish
# degrees. Round 7 spent all its effort on stone SIZES (BLK_MIN/BLK_MAX,
# _lengths' three humps, _tall_plan) and none at all on stone SHAPES, so the
# elevation read as ONE SHAPE SCALED, which is the "almost a pattern" complaint
# coming back in different words.
#
# Look at ref1:stone_base: there is not a rectangle in it. Five-, six- and
# seven-sided faces, corners knocked clean off, no two edges parallel, small
# stones wedged into the gaps the big ones leave, and faces sitting at slightly
# different angles to the wall so the field is not flush. The linked reference
# thread does all of that with a procedural texture; we have no textures, so it
# has to be FORM -- which is better anyway, because form is the only kind of
# detail that survives the Solid viewport shading Shanee inspects the .blend in.
#
# So a stone is not a box any more:
#   _outline()  draws its FACE as a jittered polygon inscribed in the rectangle
#               its bed allots it -- knocked corners, a dished or bulged long
#               edge, a tapered or sheared silhouette, a degree of roll;
#   _stone()    extrudes that outline off the bed plane with a 45-degree arris
#               all round the face, so a stone keeps the bright cut edge the old
#               bevel gave it and costs LESS than the box it replaces (6n-4 tris
#               at n = 6 is 32, against a beveled box's 44);
#   _face_plane() tips a third of them slightly out of the wall plane, biased so
#               the tip can only ever go the safe way (see its docstring).
#
# The seam stone is the one that could not just be shaped. It straddles a bay
# edge and used to let clamp_to_seams snap whatever crossed the plane, which is
# a clean cut for a box and a MESS for a polygon: a vertex 40 mm past the seam
# snaps onto it and brings its own z and its own face depth with it, so the two
# halves stop agreeing at the joint and every course grows a few-mm step, every
# 2 m, exactly the seam round 6 and round 7 were spent killing. _clip_u()
# therefore cuts the outline against the seam plane ANALYTICALLY, in
# seam-relative coordinates, before it is extruded -- both pieces clip the same
# polygon on the same plane, so the vertices on the cut are bit-identical and the
# two halves are one stone. Nothing there needs clamping at all any more.
TILT = .012           # how far a tilted stone's crown leaves the wall plane.
TILT_P = .40          # ...and the fraction of stones that tilt. A whole field of
                      # tilted faces reads as damage; a third of them reads as a
                      # wall nobody had a set square for. Half tip out and half
                      # tip back (see _tilt), so THE MEAN CROWN IS STILL y = 0 --
                      # the plane corners.py matches and the whole face ladder is
                      # measured from. Tipping them all one way would move the
                      # family's face by 5 mm, which is a step against every
                      # quoin in the kit.
LOW_P = .16           # stones that do not fill their bed's full height, leaving
                      # a wedge of mortar over or under them. The cheapest cure
                      # there is for a course reading as a ROW.


# ---------------------------------------------------------------- styles ------
# ROUND 9, FAULT 1: THE KIT NEEDS SEVERAL MASONRY STYLES, NOT ONE.
#
# Shanee, having been told ref1's stones are rounded cobbles: "some are
# rounded/cobbles, not all. It'd be good to have variation of wall styles for
# different masonry styles."  Rounds 7 and 8 read every complaint about the
# brickwork as "the one style is wrong" and re-tuned the one style, which is why
# the note keeps coming back in different words. Three DIFFERENT walls is the
# answer, each internally consistent, each reading as one mason's work:
#
#   cobble   ref1's ground floor. Rounded, near-equant stones off a river bed,
#            packed tight, thin joints, no dressed faces anywhere. The style
#            that was missing.
#   rubble   the middle case, and what this family has always built: roughly
#            levelled beds, hewn irregular stones, big through-stones, the odd
#            boulder, a real spread of sizes.
#   ashlar   ref3's ground floor. Squared dressed blocks, fine regular joints,
#            barely any face relief. REGULARITY IS CORRECT HERE -- it is a
#            different material worked by a different trade, not the "almost a
#            pattern" defect of round 7. (Its quoins belong to corners.py, which
#            reads its beds and its face ladder out of this module, so
#            SM_Corner_StoneQuoin lands on an ashlar bay's own courses.)
#
# WHAT EVERY STYLE SHARES, without exception, because this is what lets a level
# artist put any two of them side by side: the course grid (ROWS_P / ROWS_A /
# ROWS_B), the plinth (PLINTH_Z, PLINTH_CAP), the sill band, the wall head, the
# face ladder (FACE / BLK_Y / SKIRT_Y / MORT_Y) and the seam rule. A style is a
# stone SHAPE, a joint width, a size distribution and a tone mix -- never a bed
# line and never a projection. That discipline is what killed the bay seams in
# round 6 and it does not get to regress for a new look.
#
#   form   how one stone's outline is drawn: "round" (the cell with its corners
#          taken round, i.e. a cobble), "hewn" (a knocked-cornered polygon),
#          "dressed" (a near-rectangle with its corners taken off)
#   rise   the crown's height above the stone's widest section, as a fraction of
#          its SHORT side -- i.e. how domed the face is. Capped by the ladder
#          (SKIRT_Y - crown), so this is a ceiling, not a promise.
#   mid    where the shoulder ring sits, as a scale of the outline. Small = a
#          narrow shoulder and a broad crown; large = a broad rolling shoulder.
#   share  how much of the climb happens ABOVE the shoulder. With mid ~.62 and
#          share ~.40 the shoulder runs 35-55 deg off the face and the crown
#          15-30 deg, i.e. they differ by less than spec.SMOOTH_ANG (34) and
#          shade as ONE CURVE instead of creasing into a lip. That invariant is
#          what the chimney family spent five rounds learning; it is the same
#          shape here.
#   fill   ROUND form only: how round each of the four corners is cut, as a
#          fraction of the stone's own half-extents. The corner is a quarter
#          ellipse, so a stone gives back exactly .2146 * fill^2 of its cell and
#          nothing else -- packing is arithmetic, not a tuning problem. fill 1.0
#          is a full ellipse (78.5% of the cell); fill .53 keeps 94% of it.
#   arc    ...and how many INTERIOR points that quarter ellipse carries. 1 is
#          two chords, i.e. a 12-vertex outline, and it is also the triangle
#          budget: at rings = 2 a stone costs 6 * (verts) tris.
#   chamf  how often a corner is cut as ONE chord instead of an arc: a stone
#          that was split rather than water-worn.
#   rings  how many shoulder rings the dome carries. 1 is a rim band and a
#          broad cap; 2 spreads the same rise over three zones and is what makes
#          a cobble read as a cushion rather than as a chamfered tile.
#   wmid / wlong / wsmall   stone widths, in course heights
STYLES = {
    # ROUND 12, THE COBBLE, AND IT IS A CONSTRUCTION CHANGE (see _round_outline
    # and the header). "Reads as squared octagonal tiles, not rounded" three
    # rounds running, because rounds 9-11 kept re-tuning ONE construction -- a
    # superellipse ring clamped into the cell -- whose clamp turns most of the
    # outline into four straight flats as soon as the ring is scaled far enough
    # to pack. The outline is now the cell with its four corners taken round
    # (`fill`, `arc`, `chamf`), so roundness and packing stop fighting: the only
    # area a stone gives back is .2146 * fill^2 of its cell.
    #   `fill` (.44, .74) is the packing, measured: at (.66, .96) the wall came
    # out as pebbles in lime (coverage 75.6%, joint 22%), and at (.44, .74) it
    # measures 84.9% coverage and 9.0/10.4% -- round 11's packing exactly, with a
    # two-chord arc on every corner instead of a 45 deg chamfer.
    #   `rings` 2 stays: three slope zones is what makes a cobble read as a
    # cushion rather than a plate with a chamfer, and the outline is the same
    # cost either way.
    "cobble": dict(
        form="round", fill=(.44, .74), arc=1, chamf=.20, jit=.09, hard=.20,
        roll=.030, rings=2,
        rise=(.30, .42), mid=(.58, .64), share=.22, ecc=.14,
        wmid=(.82, 1.30), wlong=(1.42, 1.95), wsmall=(.52, .80),
        long=.15, small=.30, split=.30, tall=.44, tall_wide=(.26, .42),
        low=.11, warm=.30, pale=.13, dark=.018, var=.055, tint=.055,
        joint=.005, joint_pl=.005, mort_shade=.64, mort_pale=.15),
    "rubble": dict(
        form="hewn", sides=6, e=(.40, .56), jit=.18, hard=.34, roll=.031,
        rise=(.22, .33), mid=(.62, .72), share=.47, ecc=.13,
        wmid=(1.00, 1.62), wlong=(1.90, 2.65), wsmall=(.58, .95),
        long=.17, small=.17, split=.14, tall=.55, tall_wide=(.30, .52),
        low=.16, warm=.30, pale=.16, dark=.015, var=.055, tint=.055,
        joint=JOINT, joint_pl=JOINT_PL, mort_shade=MORT_SHADE, mort_pale=.17),
    "ashlar": dict(
        form="dressed", sides=5, e=(.70, .85), jit=.10, hard=.10, roll=.012,
        rise=(.07, .12), mid=(.84, .90), share=.34, ecc=.07,
        wmid=(1.30, 1.85), wlong=(2.05, 2.45), wsmall=(.85, 1.15),
        long=.10, small=.10, split=.05, tall=.20, tall_wide=(.34, .50),
        low=.05, warm=.22, pale=.30, dark=.008, var=.038, tint=.040,
        joint=.011, joint_pl=.010, mort_shade=.78, mort_pale=.30),
}


def style(name):
    """PUBLIC: a copy of one style table, so a caller can nudge one field."""
    return dict(STYLES[name])


def _unit(du, dv):
    m = sqrt(du * du + dv * dv)
    return (du / m, dv / m) if m > 1e-9 else (1.0, 0.0)


def _dedupe(poly, eps=8e-4):
    """Drop vertices that landed on top of their neighbour. A zero-length edge
    makes bmesh refuse the whole face, and _emit swallows that -- so the stone
    would simply be missing a side and nobody would be told."""
    out = []
    for q in poly:
        if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > eps:
            out.append(q)
    while len(out) > 3 and (abs(out[0][0] - out[-1][0])
                            + abs(out[0][1] - out[-1][1])) <= eps:
        out.pop()
    return out


def _cell_eps(l, h, roll):
    """The in-plane shrink that pays for a roll.

    NEARLY NOTHING, and that is deliberate. The cell rule is enforced by the
    CLAMP at the end of _outline / _round_outline -- every vertex, unconditionally
    -- so this shrink is not what keeps a stone out of its neighbour; all it buys
    is that a rolled corner is not the vertex the clamp flattens. The first cut of
    round 9 paid 5 mm a side for that, i.e. 10 mm out of every joint in the
    family, which is most of why the measured joint did not come down when the
    nominal one was nearly halved. Four 1 mm flats on a rolled stone cost
    nothing; 10 mm of open joint on every stone costs the whole complaint."""
    return min(.0012, abs(roll) * max(l, h) * .12)


def _outline(r, l, h, clips=(.20, .42, .29, .09), mid=.30, ju=.0045, jv=.0038,
             taper=0.0, flip=False, lean=0.0, roll=0.0, dish=.10):
    """The FACE OUTLINE of one hand-cut stone: a CCW polygon in (u, v), drawn
    inside the l x h rectangle its bed allots it -- AND NEVER OUTSIDE IT.

    clips   distribution over HOW MANY of the four corners get knocked off. A
            chamfered corner is the single cheapest thing that says "cut by
            hand", and it is what the reference's stones are full of.
    taper   narrows the top (or, with `flip`, the bottom) into a wedge
    lean    shears the outline into a parallelogram
    mid     chance the longest edge gains a mid-point, so the stone has an odd
            number of sides and its two long edges are not parallel
    dish    how far that mid-point dents inward, as a fraction of the short side
    roll    roll in the plane of the wall, radians

    ROUND 9: THE CELL RULE, borrowed from the chimney family. Every vertex is
    clamped into the cell rectangle and the roll is paid for in advance
    (_cell_eps), so no stone can reach into its neighbour's cell -- which means
    the joint the course laid out is the joint that gets drawn, and there is no
    overlap left to prevent by reserving space. Round 8 did the opposite: it grew
    the outline by OVER (14 mm) to win back the area a knocked corner gives up,
    and paid for it in 7-9 interpenetrating pairs a piece, measured with a BVH.
    A clamped vertex simply flattens that side, which is what a bedded stone's
    silhouette does anyway."""
    hu, hv = l / 2.0, h / 2.0
    eps = _cell_eps(l, h, roll)
    bu, bv = max(hu - eps, hu * .55), max(hv - eps, hv * .55)
    tu = bu * (1.0 - clamp(taper, 0.0, .15))
    if flip:
        base = [(-tu + lean, -bv), (tu + lean, -bv), (bu, bv), (-bu, bv)]
    else:
        base = [(-bu, -bv), (bu, -bv), (tu + lean, bv), (-tu + lean, bv)]
    ju, jv = min(ju, l * .09), min(jv, h * .10)
    pts = [(bu_ - (1.0 if bu_ > 0 else -1.0) * r.uniform(0.0, 1.0) * ju,
            bv_ - (1.0 if bv_ > 0 else -1.0) * r.uniform(0.0, 1.0) * jv)
           for (bu_, bv_) in base]
    q, acc, k = r.random(), 0.0, len(clips) - 1
    for i, wgt in enumerate(clips):
        acc += wgt
        if q < acc:
            k = i
            break
    order = [0, 1, 2, 3]
    r.shuffle(order)
    knock = set(order[:k])
    # NEVER BOTH ENDS OF A SHORT EDGE, on anything elongated. Knocking the two
    # corners that share a 90 mm end off a 380 x 90 stone cuts them to a point
    # and the stone comes out an ARROWHEAD -- which is what a stack of split
    # halves looked like in the second cut of this, four chevrons in a column,
    # the single most artificial thing in the wall. On a near-square stone there
    # is no short edge to run out of, and three knocked corners there is exactly
    # the polygonal boulder we do want.
    lo_, hi_ = sorted((l, h))
    if hi_ > lo_ * 1.35:
        pairs = ((1, 2), (3, 0)) if l > h else ((0, 1), (2, 3))
        for (i, j) in pairs:
            if i in knock and j in knock:
                knock.discard(j if order.index(j) > order.index(i) else i)
    m = min(l, h)
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
        # ASYMMETRIC ON PURPOSE. Two equal cuts make a 45-degree corner, and a
        # field of stones each with one clean 45-degree corner is just another
        # repeating shape -- it was the most obvious thing about the first cut of
        # this. So the two legs are drawn independently and then one of them is
        # often cut right back, which is what turns "chamfered box" into "the
        # corner came off when they dressed it".
        # ROUND 9: .10-.34 of the short side, not .18-.62. Every millimetre a
        # knocked corner gives up goes to the JOINT, and round 8 gave up so much
        # of it that the field read as tiles laid on a dark board however tight
        # the nominal joint was. A corner cut a third of the way back still says
        # "cut by hand"; one cut two thirds of the way back says "gravel".
        # ROUND 10: .09-.27, measured. A knocked corner gives its area to the
        # JOINT, and the raycast gauge says how much: the rubble's drawn joint
        # was 33 mm on a 285 mm stone against a 16 mm nominal, so 17 of it came
        # out of the outline. Trimming the legs by a fifth and halving the
        # corner jitter (ju/jv below) takes ~5 mm of that back without touching
        # what the knock is FOR, which is that the corner reads as cut by hand.
        s_i = r.uniform(.10, .31) * m
        s_o = r.uniform(.10, .31) * m
        if r.random() < .42:
            s_i, s_o = ((s_i * r.uniform(.22, .55), s_o) if r.random() < .5
                        else (s_i, s_o * r.uniform(.22, .55)))
        s_i, s_o = min(s_i, li * .32), min(s_o, lo * .32)
        out.append((c[0] - din[0] * s_i, c[1] - din[1] * s_i))
        out.append((c[0] + dout[0] * s_o, c[1] + dout[1] * s_o))
    out = _dedupe(out)
    if mid > 0.0 and len(out) <= 6 and r.random() < mid:
        n = len(out)
        j = max(range(n), key=lambda i: (out[(i + 1) % n][0] - out[i][0]) ** 2
                                        + (out[(i + 1) % n][1] - out[i][1]) ** 2)
        a, b = out[j], out[(j + 1) % n]
        du, dv = b[0] - a[0], b[1] - a[1]
        nu, nv = _unit(-dv, du)          # inward normal of a CCW outline
        s = r.uniform(-.34, .70) * dish * m
        t = r.uniform(.36, .64)
        out.insert(j + 1, (a[0] + du * t + nu * s, a[1] + dv * t + nv * s))
    if roll:
        ca, sa = cos(roll), sin(roll)
        out = [(u * ca - v * sa, u * sa + v * ca) for (u, v) in out]
    return _dedupe([(clamp(u, -hu, hu), clamp(v, -hv, hv)) for (u, v) in out])


def _round_outline(r, l, h, sides=12, fill=(.66, .96), jit=.09, hard=.20,
                   roll=0.0, arc=1, chamf=.22, e=None, infl=None):
    """A COBBLE'S outline: THE CELL, WITH ITS FOUR CORNERS TAKEN ROUND.

    ROUND 12, AND IT IS A DIFFERENT CONSTRUCTION RATHER THAN ANOTHER RETUNE.
    "Cobble reads as squared octagonal tiles, not rounded -- the cobble style is
    the one that should be roundest, per ref1", for the third round running. It
    kept coming back because rounds 9-11 all drew the outline the same way -- a
    superellipse ring, `sides` vertices spread evenly round it, every vertex
    clamped into the cell -- and then fought the packing/roundness trade with
    `e` (the corner sharpness) and `infl` (how far past circumscription the ring
    is scaled). Those two pull against each other, and the arithmetic says the
    fight was unwinnable:

        with sides = 10, e = .88 and infl = 1.16 the ring is scaled 1.219, so
        the vertices at 0 deg AND at 36 deg BOTH land past u = bu and are both
        clamped to it. The outline between them is therefore a DEAD STRAIGHT
        VERTICAL EDGE running 76% of the half-height, and the same at all four
        axes. That is an octagon -- not because the curve was square, but
        because the clamp ate three quarters of it. Measured off the render, it
        is exactly what the note describes.

    The clamp is not optional (it is what makes overlap impossible), so the
    answer is to stop drawing a curve that has to be clamped. A bedded cobble is
    its cell with the corners knocked round: FLAT where it beds against its
    neighbour, ROUND where three stones meet and there is nowhere to bed. So the
    outline is now built the other way about -- flats first, then arcs:

      * each corner is a quarter ELLIPSE of radii (f*bu, f*bv), drawn with
        `arc` interior points, so it is a real arc and not one 45 deg chamfer;
      * `f` is drawn PER CORNER, so one stone comes out nearly round and the
        next keeps a squarer shoulder, and `hard` leaves one corner of one stone
        in five nearly square (a broken face);
      * between two corners the outline runs straight along the cell edge, hard
        against the plane its neighbour is bedded to -- so the joint there is
        the joint the course laid out and nothing else;
      * `chamf` cuts one corner in five as a single chord instead of an arc,
        which is what a stone that was split rather than worn looks like.

    THE PACKING IS NOW ARITHMETIC RATHER THAN A TUNING PROBLEM. The only area a
    stone gives back is the four corner segments, which is exactly
    (1 - pi/4) f^2 = .2146 f^2 of the cell, whatever the aspect ratio:

        f = .60  ->  92.3% of the cell        f = .85  ->  84.5%
        f = .70  ->  89.5%                    f = 1.00 ->  78.5%  (a full ellipse)

    so `fill` sets the packing directly and roundness costs what it costs and
    nothing more. At fill (.66, .96) the mean stone keeps ~87% of its cell, which
    is better packing than round 11's clamped superellipse managed (85.3%
    measured) while the corner is a two-chord arc instead of a chamfer.

    Every vertex is still inside the cell by construction and clamped to it
    afterwards, so no stone can reach into its neighbour -- the invariant that
    makes the joint the course laid out the joint that gets drawn.

    `e` and `infl` are accepted and ignored: they were the superellipse's knobs
    and callers (and the style table) may still name them."""
    hu, hv = l / 2.0, h / 2.0
    eps = _cell_eps(l, h, roll)
    bu, bv = max(hu - eps, hu * .55), max(hv - eps, hv * .55)
    k = max(1, int(arc))
    fs = [clamp(r.uniform(*fill) * (1.0 + r.uniform(-jit, jit)), .10, 1.0)
          for _ in range(4)]
    if r.random() < hard:
        fs[r.randrange(4)] *= r.uniform(.16, .42)
    flat = r.randrange(4) if r.random() < chamf else -1
    out = []
    for i in range(4):
        su = 1.0 if i in (0, 1) else -1.0
        sv = -1.0 if i in (0, 3) else 1.0
        ru_, rv_ = fs[i] * bu, fs[i] * bv
        cu_, cv_ = su * (bu - ru_), sv * (bv - rv_)
        t0 = -pi / 2 + i * (pi / 2)
        m = 1 if i == flat else k + 1
        for s in range(m + 1):
            a_ = t0 + (pi / 2) * (s / m)
            g = 1.0
            if 0 < s < m:
                # only the INTERIOR of an arc is jittered. The two tangent points
                # are where the outline meets the cell edge, and moving them is
                # moving the joint.
                a_ += (pi / 2) * r.uniform(-.13, .13) / m
                g = 1.0 - r.uniform(0.0, jit * .55)
            out.append((cu_ + ru_ * cos(a_) * g, cv_ + rv_ * sin(a_) * g))
    if roll:
        ca, sa = cos(roll), sin(roll)
        out = [(u * ca - v * sa, u * sa + v * ca) for (u, v) in out]
    return _dedupe([(clamp(u, -hu, hu), clamp(v, -hv, hv)) for (u, v) in out])


def _shape(r, sty, l, h, seam=False):
    """One stone's outline, in the style's own hand. `seam` drops the mid-point
    dish: _clip_u wants a convex outline and a dished edge is not worth a special
    case on the one stone per course that has to come out identical on two
    different meshes."""
    f = sty["form"]
    rl_ = r.uniform(-1, 1) * sty["roll"]
    if f == "round":
        return _round_outline(r, l, h, fill=sty["fill"], jit=sty["jit"],
                              hard=sty["hard"], roll=rl_,
                              arc=sty.get("arc", 1), chamf=sty.get("chamf", .22))
    if f == "dressed":
        # A DRESSED BLOCK IS ALLOWED TO BE A RECTANGLE. Its corners are pulled in
        # by a couple of millimetres and one of them is often taken off, but the
        # regularity is the material -- see the note on STYLES["ashlar"].
        return _outline(r, l, h, clips=(.58, .36, .06, .0),
                        mid=0.0 if seam else .18, ju=.005, jv=.004,
                        taper=r.uniform(0.0, .030), flip=r.random() < .5,
                        lean=r.uniform(-1, 1) * .004, roll=rl_, dish=.030)
    q = r.random()
    if q < .17:            # a WEDGE: one end of it frankly narrower
        clips, mid, tp, dish = (.34, .46, .20, .0), .20, r.uniform(.08, .19), .05
    elif q < .36:          # a polygonal BOULDER: most of its corners off
        clips, mid, tp, dish = (.0, .06, .38, .56), .38, r.uniform(0.0, .07), .09
    else:                  # an ordinary BLOCK -- still not a rectangle
        clips, mid, tp, dish = (.20, .42, .29, .09), .30, r.uniform(0.0, .06), .07
    return _outline(r, l, h, clips=clips, mid=0.0 if seam else mid, taper=tp,
                    flip=r.random() < .5, lean=r.uniform(-1, 1) * .008,
                    roll=rl_, dish=dish)


def _clip_u(poly, plane, keep_lo):
    """The part of an outline on one side of the vertical plane u = `plane`.

    THE SEAM RULE, done by construction instead of by clamp_to_seams. Both
    pieces at a bay edge build the same polygon in the same seam-relative
    coordinates and cut it here on the same plane, so the vertices ON the cut are
    bit-identical between the two meshes and the stone reads as one stone across
    the joint. Clamping cannot do that: it snaps a stray vertex onto the plane
    and keeps its z and its face depth, which is a step, not a cut."""
    out, n = [], len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ia = (a[0] <= plane) if keep_lo else (a[0] >= plane)
        ib = (b[0] <= plane) if keep_lo else (b[0] >= plane)
        if ia:
            out.append(a)
        if ia != ib and abs(b[0] - a[0]) > 1e-9:
            t = (plane - a[0]) / (b[0] - a[0])
            out.append((plane, a[1] + (b[1] - a[1]) * t))
    return _dedupe(out)


def _tilt(r, tilt, d, d_floor):
    """Draw this stone's tilt, signed: + tips the face OUT of the wall, - tips it
    BACK into it. Which way is safe is not symmetric, and both directions have
    something in this module's depth ladder waiting to be broken by them:

      * tipping OUT is free for walling (the nearest thing in front of a wall
        block is nothing at all, and PROUD_MAX is 100 mm further out) and is
        forbidden on the plinth, whose cap slab's -.050 nose is 4 mm in front of
        its proudest stone -- so _footing passes a NEGATIVE tilt, meaning
        "recess only".
      * tipping BACK runs at the mortar layer 30 mm behind the face, and round 7
        measured that pair fighting at 4 mm of margin and clean at 10. So a
        recess is capped at half the distance between this stone's own relief and
        the SHALLOWEST relief its run can produce: a tipped face can never end up
        shallower than a flat stone in the same run already is, and every
        clearance in the ladder is exactly what it was before round 8."""
    if r.random() >= TILT_P:
        return 0.0
    back = min(abs(tilt), max(0.0, (d - d_floor) * .5))
    if tilt < 0:
        return -back
    return abs(tilt) if r.random() < .5 else -back


def _face_plane(r, poly, d, tilt):
    """The plane a stone's FACE sits on, as (cu, cv, gu, gv, bias), so that
    y_face(u,v) = y_bed - d + gu*(u-cu) + gv*(v-cv) + bias.

    Tilting a face out of the wall plane is what stops the field being perfectly
    flush, and the BIAS is what makes it safe: the whole tip is taken to one side
    of the nominal depth. A walling stone (tilt > 0) can therefore only get
    PROUDER, never sink back toward the mortar plane 30 mm behind it and start
    fighting it; a plinth stone, which is passed a NEGATIVE tilt, can only get
    flatter, never push past the nose of its own cap slab -- the two failures
    this family's depth ladder exists to prevent."""
    n = max(1, len(poly))
    cu = sum(q[0] for q in poly) / n
    cv = sum(q[1] for q in poly) / n
    t = min(abs(tilt), d * .28)
    if t < 1e-5:
        return (cu, cv, 0.0, 0.0, 0.0)
    ang = r.uniform(0.0, 2 * pi)
    ca, sa = cos(ang), sin(ang)
    span = max([abs((q[0] - cu) * ca + (q[1] - cv) * sa) for q in poly] + [1e-4])
    g = t / span
    return (cu, cv, g * ca, g * sa, (t if tilt < 0 else -t))


def _stone(p, poly, at, y_bed, d, mat, tint, shade, plane, rise, mid=.60,
           share=.42, ecc=.13, pin_u=None, cone=False, seed=0, extent=None,
           rings=1):
    """ONE STONE: a SKIRT, a SHOULDER and a CROWN.

    ROUND 9, AND THIS IS FAULTS 2 AND 3 IN ONE SHAPE. Shanee: the stones "look
    bulky/square/polygonal and have a lot of gap in-between at times". Both of
    those were this function, and they were the same defect seen twice:

      * round 8 built a stone as an outline extruded to a FLAT n-gon face with a
        45-degree arris round it. Measured on the render, the median stone's
        whole front relief was 6.3% of its width, and the face itself was one
        plane by construction -- so there was no bulge, no falling away, nothing
        for light to run across, and every edge was a crisp machined chamfer.
      * that arris was also cut INWARD from the outline (14 mm a side), and the
        outline was drawn 14 mm OVERSIZE to win the area back. So what the eye
        read as the edge of the stone was neither the cell nor the outline, and
        the drawn joint measured 14-21% of a stone width against the reference's
        10 -- while the oversize still bought 7-9 interpenetrating pairs a piece.

    So a stone is now three rings and a point, and the middle ring is the whole
    trick:

      ring 0  THE BED, one POINT on the stone's own axis at y_bed, buried in
              the mortar layer. Nothing sees it.
      ring 1  THE WIDEST SECTION, the outline carried out to SKIRT_Y -- in
              FRONT of the mortar. This is the silhouette the eye reads, and
              because it is the cell undiminished, the joint that gets drawn is
              the joint the course laid out. A vertical skirt is also what a
              bedded stone's edge actually looks like.
      ring 2  THE SHOULDER, the outline scaled to `mid`, carrying (1 - `share`)
              of the climb to the crown.
      apex    THE CROWN, off-centre, on the face ladder (y_bed - d).

    The shoulder and the crown differ by less than spec.SMOOTH_ANG, so they shade
    as ONE CURVE: the face BULGES and FALLS AWAY instead of folding at a rim.
    `rise` (the crown's height over ring 1) is capped by the ladder, so a stone
    bedded shallow comes out a flattish slab and a proud one comes out round --
    which is the proportion variation the brief asks for, for free.

    ROUND 11 REPLACED RING 0 WITH A POINT and made ring 1 the outermost ring of
    a proper dome. See the note at the bed point below: it closes the shell for
    FEWER triangles than the open version cost, it is the shape (a cobble tapers
    into its bed, it does not sit on a vertical kerb), and it is what finally
    took check_zfight to zero -- a back cone has no axis-aligned facet for a
    dressed slab's top face to be compared against.

    Cost: 4n triangles with one shoulder ring, 6n with two -- against round 9's
    5n for one. `cone` drops the shoulder on small packers (2n), where nobody
    reads a 5 mm shoulder anyway. `rings` = 2 is what the cobble style asks for:
    three slope zones instead of two, which is the difference between a cushion
    and a plate with a chamfer round it.

    `pin_u` names a u that the shoulder and the crown must not leave (the bay
    seam): the shoulder is then scaled TOWARD that plane rather than toward the
    stone's own centroid and the crown sits ON it, so a stone cut at a bay edge
    produces bit-identical vertices on the cut in both pieces and the two halves
    are one stone. See _seam_stone."""
    poly = _dedupe(poly)
    n = len(poly)
    if n < 3 or d <= .008:
        return []
    ax, az = at
    cu, cv, gu, gv, bias = plane
    r = rng(f"sw/dome/{seed}")
    # the CROWN plane: the face ladder, tilted by _face_plane's gradient
    yf = lambda u, v: y_bed - d + gu * (u - cu) + gv * (v - cv) + bias
    ycr = yf(cu, cv)
    # ring 1 sits at the crown plus `rise`, and never behind SKIRT_Y (which is
    # what keeps the widest section in front of the mortar) nor inside the bed
    ys = min(SKIRT_Y, ycr + rise, y_bed - .008)
    if ys < ycr + .009:
        ys = min(max(ycr + .009, ys), y_bed - .008)
        cone = True                     # nothing left to dome: a dressed slab
    pu = cu if pin_u is None else pin_u
    fu = clamp(mid * r.uniform(.96, 1.04), .48, .88)
    fv = clamp(mid * r.uniform(.96, 1.04), .48, .88)
    lu, lv = r.uniform(-.17, .17), r.uniform(-.17, .17)   # a lopsided cushion
    # `extent` is the stone's half-size BEFORE any seam clip. It has to be given
    # for a seam stone: the lean and the crown offset are scaled by it, so
    # measuring it off the CLIPPED polygon made the two halves of one seam stone
    # disagree about where their shared vertices sit -- 21 mm of step at every
    # bay edge, which is exactly the seam _clip_u exists to prevent. Caught by
    # comparing every piece's x = -GRID/2 cut profile with its x = +GRID/2 one.
    hu = extent[0] if extent else max([abs(q[0] - pu) for q in poly] + [1e-4])
    hv = extent[1] if extent else max([abs(q[1] - cv) for q in poly] + [1e-4])
    # THE CROWN'S OFFSET AND THE PER-VERTEX LUMP ARE DRAWN BEFORE THE RING LOOP,
    # and the lump is a function of the vertex POSITION rather than of the rng.
    # It has to be: a seam stone is built twice, from two DIFFERENT clipped
    # polygons, and anything drawn inside the loop would consume a different
    # number of dice on each side -- so the two halves would disagree by a few
    # mm on the vertices they share, which is precisely the seam step round 8
    # went to the trouble of _clip_u to kill.
    au = 0.0 if pin_u is not None else r.uniform(-ecc, ecc) * hu * fu
    av = r.uniform(-ecc, ecc) * hv * fv
    lump = lambda u, v: 1.0 + .155 * _nz.noise((u * 9.0, v * 9.0, 3.1))
    # THE BED IS A POINT, NOT A RING (round 11), and that one change pays for
    # everything else in this function:
    #   * IT CLOSES THE SHELL. Round 9 dropped the bed FACE to save n-2 tris a
    #     stone and relied on the bed ring being buried in an opaque mortar body
    #     to hide the opening. A point needs no face at all, so the stone is a
    #     closed solid for n FEWER triangles than the open ring version -- the
    #     back cone is n triangles where the bed-to-skirt band was n quads.
    #   * IT KILLS THE LAST OF THE Z-FIGHT. A stone whose outline was clamped
    #     flat on a cell edge -- which is most stones -- used to carry that flat
    #     straight back to the bed at the same z, so the underside of its skirt
    #     was a dead HORIZONTAL facet sitting 6 mm above the top face of the
    #     plinth cap it beds on. check_zfight buckets a face by its normal
    #     ROUNDED TO TWO DECIMALS and then compares n.centre, so two +Z faces
    #     whose normals differ by the .01 p.wobble easily puts on a 95 mm facet
    #     can differ by a centimetre of n.centre over a 1 m lever arm and read as
    #     coincident 6.5 mm apart. That is the 22 cm2 that was left on
    #     SM_Wall_StoneRubble_2m_B, measured. Every face of the back cone rakes
    #     from the outline to a point on the stone's own axis, so not one of them
    #     is axis-aligned and none can be compared with a dressed slab's top at
    #     all. (Widening the bed joint would also have cleared it -- and would
    #     have put the wall's first course 10 mm off the bed line corners.py lays
    #     its quoins on, i.e. traded a measurement artefact for a real step at
    #     every quoin in the kit.)
    #   * AND IT IS THE SHAPE. A cobble is widest at its face and tapers into the
    #     bed; the vertical skirt it replaces was the "tile edge" half of "reads
    #     as squared octagonal tiles".
    # Nothing about the silhouette changes: ring 1 is still the cell, still in
    # front of the mortar, so the drawn joint is still the joint the course laid
    # out. For a seam stone the point sits ON the pin plane at v = 0, so both
    # halves put it in the same place and the cut stays bit-identical.
    vs = [(ax + pu, y_bed, az + 0.0)]                        # 0: THE BED POINT
    vs += [(ax + u, ys, az + v) for (u, v) in poly]          # 1..n: the cell
    F = [(0, 1 + (i + 1) % n, 1 + i) for i in range(n)]      # the back cone
    o = 1
    if not cone:
        # THE DOME, as `rings` shoulder rings on a SPHERICAL profile. One ring
        # (the default, and what the rubble and the ashlar want) gives two slope
        # zones: a rim band and a broad near-flat cap, which is a plate with a
        # chamfer on anything as domed as a cobble. Two rings spread the same
        # rise over three zones -- a steep rolled rim, a shoulder, a small cap --
        # and THAT is what reads as a cushion in flat-shaded Solid viewport,
        # where a face's tone is its slope and nothing else. The scales come off
        # `mid` and the heights off sqrt(1 - f^2), so consecutive zones differ by
        # well under spec.SMOOTH_ANG (measured 28 and 11 degrees on the median
        # cobble) and shade as ONE curve rather than creasing at a rim.
        prof = ([(mid, 1.0 - share)] if rings < 2 else
                [(min(mid * 1.30, .88), 0.0), (mid * .72, 0.0)])
        for k, (f, hh) in enumerate(prof):
            fu_, fv_ = fu * f / mid, fv * f / mid
            hh = hh or sqrt(max(1.0 - f * f, 0.0))
            for (u, v) in poly:
                mu_ = pu + (u - pu) * fu_
                mv_ = cv + (v - cv) * fv_
                yy = yf(mu_, mv_)
                ym = yy + (ys - yy) * (1.0 - hh) * (1.0 + lu * (u - pu) / hu
                                                    + lv * (v - cv) / hv) * lump(u, v)
                vs.append((ax + mu_, min(max(ym, yy + .0015), ys - .0015), az + mv_))
            for i in range(n):
                j = (i + 1) % n
                F.append((o + i, o + j, o + n + j, o + n + i))   # a shoulder
            o += n
    vs.append((ax + pu + au, min(yf(pu + au, cv + av), ys - .003), az + cv + av))
    A = len(vs) - 1
    for i in range(n):
        F.append((o + i, o + (i + 1) % n, A))                # the crown
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _wob(p, amount=WOB, **kw):
    """p.wobble() with the noise field pinned first -- see NOISE_SEED. Every
    piece in the family goes through here; nothing calls p.wobble() directly."""
    _nz.seed_set(NOISE_SEED)
    p.wobble(amount, **kw)


def _blotch(x, z, seed=1, f=.72):
    """Smooth -1..1 field. Real walling varies in PATCHES -- a run of warm
    blocks, a damp dark corner -- not block-by-block like confetti."""
    return _nz.noise((x * f + seed * 3.7, z * f + seed * 1.3, seed * .41))


def _pick(r, t, warm, pale, dark, b=0.0):
    """Block colour. Damp and dark at grade, warmer and paler up in the sun,
    clustered by the blotch field `b`. The mix is pale/warm-led: the reference's
    ground floor is a pale warm cream-grey, not a cool neutral. `dark` stays
    tiny -- stone_pale against stone_dark is a 90 L jump and at one block in
    twenty the wall stops reading as masonry."""
    q = r.random()
    d = dark + (1.0 - t) * (1.0 - t) * .028 + max(-b, 0.0) * .03
    w = warm + t * .04 + max(b, 0.0) * .16
    pl = pale + max(b, 0.0) * .12
    if q < d:
        return "stone_dark"
    if q < d + w:
        return "stone_warm"
    if q < d + w + pl:
        return "stone_pale"
    return "stone"


def _tone(r, t, b, warm, pale, dark, var):
    """Value comes mostly from the PATCH field and only a little from the die.
    The other way round -- which is what a big `var` gives you -- is confetti:
    every stone a different value from the one beside it, which at any distance
    averages back to one flat tone with a busy grain, and up close reads as
    sample tiles rather than as one wall. The upper clamp matters too: at 1.28
    on stone_pale a block blew out to near white every twentieth stone."""
    m = _pick(r, t, warm, pale, dark, b)
    sd = (1.0 + b * .105 + r.uniform(-var, var) + lerp(-.05, .04, t)
          + (.14 if m == "stone_dark" else 0.0))   # a dark STONE, not a hole:
    # stone_dark is 40 L below stone, and darkened another 10% on top of that it
    # read as a missing block. It is now lifted instead, so it lands where the
    # references' wet lower stones sit -- clearly the darkest thing in the wall,
    # clearly still a stone.
    return m, clamp(sd, .60, 1.15)


# ------------------------------------------------------------------ openings --
class Op:
    """A round-headed opening from spec.OPENINGS, and the geometry questions the
    walling needs to ask it."""

    def __init__(self, key, sur, segs):
        o = S.OPENINGS[key]
        self.R = o["w"] / 2
        self.z0 = o["sill"]
        self.z1 = o["sill"] + o["h"]
        self.spring = self.z1 - self.R
        self.sur = sur                 # width of the dressed surround
        self.segs = segs               # voussoirs in the ring

    def hw(self, z, extra=0.0):
        """Half-width of the void, inflated by `extra`, at height z."""
        rr = self.R + extra
        if z <= self.spring:
            return rr
        d = z - self.spring
        return sqrt(rr * rr - d * d) if d < rr else 0.0

    def spans(self, zb, zt, extra):
        """The x runs in a course [zb,zt] that are clear of the opening and its
        surround. Evaluated at the course TOP above the springing, so what
        overhangs at the course bottom is always hidden behind the ring."""
        if zt <= self.z0 + 1e-6:
            return [(-HX, HX)]
        hw = self.hw(zt if zb >= self.spring else self.spring, extra)
        if hw <= 0.0:
            return [(-HX, HX)]
        if hw >= HX - .03:
            return []
        return [(-HX, -hw), (hw, HX)]

    def _arc(self, extra, a0, a1, n):
        rr = self.R + extra
        out = []
        for i in range(1, n + 1):
            a = lerp(a0, a1, i / n)
            out.append((rr * cos(a), self.spring + rr * sin(a)))
        return out

    def outline(self, zt, extra, xm=BITE, n=10, z0=0.0):
        """(x,z) outline(s) of the bay minus the inflated void. An opening that
        reaches the ground gives one U; an interior opening leaves a hole, which
        a single extruded profile cannot describe, so it is cut into a left and a
        right half that bury into each other at x = 0. The caller gives the two
        halves different y AND z extents so they share no plane at all."""
        rr = self.R + extra
        zb = self.z0 - extra
        if zb <= 1e-4:
            return [[(-HX, z0), (-rr, z0), (-rr, self.spring)]
                    + self._arc(extra, pi, 0.0, n)
                    + [(rr, z0), (HX, z0), (HX, zt), (-HX, zt)]]
        left = ([(-HX, z0), (xm, z0), (xm, zb), (-rr, zb), (-rr, self.spring)]
                + self._arc(extra, pi, pi / 2, max(2, n // 2))
                + [(xm, self.spring + rr), (xm, zt), (-HX, zt)])
        return [left, [(-x, z) for (x, z) in left]]


# ------------------------------------------------------------------- shells ---
def _core(p, zt, op=None, extra=CLR):
    """The solid core, buried behind the mortar layer. Nothing ever sees its
    front face now -- _mortar owns the surface the joints show -- so it goes back
    to being the dark mass it always was, and its back still stops 4 mm inside
    the plaster lining instead of sharing its plane."""
    if op is None:
        p.plate((0, (BED + CORE_Y1) / 2, zt / 2), (G, CORE_Y1 - BED, zt),
                "stone_dark", tint=.03, shade=CORE_SHADE)
        return
    for i, (y0, y1, z0, z1) in enumerate(((BED, CORE_Y1, 0.0, zt),
                                          (BED2, CORE_Y2, SPLIT_Y, zt + SPLIT_Y))):
        polys = op.outline(z1, extra, z0=z0)
        if i >= len(polys):
            break
        p.prism(polys[i], y1 - y0, "stone_dark", axis='Y',
                at=(0, (y0 + y1) / 2, 0), bevel=0, tint=.03, shade=CORE_SHADE)


# ------------------------------------------------------------------ mortar ----
def mortar_field(p, zb, zt, x0, x1, ri, y=MORT_Y, shade=MORT_SHADE, pale=.17,
                 pad_lo=MORT_CLR, pad_hi=MORT_CLR):
    """THE JOINT PLANE for one course, laid as one or two patches.

    `zb`/`zt` and `x0`/`x1` are the COURSE's own bounds -- the bed lines and the
    span. The patch is grown past them here, and by exactly the clearances the
    depth ladder needs (MORT_CLR / MORT_XPAD), because getting that wrong is
    what put 437 cm2 of coincident surface back into this family in round 9:
    the caller used to pass pre-padded bounds and the padding it chose (8.8 mm)
    was smaller than the joint the stones were laid on (8.0 mm a side), so the
    patch's horizontal faces landed 0.8 mm off the skirts of the course above.
    One rule, in one place, expressed as a clearance rather than as a bite.

    This is what Shanee was asking for when he asked whether the mortar needed a
    colour of its own. Before, the "mortar" was whatever you could see of the
    dark core through a 20 mm slot -- one flat near-black value over the whole
    piece, so a joint read as an absence rather than as a material. Now it is a
    surface of its own, 50 mm behind the stone faces (so the recess is real and
    self-shadowing), at a tone that catches light, and PATCHED: each patch takes
    its own value off its own rng, some of them on `stone` rather than
    stone_dark, so the joints in one course are a different mortar from the
    joints two courses up -- lime that was mixed on a different day.

    KEYED ON THE COURSE AND THE SPAN, never on the piece: two variants meeting
    at a bay seam must show the same mortar behind the same joint, or the seam
    is a tonal step full height. `ri` only picks the depth parity.

    PUBLIC: corners.py backs its quoins with this."""
    if x1 - x0 < .05:
        return
    # grow past the span, but never at a BAY SEAM (x = +-GRID/2 is a snap plane:
    # coincidence there is between two pieces that are always placed together,
    # it is excluded from the measurement by construction, and both neighbours
    # must put the same solid there) and never more than halfway to the bay
    # centre, so the two spans either side of an opening cannot meet.
    if abs(x0 + HX) > 1e-6:
        x0 -= min(MORT_XPAD, abs(x0) * .5)
    if abs(x1 - HX) > 1e-6:
        x1 += min(MORT_XPAD, abs(x1) * .5)
    w = x1 - x0
    # ONE PATCH PER SPAN, and that is a SEAM fix as well as a simplification.
    # Round 8 laid one patch per ~0.95 m so the lime changed batch along the
    # wall, and paid for the overlap between two patches in a course by sinking
    # every other one MORT_STEP -- which put the patch at x = -GRID/2 on one
    # depth and the patch at x = +GRID/2 on the other, i.e. a 4-7 mm step in the
    # joint plane at every bay edge. Invisible in itself (it is 60 mm down a
    # shadowed joint, behind a seam stone), but it was the ONE thing left that
    # made a piece's two cut profiles differ, and a rule that is only nearly true
    # is a rule nobody can check. One patch per span: both bay edges are the same
    # solid, the profile is identical, and there is no intra-course overlap to
    # hold apart. The batch-to-batch variation is now course to course, which is
    # all a 16 mm joint can show anyway.
    # KEYED ON THE COURSE ALONE -- not on the span. An opening's courses are
    # walled in two spans, and keying on x0 gave the span that runs to the +GRID/2
    # seam a different mortar depth from the one a plain bay puts there: the arch
    # bay's +x cut profile then differed from the window bay's -x profile by
    # 26 mm, which is Shanee's round-6 note ("StoneWindow next to StoneArch shows
    # seams") coming back through the mortar instead of through the stones. Two
    # spans of one course never overlap (the opening is between them), so one
    # depth for the whole course is safe as well as identical everywhere.
    r = rng(f"sw/mortar/{zb:.4f}")
    zb, zt = max(zb - pad_lo, 0.0), zt + pad_hi
    # Adjacent COURSES still overlap (each course's patch runs LAP*.55 past its
    # bed lines), so their front and back planes are held apart by parity --
    # front by MORT_STEP, back by 12 mm -- with a jitter deliberately SMALLER
    # than either, so the two can never close to within check_zfight's 0.2 mm.
    yy = y + (MORT_STEP if ri % 2 else 0.0) + r.uniform(-.0012, .0012)
    th = MORT_T + (.006 if ri % 2 else -.006) + r.uniform(-.0012, .0012)
    # a warm patch and a cool patch of mortar are two batches of lime, and that
    # is exactly the "colour for the mortar in between" that was missing
    warm = r.random() < pale
    m = "stone_warm" if warm else "stone_dark"
    sd = (.64 if warm else shade) * (1.0 + r.uniform(-.24, .24))
    p.plate(((x0 + x1) / 2, yy + th / 2, (zb + zt) / 2),
            (w, th, zt - zb), m, tint=.07, shade=sd)


def _skim(p, zt):
    """Plaster lining on the inner face, so interiors are not black stone. It
    OWNS the y = T plane -- nothing else in the piece reaches it."""
    p.plate((0, (SKIM_Y + T) / 2, (.008 + zt) / 2),
            (G - .010, T - SKIM_Y, zt - .008), "plaster_dim", tint=.04)


def _blank(p, op, e=.012):
    """Dark blank plugging the back of an opening: stops daylight and stops the
    pale lining reading as paper stuck over the hole. It sits at .300-.326, so
    every insert depth in the kit fits in front of it."""
    y0, y1 = BLANK_Y
    z0, z1 = max(op.z0 - e, 0.0), op.z1 + e
    p.plate((0, (y0 + y1) / 2, (z0 + z1) / 2),
            (2 * (op.R + e), y1 - y0, z1 - z0), "stone_dark", tint=.02, shade=.15)


# ------------------------------------------------------------- the seam rule --
def _seam_stone(p, side, zlo, zhi, y, depth, joint, sty, warm, pale, dark,
                max_reach=9.9, rl=RL_WALL, tilt=TILT):
    """The stone that STRADDLES a bay seam.

    THIS is what makes two different variants -- and, since round 9, two
    different STYLES -- meet with no visible line. The notional stone spans
    [seam-a, seam+b] and everything about it (width, split point, shape, relief,
    material, shade) comes from an rng keyed on the COURSE ALONE, with tint 0 so
    _paint's per-primitive jitter (which depends on how many primitives the piece
    happened to emit first) cannot pull the two halves apart. The piece on the
    left keeps [seam-a, seam], the piece on the right keeps [seam, seam+b], and
    together they are ONE stone. Returns how far it reaches INTO this piece.

    The outline is clipped by _clip_u, in coordinates whose u = 0 is the seam --
    not by clamp_to_seams, which snaps a stray vertex onto the plane and keeps
    its z and its depth, i.e. makes a step rather than a cut. Round 9 adds the
    other half of that rule: the stone is DOMED now, so the shoulder is scaled
    toward the seam plane and the crown sits ON it (see _stone's `pin_u`), and
    every per-vertex draw in _stone is a function of position rather than of the
    dice -- because the two halves clip to different polygons and so would
    consume different numbers of dice.

    A style keyed on the course means a cobble bay and an ashlar bay meeting at a
    seam share ONE stone across it, drawn in the LEFT piece's hand on the left of
    the seam and the right piece's on the right. Its two halves are then not
    identical, so `mono` is on: both pieces draw the seam stone in the style
    common to the whole family -- hewn rubble -- which is the one shape either
    neighbour can be bonded into.

    `max_reach` clips only the half INSIDE this piece, never the overhang: on the
    arch bay a course has barely 140 mm of wall between the seam and the dressed
    jamb, and a .27 reach used to drive the seam stone straight through the
    surround."""
    r = rng(f"sw/seamstone/{zlo:.4f}/{zhi:.4f}")
    mono = STYLES["rubble"]      # see the docstring: ONE recipe for every style
    warm, pale, dark = mono["warm"], mono["pale"], mono["dark"]
    w = r.uniform(.26, .46)
    u = r.uniform(.38, .62)
    a, b = w * u, w * (1.0 - u)
    reach = min(a if side > 0 else b, max_reach)
    h = zhi - zlo
    t = clamp((zlo + zhi) / 2 / H)
    m, sd = _tone(r, t, 0.0, warm, pale, dark, .07)
    d = _relief(w, depth, rl)
    poly = _shape(r, mono, w, h, seam=True)
    poly = [(uu + (b - a) / 2.0, vv) for (uu, vv) in poly]   # u = 0 is the seam
    plane = _face_plane(r, poly, d, _tilt(r, tilt, d, depth * rl[0] * rl[2]))
    rise = min(w, h) * r.uniform(*mono["rise"])
    ext = ((max(q[0] for q in poly) - min(q[0] for q in poly)) / 2,
           (max(q[1] for q in poly) - min(q[1] for q in poly)) / 2)
    poly = _clip_u(poly, 0.0, side > 0)
    poly = (_clip_u(poly, -reach, False) if side > 0
            else _clip_u(poly, reach, True))
    _stone(p, poly, (side * HX, (zlo + zhi) / 2), y + r.uniform(0, .006),
           d, m, 0.0, sd, plane, rise, mid=r.uniform(*mono["mid"]),
           share=mono["share"], ecc=mono["ecc"], pin_u=0.0,
           cone=h < .115, seed=f"seam/{zlo:.4f}", extent=ext)
    return reach


def _one(p, r, cu, cz, l, h, t, y, depth, joint, sty, warm, pale, dark, var,
         tint, rl=RL_WALL, tilt=TILT, low=LOW_P):
    """ONE STONE, laid in its cell -- and since round 9, in its style's hand.

    THE CELL RULE, and it is the whole of fault 3. The caller hands this function
    a rectangle that its neighbours are already clear of by the course's joint,
    and nothing here may leave that rectangle: the centre jitter is taken OUT of
    the cell before the outline is drawn, the roll is paid for by _cell_eps, and
    every vertex is clamped by _outline / _round_outline. So the joint the course
    laid out is the joint that gets drawn, overlap is impossible by arithmetic
    rather than by reserving space for it, and the joint can therefore be set to
    what the reference actually shows (9% of a stone width) instead of to
    whatever the jitter needed. Round 8 did it the other way round -- a 36 mm
    joint, an outline drawn 14 mm oversize into it, and 7-9 measured
    interpenetrating pairs a piece anyway."""
    if l < .05 or h < .04:
        return
    # A stone need not fill its bed to the last millimetre. A sixth of them sit
    # low or high in the course with a wedge of mortar over or under them, which
    # is how the reference gets a bed line you can follow without getting a bed
    # line you can measure.
    if h > .130 and r.random() < low:
        cut = min(r.uniform(.006, .022), h * .14)
        h -= cut
        cz += r.uniform(-.5, .5) * cut
    b = _blotch(cu, cz)
    m, sd = _tone(r, t, b, warm, pale, dark, var)
    d = _relief(l, depth, rl) * r.uniform(rl[2], rl[3])
    # ---- the bedding jitter, PAID FOR out of the cell ----------------------
    jx = min(.0010, l * .006)
    jy = min(.0010, h * .006)
    cu += r.uniform(-1, 1) * jx
    cz += r.uniform(-1, 1) * jy
    poly = _shape(r, sty, l - 2 * jx, h - 2 * jy)
    tl = _tilt(r, tilt, d, depth * rl[0] * rl[2])
    # ...and every stone is bedded to its own depth in the mortar, INWARD only:
    # the bed plane is the shallowest thing the mortar has to swallow, so it may
    # go deeper into the lime but never nearer the surface of it.
    _stone(p, poly, (cu, cz), y + r.uniform(0, .006), d, m, tint, sd,
           _face_plane(r, poly, d, tl),
           min(l, h) * r.uniform(*sty["rise"]),
           mid=r.uniform(*sty["mid"]), share=sty["share"], ecc=sty["ecc"],
           cone=(l < .195 or h < .112), rings=sty.get("rings", 1),
           seed=f"{cu:.4f}/{cz:.4f}/{l:.3f}")


def _lengths(r, span, long, small, sty, course=COURSE):
    """The width distribution for one course, normalised to fill `span` exactly.

    THREE-HUMPED -- genuinely big blocks, a plain middle, and real packers --
    rather than one narrow band around the mean, because the outliers are what
    the eye reads as hand-laid. ROUND 9 draws every width in COURSE HEIGHTS
    instead of in metres, which is what lets one distribution serve a .232 course
    and a .250 plinth course and keeps every stone's aspect where the style put
    it: the cobble style asks for .86-1.34 courses (near-equant, as ref1's river
    stones are), the rubble style .95-1.62 with through-stones out at 2.65, the
    ashlar style 1.30-1.85 and hardly any spread at all."""
    lens, tot = [], 0.0
    while tot < span:
        q = r.random()
        if q < long:
            L = course * r.uniform(*sty["wlong"])
        elif q < long + small:
            L = course * r.uniform(*sty["wsmall"])
        else:
            L = course * r.uniform(*sty["wmid"])
        L = clamp(L, BLK_MIN, BLK_MAX)
        lens.append(L)
        tot += L
    if len(lens) > 1 and tot - lens[-1] > span * .74:
        lens.pop()          # drop the overshoot rather than squeeze every stone
    k = span / sum(lens)
    return [L * k for L in lens]


def _fill(p, x0, x1, zlo, zhi, key, y, depth, joint, sty, long, small, split,
          warm, pale, dark, var, tint, skip, rl=RL_WALL, tilt=TILT, low=LOW_P):
    """Lay one course between two fixed edges. Joint WIDTHS vary per joint as
    well as stone widths: all-one-width joints put a regular grid back over
    however irregular the stones are, and the joint is the line the eye actually
    follows. A wide slot is sometimes filled with one full-height stone and a
    stack of two small squarish ones beside it, which is how ref1 works small
    stones into a course without breaking the coursing."""
    span = x1 - x0
    if span < .07:
        return
    r = rng(f"sw/fill/{key}/{x0:.3f}")
    h = zhi - zlo
    lens = _lengths(r, span, long, small, sty, max(h, .10))
    edges = [x0]
    for L in lens:
        edges.append(edges[-1] + L)
    js = [joint * r.uniform(.72, 1.44) for _ in range(len(lens) + 1)]
    last = len(lens) - 1
    t = clamp((zlo + zhi) / 2 / H)
    for i, L in enumerate(lens):
        a = edges[i] + (0.0 if i == 0 else js[i] / 2)
        b2 = edges[i + 1] - (0.0 if i == last else js[i + 1] / 2)
        if r.random() < skip:
            continue
        ln, cu = b2 - a, (a + b2) / 2
        if ln > h * 1.55 and r.random() < split:
            # A WIDE SLOT TAKES ONE FULL-HEIGHT STONE AND A STACK OF TWO SMALL
            # SQUARISH ONES BESIDE IT -- ref1's "big stones at the bottom,
            # smaller ones packed into the gaps". Splitting the slot's LENGTH
            # first is what keeps every stone in the cluster near square; round
            # 7 halved its HEIGHT and kept the full length, i.e. made 4:1 slats.
            f = r.uniform(.50, .64)
            g = joint * r.uniform(.7, 1.1)
            if r.random() < .5:
                (xa0, xa1), (xb0, xb1) = (a, a + ln * f), (a + ln * f + g, b2)
            else:
                (xb0, xb1), (xa0, xa1) = (a, b2 - ln * f - g), (b2 - ln * f, b2)
            _one(p, r, (xa0 + xa1) / 2, (zlo + zhi) / 2, xa1 - xa0, zhi - zlo,
                 t, y, depth, joint, sty, warm, pale, dark, var, tint, rl,
                 tilt, low)
            mid = lerp(zlo, zhi, r.uniform(.40, .60))
            for zz0, zz1 in ((zlo, mid - joint / 2), (mid + joint / 2, zhi)):
                _one(p, r, (xb0 + xb1) / 2, (zz0 + zz1) / 2,
                     (xb1 - xb0), zz1 - zz0, t, y, depth, joint, sty, warm,
                     pale, dark + .03, var, tint, rl, tilt, low)
            continue
        _one(p, r, cu, (zlo + zhi) / 2, ln, zhi - zlo, t, y, depth, joint, sty,
             warm, pale, dark, var, tint, rl, tilt, low)


# ------------------------------------------------------- blocks across courses --
def _tall_plan(rows, seed, rate, wide=(.30, .52), margin=.58):
    """Which blocks span TWO courses.

    A wall whose every stone is exactly one course tall is a wall of rows, and
    rows are the pattern. Real coursed rubble has a few big stones that take up
    two beds and force their neighbours to pack round them, and one of those per
    two or three courses is enough to break the rhythm of the whole elevation.

    Kept `margin` clear of both bay seams, so a tall block never interacts with
    how two pieces meet: the seam stones and the bed lines are untouched."""
    r = rng(f"sw/tall/{seed}")
    out, ri = [], 0
    while ri < len(rows) - 1:
        if r.random() < rate:
            w = r.uniform(*wide)
            xc = r.uniform(-HX + margin, HX - margin)
            out.append((ri, xc - w / 2, xc + w / 2))
            ri += 2
        else:
            ri += 1
    return out


def _minus(a0, a1, occ, pad, keep=.115):
    """[a0,a1] with the occupied runs (grown by `pad`) taken out of it."""
    segs = [(a0, a1)]
    for (u0, u1) in occ:
        nxt = []
        for (s0, s1) in segs:
            if u1 + pad <= s0 or u0 - pad >= s1:
                nxt.append((s0, s1))
                continue
            if u0 - pad > s0:
                nxt.append((s0, u0 - pad))
            if u1 + pad < s1:
                nxt.append((u1 + pad, s1))
        segs = nxt
    return [(a, b) for (a, b) in segs if b - a > keep]


def _inside(spans, a, b):
    return any(x0 - 1e-6 <= a and b <= x1 + 1e-6 for (x0, x1) in spans)


def _sty(sty):
    return STYLES[sty] if isinstance(sty, str) else sty


def _blocks(p, rows, seed, op=None, extra=None, y=BLK_Y, depth=PROUD,
            joint=None, long=None, small=None, split=None, warm=None, pale=None,
            dark=None, var=None, tint=None, skip=0.0, bevel=JOINT_BEV,
            tall=None, tall_wide=None, rl=RL_WALL, mortar=True, bite_lo=False,
            bite_hi=True, tilt=TILT, low=None, sty="rubble", plinth=False):
    """COURSED BLOCK FACING over the canonical rows, in one of the family's
    STYLES. Every piece walls the same rows, so bed lines match across a bay
    seam AND across a change of style; each course starts and ends with a seam
    stone, so the seam itself is covered by one stone rather than by two
    independently jittered halves; each course is backed by the mortar layer,
    which is keyed on the course and so is the same solid on both pieces.

    Every keyword that is left None comes out of the style table, so a caller
    only names what it wants to differ. `bevel` is kept for the public signature
    (corners.py's course_run) and no longer does anything: a stone's arris is its
    shoulder now, not a chamfer."""
    sty = _sty(sty)
    pick = lambda v, k: sty[k] if v is None else v
    joint = pick(joint, "joint_pl" if plinth else "joint")
    long, small = pick(long, "long"), pick(small, "small")
    split, warm = pick(split, "split"), pick(warm, "warm")
    pale, dark = pick(pale, "pale"), pick(dark, "dark")
    var, tint = pick(var, "var"), pick(tint, "tint")
    tall, tall_wide = pick(tall, "tall"), pick(tall_wide, "tall_wide")
    low = pick(low, "low")
    _nz.seed_set(NOISE_SEED)      # _blotch samples the noise field; see NOISE_SEED
    ex = (op.sur + joint * .4) if (op is not None and extra is None) else (extra or 0.0)
    n = len(rows)
    lo = lambda ri: (rows[ri][0] - LAP) if (ri == 0 and bite_lo) else rows[ri][0] + joint / 2
    hi = lambda ri: (rows[ri][1] + LAP) if (ri == n - 1 and bite_hi) else rows[ri][1] - joint / 2
    talls = _tall_plan(rows, seed, tall, wide=tall_wide)
    for ri, (zb, zt) in enumerate(rows):
        zlo, zhi = lo(ri), hi(ri)
        spans = op.spans(zb, zt, ex) if op is not None else [(-HX, HX)]
        if mortar:
            # THE PATCH CLEARS THE STONES BY MORT_CLR, always. Which stone is
            # nearest depends on the course: an end course that BITES into the
            # slab above or below it lays its stones LAP past the bed line, an
            # ordinary one half a joint past it.
            #   KEYED ON THE CANONICAL JOINT, NOT ON THIS STYLE'S, for the same
            # reason the seam stone is: a cobble bay packs on 7 mm and a rubble
            # bay on 12, and if the patch took the style's number then the two
            # would put mortar bodies of DIFFERENT height either side of one bay
            # seam -- a 2.5 mm step in the joint plane at every seam between two
            # styles, which is the one thing round 9 got right and this must not
            # undo. max(), so a caller asking for a wider joint than the family's
            # still gets its clearance.
            j_near = max(joint, JOINT) / 2
            p_lo = (LAP if (ri == 0 and bite_lo) else j_near) + MORT_CLR
            p_hi = (LAP if (ri == n - 1 and bite_hi) else j_near) + MORT_CLR
            for (x0, x1) in spans:
                mortar_field(p, zb, zt, x0, x1, ri, shade=sty["mort_shade"],
                             pale=sty["mort_pale"], pad_lo=p_lo, pad_hi=p_hi)
        # the two-course blocks that occupy this row, and the ones starting in it
        occ, rt = [], rng(f"sw/tallone/{seed}/{ri}")
        for (i0, a, b) in talls:
            if i0 not in (ri, ri - 1):
                continue
            spans2 = (op.spans(rows[i0 + 1][0], rows[i0 + 1][1], ex)
                      if op is not None else [(-HX, HX)])
            if not (_inside(spans, a, b) and _inside(spans2, a, b)):
                continue
            occ.append((a, b))
            if i0 == ri:
                z0, z1 = zlo, hi(i0 + 1)
                _one(p, rt, (a + b) / 2, (z0 + z1) / 2, b - a, z1 - z0,
                     clamp((z0 + z1) / 2 / H), y, depth, joint, sty, warm, pale,
                     dark, var, tint, rl, tilt, low * .5)
        # THE SEAM STONE'S OWN BED BOUNDS, on the family's canonical joint
        # rather than on this style's. A style may pack tighter than another --
        # the ashlar runs an 11 mm joint against the rubble's 16 -- and if the
        # seam stone took that number, its rng key and its height would change
        # with it, so a cobble bay and an ashlar bay would put two DIFFERENT
        # stones either side of the same bay edge. Canonical: one stone.
        zs_lo = (rows[ri][0] - LAP) if (ri == 0 and bite_lo) else rows[ri][0] + JOINT / 2
        zs_hi = (rows[ri][1] + LAP) if (ri == n - 1 and bite_hi) else rows[ri][1] - JOINT / 2
        for (x0, x1) in spans:
            a0, a1 = x0, x1
            room = x1 - x0
            mr = room if room < .34 else room - .12
            if abs(x0 + HX) < 1e-6:
                a0 = -HX + joint + _seam_stone(p, -1, zs_lo, zs_hi, y, depth,
                                               joint, sty, warm, pale, dark, mr,
                                               rl, tilt)
            if abs(x1 - HX) < 1e-6:
                a1 = HX - joint - _seam_stone(p, +1, zs_lo, zs_hi, y, depth,
                                              joint, sty, warm, pale, dark, mr,
                                              rl, tilt)
            for (u0, u1) in _minus(a0, a1, occ, joint * .6):
                _fill(p, u0, u1, zlo, zhi, f"{seed}/{ri}/{u0:.3f}", y, depth,
                      joint, sty, long, small, split, warm, pale, dark, var,
                      tint, skip, rl, tilt, low)


def course_run(p, x0, x1, rows, key, joint=None, y=BLK_Y, depth=PROUD,
               long=None, small=None, split=None, warm=None, pale=None,
               dark=None, var=None, tint=None, bevel=JOINT_BEV, rl=RL_WALL,
               mortar=True, bite_lo=False, bite_hi=True, tilt=TILT, low=None,
               sty="rubble"):
    """PUBLIC: lay the family's canonical coursed facing between two arbitrary
    x bounds, over `rows` -- i.e. on somebody else's piece.

    corners.py fills the field of SM_Corner_StoneInner with this, so the masonry
    that meets a stone wall run is literally the same masonry, laid on the same
    bed lines at the same relief with the same mortar behind it. A corner that
    generates its own rubble is a corner that reads as a different building.
    `sty` picks the style; the default is the rubble the corners were built
    against, so an existing caller gets exactly what it got before."""
    sty = _sty(sty)
    pick = lambda v, k: sty[k] if v is None else v
    joint = pick(joint, "joint")
    long, small = pick(long, "long"), pick(small, "small")
    split, warm = pick(split, "split"), pick(warm, "warm")
    pale, dark = pick(pale, "pale"), pick(dark, "dark")
    var, tint = pick(var, "var"), pick(tint, "tint")
    low = pick(low, "low")
    _nz.seed_set(NOISE_SEED)
    n = len(rows)
    for ri, (zb, zt) in enumerate(rows):
        zlo = (zb - LAP) if (ri == 0 and bite_lo) else zb + joint / 2
        zhi = (zt + LAP) if (ri == n - 1 and bite_hi) else zt - joint / 2
        if mortar:
            j_near = max(joint, JOINT) / 2
            mortar_field(p, zb, zt, x0, x1, ri,
                         shade=sty["mort_shade"], pale=sty["mort_pale"],
                         pad_lo=(LAP if (ri == 0 and bite_lo) else j_near) + MORT_CLR,
                         pad_hi=(LAP if (ri == n - 1 and bite_hi) else j_near) + MORT_CLR)
        _fill(p, x0, x1, zlo, zhi, f"{key}/{ri}", y, depth, joint, sty, long,
              small, split, warm, pale, dark, var, tint, 0.0, rl, tilt, low)


# ------------------------------------------------------------ dressed courses --
def _seam_slab(p, side, z0, z1, y0, y1, key, taper, skew, bevel, shade, pale,
               max_reach):
    """The dressed slab that STRADDLES a bay seam -- the seam-stone rule applied
    to the three strongest lines in the piece.

    Round 6 gave these a half joint each side of the seam instead, on the grounds
    that a slab clamped at the seam puts its cut face on the core's own seam
    face. True, and harmless -- that plane is a butt joint between two pieces
    that are always placed together, exactly like the core's own. What was NOT
    harmless was the result: the plinth cap, the sill band and the wall head are
    the longest uninterrupted horizontals on the elevation, and a 16 mm dark nick
    through all three at the same x, repeating every 2 m, is a seam line you can
    count off down the street. One slab across the joint, keyed on the band alone
    and with tint 0, and there is nothing there to see."""
    r = rng(f"sw/seamslab/{key}/{z0:.4f}")
    # AS LONG AS THE SLABS IT SITS BETWEEN. At .30-.46 the seam slab was half the
    # length of the run's other slabs, which put a pair of unusually close joints
    # either side of every bay edge -- so the seam stopped being a line and became
    # a RHYTHM at 2 m instead, which is just as readable. Same length, no rhythm.
    w = r.uniform(.52, .72)
    u = r.uniform(.40, .60)
    a, b = w * u, w * (1.0 - u)
    reach = min(a if side > 0 else b, max_reach)
    if side > 0:
        x_lo, x_hi = HX - reach, HX + b
    else:
        x_lo, x_hi = -HX - a, -HX + reach
    m = "stone_pale" if r.random() < pale else "stone_warm"
    p.box(((x_lo + x_hi) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
          (x_hi - x_lo, y1 - y0, z1 - z0), m, bevel=bevel, seg=1, tint=0.0,
          taper=taper, taper_axis='Y', skew=(0, skew),
          shade=shade + r.uniform(-.05, .05))
    return reach


def _slabs(p, spans, z0, z1, y0, y1, key, per_m=1.6, joint=.016, taper=.98,
           skew=.006, tint=.05, bevel=.010, shade=.93, var=.060, pale=.70,
           seam=True):
    """A run of long dressed slabs -- plinth cap, sill band, wall head, coping.
    ref3's strongest horizontals, and so the family's worst seam risk: every one
    of them lays a seam slab across the bay edge before it fills the rest.

    shade .93 rather than 1.0: dressed stone is stone_pale, which is 40 L above
    the field's stone, and at full value three near-white bands across a grey
    wall stopped being string courses and became stripes."""
    r = rng(f"sw/slab/{key}")
    for (x0, x1) in spans:
        a0, a1 = x0, x1
        room = x1 - x0
        mr = room if room < .30 else room - .14
        if seam and abs(x0 + HX) < 1e-6:
            a0 = -HX + joint + _seam_slab(p, -1, z0, z1, y0, y1, key, taper,
                                          skew, bevel, shade, pale, mr)
        if seam and abs(x1 - HX) < 1e-6:
            a1 = HX - joint - _seam_slab(p, +1, z0, z1, y0, y1, key, taper,
                                         skew, bevel, shade, pale, mr)
        w = a1 - a0
        if w < .06:
            continue
        n = max(1, int(round(w * per_m)))
        for i in range(n):
            a = lerp(a0, a1, i / n) + (joint / 2 if i else 0.0)
            b = lerp(a0, a1, (i + 1) / n) - (joint / 2 if i < n - 1 else 0.0)
            m = "stone_pale" if r.random() < pale else "stone_warm"
            p.box(((a + b) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
                  (b - a, y1 - y0, z1 - z0), m, bevel=bevel, seg=1, tint=tint,
                  taper=taper, taper_axis='Y', skew=(0, skew),
                  shade=shade + r.uniform(-var, var))


def slab_mat(key, pale=.52):
    """PUBLIC: the same dressed-slab material draw the walls' three horizontals
    use, so a corner's cap / band / head stone is out of the same bag."""
    r = rng(f"sw/slabmat/{key}")
    return "stone_pale" if r.random() < pale else "stone_warm"


def _footing(p, seed, op=None, long=.44, sty="rubble"):
    """Battered plinth: bigger, tighter-jointed blocks standing 26 mm prouder
    than the walling above, closed by a chamfered cap. Both references start the
    stone storey with one ("big stones at the bottom, smaller ones packed into
    the gaps"), and it is a HORIZONTAL -- which is what a flat coursed wall needs
    to stop it reading as wallpaper. Two .25 courses, so the blocks down here are
    frankly bigger than the walling above rather than merely prouder, and they
    are laid in the SAME STYLE as the wall above them: a cobble bay gets a
    plinth of big rounded boulders, an ashlar bay gets dressed footing blocks."""
    # tilt NEGATIVE, i.e. biased to lie back rather than to stand out: the
    # plinth's job is to be one clean projecting mass under its cap, and a stone
    # here that tipped forward would pass the cap's own -.050 nose and read as a
    # broken plinth. `low` is halved too -- these are dressed blocks on a tight
    # joint, not rubble.
    st = _sty(sty)
    _blocks(p, ROWS_P, seed, op=op, depth=PROUD_PL, plinth=True, sty=st,
            long=long, small=.10, split=.06, warm=st["warm"] + .06,
            pale=st["pale"] + .02, dark=.012, var=.055, tall=.55,
            tall_wide=(.36, .60), rl=RL_PLINTH, bite_lo=True, tilt=-TILT * .8,
            low=st["low"] * .5)
    z0 = PLINTH_Z - PLINTH_CAP
    spans = op.spans(z0, PLINTH_Z, op.sur + .020) if op is not None else [(-HX, HX)]
    _slabs(p, spans, z0, PLINTH_Z, *SLAB_CAP_Y, "pcap", per_m=1.5, taper=.86,
           skew=.012, bevel=.010)


def _band(p, op=None, sill_half=None):
    """The sill string course at 1.05 = OPENINGS.win_ground's sill. On EVERY
    piece, at the same z, projection and depth -- that is the point."""
    if op is None:
        spans = [(-HX, HX)]
    elif sill_half is not None:
        spans = [(-HX, -(sill_half + .020)), (sill_half + .020, HX)]
    else:
        spans = op.spans(BAND_Z0, SILL_Z, op.sur + .020)
    _slabs(p, spans, BAND_Z0, SILL_Z, *SLAB_BAND_Y, "band", per_m=1.5, taper=.90,
           skew=.010, bevel=.010)


def _head(p):
    """Wall-head course: flat slabs across the full thickness, the way ref3's
    stone storey is finished off under the timber above. The core stops 4 mm
    inside it and the lining 4 mm below it, so it owns the wall's top plane."""
    _slabs(p, [(-HX, HX)], HEAD_Z, H, *SLAB_HEAD_Y, "head", per_m=1.6,
           taper=.98, skew=.006, bevel=.009)


# ------------------------------------------------------------ reveal liners ---
def _jamb(p, op, z0, z1, key, every=1, y0=-.038, y1=REV_D, gap=.016):
    """Dressed jamb up both sides of an opening: uniform-width ashlar, so the
    reveal surface at x = +-R belongs to the LINER and nothing else.

    ITS JOINTS LAND ON THE WALL'S BED LINES (every `every`-th one), not on an
    even division of its own height. A jamb is bonded into the walling beside
    it; when its joints fell wherever h/n put them, the course running up to the
    surround met a stone face with a joint 40 mm above or below its own bed, and
    that little stagger is visible all the way up an opening. Bigger stones than
    the field, on the field's beds -- which is what a jamb actually is."""
    r = rng(f"sw/jamb/{key}")
    inner = [z for z in BEDS if z0 + .13 < z < z1 - .13][::max(1, every)]
    zs = [z0] + inner + [z1]
    n = len(zs) - 1
    for sx in (-1, 1):
        for i in range(n):
            a = zs[i] + (gap / 2 if i else 0.0)
            b = zs[i + 1] - (gap / 2 if i < n - 1 else 0.0)
            q = r.random()
            m = "stone_pale" if q < .55 else ("stone_warm" if q < .82 else "stone")
            p.box((sx * (op.R + op.sur / 2), (y0 + y1) / 2, (a + b) / 2),
                  (op.sur, y1 - y0, b - a), m, bevel=.008, seg=1, tint=.055,
                  shade=1.02 + r.uniform(-.07, .07))


def _ring(p, op, key, y0=-.038, y1=REV_D, gap=.007):
    """Voussoir ring. `ri` is solved so each wedge's inner CHORD lands exactly on
    the opening radius: pass r_out = R + sur and the polygon's flats cut 10 mm
    INTO the opening, which is how the wall's arch and the window insert's arch
    ended up fighting for the same 20 mm of clearance."""
    d = pi / op.segs
    ri = op.R / cos((d - 2 * gap) / 2)
    r = rng(f"sw/ring/{key}")
    step = 180.0 / op.segs
    for i in range(op.segs):
        q = r.random()
        m = "stone_pale" if q < .58 else ("stone_warm" if q < .84 else "stone")
        p.arch((0, (y0 + y1) / 2, op.spring), ri + op.sur, y1 - y0, m,
               thickness=op.sur, segs=1, span=step, start=i * step, tint=.06,
               tint_seed=f"{key}/{i}", bevel=.007, wedge_gap=gap)


def _keystone(p, op, w=.18, h=.155, y0=-.054, y1=.140):
    """The oversized keystone both refs put over an arch. Sits just ABOVE the
    crown, never below it: below it would intrude into the opening (which is what
    made the window insert's arch and this one fight), and exactly on it would be
    coplanar with the crown voussoir's horizontal inner chord."""
    p.box((0, (y0 + y1) / 2, op.z1 + .014 + h / 2), (w, y1 - y0, h), "stone_pale",
          bevel=.012, seg=1, tint=.05, shade=1.06)


def _sill(p, op, half, y0=-.052, y1=REV_D):
    """The band, thickened under the window into a projecting sill. Its top face
    IS the reveal floor, at exactly OPENINGS.win_ground's sill."""
    p.box((0, (y0 + y1) / 2, (BAND_Z0 + SILL_Z) / 2),
          (2 * half, y1 - y0, SILL_Z - BAND_Z0), "stone_pale", bevel=.014,
          seg=1, tint=.05, skew=(0, .010), shade=1.03)


def _threshold(p, op, h=.110, y0=-.052, y1=REV_D):
    """Heavy threshold slab in the foot of a doorway; the jambs stand on it."""
    p.box((0, (y0 + y1) / 2, h / 2), (2 * (op.R + CLR - BITE), y1 - y0, h),
          "stone_pale", bevel=.014, seg=1, tint=.05, skew=(0, .008), shade=1.04)


# ============================================================ THE ARCADE =====
# ROUND 13: AN ARCADED UNDERCROFT, WHICH THIS FAMILY COULD NOT BUILD AT ALL.
#
# Four of the new references open the ground floor into an ARCADE -- a run of
# arches with the storey above carried on them, used for stabling, market stalls
# and tables (r9 is the clearest: lit arches, tables under them, cobbles running
# straight through; r11 runs the same idea under a multi-gable roofline; r6/r7,
# the 3D build, carry the jetty on dressed stone piers). Everything this family
# offered was a SOLID wall with a punched opening, and a punched opening is not
# an arcade however wide you cut it: an arcade is open to the ground, it is a
# hole THROUGH the wall rather than a recess in it, and the wall above it is
# carried on piers rather than standing on itself.
#
# THE PROPORTION IS READ OFF r9: the arch is wide and generous and the pier
# between two bays is comparatively slim. On the kit's 2 m module that is a
# 1.54 m clear opening on a 0.46 m pier (3.3 : 1), which is as slim as 0.36 m of
# masonry can honestly carry a storey.
#
# WHAT AN ARCADE BAY HAS TO OBEY, and every line of this section is one of them:
#
#  1. IT IS INTERCHANGEABLE WITH A SOLID BAY. The wall head (HEAD_Z, y -.040..T),
#     the plinth (PLINTH_Z, PLINTH_CAP, nose -.050), the sill band (BAND_Z0,
#     SILL_Z, nose -.030) and every bed line in BEDS land at exactly the z, the
#     projection and the depth they land at on SM_Wall_StoneRubble_2m_A -- the
#     dressed horizontals are laid by the family's OWN _slabs/_seam_slab on the
#     family's own keys, so the plinth cap and the string course run across the
#     bay edge as ONE slab. A storey sitting on a run of arcade and solid bays
#     sits flat. demo() puts one of each side by side on purpose.
#
#  2. TWO BAYS SHARE A PIER. Each bay carries HALF of it (ARC_HALF) at each seam
#     and every stone in that half is keyed on its BED ALONE -- never on the
#     piece -- so both meshes draw the same block and the pier reads as one pier.
#     That is round 6's seam-stone rule applied to a dressed element. It also
#     means SM_Wall_StoneArcadePier, the end respond, continues the same bond.
#
#  3. THE OPENING IS OPEN, SO THE REVEAL AND THE SOFFIT ARE VISIBLE SURFACES.
#     Everything that touches the opening is a THROUGH stone -- the pier blocks
#     and the voussoirs run in ONE solid from the face plane back to ARC_BACK,
#     16 mm inside the plaster lining -- so there is no depth at which the eye
#     runs off dressed stone onto a backing plate. (The window and cellar-arch
#     pieces get away with a liner only REVEAL-deep because you cannot walk
#     through them; an arcade you can.)
#
# THE DEPTH LADDER, arcade only. The wall ladder above is untouched:
#     y = -.058/-.046  hood mould / impost noses
#     y = -.050        the plinth cap's nose -- the family's number, unchanged
#     y = -.042  ARC_FACE_PL  the pier's PLINTH blocks (the batter)
#     y = -.030        the arch ring's face
#     y = -.024  ARC_FACE     the pier shaft's face: 14 mm proud of the rubble
#                       field's mean crown, which is what makes a dressed pier
#                       read as a pier rather than as a patch of pale wall
#     y = -.008  PIER_Y0 the pier's joint filler -- what you see in a BED JOINT,
#                       16 mm behind the face. A dressed joint is a LINE; the
#                       60 mm the rubble field runs (MORT_Y) would read as a slot
#     y =  .140  BED    the spandrel's core, as on every other piece
#     y =  .320  PIER_Y1 ...the joint filler's back
#     y =  .334  SKIM_Y the lining, which owns y = T for the whole piece
#     y =  .350  ARC_BACK  every through stone's back, 16 mm inside the lining
#     y =  .360  T      the lining, and NOTHING else
# and the pier's filler stops INSIDE the impost rather than butting it, so the
# one horizontal interface in the piece is buried in a solid instead of being a
# shared plane. Measured with check_zfight: 0 cm2 -- and two of these numbers
# were MOVED by that measurement, not chosen (see PIER_Y1 and pier_run's
# `over`).
#
# WHY THE RING IS EXACTLY AS THICK AS THE PIER IS WIDE (ARC_SUR == ARC_HALF): an
# arch is its pier turned over. It also means the extrados lands EXACTLY on the
# bay seam at the springing, for both profiles, so there is never a sliver of
# unfaced wall beside the springing -- the ring hands the wall face straight to
# the pier below it and to the spandrel coursing above it.

ARC_HALF   = .23      # half-pier carried at EACH bay seam: two bays make .46
ARC_R      = HX - ARC_HALF        # .77   half the clear opening (1.54 wide)
ARC_SUR    = ARC_HALF             # .23   ring thickness == pier width
ARC_SEGS   = 6        # voussoirs per half ring. The arc length works out at
                      # ~.20 m a stone, i.e. the family's own COURSE, so the
                      # voussoirs read as the same masonry turned on its side.
ARC_SPRING = min(BEDS, key=lambda z: abs(z - 1.52))   # 1.5196 -- A BED LINE, so
                      # the impost's top and the springer land on the course grid
ARC_IMP    = .105     # impost height
ARC_LIFT   = .010     # ...and how far its top sits ABOVE the springing, so the
                      # first voussoir's bed joint is buried in it instead of
                      # opening a 4 mm slot straight through the wall
ARC_FACE   = -.024    # the pier shaft's dressed face
ARC_FACE_PL= -.042    # ...and its plinth's (the batter), inside the cap's -.050
ARC_JNT    = .014     # the pier's bed joint: dressed work, not rubble
ARC_BACK   = SKIM_Y + LAP        # .350  every through stone's back
PIER_Y0    = -.008    # the pier's joint filler, front...
PIER_Y1    = SKIM_Y - .014   # .320 ...and back, AND THAT NUMBER IS MEASURED. It
                      # was T - .014 = .346 for one round, which is 4 mm in front
                      # of ARC_BACK, where every through stone's back face is --
                      # and check_zfight duly found 851 cm2 of one pier block's
                      # back against the filler's on SM_Wall_StoneArcadePier
                      # (p.wobble moves a 2 m plate and a 200 mm block by up to
                      # 3 mm each, so 4 mm of designed separation is inside the
                      # noise; this family measured the threshold at ~10 mm twice
                      # already, see MORT_T). There is no room BEHIND the stones
                      # -- the lining's front is only 16 mm back from them -- so
                      # the filler stops 14 mm in FRONT of the lining instead:
                      # 30 mm clear of the stones, 14 mm clear of the lining, and
                      # the 14 mm of empty joint left behind it is closed by the
                      # lining itself, which is opaque and covers the whole back
                      # of the pier.
PIER_IN    = .014     # ...and how far it sits inside the reveal, so the joint
                      # reads from the reveal too and the filler can never reach
                      # the surface the eye follows through the arch
SLAB_IN    = .016     # how far the plinth cap and the string course project PAST
                      # the reveal into the opening. Not decoration: it keeps
                      # their end faces off the plane of the pier's reveal (which
                      # they would otherwise z-fight against in the bite zones),
                      # and a pier base wider than its shaft is what a base IS.


class Arc(Op):
    """An ARCADE opening: full height, open to the ground, springing from a pier
    either side, with the storey above carried on the piers.

    `d` is the two-centred offset. 0 draws r9's round head; a positive number
    draws the slightly pointed head of r9's doorway and r11's arcade. BOTH
    PROFILES SPRING FROM THE SAME LINE AT THE SAME WIDTH and both put their
    extrados exactly on the bay seam at the springing, so the A and B bays
    interchange freely in a run and neither leaves a strip of unfaced wall.

    It is an Op subclass because _blocks(), mortar_field() and the seam rule ask
    an opening exactly three questions -- .sur, .spans() and .hw() -- and the
    right way to add a new kind of hole to this family is to answer them, not to
    fork the walling."""

    def __init__(self, d=0.0, r=ARC_R, spring=ARC_SPRING, sur=ARC_SUR,
                 segs=ARC_SEGS):
        self.R = r                       # half the clear opening
        self.d = d                       # two-centred offset (0 = round head)
        self.rad = r + d                 # the generating radius
        self.sur = sur
        self.segs = segs
        self.z0 = 0.0
        self.spring = spring
        self.rise = sqrt(max(self.rad * self.rad - d * d, 0.0))
        self.z1 = spring + self.rise     # the crown of the intrados

    # ---- the profile --------------------------------------------------------
    def rise_at(self, extra=0.0):
        rr = self.rad + extra
        return sqrt(max(rr * rr - self.d * self.d, 0.0))

    def hw(self, z, extra=0.0):
        """Half-width of the void, inflated by `extra`, at height z. Below the
        springing it is the reveal; above it, the two-centred arc."""
        if z <= self.spring:
            return self.R + extra
        rr = self.rad + extra
        dz = z - self.spring
        if dz >= rr:
            return 0.0
        return max(0.0, sqrt(rr * rr - dz * dz) - self.d)

    def spans(self, zb, zt, extra, cut=.020):
        """The x runs in a course that are clear of the arch, evaluated at the
        course TOP (Op's rule: what overhangs at the course bottom is hidden
        behind the ring, which stands 20 mm proud of the field).

        Two differences from Op.spans, both because this opening reaches the
        ground: a course entirely BELOW the springing belongs to the pier and
        gets no walling at all, and the cutoff is finer (20 mm, not 30) because
        the courses just above the springing are slivers between the extrados
        and the bay edge -- and a sliver left unwalled here is a dark groove at
        the seam, which is the one thing this family has spent six rounds
        killing. A sliver gets the seam stone, clipped, and the neighbour draws
        the same one."""
        if zt <= self.spring + 1e-6:
            return []
        hw = self.hw(zt if zb >= self.spring else self.spring, extra)
        if hw >= HX - cut:
            return []
        return [(-HX, -hw), (hw, HX)] if hw > 1e-6 else [(-HX, HX)]

    def theta(self):
        """Degrees of arc in ONE half, springing to crown. 90 for a round head."""
        return degrees(atan2(self.rise, self.d)) if self.d > 1e-9 else 90.0

    def imp_z0(self):
        return self.spring + ARC_LIFT - ARC_IMP

    def theta_at(self, extra=0.0):
        """Degrees of arc in one half at radius rad + `extra`, springing to the
        point where that arc crosses the centre line. It is NOT theta() for a
        two-centred arch: the extrados of a pointed arch meets its twin higher
        AND at a smaller angle than the intrados does, and sampling both edges to
        the intrados angle is what puts a notch in the top of a hood mould."""
        rr = self.rad + extra
        return degrees(acos(clamp(self.d / rr, -1.0, 1.0))) if rr > 1e-9 else 90.0

    def band(self, r0, r1, n=9):
        """(x,z) polygon of a BAND running round the arch between the radii
        rad+r0 and rad+r1 -- a hood mould, a label, a second order. One closed
        polygon rather than a run of wedges: a moulding has no joints, and as one
        prism it costs a tenth of what the same band costs as voussoirs (measured
        1944 tris as 18 wedges, 190 as this)."""
        def edge(off, side, a0, a1):
            c = -side * self.d
            rr = self.rad + off
            return [(c + rr * cos(radians(lerp(a0, a1, i / n))),
                     self.spring + rr * sin(radians(lerp(a0, a1, i / n))))
                    for i in range(n + 1)]
        t1, t0 = self.theta_at(r1), self.theta_at(r0)
        # round the band as one loop: OUT along the top (left springing, over the
        # crown, down to the right springing) and BACK along the underside.
        loop = (edge(r1, -1, 180.0, 180.0 - t1) + edge(r1, +1, t1, 0.0)
                + edge(r0, +1, 0.0, t0) + edge(r0, -1, 180.0 - t0, 180.0))
        return _dedupe(loop, 1e-5)

    def outline(self, zt, extra, z0=0.0, n=11, hx=HX):
        """(x,z) polygon of the bay between z0 and zt, minus the void inflated by
        `extra`. One polygon, because an opening that reaches the ground leaves a
        U rather than a hole (see Op.outline for the two-piece case)."""
        top = self.spring + self.rise_at(extra)
        lim = hx - .002
        zc = max(z0, self.spring)
        edge = [(-min(self.hw(z0, extra), lim), z0)]
        if z0 < self.spring - 1e-6:
            edge.append((-min(self.hw(self.spring, extra), lim), self.spring))
        for i in range(1, n + 1):
            z = lerp(zc, top, i / n)
            edge.append((-min(self.hw(z, extra), lim), min(z, zt - .002)))
        right = [(-u, v) for (u, v) in reversed(edge[:-1])]
        return [[(-hx, z0)] + edge + right + [(hx, z0), (hx, zt), (-hx, zt)]]


# ---------------------------------------------------------- arcade shells -----
def _arc_core(p, arc, extra=ARC_SUR - .020):
    """The core, exactly where every other piece in the family puts it (BED to
    CORE_Y1). Its void stops 20 mm INSIDE the ring's extrados, so the ring
    covers it at every angle and nothing of it is ever visible through the arch;
    its legs run down inside the piers, where the pier stones are already 100 mm
    in front of it and the lining is behind it."""
    poly = arc.outline(HEAD_Z + LAP, extra)[0]
    p.prism(poly, CORE_Y1 - BED, "stone_dark", axis='Y',
            at=(0, (BED + CORE_Y1) / 2, 0), bevel=0, tint=.03, shade=CORE_SHADE)


def _arc_skim(p, arc, lap=.014):
    """The plaster lining, and on an arcade it is the ONE solid that owns y = T.

    Its void is the opening LAPPED INWARD by `lap`, i.e. the plaster returns 14 mm
    over the arris of the reveal and the soffit, the way plaster actually meets
    masonry. That single sign is what makes the arcade's inner face buildable:
    every through stone stops at ARC_BACK, 16 mm inside this plate, so the lining
    is never in the same plane as anything else, and the reveal shows dressed
    stone for 350 of its 360 mm."""
    poly = arc.outline(HEAD_Z - BITE, -lap, z0=.008, hx=HX - .005)[0]
    p.prism(poly, T - SKIM_Y, "plaster_dim", axis='Y',
            at=(0, (SKIM_Y + T) / 2, 0), bevel=0, tint=.04)


def _pier_filler(p, x0, x1, zt):
    """What you see in the pier's BED JOINTS: a filler standing 16 mm behind the
    dressed faces and 14 mm inside the reveal, so a joint is a fine dark line on
    three faces of the pier instead of a slot through it. It is the dressed-work
    equivalent of mortar_field, at a dressed joint's depth."""
    # keyed on NOTHING: two bays put half of this filler each, and a shade drawn
    # per piece would be a tonal step visible down every bed joint in the pier.
    r = rng("sw/pierfill")
    # `stone`, not stone_dark, and lifted: a dressed bed joint is 14 mm wide and
    # 16 mm deep, and at stone_dark x MORT_SHADE it rendered as a row of black
    # slots -- a hole, not a joint. The rubble field can afford that tone because
    # its joints are 60 mm down a shadowed recess between two domed stones; this
    # one is a line you look straight into.
    p.plate(((x0 + x1) / 2, (PIER_Y0 + PIER_Y1) / 2, zt / 2),
            (x1 - x0, PIER_Y1 - PIER_Y0, zt), "stone", tint=.04,
            shade=.90 + r.uniform(-.05, .05))


# ------------------------------------------------------------- the pier -------
def pier_run(p, x0, x1, z0, z1, face=ARC_FACE, y1=ARC_BACK, joint=ARC_JNT,
             bite_lo=False, bite_hi=False, pale=.52, beds=None, over=(0.0, 0.0)):
    """PUBLIC: a run of the arcade pier's dressed THROUGH stones, laid on the
    family's own bed lines between two arbitrary x bounds.

    KEYED ON THE BED ALONE. The half-pier an arcade bay carries at one seam and
    the half its neighbour carries at the other are then the same stone --  same
    material, same projection, same lean -- so the joint between two bays
    disappears and the pier reads as one pier. SM_Wall_StoneArcadePier is the
    same call at its own width, so an end respond continues the bond too.

    One stone per course across the whole pier is not a simplification: at 460 mm
    on a 230 mm course that IS the stone a mason would use, and it is what r6 and
    r9 both show -- the pier is the one place in a rubble wall where the blocks
    are big, square and pale.

    `over` runs the block PAST a bay seam so clamp_to_seams cuts it dead flat
    there, exactly as _seam_slab does. It is not a detail: a block that stops ON
    the seam keeps its 11 mm arris, two bays put two of them back to back, and
    the pier grows a 22 mm V groove down its centre with the joint filler showing
    at the bottom of it -- measured on the first render, and it read as a split
    pier. Cut, the two halves weld into one block."""
    beds = beds or BEDS
    zs = [z0] + [z for z in beds if z0 + .06 < z < z1 - .06] + [z1]
    n = len(zs) - 1
    for i in range(n):
        a = (zs[i] - LAP) if (i == 0 and bite_lo) else zs[i] + joint / 2
        b = (zs[i + 1] + LAP) if (i == n - 1 and bite_hi) else zs[i + 1] - joint / 2
        r = rng(f"sw/pier/{zs[i]:.4f}")
        q = r.random()
        m = "stone_pale" if q < pale else ("stone_warm" if q < pale + .28 else "stone")
        y0 = face + r.uniform(-.007, .007)
        # TINT 0, AND THAT IS THE SEAM RULE AGAIN. _paint's per-primitive jitter
        # is drawn from the PIECE's rng in emit order, so two bays that draw the
        # same pier stone from the same bed key would still tint it differently
        # -- which put a full-height tonal step down the middle of every pier the
        # first time this was rendered. The value variation is the bed key's, so
        # both halves get the same one.
        u0, u1 = x0 - over[0], x1 + over[1]
        p.box(((u0 + u1) / 2, (y0 + y1) / 2, (a + b) / 2),
              (u1 - u0, y1 - y0, b - a), m, bevel=.011, seg=1, tint=0.0,
              taper=.988, taper_axis='Y', skew=(0, r.uniform(-.005, .005)),
              shade=1.02 + r.uniform(-.045, .045))


def _impost(p, x0, x1, arc, nose=-.052):
    """The impost the arch springs from: a chamfered block capping the pier, its
    top ARC_LIFT above the springing so the springer's bed joint is buried in it.
    r9 puts one on every pier -- it is what makes the springing line read as a
    line rather than as the point where the wall happens to start curving.

    ONE PROFILE FOR BOTH VARIANTS, keyed on the springing alone like every other
    stone in the pier. B carried a plain slab for one round, which looked fine on
    its own bay and put a chamfered half and a square half either side of every
    pier where an A bay met a B bay -- the two variants have to interchange, and
    that means everything BELOW the springing is common to both. The variants
    differ in the head: A is round with a keystone, B is pointed under a hood."""
    z1 = arc.spring + ARC_LIFT
    h = ARC_IMP
    r = rng(f"sw/impost/{z1:.4f}")
    prof = [(nose, 0.0), (ARC_BACK, 0.0), (ARC_BACK, -h),
            (nose + .044, -h), (nose, -h * .58)]
    p.prism(prof, x1 - x0, slab_mat(f"imp/{z1:.4f}"), axis='X',
            at=((x0 + x1) / 2, 0.0, z1), bevel=.009, seg=1, tint=0.0,
            shade=1.05 + r.uniform(-.04, .04))


def _pier_slab(p, sx, z0, z1, y0, y1, key, taper=.90, skew=.010, bevel=.010,
               shade=.93, pale=.70, joint=.014):
    """One dressed horizontal across a half-pier -- the plinth cap or the sill
    string course. It is the family's OWN _seam_slab across the bay edge, on the
    family's own key, so it is bit-identical to the slab the neighbouring bay
    (solid or arcade) lays there; anything the seam slab does not reach is closed
    with one filler block on a normal joint."""
    x_in = sx * (ARC_R - SLAB_IN)
    reach = _seam_slab(p, sx, z0, z1, y0, y1, key, taper, skew, bevel, shade,
                       pale, HX - abs(x_in))
    a = sx * (HX - reach)
    if abs(x_in - a) > .026:
        r = rng(f"sw/pierslab/{key}/{z0:.4f}/{sx}")
        m = "stone_pale" if r.random() < pale else "stone_warm"
        lo, hi = sorted((a + sx * joint, x_in))
        p.box(((lo + hi) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
              (hi - lo, y1 - y0, z1 - z0), m, bevel=bevel, seg=1, tint=0.0,
              taper=taper, taper_axis='Y', skew=(0, skew),
              shade=shade + r.uniform(-.05, .05))


# -------------------------------------------------------------- the arch ------
def _arch_ring(p, arc, key, y0=-.030, y1=ARC_BACK, segs=None, gap=.0055,
               jit=.008, pale=.46, bevel=.009):
    """The voussoirs, laid as THROUGH stones: one solid from the face plane to
    ARC_BACK, so the ring IS the soffit and the soffit cannot show a backing
    plate at any depth.

    `ri` is solved so each wedge's inner CHORD lands exactly on the opening
    (the same arithmetic as _ring: a polygon inscribed on the radius eats 10 mm
    out of the opening at every joint), and the extrados is pinned to
    rad + arc.sur so it lands exactly on the bay seam at the springing."""
    segs = segs or arc.segs
    th = arc.theta()
    step = th / segs
    ri = arc.rad / cos((radians(step) - 2 * gap) / 2)
    r_out = arc.rad + arc.sur
    r = rng(f"sw/arcring/{key}")
    for side in (-1, 1):
        cx = -side * arc.d
        base = (180.0 - th) if side < 0 else 0.0
        for i in range(segs):
            q = r.random()
            m = ("stone_pale" if q < pale else
                 ("stone_warm" if q < pale + .28 else "stone"))
            yy = y0 + r.uniform(0, jit)
            p.arch((cx, (yy + y1) / 2, arc.spring), r_out, y1 - yy, m,
                   thickness=r_out - ri, segs=1, span=step,
                   start=base + step * i, tint=.05,
                   tint_seed=f"{key}/{side}/{i}", bevel=bevel, wedge_gap=gap)


def _hood(p, arc, key, r0=.150, r1=.214, y0=-.058, y1=.100, n=9, pale=.62):
    """The hood mould / label over an arch (r9 puts one over its doorway; it is
    the cheapest way to make a second arch profile read as a second mason).

    ONE continuous band, not a ring of wedges: drawn stone by stone it read as a
    ragged extra ring of rubble stuck to the face. It never passes the ring's own
    extrados, which is already on the bay seam, and its foot is buried in the
    impost so it stops as a label rather than running into the ground."""
    r = rng(f"sw/hood/{key}")
    m = "stone_pale" if r.random() < pale else "stone_warm"
    p.prism(arc.band(r0, r1, n), y1 - y0, m, axis='Y', at=(0, (y0 + y1) / 2, 0),
            bevel=.008, seg=1, tint=.04, shade=1.02 + r.uniform(-.04, .04))


def _arc_keystone(p, arc, w=.225, h=.205, y0=-.056, y1=ARC_BACK):
    """The oversized keystone r9 puts at the crown of its round arches. It sits
    just ABOVE the intrados crown and inside the ring's own depth, so what shows
    is its 24 mm of extra projection, not a block stuck on the wall."""
    r = rng(f"sw/arckey/{arc.spring:.3f}")
    p.box((0, (y0 + y1) / 2, arc.z1 + .012 + h / 2), (w, y1 - y0, h),
          "stone_pale", bevel=.012, seg=1, tint=.05, taper=.96, taper_axis='Y',
          shade=1.07 + r.uniform(-.04, .04))


# -------------------------------------------------------------- the bay -------
def arcade_bay(p, arc, seed, sty="rubble", **kw):
    """PUBLIC: the ENTIRE arcade-bay build -- lining, core, two half-piers,
    plinth, cap, string course, imposts, arch, spandrel and wall head -- on a
    Part somebody else owns, exactly as plain_bay() does for a solid bay.

    A and B are this function with two arch profiles, which is the cheapest
    possible guarantee that they share every bed line, every projection, every
    depth and the same springing line and opening width, i.e. that they
    interchange in a run."""
    _arc_core(p, arc)
    _arc_skim(p, arc)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * HX, sx * ARC_R))
        f0, f1 = sorted((sx * HX, sx * (ARC_R + PIER_IN)))
        _pier_filler(p, f0, f1, arc.spring + .004)
        ov = (.030, 0.0) if sx < 0 else (0.0, .030)   # cut flat on the bay seam
        pier_run(p, x0, x1, 0.0, ROWS_P[-1][1], face=ARC_FACE_PL, bite_hi=True,
                 over=ov)
        pier_run(p, x0, x1, PLINTH_Z, BAND_Z0, bite_lo=True, bite_hi=True, over=ov)
        pier_run(p, x0, x1, SILL_Z, arc.imp_z0(), bite_lo=True, bite_hi=True,
                 over=ov)
        _impost(p, x0, x1, arc)
        _pier_slab(p, sx, PLINTH_Z - PLINTH_CAP, PLINTH_Z, *SLAB_CAP_Y, "pcap",
                   taper=.86, skew=.012)
        _pier_slab(p, sx, BAND_Z0, SILL_Z, *SLAB_BAND_Y, "band", taper=.90,
                   skew=.010)
    _arch_ring(p, arc, seed)
    _blocks(p, ROWS_B, seed + 2, op=arc, sty=sty, **kw)
    _head(p)


def _pier_cap(p, x0, x1, z0, z1, y0, y1, key, taper=.94, skew=.008, bevel=.010,
              shade=.93, pale=.70):
    """One dressed horizontal right across a standalone pier -- no seam slab,
    because this piece's x planes are its own ends rather than a bay seam. Same
    z, same nose, same material bag as the run it terminates."""
    r = rng(f"sw/piercap/{key}/{z0:.4f}")
    p.box(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
          (x1 - x0, y1 - y0, z1 - z0), slab_mat(f"{key}/{z0:.3f}", pale),
          bevel=bevel, seg=1, tint=0.0, taper=taper, taper_axis='Y',
          skew=(0, skew), shade=shade + r.uniform(-.05, .05))


# -------------------------------------------------------------------- pieces --
def plain_bay(p, seed, plinth_long=.44, sty="rubble", **kw):
    """PUBLIC: the ENTIRE plain-wall build -- core, lining, plinth, courses, sill
    band, courses, wall head -- on a Part somebody else owns.

    wall_a/b/c are this function with three sets of dice, which is the cheapest
    possible guarantee that they share every bed line, every projection and every
    depth. corners.py's demo also builds its context bays with it: the question
    that demo has to answer is whether a corner continues the wall it terminates,
    and a stand-in wall with coursing of its own could only ever prove that the
    stand-in was wrong. It did, for six rounds -- the corners demo showed the
    quoins against a field of small round cobbles that exists nowhere in the kit.

    `sty` picks the masonry style (see STYLES). Everything OUTSIDE the facing --
    core, lining, plinth level, sill band, wall head, every bed line -- is
    identical whichever style is asked for, which is what lets a cobble bay stand
    next to an ashlar one with no step and no seam."""
    _core(p, HEAD_Z + LAP)
    _skim(p, HEAD_Z - BITE)
    _footing(p, seed, long=plinth_long, sty=sty)
    _blocks(p, ROWS_A, seed + 1, sty=sty, **kw)
    _band(p)
    _blocks(p, ROWS_B, seed + 2, sty=sty, **kw)
    _head(p)


def wall_a():
    """Plain coursed bay: plinth, a course, the sill band, seven courses to the
    wall head."""
    p = Part("SM_Wall_StoneRubble_2m_A", budget="wall", seams=SEAMS)
    plain_bay(p, 11)
    _wob(p)
    return p.finish()


def wall_b():
    """Same grid, different rhythm: big-block wall. A quarter of the stones are
    boulders and half again as many span two courses, so next to A the coursing
    reads as the same wall built by a mason with a bigger cart."""
    p = Part("SM_Wall_StoneRubble_2m_B", budget="wall", seams=SEAMS)
    plain_bay(p, 21, plinth_long=.52, long=.26, small=.12, split=.10, pale=.20,
              warm=.28, tall=.80, tall_wide=(.34, .58))
    _wob(p)
    return p.finish()


def wall_c():
    """Warm variant: warmer mix, harder value patches, more small packers worked
    in round the big stones, and a couple of blocks fallen out to show the
    mortar bed behind."""
    p = Part("SM_Wall_StoneRubble_2m_C", budget="wall", seams=SEAMS)
    plain_bay(p, 31, plinth_long=.55, warm=.40, pale=.13, long=.13, small=.26,
              split=.20, skip=.022, var=.080, tall=.40)
    _wob(p)
    return p.finish()


def wall_cobble_a():
    """ROUNDED RUBBLE / COBBLE -- ref1's ground floor, and the style this family
    did not have. Near-equant water-worn stones off a river bed, packed tight on
    a 20 mm joint, every one domed hard and not a dressed face anywhere. Same
    plinth, same sill band, same wall head, same bed lines as every other piece
    here: only the stones are different."""
    p = Part("SM_Wall_StoneCobble_2m_A", budget="wall", seams=SEAMS)
    plain_bay(p, 71, plinth_long=.46, sty="cobble")
    _wob(p)
    return p.finish()


def wall_cobble_b():
    """The same cobbling from a coarser bed: more big water-worn boulders with
    small stones wedged into the gaps they leave, which is the pattern the
    reference actually shows."""
    p = Part("SM_Wall_StoneCobble_2m_B", budget="wall", seams=SEAMS)
    plain_bay(p, 81, plinth_long=.54, sty="cobble", long=.19, small=.22,
              tall=.46, warm=.34, pale=.11)
    _wob(p)
    return p.finish()


def wall_ashlar_a():
    """SQUARED / DRESSED ASHLAR -- ref3's ground floor. Rectangular blocks on a
    13 mm joint with barely 15 mm of face relief on them, laid to a regular
    course. THE REGULARITY IS THE MATERIAL, not the round-7 defect: this is
    quarried stone worked square by a mason with a chisel, and next to the cobble
    bay it should read as a different trade rather than as a better or worse
    version of the same one. Its quoins come from corners.py, which lands
    SM_Corner_StoneQuoin on these very beds."""
    p = Part("SM_Wall_StoneAshlar_2m_A", budget="wall", seams=SEAMS)
    plain_bay(p, 91, plinth_long=.34, sty="ashlar")
    _wob(p, WOB * .45)          # dressed work does not wander
    return p.finish()


def wall_win():
    """Ground-floor window wall -- OPENINGS.win_ground in a dressed ashlar
    surround sitting on the sill string course (ref2, stone_arch crop). The WALL
    owns the arch; the windows family drops a frame + glazing into the reveal."""
    p = Part("SM_Wall_StoneWindow_2m", budget="wall", seams=SEAMS)
    op = Op("win_ground", sur=.155, segs=7)
    _core(p, HEAD_Z + LAP, op)
    _skim(p, HEAD_Z - BITE)
    _blank(p, op)
    _footing(p, 41, op=op, long=.50)
    _blocks(p, ROWS_A, 42, op=op)
    _band(p, op, sill_half=.625)
    _blocks(p, ROWS_B, 43, op=op, pale=.20, warm=.30)
    _head(p)
    # ---- the dressed reveal: sill, jambs, voussoir ring, keystone
    _sill(p, op, .625)
    _jamb(p, op, SILL_Z - LAP, op.spring + .02, 44)
    _ring(p, op, 45)
    _keystone(p, op)
    _wob(p)
    return p.finish()


def wall_arch():
    """Arched cellar opening -- ref1's big timber-doored arch. Voussoir ring on
    dressed jambs standing on a threshold slab; the doors family provides the
    leaf. Carries the SAME plinth, sill band and wall head as every other piece
    in the family, so it can sit next to any of them."""
    p = Part("SM_Wall_StoneArch_2m", budget="wall", seams=SEAMS)
    op = Op("door_cellar", sur=.205, segs=9)
    _core(p, HEAD_Z + LAP, op)
    _skim(p, HEAD_Z - BITE)
    _blank(p, op)
    _footing(p, 51, op=op, long=.50)
    _blocks(p, ROWS_A, 52, op=op)
    _band(p, op)
    _blocks(p, ROWS_B, 53, op=op, warm=.32, pale=.18)
    _head(p)
    _threshold(p, op)
    _jamb(p, op, .110 - LAP, op.spring + .02, 54, every=2)
    _ring(p, op, 55)
    _keystone(p, op, w=.22, h=.185)
    _wob(p)
    return p.finish()


def wall_plinth():
    """Half-height wall: yard / garden / plinth run, capped with flat coping
    slabs. Its courses ARE the tall walls' courses -- plinth, band and bed lines
    all land on the same z -- so it stacks under any 2 m piece or runs alongside
    one without a step."""
    hh = H / 2
    rows_b = [rr for rr in ROWS_B if rr[1] <= hh - .10]
    cope0 = rows_b[-1][1] if rows_b else SILL_Z
    p = Part("SM_Wall_StonePlinth_2m", budget="wall",
             seams=dict(x=(-HX, HX), y=(0, T), z=(0, hh)))
    _core(p, cope0 + LAP)
    _skim(p, cope0 - BITE)
    _footing(p, 61, long=.50)
    _blocks(p, ROWS_A, 62)
    _band(p)
    _blocks(p, rows_b, 63)
    _slabs(p, [(-HX, HX)], cope0, hh, SLAB_CAP_Y[0], T, "cope", per_m=1.5, taper=.99,
           skew=.008, bevel=.010)
    _wob(p)
    return p.finish()


def wall_arcade_a():
    """ONE BAY OF OPEN ARCADE, round-headed -- r9's proportion: a wide generous
    arch (1.54 m clear) on a comparatively slim dressed pier (.46 m where two
    bays meet), the wall above it solid, and the opening a genuine HOLE through
    the wall that a horse, a market stall or a table fits under.

    It carries a storey, so the wall head, the plinth, the sill band and every
    bed line are the ones every other piece in this family uses, at the same
    projection: drop it into a run of solid bays and the timber storey above sits
    flat on all of them. The demo puts it hard against the cobble bay to show
    exactly that junction."""
    p = Part("SM_Wall_StoneArcade_2m_A", budget="wall", seams=SEAMS)
    arc = Arc(d=0.0)
    arcade_bay(p, arc, 111)
    _arc_keystone(p, arc)
    _wob(p)
    return p.finish()


def wall_arcade_b():
    """The second bay, so a run of arches does not read as one arch copied.

    SAME SPRINGING LINE, SAME OPENING WIDTH, SAME PIER, SAME IMPOST -- so A and
    B interchange freely and a level artist can alternate them without measuring
    anything. Everything below the springing is common to both, because two bays
    SHARE the pier between them and half of it is drawn in each mesh. What
    differs is the head: a slightly POINTED two-centred arch (r9's doorway and
    r11's arcade both have one) under a proud hood mould that dies onto the
    impost as a label stop, against A's round head and keystone. Read along a
    run, that is two masons rather than one stamp."""
    p = Part("SM_Wall_StoneArcade_2m_B", budget="wall", seams=SEAMS)
    arc = Arc(d=.13, segs=7)
    arcade_bay(p, arc, 121, warm=.34, pale=.14, long=.20)
    # the hood mould: a proud band on the OUTER part of the ring (never past its
    # extrados, which is already on the bay seam), its own coarser voussoir
    # division so its joints do not line up with the ring's, and its foot buried
    # in the impost so it stops as a label rather than running into the ground.
    _hood(p, arc, 122)
    _wob(p)
    return p.finish()


def arcade_pier():
    """THE END OF AN ARCADE RUN: the standalone pier / respond, so a run can
    terminate on a pier instead of being cut off mid-arch.

    It is ARC_PIER wide -- exactly the pier two arcade bays make between them --
    and every stone in it comes out of pier_run() keyed on the BED ALONE, so
    butted against the last bay's half-pier it continues the same bond, the same
    projection and the same material draw. Placement is the obvious one: centre
    it half its width past the last bay's seam (the demo does it at
    x = bay_centre -/+ 1.23), and the run reads pier-arch-pier-arch-pier.

    It is dressed to the wall head rather than stopping at the springing, because
    the end of an arcade is also the end of the wall above it: that is a quoined
    respond, and r6/r7 build exactly this -- a pale ashlar pier with squared
    quoins running the full height of the stone storey, carrying the jetty. It
    also stands alone as a free-standing pier under a beam."""
    hx = ARC_HALF
    p = Part("SM_Wall_StoneArcadePier", budget="wall",
             seams=dict(x=(-hx, hx), y=(0, T), z=(0, H)))
    arc = Arc()
    _pier_filler(p, -hx + PIER_IN, hx - PIER_IN, HEAD_Z + .010)
    ov = (.030, .030)          # both ends butt: no arris, cut flat
    pier_run(p, -hx, hx, 0.0, ROWS_P[-1][1], face=ARC_FACE_PL, bite_hi=True,
             over=ov)
    _pier_cap(p, -hx, hx, PLINTH_Z - PLINTH_CAP, PLINTH_Z, *SLAB_CAP_Y, "pcap",
              taper=.86, skew=.012)
    pier_run(p, -hx, hx, PLINTH_Z, BAND_Z0, bite_lo=True, bite_hi=True, over=ov)
    _pier_cap(p, -hx, hx, BAND_Z0, SILL_Z, *SLAB_BAND_Y, "band", taper=.90,
              skew=.010)
    pier_run(p, -hx, hx, SILL_Z, arc.imp_z0(), bite_lo=True, bite_hi=True,
             over=ov)
    _impost(p, -hx, hx, arc)
    pier_run(p, -hx, hx, arc.spring + ARC_LIFT, HEAD_Z, bite_hi=True, over=ov)
    _pier_cap(p, -hx, hx, HEAD_Z, H, *SLAB_HEAD_Y, "head", taper=.98, skew=.006)
    _wob(p, WOB * .55)
    return p.finish()


def build():
    return [wall_a(), wall_b(), wall_c(),
            wall_cobble_a(), wall_cobble_b(), wall_ashlar_a(),
            wall_win(), wall_arch(), wall_plinth(),
            wall_arcade_a(), wall_arcade_b(), arcade_pier()]


# ---------------------------------------------------------------------- demo --
def demo():
    """A corner of the inn's stone storey, composed as a shot rather than a row:
    an ARCADED UNDERCROFT terminating on its respond at the west end, running
    straight into the solid walling (cobble / cellar arch / window bay / ashlar)
    that turns a corner into a receding side run, with the half-height wall
    closing a yard in the foreground and a gate gap lined up on the cellar arch.
    The front run deliberately puts the window bay hard against the arch bay --
    the junction Shanee found the seam in -- and the arcade hard against the
    cobble bay, which is the same question asked of round 13's pieces: one wall
    head, one plinth, one string course, one set of bed lines, whatever is under
    them."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    A, B, C = ("SM_Wall_StoneRubble_2m_" + s for s in "ABC")
    COB_A, COB_B = "SM_Wall_StoneCobble_2m_A", "SM_Wall_StoneCobble_2m_B"
    ASH = "SM_Wall_StoneAshlar_2m_A"
    WIN, ARCH, PL = "SM_Wall_StoneWindow_2m", "SM_Wall_StoneArch_2m", "SM_Wall_StonePlinth_2m"
    ARC_A, ARC_B = "SM_Wall_StoneArcade_2m_A", "SM_Wall_StoneArcade_2m_B"
    RESP = "SM_Wall_StoneArcadePier"

    # (name, location, z-rotation in degrees)
    plan = [
        # THE ARCADED UNDERCROFT, at the west end of the front elevation. It
        # answers round 13's question twice over: the open end TERMINATES on the
        # standalone respond instead of stopping mid-arch, and the other end runs
        # STRAIGHT INTO the solid cobble bay with nothing between them -- one
        # wall head, one plinth, one string course, one set of bed lines,
        # whatever is under them, because a level artist has to be able to swap
        # an arcade bay for a solid one in a run and still land the storey above
        # flat on both. The two profiles alternate (round head with a keystone,
        # then pointed under its hood) on one springing line and one opening
        # width, and the pier between them is two half-piers keyed on the bed
        # alone, so a run reads pier-arch-pier-arch-pier.
        (RESP,  (-9.23, 0.0, 0.0), 0),
        (ARC_A, (-8.0, 0.0, 0.0),  0),
        (ARC_B, (-6.0, 0.0, 0.0),  0),
        # front elevation, faces -Y, tiles along X
        # THREE STYLES IN ONE RUN, which is the question round 9 has to answer:
        # cobble, then the rubble cellar arch and window bays, then ashlar. If
        # the styles did not share the plinth, the band, the head, the bed lines
        # and the face ladder, every one of these joints would be a step.
        (COB_A, (-4.0, 0.0, 0.0),  0),
        (ARCH,  (-2.0, 0.0, 0.0),  0),
        (WIN,   (0.0, 0.0, 0.0),   0),
        (ASH,   (2.0, 0.0, 0.0),   0),
        # side run: rotated +90 so the outer face is the x = 3.0 plane, tiles +Y
        (A,     (3.0, 1.0, 0.0),  90),
        (COB_B, (3.0, 3.0, 0.0),  90),
        (C,     (3.0, 5.0, 0.0),  90),
        # half-height wall wrapping a small yard off the corner, gateway left
        # open on the cellar arch
        (PL,   (2.0, -3.4, 0.0),  0),
        (PL,   (3.0, -2.4, 0.0), 90),
        (PL,   (3.0, -0.4, 0.0), 90),
    ]
    out = []
    for nm, loc, rz in plan:
        s = src.get(nm)
        if not s:
            continue
        o = s.copy()
        o.data = s.data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (0.0, 0.0, rz * 3.14159265 / 180.0)
        out.append(o)
    for nm in src:
        src[nm].location = (0, 60, 0)      # park the originals out of frame
    return out
