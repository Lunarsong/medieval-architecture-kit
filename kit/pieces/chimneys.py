"""Chimneys. Both references break their rooflines with the same thing: a tall,
narrow, pale stone stack wearing a little hat.

Read off the reference crops (ref2:chimney, ref1:chimney):
  * The shaft is NARROW and TALL -- about 0.95m square, and 2.5-3x that high
    above the shoulder. The silhouette is a near-clean rectangle: the masonry
    reads through course lines and value, not through big lumps.
  * The stones are near-EQUANT (w/h about 1.0-1.5), 4-5 across a face -- FINER
    than the wall the stack rises from, never coarser: a chimney is a narrow
    element and the same stone reads bigger on it (see R6) -- packed tight enough
    that the joints read as thin dark creases. The value range in a
    stack is wide but it is not stone-by-stone: it runs in patches, and the
    near-black is the JOINTS, not every fifth stone.

THE SHAFT IS COURSED RUBBLE OF ROUNDED STONES, AND BOTH HALVES OF THAT MATTER.
The family has spent five rounds losing one of them to win the other, so read the
history before changing _cobble:
  R1  p.blob cushions. Right SHAPE, but a hexagon inscribed in a rectangle only
      reaches .866 of its half-width, so closing the perpends meant laying every
      stone ~15% oversize -- and that oversize was the stones sinking into each
      other Shanee reported first.
  R2  squared and shrank the end stone of every course, which on a 0.96 m face
      carrying two stones a course is all of them: the shaft came out as
      wallpaper, the same even grid on all four faces.
  R3  plain p.box(bevel=0) in cells. Cannot interpenetrate, and cannot be a
      stone: a box with no bevel is ONE flat plate with a 90 deg arris round it,
      and 168 of them in a grid is Lego. The lead, on the render: "flat-faced
      rectangular blocks ... no face relief, hard square edges, uniform widths,
      and there is no mortar recess."
  R4  the _cobble cushion, but with the chamfer measured against the stone's
      RELIEF instead of the depth it actually has to climb (BACK + relief). At
      .85 the flank came out at 53 deg off the face against a 34 deg smoothing
      angle, so every stone still CREASED at its rim and still read as a plate --
      and the corner cuts were on the face ring, which rounds the crown and
      leaves the SILHOUETTE a rectangle. Shanee: "too regular/patterned on each
      face."
  R5  _cobble's base ring IS the stone's cell, with corners pulled in and one to
      three of them cut off, and the chamfer to the face ring set at
      1/tan(34 deg) of the depth it climbs. No interpenetration, and the rim
      shaded round. Tone went hard `stone`-led with a FEW real outliers rather
      than four materials at even odds, and the mortar became a lit surface on
      `stone` instead of a black slot on stone_dark.
  R6  what is here, and it fixes the two things R5 could still be MEASURED to be
      getting wrong.
      THE FACE. In the colour-free solid render the stones were still flat plates
      with one folded lip: measured, the median dome rose 8% of the stone's width
      and at a 20 deg tolerance 30% of stones had 85% of the face inside ONE
      plane. Chamfer arithmetic cannot reach that, because the chamfer was never
      the problem -- a 4-corner outline gives a 4-facet cap around an off-centre
      apex, i.e. two big triangles with a fold line between them, which is sheet
      metal however deep you make it. So the face is now what util.Part.blob
      draws, and blob was the primitive to read all along: an 8-sided jittered
      outline inscribed in the cell, a ring at MIDR of it carrying most of the
      climb, an off-centre crown -- a cushion that bulges in TWO STEPS. Measured
      on the same 800 stones: the dome rises 22% of the stone's width (19% of it
      inside 30 deg of the face normal, against R5's 5%), and not one stone in
      the family holds 85% of its face in one plane. Long stones no longer end in
      razor wedges either: the ring is a SCALE of the outline, so its band is 22%
      of every half-extent instead of a fixed 46 mm, and ASPECT caps a stone at
      2:1 so there is nothing left that a dome cannot sit on.
      THE SIZE. The lead, with this family's closeup beside stone_walls': "the
      chimney's stones read visibly LARGER than the wall's ... it is a narrower
      element, so the same stone size looks bigger on it." R5 matched
      stone_walls' .265 course exactly, on the argument that one course height
      means one quarry -- and that argument is wrong, because a course reads
      against the WIDTH OF THE THING IT IS ON. Three stones across a 0.96 m shaft
      is coarser masonry than six across a 2 m wall whatever the tape says. The
      shafts run .222 now and the median stone is 0.25 x 0.20 against the wall's
      0.36 x 0.27: four to five a course, and finer in absolute size than the
      wall it rises from, which is the way round it has to be.
      PAID FOR IN TRIANGLES by three things, because 4 faces of 2.6 m inside a
      3000-tri cap does not give a smaller, rounder stone for nothing: no stone
      carries a back (every one is bedded 10 mm inside an opaque mortar body, so
      those n-2 triangles were buried in lime), the packers and the halves of
      split cells are cones rather than two-step cushions (BIG_A), and the
      dressed variant runs 7 sides where the rubble runs 8.
  R9  the joints. Shanee, on the assembled .blend: the stones "have a lot of gap
      in-between at times which might not make much sense". Measured at the
      shaft's own joint plane, the drawn joint ran 19% of a stone width where
      ref1's cobbles pack at nearer 10, and the arithmetic says where it went:
      what the eye reads as the edge of a stone is not its outline -- that is
      bedded BACK inside the mortar -- but the section where its shoulder crosses
      the mortar surface, and three separate things were eating that section.
      (a) THE SHOULDER'S OWN TAPER (SUPERSEDED -- see R11 (a) below), ~10% of a
          half-extent by the time it gets
          there, and 21% on a cone. Paid for by GROW: the cell rule then applied
          to the stone's CORE -- every section from the mortar surface outward,
          i.e. every section anybody can see -- and the buried skirt below it may
          oversail its cell by up to 11 mm, which is where two neighbours now
          share volume and where nothing can see them do it. The ceiling is set
          by CORNER_J, not chosen. Verified by slicing every stone at the joint
          plane and 4, 10 and 20 mm in front of it: zero overlapping sections.
      (b) `eps`, the shrink that paid for the in-plane roll: 4.5 mm a side, i.e.
          9 mm of every joint, to protect four corners from a clamp that is what
          enforces the cell rule anyway. Now 1.2 mm.
      (c) the outline giving area back at its corners -- `e` .40-.58 -> .24-.38,
          the radius jitter .30 -> .20, and the hard-pulled vertex .68 -> .82,
          which also kills the dark triangular chip it used to cut.
      Measured after: 15.5% on stack A against 19.1 before, coverage .58 -> .78.
      THE MORTAR IS ONE BODY PER MODULE AGAIN (see _mortar), because banding it
      alternated the joint plane by 6 mm and half a stack's rims ended up 0.4 mm
      from showing; and the breast's mortar beds now sit MORT_IN behind the face
      of the step they back, per step, for the same reason.
  R11 (a) IT BOUGHT THAT GAIN WITH INTERPENETRATION, and that is not a trade this
      family gets to make -- it is the very defect it has spent five rounds
      avoiding. Measured on every stone's footprint: 1548 pairs sharing volume,
      395 of them on SM_Chimney_Stack_2_6m_A, 28 mm deep, which is exactly two
      neighbours each oversailing GROW + 6 mm across a 6 mm joint. GROW is gone
      and the cell rule is absolute again. The joint is closed the way
      stone_walls closes it instead, from the two directions that cost nothing:
      the BURIAL, 10 mm -> 6, which is what sets a flank's taper where it crosses
      the mortar surface and so IS the joint; and CIRCUMSCRIPTION (INFL), which
      scales the outline ring past its own chords so the clamp cuts flats at the
      four axes instead of every chord cutting a sagitta out of the pack. The
      outline is ROUNDER for it, not squarer (`ee` .24-.38 -> .40-.56), because
      it is no longer the corner that has to pay. Measured after: zero
      overlapping pairs anywhere in the family, and the drawn joint on stack A
      down from 15.0% to 9.1% of a stone width (raycast gauge, 1.5 mm grid,
      median run against median run), with zero back-facing hits.
  R11 (b) AND THE STONES ARE FINER. "Chimney stones are still coarser than the
      wall's on a 0.96 m face; a chimney should read the same or finer." The
      shafts ran .222 courses and a median cell of 257 x 187 against the wall's
      cobble at 222 x 226 -- the same stone on half the width of wall, which
      reads coarser however the tape falls. The shafts run .188-.222 now and the
      median cell is 237 x 172, drawing 182 x 168 against the wall's cobble at
      216 x 218 and its rubble at 312 x 215: finer than either, which is the way
      round it has to be on a 0.96 m face. The triangles come out of the joint,
      not out of `sides` -- 8 is the floor for a cone cap, because at 7 the
      facets round an off-centre apex differ by more than spec.SMOOTH_ANG and the
      stone creases into a paper dart (built it, looked at it, put it back).
  R12 THE OUTLINE WAS THE CELL RECTANGLE, and everything wrong with the round-11
      render followed from that one fact. `infl` scaled the superellipse ring
      1.20 past its own chords and the per-vertex clamp then flattened it into
      the cell: at sides = 8 and ee .42-.58 EVERY vertex lands outside the cell,
      most of them on its own corners, and _dedupe collapses the ring to four or
      five points. Measured on the render: 86-90% coverage with NO CONTINUOUS
      JOINT ANYWHERE -- just a dark triangular chip where two corners failed to
      meet -- and a cap of four facets over a 4-gon, which is the folded paper
      dart R6 thought it had killed. The raycast gauge reported 6-10%, which is
      the joint being NEARLY CLOSED and is exactly why a number is not a look.
        The fix is stone_walls' round-12 construction at this family's scale, and
      it is the same file to read for both: the outline is the CELL WITH ITS
      CORNERS TAKEN ROUND -- flats first, then a quarter ellipse of radii
      (f*bu, f*bv) at each corner (FILL / ARC / ARC_P / CHAMF). So the perpend is
      a continuous recess of the width the course laid out, the give-back is
      exactly .2146 f^2 of the cell whatever the aspect, and the cap is a cone of
      10-12 facets instead of four.
        THE BURIAL IS REVERSED WITH IT. BACK was 3 mm behind a mortar surface
      2 mm in, i.e. the widest section of every stone was buried 1 mm and the
      flank had already tapered by ~2 mm a side before anybody could see it. At
      BACK = 1.2 mm the outline stands 0.8 mm PROUD of the mortar, so what the
      eye reads as the edge of a stone is its cell -- stone_walls' SKIRT_Y rule,
      reached from the other side. Verified by raycast: zero back-facing hits on
      every stack, so no rim is open.
        PAID FOR IN TRIANGLES, because a cone costs one triangle per outline
      vertex and a 2.6 m shaft carries ~250 stones inside a 3000-tri cap: ARC_P
      (.62) leaves two corners of the median stone as single chords, and BIG_A
      went .062 -> .105 so only the genuinely big stones keep a shoulder ring.
      Stack A lands at 2804 tris.
      Measured after, on a 1.5 mm raycast grid, median run against median run,
      with the mortar body TAGGED BY MATERIAL rather than found by a depth
      threshold -- so the geometry measured is exactly the geometry that ships,
      p.wobble and all, and "joint" means "you can see lime here" (see the same
      note in stone_walls: a threshold reads half again too high because it
      counts the outer millimetres of every shoulder as joint):
          stack 1.6 A  8.3% across / 11.7% up  cover 85.3%  stone 144 x 180 mm
          stack 2.6 A  9.5 / 8.5   cover 85.4  stone 174 x 159
          stack 2.6 B  4.3 / 6.5   cover 91.4  stone 244 x 184  (dressed variant,
                       deliberately the finest joint in the family)
          stack 2.6 C  7.8 / 10.4  cover 87.1  stone 212 x 173
      against stone_walls' cobble at 201 x 202 mm and its rubble at 250 x 204 on
      a 2 m face, so the stack reads FINER than the wall it rises from on a
      0.96 m one. Stone-vs-stone volume overlap, by a BVH per stone over every
      pair in every piece: ZERO. check_zfight: 0 cm2. Zero back-facing hits.
  R13 IT WAS STILL A CARVED PATTERN, and every round from 4 to 12 had been
      working on the STONE while the three things that actually made it read as
      pattern were the FACING: how proud each stone stands, what the corner does,
      and whether the bed lines are ruled. Shanee, twice: "too regular/patterned
      on each face." The lead, with the closeup beside a stone_walls bay:
      (1) NO RELIEF. "Every stone sits in ONE plane with a narrow dark groove
      between. Nothing stands proud, nothing recedes." True, and it was
      ARITHMETIC rather than dice. _crown read
      `min(max(back + relief, RISE_LO*g), RISE_HI*min(w,h), back + CROWN_MAX)`,
      and at (.26, .37) the size floor and the size ceiling sat 11 mm apart on
      the median stone while the whole per-stone bedding draw -- three factors
      multiplied together, a 24 mm span -- fell BELOW the floor for most of its
      range. What the draw actually moved the crown by:
          stone 140 x 160  11.1 mm     stone 240 x 190  0.0 mm
          stone 174 x 159   6.8 mm     stone 300 x 210  0.0 mm
      Every stone over ~230 mm came out at exactly RISE_LO*sqrt(w*h). Relief was
      therefore a pure function of stone SIZE -- two neighbours of the same size
      had bit-identical projection -- and a facing whose only depth cue is 1:1
      with area IS a pattern carved into one plane. No re-seeding could have
      moved it; that is why five rounds of re-seeding did not.
        Fixed by making the band wide (.11, .46) and CLAMPING THE DRAW INTO IT
      rather than under it, and by giving the draw real tails (SET_BACK_P /
      PROUD_P: one stone in six laid flat, one in six standing out hard, all of
      it riding the _bedding swell so boldness runs in patches). Measured per
      stone off the built mesh, on the -Y face of every stack:
          crown p05-p95 spread  27 -> 47-56 mm      sd 9.6 -> 13-16 mm
          median crown          43 -> 40 mm (deliberately unchanged: it is the
                                SPREAD that was missing, not the depth)
      A stone standing 9 mm proud beside one standing 62 sits 53 mm back, which
      is the "let a few sit noticeably back" the note asks for.
        AND THE OUTLINES SANK TOO -- but only just, and the first cut of this
      round measured why. Sinking a stone's whole shell moves the section the eye
      reads as its edge back with it, which is the honest way to bed a stone
      deep; it also narrows every visible section by
      (sink + BACK - MORT_IN)/(.52*(BACK+crown)) x 30% of a half-extent A SIDE.
      At SINK_MAX = .018 capped on the crown, coverage fell 85% -> 57-71% and the
      drawn joint went to 25-53% of a stone: pebbles scattered in lime, the exact
      failure rounds 9-12 closed. Isolated by rebuilding with the sink forced to
      zero (coverage came straight back with the wander still in, so the wander
      was innocent). SINK_MAX is .0025 now, capped on the stone's own TAPER.
      (2) THE CORNER WAS A HARD ARRIS. "Each face's coursing independent ... it
      tells the eye the faces are wallpaper on a box." The toothing existed in
      the topology since round 6 -- one face owns each corner on each course and
      returns past it -- and it was DRAWN FLUSH: the return was cut to
      `crown + 6 mm`, i.e. exactly enough to close the corner joint and land
      level with the perpendicular face's own crowns, which is a clean vertical
      edge by construction. Now the face that turns the corner is dealt a LONG
      end stone (LONG, 1.3-1.7 courses) and the face that stops at it a SHORT one
      (SHORT, .52-.84), ownership alternating course by course; the return is
      drawn rather than derived; and CORNER_J is jittered per course so the
      corner joint is not a second ruled line beside the first. Zero triangles.
      The first cut let a 300 mm through-stone run 86 mm past the arris and it
      came out as a flat flap hanging off the corner -- past the arris a cobble
      is a shell with nothing behind it -- so the return is capped on TURN_MAX,
      on .30 of the stone's own width, and on ASPECT, which is the same 2:1 rule
      _widths lays the course by.
      (3) THE COURSES WERE BANDED. "The bed joints run dead straight and level
      all the way round at a constant course height." _rows jittered the course
      HEIGHTS +-26% and `bed` gave each stone a slice back to the joint -- but at
      .011 of a cell that slice is 1.3 mm, and a jittered ladder of straight lines
      is still a ladder. A bed line is now a piecewise-constant WANDER in the
      PERIMETER coordinate (see _wander), drawn once per module and read by all
      four faces, so the courses step up and down round the stack AND still close
      exactly at every arris. Each stone takes the max of its bed line over its
      own span and the min of its head line, which makes overlap impossible by
      the same kind of arithmetic as the cell rule and hands everything it costs
      to the joint -- so a bed line steps at a perpend and DIES OUT where a stone
      straddles a step. Measured by raycasting the face on a 1.5 mm grid and
      counting scanlines that are almost entirely joint, which is exactly what a
      ruled bed line is:
          height that is a dead level bed line (>95% of the scanline is joint)
              2.3-2.8%  ->  1.3-2.3%
      The first cut of this drew (3, 7) steps round the 3.84 m circuit, i.e.
      0.7-1.75 per 0.96 m face, and barely moved the number: it is the DENSITY
      that breaks the line, not the amplitude. (7, 13).
      (4) AND THE CAPS WERE SLABS. "A chimney wants a projecting drip course near
      the top, not a plain slab." Every oversailing course in the family was one
      `_course_ring` -- a square box with a flat top and a flat nose, which is a
      slab whatever it projects. `_drip` replaces them with a moulding: a lower
      step, a dark reveal under the nose of an upper step, and a WEATHERED top.
      Both caps, both stack string courses, the haunch cornice and the breast
      capstone. On a stack the ceiling is the declared envelope (ENV - W/2 =
      100 mm less p.wobble) so the step is 10 mm and the weathering does the work;
      on the caps there is 240 mm and the step is 50.
      MEASURED AFTER, as it ships (same gauges as round 12, mortar tagged by
      material, 1.5 mm raycast grid, median run against median run):
          stack 1.6 A  joint 13.6% across / 27 mm up   cover 79.9%
          stack 2.6 A  12.5 / 31.5                     cover 79.5
          stack 2.6 B   8.7 / 18.0                     cover 86.0
          stack 2.6 C  12.2 / 27.0                     cover 83.2
      The BED joints are wider than round 12's 8.5-11.7 mm and that is the wander
      being paid for -- it is what "a bed joint dies out" costs, and it is the
      note being answered rather than a regression. The perpends are where they
      were. Cell-rule test over all 878 stones in the family: ZERO overlapping
      cells. BVH surface overlap over every cobble pair on every piece: ZERO.
      check_zfight: 0 cm2. Tri budget: 1831 / 2837 / 2568 / 2734 of 3000.
Whatever the next round changes, the invariants are: no vertex of a stone ever
leaves its cell (that is what makes overlap impossible by arithmetic rather than
by tuning -- 800 stones, zero bounding-box overlaps, let alone surface ones); the
climb from outline to crown stays inside RISE_LO..RISE_HI of the stone's own size
(that is what stops a packer being a spike and a boulder being a plate); and the
band-to-cap step stays inside spec.SMOOTH_ANG (that is what makes the two shade
as ONE CURVE instead of creasing into a lip). Break any of them and the family
goes back to choosing between Lego and interpenetration.
And since round 13 there is a fourth: a bed line's wander is read as MAX over a
stone's span for its bed and MIN for its head, which is what makes a wandering
course incapable of driving two stones into each other -- the same shape of
argument as the cell rule, and the reason the wander could be turned up without
re-opening the interpenetration this family spent five rounds closing.
  The rest of the irregularity comes from the things a mason varies -- course
heights, stone widths, split courses, through-stones, quoins, how proud each
stone beds, which face turns the corner and how long its return is, and where a
bed line steps -- and one course scale runs through the stacks, the haunch and
the breast alike: one quarry, one mason.
  * ref2's cap is the signature: a DARK low-pyramid slab roof overhanging the
    shaft by ~0.2m all round, floating on four short iron legs so you see
    daylight (and smoke) through the gap under it.
  * ref1's cap is the other classic: two corbelled courses that oversail the
    shaft, with squat terracotta pots bedded in dark flaunching on top.
  * Where a stack pierces the roof it FLARES out, and at the field's 65 deg the
    intersection spans 2.34 m vertically (1.09 m of shaft depth x tan65) -- the
    down-slope side shows the whole diagonal, the up-slope side only a sliver of
    shoulder above the shingles. That flare is `Base_Roof`, and it is what stops
    a chimney looking pasted on. IT IS ALSO THE FLASHING: there is no separate
    chimney flashing piece in the kit, the haunch's lead skirt is it.

PLACEMENT  --  THE CONTRACT AN ASSEMBLER HAS TO KEEP
  Stacks / caps / base: origin at the footprint centre (prop convention), Z=0 at
      the bottom. The core footprint is W (0.96) square on every piece, and no
      stack module carries a collar at its top, so modules butt into one
      continuous shaft: 1.6 + 2.6 + cap, in any order. The caps supply the
      oversailing top detail.
  Base_Roof: Z=0 is the DOWN-SLOPE TOE of the haunch and local +Y is up-slope.
      The stack axis is X=0, Y=0, so the toe sits BASE_TOE down-slope of the axis
      and the back of the haunch BASE_UP up-slope of it (the wedge is deliberately
      lopsided: a haunch throws its bulk down the slope). Its stepped underside
      follows the FIELD roof plane -- 65 deg, S.PITCH_F, not the kit's authored
      52 -- so drop it until the toe touches the SHINGLE SURFACE:

          y_axis = ridge_pos - BASE_UP            (the wedge's back on the ridge)
          toe_z  = ridge_z - Z_ROOF + ROOF_SKIN   (== ridge_z - TOE_DROP)
          place("SM_Chimney_Base_Roof",   (x, y_axis, toe_z))
          place("SM_Chimney_Stack_2_6m_A",(x, y_axis, toe_z + BASE_H), z=kz)
          place("SM_Chimney_Cap_*",       (x, y_axis, toe_z + BASE_H + 2.60*kz))

      Generally (a stack anywhere on a slope, not just under a ridge):
          toe_z = zsurf(y_axis - BASE_TOE) + ROOF_SKIN
      where zsurf is the NOMINAL field plane ridge_z - |dy|*tan65 and ROOF_SKIN
      is how far roofs.py's shingle skin stands above it (measured, see below).
      +Y is up-slope, so a chimney on the other slope of the same ridge is the
      same piece at rz=180 with y_axis = ridge_pos + BASE_UP.
      DO NOT BURY THE STACK. With the haunch placed the stack's foot sits
      BASE_H above the toe, i.e. 1.48 m clear of the roof surface at its own
      axis; burying it (assemble_inn.chimney's old "foot ~1 m under the ridge")
      is what the haunch replaces.
      THE RIDGE CAP DOES NOT NEED SUPPRESSING, and this was checked rather than
      assumed. With the axis at ridge_pos - BASE_UP the cornice reaches only
      y = ridge_pos - 0.42, clear of SM_Roof_Ridge_2m's y band (ridge_pos +- 0.19),
      and the stack's foot seats at 0.086 m above the cap's top -- so the cap
      passes BEHIND the chimney and reads as the ridge continuing, which is
      right. It does interpenetrate the wedge's topmost buried step (y
      ridge_pos-0.19 .. ridge_pos, z below the shoulder): solid inside solid,
      nothing visible. Do NOT move the axis further down-slope to avoid that --
      at ridge_pos - BASE_UP - 0.16 the whole chimney drops 0.34 m and the ridge
      cap comes out through the SHAFT.
      Known and left open: from a viewpoint above and behind the ridge you can
      see 159 px of sky through the void under the cornice's oversailing corner
      (measured, 1200x900). That void is what an oversail is, it was there at
      52 deg too, and closing it means widening the wedge to the cornice's full
      width, i.e. losing the oversail.
  Breast: an add-on, not a wall piece. Its BACK plane is Y=0 -- the wall's OUTER
      face -- and it grows outward (-Y) like all other kit relief, so it snaps to
      a stone wall bay at (bay_x, 0, 0) with no offset (rotate it about Z to put
      it on a gable end). Seat for a stack on top at Z=H_GROUND, on the flue
      axis Y=BR_AXIS, clear of the wall above. A breast climbing a gable WALL is
      a different condition from a stack rising from a ridge and carries no roof
      plane at all: nothing in the pitch fix touches it.
"""
import bpy
from math import radians, tan, cos, sin, pi
from mathutils import noise as _nz
from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "chimneys"
COLLECTION = "07_Chimneys"

