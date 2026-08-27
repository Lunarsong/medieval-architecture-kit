"""Corners -- the vertical joints where two wall runs meet.

Read off the references:
  * ref1, right of the porch: the corner post is a CHUNKY hand-hewn timber about
    0.32m square (measured against the 1.10m door beside it), standing ~0.08
    proud of the plaster on both faces, mid-brown, heavily chamfered, swelling
    (jowled) at the head where the wall plates lap over it. Nothing else happens
    on a corner bay -- the post IS the corner.
  * ref2, front gable corner: the stone storey turns with blocks BIGGER and only
    slightly paler than the field rubble, alternating long-and-short course by
    course, over a projecting plinth finished with a flat dressed cap. Blocks are
    roughly 1.5:1 -- about 0.45 long by 0.29 tall.
  * ref2 left wing + ref1 left corner: the upper storey JETTIES out over the
    stone. At the corner two chunky sill beams (~0.28 deep) lap over each other,
    a diagonal dragon beam bisects the angle, a knee brace carries it down to the
    wall, and small pale stone corbels break out of the masonry below.

Conventions: every piece is the T x T corner cell of spec.py -- X in [-T,0],
Y in [0,T] -- so the two EXPOSED faces are the y=0 plane and the x=-T plane, and
the arris between them is the outside corner. Relief bulges outward (-X/-Y)
only; x=0 and y=T are the inner faces where the wall runs butt on.

Two pieces cannot fit T x T, and both say so in their declared snap box:
  * SM_Corner_JettyJoint -- a jetty projects spec.JETTY by definition, so its box
    is the cell grown by JETTY outward and its z=0 sits JETTY_BAND below the
    storey line it serves. The cell it grows FROM is the TIMBER one
    (beams.SILL_CELL): it is the corner of a half-timber storey, and
    assemble_inn.py places it on the same rectangle as the sill runs. Built on
    the stone cell -- which it was -- it missed them by T_STONE - T_TIMBER.
  * SM_Corner_ArchBrace / _B / SM_Corner_ArchBrace_Pair -- the arched braces
    that spring off a corner post reach ~1m ALONG each wall plate (ref3), and a
    T x T cell has no wall length in it at all: the post fills the cell in both
    directions. spec.py allows exactly this as "deliberate seam-spanning trim
    which must be a SEPARATE piece", so the braces are their own piece(s).
    SM_Corner_ArchBrace and SM_Corner_ArchBrace_B are ONE brace each and are THE
    components -- two differently hewn sticks, arm 0 and arm 1 of a corner. The
    Pair is those two stamped at the same origin as the post, with a box grown
    +BR_RUN along each wall run. Read the block headed ONE BRACE IS THE
    COMPONENT before placing any of them -- it has the frame, the two placement
    rows (name included), why the second one's rz is 90 rather than a mirror,
    and why the arms may not be the same stick. Nothing else in the family
    crosses a seam.

Head sizes: a T x T corner post can legally mushroom to T + PROUD_MAX = 0.40 and
no further, so HEAD_MAX is 0.39 (1cm kept back for wobble). The references push a
corner head nearer 0.5m; getting the rest of the way needs spec.PROUD_MAX raised.

Chamfers are single-segment on purpose: a 1-segment bevel stays a crisp flat
facet (45 deg > SMOOTH_ANG), a 2-segment one smooths into a fillet and reads as
a bright white outline round every stone under the kit's sky light.

===========================================================================
ROUND 7: THE STONE CORNERS ARE NOW BUILT OUT OF stone_walls
===========================================================================
Shanee: "make the corner/edge/end pieces connect nicer".  A corner is not a
piece, it is an INTERFACE, and these three had invented every number in it:

  quoin course height .293   vs the wall's .265 course grid  -> no bed joint ran
                                round the arris; the quoins were a column of
                                blocks stuck on the end of a wall
  plinth cap top      .360   vs the wall's .585               -> a 225 mm step
  plinth stones       .150 proud, small round cobbles
                             vs the wall's coursed blocks at .032 proud
                                                             -> 120 mm of step,
                                and a masonry that exists nowhere else in the kit
  quoin blocks        .105 proud vs the wall's .010           -> a 95 mm step
  sill string course  absent (variant B had one of its own at 1.86, which the
                             walls do not have at all)        -> the strongest
                                horizontal on the elevation died at the corner
  wall head           2.900 vs 2.905, and a different nose

So the stone corners now import stone_walls and read ALL of it from there:
SW.ROWS_P / ROWS_A / ROWS_B for the bed joints, SW.PLINTH_Z / BAND_Z0 / SILL_Z /
HEAD_Z for the horizontals, SW.SLAB_*_Y for their noses, SW.MORT_Y for the joint
plane, SW.course_run() for SM_Corner_StoneInner's field, and SW.plain_bay() for
the demo's context bays -- because a demo that shows the quoins against an
invented wall cannot answer the only question the demo is for.

Quoins are still BIGGER and squarer than the field stones (one dressed block per
course, wrapping the whole cell, alternating long-and-short) and still stand a
little prouder. They just do it on the wall's own beds.
"""
import bpy
from math import cos, sin, radians, pi
from mathutils import noise as _nz
from kit import spec as S
from kit.util import Part, rng, lerp, clamp
# SM_Corner_JettyJoint terminates a run of SM_Beam_JettySill_2m_*, so it takes
# THE JETTY SILL PROFILE from the family that owns it rather than keeping its
# own copy of the numbers. Read the block at the top of beams.py before touching
# jetty_joint(): a local number here is exactly how the corner came to be a
# different size from the beams it joins.
from kit.pieces import beams as B
# ... and the stone corners take THE WHOLE MASONRY INTERFACE from the family
# whose walls they terminate. Every number below that used to be local -- course
# height, plinth level, projection, joint plane, the string course -- is now read
# from here. See the ROUND 7 note above for what each of them cost.
from kit.pieces import stone_walls as SW
# ... and the arch brace takes THE PLATE IT IS HOUSED IN from the family that
# owns it. timber_walls.Z_HEAD is PINNED (the wall plate is the lintel over
# win_upper), and a head datum invented here instead is exactly how the brace
# came to stop 108 mm short of the plate it claims to land in.
from kit.pieces import timber_walls as TW

FAMILY = "corners"
COLLECTION = "03_Corners_Posts"

TS, TT = S.T_STONE, S.T_TIMBER      # 0.36 stone cell, 0.24 timber cell
HG, HU = S.H_GROUND, S.H_UPPER      # 3.0 / 2.6
J = S.JETTY                         # 0.45 overhang
JETTY_BAND = 0.80                   # height of the jetty transition piece

# ------------------------------------------------- the stone-corner interface -
Q_PROUD = .014        # a quoin's face. The field's biggest blocks land on
                      # SW.FACE = -.010 and its mean face is y = 0, so a quoin
                      # stands 14 mm out of the wall -- proud enough to read as
                      # dressed work, nowhere near the 105 mm step it was.
Q_PROUD_PL = .042     # ditto in the plinth, whose field mean face is -.032
Q_DEEP = .155         # how far a quoin block reaches into the T x T cell, i.e.
                      # how long its return shows on the other elevation
Q_DEEP_PL = .180
Q_MORT = SW.MORT_Y    # the corner's joint plane IS the wall's joint plane
Q_BEV = SW.JOINT * SW.JOINT_BEV     # ... and its arris is cut the same way
Q_BED = .014          # THE BED UNDER (AND OVER) A DRESSED SLAB, and the round-13
                      # z-fight fix. A quoin course is laid inside its canonical
                      # row with HALF a joint at each end, so where a course meets
                      # another course the joint between them is a full SW.JOINT
                      # (10.5 mm) -- but where it meets one of the three dressed
                      # slabs (_plinth_L's cap, _band_L, _head_L) the slab occupies
                      # the row plane itself, so the joint there was half a joint,
                      # 5.25 mm. Against it: +-6.2 mm of per-course bed jitter (dz,
                      # at variant B's rough=0.55) and up to 3.6 mm of tilt sag
                      # across a 385 mm block. The jitter was bigger than the joint
                      # it was jittering inside, so a block could sit straight down
                      # on the slab -- MEASURED at 611 cm2 on SM_Corner_StoneQuoin_B,
                      # the soffit of the first course above the sill band against
                      # the band's top face, 0.466 mm apart, and the whole family's
                      # residual at the 0.5 mm pass. It landed on THAT slab and not
                      # the other five interfaces because the band slab's top comes
                      # out dead flat: it spans the whole cell, so all four of its
                      # top corners sit on an x butt plane where util's wobble fades
                      # to zero, and a dead-flat plane is the one thing a jittered
                      # soffit can be exactly coplanar with.
                      # 14 mm, not 5.25: it is the worst-case excursion (6.2 dz +
                      # 3.6 tilt, and 5.0 of wobble on a return block whose deep end
                      # is off the butt plane) with a millimetre left over. And the
                      # jitter at a slab interface is now SIGNED -- see _quoin_courses
                      # -- so it can only ever open that joint, never close it.
CORE_STEP = .009      # how much the odd core band's BURIED planes step by -- the
                      # step it takes round the skim, and how deep its junction
                      # closers reach. Its own number rather than SW.MORT_STEP or
                      # GAP, because at .006 those planes land on planes the skim
                      # already owns (its faces sit at -SKIM_OFF and
                      # -SKIM_OFF-SKIM_T, i.e. -.006 and -.036); .009 clears both
                      # by more than the wobble amplitude.

# ------------------------------------------------------------- z-fighting ----
# Two opaque coplanar faces that overlap cannot be ordered, so the renderer
# flickers between them; check_zfight.py measures the offending area in cm2 and
# this family was the worst in the kit at 111,700. Every one of those pairs came
# from the same habit: a solid butting ONTO the plane another solid already
# claims -- the skim landing exactly on the core's inner face, a stone's flat
# back landing exactly on the core's outer face, two wall plates sharing an end.
#
# THE RULE, everywhere below: a solid either laps GAP INTO the next one or stops
# GAP SHORT of it, so along any view ray the frontmost surface is unambiguous
# and the only coincidences left are buried inside opaque geometry. Where three
# solids meet one plane, they get three different offsets (SKIM_OFF / SKIM_T /
# CORE_SK below) rather than two of them sharing.
#
# WITH ONE EXCEPTION, added in round 8: the two BUTT planes, x=0 and y=T. Those
# are not surfaces, they are joints between two pieces that are always placed
# together, and check_zfight excludes a piece's own declared snap planes for
# exactly that reason. Solids that have to REACH them do, and the plaster is what
# gets out of the way -- see the round-8 block below.
GAP     = 0.006   # the offset. Under a typical bevel, so the two chamfered
                  # faces do not even touch, let alone share a plane.
SKIM_T  = 0.030   # the plaster skim IS the inner surface, and is this thick

# =========================================================================
# ROUND 12: THE RULE IS OLDER THAN THE PIECES THAT BREAK IT.
# =========================================================================
# check_zfight was corrected this round -- it used to compare two faces' plane
# offsets along their OWN canonical normals, which is meaningless once wobble has
# turned them by a few thousandths and their centres are half a metre apart; it
# now projects each centre onto the other's plane. On the corrected tool this
# family measured 731 cm2 at the 0.5 mm engine pass, UP from 386, and every
# millimetre of it was in the three gallery pieces -- which is to say, in the
# newest code in the file, written after the rule above was already written down.
# Six faults, all of them one of two habits:
#
#   731 cm2  a post footed ON its stone pad instead of GAP into it (both gallery
#            pieces; gallery_stair had already found and fixed its own copy, and
#            that fix is where 386 of the old number went). See GA_PADT.
#   409+322+317+176+176 cm2 (at the 1-2.5 mm passes, and moving between builds)
#            deck boards whose thickness jitter ran BOTH ways about the nominal
#            GA_DK_T that the joist and beam laps are measured from. See GA_DK_V.
#   409 cm2  a beam slid bodily down by GAP to clear its twin's soffit, which
#            landed its TOP on the deck soffit instead. See gallery_corner.
#   149 cm2  a brace sprung exactly ON the soffit of the beam it carries.
#   682 cm2  a collar ring authored at a height that happened to land its top
#            1 mm under the jowl's sole. See FLARE_LAP.
#   229+141 cm2  the stone core stopping GAP SHORT of the head slab, which put
#            its top on the top quoin course's bed joint. See _core.
#    62 cm2  two runs of deck boarding butting face to face at the corner.
#
# Family now measures 0 cm2 at 0.2, 0.5, 1.0 and 2.5 mm (it was 386 / 731 /
# 1735 / 3109). What is left at 5 mm is hand-laid rubble: quoin blocks whose
# +-4 mm bed jitter brings two of them within a hair of each other, which is not
# an authored shared plane and not something a coursed masonry can be rid of.
#
# AND ONE THING WORTH KNOWING ABOUT THE TOOL, measured this round: it buckets
# faces by their normal ROUNDED TO 2 dp, so a pair whose two wobbled normals
# round either side of a 0.005 boundary is never compared at all. That is how
# SM_Corner_GalleryBay_2m's pad pair -- 573 cm2, 0.11 mm apart -- stayed
# invisible to it at every tolerance up to 20 mm while its twin on the corner
# reported 731. Fixing what the tool reports is not the same as fixing the
# piece; both were fixed here, and only one of them was ever on the report.

# =========================================================================
# ROUND 8: THE JUNCTION PLANES.  NOTHING STOPS SHORT OF A BUTT PLANE.
# =========================================================================
# Round 7 got every horizontal and every bed joint to run out of the wall and
# round the arris -- and then left a 30 mm hole where the quoin meets the wall.
# Measured on all three stone corners: a full-height strip of M_plaster_dim,
# +22-30 lum against the masonry, visible FROM OUTSIDE at the quoin/wall
# junction, because EVERY solid stopped short of the butt plane and the only
# thing that reached it was the plaster lining:
#
#     quoin blocks   x = -JOINT/2 = -.018     (a half joint back)
#     the core       x = -CORE_IN = -.024     (GAP inside the skim)
#     cap/band/head  x = -BAND_IN = -.018
#     THE SKIM       x =  0        <-- so this is what you saw, at y = +.040
#
# ... and the wall run starts at x = 0. Same hole on the other elevation at
# y = T, where the three dressed slabs stopped 18 mm short.
#
# So the rule for the two BUTT planes (x = 0 and y = T) is now the opposite of
# the rule for everything else in this file: the masonry REACHES them -- the
# quoin blocks and all three dressed slabs overshoot and are cut dead flat by
# clamp_to_seams, exactly as stone_walls' seam stones are cut flat at a bay
# seam -- and the PLASTER is the thing that keeps clear, held SKIM_OFF off both
# planes and SKIM_END back from both elevations, behind the core's junction
# closers. Two independent belts: the junction is closed by stone, and there is
# no plaster within 86 mm of either elevation to leak through it if it opens.
SKIM_OFF = GAP    # the skim is held this far off BOTH butt planes. It used to
                  # own x=0 and y=T, which is precisely why every solid that has
                  # to reach those planes was written to stop short of it.
SKIM_END = 0.086  # ... and its two ends stop this far in from the two EXPOSED
                  # planes: behind the core's junction closers (which are
                  # SKIM_END - GAP deep), so no ray from outside reaches it.
CORE_SK  = SKIM_OFF + SKIM_T + GAP  # .042 -- where the core steps back to let
                  # the skim through. The core reaches the butt planes either
                  # side of that step; those two tabs ARE the closers, and they
                  # carry the mortar face (Q_MORT) out to the junction so a bed
                  # joint at the corner bottoms out on mortar like every other
                  # joint in the wall.
BUTT_BEV = GAP    # how far past a butt plane a facing must overshoot ON TOP OF
                  # its own chamfer: less than its bevel and clamp_to_seams
                  # leaves a 45-degree facet running the full height of the
                  # junction, which under a low sun is its own pale line.
# BURY_S / BURY_B lived here: how deep a facing stone sank its flat back into the
# core, kept at 18-26mm rather than GAP because wobble() warps a big core face
# out of plane by up to its own amplitude. Both are gone -- a quoin block now
# reaches Q_DEEP (155mm) into the cell, so its back is nowhere near any face.
# The rule they encoded still holds everywhere else in the file.

NECK_W = 0.30                       # EVERY timber corner post is waisted to this
                                    # width below its jowl, because that is the
                                    # plane SM_Corner_ArchBrace_Pair lands on.
PROUD_T = NECK_W - TT               # 0.06 -- how far the neck stands proud of the
                                    # plaster, i.e. the plane the braces lie in
HEAD_MAX = TT + S.PROUD_MAX - .01   # 0.39 -- widest a T x T post head may jowl to
FLARE_LAP = 0.008                   # HOW FAR THE JOWL HANGS BELOW ITS OWN SPRING
                                    # LINE. _flare builds each band .016 taller
                                    # than its slice so consecutive bands lap
                                    # rather than share a plane, and box() grows
                                    # about the centre, so the first band's sole
                                    # is this far BELOW zs. Anything stacked up
                                    # against the underside of the jowl has to
                                    # know that: at zs it would be 8 mm inside
                                    # the flare, and 9 mm below zs it was 1 mm
                                    # off it. See the collar rings.
# ------------------------------------------------- the post-to-post foot -----
# Shanee, round 13: "SM_Corner_TimberPost_A.005 is a timber post on a timber
# post, which is fine, but their design has a concrete or stone slab, which makes
# the connection to the timber post under a bit weird."  Right, and the reason is
# arithmetic: assemble_inn.corners() stacks FOUR storeys -- 0.45 stone, then
# 3.45 / 6.45 / 9.05 all timber -- so the stone pad on _A and _C is correct at
# exactly one of them (the first timber storey, where the post lands on masonry)
# and is a slab of ashlar floating two storeys up at the other two.
#
# WHAT THE FOOT CAN AND CANNOT SHOW. The post's cell is z = 0..H and z = 0 is the
# head of the post below, so a tenon cannot be modelled: it would have to cross
# z = 0 into another piece's volume, which breaks the snap box and would show up
# in check_collisions as two objects interpenetrating. The tenon is therefore
# where a tenon belongs -- inside the wall plate below -- and what this foot
# models is the half of the joint that is ABOVE the joint line and that a level
# artist can actually see:
#   * the SHOULDER, a squared oak band bearing on the plate and lapping FOOT_OUT
#     over its arris, so the joint reads as housed rather than butted;
#   * the SHOE above it, sallied (splayed) so the timber spreads onto its
#     bearing -- widest at the sole, dying back to the shaft's own section;
#   * two PEGS driven through each exposed face of the shoe, which is the only
#     part of a pegged tenon that ever shows from the street;
#   * a CHAMFER STOP where the shaft's arris chamfer dies over the joint.
# Nothing pale, nothing that is not the post's own timber.
FOOT_SH  = 0.030                    # the bearing shoulder: 30 mm of squared oak
                                    # sitting on the plate below. Occupies the
                                    # stone pad's slot in the stack (pad, then
                                    # sole lapping GAP into it, then the shaft
                                    # GAP above it) so the three coincident
                                    # z = 0 faces the pad variant had to design
                                    # away cannot come back here either.
FOOT_OUT = 0.026                    # how far shoulder and shoe oversail the
                                    # shaft at the sole. The stone pad's is
                                    # 0.045 and the plain sole plate's 0.004;
                                    # this sits between them, and w + FOOT_OUT =
                                    # 0.371 leaves 29 mm inside T + PROUD_MAX
                                    # for the shoe's own chamfer and the wobble.
FOOT_SPL = 0.024                    # the sally: how much wider the shoe's sole is
                                    # than its head, over the 0.135 band. 10 deg,
                                    # which is a splay you can read at street
                                    # distance -- the plain sole plate's own 4 mm
                                    # of oversail is not, which is why variant B's
                                    # unpadded foot reads as a butt joint.
FOOT_PEG = 0.44                     # peg height up the shoe band, as a fraction
                                    # of it. The band splays, so the face plane a
                                    # peg head has to sit under moves with height
                                    # and is worked out from this rather than
                                    # guessed -- at the sole it is FOOT_OUT proud
                                    # of the shaft, at the top flush with it.
COL_H    = 0.040                    # collar ring height ...
COL_G    = 0.013                    # ... and the clearance above, below and
                                    # between them. 13 mm is what fits two rings
                                    # into the 120 mm between the bead's terminus
                                    # boss and the jowl's sole with a real gap at
                                    # each of the three joints; it is also more
                                    # than twice the piece's wobble amplitude, so
                                    # no build closes one of them.
