"""Roofs -- the field, the eave, the ridge and the joints. Half the reference's
height is roof, so this family carries the silhouette for the whole kit.

WHAT WAS MEASURED OFF THE REFERENCES
------------------------------------
ref3 (greyscale linework, cropped 4-8x) is the form reference; ref1 supplies the
bell-cast eave.

* EVERY COURSE STEPS OUT OVER THE ONE BELOW IT, AND EVERY COURSE IS ALSO
  PAINTED AS IF IT DID. The step came first: each tab is TILTED about the ridge
  axis by atan(RELIEF/gauge) ~ 14.5 deg, so its butt end rides RELIEF = 0.032
  out of the course below and its head end lies back down on the boarding.
  Because the drop over one gauge is exactly RELIEF, the step at every butt line
  is 0.032 (0.042 after assemble_inn's stretch -- the 30-40 mm the critics asked
  for), NOTHING accumulates up the slope, and the panel still snaps at
  slope_vec(1). It costs no tris at all.
  THAT WAS NOT ENOUGH ON ITS OWN, and it is worth knowing why. A 32 mm riser on
  a building seen whole is one or two pixels, and it faces DOWN-slope, so from
  any camera looking down at a roof it is foreshortened to nothing: the field
  measured a p05-p95 luma spread of 66 on the demo render against 108 on ref3's
  roof and 142 on ref2's, i.e. it still read as a plane with lines on it. So the
  same relief is now also PAINTED into the vertex colour, in the direction the
  light actually falls (see SH_BUTT): lit along the proud butt edge, dark in the
  crevice under the course above, with one extra edge loop across the tab so the
  dark band lands inside the strip you can actually see. The joints between tabs
  in a course are real 7 mm slots (see GAP) and each tab is shaded a little
  lighter on one side than the other, so the vertical joints read too -- ref3's
  shingles are separated on all four sides, and ours were separated on one.
* SHINGLES ARE FINE, AND IT IS THE COURSE THAT HAS TO READ, NOT THE TAB. On
  ref3's left wing the courses read at roughly 7 to the metre and a tab is
  about 1.4x as wide as the course is deep.
  MIND WHICH WORLD YOU MEASURE IN. assemble_inn.py rebuilds the roof at 65 deg
  by scaling z by ZK = 1.6755, which stretches a course measured along the slope
  by 1.4634 and its rise by 1.3200. NO SINGLE GAUGE CAN PUT BOTH WORLDS INSIDE
  the brief's 6-8 courses per metre: 6-8 as authored wants ROW in 0.125..0.167,
  6-8 assembled wants 0.085..0.114, and the two do not overlap. ROW = 0.125
  takes the world THIS FAMILY IS JUDGED IN -- 8.0 courses per metre of slope on
  its own renders, dead on the fine end of the brief -- and still assembles to a
  0.165 rise per course, 6.1 to the vertical metre, which is the painting's
  number. The previous 0.105 optimised for the assembled world alone and
  measured 9.5/m here, which is finer than a course can carry a shadow line.
  TAB = G/14 = 0.1429 in both worlds, since X is never stretched: the brief's
  0.12-0.15, and 1.14x the gauge.
* The butt line WANDERS. In the linework no course is straight: it waves over
  roughly a metre and individual tabs sit a few mm high or low. The wander here
  is two sine harmonics with period GRID, so it is identical either side of a
  tiling seam and no course line breaks across it. Amplitudes are a fraction of
  the gauge, so the wander stays proportional if the course depth changes. Each
  tab is placed by its BUTT, not its centre, so wandering it down-slope does
  not also drop its butt below the course's step line: the shadow line stays
  continuous while its edge stays ragged.
* MOSS IS A TONE. There is no `moss` and no warm-brown tab scattered through a
  field -- at 1-2 % they read as green and orange confetti, which is what the
  critics called them. The field is `shingle_moss` throughout and the age is
  carried by VALUE: soft weathering BLOTCHES a few shingles across (two
  harmonics of period GRID whose phase walks with the course, so they drift
  diagonally and are identical either side of a tiling seam), one tone per
  course over that, a per-tab jitter, a scatter of properly dark weathered
  shakes that only ever land INSIDE a blotch, and a low-saturation warm/cool
  drift from `tint`. `moss` survives in exactly one place, the valley soakers,
  which is where the brief allows a few green shingles.
* A TAB IS 10 TRIS: a box's 12, minus the face lying on the boarding and (for
  every course but the panel's last) the head under the next course's lap, plus
  one edge loop across it to carry the course shadow band. That is what pays for
  courses this fine on the kit's most-placed piece.
* THE TRIM ALL LAPS THE FIELD, so every piece that laps it -- ridge board, hip
  board, verge plank and cap, apron lead -- is placed off BUILD, the height of
  a course butt above the boarding. Change RELIEF and they follow.
* THE RIDGE (ref3 at 8x) is a two-line band: a wide board laid on each slope
  with a narrower batten showing along its lower edge, then a roll over the
  apex. Standing on it is the CRESTING -- small upright plates with SPLAYED
  FEET, a waist and a rounded head, ~0.25 wide and ~0.27 tall. Measured against
  the chimney beside them that is ~0.8 m centres; here they are at 0.5 (four per
  bay) so one bay of ridge reads as a comb, not as four lonely spikes.
* THE EAVE (ref1) is the kit's signature, AND IT USED TO REACH A THIRD OF THE
  WAY DOWN THE WALL. spec.SWEEP = 0.22 is a displacement along the slope NORMAL
  that dies out over SWEEP_LEN, and the rafter tails follow that curve and poke
  out THROUGH the fascia plank with a tooth course hung between the noses. Three
  things were wrong with the proportion, all of them here and all measured:
    - the flare STOPPED TURNING at the drip. _Surf.d clamped the displacement
      for s < 0, so every millimetre of eave built outboard of the origin came
      back down the nominal 52 deg line. The trim alone therefore hung 0.64 m
      below the shingle drip on the assembled building. d(s) now continues
      C1-straight below s = 0, so outboard reach is nearly free in height.
    - SWEEP_LEN 0.60 put the flare 0.37 m of PLAN inboard of the drip, which is
      further than a sane EAVE_OVER, so the roof crossed the wall plane well
      above the datum. 0.38 fits it in 0.234 m.
    - the trim band itself was 0.64 m deep against 0.24-0.26 m measured on ref2
      and on the r6/r7 render. Fascia 0.165 not 0.340, teeth let INTO its lower
      edge instead of hung under it, rafter noses 0.062 deep at the cut.
  Net: the lowest thing on the piece now sits 0.013 m ABOVE its own origin, so
  the eave's drop below the wall head is EAVE_OVER's alone and nothing else.
  Read eave()'s docstring for the reference measurements behind those numbers.
* THE VERGE (ref3, left wing) on an ordinary rake is PLAIN: one deep plank whose
  outer face is the roof edge, a narrower plank tucked behind it, a cap bead on
  its face, a dark soffit with purlin stubs in it, and a row of little teeth. The
  scalloped, ogee-tailed ceremonial version belongs to a decorated gable and
  gables.py builds it; this is the workaday one, and the two share trim widths.
  WHAT CLOSES THE EDGE IS A KERB LIP, not the plank. Every layer of rake trim is
  extruded along X, so its outer face is PARALLEL TO THE ROOF PLANE, and anything
  wide up there takes the same light as the shingles and reads as wood lying in
  the field instead of trim closing its edge. So the top of the verge steps DOWN
  outboard in narrow treads, the highest of them a lip that laps the cut course
  ends. Same fix, same numbers, in gables.py's bargeboard. See verge().

CONVENTIONS (spec.py's ROOF-FAMILY rules, plus what this family adds)
---------------------------------------------------------------------
SLOPE / EAVE / VERGE / FLASHING use the standard roof frame:
    origin = lower edge, centre in X, ON THE NOMINAL 52 deg slope
    X in [-GRID/2, GRID/2]                 -> tiles along the ridge at GRID
    climbs +Y by SLOPE_SEG*cos P, +Z by SLOPE_SEG*sin P
                                           -> tiles up the slope at slope_vec(1)
Courses are placed by their HEAD, at arc length k*ROW for k = 1..n, so the top
course's head lands exactly on s = SLOPE_SEG and the bottom course's butt hangs
0.45*ROW BELOW s = 0 and laps over the panel underneath. That is what real
shingles do; it keeps the course rhythm continuous across the up-slope seam --
including the step, since a course's step depends only on its own gauge -- and
it is why the declared y/z seams run a little past the panel itself.
TAB divides GRID exactly (G/14) and the stagger is a 4-phase cycle of quarter
tabs, so the part tab at x = +GRID/2 pairs with the part tab at x = -GRID/2 of
the next panel and makes one whole shingle. X jitter fades to zero within 0.28
of the seam.

EAVE: its origin is the nominal-slope point, i.e. EAVE_OVER horizontally
    outboard of the wall face, and its drop below the wall head is therefore
    EAVE_OVER * tan(assembled pitch) -- 0.30 m at EAVE_OVER 0.14. The bell-cast
    throws the shingle drip a further (-0.19, +0.16) out and UP from there, and
    the straightened flare carries the trim out to y = -0.42 while keeping its
    lowest point 0.013 ABOVE the origin. So the piece oversails 0.56 m past the
    wall face and hangs 0.29 m below the datum, where it used to oversail 0.87 m
    and hang 1.67 m.
RIDGE: ridge along X, origin ON the ridge line, Z = 0 there -- the same frame as
    gables.ridge_comb, so the two swap. It LAPS the field (its underside sits at
    t = BUILD + 0.008, clear of the highest course butt) instead of replacing it,
    so a slope panel may run its top course right up to the ridge.
VERGE: origin on the rake, x = 0 on the OUTER X SEAM of the last slope panel.
    Body laps -X onto the field and overhangs +X by VERGE_OVER. Climbs at
    slope_vec(1). Mirror in X for the other rake.
HIP / VALLEY: authored in WORLD orientation, origin at the corner point, running
    along HIP_DIR = (cos P, cos P, sin P)/HIP_K. One piece is
    HIP_SEG = SLOPE_SEG*sqrt(1 + cos^2 P) = 1.879 long, which is exactly the hip
    advance for ONE slope segment on both adjacent slopes -- so hips, valleys and
    slope panels tile in lock-step, and any roof whose half-span is a whole
    number of slope segments hips and valleys exactly. Step vector HIP_STEP =
    (SLOPE_SEG*cos P, SLOPE_SEG*cos P, SLOPE_SEG*sin P). Mirror in X for the
    other hand. A VALLEY REACHES VLAP BELOW ITS OWN ORIGIN: its lead tongue and
    its bottom cut course LAP the piece below, the way a slope panel's bottom
    course laps the panel below it, so a run reads as one gutter with a
    repeating lap instead of a line of butt joints. Its declared seams therefore
    run a little past the corner point at the foot.
FLASHING, APRON (SM_Roof_Flash_Wall_2m): wall face on Y = 0 rising +Z, roof
    falls away in -Y. The joint runs ACROSS the fall. Tiles along X at GRID.
FLASHING, STEP (SM_Roof_Flash_Step_1m6): the SIDE abutment, where the fall line
    runs PARALLEL to the wall instead of into it -- a range dying into the flank
    of a cross wing. Wall face on X = 0 with the wall body in +X, roof falls away
    in -X, origin on the nominal 52 deg slope at the wall face. It closes the
    edge of a roof that runs UP the slope, so its frame is the VERGE's, not the
    apron's: it tiles UP THE SLOPE at slope_vec(1). Mirror in X for the other
    hand. The two flashings are not interchangeable and neither covers the
    other's condition.
FLASHING, STEP AT AN EAVE (SM_Roof_Flash_StepEave_0m6): the SAME abutment where
    it starts at an EAVE instead of at a panel boundary -- the bottom of a
    cross-wing junction. Same frame as the step flashing above, and its origin is
    the EAVE COURSE'S OWN ANCHOR at the wall face, so the assembler places it at
    the point it already places SM_Roof_Eave_2m at, moved along the run to the
    wall plane. It is built on the EAVE'S SURFACE, _Surf(sweep=S.SWEEP), NOT on
    the nominal plane: the bell-cast puts the eave's shingles up to SWEEP = 0.22
    out along the slope normal at the drip, which is deeper than the whole
    BUILD + FS_UP = 0.218 of a flat flashing, so the flat piece would be buried
    there. 5 courses, arc 0.643399 (s 0.570560), at the EAVE's arc gauge
    0.128680 -- 13 courses per SLOPE_SEG, the same count as the field's, over a
    swept surface that is 1.672839 long instead of 1.600. The lowest course sits
    at arc 0 (head at 1*ra, butt hanging 0.45*ra below the origin), exactly the
    eave's own first course. It does NOT hand over to the flat step flashing at
    its own top: that one has to be laid at s = SLOPE_SEG from the same origin or
    its 0.123077 gauge drifts 0.044825 out of step with the panel above by the
    segment boundary. Mirror in X for the other hand.
EAVE STOP END (SM_Roof_Eave_StopEnd): closes the END GRAIN of an eave run that
    terminates against a wall. The eave has no return of its own and cannot: its
    cap bead is (wx, .100, .052) centred on x = 0, i.e. exactly on both tiling
    seams, so finish() planes its bevel off. Same frame and SAME ORIGIN as the
    eave step flashing above, so one placement point serves both. One dentil
    pitch long (EST_L = DENT_P = 0.198444) and reaching x -0.2144..-0.0050
    measured; the eave run's last outer X seam must land EST_L short of the wall
    face, and the piece laps back over it. Mirror in X for the other hand.

HALF AND QUARTER TILES: every fraction in this family is AUTHORED, and the
    up-slope ones are whole COURSE COUNTS rather than 0.5 and 0.25 -- see the
    HALF AND QUARTER TILES block in the constants for the arithmetic that forces
    that, and build() for the list.

Moss, weeds and creeper are props' job. The green here is `moss`-toned SHINGLES
scattered through `shingle_moss` ones -- ref2's roof colour, not welded greenery.
demo() adds CTX_* context (walls, a chimney) that is NOT kit geometry, and
build() never returns it.
"""
import bpy
from math import radians, degrees, tan, cos, sin, sqrt, hypot, atan2, pi
from mathutils import Matrix, Vector
from kit import spec as S
from kit.util import Part, rng, lerp, clamp, smoothstep, _euler

FAMILY = "roofs"
COLLECTION = "04_Roof"

G = S.GRID
HB = G / 2.0
L = S.SLOPE_SEG
PD = S.PITCH_DEG
COSP, SINP = S.COS_P, S.SIN_P
TANP = SINP / COSP

# COURSE GEOMETRY.  Two worlds, and the numbers are set in the one the critics
# measure in: assemble_inn.py rebuilds the roof at 65 deg by scaling z by
# ZK = tan(65)/tan(52) = 1.6755, which stretches a course measured ALONG THE
# SLOPE by |(cos52, ZK*sin52)| = 1.4634 and its RISE by 1.6755*0.788 = 1.3200.
#     assembled gauge = 1.4634 * ROW        assembled rise = 1.3200 * ROW
# The brief and the critics both ask for ~0.15 m of rise per course (6.8 per
# metre) with tabs 0.12-0.15 wide, so:
#     ROW 0.125  ->  gauge 0.125, rise 0.099, 8.0 courses/m  AS AUTHORED
#                ->  gauge 0.183, rise 0.165, 6.1 per vertical m  ASSEMBLED
#     TAB 0.1429 ->  0.1429 in both worlds; X is never stretched
# Relief is stretched by |(sin52, ZK*cos52)| = 1.302 along the slope normal, so
# RELIEF 0.032 authored is a 0.042 step on the assembled building. Both ends of
# that are inside the 30-40 mm the critics asked for, near enough.
ROW = 0.125                 # course depth along the 52 deg slope (the GAUGE).
                            # 8.0 courses per metre AS AUTHORED, which is what
                            # this family's own renders show and what the brief's
                            # "6-8 per metre" is checked against. Assembled at
                            # 65 deg that is a 0.183 gauge and a 0.165 rise, i.e.
                            # 6.1 courses per vertical metre -- the painting's
                            # number. The previous 0.105 was inside the band in
                            # the assembled world only and measured 9.5/m here,
                            # which is finer than a course can carry a shadow.
TAB = G / 14.0              # 0.1429 -- must divide GRID for the seam tabs to
                            # pair up across a bay boundary. 1.14x the gauge.
OV = 1.45                   # shingle length / course depth, i.e. the lap. Only
                            # sets how far a tab reaches past the next course's
                            # butt (0.45 gauge); the tilt is RELIEF/gauge.
GAP = 0.007                 # SLOT BETWEEN TABS IN A COURSE. The tabs used to
                            # butt with a 1.5 mm overlap, so a course was one
                            # unbroken ribbon and the only joint you could see
                            # was the course line: measured on the demo render
                            # the field's horizontal detail (mean |dH| 4.7) was
                            # half its vertical (9.5), where ref3's roof runs
                            # 10.9 and 10.8 -- the reference's shingles are
                            # outlined on ALL FOUR sides. A 7 mm slot shows the
                            # course below, 32 mm down and painted dark, so the
                            # vertical joint is a thin dark line rather than the
                            # chamfered outline that read as brickwork.
THICK = 0.040               # tab thickness. MUST be >= RELIEF, or the butt step
                            # opens a gap you can see the boarding through.
RELIEF = 0.032              # <<< THE COURSE STEP: how far each course's butt
                            # rides out of the course below. 32 mm as authored --
                            # the middle of the 30-40 mm the critics asked for --
                            # and 42 mm assembled.
LIFT = OV * RELIEF * 0.5    # 0.0232 -- butt underside above the boarding. The
                            # tilt is centred on the boarding plane so the mean
                            # field surface stays where every other family
                            # expects it; only the butts stand higher.
BUILD = LIFT + THICK        # 0.0632 -- outer face of a course butt above the
                            # boarding. EVERYTHING that laps the field (ridge,
                            # hip, verge, apron) is placed off this.

# THE PAINTED COURSE RELIEF.  A 32 mm step is 1-2 px on a building seen whole,
# and the riser that casts the shadow faces DOWN-slope, so from any camera above
# the roof it is foreshortened to nothing. That is why the last round's real,
# correct, geometric step still measured as a flat plane from outside: the
# demo render's field came out mean 144 with a p05-p95 luma spread of 66,
# against 108 (ref3) and 142 (ref2) on the same measurement.
# So the step is also PAINTED, and painted the way the light actually falls on
# it: every tab's outer face carries a vertex-colour gradient, bright at the
# proud butt edge and dark at the head where it tucks into the crevice under the
# course above. A tab is exposed for one gauge out of its 1.45, so the visible
# gradient runs SH_BUTT -> about 0.6 of it, which is a real shadow band under
# every course at any distance in any light, for no tris at all.
# A tab is EXPOSED for 1/OV of its length and lapped for the rest, so a plain
# corner-to-corner ramp spends two thirds of its range on geometry nobody can
# see: the widest the visible strip could vary was 1.8x, and rescaling the ramp
# could not help -- the outer face's only vertices are its four corners, so the
# ramp is whatever it is between them. So the outer face carries ONE extra edge
# loop, across the tab at SH_BAND_AT of its length, just inside the line where
# the course above starts covering it. That is +2 tris on an 8-tri tab and it
# buys a real shadow BAND, dark, with an edge, tight under every course, instead
# of a soft ramp -- and it lets the hidden head stay a sane tone instead of
# being driven to black to make the visible part dark enough.
# HOW HARD TO PAINT IT. Display gamma flattens albedo ratios by about the
# 1/2.2 power, so the 2:1 ramp this started with showed up as 130 vs 100 in the
# render -- there, but not what the reference does. ref3's roof field measures a
# p05-p95 luma spread of 108 and ref2's 142; ours measured 66 before this round.
# So the ramp is 3:1, which lands as roughly 1.6:1 on screen, and the darkest
# lines (the riser, and the head buried under the lap) go much darker still.
SH_BUTT = 1.26              # multiplier at the proud, lit butt edge
SH_BAND = 0.42              # at the band line: the course shadow
SH_HEAD = 0.16              # at the head, under the lap (mostly invisible)
SH_BAND_AT = 0.58           # where the band sits along the tab (exposure = .69)
SH_RISER = 0.20             # the butt riser itself: the darkest line on a roof
SH_ROLL = 0.095             # ACROSS the tab: each one is shaded a touch lighter
                            # on one side than the other, in alternating
                            # directions, like a split shake that has cupped. It
                            # puts a value STEP at every vertical joint, which is
                            # how ref3's shingles read as separate shingles
                            # without the dark outline on all four sides that
                            # made an earlier round look like brickwork. It is
                            # what the horizontal detail measurement was missing.
EXPO = 1.0 / OV             # 0.690 -- exposed fraction of a tab


def _course_shade(t, g0=SH_BUTT, gb=SH_BAND, g1=SH_HEAD, fb=SH_BAND_AT):
    """Vertex-colour multiplier along a tab: t = 0 at the butt, 1 at the head."""
    if t <= fb:
        return lerp(g0, gb, t / fb)
    return lerp(gb, g1, (t - fb) / (1.0 - fb))
SLAB = 0.050                # roof boarding under the shingles
SWEEP_LEN = 0.38            # SLOPE LENGTH OVER WHICH THE BELL-CAST DIES OUT.
                            # 0.60 before, and it was too long for a short
                            # EAVE_OVER. The flare occupies SWEEP_LEN*cos52 of
                            # PLAN, so at 0.60 it was still 0.37 m inboard of
                            # the drip when it reached the wall face: with the
                            # eave brought in to EAVE_OVER 0.14 the roof surface
                            # would have crossed the wall plane 0.20 m ABOVE the
                            # datum and left a slot along every eave that the
                            # wall-head band could not tuck under. 0.38 puts the
                            # flare in 0.234 m of plan, so the lift at the wall
                            # face is 0.06 m -- covered by the fascia and the
                            # soffit -- and it takes the drip tangent from 16 deg
                            # to 2.8 deg, which is the dead-flat, faintly
                            # upturned edge ref1 and r6 both show. The flare is
                            # still 3.8 courses deep, so it reads as a sweep and
                            # not as a kink, and d(s) is unchanged for
                            # s >= SWEEP_LEN so panels still snap at slope_vec(1).

SH = "shingle_moss"         # ref2's mossy grey-green field -- the WHOLE field
SH_W = "shingle"            # ref1's warm brown: the _Warm variant piece only,
                            # never scattered through a moss field as confetti
MOSS = "moss"               # valley soakers only (the brief's "few shingles
                            # tucked in a valley"); never in the open field
LEAD = "stone_pale"         # DRESSED LEAD. `iron` is the palette's near-black
                            # wrought iron and it is right for hinges and
                            # lanterns; on a 2 m apron it read as a black hole
                            # punched in the roof. Weathered lead is a light
                            # grey, which stone_pale at a cool shade gives us
                            # without adding a material.

VO = S.VERGE_OVER           # 0.30
BW = 0.340                  # verge plank face depth (gables' rake board is 0.46)
BT = 0.075                  # ... and its thickness

N_SEG = max(1, int(round(L / ROW)))     # 13 -- courses _field lays in one segment
ROW_S = L / N_SEG                       # 0.123077: the field's OWN gauge

HIP_K = sqrt(1.0 + COSP * COSP)                  # 1.1744
HIP_SEG = L * HIP_K                              # 1.879
HIP_STEP = Vector((L * COSP, L * COSP, L * SINP))
HIP_DIR = Vector((COSP, COSP, SINP)) / HIP_K


HIP_ROW = HIP_SEG / N_SEG                        # 0.144532 -- one cut course
                                                 # along the arris. _arris
                                                 # derives exactly this from
                                                 # HIP_SEG, so a part length cut
                                                 # to a whole number of them
                                                 # keeps the full piece's gauge.


def hip_step(length=HIP_SEG):
    """The (x, y, z) a run advances for `length` of arris. HIP_STEP at HIP_SEG.
    A part-length valley needs its own, or its declared seams bound the full
    piece's footprint and the assembler cannot tell where the piece ends."""
    return HIP_DIR * length

# THE VALLEY LAPS ITS NEIGHBOUR -- see _arris.
# A run of valley pieces used to BUTT. Every piece began and ended with its own
# full detail: the lead sheet stopped dead on the piece boundary and the next one
# started there, its cut courses started again half a gauge in from the end, and
# the joint between two pieces was a line across the gutter with nothing lapping
# it. Shanee read a run as "2 pieces separated ... shows the join instead", twice.
# A real lead valley is laid in sheet lengths that LAP: each sheet reaches DOWN
# over the head of the one below it, welted at its edge, so what a run shows is a
# repeating lap line -- one continuous gutter with a rhythm in it, which is the
# opposite of a butt. Three numbers do it, and they work on identical pieces
# stacked at HIP_STEP because the sheet RAMPS along its own length.
VLAP    = 0.155   # how far a piece's lead tongue reaches down-slope PAST its own
                  # origin, i.e. over the head of the piece below it
VLIFT   = 0.028   # how far proud of the nominal channel that tongue's tip sits.
                  # The sheet ramps from VLIFT at its tip to zero at its head, so
                  # the upper sheet always lands ON the lower one with air
                  # between them instead of two coincident faces. It MUST be
                  # bigger than the sheet's own thickness or the tip lands
                  # exactly on the sheet below and they fight.
VLEAD_T = 0.014   # lead sheet thickness. Thin, because the whole
                  # channel already has to sit BUILD proud of the boarding to
                  # clear the field it laps.
VSOAK   = 0.006   # the same ramp on the cut courses, far too small to read as a
                  # heavier course at the lap but enough that a run laid with any
                  # overlap (assemble_inn.py widens this piece by 1.12) laps
                  # instead of fighting.