# ------------------------------------------------------------------ sizes ----
W       = 0.96       # stack core footprint (square)
HW      = W / 2
ENV     = 0.58       # declared half-envelope: core + stone relief + oversails
H_SHORT = 1.60
H_TALL  = 2.60

CAP_H   = 0.74       # little roof cap (ref2)
POT_H   = 0.68       # corbelled cap + pots (ref1)

# ------------------------------------------------------------- the field -----
# THE PITCH THIS PIECE IS PLACED IN, NOT THE PITCH THE KIT AUTHORS AT.
#
# Every roof piece is drawn at S.PITCH (52 deg) so that any roof piece meets any
# other; the assembler then stretches the whole roof WORLD in Z by
# ZK = tan65/tan52 = 1.675, placing each roof piece at z*ZK with scale
# (s, s, s*ZK). A CHIMNEY IS PLACED UNSTRETCHED (it is a prop, not a roof
# piece), so every plane in this module that models THE ROOF has to be cut
# against the field's 65 deg. Cutting them at 52 is what put a hard horizontal
# cut line at the foot of every stack the assemblers place: the haunch was never
# placed at all, the bare shaft was dropped ~1.5 m into the ridge instead, and
# the shaft's own bottom course came out the shingles as six loose-looking
# stones lying on the roof (measured on out/inn_example.blend, stack
# SM_Chimney_Stack_2_6m_A.001 at x 17.71: 2280 px of shaft-on-shingle contact,
# 821 of it a dead horizontal line).
#
# AUDIT, site by site, 2026-08-28. Every use of the pitch in this file:
#   Z_ROOF                     roof height at the wedge's back        FIELD
#   _y_roof(z)                 how far up-slope the roof has risen    FIELD
#   base_roof: smax            slope run of the skirt's footprint     FIELD
#   base_roof: _on_roof        a point on the roof plane              FIELD
#   base_roof: flap rot (x2)   lead lying IN the roof plane           FIELD
#   demo: run / ctx rotation   the demo's own context slope           FIELD
#   demo: gable infill apex    must match that slope                  FIELD
#   demo: z_roof(y)            where the demo's chimneys land         FIELD
# ELEVEN sites, ALL of them the field. NOT ONE is the chimney's own geometry --
# a chimney is plumb, its caps carry their own tapers, and the breast is a wall
# piece with no roof plane in it -- so the fix is this definition and nothing
# else. (dormers.py learned the other way round: an earlier round there patched
# the single most obvious call site and left 21 others cutting at 52.)
TANP    = S.TAN_F                       # 2.14451  tan(65), the field AS PLACED
COS_F   = cos(S.PITCH_F)                # 0.42262
SIN_F   = sin(S.PITCH_F)                # 0.90631
PF_DEG  = S.PITCH_F_DEG                 # 65.0

# ...AND THE ROOF IS NOT ITS OWN PLANE. roofs.py's shingle skin stands PROUD of
# the nominal plane z = ridge - |dy|*tan65, because a course laps the one below
# it. Measured by raycasting straight down onto out/inn_example.blend's main
# roof at x 17.71, 17 samples from y 2.16 to 0.56 (the ridge cap's own two rows
# excluded): the surface sits +0.091 to +0.190 m in Z above the nominal plane,
# mean +0.154, i.e. +0.038..+0.080 measured PERPENDICULAR to the slope. That
# 0.10 m band is one course's saw-tooth.
#   The datum is the BOTTOM of that band, not the mean: a toe buried in the
# shingles is invisible, a toe floating over them is the defect. So the piece's
# own model of the roof surface is `nominal + ROOF_SKIN` with ROOF_SKIN at the
# low end, and Z_SLIV below carries the rest of the band so the shoulder clears
# the proudest course too.
ROOF_SKIN = 0.095
SKIN_BAND = 0.110       # ...and how far the skin's saw-tooth reaches above that

# THE SAME NUMBER stone_walls and timber_walls pin, deliberately: _blotch reads
# mathutils.noise, which is seeded PER BLENDER PROCESS, and this module never
# pinned it. util.Part.wobble was fixed at source to seed from the part name, so
# the GEOMETRY here is byte-identical run to run -- but wobble seeds at the END of
# a piece, and _blotch runs at the start, so the first piece built sampled whatever
# field the process happened to boot with and the stones' MATERIALS and shades came
# out different on every build. Same field as the walling means one more thing: the
# damp patches and sunned runs on a stack agree with the ones on the wall it lands
# on, which is a fair part of what "one mason" means.
NOISE_SEED = 20240823

# --- the base haunch. Measured off ref3: the shaft (~1.1m dressed) comes down
# --- into a WEDGE half again as wide at its foot, battering in over the slope,
# --- and the two meet at a cornice that oversails the shaft all round.
#
# THE FOOTPRINT IS DERIVED FROM THE SHAFT NOW, NOT TUNED TO A PITCH. BASE_TOE and
# BASE_UP are HORIZONTAL distances, and the wedge's height is tan(field) times
# their sum -- so they are exactly the kind of number dormers.py's second defect
# was: a length tuned to 52 deg that inverts its own profile at 65. At 52 a
# 1.30 m footprint gave a 1.82 m shoulder; the SAME footprint at 65 gives 2.79
# and a haunch taller than the shaft standing on it.
#   Shrinking the footprint to keep the old height does not work either. The
# floor is set by the SHAFT, not by taste: the wedge has to reach past the
# shaft's own faces on both sides, and the shaft's proudest cobble stands at
# HW + CROWN_MAX = 0.554. That forces
#     BASE_TOE + BASE_UP >= 1.12  ->  Z_SH >= 2.60  ->  BASE_H >= 2.85
# so ~2.85 is the SHORTEST haunch a 0.96 m shaft can have on a 65 deg roof, and
# the old 2.07 was only ever reachable at 52. This is the same arithmetic that
# makes the shaft/shingle intersection 2.34 m tall: the roof drops that far
# across the chimney's own depth, and the haunch has to bridge it.
#   What the pitch costs, and it is stated rather than hidden: the down-slope
# face's batter drops from 9.9 to 7.1 deg per side in width and from 7.5 to
# 4.2 deg in depth, because a batter needs horizontal room and 65 deg gives
# none. BASE_TW stays at its measured 1.74 rather than growing to 2.00 to hold
# the old batter -- 2.00 is wider than a 2 m wall bay and would break the
# declared x envelope and collide with dormers.
BASE_UP  = HW + .02  # 0.50  stack axis -> up-slope back of the wedge. The wedge
                     # reaches the shaft's own up-slope face; the cornice's
                     # 80 mm up-slope oversail then covers its proudest cobble
                     # (0.554 < 0.50 + 0.08). At the old 0.44 the shaft's back
                     # stones stood 34 mm past the cornice that crowns them.
BASE_TOE = HW + .14  # 0.62  stack axis -> down-slope toe of the wedge. 75 mm
                     # past the shaft's proudest cobble: every extra 10 mm here
                     # costs 21 mm of haunch height at 65 deg.
BASE_TW  = 1.74      # wedge width at the toe -- 1.6x the dressed shaft
BASE_SW  = 1.10      # wedge width at the shoulder, the shaft's own width
BASE_TT  = BASE_TOE - .17   # 0.45  axis -> down-slope face AT the shoulder, so
                     # the face rakes. Held above BASE_TT >= 0.397, which is
                     # what puts the cornice's own nose (BASE_TT + 0.160) out
                     # past the shaft's proudest cobble.
Z_SLIV   = SKIN_BAND + .09   # 0.20  shoulder clearance above the piece's model
                     # of the roof surface. SKIN_BAND covers the shingle course
                     # saw-tooth, the 0.09 is the sliver that actually reads:
                     # 0.09..0.20 in Z above the real shingles, 0.038..0.085
                     # measured perpendicular, against 0.0985 perpendicular at
                     # the authored 52 deg. Below SKIN_BAND the shingles come
                     # through the cornice.
Z_ROOF   = TANP * (BASE_TOE + BASE_UP)   # 2.4018  roof SURFACE height at the
                                         # up-slope back, above the toe
Z_SH     = Z_ROOF + Z_SLIV               # 2.6018  shoulder
CORN_H   = 0.245                         # the two-course oversailing cornice
BASE_H   = Z_SH + CORN_H                 # 2.8468  toe to seat
BASE_W   = BASE_TW                       # legacy alias: the widest footprint
# FOR THE ASSEMBLER: toe_z = ridge_z - TOE_DROP puts the wedge's back on the
# ridge with its toe on the shingles, when the axis is at ridge_pos -+ BASE_UP.
TOE_DROP = Z_ROOF - ROOF_SKIN            # 2.3068

BR_W0, BR_W1 = 1.50, 1.06   # breast width at plinth top / at the collar
BR_D0, BR_D1 = 0.98, 0.92   # breast projection at plinth top / at the collar
BR_AXIS = -0.46             # flue axis: where a stack sits on the breast


# ------------------------------------------------------------ private tools ---
def _bx(p, center, size, mat, **kw):
    """p.box(), with every face it made actually painted.

    WHY: util.Part._emit loses a primitive's own faces when the bevel rebuilds
    them (`f.is_valid` goes False and bmesh.ops.bevel returns only the new bevel
    strips), so a BEVELED box keeps material slot 0 and the default white vertex
    colour. Inside one Part that silently repaints every beveled primitive in
    whichever material happened to be used first -- it is why this family's dark
    lead cap was rendering as pale stone. Repainted here; the real fix belongs in
    util._emit and is reported upstream, not forked into this module.
    """
    before = set(p.bm.faces)
    p.box(center, size, mat, **kw)
    new = [f for f in p.bm.faces if f.is_valid and f not in before]
    p._paint(new, mat, kw.get("tint", 0.05), kw.get("shade", 1.0))
    return new


def _pr(p, verts2d, thickness, mat, **kw):
    """p.prism() with the same repaint fix as _bx()."""
    before = set(p.bm.faces)
    p.prism(verts2d, thickness, mat, **kw)
    new = [f for f in p.bm.faces if f.is_valid and f not in before]
    p._paint(new, mat, kw.get("tint", 0.05), kw.get("shade", 1.0))
    return new


def _lay(seed, x=0.0, y=0.0, amp=.0040):
    """Bed a centred body a few mm OFF the shaft axis. Deterministic.

    Two things wanted this, and they are the same thing.

    (1) LOOK. Every hidden mortar bed and every dressed course in this family was
        laid dead on the axis, so all four joints on a shaft came out the same
        8mm and every oversailing course was exactly concentric with the stones
        under it. A hand-laid stack has none of that; 3-4mm of bedding error
        makes the four joints unequal and the courses sit slightly askew, which
        is free irregularity on the one part of the piece that reads as machined.

    (2) MEASUREMENT. check_zfight decides a plane pair on
        `sep = min(|dA - dB|, |dA + dB|)`, where d = normal . centre. The second
        term is there to catch a face and its back-to-back twin, but it also
        matches any two faces that are simply EQUIDISTANT from the origin with
        opposite normals -- which is exactly what the two opposite sides of a box
        centred on the axis are. That is what the family's 182,774 cm2 was: the
        stack's own mortar core, its +X face against its -X face, 944mm apart,
        with nothing coincident anywhere near them (see the report). Off the axis
        by `amp`, the two planes differ by 2*amp and the reading is honest again.
    """
    r = rng(f"ch/lay/{seed}")
    return (x + r.choice((-1, 1)) * r.uniform(.62, 1.0) * amp,
            y + r.choice((-1, 1)) * r.uniform(.62, 1.0) * amp)


# --- the course grid --------------------------------------------------------
def _rows(z0, z1, course, key, fine=.90, jitter=.26):
    """Bed lines for one shaft module, SHARED by all four faces.

    A chimney's courses run right round the stack -- that is what makes four
    faces read as one built object instead of four wallpapered panels -- so the
    grid is drawn once here and handed to every face. What differs face to face
    is everything laid ON it: stone widths, splits, through-stones, tone, relief.

    Heights are jittered by +-26% and taper by `fine` toward the top. An even
    ladder of bed lines is half of what reads as "patterned" -- it keeps beating
    time no matter what stones sit on it -- and the lead still read the shaft as
    "near-uniform courses" at +-18%, so the spread is wider and the courses are
    taller. Real courses get shallower as a stack climbs, because the mason is
    lifting the stones higher.

    The other half of the answer is not here: it is `bed` in _rubble, which lets
    every individual stone give a slice of its cell back to the joint, so the bed
    LINE itself is ragged instead of ruled. A jittered ladder of straight lines
    is still a ladder.
    """
    n = max(1, int(round((z1 - z0) / course)))
    r = rng(f"ch/rows/{key}")
    hs = [lerp(1.0, fine, i / max(n - 1, 1)) * (1 + r.uniform(-jitter, jitter))
          for i in range(n)]
    k = (z1 - z0) / sum(hs)
    out, z = [], z0
    for hh in hs:
        out.append((z, z + hh * k))
        z += hh * k
    return out


def _blotch(u, v, ph=0.0, f=1.20):
    """Smooth -1..1 field across a face. Stone varies in PATCHES -- a run of
    warm blocks, a damp dark corner -- not stone by stone like confetti. Same
    device as stone_walls._blotch, which is a good part of why the two families
    now read as one quarry. `ph` is the face's own phase, so no two faces of a
    stack blotch alike.
    """
    return _nz.noise((u * f + ph * 3.1, v * f + ph * 1.7, ph * .37))


def _bedding(u, v, ph):
    """Relief multiplier for a stone bedded at (u, v): a smooth swell across the
    face, so the skin bulges and hollows the way laid masonry does.

    With p.blob cushions this swell was also load-bearing STRUCTURALLY: two
    cushions that overlap laterally punch through each other's lit face as soon
    as one is ~1.4x as deep as the other, so per-stone relief had to be given up
    to stop the interpenetration Shanee first complained about. A box laid inside
    its own cell has a real joint on every side, so no relief difference can push
    one stone into the next, and the per-stone draw is back on top of this swell
    (see the emit inside _rubble). The swell keeps the LARGE-scale variation --
    which is the half of it the eye actually reads as a hand-laid wall.
    """
    return (1.0 + .13 * sin(2.3 * u + ph) + .09 * sin(1.7 * v + ph * 1.7)
            + .045 * sin(5.1 * (u + v) + ph * .5))


def _hw(z):
    """Half-width of the base wedge at height z. A STRAIGHT rake, because the
    thing that makes a haunch read is one unbroken raking line from the toe up to
    the cornice -- curve it and the flare hides in the bottom 30cm, which is the
    part the shingles cover."""
    return lerp(BASE_TW / 2, BASE_SW / 2, clamp(z / Z_SH))


def _yf(z):
    """The down-slope face of the wedge at height z -- it rakes back as it climbs
    (so the toe is the furthest point down the roof, as in both references)."""
    return -lerp(BASE_TOE, BASE_TT, clamp(z / Z_SH))


def _y_roof(z):
    """How far up-slope the roof SURFACE has risen to height z, capped at the
    wedge's back (which the contract puts on the ridge, where the roof stops
    climbing). 65 deg -- see TANP: this is the FIELD, not the authored pitch."""
    return min(BASE_UP, z / TANP - BASE_TOE)


def _pick(r, t, dark=.02, warm=.32, pale=.065, b=0.0):
    """Stone colour, clustered by the blotch field `b`: damp and dark low down,
    warmer and paler up in the light.

    ROUND 4/5 -- THE BLOTCHING. Shanee, and the lead reading the closeup:
    "near-white blocks against dark grey ... it traded 'too regular' for
    'regular AND noisy'." That was this function plus _tone. The mix used to put
    a quarter of the stones on stone_pale (#A39D91, a full 22 sRGB points above
    `stone`) and another third on stone_warm, so on a face carrying three stones
    a course roughly every other stone was a different MATERIAL from its
    neighbour. Four materials at even odds is not "value variation", it is a
    chequer of paint samples.

    Round 4 pulled pale to .13 and it was still the loudest thing in the render,
    because a 0.96 m face only carries 3-4 stones a course: one pale stone in
    eight on a 2 m wall is a quiet accent, and one in eight on a chimney is
    every other course. So the mix is now hard `stone`-led -- 58% plain, 32%
    warm (only 12 sRGB points off `stone`: a tone, not a colour), 6.5% pale and
    2% dark. The pale and the dark are the FEW stones that are genuinely
    different, which is what ref1 shows: one grey with a handful of bleached and
    a handful of wet stones in it, and the near-black is the JOINTS.
    """
    q = r.random()
    d = dark + (1.0 - t) * (1.0 - t) * .022 + max(-b, 0.0) * .030
    w = warm + t * .03 + max(b, 0.0) * .08
    pl = pale + t * .02 + max(b, 0.0) * .045
    if q < d:
        return "stone_dark"
    if q < d + w:
        return "stone_warm"
    if q < d + w + pl:
        return "stone_pale"
    return "stone"


def _tone(r, t, b, dark, warm, pale, var):
    """Material + shade for one stone: patch-clustered, damp low, bleached high.

    VALUE COMES FROM THE PATCH, NOT FROM THE STONE. Same lesson stone_walls._tone
    learned: a big per-stone die is confetti -- every stone a different value from
    the one beside it, which at demo distance averages back to one flat tone with a
    busy grain and up close reads as sample tiles. So the die is SMALLER than the
    smooth _blotch field it rides on (.036 against .075), which puts the light and
    dark in RUNS -- a damp corner, a sunned patch -- the way masonry weathers.

    The two extreme materials are pulled hard back toward the middle rather than
    pushed away from it: stone_dark is LIFTED (as stone_walls does) so it reads as
    a wet stone and not as a missing one, and stone_pale is dropped .155 -- nearly
    twice round 4's .085 -- because #A39D91 unpenalised is the "near-white block"
    in the lead's note. The clamp is .84-1.05, against round 4's .76-1.09 and
    round 3's .58-1.18: measured on the rendered face that is about 1.2 stops of
    total spread, against 2.2 and 4.5.

    `rare` is the deliberate exception -- roughly one stone in twenty-two is
    allowed a real excursion, because a wall with NO outliers reads as
    machine-laid. A FEW stones differ; every stone does not.
    """
    m = _pick(r, t, dark, warm, pale, b)
    rare = r.uniform(-.10, .075) if r.random() < .045 else 0.0
    sd = (1.0 + b * .075 + r.uniform(-var, var) + lerp(-.030, .024, t) + rare
          + (.135 if m == "stone_dark" else 0.0)
          - (.155 if m == "stone_pale" else 0.0))
    return m, clamp(sd, .84, 1.05)