BR_RUN = 0.92                       # arched brace: reach along the wall plate
BR_SPRING_Z = 1.68                  # WHERE THE ARCH COMES INTO DAYLIGHT: the height
                                    # its soffit clears BR_SPRING_U, and
                                    # the datum the whole visible arc is measured
                                    # from. It is a solved-for target, not an input
                                    # -- _brace_seat drives `drop` until the soffit
                                    # lands on it -- because the two things that
                                    # decide where the arc becomes visible both
                                    # moved when the ends were seated: the head
                                    # datum came up 110 mm to reach the real plate,
                                    # and the foot now spends ~100 mm of climb
                                    # inside the post before it clears the face.
                                    # Left as a fixed `drop` the visible arch lost
                                    # a third of its height; pinned here it shows
                                    # 0.75 m of daylight arch, 1.674 up to the
                                    # 2.420 soffit, and every brace in a run
                                    # springs off one line whatever it was hewn
                                    # like. The cost is 0.26 m of arc buried in the
                                    # post below it -- that IS the fix: a foot that
                                    # lands is a foot that is inside something.
BR_SPRING_U = TW.W_POST / 2         # 0.080 -- and THAT is the plane it clears, not
                                    # x = 0. The wall run leaving a corner carries
                                    # its own seam half-post over x = 0..0.080 at
                                    # POST_Y (-0.080), 26 mm PROUD of the brace, so
                                    # the arch is behind timber until it passes
                                    # 0.080 whatever happens at x = 0. Aiming the
                                    # springing line at x = 0 instead put 0.2 m of
                                    # arch behind that post and the arcade read a
                                    # storey short.
BR_DROP = 1.10                      # seed for that solve, and the fallback shape
BR_TW = 0.138                       # brace section in the wall plane. WAS 0.175,
                                    # and the section is what sizes BOTH of this
                                    # piece's housings, because a cut taken square
                                    # across a timber is one section wide however
                                    # it is angled. At 0.175 the head's cut face
                                    # was 0.178 tall and the plate it hides in is
                                    # 0.180 (timber_walls.Z_HEAD), and the foot's
                                    # cut face was wider than the 0.160 post
                                    # (W_POST) a wall run actually offers. It was
                                    # also wider than anything around it: the wall
                                    # it lies on frames at W_STUD 0.130 and braces
                                    # at W_BRACE 0.100.
BR_DEEP = 0.058                     # brace thickness through the wall
BR_SPRING = 68.0                    # FOOT tangent, degrees above horizontal, and
                                    # HEAD tangent -- see _arc_curve. A brace's two
BR_LAND = 8.0                       # ends want different angles: the foot leaves
                                    # the post like a brace, the head dies into the
                                    # plate like an arch.
BR_LET_IN = 0.006                   # how far the brace is LET INTO the post's face
                                    # plane. Not zero: flush, the brace's own face
                                    # and the post neck's face are one plane over
                                    # the whole lap, two pieces' wobble then
                                    # interleaves through it, and the joint reads as
                                    # a crack. 6 mm is the kit's own smallest ladder
                                    # step (timber_walls: plate -0.092, bead -0.086)
                                    # and it puts the POST proud of the BRACE, which
                                    # is the right way round for a frame.
BR_FACE = -PROUD_T + BR_LET_IN      # -0.054 -- the brace's outer face plane. It sits
                                    # in timber_walls' ladder 4 mm proud of the studs
                                    # (FY -0.050), 16 mm behind the rails (BY -0.070),
                                    # 26 mm behind a seam post (POST_Y -0.080), 38 mm
                                    # behind the wall plate (PLATE_Y -0.092) and 20 mm
                                    # proud of the plaster crown (PANEL_Y -0.034).
                                    # Every member it is housed in therefore covers
                                    # it, and it still stands clear of the render.
BR_MID_Y = BR_FACE + BR_DEEP / 2    # -0.025 -- the brace's OWN CENTRE PLANE, i.e.
                                    # how far outside the wall face (y=0) the middle
                                    # of the timber lies. The single brace piece is
                                    # symmetric about it, and every placement rule
                                    # below is written in terms of it.
BR_FOOT_BURY = 0.018                # how far INSIDE the post's face plane (x=0) the
                                    # foot's cut face stops. The whole cut face is
                                    # behind it, so the squared end is inside the
                                    # post, not lying over the panel beside it.
BR_PEG_R = 0.016                    # joint peg radius
BR_PEG_OUT = 0.0165                 # ... and how far its head stands out of a face
PLATE_BAND = 0.20                   # head-plate band: plate soffit is at H-this
PLATE_SOF, PLATE_TOP = TW.Z_HEAD    # 2.420 / 2.600 -- THE PLATE THE HEAD IS HOUSED
                                    # IN, read from the family that owns it rather
                                    # than guessed from PLATE_BAND. timber_walls
                                    # PINS Z_HEAD[0]: the wall plate is the lintel
                                    # over win_upper (head 2.40 + 20 mm of core), so
                                    # 2.420 is the soffit an arch brace has to reach.
                                    # The corner POST's own plate soffit is still
                                    # H - PLATE_BAND = 2.400, 20 mm low against it;
                                    # moving that moves the post's plates, dentils
                                    # and jowl, and the post is not this task. Said
                                    # out loud rather than left for the next reader
                                    # to assume 2.400 was measured.
WAIST_Z = 1.15                      # shaft is plumb above this, waisted below


def _seams(T, H, out=(0.0, 0.0)):
    """Corner cell snap box, optionally grown outward (jetty piece only)."""
    return dict(x=(-T - out[0], 0.0), y=(-out[1], T), z=(0.0, H))


def _wob(p, amount=None, **kw):
    """p.wobble() with the noise field PINNED first.

    mathutils.noise is seeded per Blender PROCESS, and Part.wobble displaces by
    noise_vector, so "same code, same mesh" was false for every piece in this
    family: two builds of identical code came out millimetres apart, the clamp
    report flickered on and off between runs, and a rebuild would not reproduce
    the .blend anyone was looking at. Same seed as stone_walls and
    timber_walls -- it is one kit-wide bug whose proper home is util.Part.wobble,
    which a piece module may not edit. Nothing here calls p.wobble() directly."""
    _nz.seed_set(SW.NOISE_SEED)
    p.wobble(SW.WOB if amount is None else amount, **kw)