VWELT_SINK = 0.008  # HOW FAR A WELT IS BEDDED INTO THE SHEET IT TURNS UP OUT OF.
                  # THIS WAS THE WHOLE OF THIS FAMILY'S NEAR-COINCIDENT SURFACE.
                  # Both welts on the ordinary valley -- the long edge bead and
                  # the lap welt across the tongue -- were placed with their
                  # UNDERSIDE exactly on the lead sheet's top face: centre at
                  # top(u) + half their own thickness. The bead's underside is
                  # 0.030 x 2.018 m after its bevel, twice over (one per plane),
                  # which is 1211 cm2 -- the entire number the corrected
                  # check_zfight reported for roofs, and 100 % of it. The sheet
                  # is 14 mm thick, so sinking the welts 8 mm puts their
                  # undersides 8 mm below the sheet's top face and 6 mm above its
                  # underside: interior to the lead on both sides, nothing to
                  # fight with, and no new pair opened against the sheet's back.
                  # Their heights grow by the same 8 mm, so every OUTER face --
                  # the whole silhouette of the channel -- is exactly where it
                  # was. This is not a dodge and it is not new: valley_eave's
                  # VF_WELT was moved to -0.008 for this identical defect last
                  # round ("bedded in the lead rather than balanced on it --
                  # which is also what a welt is"), and a welt really is formed
                  # out of the sheet, so the two solids SHOULD interpenetrate.
                  # The alternatives are worse: lifting the bead opens a 2 m slot
                  # along the gutter edge, and stopping the sheet short of the
                  # bead trades a 605 cm2 face pair for a 285 cm2 one where the
                  # sheet's cut edge meets the bead's inner cheek.

# PER-COURSE YAW for the cut courses. Two consecutive arris tabs used to be laid
# at the same lateral offset with no yaw, and they overlap by more than one
# course advance, so their SIDE faces were coplanar AND overlapping: 17 cm2 of
# coincident shingle_moss on the hip, which was this family's last z-fighting
# entry in out/zfight.json. Five distinct phases, so no two tabs within the lap
# distance of one another share a side plane. It costs no tris, and a hand-laid
# shingle is not square to its course anyway -- _field yaws its tabs for the
# same two reasons.
YAW5 = (1.00, -0.62, 0.38, -1.00, 0.72)

# ===========================================================================
# WHY A HAND-LAID FIELD USED TO LAND TWO TABS ON ONE PLANE, AND WHAT BOUNDS IT
# ===========================================================================
# Measured with ZFIGHT_TOL=0.0005 (the 0.2 mm default reports 0 for every family
# and discriminates nothing). The corrected check_zfight -- which now projects
# each face's centre onto the other's plane, and registers every face at the
# floor AND ceil of each normal component so two coplanar faces either side of a
# rounding boundary are actually compared -- found 541 cm2 across six pieces of
# this family, ALL of it shingle against shingle on the tiling panels, and all of
# it fully exposed. That is the population that matters: unlike the 1211 cm2
# closed last round (of which an auditor showed only 17 cm2, 1.4 %, was
# ray-reachable at all), you can see every one of these.
#
# There were TWO mechanisms, and both are the same mistake: A DESIGNED CLEARANCE
# ATTACKED BY INDEPENDENT JITTER ON BOTH SIDES OF IT.
#
#   1. SIDE AGAINST SIDE -- 5 of the 6 pieces, ~70 cm2 each, which is a whole
#      tab flank. Two neighbours in ONE course. The design clearance is GAP, the
#      7 mm slot each tab gives up half of. Three independent per-tab draws then
#      ate it: the tab's own lateral jitter (+/-4 mm, x1.3 on variant B), `skew`
#      (+/-7 mm, which shifts only the outer ring and therefore SLANTS both side
#      faces), and a `yaw` whose sign flipped every two tabs. Two neighbours
#      drawing opposite extremes closed 7 mm of slot and then some. Measured
#      before: the MEDIAN side-to-side separation on a slope panel was 4.1 mm,
#      not 7, and the tail reached 0.18 mm.
#   2. OUTER AGAINST OUTER -- the 47.3 cm2 on SM_Roof_Slope_2m_A at
#      (0.932, 0.335, 0.502), 0.026 mm apart, which is the one this family's own
#      auditor predicted and named. It is course k's HEAD strip against course
#      k+1's BUTT strip, in the lap. The design clearance is RELIEF: two courses'
#      outer planes are exactly `relief` apart because a course's butt line
#      advances by one gauge. Four independent draws ate it -- the per-course
#      wander PHASE (independent, so two butt lines can converge and shrink the
#      advance by 0.6 of a gauge), the per-course butt height `cl`, the tab
#      length `dp`, and `pl`, the curl that lifted a WHOLE tab (up to 16 mm of a
#      32 mm relief) INCLUDING the head that the course above has to clear.
#
# THE FIX IS NOT LESS RELIEF AND NOT LESS WANDER. Shanee has praised this roof
# and the per-course step is why. Every amplitude below is the one it was, or
# larger. What changed is that each quantity's RELATIVE value between the two
# neighbours that can touch is now BOUNDED:
#
#   * joints, not tabs.  The lateral jitter moves the JOINT, once, and both tabs
#     that meet there follow it. The slot is then exactly GAP by construction,
#     whatever the jitter did, and the joint lines wander exactly as far as
#     before. Tab widths now vary, which they should.
#   * skew and yaw are HARMONICS OF POSITION, not draws.  Both are smooth in x
#     with period GRID (or GRID/2), so two tabs a tab-width apart differ by at
#     most amplitude x 2 sin(pi*TAB/period) -- 2.2 mm of skew and 0.8 deg of yaw
#     -- instead of by twice the amplitude. The amplitude at any one tab is
#     unchanged. Bonus: sin(2 pi x / G) is ZERO at x = +/-GRID/2, so the seam
#     part-tabs are unskewed and unyawed and nothing overshoots the tiling plane.
#   * the butt-line wander is ONE FIELD FOR THE PANEL whose phase TURNS SLOWLY
#     with the course.  That is what an uneven boarding actually does: successive
#     courses follow the same undulation, drifting. Amplitude per course is
#     unchanged (and its scale still walks), but two adjacent courses now differ
#     by at most WAND_D1/D2 radians of phase, so the butt-line ADVANCE stays near
#     one gauge and the relief between planes survives.
#   * `cl` walks instead of being redrawn.  Same range, bounded step, so the
#     per-course butt height still covers its whole band -- gradually, like
#     boarding that sags -- and two adjacent courses differ by CL_STEP of it.
#   * A CURLED SHAKE LIFTS ITS BUTT, NOT ITS BODY.  `pl` is now applied as extra
#     TILT pivoted on the course line one gauge up -- i.e. on the line where the
#     next course's butt lands, which is exactly what holds a real shingle down.
#     The butt still stands the full `pl` proud (nothing about the visible curl
#     changes); above the pivot the tab tips slightly AWAY from the course above
#     instead of into it. The curl now only ever OPENS clearances.
#   * the raggedness lost to the tighter `dp` and per-tab arc jitter is paid back
#     -- with interest -- by SLIDE, a new per-tab displacement ALONG THE TAB'S
#     OWN PLANE. Sliding a tab down-slope inside its own plane moves its butt
#     edge and its riser and changes NO plane at all, so it buys ragged butt line
#     for exactly zero clearance. That is why the numbers below are tighter than
#     the ones they replace and the edge is not straighter.
#
# Worst case, arithmetic rather than hope, on variant B (the widest wander and
# the tallest lift): the outer-plane clearance cannot fall below ~5 mm and the
# side slot below ~3 mm, against a 0.5 mm tolerance. Typical is ~30 mm and 6 mm.
JIT_X    = 0.004   # lateral jitter, now on the JOINT and shared by both tabs
SKEW_A   = 0.005   # skew amplitude; a sin of period GRID in x, not a draw
YAW_A    = 0.90    # deg of yaw amplitude; a sin of period GRID/2 in x
WAND_D1  = 0.28    # rad the 1st wander harmonic turns per course
WAND_D2  = 0.40    # ... and the 2nd
WAND_AS  = 0.06    # per-course wander-amplitude walk step (bounded, not redrawn)
WAND_TAB = 0.015   # per-tab arc SHIFT of the butt, as a fraction of the gauge.
                   # This one moves the tab's PLANE, so it is charged against the
                   # relief and kept small -- see SLIDE, which is free.
SLIDE    = 0.130   # per-tab slide ALONG the tab's own plane, fraction of a
                   # gauge. Moves the butt edge, moves no plane, costs nothing.
DP_JIT   = 0.026   # tab-length jitter (was .05/.04); also moves the plane
TC_JIT   = 0.025   # per-tab normal offset, fraction of thickness (was .05)
CL_STEP  = 0.14    # per-course butt-height walk step, fraction of its own band
CURL_MAX = 0.32    # curl lift ceiling, fraction of thickness (was .40)

# ===========================================================================
# HALF AND QUARTER TILES -- AUTHORED, NOT SCALED
# ===========================================================================
# WHAT WAS MEASURED, AND WHERE THE DISTORTION ACTUALLY IS. On the assembled
# showpiece (852 objects) this family carried three non-unit scales:
#
#   SM_Roof_Slope_2m_*   42 objects at (1.000, 0.416, 0.697)
#   SM_Roof_Ridge_2m     15 objects at (1.000, 0.620, 1.039)
#   SM_Roof_Eave_2m      12 objects at (0.600, 1.000, 1.675)
#
# assemble_inn.putr places a roof piece with scale (sx, sy, sy*ZK), ZK =
# tan65/tan52 = 1.675477. So the Z component of every one of those is sy*ZK and
# is NOT a distortion: 0.416*1.675477 = 0.6970 and 0.620*1.675477 = 1.0388, both
# to four places. The stretch is the whole mechanism by which 52 deg pieces build
# a 65 deg roof, and a plane through a point scaled (s, s, s*ZK) is unchanged, so
# every seam still meets. Do not try to remove it.
#
# THE THREE REAL NUMBERS, AND WHICH ARE OURS:
#   * slope sy = 0.416 -- the part course laid at the ridge, squashed to 41.6 %
#     ALONG THE SLOPE. The course gauge on that panel is 0.416 of the field's.
#     This is the one that matters most and it is ours to fix: a course gauge is
#     the thing the eye measures a roof by.
#   * eave sx = 0.600 -- squashed to 60 % ALONG THE RIDGE, which compresses the
#     fascia, the rafter noses and the DENTIL ROW horizontally by 40 % on the
#     most visible moulding line on the building. Ours to fix.
#   * ridge sy = 0.620 -- NOT a part-length remainder. It is assemble_inn's
#     RIDGE_S constant, applied to every ridge cap, and sy is ACROSS the ridge,
#     not along it. All 15 caps measured sx = 1.000, i.e. nothing on the
#     showpiece is squashed along the ridge at all; what 0.620 narrows is the
#     cap's cross section (board 0.255 -> 0.158, roll 0.175 -> 0.109), and the
#     cresting's 0.5 m pitch along the ridge is untouched. A part-length ridge
#     piece therefore fixes nothing that is currently broken -- but spans() will
#     hand out sx < 1 the moment a block's run is not a whole number of bays, so
#     the pieces exist for that and for the user's half-tile request.
#
# WHY A FRACTION OF A PANEL CANNOT BE EXACTLY A HALF. _field lays courses by
# HEAD at a0 + k*ra with n = round(span/ROW) courses, so one SLOPE_SEG carries
# N_SEG = 13 courses of ra = ROW_S = 0.123077. 13 is odd: half of it is 6.5
# courses, and a panel spanning exactly L/2 = 0.800 can only hold 6 courses at
# gauge, leaving 0.0615 over -- which shows up as ONE course line exposed 1.5x
# (0.1846 against 0.1231), a gauge defect of exactly the kind this task exists to
# remove, 6 mm of bare boarding, or an 8 % gauge error if you divide 0.800 by 6.
# So the up-slope partials are authored at WHOLE COURSE COUNTS and their true
# lengths are stated rather than assumed:
#
#     SLOPE_HALF_N = 7 courses = 0.861538 m of slope   (0.5385 of SLOPE_SEG)
#     SLOPE_QTR_N  = 3 courses = 0.369231 m of slope   (0.2308 of SLOPE_SEG)
#     7 + 3 + 3 = 13 = one whole panel, EXACTLY.
#
# That is the composition that matters to an assembler: a full segment decomposes
# into one half plus two quarters with no residue at all. Two halves make 14
# courses, one course MORE than a segment; that is arithmetic, not a bug, and the
# ridge cap laps 0.158 m of slope (1.28 courses) so a one-course over- or
# under-run at the ridge is covered either way.
#
# ALONG THE RIDGE nothing about the course gauge changes -- only how many tabs
# fit -- so the width fractions are clean, with one exception worth stating:
# TAB = G/14, so a half bay is exactly 7 tabs and a QUARTER bay is 3.5. _field
# divides the span by round(span/TAB), so a 1 m piece gets tw = TAB exactly and a
# 0.5 m piece gets tw = 0.125, 12.5 % narrower. That is why there is no
# quarter-width SLOPE panel: on a field piece the tab is the only repeat there
# is. On the eave and the ridge the repeats that matter (dentil 0.198444,
# cresting 0.500) are preserved exactly at every width -- see DENT_P / CREST_P.
SLOPE_HALF_N = 7            # courses in the half-height slope panel
SLOPE_QTR_N  = 3            # ... and in the quarter-height one. 7+3+3 = N_SEG.
VAL_HALF_N   = 7            # cut courses in the half-length valley. The arris
VAL_QTR_N    = 3            # advance is ROW*HIP_K, so an arris also carries 13
                            # courses per HIP_SEG and 7+3+3 closes it exactly.
                            # HIP_ROW, the arris course advance, is defined with
                            # HIP_SEG below.

# THE EAVE'S AND THE RIDGE'S REPEATS, LIFTED OUT AS PITCHES so a part-length
# piece can keep them instead of scaling them. Each is written so that at wx = G
# it reproduces the full piece's own positions to the last millimetre.
RAF_P   = 0.400             # rafter-tail centres, symmetric about x = 0. At
                            # wx = G that is -0.8 -0.4 0 0.4 0.8, the five the
                            # full eave has always had.
RAF_HW  = 0.0575            # half a tail's width, for deciding what fits
DENT_P  = 1.786 / 9.0       # 0.198444 -- THE DENTIL PITCH, and the number the
                            # brief singles out. The full eave runs ten teeth
                            # from -0.902 to +0.884; that is this pitch with
DENT_PH = -0.902 + 5.0 * DENT_P      # 0.090222 -- ... this phase about x = 0.
                            # Anchoring the lattice to the piece CENTRE rather
                            # than to its -X seam is not cosmetic: the teeth are
                            # dropped wherever they fall within 0.085 of a rafter
                            # tail, and a seam-anchored lattice on a 1 m piece
                            # lands three of its five teeth within 8 mm of a tail
                            # and deletes them. Centre-anchored, a 1 m piece
                            # keeps four teeth at -0.3067 -0.1082 0.0902 0.2887
                            # -- four of the full piece's OWN positions, all of
                            # them 0.090-0.111 clear of a tail, none deleted.
DENT_HW = 0.040             # half a tooth's width
ST_P    = (G - 0.18) / (max(4, int(round((G - 0.18) / TAB))) - 1)
                            # 0.151667 -- the doubled starter course's tab pitch
                            # at the drip. Written as the full piece's own
                            # spacing so a partial keeps the pitch and simply
                            # carries fewer starters, instead of spreading the
                            # same count over a shorter run.
CREST_P = 0.500             # cresting-plate centres on the ridge, four to a bay.
                            # 0.5 divides G, G/2 AND G/4, so the comb's pitch is
                            # exact on every width and continuous across every
                            # seam -- the one repeat in this family that costs
                            # nothing to keep.


def _lattice(hb, pitch, phase=0.0, halfw=0.0):
    """Centre-anchored repeat positions inside x in [-hb, hb].

    Returns every x = phase + pitch*m whose own half-width still clears both
    tiling seams, ascending. At hb = G/2 each caller's (pitch, phase) reproduces
    the full piece's hand-written positions, which is what makes a partial piece
    a genuine part OF the full one rather than a new spacing that happens to look
    similar."""
    lim = hb - halfw + 1e-9
    m0 = int((-lim - phase) / pitch) - 1
    m1 = int((lim - phase) / pitch) + 1
    return [phase + pitch * m for m in range(m0, m1 + 1)
            if -lim <= phase + pitch * m <= lim]