# ----------------------------------------------------- rounded coursed rubble --
# ROUND 4. The lead, reading renders/chimneys/closeup.png: "a stack of flat-faced
# rectangular blocks in near-uniform courses ... no face relief, hard square
# edges, uniform widths, and there is no mortar recess."  All four of those were
# true, and all four came out of one decision: round 3 laid every stone as
# p.box(..., bevel=0). A box with no bevel has ONE flat plate for a face and a
# 90 deg arris all the way round it, and 168 of them in a grid is Lego.
#
# The history matters, because the two obvious cures are both wrong:
#   * p.blob cushions (round 1) are the right SHAPE but they were laid ~15%
#     oversize to close the perpends of a hexagon inside a rectangle, and that
#     oversize is the interpenetration Shanee reported first;
#   * plain boxes (round 3) cannot interpenetrate but they are plates.
# So the primitive is _cobble(): a cushion whose OUTLINE IS INSCRIBED IN ITS CELL
# -- clamped to it vertex by vertex, so it needs no oversize and cannot reach into
# a neighbour by construction -- bulging in two steps to an off-centre crown.
# Rounded stone AND no interpenetration, which is the pair of things this family
# spent five rounds failing one at a time.
#
# THE JOINT IS NOW A SURFACE. Round 3's "mortar" was the dark core 22 mm behind
# the stone backs, i.e. a black slot with no tone: that is the missing "mortar
# recess". _mortar() replaces it with a banded mass whose front plane sits 6 mm
# behind the face plane at MORT_SHADE, exactly the way stone_walls.mortar_field
# does it and for the same reason -- a joint you can see the colour of.
JOINT    = .003   # nominal gap between two cells inside a course. SMALL on
                  # purpose: ref1's rubble is packed TIGHT, its joints a thin
                  # dark crease about an eighth of a stone. It is no longer the
                  # whole story and it is not meant to be: since round 12 the
                  # outline is the cell with its corners taken round, so the
                  # drawn joint is this gap ALONG the flats plus the corner
                  # segments where three stones meet -- 15-21 mm on a 0.96 m
                  # stack, i.e. 4-12% of a stone (the low end is the
                  # dressed variant), which is where ref1 packs.
                  # (Round 11 read 6-10% here too, and that number was the joint
                  # NEARLY CLOSED: the outline had been clamped into the cell
                  # rectangle, so there was no continuous joint to measure --
                  # only a dark chip at the corners. A gauge that says the same
                  # thing about two very different walls is a warning to go and
                  # LOOK at the render, which is what round 12 did.)
CORNER_J = .028   # joint at an arris: the face that does NOT own the corner on
                  # this course stops this far short of it, x .85-1.5 drawn per
                  # course (see _rubble) so the corner joint is not itself a ruled
                  # line. MUST STAY > BACK + SINK_MAX-on-a-corner-stone (.0112),
                  # or the two skins meeting at that corner share volume -- that
                  # is the arris interpenetration, closed by arithmetic. Round 13
                  # took it .022 -> .028 to buy that margin back after the bedding
                  # sink went in; at a 45 deg view a stone standing 12-74 mm proud
                  # hides a 28 mm return joint, so nothing opens up.
TURN_MAX = .066   # ...and the LONGEST return a stone that owns an arris may make
                  # past it. The stacks declare ENV = .58 round a .48 half-core,
                  # so 100 mm is all there is; .086 leaves 14 mm for p.wobble and
                  # the mid-ring lean. See the note on the return in _rubble.emit.
LONG, SHORT = (1.30, 1.70), (.52, .84)
                  # LONG-AND-SHORT WORK AT THE ARRIS, in course heights. The
                  # single most "patterned" thing about the old stack, and the
                  # lead named the mechanism: "the stones on the left face and the
                  # stones on the front face meet at a clean vertical edge, each
                  # face's coursing independent ... it tells the eye the faces are
                  # wallpaper on a box."
                  #   The toothing was already there in the topology -- one face
                  # owns each corner on each course and returns past it -- but the
                  # return was cut to `crown + 6 mm`, i.e. just enough to CLOSE
                  # the corner joint and land flush with the perpendicular face's
                  # own crowns. A flush return is a clean arris by construction.
                  # What a mason actually lays is a LONG stone on the face that
                  # turns the corner and a SHORT one on the face that stops at it,
                  # alternating course by course, so the corner reads as a
                  # zip of alternating long and short ends. That is drawn now:
                  # the end stone of a course is dealt from LONG if this face owns
                  # the arris and from SHORT if it does not (see _widths), the
                  # return itself is drawn rather than derived, and CORNER_J is
                  # jittered per course. Costs nothing in triangles.
BACK     = .0012  # how far a cobble's OUTLINE sits behind the face plane.
                  #   ROUND 12 REVERSED THE SIGN OF THIS AGAINST THE MORTAR, and
                  # that is what makes the outline the thing the eye reads. What
                  # reads as the edge of a stone is not its outline if the
                  # outline is BURIED -- it is the section where the flank
                  # crosses the mortar surface, and that section is
                  # (BACK - MORT_IN) / apex-depth narrower than the cell on every
                  # side. At BACK = 3 mm behind a MORT_IN = 2 mm mortar plane
                  # that was ~2 mm a side given away before anybody could see it,
                  # and round 9's answer -- growing the buried skirt (GROW) --
                  # is what put 1548 interpenetrating pairs in the family.
                  #   At 1.2 mm the outline stands 0.8 mm PROUD of the mortar
                  # surface, so the widest section of the stone IS its cell and
                  # the drawn joint is the joint the course laid out. That is
                  # stone_walls' SKIRT_Y rule reached from the other side, and it
                  # costs nothing in overlap: the cell clamp is untouched.
                  #   The risk it trades against is an OPEN RIM -- a cobble has
                  # no back face, so if its rim stood clear of the mortar a
                  # grazing ray could pass under it. It cannot: the mortar body
                  # is opaque 0.8 mm behind the rim, and every stack was raycast
                  # on a 1.5 mm grid for back-facing hits. Zero, every piece.
                  # (The stacks run .0006 of wobble and the mortar body does not
                  # wobble at all, so 0.8 mm still has margin.)
                  # CORNER_J is still well over BACK, which is the inequality
                  # that makes arris interpenetration impossible.
BITE_V   = .010   # vertical overshoot at a module seam. clamp_to_seams shears it
                  # flat, so two butted shaft modules meet with no band of bare
                  # mortar between them
MORT_IN  = .002   # mortar front plane, measured in from the face plane. The
                  # rendered recess is therefore (a stone's own crown + 2 mm),
                  # about 50 mm on the mean stone -- stone_walls runs 30 mm on a
                  # 2 m wall, and this is a 0.96 m stack of domed cobbles.
                  # MUST STAY > BACK: that inequality is what puts the stone's
                  # widest section in FRONT of the lime it is bedded in.
MORT_SHADE = .60  # ...and its tone, ON `stone`, NOT on stone_dark. This is the
                  # "there is no mortar recess" half of the lead's note and it
                  # was a MATERIAL bug, not a geometry one: stone_dark (#46433D)
                  # at .74 renders at 47% of the stone face beside it, which is
                  # a black slot -- an absence, exactly what the lead could not
                  # see a joint in. `stone` at .66 renders at 66% of the face:
                  # unmistakably a recess, unmistakably still lime you can read
                  # the colour of. stone_walls reaches the same place from the
                  # other side (stone_dark at .70 behind a 30 mm recess).
MIDR     = .70    # ROUND 6, AND THE WHOLE ANSWER TO "flat plates with one folded
                  # lip". Where a cobble's SECOND ring sits, as a fraction of its
                  # outline.
                  #   Round 5 built the face as ONE ring, inset from the outline
                  # by an absolute chamfer of 1/tan(34 deg) of the depth it had
                  # to climb, with an apex barely above it. Measured off the
                  # solid render: the dome rose 8% of the stone's width and 30%
                  # of stones had 85% of the face inside one plane at a 20 deg
                  # tolerance. That is sheet metal, and no amount of chamfer
                  # tuning reaches it, because the chamfer was never the problem:
                  # THE FACE ITSELF WAS FLAT, one plate with a lip folded round
                  # it, and the ring/apex pair only ever added a 16 mm crease at
                  # the middle of a 220 mm stone.
                  #   So the face is now a cushion that bulges in TWO STEPS --
                  # exactly what util.Part.blob draws, which is the primitive
                  # this family should have been reading all along: outline -> a
                  # ring at MIDR of it, carrying most of the climb -> an
                  # off-centre apex. The ring is a SCALE of the outline, not an
                  # absolute inset, and that is the other half of the fix. An
                  # absolute inset gives a 400 mm stone the same 46 mm band as a
                  # 150 mm one, so a long stone stayed a plate with its ends
                  # folded into the razor wedges Shanee saw. At .78 the band is
                  # 22% of EACH half-extent, so a long stone comes out as a LOAF
                  # -- domed hard across, gently along -- and no band anywhere is
                  # a sliver.
DOME     = .48    # ...and how much of the climb happens ABOVE that ring. MIDR and
                  # DOME together are the profile. With the ring at .78 of the
                  # outline and 45% of the climb below it, the outer band runs
                  # 37-56 deg off the face and the cap 15-27 deg: they differ by
                  # 22-29 deg, i.e. INSIDE spec.SMOOTH_ANG (34), so the band and
                  # the cap shade as ONE CURVE and the stone reads round instead
                  # of creasing at a rim. That invariant is the one thing round 5
                  # had right -- it just met it with a flat face. The cap carries
                  # ~60% of the area, and it is a cone of n facets rather than a
                  # plane, so no stone reads as one plane either.
RISE_LO, RISE_HI = .11, .46
                  # THE DOME IS TIED TO THE STONE, NOT TO THE WALL -- but it is
                  # a BAND the per-stone draw moves inside, never a floor the
                  # draw disappears under. See _crown().
                  #   ROUND 13, AND THIS IS THE "no relief" DEFECT, MEASURED.
                  # Shanee, twice: "too regular/patterned on each face"; the
                  # lead, with the closeup beside a stone_walls bay: "every stone
                  # on the chimney sits in ONE plane with a narrow dark groove
                  # between; nothing stands proud, nothing recedes."
                  #   At (.26, .37) that was arithmetically true and it had
                  # nothing to do with the dice. _crown read
                  # `min(max(back + relief, RISE_LO*g), RISE_HI*min(w,h), ...)`,
                  # i.e. the size floor RISE_LO*sqrt(w*h) and the size ceiling
                  # RISE_HI*min(w,h) sat only 11 mm apart on the median stone --
                  # and the whole per-stone bedding draw (depth .040 x .62-1.22,
                  # a 24 mm span) fell BELOW the floor for most of its range. Run
                  # the numbers the module actually draws:
                  #     stone 140 x 160   the draw moves the crown 11.1 mm
                  #     stone 174 x 159   ...............................  6.8
                  #     stone 240 x 190   ...............................  0.0
                  #     stone 300 x 210   ...............................  0.0
                  # Every stone over ~230 mm came out at EXACTLY RISE_LO*g,
                  # whatever the mason drew for it. So relief was a pure function
                  # of stone SIZE: two neighbours of the same size had bit-identical
                  # projection, and a facing whose only depth cue is correlated 1:1
                  # with area is a pattern carved into one plane -- which is what
                  # it looks like, and no amount of re-seeding could have moved it.
                  #   At (.11, .46) the band on that median stone is 18-73 mm, the
                  # draw spans it, and relief is DECORRELATED from size: measured
                  # per stone off the built mesh, the -Y face of stack A went from
                  # a p05-p95 crown spread of 27 mm (sd 10) to 50 mm (sd 16), with
                  # the crown/size correlation down from .93 to .35.
                  #   The two invariants the old floor and ceiling were there for
                  # survive, because they are still the band's ends: a packer
                  # cannot be a spike (RISE_HI is off the SHORT side, so a 90 mm
                  # stone is capped at 41 mm) and a big stone cannot be a plate
                  # (RISE_LO*g gives a 300 mm through-stone at least 28 mm). And
                  # the band-to-cap step stays inside spec.SMOOTH_ANG at both ends:
                  # 21 deg vs 9 at the flattest, 56 vs 30 at the boldest.
SINK_MAX = .0025  # ...and how far a stone may be BEDDED BACK, i.e. how far its
                  # whole shell -- outline, shoulder and crown together -- slides
                  # in behind the face plane. The dome above is what makes a stone
                  # stand PROUD; this is the other half of the lead's note ("let a
                  # few sit noticeably back"), and it is a different thing: a shy
                  # dome is a FLATTER stone, a sunk one is a stone SET DEEPER, and
                  # only the second moves the section the eye reads as the stone's
                  # edge back behind its neighbours' and opens the joint round it.
                  #   Correlated with the dome draw (see _rubble.emit), so the
                  # flattest stones are also the deepest-bedded and the ladder is
                  # the sum of the two: net crown 12-74 mm against the old 35-62.
                  #   IT IS SMALL, AND THE FIRST CUT OF ROUND 13 MEASURED WHY. At
                  # .018, capped at .42 of the stone's own crown, the family's
                  # coverage fell from 85% to 57-71% and the drawn joint went to
                  # 25-53% of a stone: a wall of pebbles scattered in lime, which
                  # is the exact failure rounds 9-12 spent themselves closing.
                  # The arithmetic is unforgiving and it is worth writing down.
                  # What the eye reads as the edge of a sunk stone is where its
                  # flank crosses the MORTAR surface, and the flank draws in by
                  # (1 - MIDR) = 30% of a half-extent over the whole climb to the
                  # mid ring (~.52 of it). So sinking a stone by `s` narrows every
                  # visible section by  (s + BACK - MORT_IN)/(.52*(BACK+crown)) x 30%
                  # of a half-extent A SIDE -- on a shy 20 mm stone, 8 mm of sink is
                  # a fifth of the stone gone, and the shy stones are exactly the
                  # ones this was sinking. Isolated by rebuilding with the sink
                  # forced to zero: coverage came straight back to 83-90% with the
                  # bed-line wander still in, so the wander was innocent and this
                  # was the whole of it.
                  #   So the cap is written against the TAPER instead of against
                  # the crown -- .09 of the stone's own climb, which holds the
                  # narrowing under ~4.5% of a half-extent whatever the stone --
                  # and the ladder that answers "let a few sit noticeably back" is
                  # carried by the DOME, where it costs no coverage at all: a stone
                  # standing 9 mm proud beside one standing 62 sits 53 mm back, and
                  # that is the p05 and the p95 of the shipped facing. What the
                  # sink adds on top is that the OUTLINES are no longer one plane
                  # either, which is what stops the field looking milled at a
                  # grazing angle.
                  #   AND AT .010 ON A STONE THAT TURNS AN ARRIS, because
                  # CORNER_J > BACK + sink is the inequality that keeps the two
                  # skins meeting at a corner out of each other's volume.
BIG_A    = .105   # m2. Above this a stone gets the full two-step cushion, below
                  # it a cone. See the note at the call site in _rubble.emit.
                  #   ROUND 12 RAISED IT FROM .062, and it is the triangle budget
                  # again rather than a taste: the outline went from a ring that
                  # _dedupe collapsed to 4-5 points to a real 10-12-gon, so a
                  # cone costs 10-12 triangles and a cushion three times that. At
                  # .062 a 2.6 m stack came out at 4363 against a 3000 cap. At
                  # .105 only the genuinely big stones -- through-stones, long
                  # stones, dressed quoins -- keep a shoulder ring, everything
                  # else is a cone of 10-12 facets round an off-centre apex, and
                  # stack A lands at 2804. A 12-facet cone at a 28-36 deg flank
                  # IS a pebble; the four-facet cone over a clamped rectangle
                  # that round 11 was drawing was a paper dart, and that was the
                  # outline's fault, not the cone's.
CROWN_MAX = .074  # ...and the hard ceiling on any crown, in metres. The stacks
                  # declare a half-envelope of ENV (0.58) round a 0.48 half-core,
                  # so 100 mm is all the room there is on a face and p.wobble
                  # spends 6 of it. Anything past that does not read as a bolder
                  # stone, it reads as a stone with its face sheared flat by
                  # clamp_to_seams, which is what the envelope check does with it.
OVERSAIL = CROWN_MAX + .012
                  # THE OVERSAIL LADDER, IN ONE NUMBER, AND DERIVED RATHER THAN
                  # CHOSEN. _crown caps every cobble in the family at CROWN_MAX
                  # proud of its own face plane and p.wobble spends 6 mm more, so
                  # any dressed course meant to READ as oversailing rubble has to
                  # project at least this far -- string courses, corbels, cap
                  # collars, the haunch cornice, the breast's drip band and its
                  # capstone, all of them.
                  #   Round 5 sized those by hand against a max_proud() that did
                  # its own arithmetic, and the two drifted: the function said
                  # 76 mm, the geometry did 106, and the courses were built at 24
                  # to 58 -- so EVERY oversailing course in the family was
                  # actually behind the stones it oversails. That is the "string
                  # course reads as a recess" note arriving from a third
                  # direction, and it is why the second source of truth is gone
                  # and this one is a sum of the two constants that make it.
FILL     = (.34, .62)
                  # ROUND 12, AND IT REPLACES INFL/EE ENTIRELY (see _cobble).
                  # How round a cobble's four corners are cut, as a fraction of
                  # its own half-extents: the corner is a quarter ellipse of
                  # radii (f*bu, f*bv), so the stone gives back exactly
                  # (1 - pi/4) f^2 = .2146 f^2 of its cell and the rest of the
                  # outline runs dead straight along the cell edge, hard against
                  # the plane its neighbour beds to. Packing is therefore
                  # arithmetic rather than a tuning problem:
                  #     f = .40 -> 96.6% of the cell    f = .70 -> 89.5%
                  #     f = .54 -> 93.7%                f = 1.0 -> 78.5% (ellipse)
                  # At (.38, .70) the mean stone keeps 94% of its cell -- tighter
                  # than round 11's clamped superellipse managed -- while every
                  # corner is a real two-chord arc instead of one 45 deg chamfer.
ARC      = 1      # ...and how many INTERIOR points each of those arcs carries.
                  # 1 is two chords across the 90 deg, i.e. 12 vertices on the
                  # whole outline. It is also the whole triangle budget: a cone
                  # costs one triangle per vertex and a two-step cushion three,
                  # so ARC = 2 (16 vertices) would put a 2.6 m stack 800 tris
                  # over spec.TRI_BUDGET["chimney"]. Measured: at ARC = 1 the
                  # chord sagitta is 7.6% of the corner radius, about 3 mm on the
                  # median stone, which is under the wobble.
ARC_P    = .62    # ...and how often a corner gets that interior point at all.
                  # See the note at the draw in _cobble: this is the triangle
                  # budget expressed as a shape. The stone that loses the draw
                  # keeps a single-chord corner, which is a split face rather
                  # than a worn one, so the field reads as a mix of both.
CHAMF    = .20    # ...and how often a corner is cut as ONE chord instead: a
                  # stone that was split rather than water-worn. A field where
                  # every corner is the same arc is a field of one shape scaled,
                  # which is the note this family keeps getting.
INFL     = 1.20   # SUPERSEDED BY FILL (round 12) -- kept because _rubble's
                  # public signature names it. It scaled the outline ring past
                  # circumscription so the clamp cut flats at the four axes; at
                  # 1.20 with 8 sides EVERY vertex clamped, most onto the cell's
                  # own corners, and _dedupe collapsed the outline to the cell
                  # RECTANGLE. See the note in _cobble.
ROLL     = 3.8    # max in-plane roll, degrees, for a NEAR-SQUARE stone. Scaled
                  # down by aspect (see _cobble) so a long stone rolls less: the
                  # same rule stone_walls._one settled on, because the corner
                  # excursion a roll costs is what has to stay inside the cell.
ASPECT   = 2.00   # the longest a stone may be, in its own course heights. Round
                  # 5 drew up to 2.35 courses and then multiplied by wmul, so the
                  # tail ran past 3:1 -- and a 3:1 stone is the one that cannot
                  # be domed (its crown is a ridge, its ends are wedges) and the
                  # one the verifier found the slivers on. Long stones are still
                  # what breaks a course up; 2:1 is long enough to read as one.
# THE PER-STONE BEDDING DIE, three-humped: how deep the mason set THIS stone,
# as a multiple of the run's nominal `depth`. See emit() in _rubble.
#   Round 12 ran a single hump, .62-1.22, and it did not matter what it drew
# because _crown's size floor ate it (see RISE_LO). Now that the draw reaches the
# geometry it has to have OUTLIERS in it, for the same reason _widths is
# three-humped: a field where every stone is within 20% of the mean is a field of
# one stone repeated, whatever the mean is. So most stones are ordinary, one in
# six is set back hard and one in six stands out hard, and the two tails are what
# the eye reads as a hand-laid facing.
SET_BACK_P = .17        # ...how often a stone is bedded shy and deep
PROUD_P    = .17        # ...and how often it is laid bold and shallow
REL_SHY  = (.30, .60)
REL_MID  = (.80, 1.36)
REL_BOLD = (1.48, 2.10)
# ...and the smooth swell across the face (see _bedding) is raised to this power
# before it multiplies the die, so the relief runs in PATCHES -- a proud shoulder
# of wall, a hollow where the lime took the weather -- rather than as confetti.
SWELL_P  = 1.25

# --------------------------------------------------------- the bed line -------
WANDER   = .13    # HOW FAR A BED LINE WANDERS, as a fraction of the module's
                  # mean course height. Defect 3 of the lead's note: "the bed
                  # joints run dead straight and level all the way round at a
                  # constant course height. Break the course height, let a bed
                  # joint step or die out."
                  #   _rows already jittered the course HEIGHTS by +-26% and
                  # tapered them up the stack, and `bed` gave each stone a slice
                  # of its cell back to the joint -- but at .011 of a cell that
                  # slice is 1.3 mm, and every bed line was still one dead level
                  # ruled line running right round the stack. A ladder of jittered
                  # straight lines is still a ladder.
                  #   So a bed line is now a piecewise-constant WANDER in the
                  # perimeter coordinate: it takes WSEG steps of up to this
                  # fraction of a course somewhere round the stack, and each
                  # stone takes the MAX of it over its own span for its bed and
                  # the MIN for its head. That ordering is the whole safety
                  # argument -- for any two stones bedded on the same line whose
                  # spans overlap at u*, min <= f(u*) <= max, so the stone above
                  # can never reach below the stone below, and what the wander
                  # costs is always given to the JOINT. A course therefore varies
                  # in height along its own length, a bed line visibly STEPS at a
                  # perpend, and where a stone straddles a step the joint opens
                  # and the bed line DIES OUT. Zero triangles.
                  #   IT IS PERIODIC IN THE PERIMETER, not per face: the wander
                  # is drawn once per bed line as a function of arc length round
                  # the shaft, and each face maps its own u onto that (see _dress
                  # and `sarc`). So the courses wander AND still meet exactly at
                  # all four arrises, which is what keeps four faces reading as
                  # one built object rather than four wallpapered panels.
                  #   The first and last bed lines of a module never wander:
                  # those are the module seam, where two butted shafts have to
                  # meet flush.