def _bx(p, x, y, z, mat, **kw):
    """A box written as BOUNDS -- x=(x0,x1), y=(y0,y1), z=(z0,z1). Everything in
    this module that has to line up with (or deliberately clear) another solid
    is written this way: centre-and-size hides which planes two solids share,
    which is how the family collected 111,700 cm2 of z-fighting."""
    p.box(((x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2),
          (x[1] - x[0], y[1] - y[0], z[1] - z[0]), mat, **kw)


def _pz(p, plan, z, mat, **kw):
    """_bx's big brother: a vertical prism written as a PLAN (a list of (x,y),
    CCW) between z=(z0,z1). The core needs a plan rather than a box now that it
    has to reach both butt planes while stepping round the plaster lining, and
    the same reason applies: the shape has to be readable as which planes it
    lands on."""
    p.prism(plan, z[1] - z[0], mat, axis='Z', at=(0, 0, (z[0] + z[1]) / 2), **kw)


def _core(p, T, z_top, mort_x=True, mort_y=True, bands=4):
    """The core of a stone corner cell -- and, on its EXPOSED faces, THE MORTAR.

    Those faces are pulled back to Q_MORT, which is literally stone_walls'
    MORT_Y: the joint plane of the corner and the joint plane of the wall are the
    same plane, so a bed joint runs out of the wall and round the arris at the
    same depth instead of turning into a 10 mm scratch. And it is laid in `bands`
    up the height, at alternating depth and with tones drawn the way
    SW.mortar_field draws them, because one flat value over three metres of
    joint is exactly the dead mortar Shanee asked about.

    AND IT NOW REACHES BOTH BUTT PLANES, which is the round-8 fix: it is no
    longer a rectangle stopping CORE_IN short of x=0 and y=T, it is an eight-sided
    prism that steps round the plaster skim (CORE_SK, which is the skim's own
    thickness plus a GAP either side) and runs out to the butt plane on either
    side of that step. Those two 50 mm tabs are what closes the junction: they
    carry the mortar face at Q_MORT all the way to x=0 and to y=T, so the bed
    joint between two quoin blocks at the corner bottoms out on the same mortar
    as every other joint in the wall instead of showing daylight and, behind it,
    the plaster lining -- which is exactly the pale full-height line that was
    measured on all three stone corners.

    The step keeps the old promise as well: the core still shares no plane with
    the skim (it stops GAP outside it, and the skim in turn is held SKIM_OFF off
    the butt planes), and it is still nowhere near the wall's visible interior
    surface. `mort_x` / `mort_y` say which faces are actually exposed: on the
    re-entrant corner the x = -T plane is a BUTT plane (the wing's facade carries
    on through it), so the core has to reach it.

    `z_top` LAPS GAP UP INTO the slab that covers the cell, it does not stop GAP
    short of it. Stopped short -- at SW.HEAD_Z - GAP, which is what both callers
    passed -- the core's top face landed on SW.HEAD_Z - JOINT/2, which is where
    the top quoin course's own top face is: the same bed joint under the same
    head slab. Measured 229 + 141 cm2 of stone-on-stone on
    SM_Corner_StoneQuoin_A, in a 6 mm slot nobody can see, which is exactly the
    kind of pair an engine's coarse depth buffer finds anyway. Lapped up into
    the head slab -- which covers the cell in plan on every one of these pieces,
    nose included -- the core's top face is buried in opaque stone and there is
    no plane left to share."""
    x0b = -T + (Q_MORT if mort_x else 0.0)
    y0b = Q_MORT if mort_y else 0.0
    r = rng(f"{p.name}/mortar")
    for i in range(bands):
        za = z_top * i / bands - (GAP if i else 0.0)
        zb = z_top * (i + 1) / bands
        # neighbouring bands share NO side plane -- the offset is applied to all
        # of them, not just the two exposed ones. Applied to the exposed
        # pair only, the GAP of z-overlap between two bands left ~18 cm2 of
        # coincident face on each INNER plane instead.
        d = SW.MORT_STEP if i % 2 else 0.0      # the EXPOSED pair
        e = CORE_STEP if i % 2 else 0.0          # ... and the buried ones
        warm = r.random() < .17
        m = "stone_warm" if warm else "stone_dark"
        sd = (.52 if warm else SW.MORT_SHADE) * (1.0 + r.uniform(-.20, .20))
        x0, y0 = x0b + d, y0b + d
        # the step round the skim moves OUT of it on the odd bands and the tabs
        # get shallower, so no two bands share a buried plane either
        sk, en = CORE_SK + e, SKIM_END - GAP - e
        _pz(p, [(x0, y0), (0.0, y0), (0.0, en), (-sk, en), (-sk, T - sk),
                (-T + en, T - sk), (-T + en, T), (x0, T)], (za, zb), m,
            bevel=0, tint=.07, shade=sd)


def _skim(p, T, H):
    """Plaster lining the two INNER faces so the butt faces read as an interior
    surface instead of a sawn-off block.

    ONE L-shaped solid, not two crossed plates: two plates lapping at the inner
    arris both put a face on y=T and fought over the lap.

    IT IS THE ONE THING IN THE CELL THAT KEEPS OFF THE BUTT PLANES. Those planes
    are covered by the end of a wall run and are never seen once the kit is
    snapped together, whereas the plaster leaking round the masonry that has to
    reach them was visible from the street on every stone corner. So it sits
    SKIM_OFF back in a rebate (invisible: 6 mm), and both ends stop SKIM_END in
    from the two EXPOSED elevations, well behind the core's junction closers and
    well behind the deepest quoin block (Q_DEEP_PL, 180 mm)."""
    # ... and it keeps off the CORE'S SOLE the same way. Both were authored to
    # start at z = GAP, i.e. on one plane, and the only thing separating them was
    # wobble: on SM_Corner_StoneQuoin_A the core's sole happened to land at
    # 0.0057 and cleared, on _B it landed at 0.00602 against the skim's 0.00600
    # and check_zfight measured 23 cm2 of M_plaster_dim fighting M_stone -- the
    # family's last coincident pair, and one that would move from piece to piece
    # with the noise. So the skim now starts at 3*GAP. Same rule as everywhere
    # else here: where two solids want one plane, the plaster is the one that
    # moves, and it moves by more than the wobble amplitude.
    o, e, s = SKIM_OFF, SKIM_END, SKIM_T
    p.prism([(-o, e), (-o, T - o), (-T + e, T - o), (-T + e, T - o - s),
             (-o - s, T - o - s), (-o - s, e)], H - 4 * GAP, "plaster_dim",
            axis='Z', at=(0, 0, H / 2 + GAP), bevel=0, tint=.04)


# ============================================================== timber post ==
def _pegs(p, at, n=2, axis='Y', r=0.020, spread=0.13, seed=0, length=0.045):
    """Oak dowel pegs -- the joint marks that make framing read as framing.

    `length` is the dowel along its own axis, centred on `at`. The default 0.045
    is a peg tucked under one face; pass the full THICKNESS of the timber plus
    two heads to drive it right THROUGH, which is what a real pegged tenon is --
    and what SM_Corner_ArchBrace needs, because a peg that only shows on one
    face is not symmetric about the timber's centre plane and so does not
    survive the 90 degree rotation that turns one brace into the other half of
    a corner pair. See THE FRAME, above the brace section."""
    rr = rng(f"{p.name}/peg/{seed}")
    for i in range(n):
        o = (i - (n - 1) / 2) * spread
        c = (at[0] + (o if axis == 'Y' else 0), at[1] + (0 if axis == 'Y' else o),
             at[2] + rr.uniform(-.012, .012))
        p.cyl(c, r, length, "oak_dark", sides=6, axis=axis, cap=True, tint=.06,
              shade=.80 + rr.uniform(0, .10))


def _wobble_pin_butts(p, T, amount, freq=1.7, full=False):
    """wobble(), then put every vertex that was AUTHORED on a BUTT plane back
    onto it.

    A corner cell butts against a wall run on x=0 and y=T. util.wobble() fades
    on whole axes (default "xz"), so x=0 comes out dead flat but y=T comes out
    displaced by up to `amount`; passing axes="xyz" instead would fade y=0 and
    x=-T as well -- and those two are the EXPOSED faces of a corner, which is
    exactly where the hand-hewn irregularity has to live. So wobble everything,
    then re-pin the butt planes. Only sub-millimetre on this piece, but y=T is
    where a 340mm-deep sill section lands, and a section that has been made
    identical to the micron should arrive on a flat plane.

    `full` restores those vertices COMPLETELY, not just their plane coordinate.
    Pinning x alone still let the butt vertices ride up and down in z by
    `amount`, and where the thing arriving is a 367mm sill section whose own
    wobble is faded to exactly zero at its ends (util fades on the axes a run
    piece tiles on), 5mm of z on the corner's cut face is a step the eye reads
    as a line at the joint. Only SM_Corner_JettyJoint asks for it: on the posts
    and quoins the in-plane wander at a butt plane is wanted, because the wall
    they meet is rubble."""
    on_x = [v for v in p.bm.verts if abs(v.co.x) < 1e-6]
    on_y = [v for v in p.bm.verts if abs(v.co.y - T) < 1e-6]
    was = {v: v.co.copy() for v in (on_x + on_y)} if full else {}
    _nz.seed_set(SW.NOISE_SEED)
    p.wobble(amount, freq=freq)
    for v in on_x:
        v.co.x = 0.0
    for v in on_y:
        v.co.y = T
    for v, co in was.items():
        v.co = co


def _teeth_y(p, v_range, x, z, mat, step=0.112, size=(0.075, 0.05, 0.05), seed=0):
    """dentil() only runs along X; this is the same tooth course running along Y."""
    r = rng(f"{p.name}/teethY/{seed}")
    v0, v1 = v_range
    n = max(1, int(round((v1 - v0) / step)))
    for i in range(n):
        cy = lerp(v0, v1, (i + 0.5) / n)
        p.box((x, cy, z), size, mat, bevel=.007, seg=1, tint=.05,
              shade=.94 + r.uniform(-.07, .07))


def _flare(p, T, z0, z1, w0, w1, mat, n=4, k=2.1, bevel=.011, shade=.94):
    """THE JOWL. A stack of tapered boxes whose two OUTER faces sweep from w0 up
    to w1 along the curve w = w0 + dw*s**k, while the two INNER faces stay planted
    on x=0 and y=T (the planes the wall runs butt against -- they may not move).
    k>1 hollows the swell so the head MUSHROOMS out at the top the way a hewn
    jowl post does in ref3, instead of splaying evenly like a lamp base.

    skew is what plants the inner faces: box() scales the +Z face about the box
    centre, so shifting it back by (wb-wt)/2 on both axes pins x=0 and y=T.
    """
    for i in range(n):
        s0, s1 = i / n, (i + 1) / n
        wb = w0 + (w1 - w0) * s0 ** k
        wt = w0 + (w1 - w0) * s1 ** k
        zb, ze = lerp(z0, z1, s0), lerp(z0, z1, s1)
        kk = (wb - wt) / 2
        p.box((-wb / 2, T - wb / 2, (zb + ze) / 2), (wb, wb, ze - zb + .016),
              mat, bevel=bevel, seg=1, tint=.05, taper=wt / wb, taper_axis='XY',
              skew=(kk, kk), shade=shade + .035 * i)


def timber_post(name, w=0.345, neck=NECK_W, head=HEAD_MAX, jz=0.48, jn=4, jk=2.4,
                bead=0.0, teeth=True, straps=0, pad=True, collar=0, foot="pad",
                seed=1):
    """Half-timber storey corner post. Any post wide enough to be a corner post
    is wider than a 0.24 wall, so it fills the whole cell and stands proud on
    both faces -- which is exactly what ref1 shows.

    The head JOWLS, hard. The shaft is waisted from `w` at the sole to `neck` by
    WAIST_Z and runs plumb from there, then swells on a curve over `jz` up to
    `head` -- the widest a T x T corner cell can legally get, T + PROUD_MAX. That
    is 0.045 of flare on EACH exposed face plus a 0.018 cap lip on top of it, off
    a 0.30 neck, where the old post managed 0.02 off a 0.32 shaft. The head is
    1.30x the neck instead of 1.13x, so the corner now reads as a jowled post
    carrying two lapped wall plates rather than as a slightly fat stud.

    Above WAIST_Z the shaft is deliberately plumb at exactly NECK_W: that is the
    plane SM_Corner_ArchBrace_Pair springs its braces off, so every post variant
    has to present the same face there. The braces are let BR_LET_IN (6 mm) into
    it rather than lying on it, so this face stays the proud one at the joint and
    the two pieces never share a plane; and their feet are buried inside this
    shaft, which is 0.30 wide against a 0.133 cut face (arm A's section; arm B's
    is 0.130 -- see arch_brace_single, where 0.116 was quoted and measured wrong).

    outward="xy": a corner post is proud on BOTH exposed faces. Without that
    declaration util clamped every vertex past x=-T flat onto the cell plane, so
    the post stood 0.105 proud on its y face and dead flush on its x face -- a
    corner that visibly changed size depending which wall you looked along, and
    ~1200 cm2 of the family's z-fighting, since the whole crushed jowl, both
    plates and the sole plate ended up coplanar on x=-T.
    """
    T, H = TT, HU
    p = Part(name, budget="corner", seams=_seams(T, H), outward="xy")
    tenon = foot == "tenon"           # post-to-post: no pad, a housed foot
    pad = pad and not tenon
    sh = 0.135                        # sole plate band
    zt = H - PLATE_BAND               # plate soffit == top of the post proper
    zs = zt - jz                      # where the jowl springs off the shaft
    pd = head - T                     # how far the plates stand proud
    wat = lambda z: lerp(w, neck, clamp(z / WAIST_Z))    # shaft width at height z
    # The base is a STACK, not three solids all starting on z=0: pad, then sole
    # plate lapping GAP into it, then the shaft footing GAP above the pad. Three
    # coincident bottom faces on z=0 was this piece's worst pair (~1900 cm2).
    # The housed foot rides the SAME stack -- the shoulder stands in the pad's
    # slot -- so it inherits that separation instead of re-deriving it.
    z_pad = FOOT_SH if tenon else (.10 if pad else 0.0)
    z_sole = z_pad - (GAP if (pad or tenon) else 0.0)

    # ---- shaft: waisted to the neck, then plumb up to the jowl ------------
    kk = (w - neck) / 2
    _bx(p, (-w, 0.0), (T - w, T), (z_pad + GAP, WAIST_Z + .020), "oak_dark",
        bevel=.024, seg=1, tint=.05, taper=neck / w, taper_axis='XY',
        skew=(kk, kk), shade=.84)
    _bx(p, (-neck, 0.0), (T - neck, T), (WAIST_Z - .012, zs + .01), "oak_dark",
        bevel=.022, seg=1, tint=.05, shade=.88)
    # ---- the jowl, and the cap piece the plates land on -------------------
    _flare(p, T, zs, zt - .046, neck, head - .022, "oak_dark", n=jn, k=jk)
    _bx(p, (-head, 0.0), (T - head, T), (zt - .046, zt + GAP), "oak_dark",
        bevel=.012, seg=1, tint=.05, shade=1.06)   # laps GAP up into the plate
    # chamfer stops: the little carved blocks that end a post's chamfer. They
    # stand GAP proud of the shaft face rather than dead flush with it -- flush,
    # the block's face and the shaft's face were one plane wherever the shaft
    # runs plumb, and fought over the whole block.
    # The housed foot gets a THIRD pair, low down: the arris chamfer has to die
    # over the joint or the shaft's 24 mm chamfer runs straight into the shoe and
    # the foot reads as a butt again. 0.235 clears the shoe's top (0.159) by 76 mm.
    for z in ((0.235,) if tenon else ()) + (0.55, zs - 0.24):
        ww = wat(z)
        _bx(p, (-ww * .84, -ww * .16), (T - ww - GAP, T - ww + .048),
            (z - .0425, z + .0425), "oak_dark", bevel=.010, seg=1, tint=.05,
            shade=.74)
        _bx(p, (-ww - GAP, -ww + .048), (T - ww * .84, T - ww * .16),
            (z - .0425, z + .0425), "oak_dark", bevel=.010, seg=1, tint=.05,
            shade=.71)
    # ---- rolled bead on the arris (variant C) -----------------------------
    if bead > 0:
        z0b, z1b = WAIST_Z + .10, zs - .16
        p.cyl((-neck + bead * .52, T - neck + bead * .52, (z0b + z1b) / 2), bead,
              z1b - z0b, "oak_dark", sides=8, axis='Z', tint=.05, shade=1.0)
        for z in (z0b, z1b):
            p.cyl((-neck + bead * .52, T - neck + bead * .52, z), bead * 1.45,
                  .065, "oak_dark", sides=8, axis='Z', tint=.05, shade=.86)
    # ---- collar rings at the jowl spring (variant C) ----------------------
    # Rings and straps WRAP the shaft, so they would otherwise put a second face
    # on x=0 and y=T -- the two planes the shaft itself has to stand on. They
    # stop GAP short of both instead: those planes are buried butt joints, and
    # the wrap reads exactly the same.
    #
    # AND THE STACK IS NOW HUNG FROM THE FLARE, not measured up from nowhere.
    # _flare builds each band .016 over-tall so the bands lap, so the first
    # band's SOLE sits FLARE_LAP below zs -- 1.852 on variant C. The top ring
    # used to be authored at zs - .100 + .066*i, which put its top face at
    # 1.851: one millimetre off that sole, over the post's whole cross-section,
    # 682 cm2 measured and the second-largest coincident pair in the family.
    # Anchored here it is COL_G clear of the flare whatever jz the variant was
    # given, the rings are COL_G apart, and the lowest one stays COL_G above the
    # rolled bead's terminus boss below it (top at zs - .1275 on variant C).
    # Two rings is what variant C uses and what the 120 mm between the boss and
    # the flare has room for; a third would want the bead shortened to suit.
    for i in range(collar):
        ww = neck + .030 + .022 * i
        z = (zs - FLARE_LAP - COL_G - COL_H / 2
             - (COL_H + COL_G) * (collar - 1 - i))
        _bx(p, (-ww, -3 * GAP), (T - ww, T - 3 * GAP),
            (z - COL_H / 2, z + COL_H / 2),
            "oak_dark", bevel=.010, seg=1, tint=.05, shade=.90 + .07 * i)
    # ---- iron straps (variant B) -----------------------------------------
    for i in range(straps):
        z = lerp(0.60, zs - 0.34, i / max(1, straps - 1))
        ww = wat(z) + .012
        _bx(p, (-ww, -3 * GAP), (T - ww, T - 3 * GAP), (z - .024, z + .024),
            "iron", bevel=.007, seg=1, tint=.07)
    # ---- wall plates, lapping over the mushroomed head -------------------
    # The X plate is the through member; the Y plate dies INTO it, GAP short at
    # both ends and GAP in from its outer face -- which is how a lapped plate is
    # actually cut, and it stops the pair sharing three planes (~950 cm2).
    #
    # AND THE THROUGH MEMBER NOW FINISHES ON THE STOREY LINE, which is what
    # Shanee's second question is really about: z = H is a BUTT PLANE, the plane
    # the storey above lands on, so round 8's rule for x = 0 and y = T applies to
    # it too -- nothing stops short of a butt plane. It used to stop at zt + .170
    # = 2.570, 30 mm below the line, while the Y plate reached 2.600, so the top
    # of the post was not level: a post stacked on it bore on the Y plate and
    # floated over a 30 mm slot on the whole -X elevation. Measured on two
    # SM_Corner_TimberPost_A stacked at HU. The through member now tops out at H
    # and the Y plate dies GAP into it instead of standing 30 mm over it, so the
    # slot is 6 mm on one 200 mm beam end instead of 30 mm on a 240 mm one, and
    # nothing shares the z = H plane in the open (the Y plate's top is inside the
    # X plate everywhere the two overlap).
    _bx(p, (-head, 0.0), (-pd, T), (zt, zt + PLATE_BAND), "oak_dark",
        bevel=.016, seg=1, tint=.05, shade=.92)                      # along X
    _bx(p, (-head + GAP, -head + .200 + GAP), (-pd + GAP, T - GAP),
        (zt + .030, zt + PLATE_BAND - GAP), "oak_dark", bevel=.016, seg=1,
        tint=.05, shade=1.0)                                         # along Y
    # ---- joist-tooth course under the plates (ref2 signature) ------------
    if teeth:
        p.dentil((-head + .060, -.060), zt - .042, -pd * .58, "oak_dark",
                 step=.112, size=(.05, .085, .05), tint=.05, seed=3)
        _teeth_y(p, (0.03, T - .05), -head + pd * .42, zt - .042, "oak_dark",
                 seed=4)
    # ---- sole plate: square about the shaft, so it actually covers its foot --
    # Each band that wraps the shaft stops a DIFFERENT distance short of the
    # inner planes -- sole 2*GAP, straps/collars 3*GAP, pad 4*GAP. All of them
    # at one offset and their 45-degree arris chamfers landed on the shaft's.
    ws = w + .008
    if tenon:
        # THE SHOE, sallied: same band, but its sole stands FOOT_SPL wider than
        # its head so the timber spreads onto its bearing. Written the way _flare
        # writes the jowl -- taper + skew, so the two INNER faces stay planted and
        # only the two exposed ones move -- and pinned 4*GAP off them rather than
        # the plain sole's 2*GAP, because the shoulder below now owns 2*GAP and
        # the two bands overlap in z by GAP where they lap.
        kk = FOOT_SPL / 2
        p.box((-4 * GAP - ws / 2, T - 4 * GAP - ws / 2, z_sole + sh / 2),
              (ws, ws, sh), "oak_dark", bevel=.014, seg=1, tint=.05,
              taper=(ws - FOOT_SPL) / ws, taper_axis='XY', skew=(kk, kk),
              shade=.88)
    else:
        _bx(p, (-ws, -2 * GAP), (T - ws, T - 2 * GAP), (z_sole, z_sole + sh),
            "oak_dark", bevel=.014, seg=1, tint=.05, shade=.88)
    # ---- what the post stands ON: a stone pad, or the joint into the timber --
    if tenon:
        # THE SHOULDER. Squared oak bearing on the wall plate of the post below
        # and lapping FOOT_OUT over its arris, so the joint reads as housed and
        # not as two timbers stacked. It is the PROUD member at its own joint --
        # 6 mm outside the shoe's sole -- for the same reason BR_LET_IN puts the
        # post proud of the brace: at one plane the two chamfers interleave and
        # the joint reads as a crack.
        wsh = w + FOOT_OUT
        _bx(p, (-wsh - 2 * GAP, -2 * GAP), (T - wsh - 2 * GAP, T - 2 * GAP),
            (0.0, z_pad), "oak_dark", bevel=.012, seg=1, tint=.05, shade=.80)
    elif pad:
        wp = w + .045
        _bx(p, (-wp, -4 * GAP), (T - wp, T - 4 * GAP), (0.0, z_pad),
            "stone_pale", bevel=.014, seg=1, tint=.08, shade=.96)
    # ---- pegs: two through the jowl head, two at the spring, two at the sole
    # .030 in from the jowl face, not .010: a peg is a 45 mm cylinder laid ALONG
    # the axis it is driven on, so at .010 its head sat 22.5 mm outside the face
    # and 2.5 mm outside T + PROUD_MAX -- clamp_to_seams sliced the head flat off
    # every peg on the jowl. (It only showed up once the noise field was pinned;
    # unseeded it happened on some builds and not others.)
    _pegs(p, (-head / 2, T - head + .030, zt - .150), n=2, axis='Y',
          spread=.17, seed=5)
    _pegs(p, (-head + .030, T - head / 2, zt - .150), n=2, axis='X',
          spread=.17, seed=6)
    _pegs(p, (-neck / 2, T - neck + .008, zs - .38), n=2, axis='Y', seed=1)
    _pegs(p, (-neck + .008, T - neck / 2, zs - .38), n=2, axis='X', seed=2)
    # ... and the sole pair, on the Y face only -- but NOT on a housed foot,
    # where the joint pegs below stand in for them. Both sets and the -Y face
    # carried four peg heads in a 200 mm band, two of them through the chamfer
    # stop, which reads as a repair rather than as a joint.
    if not tenon:
        _pegs(p, (-w / 2, T - w + .008, sh + .12), n=2, axis='Y', spread=.11,
              seed=3)
    # ---- and the joint pegs, on BOTH exposed faces of the housed foot ------
    # The only part of a pegged tenon that ever shows from the street. The shoe
    # SPLAYS, so the face plane a head has to sit under moves with height: it is
    # interpolated at FOOT_PEG rather than taken at the sole, where the head
    # would have stood 10 mm inside the timber, or at the head, where it would
    # have floated 14 mm off it.
    if tenon:
        zp = z_sole + sh * FOOT_PEG
        wp = ws - FOOT_SPL * FOOT_PEG          # the shoe's width at that height
        fx, fy = -4 * GAP - wp, T - 4 * GAP - wp        # its two exposed faces
        _pegs(p, (-4 * GAP - wp / 2, fy + .012, zp), n=2, axis='Y',
              spread=.13, seed=11)
        _pegs(p, (fx + .012, T - 4 * GAP - wp / 2, zp), n=2, axis='X',
              spread=.13, seed=12)
    # .005, not .007: HEAD_MAX keeps only 10 mm back from T + PROUD_MAX for
    # wobble, and now that the noise field is PINNED (see _wob) the 7 mm pass
    # deterministically pushed ~50 verts of the jowl 5 mm past the allowance
    # every build, so clamp_to_seams flattened part of it every build. Before
    # seeding it did that on some runs and not others, which is how it went
    # unnoticed. At the family amplitude it fits.
    _wob(p, freq=1.3)
    return p.finish()


# ============================================================= arched braces =
# BOTH ENDS ARE HOUSED BY CONSTRUCTION. That is the design of this section, and
# it is written as arithmetic rather than as constants because constants are what
# went wrong: the head datum was a guess (H - PLATE_BAND = 2.400) against a plate
# whose soffit is pinned at 2.420, the foot was squared on a horizontal plane
# wherever the curve happened to reach it, and both were then quoted as landed in
# a docstring. Measured afterwards, 63% of the head's cut face stood in open air
# 108 mm below the plate soffit, and 88 of the foot's 167 mm hung past the post
# over bare plaster.
#
# So neither end is placed by a number any more. _brace_seat() builds the outline,
# then MEASURES its two cut faces and moves the outline until:
#   * the foot's cut face is entirely behind the post's face plane, BR_FOOT_BURY
#     inside it -- it is inside the post, whatever section or spring angle this
#     particular instance was hewn with;
#   * the head's cut face is CENTRED in timber_walls' plate band, so it is buried
#     in the plate top and bottom with the same margin.
# Vary the timber and both ends still land, because the seat is measured off the
# timber that was actually built.
def _arc_curve(span, drop, tw, spring=BR_SPRING, land=BR_LAND, n=10, adze=0.0,
               seed=0):
    """Centreline and outline of a curved arched brace, in
    (along-the-plate, height-below-the-head-datum).

    A CUBIC Bezier from the foot at (0, -drop) to the head at (span, 0), leaving
    the post at `spring` degrees above horizontal and arriving at the plate at
    `land`. Two handles rather than one is the point of the change: as a
    quadratic, one number (`bow`) had to serve both ends, and they pull opposite
    ways. Flat enough at the head to die into the plate put the foot within 5
    degrees of vertical -- and every millimetre of x a seated foot has to travel
    before it reaches daylight costs tan(spring) of height buried in the post, so
    at 85 degrees the 0.16 m from tenon to daylight would bury 1.8 m of arc. At a
    brace-like 60 degrees the same quadratic's head arrived at 20 degrees and
    rammed the plate instead of dying into it. With a handle each end, each joint
    gets the angle it needs and the middle is still one smooth arc. At the
    family's 69 / 7 that burial is 0.26 m, and the arch shows 0.75 m.

    BOTH ENDS ARE CUT SQUARE TO THE AXIS, which is simply the natural end of an
    offset curve -- there is no snapping to a plane here at all. It matters
    because a square cut is ONE SECTION wide however the timber is angled, while
    the horizontal foot cut this used to make is tw / sin(spring) wide: 170 mm of
    end grain measured off a 175 mm brace, wider than the 160 mm post
    (timber_walls W_POST) a wall run has to bury it in.

    `adze` swells and starves the section by up to that fraction along the curve
    and dies to zero at BOTH ends -- hand-hewn where it shows, exact where it is
    housed.
    """
    a0, a1 = radians(spring), radians(land)
    ch = (span * span + drop * drop) ** .5
    h = ch * 0.46
    P0, P3 = (0.0, -drop), (span, 0.0)
    P1 = (P0[0] + cos(a0) * h, P0[1] + sin(a0) * h)
    P2 = (P3[0] - cos(a1) * h, P3[1] - sin(a1) * h)
    r = rng(f"{FAMILY}/arc/{seed}")
    k0, k1 = r.uniform(0, 2), r.uniform(0, 2)
    mid = []
    for i in range(n + 1):
        t = i / n
        b0, b1, b2, b3 = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        mid.append((b0 * P0[0] + b1 * P1[0] + b2 * P2[0] + b3 * P3[0],
                    b0 * P0[1] + b1 * P1[1] + b2 * P2[1] + b3 * P3[1]))
    soffit, back = [], []
    for i, (u, v) in enumerate(mid):
        t = i / n
        j0, j1 = max(0, i - 1), min(n, i + 1)
        du, dv = mid[j1][0] - mid[j0][0], mid[j1][1] - mid[j0][1]
        L = (du * du + dv * dv) ** .5 or 1.0
        nu, nv = -dv / L, du / L                     # left normal = toward corner
        w = tw * (1 + adze * sin(pi * t) *
                  (.62 * sin(pi * (2 * t + k0)) + .38 * sin(pi * (3 * t + k1)))) / 2
        back.append((u + nu * w, v + nv * w))
        soffit.append((u - nu * w, v - nv * w))
    return mid, soffit + back[::-1]


def _seat_once(run, drop, tw, spring, land, n, adze, seed):
    """THE OUTLINE, PLACED SO BOTH ENDS ARE HOUSED. Returns (poly, mid, zt).

    `poly` and `mid` are in the brace's own frame with x = 0 on the post's face
    plane; `zt` is the absolute height of the head datum, so the piece is built at
    at=(0, BR_MID_Y, zt). Two measurements do the placing, and both are taken off
    the outline that was actually built rather than assumed from the inputs:

    ALONG X. poly[0] and poly[-1] are the foot's two cut-face corners. The whole
    outline is slid until the further of them sits BR_FOOT_BURY behind x = 0, so
    the entire cut face is inside the post. `span` is then re-solved so the piece
    still reaches exactly `run` -- the reach is what the declared snap box and
    every placement rule quote, and it may not drift when the section does.

    IN Z. poly[n] and poly[n+1] are the head's cut-face corners. zt centres that
    face in timber_walls' plate band (PLATE_SOF..PLATE_TOP), so the head is buried
    by the same margin above the soffit and below the plate's top, and the arc
    disappears behind a plate that stands 38 mm proud of it.
    """
    span, du = run, 0.0
    for _ in range(6):
        mid, poly = _arc_curve(span, drop, tw, spring, land, n, adze, seed)
        du = -(max(poly[0][0], poly[-1][0]) + BR_FOOT_BURY)
        err = run - (max(u for u, _ in poly) + du)
        if abs(err) < 1e-7:
            break
        span += err
    zt = (PLATE_SOF + PLATE_TOP) / 2 - (poly[n][1] + poly[n + 1][1]) / 2
    return ([(u + du, v) for (u, v) in poly],
            [(u + du, v) for (u, v) in mid], zt)


def _brace_seat(run=BR_RUN, spring_z=BR_SPRING_Z, spring_u=BR_SPRING_U,
                tw=BR_TW, spring=BR_SPRING, land=BR_LAND, n=10, adze=0.0, seed=0):
    """_seat_once, with `drop` solved so the arch SPRINGS WHERE IT SHOULD.

    Seating the two ends fixes where the arc is HOUSED and says nothing about
    where it becomes visible, and the second is the number the eye reads: the
    height at which the soffit clears BR_SPRING_U and comes into daylight. Both
    of its inputs moved this round -- the head datum rose 110 mm onto
    timber_walls' real plate soffit, and the foot now starts 0.26 m of climb
    further down, inside the post -- so a fixed `drop` cost the visible arch a
    third of its height and the demo's arcade turned into a row of small
    brackets. Newton on `drop` (the crossing moves ~1:1 with it) puts it back
    and, more usefully, makes the springing line a DATUM: every brace in a run,
    whatever section or angle it was hewn with, comes out from behind its post at
    the same height. Solved, not authored, so no variant can drift off it.
    """
    drop = BR_DROP
    poly = mid = None
    for _ in range(8):
        poly, mid, zt = _seat_once(run, drop, tw, spring, land, n, adze, seed)
        err = zt + _walk(poly[:n + 1], u=spring_u)[1] - spring_z
        if abs(err) < 2e-4:
            break
        drop += err
    return poly, mid, zt


def _walk(pts, u=None, v=None):
    """The point on a polyline at a given u (or a given v). Joint pegs are put on
    the curve with this instead of at guessed coordinates, so they stay on the
    timber when the timber is hewn differently."""
    k = 0 if u is not None else 1
    tgt = u if u is not None else v
    for a, b in zip(pts, pts[1:]):
        if min(a[k], b[k]) <= tgt <= max(a[k], b[k]) and abs(b[k] - a[k]) > 1e-9:
            t = (tgt - a[k]) / (b[k] - a[k])
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return min(pts, key=lambda p: abs(p[k] - tgt))


# ---------------------------------------------------------------------------
# ONE BRACE IS THE COMPONENT.  THE PAIR IS AN ASSEMBLY OF TWO OF IT.
# ---------------------------------------------------------------------------
# Shanee: "Maybe SM_Corner_ArchBrace_Pair should be split into single
# component?"  Right, and it is a MODULARITY fault, not a defect -- the pair
# measures and always measured x -0.317..0.920, y -0.079..1.160, an L of two
# braces welded into one asset. A corner where only ONE direction wants a brace
# cannot use it, and a run of wall that wants a brace away from a corner cannot
# use it at all. So the brace is a piece and the pair is KEPT -- the assembler
# places it at 12 corners: assemble_inn.corners(brace=True) runs MAIN SWSENENW
# on two timber storeys (8) and HERO SWSE on two (4).
#
# WHAT THE FIRST SPLIT GOT WRONG, and it is the reason this pass exists. Both
# arms were stamped from ONE frozen blank, so the pair's two braces came out
# vertex-identical: max deviation 0.000001 m, one stick of timber photocopied.
# That is the one thing this kit does not do. The single-blank trick was there to
# make "two singles ARE the pair" true, and the equivalence is worth keeping --
# but it is an equivalence between the pair's arm i and the SINGLE PIECE FOR ARM
# i, not between the two arms. So there are now two blanks, _brace_var(0) and
# _brace_var(1), hewn from different section, spring, land, adze and wobble; the
# pair stamps var 0 at row 0 and var 1 at row 1; and the two singles
# SM_Corner_ArchBrace and SM_Corner_ArchBrace_B are those same two blanks. Two
# singles are still the pair, vertex for vertex -- they are just not each other.
#
# THE FRAME.  SM_Corner_ArchBrace's local axes, and the frame the blanks are
# built in:
#     +X    the direction the brace REACHES along the wall run.
#     x = 0 the face of the post it springs off -- i.e. the plane where the wall
#           run starts, and at a corner that is the cell's butt plane. The whole
#           foot is BEHIND it, inside the post (see _brace_seat).
#     y = 0 the wall's OUTER FACE, spec.py's convention. The timber lies at
#           y = BR_FACE .. BR_FACE + BR_DEEP (-0.054 .. 0.004), let 6 mm into the
#           plane every timber_post presents at its neck (NECK_W). That puts it
#           behind timber_walls' rails (BY -0.070), its seam posts (POST_Y
#           -0.080) and its wall plate (PLATE_Y -0.092) -- so every member it is
#           jointed to covers it -- and 20 mm proud of the plaster crown.
#     z = 0 the storey floor. The head is housed in the wall plate band
#           (2.420..2.600); the foot springs BR_DROP below the head datum.
#
# PLACING IT.  A rotation rz turns the REACH to +X / +Y / -X / -Y for
# rz = 0 / 90 / 180 / 270, and turns the OUTWARD face to -Y / +X / +Y / -X.
#   * on a wall whose outward direction MATCHES the rotated outward, put the
#     origin ON that wall's outer face plane, at the storey floor, at the point
#     the brace springs from;
#   * on a wall whose outward is the OTHER way, slide the origin
#     2 * BR_MID_Y = -0.050 m along that wall's outward direction.
# That second case is not a quirk, it is the geometry: two braces at an OUTSIDE
# corner are a MIRROR pair (the cell's two exposed faces are y=0 and x=-T, so
# they face -Y and -X), and no rotation mirrors. It only works at all because
# each blank is symmetric about its own centre plane -- which is exactly why the
# joint pegs are driven RIGHT THROUGH the timber instead of tucked under one
# face: a one-sided peg comes out on the HIDDEN face of the second brace.
#
# So at a corner post placed at C with rotation RZ:
#     put("SM_Corner_ArchBrace",   C,                              RZ +  0)
#     put("SM_Corner_ArchBrace_B", C + rot(RZ, (-0.290, 0.240, 0)), RZ + 90)
# and arch_brace_place(C, RZ) returns exactly those two rows, NAME INCLUDED.

ARCH_BRACE_ARMS = ("SM_Corner_ArchBrace", "SM_Corner_ArchBrace_B")


def arch_brace_place(at=(0.0, 0.0, 0.0), rz=0.0, deep=BR_DEEP):
    """WHERE THE ASSEMBLER PUTS TWO SINGLE BRACES SO THAT THEY ARE ONE
    SM_Corner_ArchBrace_Pair. `at` and `rz` are the CORNER POST's own placement
    -- the same two arguments the pair is placed with today. Returns two rows of
    (name, (x, y, z), rz_degrees), ready to hand straight to put():

        for nm, loc, r in corners.arch_brace_place(C, RZ):
            put(nm, loc, r)

    THE NAME IS PART OF THE ROW because the two arms are not the same brace any
    more (see above): row 0 is SM_Corner_ArchBrace, row 1 is
    SM_Corner_ArchBrace_B, and placing arm 0's piece twice would put the
    photocopy back.

    Row 0 -- the brace into the run that leaves the cell on +X, whose wall face
    is the y=0 plane: THE CORNER POST'S OWN ORIGIN, rz + 0. No offset, because a
    brace at rz 0 already faces -Y like that wall.

    Row 1 -- the brace into the run that leaves on +Y, whose wall face is x=-T:
    rz + 90, at (-T + 2*BR_MID_Y, T, 0) = (-0.290, 0.240, 0) in the corner's own
    frame. The T in y is where that run starts (the cell's other butt plane); the
    -0.290 is the mirror correction described above -- rotated 90 deg the brace
    faces +X while that wall faces -X, so it is slid back through its own centre
    plane twice.

    The assembler's storey stretch comes along unchanged: it scales the pair by
    (1, 1, zs) about the corner's own origin, both rows here sit at that origin's
    z, and a rotation about Z never touches z -- so putting the SAME scale on
    each single gives the same mesh as scaling the pair. (assemble_inn.py passes
    it as `scale=csc`; braces that do not ride it are what made them look like
    they were floating about, and that was never this piece.)
    """
    mid = BR_FACE + deep / 2
    c, s = cos(radians(rz)), sin(radians(rz))
    rows = ((ARCH_BRACE_ARMS[0], (0.0, 0.0, 0.0), 0.0),
            (ARCH_BRACE_ARMS[1], (-TT + 2 * mid, TT, 0.0), 90.0))
    return [(nm, (at[0] + ox * c - oy * s, at[1] + ox * s + oy * c, at[2] + oz),
             rz + orz) for nm, (ox, oy, oz), orz in rows]


ARCH_BRACE_PLACE = arch_brace_place()   # the two rows in the corner's own frame


def _brace_var(var):
    """HOW ARM `var` IS HEWN. Per-INSTANCE variation, drawn at stamp time.

    The regression this fixes: variation used to live in ONE authored blank, so
    every brace in the kit was that blank and the pair was it twice. Here the
    variation is a property of the INSTANCE -- arm 0 and arm 1 of a pair get
    different section, spring angle, landing angle, adze profile, tone and (via
    the blank's name, which seeds util's noise field) a different hand-hewn
    surface. Nothing that varies can unland an end: _brace_seat measures the
    timber it is given and seats THAT, and the adze dies to zero at both ends, so
    every variant's cut faces are still one section across and still inside their
    housings.
    """
    r = rng(f"{FAMILY}/archbrace/{var}")
    return dict(tw=BR_TW * r.uniform(.94, 1.03),
                spring_z=BR_SPRING_Z + r.uniform(-.014, .014),
                spring=BR_SPRING + r.uniform(-3.0, 3.0),
                land=BR_LAND + r.uniform(-2.0, 2.0),
                adze=r.uniform(.08, .14),
                shade=.97 + r.uniform(-.05, .04),
                seed=var)


def _brace_blank(var=0, **over):
    """ONE arched brace, hand-hewn as arm `var`, in THE FRAME above.

    A scratch Part rather than geometry emitted straight into the piece, because
    THE WOBBLE HAS TO HAPPEN HERE, in the brace's own frame. util.Part.wobble
    seeds its noise field from the part NAME and samples it at world position, so
    wobbling the pair as a whole gives its two braces surfaces that depend on
    where they were stamped, and neither is the surface the single piece would
    have had. Wobbled in the blank, arm `var` is the same stick of timber
    wherever it is used, and SM_Corner_ArchBrace / _B are true drop-ins for the
    pair's two halves.

    The name carries `var`, which is what makes the two arms different sticks:
    it is the wobble field's seed and every rng() below hangs off it.
    """
    k = _brace_var(var)
    k.update(over)
    b = Part(f"SM_Corner_ArchBrace#{k['seed']}", smooth=True)
    b.seams = dict(x=(-TT, BR_RUN), z=(0.0, HU))
    poly, mid, zt = _brace_seat(tw=k["tw"], spring_z=k["spring_z"],
                                spring=k["spring"], land=k["land"],
                                adze=k["adze"], seed=k["seed"])
    b.prism(poly, BR_DEEP, "oak_dark", axis='Y', at=(0.0, BR_MID_Y, zt),
            bevel=.013, seg=1, tint=.05, shade=k["shade"])
    # A pegged tenon at each joint, driven THROUGH -- so the blank is symmetric
    # about y = BR_MID_Y and survives the 90 deg rotation that makes the second
    # half of a corner pair. Both sit ON the centreline (see _walk) rather than at
    # coordinates that were right for one section only:
    #   foot  50 mm behind the post's face plane (BR_FOOT_BURY + 32), i.e. through
    #         the tenon. Its head stands 10 mm proud of the POST's face, which is
    #         where a peg driven into a mortice shows.
    #   head  75 mm below the plate soffit, i.e. on the last piece of brace still
    #         in daylight. Anything higher is inside the plate and 38 mm behind
    #         its face, so it would peg nothing anyone can see.
    thru = BR_DEEP + 2 * BR_PEG_OUT
    fu, fv = _walk(mid, u=-(BR_FOOT_BURY + .032))
    _pegs(b, (fu, BR_MID_Y, zt + fv), n=1, axis='Y', r=BR_PEG_R,
          length=thru, seed=7)
    hu, hv = _walk(mid, v=PLATE_SOF - .075 - zt)
    _pegs(b, (hu, BR_MID_Y, zt + hv), n=1, axis='Y', r=BR_PEG_R,
          length=thru, seed=8)
    _wob(b, .006, freq=1.2)
    return b


def arch_brace_single(name=ARCH_BRACE_ARMS[0], var=None, **over):
    """ONE curved arched brace: springs off a post face, arches over BR_RUN and
    is housed in the wall plate -- ref3's most repeated detail, and the thing
    that stops a corner reading as two flat walls butted together.

    THE COMPONENT. Use it wherever ONE brace is wanted: a corner braced in one
    direction only, the two ends of a bay so a run of wall reads as an arcade,
    the spandrel beside a doorway. Two of them at a corner, placed by
    arch_brace_place(), ARE SM_Corner_ArchBrace_Pair.

    `var` PICKS WHICH ARM, AND THE NAME PICKS IT FOR YOU. Left at None -- which
    is the default, and what every caller should use -- var comes from the name's
    position in ARCH_BRACE_ARMS, so SM_Corner_ArchBrace is arm 0 and
    SM_Corner_ArchBrace_B is arm 1 and there is no way to ask for one and build
    the other. It used to default to 0 whatever name was passed, which made
    `arch_brace_single(ARCH_BRACE_ARMS[1])` -- the obvious call, and the one
    arch_brace_place() hands you the name for -- silently rebuild arm 0 under
    arm B's name: the vertex-identical photocopy this whole section exists to
    prevent, one keyword away. Passing a var that contradicts a known arm's name
    is now an error rather than a surprise; pass any var you like with a name of
    your own if you want a third stick.

    SEAM-SPANNING TRIM, and the declared box says so: it reaches BR_RUN along
    the wall run and a T x T corner cell has no wall length in it at all, so
    spec.py's "deliberate seam-spanning trim which must be a SEPARATE piece" is
    what this is. y is declared as a wall's (0..T_TIMBER) even though the whole
    piece is relief standing proud of y=0 -- that IS what it is, relief, and
    outward="y" is what lets it stand there.

    BOTH ENDS LAND, and this time that is a measurement, not a claim. THE NUMBERS
    ARE ARM A, with arm B's given wherever the two differ -- and they do differ,
    which is what the previous version of this docstring got wrong when it said
    "arm B is within 2 mm of each of them". The head lands on a DATUM (centred in
    the plate band) so the two arms agree there within 2 mm; the foot lands on a
    PLANE (x = -BR_FOOT_BURY) and its HEIGHT falls wherever the solved drop puts
    it, which is up to 29 mm apart between arms. Burial below is a 21 x 21 grid
    over each cut face, arrises included, every sample tested by ray parity
    against each loose shell of the pieces the brace is jointed to -- per shell,
    because parity over a whole piece cancels wherever two of its solids lap:

      foot  cut SQUARE TO THE AXIS, so ONE SECTION across however it is angled:
            133.0 mm on arm A, 130.3 mm on arm B (each arm's own tw, drawn by
            _brace_var), of which 107 mm is flat between the two 13 mm chamfers.
            Spans x -0.0180..-0.1423 on arm A and -0.0180..-0.1378 on arm B --
            the whole face behind the post's face plane, BR_FOOT_BURY = 18.0 mm
            inside it at the near edge, on both arms, because that is the plane
            _seat_once solves the outline onto. In z it is 1.4086..1.4557 on
            arm A and 1.4337..1.4850 on arm B: 25-29 mm apart, the difference
            the old "within 2 mm" hid.
            441/441 samples buried, 0.0 cm2 open, on BOTH arms, both against
            SM_Corner_TimberPost_A at a corner and against the W_POST seam post
            that two timber_walls bays make mid-run.
            It was a HORIZONTAL cut, tw / sin(spring) = 167 mm wide, with 88 mm
            of it hanging past the post over bare plaster -- 62.3 cm2 of squared
            end grain over nothing.
      head  cut square to the axis, the same one section, standing 131.0 mm tall
            in z on arm A because the landing tangent is only 6.7 deg off
            horizontal. z 2.4445..2.5755 on arm A, 2.4463..2.5737 on arm B: 24 mm
            above timber_walls' 2.420 plate soffit and 24 mm below the plate's
            2.600 top, and EQUAL above and below by construction, because
            _seat_once centres the cut face in the band. 441/441 buried, 0.0 cm2
            open, on both arms, with the arc disappearing behind a plate that
            stands 38 mm proud of it.
            It used to run 2.312..2.483, with 73.6 of 117.2 cm2 -- 63% -- of the
            face standing in open air 108 mm BELOW the soffit it claimed to be
            housed in.

    Measured on the built mesh arm A spans x -0.140..0.918, y -0.070..0.023 (the
    peg heads), z 1.410..2.573; arm B x -0.131..0.917, y -0.073..0.021, z
    1.440..2.571. 332 tris each against the 1800 corner budget. Arm A's soffit
    comes into daylight at z 1.6745 and arm B's at 1.6678 (BR_SPRING_Z's own
    +-14 mm), so 0.266 m of arm A is inside the post below its springing line and
    0.746 m of arch is in the open.

    AND IT CLEARS THE ROOF AS THE ROOF NOW IS. Its highest point, 2.573, is
    0.027 m below the wall head and 0.038 m behind the wall plate's face
    (PLATE_Y -0.092). spec.EAVE_OVER is 0.14 now, not 0.55, and roofs.py puts
    the eave's drop at EAVE_OVER * tan(assembled pitch) = 0.30 m below the wall
    head -- but every millimetre of that happens outboard of, and above, ground
    the wall plate already occupies, so anything that clears the plate clears
    this. The brace is never the piece the eave has to miss.
    """
    if var is None:
        var = ARCH_BRACE_ARMS.index(name) if name in ARCH_BRACE_ARMS else 0
    elif name in ARCH_BRACE_ARMS and var != ARCH_BRACE_ARMS.index(name):
        raise ValueError(
            f"{name} IS arm {ARCH_BRACE_ARMS.index(name)}; asking for arm {var} "
            f"under that name would build a different stick of timber from the "
            f"one SM_Corner_ArchBrace_Pair puts there. Leave var=None, or use a "
            f"name of your own.")
    p = Part(name, budget="corner", outward="y",
             seams=dict(x=(-TT, BR_RUN), y=(0.0, TT), z=(0.0, HU)))
    blank = _brace_blank(var=var, **over)
    p.merge(blank)
    blank.bm.free()
    return p.finish()


def arch_brace(name="SM_Corner_ArchBrace_Pair"):
    """The PAIR: two SM_Corner_ArchBrace, one into each wall plate, springing
    off a half-timber corner post. KEPT -- the assembler places it at 12 corners
    and a level artist who wants a braced corner should not have to place two
    pieces to get one.

    It is literally the two singles stamped at arch_brace_place(), arm 0 then arm
    1, so swapping it for those two pieces changes nothing, and the pair can
    never quietly become a different brace from its components. MEASURED: place
    SM_Corner_ArchBrace and SM_Corner_ArchBrace_B on the two rows and you get 344
    vertices against this piece's 344, none of them further than 1.2e-7 m from
    its twin -- which is float round-off in the placement matrix, not geometry.

    The two arms are NOT each other, and that is the other half of the fix: they
    are hewn from different section, spring, land, adze and noise field (see
    _brace_var), and measure 0.033 m apart at their furthest -- 33.4 mm vertex for
    vertex, 33.2 / 33.4 mm as a nearest-point distance each way. (0.055 m stood
    here for a while and was never the mesh; the number is 0.033.) Against the
    0.000001 m of stamping one blank twice, which is how the first split made the
    singles match. Vertex-identical arms are the one thing this kit's whole
    character says it does not do; equivalence is between arm i and ITS piece,
    never between the arms.

    Snap it at the SAME origin as the corner post, exactly as before.
    """
    T, H = TT, HU
    p = Part(name, budget="corner", outward="xy",
             seams=dict(x=(-T, BR_RUN), y=(0.0, T + BR_RUN), z=(0.0, H)))
    for i, (_nm, loc, rz) in enumerate(arch_brace_place()):
        blank = _brace_blank(var=i)
        p.merge(blank, at=loc, rot=(0.0, 0.0, rz))
        blank.bm.free()
    return p.finish()


# =============================================================== stone quoin =
def _bed(zb, zt, j):
    """(z0, z1) offsets for one canonical course: HALF A JOINT where the course
    beds against another course, Q_BED where it beds against one of stone_walls'
    three dressed slabs.

    Which end is which is read off the slab levels rather than off the row's
    index, so it is right for any grid SW hands us and for the re-entrant corner,
    which lays its own jamb blocks on the same rows without going through
    _quoin_courses. ROWS_P[0]'s zb = 0 is deliberately NOT in the list: that
    course beds on the ground, which is the z = 0 snap plane, where coincidence
    is expected and where check_zfight excludes it."""
    ON = (SW.PLINTH_Z, SW.SILL_Z)                       # slab TOPS, laid on
    UNDER = (SW.PLINTH_Z - SW.PLINTH_CAP, SW.BAND_Z0, SW.HEAD_Z)   # slab soffits
    lo = Q_BED if any(abs(zb - z) < 1e-6 for z in ON) else j / 2
    hi = Q_BED if any(abs(zt - z) < 1e-6 for z in UNDER) else j / 2
    return lo, hi


def _quoin_courses(p, T, rows, seed, proud=Q_PROUD, deep=Q_DEEP, joint=None,
                   rough=0.0, phase=0, pale=.42, wrap=True, bed=(None, None)):
    # `bed` ADDED to unbreak the build. A fixer killed by a session limit mid-edit left
    # this function reading bed[0]/bed[1] with no such parameter in its signature, so
    # every corners build died with "NameError: name 'bed' is not defined". Defaulting
    # to (None, None) restores exactly the pre-edit behaviour -- both ends fall through
    # to j/2, a half joint -- rather than inventing a value the callers never asked for.
    # The intent was evidently a per-call override of the Q_BED end treatment; see the
    # _bed() helper just above, which computes the same thing from the ON/UNDER lists.
    """Alternating long-and-short dressed corner blocks, ONE PER CANONICAL COURSE.

    `rows` is stone_walls' own course grid, so every bed joint here is a bed
    joint of the wall run on both elevations: it comes out of the wall, crosses
    the arris and goes back into the wall on the other side. That is the whole
    difference between a quoin and a column of blocks parked on the end of a
    wall, and it is what the .293 course height this used to carry made
    impossible -- against a .265 grid it drifted out of register within three
    courses and never came back.

    The blocks are still deliberately bigger and squarer than the field stones
    (one block spans the whole 0.36 cell, ~1.3:1 on a .265 course, which is what
    ref2 draws) and still stand a little prouder. `wrap` off means only the y=0
    elevation is exposed -- the re-entrant corner -- so nothing may cross x=-T.

    ROUND 8: every block RUNS OUT PAST ITS BUTT PLANE (`bt`) and is cut flat
    there by clamp_to_seams, which is the same thing stone_walls does to the
    stone that straddles a bay seam. It used to stop half a joint short of x=0,
    which put a full-height 18 mm slot at the quoin/wall junction -- and with
    the core stopping 24 mm short as well, what showed through the slot was the
    plaster lining. There is no joint to draw there: the block the wall lays
    against the seam is cut flat on the same plane, so quoin and field meet the
    way two halves of a seam stone meet, and the only line left at the junction
    is the 14 mm step the quoin is supposed to stand proud by."""
    j = SW.JOINT if joint is None else joint
    r = rng(f"{p.name}/quoin/{seed}")
    last = len(rows) - 1
    for i, (zb, zt) in enumerate(rows):
        dz = r.uniform(-1, 1) * .004 * (1 + rough)
        # A dressed SLAB, not another course, at the end of the stack: that end
        # gets Q_BED instead of half a joint, and the jitter there is signed so
        # it can only widen the joint. See Q_BED -- the stack's two ends are the
        # only place in this masonry where the jitter is bigger than the joint.
        lo = bed[0] if (i == 0 and bed[0] is not None) else None
        hi = bed[1] if (i == last and bed[1] is not None) else None
        z0 = zb + (lo + abs(dz) if lo is not None else j / 2 + dz)
        z1 = zt - (hi + abs(dz) if hi is not None else j / 2 - dz)
        pr = proud * r.uniform(.86, 1.16 + rough * .5)
        dp = deep * r.uniform(.92, 1.06)
        # in-plane tilt only: a YAW would lift a block off the butt plane it has
        # to present flat to the wall run, and util would then cut it back flat
        # and leave a wedge of daylight
        tilt = r.uniform(-1, 1) * (0.35 + rough * 1.3)

        def mat():
            q = r.random()
            return ("stone_pale" if q < pale else
                    ("stone_warm" if q < pale + .20 else "stone"))

        def on_y(x0, x1):                       # block on the y=0 elevation
            _bx(p, (x0, x1), (-pr, dp), (z0, z1), mat(), bevel=Q_BEV, seg=1,
                tint=.075, rot=(0, tilt, 0), shade=.99 + r.uniform(-.08, .08))

        def on_x(y0, y1):                       # block on the x=-T elevation
            _bx(p, (-T - pr, -T + dp), (y0, y1), (z0, z1), mat(), bevel=Q_BEV,
                seg=1, tint=.075, rot=(tilt, 0, 0),
                shade=.97 + r.uniform(-.08, .08))

        bt = Q_BEV + BUTT_BEV                   # overshoot: see the docstring
        if not wrap:
            on_y(-T, bt)                        # re-entrant: one face, no arris
        elif (i + phase) % 2 == 0:
            on_y(-(T + pr), bt)                 # long wraps the arris
            on_x(dp + j, T + bt)                # short closes the return
        else:
            on_x(-pr, T + bt)                   # long wraps the arris
            on_y(-T + dp + j, bt)               # short closes the return


def _plinth_L(p, T, seed=0, wrap=True):
    """THE FAMILY'S PLINTH, returned round the corner: SW.ROWS_P's two courses of
    big blocks on the wall's own 32 mm batter, closed by the flat dressed cap at
    SW.PLINTH_Z with SW.SLAB_CAP_Y's nose.

    What was here before was a course of small round p.stones() cobbles 150 mm
    proud, 270 mm tall, under a cap 140 mm proud topping out at 0.36 -- a plinth
    that matched nothing in the kit, in a masonry that appears nowhere else in
    it, meeting the wall's plinth with a 225 mm step in level and a 90 mm step in
    projection. At the most-looked-at corner of the building."""
    _quoin_courses(p, T, SW.ROWS_P, seed, proud=Q_PROUD_PL, deep=Q_DEEP_PL,
                   joint=SW.JOINT_PL, pale=.30, wrap=wrap)
    nose, bv = SW.SLAB_CAP_Y[0], .016
    _bx(p, (-T + nose, bv + BUTT_BEV), (nose, T + bv + BUTT_BEV),
        (SW.PLINTH_Z - SW.PLINTH_CAP, SW.PLINTH_Z),
        SW.slab_mat(f"{p.name}/pcap"), bevel=bv, seg=1, tint=.06, shade=.98)


def _band_L(p, T):
    """The sill string course, turned round the corner at stone_walls' z and
    nose. Every wall piece in the family carries this 150 mm course at
    0.90-1.05; the quoins carried none of it, so the strongest horizontal on the
    elevation ran up to the corner and stopped. One box, because a corner stone
    that wraps an arris is one stone.

    ... and it now runs THROUGH the corner: out past both butt planes, cut flat
    there like stone_walls' seam slabs, rather than stopping BAND_IN = 18 mm
    short of each. Round 7's own lesson, applied to the last 18 mm of it: a dark
    nick through the strongest horizontal on the elevation is a seam line you can
    count off down the street -- and this one had the plaster lining behind it."""
    nose, bv = SW.SLAB_BAND_Y[0], .014
    _bx(p, (-T + nose, bv + BUTT_BEV), (nose, T + bv + BUTT_BEV),
        (SW.BAND_Z0, SW.SILL_Z),
        SW.slab_mat(f"{p.name}/band"), bevel=bv, seg=1, tint=.06, shade=1.0)


def _head_L(p, T):
    """Wall-head course, at SW.HEAD_Z (2.905, not 2.900) with SW's nose, and out
    to both butt planes for the same reason as _band_L."""
    nose, bv = SW.SLAB_HEAD_Y[0], .010
    _bx(p, (-T + nose, bv + BUTT_BEV), (nose, T + bv + BUTT_BEV),
        (SW.HEAD_Z, HG),
        SW.slab_mat(f"{p.name}/head"), bevel=bv, seg=1, tint=.05, shade=.95)


def stone_quoin(name, rough=0.0, phase=0, seed=1):
    """The outside stone corner: dressed quoins wrapping the arris on the WALL'S
    OWN course grid, over the wall's plinth, through the wall's sill band, under
    the wall's head course. Nothing in it is a number of its own any more.

    Variant B is the same corner with the long-and-short alternation started on
    the other parity and rougher stones -- which is a real difference a level
    artist can use, unlike variant B's old extra string course at 1.86, a
    horizontal that no wall in the kit has and that therefore announced the
    corner as a foreign piece from across the street."""
    T, H = TS, HG
    p = Part(name, budget="corner", seams=_seams(T, H), outward="xy")
    _core(p, T, SW.HEAD_Z + GAP)          # laps up into _head_L (see _core)
    _skim(p, T, H)
    _plinth_L(p, T, seed=seed)
    _quoin_courses(p, T, SW.ROWS_A, seed + 1, rough=rough, phase=phase)
    _band_L(p, T)
    _quoin_courses(p, T, SW.ROWS_B, seed + 2, rough=rough,
                   phase=phase + len(SW.ROWS_A))
    _head_L(p, T)
    _wob(p, freq=1.4)
    return p.finish()


# =============================================================== jetty joint =
def jetty_joint(name="SM_Corner_JettyJoint", seed=1):
    """The corner of a jettied storey: two sill beams lapping over each other, a
    diagonal dragon beam bisecting the angle, a knee brace carrying it down to
    the wall corner and pale stone corbels breaking out of the masonry below.
    Place at (storey_top - JETTY_BAND); the storey above sits JETTY further out.

    THE INTERFACE, and BOTH HALVES OF IT WERE WRONG -- these are the two faults
    Shanee found on SM_Corner_JettyJoint.005:

    1. THE CELL. A jetty joint is the corner of a TIMBER storey, so its cell is
       T_TIMBER. It was built on the T_STONE cell while assemble_inn.py places
       it -- corners(blk, "timber") -- on blk.tb, the same rectangle inset
       T_TIMBER that carries the sill runs. So its return leg stood
       T_STONE - T_TIMBER = 120mm proud of the run's face and its butt plane
       landed 120mm past the run's end. Measured in out/inn_example.blend on the
       exact pair Shanee named: this piece's return face at x = 5.910 against
       SM_Beam_JettySill_2m_A.026's face at 6.030, its butt plane at y = -1.520
       against that run's end at -1.640. The cell now comes from
       B.SILL_CELL, one constant, in the file that owns the profile.

    2. THE LINE ACROSS ITSELF. The two sills were two boxes lapped over each
       other, so they butted face to face straight across the weather board's
       top -- the ledge you look down on at the outside corner of the building
       -- and each brought its own bevel to that butt, i.e. a chamfered groove
       drawn across the middle of the piece. The timber and the board are now
       ONE MITRED L EACH, swept by B.sweep() from B.sill_corner_rails(): the
       chamfer turns the arris, and there is no butt to show.

    Both sills therefore present THE JETTY SILL PROFILE -- same top, same
    soffit, same face, same depth, same weather board lip, same chamfer, same
    flat tone -- on x = B.SILL_JOINT_X and on y = B.SILL_JOINT_Y, with the cut
    faces dead flat. Vertically it works out because this piece is placed
    JETTY_BAND below the storey line while the sill runs are placed SILL_H below
    it, and both put their top face ON that line: DZ is that difference, and it
    is the only number this piece adds to the profile."""
    T, HB = B.SILL_CELL, JETTY_BAND
    p = Part(name, budget="corner", seams=_seams(T, HB, out=(J, J)),
             outward="xy")
    r = rng(name)
    out = T + J                       # 0.69 from the inner face to the new face
    # ---- the shared section, expressed in this piece's coordinates --------
    DZ = HB - B.SILL_TOP              # 0.32: lift from a run piece's frame
    zt = HB                           # top of the sill == the storey line
    zb = B.SILL_SOF + DZ              # its soffit, at either butt plane
    zc = B.SILL_TOP - B.SILL_CAP + DZ  # underside of the weather board band
    fy, by = B.SILL_FACE, B.SILL_BACK             # face/back on the y=0 wall
    fx, bx = -T + B.SILL_FACE, -T + B.SILL_BACK   # ... and on the x=-T wall
    # The stone storey below stands this far proud of the timber face it carries
    # (assemble_inn.py's INSET: the two rectangles are the same rectangle inset
    # by their own wall thickness), so the stone corbels that break out of the
    # masonry have to be measured off THAT plane, not off this cell's faces.
    so = TS - TT                      # 0.12

    # ---- diagonal dragon beam, which the mitred sill laps over ------------
    # Its INNER end stays pulled inside the piece's own box: the 0.20 section is
    # perpendicular to the diagonal, so an end ON a butt plane put a corner 66mm
    # past it and util clamped that corner flat ONTO the plane -- straight into
    # the floor plate's face.
    # It now runs THROUGH the mitre and shows its tapered nose NOSE past the
    # outside arris, which is the only way it can be seen at all: inside the
    # band it was enclosed by the two sills and the floor plate on every side,
    # 60-odd tris of geometry no camera could ever reach. Four "joist soffits"
    # that used to sit in here were the same thing, and they are gone.
    NOSE = .044
    p.beam((-.075, T - .085, (zb + zc) / 2 - GAP),
           (fx - NOSE, fy - NOSE, (zb + zc) / 2 - GAP),
           .20, zc - zb - 4 * GAP, "oak_dark", bevel=.022, seg=1, tint=.05,
           shade=.80, taper=.74)
    # ---- knee brace under it, in the vertical plane of the diagonal -------
    # Every z here hangs off zb, the soffit of the shared section, so the brace
    # keeps meeting the beam it carries when that section is retuned. Written as
    # 0.40 it happened to sit 60mm under the old soffit and 25mm INSIDE the new
    # one, which is how a "shared" section quietly stops being shared.
    prof = [(0.0, .04), (0.0, zb - .06), (.60, zb - .01), (.60, zb - .17),
            (.30, .19), (.13, .06)]
    p.prism(prof, .19, "oak_dark", axis='Y', at=(-T, 0.0, 0.0), rot=(0, 0, 225),
            bevel=.014, seg=1, tint=.05, shade=.90)
    # ---- THE SILL, TURNING THE CORNER: one mitred L of timber and one mitred
    #      L of weather board, swept from the profile beams.py owns. Both keep
    #      B.SILL_TONE / B.SILL_CAP_TONE flat, with no per-prism jitter: the run
    #      pieces do too, and an 8% tone step between two butted timbers draws
    #      the joint as clearly as a groove does. The board still beds
    #      B.SILL_CAP_LAP down INTO the timber, because its lower arris is the
    #      shadow line the eye follows along the whole jetty and that line has
    #      to leave the corner at the height it arrives at.
    for board in (False, True):
        fr, bk = B.sill_corner_rails(T, board=board)
        B.sweep(p, fr, bk, B.sill_bands(dz=DZ, board=board),
                "oak_mid" if board else "oak_dark",
                shade=B.SILL_CAP_TONE if board else B.SILL_TONE,
                fall=B.sill_fall(board))
    # ---- the floor plate closing the cell behind the two sills, the same
    #      dark straight plate SM_Beam_JettySill_2m_* carries (_sill_back), so
    #      the joist line runs on through the corner
    _bx(p, (bx - GAP, 0.0), (by - GAP, T), (zb, zt), "oak_dark", bevel=0,
        tint=.03, shade=.62)
    # ---- pale stone corbels breaking out of the MASONRY BELOW -- so they are
    #      set out from the stone storey's faces (`so` proud of this cell's),
    #      standing 0.13 clear of them, with their heads buried GAP up inside
    #      the sill soffit so they meet it rather than land on its plane.
    #      They used to be measured off the cell, which put the return pair
    #      inside the stone instead of breaking out of it.
    for xx in (-0.10, -0.27):
        _bx(p, (xx - .0675, xx + .0675), (-so - .130, -so + .030),
            (zb + GAP - .115, zb + GAP), "stone_pale", bevel=.011, seg=1,
            tint=.07, shade=.96 + r.uniform(-.06, .06))
    for yy in (0.155, -0.015):
        _bx(p, (-T - so - .130, -T - so + .030), (yy - .0675, yy + .0675),
            (zb + GAP - .115, zb + GAP), "stone_pale", bevel=.011, seg=1,
            tint=.07, shade=.96 + r.uniform(-.06, .06))
    _bx(p, (-T - so - .155, -T - so + .045), (-so - .155, -so + .045),
        (0.0, .11), "stone_pale", bevel=.012, seg=1, tint=.07,
        shade=1.0)                                       # pad under the brace
    # ---- pegs: the lap the mitre no longer shows. A real dragon-beam corner
    #      is pegged through both ways, and the pegs are where the eye reads
    #      the joinery now that there is no line to read it from.
    _pegs(p, (-out + .175, fy + .01, (zb + zc) / 2), n=2, axis='Y', seed=5)
    _pegs(p, (fx + .01, -J + .175, (zb + zc) / 2), n=2, axis='X', seed=6)
    _pegs(p, (-T - .085, -.085, (zb + zc) / 2 + .055), n=1, axis='Y', seed=7)
    _wobble_pin_butts(p, T, .005, freq=1.5, full=True)
    return p.finish()


# ============================================================== inner corner =
def inner_corner(name="SM_Corner_StoneInner", seed=1):
    """Re-entrant (270 deg) corner: the armpit where a wing meets the main range.
    Only the y=0 face is exposed here -- the crease runs up the x=-T edge, where
    the wing's own facade plane carries on -- so the dressed jamb blocks tooth
    into that crease and an oak corbel at the head catches the roof valley.

    The field beside the jamb is laid by SW.course_run(), i.e. by stone_walls
    itself: same beds, same block sizes, same relief, same joints. It used to be
    a p.stones() cobble field on a course of its own, so the one piece whose
    whole job is to be inconspicuous between two wall runs was the piece that
    looked least like them."""
    T, H = TS, HG
    p = Part(name, budget="corner", seams=_seams(T, H), outward="xy")
    r = rng(name)
    # x=-T is a BUTT plane here, not an exposed face: the wing's facing carries
    # straight on through it, so the core has to reach it
    _core(p, T, SW.HEAD_Z + GAP, mort_x=False)   # laps up into _head_L
    _skim(p, T, H)
    _plinth_L(p, T, seed=seed, wrap=False)
    jw = 0.175                                   # dressed jamb width
    rows = list(SW.ROWS_A) + list(SW.ROWS_B)
    for i, (zb, zt) in enumerate(rows):
        if SW.BAND_Z0 - .01 < zb < SW.SILL_Z:    # the band owns that course
            continue
        tooth = .026 if i % 2 == 0 else 0.0      # toothing in and out
        _bx(p, (-T, -T + jw), (-Q_PROUD - tooth, Q_DEEP),
            (zb + SW.JOINT / 2, zt - SW.JOINT / 2),
            "stone_pale" if r.random() > .30 else "stone_warm",
            bevel=Q_BEV, seg=1, tint=.075, rot=(0, r.uniform(-.5, .5), 0),
            shade=.98 + r.uniform(-.09, .09))
    # the field between the jamb and the butt plane, laid by stone_walls. mortar
    # off: this cell's joint plane is its own core, at the same Q_MORT depth, and
    # a second plate on it would be a coplanar pair the width of the piece.
    x0 = -T + jw + SW.JOINT
    for rows_, key in ((SW.ROWS_A, "A"), (SW.ROWS_B, "B")):
        SW.course_run(p, x0, 0.0, rows_, f"{name}/{key}", mortar=False,
                      small=.24, long=.10, split=.10)
    _band_L(p, T)
    _head_L(p, T)
    # oak valley corbel in the crease, projecting outward on -Y. Both solids
    # are kept off the core's x=-T and y=0 planes, and the bracket's reach is
    # inside PROUD_MAX -- at 0.235 it was clamped back to 0.16, which planted it
    # on the same plane as the block above it.
    _bx(p, (-T + .012, -T + .222), (-.152, .048), (H - .50, H - .30),
        "oak_dark", bevel=.014, seg=1, tint=.05, shade=.90)
    prof = [(.020, 0.0), (-.135, 0.0), (-.05, -.31), (.020, -.34)]
    p.prism(prof, .18, "oak_dark", axis='X', at=(-T + .105, .0, H - .40),
            bevel=.012, seg=1, tint=.05, shade=.82)
    _wob(p, freq=1.4)
    return p.finish()


# ===========================================================================
# THE TIMBER GALLERY  (r10, r8, r7)
# ===========================================================================
# r10 and r8 both run an EXTERNAL GALLERY along the upper floor over an open
# ground floor, and r7 -- the 3D render, i.e. the one in the set that shows what
# is actually reachable in geometry -- draws the whole thing in one crop: a
# heavy edge beam on posts, joists behind it, a boarded deck, and a balustrade
# of balusters between newels with a handrail and a bottom rail. r9 has the same
# idea as a shallow balcony on brackets. r10 adds the other half of it: an
# OUTSIDE STAIR against the wall, with a handrail, climbing to the gallery. The
# kit had none of it.
#
# WHY IT LIVES IN corners.py. This family already owns the standing timber (the
# jowled corner posts) and the jetty joint, and a gallery is the same trade:
# posts, a beam, joists, a deck, a rail. It is also the same INTERFACE problem
# the round-7/8 notes above are about -- a gallery that invents its own storey
# height, its own post section or its own chamfer is a foreign piece bolted onto
# the elevation, exactly as the quoins were. So every number below is either
# spec's or beams.py's:
#
#   the storey line   GA_TOP == spec.H_GROUND. The deck's TOP FACE is the storey
#                     line, so the gallery floor and the upper storey's floor
#                     are one floor and a door opens straight onto it.
#   the deck          built the way beams.jetty_soffit builds the jetty's floor:
#                     boards over joists over a beam; joists bedding GAP up INTO
#                     the boards (B.JS_JTOP's rule); the boards' top held GAP
#                     UNDER the storey line so the wall standing on that line
#                     cannot z-fight them (B.JS_TOP's rule); joists on
#                     B.JS_PITCH = GRID/5 with THE SEAM FALLING MID-BAY between
#                     two of them.
#   the section       every long timber is a CHAMFERED-RECTANGLE SECTION
#                     extruded (_cham_rect), chamfer B.CHAM, never a bmesh
#                     bevel -- see jetty_joint()'s note: a bevel chamfers the
#                     END faces too, so two rails butted at a bay seam meet
#                     chamfer to chamfer and draw a V-groove down every module
#                     boundary. Extruded, the butt faces are dead flat.
#   the posts         B.oct_shaft: square at both ends with the four chamfers
#                     running out of them over B.CHAM_RET. That STOP CHAMFER is
#                     the most legible carpentry in the kit and it is the same
#                     stop the porch post and the wall studs carry.
#   the braces        B._arch_brace through B.wprism, i.e. corbel_knee's worked
#                     timber: a real stop-chamfer round the outline, dying at
#                     the foot and at the head because those two ends are
#                     tenons and a chamfer that runs into a joint is exactly
#                     what makes hand carpentry look extruded.
#   the pegs          B._pegs -- riven oak, tapered, standing proud, oak_pale.
#                     NOT this file's _pegs(): those are oak_dark, which is the
#                     one thing you cannot see in SOLID shading, and beams.py
#                     settled that kit-wide in its round 9. The five older
#                     pieces keep theirs; re-pegging verified work is not this
#                     round's job, and saying so is cheaper than half-doing it.
#
# TILING. A run of SM_Corner_GalleryBay_2m tiles at GRID: the bressumer, the
# ledger, the handrail and the bottom rail run the full module and butt END TO
# END on x = +-GRID/2 with flat cut faces, the deck boards cross the seam and
# are cut flat there by clamp_to_seams (which is what a boarded floor does at a
# joint anyway), and the ONE post per module stands at the bay CENTRE, where it
# can throw a brace both ways. A post on the seam would be half in each module,
# which spec.py forbids, and would put half a chamfer stop on a butt plane.
#
# THE BALUSTRADE RHYTHM is one number, GA_BAL_N = 7 stations a module: six
# balusters and, at the middle station, the newel -- which IS the post, carried
# up through the deck. Odd on purpose: an even count has no middle station, so
# the newel would have to displace the rhythm and a run would read as a repeat
# every 2 m instead of as a continuous balustrade. The gap across the seam is
# one station like every other gap.
#
# TRI BUDGET. These three declare the WALL and GROUND caps, not the CORNER one,
# and that is a size class rather than a family name: spec.TRI_BUDGET exists so
# that no one piece eats the kit ("the point of the per-piece cap is to stop any
# one piece eating the budget"). A corner post is a 0.36 m cell; a gallery bay
# is a GRID-wide, storey-tall module that stands in for a wall bay, and the
# stair is a stair, which the kit budgets at "ground" -- that collection is
# literally 13_Ground_Stairs. All three land well inside their cap.
GA_D     = 1.20                     # deck depth, wall face to the outer plane
GA_TOP   = HG                       # 3.00 -- THE STOREY LINE the deck meets
GA_DKT   = GA_TOP - GAP             # 2.994 deck top: GAP under the storey line
GA_DK_T  = 0.038                    # floorboard thickness -- OF THE THINNEST
                                    # BOARD, not of the average one
GA_DK_V  = 0.010                    # ... and how much thicker one may be hewn.
# THE JITTER IS ONE-SIDED, and that is a round-12 fix. It used to be
# GA_DK_T * (1 + u(-.14, .10)), i.e. +-5 mm either side of GA_DK_T, while GA_DKS
# below is computed from GA_DK_T alone -- so half the boards came out THINNER
# than nominal, their soffits rose ABOVE GA_DKS, and they ate the whole GAP that
# the joists and the bressumer lap up into them by. Measured on the built mesh at
# the 0.5 mm engine pass: board soffits landing anywhere in 2.9537..2.9611
# against beam and joist tops at 2.9552..2.9638 -- five coincident pairs and
# ~1400 cm2 on SM_Corner_GalleryCorner, two more on SM_Corner_GalleryBay_2m, and
# WHICH of them are inside 0.5 mm changes with the noise field, which is the
# worst kind of fault: real, and different on every build.
# A board may now only ever be THICKER than nominal, so GA_DKS is the HIGHEST any
# soffit can reach and the lap is never less than GAP. The deck's variation is
# unchanged in kind -- tops flush, thickness varying downward, which is what
# _gal_deck always claimed -- it just no longer varies upward through the joint.
GA_DKS   = GA_DKT - GA_DK_T         # 2.956 the HIGHEST a board soffit reaches
GA_JT    = GA_DKS + GAP             # 2.962 joists bed GAP up INTO the boards
GA_JD    = 0.185                    # joist depth
GA_JW    = B.JS_JOIST_W             # 0.138 -- the kit's floor joist width
GA_JS    = GA_JT - GA_JD            # 2.777 joist soffit
GA_JP    = B.JS_PITCH               # 0.40 -- five a module, seam mid-bay
GA_BMT   = GA_JT                    # 2.962 bressumer top, buried in the deck
GA_BMD   = 0.300                    # ... its depth: the heavy edge beam
GA_BMS   = GA_BMT - GA_BMD          # 2.662 its soffit -- the gallery's shadow
GA_BMW   = 0.220                    # ... and its width through the gallery
GA_LGT   = GA_JS + GAP              # 2.783 ledger top: joists lap GAP into it
GA_LGD   = 0.190
GA_LGW   = 0.200

GA_RTOP  = GA_TOP + 0.95            # 3.95 handrail top
GA_RT    = 0.105                    # handrail depth
GA_RSOF  = GA_RTOP - GA_RT          # 3.845
GA_RW    = 0.150                    # ... and width
GA_BRT   = GA_TOP + 0.205           # 3.205 bottom rail top
GA_BRB   = GA_BRT - 0.100
GA_BRW   = 0.125
GA_CAPT  = GA_RTOP + 0.085          # 4.035 newel cap top
GA_FINT  = GA_CAPT + 0.150          # 4.185 finial top
GA_H     = 4.20                     # declared height of every gallery piece

# THE Y LADDER at the outer edge. Nothing shares a plane with anything (the
# round-8 rule), and the order is the order a carpenter builds in: the beam is
# the outermost thing, the post stands GAP behind its face, the newel behind the
# post, the rails behind the newel, the balusters behind the rails. Five planes,
# 6 mm apart, and every one of them a real reveal rather than a coincidence.
GA_YE    = -GA_D                    # -1.200 the gallery's OUTER PLANE (the beam)
GA_PADT  = 0.155                    # THE STONE PAD'S TOP -- and every post in
# this section is footed GAP INTO it, never ON it. Footed on it, a post's square
# bottom cap (oct_shaft caps its ends square, 0.24-0.27 across) and the pad's top
# face are one plane, and it is one of the biggest single faces either solid has:
# measured at the 0.5 mm engine pass, 731 cm2 on SM_Corner_GalleryCorner and 573
# cm2 on SM_Corner_GalleryBay_2m. gallery_stair() found and fixed its own copy of
# this last round -- 386 cm2, and its comment says so -- but the fix went into
# one of the three places that butt a post onto a pad. These two are the other
# two, and the corner's 731 is the whole of what the family reports.
#
# WORTH KNOWING ABOUT THE MEASUREMENT: check_zfight buckets faces by their normal
# ROUNDED TO 2 dp, so the bay's pair is invisible to it even at a 20 mm
# tolerance -- the two faces' wobbled normals are (0.0002, -0.0050, -1) and
# (-0.0002, 0.0047, 1), which round to y = -0.01 and y = -0.00 and land in
# different buckets. Probed directly they are 0.11 mm apart over 573 cm2. So the
# family's reported number was never the whole of its coincident surface, and
# "the tool says zero" is not the same claim as "nothing is coincident".
GA_PW0   = 0.120                    # post half-width across the flats, foot
GA_PW1   = 0.106                    # ... at the head
GA_PY    = GA_YE + GAP + GA_PW0     # -1.074 the post/newel axis
GA_NW    = 0.106                    # newel half-width; no taper, because it has
                                    # to present ONE plane to the rails
GA_YR    = GA_PY - GA_NW + GAP      # -1.174 balustrade outer face
GA_YB    = GA_YR + GAP              # -1.168 baluster outer tangent
GA_BAL_R = 0.052                    # baluster max radius
GA_BAL_N = 7                        # balustrade stations a module (see above)
GA_BAL_P = S.GRID / GA_BAL_N        # 0.2857 station pitch
GA_NOSE  = 0.0125                   # how far the corbel blocks under the beam
                                    # are bedded back INTO its face


def _cham_rect(a, b, c):
    """A CHAMFERED-RECTANGLE SECTION, a x b, its four arrises cut back by c,
    centred on the origin. THE section for every long timber in the gallery.

    A section and not a bevel on purpose: bmesh.ops.bevel chamfers a primitive's
    END faces as well as its long arrises, so two rails butted at a bay seam
    meet chamfer to chamfer and leave a V-groove across the joint -- beams.py's
    finding, quoted in jetty_joint() above. Extruded, this leaves both ends dead
    flat and puts the chamfer only where a chamfer belongs."""
    ha, hb = a / 2.0, b / 2.0
    c = min(c, a * .40, b * .40)
    return [(-ha + c, -hb), (ha - c, -hb), (ha, -hb + c), (ha, hb - c),
            (ha - c, hb), (-ha + c, hb), (-ha, hb - c), (-ha, -hb + c)]


def _gtim(p, axis, u0, u1, ctr, a, b, mat="oak_dark", cham=None, cf=0.0,
          cb=0.0, tint=.05, shade=1.0, seed=0):
    """One long gallery timber: _cham_rect extruded from u0 to u1 along `axis`.

    `ctr` and (a, b) are given in the PRISM'S OWN (u, v) frame, which is the two
    axes that are not `axis`, in xyz order: along X that is (y, z), along Y it
    is (x, z), along Z it is (x, y). cf/cb chamfer the two END faces (B.wprism),
    so a timber with a free end can be stopped and one that butts a seam is left
    flat -- which is the whole point of building it this way round."""
    poly = _cham_rect(a, b, B.CHAM if cham is None else cham)
    um = (u0 + u1) / 2.0
    at = {'X': (um, ctr[0], ctr[1]), 'Y': (ctr[0], um, ctr[1]),
          'Z': (ctr[0], ctr[1], um)}[axis]
    return B.wprism(p, poly, abs(u1 - u0), mat, axis=axis, at=at, cf=cf, cb=cb,
                    wear=B.WEAR * .5, seed=f"{p.name}/gtim/{seed}", tint=tint,
                    shade=shade)


def _shaft(p, x, y, z0, z1, w0, w1, mat="oak_dark", ret=.090, mids=3,
           tint=.055, shade=1.0, seed=0):
    """A stop-chamfered octagonal post at (x, y). B.oct_shaft is built on the
    world Z axis and takes no location, so it goes into a scratch Part and is
    merged into place -- util's own "build a detail once and repeat it"."""
    s = p.sub(f"{p.name}/shaft/{seed}")
    B.oct_shaft(s, z0, z1, w0, w1, mat, ret=ret, mids=mids, tint=tint,
                shade=shade, seed=seed)
    p.merge(s, at=(x, y, 0.0))
    s.bm.free()
    s.bm = None


def _baluster(p, x, y, z0, z1, seed=0, sides=8):
    """ONE TURNED BALUSTER -- vase, waist, vase, on an octagonal turning.

    Octagonal rather than round, and stylised hard: the kit is inspected in
    SOLID shading, where colour is not drawn at all, so a baluster only exists
    if its SILHOUETTE swells and pinches. Eight sides against SMOOTH_ANG = 34
    deg keeps every facet flat, so the turning reads across the face as well as
    round the edge."""
    L = z1 - z0
    r = rng(f"{p.name}/bal/{seed}")
    prof = [(.80, .00), (1.0, .17), (.55, .43), (.94, .69), (.55, .87),
            (.70, 1.0)]
    p.lathe([(rr * GA_BAL_R, hh * L) for (rr, hh) in prof], "oak_dark",
            at=(x, y, z0), sides=sides, axis='Z', tint=.05,
            shade=.95 + r.uniform(-.05, .06))


def _finial(p, x, y, z0, z1, seed=0, w=0.086):
    """A newel's acorn. r10's gallery newels all carry a shaped cap and a little
    turned head, and at any distance that is most of what the balustrade's
    silhouette is made of."""
    L = z1 - z0
    r = rng(f"{p.name}/finial/{seed}")
    prof = [(.86, .00), (1.0, .16), (.62, .42), (.70, .60), (.22, .88),
            (.0, 1.0)]
    p.lathe([(rr * w * (1 + r.uniform(-.04, .04)), hh * L) for (rr, hh) in prof],
            "oak_dark", at=(x, y, z0), sides=6, axis='Z', tint=.05,
            shade=1.02 + r.uniform(-.04, .04))


def _newel_head(p, x, y, seed=0, w=GA_NW):
    """Cap block + acorn over a newel: the chamfered abacus the handrail dies
    into, then the head."""
    _gtim(p, 'Z', GA_RTOP - GAP, GA_CAPT, (x, y), (w + .050) * 2,
          (w + .050) * 2, cham=.020, cb=.016, shade=1.05, seed=f"cap{seed}")
    _finial(p, x, y, GA_CAPT - GAP, GA_FINT, seed=seed, w=w * .80)


def _brace(p, plane, face, soffit, run, off, drop=.74, w=.155, thick=.140,
           mat="oak_dark", shade=.93, seed=0):
    """A curved knee brace springing off a post into the beam it carries.

    B._arch_brace's outline (leaves the post plumb, meets the beam level, soffit
    concave toward the corner the two make, spandrel left open) worked through
    B.wprism, i.e. corbel_knee's timber: a real stop-chamfer round the outline
    that DIES at the foot and at the head, because those two ends are tenons.

    `plane` 'Y' lays the brace in the X-Z plane with its thickness through Y at
    `off`; 'X' lays it in the Y-Z plane with its thickness through X. `face` is
    the post face it springs from, `run` its reach along the beam (signed)."""
    A = (face, soffit)
    F = (face, soffit - drop)
    D = (face + run, soffit)
    poly = B._arch_brace(A, F, D, w=w, arc=.20, n=6)
    at = (0.0, off, 0.0) if plane == 'Y' else (off, 0.0, 0.0)
    B.wprism(p, poly, thick, mat, axis=plane, at=at, cf=B.CHAM * .85,
             cb=B.CHAM * .85, tint=.06, shade=shade,
             seed=f"{p.name}/brace/{seed}",
             cw=lambda u, v: clamp(min((abs(u - face) - .080) / .055,
                                       (soffit - .045 - v) / .050)))


def _gal_deck(p, x0, x1, y0, y1, n=6, seed=0, mat="oak_mid"):
    """THE BOARDED DECK -- boards along X, banded across the depth, their TOPS
    flush at GA_DKT and only their thickness varying downward.

    That is B._deck's rule and B._deck's reason: a floor is levelled whatever
    the boards do underneath, and nothing here may foul the plane the wall
    stands on. The joints are real gaps rather than a change of tone, because
    SOLID shading does not draw tone.

    "Only downward" is now literally true of the thickness as well -- see
    GA_DK_V. A board thinner than GA_DK_T would lift its soffit above GA_DKS,
    which is the plane the joists and the bressumer are lapped GAP up through."""
    r = rng(f"{p.name}/deck/{seed}")
    for i in range(n):
        va = lerp(y0, y1, i / n) + (0.0 if i == 0 else .0045)
        vb = lerp(y0, y1, (i + 1) / n) - (0.0 if i == n - 1 else .0045)
        t = GA_DK_T + GA_DK_V * r.random()
        p.plate(((x0 + x1) / 2, (va + vb) / 2, GA_DKT - t / 2),
                (x1 - x0, vb - va, t), mat, tint=.05,
                shade=.94 + r.uniform(-.05, .05))


def _gal_deck_y(p, x0, x1, y0, y1, n=6, seed=0, mat="oak_mid"):
    """The same deck for a run whose wall lies along Y: boards run along Y and
    band across X. The corner needs both, and the change of direction where they
    meet is a trimmer joint -- which is what a boarded deck really does where
    two runs turn a corner."""
    r = rng(f"{p.name}/decky/{seed}")
    for i in range(n):
        ua = lerp(x0, x1, i / n) + (0.0 if i == 0 else .0045)
        ub = lerp(x0, x1, (i + 1) / n) - (0.0 if i == n - 1 else .0045)
        t = GA_DK_T + GA_DK_V * r.random()      # thicker only -- see GA_DK_V
        p.plate(((ua + ub) / 2, (y0 + y1) / 2, GA_DKT - t / 2),
                (ub - ua, y1 - y0, t), mat, tint=.05,
                shade=.94 + r.uniform(-.05, .05))


def _wob_pin(p, planes, amount=.0045, freq=1.5):
    """The family's pinned wobble (see _wob), then put back every vertex that
    was AUTHORED on one of `planes` -- each given as (axis index, value).

    Same argument as _wobble_pin_butts above: util.wobble fades on whole axes,
    and a gallery's butt plane (the wall face y = 0, and on the corner x = 0 and
    y = T) is not an axis the piece tiles on, so it comes out displaced. The
    exposed faces keep their hand-hewn wander; the joints stay flat."""
    keep = [([v for v in p.bm.verts if abs(v.co[i] - c) < 1e-6], i, c)
            for (i, c) in planes]
    _nz.seed_set(SW.NOISE_SEED)
    p.wobble(amount, freq=freq)
    for vs, i, c in keep:
        for v in vs:
            v.co[i] = c


# ------------------------------------------------------- 1. the gallery bay --
def gallery_bay(name="SM_Corner_GalleryBay_2m", seed=1):
    """ONE MODULE OF EXTERNAL TIMBER GALLERY -- r10's and r8's whole upper floor.

    GRID wide, GA_D deep, hung on a wall whose face is y = 0, with its DECK TOP
    ON THE STOREY LINE so it meets the floor inside. Bottom to top it is: a
    stone pad; a stop-chamfered octagonal post standing the full height of the
    open ground floor; two curved braces off it into a heavy bressumer; joists
    at B.JS_PITCH from that beam back to a ledger on the wall, with a corbel
    block breaking out of the beam's face under each of them (r7's run of little
    squares under the deck, and this family's own joist-tooth idiom); a boarded
    deck; and on the outer edge a balustrade of six turned balusters and a newel
    -- the post again, carried up through the deck and finished with a cap and
    an acorn.

    Tile it at GRID and the beams, rails and boards butt end to end, the joist
    rhythm runs on with the seam falling mid-bay, and the balustrade's stations
    step across the joint unbroken. The post lands every 2 m at a bay centre,
    which is where r7 puts them.
    """
    G = S.GRID
    p = Part(name, budget="wall", outward="y",
             seams=dict(x=(-G / 2, G / 2), y=(GA_YE, 0.0), z=(0.0, GA_H)))
    r = rng(f"{name}/{seed}")

    # ---- the post, FOOTED GAP INTO its pad (see GA_PADT), never on it -------
    _shaft(p, 0.0, GA_PY, GA_PADT - GAP, GA_BMS + GAP, GA_PW0, GA_PW1, seed=1)
    _gtim(p, 'Z', 0.0, GA_PADT, (0.0, GA_PY), .335, .335, "stone_pale",
          cham=.020, cb=.014, tint=.08, shade=.98, seed=2)
    # ---- the two curved braces it carries the bressumer on -----------------
    #      Their heads lap GAP UP INTO the beam. Sprung at GA_BMS exactly -- one
    #      number used twice -- each brace's flat top and the bressumer's soffit
    #      were one plane, 149 cm2 measured on this piece at the 1 mm pass, and
    #      the soffit of a gallery is the face you stand under and look at.
    for sgn in (-1, 1):
        _brace(p, 'Y', GA_PW1 * .88 * sgn, GA_BMS + GAP, .60 * sgn, GA_PY,
               seed=f"b{sgn}")
    # ---- THE BRESSUMER: the outer edge beam, full module, butting flat ------
    _gtim(p, 'X', -G / 2, G / 2, (GA_YE + GA_BMW / 2, GA_BMS + GA_BMD / 2),
          GA_BMW, GA_BMD, shade=.92, seed=3)
    # ---- the ledger. It REACHES y = 0, the butt plane: nothing stops short of
    #      a butt plane (round 8), or the deck opens a slot along the wall
    _gtim(p, 'X', -G / 2, G / 2, (-GA_LGW / 2, GA_LGT - GA_LGD / 2),
          GA_LGW, GA_LGD, shade=.86, seed=4)
    # ---- joists at B.JS_PITCH, the seam falling MID-BAY between two of them.
    #      They lap GAP down into the ledger and stop GAP short of the
    #      bressumer's back, so neither joint is a shared plane
    for i in range(5):
        x = -G / 2 + GA_JP * (i + .5)
        _gtim(p, 'Y', GA_YE + GA_BMW + GAP, 0.0, (x, GA_JS + GA_JD / 2),
              GA_JW, GA_JD, cham=.024, tint=.045,
              shade=.88 + r.uniform(-.04, .04), seed=f"j{i}")
    # the corbel blocks stand under the JOISTS, so their stations are the
    # joists' stations: dentil() spaces n blocks evenly across the range given,
    # so the range is the WHOLE module and not the first-to-last joist -- over
    # (-0.8, 0.8) the pitch came out 0.32 and the gap across the bay seam 0.72,
    # which is a rhythm that visibly stumbles at every module line
    p.dentil((-G / 2, G / 2), GA_BMS + .062, GA_YE - GA_NOSE, "oak_dark", n=5,
             size=(.082, .086, .118), tint=.05, seed=6)
    # ---- the deck ----------------------------------------------------------
    _gal_deck(p, -G / 2, G / 2, GA_YE, 0.0, n=6, seed=seed)

    # ---- THE BALUSTRADE ----------------------------------------------------
    _gtim(p, 'X', -G / 2, G / 2, (GA_YR + GA_RW / 2, GA_RSOF + GA_RT / 2),
          GA_RW, GA_RT, cham=.022, shade=1.04, seed=7)              # handrail
    _gtim(p, 'X', -G / 2, G / 2, (GA_YR + GA_BRW / 2, (GA_BRB + GA_BRT) / 2),
          GA_BRW, GA_BRT - GA_BRB, cham=.020, shade=.90, seed=8)   # bottom rail
    for i in range(GA_BAL_N):
        if i == GA_BAL_N // 2:              # the middle station is the newel,
            continue                        # and the newel is the post
        _baluster(p, -G / 2 + GA_BAL_P * (i + .5), GA_YB + GA_BAL_R,
                  GA_BRT - 2 * GAP, GA_RSOF + 2 * GAP, seed=f"{seed}/{i}")
    _shaft(p, 0.0, GA_PY, GA_BMS + .090, GA_RSOF + 3 * GAP, GA_NW, GA_NW * .95,
           mids=2, seed=9)
    _newel_head(p, 0.0, GA_PY, seed=seed)

    # ---- pegs: the bressumer into the post, the rails into the newel. These
    #      are B._pegs, the kit's riven oak trenail -- pale, tapered, standing
    #      proud of the face it is driven into, i.e. the only kind of peg that
    #      can be seen at all in SOLID shading
    B._pegs(p, (-.245, .245), GA_YE, GA_BMS + .155, r_=.024, axis='Y')
    B._pegs(p, (0.0,), GA_YE, GA_BMS + .155, r_=.026, axis='Y')
    B._pegs(p, (0.0,), GA_PY - GA_NW, GA_RSOF - .080, r_=.020, axis='Y')
    B._pegs(p, (0.0,), GA_PY - GA_NW, GA_BRB + .048, r_=.020, axis='Y')
    _wob_pin(p, [(1, 0.0)], .0045, freq=1.5)
    return p.finish()


# ---------------------------------------------------- 2. the gallery corner --
def gallery_corner(name="SM_Corner_GalleryCorner", seed=1):
    """THE GALLERY TURNING A CORNER -- r10's does exactly this over the porch.

    It fills the square OUTSIDE the building's own T x T corner cell:
    x in [-T-GA_D, 0], y in [-GA_D, T], with the cell itself (x in [-T, 0],
    y in [0, T]) left empty for the corner post of the storey above, so the deck
    is an L wrapping the building's arris. That is the same declared box as
    SM_Corner_JettyJoint's -- the corner cell grown outward -- and the same
    cell, B.SILL_CELL == T_TIMBER, for the same reason: a gallery hangs on a
    TIMBER storey. Snap it at the same origin as SM_Corner_TimberPost and the
    two runs butt on x = 0 and y = T, which is where a GalleryBay's beams,
    rails, ledger and boards end.

    ONE chunky corner post carries both bressumers, so neither beam has to show
    an end on an exposed plane, and it comes up through the deck as the corner
    newel with both handrails dying into it. Everything on the return elevation
    is offset GAP in z from its twin on the front: two beams crossing at a
    corner otherwise share their SOFFIT plane, and a gallery's soffit is the one
    face you are always looking up at.
    """
    T = B.SILL_CELL                       # 0.24 -- the timber storey's cell
    XE = -T - GA_D                        # -1.44 the return elevation's plane
    p = Part(name, budget="wall", outward="xy",
             seams=dict(x=(XE, 0.0), y=(GA_YE, T), z=(0.0, GA_H)))
    r = rng(f"{name}/{seed}")
    CW0, CW1, CNW = .135, .120, .122      # the corner post is the fatter one
    px = XE + GAP + CW0                   # -1.299 its axis in x
    py = GA_YE + GAP + CW0                # -1.059 ... and in y
    XR = px - CNW + GAP                   # -1.415 return balustrade face
    XB = XR + GAP                         # -1.409 return baluster tangent

    # ---- the corner post, FOOTED GAP INTO its pad (see GA_PADT) ------------
    _shaft(p, px, py, GA_PADT - GAP, GA_BMS + GAP, CW0, CW1, seed=1)
    _gtim(p, 'Z', 0.0, GA_PADT, (px, py), .365, .365, "stone_pale", cham=.020,
          cb=.014, tint=.08, shade=.98, seed=2)
    # each brace's head laps GAP up into the beam it carries -- and the return
    # beam's soffit is itself GAP lower, so its brace springs GAP lower too
    _brace(p, 'Y', px + CW1 * .88, GA_BMS + GAP, .60, py, seed="bx")
    _brace(p, 'X', py + CW1 * .88, GA_BMS, .60, px, shade=.90, seed="by")

    # ---- the two bressumers, dying into the post ---------------------------
    #      The return beam is offset GAP in z from the front one so the two do
    #      not share the soffit you look up at. That offset used to be a bodily
    #      SLIDE, which moved the problem to the top face: at GA_BMS - GAP +
    #      GA_BMD its top landed on GA_DKS, the nominal deck soffit, i.e. the one
    #      plane in the piece it had to stay clear of -- 409 cm2 of oak against
    #      board at the 1 mm pass, the largest of five pairs in that band. So the
    #      return beam is GAP DEEPER AT BOTH ENDS instead: soffit GAP lower than
    #      the front beam's, top GAP higher, both ends still well inside the
    #      boards (they are 38-48 mm thick over a 2.956 soffit). The two beams
    #      cross at the corner, so a shared TOP plane is 28 cm2 of coincidence
    #      there as surely as a shared soffit is 2182 across the whole L.
    _gtim(p, 'X', px, 0.0, (GA_YE + GA_BMW / 2, GA_BMS + GA_BMD / 2),
          GA_BMW, GA_BMD, shade=.92, seed=3)
    _gtim(p, 'Y', py, T, (XE + GA_BMW / 2, GA_BMS + GA_BMD / 2),
          GA_BMW, GA_BMD + 2 * GAP, shade=.90, seed=4)
    # ---- a ledger against each face of the building's corner cell ----------
    _gtim(p, 'X', -T, 0.0, (-GA_LGW / 2, GA_LGT - GA_LGD / 2),
          GA_LGW, GA_LGD, shade=.86, cf=B.CHAM, seed=5)
    _gtim(p, 'Y', 0.0, T, (-T - GA_LGW / 2, GA_LGT - GAP - GA_LGD / 2),
          GA_LGW, GA_LGD, shade=.84, cf=B.CHAM, seed=6)
    # ---- joists, ON THE RUN'S OWN STATIONS. A GalleryBay snapped at x = 0 has
    #      its five joists at GA_JP centres, so walking that grid back through
    #      the corner puts them at -0.2, -0.6, -1.0 and -1.4; the -1.4 one falls
    #      inside the corner post and is not cut. The two clear of the building's
    #      cell carry the return strip as well and run the full depth of the L;
    #      the one inside the cell stops on the front wall's face.
    #
    #      There is deliberately NO second set running the other way. A short
    #      set along X would cross these at the same level and the underside
    #      would read as a criss-cross grid, which is not a floor: the return
    #      strip is only T deep and these two trim it, exactly as a real deck
    #      trims a corner off the longer run's joists.
    for i, x in enumerate((-1.0, -0.6, -0.2)):
        _gtim(p, 'Y', GA_YE + GA_BMW + GAP, T if x < -T - .02 else 0.0,
              (x, GA_JS + GA_JD / 2), GA_JW, GA_JD, cham=.024, tint=.045,
              shade=.88 + r.uniform(-.04, .04), seed=f"j{i}")
    # corbel blocks on the same stations on the front, and on the RETURN run's
    # stations (GA_JP back from its butt plane y = T) on the return
    p.dentil((-1.2, 0.0), GA_BMS + .062, GA_YE - GA_NOSE, "oak_dark", n=3,
             size=(.082, .086, .118), tint=.05, seed=7)
    # two only: dentil()/_teeth_y space n blocks evenly INSIDE the range, so
    # this is the range whose two stations land on T - GA_JP/2 and
    # T - 3*GA_JP/2. A third would sit at -0.96, half buried in the corner post
    _teeth_y(p, (T - 2.5 * GA_JP, T - .5 * GA_JP), XE - GA_NOSE,
             GA_BMS - GAP + .062, "oak_dark", step=GA_JP,
             size=(.086, .082, .118), seed=8)
    # ---- the L of deck -----------------------------------------------------
    #      The return strip starts GAP past y = 0 rather than ON it. The front
    #      strip's last board ends exactly on y = 0 (that is where its run of
    #      deck stops), so a return board starting there met it face to face --
    #      two boards, one plane, 62 cm2 measured. Held GAP off, the trimmer
    #      joint at the arris is a real 6 mm gap, which is what every other joint
    #      in this deck already is (the bands are laid 4.5 mm apart) and what a
    #      boarded floor does where two runs change direction.
    _gal_deck(p, XE, 0.0, GA_YE, 0.0, n=6, seed=seed)          # front strip
    _gal_deck_y(p, XE, -T, GAP, T, n=6, seed=seed + 3)         # return strip

    # ---- the balustrade, both ways, meeting at the corner newel ------------
    _gtim(p, 'X', px, 0.0, (GA_YR + GA_RW / 2, GA_RSOF + GA_RT / 2),
          GA_RW, GA_RT, cham=.022, shade=1.04, seed=9)
    _gtim(p, 'X', px, 0.0, (GA_YR + GA_BRW / 2, (GA_BRB + GA_BRT) / 2),
          GA_BRW, GA_BRT - GA_BRB, cham=.020, shade=.90, seed=10)
    _gtim(p, 'Y', py, T, (XR + GA_RW / 2, GA_RSOF - GAP + GA_RT / 2),
          GA_RW, GA_RT, cham=.022, shade=1.02, seed=11)
    _gtim(p, 'Y', py, T, (XR + GA_BRW / 2, (GA_BRB + GA_BRT) / 2 - GAP),
          GA_BRW, GA_BRT - GA_BRB, cham=.020, shade=.88, seed=12)
    # balusters at a pitch as near the run's GA_BAL_P as the corner's own span
    # allows. A corner is where a balustrade takes up its slack, and 8 mm of
    # pitch is invisible where a station MISSING at the arris would not be.
    for lo, hi, ax in ((px + CNW, 0.0, 'x'), (py + CNW, T, 'y')):
        n = max(1, int(round((hi - lo) / GA_BAL_P)) - 1)
        for i in range(n):
            u = lerp(lo, hi, (i + 1) / (n + 1))
            if ax == 'x':
                _baluster(p, u, GA_YB + GA_BAL_R, GA_BRT - 2 * GAP,
                          GA_RSOF + 2 * GAP, seed=f"cx{i}")
            else:
                _baluster(p, XB + GA_BAL_R, u, GA_BRT - 3 * GAP,
                          GA_RSOF + GAP, seed=f"cy{i}")
    _shaft(p, px, py, GA_BMS + .090, GA_RSOF + 3 * GAP, CNW, CNW * .95,
           mids=2, seed=13)
    _newel_head(p, px, py, seed=seed, w=CNW)
    B._pegs(p, (-.62,), GA_YE, GA_BMS + .155, r_=.024, axis='Y')
    B._pegs(p, (-.62,), XE, GA_BMS + .130, r_=.024, axis='X')
    # one peg into each face of the corner newel. B._pegs' `face` is the PLANE
    # the peg is driven into, so a peg in an x plane is an X-axis peg -- passed
    # as 'Y' it read -1.421 as a y coordinate and put the head 90 mm outside
    # the piece's own box, where clamp_to_seams sliced it flat
    B._pegs(p, (py,), px - CNW, GA_RSOF - .080, r_=.020, axis='X')
    B._pegs(p, (px,), py - CNW, GA_RSOF - .080, r_=.020, axis='Y')
    _wob_pin(p, [(0, 0.0), (1, T)], .0045, freq=1.5)
    return p.finish()


# ----------------------------------------------------- 3. the outside stair --
ST_W     = 1.10                     # flight width, wall face to outer plane
ST_RUN   = 2 * S.GRID               # 4.00 -- THE FLIGHT IS TWO BAYS LONG, so it
                                    # spends a whole number of wall modules
ST_N     = 15                       # risers
ST_RISE  = GA_TOP / ST_N            # 0.200 == ground.RISE, the kit's riser
ST_GO    = ST_RUN / ST_N            # 0.2667 going
ST_SLOPE = ST_RISE / ST_GO          # 0.75
ST_TT    = 0.062                    # tread thickness
ST_NOSE  = 0.032                    # nosing over the step below
ST_K0    = 2                        # first tread carried by the strings; tread
                                    # 1 is a stone block on the ground
ST_BASE  = -1.500                   # x the stone bottom step runs to -- PAST
                                    # where the string starts, so the toe is
                                    # bedded in it and the bottom newel stands
                                    # on it
ST_TOE   = 0.055                    # where the string's toe rests: its underside
                                    # is the straight rake CLAMPED to this, so
                                    # the plank has a flat foot to sit on
                                    # instead of running below the ground plane
ST_SD    = 0.280                    # string depth under the notch beds
ST_YS    = -1.000                   # the outer string's outer face
ST_YSW   = 0.140                    # string thickness
ST_YN    = -ST_W + GAP              # -1.094 newel outer flat
ST_NW    = 0.085                    # newel half-width across the flats
ST_YR    = ST_YN + 3 * GAP          # -1.076 THE RAILS' OUTER FACE. Three GAPs,
                                    # not one: the newel is a TAPERED octagon,
                                    # so its flat travels from -1.094 at the
                                    # foot to -1.088 at the head, and a rail
                                    # face 4 mm off the end of that travel is
                                    # inside the wobble amplitude -- the two
                                    # crossed and left 45 cm2 of coincident
                                    # oak on the middle newel. 18 mm clears the
                                    # whole taper and the wander with it.


def _st_x(k):
    """x of the BACK edge of tread k. Tread ST_N lands on the storey line."""
    return -ST_RUN / 2 + k * ST_GO


def _st_z(k):
    """Top of tread k -- and tread ST_N's top IS GA_DKT, the gallery deck."""
    return GA_DKT - (ST_N - k) * ST_RISE


def _st_line(x, off=0.0):
    """The pitch line through the tread tops at their backs, plus `off`. Every
    raking thing on the stair is stated as an offset from this one line, which
    is why the handrail can be made to land exactly on GA_RTOP."""
    return ST_SLOPE * (x + ST_RUN / 2) + (GA_DKT - ST_N * ST_RISE) + off


def _st_string(p, y, shade=.90):
    """A CUT (open) STRING: a raking plank with a notch sawn for every tread, so
    the flight's silhouette from the side is the staircase itself.

    A closed string would have to stand a full riser above every tread top, and
    would then run 235 mm above the gallery deck at the head -- a rail the
    gallery does not have and cannot meet. A cut string dies level with the
    landing instead.

    Its underside is one straight rake ST_SD below the notch beds, CLAMPED at
    ST_TOE: that rake reaches z = 0 half a metre before the plank does, so
    unclamped the foot of the string is below the ground. The clamp is the knee
    every real string is cut with and it gives the plank a flat foot to stand
    on. Even so there is no plank left under tread 1, which is why tread 1 is a
    stone block on the ground and the string starts at ST_K0 = 2."""
    x0, xn = _st_x(ST_K0 - 1), _st_x(ST_N)
    knee = ((ST_TOE - (GA_DKT - ST_N * ST_RISE) + ST_TT + ST_SD) / ST_SLOPE
            - ST_RUN / 2)                    # where the rake meets the flat foot
    pts = [(x0, ST_TOE), (max(knee, x0 + .02), ST_TOE),
           (xn, _st_line(xn, -ST_TT - ST_SD)), (xn, _st_z(ST_N) - ST_TT)]
    for k in range(ST_N, ST_K0, -1):
        pts.append((_st_x(k - 1), _st_z(k) - ST_TT))
        pts.append((_st_x(k - 1), _st_z(k - 1) - ST_TT))
    pts.append((x0, _st_z(ST_K0) - ST_TT))
    p.prism(pts, ST_YSW, "oak_dark", axis='Y', at=(0.0, y + ST_YSW / 2, 0.0),
            bevel=.010, seg=1, tint=.05, shade=shade)


def gallery_stair(name="SM_Corner_GalleryStair", seed=1):
    """THE OUTSIDE STAIR UP TO THE GALLERY -- r10's strongest single feature.

    ONE STOREY, exactly: fifteen risers of ground.RISE = 0.20 climb
    spec.H_GROUND, and the top tread's face IS the gallery deck (GA_DKT), so the
    flight lands on it with no step and no invented number. Two bays long
    (ST_RUN = 2*GRID), so a level artist spends a whole number of wall modules
    on it and the gallery takes over on the module line where the stair ends,
    which is exactly how r10 lays it out.

    Two cut strings; treads housed in their notches with a chamfered nose and a
    nosing over the step below; the bottom two steps in stone, because a raking
    plank has no depth left down there; a trestle post on a pad at mid span with
    a curved brace each way; and on the open side a raked handrail and mid rail
    on three stop-chamfered newels. THE HANDRAIL LANDS AT GA_RTOP -- the stair
    rail and the gallery rail are the same height where they meet, which is the
    whole reason that 0.956 is derived rather than chosen.
    """
    p = Part(name, budget="ground", outward="y",
             seams=dict(x=(-ST_RUN / 2, ST_RUN / 2), y=(-ST_W, 0.0),
                        z=(0.0, GA_H)))
    r = rng(f"{name}/{seed}")
    ys_out, ys_in = ST_YS, -0.20
    ny = ST_YN + ST_NW                              # the newel line
    tx = _st_x(8)                                   # the trestle's station

    # ---- the two strings -----------------------------------------------
    _st_string(p, ys_out, shade=.90)
    _st_string(p, ys_in, shade=.84)
    # ---- the bottom two steps, in stone: two blocks each, so a joint shows --
    # THE BOTTOM STEP, in stone, AND THE STRING'S BEDDING IN ONE BLOCK.
    #
    # It has to be both. A cut string cannot rest on the step it serves -- the
    # gap between a notch bed and the tread below it is RISE - ST_TT = 138 mm,
    # which is no plank at all -- so the string runs on down PAST the bottom
    # risers to the ground, and the masonry fills what is left. Built as a
    # separate pad beside the toe that read as a boulder dropped next to the
    # stair; run THROUGH the toe (to ST_BASE, past where the string starts) it
    # reads as what it is, a stone step with the timber springing out of it, and
    # it is the pad as well, so there is one pale object at the foot instead of
    # three. It is also what carries the bottom newel.
    #
    # Two stones to it, BONDED rather than butted: they lap 30 mm in y and the
    # inner one is laid 5 mm lower on a 4 mm thicker bed, so no face of one lands
    # on a face of the other. Butted on a shared y plane -- which is what they
    # were -- that joint was 319 cm2 of coincident stone, the worst pair in the
    # family, and the 5 mm it takes to fix reads as hand-laid anyway. The outer
    # stone is SPLAYED 40 mm proud of the flight's own plane, which is what a
    # bottom step does and what keeps it out from behind the string.
    for j, (ya, yb, dz, dx) in enumerate(((-1.14, -0.475, 0.0, 0.0),
                                          (-0.505, 0.0, -.005, .012))):
        xa, xb = -ST_RUN / 2, ST_BASE
        _gtim(p, 'Y', ya, yb,
              ((xa + xb) / 2 + dx, (.004 * j + _st_z(1) + dz) / 2),
              xb - xa - 2 * abs(dx), _st_z(1) + dz - .004 * j,
              "stone" if j else "stone_pale", cham=.022, cf=B.CHAM, tint=.09,
              shade=.96 + r.uniform(-.06, .06), seed=f"s{j}")
    # ---- the treads: chamfered all round, a nosing over the step below, the
    #      outer end stopped and the wall end left square (it is buried)
    #      Its back runs GAP PAST the notch's riser and is buried in the string
    #      above the bed, rather than landing ON that riser: landed on it, every
    #      tread put its back face and its back chamfer in the same plane as the
    #      string it sits in
    for k in range(ST_K0, ST_N + 1):
        # ... except the LANDING tread, whose back is the module line itself:
        # there is no string beyond it to bury the lap in, and x = ST_RUN/2 is
        # a declared snap plane, so it is cut dead flat on it like every other
        # butting piece in the kit
        # ... and its underside is GAP BELOW the notch bed, so it BEDS INTO the
        #     string instead of landing on it. Sitting exactly on the bed -- one
        #     number, used twice -- put a tread's whole underside in the same
        #     plane as the notch it sits in, on both strings, for every tread.
        #     Wobble hid most of them and left one 17 cm2 pair standing, which is
        #     the worst kind of fault: real, and invisible on any given build.
        xa = _st_x(k - 1) - ST_NOSE
        # 2*GAP, not GAP: at one GAP the tread's back-bottom CHAMFER -- a 45
        # degree facet -- landed in the same 45 degree plane as the string's
        # bevel at the notch's re-entrant corner. The lap is buried either way
        xb = _st_x(k) + (2 * GAP if k < ST_N else 0.0)
        _gtim(p, 'Y', -1.04, 0.0,
              ((xa + xb) / 2, _st_z(k) - (ST_TT + GAP) / 2),
              xb - xa, ST_TT + GAP, "oak_mid", cham=.020, cf=B.CHAM * .8,
              tint=.05, shade=.98 + r.uniform(-.05, .05), seed=f"t{k}")
    # ---- the trestle at mid span -------------------------------------------
    tz = _st_line(tx, -ST_TT - ST_SD)
    # The post is footed GAP INTO its pad, not ON it. Landed on it -- which it
    # was -- the shaft's bottom face and the pad's top face were one plane, and
    # at the 0.5 mm pass check_zfight measures for engine depth precision that
    # was 386 cm2. Same fix the timber posts' pad/sole/shaft stack already uses
    # two hundred lines up. It was called "the whole family's remaining
    # coincident surface" here, and that was wrong twice over: the tool was
    # comparing plane offsets along the wrong normals at the time, and the same
    # butt was standing in BOTH gallery pieces, unfixed, for another 1304 cm2.
    # A fix applied to one of three identical joints is a third of a fix; see
    # GA_PADT.
    _shaft(p, tx, ys_out + ST_YSW / 2, .13 - GAP, tz + GAP, .098, .088, mids=2,
           seed=3)
    _gtim(p, 'Z', 0.0, .13, (tx, ys_out + ST_YSW / 2), .305, .305,
          "stone_pale", cham=.018, cb=.012, tint=.08, shade=.98, seed=4)
    for sgn in (-1, 1):
        _brace(p, 'Y', tx + .086 * sgn, tz, .46 * sgn,
               ys_out + ST_YSW / 2, drop=.60, w=.150, thick=.125,
               seed=f"tb{sgn}")

    # ---- the balustrade: three newels, a raked handrail and a mid rail -----
    # .150 back from each module line, not .115: the newel CAP is wider than the
    # newel (it is an abacus), and at .115 its outer corner stood 16 mm past
    # x = GRID, where clamp_to_seams cut it square
    xs = (ST_BASE - .120, tx, ST_RUN / 2 - .150)
    for i, x in enumerate(xs):
        # the bottom newel stands ON the stone step, lapping GAP into it
        z0 = _st_z(1) - GAP if i == 0 else _st_line(x, -ST_TT - ST_SD - .05)
        _shaft(p, x, ny, z0, _st_line(x, 1.02), ST_NW, ST_NW * .93, mids=2,
               seed=f"n{i}")
        _gtim(p, 'Z', _st_line(x, 1.02) - GAP, _st_line(x, 1.10), (x, ny),
              (ST_NW + .046) * 2, (ST_NW + .046) * 2, cham=.018, cb=.014,
              shade=1.05, seed=f"nc{i}")
        _finial(p, x, ny, _st_line(x, 1.10) - GAP, _st_line(x, 1.225),
                seed=f"nf{i}", w=.070)
    for i, (off, w_, d_, sh) in enumerate(((0.956, .150, .105, 1.04),
                                           (0.500, .125, .095, .92))):
        # ONE raked timber per rail: p.beam's section is perpendicular to the
        # rake, which is how a rail is really cut, and its ends butt the newels
        # it dies into. `off` is read off _st_line, so the TOP OF THE HANDRAIL
        # arrives at GA_RTOP on the module line x = ST_RUN/2 -- the stair rail
        # and the gallery rail are the same height where they meet.
        # Each rail's own outer face: ST_YR for the handrail, GAP behind it for
        # the mid rail, so the two never share the plane either
        ry = ST_YR + i * GAP + w_ / 2
        p.beam((xs[0] - .020, ry, _st_line(xs[0] - .020, off - d_ / 2)),
               (ST_RUN / 2 - .045, ry, _st_line(ST_RUN / 2 - .045,
                                                off - d_ / 2)),
               w_, d_, "oak_dark", bevel=.020, seg=1, tint=.05, shade=sh)
    for k in (5, 7, 11, 13):
        x = _st_x(k)
        _gtim(p, 'Z', _st_z(k) - .050, _st_line(x, .930), (x, ny), .078, .078,
              cham=.016, shade=.94, seed=f"sb{k}")
    for k in (6, 12):
        B._pegs(p, (_st_x(k),), ST_YS,
                _st_line(_st_x(k), -ST_TT - ST_SD / 2), r_=.022, axis='Y')
    _wob_pin(p, [(1, 0.0)], .0040, freq=1.6)
    return p.finish()


# ======================================================================= api =
def build():
    return [
        timber_post("SM_Corner_TimberPost_A", w=.345, pad=True, seed=1),
        timber_post("SM_Corner_TimberPost_B", w=.325, jz=.38, jn=2, jk=1.5,
                    straps=3, pad=False, teeth=False, seed=2),
        timber_post("SM_Corner_TimberPost_C", w=.355, jz=.54, jn=5, jk=2.8,
                    bead=.055, collar=2, pad=True, seed=3),
        # THE FULLY-TIMBER PAIR. Same posts, housed feet instead of stone pads:
        # use these at every timber storey ABOVE the first. See the note over
        # FOOT_SH, and the `foot` paragraph in timber_post.
        timber_post("SM_Corner_TimberPost_Tenon_A", w=.345, foot="tenon", seed=4),
        timber_post("SM_Corner_TimberPost_Tenon_B", w=.355, jz=.54, jn=5, jk=2.8,
                    bead=.055, collar=2, foot="tenon", seed=5),
        # no var= here on purpose: the NAME picks the arm (see arch_brace_single)
        arch_brace_single(ARCH_BRACE_ARMS[0]),
        arch_brace_single(ARCH_BRACE_ARMS[1]),
        arch_brace(),
        stone_quoin("SM_Corner_StoneQuoin_A", seed=11),
        stone_quoin("SM_Corner_StoneQuoin_B", rough=.55, phase=1, seed=21),
        jetty_joint(),
        inner_corner(),
        gallery_bay(),
        gallery_corner(),
        gallery_stair(),
    ]


# ------------------------------------------------------------------- context -
# Plain filler bays, built only inside demo() so the corners have something to
# be a corner OF. Not kit pieces: no SM_ prefix, no budget, never exported.
def _ctx_stone_wall(name, seed=1):
    """A plain stone bay, built by stone_walls.plain_bay() -- the actual wall the
    stone corners have to meet, not an imitation of it.

    This is the change that makes the corners demo mean anything. It used to
    build its own p.stones() rubble on its own .27/.295 courses with its own
    plinth at 0.36, so the demo compared the quoins against a wall that exists
    nowhere in the kit: the quoins could line up perfectly with the context and
    still step 200 mm against every real SM_Wall_Stone* piece, which is exactly
    what they did. Context, not a kit piece: no SM_ prefix, never exported."""
    G, T, H = S.GRID, TS, HG
    p = Part(name, seams=dict(x=(-G / 2, G / 2), y=(0, T), z=(0, H)))
    SW.plain_bay(p, seed)
    _wob(p)
    return p.finish()


def _ctx_timber_wall(name, seed=1, braces=True):
    """Cream panels, many narrow mid-brown timbers -- BRIEF: verticals ~0.6m.

    `braces=False` leaves the bay's two arches out, for the runs where demo()
    puts the real SM_Corner_ArchBrace on them instead. Context geometry that
    imitates a kit piece is fine as background; it is not fine standing next to
    the piece it imitates.

    THE TWO BANDS A BRACE IS JOINTED TO ARE THE REAL ONES, read from
    timber_walls, because the demo is where this family's claim that both ends
    of a brace land has to be visible rather than argued:
      * the WALL PLATE is Z_HEAD (2.420..2.600) at PLATE_Y (-0.092), not a
        0.19 band at H-0.095 standing 0.053 proud. On the old band the brace's
        head -- correctly housed in the real plate -- came out 1 mm in FRONT of
        the context plate's face, so the demo showed the piece poking through the
        very member that is supposed to swallow it;
      * the SEAM POSTS are W_POST (0.160) at POST_Y (-0.080), centred on the
        tiling plane so two bays make one post. The arcade's braces spring off
        their faces and bury their feet in them, and a 0.145 stud inset 12 mm
        from the seam is not the thing they land in on a real wall.
    Everything else here stays a stand-in."""
    G, T, H = S.GRID, TT, HU
    p = Part(name, seams=dict(x=(-G / 2, G / 2), y=(0, T), z=(0, H)))
    r = rng(name)
    p.plate((0, T / 2 + .014, H / 2), (G, T - .028, H), "plaster", tint=.05,
            shade=.92)
    tw, td = .130, .052
    pby, pbk = TW.POST_Y, TW.POST_BACK
    p.box((0, -td / 2 + .004, .080), (G, td + .01, .16), "oak_dark", bevel=.012,
          seg=1, tint=.05, shade=.86)                        # sole plate
    p.box((0, (TW.PLATE_Y + TW.BY + TW.BD) / 2, (PLATE_SOF + PLATE_TOP) / 2),
          (G, TW.BY + TW.BD - TW.PLATE_Y, PLATE_TOP - PLATE_SOF), "oak_dark",
          bevel=.012, seg=1, tint=.05, shade=.98)            # wall plate
    p.dentil((-G / 2 + .06, G / 2 - .06), PLATE_SOF - .046, TW.PLATE_Y * .72,
             "oak_dark", step=.112, size=(.05, .085, .05), tint=.05, seed=2)
    p.box((0, -td / 2 + .004, 1.40), (G, td + .008, .150), "oak_dark",
          bevel=.011, seg=1, tint=.05, shade=.90)            # mid rail
    for sx in (-1, 1):
        # HALF-posts, built timber_walls' way: half a W_POST reaching SEAM_CUT
        # past the tiling plane and cut flat on it, so two bays make one 0.160
        # post and the arris chamfer dies before the seam instead of surviving it
        # as a facet. Built as a full-width box centred on the seam it clamps 80
        # mm rather than 30 and prints a CLAMP line that reads like a fault.
        hw = TW.W_POST / 2 + TW.SEAM_CUT
        p.box((sx * (G / 2 - TW.W_POST / 4 + TW.SEAM_CUT / 2), (pby + pbk) / 2,
               (.08 + PLATE_SOF) / 2),
              (hw, pbk - pby, PLATE_SOF - .08), "oak_dark", bevel=.011,
              seg=1, tint=.05, shade=.88 + r.uniform(-.04, .06))
    for x in (-G / 6, G / 6):                                # field studs
        p.box((x, -td / 2 + .002, H / 2), (tw, td, H - .28), "oak_dark",
              bevel=.011, seg=1, tint=.05, shade=.88 + r.uniform(-.04, .06))
    for sx in (-1, 1):
        p.beam((sx * (G / 2 - .07), -td / 2, .22), (sx * (G / 2 - .58), -td / 2, 1.30),
               tw, td, "oak_dark", bevel=.010, seg=1, tint=.05, shade=.86)
    # arched braces under the wall plate at both bay ends, so the corner post's
    # own arches (SM_Corner_ArchBrace_Pair) read as one continuous arcade -- ref3.
    # Seated by _brace_seat like the real piece, off the seam post's face, so the
    # context arches land the way the kit ones do instead of nearly doing so.
    for sx in ((-1, 1) if braces else ()):
        # -sx: they spring from the bay ENDS toward the middle. Signed the other
        # way they ran straight off the bay and were clamped flat at the seam.
        poly, _m, zt = _brace_seat(run=.80, tw=.125, adze=.11, seed=f"ctx{sx}")
        p.prism([(-sx * u, v) for (u, v) in poly], BR_DEEP, "oak_dark", axis='Y',
                at=(sx * (G / 2 - TW.W_POST / 2), BR_MID_Y, zt),
                bevel=.012, seg=1, tint=.05, shade=.94)
    _wob(p, .006)
    return p.finish()


def _ctx_sill(name, length):
    """Jetty sill beam along a run (the beams family owns the real one).

    Context, but SWEPT FROM THE REAL SECTION -- B.sweep() through B.sill_bands()
    on straight rails -- not modelled to look like it. It is the thing
    SM_Corner_JettyJoint butts against in this demo, so a stand-in that is a
    different depth, or one whose ends are bevelled when the real piece's are
    cut flat, makes the CORNER look like the piece that is wrong. Same frame as
    the real run piece too -- y=0 is the wall face, z=0 the soffit datum -- so it
    is placed the way a sill is placed: at storey_top - SILL_H. Straight, not
    swagged; the swag belongs to the real piece."""
    p = Part(name, seams=None)
    for board in (False, True):
        f = B.SILL_FACE - (B.SILL_CAP_O if board else 0.0)
        fr = [((-length / 2, f), (0., 1.), 1.), ((length / 2, f), (0., 1.), 1.)]
        bk = [((-length / 2, B.SILL_BACK), (0., -1.), 1.),
              ((length / 2, B.SILL_BACK), (0., -1.), 1.)]
        B.sweep(p, fr, bk, B.sill_bands(board=board),
                "oak_mid" if board else "oak_dark",
                shade=B.SILL_CAP_TONE if board else B.SILL_TONE,
                fall=B.sill_fall(board))
    n = max(2, int(length / .62))
    for i in range(n):
        x = lerp(-length / 2 + .34, length / 2 - .34, i / max(1, n - 1))
        p.box((x, -.05, B.SILL_SOF + GAP - .0575), (.135, .16, .115),
              "stone_pale", bevel=.011, seg=1, tint=.07, shade=.96)
    return p.finish()


def _ctx_eave(name, length):
    p = Part(name, seams=None)
    p.box((0, 0, 0), (length, .30, .17), "oak_dark", bevel=.014, seg=1, tint=.05)
    p.dentil((-length / 2 + .06, length / 2 - .06), -.115, -.19, "oak_dark",
             step=.112, size=(.05, .085, .05), tint=.05)
    return p.finish()


def demo():
    """South-east corner of an inn: quoined stone base, a jettied half-timber
    storey, the jetty joint carrying it, and the armpit of a lower wing on the
    left, dressed with the inner corner.

    ... and, over the ground floor, THE GALLERY: an outside stair up the front
    elevation, the gallery turning the south-east corner on its own post, and
    two bays running on up the east elevation. That is r10's arrangement, and
    it is the only thing that proves the three new pieces: that a run of bays
    tiles at GRID into a continuous balustrade, that the corner takes both runs
    without a step, and that the flight's top tread arrives on the deck."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []

    def dup(o, loc, rz=0.0):
        c = o.copy()
        c.data = o.data
        bpy.context.scene.collection.objects.link(c)
        c.location = loc
        c.rotation_euler = (0, 0, radians(rz))
        out.append(c)
        return c

    def put(nm, loc, rz=0.0):
        return dup(src[nm], loc, rz)

    sw = [_ctx_stone_wall(f"_ctx_stone_{i}", seed=i * 7 + 1) for i in range(4)]
    # 0 and 1 are the FRONT run and carry no arches of their own: the arcade on
    # that elevation is made of real SM_Corner_ArchBrace, below.
    tw = [_ctx_timber_wall(f"_ctx_timber_{i}", seed=i * 11 + 3, braces=i >= 2)
          for i in range(4)]

    # ---- ground storey, stone -------------------------------------------
    dup(sw[0], (1.0, 0, 0)); dup(sw[1], (3.0, 0, 0))              # front run
    put("SM_Corner_StoneQuoin_A", (4.36, .36, 0), 90)              # hero corner
    dup(sw[2], (4.36, 1.36, 0), 90); dup(sw[3], (4.36, 3.36, 0), 90)
    put("SM_Corner_StoneInner", (0, 0, 0), 0)                      # armpit
    dup(sw[1], (-.36, -1.0, 0), 90)                                # wing east
    put("SM_Corner_StoneQuoin_B", (-.36, -2.0, 0), 90)             # wing corner
    dup(sw[3], (-1.36, -2.36, 0), 0)                               # wing south

    # ---- jetty transition -----------------------------------------------
    # The joint fills the TIMBER corner cell (B.SILL_CELL), so its corner spot
    # is the wall corner + that cell -- NOT the stone corner's + T_STONE, which
    # is where this demo used to put it. Get that wrong by the 0.12 between the
    # two thicknesses and the return leg stands 0.12 proud of the run it meets,
    # which is exactly the fault Shanee found in the assembled inn.
    JC = B.SILL_CELL
    put("SM_Corner_JettyJoint", (4.36, JC, HG - JETTY_BAND), 90)
    # ... and the two runs are cut to land ON its butt planes: the front run
    # ends at x = 4.36 - JC (its y = SILL_JOINT_Y plane) and the east run at
    # y = JC (its x = SILL_JOINT_X plane), both on the wall face plane (front
    # y=0, east x=4.36) and SILL_H below the storey line.
    s1 = _ctx_sill("_ctx_sill_front", 4.36 - JC)
    s1.location = ((4.36 - JC) / 2, 0.0, HG - B.SILL_H); out.append(s1)
    s2 = _ctx_sill("_ctx_sill_east", 4.36 - JC)
    s2.location = (4.36, (4.36 + JC) / 2, HG - B.SILL_H)
    s2.rotation_euler = (0, 0, radians(90)); out.append(s2)

    # ---- upper storey, half-timber --------------------------------------
    put("SM_Corner_TimberPost_A", (4.81, -.21, HG), 90)
    put("SM_Corner_ArchBrace_Pair", (4.81, -.21, HG), 90)   # arches both ways
    dup(tw[0], (3.57, -J, HG)); dup(tw[1], (1.57, -J, HG))
    # The far end of the front run gets a post too -- and its cell is the WALL'S
    # THICKNESS BAND, y = -J .. -J+TT. It stood a whole T_TIMBER north of that,
    # at y = -J+TT, which put the entire post INSIDE the wall it terminates: its
    # proud face at y = -0.27 sat in the middle of a wall body spanning -0.45 to
    # -0.21, so the piece was invisible from outside and poking out of the
    # inside face. Nothing in the demo showed it because we only ever look at
    # the demo from outdoors.
    put("SM_Corner_TimberPost_C", (0.57, -J, HG), 0)
    dup(tw[2], (4.81, .79, HG), 90); dup(tw[3], (4.81, 2.79, HG), 90)

    # ---- THE ARCADE ALONG THE FRONT, out of SM_Corner_ArchBrace -----------
    # The point of splitting the pair. The front elevation's wall face is
    # y = -J and it faces -Y, so a brace reaching +X goes at rz 0 with its
    # origin ON that plane, and one reaching -X goes at rz 180 with its origin
    # slid 2*BR_MID_Y = -0.062 further out (see THE FRAME). Post C at x = 0.57
    # is braced in ONE direction only -- the case the welded pair could not
    # serve at all -- and the bay seam at x = 2.57 is braced BOTH ways, which is
    # the case that has no corner in it. Together with the pair's own front
    # arch at the hero corner they read as one continuous arcade: spans
    # 0.57-1.49, 1.65-2.57, 2.57-3.49, 3.65-4.57.
    # x = 0 is THE FACE OF THE POST, which at a corner is the cell's butt plane
    # (0.57 here, as at the hero corner) but MID-RUN is HALF A POST off the bay
    # seam: the seam post is W_POST wide and centred on the seam, so its two
    # faces are W_POST/2 either side of x = 2.57. Sprung off the seam itself the
    # two feet would cross inside each other; sprung off the post's faces each
    # buries its own foot in the post's own half and the arches rise off it
    # instead of meeting in a V above it.
    # BOTH ARMS ARE ON SHOW: the arcade uses arm A and arm B, which is what the
    # pair at the hero corner is made of, and standing them in a row is the point
    # -- two braces of the same family that are not the same stick.
    SEAMP = TW.W_POST / 2
    A0, A1 = ARCH_BRACE_ARMS
    put(A0, (0.57, -J, HG), 0)
    put(A1, (2.57 + SEAMP, -J, HG), 0)
    put(A0, (2.57 - SEAMP, -J + 2 * BR_MID_Y, HG), 180)

    # ---- THE TIMBER GALLERY, laid out the way r10 lays it out: an outside
    #      stair climbing the FRONT elevation, the gallery turning the
    #      south-east corner on its own post, and a run of bays carrying on up
    #      the EAST elevation over the open ground floor.
    #
    #      Nothing here is placed by eye. SM_Corner_GalleryCorner is the corner
    #      cell grown outward, so it snaps at THE SAME ORIGIN as the timber
    #      corner post above it and wraps that post's cell exactly. The bays
    #      snap on the same 2 m stations as the timber walls behind them, so
    #      their bressumers, ledgers, rails and boards butt the corner's on
    #      x = 0 / y = T. And the stair is two bays long, so its top tread lands
    #      on the module line x = 4.57 -- which IS the corner's return butt
    #      plane -- at GA_DKT, the height of the deck it lands on.
    put("SM_Corner_GalleryCorner", (4.81, -.21, 0), 90)
    put("SM_Corner_GalleryBay_2m", (4.81, .79, 0), 90)
    put("SM_Corner_GalleryBay_2m", (4.81, 2.79, 0), 90)
    put("SM_Corner_GalleryStair", (2.57, -J, 0), 0)

    e1 = _ctx_eave("_ctx_eave_front", 4.92)
    e1.location = (2.39, -J - .015, HG + HU - .085); out.append(e1)
    e2 = _ctx_eave("_ctx_eave_east", 4.1)
    e2.location = (4.81 + .015, 2.30, HG + HU - .085)
    e2.rotation_euler = (0, 0, radians(90)); out.append(e2)

    for o in list(src.values()) + sw + tw:
        o.location = (0, 60, 0)            # park the originals out of frame
    return out