class _Part(Part):
    """util.Part with one local repair.

    util.Part._emit bevels a primitive and then keeps `[f for f in fs if
    f.is_valid]` -- but bmesh.ops.bevel INVALIDATES the six original faces of a
    box and only partly returns replacements in res["faces"], so a beveled
    primitive loses its big flat faces from the paint list. They keep material
    index 0 and whatever vertex colour they interpolated, i.e. every beveled
    timber renders in the piece's FIRST material. That is a shared-library bug
    (reported in `needs`); until it is fixed there, tag every face as it is made
    and paint anything still untagged. dormers.py carries the same fix.
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

    def tab(self, center, size, mat, rot=None, tint=.07, taper=.90, shade=1.0,
            skew=(0, 0), head=False, butt=SH_RISER, taper_x=1.0,
            grad=(SH_BUTT, SH_BAND, SH_HEAD), roll=0.0):
        """A SHINGLE TAB: util.Part.box with the hidden faces left out.

        A tab is laid on the boarding and lapped by the course above it, so two
        of a box's six quads can never be seen: the one lying on the boarding,
        and (for every course but the panel's last) the head under the next
        course's lap. Dropping them takes a tab from 12 tris to 8; the band loop
        that carries the course shadow puts it back to 10, so a tab is still
        cheaper than a box, and the roof -- the kit's biggest tri consumer,
        placed a few hundred times in the example inn -- pays two tris for the
        one thing that makes it read as a roof rather than a painted plane.

        Local frame is the surface frame: X along the ridge, Y up the slope, Z
        out of the roof. The kept faces are the outer face (in two strips, split
        at the band line that carries the course shadow), the BUTT (-Y, the one
        whose riser draws the course line) and the two sides.
        """
        cx, cy, cz = center
        sx, sy, sz = size[0] / 2, size[1] / 2, size[2] / 2
        # taper_x defaults to 1: a tab is NOT chamfered along the ridge. Tapered
        # sides gave every tab a dark outline on all four edges, which read as a
        # brick wall. The vertical joint the reference does have is a straight
        # slot -- see GAP -- so the sides stay square and only the up-slope
        # faces pull in.
        tx, ty = sx * taper_x, sy * taper
        kx, ky = skew
        vs = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
              (-tx + kx, -ty + ky, sz), (tx + kx, -ty + ky, sz),
              (tx + kx, ty + ky, sz), (-tx + kx, ty + ky, sz)]
        # the band loop across the outer face (see SH_BAND_AT)
        yb = lerp(-ty + ky, ty + ky, SH_BAND_AT)
        vs += [(-tx + kx, yb, sz), (tx + kx, yb, sz)]
        mtx = _euler(rot)
        vs = [tuple(mtx @ Vector(v) + Vector((cx, cy, cz))) for v in vs]
        F = [(7, 6, 9, 8), (8, 9, 5, 4),        # outer face, split at the band
             (0, 4, 5, 1),                      # butt -- the course shadow line
             (1, 5, 6, 2), (3, 7, 4, 0)]        # the two sides
        if head:
            F.append((2, 6, 7, 3))
        fs = self._emit(vs, F, mat, tint, 0, None, shade)
        # PAINTED COURSE RELIEF -- see the SH_BUTT note in the constants.
        # The step-out is real geometry, but at building scale it is 1-2 px of a
        # riser that faces DOWN-slope, i.e. away from any camera looking down at
        # the roof. So the same relief is painted into the vertex colour, in the
        # direction the light actually falls: the proud butt edge lit, the head
        # dark where it disappears under the course above, and the riser itself
        # darkest of all. That gradient reads at any distance in any light and
        # costs nothing, and it is most of why this field no longer measures as
        # a plane with lines drawn on it.
        if (butt < 1.0 or grad) and abs(sy) > 1e-6:
            # Work in the tab's own frame. Winding is not a reliable guide for
            # which face is the butt (finish() recalculates normals afterwards),
            # so test the axis of the normal and the side of the centroid.
            inv = _euler(rot).inverted()
            inv3 = inv.to_3x3()
            ctr = Vector(center)
            grad = grad or (1.0, 1.0, 1.0)
            for f in fs:
                loc = [inv @ (l.vert.co - ctr) for l in f.loops]
                mid = sum(loc, Vector((0, 0, 0))) / len(loc)
                if butt < 1.0 and abs((inv3 @ f.normal).y) > 0.45 and mid.y < 0.0:
                    for l in f.loops:             # the riser: one dark band
                        c = l[self.clay]
                        l[self.clay] = (c[0] * butt, c[1] * butt,
                                        c[2] * butt, 1.0)
                    continue
                for l, v in zip(f.loops, loc):    # butt -> band -> head
                    m = _course_shade(clamp((v.y + sy) / (2.0 * sy)), *grad)
                    if roll:                      # ... and across the tab
                        m *= 1.0 + roll * clamp(v.x / sx, -1.0, 1.0)
                    c = l[self.clay]
                    l[self.clay] = (c[0] * m, c[1] * m, c[2] * m, 1.0)
        return fs


def _frame(ex, ey):
    """Right-handed rotation whose columns are ex, ey, ex x ey."""
    ex = Vector(ex).normalized()
    ey = Vector(ey).normalized()
    return Matrix((ex, ey, ex.cross(ey))).transposed().to_4x4()


# ------------------------------------------------------------- the surface ---
class _Surf:
    """The roof surface in the standard roof frame, parametrised by s = distance
    along the NOMINAL 52 deg slope from the piece origin.

    A bell-cast eave displaces it along the slope normal by
        d(s) = SWEEP * (1 - s/SWEEP_LEN)^2      for s < SWEEP_LEN
    so it rejoins the nominal plane at s = SWEEP_LEN and every panel above still
    snaps at slope_vec(1). Everything downstream works in ARC LENGTH along the
    curved surface, so the shingle rhythm stays even through the flare instead of
    bunching up where the surface is steepest.
    """

    def __init__(self, sweep=0.0, slen=SWEEP_LEN, n=64):
        self.sw, self.sl = sweep, slen
        smax = max(slen, L + 0.4)
        self._s = [smax * i / n for i in range(n + 1)]
        self._a = [0.0]
        for i in range(1, n + 1):
            ds = self._s[i] - self._s[i - 1]
            m = self.dp((self._s[i] + self._s[i - 1]) * 0.5)
            self._a.append(self._a[-1] + ds * sqrt(1.0 + m * m))
        self._k0 = sqrt(1.0 + self.dp(0.0) ** 2)     # |tangent| at the drip edge

    def d(self, s):
        if self.sw == 0.0 or s >= self.sl:
            return 0.0
        if s < 0.0:
            # BELOW THE DRIP EDGE THE BELL-CAST KEEPS GOING, IN A STRAIGHT LINE.
            # This used to read `u = 1 - max(s, 0)/sl`, i.e. d was CLAMPED to
            # SWEEP for s < 0 -- so every millimetre of eave built outboard of
            # the origin (the fascia, the tooth course, the rafter noses, the
            # starter courses) came back down the nominal 52 deg line, and the
            # trim alone hung 0.64 m below the drip on the assembled building.
            # The flare threw the edge OUT and the trim immediately threw it
            # back DOWN, which is most of why the eave reached a third of the
            # way down the wall. It was also inconsistent with arc(), which has
            # always measured s <= 0 at _k0 = |tangent at s = 0| -- i.e. arc
            # already assumed the straight continuation this now builds.
            # C1 at s = 0: value SWEEP, slope dp(0). A sprocketed eave really
            # does run out straight past the last rafter, and at SWEEP_LEN 0.38
            # that line leaves at 2.8 deg, so 0.4 m of outboard reach costs
            # 0.02 m of height instead of 0.51 m.
            return self.sw - 2.0 * self.sw / self.sl * s
        u = 1.0 - s / self.sl
        return self.sw * u * u

    def dp(self, s):
        if self.sw == 0.0 or s >= self.sl:
            return 0.0
        return -2.0 * self.sw / self.sl * (1.0 - max(s, 0.0) / self.sl)

    def arc(self, s):
        if s <= 0.0:
            return s * self._k0
        for i in range(1, len(self._s)):
            if self._s[i] >= s:
                t = (s - self._s[i - 1]) / (self._s[i] - self._s[i - 1])
                return lerp(self._a[i - 1], self._a[i], t)
        return self._a[-1] + (s - self._s[-1])

    def s_at(self, a):
        if a <= 0.0:
            return a / self._k0
        for i in range(1, len(self._a)):
            if self._a[i] >= a:
                t = (a - self._a[i - 1]) / (self._a[i] - self._a[i - 1])
                return lerp(self._s[i - 1], self._s[i], t)
        return self._s[-1] + (a - self._a[-1])

    def frame(self, s):
        """(tangent, normal), 2D unit vectors in (y, z)."""
        m = self.dp(s)
        ty, tz = COSP - m * SINP, SINP + m * COSP
        k = hypot(ty, tz) or 1.0
        ty, tz = ty / k, tz / k
        return (ty, tz), (-tz, ty)

    def pt(self, s, t=0.0):
        """World (y, z) of the point t out along the surface normal at s."""
        dd = self.d(s)
        y = s * COSP - dd * SINP
        z = s * SINP + dd * COSP
        if t:
            _, (ny, nz) = self.frame(s)
            y += ny * t
            z += nz * t
        return (y, z)

    def mtx(self, s):
        """Local (along ridge, up slope, out of roof) -> world."""
        (ty, tz), (ny, nz) = self.frame(s)
        return Matrix(((1.0, 0.0, 0.0),
                       (0.0, ty, ny),
                       (0.0, tz, nz))).to_4x4()


FLAT = _Surf()


def _put(p, sf, x, s, t, size, mat, **kw):
    """A box in the surface frame. size = (along ridge, along slope, out)."""
    y, z = sf.pt(s, t)
    return p.box((x, y, z), size, mat, rot=sf.mtx(s), **kw)


def _puttab(p, sf, x, s, t, size, mat, rot_extra=None, **kw):
    """A shingle tab in the surface frame -- 10 tris, hidden faces omitted.
    `rot_extra` is applied INSIDE the surface frame: it is the course tilt that
    lifts the tab's butt out of the course below."""
    y, z = sf.pt(s, t)
    m = sf.mtx(s)
    return p.tab((x, y, z), size, mat, rot=(m @ rot_extra) if rot_extra else m,
                 **kw)


def _slab(p, sf, x0, x1, s0, s1, t0, t1, mat="oak_dark", n=7, shade=.50,
          tint=.03):
    """Roof boarding: a solid that follows the (possibly swept) surface."""
    ss = [lerp(s0, s1, i / (n - 1.0)) for i in range(n)]
    poly = [sf.pt(s, t1) for s in ss] + [sf.pt(s, t0) for s in ss[::-1]]
    return p.prism(poly, x1 - x0, mat, axis='X', at=((x0 + x1) / 2, 0, 0),
                   bevel=0, tint=tint, shade=shade)


# ------------------------------------------------------------- the shingles --
def _shmat(r, moss=0.0, warm=0.0, base=SH):
    """The field is ONE material. moss/warm default to zero because a green or
    orange tab dropped through a shingle_moss field at 1-2 % reads as confetti,
    not as age -- age is carried by the per-course value drift instead. moss is
    passed non-zero in exactly one place, the valley soakers."""
    q = r.random()
    if moss and q < moss:
        return MOSS
    if warm and q < moss + warm:
        return SH_W
    return base


STAG = (0.00, 0.50, 0.25, 0.75)   # 4-phase stagger: no 2-course checkerboard

# Phases of the weathering blotches. FIXED, not drawn from the piece's own RNG:
# the blotch field has period GRID in x, so with a shared phase it runs
# CONTINUOUSLY across every bay seam and between different variants standing side
# by side. Drawn per piece, variant A and variant C met at a seam with different
# phase and put a soft vertical step down the join -- the one thing a tiling kit
# must never show. The variants differ in wander, stagger phase, per-course tone
# and per-tab jitter instead, which is plenty.
QA, QB = 1.37, 4.11


def _field(p, sf, x0, x1, s0, s1, seed, row=ROW, tab=TAB, moss=0.0, warm=0.0,
           wander=1.0, thick=THICK, relief=RELIEF, taper=0.97, t0=0.0, phase=0.0,
           lift=1.0, shade_var=0.150, course_var=0.165, tint=.090,
           butt=SH_RISER, clump=0.130, curl=0.055, mat=SH, key=None,
           xper=None):
    """Coursed shingle tabs on `sf`, over x in [x0,x1] and slope s in [s0,s1].
    Courses are placed by HEAD at arc s0 + k*row, so the last head lands on s1
    and the first butt hangs below s0 to lap the panel underneath.

    THE COURSE STEP is what makes this read as a roof instead of a painted
    plane. Every tab is tilted about the ridge axis by th = atan(relief/gauge),
    so the surface it presents drops by exactly `relief` over one course: the
    butt of each course therefore stands `relief` out of the course below it and
    casts a shadow line, while nothing accumulates up the slope, so the panel
    still snaps at slope_vec(1) and still tiles at GRID. It costs nothing -- a
    tab is the same 10 tris either way.

    Everything else here exists to make the COURSE, and not the tab, the thing
    the eye picks up at thumbnail size:
      * a tab is placed by its BUTT, so the wander ragged-edges the course
        without breaking the step line;
      * the stagger is 4-phase, so there is no two-course checkerboard cell to
        be mistaken for a course (that is what got measured as "0.25 m per
        course" when the courses were half that);
      * value jitter is mostly PER COURSE, so what varies reads as weathering
        running along the courses rather than as confetti;
      * one material. Moss is a tone here, not a green tab.

    AND EVERY JITTER IN HERE IS BOUNDED IN ITS RELATIVE EFFECT ON THE NEIGHBOUR
    IT CAN TOUCH -- see the JIT_X..CURL_MAX block for the measurement that forced
    it. Two clearances are load-bearing and both used to be attacked from both
    sides by independent draws: GAP, the 7 mm slot between two tabs in a course,
    and RELIEF, the 32 mm between two courses' outer planes. The joint jitter is
    shared by the pair that meets at it; skew and yaw are smooth harmonics of x;
    the wander is one field whose phase turns slowly with the course; `cl` walks;
    and the curl is a tilt pivoted on the course line above rather than a lift of
    the whole tab. Amplitudes are unchanged or larger.

    `key` OVERRIDES THE PIECE NAME IN THE RNG SEED, and it is what makes a
    half-height panel provably the same field as the full one rather than a
    similar-looking one. Every per-course quantity here -- the wander phase and
    amplitude, the butt-height walk, the skew and yaw signs -- and then every
    per-tab draw comes off ONE stream consumed in course order, so a panel laid
    over the same x span with the same key and FEWER courses reproduces the full
    panel's courses 1..n exactly, tab for tab. Its gauge cannot drift from the
    full panel's, because it IS the full panel's.

    `xper` IS THE PERIOD OF EVERY HARMONIC IN X, and a piece narrower than GRID
    has to set it or it does not tile. The wander, the skew and the yaw are all
    sines of period GRID precisely so that they take the SAME VALUE at x = -G/2
    and x = +G/2: that is what makes a course line run unbroken across a bay
    seam, and it is why the seam part-tabs come out unskewed and unyawed and
    nothing overshoots the tiling plane. On a half-bay panel sin(2 pi x / G) is
    -1 and +1 at the two seams instead of equal, so the seam tabs were skewed the
    full SKEW_A and finish() cut 40-74 verts off each of them at 0.005 m -- the
    part tab at one panel's seam and the part tab at the next panel's no longer
    made one shingle. Setting xper to the piece's own width restores the property
    exactly. The weathering blotch is deliberately NOT rescaled: its period is
    GRID with a FIXED phase so that the damp patches are the same size on every
    piece in the family, which is a different job from tiling.
    """
    xp = xper or G
    r = rng(f"{key or p.name}/field/{seed}")
    a0, a1 = sf.arc(s0), sf.arc(s1)
    n = max(1, int(round((a1 - a0) / row)))
    ra = (a1 - a0) / n
    nt = max(1, int(round((x1 - x0) / tab)))
    tw = (x1 - x0) / nt
    # --- the tilt: drop `relief` over one gauge -----------------------------
    th = atan2(relief, ra)
    tn = relief / ra                       # tan of the nominal course tilt
    hz = thick * 0.5                       # butt end lifts out of the roof
    # PER-TAB TILT. 1.8 deg, unchanged: at 0.85 deg it was doing nothing for the
    # light and the field's only value variation was painted. It is indexed on
    # THE COURSE AS WELL AS THE TAB -- indexed on the tab alone, every course got
    # the identical alternating pattern, and with the half-tab stagger that made
    # a two-course cell you could mistake for one coarse course, which is what
    # got measured as "0.25 m per course".
    # It stays a free-running draw because a rotation about the RIDGE axis moves
    # neither side face: the tilt cannot close a joint. It is the only one of the
    # three per-tab rotations that needed no bound.
    DTH = [radians(1.80 * (1 if i % 2 else -1) * (.55 + .45 * ((i * 3) % 7) / 6.))
           for i in range(64)]
    # THE BUTT-LINE WANDER IS ONE FIELD FOR THE WHOLE PANEL, and what changes
    # from course to course is its PHASE, slowly. Period GRID, so it is identical
    # either side of a tiling seam; amplitudes are a FRACTION OF THE GAUGE, so
    # the wander stays proportional if the course depth changes. Per course the
    # amplitude still moves, as a bounded walk rather than a fresh draw --
    # because an independent phase per course is what let two adjacent butt lines
    # converge until the advance between them, and with it the whole 32 mm of
    # relief between their outer planes, went to nothing.
    WP1, WP2 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
    WA1 = ra * r.uniform(.07, .18) * wander
    WA2 = ra * r.uniform(.03, .09) * wander
    asc, clj, sks, yws = [], [], [], []
    av, cv = 1.0, 0.5
    for k in range(n):
        av = clamp(av + r.uniform(-WAND_AS, WAND_AS), .76, 1.24)
        cv = clamp(cv + r.uniform(-CL_STEP, CL_STEP), 0.0, 1.0)
        asc.append(av)
        clj.append(cv * relief * .22 * lift)   # same band, walked not redrawn
        sks.append((1.0 if r.random() < .5 else -1.0) * r.uniform(.55, 1.0))
        yws.append((1.0 if r.random() < .5 else -1.0) * r.uniform(.55, 1.0))
    # WEATHERING PATCHES. Age on the reference roof is not per-shingle noise, it
    # is soft blotches a few shingles across that drift along and across the
    # courses -- lichen and damp, read as VALUE. Two harmonics with period GRID
    # in x (so the pattern is identical either side of a tiling seam) whose phase
    # walks with the course index, which tilts the blotches instead of striping
    # them. It is a grey-green tone shift on the one field material, never a
    # green tab dropped in: that read as confetti and the brief forbids it.
    out = []
    for k in range(n):
        head = a0 + (k + 1) * ra
        off = (STAG[k % 4] + phase) * tw
        # THE JOINTS, JITTERED ONCE EACH. Both tabs meeting at a joint take the
        # same offset from it, so the slot between them is exactly GAP however
        # far the joint moved -- where jittering each TAB let two neighbours draw
        # opposite extremes and close the slot completely. The joint lines wander
        # exactly as far as they did; only the tab widths now vary with them,
        # which is what a hand-split shingle does anyway.
        ej = [x0 + tw * j - off for j in range(nt + 2)]
        ej = [xe + r.uniform(-1, 1) * JIT_X * wander
              * smoothstep(0.0, 0.28, min(xe - x0, x1 - xe)) for xe in ej]
        # ONE butt height and ONE base tone for the whole course
        cl = t0 + LIFT * (relief / RELIEF if RELIEF else 1.0) + clj[k]
        csh = 1.0 + r.uniform(-course_var, course_var * .8)
        for i in range(nt + 1):
            lo, hi = max(ej[i], x0), min(ej[i + 1], x1)
            if hi - lo < tw * 0.18:
                continue
            # THE JOINT: pull each end in by half a slot, but NEVER at a tiling
            # seam -- the part tab at x1 and the part tab at x0 of the next panel
            # are two halves of ONE shingle, so shrinking both would open a
            # double-width slot straight up every bay boundary.
            lo += 0.0 if lo <= x0 + 1e-6 else GAP * .5
            hi -= 0.0 if hi >= x1 - 1e-6 else GAP * .5
            if hi - lo < tw * 0.12:
                continue
            cu = (lo + hi) / 2
            jf = smoothstep(0.0, 0.28, min(cu - x0, x1 - cu))
            hd = head + asc[k] * (WA1 * sin(2 * pi * cu / xp + WP1 + k * WAND_D1)
                                  + WA2 * sin(4 * pi * cu / xp + WP2
                                              + k * WAND_D2)) \
                 + r.uniform(-1, 1) * ra * WAND_TAB * jf * wander
            bt = hd - ra * OV * (1 + r.uniform(-DP_JIT, DP_JIT * .85) * wander)
            # A CURLED SHAKE LIFTS ITS BUTT, NOT ITS WHOLE BODY. A few tabs stand
            # proud of their course -- a thicker shake, or one that has cupped;
            # they catch the sun and drop a shadow on the tab beside them, which
            # is the other half of "hand-laid". `pl` used to raise the whole tab,
            # HEAD INCLUDED, so a 16 mm curl spent half the 32 mm of relief that
            # the course above it needs to clear. Applied as extra TILT instead,
            # tan going up by pl/gauge, the tab pivots on the course line ONE
            # GAUGE ABOVE ITS BUTT -- which is precisely the line the next
            # course's butt lands on, and precisely what nails a real shingle
            # down. The butt still stands the full `pl` proud; above the pivot the
            # tab now tips AWAY from the course above rather than into it, so the
            # curl can only ever OPEN a clearance.
            pl = r.uniform(.18, CURL_MAX) * thick if r.random() < curl else 0.0
            phi = atan2(tan(th - DTH[(k * 5 + i) % 64]) + pl / ra, 1.0)
            cph, sph = cos(phi), sin(phi)
            sy = (hd - bt) * 0.5 / cph         # half length along the tilted tab
            # place by the BUTT: its underside lands on `cl` (+ the curl) whatever
            # the wander did to this tab's own length or position, so the step
            # line holds.
            tc = cl + pl - sy * sph + hz * cph \
                 + r.uniform(-1, 1) * thick * TC_JIT
            # ... and then SLIDE the tab along its own plane. Down-slope inside
            # its own plane, a tab's butt edge and riser move and NO PLANE MOVES,
            # so this is ragged butt line for zero clearance -- which is what pays
            # for WAND_TAB and DP_JIT being tighter than the draws they replace.
            ds = r.uniform(-1, 1) * ra * SLIDE * jf * wander
            tc -= ds * sph / cph
            bl = 1.0 + clump * (.62 * sin(2 * pi * cu / G + QA + k * .83)
                                + .38 * sin(4 * pi * cu / G + QB - k * 1.27))
            # a scatter of properly dark, weathered shakes -- but only INSIDE a
            # damp blotch, never sprinkled across the whole field, which is the
            # difference between age and confetti
            if bl < 1.0 - clump * .30 and r.random() < .34:
                bl *= .74
            # skew and yaw are SMOOTH IN X, not drawn per tab: neighbours a tab
            # apart differ by at most amplitude x 2 sin(pi TAB / period), and both
            # harmonics vanish at x = +/-GRID/2 so the seam part-tabs stay square
            # to the tiling plane.
            rx = (Matrix.Rotation(-phi, 4, 'X')
                  @ Matrix.Rotation(radians(YAW_A) * yws[k]
                                    * sin(4 * pi * cu / xp), 4, 'Z'))
            out += _puttab(p, sf, cu, sf.s_at((hd + bt) * 0.5 + ds), tc,
                           (hi - lo, sy * 2.0, thick),
                           _shmat(r, moss, warm, mat), tint=tint, taper=taper,
                           rot_extra=rx, butt=butt,
                           roll=SH_ROLL * (1 if (k * 3 + i * 5) % 3 else -1)
                                * (.7 + .3 * ((i * 7 + k) % 4) / 3.),
                           skew=(SKEW_A * sks[k] * sin(2 * pi * cu / xp), 0.0),
                           head=(k >= n - 1),
                           shade=csh * bl * (1.0 + r.uniform(-shade_var,
                                                             shade_var * .8)))
    return out


def _pfield(p, org, ex, ey, u0, u1, v0, v1, seed, row=ROW, tab=TAB,
            thick=THICK, relief=RELIEF, moss=0.0, warm=0.0, t0=0.0, taper=.97,
            tint=.085, stagger=.5, wander=1.0, butt=SH_RISER, shade_var=.140,
            course_var=.145, clump=.09, mat=SH):
    """The same stepped courses on an arbitrary flat plane -- hips, valleys and
    flashing, where the plane is not the piece's own slope. Courses run along
    ex and climb ey (ey must point UP-slope, or the steps face the wrong way);
    ex x ey must point out of the roof."""
    r = rng(f"{p.name}/pfield/{seed}")
    ex, ey = Vector(ex).normalized(), Vector(ey).normalized()
    ez = ex.cross(ey).normalized()
    M = _frame(ex, ey)
    n = max(1, int(round((v1 - v0) / row)))
    ra = (v1 - v0) / n
    nt = max(1, int(round((u1 - u0) / tab)))
    tw = (u1 - u0) / nt
    th = atan2(relief, ra)
    ct, st = cos(th), sin(th)
    hz = thick * 0.5
    # see _field for the whole argument. The tilt is a free draw (a rotation about
    # the course axis moves no side face); the YAW is not, because it slants both
    # of them, and the alternating table here put up to 1.8 deg between two
    # neighbours across a 7 mm slot. Flashing measured a 4.3 mm minimum, but on
    # only 70 tabs -- that is a small sample getting away with it, not a bound.
    DTH = [radians(1.80 * (1 if i % 2 else -1) * (.55 + .45 * ((i * 3) % 7) / 6.))
           for i in range(64)]
    ROT = [M @ Matrix.Rotation(-th + d, 4, 'X') for d in DTH]
    out = []
    for k in range(n):
        head = v0 + (k + 1) * ra
        off = (STAG[k % 4] * stagger * 2.0) * tw
        cl = t0 + LIFT * (relief / RELIEF if RELIEF else 1.0) \
             + r.uniform(0, relief * .22)
        csh = 1.0 + r.uniform(-course_var, course_var * .8)
        sks = (1.0 if r.random() < .5 else -1.0) * r.uniform(.55, 1.0)
        yws = (1.0 if r.random() < .5 else -1.0) * r.uniform(.55, 1.0)
        for i in range(nt + 1):
            cu = u0 + tw * (i + 0.5) - off
            lo, hi = max(cu - tw / 2, u0), min(cu + tw / 2, u1)
            if hi - lo < tw * 0.18:
                continue
            lo += 0.0 if lo <= u0 + 1e-6 else GAP * .5      # see _field
            hi -= 0.0 if hi >= u1 - 1e-6 else GAP * .5
            if hi - lo < tw * 0.12:
                continue
            jf = smoothstep(0.0, 0.10, min(lo - u0, u1 - hi))
            um = (lo + hi) * 0.5
            # most of the butt raggedness now SLIDES along the tab's own plane,
            # where it moves the butt edge and no plane at all -- see _field
            ds = r.uniform(-1, 1) * ra * SLIDE
            hd = head + r.uniform(-1, 1) * ra * WAND_TAB * wander + ds
            dp = ra * OV * (1 + r.uniform(-DP_JIT, DP_JIT * .85))
            sy = dp * 0.5 / ct
            tc = cl - sy * st + hz * ct + r.uniform(-1, 1) * thick * TC_JIT \
                 - ds * st / ct
            c = (Vector(org) + ex * ((lo + hi) / 2) + ey * (hd - dp / 2)
                 + ez * tc)
            bl = 1.0 + clump * (.62 * sin(2 * pi * (lo + hi) * .5 / G + QA + k * .83)
                                + .38 * sin(4 * pi * (lo + hi) * .5 / G + QB - k * 1.27))
            out += p.tab(tuple(c), (hi - lo, sy * 2.0, thick),
                         _shmat(r, moss, warm, mat), tint=tint,
                         rot=(ROT[(k * 5 + i) % 64]
                              @ Matrix.Rotation(radians(YAW_A) * yws
                                                * sin(4 * pi * um / G), 4, 'Z')),
                         taper=taper,
                         roll=SH_ROLL * (1 if (k * 3 + i * 5) % 3 else -1),
                         butt=butt,
                         skew=(SKEW_A * sks * sin(2 * pi * um / G) * jf, 0.0),
                         head=(k >= n - 1),
                         shade=csh * bl * (1.0 + r.uniform(-shade_var,
                                                           shade_var * .8)))
    return out


# ------------------------------------------------------------ 1. slope tile --
SLOPE_CFG = {"A":    dict(wander=1.00, lift=1.0, phase=0.000, course_var=.145),
             "B":    dict(wander=1.30, lift=1.4, phase=0.125, course_var=.180,
                          shade_var=.120),
             "C":    dict(wander=0.85, lift=0.8, phase=0.375, course_var=.115),
             "Warm": dict(wander=1.10, lift=1.0, phase=0.250, course_var=.150,
                          mat=SH_W)}
SLOPE_CURL = ((-.52, .44), (.63, 1.07))   # variant B's two curled shakes


def slope(var="A", nrow=N_SEG, wx=G, nm=None):
    """The field panel: 2 m along the ridge by one SLOPE_SEG up it. Four
    variants so a big roof does not read as copy-paste.

    The variants differ in VALUE and in how hard the courses wander -- never by
    dropping a differently coloured tab into the field, which is what read as
    green and orange confetti. A is the plain field, B the heavily weathered one
    (wider per-course drift, two curled tabs), C the quiet sun-bleached one, and
    _Warm is the brief's alternate roof: the SAME geometry in `shingle` for a
    level artist who wants ref1's warm brown roof instead of ref2's moss.

    FRACTIONAL PANELS, and the two things that make them honest.

    `nrow` is a COURSE COUNT, not a fraction, and the panel's span up the slope
    is nrow*ROW_S. That is the whole point: _field derives its gauge as
    span/round(span/ROW), so a panel spanning a whole number of ROW_S lands back
    on ra = ROW_S = 0.123077 EXACTLY -- the full panel's own gauge, to the last
    figure -- while a panel spanning L/2 = 0.800 would get 6 courses of 0.1333,
    8 % coarse, or 6 courses at gauge with 0.0615 left over and one course line
    exposed 1.5x. 7 + 3 + 3 = 13 = one whole panel, so half + quarter + quarter
    rebuilds a segment with no residue.

    `wx` shortens the panel ALONG THE RIDGE instead, which touches no course
    gauge at all -- only how many tabs fit. wx = G/2 is exactly 7 tabs of
    TAB = G/14, so a half-width panel keeps the tab width too. There is
    deliberately no quarter-WIDTH field panel: G/4 is 3.5 tabs, so it would have
    to run tw = 0.125 against the field's 0.142857, and on a plain field panel
    the tab is the only repeat there is to get wrong.

    Both partials share the full variant's field RNG (`key`), so their courses
    are not merely at the same gauge as the full panel's -- they ARE the full
    panel's first nrow courses."""
    cfg = SLOPE_CFG[var]
    hb = wx / 2.0
    span = nrow * ROW_S
    p = _Part(nm or f"SM_Roof_Slope_2m_{var}", budget="roof",
              seams=dict(x=(-hb, hb), y=(-.20, span * COSP + .05),
                         z=(-.24, span * SINP + .08)))
    sf = FLAT
    r = rng(p.name)
    _slab(p, sf, -hb, hb, -0.10, span + .01, -SLAB, .002, n=2)
    # Battens at the full panel's own 0.66 m pitch rather than three however
    # short the panel is: a 0.37 m quarter panel with three battens in it is a
    # solid raft of oak under the boarding for no reason.
    nbat = max(1, int(round((span - 0.28) / ((L - 0.28) / 2.0))) + 1)
    for k in range(nbat):
        # Battens under the boarding. Their top is buried 7 mm INSIDE the
        # boarding instead of landing on its underside plane: those three shared
        # planes were 4800 cm2 -- two thirds -- of this family's z-fighting, and
        # they are 2 m x 80 mm each, so they flickered across the whole panel.
        # Narrower than GRID too, so batten and boarding do not share the x seam.
        # ... and NOT centred on x = 0: a batten centred there has its two end
        # faces at the same |distance| from the origin plane, which check_zfight
        # scores as a coincident pair (it tests both orientations of the shared
        # normal, so a symmetric solid pairs with itself). Three battens x 34 cm2
        # was the whole of this piece's coincident surface. 6 mm off centre is
        # invisible under the boarding and reads as hand-laid anyway.
        _put(p, sf, -0.006,
             (span * .5 if nbat < 2 else lerp(.14, span - .14, k / (nbat - 1.0))),
             -SLAB - .014,
             (wx - .024, .080, .042), "oak_dark", bevel=0, tint=.04, shade=.44)
    _field(p, sf, -hb, hb, 0.0, span, seed=var,
           key=f"SM_Roof_Slope_2m_{var}" if (nrow != N_SEG or wx != G) else None,
           xper=None if wx == G else wx, **cfg)
    if var == "B":                            # two tabs curled off the course
        for (cx, cs) in SLOPE_CURL:
            if cs > span - ROW_S or abs(cx) > hb - TAB:
                continue
            _put(p, sf, cx, cs, BUILD + .014, (TAB - .02, ROW * 1.5, .028),
                 cfg.get("mat", SH), bevel=0, tint=.09, shade=.82)
    p.wobble(.009, freq=1.35)
    return p.finish()


# ------------------------------------------------------ 2. swept eave course --
def eave(wx=G, nm=None):
    """THE signature piece, RE-PROPORTIONED. The bottom SWEEP_LEN of slope
    flattens under a 0.22 bell-cast and then runs STRAIGHT OUT past the drip at
    2.8 deg (see _Surf.d), so the overhang is bought sideways instead of
    downwards; the rafter tails follow that curve and poke out through the
    fascia plank, and a tooth course hangs between their noses. Same panel
    footprint as a slope tile, so one snaps straight on top at slope_vec(1).

    WHY IT WAS RE-PROPORTIONED. Shanee, on all four assembled buildings: the
    roof "goes about a third or half way onto the floor partially obstructing
    windows". Measured on this piece, in the 65 deg world assemble_inn builds:
    the shingle drip hung 1.03 m below the wall head and the BOTTOM OF THE TRIM
    hung 1.67 m -- a 0.64 m deep eave band on a 2.60 m storey, i.e. a quarter of
    the storey of fascia alone, before EAVE_OVER's own drop was counted.

    WHAT THE REFERENCES ACTUALLY DO (crops measured at 3.5-9x, px/m fixed off
    the shingle gauge and a standing figure):
      r6 / r7  the 3D render of a comparable inn, the fairest bar because it is
               geometry, not paint. Right wing, frontal: shingle drip at y 537,
               top-storey floor (sill beam over the joists) at y 680, 53 px/m,
               so 2.70 m of the storey is VISIBLE WALL. The storey is 2.8-2.9 m,
               so the drip sits 0.1-0.2 m below the wall head -- 4-7 %.
      ref2     left wing at 3x: the shingle drip lands on the TOP OF THE WALL
               PLATE (drip y 600, plate 605-618) and the visible eave band --
               plate plus rafter ends -- is 13 px, 0.24 m. 2-6 %.
      ref1     the swept eave over the porch: the courses visibly flatten, the
               drip edge sits on the eave beam at the wall head. ~5 %.
    So the reference band is 4-8 % OF THE STOREY, and the eave band under the
    drip is ~0.25 m, not 0.64. The kit's own OPENINGS agree independently:
    win_upper's head is at 2.40 in a 2.60 storey, so anything hanging more than
    0.20 m below the wall head is standing in a window, which is the complaint.

    SO: the trim band is cut from 0.64 m to 0.25 m assembled, and it is hung so
    the LOWEST thing on the piece sits within ~0.03 m of the piece's own origin
    instead of 0.29 m below it. With the fascia no longer diving, the drop is
    then EAVE_OVER's alone and the number is honest: 0.14 -> 0.30 m, 11.5 % of
    the storey measured to the datum and ~5 % measured to the wall head under
    the plate band. The overhang does NOT shrink with it -- it is carried
    sideways by the straightened bell-cast, 0.40 m of it past the origin, so the
    piece still oversails ~0.54 m and keeps its soffit, its noses and its
    shadow line.

    PART-LENGTH EAVES, AND THE ONE MEASUREMENT THAT DECIDES THEM. `wx` shortens
    the piece ALONG THE RIDGE. Twelve of these were placed on the showpiece at
    sx = 0.600 -- fascia, rafter noses and the DENTIL ROW compressed 40 % across
    the run -- because a trimmed course had nothing else to be filled with. So
    every repeat on the piece is now a PITCH held constant while the count falls:
    rafter tails at RAF_P = 0.400 symmetric about the centre, dentils at
    DENT_P = 0.198444 on the centre-anchored lattice (see DENT_PH for why the
    anchor is the centre and not the seam), starter courses at ST_P = 0.151667.
    At wx = G each reproduces the full piece's own hand-written positions.

    WHAT DOES NOT CHANGE WITH wx, and the assembler needs the number: the piece
    is 1.4495 m deep ACROSS THE SLOPE at every length -- y from -0.4189 to
    +1.0306 -- against STEPY = 0.98515 m of nominal tile footprint. The swept
    bell-cast reaches 0.4189 m DOWN-SLOPE past the piece's own origin and the
    head runs 0.0455 m past L*cos P. Shortening the run does not shorten the
    sweep, and it must not: the sweep is what directs water down and off, and an
    eave re-arced to fit a shorter run is the version that was rejected for
    pooling water. Guard a partial eave with exactly the projection you guard the
    full one with."""
    sf = _Surf(sweep=S.SWEEP)
    hb = wx / 2.0
    # Seams tightened onto what the piece now actually occupies (was y -0.66,
    # z -0.50): a slack bound cannot catch this regression coming back.
    p = _Part(nm or "SM_Roof_Eave_2m", budget="roof",
              seams=dict(x=(-hb, hb), y=(-.46, L * COSP + .05),
                         z=(-.14, L * SINP + .12)))
    r = rng(p.name)
    # The boarding stops just BEHIND the fascia's outer face (it used to run
    # 0.09 m past it, which with the old clamped surface was 0.09 m of bare
    # slab hanging below the trim).
    _slab(p, sf, -hb, hb, -0.085, L + .01, -SLAB, .002, n=9)

    # ---- rafter tails: bell-cast, tapering to a cut nose -----------------
    # NOSE -0.135 (was -0.240) and the nose is 0.100 deep (was 0.140-0.068
    # measured off a surface that was diving at 52 deg). On the straightened
    # bell-cast s = -0.135 is 0.38 m OUTBOARD of the origin and only 0.01 m
    # below it, so the noses reach further past the wall than they used to
    # while sitting 0.26 m higher.
    NOSE, ROOT = -0.135, 0.66
    xs = _lattice(hb, RAF_P, 0.0, RAF_HW)   # -0.8 -0.4 0 0.4 0.8 at wx = G
    for cx in xs:
        jn = r.uniform(-.012, .010)
        ss = [lerp(NOSE, ROOT, j / 6.0) for j in range(7)]
        dep = [lerp(.062, .150, j / 6.0) for j in range(7)]
        # The rafter's top is buried IN the boarding, and how deep is now ramped.
        # It used to be a flat -SLAB + 0.004 for the whole length: 4 mm of
        # clearance from the boarding's underside plane, which p.wobble's 8 mm
        # closes -- 85 cm2 of oak_dark against oak_mid at 1.5 mm, on a face 2 m
        # long. Up-slope, where the pair was measured, the top is now 14 mm in
        # and nothing can reach it; at the NOSE, the only place the top face is
        # outside the boarding at all, it is left at 4 mm so the visible nose
        # section is unchanged to the millimetre.
        top = [sf.pt(s + jn, -SLAB + lerp(.004, .014, j / 6.0))
               for (j, s) in enumerate(ss)]
        bot = [sf.pt(s + jn, -SLAB - d) for s, d in zip(ss, dep)]
        nose = sf.pt(NOSE + jn - .030, -SLAB - .030)
        p.prism(top + bot[::-1] + [nose], .115, "oak_mid", axis='X',
                at=(cx, 0, 0), bevel=.012, seg=1, tint=.065,
                shade=1.02 + r.uniform(-.08, .05))

    # ---- fascia plank at the drip edge; the noses come through it --------
    # 0.165 deep, not 0.340. Its top still tucks just under the starter courses
    # (t = +0.045) and its bottom now stops at t = -0.120, which on the
    # straightened surface is 0.011 ABOVE the piece origin: 0.276 m of visible
    # band assembled, against the 0.24-0.26 m measured on ref2 and r6.
    # 6 mm off centre, for the reason in slope(): a solid centred on x = 0 pairs
    # its own two end faces in check_zfight, and this plank's were 177 cm2.
    _put(p, sf, 0.006, -0.055, -0.013, (wx - .020, .075, .117), "oak_dark",
         bevel=.012, seg=1, tint=.05, shade=.80)
    _put(p, sf, 0.0, -0.062, .028, (wx, .100, .052), "oak_pale", bevel=.014,
         seg=2, tint=.05, shade=1.06)
    # The run is NOT symmetric about x = 0: with the teeth at +/-0.895 etc, tooth
    # i and tooth 9-i are mirror images, their end faces sit the same distance
    # either side of the origin plane, and check_zfight scores that as a
    # coincident pair (81 cm2 of it) on two solids 1.8 m apart. Same reason the
    # fascia is 6 mm off centre.
    # The teeth are a DENTIL ROW let into the fascia's lower edge, not a second
    # storey of trim hung under it. They used to sit at t = -0.325 with the
    # fascia bottom at -0.29, so the pair together made a 0.64 m band; now they
    # are let 0.045 into the fascia and project 0.045 below it -- 0.075 m of
    # tooth assembled, the reference's dentil, and they are what sets the
    # piece's lowest point at 0.034 m below its own origin.
    # AND THE PITCH IS THE PITCH AT EVERY LENGTH. Written as a lattice rather
    # than as ten hand-placed teeth so a part-length eave carries the same
    # 0.198444 m dentil, not the same ten teeth squeezed into a shorter run --
    # which is exactly what sx = 0.600 was doing to 12 of these on the showpiece,
    # a 40 % compression on the building's most visible moulding line. At wx = G
    # the lattice returns -0.902 ... +0.884, the ten it always had.
    for cx in _lattice(hb, DENT_P, DENT_PH, DENT_HW):
        if min(abs(cx - u) for u in xs) < .085:
            continue
        _put(p, sf, cx, -0.054, -0.079, (.080, .098, .075), "oak_dark",
             bevel=.008, seg=1, tint=.06, shade=.86 + r.uniform(-.06, .06))

    # ---- the field, plus a doubled starter course at the drip -----------
    _field(p, sf, -hb, hb, 0.0, L, seed="eave", wander=1.05,
           key="SM_Roof_Eave_2m" if wx != G else None,
           xper=None if wx == G else wx)
    # A real shingle roof is THREE layers thick at the drip: the field course,
    # plus two starter courses under it. That build-up is what gives the eave a
    # deep dark line instead of a paper edge, and it is the one place the roof
    # silhouette is seen against the sky from below.
    ra = (sf.arc(L) - sf.arc(0.0)) / max(1, int(round(sf.arc(L) / ROW)))
    # The starters keep ST_P too, and simply run out: spreading the full piece's
    # thirteen across a shorter drip would have been the same 40 % compression
    # one layer down, where the roof is seen against the sky from below.
    nst = max(2, int((wx - 0.18) / ST_P + 1e-9) + 1)
    stx = (nst - 1) * ST_P * 0.5              # 0.91 at wx = G, i.e. HB - 0.09
    thst = atan2(RELIEF, ra)                  # the field's own course tilt
    # Per-tab tilt on the starters too. Laid at ONE angle they were exactly
    # parallel to the field course above them, and where the wander brought the
    # two to the same offset the outer faces coincided (66 cm2 at the drip).
    TLS = [Matrix.Rotation(-thst + radians(2.2 * (1 if i % 2 else -1)
                                          * (.6 + .4 * ((i * 3) % 5) / 4.)), 4, 'X')
           for i in range(8)]
    dp = ra * OV * .92
    sy = dp * .5 / cos(thst)
    # The two starter layers are 23 mm apart along the normal, not 16 mm, and
    # the per-tab tilt jitter below is 2.2 deg, not 1.1. On the straightened
    # bell-cast the surface under the drip is no longer kinked at s = 0, so the
    # starters and the field's bottom course came out nearly parallel and
    # check_zfight found 19 cm2 of coincident shingle at the drip -- the same
    # defect the jitter was added for in the first place, just with less angle
    # left to separate them.
    for cl, ds, sh, ph in ((LIFT - .019, .34, .96, 0.0),
                           (LIFT - .042, .02, .86, 0.5)):
        sm = sf.s_at(ra * ds - ra * OV * .5)
        tc = cl - sy * sin(thst) + THICK * .5 * cos(thst)
        for i in range(nst):
            _puttab(p, sf,
                    lerp(-stx, stx, (i + ph * .5) / (nst - 1.0 + ph * .5)),
                    sm, tc, (TAB - .012, sy * 2.0, THICK), SH,
                    tint=.085, taper=.95, head=True, rot_extra=TLS[i % 8],
                    roll=SH_ROLL * (1 if i % 3 else -1),
                    shade=sh + r.uniform(-.07, .06))
    p.wobble(.008, freq=1.3)
    return p.finish()


# ------------------------------------------------------------- 3. ridge cap --
def _crest_poly(w, h):
    """One cresting plate off ref3: splayed feet, a waist, a rounded head."""
    return [(-w * .50, -h * .05), (-w * .40, h * .11), (-w * .16, h * .27),
            (-w * .19, h * .55), (-w * .12, h * .82), (0.0, h),
            (w * .12, h * .82), (w * .19, h * .55), (w * .16, h * .27),
            (w * .40, h * .11), (w * .50, -h * .05)]


def ridge(wx=G, nm=None):
    """Ridge along X, origin on the ridge line -- gables.ridge_comb's frame, so
    the two swap. A wide board laid on each slope with a batten showing along
    its lower edge (ref3's two-line band), a roll over the apex, and the row of
    upright cresting plates standing on it. It LAPS the field, so a slope panel
    can run its top course right up to the ridge.

    PART-LENGTH CAPS. `wx` shortens the piece along the ridge. The cap's only
    repeat is the cresting comb, and CREST_P = 0.500 divides G, G/2 and G/4
    alike, so the comb's pitch is exact at every length and continuous across
    every seam -- four plates on a 2 m cap, two on a 1 m, one on a 0.5 m, all at
    0.5 m centres. Nothing else on the piece is a repeat; the board, the batten
    and the roll are simply cut to length.

    ONE THING THESE DO NOT FIX, said plainly because the measurement says so.
    Fifteen ridge caps on the showpiece measured scale (1.000, 0.620, 1.039).
    That 0.620 is assemble_inn's RIDGE_S and putr applies it as sy -- ACROSS the
    ridge, narrowing the board from 0.255 to 0.158 and the roll from 0.175 to
    0.109. Every one of the fifteen had sx = 1.000, so no ridge cap on that
    building is compressed along its own length and no part-length piece would
    have changed any of them."""
    hb = wx / 2.0
    p = _Part(nm or "SM_Roof_Ridge_2m", budget="roof",
              seams=dict(x=(-hb, hb), y=(-.36, .36), z=(-.34, .50)))
    r = rng(p.name)
    BOARD, LAP = 0.255, BUILD + .008     # laps clear of the course butts
    # BTH: the board is 0.080 thick, not 0.056, and the thickness is doing a job.
    # LAP puts the board's UNDERSIDE 8 mm over a nominal course butt, which is
    # right -- but the field's proudest tabs are not nominal: a curled tab
    # (+0.016) and wobble (+0.009) take one in eight of them to ~0.088, and
    # assemble_inn makes that worse, because it scales the FIELD's relief by
    # 1.302 while a ridge cap placed with sy = RIDGE_S = 0.62 has its
    # perpendicular offsets scaled by only 0.713. At 0.056 the board's outer face
    # landed at 0.0906 in that world against tabs reaching 0.115, so shingle
    # corners came THROUGH the ridge board on the assembled inn -- the same
    # defect as tile ends showing past a bargeboard, one edge over. Thickening
    # the board lifts its outer face to 0.151 (0.108 assembled) and closes it
    # WITHOUT lifting the underside, so no gap opens along its lower edge.
    # gables.ridge_comb carries the identical numbers: the two pieces must still
    # swap on one ridge with no step.
    BTH = 0.080
    for sgn in (-1, 1):
        ey = Vector((0, sgn * COSP, -sgn * SINP))       # down-slope
        ez = Vector((0, sgn * SINP, sgn * COSP))        # out of the roof
        M = _frame((sgn, 0, 0), ey)
        c = ey * (BOARD / 2) + ez * (LAP + BTH / 2)
        p.box(tuple(c), (wx, BOARD, BTH), "oak_mid", rot=M, bevel=.014, seg=1,
              tint=.05, shade=.98 + r.uniform(-.03, .03))
        # the batten showing along the board's lower edge: buried 13 mm in the
        # thicker board, standing 37 mm proud of it
        c = ey * (BOARD - .034) + ez * (LAP + BTH + .012)
        p.box(tuple(c), (wx, .075, .050), "oak_dark", rot=M, bevel=.010, seg=1,
              tint=.05, shade=.78)
    # The roll over the apex leans 6 mm down the front slope. Dead centred, its
    # two down-slope faces sat the same distance either side of the y = 0 plane,
    # which check_zfight scores as a coincident pair: 1135 cm2, two thirds of
    # the whole family's coincident surface, on a solid that has nothing to
    # fight with. A ridge roll laid by hand never sits dead centre.
    p.box((0, .006, LAP + .075), (wx, .175, .098), "oak_pale", bevel=.020, seg=2,
          tint=.05, shade=1.07)
    n = max(1, int(round(wx / CREST_P)))
    for i in range(n):
        cx = lerp(-hb, hb, (i + .5) / n)
        w = .250 * (1 + r.uniform(-.04, .04))
        h = .262 * (1 + r.uniform(-.05, .05))
        p.prism([(a, b + LAP + .110) for (a, b) in _crest_poly(w, h)], .070,
                "oak_pale", axis='X', at=(cx + r.uniform(-1, 1) * .012, 0, 0),
                bevel=.007, seg=1, tint=.06, shade=1.03 + r.uniform(-.09, .07))
    p.wobble(.006, freq=1.9)
    # The sag is a droop over the piece's own span, so it scales with it -- a
    # 0.5 m cap sagging the full 16 mm would stand 16 mm below its neighbours'
    # ends at both of its seams.
    p.sag(.016 * wx / G, axis='x', span=(-hb, hb))
    return p.finish()


# ---------------------------------------------------------- 4. verge / rake --
def verge():
    """Ordinary rake trim. Origin on the outer X seam of the last slope panel;
    body laps -X onto the field and overhangs +X by VERGE_OVER. A KERB LIP over
    the cut tile ends, the deep plank under it, a thinner plank behind, a cap
    bead on the plank's face, dark soffit with purlin stubs, and a row of little
    teeth. Climbs at slope_vec(1); mirror in X for the other rake. gables.py has
    the scalloped ceremonial version, and the two share this profile.

    THE PROFILE IS THE POINT, and it is the same fix gables.py's bargeboard just
    had. Every layer here is extruded along X, so its outer face is PARALLEL TO
    THE ROOF PLANE; a wide one therefore takes the same light as the shingles and
    reads as wood lying IN the field rather than as trim closing its edge. This
    piece's cap roll was 0.140 wide in X, in oak_PALE, at t = 0.169 -- a pale flat
    ribbon 87 mm above the field, lapping 70 mm of it: Shanee's "the wood seems to
    go straight out from the shingles" one rake over. So the top of the verge now
    STEPS DOWN outboard in three narrow treads, the highest of them the inboard
    lip that hides the course ends:

        field butts BUILD (0.063), proudest tab 0.082, cut at x = XF
        x 0.196..0.276   LIP       t = VLIP        laps the cut ends 56 mm
        x 0.276..0.304   plank     t = VLIP-0.036
        x 0.304..0.358   cap bead  t = VLIP-0.084  (below the field's butts)

    so from anywhere outboard the lip is the highest thing on the rake, the field
    dies inside it, and the outer edge of the verge sits UNDER the shingle line
    instead of hovering over it."""
    sf = FLAT
    p = _Part("SM_Roof_Verge_2m", budget="roof",
              seams=dict(x=(-.36, VO + .07), y=(-.20, L * COSP + .32),
                         z=(-.46, L * SINP + .16)))
    r = rng(p.name)
    ss = (-.06, L + .06)
    XF = VO - .048          # where the field is cut
    VLIP = BUILD + .070     # the lip's top: 51 mm over the proudest measured tab
    # Boarding and soffit. Both stop SHORT of the deep plank's outer face and
    # of each other, and the soffit's top is buried 8 mm inside the boarding
    # rather than sharing its underside plane -- three coincident planes, 0.55 m2
    # of them, all of them at surfaces you can see. The boarding now stops at
    # 0.246 and the soffit at 0.260 so that neither lands within 12 mm of the
    # lip's two faces (0.196 / 0.276), which are new.
    _slab(p, sf, -.30, .246, -.10, L + .01, -SLAB, .002, n=2)
    _slab(p, sf, -.02, .260, -.086, L + .01, -.118, -SLAB + .008, n=2,
          shade=.32, tint=.02)
    for k in range(3):                        # purlin stubs in the soffit
        # t = -.099, not -.092: at -.092 the stub's top face landed 3 mm off the
        # boarding's underside and p.wobble's 6 mm was enough to make the two
        # coincide (210 cm2 of it). Buried in the soffit either way.
        _put(p, sf, VO - .13, lerp(.20, L - .20, k / 2.0), -.099,
             (.31, .105, .078), "oak_mid", bevel=.010, seg=1, tint=.06,
             shade=.86 + r.uniform(-.05, .05))
    _field(p, sf, -.30, XF, 0.0, L, seed="verge")
    # THE KERB LIP: 80 mm of X, its top edge the highest thing on the rake, its
    # INNER face 56 mm inside the field's cut plane and its body running 0.20 down
    # through the courses into the boarding -- so every course end dies inside it
    # and nothing can show past it however the butt line wanders. The 51 mm of it
    # that stands over the field is the shadow line down the rake.
    # Shaded well down (.70): a lip that looks at the sky the way the roof does
    # comes back as another lit plank if it is shaded like the board's face.
    # ... and it is SLID 13 mm DOWN-SLOPE of the deep plank behind it. The two
    # were both exactly L + 0.12 long on the same centre, so the lip's two end
    # faces and the plank's shared a plane and overlapped over the 47 mm of x
    # where the two solids cross -- 32 cm2 at 1.5 mm. Sliding rather than
    # SHORTENING matters: the lip is the piece's lowest thing on the rake and it
    # is what covers the bottom course's cut end, so 13 mm off its length would
    # have left that end 9 mm short at the foot of a run. Sliding keeps the
    # length, so the lap between two tiled verges is the same 120 mm it was and
    # the foot gains 13 mm of cover instead of losing 9.
    _put(p, sf, .236, L / 2 - .013, VLIP - .100, (.080, L + .12, .200),
         "oak_dark", bevel=.014, seg=1, tint=.04, shade=.70)
    # The deep plank -- its top edge is 36 mm under the lip, so the lip is the
    # only thing the field ever meets. It used to BE the roof edge at
    # BUILD + 0.020, i.e. 20 mm over a NOMINAL course butt, and the field's own
    # curled tabs (+0.016) and wobble (+0.009) reach 0.082, so the proudest tabs
    # rode over its top edge and showed their ragged ends past it.
    VT = VLIP - .036
    poly = [sf.pt(s, VT) for s in ss] + [sf.pt(s, VT - BW) for s in ss[::-1]]
    p.prism(poly, BT, "oak_mid", axis='X', at=(VO - BT / 2 + .004, 0, 0),
            bevel=.010, seg=1, tint=.055, shade=1.0)
    # the thinner plank tucked behind it
    poly = [sf.pt(s, VT - .066) for s in ss] + [sf.pt(s, VT - .066 - BW * .58)
                                                for s in ss[::-1]]
    p.prism(poly, .048, "oak_dark", axis='X', at=(VO - BT - .034, 0, 0),
            bevel=.008, seg=1, tint=.05, shade=.76)
    # the cap bead: on the plank's FACE, 48 mm under its top edge, 68 mm of X
    # instead of 140, and oak_mid rather than oak_pale. The plank's top edge
    # oversails it and throws a shadow on it, which is what a moulded top edge
    # does; laid flat ON the top edge in the palette's brightest timber it was
    # the pale ribbon this rake read as.
    _put(p, sf, .324, L / 2, VT - .077, (.068, L + .12, .058), "oak_mid",
         bevel=.014, seg=2, tint=.05, shade=1.07)
    nt = 9
    for i in range(nt):                       # little teeth under the verge
        _put(p, sf, VO - BT - .100, lerp(.09, L - .09, i / (nt - 1.0)), -.150,
             (.098, .088, .108), "oak_dark", bevel=.008, seg=1, tint=.06,
             shade=.86 + r.uniform(-.07, .07))
    p.wobble(.006, freq=1.5)
    return p.finish()


# ---------------------------------------------------------- 5. hip / valley --
def _arris(p, org, nA, nB, length, seed, valley=False, lap=None):
    """Shared builder for the convex (hip) or concave (valley) arris where two
    52 deg planes meet at a square corner. `org` is the corner point, the arris
    runs up HIP_DIR, nA/nB are the two plane normals.

    THE CUT COURSES ARE PLACED BY THEIR HEAD, exactly the way _field places the
    field's: head k lands at k*ra for k = 1..n, so the top course's head lands
    exactly on `length` and the BOTTOM COURSE'S BUTT HANGS 0.45 OF A GAUGE BELOW
    THE ORIGIN and laps the piece below. That is what makes a RUN of these read
    as one line of courses instead of a stack of separate pieces: the rhythm
    crosses the joint by construction, the same way it already crosses the seam
    between two slope panels. They still step out exactly like the field's -- one
    arris course advance is ROW*HIP_K, so they land course-for-course on the
    slope panels next to them -- and they are now the field's own length
    (ra*OV) rather than 1.65x it, so the painted butt-to-head relief spans the
    same fraction of the tab and a soaker carries the same shadow line as the
    shingle beside it instead of reading as a pale plate.

    A VALLEY ALSO LAPS ITS LEAD: the sheet reaches VLAP down-slope past the
    origin and ramps VLIFT proud at that end, so each piece's tongue lies over
    the head of the sheet below with a welt across the gutter at its edge. See
    the VLAP note in the constants.

    The boards laid along a hip are set off BUILD so they lap the field's butts
    instead of being poked through by them."""
    lap = BUILD + .008 if lap is None else lap
    r = rng(f"{p.name}/arris/{seed}")
    org = Vector(org)
    d = HIP_DIR
    want = 1.0 if valley else -1.0
    ga = ROW * HIP_K                          # course advance along the arris
    n = max(3, int(round(length / ga)))
    ra = length / n                           # this arris's course advance
    th = atan2(RELIEF, ra)
    ct, st = cos(th), sin(th)
    for (nn, other) in ((nA, nB), (nB, nA)):
        away = nn.cross(d).normalized()
        if away.dot(other) * want < 0:
            away = -away
        M = _frame(away, d)
        # The cut courses tilt like the field's, so the frame they are laid in
        # must have +Z along the plane's OUTWARD normal. away x d comes out at
        # -nn on a valley and +nn on a hip (the `away` flip above is what
        # decides it), and laying the courses in the raw frame tilted every
        # valley soaker the wrong way -- head proud, butt buried. A box with a
        # symmetric X taper is unchanged by mirroring X, so flipping the frame's
        # first axis is free.
        ax = away if away.cross(d).dot(nn) > 0 else -away
        MT = [_frame(ax, d) @ Matrix.Rotation(-th, 4, 'X')
              @ Matrix.Rotation(radians(1.15 * y), 4, 'Z') for y in YAW5]
        if valley:
            # THE GUTTER, AND IT IS RAISED TO LAP THE FIELD like every other
            # piece of trim in this family (see BUILD).
            # THIS IS THE OTHER HALF OF THE BUG. The panels either side of a
            # valley OVERRUN it -- they are buried by the roof they meet, which
            # is exactly why a valley can be laid with plain full panels -- so
            # the field's own shingles stand BUILD = 63 mm proud right across the
            # channel. The old lead sheet lay 6 mm BELOW the boarding plane, i.e.
            # 70 mm under the field's butts, so it was not a channel at all: it
            # was buried, and what actually showed in the gutter was two slopes'
            # worth of overrunning shingle ends meeting each other in a ragged
            # line. That is why the piece read as "2 pieces separated" showing
            # "the join" -- there was no gutter on show to read as one thing.
            # Raised onto the field it reads as one continuous lead channel, and
            # the joint between pieces becomes a lap in that channel.
            Ls = length + VLAP
            um = (length - VLAP) * .5
            ts = atan2(VLIFT, Ls)
            sts = sin(ts)
            MS = _frame(ax, d) @ Matrix.Rotation(-ts, 4, 'X')
            base = lap                             # sheet underside, on the field
            # outer face of the sheet at arc u: ramped VLIFT proud at the tongue,
            # dead on `base` at the head, so identical pieces stacked at HIP_STEP
            # always put the upper sheet ON the lower one -- see VLAP
            top = lambda u: base + VLEAD_T + sts * (um - u)
            p.box(tuple(org + d * um + away * .1025
                        + nn * (top(um) - VLEAD_T * .5)),
                  (.265, Ls, VLEAD_T), LEAD, rot=MS, bevel=0, tint=.04,
                  shade=.24)   # a wet, dirty channel. stone_pale is a LIGHT grey and
                               # a valley that reads as a white strip down the
                               # roof is worse than one that does not read
            # THE WELTED EDGE: the sheet's outer edge turned up into a bead. One
            # runs the whole length of each side of the gutter, and they are most
            # of what makes a run read as ONE channel -- the cut ends of the
            # field die behind them instead of meeting each other in the open.
            # BEDDED VWELT_SINK INTO THE SHEET, not balanced on it: its underside
            # used to lie exactly on the sheet's top face, 0.030 x 2.018 m of it
            # per plane, which was 1211 cm2 -- all of this family's coincident
            # surface at 0.5 mm. The bead grows downward by the same amount, so
            # its top face and both cheeks are untouched. See VWELT_SINK.
            BEAD_H = .034 + VWELT_SINK
            p.box(tuple(org + d * um + away * .216
                        + nn * (top(um) + .034 - BEAD_H * .5)),
                  (.046, Ls, BEAD_H), LEAD, rot=MS, bevel=.008, seg=1, tint=.04,
                  shade=.40)   # the bead catches the light, the channel does not
            # THE LAP WELT, across the channel at the tongue's lower edge: the
            # turned edge of the upper sheet lying on the head of the sheet
            # below. A run shows one of these every HIP_SEG -- a repeating lap,
            # which is what lead does, in place of a butt joint.
            # Bedded into the sheet like the edge bead, and for the same reason:
            # its underside lay on the sheet's top face too (58 cm2 of it per
            # plane, only kept out of the 0.5 mm report because p.wobble tilts a
            # 26 mm-long face's normal enough to fail the coplanarity test --
            # which is luck, not a fix).
            uw = -VLAP + .028
            LAPW_H = .015 + VWELT_SINK
            p.box(tuple(org + d * uw + away * .085
                        + nn * (top(uw) + .015 - LAPW_H * .5)),
                  (.235, .036, LAPW_H), LEAD, rot=MS, bevel=.005, seg=1,
                  tint=.04, shade=.46)
            thk, t_butt, soak = THICK, lap + .006, VSOAK
            a0, a1 = .228, .432                # the soaker band, across `away`
        else:
            # a board laid along the arris on each plane, lapping the field
            p.box(tuple(org + d * (length / 2) + away * .128 + nn * (lap + .028)),
                  (.250, length + .02, .054), "oak_mid", rot=M, bevel=.012,
                  seg=1, tint=.05, shade=.97 + r.uniform(-.03, .03))
            p.box(tuple(org + d * (length / 2) + away * .228 + nn * (lap + .058)),
                  (.070, length + .02, .046), "oak_dark", rot=M, bevel=.009,
                  seg=1, tint=.05, shade=.78)
            thk, t_butt, soak = THICK, LIFT, 0.0
            a0, a1 = .272, .518
        for k in range(n):
            # placed by the HEAD, like the field, so the course rhythm runs
            # straight through the joint between one piece and the next
            hd = (k + 1) * ra + r.uniform(-1, 1) * ra * .055
            dp = ra * OV * (1 + r.uniform(-.05, .04))
            sy = dp * .5 / ct
            cl = t_butt + soak * (1.0 - hd / length) + r.uniform(0, RELIEF * .22)
            tc = cl - sy * st + thk * .5 * ct
            # ACROSS the arris: one cut course on a hip, two soakers in a valley.
            # A valley soaker used to be a single 0.255 plate, nearly twice the
            # field's tab width, which is most of why the gutter read as a strip
            # of something else laid over the roof. Split with a wandering joint
            # they are 0.08-0.13 wide -- at or just under the field's own
            # 0.143 tab -- so the valley reads as the same shingle as the roof
            # it drains.
            e0 = a0 + r.uniform(-1, 1) * .012
            e1 = a1 + r.uniform(-1, 1) * .014
            cuts = ([e0, lerp(e0, e1, .38 + .22 * ((k * 3) % 5) / 4.0), e1]
                    if valley else [e0, e1])
            for j in range(len(cuts) - 1):
                lo = cuts[j] + (GAP * .5 if j else 0.0)
                hi = cuts[j + 1] - (GAP * .5 if j + 2 < len(cuts) else 0.0)
                # moss lives in the valley and nowhere else on a roof: a couple
                # of green shingles in a wet gutter is the brief's one exception.
                # laid with p.tab, like the field: same 10 tris, and the same
                # painted butt-to-head relief, so a cut course at a hip or in a
                # valley carries the same shadow line as the panel it lands
                # beside.
                p.tab(tuple(org + d * (hd - dp * .5) + away * ((lo + hi) * .5)
                            + nn * tc),
                      (hi - lo, sy * 2.0, thk),
                      _shmat(r, .022 if valley else 0.0),
                      rot=MT[(k * 2 + j) % 5], tint=.085, taper=.94,
                      head=(k >= n - 1),
                      roll=SH_ROLL * (1 if (k + j) % 3 else -1),
                      shade=(.96 if valley else 1.0) + r.uniform(-.13, .10))
    if not valley:
        up = (nA + nB).normalized()
        M = _frame(up.cross(d), d)
        p.box(tuple(org + d * (length / 2) + up * (lap + .074)),
              (.170, length + .02, .094), "oak_pale", rot=M, bevel=.020, seg=2,
              tint=.05, shade=1.06)


_NA = Vector((0, -SINP, COSP))          # plane rising +y
_NB = Vector((-SINP, 0, COSP))          # plane rising +x


def hip():
    """Hip capping for the convex arris. Authored in world orientation: origin
    at the corner point, running up HIP_DIR, HIP_SEG long -- exactly one slope
    segment's advance, so it tiles in lock-step with the panels either side.
    Mirror in X for the other hand."""
    p = _Part("SM_Roof_Hip_1m9", budget="roof",
              seams=dict(x=(-.62, HIP_STEP.x + .62),
                         y=(-.62, HIP_STEP.y + .62),
                         z=(-.42, HIP_STEP.z + .40)))
    _arris(p, (0, 0, 0), _NA, _NB, HIP_SEG, seed=1)
    p.wobble(.006, freq=1.6)
    return p.finish()


def valley(narc=None, nm=None):
    """The concave arris where a cross wing runs into a main slope: a dressed
    lead channel with shingle soakers lapping in over it from both sides. Same
    frame, step and length as the hip. Mirror in X for the other hand.

    IT IS BUILT TO LAP THE PIECE BELOW IT, not to butt against it. The lead
    tongue reaches VLAP past the origin and stands VLIFT proud there, welted at
    its edge; the soaker courses are placed by their head so the bottom course
    hangs below the origin like the bottom course of a slope panel. A run
    therefore shows a repeating lap across one continuous gutter -- which is
    what lead does -- instead of a line where two pieces meet.

    PART LENGTHS. `narc` is a COURSE COUNT along the arris, and the length is
    narc*HIP_ROW. _arris derives its own advance as length/round(length/(ROW*
    HIP_K)), so a length that is a whole number of HIP_ROW lands back on
    ra = 0.144532 exactly -- the full piece's gauge -- while a piece cut to half
    of HIP_SEG would carry 6 courses of 0.1512, 4.6 % coarse, with a joint that
    no longer lands course-for-course on the slope panels beside it. 13 courses
    per HIP_SEG, and 7 + 3 + 3 = 13, so half plus quarter plus quarter is one
    whole length with no residue.

    Everything that makes a run read as one gutter is length-independent and
    stays: the tongue still reaches VLAP = 0.155 past the piece's own origin and
    still stands VLIFT proud there, and the sheet still ramps to zero at its
    head -- so a half laps a full, a full laps a quarter, and any mix of them
    laps in either order."""
    narc = N_SEG if narc is None else narc
    length = narc * HIP_ROW
    st = hip_step(length)
    p = _Part(nm or "SM_Roof_Valley_1m9", budget="roof",
              seams=dict(x=(-.62, st.x + .62),
                         y=(-.62, st.y + .62),
                         z=(-.40, st.z + .40)))
    _arris(p, (0, 0, 0), _NA, _NB, length, seed=2, valley=True)
    # Boarding in the bottom of the gutter, so no daylight shows through. It sits
    # DIRECTLY under the lead V now (its top is 3 cm below the channel's vertex,
    # clear of the ramp) rather than 5 cm under the arris line: the channel is
    # raised onto the field, so a board left down at the arris closed nothing and
    # the piece was open underneath wherever the slopes do not overrun it.
    up = (_NA + _NB).normalized()
    p.box(tuple(HIP_DIR * (length / 2) + up * .0325),
          (.46, length + .02, .075), "oak_dark", rot=_frame(up.cross(HIP_DIR),
                                                            HIP_DIR),
          bevel=0, tint=.03, shade=.40)
    p.wobble(.005, freq=1.7)
    return p.finish()


# ------------------------------------------------ 5b. the valley FOOT --------
# WHY THIS PIECE EXISTS, AND WHY A MODULAR VALLEY COULD NOT BE IT.
# SM_Roof_Valley_1m9 is laid identically at every step k of a run, so it cannot
# carry a bottom-of-run-only bend -- and the bottom of a run is exactly where
# the roof stops being a plane. The eave's bell-cast displaces the surface by
# SWEEP = 0.22 along the normal at the eave line, dying out over SWEEP_LEN =
# 0.60 of slope, while the ordinary valley's channel sits a FLAT lap of
# BUILD + 0.008 = 0.071 above the NOMINAL plane. d(s) exceeds lap - BUILD for
# every s below 0.486, so the lowest 0.57 m of arris is UNDER the swept field:
# the gutter is buried by the roof it is meant to drain, the run ends in a
# squared pale stub, and the two slopes run on down to the eave under it
# meeting shingle on shingle. That is the fault this piece closes.
#
# THE FOOT RIDES THE SWEPT SURFACE INSTEAD OF THE NOMINAL PLANES, and it is one
# whole HIP_SEG long, so it REPLACES the k = 0 length of a run rather than
# being tucked under it. Everything it carries -- lead, welts, soakers, fillet
# -- is offset from the CURVE where the two bell-cast surfaces meet, not from
# the two flat planes, so the channel keeps the same 71 mm of air over the roof
# the whole way down. At its head (s = SLOPE_SEG, one slope segment up, where
# the sweep has been dead for a metre) it is geometrically identical to an
# ordinary length's head, so the piece above laps it with exactly the ordinary
# 12 mm of air and exactly the ordinary welt: the transition is a lap, not a
# joint.
#
# THE CURVE. Plane A is swept along nA by d(sA) and plane B along nB by d(sB),
# and on the valley sA = sB = s, so the two swept surfaces meet at
#       x = y = s*cos P - d(s)*sin P        z = s*sin P + d(s)*cos P
# -- the eave's own profile, with its horizontal offset applied to BOTH x and
# y. Two things follow, and both matter:
#   * the swept valley stays EXACTLY on the 45 degree plan line, so the piece
#     still places with the assembler's mirror-per-quadrant logic; and
#   * it runs out and up from the nominal corner by (-0.173, -0.173, +0.135),
#     landing precisely where the two eaves' drip edges meet. So the mouth has
#     somewhere real to be.
#
# THE MOUTH. Past s = VF_S0 the whole cross section is rotated RIGIDLY about
# the horizontal axis across the valley (h = (1,-1,0)/sqrt2, perpendicular to
# both the 45 degree plan line and the valley tangent), so the lead turns down
# over the corner as one piece of dressed sheet, welts and all, and ends in a
# turned drip roll standing clear of both fascias. It has to clear the eave's
# own drip bead on the way out -- that bead's top is 0.072 above the swept
# boarding and a channel at the flat lap has its underside at 0.064 -- so the
# lead is carried out on a sprocket fillet that lifts it VF_LIFT over the last
# VF_LIFT_S of slope. A bell-cast eave does that to a valley in reality, and it
# is what makes the outlet read as built rather than as a strip floating over
# the shingles.
VF_S0     = -0.020    # slope at which the lead leaves the swept surface
VF_MARC   = 0.150     # arc length of the turned-down mouth beyond it
VF_MTURN  = 58.0      # degrees the mouth turns below the surface tangent
VF_MTAP   = 0.78      # ... narrowing to this fraction of the channel width
VF_LIFT   = 0.026     # sprocket lift at the foot, to clear the eave drip bead
VF_LIFT_S = 0.34      # slope over which that lift is taken up
VF_RAMP   = 0.40      # arc over which the head lap ramp is taken up. Above it
                      # the channel runs PARALLEL to the roof: the ramp exists
                      # only to hold the lapped head clear of the sheet above
                      # it, and running it the whole length would have stood
                      # the soakers 30 mm proud at the foot for nothing.
VF_STS    = VLIFT / sqrt((HIP_SEG + VLAP) ** 2 + VLIFT ** 2)   # ordinary ramp
# The welt's underside used to start at v = .000, which is exactly the plane of
# the lead sheet's own top face, and the two overlap for 42 mm across the whole
# 2 m length: check_zfight measured 256 cm2 of M_stone_pale against M_stone_pale
# on this piece, its only entry for the family. Sunk 8 mm INTO the sheet instead,
# so the welt is bedded in the lead rather than balanced on it -- which is also
# what a welt is.
VF_WELT   = ((-.023, -.008), (.023, -.008), (.026, .012),
             (.014, .030), (-.014, .030), (-.026, .012))
VF_FILL   = (-.055, .232)          # the fillet, across, under the lead
VF_H      = Vector((1.0, -1.0, 0.0)).normalized()   # horizontal, across the V


def _terp(xs, ys, x):
    """Linear interpolation on a monotone table, extrapolated at both ends."""
    if x <= xs[0]:
        return ys[0] + (x - xs[0]) * (ys[1] - ys[0]) / (xs[1] - xs[0])
    for i in range(1, len(xs)):
        if xs[i] >= x:
            t = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return lerp(ys[i - 1], ys[i], t)
    return ys[-1] + (x - xs[-1]) * (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])