WSEG     = (7, 13)# ...and how many steps a bed line takes in one circuit.
                  # IT IS THE DENSITY THAT MATTERS, not just the amplitude, and
                  # the first cut of round 13 got it wrong: (3, 7) steps round a
                  # 3.84 m circuit is one step every 0.55-1.3 m, so a 0.96 m face
                  # saw 0.7-1.75 of them and most of a face still had one dead
                  # level bed line running right across it. Measured on a 1.5 mm
                  # raycast grid, counting scanlines that are almost entirely
                  # joint (which is exactly what a ruled bed line is), it barely
                  # moved the number. At (7, 13) every face sees 1.7-3.3 steps.


def _wander(key, rows, per, seg=WSEG, amp_f=WANDER, ends=(True, True)):
    """THE BED LINES' WANDER, drawn once for a whole module and shared by every
    face of it. Returns one entry per bed line (len(rows) + 1 of them), each a
    (breaks, values) pair describing a piecewise-constant offset in the PERIMETER
    coordinate `s`.

    See WANDER for why this exists. The three things that make it safe:

      * it is a function of s alone, and s runs continuously round the stack (see
        _dress), so face A's offset where it meets face B is face B's offset --
        the courses wander AND still close at every arris;
      * every stone takes the MAX of its own bed line over its own span and the
        MIN of its head line, so the wander can only ever give ground back to the
        joint. Two stones bedded on one line whose spans overlap at u* satisfy
        min <= f(u*) <= max, so the upper can never reach down into the lower:
        no interpenetration is possible by arithmetic, exactly as the cell rule
        makes it impossible across a perpend;
      * bed line 0 and bed line n are drawn flat when `ends` says so, because
        those are the module seam and two butted shafts have to meet with no
        step.

    The amplitude is a fraction of the module's MEAN course height, so a fine
    course wanders less than a coarse one and the whole thing scales with the
    piece.
    """
    n = len(rows)
    amp = amp_f * ((rows[-1][1] - rows[0][0]) / max(n, 1))
    out = []
    for j in range(n + 1):
        flat = (j == 0 and ends[0]) or (j == n and ends[1])
        r = rng(f"ch/wander/{key}/{j}")
        if flat or amp < 1e-5:
            out.append(((), (0.0,)))
            continue
        k = r.randint(*seg)
        br = tuple(sorted(r.uniform(0, per) for _ in range(k)))
        vals = [r.uniform(-1, 1) * amp for _ in range(k + 1)]
        vals[-1] = vals[0]            # periodic: last segment wraps into the first
        out.append((br, tuple(vals)))
    return out


def _wval(bl, s, per):
    br, vals = bl
    if not br:
        return vals[0]
    s %= per
    i = 0
    while i < len(br) and s >= br[i]:
        i += 1
    return vals[i]


def _wspan(bl, sa, sb, per):
    """(min, max) of one bed line's wander over the arc [sa, sb]."""
    br, vals = bl
    if not br:
        return (vals[0], vals[0])
    a, b = (min(sa, sb) % per, max(sa, sb) % per)
    if b < a:                      # a span that wrapped: take the whole circuit
        return (min(vals), max(vals))
    vs = [_wval(bl, a, per), _wval(bl, b, per)]
    for i, x in enumerate(br):
        if a < x < b:
            vs.append(vals[i])
            vs.append(vals[i + 1])
    return (min(vs), max(vs))


def _crown(relief, w, h, back=BACK):
    """How far a cobble laid at `relief` ACTUALLY stands off its face plane.

    ONE function, read by both _cobble (which builds the dome) and _rubble (which
    has to know how far a corner stone reaches round its arris), so the two can
    never disagree about how proud a stone is.

    `relief` is the bedding draw -- how deep the mason set THIS stone -- but the
    crown of a cushion is a property of the STONE:

      * the FLOOR is RISE_LO of sqrt(w*h), which is what stops a 340 mm
        through-stone being handed 8% of its width, i.e. the plate the verifier
        measured on "the large stones";
      * the CEILING is RISE_HI of the SHORT side, not of sqrt(w*h), and the
        difference matters on a flat stone: at 4:1, sqrt(w*h) is twice the short
        side, so a ceiling drawn off it lets the band across the stone stand up
        at 78 deg against a 36 deg cap -- a 42 deg crease, past
        spec.SMOOTH_ANG, which renders as exactly the folded lip this round is
        here to kill. Off the short side the band never passes ~59 deg and the
        band-to-cap step never passes 30;
      * and CROWN_MAX over the top of both, because a stone whose dome is drawn
        off its own size can be given more than the piece's declared envelope
        has room for -- measured on the first build of this round at 106 mm
        against the stacks' 100 mm, where clamp_to_seams silently sheared the
        proudest crowns flat.

    ROUND 13: IT IS A BAND THE DRAW MOVES INSIDE, NOT A FLOOR IT VANISHES UNDER.
    The old form was `min(max(back + relief, RISE_LO*g), RISE_HI*min(w,h), ...)`
    -- a floor drawn off the stone's size, a ceiling drawn off its size, and the
    mason's draw somewhere underneath both of them. With RISE_LO/RISE_HI 11 mm
    apart on the median stone that made the crown a pure function of AREA: on
    anything over ~230 mm the whole 24 mm bedding draw moved it 0.0 mm (the table
    is under RISE_LO). A facing whose only depth cue is 1:1 with stone size reads
    as a pattern carved into one plane, which is exactly the note. The band is
    wide now and the draw is clamped INTO it, so two neighbours of the same size
    can be 50 mm apart in projection -- and _band() is public so emit() can ask
    where in the band a stone landed and bed the shy ones deeper still.

    _band() is ordered min/max, never a bare clamp(): on a very flat stone the
    floor lands above the ceiling, and a clamp would then return the floor --
    handing the flattest stone in the wall the deepest dome in it.
    """
    lo, hi = _band(w, h)
    return clamp(relief, lo, hi)


def _band(w, h):
    """(flattest, boldest) crown a stone of this size may be given, in metres.

    The floor is RISE_LO of sqrt(w*h) -- what stops a 340 mm through-stone being
    handed 8% of its width, i.e. the plate the verifier measured on "the large
    stones". The ceiling is RISE_HI of the SHORT side, not of sqrt(w*h): at 4:1
    sqrt(w*h) is twice the short side, so a ceiling drawn off it lets the band
    across the stone stand up at 78 deg against a 36 deg cap -- a 42 deg crease,
    past spec.SMOOTH_ANG, which renders as the folded lip round 6 killed. And
    CROWN_MAX over the top of both, because a dome drawn off the stone's own size
    can otherwise ask for more than the piece's declared envelope has room for.
    """
    w, h = max(w, 1e-6), max(h, 1e-6)
    lo = RISE_LO * (w * h) ** .5
    hi = min(RISE_HI * min(w, h), CROWN_MAX)
    return (min(lo, hi), max(lo, hi))


def _free(lo, hi, blocked):
    """[lo, hi] minus the u-intervals a through-stone from the course below is
    still standing in. Returns the runs of course left to fill."""
    out = [(lo, hi)]
    for b0, b1 in blocked:
        nxt = []
        for a0, a1 in out:
            if b1 <= a0 or b0 >= a1:
                nxt.append((a0, a1))
                continue
            if b0 - a0 > .04:
                nxt.append((a0, b0))
            if a1 - b1 > .04:
                nxt.append((b1, a1))
        out = nxt
    return out


def _clear(a, b, blocked):
    """Is the u-run [a, b] free of every through-stone still standing in it?

    THE QUOIN NEEDED THIS AND DID NOT HAVE IT, and a BVH self-overlap check is
    the only reason anyone would ever find it: a through-stone spanning courses
    k and k+1 registers its cell in `blocked`, and course k+1's FILL honours that
    through `_free` -- but the dressed quoin is laid BEFORE the fill, straight
    onto [lo, lo + qw], with nothing consulted. On the ashlar stack, where
    quoin=.90, that put one quoin 26 mm inside the through-stone beside it: one
    pair in 700 stones, invisible in a render, and exactly the class of defect
    ("stones interpenetrating at the edges") this family has spent three rounds
    trading its stone-ness against. Measured, not eyeballed.
    """
    return all(b <= x0 or a >= x1 for (x0, x1) in blocked)


def _widths(r, span, h, wide, big, wmul, small=.17, aspect=ASPECT,
            end_lo=0, end_hi=0):
    """Stone widths for one run of course, laid then normalised to fit exactly.

    THREE-HUMPED, like stone_walls._lengths and for the same reason: a course
    whose stones are all 1.0-1.4x the course height is a course of near-identical
    cells, and "uniform widths" is one of the four things the lead called out. So
    the draw is a genuinely long stone (1.42-1.88 courses), a plain near-equant
    middle, or a real packer at half a course -- and the outliers are what the eye
    reads as hand-laid. Widths are drawn against the COURSE HEIGHT throughout, so
    the stones stay equant whatever the course does.

    EVERY WIDTH IS CAPPED AT `aspect` COURSES, and the normalisation is capped
    with it. Round 5 drew up to 2.35 and then multiplied by wmul (up to 1.20) and
    then normalised by up to 1/.70, so the tail ran past 3:1 -- and a 3:1 stone
    is the one that cannot carry a dome and the one the verifier found the razor
    wedges on. See ASPECT.
    """
    cap = h * aspect
    ws = []
    while sum(ws) < span:
        q = r.random()
        if q < big:
            w = h * r.uniform(1.38, 1.82)
        elif q < big + small:
            w = h * r.uniform(.50, .78)
        else:
            w = h * r.uniform(.90, wide)
        ws.append(min(w * wmul, cap))
    if len(ws) > 1 and sum(ws) - ws[-1] > span * .70 and span / (len(ws) - 1) <= cap:
        ws.pop()
    k = span / sum(ws)
    ws = [w * k for w in ws]
    # the stretch the normalisation just applied can push the longest stone past
    # the cap on its own; hand the excess back to the rest of the course rather
    # than letting one stone eat it
    for _ in range(3):
        over = sum(max(0.0, w - cap) for w in ws)
        if over < 1e-5 or len(ws) < 2:
            break
        room = sum(cap - w for w in ws if w < cap)
        if room < 1e-5:
            break
        f = min(1.0, over / room)
        ws = [min(w, cap) + (f * (cap - w) if w < cap else 0.0) for w in ws]
    # AND NO SLIVERS. "Long stones end in razor-thin wedge slivers" -- the second
    # half of that was not the stone's shape at all, it was that a 45 mm stone
    # got laid next to a 300 mm one in the first place. The narrowest widths in
    # this table come out of the `small` hump and then get multiplied by wmul and
    # by the normalisation, and .085 * .84 * .72 is 51 mm: that is not a packing
    # stone, it is a joint that got counted as one. Anything under the floor is
    # handed to its neighbour, so the course still fills exactly and the smallest
    # stone in it is a stone.
    floor = max(h * .40, .072)
    out = []
    for w in ws:
        if out and w < floor:
            out[-1] += w
        else:
            out.append(w)
    if len(out) > 1 and out[0] < floor:
        out[1] += out[0]
        out.pop(0)
    # ---- LONG AND SHORT WORK AT THE ARRIS (round 13) ------------------------
    # `end_lo` / `end_hi` are +1 if this face TURNS the corner at that end of the
    # course and -1 if it stops at it. The stone that turns the corner is dealt a
    # LONG length and the one that stops at it a SHORT one -- which is what a
    # mason lays at a rubble quoin, and it is the thing that stops the arris
    # reading as a clean vertical edge with two independent facings either side
    # of it. Ownership alternates course by course (see _dress), so the corner
    # comes out as a zip of alternating long and short ends on BOTH faces.
    #   The length is taken from (or given to) the NEXT stone along, so the run
    # still fills its span exactly and neither stone can leave [floor, cap]. If
    # the run is one stone long there is nowhere to take it from and it is left
    # alone -- a single stone spanning a whole course already turns the corner.
    def _end(i, j, want):
        tot = out[i] + out[j]
        tgt = h * (r.uniform(*LONG) if want > 0 else r.uniform(*SHORT))
        out[i] = clamp(tgt, max(floor, tot - cap), min(cap, tot - floor))
        out[j] = tot - out[i]
    if len(out) > 1:
        if end_lo:
            _end(0, 1, end_lo)
        if end_hi:
            _end(len(out) - 1, len(out) - 2, end_hi)
    return out


# --------------------------------------------------------------- the cobble ---
def _cobble(p, axis, sign, const, u_lo, u_hi, v_lo, v_hi, mat, seed,
            relief=.034, tint=.045, shade=1.0, sides=8, at=(0, 0, 0),
            midr=MIDR, dome=DOME, jit=.11, back=BACK, roll=ROLL, seal=False,
            steps=2, infl=None, ee=None, fill=None, arc=ARC, chamf=CHAMF,
            arc_p=ARC_P, rise=None):
    """ONE ROUNDED STONE: a cushion that bulges in TWO STEPS, which is the shape
    util.Part.blob draws and the whole answer to "flat plates with one folded lip".

    Built in the face's own (u, v, depth) frame, three rings deep:

      * OUTLINE -- THE CELL WITH ITS FOUR CORNERS TAKEN ROUND (round 12; the
        note in the body has the arithmetic). Straight along each cell edge --
        which is where the stone beds against its neighbour, so the perpend is a
        continuous recess of the width the course laid out -- and a quarter
        ELLIPSE of radii (f*bu, f*bv) at each corner, where three stones meet and
        there is nowhere to bed. `f` is drawn per corner, one corner in five is a
        single chord and one in five is left nearly square, so no two stones are
        the same shape. It sits `back` behind the face plane, which since round
        12 is IN FRONT of the mortar surface (BACK < MORT_IN), so the section the
        eye reads is the cell itself.
          Every vertex is inside the cell by construction and clamped to it
        afterwards, so two neighbouring cobbles cannot share volume however they
        are domed, leaned, rolled or tilted: no oversize, no tuning. That is the
        rule p.blob could not obey (its ring is scaled 1.03 at the shoulder and
        its jitter is unclamped, so closing the perpends meant growing the stone)
        and it is why this family kept trading stone-ness for overlap.
          IT IS 10-12 VERTICES, and they are all spent on CURVATURE. That
        matters twice over: a cone cap over a 4-gon is two big triangles with a
        fold line between them -- the "one folded lip" of round 5, drawn by the
        topology itself, and exactly what round 11 got back when `infl` clamped
        its ring into the cell rectangle -- while a cone over a 10-gon is ten
        narrow facets that shade as one curve.
      * MID RING -- the outline SCALED to `midr` of itself (a scale, NOT an
        absolute inset: see MIDR -- the inset is what made a long stone a plate
        with wedges on its ends), carrying (1 - `dome`) of the whole climb. It is
        22% of the way in from the outline, so the band between them is a real
        band on a big stone and on a small one alike, and it runs 37-56 deg off
        the face.
      * APEX -- one vertex, off-centre, at the crown, `dome` of the climb above
        the mid ring, so the cap is a 15-27 deg cone of n facets. Band and cap
        differ by 22-29 deg, inside spec.SMOOTH_ANG, so they shade as ONE CURVE:
        a stone with a rounded shoulder, not a plate with a lip. Every mid-ring
        vertex carries its own depth and the crown sits off-centre, so the
        cushion is lopsided rather than a cone of revolution.

    THE CLIMB is `_crown(relief, w, h)` -- clamped to a fraction of sqrt(w*h),
    so the dome is a property of the STONE. On the median stone it is 25% of the
    width, against round 5's measured 8%.

    ROLL. The stone is rotated a little in its own plane. The corner excursion
    that costs is `eps`, and the base ring is pre-shrunk by exactly `eps` before
    rotating, so a rolled stone STILL cannot leave its cell. The angle is
    eps/max(hu, hv), so a near-square stone rolls ~4 deg and a long one ~1 --
    which is the right way round: at a 2.5:1 aspect a degree of roll is
    invisible, and a squarish stone shows it (stone_walls._one, same finding).

    3n tris for an n-gon outline -- 12 uncut, 15 with one corner off, ~16 on
    average -- and NOT ONE of them on the back, which is bedded 12 mm inside an
    opaque mortar body where no view ray reaches it. Round 5 spent n-2 tris a
    stone sealing that back, which on a 2.6 m shaft is 600 triangles of the
    3000-tri budget buried in the lime; the budget is why the stones could not
    be both smaller and rounder. The winding is built right-handed for the
    frame instead (see the flip at the end), so nothing relies on
    recalc_face_normals guessing which way an open shell faces. `seal` puts the
    back on the few stones that turn an arris, where the shell does reach past
    the mortar body.

    Nothing here can grow the footprint: the lean and the dome move depth only,
    the roll is paid for in advance, and the jitter only ever pulls a corner
    inward. `sign` is the outward direction on `axis`; u runs across the face,
    v is Z.
    """
    r = rng(f"ch/cob/{seed}")
    fill = FILL if fill is None else fill
    hu, hv = (u_hi - u_lo) / 2, (v_hi - v_lo) / 2
    if hu < .020 or hv < .016:
        return
    mu, mv = (u_lo + u_hi) / 2, (v_lo + v_hi) / 2
    # ---- the roll, and the shrink that pays for it -------------------------
    # THE ROLL COSTS THE JOINT, so it is a quarter of what it was. eps is the
    # in-plane shrink that pays for rolling the outline without letting it leave
    # the cell, and at 9 mm it put every stone 9 mm inside its cell on all four
    # sides -- 18 mm of the joint between any two neighbours, before the joint
    # itself and before the shoulder. That bought 3.8 deg of roll on a RECTANGLE,
    # where roll is the only thing that stops four parallel sides reading as a
    # grid. The outline is an 8-gon with its own angle and radius jitter now, so
    # roll is a garnish and it can pay 4.5 mm for it.
    # ROUND 9: 1.2 mm, not 4.5. The cell rule is enforced by the CLAMP on every
    # ring vertex below, not by this shrink -- all the shrink buys is that a
    # rolled corner is not the vertex the clamp flattens, and at 4.5 mm it was
    # buying that with 9 mm of every joint on the stack (4.5 a side), which is a
    # quarter of the gap Shanee is looking at. The roll scales with it (see `th`),
    # so a rolled stone now turns about a degree instead of four; the outline is
    # an 8-gon with its own angle and radius jitter, so the roll was a garnish.
    eps = min(.0012, min(hu, hv) * .02)
    th = r.uniform(-1, 1) * radians(roll) * min(1.0, eps / (radians(roll) *
                                                            max(hu, hv)))
    ct, st = cos(th), sin(th)
    bu, bv = hu - eps, hv - eps
    rot2 = lambda u, v: (u * ct - v * st, u * st + v * ct)
    # ---- the climb from the outline to the crown, and the width of the band
    #      between the two rings -- which is what a corner cut is scaled by.
    #      `rise` is the stone's NET projection past the face plane, drawn by the
    #      caller (see _rubble.emit); `back` is how deep the mason bedded it. The
    #      two are independent since round 13 -- a stone can be flat AND proud, or
    #      bold AND sunk -- and that independence is the relief ladder. D is the
    #      full climb from the outline, so a sunk stone keeps its own dome and
    #      simply slides in: the shape does not change, its depth in the wall does.
    D = back + (rise if rise is not None else _crown(relief, 2 * bu, 2 * bv, back))
    # ---- NOTHING GROWS. Round 9 paid for the shoulder's taper by letting the
    #      buried skirt oversail its cell by up to 11 mm a side, on the argument
    #      that two neighbours then share volume only inside an opaque mortar
    #      body. Measured with a footprint test over every stone in the family,
    #      that argument bought 1548 interpenetrating pairs, 395 of them on
    #      SM_Chimney_Stack_2_6m_A alone and 28 mm deep -- two neighbours each
    #      oversailing 17 mm across a 6 mm joint. Burying stones in each other is
    #      not a way to close a joint, whatever is in front of them, and
    #      stone_walls closes the same joint with no overlap at all: it puts the
    #      stone's WIDEST SECTION IN FRONT OF THE MORTAR, so what the eye reads
    #      as the edge of a stone is its cell and nothing else. See BACK -- the
    #      burial is 4 mm now rather than 15, which is what that costs here, and
    #      `sec` below is what pays the rest.

    # ---- the OUTLINE: a jittered superellipse inscribed in the cell.
    #      `e` is the corner sharpness. It runs SQUARE-ISH on purpose: at 1.0 the
    #      ring is an ellipse, which fills only 79% of its cell, and every square
    #      millimetre it gives back goes to the JOINT -- the first cut of this
    #      drew .55-.78 and a tight rubble course came out as pebbles scattered
    #      in lime. At .40-.58 it fills 86-93%, which leaves the joint the width
    #      JOINT says it is, and it still spreads one stone squared-off against
    #      the next water-worn, which is the spread a rubble course shows.
    #      Vertices are jittered in angle AND radius, one of them pulled hard,
    #      and every one is clamped into the cell: a clamped vertex flattens that
    #      side, so most stones carry two or three flats and no two are alike.
    # ROUND 11: .40-.56, and ROUNDER than round 9's .24-.38 rather than squarer,
    # because `sec` pays for the packing instead of the corner does. An n-gon
    # whose vertices sit ON a curve lies INSIDE it everywhere else by the sagitta
    # of its chords -- 1 - cos(pi/n), which is 10% of a half-extent at n = 7 --
    # and that is not roundness, it is the DISCRETISATION of roundness, paid for
    # twice, once by each neighbour. Scaling the ring by sec(pi/n) x `infl` makes
    # the polygon CIRCUMSCRIBE the same superellipse -- identical curve, chords
    # straddling it -- and the per-vertex clamp turns the overshoot near the four
    # axes into the two or three FLATS a bedded rubble stone actually has. Same
    # device, same numbers, as stone_walls._round_outline; the two families draw
    # the same stone at different scales and they should reach it the same way.
    # ROUND 12: THE OUTLINE IS THE CELL WITH ITS CORNERS TAKEN ROUND, and this
    # is a different construction rather than another retune of the same one.
    # Rounds 9-11 all drew a superellipse ring, `sides` vertices spread evenly
    # round it, every vertex clamped into the cell, and fought the
    # packing/roundness trade with `ee` (the corner sharpness) and `infl` (how
    # far past circumscription the ring is scaled). The arithmetic says that
    # fight cannot be won: at sides = 8, ee = .49 and infl = 1.20 the ring is
    # scaled 1.30, so the vertex at 0 deg lands at 1.30 bu and the one at 45 deg
    # at 1.10 bu AND 1.10 bv -- i.e. EVERY vertex clamps, most of them onto the
    # cell's own corners, and _dedupe then collapses the ring to four or five
    # points. The outline was therefore the cell RECTANGLE: measured on the
    # render, 86-90% coverage with no continuous joint anywhere, just a dark
    # triangular chip where two stones' corners failed to meet. That is the
    # "flat-faced rectangular blocks" the lead called out in round 4 arriving
    # again by a different route, and it is also why the cap creased into a
    # paper dart -- a cone over a 4-gon has four facets.
    #
    # So the outline is built flats-first now, exactly as stone_walls builds it
    # (same construction, same numbers, one quarry):
    #   * each corner is a quarter ELLIPSE of radii (f*bu, f*bv) drawn with
    #     `arc` interior points, so it is a real arc and not one 45 deg chamfer;
    #   * `f` is drawn PER CORNER, so one stone comes out nearly round and the
    #     next keeps a squarer shoulder, and one corner in five is left nearly
    #     square (a stone with a broken face);
    #   * between two corners the outline runs dead straight along the cell edge,
    #     hard against the plane its neighbour beds to -- so the perpend is a
    #     CONTINUOUS thin recess of the width the course laid out, which is what
    #     was missing;
    #   * `chamf` cuts one corner in five as a single chord: split, not worn.
    # The area a stone gives back is then exactly (1 - pi/4) f^2 = .2146 f^2 of
    # its cell whatever its aspect, so packing is arithmetic instead of a tuning
    # problem: f = .53 keeps 94% of the cell, f = 1.0 is a full ellipse at 78.5%.
    # Every vertex is inside the cell by construction and clamped to it after, so
    # the cell rule -- the invariant that makes overlap impossible -- is intact.
    k_arc = max(1, int(arc))
    fs = [clamp(r.uniform(*fill) * (1.0 + r.uniform(-jit, jit)), .10, 1.0)
          for _ in range(4)]
    if r.random() < .22:
        fs[r.randrange(4)] *= r.uniform(.16, .42)
    flat = r.randrange(4) if r.random() < chamf else -1
    ring = []
    for i in range(4):
        su = 1.0 if i in (0, 1) else -1.0
        sv = -1.0 if i in (0, 3) else 1.0
        ru_, rv_ = fs[i] * bu, fs[i] * bv
        cu_, cv_ = su * (bu - ru_), sv * (bv - rv_)
        t0 = -pi / 2 + i * (pi / 2)
        # ...and a corner is only ARCED if it wins the draw. THIS IS THE
        # TRIANGLE BUDGET, not a style choice: a cone costs one triangle per
        # outline vertex, an arced corner carries three vertices and a chorded
        # one two, and a 2.6 m shaft carries ~250 stones inside
        # spec.TRI_BUDGET["chimney"] = 3000. At arc_p = .62 the median stone is a
        # 10-gon -- two worn corners and two split ones -- which leaves room for
        # the biggest stones to keep their shoulder ring (BIG_A).
        m_ = 1 if (i == flat or r.random() >= arc_p) else k_arc + 1
        for s in range(m_ + 1):
            a_ = t0 + (pi / 2) * (s / m_)
            g = 1.0
            if 0 < s < m_:
                # only the INTERIOR of an arc is jittered: the two tangent points
                # are where the outline meets the cell edge, and moving one of
                # those is moving the joint.
                a_ += (pi / 2) * r.uniform(-.13, .13) / m_
                g = 1.0 - r.uniform(0.0, jit * .55)
            ring.append((clamp(cu_ + ru_ * cos(a_) * g, -bu, bu),
                         clamp(cv_ + rv_ * sin(a_) * g, -bv, bv)))
    # two vertices that landed on top of each other are a zero-area triangle in
    # the band and a face bmesh refuses outright (which _emit swallows in
    # silence, so the stone would simply be missing a side)
    base = []
    for (uu, vv) in ring:
        if not base or abs(uu - base[-1][0]) + abs(vv - base[-1][1]) > min(bu, bv) * .045:
            base.append((uu, vv))
    while len(base) > 4 and (abs(base[0][0] - base[-1][0])
                             + abs(base[0][1] - base[-1][1])) < min(bu, bv) * .045:
        base.pop()
    n = len(base)
    # ---- the MID RING: the outline SCALED toward its own centre, carrying all
    #      but `dome` of the climb, and it is a SCALE for a reason. Round 5 inset
    #      the ring by an absolute chamfer, which on a 400 mm stone is a 46 mm
    #      strip round a 300 mm plate -- the plate the verifier measured, with
    #      the strip folding into a razor wedge at each end. Scaled, the band is
    #      22% of every half-extent, so the whole face is the cushion: domed hard
    #      across a long stone and gently along it, i.e. a loaf.
    fu = clamp(midr * r.uniform(.955, 1.045), .60, .88)
    fv = clamp(midr * r.uniform(.955, 1.045), .60, .88)
    d1 = D * (1 - dome * r.uniform(.86, 1.14))
    # a lean across the whole stone, plus a per-vertex lump on the ring, so the
    # cushion is lopsided rather than a cone of revolution
    lu, lv = r.uniform(-.13, .13), r.uniform(-.13, .13)
    q = [rot2(u, v) + (r.uniform(-.004, .004),) for (u, v) in base]
    # ...and the lean is FLOORED. It tips the shoulder ring, which is what makes
    # the cushion lopsided instead of a cone of revolution -- but the ring's depth
    # is also what sets where the flank crosses the mortar surface, so a corner
    # leaned down to .70 of d1 has already drawn in half its taper by the time
    # anybody can see it, and that is joint. Measured: raising the lean from .07
    # to .15 unfloored cost four points of coverage on its own.
    mid = [rot2(u * fu, v * fv)
           + (d1 * clamp(1 + lu * u / max(bu, 1e-6) + lv * v / max(bv, 1e-6),
                         .84, 1.22)
              * (1 + r.uniform(-.050, .042)),)
           for (u, v) in base]
    # ...and the crown, off-centre inside the mid ring. The climb is measured
    # from the OUTLINE, which is bedded `back` inside the mortar, so the stone
    # stands (D - back) proud of the face plane -- see _crown, and OVERSAIL for
    # what every dressed course in the family has to clear because of it.
    ru = sum(abs(u) for (u, v) in base) / n * fu
    rv = sum(abs(v) for (u, v) in base) / n * fv
    # THE CROWN IS ONLY JUST OFF CENTRE, and on a cone barely off at all. Pushed
    # hard off centre it throws a ridge from the crown out to one side of the
    # outline -- a bright beak, or a dark chevron on the shaded side -- and a
    # ridge is a fold, which is the one thing this round exists to stop. A cone
    # is worse for it than a cushion, because there the offset lands on the only
    # surface the stone has. The irregularity a stone needs is in its outline and
    # in its lean, not in throwing its crown at a corner.
    ecc = .14 if steps > 1 else .025
    au, av = rot2(r.uniform(-ecc, ecc) * ru, r.uniform(-ecc, ecc) * rv)
    # a cone has no shoulder to carry the last of the climb, so it gets a little
    # less of it: a packer drawn to the full crown comes out as a spike
    apex = (au, av, D if steps > 1 else D * .84)
    # ---- into world space. depth 0 is the base ring, so the outward offset from
    #      the face plane is (depth - back).
    def w3(uu, vv, dd):
        off = sign * (dd - back)
        if axis == 'Y':
            return (mu + uu + at[0], const + off + at[1], mv + vv + at[2])
        return (const + off + at[0], mu + uu + at[1], mv + vv + at[2])

    # `steps` = 1 drops the mid ring and runs the outline straight to the crown:
    # n tris instead of 3n. It is for the packers and the halves of a split cell,
    # where the whole stone is 100 mm across -- at that size a cone IS the shape
    # (a rounded pebble reads off its silhouette and its one slope, not off a
    # 5 mm shoulder), and the triangles it gives back are what pays for the
    # course being finer everywhere. Every facet still faces its own way, so a
    # packer is no more one plane than a boulder is.
    rings = [q, mid] if steps > 1 else [q]
    vs = [w3(*x) for ring in rings for x in ring] + [w3(*apex)]
    A = len(vs) - 1                          # apex index
    F = []
    if seal:
        # THE BACK IS A CONE TO A POINT, NOT A FLAT FACE (round 11). A corner
        # stone is the one place a cobble's shell reaches past the mortar body it
        # is bedded in, so that one has to be closed -- and round 11 put its base
        # ring only 1 mm behind the mortar's own side plane, which made a FLAT
        # back a second opaque face on very nearly that plane: check_zfight found
        # 1666 cm2 of it across the family the moment the burial came down. A
        # point 8 mm further in closes the shell just as well, on n triangles
        # rather than n - 2, and not one facet of it is parallel to anything.
        vs.append(w3(0.0, 0.0, -.008))
        B = len(vs) - 1
        for i in range(n):
            F.append((B, (i + 1) % n, i))
    for k in range(len(rings) - 1):          # the band(s)
        o0, o1 = k * n, (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            F.append((o0 + i, o0 + j, o1 + j, o1 + i))
    o = (len(rings) - 1) * n                 # the cap
    for i in range(n):
        F.append((o + i, o + (i + 1) % n, A))
    # WINDING, and it is not cosmetic. The (u, v, depth) -> world map is a
    # coordinate swap on a Y face and a cyclic rotation on an X face, and `sign`
    # negates the depth axis, so the frame comes out LEFT-handed on exactly half
    # the faces of a square shaft (+Y and -X) -- which built half of every stack
    # inside out. finish() called recalc_face_normals and nobody ever saw it,
    # but an open shell has no volume for that heuristic to read, so a dome with
    # no back is not safe to hand it. Flip the winding here and every face of
    # every stone is built pointing out.
    if (sign > 0) == (axis == 'Y'):
        F = [tuple(reversed(f)) for f in F]
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _rubble(p, axis, sign, const, u_range, v_range, seed, course=.215, fine=.90,
            depth=.034, tint=.045, shade_var=.036, big=.18, split=.18, thru=.11,
            wide=1.42, dark=.02, warm=.30, pale=.13, at=(0, 0, 0), mono=None,
            shade_mul=1.0, rows=None, own_lo=None, own_hi=None,
            quoin=0.0, joint=JOINT, butt=(False, False), wmul=1.0, closer=.16,
            small=.17, bed=.011, sides=8, infl=INFL, ee=(.42, .58), back=BACK,
            fill=None, wander=None, sarc=None, per=None, sink=SINK_MAX):
    """COURSED RUBBLE on ONE rectangular face, laid as _cobble cushions -- the
    chimney's version of the walling in stone_walls, so the two families read as
    one quarry and one mason.

    WHAT BREAKS THE GRID (the lead's "near-uniform courses"):
      * `rows` is the shared course grid (see _rows), heights jittered +-26% and
        tapering as the stack climbs;
      * `wander` -- ROUND 13, and it is the answer to "the bed joints run dead
        straight and level all the way round at a constant course height". Each
        bed LINE steps up and down round the stack (see _wander), a stone takes
        the max of its bed line over its own span and the min of its head line,
        and the result is a course whose height varies along its own length, bed
        lines that visibly STEP at a perpend, and joints that open out and DIE
        where a stone straddles a step. Periodic in the perimeter, so it does all
        that and still closes at every arris;
      * `bed` -- every stone gives a random slice of its cell back to the bed
        joint, top and bottom independently and NEVER outward, so a bed line is
        ragged rather than ruled. This is the cheapest and by far the strongest
        of the grid-breakers, and it costs nothing: what the stone gives up is
        mortar, which is what should be there;
      * widths are three-humped (see _widths) and drawn per course, so vertical
        joints never line up between courses;
      * `thru` stands one stone through TWO courses, `big` lays a long stone,
        `split` drops two stacked stones into a wide cell, `closer` puts a narrow
        closer beside a big one, `quoin` dresses the corner;
      * relief, chamfer, lean, dome and tone all vary per stone, on top of the
        _bedding swell and the _blotch patch field.

    ARRISES, AND THE LONG-AND-SHORT WORK ON THEM. `own_lo` / `own_hi` are
    per-course lists saying whether this face owns the corner at that end of u;
    None means that end is not an arris of a square shaft (a haunch face, a
    breast return) and simply stops flush.
    On every course ONE of the two faces meeting at a corner OWNS it: its end
    stone turns the corner, and the other face stops `cj` short. Ownership walks
    up the stack (see _dress), so the corner is TOOTHED -- which is what a mason
    does, and it means the two faces' stones can never occupy the same volume:
    the owner reaches past the arris plane only in u, and only (BACK + its own
    bedding sink) past it in depth, while the face that does not own it is `cj`
    clear, and cj > BACK + SINK_MAX-on-a-corner-stone.
      ROUND 13 MADE THAT TOOTHING VISIBLE, which is the whole of the lead's
    defect 2. The topology was right and the DRAWING was flush: the return was
    cut to `crown + 6 mm`, i.e. exactly enough to close the corner joint and land
    level with the perpendicular face's own crowns, which is a clean vertical
    arris by construction. Now the face that turns the corner is dealt a LONG end
    stone and the face that stops at it a SHORT one (see _widths), the return is
    drawn rather than derived, and `cj` is jittered per course -- so the corner
    reads as alternating long returns and short ends on both faces, which is what
    "the faces are wallpaper on a box" was the absence of.

    `axis` is the face-normal axis, `sign` which way is outward (+1/-1).
    u runs across the face (X for a Y-face, Y for an X-face); v is Z.
    """
    _nz.seed_set(NOISE_SEED)             # _blotch samples it -- see NOISE_SEED
    r = rng(f"ch/{p.name}/{seed}/{axis}{sign}")
    ph = r.uniform(0, 9)                 # this face's blotch / swell phase
    u0, u1 = u_range
    v0, v1 = v_range
    if u1 - u0 < .07 or v1 - v0 < .05:
        return
    rows = rows if rows is not None else _rows(v0, v1, course,
                                               f"{p.name}/{seed}", fine)
    n_row = len(rows)
    # ---- the bed lines' wander. A face of a square shaft is handed the module's
    #      own set plus the map from its u onto the perimeter, so all four faces
    #      step in the same places and the courses close at every arris. A face
    #      that is nobody's neighbour (a haunch band, a breast return) draws its
    #      own over its own u.
    if wander is None:
        per = max(u1 - u0, .01) + .35     # wider than the face, so it never wraps
        wander = _wander(f"{p.name}/{seed}/{axis}{sign}", rows, per,
                         ends=(True, True))
        sarc = (-u0, 1.0)
    per = per if per else max(u1 - u0, .01)
    s_of = lambda u: sarc[0] + sarc[1] * u
    cur_cj = [CORNER_J]                  # this course's corner joint, for emit()

    def emit(ua, ub, va, vb, mat=None, prom=1.0, wa=False, wb=False,
             j_lo=None, j_hi=None):
        """One stone. `wa`/`wb` turn the arris at the lo/hi end of u; `j_lo` /
        `j_hi` are the bed lines its bed and its head are laid on."""
        # ---- THE BED LINE WANDERS (round 13). The stone takes the MAX of its
        #      bed line over its own span and the MIN of its head line, which is
        #      what makes the wander incapable of driving two stones into each
        #      other: for any pair on one line whose spans overlap at u*,
        #      min <= f(u*) <= max. Everything it costs goes to the joint, which
        #      is where a bed line dies out.
        if j_lo is not None or j_hi is not None:
            sa, sb = s_of(ua), s_of(ub)
            if j_lo is not None:
                va += _wspan(wander[j_lo], sa, sb, per)[1]
            if j_hi is not None:
                vb += _wspan(wander[j_hi], sa, sb, per)[0]
        w, hh = ub - ua, vb - va
        if w < .062 or hh < .050:
            return                      # a sliver is mortar, not a stone
        cu, cv = (ua + ub) / 2, (va + vb) / 2
        t = clamp((cv - v0) / max(v1 - v0, .5))
        b = _blotch(cu, cv, ph)
        if mono:
            m, sd = mono, 1.0 + r.uniform(-shade_var, shade_var)
        elif mat:
            # a NAMED stone (a quoin, the dressed drip course) still pays the
            # pale penalty. A dressed quoin column IS meant to read as pale --
            # it is an ordered feature, not noise -- but on the ashlar stack,
            # where quoin = .90, unpenalised stone_pale put a stack of the
            # brightest thing in the palette up all four arrises: that is the
            # "near-white blocks" of the lead's note wearing a job title.
            m = mat
            sd = (1.0 + b * .05 + r.uniform(-shade_var, shade_var) * .8
                  - (.145 if mat == "stone_pale" else 0.0))
        else:
            m, sd = _tone(r, t, b, dark, warm, pale, shade_var)
        # ---- THE RELIEF LADDER (round 13). Defect 1 of the lead's note: "every
        #      stone sits in ONE plane with a narrow dark groove between; nothing
        #      stands proud, nothing recedes."  The draw was already here and it
        #      was already three things multiplied together -- and none of it
        #      reached the geometry, because _crown's size floor swallowed the
        #      whole span (see RISE_LO for the table). So this now draws TWO
        #      independent things and both of them land:
        #        `rel`  how bold the dome is, three-humped so one stone in six is
        #               laid flat and one in six stands out hard, all of it
        #               riding the smooth _bedding swell so the boldness runs in
        #               PATCHES rather than as confetti;
        #        `sink` how deep the mason bedded the whole stone, correlated
        #               with the first -- the flat stones are also the deep ones
        #               -- so a shy stone recedes as well as flattening, which is
        #               the "let a few sit noticeably back" half of the note. A
        #               flatter dome alone is a flatter stone, not a deeper one.
        #      The stone's shape does not change when it sinks; the whole shell
        #      slides in, so its outline (the section that draws the joint) goes
        #      back with it and the joint opens round it, which is what a
        #      deep-bedded stone looks like.
        q = r.random()
        if q < SET_BACK_P:
            k = r.uniform(*REL_SHY)
        elif q > 1.0 - PROUD_P:
            k = r.uniform(*REL_BOLD)
        else:
            k = r.uniform(*REL_MID)
        rel = depth * k * max(_bedding(cu, cv, ph), .30) ** SWELL_P
        rel *= lerp(.95, 1.10, clamp((w - .17) / .28)) * prom
        # ---- the ragged bed. A FIXED slice of the cell goes back to the joint
        #      and then gets SPLIT unevenly between the head and the bed, rather
        #      than each end drawing its own slice: the bed line wanders by the
        #      whole slice while the joint never opens by more than it. Drawing
        #      the two ends independently (round 4) meant the expected loss was
        #      the slice but the worst case was TWICE it, and 2 x 7.5% of a .265
        #      course is a 40 mm black band -- the ruled horizontal darks the
        #      lead read as "near-uniform courses". Only ever gives ground back
        #      to the joint, so no stone can grow into its neighbour; skipped at
        #      a module seam, where two butted shafts must meet with no gap.
        f = r.random()
        if va > v0 + 1e-6 and vb < v1 - 1e-6:
            k_v = hh * bed * r.uniform(.45, 1.0)
            va += k_v * f
            vb -= k_v * (1 - f)
        elif va > v0 + 1e-6:
            va += hh * bed * r.uniform(.20, .70)
        elif vb < v1 - 1e-6:
            vb -= hh * bed * r.uniform(.20, .70)
        if not (wa or wb):
            k_u = w * .008 * r.uniform(.40, 1.0)
            g = r.random()
            ua += k_u * g
            ub -= k_u * (1 - g)
        elif not wa:
            ua += w * .015 * r.random()
        elif not wb:
            ub -= w * .015 * r.random()
        # ---- HOW DEEP THIS ONE IS BEDDED. Where the stone landed inside its own
        #      size band is `t_rel`; a stone at the top of the band is laid on the
        #      face, one at the bottom is pushed in. Capped at .42 of its own
        #      crown so its shoulder is still in front of the mortar (see
        #      SINK_MAX), and hard-capped on a stone that turns an arris, because
        #      cj > BACK + sink is what keeps the two skins at that corner out of
        #      each other.
        cw, ch_ = ub - ua, vb - va
        b_lo, b_hi = _band(cw, ch_)
        crown = clamp(rel, b_lo, b_hi)
        t_rel = clamp((crown - b_lo) / max(b_hi - b_lo, 1e-6))
        sunk = min(sink * (1 - t_rel) ** 1.4 * r.uniform(.40, 1.15),
                   .09 * (BACK + crown), .006 if (wa or wb) else sink)
        net = max(crown - sunk, .012)
        # the stone that owns an arris turns it by its own projection plus a
        # drawn overrun, so the return covers the `cj` the perpendicular face
        # left and then keeps going -- a LONG stone turning the corner, not a
        # flush one closing a joint. The floor is what closes the corner (the
        # return must always cover cj, however shy the stone) and TURN_MAX is
        # the shaft's declared envelope minus room for p.wobble. It is capped on
        # the stone's OWN WIDTH as well: the first cut of round 13 let a 300 mm
        # through-stone run 86 mm past the arris, and past the arris a cobble is
        # a shell with nothing behind it -- so it came out as a pale flat flap
        # hanging off the corner rather than as a stone turning it.
        #   ...and capped on ASPECT as well, which is the same rule _widths lays
        # the course by: the return is added AFTER the width is drawn, so a
        # 1.7-course stone plus a 66 mm return is a 2.4:1 cell -- and a cell past
        # 2:1 is the one whose cushion comes out as a ridge with a fold down it,
        # which is what the first cut of this drew at the arris. The floor always
        # wins over both caps, because the return has to close the corner.
        t_lo = cur_cj[0] + .010
        t_hi = max(t_lo, min(TURN_MAX, .30 * (ub - ua),
                             ASPECT * (vb - va) - (ub - ua)))
        turn = clamp(net + BACK + .010 + r.uniform(0, .016), t_lo, t_hi)
        if wa:
            ua -= turn
        if wb:
            ub += turn
        # SIDES AND STEPS BY SIZE, and this is where the triangle budget is
        # actually spent. A cone (steps=1) costs `sides` triangles and a two-step
        # cushion costs three times that, so the shoulder goes on the stones the
        # eye reads -- everything above BIG_A, which is a bit under half of them
        # and rather more than half the visible area -- and the packers and the
        # halves of split cells are cones. At 120 mm across, a cone with 8 sides
        # and an off-centre crown IS a pebble; nobody can see a 4 mm shoulder on
        # it, and the triangles it gives back are what pays for the course being
        # finer everywhere. It is also why the verifier's note lands on "the
        # large stones": those are the ones that must be domed, and they are.
        big = (ub - ua) * (vb - va) >= BIG_A
        _cobble(p, axis, sign, const, ua, ub, va, vb, m,
                seed=f"{p.name}/{seed}/{axis}{sign}/{cu:.4f}/{cv:.4f}",
                rise=net, tint=tint, shade=clamp(sd * shade_mul, .70, 1.12),
                at=at, sides=sides, steps=2 if big else 1,
                # a corner stone is the one place a cobble's back reaches past
                # the mortar body it is bedded in, so that one gets a back
                seal=(wa or wb),
                fill=fill, back=back + sunk)

    # THE BITE IS TRIMMED AT THE PIECE'S OWN Z SEAM, NOT LEFT FOR finish() TO CUT.
    # BITE_V exists so a butted course runs right up to the seam with no band of
    # bare mortar (see BITE_V), and where the biting course IS the piece's top or
    # bottom the overshoot used to be sheared off by Part.clamp_to_seams -- which
    # gives the identical mesh, but reports it: 80/57/72/72/18 verts cut at 9-10
    # mm on five of eight pieces, i.e. the family logging a 10 mm deformation on
    # every build for something entirely deliberate. Trimmed here the seam is
    # still flush, the interlock is unchanged, and `clamped` reads 0 so a real
    # clamp -- the kind that flattened 173 dormer vertices onto a seam -- is
    # visible the moment it happens. An INTERNAL bite (the ashlar shaft's upper
    # field biting 10 mm down into its string course) is untouched: it is nowhere
    # near a seam, so the min/max does nothing to it.
    zlim = getattr(p, "seams", None) or {}
    z_lo_lim, z_hi_lim = zlim.get('z', (-1e9, 1e9))
    blocked = []                 # u-runs a through-stone is standing in
    for k, (zb, zt) in enumerate(rows):
        h = zt - zb
        nxt = rows[k + 1] if k + 1 < n_row else None
        v_lo = max(zb - BITE_V, z_lo_lim) if (k == 0 and butt[0]) else zb + joint * .5
        v_hi = min(zt + BITE_V, z_hi_lim) if (k == n_row - 1 and butt[1]) else zt - joint * .5
        # ---- who owns each arris on this course. Both faces meeting at a
        #      corner read the SAME list (built in _dress), so exactly one of
        #      them turns it: never two, which would share the corner volume,
        #      and never neither, which would leave the corner open.
        o_lo = bool(own_lo[k % len(own_lo)]) if own_lo else False
        o_hi = bool(own_hi[k % len(own_hi)]) if own_hi else False
        # ...and the corner joint is drawn per course rather than fixed at
        # CORNER_J: a corner whose every course stops the same 22 mm short is a
        # second ruled vertical line running the height of the stack, right where
        # the first one is.
        cj = CORNER_J * r.uniform(.85, 1.50)
        cur_cj[0] = cj
        lo = u0 if (o_lo or own_lo is None) else u0 + cj
        hi = u1 if (o_hi or own_hi is None) else u1 - cj
        blocked_next = []
        # ---- a dressed quoin on the corner this course owns. Alternating long
        #      and short faces at the corner is the oldest trick in masonry and
        #      it is drawn plainly on ref1's stack.
        if quoin and (o_lo or o_hi) and r.random() < quoin:
            qw = clamp(h * r.uniform(1.20, 1.65), .17, .40)
            if hi - lo - qw > .16:
                # ...but never ON a through-stone from the course below -- see
                # _clear(). The fill honours `blocked`; the quoin is laid before
                # the fill and has to honour it for itself.
                if o_lo and _clear(lo, lo + qw + joint * .5, blocked):
                    emit(lo, lo + qw, v_lo, v_hi, mat="stone_pale", prom=1.10,
                         wa=True, j_lo=k, j_hi=k + 1)
                    lo += qw + joint * .5
                    o_lo = False
                elif o_hi and _clear(hi - qw - joint * .5, hi, blocked):
                    emit(hi - qw, hi, v_lo, v_hi, mat="stone_pale", prom=1.10,
                         wb=True, j_lo=k, j_hi=k + 1)
                    hi -= qw + joint * .5
                    o_hi = False
        # ---- fill what is left of the course, run by run
        for (a0, a1) in _free(lo, hi, blocked):
            if a1 - a0 < .05:
                continue
            # LONG AND SHORT AT THE ARRIS: the end stone of a run that reaches a
            # corner is dealt long if this face turns that corner and short if it
            # stops at it. `own_* is not None` is what says the end IS an arris of
            # a square shaft rather than a haunch band stopping in mid-air.
            at_lo = abs(a0 - lo) < 1e-9 and own_lo is not None
            at_hi = abs(a1 - hi) < 1e-9 and own_hi is not None
            ws = _widths(r, a1 - a0, h, wide, big, wmul, small,
                         end_lo=(1 if o_lo else -1) if at_lo else 0,
                         end_hi=(1 if o_hi else -1) if at_hi else 0)
            # a narrow closer beside the widest stone, the way a course gets
            # made up to length by hand
            if len(ws) > 1 and r.random() < closer:
                i_big = max(range(len(ws)), key=lambda i: ws[i])
                # ...and BOTH halves have to survive as stones. Splitting a
                # 180 mm stone 3:1 leaves a 45 mm razor, which is where half the
                # slivers in the family came from -- see the floor in _widths.
                cut = ws[i_big] * r.uniform(.26, .38)
                fl = max(h * .42, .078)
                if cut >= fl and ws[i_big] - cut >= fl:
                    ws[i_big] -= cut
                    ws.insert(i_big + (1 if r.random() < .5 else 0), cut)
            e = [a0]
            for w in ws:
                e.append(e[-1] + w)
            last = len(ws) - 1
            # every perpend its own width, as stone_walls does: a course whose
            # joints are all one width puts a regular grid back over however
            # irregular the stones are, and the joint is the line the eye follows
            js = [joint * r.uniform(.72, 1.45) for _ in range(len(ws) + 1)]
            for i, w in enumerate(ws):
                # flush at a field edge, half a joint anywhere inside
                fa = (i == 0 and abs(e[0] - lo) < 1e-9)
                fb = (i == last and abs(e[-1] - hi) < 1e-9)
                ua = e[i] + (0.0 if fa else js[i] * .5)
                ub = e[i + 1] - (0.0 if fb else js[i + 1] * .5)
                wa, wb = fa and o_lo, fb and o_hi
                # ---- a stone standing through this course and the next. The one
                #      thing that stops a shared bed grid reading as a grid.
                if (nxt and not (wa or wb) and ub - ua > h * .74
                        and ua - lo > .10 and hi - ub > .10
                        and r.random() < thru):
                    top = min(nxt[1] + BITE_V, z_hi_lim) \
                        if (k + 1 == n_row - 1 and butt[1]) \
                        else nxt[1] - joint * .5
                    emit(ua, ub, v_lo, top, prom=1.06, j_lo=k, j_hi=k + 2)
                    blocked_next.append((e[i], e[i + 1]))
                    continue
                # ---- or two stacked stones in a wide cell. Never on a cell that
                #      owns an arris: that stone has to turn the corner, and two
                #      half stones that both stopped short would leave the corner
                #      column open to the cavity behind.
                # ...and ONLY on a cell square enough that halving it leaves two
                # stones and not two slivers. Round 5 split anything wider than
                # 1.05 courses, so a 2:1 cell became two 4:1 ones -- and 4:1 is
                # the aspect at which the band across a stone stands up at 78 deg
                # and the cushion goes back to being a plate with a lip. Bounded
                # here as well as in _widths, because the halves are drawn from
                # the CELL, not from the width table.
                if (h * 1.05 < ub - ua < h * 1.32 and h > .185 and not (wa or wb)
                        and r.random() < split):
                    mv = lerp(v_lo, v_hi, r.uniform(.40, .60))
                    # only the OUTER end of each half is on a bed line: the split
                    # between them is inside the course and has no line to ride
                    for jl, jh, za, zc in ((k, None, v_lo, mv - joint * .5),
                                           (None, k + 1, mv + joint * .5, v_hi)):
                        jog = r.uniform(0, .012)     # the two are not a stack of
                        emit(ua + jog, ub, za, zc, prom=.96,   # identical twins
                             j_lo=jl, j_hi=jh)
                    continue
                emit(ua, ub, v_lo, v_hi, wa=wa, wb=wb, j_lo=k, j_hi=k + 1)
        blocked = blocked_next


def _dress(p, z0, z1, seed, w=W, rows=None, course=.265, fine=.90, jitter=.26,
           tooth="rand", **kw):
    """Dress all four faces of a square shaft between z0 and z1.

    ONE course grid, FOUR DIFFERENT FACES. The bed lines are shared, because a
    chimney's courses run right round the stack and that is what makes the four
    faces read as one built object; everything laid on them is drawn from the
    face's own rng AND its own parameter jitter, so one face comes out
    wide-stoned with few splits and the next fine and busy. That is the answer to
    the wallpaper: it was never literally one seed for four faces (each already
    had its own), it was that the recipe -- two stones a course, both of them
    squared and shrunk to fit by the old _seat() -- left the seed nothing to
    vary. Face-level parameter jitter is what makes the difference visible from
    across the street rather than only in the joints.

    THE ARRISES. At each of the four corners, exactly one of the two faces
    meeting there turns the corner on any given course, and both faces read the
    same list to decide which -- so the corner is always closed by stone and the
    two skins can never occupy the same volume. `tooth` picks how ownership
    walks up the stack:
      "alt"   strict alternation -- proper long-and-short quoining, for the
              dressed variant, where the corner is meant to read as deliberate;
      "rand"  mostly alternating with the odd run of two or three -- a rubble
              corner, where strict alternation is itself a pattern the eye finds.
    """
    hw = w / 2
    rows = rows if rows is not None else _rows(z0, z1, course,
                                              f"{p.name}/{seed}", fine, jitter)
    n = len(rows)
    own = {}
    for ci, cid in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))):
        if tooth == "alt":
            own[cid] = [(k + ci) % 2 == 0 for k in range(n)]
        else:
            cr = rng(f"ch/tooth/{p.name}/{seed}/{ci}")
            seq, cur = [], cr.random() < .5
            for k in range(n):
                if k and cr.random() < .70:
                    cur = not cur
                seq.append(cur)
            own[cid] = seq
    # (ax, sign, const, corner id at the lo end of u, corner id at the hi end).
    # u is X on a Y-face and Y on an X-face, so the same corner is one face's
    # hi end and the other's lo end -- which is what pairs the lists up.
    # ---- THE BED LINES' WANDER, drawn ONCE for the module and shared by all
    #      four faces as a function of ARC LENGTH ROUND THE SHAFT. `sarc` is that
    #      face's map from its own u onto the circuit, s = s0 + dir * u, laid out
    #      anticlockwise from the (-hw, -hw) corner:
    #          -Y face  s: 0 -> W     +X face  s: W  -> 2W
    #          +Y face  s: 2W -> 3W   -X face  s: 3W -> 4W
    #      Each corner is therefore ONE value of s read by both faces meeting
    #      there, so the courses wander freely and still close exactly at all
    #      four arrises -- which is the whole point of sharing a course grid in
    #      the first place. See _wander.
    per = 4 * w
    wnd = _wander(f"{p.name}/{seed}/{z0:.3f}", rows, per)
    faces = (('Y', -1, -hw, (-1, -1), (1, -1), (hw, 1.0)),
             ('Y', 1, hw, (-1, 1), (1, 1), (2 * w + hw, -1.0)),
             ('X', -1, -hw, (-1, -1), (-1, 1), (3 * w + hw, -1.0)),
             ('X', 1, hw, (1, -1), (1, 1), (w + hw, 1.0)))
    for i, (ax, sg, cst, c_lo, c_hi, sarc) in enumerate(faces):
        # True in `own` means the Y face of that corner owns it
        flip = (ax == 'X')
        o_lo = [b != flip for b in own[c_lo]]
        o_hi = [b != flip for b in own[c_hi]]
        fr = rng(f"ch/face/{p.name}/{seed}/{i}")
        kf = dict(kw)
        kf["split"] = clamp(kw.get("split", .18) * fr.uniform(.55, 1.55), 0, .75)
        kf["thru"] = clamp(kw.get("thru", .20) * fr.uniform(.45, 1.60), 0, .45)
        kf["big"] = clamp(kw.get("big", .18) * fr.uniform(.55, 1.60), 0, .60)
        kf["small"] = clamp(kw.get("small", .17) * fr.uniform(.60, 1.45), 0, .40)
        # relief varies FACE TO FACE as well as stone to stone, so one side of a
        # stack beds shallow and dressed and the next stands rough and proud
        kf["depth"] = kw.get("depth", .034) * fr.uniform(.88, 1.14)
        kf["wmul"] = fr.uniform(.84, 1.20)
        _rubble(p, ax, sg, cst, (-hw, hw), (z0, z1), seed * 10 + i, rows=rows,
                own_lo=o_lo, own_hi=o_hi, wander=wnd, sarc=sarc, per=per, **kf)