class _VSurf:
    """The curve where two bell-cast eave surfaces meet at a square corner, and
    the moving frame on it. Parametrised by s = each plane's OWN nominal slope
    distance from its eave line (the two are equal along the valley), so it
    shares a parameter with _Surf and therefore with the eave piece's courses.

    basis(s) gives the two planes' outward normals nA/nB, the two in-plane
    directions aA/aB running AWAY from the valley into each plane's own
    territory, the shared valley tangent T and the bisector up. Each (a, T, n)
    is orthonormal, and at s >= SWEEP_LEN they reduce exactly to _arris's
    away / HIP_DIR / normal -- which is why this piece's head and an ordinary
    length's head are the same object and lap like two ordinary lengths."""

    def __init__(self, sweep=S.SWEEP, slen=SWEEP_LEN, s0=-0.45, s1=L + 0.40,
                 n=144):
        self.sf = _Surf(sweep=sweep, slen=slen)
        self._s = [lerp(s0, s1, i / n) for i in range(n + 1)]
        acc, vals = 0.0, [0.0]
        for i in range(1, n + 1):
            ds = self._s[i] - self._s[i - 1]
            acc += ds * self.speed((self._s[i] + self._s[i - 1]) * .5)
            vals.append(acc)
        # measured FROM s = 0, so above the sweep arc(s) == HIP_K * s exactly
        z = _terp(self._s, vals, 0.0)
        self._a = [v - z for v in vals]

    def speed(self, s):
        """|dP/ds| along the valley. Exactly HIP_K where the roof is flat."""
        m = self.sf.dp(s)
        k = sqrt(1.0 + m * m)
        ty = (COSP - m * SINP) / k
        return k * sqrt(1.0 + ty * ty)

    def arc(self, s):
        return _terp(self._s, self._a, s)

    def s_at(self, a):
        return _terp(self._a, self._s, a)

    def pt(self, s):
        y, z = self.sf.pt(s, 0.0)
        return Vector((y, y, z))

    def basis(self, s):
        (ty, tz), _n = self.sf.frame(s)
        q = sqrt(1.0 + ty * ty)
        return dict(s=s, tp=1.0,
                    P=self.pt(s),
                    T=Vector((ty, ty, tz)) / q,
                    aA=Vector((-1.0, ty * ty, ty * tz)) / q,
                    aB=Vector((ty * ty, -1.0, ty * tz)) / q,
                    nA=Vector((0.0, -tz, ty)),
                    nB=Vector((-tz, 0.0, ty)),
                    up=Vector((-tz, -tz, 2.0 * ty)).normalized())