def _mort_body(p, key, x0, x1, y0, y1, z0, z1, shade=MORT_SHADE, warm=.22,
               tint=.055):
    """One MORTAR body: an opaque solid whose front and side faces ARE the joint
    planes of the rubble bedded into it.

    This is the "no mortar recess" half of the lead's note, and it is the same
    fix stone_walls.mortar_field made: the joint used to be whatever you could
    see of a near-black core 22 mm behind the stone backs -- an absence, one flat
    value, no colour. A joint has to be a SURFACE, close enough behind the stones
    that light gets into it (here 6 mm behind the face plane, so the rendered
    recess is a stone's own relief plus 6 -- about 40 mm on the mean stone, next
    to stone_walls' 30 mm on a 2 m wall) and light enough to read as lime rather
    than as a hole. Some bodies are mixed warm, which is two batches of lime.

    Every cobble's base ring is bedded BACK behind the face plane, i.e. 10 mm
    INSIDE this body, so no wobble displacement can bring a stone's back and this
    body's front into one plane -- the coplanar pair that started the kit's whole
    z-fighting hunt.
    """
    r = rng(f"ch/mortar/{key}")
    # `stone` at MORT_SHADE, not stone_dark: see the note on MORT_SHADE. A joint
    # rendered at 47% of the face beside it is a hole; at 66% it is lime in
    # shadow, which is the thing the lead could not find.
    m = "stone_warm" if r.random() < warm else "stone"
    sd = (shade * .95 if m == "stone_warm" else shade) * (1.0 + r.uniform(-.11, .11))
    p.plate(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
            (x1 - x0, y1 - y0, z1 - z0), m, tint=tint, shade=sd)


def _mortar(p, z0, z1, w=W, bands=None):
    """The shaft's core, which IS its mortar: a stack of bodies whose four sides
    are the joint plane of the four dressed faces.

    ROUND 9: IT IS ONE BODY PER MODULE AGAIN, and that is a joint-width fix, not
    a simplification. The bands were there so the lime changed batch as the stack
    climbed, and they paid for the z-fight between two overlapping bands by
    alternating their half-width by 6 mm -- so HALF the joint plane on a shaft
    stood 6 mm further back than the other half. That does not matter while the
    stones are bedded 15 mm inside it; it matters completely once the joint is
    drawn by where a stone's shoulder CROSSES this surface (see GROW), because
    the compensation is computed from one burial depth and can only be right for
    one of the two. Measured: on the odd bands the stones' back rings ended up
    0.4 mm BEHIND the mortar surface -- i.e. their open rims were on the point of
    showing -- and the drawn joint ran 30-35% of a stone width there.
    One body: one burial depth (BACK - MORT_IN, 8 mm), the oversail exactly
    right everywhere, no adjacent-band pair to z-fight, and 24-60 triangles back.
    What it costs is the batch-to-batch tone variation, which was worth having
    when the joint was 50 mm wide and is not worth a 6 mm step in the joint plane
    now that the joint is a crease. `bands` is kept in the signature so a caller
    that wants the old behaviour can still ask for it.
    """
    hw = w / 2 - MORT_IN
    # ROUND 11: amp .0003, NOT .0022, AND IT IS A JOINT-WIDTH FIX. _lay shifts a
    # body a few mm off the shaft axis so its four joints come out unequal, which
    # is free hand-laid irregularity while the stones are bedded 8 mm inside it.
    # It is not free once the burial is 2 mm: the shift lands on the -Y face's
    # burial with one sign and the +Y face's with the other, so a 2.2 mm draw
    # made one face of a stack 4 mm deep in lime (the joint drew half again as
    # wide) and the opposite face flush with it (an open rim, one wobble away
    # from showing). Measured: SM_Chimney_Stack_2_6m_C drew 10.2% where stack A
    # drew 6.0 with identical stone rules, and the whole difference was this
    # draw. The unequal-joint irregularity is now where it belongs -- in the
    # outline jitter and the per-perpend joint width, which are per STONE.
    ox, oy = _lay(f"mortar/{p.name}/{z0:.2f}", amp=.0003)
    _mort_body(p, f"{p.name}/{z0:.2f}", ox - hw, ox + hw, oy - hw, oy + hw,
               z0, z1)


def _course_ring(p, z, h, w, proud, mat="stone", tint=.05, bevel=.014, shade=.98):
    """One oversailing dressed course -- drip band, corbel, collar. Laid a few mm
    off the axis (see _lay) so the oversail is unequal side to side, the way a
    hand-cut course sits."""
    ox, oy = _lay(f"ring/{p.name}/{z:.3f}/{w:.2f}")
    return _bx(p, (ox, oy, z + h / 2), (w + 2 * proud, w + 2 * proud, h), mat,
               bevel=bevel, seg=1, tint=tint, shade=shade)


def _drip(p, z0, key, w=W, h0=.055, h1=.078, out0=OVERSAIL - .020,
          out1=OVERSAIL + .028, mat="stone", mat_top=None, shade=1.0,
          weather=.962, rev=.024):
    """A PROJECTING DRIP COURSE: two stepped oversails with a dark reveal under
    the upper nose, and a WEATHERED top so the water runs off it.

    ROUND 13, defect 4 of the lead's note -- "a chimney wants a projecting drip
    course near the top, not a plain slab".  Every oversailing course in the
    family was one `_course_ring`: a single square box with a flat top and a flat
    nose, which is a slab whatever it projects.  What both references draw, and
    what a chimney has to have or the rain runs down the shaft, is a MOULDING --
    a lower course that steps out a little, a dark reveal under the nose of an
    upper course that steps out further, and a weathered (sloped) top on the top
    one.  Three planes and a shadow instead of one plane.

    The ladder is the family's usual one and it is not free to pick: OVERSAIL is
    the proudest a cobble on the shaft below can stand, so `out0` has to clear
    that or the drip reads as a RECESS, and `out1` has to clear `out0`.  On a
    STACK the ceiling is the declared envelope (ENV - W/2 = .100, less p.wobble),
    which is why the stacks pass a tighter pair than the caps do.

    The reveal is proud of the lower course's nose and inside the upper one's, so
    it shows as a dark band under the overhang and shares a plane with neither.
    Returns the z its top lands on.
    """
    _course_ring(p, z0, h0, w, out0, mat, shade=shade * .97)
    _shadow_line(p, z0 + h0 * .72, w + 2 * (out1 - .012), rev)
    ox, oy = _lay(f"drip/{key}", amp=.0040)
    z1 = z0 + h0 - .006
    _bx(p, (ox, oy, z1 + h1 / 2), (w + 2 * out1, w + 2 * out1, h1),
        mat_top or mat, bevel=.016, seg=1, tint=.05, shade=shade,
        taper=weather, taper_axis='XY')
    return z1 + h1


def _shadow_line(p, z, w, h=.022):
    ox, oy = _lay(f"shade/{p.name}/{z:.3f}", amp=.0030)
    p.plate((ox, oy, z), (w, w, h), "stone_dark", tint=.02, shade=.50)


def _flue(p, z, w=.78, depth=.075, sink=.022):
    """Dark throat on top of a shaft, so the chimney is not a solid lump.

    The throat starts `sink` BELOW z, buried in the collar it stands on: sharing
    the collar's top plane instead put two opaque faces in the same plane over
    the whole 0.76m throat (5400 cm2 of z-fighting, the second worst pair in the
    family). Same reason the iron grate straddles the throat's rim instead of
    landing on it.
    """
    ox, oy = _lay(f"flue/{p.name}", amp=.0035)
    _bx(p, (ox, oy, z + (depth - sink) / 2), (w, w, depth + sink), "stone_dark",
        bevel=.012, seg=1, tint=.04, shade=.62)
    gx, gy = _lay(f"grate/{p.name}", amp=.0035)
    p.plate((gx, gy, z + depth - .006), (w - .26, w - .26, .036), "iron", tint=.02)


# ------------------------------------------------------------------- stacks ---
def _stack(name, h, seed, kind):
    """A shaft module. No collar at the top: modules butt into one continuous
    shaft and the cap pieces carry the oversailing detail."""
    p = Part(name, budget="chimney",
             seams=dict(x=(-ENV, ENV), y=(-ENV, ENV), z=(0, h)))
    if kind == "rubble":
        # ref2's shaft: one continuous field of coursed rubble, nothing else.
        # THE COURSE IS BACK DOWN TO .212, AND THAT IS THE LEAD'S NOTE, not a
        # relapse. Round 5 matched stone_walls' .265 exactly on the argument that
        # one course height means one quarry -- and it is the wrong argument,
        # because a course is read against the WIDTH OF THE THING IT IS ON. The
        # lead, with the two closeups side by side: "the chimney's stones read
        # visibly LARGER than the wall's ... it is a narrower element, so the same
        # stone size looks bigger on it." Three stones across a 0.96 m shaft is
        # coarser masonry than six across a 2 m wall, whatever the tape says. At
        # .212 the shaft carries four to five a course, ~0.24 x 0.19 against the
        # wall's ~0.36 x 0.265: finer in absolute size, which is what a chimney
        # wants. The triangles come out of the stones' backs (see _cobble).
        _dress(p, 0, h, seed, course=.200, fine=.90, jitter=.26, depth=.046,
               sides=8, big=.18, split=.12, thru=.20, wide=1.30, quoin=.22,
               closer=.12, small=.11, butt=(True, True))
    elif kind == "ashlar":
        # ref1's flavour: squarer dressed blocks, quoined corners, string course
        mid = h * .47
        # fill (.20, .38), not FILL: this variant is DRESSED stone, so its
        # corners are barely taken off -- a readable arris is right for it where
        # the rubble wants a water-worn cobble. Round 12 moved that dial from
        # `sides` (which no longer draws the outline; see _cobble) to the corner
        # radius, which is where it always belonged. It also packs tighter, which
        # is what dressed blockwork does: 4.3% across, cover 91.4%.
        _dress(p, 0, mid - .086, seed, course=.212, fine=.97, jitter=.13,
               depth=.037, sides=7, fill=(.20, .38),
               big=.10, split=.12, thru=.12, wide=1.12, quoin=.90, closer=.10,
               small=.10, dark=.015, warm=.26, pale=.16, shade_var=.040,
               tint=.040, bed=.016, tooth="alt", butt=(True, False))
        # dark reveal, then a string course that has to OVERSAIL the blockwork.
        # The numbers are a LADDER and they matter: the proudest stone lands at
        # hw + CROWN_MAX (.074), the reveal's nose at hw + .080 and the ring's at
        # hw + OVERSAIL, so the reveal reads as a shadow under a course that
        # really does oversail. Its foot lands 8mm INSIDE the reveal plate rather
        # than on the reveal's top plane: that shared plane was 9450 cm2 of
        # z-fight.
        _shadow_line(p, mid - .086, W + .100, .030)
        # a moulded string course, not a slab: a lower step at the oversail the
        # cobbles below demand, a dark reveal, and a weathered top. The ceiling
        # here is the STACK envelope (ENV - W/2 = 100 mm less p.wobble), not the
        # cap's 240, so the step is 10 mm and the weathering does the rest.
        _drip(p, mid - .078, f"{p.name}/str", h0=.050, h1=.064,
              out0=OVERSAIL, out1=OVERSAIL + .010, mat="stone",
              mat_top="stone_pale", shade=.99, weather=.970, rev=.020)
        # the upper field starts ON the ring's top and its bottom course bites
        # 10mm down into it (butt), so there is no band of bare bed above the
        # string course -- there used to be a 30mm one
        _dress(p, mid + .042, h, seed + 3, course=.200, fine=.97, jitter=.13,
               depth=.035, sides=7, fill=(.20, .38),
               big=.10, split=.12, thru=.12, wide=1.12, quoin=.90, closer=.10,
               small=.10, dark=.015, warm=.24, pale=.18, shade_var=.040,
               tint=.040, bed=.016, tooth="alt", butt=(True, True))
    else:  # "raised": rubble below a corbelled offset, finer stone above it
        mid = h * .54
        _dress(p, 0, mid, seed, course=.222, fine=.95, jitter=.27, depth=.050,
               sides=8, big=.24, split=.12, thru=.18, wide=1.22, quoin=.18,
               closer=.16, small=.20, dark=.035, warm=.34, pale=.10,
               butt=(True, False))
        _shadow_line(p, mid, W + .108)
        # the rubble below stands up to hw + CROWN_MAX proud, so a corbelled
        # offset has to oversail by more than that or it reads as a recess --
        # and since round 13 it is a two-step moulding with a weathered top
        # rather than one box (see _drip)
        _drip(p, mid + .008, f"{p.name}/cor", h0=.048, h1=.062,
              out0=OVERSAIL, out1=OVERSAIL + .010, mat="stone", shade=.97,
              weather=.972, rev=.020)
        _dress(p, mid + .118, h, seed + 5, course=.188, fine=.95, jitter=.20,
               depth=.038, sides=8,
               big=.12, split=.16, thru=.16, wide=1.16, quoin=.28, closer=.14,
               small=.16, warm=.28, pale=.15, dark=.02, shade_var=.050,
               butt=(True, True))
    # .0006, NOT .006, AND THE BURIAL IS WHY. The mortar body below is laid
    # AFTER this call and so is not displaced at all, while every stone's bed
    # ring is -- so the wobble amplitude is the whole error budget between a
    # stone's open rim and the lime it is bedded in, and round 11 spent that
    # burial on the joint (BACK, 10 mm -> 6). At .006 a rim could stand 2 mm
    # PROUD of the mortar and show the inside of its own shell down the joint --
    # measured by raycasting every stack on a 1.5 mm grid and counting hits on
    # back-facing polygons: 394 of them at .0035, 192 at .0018, zero at .0006.
    # (mathutils.noise_vector returns components past 1.0, so the safe
    # burial is about 1.5x the amplitude, not 1.0x -- measured, not assumed.)
    # The stones carry 40-70 mm of dome and their outlines are drawn from an
    # 8-gon with angle and radius jitter, so what .006 of whole-piece noise was
    # buying on top of that was small; what it would cost now is not.
    p.wobble(.0006, freq=2.1)
    # THE MORTAR IS LAID AFTER THE WOBBLE. Unwobbled, the burial is exactly the
    # number BACK says it is; wobbled, a 0.96 m plate's four corners sample a
    # field with two cycles across them and its front face can differ from the
    # local displacement of a 200 mm stone by more than the amplitude itself.
    # What that costs is a dead-flat joint surface instead of a gently wavy one,
    # 2 mm behind a facing whose stones stand 50 mm proud of it: nothing visible.
    _mortar(p, 0, h)
    return p.finish()


def stack_short_a():
    """Short module (1.6m): a stack that only just clears a ridge, or a spacer
    under a tall one."""
    return _stack("SM_Chimney_Stack_1_6m_A", H_SHORT, 11, "rubble")


def stack_tall_a():
    return _stack("SM_Chimney_Stack_2_6m_A", H_TALL, 21, "rubble")


def stack_tall_b():
    return _stack("SM_Chimney_Stack_2_6m_B", H_TALL, 31, "ashlar")


def stack_tall_c():
    return _stack("SM_Chimney_Stack_2_6m_C", H_TALL, 41, "raised")


# --------------------------------------------------------------------- caps ---
def cap_roof():
    """ref2's cap: a dark low-pyramid roof on four iron legs, floating clear of
    the flue so smoke gets out sideways. It overhangs hard -- that little roof is
    most of why the reference chimney reads as fantasy-medieval."""
    p = Part("SM_Chimney_Cap_Roof", budget="chimney",
             seams=dict(x=(-0.72, 0.72), y=(-0.72, 0.72), z=(0, CAP_H)))
    # The oversailing course the cap sits on, dressed so it matches the shaft --
    # and it has to oversail the shaft's proudest cobble, not the shaft's core,
    # or the stones of the module below stand out past the cap that crowns them.
    # ROUND 13: it is a DRIP COURSE, not a collar. This was one 105 mm box with a flat
    # top and a flat nose -- "a chimney wants a projecting drip course near the
    # top, not a plain slab" -- and the cap has 240 mm of declared envelope round
    # the shaft to spend, so there was never a reason for it to be a slab.
    z_col = _drip(p, 0.0, f"{p.name}", h0=.058, h1=.082,
                  out0=OVERSAIL - .018, out1=OVERSAIL + .034, shade=1.00)
    _flue(p, z_col, .76, .060)
    # four iron legs, corner-set, with a spread foot. The SET is nudged off the
    # axis as one (see _lay) -- four legs on a perfect mirror grid put each
    # opposite pair's faces the same distance from the axis, which reads as a
    # coincident pair even though they are 0.75m apart.
    lx, ly = _lay(f"legs/{p.name}", amp=.0045)
    for sx in (-1, 1):
        for sy in (-1, 1):
            # the foot is BEDDED 15mm into the throat's rim: standing it on the
            # rim put its underside in the rim's top plane, four times over
            _bx(p, (sx * .335 + lx, sy * .335 + ly, .184), (.150, .150, .068),
                "iron", bevel=.010, seg=1, tint=.04)
            _bx(p, (sx * .335 + lx, sy * .335 + ly, .350), (.095, .095, .280),
                "iron", bevel=.010, seg=1, tint=.05, taper=.9)
    # thin eave fascia, then a proper low pyramid: dark, like slate or lead
    fx, fy = _lay(f"fascia/{p.name}", amp=.0040)
    _bx(p, (fx, fy, .512), (1.34, 1.34, .052), "iron", bevel=.016, seg=2,
        tint=.05, shade=1.10)
    _bx(p, (fx, fy, .630), (1.30, 1.30, .190), "iron", bevel=.012, seg=1,
        tint=.05, taper=.13, taper_axis='XY', shade=1.22)
    # finial: top at .738, clear of the z=CAP_H seam (it used to overshoot by
    # 16mm and get clamped flat) and 13mm clear of the pyramid apex, so its foot
    # is buried in the pyramid and its head shares no plane with it
    _bx(p, (fx, fy, .713), (.12, .12, .050), "iron", bevel=.010, seg=1, tint=.04,
        shade=1.3)
    p.wobble(.005, freq=2.4)
    return p.finish()


def cap_pots():
    """ref1's cap: two corbelled courses oversailing the shaft, squat clay pots
    bedded in dark flaunching, one banded with iron."""
    p = Part("SM_Chimney_Cap_Pots", budget="chimney",
             seams=dict(x=(-0.64, 0.64), y=(-0.64, 0.64), z=(0, POT_H)))
    # the upper corbel course starts 6mm INSIDE the lower one instead of on its
    # top plane: two 0.96m-square opaque faces in one plane was 9600 cm2 of
    # z-fighting, the worst pair in the family after the breast. _drip keeps
    # that bite.
    # ROUND 13: the two courses are a DRIP MOULDING now (see _drip) -- the upper
    # one steps out 40 mm past the lower instead of 20, and its top is WEATHERED
    # rather than flat, which is what stops ref1's corbelled cap reading as the
    # pale slab it was rendering as.
    _drip(p, 0.0, f"{p.name}", h0=.074, h1=.106,
          out0=OVERSAIL - .014, out1=OVERSAIL + .040, mat="stone",
          mat_top="stone_pale", shade=1.01, weather=.948, rev=.026)
    # flaunching: a dark bedding pad set well inside the corbel
    px, py = _lay(f"flaunch/{p.name}", amp=.0040)
    _bx(p, (px, py, .188), (W - .20, W - .20, .050), "stone_dark", bevel=.014,
        seg=1, tint=.04, shade=.66)
    # Both pots are BEDDED at .150 -- 25mm down inside the corbel course, the way
    # a pot is actually bedded in flaunching. Sitting them at .175 put their base
    # discs exactly on the corbel's top plane, and their rim caps exactly on the
    # underside of the dark mouth ring (770 cm2 + 230 cm2 of z-fighting).
    z_bed = .150
    prof = [(0.00, .00), (.200, .00), (.204, .06), (.186, .13), (.176, .30),
            (.182, .36), (.214, .40), (.196, .445), (.162, .425)]
    p.lathe(prof, "terracotta", at=(-0.195, -0.030, z_bed), sides=10, tint=.07)
    # dark mouth: its foot is buried 18mm down inside the pot's belly, its head
    # stands 12mm clear of the pot's rim cap
    p.cyl((-0.195, -0.030, z_bed + .422), .166, .030, "stone_dark", sides=10,
          tint=.03, shade=.62)
    p.cyl((-0.195, -0.030, z_bed + .155), .192, .036, "iron", sides=10, tint=.04)
    # squat pot, leaning off the vertical like ref1's
    prof2 = [(0.00, .00), (.178, .00), (.180, .05), (.162, .10), (.156, .21),
             (.190, .255), (.172, .295), (.140, .276)]
    p.lathe(prof2, "terracotta", at=(0.225, .080, z_bed), sides=10, tint=.07,
            rot=(6.0, -4.0, 0))
    # this pot LEANS, so its mouth has to follow the tilted axis out to where the
    # rim actually is: 0.271m along a (6, -4) axis lands 19mm -x and 28mm -y of
    # the pot's foot. The old ring ignored that and hung off one side of the rim.
    p.cyl((0.225 - .019, .080 - .0285, z_bed + .271), .146, .030, "stone_dark",
          sides=10, tint=.03, rot=(6.0, -4.0, 0), shade=.62)
    p.wobble(.004, freq=2.6)
    return p.finish()


# --------------------------------------------------------------------- base ---
def base_roof():
    """The HAUNCH where a stack punches through the roof -- the piece that stops a
    chimney reading as a fence post stuck through the shingles, and the only lead
    flashing the kit has.

    THE ROOF IS THE FIELD'S 65 DEG, NOT THE KIT'S AUTHORED 52 (see TANP). A
    chimney is placed unstretched into a roof world that has been stretched in Z,
    so a haunch cut for 52 has an underside 0.74 m too shallow: the wedge stands
    off the shingles, its shoulder lands below the roof surface, and the piece
    was simply never placed -- both assemblers dropped the bare shaft into the
    ridge instead and got a hard horizontal cut line with six loose-looking
    stones lying on the roof below it.

    Both references build it the same way and it is all about width: the shaft
    comes down, meets a cornice that OVERSAILS it on every side, and below that
    the masonry spreads into a battered wedge half again as wide as the shaft at
    its foot, riding 2.65 m of slope down to a toe. Nothing about it is the same
    width as the shaft.

    Z=0 is the down-slope toe ON THE SHINGLE SURFACE (not on the nominal plane --
    see ROOF_SKIN), local +Y is up-slope, the stack axis is (0, 0). The core is
    stepped so its underside stays inside the roof surface everywhere.
    """
    p = Part("SM_Chimney_Base_Roof", budget="chimney",
             seams=dict(x=(-0.96, 0.96), y=(-0.74, 0.62), z=(0, BASE_H)))
    r = rng("ch/base")

    # ---- battered core: stepped up the slope, tapering in as it climbs -------
    # THE STEP COUNT IS DERIVED. At 52 deg nine steps over a 1.82 m shoulder gave
    # 0.203 m treads; the same nine over 65 deg's 2.60 m gives 0.289, and the
    # tread is what decides how far each step's back corner floats clear of the
    # shingles before the step above buries it.
    n = max(6, int(round(Z_SH / .203)))          # 13
    dz = Z_SH / n
    for i in range(n):
        z0, z1 = i * dz, (i + 1) * dz
        y_up = _y_roof(z1)                       # roof surface at the step's top
        if y_up < -BASE_TOE + .06:
            continue
        yf = (_yf(z0) + _yf(z1)) / 2             # raking down-slope face
        hw0, hw1 = _hw(z0), _hw(z1)
        # the 6% overlap between steps runs UPWARD only on the bottom one: at
        # i=0 it used to push the box 0.006 m under Z=0 and finish() sheared it
        # flat, which is the whole of this piece's old clamp report.
        zb0 = z0 - (dz * .03 if i else 0.0)
        zb1 = z1 + dz * .03
        _bx(p, (0, (y_up + yf) / 2, (zb0 + zb1) / 2),
            (2 * hw0, y_up - yf, zb1 - zb0), "stone", bevel=.015, seg=1,
            taper=hw1 / hw0, taper_axis='X', tint=.06,
            shade=.90 + r.uniform(-.04, .04))

    # ---- dressing. The rubble stops 9cm short of the arris on purpose: the
    #      core's own beveled corner then carries one unbroken raking line from
    #      toe to cornice, which is exactly how ref3 draws the wedge. Cobbles
    #      over the whole corner turn that line into a lumpy blur.
    ARR = .092
    # SEVEN bands, not five. The band height IS the course height here (one
    # course per band), so the two numbers are locked together: at .245 courses
    # -- the family's own, so the haunch is the same masonry as the shaft landing
    # on it -- five bands of .365 gave five stones stacked up the whole 1.8 m
    # wedge, the coarsest thing in the family and it sits at eye level on the
    # roof. Seven gives .261, i.e. courses that match the shaft above.
    # ...and EIGHT now the course is .205: the band height and the course height
    # are locked together (one band, two courses on the down-slope face), so a
    # finer course means one more band or the wedge stops matching the shaft
    # landing on it.
    # ...AND THE COUNT IS DERIVED NOW, for the same reason the step count is: the
    # band height is Z_SH/nb, and Z_SH is a function of the pitch. Eight bands
    # over 65 deg's 2.60 m shoulder would be 0.325 m each -- back to the coarsest
    # masonry in the family, at eye level on the roof. 0.228 is the band height
    # eight gave at 52 deg, so hold that and take however many bands it needs.
    nb = max(6, int(round(Z_SH / .228)))         # 11
    for b in range(nb):
        z0, z1 = Z_SH * b / nb, Z_SH * (b + 1) / nb
        zm = (z0 + z1) / 2
        hw = _hw(zm)
        # down-slope face: the hero. The whole trapezoid faces down the roof.
        # Two courses per band (course .21 against a .353 band) -- the wedge used
        # to carry ONE 0.35m course per band, i.e. five stones stacked up the
        # whole haunch, which is the coarsest masonry in the family and it sits
        # at eye level on the roof.
        _rubble(p, 'Y', -1, _yf(zm), (-hw + ARR, hw - ARR), (z0 + .006, z1 - .006),
                61 + b, course=.205, fine=1.0, depth=.052, big=.20,
                split=.20, thru=.12, closer=.20,
                dark=.055 - .080 * b / nb,
                pale=.05 + .096 * b / nb, wide=1.32)
        # the two raking sides: only what stands clear of the shingles
        for sg in (-1, 1):
            u_hi = _y_roof(z0) - .04
            if u_hi - _yf(zm) < .20:
                continue
            _rubble(p, 'X', sg, sg * hw, (_yf(zm) + .05, u_hi), (z0 + .006, z1 - .006),
                    70 + b * 3 + int(sg), course=.205, fine=1.0,
                    depth=.046, big=.16, split=.16, thru=.10, closer=.18,
                    dark=.055 - .080 * b / nb,
                    pale=.05 + .096 * b / nb, wide=1.36)

    # ---- cornice: two oversailing courses. That shadow line, right where the
    #      shaft lands on the wedge, is the hardest mark ref3 draws ------------
    #      The upper course starts 14mm INSIDE the lower one instead of on its
    #      top plane -- that shared 1.22 x 1.09 m plane was 13,250 cm2 of
    #      z-fighting, the whole of this piece's total -- and it now runs all the
    #      way up to BASE_H, which is where a stack module seats. It used to stop
    #      15mm short and leave a slot right round the shaft.
    y0c, y1c = _yf(Z_SH), BASE_UP
    # THE OVERSAIL IS MEASURED, NOT CHOSEN (see OVERSAIL): the wedge's stones
    # stand up to CROWN_MAX proud of a face that already rakes, so a cornice at
    # round 5's .062 was INSIDE the stones it is supposed to oversail -- the
    # "string course reads as a recess" defect, still there and still unmeasured,
    # one band lower down the piece.
    for k, (over, h, sh) in enumerate(((OVERSAIL + .012, .100, .93),
                                       (OVERSAIL + .074, CORN_H - .086, 1.06))):
        zc = Z_SH + (0 if k == 0 else .086)
        ylo, yhi = y0c - over, y1c + over * .5
        cx, _ = _lay(f"corn/{k}", amp=.0045)
        # the top course is WEATHERED (round 13): a cornice with a dead flat top
        # is a slab, and this one is the hardest mark either reference draws on
        # the haunch. It still seats a stack module -- 1.42 m tapered to 1.38
        # against a .96 core.
        _bx(p, (cx, (ylo + yhi) / 2, zc + h / 2),
            (BASE_SW + 2 * over, yhi - ylo, h), "stone", bevel=.018, seg=1,
            tint=.055, shade=sh,
            taper=1.0 if k == 0 else .972, taper_axis='XY')
    _shadow_line(p, Z_SH - .014, BASE_SW - .03, .034)
    # a course of small stones along the front of the drip band, so the cornice
    # is masonry and not a poured slab
    _rubble(p, 'Y', -1, y0c - .150, (-.44, .44), (Z_SH + .104, Z_SH + .226),
            180, course=.114, fine=1.0, depth=.027, big=0, split=0, thru=0,
            closer=.30, wide=1.80, shade_var=.05, dark=.02, pale=.10)

    # ---- lead skirt: flaps lying IN the roof plane, lapped over the shingles
    #      all round the foot. One dark raking line each side plus an apron over
    #      the toe -- that line is what beds the haunch INTO the roof instead of
    #      parking it on top, and it buries the stepped notches of the core.
    #      (A ladder of upright soaker tabs reads as a fire escape; neither
    #      reference has one.)
    #      65 DEG, EVERY TERM. The skirt IS this kit's chimney flashing -- there
    #      is no separate flashing piece -- so cutting it at the authored 52 is
    #      not a cosmetic error: the flaps come out 22.7 deg off the shingles
    #      they are supposed to lie on, which lifts the up-slope end of a 0.88 m
    #      flap 0.34 m clear of the roof and drives its down-slope end the same
    #      distance in. That is the whole reason the assembler's docstring calls
    #      the skirt something to keep "buried in the steeper one".
    smax = (BASE_TOE + BASE_UP) / COS_F      # 2.6502  slope run of the footprint
    def _on_roof(s, lift):
        """A point `s` along the slope from the toe, `lift` clear of the SHINGLE
        SURFACE (which is where Z=0 sits -- see ROOF_SKIN)."""
        return (-BASE_TOE + s * COS_F - lift * SIN_F,
                s * SIN_F + lift * COS_F)
    # THE SKIRT HAS TO SPAN THE SHINGLE BAND, NOT LIE ON A PLANE, AND THIS WAS
    # MEASURED OFF A RENDER, not reasoned. First cut of the 65 deg fix kept the
    # old 40 mm plate at a 0.050 lift; rendered on the inn's east ridge stack the
    # skirt was INVISIBLE -- not one dark pixel either side of the haunch. Why:
    # Z=0 is pinned to the BOTTOM of the shingle band (see ROOF_SKIN) so a toe
    # never floats, which means the real shingle surface runs 0 to SKIN_BAND
    # (0.110 in Z, 0.046 measured perpendicular) ABOVE the piece's model of it,
    # and a 40 mm flap 30 mm up is simply inside the tabs.
    #   So the flap is a SECTION that crosses the whole band: 85 mm thick,
    # centred 52 mm off the model surface. Underside 9 mm above the model, i.e.
    # 30 mm bedded into the proudest course and 9 mm proud of the shallowest --
    # never floating; top 95 mm off the model, i.e. 49-95 mm clear of the
    # shingles, which is a lead soaker you can see. Chunky, and the kit is
    # "chunky readable forms": a lead apron dressed over shingle tabs does stand
    # up off them.
    LIFT, LEAD_T = .052, .085
    for k in range(3):
        s0, s1 = smax * k / 3, smax * (k + 1) / 3
        ym, zm = _on_roof((s0 + s1) / 2, LIFT)
        hw = _hw(min(zm, Z_SH))
        # ONE world-space offset for both flaps of a course, not one each: a
        # mirrored pair of plates has both members the same distance from the
        # axis, which check_zfight reads as a coincident pair (these two are
        # 1.89m apart). Shifting the pair together guarantees 2*amp of daylight
        # between the two planes; shifting them independently only makes the
        # collision unlikely, and it came up anyway. See _lay().
        fx, fy = _lay(f"flap/{k}", amp=.0050)
        for sg in (-1, 1):
            p.plate((sg * (hw + .052) + fx, ym + fy, zm),
                    (.150, (s1 - s0) * .98, LEAD_T),
                    "stone_dark", tint=.04, shade=.56,
                    rot=(PF_DEG, 0, 0))
    # THE APRON HAS TO COVER THE TOE, AND ITS LENGTH IS WHAT DECIDES THAT.
    # It used to be 0.30 long centred 0.170 up the slope, i.e. starting 0.020
    # PAST the toe with the toe's own bottom arris left looking for the shingles.
    # Length 0.340 centred 0.170 puts its down-slope edge EXACTLY on the toe
    # (s = 0) and its lowest vertex at world z = (LIFT - LEAD_T/2) * cos65 =
    # +0.0040, so the seam clamp never sees it. Measured the hard way: at 0.335
    # centred 0.155 the corner lands at -0.0075 and finish() shears six verts
    # flat -- rotating a plate about X tilts its half-THICKNESS into z as well as
    # its half-length, and the first cut of this fix forgot the second term.
    ya, za = _on_roof(.170, LIFT)
    # ...and it stops 20mm short of the raking flaps' inner edge rather than
    # running under them: two lead flaps in the SAME plane of the roof, one lying
    # over the other, is 760 cm2 of z-fighting on the roof surface itself. The
    # flaps' inner edge is at _hw(z of flap 0) + 0.052 - 0.075, so the width is
    # derived from the wedge rather than left at the old literal 1.55, which was
    # measured against a 0.86 toe.
    _, z_f0 = _on_roof(smax / 6, LIFT)
    ap_w = 2 * (_hw(min(z_f0, Z_SH)) + .052 - .075 - .020)
    ax_, _ = _lay("apron", amp=.0050)
    p.plate((ax_, ya, za), (ap_w, .340, LEAD_T), "stone_dark", tint=.04,
            shade=.56, rot=(PF_DEG, 0, 0))
    p.wobble(.0012, freq=2.0)
    return p.finish()