def _sweep(p, rings, mat, bevel=0.0, seg=None, tint=.04, shade=1.0):
    """One solid swept along a curve. `rings` are cross sections of equal
    length given in the same rotational order; capped at both ends."""
    m = len(rings[0])
    vs = [tuple(v) for ring in rings for v in ring]
    F = [tuple(range(m))[::-1]]
    for i in range(len(rings) - 1):
        a, b = i * m, (i + 1) * m
        for j in range(m):
            k = (j + 1) % m
            F.append((a + j, a + k, b + k, b + j))
    F.append(tuple(range((len(rings) - 1) * m, len(rings) * m)))
    return p._emit(vs, F, mat, tint, bevel, seg, shade)


VFT = _VSurf()
VF_NMOUTH = 3


def _vf_o(vs, s):
    """Outer face of the lead at s, along the plane normal, FROM THE SWEPT
    SURFACE. At s = SLOPE_SEG it is exactly the ordinary piece's head offset,
    and it rises at the ordinary ramp rate below it for VF_RAMP of arc -- same
    ramp, so the same lap."""
    return (BUILD + .008 + VLEAD_T - VLIFT * .5
            + VF_STS * min(vs.arc(L) - vs.arc(s), VF_RAMP)
            + VF_LIFT * smoothstep(VF_LIFT_S, 0.0, s))


def _vf_sections(vs):
    """The moving frames the whole piece is built on: stations up the swept
    valley, then the mouth as a RIGID rotation of the lowest of them about h.
    Rigid, because a mouth bent plane by plane would open the V; rotating the
    whole cross section about the axis across the valley keeps the two flanks
    square to one another, which is what dressing one sheet of lead over a
    corner actually does. Returned mouth-tip first, head last."""
    secs = []
    for s in (VF_S0, .04, .11, .19, .28, .38, .49, .60, .78, 1.02, 1.30, L):
        b = vs.basis(s)
        b["o"] = _vf_o(vs, s)
        secs.append(b)
    f0 = secs[0]
    D0 = -f0["T"]
    U0 = VF_H.cross(D0)                    # out of the roof at the mouth
    tt = radians(VF_MTURN)
    rad = VF_MARC / tt
    mouth = []
    for i in range(1, VF_NMOUTH + 1):
        a = tt * i / VF_NMOUTH
        M = Matrix.Rotation(a, 4, VF_H)
        mouth.append(dict(s=VF_S0, tp=lerp(1.0, VF_MTAP, i / VF_NMOUTH),
                          o=f0["o"],
                          P=f0["P"] + rad * (D0 * sin(a) + U0 * (cos(a) - 1.0)),
                          T=(M @ f0["T"]), up=(M @ f0["up"]),
                          aA=(M @ f0["aA"]), aB=(M @ f0["aB"]),
                          nA=(M @ f0["nA"]), nB=(M @ f0["nB"])))
    return mouth[::-1] + secs


def _vf_ring(sec, ka, kn, prof, base):
    """One cross section: `prof` is (across, out) in the section's own frame,
    `base` the offset of its zero along that plane's normal."""
    P, a, n, tp = sec["P"], sec[ka], sec[kn], sec["tp"]
    return [P + a * (u * tp) + n * (base + v) for (u, v) in prof]


def valley_eave():
    """THE FOOT OF A VALLEY RUN. One HIP_SEG long, same 45 degree plan line and
    the same frame and orientation as SM_Roof_Valley_1m9 (authored running
    +X +Y +Z, mirrored per quadrant), and it REPLACES the run's lowest ordinary
    length: place it at the run's p0 and start the ordinary pieces one step up.
    Its head is an ordinary head, so the length above laps it with the ordinary
    welt; its foot rides the bell-cast out to the drip edge and turns down over
    the corner into a mouth that discharges past both fascias."""
    vs = VFT
    p = _Part("SM_Roof_Valley_Eave_1m9", budget="roof",
              seams=dict(x=(-.80, HIP_STEP.x + .62),
                         y=(-.80, HIP_STEP.y + .62),
                         z=(-.46, HIP_STEP.z + .40)))
    r = rng(p.name)
    secs = _vf_sections(vs)
    body = secs[VF_NMOUTH:]                  # the stations on the roof itself
    tip = secs[0]

    for (ka, kn, flip) in (("aA", "nA", True), ("aB", "nB", False)):
        # ---- the sprocket fillet: what carries the lead out over the eave.
        # It follows the lead, so the lift at the foot has something under it,
        # and it dies 6 mm under the sheet with its end hidden behind the welt.
        fl = []
        for (i, sc) in enumerate(body):
            dep = .020 if i == 0 else .048
            ring = _vf_ring(sc, ka, kn,
                            ((VF_FILL[0], -dep), (VF_FILL[1], -dep),
                             (VF_FILL[1], -.006), (VF_FILL[0], -.006)),
                            sc["o"] - VLEAD_T)
            if i == len(body) - 1 and flip:
                # The two fillets cross each other in the angle, and their HEAD
                # CAPS were cut on the same section plane -- two coplanar,
                # overlapping faces, and the last 19 cm2 of z-fighting in this
                # family. One of them stops 12 mm short, which nothing can see:
                # the head of this piece is lapped by the length above it.
                ring = [v - sc["T"] * .012 for v in ring]
            fl.append(ring)
        _sweep(p, fl, "oak_dark", tint=.03, shade=.40)
        # ---- the lead: one sheet per plane, the ordinary section exactly ----
        _sweep(p, [_vf_ring(sc, ka, kn,
                            ((-.030, -VLEAD_T), (.235, -VLEAD_T),
                             (.235, 0.0), (-.030, 0.0)), sc["o"])
                   for sc in secs], LEAD, tint=.04, shade=.24)
        # ---- the welted edge, running the whole length and round the mouth --
        _sweep(p, [_vf_ring(sc, ka, kn, [(.216 + u, v) for (u, v) in VF_WELT],
                            sc["o"]) for sc in secs], LEAD, tint=.04, shade=.40)
        # ---- the turned drip roll across the mouth --------------------------
        ax = tip[ka] if not flip else -tip[ka]
        p.box(tuple(tip["P"] + tip[ka] * (.1025 * tip["tp"])
                    + tip[kn] * (tip["o"] + .013) - tip["T"] * .004),
              (.265 * tip["tp"], .034, .030), LEAD,
              rot=_frame(ax, tip["T"]), bevel=.007, seg=1, tint=.04, shade=.52)

    # ---- the cut courses, on the ordinary run's own rhythm -----------------
    # Heads are placed DOWN from the head at the ordinary piece's course
    # advance, so course k of this piece and course k of the length above it
    # make one line. What the lap shows is a welt and a course, nothing else.
    n_ord = max(3, int(round(HIP_SEG / (ROW * HIP_K))))
    ra_p = (HIP_SEG / n_ord) / HIP_K              # per-plane arc per course
    a_top, a_bot = vs.sf.arc(L), vs.sf.arc(VF_S0 + .012)
    heads, j = [], 0
    while a_top - j * ra_p - ra_p * OV >= a_bot - 1e-6:
        heads.append(a_top - j * ra_p)
        j += 1
    for (ka, kn, flip) in (("aA", "nA", True), ("aB", "nB", False)):
        for (k, hd0) in enumerate(heads):
            hd = hd0 + r.uniform(-1, 1) * ra_p * .045
            dp = ra_p * OV * (1 + r.uniform(-.05, .04))
            av_h = vs.arc(vs.sf.s_at(hd))
            av_b = vs.arc(vs.sf.s_at(hd - dp))
            adv = av_h - vs.arc(vs.sf.s_at(hd - ra_p))
            th = atan2(RELIEF, max(adv, 1e-4))
            ct, st = cos(th), sin(th)
            sy = (av_h - av_b) * .5 / ct
            sc = vs.basis(vs.s_at((av_h + av_b) * .5))
            cl = _vf_o(vs, sc["s"]) + .006 + r.uniform(0, RELIEF * .22)
            tc = cl - sy * st + THICK * .5 * ct
            ax = sc[ka] if not flip else -sc[ka]
            e0 = .228 + r.uniform(-1, 1) * .012
            e1 = .432 + r.uniform(-1, 1) * .014
            cuts = (e0, lerp(e0, e1, .38 + .22 * ((k * 3) % 5) / 4.0), e1)
            for jj in range(2):
                lo = cuts[jj] + (GAP * .5 if jj else 0.0)
                hi = cuts[jj + 1] - (0.0 if jj else GAP * .5)
                M = (_frame(ax, sc["T"]) @ Matrix.Rotation(-th, 4, 'X')
                     @ Matrix.Rotation(radians(1.15 * YAW5[(k * 2 + jj) % 5]),
                                       4, 'Z'))
                p.tab(tuple(sc["P"] + sc[ka] * ((lo + hi) * .5) + sc[kn] * tc),
                      (hi - lo, sy * 2.0, THICK), _shmat(r, .022),
                      rot=M, tint=.085, taper=.94, head=(k == 0),
                      roll=SH_ROLL * (1 if (k + jj) % 3 else -1),
                      shade=.96 + r.uniform(-.13, .10))
    p.wobble(.004, freq=1.7)
    return p.finish()




# ================================================ 5c. the LACED valley =======
# WHY THERE IS A SECOND VALLEY, AND WHAT WAS WRONG WITH THE FIRST.
# SM_Roof_Valley_1m9 is a LEAD-LINED OPEN VALLEY: a dressed metal channel down
# the angle with shingle soakers lapping in over it from both sides. It is
# correct building and it is not what the references show. Two faults, and only
# the second is about colour:
#
#   1. THE SOAKER COURSES DO NOT RUN WITH THE FIELD'S COURSES. _arris lays its
#      cut courses in the frame (away, HIP_DIR) -- across the arris and up it --
#      so a soaker's course line runs along `away`, which is at
#      acos(1/HIP_K) = 31.6 degrees to the field's own course line (the field
#      courses run along X; `away` is perpendicular to the arris, not to the
#      slope). Every course therefore arrives at the valley, stops, and starts
#      again as a diagonal. That chevron is what makes the piece read as a band
#      of something else laid over the roof, whatever colour it is.
#   2. A bright grey strip down a mossy roof reads as a foreign object.
#
# A LACED (SWEPT) VALLEY is how a shingle or tile roof closes an angle without
# metal, and it is what every storybook inn has: the courses from the two slopes
# are carried THROUGH the angle over a rounded valley board, each course swinging
# round in a curve instead of being cut off against a channel. Nothing grey, no
# seam, one continuous shingled surface with a soft sweep down the angle.
#
# HOW THIS ONE IS BUILT -- the three facts that make the courses continuous:
#
#   * A COURSE IS A LINE OF CONSTANT SLOPE COORDINATE, on both planes. On plane A
#     (rising +y) that line runs along X and on plane B along Y, and BOTH are
#     lines of constant z. So course m of one roof and course m of the other are
#     already at the same height and already meet at the valley: they need no
#     step, only a bend. The band is therefore coursed in the SAME s the slope
#     panels are coursed in -- gauge ROW_S = SLOPE_SEG/13, heads at k*ROW_S --
#     so its courses land on the field's, course for course, on both sides.
#   * THE BEND IS ROUNDED, NOT MITRED, AND THE SURFACE AND THE LINE ARE ROUNDED
#     OVER DIFFERENT WIDTHS. In cross section the two lapped planes meet at 112
#     degrees; LC_R takes that vertex out into a trough, tight, because a rounded
#     V sitting inside a sharp one stands 0.205*R proud of it and a generous
#     radius lifts the sweep off the roof. The COURSE LINE's 90 degree kink in
#     plan is eased separately and much more broadly, over LC_SWP (see
#     _Lace.qeff, whose blend has zero slope at the trough bottom -- that is the
#     whole of the "swept" in swept valley). Tight boarding, wide walk: which is
#     how the real thing is laid. On top of that the courses SWING LC_DIP
#     down-slope as they cross, the swoop a laced valley gets from carrying its
#     courses round the extra length of the sweep. Every course swings by the
#     same amount, so the gauge is untouched and only the LINES bend -- and the
#     swing dies out well inside the band, so the band's outer courses are dead
#     on the field's own.
#   * THE LAP IS KEPT CONSTANT ROUND THE SWEEP. Two adjacent course lines are
#     0.123 apart on the flanks but 0.145 apart through the trough (the valley
#     advances HIP_K faster than either plane does), so a tab of one fixed
#     length would lose most of its lap exactly where the roof leaks. Each tab
#     is therefore built to the MEASURED perpendicular spacing at its own
#     position (see `sps`), so the step at every butt stays exactly RELIEF the
#     whole way round -- and the tabs are then cut to the FIELD'S proportions
#     through the sweep (LC_TABC, LC_DPF) rather than left to come out half as
#     wide and half as long again, which is what read as a picket fence.
#
# It laps the field it overruns (LC_LAP), it is one HIP_SEG long, it starts and
# ends on the same course rhythm, and its bottom course hangs 0.45 of a gauge
# below its own origin to lap the piece under it. So it is a DROP-IN swap for
# SM_Roof_Valley_1m9: same origin, same 45 degree plan line, same HIP_STEP
# tiling, same mirroring, same lap. In assemble_inn.valley_run() it is one
# string.
# N_SEG (13) and ROW_S (0.1231, the field's OWN gauge per plane) are defined up
# in the constants block, with the half/quarter-tile arithmetic that needs them.
LC_LAP  = THICK + .012   # HOW HIGH THE LACED SURFACE RIDES, and the number that
                         # decides whether the band reads as roof or as a strip
                         # laid over one. What it has to clear is the field that
                         # OVERRUNS the valley: those tabs' outer faces stand
                         # BUILD = 0.063 proud of the nominal plane. A band whose
                         # own SURFACE sat at BUILD (which is where the lead
                         # channel sits, and it is right for a channel) puts its
                         # tab butts a further 0.063 up, so the band's visible
                         # face stands 0.103 above the field's -- a 100 mm welt,
                         # 134 mm on the assembled roof. Riding at THICK + 0.012
                         # instead puts the band's tab UNDERSIDES 0.075 up, i.e.
                         # 12 mm clear of the field's tab tops, and its visible
                         # face 46 mm above the field's: the height of one course
                         # lapping the course below it, which is what a shingle
                         # roof does everywhere else anyway.
LC_R    = 0.145          # RADIUS OF THE SWEPT TROUGH, in cross section, and the
                         # one number to be careful with. A rounded V sitting
                         # inside a sharp one stands 0.205*R proud of it at the
                         # bottom, so a generous radius lifts the whole trough
                         # off the crease and the sweep stops reading as a
                         # valley and starts reading as a welt laid along one.
                         # 0.145 fills the bottom 30 mm of a 260 mm deep V:
                         # enough to take the crease out and carry a shingle
                         # round, not enough to bulge.
LC_W    = 0.380          # band half width, measured as ARC across the trough
LC_SWP  = 0.280          # HOW BROAD THE SWEEP IS: the half width over which a
                         # course line's 90-degree kink at the valley is eased
                         # into a curve. Deliberately NOT tied to LC_R. The
                         # surface rounding has to stay tight or the trough
                         # bulges (see LC_R), but a course eased over only that
                         # 0.086 turns the corner in 170 mm, which is a mitre
                         # with a fillet on it, not a sweep. Easing the LINE over
                         # 0.28 while the SURFACE rounds over 0.086 is exactly
                         # what a roofer does with a swept valley: the boarding
                         # is rounded tight in the angle and the courses are
                         # walked round it over a much wider zone.
LC_RAG  = 0.045          # per-course raggedness of the band's two outer edges
LC_DIP  = 0.055          # THE SWOOP: how far the courses swing DOWN-slope as
                         # they cross the trough, which is what a laced valley
                         # gets from carrying its courses round the extra length
                         # of the sweep. Rounding the surface already lifts the
                         # trough 22 mm in z on its own, so what the eye sees is
                         # the balance, about 21 mm here and 36 mm assembled.
                         # MEASURED, NOT GUESSED, AND THE TEMPTATION IS TO
                         # OVERDO IT. At 0.086 over the whole band width the
                         # band's courses ran a fifth of a course BELOW the
                         # field's for its whole width, and the band stopped
                         # reading as the roof's own courses and started reading
                         # as a separate strip laid down the angle -- the exact
                         # fault this piece exists to cure, reintroduced by
                         # decoration. Small, and local.
LC_DIPW = 0.240          # ... and it dies well INSIDE the band, with zero slope
                         # there, so the outer half of every course is dead on
                         # the field's own course line and only the sweep itself
                         # swings. That is what keeps the two continuous.
LC_SARK = 0.300          # half width of the boarding under the band. It has to
                         # stay INSIDE the raggedest course the band can lay
                         # (LC_W - LC_RAG), or the board shows through the gap at
                         # the edge as a brown patch on the roof.
LC_THK  = 0.034          # the band's tabs are thinner than the field's: a sweep
                         # is laid with thinner shingles because they have to
                         # bend, and every mm of it is a mm of step at the band's
                         # edge.
LC_TABC = 0.82           # tab width through the sweep, as a fraction of TAB. A
                         # sweep IS laid with narrower shingles, but not much
                         # narrower: at 0.62 the trough's tabs came out 0.09 wide
                         # by 0.21 long -- a picket fence standing up the valley,
                         # nothing like the field's 0.14 x 0.18 -- and that
                         # proportion, not the sweep itself, was what still read
                         # as a strip of something else.
LC_DPF  = 0.86           # ... and the same argument for their LENGTH. Two course
                         # lines are 0.123 apart on the flank and 0.145 apart
                         # through the trough (the valley advances HIP_K faster
                         # than either plane), so a full OV lap there makes a tab
                         # 0.21 long. The sweep is laid to a shorter lap instead
                         # -- 1.25 rather than 1.45, still a full cover -- so a
                         # tab in the trough is the same size as a tab in the
                         # field, which is the whole object of the exercise.
LC_LACE = (-.34, .10, -.10, .34)   # WHICH SHINGLE CROSSES THE TROUGH. Every
                         # course is cut into tabs OUTWARD FROM THE TROUGH, from
                         # a seed offset this far (in trough-tab widths) off the
                         # bottom, so a tab always LACES across the trough and a
                         # joint never lands in it. A joint down the trough is
                         # precisely the seam this piece exists to remove.
LC_H    = VF_H           # (1,-1,0)/sqrt2 -- horizontal, across the V


def _lc_rate(vs, s):
    """d(station)/d(flank distance) for a course on either plane: the rate at
    which a course line runs BACK down the valley as it goes out into the field.
    Exactly COS_P/HIP_K on the flat, which is where the 45 degree plan line and
    the 31.6 degrees of the last section both come from."""
    (ty, _tz), _n = vs.sf.frame(s)
    return ty / sqrt(1.0 + ty * ty)


def _lc_bell(w, halfw):
    """A smooth hump, 1 at w = 0 and flat-zero at +/- halfw."""
    if halfw <= 0.0 or abs(w) >= halfw:
        return 0.0
    u = 1.0 - (w / halfw) ** 2
    return u * u


class _Lace:
    """The laced valley SURFACE: the two roof planes, each lifted `lap` clear of
    the field it laps, meeting in a rounded trough of radius `r` instead of in a
    crease. Parametrised by (s, w):

        s  each plane's own slope coordinate -- the same s the slope panels and
           the eave are coursed in, and equal on the two planes along a valley;
        w  signed ARC across the trough, 0 at its bottom, +ve into plane B.

    It takes a _VSurf, so it rides a bell-cast eave as happily as a flat plane:
    _VSurf(sweep=0) is the ordinary length, VFT the foot of a run."""

    def __init__(self, vs, lap=LC_LAP, r=LC_R, dip=LC_DIP, dipw=LC_DIPW,
                 swp=LC_SWP):
        self.vs = vs
        self._lap = lap if callable(lap) else (lambda s, v=lap: v)
        self.r, self.dip, self.dipw, self.swp = r, dip, dipw, swp
        self._c = {}

    # ---- the cross section at one station ----------------------------------
    def sect(self, s):
        key = round(s, 6)
        sc = self._c.get(key)
        if sc is not None:
            return sc
        b = self.vs.basis(s)
        up = b["up"]
        cph = clamp(up.dot(b["nA"]), .02, 1.0)   # cos of the flank angle from up
        sph = sqrt(max(0.0, 1.0 - cph * cph))
        ph = atan2(sph, cph)
        yv, zv = self.vs.sf.pt(s, self._lap(s))  # where the two LAPPED planes meet
        V = Vector((yv, yv, zv))
        sc = dict(V=V, up=up, aA=b["aA"], aB=b["aB"], nA=b["nA"], nB=b["nB"],
                  T=b["T"], cph=cph, sph=sph, ph=ph,
                  C=V + up * (self.r / cph),     # centre of the rounding
                  wr=self.r * ph,                # arc of the round, each side
                  qt=self.r * sph / cph)         # where it leaves the flank
        self._c[key] = sc
        return sc

    def prof(self, sc, w):
        """(point, outward normal, across-tangent) at across-arc w."""
        wr = sc["wr"]
        if abs(w) <= wr:
            ps = w / self.r
            cs, sn = cos(ps), sin(ps)
            return (sc["C"] + (LC_H * sn - sc["up"] * cs) * self.r,
                    sc["up"] * cs - LC_H * sn,
                    LC_H * cs + sc["up"] * sn)
        if w > 0.0:
            return (sc["V"] + sc["aB"] * (sc["qt"] + w - wr), sc["nB"], sc["aB"])
        return (sc["V"] + sc["aA"] * (sc["qt"] - w - wr), sc["nA"], -sc["aA"])

    def qeff(self, sc, w):
        """Flank distance from the vertex -- but eased, over +/- LC_SWP, into a
        curve with ZERO SLOPE at the trough bottom. Feed it to `station` and the
        course line's 90 degree kink at the arris becomes a smooth sweep, while
        outside the easing width the flanks stay EXACTLY where the field's own
        courses are, which is what keeps the two continuous."""
        ws = self.swp
        q1 = sc["qt"] + ws - sc["wr"]              # flank distance at the join
        if abs(w) >= ws or q1 <= 1e-6:
            return max(sc["qt"] + abs(w) - sc["wr"], 0.0)
        t = abs(w) / ws
        e = ws / q1                    # f(1)=1, f'(1)=ws/q1 (smooth join), f'(0)=0
        a, b = 3.0 - e, e - 2.0
        return q1 * (a * t * t + b * t * t * t)

    def station(self, s_head, w):
        """The station at which the course of plane-coordinate `s_head` crosses
        across-arc w: back down the flank at the geometric rate, plus the lace's
        own swing down-slope through the trough."""
        s = s_head
        for _ in range(2):             # exact in one pass on a flat valley
            s = (s_head - _lc_rate(self.vs, s) * self.qeff(self.sect(s), w)
                 - self.dip * _lc_bell(w, self.dipw))
        return s

    def point(self, s_head, w):
        sc = self.sect(self.station(s_head, w))
        P, N, _a = self.prof(sc, w)
        return P, N


def _lc_sark(p, lc, s0, s1, half=LC_SARK, depth=.055, n=7, ramp=.005,
             mat="oak_dark", shade=.30, rise=.010):
    """The valley board under the band: a solid that follows the trough, so no
    daylight shows through the slots between tabs and every course butt has
    something dark behind it.

    ITS ENDS FOLLOW THE COURSE LINES, not the stations. A board cut square
    across the valley leaves two big triangles of itself standing proud of the
    field at the head of the piece -- a course line runs BACK down the valley as
    it goes out into the field (see _lc_rate), so the band it carries is a
    parallelogram in (station, across), not a rectangle. Squaring it off was
    worth two 0.07 m2 dark wedges either side of the head. So the rings are
    placed with the same lc.point() the courses are.

    Its top also RAMPS `ramp` down over its own length, so the board of one
    length lies just clear of the board of the length below it instead of
    sharing a plane with it (the VLIFT trick, for the same reason).

    It is carried 10 mm ABOVE the surface, not 2 mm like the field's boarding.
    In the trough a course's tabs stand on end along the valley, so the 7 mm slot
    between two of them is a 180 mm long slit pointing straight at anyone looking
    down the roof, and with 21 mm of air under it the board at the bottom read as
    a brown streak rather than as a shadow. Ten millimetres halves the slit and
    still leaves 13 mm of clearance under the last exposed part of a tab."""
    rings = []
    for i in range(n):
        sa = lerp(s0, s1, i / (n - 1.0))
        lift = ramp * (1.0 - (sa - s0) / max(s1 - s0, 1e-6))
        top, bot = [], []
        for j in range(5):
            P, N = lc.point(sa, lerp(-half, half, j / 4.0))
            top.append(P + N * (lift + rise))
            bot.append(P + N * (lift - depth))
        rings.append(top + bot[::-1])
    return _sweep(p, rings, mat, tint=.03, shade=shade)


def _laced(p, lc, ks, seed, w=LC_W, rag=LC_RAG, thick=LC_THK, relief=RELIEF,
           moss=.022, mat=SH, tint=.085, ns=40, head_k=None, tabf=1.0,
           dpf=1.0, cl_off=0.0, turn=0.0, curl=.05, course_var=.150,
           shade_var=.135, wander=1.0, taper=.95, key=None):
    """Lay the field's own courses ROUND the trough, one strip of tabs per
    course running unbroken from plane A through the sweep into plane B.

    Each course is sampled as a curve first (`pts`), then cut into tabs by ARC
    LENGTH along that curve -- which is what keeps a tab the same width whether
    it is out on the flank beside the field or standing on end in the trough --
    and every tab is given the tilt, the length and the lap that its OWN
    measured course spacing asks for, so the course step stays exactly `relief`
    the whole way round. `turn` rotates a course down over the end of the piece
    (the boot at the foot of a run).

    A course's position here is sa = k*ROW_S, indexed straight off the field's
    own gauge, so a shorter run of ks is at the full piece's gauge by
    construction. `key` goes further and puts it on the full piece's RNG stream
    as well, so a part-length laced valley is not merely at the same gauge -- it
    is the full piece's courses 1..n, sweep jitter and all."""
    r = rng(f"{key or p.name}/laced/{seed}")
    ks = list(ks)
    top = ks[-1] if head_k is None else head_k
    out = []
    dip0, swp0 = lc.dip, lc.swp
    for k in ks:
        # A hand-laid sweep is not a machined fan: swing each course a little
        # more or less than the last, and start its curve a little sooner or
        # later. Restored below, so the boarding and every other course see the
        # nominal figures.
        lc.dip = dip0 * (1.0 + r.uniform(-.14, .14) * wander)
        lc.swp = swp0 * (1.0 + r.uniform(-.08, .08) * wander)
        sa = k * ROW_S
        WA = w + r.uniform(-1, 1) * rag * wander
        WB = w + r.uniform(-1, 1) * rag * wander
        ws = [lerp(-WA, WB, i / (ns - 1.0)) for i in range(ns)]
        pts, nrm = [], []
        for wi in ws:
            P, N = lc.point(sa, wi)
            pts.append(P)
            nrm.append(N)
        below = [lc.point(sa - ROW_S, wi)[0] for wi in ws]
        tang, arc = [], [0.0]
        for i in range(ns):
            a = pts[max(i - 1, 0)]
            b = pts[min(i + 1, ns - 1)]
            tang.append((b - a).normalized())
            if i:
                arc.append(arc[-1] + (pts[i] - pts[i - 1]).length)
        sps = [((pts[i] - below[i])
                - tang[i] * (pts[i] - below[i]).dot(tang[i])).length
               for i in range(ns)]
        total = arc[-1]
        a_mid = total * .5                      # arc at the trough bottom, w = 0
        for i in range(1, ns):
            if ws[i - 1] <= 0.0 <= ws[i]:
                t = -ws[i - 1] / max(ws[i] - ws[i - 1], 1e-9)
                a_mid = lerp(arc[i - 1], arc[i], t)
                break

        def probe(a):
            """(w, point, tangent, normal, course spacing) at arc a."""
            i = 1
            while i < ns - 1 and arc[i] < a:
                i += 1
            t = (a - arc[i - 1]) / max(arc[i] - arc[i - 1], 1e-9)
            T = tang[i - 1].lerp(tang[i], t).normalized()
            N = nrm[i - 1].lerp(nrm[i], t)
            N = (N - T * N.dot(T)).normalized()
            return (lerp(ws[i - 1], ws[i], t), pts[i - 1].lerp(pts[i], t),
                    T, N, lerp(sps[i - 1], sps[i], t))

        # ---- cut the course into tabs, OUTWARD FROM THE TROUGH ------------
        # Not from one end: a course cut from its end drops a joint wherever the
        # arithmetic lands, and a joint in the trough is a seam straight down the
        # valley -- the one thing this piece exists to remove. Seeded a fraction
        # of a tab off the bottom instead, a shingle always LACES across the
        # trough, and which shingle it is walks with the course (LC_LACE), which
        # is what lacing means. Tabs narrow through the sweep as well.
        def step(a, sgn):
            wq = probe(clamp(a + sgn * TAB * .4, 0.0, total))[0]
            return (TAB * tabf * lerp(LC_TABC, 1.0,
                                      smoothstep(0.0, lc.swp, abs(wq)))
                    * (1.0 + r.uniform(-.06, .06) * wander))

        a_seed = clamp(a_mid + LC_LACE[int(k) % 4] * TAB * tabf * LC_TABC,
                       0.0, total)
        hi_e, lo_e = [a_seed], [a_seed]
        while hi_e[-1] < total:
            hi_e.append(hi_e[-1] + step(hi_e[-1], 1.0))
        while lo_e[-1] > 0.0:
            lo_e.append(lo_e[-1] - step(lo_e[-1], -1.0))
        edges = lo_e[::-1][:-1] + hi_e
        # ONE tone for the whole course, like _field: what varies then reads as
        # weathering running along the courses instead of as confetti.
        csh = 1.0 + r.uniform(-course_var, course_var * .8)
        pw = (r.uniform(0, 6.283), r.uniform(.05, .13) * ROW_S * wander)
        # one skew and one yaw amplitude per course; the harmonics below carry
        # the variation ALONG it, so two neighbours cannot draw opposite extremes
        sks = (1.0 if r.random() < .5 else -1.0) * r.uniform(.55, 1.0)
        yws = (1.0 if r.random() < .5 else -1.0) * r.uniform(.55, 1.0)
        # HOW FAR THE COURSE TURNS ACROSS EACH JOINT, and why it matters.
        # A tab is a CHORD of its course and it is pivoted on the course line at
        # its HEAD, so two neighbours meeting at a joint are two chords hinged at
        # their head ends: where the course curves -- and through the sweep it
        # curves hard, LC_R is a 145 mm radius -- their facing side faces FAN, and
        # on the closing side of the bend they run together over the tab's own
        # length. dp*sin(turn) is 18 mm at the 5.8 deg turn measured beside the
        # trough, against a 7 mm slot, so the two tabs crossed. That is the
        # remaining shingle-on-shingle pair on both laced pieces (50 cm2 at
        # (0.346, 0.136, 0.568) on the eave length), and no amount of bounding the
        # per-tab draws touches it: the fan is in the course, not in the jitter.
        # So the joint inset is no longer a flat GAP/2 -- it OPENS by half the
        # closing rate, only on the side that closes, so the slot at the visible
        # BUTT end stays GAP the whole way round the sweep and the extra width
        # goes into the head, under the lap where nothing sees it.
        cpt, cnm = [], []
        for e in edges:
            _q = probe(min(max(e, 0.0), total))
            cpt.append(_q[1])
            cnm.append(_q[3])
        cdir = []
        for j in range(len(edges) - 1):
            _d = cpt[j + 1] - cpt[j]
            cdir.append(_d.normalized() if _d.length > 1e-9 else Vector((1, 0, 0)))

        # RENAMED from `turn`, which SHADOWED the scalar `turn=0.0` parameter in this
        # function's own signature. By the time the tab matrix used radians(turn) the
        # name held this function, so every roofs build died with
        # "TypeError: must be real number, not function" -- the whole kit, since
        # check_zfight, build_kit and assemble_inn all build roofs. Introduced by a
        # fixer that was killed by a session limit mid-edit.
        def joint_turn(j):
            """sin of the course's turn across joint j, signed POSITIVE when the
            two tabs meeting there converge as they run down-slope."""
            if j <= 0 or j >= len(cdir):
                return 0.0
            return cdir[j].cross(cdir[j - 1]).dot(cnm[j])

        for i in range(len(edges) - 1):
            lo, hi = max(edges[i], 0.0), min(edges[i + 1], total)
            if hi - lo < TAB * .30:
                continue
            # A TAB IS A CHORD OF ITS COURSE, not a tangent to it. Placed on the
            # tangent at its own midpoint, a straight box spanning the sweep
            # lifts both its ends off the surface by the sagitta -- 17 mm on the
            # tab that laces the trough, which is half its own thickness again.
            # Built between its two END points instead, it sinks its middle into
            # the boarding by that much and lands flat: the same thing a shingle
            # does when it is bent over a rounded valley board.
            wq, P, T, N, sp = probe((lo + hi) * .5)
            _w0, P0, _t0, N0, _s0 = probe(lo)
            _w1, P1, _t1, N1, _s1 = probe(hi)
            T = (P1 - P0).normalized()
            N = (N0 + N1 + N)
            N = (N - T * N.dot(T)).normalized()
            P = (P0 + P1) * .5
            wid = (P1 - P0).length
            # A CURLED SHAKE LIFTS ITS BUTT, NOT ITS BODY -- the same correction
            # _field carries, for the same measured reason. `pl` used to be added
            # to `cl`, i.e. it raised the whole tab including the head the course
            # above has to clear, spending up to 16 mm of a 32 mm relief. Rolled
            # into the tilt as (relief + pl) / sp it pivots the tab on the course
            # line one gauge above its butt, which is the line the next course's
            # butt lands on: the butt still stands the full `pl` proud and the
            # head now tips away from the course above instead of into it.
            pl = r.uniform(.18, CURL_MAX) * thick if r.random() < curl else 0.0
            th = atan2(relief + pl, sp)
            ct, st = cos(th), sin(th)
            dp = (sp * OV * dpf
                  * lerp(LC_DPF, 1.0, smoothstep(0.0, lc.swp, abs(wq)))
                  * (1 + r.uniform(-.05, .04) * wander))
            sy = dp * .5 / ct
            # butt underside above the surface
            cl = (cl_off + LIFT * (relief / RELIEF if RELIEF else 1.0) + pl
                  + r.uniform(0, relief * .22))
            tc = cl - sy * st + thick * .5 * ct
            # the butt line wanders along the course, coherently, plus a little
            # per-tab jitter -- the same two things _field does
            wd = (pw[1] * sin(2 * pi * (lo + hi) * .5 / .82 + pw[0])
                  + r.uniform(-1, 1) * ROW_S * .035 * wander)
            # the joint insets: GAP/2 each side, opened by half the closing rate
            # wherever the course turns the way that runs two tabs together
            ilo = GAP * .5 + min(dp * max(0.0, joint_turn(i)) * .55, wid * .16)
            ihi = GAP * .5 + min(dp * max(0.0, joint_turn(i + 1)) * .55, wid * .16)
            wid -= ilo + ihi
            P = P + T * ((ilo - ihi) * .5)
            up = N.cross(T)                        # up-slope, in the surface
            # YAW AND SKEW ARE SMOOTH IN ARC ALONG THE COURSE, not drawn per tab.
            # These tabs already share their joints -- a course is cut at `edges`
            # and every tab is inset GAP from both of them -- so the slot could
            # only be closed by the two rotations that slant a side face, and
            # both of them were drawn independently: YAW5 puts up to 2.3 deg
            # between consecutive tabs and the skew draw put up to 12 mm, against
            # a 7 mm slot. That is the 47.3 cm2 of shingle-on-shingle on
            # SM_Roof_ValleyLaced_Eave_1m9 at (0.194, 0.016, 0.372), 0.46 mm
            # apart. As harmonics of arc with periods long against TAB the
            # amplitude at any one tab is unchanged and two neighbours differ by
            # 0.5 deg and 2 mm. (YAW5 stays as it is in _arris, where the tabs it
            # separates share no joint and genuinely do overlap each other.)
            M = (_frame(T, up) @ Matrix.Rotation(radians(turn) - th, 4, 'X')
                 @ Matrix.Rotation(radians(1.15) * yws
                                   * sin(2 * pi * (lo + hi) * .5 / 1.40), 4, 'Z'))
            ctr = P + up * (wd - dp * .5) + N * tc
            out += p.tab(tuple(ctr), (wid, sy * 2.0, thick),
                         _shmat(r, moss if abs(wq) < lc.r * .85 else 0.0, 0.0,
                                mat),
                         rot=M, tint=tint, taper=taper, head=(k >= top),
                         roll=SH_ROLL * (1 if (int(k) * 3 + i * 5) % 3 else -1),
                         skew=(SKEW_A * sks
                               * sin(2 * pi * (lo + hi) * .5 / 2.40), 0.0),
                         shade=csh * (1.0 + r.uniform(-shade_var,
                                                      shade_var * .8)))
    lc.dip, lc.swp = dip0, swp0
    return out