# -------------------------------------------------------------------- breast --
def breast():
    """External chimney breast: a battered stone pier standing against a wall,
    weathered back with stepped shoulders to the stack footprint. Back plane is
    Y=0 (the wall's outer face); it grows outward, -Y.

    THE DARK BACKING IS THREE SOLIDS, NOT NINE STACKED PLATES -- don't put the
    stack back. This was the worst z-fighting piece in the kit (101,000 cm2): it
    carried a full-height core plate PLUS one plate per battered level, and every
    plate butted its neighbour exactly, so each of those eight butt joints put
    two opaque 1.3 m2 faces in one plane -- and being a MORTAR bed, the flicker
    showed through every joint between the stones, which is the one place you
    always see the backing. It is now a plinth bed, ONE tapered body bed (the
    batter is a taper, not a stack of steps) and a collar bed. Each reaches
    ~20mm INSIDE its neighbour and each has its own front and back plane, so no
    two faces are coplanar and every interface is buried between two opaque
    surfaces where no view ray can reach it.
    """
    H = S.H_GROUND
    p = Part("SM_Chimney_Breast_2m", budget="chimney",
             seams=dict(x=(-0.90, 0.90), y=(-1.16, 0.0), z=(0, H)))
    z_pl, z_sh, z_co = 0.34, 2.26, 2.72
    pw, pd = BR_W0 + .10, BR_D0 + .07

    def bed(z0, z1, w0, w1, y_front, y_back, shade=MORT_SHADE, mat="stone"):
        """One mortar bed, written as PLANES rather than centre + size: the
        numbers that must not collide are then the numbers you can read.

        ROUND 9: `y_front` IS A JOINT PLANE, and every caller now puts it
        MORT_IN behind the face plane of the facing it backs -- exactly where
        _mortar puts the stacks'. It used to sit wherever a clearance argument
        left it (the body bed was 42 mm behind the bottom step's face, i.e. 32 mm
        in FRONT of the stones' back rings), which had two consequences the slice
        test found at once: the cobbles' open rims were exposed in the joint, and
        with round 9's oversail their buried skirts overlapped each other where
        anyone could see it -- 23 pairs on this piece. It is also `stone` at
        MORT_SHADE now rather than stone_dark at .62, for the reason in the note
        on MORT_SHADE: a joint at 47% of the face beside it is a hole.

        Laid a few mm off the pier's centreline -- see _lay(). A bed with no
        batter (w1 == w0) has both of its sides exactly the same distance from
        that centreline, which is the 3,621 cm2 the plinth bed was reporting: its
        two sides, 1.50m apart, with nothing coincident between them.
        """
        ox, _ = _lay(f"bed/{z0:.2f}/{z1:.2f}", amp=.0010)
        p.box((ox, (y_front + y_back) / 2, (z0 + z1) / 2),
              (w0, y_back - y_front, z1 - z0), "stone_dark", bevel=0,
              taper=w1 / w0, taper_axis='X', tint=.03, shade=shade)

    # ---- plinth: fatter, darker, wet stone -- same language as the wall plinths.
    #      Its bed runs 20mm past the plinth top, up inside the body's bed.
    bed(0, z_pl + .020, pw - 2 * MORT_IN, pw - 2 * MORT_IN, -pd + MORT_IN,
        -.020)
    # ONE course of big wet blocks, not two of .190. A plinth is the heaviest
    # masonry on the piece and .190 on a 1.6 m pier is a brick course: the whole
    # base read as gravel, and it was also a third of the triangles that put this
    # piece 43% over its budget.
    _rubble(p, 'Y', -1, -pd, (-pw / 2, pw / 2), (0, z_pl), 81, course=.290,
            fine=1.0, depth=.056, big=.26, split=.14, thru=0, closer=.22,
            dark=.12, pale=.05, tint=.065, wide=1.50, shade_mul=.90,
            butt=(True, False))
    for sg in (-1, 1):
        _rubble(p, 'X', sg, sg * pw / 2, (-pd + .05, -.05), (0, z_pl),
                82 + int(sg) * 5, course=.290, fine=1.0, depth=.052, big=.22,
                split=.12, thru=0, closer=.20, dark=.12, pale=.05, tint=.065,
                wide=1.60, shade_mul=.90, butt=(True, False))
    # drip band, straddling the plinth top so it buries the bed's top plane.
    # It stops 25mm short of the wall face: at pd + .02 deep it used to push
    # 20mm PAST Y=0, into the wall, and get sheared off by the seam clamp.
    # ...and it has to stand PAST the plinth's cobbles, or the heaviest course
    # on the piece has a recess for a capping. Written as planes: front at the
    # plinth face plus OVERSAIL, back 25mm short of the wall, and the width the
    # same clearance round the plinth's own returns (which reach pw/2 +
    # CROWN_MAX = .874, inside the piece's .90 seam).
    dx_, _ = _lay("drip", amp=.0045)
    y0d, y1d = -pd - OVERSAIL, -.025
    _bx(p, (dx_, (y0d + y1d) / 2, z_pl - .01),
        (pw + 2 * (CROWN_MAX + .015), y1d - y0d, .080), "stone",
        bevel=.014, seg=1, tint=.05, shade=1.00, taper=.972, taper_axis='XY')
    # ---- battered body: ONE tapered bed behind six dressed courses. The bed
    #      keeps 30mm clear of the rubble planes at the foot and 45mm at the
    #      head, so it never pokes out between the stones and its top face stays
    #      buried inside the first shoulder block.
    # The bed's front plane has to clear the SHALLOWEST course of facing, not the
    # deepest: the pier batters, so the facing's own plane walks back 30mm up the
    # body while this one plane stays put. At -BR_D0 + .014 it landed within a
    # millimetre of the third level's stone backs -- 188 cm2 of coplanar mortar
    # bed against stone, which shows through the joints, which is the one place
    # you always look. .042 puts it 12mm behind even the top level.
    # (the body's beds are laid per STEP inside the loop below -- one plane 42 mm
    #  behind the bottom step's face cannot also be 2 mm behind the top step's,
    #  and it is the joint plane for both)
    # ---- ONE COURSE GRID FOR THE WHOLE BODY, at the family's own course height.
    #      This is the same fix stone_walls made in round 6 and it does three
    #      things at once. (1) The pier is the piece that stands against a stone
    #      WALL, and at .180 it was 1.5 courses to the wall's every one -- a
    #      different mason bonded into the same building. .265 is stone_walls'
    #      COURSE exactly. (2) The batter used to be six levels each generating
    #      its OWN row grid, so the bed lines restarted every 320 mm and the pier
    #      read as six stacked panels. Now the grid is drawn once over the whole
    #      body and the batter steps are laid ON it, four of them, each carrying
    #      two of the shared courses -- so a through-stone can still span a bed
    #      inside a step. (3) It is most of the 1100 triangles this piece had to
    #      give back: 190 stones became 80, each of them bigger and rounder.
    rows = _rows(z_pl, z_sh, .224, f"{p.name}/body", fine=.96, jitter=.22)
    steps = 4
    per = max(1, (len(rows) + steps - 1) // steps)
    for i in range(0, len(rows), per):
        grp = rows[i:i + per]
        zb, zt = grp[0][0], grp[-1][1]
        t0 = clamp((zb - z_pl) / (z_sh - z_pl))
        w0 = lerp(BR_W0, BR_W1 + .26, t0)
        d0 = lerp(BR_D0, BR_D1 + .03, t0)
        # this step's own mortar bed: front MORT_IN behind the step's face
        # plane, sides MORT_IN inside its return planes, and a back plane that
        # steps 8 mm deeper per step so no two beds share one
        bed(zb - .014, zt + .016, w0 - 2 * MORT_IN, w0 - 2 * MORT_IN,
            -d0 + MORT_IN, -.044 - .008 * (i // max(per, 1)))
        _rubble(p, 'Y', -1, -d0, (-w0 / 2, w0 / 2), (zb, zt), 90 + i, rows=grp,
                depth=.049, big=.20, split=.12, thru=.16, closer=.18,
                wide=1.42, pale=.06, dark=.02)
        for sg in (-1, 1):
            _rubble(p, 'X', sg, sg * w0 / 2, (-d0 + .05, -.05), (zb, zt),
                    100 + i * 3 + int(sg), rows=grp, depth=.044, big=.16,
                    split=.10, thru=.12, closer=.16, wide=1.55, wmul=1.10,
                    pale=.06, dark=.02)
    # ---- weathered shoulders stepping in to the flue
    for k in range(3):
        z0, z1 = lerp(z_sh, z_co, k / 3), lerp(z_sh, z_co, (k + 1) / 3)
        t = (k + 1) / 3
        w = lerp(BR_W1 + .26, BR_W1 + .03, t)
        d = lerp(BR_D1 + .03, BR_D1, t)
        cy = lerp(-(BR_D1 + .03) / 2, BR_AXIS, t)
        sx_, _ = _lay(f"shoulder/{k}", amp=.0045)
        _bx(p, (sx_, cy, (z0 + z1) / 2), (w, d, (z1 - z0) * 1.06), "stone",
            bevel=.016, seg=1, tint=.06, shade=.94 + .03 * k)
    # ---- collar: the seat a stack module sits on, on the flue axis. Its bed
    #      starts 20mm down inside the top shoulder block and stops 60mm short of
    #      the top, so the pale capstone buries its top plane instead of sharing
    #      it (that was three coplanar faces at Z=H, 26,000 cm2 of the total).
    bed(z_co - .020, H - .060, BR_W1 - 2 * MORT_IN, BR_W1 - 2 * MORT_IN,
        BR_AXIS - (BR_D1 - .06) / 2 + MORT_IN, -.030)
    _rubble(p, 'Y', -1, BR_AXIS - (BR_D1 - .06) / 2, (-.50, .50), (z_co, H - .085),
            120, course=.186, fine=1.0, depth=.043, big=.10, split=.10,
            thru=0, closer=.20, wide=1.55, pale=.06, dark=.02)
    for sg in (-1, 1):
        _rubble(p, 'X', sg, sg * (BR_W1 - .06) / 2,
                (BR_AXIS - .40, BR_AXIS + .40), (z_co, H - .085), 122 + int(sg),
                course=.186, fine=1.0, depth=.040, big=.10, split=.08, thru=0,
                closer=.18, wide=1.60, wmul=1.10, pale=.06, dark=.02)
    # capstone: 10mm shy of the wall face (it used to run 5mm into it and lose
    # its back edge to the clamp) and matched to the stack footprint it seats
    # ...and it oversails the collar's cobbles on all three exposed sides: they
    # stand (BR_W1 - .06)/2 + CROWN_MAX = .574 out in x and reach -.964 in y.
    kx_, _ = _lay("capstone", amp=.0045)
    y0k, y1k = BR_AXIS - (BR_D1 - .06) / 2 - OVERSAIL, -.010
    # ...and weathered, for the reason in _drip: a flat-topped capstone is a slab.
    _bx(p, (kx_, (y0k + y1k) / 2, H - .042),
        (BR_W1 - .06 + 2 * OVERSAIL, y1k - y0k, .084), "stone_pale",
        bevel=.014, seg=1, tint=.05, shade=1.02, taper=.962, taper_axis='XY')
    p.wobble(.0012, freq=2.0)
    return p.finish()


def build():
    return [stack_short_a(), stack_tall_a(), stack_tall_b(), stack_tall_c(),
            cap_roof(), cap_pots(), base_roof(), breast()]


# --------------------------------------------------------------------- demo ---
def _ctx_shade(p, k):
    """Push a whole context Part darker, so big flat surfaces do not blow out
    under the reference light and steal attention from the chimneys."""
    for f in p.bm.faces:
        for l in f.loops:
            c = l[p.clay]
            l[p.clay] = (c[0] * k, c[1] * k, c[2] * k, 1.0)


def _ctx_slope(length, run_s, seed):
    """One shingled roof slope for the demo shot: built flat climbing +Y, then
    transformed onto the pitch by the caller. Context only -- the roofs family
    owns the real roof pieces."""
    p = Part(f"DEMO_Slope_{seed}")
    rows = max(2, int(run_s / .21))
    # the deck is shingle-coloured on purpose: p.shingles() makes 500 beveled
    # boxes and the util paint bug (see _bx) drops all of their main faces into
    # material slot 0, so slot 0 has to BE the shingle material. Wrapping every
    # shingle in _bx would be the clean fix but costs an O(n^2) face scan.
    p.plate((0, run_s / 2 - .12, -.11), (length, run_s + .34, .20),
            "shingle_moss", tint=.04, shade=.42)
    p.shingles(length, rows, "shingle_moss", mat_alt="moss", row=.21, tab=.26,
               thick=.040, tint=.11, seed=seed, at=(0, -.18, 0))
    # fascia + a hint of rafter ends at the eave
    _bx(p, (0, -.21, -.03), (length, .15, .26), "oak_dark", bevel=.012, seg=1,
        tint=.06, shade=.9)
    _ctx_shade(p, .58)
    return p


def demo():
    """A shot, not a row: the corner of an inn, with the hero stack (base + tall
    + little roof cap) breaking the front slope just below the ridge, a shorter
    potted stack further down the roof, and the breast climbing the gable end on
    the right with a stack of its own."""
    from mathutils import Matrix
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []

    def place(nm, loc, rot=(0, 0, 0)):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = [radians(a) for a in rot]
        out.append(o)
        return o

    # ---------------- context: the corner of a building ---------------------
    # THE DEMO ROOF IS THE FIELD'S 65 DEG. It used to be built at S.PITCH, which
    # made this shot the one place in the project where the haunch looked right --
    # a demo that agrees with the piece and disagrees with every building the kit
    # makes is worse than no demo. `run` is held at the old 2.11 m half-span
    # (a 4.2 m deep building) and the RIDGE is derived from it, rather than the
    # other way round: deriving the run from a fixed 5.60 ridge at 65 deg gives a
    # 2.5 m deep building.
    z_eave = 2.90
    run = 2.11                               # horizontal run of one slope
    z_ridge = z_eave + run * TANP            # 7.425
    run_s = (run ** 2 + (z_ridge - z_eave) ** 2) ** .5
    x0, x1 = -4.7, 2.7                       # gable ends
    cx = (x0 + x1) / 2
    over = 0.50                              # eave overhang past the wall
    wy = run - over                          # front wall plane
    for sg in (-1, 1):
        sl = _ctx_slope(x1 - x0 + 2 * S.VERGE_OVER, run_s, 7 if sg < 0 else 8)
        m = Matrix.Translation((cx, sg * run, z_eave))
        if sg > 0:
            m = m @ Matrix.Rotation(radians(180), 4, 'Z')
        sl.transform(m @ Matrix.Rotation(S.PITCH_F, 4, 'X'))
        out.append(sl.finish())

    ctx = Part("DEMO_Context")
    # ridge cap + the dentil tooth course ref2 runs along every ridge
    _bx(ctx, (cx, 0, z_ridge - .03), (x1 - x0 + .3, .34, .18), "shingle_moss",
        bevel=.016, seg=1, tint=.08)
    ctx.dentil((x0 + .30, x1 - .30), z_ridge + .13, 0.0, "shingle_moss",
               step=.31, size=(.075, .15, .22), tint=.07)
    # walls: stone ground storey, plaster above, on both visible sides
    for sg in (-1, 1):
        _bx(ctx, (cx, sg * wy, S.H_GROUND / 2), (x1 - x0, .34, S.H_GROUND),
            "stone", bevel=.02, tint=.07)
    # the gable-end walls climb to where the roof actually crosses them, and the
    # infill triangle starts there. At 52 deg the single triangle sprang straight
    # off the wall head and fell 0.54 m short of the ridge; at 65 deg the same
    # arithmetic misses by 0.97, which is a hole under the ridge on both ends.
    z_gb = z_ridge - wy * TANP - S.H_GROUND       # roof height above the wall head
    for x in (x0 + .17, x1 - .17):
        _bx(ctx, (x, 0, (S.H_GROUND + z_gb) / 2), (.34, 2 * wy, S.H_GROUND + z_gb),
            "stone", bevel=.02, tint=.07)
        _pr(ctx, [(-wy, 0), (wy, 0), (0, wy * TANP)], .34, "plaster_dim",
            axis='X', at=(x, 0, S.H_GROUND + z_gb), bevel=.02, tint=.05)
    _ctx_shade(ctx, .72)
    out.append(ctx.finish())

    # the SHINGLE SURFACE, not the nominal plane -- what a toe actually lands on.
    # The context slope's tabs are 0.040 thick, so its skin in Z is 0.040/cos65 =
    # 0.095, which is ROOF_SKIN: the same number roofs.py measures out at.
    z_roof = lambda y: z_ridge - TANP * abs(y) + ROOF_SKIN

    # ---------------- hero: base + tall stack + little roof cap -------------
    # THE CONTRACT: axis BASE_UP down-slope of the ridge, so the wedge's back
    # lands on the ridge line and its whole stepped underside is on one slope.
    hx, hy = -0.45, -BASE_UP
    toe = z_roof(hy - BASE_TOE)
    place("SM_Chimney_Base_Roof", (hx, hy, toe))
    place("SM_Chimney_Stack_2_6m_A", (hx, hy, toe + BASE_H))
    place("SM_Chimney_Cap_Roof", (hx, hy, toe + BASE_H + H_TALL))

    # ---------------- second stack: further down the slope, potted ----------
    sx, sy = -3.30, -1.06
    toe2 = z_roof(sy - BASE_TOE)
    place("SM_Chimney_Base_Roof", (sx, sy, toe2))
    place("SM_Chimney_Stack_1_6m_A", (sx, sy, toe2 + BASE_H))
    place("SM_Chimney_Cap_Pots", (sx, sy, toe2 + BASE_H + H_SHORT))

    # ---------------- breast climbing the right-hand gable ------------------
    # rotated +90 about Z, so its back plane lies on the gable's +X wall face
    by = -0.55
    place("SM_Chimney_Breast_2m", (x1, by, 0.0), rot=(0, 0, 90))
    place("SM_Chimney_Stack_2_6m_B", (x1 - BR_AXIS, by, S.H_GROUND))
    place("SM_Chimney_Stack_1_6m_A", (x1 - BR_AXIS, by, S.H_GROUND + H_TALL))
    place("SM_Chimney_Cap_Pots", (x1 - BR_AXIS, by, S.H_GROUND + H_TALL + H_SHORT))

    for nm in src:
        src[nm].location = (0, 40, 0)
    return out