VFLAT = _VSurf(sweep=0.0)          # the ordinary, un-swept valley curve


def valley_laced(nk=None, nm=None):
    """THE LACED VALLEY -- a drop-in alternative to SM_Roof_Valley_1m9 with no
    metal in it. Same origin, same 45 degree plan line, same HIP_SEG length,
    same mirroring and the same lap, so a run of these places exactly where a
    run of lead ones does. What it shows is the roof's own courses sweeping
    round the angle: same gauge, same tabs, same course step, no channel.

    PART LENGTHS. `nk` is a course count, and this piece makes the arithmetic
    obvious: its courses live at sa = k*ROW_S in each plane's OWN slope
    coordinate -- the same coordinate the slope panels are coursed in -- so a
    run of nk courses is at ROW_S whatever nk is, and 7 + 3 + 3 = N_SEG rebuilds
    a whole length. Both partials are laid on the full piece's RNG key, so their
    courses ARE its courses 1..nk. Its foot laps the piece below by the bottom
    course's own 0.45 of a gauge, exactly as the full piece does, so any mix of
    lengths stacks."""
    nk = N_SEG if nk is None else nk
    st = hip_step(nk * ROW_S * HIP_K)
    p = _Part(nm or "SM_Roof_ValleyLaced_1m9", budget="roof",
              seams=dict(x=(-.62, st.x + .62),
                         y=(-.62, st.y + .62),
                         z=(-.36, st.z + .40)))
    lc = _Lace(VFLAT)
    _lc_sark(p, lc, -.115, nk * ROW_S + .002)
    _laced(p, lc, range(1, nk + 1), seed=3,
           key="SM_Roof_ValleyLaced_1m9" if nk != N_SEG else None)
    p.wobble(.005, freq=1.7)
    return p.finish()


def valley_laced_eave():
    """THE FOOT OF A LACED RUN, for the same reason SM_Roof_Valley_Eave_1m9
    exists: an ordinary length is laid identically at every step of a run, so it
    cannot carry a bottom-of-run-only bend, and the bottom of a run is exactly
    where the roof stops being a plane. This one rides the two bell-cast eave
    surfaces (VFT) all the way to the corner where the two drip edges meet, and
    finishes in a BOOT -- a last course turned down over the corner, which is
    what a swept valley does in place of the lead one's drip roll.

    It REPLACES the lowest ordinary length of a run: place it at the run's p0
    with the same mirroring and start the ordinary lengths one step up. Its head
    is an ordinary head, so the length above laps it with the ordinary lap."""
    lc = _Lace(VFT, lap=lambda s: LC_LAP + VF_LIFT * smoothstep(VF_LIFT_S, 0.0, s))
    p = _Part("SM_Roof_ValleyLaced_Eave_1m9", budget="roof",
              seams=dict(x=(-.85, HIP_STEP.x + .62),
                         y=(-.85, HIP_STEP.y + .62),
                         z=(-.46, HIP_STEP.z + .40)))
    # THE SARK STOPS ON THE BOOT'S OWN COURSE LINE, not 0.26 of arc past it.
    # -0.34 was a "generous" constant chosen when the surface below the drip
    # still dived at 52 deg, so the extra arc mostly went DOWN and out of sight.
    # With the bell-cast straightened (see _Surf.d) the same constant put the
    # board 0.41 m outboard of the last shingle and 0.41 m past this piece's
    # declared x seam, where finish() cut it. That is also the exact defect
    # assemble_inn.py refuses to place this piece for -- "its sark board
    # reaching 0.12 past its last shingle and 0.43 past the eave drip, a blank
    # slab hanging out of the silhouette". Tying it to the boot's own arc fixes
    # both, and it cannot drift again if the sweep is retuned.
    _lc_sark(p, lc, -0.62 * ROW_S, L + .002, n=9)
    _laced(p, lc, range(1, N_SEG + 1), seed=4)
    # the starter course under the lowest one, and the boot that turns down over
    # the corner: the two eaves' drip edges meet at a point out here, and the
    # sweep has to close over it or the run ends in a cliff.
    _laced(p, lc, [0.02], seed=5, w=LC_W - .045, dpf=.92, cl_off=-.016,
           curl=0.0, wander=.5, head_k=99, moss=0.0)
    _laced(p, lc, [-0.62], seed=6, w=LC_W - .085, dpf=1.05, turn=52.0,
           cl_off=-.004, curl=0.0, wander=.5, head_k=99, moss=0.0)
    p.wobble(.004, freq=1.7)
    return p.finish()

# -------------------------------------------------- 6. roof-to-wall flashing --
def flashing():
    """Apron flashing where a slope falls away from a wall -- the downhill face
    of a chimney, or a lean-to abutment. Wall face on Y=0 rising +Z, roof falls
    away in -Y at 52 deg, tiles along X at GRID. Lead upstand with a tuck-in
    bead, a cover sheet down the slope with its nose turned over the course
    below, then four laps of shingle soakers."""
    p = _Part("SM_Roof_Flash_Wall_2m", budget="roof",
              seams=dict(x=(-HB, HB), y=(-.95, .09), z=(-1.20, .38)))
    ey = Vector((0, -COSP, -SINP))            # down-slope, away from the wall
    nz = Vector((0, -SINP, COSP))             # out of the roof
    M = _frame((-1, 0, 0), ey)
    p.box((0, .024, .140), (G, .030, .282), LEAD, bevel=0, tint=.05, shade=.88)
    p.box((0, .034, .288), (G, .056, .040), LEAD, bevel=.008, seg=1, tint=.05,
          shade=1.00)
    # The cover sheet: 0.40 DOWN THE SLOPE and 20 mm thick. Its size was
    # (G, .020, .400) -- 20 mm of slope by 400 mm out of the roof -- so this
    # piece was shipping a 2 m x 0.4 m lead fin standing off the slope, which is
    # the black slab in the old lineup render. Set off BUILD so the soakers tuck
    # under it instead of poking through it.
    c = ey * .130 + nz * (BUILD + .014)
    p.box((0, c.y, c.z), (G, .270, .020), LEAD, rot=M, bevel=0, tint=.05,
          shade=.92)
    c = ey * .268 + nz * (BUILD + .011)   # top clear of the sheet's plane
    p.box((0, c.y, c.z), (G, .076, .042), LEAD, rot=M, bevel=.010, seg=1,
          tint=.05, shade=.86)
    # Soakers, laid UP the slope: ey pointed down-slope here, which laid every
    # course butt-uphill -- invisible while the courses were flat, a row of
    # backwards steps now that they are not.
    _pfield(p, (0, 0, 0), (1, 0, 0), tuple(-ey), -HB, HB,
            -(.24 + ROW * 4), -.24, seed="flash", t0=.004)
    p.box((0, -.022, -.034), (G, .058, .058), "oak_dark", bevel=0, tint=.03,
          shade=.34)
    p.wobble(.005, freq=1.8)
    return p.finish()


# ------------------------------------ 6b. roof-to-wall STEP FLASHING ---------
# WHY THIS PIECE EXISTS, AND WHY THE APRON COULD NOT BE IT.
# SM_Roof_Flash_Wall_2m is an APRON: its own docstring fixes the condition as
# "Wall face on Y=0 rising +Z, roof falls away in -Y", i.e. the slope runs
# DOWN-HILL AWAY from the wall and the joint is one horizontal line across the
# fall. That is the downhill face of a chimney, and it is the only roof-to-wall
# condition this family had.
# It is the wrong condition for a roof running SIDEWAYS into a wall -- a range
# meeting the flank of a cross wing, which is what every roof-to-wall junction on
# the example inn actually is. There the fall line is PARALLEL to the wall, the
# joint climbs the wall at the pitch, and one horizontal apron laid across it
# either floats above the roof at one end or is buried at the other. What that
# condition wants is soakers and a STEP FLASHING: a lead tongue under every
# course turned up against the wall, and a cover cut in steps that follow the
# courses -- the staircase line every stone building has where a roof dies into
# a gable flank.
#
# ITS FRAME IS THE VERGE'S, because it does the same job one edge over: it closes
# the edge of a roof that runs UP THE SLOPE, so it tiles up the slope at
# slope_vec(1) and not along the ridge. Wall face on X = 0 with the wall body in
# +X and the roof falling away in -X; origin on the nominal 52 deg slope at the
# wall face. Mirror in X for the other hand.
FS_TONG  = 0.190     # how far a soaker's tongue reaches out into the roof
FS_UP    = 0.155     # upstand height, measured VERTICALLY off the roof surface
FS_LEADT = 0.013     # lead thickness -- the same 13-14 mm the valley uses
FS_CUT   = (0.150, 0.305)   # the cut course band, out from the wall face. 0.155
                     # wide, so _pfield lays ONE tab per course at 0.155 against
                     # the field's own 0.1429 -- a cut shingle, which is what a
                     # course beside a wall is, rather than a wide plate.
FS_COVH  = 0.115     # depth of one step of the cover flashing
FS_COVX  = -0.0265   # ... and how far it stands off the wall face. The upstand
                     # sits at -0.0075 and is 13 mm thick, so the cover's back
                     # face is 5.5 mm clear of the upstand's front face: it laps
                     # it without sharing a plane with it.


def flash_step(nrow=N_SEG, nm=None):
    """STEP FLASHING for a SIDE ABUTMENT -- a roof running into a wall that
    rises past it. Wall face on X = 0, wall body +X, roof falls away in -X;
    origin on the nominal 52 deg slope at the wall face; climbs +Y by
    SLOPE_SEG*cos P and +Z by SLOPE_SEG*sin P, so it tiles UP THE SLOPE at
    slope_vec(1) exactly as the verge does. Mirror in X for the other hand.

    Four layers, and each of them keeps the field's own gauge because it is
    indexed on the field's own courses:
      * cut courses lying on the roof, laid by _pfield at ra = span/nrow, which
        for a whole number of ROW_S is 0.123077 -- the slope panel's gauge, so
        the cut course beside the wall lands on the course beside it;
      * one lead SOAKER per course under them, 1.7 courses long so consecutive
        soakers lap by 0.7 of a course. Alternate soakers stand 5.5 mm further
        out of the roof, because two lapping sheets laid at one offset put 163
        cm2 of coincident lead face on every lap -- the defect this file has
        closed twice already, in the valley welts and in the batten tops;
      * a continuous upstand turned up the wall FS_UP off the roof surface;
      * the COVER, cut in steps, one step per course: tread ra*cos P = 0.0758,
        rise ra*sin P = 0.0971, which is the pitch, so the staircase reads as
        the roof's own courses climbing the wall. Alternate steps sit 4 mm
        further off the wall for the same reason the soakers do.

    `nrow` shortens it up the slope in whole courses, exactly like slope()."""
    span = nrow * ROW_S
    ra = span / nrow
    sf = FLAT
    p = _Part(nm or "SM_Roof_Flash_Step_1m6", budget="roof",
              seams=dict(x=(-.42, .02), y=(-.24, span * COSP + .06),
                         z=(-.26, span * SINP + FS_UP + .10)))
    r = rng(p.name)
    # boarding, so the joint is never open to daylight
    _slab(p, sf, -.40, -.004, -0.10, span + .01, -SLAB, .002, n=2)
    # ---- soakers: one per course, lapping, alternately proud ---------------
    for k in range(nrow):
        _put(p, sf, -FS_TONG * .5 - .008, (k + .5) * ra, LIFT - .004
             + (k % 2) * .0055, (FS_TONG, 1.7 * ra, FS_LEADT), LEAD, bevel=0,
             tint=.04, shade=.30)
    # ---- the cut courses on the roof --------------------------------------
    _pfield(p, (0, 0, 0), (1, 0, 0), (0, COSP, SINP),
            -FS_CUT[1], -FS_CUT[0], 0.0, span, seed="step", t0=.004)
    # ---- the upstand, turned up the wall -----------------------------------
    ss = (-.05, span + .05)
    base = [sf.pt(s, BUILD + .004) for s in ss]
    poly = [(base[0][0], base[0][1]), (base[1][0], base[1][1]),
            (base[1][0], base[1][1] + FS_UP), (base[0][0], base[0][1] + FS_UP)]
    p.prism(poly, FS_LEADT, LEAD, axis='X', at=(-.0075, 0, 0), bevel=0,
            tint=.04, shade=.34)
    # ---- the cover, cut in steps that follow the courses -------------------
    for k in range(nrow):
        yb, zb = sf.pt((k + 1) * ra, BUILD + .004)
        y0 = sf.pt(k * ra, BUILD + .004)[0] - .55 * ra * COSP
        p.box((FS_COVX - (k % 2) * .004, (y0 + yb) * .5,
               zb + FS_UP - FS_COVH * .5), (.014, yb - y0, FS_COVH), LEAD,
              bevel=0, tint=.04, shade=.46 + r.uniform(-.04, .04))
    p.wobble(.005, freq=1.8)
    return p.finish()


# ---------------------------- 6c. the EAVE'S side abutment, and its stop end --
# WHY THERE ARE TWO MORE PIECES HERE, AND WHY THE 13-COURSE STEP FLASHING IS NOT
# EITHER OF THEM.
#
# Shanee, on a close-up of the inn's cross-wing junction: "There is a hole/gap in
# the roof ... The 2 roof lines / eaves are different heights. Is that
# intentional? I think it's fine but I wonder if we need any special pieces in
# some cases to make it look more natural."
#
# The step IS intentional -- assemble_inn's range datum is 8.80 + BASE and its
# cross wing's is 9.60 + BASE, and a wing datum BELOW the range's would drop the
# wing's eave clear of the range's roof and leave no valley line to lay at all.
# What was missing is the two pieces that close the junction the step makes.
# Measured on the assembled inn (52 deg world, i.e. before putr's ZK stretch):
#
#   range eave anchor   z52 5.341639   world  8.9498
#   wing  eave anchor   z52 5.819116   world  9.7498     <- the 0.800 m step
#   wing roof plane at the wing's own wall face (its datum / ZK)
#                       z52 5.998308   world 10.0500
#
# so THE ABUTMENT IS 1.100 m OF WORLD HEIGHT, NOT 0.800. The extra 0.300 is the
# eave's own drop below its datum, EAVE_OVER * tan P = 0.179192 in the 52 world
# -- the number eave()'s docstring already states -- because a flashing starts at
# the eave's ANCHOR and the anchor is not the datum. Measured three ways, in
# courses (flat gauge, one course rises ROW_S*sin P = 0.096986):
#
#   up to the wing's eave anchor  0.477477  ->  4.92 courses
#   up to the wing's eave TRIM    0.485477  ->  5.01 courses   <- the visible joint
#   up to the wing's roof plane   0.656669  ->  6.77 courses   <- the whole joint
#
# and the count that actually decides it is neither of the first two: it is what
# still FITS. The cover flashing carries FS_UP = 0.155 of upstand above the roof
# surface, so the top of the lead at nrow courses sits at surface + 0.041 + 0.155:
#
#   nrow = 4   top 0.54458                       0.112 clear of the wing's plane
#   nrow = 5   top 0.64598                       0.011 clear                <- ok
#   nrow = 6   top 0.74738     0.091 THROUGH the wing's roof plane, 0.152 world
#
# So nrow = 5. Four leaves 0.22 m of world height of open joint at the most
# visible corner on the building; six pushes the top step of the cover 0.152 m
# out through the wing's roof. Five stops 0.060 m of world height short of the
# wing's fascia bottom with the CUT COURSES and covers all of it with the LEAD,
# which is what a step flashing is for, and its upstand runs 0.037 m under the
# wing's own roof boarding, which is what an upstand is for.
#
# AND IT CANNOT BE THE FLAT PIECE SHORTENED. SM_Roof_Flash_Step_1m6 is built on
# FLAT. This abutment starts at an EAVE, and the bottom SWEEP_LEN = 0.38 of an
# eave is displaced up to SWEEP = 0.22 out along the slope normal by the
# bell-cast (see _Surf.d): at s = 0 the eave's own shingle surface stands
# 0.22 + BUILD = 0.283 out of the nominal plane while a flat flashing's cover
# tops out at BUILD + FS_UP = 0.218, so the flat piece would be BURIED -- its
# lead 0.065 UNDER the shingles it is meant to cover, and its first 3.5 courses
# (arc 0.4528 of sweep / ra) inside the roof. So this piece is built on the
# EAVE'S OWN SURFACE, _Surf(sweep=S.SWEEP), and takes the eave's own arc gauge:
#
#   slope panel / flat flash_step   13 courses over s = 1.600     ra 0.123077
#   swept eave / this piece         13 courses over arc 1.672839  ra 0.128680
#
# Thirteen courses per SLOPE_SEG in both, which is what makes them lock together;
# the arc gauge is larger only because the swept surface is longer than the
# chord. 5 * 0.128680 = 0.643399 of arc, s = 0.570560 -- hence the 0_m6 in the
# name. That is exactly the eave course's own courses 1..5.
#
# The pattern is the family's own: valley() has valley_eave(), valley_laced() has
# valley_laced_eave(), and the eave version is its OWN function rather than a
# branch, because the surface, the gauge and the reach down-slope all change.
ES_DOWN  = -0.09     # how far DOWN-SLOPE, in ARC, the upstand and soakers run
                     # past the piece origin. The eave's lowest field course
                     # butts at arc -0.45*ra = -0.0579 (local y -0.2312); at the
                     # flat piece's -0.05 the upstand stopped 0.008 SHORT of it
                     # and left the drip course's own joint open. -0.09 reaches
                     # 0.032 past it. The eave's TRIM runs further still, to
                     # local y -0.4189, and is closed by the stop end below, not
                     # by lead.
ES_SLAB  = -0.13     # ... and the boarding, one course further out again
ES_NSEC  = 6         # sections in the swept boarding and the swept upstand. The
                     # flat piece uses a 2-point prism, which on a curved surface
                     # is a chord: it would sag 0.03 below the sweep at mid-span
                     # and take the upstand's effective height with it.


def flash_step_eave(nrow=5, nm=None):
    """STEP FLASHING for the SIDE ABUTMENT AT AN EAVE -- the bottom of the
    junction where a range's roof dies into the flank of a cross wing standing
    one eave-step higher. Read the block above for the measurement that fixes
    nrow at 5 and for why the flat SM_Roof_Flash_Step_1m6 cannot serve here.

    FRAME -- identical to SM_Roof_Flash_Step_1m6's, so the two stack up the same
    wall, and identical to SM_Roof_Eave_StopEnd's, so the assembler places this
    piece and the stop end at ONE point:
      * wall face on X = 0, wall body +X, roof falls away in -X;
      * origin ON THE NOMINAL 52 deg SLOPE at the wall face, at the EAVE COURSE'S
        OWN ANCHOR -- the same (x, y, z52) the assembler already places
        SM_Roof_Eave_2m at, offset only along the run to the wall plane. The
        piece's own surface is the eave's, so it starts 0.220 out along the slope
        normal from that origin exactly as the eave course does (surface point at
        s = 0 is local y -0.17336, z +0.13545), and nothing has to be moved to
        meet the bell-cast;
      * climbs +Y by SLOPE_SEG*cos P and +Z by SLOPE_SEG*sin P, so it tiles up
        the slope at slope_vec(1) -- but it is NOT a tiling piece: it is the
        first 5 courses of a run, and it does not hand over to the flat piece at
        its own top. WHERE THE FLAT PIECE GOES, if the wall above wants one at
        all (this junction's does not -- see below): at s = SLOPE_SEG exactly,
        i.e. slope_vec(1) from this origin, so its own 0.123077 gauge lands on
        the slope panel's. Laid directly on this piece's top instead, at
        s = 0.570560, its eighth course head falls 0.044825 short of the segment
        boundary and every course line above it is out of step with the panel;
      * mirror in X for the other hand (putr's `mx='X'` -- a mesh mirror, not a
        negative scale, because a negative scale would invert the winding).

    HOW FAR UP THE SLOPE THE LOWEST COURSE SITS, since it starts at an eave and
    not at a panel boundary: at zero. The lowest cut course's HEAD is at arc
    1*ra = 0.128680 and its butt hangs 0.45*ra = 0.0579 of arc BELOW the origin,
    which is the eave course's own first course to the millimetre -- _field
    places courses by head at k*ra for k = 1..n on both pieces. The lead runs
    further out than the shingles do (ES_DOWN, ES_SLAB) so nothing is open at the
    drip.

    WHAT IT TILES BY: nothing along the ridge -- it is a one-off at a wall, and
    nothing up the slope either, at the junction it was measured for. Above
    nrow = 5 courses the top of its cover is already at local z 0.64598 against
    the wing's roof plane at the wall face at 0.656669 -- 0.011 short, 0.018 in
    world z -- so the lead covers the whole joint even though the cut courses
    stop 0.060 m of world height below the wing's fascia bottom. What is left
    above it (courses 6 and 7, to the valley foot at 7.04 courses / local z
    0.656669) sits INSIDE the wing's eave soffit, above the wing's drip line and
    behind its 0.42 m of overhang. SM_Roof_Flash_Step_1m6 is for a wall that goes
    higher than that -- a chimney cheek, or a bigger eave step.

    Four layers, all indexed on the eave's own courses: cut courses laid by
    _field on the eave's surface at the eave's arc gauge 0.128680; one lapping
    lead soaker per course, alternately 5.5 mm prouder so two lapping sheets
    never share a plane; a continuous upstand turned up the wall FS_UP off the
    surface; and the cover cut in steps, one per course, whose tread and rise are
    the eave's own -- so near the drip the staircase flattens with the bell-cast
    instead of climbing at 52 deg through it."""
    sf = _Surf(sweep=S.SWEEP)
    # THE EAVE'S OWN GAUGE, derived by eave()'s own line rather than assumed.
    ra = (sf.arc(L) - sf.arc(0.0)) / max(1, int(round(sf.arc(L) / ROW)))
    span = nrow * ra                        # in ARC along the swept surface
    s_top = sf.s_at(span)
    # Seams tightened onto what the piece MEASURES (x -0.4001..-0.0008,
    # y -0.3034..0.3968, z 0.0790..0.6854), not onto a slack bound: nothing may
    # cross x = 0, the wall face, and the y bound is what proves this piece does
    # not deepen any eave's plan footprint (the eave itself reaches y -0.4189, so
    # the assembler's EAVE_PROJ = 0.465 still guards the drip and is unchanged).
    p = _Part(nm or "SM_Roof_Flash_StepEave_0m6", budget="roof",
              seams=dict(x=(-.42, .01), y=(-.32, .42), z=(.06, .71)))
    r = rng(p.name)
    # boarding, so the joint is never open to daylight -- and following the
    # sweep, not chording it (see ES_NSEC)
    _slab(p, sf, -.40, -.004, sf.s_at(ES_SLAB), s_top + .01, -SLAB, .002,
          n=ES_NSEC)
    # ---- soakers: one per course, lapping, alternately proud ---------------
    for k in range(nrow):
        _put(p, sf, -FS_TONG * .5 - .008, sf.s_at((k + .5) * ra), LIFT - .004
             + (k % 2) * .0055, (FS_TONG, 1.7 * ra, FS_LEADT), LEAD, bevel=0,
             tint=.04, shade=.30)
    # ---- the cut courses on the eave's own surface -------------------------
    _field(p, sf, -FS_CUT[1], -FS_CUT[0], 0.0, s_top, seed="stepeave", t0=.004)
    # ---- the upstand, turned up the wall, following the sweep --------------
    ss = [lerp(ES_DOWN, span + .05, i / (ES_NSEC - 1.0)) for i in range(ES_NSEC)]
    base = [sf.pt(sf.s_at(a), BUILD + .004) for a in ss]
    poly = base + [(y, z + FS_UP) for (y, z) in base[::-1]]
    p.prism(poly, FS_LEADT, LEAD, axis='X', at=(-.0075, 0, 0), bevel=0,
            tint=.04, shade=.34)
    # ---- the cover, cut in steps that follow the courses -------------------
    for k in range(nrow):
        yb, zb = sf.pt(sf.s_at((k + 1) * ra), BUILD + .004)
        y0 = sf.pt(sf.s_at(k * ra), BUILD + .004)[0] - .55 * ra * COSP
        p.box((FS_COVX - (k % 2) * .004, (y0 + yb) * .5,
               zb + FS_UP - FS_COVH * .5), (.014, yb - y0, FS_COVH), LEAD,
              bevel=0, tint=.04, shade=.46 + r.uniform(-.04, .04))
    p.wobble(.005, freq=1.8)
    return p.finish()


# ------------------------------- 6d. the eave's STOP END against a wall ------
# THE SECOND HALF OF THE SAME JUNCTION, AND IT IS NOT A FLASHING. Shanee, same
# render: "the range's eave fascia and its dentil course stop dead against the
# plaster: you can see the cut end of the fascia, and a dentil overhanging
# nothing."
#
# MEASURED FIRST, because "the eave already has a return and the assembler is
# cutting through it" was the answer that would have made this piece wrong. It
# does not. eave() lays its cap bead at (wx, .100, .052) centred on x = 0 --
# x = -1.000 .. +1.000 at wx = G, i.e. EXACTLY ON BOTH TILING SEAMS -- so
# finish()'s clamp_to_seams planes its bevel off and leaves a flat sawn face
# there; the fascia plank at (wx - .020, .075, .117) ends 0.016 / 0.004 inside
# the seams and keeps a 0.012 bevel, which is a chamfer, not a return. Neither
# could be otherwise: a return on a piece that tiles at GRID would stand in the
# middle of the next bay's fascia. So the return has to be its own piece.
#
# The dentil course needs no separate treatment beyond that, and this is also
# measured: _lattice returns ten teeth at wx = G, -0.902 .. +0.884, but the
# +0.884 one falls 0.084 from the rafter tail at +0.8 and eave() drops anything
# inside 0.085 -- so NINE teeth are emitted, from -0.902 to +0.685556, and the
# last tooth already stands 0.314 clear of the +X seam. Nothing overhangs the
# seam. What the render shows is simply the course STOPPING, with nothing to stop
# against. So this piece is a stop end, not a trimmed dentil: one dentil bay of
# solid block where the last tooth would have been, closing the whole band.
#
# The reference supports exactly that. r6's lean-to (crop at 3.5x, its shingle
# gauge as the scale bar) dies into the main range's wall, and its eave plate
# does not run out into the air: it stops against a VERTICAL STOP MEMBER standing
# proud of the plate, with the shingle course ends dying into the stepped
# soakers above it. Two members, one dark and proud, the pale bead running over
# the top of both to the wall -- which is what this builds.
#
# EST_L IS ONE DENTIL PITCH. The stop end is DENT_P = 0.198444 long along the
# ridge, so it replaces exactly one tooth bay: the dentil rhythm is not
# interrupted, it is terminated. It also means the assembler has ONE number to
# honour -- run the eave to one dentil pitch short of the wall face.
EST_L    = DENT_P          # 0.198444 -- one dentil bay
EST_LAP  = 0.006           # how far it laps -X over the run's cut end faces, so
                           # the two are never coplanar
# THE EAVE'S OWN TRIM SECTION, and these are eave()'s literals, not numbers of
# our own: (s, t, along-slope, out-of-roof). IF eave() MOVES ITS TRIM, MOVE
# THESE. The stop end reproduces the section it closes -- that is the whole
# requirement -- and it stands EST_PR proud of it so the two are never coplanar
# and the 0.004 x gap between them is covered.
EST_CAP  = (-0.062,  0.028, 0.100, 0.052)     # cap bead,  oak_pale
EST_FAS  = (-0.055, -0.013, 0.075, 0.117)     # fascia,    oak_dark
EST_DEN  = (-0.054, -0.079, 0.098, 0.075)     # dentil,    oak_dark
EST_PR   = 0.011           # how far the dark stop block stands proud of the
                           # fascia/dentil band it closes
EST_BEAD = 0.035           # thickness, along the ridge, of the vertical stop
                           # bead at the wall -- the member r6's lean-to plate
                           # dies into. Proud of the block again, so its own
                           # faces are 0.008-0.016 off every other face in the
                           # piece and check_zfight has nothing to pair.


def eave_stop(nm=None):
    """FASCIA / DENTIL STOP END: closes the end grain of an eave run that
    terminates against a wall. Three members, all at eave()'s own (s, t) so the
    profile is continuous through the joint:

      * a dark STOP BLOCK spanning the fascia-plus-dentil band (s -0.114..+0.006,
        t -0.1275..+0.0505 -- the union of eave()'s fascia and dentil sections
        grown EST_PR proud), one dentil bay long;
      * a dark vertical STOP BEAD at the wall, EST_BEAD thick and prouder again,
        which is the member the band actually dies into;
      * the pale CAP BEAD carried over both to the wall, at eave()'s own
        (s -0.062, t +0.028) and section (0.100 x 0.052), so the light line along
        the top of the eave runs unbroken into the stop instead of stopping one
        bay early.

    FRAME -- the eave's, and the SAME ORIGIN as SM_Roof_Flash_StepEave_0m6:
    wall face on X = 0, wall body +X, the eave run lying in -X, origin on the
    nominal 52 deg slope at the eave anchor. Built on the eave's own swept
    surface, so its members land on the eave's trim line and not on the nominal
    plane 0.22 below it. Occupies x -0.2144 .. -0.0050 measured: NOTHING crosses
    the wall face and nothing reaches +X. Mirror in X for the other hand -- it is
    symmetric about no plane, so the mirror is a real mesh mirror.

    WHAT THE ASSEMBLER MUST HONOUR: the eave run's last piece's outer X seam has
    to land EST_L = 0.198444 short of the wall face. The piece laps EST_LAP
    = 0.006 back over that seam (the pale cap bead 0.016), so a run ending
    anywhere in the last 6 mm of it still closes; further short than that and the
    gap is the run's, not the stop's. WHAT IS NOT CLOSED, measured: eave() drops
    its own +0.884 tooth (it falls 0.084 from the rafter tail at +0.8 and the rule
    drops anything inside 0.085), so at the +X hand the last tooth's edge stands
    0.2744 in from the seam and the band runs 0.2744 of bare fascia before the
    stop block picks it up; at the -X hand it is 0.058. That is eave()'s own
    lattice, not this piece's -- the fix would be its 0.085 rafter-tail threshold,
    which exists to stop a tooth landing inside a tail, so it is left alone.

    IT DOES NOT CHANGE ANY EAVE'S PLAN DEPTH. Its own y range is inside the
    eave's -0.4189..+1.0306, so EAVE_PROJ = 0.465 in the assembler still guards
    the drip and needs no new number."""
    sf = _Surf(sweep=S.SWEEP)
    # Seams tightened onto the measured extents: x -0.2144..-0.0050,
    # y -0.3460..-0.1867, z  0.0017..0.1920. The y bound is the one that matters
    # to the assembler -- it sits WELL INSIDE the eave's own -0.4189, so no eave's
    # plan depth changes and EAVE_PROJ = 0.465 needs no new number.
    p = _Part(nm or "SM_Roof_Eave_StopEnd", budget="roof",
              seams=dict(x=(-.23, .01), y=(-.36, -.15), z=(-.03, .21)))
    r = rng(p.name)
    x1 = -(EST_L + EST_LAP)                       # the lap end, over the run
    # ... and the pale bead laps 0.010 DEEPER than the dark block does. Not
    # cosmetic: at one shared x1 the block's and the bead's -X faces were the same
    # plane and check_zfight scored 26 cm2 of it. Lapping the pale line further
    # back also closes the 0.004 x gap between this piece and the run's own cap
    # bead, which ends exactly on its outer seam.
    # ---- the dark stop block: the fascia + dentil band, grown proud --------
    fs0, fs1 = EST_FAS[0] - EST_FAS[2] * .5, EST_FAS[0] + EST_FAS[2] * .5
    ds0, ds1 = EST_DEN[0] - EST_DEN[2] * .5, EST_DEN[0] + EST_DEN[2] * .5
    b_s0, b_s1 = min(fs0, ds0) - EST_PR, max(fs1, ds1) + EST_PR
    b_t0 = EST_DEN[1] - EST_DEN[3] * .5 - EST_PR
    b_t1 = EST_FAS[1] + EST_FAS[3] * .5 + .005    # only 5 mm at the top: the
    # flashing's upstand base sits at BUILD + 0.004 = 0.0672 and the pale bead
    # runs over this face anyway, so there is nothing to gain up there and
    # 0.0167 of clearance to keep.
    _put(p, sf, (x1 - .012) * .5, (b_s0 + b_s1) * .5, (b_t0 + b_t1) * .5,
         (-.012 - x1, b_s1 - b_s0, b_t1 - b_t0), "oak_dark",
         bevel=.012, seg=1, tint=.05, shade=.80 + r.uniform(-.04, .04))
    # ---- the vertical stop bead at the wall --------------------------------
    # 0.016 proud of the block DOWN-SLOPE, where it is seen, and 0.004 INSIDE it
    # top and bottom, so the block still sets the silhouette and every face of
    # the bead is >= 4 mm off every face of the block -- 8x ZFIGHT_TOL.
    _put(p, sf, -.005 - EST_BEAD * .5, (b_s0 + b_s1) * .5 - .008,
         (b_t0 + b_t1) * .5,
         (EST_BEAD, b_s1 - b_s0 + .032, b_t1 - b_t0 - .008), "oak_dark",
         bevel=.010, seg=1, tint=.06, shade=.92 + r.uniform(-.04, .04))
    # ---- the pale cap bead, carried over both to the wall ------------------
    xp = x1 - .010
    _put(p, sf, (xp - .008) * .5, EST_CAP[0], EST_CAP[1] - .002,
         (-.008 - xp, EST_CAP[2] + .020, EST_CAP[3] + .014), "oak_pale",
         bevel=.014, seg=2, tint=.05, shade=1.06)
    p.wobble(.006, freq=1.4)
    return p.finish()

# ------------------------------------------------------------------ build ----
def build():
    """The family. THE FRACTIONAL PIECES ARE NOT SCALED COPIES -- read the
    HALF AND QUARTER TILES block at the top for the arithmetic, and slope()'s
    docstring for why the up-slope fractions are course counts rather than 0.5
    and 0.25. In one line each:

      SlopeHalf / SlopeQtr  7 and 3 of the field's own courses up the slope,
                            spans 0.861538 / 0.369231 m, gauge 0.123077 both,
                            and 7 + 3 + 3 = one whole panel.
      Slope_1m              half a bay along the ridge: exactly 7 tabs of
                            TAB = G/14, so the tab width is the field's too.
      Eave_1m / _0m5        dentils still at 0.198444, tails still at 0.400,
                            starters still at 0.151667, sweep untouched.
      Ridge_1m / _0m5       cresting still at 0.500 -- exact on every width.
      Valley_1m0 / _0m4     7 and 3 cut courses, arris 1.011726 / 0.433597 m.
      ValleyLaced_1m0/_0m4  the full piece's own courses 1..7 and 1..3.
      Flash_Step_1m6        NOT a fraction -- the SIDE-ABUTMENT condition the
                            family did not have. Flash_Wall is an apron and can
                            only close a joint that runs ACROSS the fall.
      Flash_StepEave_0m6    the same abutment AT THE EAVE: 5 courses on the
                            eave's own swept surface at the eave's own arc gauge
                            0.128680, arc 0.643399. Not the flat piece shortened
                            -- the bell-cast would bury it. See 6c.
      Eave_StopEnd          closes the end grain of an eave run that dies into a
                            wall, one dentil pitch (0.198444) long, at eave()'s
                            own fascia / dentil / cap-bead section. See 6d."""
    out = [slope("A"), slope("B"), slope("C"), slope("Warm")]
    for v in ("A", "B", "C"):
        out.append(slope(v, nrow=SLOPE_HALF_N, nm=f"SM_Roof_SlopeHalf_2m_{v}"))
    for v in ("A", "B", "C"):
        out.append(slope(v, nrow=SLOPE_QTR_N, nm=f"SM_Roof_SlopeQtr_2m_{v}"))
    for v in ("A", "B", "C"):
        out.append(slope(v, wx=G / 2.0, nm=f"SM_Roof_Slope_1m_{v}"))
    out += [eave(),
            eave(G / 2.0, "SM_Roof_Eave_1m"),
            eave(G / 4.0, "SM_Roof_Eave_0m5"),
            ridge(),
            ridge(G / 2.0, "SM_Roof_Ridge_1m"),
            ridge(G / 4.0, "SM_Roof_Ridge_0m5"),
            verge(), hip(),
            valley(),
            valley(VAL_HALF_N, "SM_Roof_Valley_1m0"),
            valley(VAL_QTR_N, "SM_Roof_Valley_0m4"),
            valley_eave(),
            valley_laced(),
            valley_laced(VAL_HALF_N, "SM_Roof_ValleyLaced_1m0"),
            valley_laced(VAL_QTR_N, "SM_Roof_ValleyLaced_0m4"),
            valley_laced_eave(), flashing(), flash_step(),
            flash_step_eave(), eave_stop()]
    return out


# ==================================================================== demo ===
NS = 3                            # slope segments per main-roof side
RUN = NS * L * COSP               # 2.9556 horizontal, eave line to ridge
RISE = NS * L * SINP              # 3.7828
STEP = Vector((0.0, L * COSP, L * SINP))


def _ctx_walls(x0, x1, y0, y1, ztop, name="CTX_Walls"):
    """Demo-only: the storey under the eaves, framed on the two camera-facing
    faces. NOT a kit piece; build() never returns it."""
    p = _Part(name)
    r = rng(name)
    HW, HS = 2.60, 2.90                        # timber storey, stone storey
    zb = ztop - HW
    p.plate(((x0 + x1) / 2, (y0 + y1) / 2, zb + HW / 2),
            (x1 - x0, y1 - y0, HW), "plaster_dim", tint=.03, shade=.70)
    p.plate(((x0 + x1) / 2, (y0 + y1) / 2, zb - HS / 2),
            (x1 - x0 - .06, y1 - y0 - .06, HS), "stone_dark", tint=.03, shade=.62)
    for (u0, u1, ax) in ((x0, x1, 'X'), (y0, y1, 'Y')):
        n = max(2, int(round((u1 - u0) / .64)))
        for i in range(n + 1):
            cu = lerp(u0, u1, i / n)
            sh = .93 + r.uniform(-.05, .05)
            if ax == 'X':
                p.box((cu, y0 + .03, zb + HW / 2), (.14, .12, HW - .40),
                      "oak_dark", bevel=.012, seg=1, tint=.05, shade=sh)
            else:
                p.box((x1 - .03, cu, zb + HW / 2), (.12, .14, HW - .40),
                      "oak_dark", bevel=.012, seg=1, tint=.05, shade=sh)
    for z, h in ((ztop - .12, .24), (zb + .13, .26)):
        p.box(((x0 + x1) / 2, y0 + .01, z), (x1 - x0 + .12, .19, h), "oak_dark",
              bevel=.014, seg=1, tint=.05, shade=.88)
        p.box((x1 - .01, (y0 + y1) / 2, z), (.19, y1 - y0 + .12, h), "oak_dark",
              bevel=.014, seg=1, tint=.05, shade=.88)
    p.stones((x0, x1), (zb - HS + .12, zb - .10), y=y0 - .03, depth=.11,
             mat="stone", mat_alt="stone_pale", mat_warm="stone_warm",
             course=.37, seed=4, wobble=.26, big=.22)
    p.stones((y0, y1), (zb - HS + .12, zb - .10), y=x1 + .03, depth=.11,
             mat="stone", mat_alt="stone_pale", mat_warm="stone_warm",
             course=.37, seed=5, wobble=.26, big=.22, axis='X')
    return p.finish()


def _ctx_stack(cx, cy, zb, ztop, name="CTX_Stack"):
    """Demo-only chimney, for the flashing to work against."""
    p = _Part(name)
    p.box((cx, cy, (zb + ztop) / 2), (.86, .78, ztop - zb), "stone_pale",
          bevel=.02, seg=1, tint=.05, shade=.98, taper=.94, taper_axis='XY')
    p.stones((cx - .40, cx + .40), (ztop - 2.5, ztop - .28), y=cy - .38,
             depth=.09, mat="stone_pale", mat_alt="stone", mat_warm="stone_warm",
             course=.33, seed=7, wobble=.22, big=.14)
    p.box((cx, cy, ztop + .08), (1.06, .96, .18), "stone_pale", bevel=.02,
          seg=1, tint=.05, shade=1.06)
    p.cyl((cx, cy, ztop + .44), .17, .56, "terracotta", sides=9, bevel=.014,
          seg=1, tint=.06, r_top=.15)
    return p.finish()


def _shot(run, name, yaw=45, pitch=93, lens=80, margin=1.30):
    """An EXTRA render, taken by the module itself and written next to
    demo.png. build_piece.py frames demo() at pitch 64, i.e. looking DOWN on
    the roof from a long way off, and the two things a valley has to be judged
    on are both invisible from there: what happens at the DRIP EDGE, and
    whether the courses actually sweep round the angle. So the module takes its
    own closer looks at the near run. It renders the same scene demo() just
    built; it only moves the camera."""
    if not run:
        return
    try:
        from kit import render as R
    except Exception:
        return
    import os
    root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    try:
        R.clear_stage()
        R.look_ref2()
        R.camera(run, yaw=yaw, pitch=pitch, lens=lens, margin=margin)
        R.save(os.path.join(root, "renders", "roofs", name))
    finally:
        R.clear_stage()


def demo():
    """A shot, not a lineup: a six-bay main roof with a gable at each end, its
    swept eaves and cresting ridge, a gabled cross wing on the front right that
    brings a matched pair of VALLEYS into the same picture, and a chimney
    through the front slope with its apron flashing.

    Every number below is derived, not eyeballed. The main roof is NS = 3 slope
    segments a side, the wing is NW = 2 and its eaves sit ON the main eave line,
    so each valley is exactly 2 x HIP_SEG long and its head lands exactly one
    slope segment below the main ridge. See the note at the wing for why the hip
    piece is not in this shot."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []
    ZUP = 5.6

    def put(nm, at, rot=(0, 0, 0), mirror=False):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = (at[0], at[1], at[2] + ZUP)
        o.rotation_euler = [radians(a) for a in rot]
        if mirror:
            o.scale.x = -1
        out.append(o)
        return o

    VARS = ("A", "B", "C", "B", "A", "C", "B", "A", "C", "A")

    # ------------------------------------------------- main block, 6 bays --
    XL, XR = -6.0, 6.0
    for j, x in enumerate((-5.0, -3.0, -1.0, 1.0, 3.0, 5.0)):
        for (y0, rz, sg) in ((-RUN, 0, -1), (RUN, 180, 1)):
            put("SM_Roof_Eave_2m", (x, y0, 0), (0, 0, rz))
            for k in (1, 2):
                put(f"SM_Roof_Slope_2m_{VARS[(j * 2 + k + (0 if sg < 0 else 5)) % 10]}",
                    (x, y0 - sg * k * STEP.y, k * STEP.z), (0, 0, rz))
        put("SM_Roof_Ridge_2m", (x, 0, RISE))
    for k in range(NS):                        # gable rakes, both ends
        sy, sz = -RUN + k * STEP.y, k * STEP.z
        put("SM_Roof_Verge_2m", (XL, sy, sz), mirror=True)
        put("SM_Roof_Verge_2m", (XR, sy, sz))
        put("SM_Roof_Verge_2m", (XL, -sy, sz), (0, 0, 180))
        put("SM_Roof_Verge_2m", (XR, -sy, sz), (0, 0, 180), mirror=True)

    # ------------------------------------------ cross wing, front right ----
    # The wing's EAVES SIT ON THE MAIN EAVE LINE (WZ = 0). That one number is
    # what makes the joint exact instead of approximate: each valley then starts
    # at a main eave corner, runs at exactly 45 deg in plan because both roofs
    # are at PITCH, is a whole number of HIP_SEG long, and dies into the main
    # slope exactly one slope segment below the main ridge. The old wing floated
    # a metre above the main eave with no wall under it, so the render showed its
    # underside and two eave overhangs hanging in mid air.
    #
    # WHY THIS WING IS GABLE-ENDED AND NOT HIPPED. At a VALLEY the roof surface
    # is the HIGHER of the two planes, so a panel that runs past the valley line
    # is buried under the roof it meets and overlap costs nothing -- which is why
    # both valleys here are laid with plain full panels and read clean. At a HIP
    # it is the LOWER plane that wins, so a panel that runs past the hip line
    # stands PROUD of the roof next to it. A 2 m panel on a 45 deg hip overhangs
    # by up to one whole slope segment, and no cap 0.25 m wide can hide that: a
    # hipped end wants panels cut on the diagonal, which is a level-artist edit
    # (or assemble_inn.py's part-bay scaling), not something a demo can snap
    # together. The hip piece is in the lineup; putting it here would only
    # demonstrate the flaps it used to produce.
    NW = 2
    lead_run, lace_run = [], []      # the far valley and the near one
    WRUN, WRISE = NW * L * COSP, NW * L * SINP      # 1.9707, 2.5215
    WX = 4.0                                        # wing ridge, on a bay line
    xw0, xw1 = WX - WRUN, WX + WRUN                 # 2.029, 5.971
    WEND = -RUN - WRUN                              # -4.926 gable end
    WBACK = WRISE / TANP - RUN                      # -0.985 ridge into the slope
    WMID = (WEND + -RUN) / 2                        # -3.941 eave-panel centre

    # Side slopes: two panels a course at exact GRID spacing, the eave piece on
    # the eave line and the rest plain field. They overrun the valley by up to a
    # metre and the gable rake by 15 mm, both of which are covered.
    for (xe, rz, sg) in ((xw0, -90, 1), (xw1, 90, -1)):
        put("SM_Roof_Eave_2m", (xe, WMID, 0.0), (0, 0, rz))
        put("SM_Roof_Slope_2m_B", (xe, WMID + G, 0.0), (0, 0, rz))
        for j in (0, 1):
            put("SM_Roof_Slope_2m_" + ("C", "A")[j],
                (xe + sg * STEP.y, WMID + j * G, STEP.z), (0, 0, rz))

    # The wing's gable rakes, and its ridge from the gable back into the slope.
    for k in range(NW):
        put("SM_Roof_Verge_2m", (xw0 + STEP.y * k, WEND, STEP.z * k), (0, 0, -90))
        put("SM_Roof_Verge_2m", (xw1 - STEP.y * k, WEND, STEP.z * k), (0, 0, 90),
            mirror=True)
        # THE RUN, AND ITS FOOT. k = 0 is the lowest length of each run and it
        # is the FOOT piece, not an ordinary one: it sits at exactly the same
        # place an ordinary length would (the run's p0, here the corner where
        # the wing's eave line meets the main eave line), with the same
        # mirroring, and the k = 1 length laps it with the ordinary welt.
        #
        # THE TWO VALLEYS IN THIS SHOT ARE DELIBERATELY DIFFERENT PIECES: the
        # FAR one is the lead-lined open valley, the NEAR one the laced (swept)
        # shingle valley, laid at exactly the same places with exactly the same
        # rule. One picture therefore carries both, against the same field, in
        # the same light -- which is the only fair way to judge whether the
        # courses really do sweep round the angle.
        nm = "SM_Roof_Valley_Eave_1m9" if k == 0 else "SM_Roof_Valley_1m9"
        lead_run.append(put(nm, (xw0 + STEP.y * k, -RUN + STEP.y * k,
                                 STEP.z * k)))
        nm = ("SM_Roof_ValleyLaced_Eave_1m9" if k == 0
              else "SM_Roof_ValleyLaced_1m9")
        lace_run.append(put(nm, (xw1 - STEP.y * k, -RUN + STEP.y * k,
                                 STEP.z * k), mirror=True))
    for j in (0, 1):
        put("SM_Roof_Ridge_2m", (WX, WEND + 1.0 + j * G, WRISE), (0, 0, 90))

    # ------------------------------------------- chimney + apron flashing --
    CX, CY, CW = -2.60, -1.34, 0.39
    put("SM_Roof_Flash_Wall_2m", (CX, CY - CW, (CY - CW + RUN) * TANP))

    out.append(_ctx_walls(XL + .30, XR - .30, -RUN + .55, RUN - .55, ZUP - .06))
    out.append(_ctx_walls(xw0 + .55, xw1 - .55, WEND + .55, -RUN + 1.0,
                          ZUP - .06, name="CTX_Wing"))
    out.append(_ctx_stack(CX, CY, ZUP - 2.2, ZUP + (CY + RUN) * TANP + 1.75))
    for nm in src:
        src[nm].location = (0, 80, 0)
    # the sweep of the courses, and then the boot at the drip edge
    _shot(lace_run, "demo_lace.png", yaw=44, pitch=74, lens=95, margin=1.34)
    _shot(lace_run, "demo_foot.png", yaw=45, pitch=93, lens=80, margin=1.30)
    return out
