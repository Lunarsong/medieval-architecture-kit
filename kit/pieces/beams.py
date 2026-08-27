"""
Beams, corbels and posts -- the exposed structural timber of the inn. This is
the family that gives all three references their strongest horizontal line: the
heavy bressummer that carries the jettied upper storey, the carved brackets
tucked under it, the chamfered porch posts, the door lintel, the arch-braced
tie beam and the run of rafter tails that pokes out under the swept eave.

Read off the reference crops (ref1 jetty + swept_eave, ref3:porch, ref3 whole):
  * ref1, jetty over the front door: the bressummer is ONE fat hewn timber
    ~0.36 deep and ~0.34 thick, its outer face flush with the storey above
    (i.e. JETTY proud of the stone below), capped by a weather board that lips
    over it. Its arrises are chamfered, its top edge wanders and droops, and
    its front face is not one plane -- it is two or three adze facets.
  * ref1, right-hand jetty: the overhang is carried on slim curved knee braces
    alternating with scrolled corbels that curl to a nose at the bottom.
  * ref3, porch and lean-to: posts are SLENDER (~0.20 across the flats over
    2.5m), chamfered between square stops, splayed foot, a modest bolster head
    -- NOT a flared capital -- and long thin curved braces.
  * ref3, everywhere: a fine tooth course (~0.21 spacing) hangs under every
    jetty, eave and barge. It is cheap and it is most of what makes the timber
    read as crafted rather than sawn.
  * ref1, eaves: the tails lie SHALLOW and flick flatter at the tip, because
    the kit's eave is bell-cast (S.SWEEP) -- nothing like the 52 degree roof
    pitch -- and their cut noses poke out THROUGH a wide flat fascia plank.
  * ref1 and ref3, EVERY long horizontal: nothing is straight. The bressummer
    swags between its brackets, the lean-to's eave rail dips and lifts again,
    the jetty line on ref3's long wall bows by a good 5% of its span and rises
    at the corner. A straight timber is the single fastest way to make this kit
    look extruded, so every member in this family is bowed (see _bend): the 4m
    tie is cambered up TIE_CAM, the eave fascia droops EAVE_BOW and the lintel
    soffit cambers LINT_CAM -- all 6-8% of their span, because each of those
    spans a bay or two ON ITS OWN and its curve is read whole. A RUN piece is
    different: its bow REPEATS every 2m, so what reads at 7% on a single 4m tie
    reads as a scalloped edge along a wall and makes each module look a
    different size from its neighbour. The run pieces therefore swag SILL_BOW,
    which is 2.75%.

BEAM-FAMILY PLACEMENT (an extension of the wall convention in spec.py):
    Y = 0 is the OUTER FACE OF THE WALL the timber is fixed to. The body runs
    +Y into that wall (never past its inner face) and the structural
    projection runs -Y, outward. A bressummer or a rafter tail exists in order
    to cantilever past the wall face, so -- unlike wall relief -- it stands
    further out than PROUD_MAX; every piece therefore declares its true -Y
    extent in `seams`, so p.finish() still validates it exactly.

    RUN pieces (sill beam, rafter tails) tile along X at exactly GRID and are
    cut dead flat on x = +/-GRID/2, with zero wander at the end stations, so a
    row of them reads as one continuous timber. Their bow uses a sin^2 profile
    -- the deflection of a beam continuous over its supports, zero displacement
    AND zero slope at both stations -- and their stations are CLUSTERED toward
    the seams (`_stations`, ease), because the mesh only SAMPLES that curve and
    even sampling is what used to leave a hard crease at every joint. The low
    point of a run is its BAY CENTRE.
    POINT pieces (corbels, post, lintel, tie beam) are centred on their own
    footprint with Z=0 at the bottom, ready to snap under a run piece.

THE ONE INTERFACE IN THIS FAMILY is the jetty run: A, B and C butt end to end
and SM_Corner_JettyJoint (kit/pieces/corners.py, which imports the numbers from
here) terminates it. Read "THE JETTY SILL PROFILE" below before touching any of
the three sill variants -- a run of them has to read as one timber, and it did
not: their soffits sat at three different heights, their depths differed by
20mm, C tapered 30mm along its length and only two of them carried the weather
board, so every joint stepped. Everything about that section is now one set of
constants, and demo() puts the whole run plus the corner in a line so the step
would be visible if it ever came back.

    The section is now identical at every seam to the micron, but a run of it
    STILL read as pieces of different sizes, and that was the swag: at 140mm of
    dip per 2m module the soffit fell 41% of the beam's own depth and came back
    up at every joint, so beside the corner joint -- which is flat, because it
    is where the run is CARRIED -- each sill looked like a deeper timber, and
    the sampled curve left a 15 degree crease in both the top line and the
    soffit at every station. The dip is now SILL_BOW = 55mm (2.75% of span,
    read off the references' bressummer rather than off their whole-wall bow,
    which no 2m module can carry) and the stations are eased, so a mixed A/B/C
    run and the corner read as one hand-hewn timber with a gentle droop.

    ROUND 8 -- Shanee, of the assembled inn: "a large gap between
    SM_Corner_JettyJoint.005 and SM_Beam_JettySill_2m_A.026", "a visible
    seam/line in SM_Corner_JettyJoint.005 itself", "a seam between
    SM_Beam_JettySill_2m_A.024 and _B.007". Three separate faults, and the
    section being right was not enough to stop any of them:

      GAP    the corner was built on the T_STONE cell and assemble_inn.py places
             it on the T_TIMBER one. 120mm, measured. See SILL_CELL.
      LINE   two solids butted face to face where one continuous solid belongs
             -- inside the corner (two lapped boxes) and at every 2m joint (a
             bmesh bevel chamfers the END faces too, so two sills met chamfer to
             chamfer down a 26mm V-groove). Both are now single swept solids
             whose butt faces are dead flat: see sweep() and sill_corner_rails().
      TONE   and even with the geometry exact, each variant jittered its own
             shade by up to 8.5%, which draws a joint as clearly as a groove.
             The run is one flat tone now: SILL_TONE.

    The three butt planes are checkable, not eyeballable: at every one of them
    the two pieces present the same 20 section points to 5 decimal places.

Vertical interlock, so the family stacks with spec.py's storey heights:
    SILL_H   0.48  sill band; place a sill run at H_GROUND - SILL_H
    SILL_BOW 0.055 the run's soffit is SILL_BOW above z=0 at the seams and dead
                   on z=0 at the bay centre, so a bracket or a post goes UNDER
                   THE MIDDLE OF A BAY -- which is where a prop belongs under a
                   sagging beam, and what ref1 and ref3 both show. At a seam
                   station, pack a bracket up by SILL_BOW.
    CORBEL_H 0.60  both corbels are exactly this tall and reach the same way
                   out, so they are interchangeable under a sill soffit
    POST_H   H_GROUND - SILL_H, so a porch post carries a sill run directly
                   (again at the bay centre, where the swag comes down to meet
                   the post head)
    RAFT_H   0.54 to the top of the wall plate; place at head height - RAFT_H.
                   The plate stays dead straight -- only what cantilevers past
                   the wall face droops.

===============================================================================
ROUND 9(b) -- CARVING ON THE OTHER SEVEN PIECES, AND THE HOUSING, VERIFIED.
===============================================================================
Shanee, of the whole kit: "the wood overall still needs a texture or detail."
It cannot be a texture (the .blend is inspected in SOLID shading, where one
material draws one flat colour and an image texture or a vertex-colour tint is
simply not present), so it has to be FORM. Three things came out of that here:

1. THE SILL RUN HAD THE TREATMENT. NOTHING ELSE DID. corbel_scroll,
   corbel_knee, porch_post, lintel_door, tie_beam and rafter_tails were all
   p.prism / p.box / p.cyl with one uniform 12-15 mm bmesh bevel on every
   arris -- the soap bar, and the exact thing timber_walls' round-9 pass exists
   to end. They are built by `wprism` / `oct_shaft` now: the chamfer is part of
   the solid, so its width is a FUNCTION OF POSITION and can stop, swell and
   wear. See THE WORKED TIMBER. Two details fell out of it that are worth
   naming, because they were commented as present and were not:
     * lintel_door had two "chamfer stop" blocks at x = +-0.70 and no chamfer
       for them to stop -- the beam was uniformly bevelled end to end;
     * porch_post's "square stops" were a constant octagon with a collar box
       lapped over each end, i.e. a chamfer that never stopped, it just went
       behind something. `oct_shaft` gives it a real square section at both
       ends with the four chamfers running out of it over 90 mm, and the collars
       are shallower so that return is visible. It is the most legible piece of
       carpentry in either family in Solid shading.
   AND IT IS ALL CHEAPER: a bevelled prism spends tris on strips round every
   edge of every face including the two ends; a 4-ring loft does not. The family
   went from 6372 tris to 5200 -- 18% less -- with far more carving in it.
   rafter_tails alone went 1368 -> 956, which is what paid for chamfering its
   five tails (its deck boarding is bevel=0 now: it is under the shingles and
   over the tails, so every arris of it is buried).

2. THE PEGS WERE INVISIBLE, AND THEY WERE THE WRONG MATERIAL. 21 mm untapered
   `iron` dowels: dark pegs in dark timber, which in Solid shading is one flat
   tone against the same flat tone. timber_walls._peg already draws them the way
   they have to be drawn -- tapered oak, `oak_pale`, 26-30 mm, standing on their
   own shoulder -- and job 2 of this round is that the wall framing and the
   exposed beams read as the same timber in the same building. Same section, same
   taper, same material now, and `_pegs` takes the FACE it is driven into rather
   than a hand-typed offset, which turned up three that were plain wrong:
   corbel_knee's lower peg was 130 mm inside solid oak and the porch post's two
   stood 54 mm out of a flat they were nominally 12 mm off.

3. ZERO-TRI CARVING ON THE RUN PIECES, where the section is frozen. The sill's
   butting profile may not move, so the two details it got cost nothing at all:
   ARRIS WEAR (sill_rails' `wear`: the chamfer's width wanders 14-30 mm along
   the length instead of a dead 22 mm, by scaling the band inset) and the
   ALTERNATING FACET TILT (_adze's `tilt`). The tilt is the same finding as
   timber_walls' 9b: the adze facets were parallel, so neighbouring facets had
   the same normal, and the hard crease between them separated two identical
   values. Both are multiplied by _fade, so both are exactly zero at x = +-1.0.
   sweep_box got the same two, which matters most on the eave fascia -- the one
   line the whole roof is read along.
   MEASURED on SM_Beam_JettySill_2m_A in Workbench/Solid at 2 m (brown pixels
   only, so the void cannot flatter the number): std of luminance inside the
   timber 0.0245 -> 0.0305 and the share of pixel pairs stepping more than 2%
   1.23% -> 1.52%, i.e. +24% on both, for zero extra tris.

THE SHARED SECTION IS PROVEN UNCHANGED, not assumed. All three sills still
present the SAME 20 section points at both butt planes (all six planes byte
identical), and against the pre-round-9 build the ONLY four points that moved
in the whole section are the hidden housing plate's:
        y 0.240 -> 0.050   and   z 0.055..0.480 -> 0.059..0.472
i.e. exactly the bug in item 4 and nothing else. The exposed bressummer, its
weather board, the chamfer, the fall and the outward projection are identical to
the micron, so the sill/SM_Corner_JettyJoint seam work cannot have regressed.

4. THE HOUSING (the z-fighting Shanee named) -- fixed and now measured. See the
   block at SILL_TAIL for the full argument. Before: the sill spanned
   y -0.492..0.240 against a timber wall's -0.145..0.240, so 385 mm of mutual
   penetration on the shallowest axis over 44 placements, the beam's back plate
   ended ON the wall's inner face (~7000 cm2 of coplanar opaque faces per bay)
   and its top ended ON the storey line the wall above starts from. After:
   SILL_TAIL = 50 mm of HOUSING, top HOUSE_DZ under the storey line, so the
   overlap is 195 mm and NOT ONE horizontal face of the beam is coplanar with a
   face of the wall (checked against SM_Wall_Timber_2m_A's own faces: the
   housing's top is at 0.472 against the wall's 0.480, and the weather board's
   top is a shed face at 1.85 degrees, not a plane). What overlap remains is the
   wall's own proud head plate and frieze buried INSIDE the bressummer, which is
   what a bressummer does to the head of the storey below it -- opaque, not
   flickering, and not something either module can place differently.

===============================================================================
ROUND 10 -- THE JETTY UNDERSIDE, LOOKED AT RATHER THAN ARGUED ABOUT.
===============================================================================
Section 7 (SM_Beam_JettySoffit_2m, SM_Beam_JettyPlate_2m,
SM_Beam_DragonBeam_Corner) was built and its numbers were right; four things
were still wrong ON THE SCREEN, and every one of them was found by opening the
PNGs rather than by reading the file. The frozen jetty sill section is untouched
(all three sills still measure 504 / 952 / 768 tris to the triangle, and
corners.py's imports -- SILL_*, sweep, sill_bands, sill_rails,
sill_corner_rails, sill_fall -- are byte identical):

  1. THE JOIST NOSES WERE BLOBS. 40 mm of projection with a 34 mm chamfer cut on
     it is a pyramid, not a moulded end, and it shaded as one smooth lozenge:
     a run of them read as studs glued to a plank. The fascia moved back to
     JS_FAS_Y = 0.072 and the moulding down to 0.018, so a nose is 64 mm proud
     with 46 mm of flat square end on it. See the block at JS_NOSE_CH.
  2. THE DRAGON BEAM WAS A BEVELLED BOX -- the soap bar THE WORKED TIMBER exists
     to end, and it chamfered the beam's two CUT ENDS, which are its tenon and
     its butt. It is swept from rails now (_dragon_rails), with a stop-chamfer
     that dies at both joints and flat cuts. Cheaper, and it turned up an 80 cm2
     coincident pair with the joists' tops that the bevel had been hiding.
  3. THE CORNER ENDED IN A DOORKNOB. A 62 mm truncated cone under the dragon
     beam's nose, where the vernacular puts the PENDANT -- the one piece of
     ornament the whole construction gets and the only thing that gives the
     corner a silhouette. It is a turned drop now (_pendant), hanging 126 mm
     clear below the beam and stopping above the bressummer's soffit line.
  4. THE DEMO CONTRADICTED THE ASSEMBLER. Its ground storey stood flush with the
     timber cell; assemble_inn.py insets the timber storeys 0.12 BEHIND the
     stone face, which is why SM_Corner_JettyJoint's stone corbels hung in
     mid-air in demo.png. The demo is on the real planes now, the walls wrap
     both corners, the upper wall runs ACROSS the dragon corner so the piece is
     seen carrying something, and the two spare pieces that show the soffit
     stand against the wall instead of lying face-up under a downward camera.
"""
import bpy
from math import pi, sin, cos, radians, sqrt
from kit import spec as S
from kit.util import Part, rng, lerp, clamp, smoothstep

FAMILY = "beams"
COLLECTION = "10_Beams_Corbels"

G        = S.GRID                  # 2.0   run length
J        = S.JETTY                 # 0.45  outward throw of a jetty
T        = S.T_STONE               # 0.36  the stone storey a jetty sits over
# ---------------------------------------------------------------------------
# HOW FAR THE BEAM REACHES INTO THE WALL -- ROUND 9, and it was a real bug.
# ---------------------------------------------------------------------------
# Shanee, of the assembled inn: "SM_Wall_Timber_2m_A.014 has overlap with
# SM_Beam_JettySill_2m_A.038 causing z fighting". Measured in
# out/inn_example.blend: 44 placements of a sill inside a wall with 385 mm of
# mutual penetration on the SHALLOWEST axis (and 409-414 mm against the stone
# storey, which is inset S.T_STONE - S.T_TIMBER further back again). The sill
# spanned y -0.492..0.240 and the timber wall spans y -0.145..0.240 -- and the
# assembler puts both on the same bay centre, so the beam reached as far into the
# building as the WHOLE THICKNESS of the wall it is supposed to be bedded in.
# Two things fell out of that, and the second is what is actually visible:
#   * the beam's back plate ENDED ON y = T_TIMBER, which is the wall's inner
#     face: two opaque coplanar faces, ~7000 cm2 per bay, i.e. z-fighting on the
#     inside face of every jettied storey. Against the stone storey the same
#     plate ended on y = T_STONE, its inner face, for the same reason;
#   * and its top face ended on z = SILL_H, which is exactly the storey line the
#     wall above starts from -- so the plate's top and the wall's bottom were
#     coplanar as well, another ~6600 cm2.
# A bressummer is HOUSED a little into the frame; it does not run through it. It
# is a beam that CANTILEVERS, so what it needs behind the wall face is a bearing,
# not a floor. So SILL_TAIL is now a housing depth of 50 mm -- and the plate's
# top is HOUSE_DZ BELOW the storey line, so it is buried inside the wall instead
# of sharing a plane with its underside.
#
# NOT TOUCHED, deliberately: SILL_FACE, SILL_DEPTH, SILL_TOP, SILL_SOF,
# SILL_CAP*, SILL_BEV, sill_bands(), sill_rails() or sill_corner_rails() -- i.e.
# the OUTWARD projection and the whole butting profile that the sill/corner seam
# work was verified on. The only thing that moved is the hidden back plate, which
# is not part of the shared section (corners.py builds its own, from its own
# cell, and is welcome to keep filling the corner cell it has to fill).
SILL_TAIL = 0.050                 # how far the beam is HOUSED into the wall
                                  # behind it. Was S.T_TIMBER (0.240), i.e. the
                                  # entire wall thickness. See the block above.
HOUSE_DZ  = 0.008                 # ... and how far its top stays below the
                                  # storey line, so no face of the housing lands
                                  # on a face of the wall it is housed in
SILL_H   = 0.48
CORBEL_H = 0.60
POST_H   = S.H_GROUND - SILL_H     # 2.52
RAFT_H   = 0.54

# ===========================================================================
# THE JETTY SILL PROFILE -- ONE cross-section, shared by every run piece.
# ---------------------------------------------------------------------------
# SM_Beam_JettySill_2m_A/_B/_C butt end to end at x = +/-GRID/2 and
# SM_Corner_JettyJoint terminates the run. A run of A, B, C, corner has to read
# as ONE timber, so the section AT A SEAM STATION is these numbers and nothing
# else, and every variant is DERIVED from them -- that is what stopped the run
# stepping in size between variants.
#
# What a variant may differ in: carving, adze facets and wander, pegs,
# mouldings, tooth courses, straps, how hard its chamfer stop waists. All of it
# must be INSET from the seam by at least SILL_INSET, or die in _fade(), so that
# the silhouette at x = +/-GRID/2 is exactly this profile.
# What a variant may NOT touch: any number below, the chamfer SILL_BEV (one
# variant chamfering differently IS a step at the joint), the board's fall, or
# the wobble amount/frequency
# (util.wobble is a function of world position, so identical settings deform
# every variant identically -- differing ones tear the joint open).
#
# ---> kit/pieces/corners.py IMPORTS THESE NAMES <--- SM_Corner_JettyJoint laps
# two sills of exactly this section over each other and presents it on BOTH
# faces, so a run arriving from either direction lands flush. Change a number
# here and the corner follows; redefine one over there and the kit drifts apart
# again.
SILL_TOP   = SILL_H            # z of the top face. The piece is placed at
                               # storey_top - SILL_H, so this lands on the
                               # storey line (see assemble_inn.py).
SILL_SOF   = 0.055             # z of the soffit AT A SEAM STATION. _bend()
                               # swags the whole piece down to z=0 mid-bay.
SILL_BOW   = SILL_SOF          # THE SWAG, and an INVARIANT, not a free number:
                               # the run dips exactly to z=0 at the bay centre,
                               # which is the plane a CORBEL_H bracket's head
                               # reaches when it is placed at
                               # storey_top - SILL_H - CORBEL_H. Both demo()
                               # and assemble_inn.py rely on that, so the two
                               # constants move together or the brackets stop
                               # touching the beam. See the note on scale in
                               # the module docstring: 55mm, not 140mm, because
                               # a RUN piece's bow repeats every 2m.
SILL_FACE  = -J                # -0.45  y of the exposed face: flush with the
                               #        storey above, JETTY proud of the wall
SILL_DEPTH = 0.34              # face-to-back depth of the exposed timber
SILL_BACK  = SILL_FACE + SILL_DEPTH        # -0.11  y of its back
SILL_CAP   = 0.058             # the weather board is the TOP BAND of the
SILL_CAP_O = 0.026             # profile, and lips this far proud of the face
SILL_BEV   = 0.022             # chamfer on the timber's four long arrises. A
                               # bressummer's arris chamfer is 25-50mm in the
                               # references and this was 13mm, which at 2m away
                               # is one pixel: the timber read as an extruded
                               # box with a stop-chamfer nobody could see. It is
                               # cut INTO the swept section now (see sweep), not
                               # bevelled on, so widening it costs nothing and
                               # cannot reach the butt faces.
SILL_CAP_BEV = 0.012           # ... and on the weather board's
SILL_CAP_FALL = 0.011          # the weather board's WEATHERING: its top sheds
                               # this far toward the face over its own depth.
                               # Part of the section, so it turns the corner and
                               # crosses every joint unbroken -- and it is the
                               # only thing that stops the top of a jetty, the
                               # ledge you look straight down on from the storey
                               # above, being one dead flat 8m plane.
SILL_INSET = 0.075             # variant detail keeps this clear of a seam
SILL_SEAM  = dict(x=(-G / 2, G / 2), y=(SILL_FACE - .075, SILL_TAIL),
                  z=(0.0, SILL_H))
# ONE TONE for the whole run. The section being identical is not enough: every
# variant used to jitter its own shade by up to +/-8.5% per prism, so two sills
# butted rendered as two different colours of timber and the joint read as a
# line even where the geometry was perfect. The bressummer's body and its board
# are painted flat (tint=0) at these two values in EVERY variant AND in
# SM_Corner_JettyJoint, so a run is one colour and all its variety is FORM.
SILL_TONE   = 1.00             # the timber
SILL_CAP_TONE = 1.10           # the weather board, a little lighter

# ---------------------------------------------------------------------------
# WHERE THE SECTION IS PRESENTED -- the other half of the interface.
# ---------------------------------------------------------------------------
SILL_END   = G / 2      # 1.00  a run piece is cut dead flat on x = +-SILL_END
SILL_CELL  = S.T_TIMBER # 0.24  the corner cell SM_Corner_JettyJoint fills, and
                        #       THE NUMBER THAT WAS WRONG. A jetty joint is the
                        #       corner of a TIMBER storey: assemble_inn.py's
                        #       corners(blk, "timber") places it on blk.tb --
                        #       the same rectangle, inset T_TIMBER, that the
                        #       sill runs are placed on -- so its cell is
                        #       T_TIMBER, not T_STONE. Built on the 0.36 stone
                        #       cell it presented its return leg 0.12 too far
                        #       out and its butt plane 0.12 too far in.
                        #       Measured in out/inn_example.blend, exactly the
                        #       pair Shanee named: SM_Corner_JettyJoint.005's
                        #       return face at x = 5.910 against
                        #       SM_Beam_JettySill_2m_A.026's face at x = 6.030,
                        #       and the joint's butt plane at y = -1.520
                        #       against that run's end at y = -1.640. That
                        #       120 mm = T_STONE - T_TIMBER is the large gap.
SILL_JOINT_X = 0.0         # the corner's butt plane for a run arriving along X
SILL_JOINT_Y = SILL_CELL   # ... and for one arriving along Y (its local y = T)
# ===========================================================================

GAP = 0.006     # "never share a plane". Two opaque coplanar faces z-fight, and
                # check_zfight.py measures it in cm2. So wherever two solids of
                # this family meet, one overlaps the other by GAP (the joint is
                # then buried inside opaque geometry) instead of butting onto
                # its plane. Keep it under the local bevel width and the two
                # chamfered faces do not even touch.

# PART OF THE SHARED SECTION (corners.py imports it): how far the weather board
# reaches DOWN into the timber it caps. The board's lower arris throws the
# shadow line that runs the whole length of a jetty, so the corner has to bed
# its board by the same amount or that line jogs at the joint -- it used to lap
# GAP there and 2*GAP on the run pieces, i.e. a 6mm step in the one line the
# eye follows along the beam.
SILL_CAP_LAP = 2 * GAP

# How far every member bows. Measured off the references: their swept eaves and
# jetty rails bow 5-10% of the span they cross, and a straight one reads as
# extruded metal. These are the mid-span deflections, in metres. SILL_BOW is up
# in THE JETTY SILL PROFILE, where it belongs: it is part of the section a run
# has to share, and it is tied to SILL_SOF.
EAVE_BOW = 0.14        # 2m eave: droop of the fascia + tail noses, 7%
TIE_CAM  = 0.25        # 4m tie is CAMBERED UP this far, 6.3%
LINT_CAM = 0.13        # 1.70m lintel soffit cambers up, 7.6%
POST_BOW = 0.045       # the porch post is a pole, not a lathe turning


# =============================================================================
# ================== THE WORKED TIMBER -- carving, as FORM =====================
# =============================================================================
# Round 9, Shanee, of the whole kit: "the wood overall still needs a texture or
# detail." It cannot BE a texture: the .blend is inspected in Solid viewport
# shading, where one material draws one flat colour per face and an image
# texture or a vertex-colour tint is simply not present. So the answer is
# geometry that casts its own light and shade -- which is the better answer for
# a game asset anyway, because it survives every shading mode and still reads at
# distance where a texture has gone to mud.
#
# The jetty sill run already had this treatment (see THE JETTY SILL PROFILE: a
# swept solid, adze facets, a waisted chamfer, the swag). NOTHING ELSE IN THE
# FAMILY DID. corbel_scroll, corbel_knee, porch_post, lintel_door, tie_beam and
# rafter_tails were all `p.prism`/`p.box` with a uniform 12-15 mm
# bmesh.ops.bevel on every arris -- the soap-bar treatment, and the exact thing
# timber_walls' round-9 pass exists to end. A uniform bevel is the worst of both
# worlds in Solid shading: every arris is rounded by the same amount so no facet
# is ever wider than the rounding, and because the rounding is smooth-shaded at
# SMOOTH_ANG there is no hard line anywhere for the light to break on.
#
# `wprism` is the fix, and it is the same idea timber_walls._hexsec uses, in the
# form this family needs: a prism whose END FACES are INSET, so the chamfer is
# part of the solid instead of a modifier on it, and so its width can be a
# FUNCTION OF POSITION. That buys the three details a hand-cut timber has:
#
#   STOP-CHAMFER   the chamfer runs the length of the member and dies short of
#                  each end. The single most characteristic joinery detail there
#                  is: a carpenter chamfers the length of a timber and squares
#                  the arris back up where the joint is, so the mortice has full
#                  wood, and the stop itself becomes the ornament. A bevel
#                  cannot do it -- it rounds every arris equally. Where the
#                  chamfer scale falls to zero the ring is still set back, so
#                  the return comes out as a little square-cut facet: the carved
#                  return, for free.
#   ARRIS WEAR     the width is jittered per profile vertex, so no two arrises
#                  of one timber are worn the same amount. "Soften the long
#                  edges unevenly rather than a uniform bevel", and it costs
#                  nothing -- it is a multiplier on a number the loft was going
#                  to use anyway.
#   BURIED ARRISES stay square (`cb=0`): a corbel's back is in a wall and a
#                  lintel's back is in a reveal. Carving what is buried is the
#                  one thing this 1600-tri budget genuinely cannot afford.
#
# The numbers are timber_walls' numbers on purpose. Job 2 of this round is that
# the wall framing and the exposed beams read as the same timber in the same
# building, and they cannot if one family chamfers 26 mm and the other 40.
CHAM      = 0.026    # == timber_walls.CHAM: chamfer on an exposed timber arris
CHAM_STOP = 0.105    # == timber_walls.CHAM_STOP: how far short of the end it dies
CHAM_RET  = 0.068    # == timber_walls.CHAM_RET: length of the carved return. A
                     # 30 mm return is a kink; oct_shaft's 90 mm one is the most
                     # legible carpentry in either family, because a long return
                     # turns the chamfer face right through the light.
CHAM_SWELL = 0.30    # == timber_walls.CHAM_SWELL: the LAMB'S TONGUE, the swell
                     # a joiner's chisel leaves just inboard of a chamfer stop
WEAR      = 0.34     # == timber_walls' `wear`: uneven arris, per edge
FACET_TILT = 0.022   # how far an adze facet's far edge cuts in past its near
                     # one. THIS is what makes a hewn face read in flat shading
                     # and the old facets did not: they stepped INWARD in
                     # parallel, so two neighbouring facets had the same normal
                     # and the hard crease between them separated two identical
                     # values -- a sharp edge you cannot see. Tilted alternately
                     # they differ by 2*atan(TILT/height) ~ 7 deg, which is a
                     # real value step. Inward only, both sides, so the section
                     # at a butt plane is untouched.


def _poly_out(poly):
    """Per-vertex outward unit normal of a closed 2D polygon, either winding."""
    n = len(poly)
    A = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
            for i in range(n))
    s = 1.0 if A > 0 else -1.0        # CCW: interior is left, so outward is right
    en = []
    for i in range(n):
        (ax, ay), (bx, by) = poly[i], poly[(i + 1) % n]
        dx, dy = bx - ax, by - ay
        L = sqrt(dx * dx + dy * dy) or 1.0
        en.append((s * dy / L, -s * dx / L))
    out = []
    for i in range(n):
        ux, uy = en[i - 1][0] + en[i][0], en[i - 1][1] + en[i][1]
        L = sqrt(ux * ux + uy * uy) or 1.0
        out.append((ux / L, uy / L))
    return out


def _stop(u0, u1, stop=CHAM_STOP, ret=CHAM_RET, ends=0.0):
    """Chamfer scale along a member: `ends` at u0/u1, full over `ret` past
    `stop`. THE stop-chamfer, as a callable, so wprism can ask per vertex."""
    def f(u, v=0.0):
        rr = max(ret, 1e-6)
        dd = min(u - u0, u1 - u)
        k = lerp(ends, 1.0, clamp((dd - stop) / rr))
        # the lamb's tongue: the chamfer swells just inboard of its return
        k *= 1.0 + CHAM_SWELL * max(0.0, 1.0 - abs(dd - (stop + rr * 1.30))
                                    / (rr * 1.15))
        return k
    return f


def oct_shaft(p, z0, z1, w0, w1, mat, ret=.090, mids=2, cend=.0035, wear=.22,
              tint=.055, shade=1.0, seed=0):
    """A POST WITH SQUARE STOPS: square section at both ends, the four chamfers
    running out of it over `ret`, a regular octagon everywhere between.

    This is the post version of the stop-chamfer, and it is the detail every
    chamfered post in both references ends with. `p.cyl` cannot do it -- its
    section is CONSTANT, so a cyl shaft has no stop and the only way to finish it
    is to hide the end of the octagon under a collar, which is what this post
    did: three cyl lifts with a box lapped over each end, i.e. a chamfer that
    never stops, it just goes behind something. Now the square end is 90 mm of
    visible squared timber with the chamfer growing out of it.

    `w` is the half-width across the flats; a regular octagon has its corners
    cut back 0.5858*w. `wear` gives each of the four arrises its own width, so
    they are not all worn the same amount, and it costs nothing.
    """
    L = max(z1 - z0, 1e-6)
    e = clamp(ret / L, .02, .40)
    ts = sorted(set([0.0, e, 1 - e, 1.0]
                    + [lerp(e, 1 - e, (i + 1) / (mids + 1)) for i in range(mids)]))
    r = rng(f"{p.name}/shaft/{seed}")
    jw = [1.0 + wear * r.uniform(-1, .45) for _ in range(4)]
    rings = []
    for t in ts:
        w = lerp(w0, w1, t)
        k = smoothstep(0, e, t) * smoothstep(0, e, 1 - t)
        c = [lerp(cend, .5858 * w, k) * jw[i] for i in range(4)]
        z = lerp(z0, z1, t)
        a = [w - min(ci, w * .82) for ci in c]
        rings.append([(w, -a[3], z), (w, a[0], z), (a[0], w, z), (-a[1], w, z),
                      (-w, a[1], z), (-w, -a[2], z), (-a[2], -w, z), (a[3], -w, z)])
    n, m = 8, len(rings)
    vs = [v for ring in rings for v in ring]
    F = [tuple(range(n))[::-1], tuple(range((m - 1) * n, m * n))]
    for li in range(m - 1):
        for i in range(n):
            j = (i + 1) % n
            F.append((li * n + i, li * n + j, (li + 1) * n + j, (li + 1) * n + i))
    return p._emit(vs, F, mat, tint, 0, None, shade)


def wprism(p, poly, thick, mat, axis='Y', at=(0, 0, 0), cf=CHAM, cb=0.0,
           cw=None, wear=WEAR, seed=0, tint=.06, shade=1.0, floor=.0018):
    """`p.prism` with a REAL chamfer instead of a bevel -- see THE WORKED TIMBER.

    poly    the profile, as for p.prism
    cf/cb   chamfer width on the near / far end face (cb=0 leaves it square)
    cw      cw(u, v) -> 0..1, the chamfer's scale at that profile point. Use
            `_stop(...)` for a stop-chamfer; None means the full width all round
    wear    per-vertex jitter on the width, i.e. an unevenly worn arris
    floor   the chamfer never quite reaches zero, so the ring stays a ring and
            remove_doubles has nothing to collapse
    """
    n = len(poly)
    h = thick / 2
    nrm = _poly_out(poly)
    r = rng(f"{p.name}/wprism/{seed}")
    ws = [1.0 + wear * r.uniform(-1, .55) for _ in range(n)]

    def ring(c):
        return [min(max(floor, c * ws[i]
                        * (cw(poly[i][0], poly[i][1]) if cw else 1.0)), c * 1.85)
                for i in range(n)]
    levels = []
    if cf > 0:
        levels.append((-h, ring(cf)))
    levels.append((-h + max(cf, 0.0), [0.0] * n))
    levels.append((h - max(cb, 0.0), [0.0] * n))
    if cb > 0:
        levels.append((h, ring(cb)))
    f = ((lambda u, v, s: (u, s, v)) if axis == 'Y' else
         (lambda u, v, s: (s, u, v)) if axis == 'X' else
         (lambda u, v, s: (u, v, s)))
    vs = []
    for (s, ins) in levels:
        for i, (u, v) in enumerate(poly):
            vs.append(f(u - nrm[i][0] * ins[i], v - nrm[i][1] * ins[i], s))
    vs = [tuple(a + b for a, b in zip(q, at)) for q in vs]
    m = len(levels)
    F = [tuple(range(n))[::-1], tuple(range((m - 1) * n, m * n))]
    for li in range(m - 1):
        for i in range(n):
            j = (i + 1) % n
            F.append((li * n + i, li * n + j, (li + 1) * n + j, (li + 1) * n + i))
    return p._emit(vs, F, mat, tint, 0, None, shade)


# ------------------------------------------------------------------ helpers --
def _stations(n, ease=0.0):
    """n+1 parameters spanning [0,1] for a timber built from its elevation.

    `ease` (0..1) migrates them from even spacing toward a cosine spacing, which
    CLUSTERS them at both ends. That is what lets a bowed RUN piece leave its
    seam station without a crease. _bend()'s curve has zero slope at the seam,
    but the mesh only SAMPLES it: with even 0.2m stations the first segment of
    the old 140mm swag already dropped 27mm, so the polyline left the seam at
    7.7 degrees and met its mirror image in the next module -- a 15 degree kink
    in the top line and the soffit at every 2m joint. Eased, the first station
    sits 87mm in and drops 1mm, and the joint reads flat."""
    return [lerp(i / n, 0.5 - 0.5 * cos(pi * i / n), ease) for i in range(n + 1)]


def _hewn(p, x0, x1, z0, z1, y0, y1, mat, seed=0, spans=6, facets=1,
          top_wave=.010, bot_wave=.0, top_sag=.010, bot_sag=.0, face_jit=.0,
          taper=.0, tint=.065, bevel=.014, shade=1.0, ease=.0,
          cham=0.0, cstop=CHAM_STOP, cends=0.0):
    """A long timber running along X, built from its SIDE ELEVATION so its top
    and bottom arrises can wander and droop like a hand-hewn beam.

    `facets` splits it lengthwise into that many prisms sharing one continuous
    top/bottom edge, each standing a hair further out (`face_jit`) and shaded a
    hair differently -- use it only on timbers long enough that they would
    really have been scarfed from two or three trees (the 4m tie), because on a
    short run the chamfered joints read as panelling.
    The end stations sit exactly on x0/x1 with no wander, so tiled copies weld
    into one continuous beam. `ease` clusters the stations toward those ends --
    see _stations(); a RUN piece that is going to be bowed wants it.

    `cham` makes it a WORKED timber instead of a bevelled one: a stop-chamfer
    down its two front arrises, dying `cstop` short of each end over a carved
    return, unevenly worn, and the back arrises left square because they are
    buried in a wall. See THE WORKED TIMBER. The chamfer is measured along the
    WHOLE member, not per facet, so a scarfed timber's chamfer runs through the
    scarf the way the timber does."""
    r = rng(f"{p.name}/hewn/{seed}")
    xs, tz, bz = [], [], []
    for i, t in enumerate(_stations(spans, ease)):
        e = 0.0 if i in (0, spans) else 1.0
        d = sin(pi * t)                          # 0 at both ends
        xs.append(lerp(x0, x1, t))
        tz.append(z1 - top_sag * d + r.uniform(-top_wave, top_wave) * e - taper * t)
        bz.append(z0 - bot_sag * d + r.uniform(-bot_wave, bot_wave) * e)
    per = max(1, spans // max(1, facets))
    out, i0 = [], 0
    while i0 < spans:
        i1 = min(spans, i0 + per)
        if spans - i1 < per * .5:
            i1 = spans
        jy = r.uniform(0, face_jit)
        pb = [(xs[i], bz[i]) for i in range(i0, i1 + 1)]
        pt = [(xs[i], tz[i]) for i in range(i0, i1 + 1)]
        if i1 < spans:
            # SCARF THE JOINT. Two facets that stop dead on the same station
            # share their whole end face -- 720 cm2 of z-fighting on the 4m tie.
            # So each facet runs GAP past the station, drawn in top and bottom,
            # and dies INSIDE the next one instead of butting onto its plane.
            u = GAP / (xs[i1 + 1] - xs[i1])
            xj = lerp(xs[i1], xs[i1 + 1], u)
            pb.append((xj, lerp(bz[i1], bz[i1 + 1], u) + GAP * .5))
            pt.append((xj, lerp(tz[i1], tz[i1 + 1], u) - GAP * .5))
        poly = pb + pt[::-1]
        sh = shade * (1.0 + r.uniform(-.085, .085))
        if cham > 0:
            out += wprism(p, poly, (y1 - y0) + jy, mat, axis='Y',
                          at=(0, (y0 - jy + y1) / 2, 0), cf=cham, cb=0.0,
                          cw=_stop(x0, x1, cstop, CHAM_RET, cends),
                          seed=f"{seed}/{i0}", tint=tint, shade=sh)
        else:
            out += p.prism(poly, (y1 - y0) + jy, mat, axis='Y',
                           at=(0, (y0 - jy + y1) / 2, 0), bevel=bevel, seg=1,
                           tint=tint, shade=sh)
        i0 = i1
    return out


def _plank(p, x0, x1, z0, z1, y0, y1, mat, n=8, bevel=.010, tint=.05,
           shade=1.0, wave=.0015, seed=0, ease=.0):
    """A board running along X, built from its side elevation as a prism with
    `n` stations instead of as a box. It costs a handful of tris more and it is
    the only reason a cap board, a drip rail or an eave fascia can FOLLOW the
    beam it is nailed to when _bend() bows the piece -- a two-station box would
    simply stay straight and tear off the curve. `ease` clusters its stations
    toward its ends, exactly as in _hewn(), so a capping board on a RUN piece
    leaves the seam along the same crease-free curve as the timber under it."""
    r = rng(f"{p.name}/plank/{seed}")
    xs = [lerp(x0, x1, t) for t in _stations(n, ease)]
    jit = [0.0] + [r.uniform(-wave, wave) for _ in range(n - 1)] + [0.0]
    poly = ([(x, z0 + j) for x, j in zip(xs, jit)]
            + [(x, z1 + j) for x, j in zip(xs[::-1], jit[::-1])])
    return p.prism(poly, y1 - y0, mat, axis='Y', at=(0, (y0 + y1) / 2, 0),
                   bevel=bevel, seg=1, tint=tint, shade=shade)


def _bend(p, amp, span=G, at=0.0, shape='wave', z_ramp=None, y_ramp=None,
          power=2.0):
    """Bow EVERYTHING built so far, in one pass, around X. This is the whole
    reason the family reads as hand-cut: the beam, the cap board, the tooth
    course, the iron strap and every peg share ONE curve, because they are all
    deformed by the same function after they are built.

    `amp` > 0 sags, < 0 cambers up.  `shape`:
        'wave'  dz = amp * sin(pi t)^power -- any power above 1 gives zero
                displacement AND zero slope at both module ends, so tiled RUN
                pieces weld into one long swagging timber with no kink at the
                station. 2.0 is the default because it is the only value that
                also has BOUNDED CURVATURE there: below 2 the curve leaves the
                station with infinite curvature, so however finely the mesh
                samples it the first segment still dives (1.4 dropped 27mm in
                the first 200mm) and the joint shows a crease. 2.0 is also the
                honest shape -- it is the deflection of a beam continuous over
                its supports, which is what a bressummer on corbels is.
        'arc'   dz = amp * sin(pi t)   -- a plain arch for a POINT piece whose
                ends are free (the tie beam).
    `z_ramp` (lo, hi) fades the bend in with height so bearing pads and brace
    feet stay put while the member they carry rises: an arch brace then bends
    up from its foot instead of floating off its pad.
    `y_ramp` (at_wall, at_tip) does the same along Y, which is how a rafter
    tail droops further the further it cantilevers past the wall plate."""
    for v in p.bm.verts:
        t = clamp((v.co.x - (at - span / 2)) / span)
        s = sin(pi * t)
        if shape == 'wave':
            s = s ** power
        w = 1.0
        if z_ramp:
            w *= smoothstep(z_ramp[0], z_ramp[1], v.co.z)
        if y_ramp:
            w *= clamp((y_ramp[0] - v.co.y) / (y_ramp[0] - y_ramp[1]))
        v.co.z -= amp * s * w


def _bez(a, b, c, n=7):
    """Quadratic bezier a -> c with control b, inclusive of both ends."""
    out = []
    for i in range(n):
        t = i / (n - 1)
        u = 1 - t
        out.append((u * u * a[0] + 2 * u * t * b[0] + t * t * c[0],
                    u * u * a[1] + 2 * u * t * b[1] + t * t * c[1]))
    return out


def _mix(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def _off(pts, du, dv):
    return [(a + du, b + dv) for (a, b) in pts]


def _arch_brace(a, b, d, w=.20, arc=.20, n=7):
    """The curved brace both refs are full of: a slender timber of section `w`
    springing from a foot `b` on a post and landing on a head `d` under a beam,
    curved so that -- like every arch brace ever cut -- it leaves the post
    vertically, meets the beam horizontally and its soffit is CONCAVE toward
    the corner `a` those two members make, leaving the spandrel open.
    `arc` is the rise as a fraction of the chord; .20 is a quarter circle.
    Returns a closed polygon in the plane of the brace."""
    def unit(f, t):
        dx, dy = t[0] - f[0], t[1] - f[1]
        L = sqrt(dx * dx + dy * dy) or 1.0
        return (dx / L, dy / L)
    ub, ud = unit(b, a), unit(d, a)
    b2 = (b[0] + ub[0] * w, b[1] + ub[1] * w)
    d2 = (d[0] + ud[0] * w, d[1] + ud[1] * w)
    rise = arc * sqrt((d[0] - b[0]) ** 2 + (d[1] - b[1]) ** 2)

    def ctrl(p0, p1):
        m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        t = unit(m, a)                      # bow toward the corner
        return (m[0] + t[0] * 2 * rise, m[1] + t[1] * 2 * rise)
    return (_bez(b, ctrl(b, d), d, n) + [d2]
            + _bez(d2, ctrl(d2, b2), b2, n)[1:])


def _pegs(p, xs, face, z, r_=.026, stand=.030, h=.052, mat="oak_pale",
          axis='Y'):
    """OAK TRENAILS at a joint, standing proud of the face they are driven into.

    ROUND 9, and it is a family-agreement fix as much as a detail one. These
    were 21 mm `iron` dowels, untapered, on `y - out*.35` -- i.e. dark pegs in
    dark timber, which in SOLID viewport shading is one flat tone against the
    same flat tone and cannot be seen at all, and iron is the wrong material
    besides: a frame this size is pegged with riven oak, and timber_walls._peg
    (which the reviewer CAN see, because it is pale and tapered) already draws
    them that way. Same section, same taper, same `oak_pale`, same 6-gon here,
    so a bressummer's pegs and the pegs in the wall it is bedded in are the same
    detail. oak_pale is not a cheat: the kit table gives it to "newly cut ends",
    and the sawn end grain of a peg is exactly that, and the heads are the only
    pale thing on the timber so "sparingly" holds.

    `face` is the plane of the member the peg is driven INTO, which is what the
    old signature got wrong at three call sites: corbel_knee's lower peg was at
    y = -0.30 inside a pad whose face is -0.43, i.e. 130 mm deep in solid oak,
    and the porch post's two were 54 mm out of a flat they were nominally 12 mm
    off. `stand` is how far the head stands out of that face; the fat end is the
    OUTER one, which is how a riven peg is driven and leaves the head on a
    shoulder of its own.
    """
    for x in xs:
        c = ((x, face - stand + h / 2, z) if axis == 'Y'
             else (face - stand + h / 2, x, z))
        p.cyl(c, r_, h, mat, sides=6, axis=axis, tint=.06, phase=.4,
              r_top=r_ * .78)


# ---------------------------------------------------------- 1. jetty sill ----
# Each variant, and SM_Corner_JettyJoint with it, is ONE SWEPT SOLID per member:
# the timber, and the weather board over it. Nothing in the run butts anything
# else face to face, and every deformation applied afterwards is zero -- with
# zero slope -- at the butt planes. That is what makes a run read as one timber:
#
#   * THE CHAMFER IS PART OF THE SOLID'S OWN PLAN (see sweep/sill_bands), so
#     the butt faces are dead flat. It used to be a bmesh bevel, and
#     bmesh.ops.bevel chamfers EVERY arris of a primitive including the two
#     ends: two sills butted then met chamfer to chamfer and left a 26 mm
#     V-groove round the whole section at x = 0, 2, 4, 6. That groove is the
#     line Shanee can see between A.024 and B.007 and between A.024 and the
#     corner. Nothing about the old SECTION was wrong -- the toolmark was.
#   * ONE TONE, flat, no per-prism jitter (SILL_TONE): a 8.5% shade step
#     between two butted sills draws the joint just as clearly as a groove.
#   * the swag (_bend, sin^2), the adze wander (_fade) and wobble all vanish at
#     x = +-SILL_END, so the two halves of a joint leave it along one tangent.
#
# SILL_EASE is part of the shared section too, like the chamfer: it decides how
# the mesh samples the swag as it leaves the seam, and two variants sampling it
# differently would leave the joint at two different angles.
SILL_EASE = 0.75


def sill_bands(dz=0.0, board=False):
    """THE BUTTING PROFILE, as a stack of (z, inset) bands from soffit to top.

    `inset` is how far that level is drawn in from the plan, so the chamfer is
    built INTO the solid and the section a neighbour meets is exactly this
    table. `dz` lifts the whole stack: SM_Corner_JettyJoint states the same
    section in its own frame, because it is placed JETTY_BAND below the storey
    line where a run piece is placed SILL_H below it. `board` gives the weather
    board's bands instead of the timber's."""
    if board:
        z0, z1, b = (SILL_TOP - SILL_CAP - SILL_CAP_LAP, SILL_TOP, SILL_CAP_BEV)
    else:
        z0, z1, b = SILL_SOF, SILL_TOP - SILL_CAP, SILL_BEV
    return [(z0 + dz, b), (z0 + b + dz, 0.0), (z1 - b + dz, 0.0), (z1 + dz, b)]


def sill_fall(board=False):
    """How far the FRONT rail of that member sits below its back one -- the
    weather board's shed. Shared, so the corner sheds by exactly as much."""
    return SILL_CAP_FALL if board else 0.0


def sweep(p, front, back, bands, mat, tint=.0, shade=1.0, fall=0.0):
    """ONE continuous closed solid, lofted from two RAILS through `bands`.

    front/back  equal-length lists of ((x, y), (ox, oy), k): the plan of the
                exposed face and of the back, each vertex carrying the direction
                it travels when a band insets, and k scaling that inset locally
                (the stop-chamfer). A vertex ON A BUTT PLANE carries no
                component across it, so the cut stays square and the arriving
                piece's cut matches it exactly.
    bands       from sill_bands().

    No util primitive can do this: box/prism/beam all chamfer with
    bmesh.ops.bevel, which cuts the end faces too. Lofted rail to rail rather
    than capped with one n-gon, so the soffit -- the face you see from the
    street, under the jetty -- stays quads once the beam is swagged."""
    plan = list(front) + list(back)[::-1]
    m, n = len(front), len(front) * 2
    vs = [(x + ox * ins * k, y + oy * ins * k, z - (fall if i < m else 0.0))
          for (z, ins) in bands
          for i, ((x, y), (ox, oy), k) in enumerate(plan)]
    F = []
    for ri in range(len(bands) - 1):
        for j in range(n):
            j2 = (j + 1) % n
            F.append((ri * n + j, ri * n + j2, (ri + 1) * n + j2, (ri + 1) * n + j))
    top = (len(bands) - 1) * n
    for j in range(m - 1):                      # soffit and top, rail to rail
        q = (j, j + 1, n - 2 - j, n - 1 - j)
        F.append(q[::-1])
        F.append(tuple(top + i for i in q))
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _efade(x, x0, x1, m=.30):
    """`_fade` for a member that is not the sill run: 1.0 inside, 0.0 with zero
    slope at x0 and x1, so a carved deviation cannot open or crease a tiling
    joint wherever the member happens to start and end."""
    return smoothstep(0, m, x - x0) * smoothstep(0, m, x1 - x)


def sweep_box(p, x0, x1, y0, y1, z0, z1, mat, n=6, bev=.014, ease=SILL_EASE,
              tint=.0, shade=1.0, stop=0.0, wear=0.0, seed=0):
    """A straight RUN member of chamfered rectangular section, swept so its two
    ENDS ARE CUT DEAD FLAT -- the jetty sill's fix applied to the family's other
    run piece, the eave. A p.box / p.beam / _plank of the same section is
    chamfered by bmesh.ops.bevel, which cuts the two END faces as well, so a row
    of them shows a 2*bev groove round the whole section at every 2m tile -- and
    on an eave that groove lands in the one line the whole roof is read along.
    Flat tone for the same reason the sill run has one: a per-piece shade jitter
    draws the joint even when the geometry does not.

    `stop` waists the chamfer over the member's centre and `wear` makes its
    width wander -- the same two carved details the sill run carries (see
    sill_rails), for the same zero tris, and both faded to nothing at the two
    tiling planes so the section a neighbour meets is unchanged. On an eave
    fascia that matters more than anywhere else in the kit: it is the one line
    the whole roof is read along, and a dead-constant 12 mm chamfer down 8 m of
    it is the machine mark that makes the eave look extruded."""
    bands = [(z0, bev), (z0 + bev, 0.0), (z1 - bev, 0.0), (z1, bev)]
    xs = [lerp(x0, x1, t) for t in _stations(n, ease)]
    r = rng(f"{p.name}/sweepbox/{seed}")
    p3, p4 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
    w3, w4 = r.uniform(1.9, 2.8), r.uniform(4.3, 5.9)
    xc = (x0 + x1) / 2
    ks = []
    for x in xs:
        k = 1.0 - stop * _win(x, at=xc)
        if wear > 0:
            k *= 1.0 + wear * _efade(x, x0, x1) * (.62 * sin(w3 * x + p3)
                                                   + .38 * sin(w4 * x + p4))
        ks.append(k)
    fr = [((x, y0), (0.0, 1.0), k) for x, k in zip(xs, ks)]
    bk = [((x, y1), (0.0, -1.0), k) for x, k in zip(xs, ks)]
    return sweep(p, fr, bk, bands, mat, tint=tint, shade=shade)


def _fade(x, m=0.30):
    """1.0 deep inside a run piece, 0.0 -- with zero slope -- at both butt
    planes. Every hand-made irregularity on a run piece is multiplied by this,
    which is why none of it can open or crease a joint."""
    return smoothstep(0, m, x + SILL_END) * smoothstep(0, m, SILL_END - x)


def _win(x, at=0.0, half=0.30):
    """Smooth window: 1 at `at`, 0 beyond +-half."""
    t = clamp((half - abs(x - at)) / (half * 0.55))
    return t * t * (3 - 2 * t)


def sill_rails(board=False, n=8, wander=0.0, breaks=(), stop=0.0, seed=0,
               wear=0.0):
    """The two plan rails of a 2m RUN piece: the face with its adze wander and
    its facet arrises, the back, and between them two dead-flat butt cuts.

    `wander`  how far the face strays from SILL_FACE mid-bay (times _fade, so
              zero at both butt planes).
    `breaks`  x positions of ADZE FACET ARRISES. A pair of stations 11 mm apart
              with a step of at least 1.1*wander in the face between them, so
              the crease clears SMOOTH_ANG (34 deg) and stays a hard arris:
              10 mm of wander spread over a 200 mm station is 3 degrees and
              shade-smooths away to nothing, and even 8 mm over 20 mm was still
              soft. Facet levels alternate in sign for the same reason. This is
              how the timber reads hand-hewn as FORM -- which is what survives
              Solid shading -- for ~16 tris a facet, and it can never open a
              joint because it is part of the swept solid and dies in _fade.
    `stop`    waists the chamfer over the bay centre: THE CARVED STOP-CHAMFER,
              where the arris squares up to take a bracket. Done by scaling the
              band inset, so it costs nothing and cannot touch the butt cut.
    `wear`    ARRIS WEAR, and it is the cheapest detail in the family: the same
              band-inset scale, modulated by two slow sines, so the chamfer is
              14 mm wide in one place and 30 mm in the next instead of a dead
              constant 22 mm down the whole 2 m. A uniform chamfer is a machine
              mark; an uneven one is a drawknife. Costs ZERO tris -- it moves
              vertices the sweep was going to emit anyway -- and it is 1.0 at
              both butt planes (times _fade), so the section a neighbour meets
              is untouched to the micron."""
    r = rng(f"beams/sill_rails/{seed}")
    p1, p2 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
    w1, w2 = r.uniform(2.2, 3.2), r.uniform(5.0, 7.0)
    p3, p4 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
    w3, w4 = r.uniform(1.7, 2.6), r.uniform(4.1, 5.6)
    brk = [clamp(b, -SILL_END + .14, SILL_END - .14) for b in breaks]
    sg = 1 if r.random() < .5 else -1
    lvl = []
    for i in range(len(brk) + 1):
        lvl.append(sg * r.uniform(.55, 1.0))
        sg = -sg
    f = SILL_FACE - (SILL_CAP_O if board else 0.0)
    xs = [lerp(-SILL_END, SILL_END, t) for t in _stations(n, SILL_EASE)]
    for b in brk:
        xs += [b - .0055, b + .0055]
    xs = sorted(xs)
    keep = [xs[0]]
    for x in xs[1:]:
        if x - keep[-1] > .004:
            keep.append(x)
    keep[-1] = SILL_END                       # the butt cut, to the micron
    front, back = [], []
    for x in keep:
        i = sum(1 for b in brk if x > b)
        dy = -_fade(x) * wander * (.45 * sin(w1 * x + p1)
                                   + .25 * sin(w2 * x + p2) + lvl[i])
        k = 1.0 - stop * _win(x)
        if wear > 0:
            k *= 1.0 + wear * _fade(x) * (.62 * sin(w3 * x + p3)
                                          + .38 * sin(w4 * x + p4))
        front.append(((x, f + dy), (0.0, 1.0), k))
        back.append(((x, SILL_BACK), (0.0, -1.0), k))
    return front, back


def sill_corner_rails(T=SILL_CELL, board=False):
    """The plan rails of the CORNER that terminates a run: one mitred L, which
    presents the section on x = SILL_JOINT_X and on y = SILL_JOINT_Y and turns
    the arris between them as ONE SOLID.

    This lives here, not in corners.py, because it IS the interface: two boxes
    lapped at the corner (which is what it was) butt face to face across the
    weather board's top -- the ledge you look straight down on at the outside
    corner of the building -- and each brought its own bevel to that butt, so
    the corner carried a chamfered groove straight across itself. That is the
    'visible seam/line in itself' Shanee found in SM_Corner_JettyJoint.005.
    A mitred L has no butt to show."""
    f = SILL_FACE - (SILL_CAP_O if board else 0.0)
    b = SILL_BACK
    front = [((SILL_JOINT_X, f), (0.0, 1.0), 1.0),      # on the X butt plane
             ((-T + f, f), (1.0, 1.0), 1.0),            # the outside arris
             ((-T + f, T), (1.0, 0.0), 1.0)]            # on the Y butt plane
    back = [((SILL_JOINT_X, b), (0.0, -1.0), 1.0),
            ((-T + b, b), (-1.0, -1.0), 1.0),           # the inside armpit
            ((-T + b, T), (-1.0, 0.0), 1.0)]
    return front, back


def _adze(p, rise=.007, lean=.052, seed=0, tilt=0.0, breaks=()):
    """The hand-hewn deformations, applied to the bare swept timber before any
    detail is added to it. All of them die at the butt planes.

    `rise` wanders the SOFFIT arris. Only the two bottom bands move, so the
    chamfer travels with the face it belongs to. Upward only, and that is not
    fussiness: SILL_BOW == SILL_SOF is an invariant, so the swag already brings
    the soffit to exactly z = 0 at the bay centre and anything added downward
    puts the piece outside its own snap box. An adze takes wood off anyway.

    `lean` TILTS THE FACET ARRISES off plumb, bottom one way and top the other.
    A hewn face really is faceted across the grain, so the arrises between
    facets are roughly upright -- but a dead-plumb hard crease on the face of a
    beam is exactly what a butt joint looks like, and this family is being fixed
    BECAUSE of butt joints that showed. Leaning them ~14 degrees, and putting
    them at positions that are not multiples of anything, makes them unmistakably
    a toolmark. The shift is faded to zero over the last 100mm, so the cut faces
    stay dead flat and dead square: only the stations between them lean.

    `tilt` TILTS EACH FACET'S PLANE, alternately, and it is the round-9 fix for
    the reason none of this carving could be SEEN in Solid shading. The facets
    stepped inward in PARALLEL -- two neighbouring facets had the SAME NORMAL,
    so the hard crease between them separated two identical values and read as
    nothing at all. A sharp edge is only visible if the two faces it divides
    shade differently. Now facet 0 cuts FACET_TILT deeper at the top, facet 1
    deeper at the bottom, and so on, so consecutive facets differ by
    2*atan(tilt/face height) ~ 7 degrees and the face of the beam reads as three
    long axe flats with a hard stop between them. `breaks` has to be the list
    `sill_rails` got, so the sign flips ON the 11 mm crease station pair instead
    of in the middle of a flat. Inward only (an adze takes wood off, and outward
    spends the proud allowance), and times _fade, so the butting section is
    untouched."""
    if rise <= 0 and lean <= 0 and tilt <= 0:
        return
    r = rng(f"beams/adze/{seed}")
    p1, p2 = r.uniform(0, 2 * pi), r.uniform(0, 2 * pi)
    w1, w2 = r.uniform(3.0, 4.2), r.uniform(7.0, 9.0)
    lid = SILL_SOF + SILL_BEV + .001
    zc = SILL_TOP - SILL_CAP
    mid = (SILL_FACE + SILL_BACK) / 2       # anything in front of this is FACE
    brk = sorted(breaks)
    for v in p.bm.verts:
        x0 = v.co.x                          # regions come off the UNLEANED x
        f = _fade(x0, .10)
        t = clamp((v.co.z - SILL_SOF) / (zc - SILL_SOF))
        if tilt > 0 and v.co.y < mid and v.co.z <= zc + 1e-4:
            up = (sum(1 for b in brk if x0 > b) % 2) == 0
            v.co.y += tilt * (t if up else 1.0 - t) * _fade(x0)
        if lean > 0 and f > 0:
            v.co.x += lean * (2 * t - 1) * f
        if rise > 0 and v.co.z <= lid:
            s = .62 * sin(w1 * x0 + p1) + .38 * sin(w2 * x0 + p2)
            v.co.z += rise * _fade(x0) * abs(s)


def _sill_beam(p, seed, spans=8, wander=.007, breaks=(), stop=.86, adze=.007,
               lean=.052, wear=.30, tilt=FACET_TILT):
    """The bressummer, and THE SHARED SECTION (see THE JETTY SILL PROFILE).
    Every variant calls this with the same bands and the same rail geometry at
    the butt planes; only the carving between them differs.

    `wear` and `tilt` are the round-9 carving, and neither costs a single tri:
    an unevenly worn chamfer (see sill_rails) and facet planes that actually
    differ in normal (see _adze). Both are 0 at the butt planes."""
    front, back = sill_rails(n=spans, wander=wander, breaks=breaks, stop=stop,
                             seed=seed, wear=wear)
    sweep(p, front, back, sill_bands(), "oak_dark", shade=SILL_TONE)
    _adze(p, rise=adze, lean=lean, seed=seed, tilt=tilt, breaks=breaks)


def _sill_cap(p, seed, spans=7):
    """Weather board -- the TOP BAND of the shared section, on every variant.
    It runs the full length, lips SILL_CAP_O proud of the beam face and throws
    the shadow line that makes the swag read at a distance (ref1's jetty). Swept
    like the timber, so it swags with it and its ends are cut just as flat.
    Left dead straight in plan on purpose: a sawn board on a hewn beam.

    It reaches SILL_CAP_LAP down INTO that timber rather than sitting on its top
    face: two opaque coplanar faces z-fight, and this pair used to fight along
    the whole 2m. That lap is a shared constant because it sets where the
    board's lower arris -- the shadow line the eye follows along a whole jetty
    -- actually lands."""
    front, back = sill_rails(board=True, n=spans, seed=seed + 40)
    sweep(p, front, back, sill_bands(board=True), "oak_mid",
          shade=SILL_CAP_TONE, fall=sill_fall(True))


def _sill_back(p):
    """The BEARING the beam is housed on, behind the wall face. Called AFTER the
    bend and left dead straight on purpose: it is the joist line the storey
    above sits on, so the bressummer swags off its outer face instead of
    dragging the whole floor down with it -- which is exactly how ref1's jetty
    reads, a straight floor edge with a drooping beam bolted to it.

    Its outer face is GAP INSIDE the timber's back face instead of on it. That
    one shared plane was the family's single worst z-fighting pair (~4800 cm2
    per variant): two opaque faces on y = SILL_BACK, flickering against each
    other. Buried inside the beam it cannot be the frontmost thing anywhere.

    ROUND 9 -- it is a HOUSING now, not a floor: SILL_TAIL deep instead of a
    whole wall thickness, and its top HOUSE_DZ under the storey line. Read the
    block at SILL_TAIL for the measurements. Both of its horizontal faces used to
    land exactly on a face of the wall it sits in, which is the z-fighting
    Shanee named; neither does now, and the beam beds 50 mm into the frame the
    way a bressummer beds into it."""
    y0 = SILL_BACK - GAP
    z0, z1 = SILL_SOF + HOUSE_DZ * .5, SILL_TOP - HOUSE_DZ
    p.plate((0, (y0 + SILL_TAIL) / 2, (z0 + z1) / 2),
            (G, SILL_TAIL - y0, z1 - z0), "oak_dark", tint=.03,
            shade=.62)


def _sill_finish(p):
    """Bend, back-plate and wobble -- identical for all three variants. The
    wobble numbers are part of the shared section: util.wobble() is a function
    of world position, so the same amount and frequency deform A, B and C
    identically and the joint stays shut."""
    _bend(p, SILL_BOW)                       # <-- the whole beam swags as one
    _sill_back(p)
    p.wobble(.005, freq=1.15)
    return p.finish()


def sill_a():
    """Plain heavy bressummer -- the workhorse. Three long adze facets down the
    face with a crease between them, a stop-chamfer squaring the arris up over
    the bracket at the bay centre, a wandering soffit, four pegs, its weather
    board, and the SILL_BOW swag between its brackets like every jetty beam in
    both references."""
    p = Part("SM_Beam_JettySill_2m_A", budget="beam", seams=dict(SILL_SEAM))
    _sill_beam(p, seed=1, spans=8, wander=.0075,
               breaks=(-.615, -.235, .185, .585),
               stop=.88, adze=.007, lean=.052, wear=.34)
    _sill_cap(p, seed=1)
    _pegs(p, (-.58, .69), SILL_FACE, .26, r_=.026)
    _pegs(p, (.11,), SILL_FACE, .37, r_=.024)
    _pegs(p, (-.20, .20), SILL_FACE, .105, r_=.022)   # the bracket's tenon pegs
    return _sill_finish(p)


def sill_b():
    """The same timber with a joist-end tooth course standing proud along its
    lower face -- ref3 runs a fine tooth course under every jetty, eave and
    barge. The teeth swag with the beam, so the tooth line is a curve.

    The teeth sit ON the face, clear of the soffit and INSET from both seams:
    hung under the soffit (as they were) they made B's silhouette 105mm
    shallower than A's at the joint, which is the step Shanee found.

    The quietest variant otherwise -- gentlest adze wander, two facets, a light
    chamfer stop -- because it is the one carrying the most applied detail and a
    tooth course over a strongly hewn face reads as noise."""
    p = Part("SM_Beam_JettySill_2m_B", budget="beam", seams=dict(SILL_SEAM))
    _sill_beam(p, seed=2, spans=8, wander=.0045, breaks=(-.475, .105, .435),
               stop=.55, adze=.005, lean=.038, wear=.26,
               tilt=FACET_TILT * .72)
    _sill_cap(p, seed=2)
    # ... clear of the section's chamfer band (SILL_SOF + SILL_BEV) and of the
    # adze rise, so the teeth stand ON the face and never break the arris
    p.dentil((-.86, .86), SILL_SOF + .086, SILL_FACE - .0125, "oak_dark", n=8,
             size=(.075, .065, .098), tint=.06, seed=2)
    # moulded fillet run along the face just under the weather board
    _plank(p, -.86, .86, SILL_TOP - SILL_CAP - .068, SILL_TOP - SILL_CAP - .018,
           SILL_FACE - .012, SILL_FACE + .040, "oak_mid", n=7, bevel=.010,
           tint=.05, shade=.92, seed=2)
    _pegs(p, (-.30, .46), SILL_FACE, .37, r_=.026)
    return _sill_finish(p)


def sill_c():
    """Rough half-hewn timber: FOUR adze facets down the face with the deepest
    wander and the hardest chamfer stop of the three, a drip rail lipped along
    its face and an iron strap over a scarf joint. The rail and the strap are
    inset from both seams and the timber is NOT tapered any more -- the old 30mm
    taper along its length meant a run of C's stepped down 30mm at every joint
    and 30mm up against an A or a B."""
    p = Part("SM_Beam_JettySill_2m_C", budget="beam", seams=dict(SILL_SEAM))
    _sill_beam(p, seed=3, spans=8, wander=.0105,
               breaks=(-.705, -.225, .285, .705), stop=.92, adze=.008,
               lean=.066, wear=.40, tilt=FACET_TILT * 1.15)
    _sill_cap(p, seed=3)
    # drip rail along the face, clear of the soffit so the two do not share it
    # -- and clear of the adze rise as well, which can lift the soffit 8mm
    _plank(p, -.88, .88, SILL_SOF + .028, SILL_SOF + .105,
           SILL_FACE - .014, SILL_FACE + .052, "oak_mid", n=9, bevel=.010,
           tint=.05, shade=.92, seed=3)
    # scarf joint: a raised block on the face plus an iron strap over it
    p.box((.30, SILL_FACE + .045, .322), (.15, .115, .164), "oak_mid",
          bevel=.010, seg=1, tint=.05, shade=1.08)
    p.box((.30, SILL_FACE + .012, .325), (.05, .07, .14), "iron", bevel=.008,
          seg=1, tint=.03)
    _pegs(p, (-.55, .82), SILL_FACE, .30, r_=.026)
    return _sill_finish(p)


# -------------------------------------------------------- 2. corbels ---------
def corbel_scroll():
    """Carved ogee corbel: a moulded pad, a hollow-chamfered throat and a
    curled volute nose. The decorated bracket under a jetty beam or a beam
    end, and the one to put where the eye goes.

    ROUND 9: WORKED, not bevelled. The volute was a prism with a uniform 15 mm
    bmesh bevel on every arris, i.e. the soap bar. Now `wprism` cuts a real
    stop-chamfer round the profile on BOTH cheeks -- unevenly worn, dying where
    the bracket enters the wall and where it enters the abacus, because that is
    where a carver's chamfer stops and because a chamfer on a buried arris is
    tris spent on nothing."""
    W = .25
    p = Part("SM_Beam_CorbelScroll", budget="beam",
             seams=dict(x=(-.18, .18), y=(-J - .10, .14), z=(0, CORBEL_H)))
    top = CORBEL_H - .11 + GAP          # dies INSIDE the abacus above, not on
    nose = (-.235, .105)                # its underside: that shared plane was
                                        # 1090 cm2 of z-fighting on its own
    prof = ([(.09, .0), (-.20, .0), (-.29, .045), nose,        # the volute toe
             (-.275, .20)]                                     # fillet step
            + _bez((-.275, .20), (-.30, .33), (-(J - .015), top), 5)
            + [(.09, top)])
    # u is y (out of the wall), v is z: the chamfer dies as the profile turns
    # back into the wall (u > 0.02) and as it climbs into the abacus
    wprism(p, prof, W, "oak_dark", axis='X', cf=CHAM, cb=CHAM, tint=.07,
           shade=.95, seed=1,
           cw=lambda u, v: clamp(min((.02 - u) / .05, (top - .050 - v) / .055)))
    # abacus: wider than the body, so the bracket reads as a capital
    p.box((0, -.175, CORBEL_H - .055), (W + .09, .55, .11), "oak_mid",
          bevel=.014, seg=1, tint=.05, shade=1.08)
    # carved eye of the volute, sunk into both cheeks
    for sx in (-1, 1):
        p.cyl((sx * (W / 2 - .008), -.245, .175), .048, .026, "oak_mid",
              sides=9, axis='X', tint=.05, shade=1.14)
    _pegs(p, (0,), -.450, CORBEL_H - .055, r_=.024)
    p.wobble(.004)
    return p.finish()


def corbel_knee():
    """Slim curved knee brace -- ref1's right-hand jetty is carried on these.
    The free edge bows hard toward the wall/beam corner, which is what gives it
    a scythe silhouette instead of reading as a filled triangle."""
    W = .19
    p = Part("SM_Beam_CorbelKnee", budget="beam",
             seams=dict(x=(-.13, .13), y=(-J - .10, .16), z=(0, CORBEL_H)))
    A = (.11, CORBEL_H - .075)                # inner corner: wall x soffit
    B = (.11, .0)                             # foot, down the wall
    D = (-(J - .02), CORBEL_H - .075)         # head, under the beam's face
    # WORKED, not bevelled (see THE WORKED TIMBER): a stop-chamfer down the
    # brace's two long arrises on both cheeks, dying at the foot, at the head
    # and where it beds against the wall face -- the three ends that are joints.
    HD = CORBEL_H - .075
    wprism(p, _arch_brace(A, B, D, w=.225, arc=.18), W, "oak_dark", axis='X',
           cf=CHAM, cb=CHAM, tint=.07, shade=.95, seed=2,
           cw=lambda u, v: clamp(min((.055 - u) / .05, (v - .010) / .060,
                                     (HD - .030 - v) / .050)))
    # bearing pad under the beam + a spur block down the wall face. Both reach
    # GAP INTO the brace rather than landing on its head and its back face --
    # those two shared planes were the whole of this piece's z-fighting.
    p.box((0, -.155, CORBEL_H - .0405), (W + .07, .55, .081), "oak_mid",
          bevel=.012, seg=1, tint=.05, shade=1.08)
    p.box((0, .056, .155), (W + .05, .12, .31), "oak_mid", bevel=.012, seg=1,
          tint=.05, shade=.96)
    # the pad's front face is y = -0.43 and the spur's is -0.004: the lower peg
    # used to be given y = -0.30, i.e. driven 130 mm INSIDE solid oak, so it was
    # a cylinder nobody could ever see
    _pegs(p, (0,), -.430, CORBEL_H - .040, r_=.024)
    _pegs(p, (0,), -.004, .170, r_=.022)
    p.wobble(.004)
    return p.finish()


# ---------------------------------------------------------- 3. porch post ----
def porch_post():
    """Chamfered porch post: splayed foot, square stops, octagonal shaft bowed
    POST_BOW out of plumb, a modest bolster head and two long thin curved
    braces sweeping up to the beam it carries. Height = H_GROUND - SILL_H, so
    it takes a sill run directly -- stand it under the CENTRE of a bay, where
    the sill's swag comes down to meet its head."""
    p = Part("SM_Beam_PorchPost", budget="beam",
             seams=dict(x=(-.76, .76), y=(-.21, .21), z=(0, POST_H)))
    W = .0998                                  # 0.20 across the flats
    p.box((0, 0, .08), (.35, .35, .16), "oak_dark", bevel=.015, seg=1,
          tint=.05, taper=.82, taper_axis='XY', shade=.82)
    p.box((0, 0, .196), (.26, .26, .084), "oak_mid", bevel=.012, seg=1,
          tint=.05, shade=.98)      # laps GAP down into the splayed foot
    # THE SHAFT, with SQUARE STOPS at both ends (oct_shaft). It was three cyl
    # lifts -- a constant octagon whose ends had to be hidden under the two
    # collars, i.e. a chamfer that never stopped. The collars are shallower now
    # so 90mm of squared timber shows above the foot and below the head with the
    # chamfers running out of it, which is how a chamfered post is finished and
    # the most characteristic bit of carpentry on the piece. Still ONE solid, so
    # the pole can be bowed out of plumb below without a step at a joint.
    oct_shaft(p, .232, 2.290, W, W * .93, "oak_mid", ret=.090, mids=3,
              tint=.055, seed=3)
    p.box((0, 0, 2.336), (.25, .25, .080), "oak_mid", bevel=.012, seg=1,
          tint=.05, shade=.98)      # laps GAP down over the shaft's top ring
    # bolster head: a bearing block, not a flared capital
    p.box((0, 0, 2.440), (.42, .235, .164), "oak_dark", bevel=.015, seg=1,
          tint=.05, taper=.86, shade=.88)
    # long thin braces sweeping up to the beam soffit. Their feet are set
    # inside the octagon's flats (x = +/-0.0998), not on them: on them, the
    # brace's foot face and the shaft's flat were one plane.
    for sx in (-1, 1):
        A = (sx * .086, 2.375)
        B = (sx * .086, 1.93)
        D = (sx * .57, 2.375)
        # worked, with the chamfer dying into the shaft at the foot and into
        # the bolster at the head -- the two ends that are tenons
        wprism(p, _arch_brace(A, B, D, w=.15, arc=.20), .15, "oak_mid",
               axis='Y', cf=CHAM * .8, cb=CHAM * .8, tint=.06, shade=.93,
               seed=f"brace{sx}",
               cw=lambda u, v: clamp(min((abs(u) - .115) / .06,
                                         (.520 - abs(u)) / .050,
                                         (2.330 - v) / .055)))
    # the shaft's flats are at +-0.0998, so that is the face a peg is driven
    # into: at -0.112 and -0.118 they stood 54mm out of it like nails
    _pegs(p, (0,), -.0998, 2.02, r_=.024)
    _pegs(p, (0,), -.0998, 1.42, r_=.024)
    # bow the whole post out of plumb, foot and head left where they were, so
    # the shaft leans out at mid height and the braces lean with it
    for v in p.bm.verts:
        v.co.y -= POST_BOW * sin(pi * clamp(v.co.z / POST_H))
    p.wobble(.005)
    return p.finish()


# ------------------------------------------------------------- 4. lintel -----
def lintel_door():
    """Door lintel: a heavy timber with a strongly cambered soffit and a carved
    diamond boss, carried on a stepped ogee corbel at each end -- the way every
    timber head over a door sits in ref1. 1.70 long, so it centres in a 2m bay
    over a door_main or door_cellar head. The soffit rises LINT_CAM at the
    crown, so the opening under it is an arch, not a slot."""
    L = 1.70
    p = Part("SM_Beam_LintelDoor", budget="beam",
             seams=dict(x=(-L / 2, L / 2), y=(-.19, .26), z=(0, .46)))
    y0, y1 = -.15, .24
    # WORKED: a stop-chamfer down both front arrises, dying at |x| = 0.70 --
    # which is exactly where the two chamfer-stop blocks below stand. Those
    # blocks were already modelled and commented as "where the beam's chamfer
    # dies", but the beam had no chamfer to stop: `_hewn` gave it one uniform
    # 14mm bmesh bevel from end to end, so the blocks stopped nothing.
    _hewn(p, -L / 2, L / 2, .115, .445, y0, y1, "oak_dark", seed=5, spans=9,
          top_wave=.010, top_sag=.014, bot_sag=-LINT_CAM,
          cham=CHAM, cstop=L / 2 - .70)
    for sx in (-1, 1):
        # stepped ogee corbel under each end, top level with the soffit springing
        prof = ([(.15, .0), (-.10, .0), (-.155, .032), (-.145, .068),
                 (-.20, .080)]
                + _bez((-.20, .080), (-.215, .108), (-.255, .140), 3)
                + [(.15, .140)])
        wprism(p, prof, .24, "oak_mid", axis='X', at=(sx * .70, 0, 0),
               cf=CHAM * .7, cb=CHAM * .7, tint=.06, shade=.94,
               seed=f"corb{sx}",
               cw=lambda u, v: clamp(min((.10 - u) / .05, (v - .012) / .030)))
        # chamfer stop: a square block where the beam's chamfer dies. It
        # stands 2*GAP proud of the beam face -- 2mm behind it, as it was, put
        # its front face on the same plane (100 cm2).
        p.box((sx * .70, y0 + .019, .28), (.075, .062, .20), "oak_mid",
              bevel=.010, seg=1, tint=.05, shade=1.02)
    # carved diamond boss on the face, the way ref3 studs its gables -- it sits
    # up in the crown, where the cambered soffit has left the deepest timber
    p.box((0, y0 + .028, .345), (.16, .075, .16), "oak_mid", bevel=.013,
          seg=1, tint=.05, rot=(0, 45, 0), shade=1.10)
    _pegs(p, (-.44, .44), y0, .33)
    p.wobble(.004)
    return p.finish()


# ----------------------------------------------------------- 5. tie beam -----
def tie_beam():
    """Arch-braced tie beam, 2 bays long: a tie CAMBERED UP TIE_CAM over its
    4m span (6% -- a tie beam is cambered so it never reads as sagged, which is
    the one horizontal in the kit that bows upward), two long curved braces
    under its ends on pad blocks, and a king-post seat riding the crown. Runs
    along X -- use it as the girding beam over a jetty run, or rotate it 90 to
    tie across a bay the way ref3's big gable does.

    The camber is applied to the whole assembly with a z-ramp, so the pads stay
    flat on their posts while the brace heads travel up with the soffit they
    land on -- the braces bend from the foot, and the arch stays closed."""
    L = 2 * G
    p = Part("SM_Beam_TieBeam_4m", budget="beam",
             seams=dict(x=(-L / 2, L / 2), y=(-.17, .17), z=(0, 1.36)))
    zb, zt = .64, .95
    # WORKED: three scarfed lifts, each with the stop-chamfer running through
    # the scarf the way the timber does (the chamfer is measured on the whole
    # 4 m member, not per facet), dying 0.22 short of each end where the tie is
    # framed into its posts.
    _hewn(p, -L / 2, L / 2, zb, zt, -.145, .145, "oak_dark", seed=6, spans=12,
          facets=3, face_jit=.016, top_wave=.009, bot_wave=.006,
          cham=CHAM, cstop=.22)
    for sx in (-1, 1):
        A = (sx * 1.79, zb + .02)
        B = (sx * 1.79, .10)
        D = (sx * .82, zb + .02)
        wprism(p, _arch_brace(A, B, D, w=.26, arc=.17), .215, "oak_mid",
               axis='Y', cf=CHAM, cb=CHAM, tint=.06, shade=.93,
               seed=f"tbrace{sx}",
               cw=lambda u, v: clamp(min((1.66 - abs(u)) / .09,
                                         (v - .14) / .07, (zb - .02 - v) / .06)))
        p.box((sx * 1.75, 0, .11), (.32, .32, .22), "oak_dark", bevel=.015,
              seg=1, tint=.05, shade=.84)
    # king-post seat, standing on the camber. It is bedded 20mm INTO the tie's
    # top: sitting on it, the two faces tracked each other through the camber
    # and stayed inside the coplanar tolerance for 240 cm2.
    p.box((0, 0, 1.000), (.24, .26, .14), "oak_mid", bevel=.013, seg=1,
          tint=.05, shade=1.08)
    _pegs(p, (-1.34, -.94, .94, 1.34), -.145, .82)
    _bend(p, -TIE_CAM, span=L, shape='arc', z_ramp=(.16, .60))
    p.wobble(.005)
    return p.finish()


# -------------------------------------------------------- 6. rafter tails ----
def rafter_tails():
    """The run of exposed rafter tails under a swept eave: a wall plate, five
    tails cantilevering EAVE_OVER past the wall face, each bell-cast so it
    flattens toward its cut nose, the boarded deck over their inner half, the
    fascia plank they are nailed through, and a tooth course hung under it. The
    tail ends poke out THROUGH the fascia, exactly as they do in ref1.

    THE SWEEP: the wall plate is bedded on the wall and stays dead straight,
    while everything that cantilevers past the wall face droops -- linearly
    with how far it reaches out, EAVE_BOW at the fascia, mid-bay. So the eave
    line dips between bays and lifts at every station, which is the swept,
    upturned eave both references live on, and the fascia and tooth course
    follow it instead of cutting across it."""
    p = Part("SM_Beam_RafterTails_2m", budget="beam",
             seams=dict(x=(-G / 2, G / 2), y=(-.72, .30), z=(0, RAFT_H)))
    # the wall plate: dead straight, and CUT SQUARE at both tile planes. Its
    # chamfer is waisted over the bay centre and unevenly worn along its length
    # (see sweep_box) -- zero tris, and it stops the one long horizontal in the
    # piece reading as an extrusion.
    sweep_box(p, -G / 2, G / 2, -.06, .26, .30, RAFT_H, "oak_dark", n=6,
              bev=.014, stop=.55, wear=.32, seed=1)
    r = rng("beams/tails")
    for i in range(5):
        x = -.80 + .40 * i
        out = -.665 + r.uniform(-.03, .02)
        A = (.246, .47 + r.uniform(-.012, .012))         # buried in the plate
        C = (out, .325 + r.uniform(-.014, .014))         # nose, flattened
        top = _bez(A, (out * .50, .355), C, 6)
        d = .155
        nose = [(out + .05, C[1] - d * .5), (out * .93, C[1] - d)]
        poly = top + nose + _off(top[::-1], 0, -d)[1:]
        # WORKED: a stop-chamfer round both cheeks that dies where the tail is
        # buried in the wall plate and picks up again over the cut nose, which
        # is the one part of a rafter tail anybody ever sees. Cheaper than the
        # bevel it replaces, and unlike the bevel it leaves a hard arris.
        wprism(p, poly, .12, "oak_mid", axis='X', at=(x, 0, 0),
               cf=CHAM * .62, cb=CHAM * .62, tint=.065, seed=f"tail{i}",
               shade=1.02 + r.uniform(-.09, .05),
               cw=lambda u, v: clamp((.150 - u) / .060))
    # roof boarding laid over the inner half of the tails: what the shingle
    # course above lands on, and what stops the run reading as a ladder. Five
    # separate boards, so the deck bell-casts with the tails under it instead
    # of spanning the sweep as one flat plate.
    for i in range(4):
        x = -.75 + .50 * i
        # bevel 0: this deck is under the shingle course and over the tails,
        # so its arrises are buried on every side. Carving what cannot be seen
        # is the one thing a 1600-tri budget genuinely cannot afford, and the
        # 130 tris it frees pay for the chamfers on the five tails below it.
        p.beam((x, .252, .505), (x, -.40, .385), .492, .05, "oak_mid",
               bevel=0, tint=.05, shade=1.04 + r.uniform(-.05, .04))
    # the flat fascia plank the tails are nailed through -- SWEPT, not a box, so
    # it follows the bell-cast AND presents a flat cut at both tile planes.
    # Eased stations, like the sill run: the fascia IS the eave line, it tiles
    # every 2m, and evenly sampled it left the same crease at every station that
    # the bressummer used to.
    sweep_box(p, -G / 2, G / 2, -.665, -.610, .275, .460, "oak_dark", n=7,
              bev=.012, shade=.84, stop=.62, wear=.34, seed=2)
    # tooth course hung under the fascia, dropped between the tails
    p.dentil((-.80, .80), .220, -.625, "oak_dark", n=4, size=(.07, .105, .11),
             tint=.06, seed=7)
    _bend(p, EAVE_BOW, y_ramp=(-.06, -.665))
    p.wobble(.004)
    return p.finish()


# =============================================================================
# ============ 7. THE JETTY UNDERSIDE -- soffit, plate, dragon corner ==========
# =============================================================================
# Shanee, of the attempt to jetty the upper storey by sliding wall pieces out by
# a sub-grid amount: "I think the floor difference is jettison style
# construction where the upper floor is supported and expanded to a larger area
# than the ground floor. Not done by just moving the walls blindly. It should be
# entire tiles allowing to do it."
#
# They are right, and the reason it could not be done from whole tiles is that
# the kit had the FRONT of a jetty and none of its BODY. A jetty is not an
# offset wall: it is a floor that genuinely GAINS AREA, carried on cantilevered
# joists, and the underside of the gained area is real geometry. Slide the upper
# wall out by JETTY and you open a GRID x JETTY hole along the whole facade with
# nothing in it -- which is exactly why it had to be faked by nudging walls
# instead of by laying a module.
#
# The vernacular names the members, and each one is now a piece or a face here:
#     JETTY PLATE   on the head of the wall below; the joists bear on it
#                                                -> SM_Beam_JettyPlate_2m
#     JOISTS        cantilever out past that plate  -> in the soffit tile
#     BRESSUMER     closes the projecting joist ends, and THE UPPER WALL SITS
#                   ON IT                        -> SM_Beam_JettySill_2m_A/B/C,
#                                                   already built, NOT touched
#     JETTY BRACKET / SPUR   the angled support under the overhang
#                                                -> SM_Beam_CorbelScroll and
#                                                   SM_Beam_CorbelKnee already
#                                                   ARE this; see THE BRACKET
#     FASCIA        the finish across the underside's edge -> in the soffit tile
#     DRAGON BEAM   the diagonal at a corner, so TWO sides can jetty at once,
#                   carrying diagonally-set joists
#                                                -> SM_Beam_DragonBeam_Corner
#
# ---------------------------------------------------------------------------
# THE FRAME -- read this before placing any of the three.
# ---------------------------------------------------------------------------
# All three are stated in ONE frame, so an assembler places them from two facts
# and no arithmetic:
#
#     z = 0  is THE STOREY LINE: the floor of the storey that jetties, and the
#            plane SM_Beam_JettySill_2m's top face already lands on. Everything
#            here HANGS BELOW IT, so all of it is placed AT that line.
#     y = 0  is the outer face of the JETTIED (upper) wall, and
#     y = J  is the outer face of the wall BELOW it.
#
# So the soffit tile spans exactly the strip a jetty opens up; the bressumer --
# placed on the wall BELOW with its face J proud (SILL_FACE = -J) -- lands its
# face on y = 0 of this frame; and the two agree by construction rather than by
# a number typed twice.
#
#     wall below    on rect R           at z0
#     UPPER wall    on R grown by J     at z0 + H          <-- the jetty
#     soffit tiles  on R grown by J     at z0 + H          <-- same plane, same line
#     dragon corner on R grown by J     at z0 + H          <-- its corner square
#     jetty plate   on R                at z0 + H          <-- same line
#     bressumer     on R                at z0 + H - SILL_H <-- unchanged
#
# ---------------------------------------------------------------------------
# JETTYING OVER A **STONE** STOREY -- the one case where R is not one rectangle,
# stated here because an assembler will hit it on the very first inn.
# ---------------------------------------------------------------------------
# assemble_inn.py builds every block as TWO rectangles: `blk.st` (the stone
# faces) and `blk.tb = blk.st` inset by INSET = T_STONE - T_TIMBER = 0.12, which
# is where the timber storeys and the sill runs go. So when a TIMBER storey
# jetties over a TIMBER storey the offset is exactly JETTY and this tile's back
# edge lands on the wall below's face, as the table above says. When it jetties
# over the STONE ground floor the CLEAR overhang is JETTY - INSET = 0.33, not
# 0.45 -- assemble_inn.py says so in as many words -- and the tile's inner
# 120 mm is then inside the head of the stone wall.
#
# That is NOT a fault to design out, it is the JOIST BEARING: a cantilevered
# joist is built INTO the wall it cantilevers from, and 120 mm of a 0.44 m joist
# tail buried in a 0.36 m wall head is a short bearing, not a collision. It is
# opaque on every side, and it shares no plane with the wall (the wall head is
# z0 + H and this tile's top is JS_TOP = 6 mm under it). Two consequences worth
# knowing:
#   * lay the tile on the SAME plane either way -- the jettied wall's face --
#     and let the tail bed itself. Do not shorten it: a J-INSET tile would leave
#     a 120 mm open slot on every timber-over-timber jetty in the kit.
#   * check_collisions.py measures mutual bbox depth, so it will report that
#     120 mm. It is the bearing, and it is meant to be there.
# demo() places its ground storey on the stone plane for exactly this reason,
# so the render shows the overhang an assembler actually gets.
#
# ---------------------------------------------------------------------------
# HOW THE SOFFIT MEETS THE BRESSUMER, and why nothing here can z-fight with it.
# ---------------------------------------------------------------------------
# The bressumer's butting profile is FROZEN (see THE JETTY SILL PROFILE) and not
# one number of it is touched by any of this. In the frame above it occupies
#     y  0 .. SILL_DEPTH (0.34)      z  -SILL_H .. 0  (-0.48 .. 0)
# i.e. it fills the OUTER three quarters of the jetty's depth and hangs well
# below the joists -- which is what a bressumer IS: a deep downstand at the
# outer edge that closes the joist ends and carries the wall. So the soffit tile
#   * keeps its whole outer end INSIDE that solid and GAP clear of every one of
#     its faces -- nose at y = 0.008 against the bressumer's face at 0, fascia
#     top at -0.010 against its top at 0, fascia bottom at -0.280 against its
#     soffit at -0.425 -- buried in opaque timber, sharing no plane with it, so
#     the pair cannot flicker;
#   * and does its visible work over the inner quarter and from underneath,
#     which is the whole of what you see when you stand under a jetty.
# It also stands alone: with no bressumer over it (a gable-end overhang, the end
# of a run, the corner in demo()) the fascia and the moulded joist noses close
# it properly by themselves. That is why the fascia is a full-depth board rather
# than a lip -- it is the tile's own closure as well as its trim, and it means
# nothing can be seen through the tile from above either.
#
# THE JOISTS TILE, and they tile the way wall studs do: pitch G/5, with a joist
# at each fifth of the module and THE SEAM FALLING MID-BAY between two of them.
# A joist ON the seam would be cut in half and would have to present half a
# moulded nose on a butt plane; a bay on the seam is boarding, and boarding has
# joints in it anyway. The two half-bays at x = +-GRID/2 are built from ONE seed
# with no tone or thickness jitter, so tile N's right half and tile N+1's left
# half are the SAME board and a run reads continuous.
JS_TOP     = -GAP                 # -0.006, THE TILE'S TOP FACE. GAP under the
                                  # storey line ON PURPOSE: the wall above
                                  # starts ON that line and two opaque coplanar
                                  # faces z-fight. This is _sill_back's HOUSE_DZ
                                  # finding, applied before it can happen again.
# ---------------------------------------------------------------------------
# THE DECK -- and it is the other half of "the floor gains area".
# ---------------------------------------------------------------------------
# The tile carried joists and a boarded soffit and NOTHING ACROSS THE JOIST
# TOPS, so a module was an open tray. That is wrong twice over. It is wrong
# about the building -- the joists cantilever in order to carry a FLOOR, and
# that boarded floor IS the area the upper storey gains, which is the whole
# thing Shanee was describing -- and it is wrong about how the kit is looked at:
# every camera in this repo (lineup, closeup, tiled, demo, and CAM_REF2's
# elevated 3/4 hero) looks DOWN, so the one face of the tile they all see was
# the one face that had nothing on it, and a run of them read as a rack of
# timber laid on the bressumer instead of as a floor stepping out over the
# storey below.
#
# The deck is cut OUT OF the joist's depth, not added under it: JS_SOF is
# unchanged to the micron, so the fascia, the boarding, the jetty plate and
# every number the bressumer interface was checked against are untouched.
JS_DECK_T  = 0.032                # floorboard thickness
JS_JTOP    = JS_TOP - JS_DECK_T + GAP   # -0.032: the joists bed GAP INTO the
                                  # deck instead of landing on its underside,
                                  # so the two share no plane -- the rule the
                                  # whole family is built on
JS_JOIST_D = 0.212                # joist depth, square-set under that deck
JS_JOIST_W = 0.138                # ... and width. Square-set, not laid flat.
JS_SOF     = JS_JTOP - JS_JOIST_D # -0.244, the joist soffit: the plane the whole
                                  # underside is read off. UNCHANGED
JS_PITCH   = G / 5                # 0.40 -- five joists a module, seam mid-bay
JS_NOSE_Y  = 0.008                # the noses, just inside the bressumer's face
# ---------------------------------------------------------------------------
# ROUND 10 -- THE NOSES READ AS BLOBS, MEASURED OFF closeup.png / tiled.png.
# ---------------------------------------------------------------------------
# The claim under JS_FAS_Y was "ref1's rafter-tail idiom, where the tails poke
# out THROUGH the fascia plank instead of dying behind it", and the numbers did
# not deliver it. The fascia's outer face was 48mm off the bressumer plane and a
# nose starts at 8, so a joist end stood 40mm proud -- and the moulded chamfer
# round it was 34mm of that 40. A 34mm chamfer on a 40mm projection is not a
# moulding, it is a pyramid: the end had no flat left on it, so in Solid shading
# each nose shaded as one smooth rounded lozenge and a run of them read as
# studs glued to a plank instead of as the ends of five square-set timbers.
# Both renders show it: closeup.png at 16 degrees above horizontal, which is the
# view that frames this face, and tiled.png with fifteen of them in a row.
#
# So the fascia moves BACK (the only free direction: the nose cannot move
# forward, y = 0 is the bressumer's own face and a nose through it would stand
# in front of the beam that is supposed to close it) and the chamfer comes down
# to a crisp arris. 64mm of projection with a 18mm moulding leaves 46mm of flat
# square end grain catching the light, which is what a joist end is.
# Everything else is derived from these two, here and in the dragon corner, so
# the run's fascia and the corner's mitre still state one section.
JS_NOSE_CH = 0.018                # the moulded (chamfered) end -- the period
                                  # detail, and the only carving on a joist that
                                  # anyone ever sees. Was 0.034, i.e. 85% of the
                                  # projection it was cut on.
JS_FAS_Y   = 0.072                # the fascia's outer face. The noses stand
JS_FAS_T   = 0.052                # 64mm proud of it: ref1's rafter-tail idiom,
                                  # where the tails poke out THROUGH the fascia
                                  # plank instead of dying behind it. Was 0.048,
                                  # which left 40mm and no flat on the end.
                                  # Still well inside the bressumer's opaque
                                  # y 0..SILL_DEPTH, so nothing here can be seen
                                  # against it or flicker with it.
JS_FAS_Z0  = JS_SOF - 0.036       # -0.280, its lower arris: the shadow line
JS_FAS_Z1  = JS_TOP - 0.004       # ... and its top, which closes the bay ends
JS_FAS_BEV = 0.014                # PART OF THE SHARED SECTION: the run's fascia
                                  # and the corner's mitre are the same four
                                  # bands, so neither butt nor mitre steps
JS_BRD_T   = 0.036                # soffit boarding thickness
JS_BRD_Z   = JS_SOF + 0.062       # -0.182, its underside: RECESSED above the
                                  # joist soffit so the joists stand proud of it
                                  # and the underside reads as STRUCTURE in
                                  # Solid shading rather than as a lid. Flush
                                  # boarding reads as a box; 62 mm survives a
                                  # grazing view.
JS_BACK    = J - GAP              # 0.444 -- the tile stops GAP short of the wall
                                  # below, so no face of it lands on that wall's
                                  # outer face
JS_D       = 0.30                 # how far the tile hangs below the storey line
JS_TONE    = 1.00                 # one flat tone for the joists, as the sill run
                                  # has one: a shade jitter down a repeating
                                  # rhythm draws every module boundary


def _joist_sec(w=JS_JOIST_W, z0=JS_SOF, z1=JS_JTOP, cham=0.028):
    """A floor joist's section: square-set, with the two LOWER arrises chamfered
    and the two upper ones left square, because the upper two are buried under
    the floor. The chamfer is part of the solid, never a bmesh bevel -- see THE
    WORKED TIMBER -- which is why it can stop dead at the nose."""
    h = w / 2
    return [(-h, z1), (-h, z0 + cham), (-h + cham, z0),
            (h - cham, z0), (h, z0 + cham), (h, z1)]


def _joist(p, at_u, v0, v1, axis='Y', seed=0, nose=JS_NOSE_CH, shade=1.0,
           mat="oak_dark", tint=.05):
    """ONE cantilevered floor joist, running along `axis` from v0 (its NOSE) to
    v1 (housed in the wall). `at_u` is its station on the other horizontal axis.

    The moulded end is wprism's near-end chamfer: a ring inset round the whole
    section at the nose and nothing at the far end, which is buried and would be
    tris spent on nothing. 32 tris, chamfer and all."""
    L = v1 - v0
    at = ((at_u, (v0 + v1) / 2, 0.0) if axis == 'Y'
          else ((v0 + v1) / 2, at_u, 0.0))
    return wprism(p, _joist_sec(), L, mat, axis=axis, at=at,
                  cf=nose, cb=0.0, wear=WEAR * .55, seed=seed, tint=tint,
                  shade=shade)


def _soffit_bay(p, x0, x1, y0, y1, n=4, seed=0, flat=False, mat="oak_mid"):
    """The boarding that CLOSES one joist bay from below: boards running along X
    and banded across the depth of the jetty, so their joints cross the joists
    at right angles and the underside carries two rhythms instead of one.

    `flat` is for the two half-bays at x = +-GRID/2. Both are built from one
    seed with no tone or thickness jitter, so tile N's right half and tile N+1's
    left half are the SAME board: the joint between them is a board joint and
    not a step in tone."""
    r = rng(f"{p.name}/soffit/{seed}")
    out = []
    for i in range(n):
        va = lerp(y0, y1, i / n) + (0.0 if i == 0 else .004)
        vb = lerp(y0, y1, (i + 1) / n) - (0.0 if i == n - 1 else .004)
        t = JS_BRD_T if flat else JS_BRD_T * (1 + r.uniform(-.16, .10))
        sh = 1.0 if flat else 1.0 + r.uniform(-.055, .055)
        out += p.plate(((x0 + x1) / 2, (va + vb) / 2, JS_BRD_Z + t / 2),
                       (x1 - x0, vb - va, t), mat,
                       tint=.0 if flat else .05, shade=sh)
    return out


def _deck(p, x0, x1, y0, y1, n=4, seed=0, mat="oak_mid"):
    """THE FLOORBOARDS THE JETTY GAINS -- laid across the joists, and the top
    face of the module.

    Boards run along X, ACROSS the joists (which run out along Y), because that
    is how a floor is boarded and because it puts a joint line every ~110 mm
    across the one face of this tile that a camera above the jetty can see.
    Their TOPS are flush at JS_TOP -- a floor is levelled whatever the boards do
    underneath -- and only their thickness varies downward, so nothing here can
    foul the wall that stands on this plane.

    Cut dead flat on both tiling planes, and since every tile in a run is the
    SAME MESH, board i of tile N is board i of tile N+1: a run reads as a
    boarded floor with a joint every 2 m, which is what a boarded floor has.
    The joints are 9 mm of real gap rather than a change of tone, because
    Shanee inspects in SOLID shading, where tone is not drawn at all."""
    r = rng(f"{p.name}/deck/{seed}")
    out = []
    for i in range(n):
        va = lerp(y0, y1, i / n) + (0.0 if i == 0 else .0045)
        vb = lerp(y0, y1, (i + 1) / n) - (0.0 if i == n - 1 else .0045)
        t = JS_DECK_T * (1 + r.uniform(-.14, .10))
        out += p.plate(((x0 + x1) / 2, (va + vb) / 2, JS_TOP - t / 2),
                       (x1 - x0, vb - va, t), mat, tint=.05,
                       shade=.94 + r.uniform(-.05, .05))
    return out


def jetty_soffit():
    """SM_Beam_JettySoffit_2m -- ONE MODULE OF THE OVERHANG'S UNDERSIDE, and the
    piece the kit was missing. GRID wide, JETTY deep, hung below the storey line.

    Five square-set joists at G/5 centres cantilever the full depth of the
    jetty, each with a chamfered moulded nose standing proud of the fascia the
    way ref1's rafter tails stand proud of theirs. Between them the soffit is
    boarded, recessed 62 mm above the joist soffits so the joists read as
    structure from below. A full-depth fascia plank closes the outer end -- and
    closes the bay ends with it, so the tile is solid: nothing shows through it
    from above and nothing shows through it from the street.

    Tile a row of these along a wall at GRID and the whole overhang closes, the
    seam falling mid-bay between two joists and the joist rhythm running on
    unbroken across it. That is what lets a jetty be built out of whole modules
    instead of out of walls nudged outward."""
    p = Part("SM_Beam_JettySoffit_2m", budget="beam",
             seams=dict(x=(-G / 2, G / 2), y=(0.0, J), z=(-JS_D, 0.0)))
    xs = [-2 * JS_PITCH + JS_PITCH * i for i in range(5)]      # -.8 .. .8
    hw = JS_JOIST_W / 2
    r = rng("beams/jetty_soffit")
    # ---- the joists, cantilevering out to their moulded noses --------------
    for i, x in enumerate(xs):
        _joist(p, x, JS_NOSE_Y, JS_BACK, axis='Y', seed=f"j{i}",
               shade=JS_TONE + r.uniform(-.045, .045))
    # ---- the boarding, closing every bay from below ------------------------
    lefts = [-G / 2] + [x + hw for x in xs]
    rights = [x - hw for x in xs] + [G / 2]
    last = len(lefts) - 1
    for i, (a, b) in enumerate(zip(lefts, rights)):
        seam = i in (0, last)
        # laps GAP into the joist beside it instead of butting onto its face,
        # and is cut DEAD FLAT where it meets a tiling seam
        _soffit_bay(p, a - (0.0 if i == 0 else GAP),
                    b + (0.0 if i == last else GAP),
                    JS_FAS_Y + JS_FAS_T - GAP, JS_BACK,
                    seed="edge" if seam else i, flat=seam)
    # ---- the fascia: a RUN member, cut dead flat on both tiling planes ------
    # sweep_box, not a box: bmesh.ops.bevel chamfers the END faces too, so a row
    # of bevelled fascias shows a 2*bev groove at every 2 m -- and this is the
    # one long line the underside of a jetty is read along.
    sweep_box(p, -G / 2, G / 2, JS_FAS_Y, JS_FAS_Y + JS_FAS_T,
              JS_FAS_Z0, JS_FAS_Z1, "oak_dark", n=6, bev=JS_FAS_BEV,
              stop=.45, wear=.30, shade=.90, seed=21)
    # ---- and the deck those joists exist to carry, closing the module ------
    _deck(p, -G / 2, G / 2, 0.0, JS_BACK, n=4, seed=1)
    p.wobble(.0038, freq=1.35)
    return p.finish()


# ---------------------------------------------------------------------------
# THE JETTY PLATE
# ---------------------------------------------------------------------------
JP_TOP  = JS_SOF + GAP            # -0.238: the joists bed GAP into it, so they
                                  # MEET it instead of landing on its plane
JP_D    = 0.126
JP_BOT  = JP_TOP - JP_D
JP_OUT  = 0.095                   # how far it stands proud of the wall face
JP_TAIL = 0.042                   # ... and how far it is housed into it. Both
                                  # numbers keep it strictly INSIDE the volume
                                  # SM_Beam_JettySill's own housing occupies
                                  # (y -0.116..0.050, z -0.425..-0.008), so
                                  # wherever a bressumer is used the plate is
                                  # buried in opaque timber and not one face of
                                  # the two is coplanar with the other.
JP_SEAM = 0.42


def jetty_plate():
    """SM_Beam_JettyPlate_2m -- the plate on the head of the wall below, which
    the cantilevered joists bear on. Modest by design: in an elevation it is a
    shadow line under the joists and nothing more, so it is a chamfered run
    timber, a drip bead along its lower outer arris to draw that line, and one
    oak trenail per joist station pegging the joists down to it.

    Placed on the wall BELOW (y = 0 is that wall's outer face) at the storey
    line, so it and the soffit tile share one z and the joists land on it by
    construction. Cut dead flat at both tiling planes, like every run piece in
    the family."""
    p = Part("SM_Beam_JettyPlate_2m", budget="beam",
             seams=dict(x=(-G / 2, G / 2), y=(-JP_OUT, JP_TAIL),
                        z=(-JP_SEAM, 0.0)))
    sweep_box(p, -G / 2, G / 2, -JP_OUT, JP_TAIL, JP_BOT, JP_TOP, "oak_dark",
              n=6, bev=.016, stop=.50, wear=.32, shade=.94, seed=22)
    # the drip bead: THE shadow line. It laps GAP up INTO the plate instead of
    # sitting on its soffit, so the pair never share a plane.
    sweep_box(p, -G / 2, G / 2, -JP_OUT + .012, -JP_OUT + .058,
              JP_BOT - .028, JP_BOT + GAP, "oak_mid", n=5, bev=.009,
              wear=.26, shade=.86, seed=23)
    _pegs(p, [-2 * JS_PITCH + JS_PITCH * i for i in range(5)], -JP_OUT,
          (JP_TOP + JP_BOT) / 2, r_=.022)
    p.wobble(.0035, freq=1.2)
    return p.finish()


# ---------------------------------------------------------------------------
# THE DRAGON CORNER
# ---------------------------------------------------------------------------
# A jetty on ONE side is a run of soffit tiles. A jetty on TWO sides has a
# problem no run piece can solve: at the corner the joists of both sides want
# the same square, and neither wall is under it. The vernacular answer is the
# DRAGON BEAM -- one heavy timber laid on the diagonal from the corner post of
# the storey below out to the corner of the jetty, carrying the shortening,
# diagonally-framed joists of both runs. That is this piece, and it is the only
# reason two jettied runs can meet at all.
#
# It is a CORNER piece and obeys the corner convention: it fills the JETTY x
# JETTY square left where two soffit runs meet, x in [-J, 0] and y in [0, J],
# and it faces out on TWO sides, so outward="xy". Its INNER corner (0, J) is the
# outside corner of the storey below -- where the dragon beam is housed into the
# corner post -- and its OUTER corner (-J, 0) is the outside corner of the
# jettied storey above. The two runs arrive on x = 0 and on y = J and meet the
# same fascia section there, and the fascia turns the outside corner AS ONE
# MITRED SOLID: two lapped boxes would butt face to face straight across the
# arris and draw a line down the middle of the corner, which is the exact fault
# that had to be fixed on SM_Corner_JettyJoint in round 8. It is not repeated.
JD_D     = 0.42                   # the corner hangs further than a run tile: the
                                  # dragon beam is the deeper member, as the
                                  # principal timber of a floor is, and it
                                  # carries a PENDANT at its nose (see _pendant)
JD_W     = 0.170                  # the dragon beam's width
JD_DEEP  = 0.030                  # ... and how much deeper than a common joist
JD_HALF  = JD_W / 2 * 1.4142136   # its half width measured along X or Y, since
                                  # it lies at 45 degrees
JD_EDGE  = J - JD_HALF            # 0.3298: where its near edge crosses x = 0,
                                  # and where its square inner cut ends
JD_LAP   = 0.020                  # how far the boarding runs under it
JD_DROP  = -0.400                 # the lowest point of the pendant. It stops
                                  # ABOVE the bressumer's soffit in this frame
                                  # (SILL_SOF - SILL_H = -0.425), so wherever a
                                  # bressumer or SM_Corner_JettyJoint closes the
                                  # corner the drop can never foul it, and it is
                                  # still 126mm clear below the dragon beam's own
                                  # soffit -- enough to be a silhouette.


def _dragon_rails(a, b, w0, w1, n=5, stop=0.075, ret=0.070):
    """Plan rails for the DRAGON BEAM, so it can be swept like every other
    worked member in this family instead of bevelled like a bar of soap.

    It was `p.beam(..., bevel=.018)`, i.e. a box with a uniform bmesh bevel on
    all twelve arrises -- the exact treatment THE WORKED TIMBER exists to end,
    and doubly wrong here because bmesh.ops.bevel chamfers the two END faces
    too: the beam's nose is tenoned into the mitred fascia and its inner end
    butts the corner housing, and a chamfer on either is a groove at a joint.
    Swept from rails the chamfer is part of the plan, so it can STOP short of
    both ends (the joints, where a carpenter squares the arris back up) and the
    two cuts stay dead flat.

    Returns (front, back) in sweep()'s form: ((x, y), inward_direction, k).
    `w0`/`w1` taper the section from the housed inner end to the nose.
    """
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = sqrt(dx * dx + dy * dy) or 1.0
    ux, uy = dx / L, dy / L
    px, py = -uy, ux                       # unit perpendicular, in plan
    front, back = [], []
    for i in range(n + 1):
        t = i / n
        cx, cy = lerp(a[0], b[0], t), lerp(a[1], b[1], t)
        hw = lerp(w0, w1, t) / 2
        k = clamp((min(t, 1 - t) * L - stop) / ret)     # the stop-chamfer
        front.append(((cx + px * hw, cy + py * hw), (-px, -py), k))
        back.append(((cx - px * hw, cy - py * hw), (px, py), k))
    return front, back


def _pendant(p, at, z_bot=JD_DROP, z_top=-0.248, mat="oak_mid", sides=8,
             shade=1.06):
    """THE PENDANT (pendill) hung under the dragon beam's nose.

    What was here was `p.cyl(r=.052, r_top=.082, h=.062)`: a 62mm truncated cone
    -- a doorknob. The drop at the outside corner of a jetty is the one piece of
    ornament the whole construction gets, it is what the eye lands on from the
    street, and every reference that has a dragon corner has one: a turned or
    carved drop hanging off the beam's end, bellied, waisted, and finished in a
    point. It is also the cheapest silhouette in this family -- a corner that
    ends in a flat mitre reads as a shelf, and a corner that ends in a drop
    reads as a building.

    Turned as a lathe of eight sides, so in SOLID shading the belly breaks into
    eight flats with hard arrises between them rather than smooth-shading into a
    blob. Its head is buried inside the beam and the fascia mitre it hangs from,
    which is where a pendant's tenon goes, and no ring of it lands on either of
    their planes."""
    d = z_top - z_bot
    # (height as a fraction of the drop, radius). The beam's soffit sits at
    # 0.83 of it and the fascia's lower arris at 0.79, so everything below the
    # collar hangs in clear air and is what actually draws the silhouette.
    prof = [(0.00, .008), (0.09, .040), (0.16, .048), (0.25, .026),
            (0.34, .052), (0.46, .072), (0.62, .060), (0.72, .032),
            (0.80, .058), (1.00, .058)]
    return p.lathe([(r, z_bot + h * d) for (h, r) in prof], mat,
                   at=(at[0], at[1], 0.0), sides=sides, tint=.05, shade=shade)


def _dragon_boards(p, mirror, seed):
    """The boarding of ONE of the two triangles the dragon beam divides the
    corner into. Boards run parallel to their own wall and are cut on the
    diagonal, lapping JD_LAP under the beam -- which is how a dragon-beam corner
    is really boarded, and why the underside of the corner reads as two fans
    meeting on a diagonal instead of as a lid.

    `mirror` reflects the whole triangle across the beam's own centreline,
    (x, y) -> (y - J, x + J), so the two sides are one construction stated twice
    and cannot drift apart. Because the second side is the exact mirror of the
    first and both stop JD_LAP inside the beam, no board of one side can ever
    overlap a board of the other."""
    y0, y1, n = JS_FAS_Y + JS_FAS_T - GAP, JS_BACK, 4
    r = rng(f"beams/dragon/{seed}")
    out = []
    for i in range(n):
        va = lerp(y0, y1, i / n) + .004
        vb = lerp(y0, y1, (i + 1) / n) - .004
        # the beam's near edge is x = y - JD_EDGE; clamp so the last band, which
        # is all beam, still leaves a sliver rather than an inverted quad
        xa = min(-.008, max(va - JD_EDGE - JD_LAP, -J + .10))
        xb = min(-.008, max(vb - JD_EDGE - JD_LAP, -J + .10))
        quad = [(xa, va), (0.0, va), (0.0, vb), (xb, vb)]
        if mirror:
            quad = [(v - J, u + J) for (u, v) in quad]
        out += p.prism(quad, JS_BRD_T, "oak_mid", axis='Z',
                       at=(0, 0, JS_BRD_Z + JS_BRD_T / 2), bevel=0, tint=.05,
                       shade=1.0 + r.uniform(-.05, .05))
    return out


def dragon_corner():
    """SM_Beam_DragonBeam_Corner -- the corner module of the jetty underside:
    the diagonal DRAGON BEAM, the short diagonally-set joists it carries on both
    sides, the boarding between them, the fascia turning the outside corner as
    one mitred solid, and a turned PENDANT hung under the beam's nose where a
    dragon post would take it -- the one piece of ornament the construction
    gets, and the thing that stops the corner reading as a shelf.

    Fills the JETTY x JETTY corner square (corner convention, outward="xy"), so
    two jettied runs meet with zero gap and zero overlap by construction."""
    p = Part("SM_Beam_DragonBeam_Corner", budget="beam",
             seams=dict(x=(-J, 0.0), y=(0.0, J), z=(-JD_D, 0.0)), outward="xy")
    zb = JS_SOF - JD_DEEP                        # the dragon beam's soffit
    zc = (JS_JTOP + zb) / 2
    # ---- the dragon beam, on the diagonal ---------------------------------
    # Its inner end is set back half its own width along the diagonal so that
    # its SQUARE CUT END lands exactly on the cell's inner corner (0, J) -- the
    # corner post of the storey below -- instead of throwing two section corners
    # past two snap planes at once. Its nose dies INSIDE the mitred fascia,
    # tenoned into it, which is where a dragon beam's outer end goes.
    # It is SWEPT, not bevelled: its chamfer is part of its plan, so it stops
    # short of both cut ends the way a carpenter's does and neither the tenon in
    # the fascia nor the butt against the housing carries a chamfered groove
    # across it. See _dragon_rails.
    A = (-JD_HALF / 2, J - JD_HALF / 2)
    B = (-J + .090, .090)
    # Its top rides GAP ABOVE the common joists' top, i.e. that much further up
    # into the deck: a dragon beam is the principal timber of the floor, so it
    # is the deeper member on both faces. That is also the rule the family runs
    # on -- two solids overlap rather than share a plane. Flush at JS_JTOP the
    # beam's top and the two joists' tops were one plane, 80 cm2 of it, measured
    # by check_zfight.py the first time this was swept (p.beam's bevel had been
    # hiding it by rounding the arris away).
    fr, bk = _dragon_rails(A, B, JD_W, JD_W * .86)
    zt = JS_JTOP + GAP
    sweep(p, fr, bk,
          [(zb, CHAM), (zb + CHAM, 0.0), (zt - CHAM * .5, 0.0),
           (zt, CHAM * .5)], "oak_dark", shade=.90)
    # ... and the housing that squares its inner end into the corner. Without it
    # the perpendicular cut leaves an open triangle at the one point of the
    # corner where neither side's boarding can reach. Its hypotenuse is set
    # 14 mm INTO the beam so the two do not share the cut plane.
    p.prism([(0.0, J), (-.014, JD_EDGE - .014), (-JD_HALF - .014, J - .014)],
            JS_JTOP - zb, "oak_dark", axis='Z', at=(0, 0, (JS_JTOP + zb) / 2),
            bevel=0, tint=.04, shade=.86)
    # ---- the two diagonally-set joists, one per run, ON THE RUN'S OWN PITCH:
    # a run's joists stand at x = .2, .6, 1.0 ... so the corner's is at -.2 and
    # the flank's at y = J - .2. The rhythm walks straight through the corner
    # instead of restarting at it.
    _joist(p, -JS_PITCH / 2, JS_NOSE_Y, -JS_PITCH / 2 + J - JD_HALF + .050,
           axis='Y', seed="dfront", shade=JS_TONE)
    _joist(p, J - JS_PITCH / 2, -J + JS_NOSE_Y,
           -JS_PITCH / 2 - JD_HALF + .050, axis='X', seed="dside",
           shade=JS_TONE)
    # ---- boarding, both triangles ------------------------------------------
    _dragon_boards(p, False, "front")
    _dragon_boards(p, True, "side")
    # ---- the fascia, TURNING THE CORNER AS ONE MITRED SOLID ----------------
    # Same four bands sweep_box builds for the run, so the section a run
    # presents on x = 0 and on y = J is the section this piece presents back.
    fy, by = JS_FAS_Y, JS_FAS_Y + JS_FAS_T
    front = [((0.0, fy), (0.0, 1.0), 1.0),
             ((-J + fy, fy), (1.0, 1.0), 1.0),
             ((-J + fy, J), (1.0, 0.0), 1.0)]
    back = [((0.0, by), (0.0, -1.0), 1.0),
            ((-J + by, by), (-1.0, -1.0), 1.0),
            ((-J + by, J), (-1.0, 0.0), 1.0)]
    sweep(p, front, back,
          [(JS_FAS_Z0, JS_FAS_BEV), (JS_FAS_Z0 + JS_FAS_BEV, 0.0),
           (JS_FAS_Z1 - JS_FAS_BEV, 0.0), (JS_FAS_Z1, JS_FAS_BEV)],
          "oak_dark", shade=.90)
    # ---- THE PENDANT, hung off the beam's nose through the mitre -----------
    # Centred 31 mm inboard of the beam's nose ON the diagonal, so its tenon is
    # inside solid timber on every side and the drop itself comes down clear of
    # both fascia legs. This is the corner's whole silhouette; see _pendant.
    _pendant(p, (-J + .112, .112))
    # ---- the deck, carried over the corner on the same four board lines the
    # run carries it on, so the floor walks through the corner unbroken -------
    _deck(p, -J, 0.0, 0.0, J, n=4, seed=2)
    _pegs(p, (-.30,), fy, zc + .030, r_=.022, axis='Y')
    _pegs(p, (J - .30,), -J + fy, zc + .030, r_=.022, axis='X')
    p.wobble(.0034, freq=1.4, axes="xyz")
    return p.finish()


# ---------------------------------------------------------------------------
# THE BRACKET -- checked first, and deliberately NOT duplicated.
# ---------------------------------------------------------------------------
# A jetty bracket (jetty spur) is the angled member under the overhang, running
# from the wall face below out to the underside of the bressumer. The family
# already has two, and they already are exactly that:
#
#   SM_Beam_CorbelScroll   moulded pad, hollow throat, curled volute nose
#   SM_Beam_CorbelKnee     slim curved knee -- the scythe silhouette off ref1's
#                          right-hand jetty
#
# Both stand CORBEL_H tall and reach to y = -(J - 0.02), i.e. from the wall face
# below out to the bressumer's own face, and both are placed at
# storey_top - SILL_H - CORBEL_H so their heads meet the bressumer's soffit --
# which is a jetty bracket in position, span, height and job. demo() uses them
# as one. A third piece of the same span under the same beam would be
# duplication, so there is none. Nor does any of this disturb them: the soffit
# tile's lowest face is -0.280 where a bracket's head is at -0.480, with the
# bressumer filling everything in between.


# ------------------------------------------------------------------ build ----
def _stand(ob):
    """Stand a piece that HANGS BELOW ITS ORIGIN on the studio floor, without
    touching one vertex of it.

    The three jetty-underside pieces are placed AT the storey line and hang
    below it -- the tile's top face is z = 0 so the storey sits ON it, which is
    the convention that lets an assembler lay a jetty from two facts (see THE
    FRAME). Every render build_piece.py makes puts a ground plane at z = -0.02
    under the family, so all three were rendering as a 14 mm sliver of joist
    top: three of the family's twelve pieces -- and the three NEW ones --
    could not be seen at all in lineup.png, and closeup.png and tiled.png, which
    both frame objs[0], were pictures of a ground plane with a comb of teeth
    lying on it. Measured before this: the soffit tile spans z -0.280..-0.006,
    the plate -0.392..-0.237 and the dragon corner -0.400..-0.006 (its pendant
    is its lowest point, so a lineup stands it on that drop -- which is honest,
    it is what the piece hangs on), against a floor at -0.020.

    ONLY THE OBJECT'S Z IS SET. The mesh still carries the canonical kit origin,
    so zeroing the object snaps the piece back to its convention position --
    which is exactly the arrangement build_kit.py documents for the whole kit
    ("Each piece's MESH still carries the canonical kit origin, so zeroing an
    object's location snaps it to its convention position"), what
    assemble_inn.put() does to every piece it places, and what demo() below
    does. Nothing that consumes this family reads the home location."""
    ob.location.z = -min(v.co.z for v in ob.data.vertices)
    return ob


def build():
    # SM_Beam_JettySoffit_2m goes FIRST on purpose: build_piece.py's tiled.png
    # tiles objs[0], and the tiling proof is what this piece most needs -- it is
    # the new run piece, and a jetty is only assemblable from whole modules if a
    # row of them closes with no step and no crease in the joist rhythm. The
    # sill run's own tiling proof is demo(), which lays five of them plus the
    # corner end to end.
    return [_stand(jetty_soffit()), _stand(jetty_plate()),
            _stand(dragon_corner()),
            sill_a(), sill_b(), sill_c(), corbel_scroll(), corbel_knee(),
            porch_post(), lintel_door(), tie_beam(), rafter_tails()]


# ===========================================================================
# ===================== DEMO CONTEXT -- not kit pieces ======================
# ===========================================================================
# A jetty is not an object, it is a RELATIONSHIP BETWEEN TWO STOREYS: the upper
# one is bigger than the one under it. With neither storey in the picture, a run
# of soffit tiles on a bressummer reads as a rack of timber on a beam, which is
# exactly how demo.png used to read -- and the one thing this whole round exists
# to answer is Shanee's "the upper floor is supported and expanded to a larger
# area than the ground floor". So demo() puts the two storeys in, as CONTEXT.
#
# These are NOT kit pieces and cannot be mistaken for one: no SM_ prefix, no
# budget, no seams, built only inside demo(). stone_walls and timber_walls own
# the real versions, and this module does not touch either. It is the same
# device dormers.py (_ctx_roof / _ctx_base) and roofs.py (_ctx_walls) already
# use for the same reason.
def _rest(o, floor=0.0):
    """DEMO ONLY: drop a rotated object until its lowest vertex sits on `floor`.

    demo() stands two pieces against the wall at an angle, and the height that
    puts them ON the ground rather than through it or above it is a function of
    the rotation -- so it is measured, not typed. Same device as _stand(), and
    like _stand() it touches nothing but the object's Z."""
    m = o.rotation_euler.to_matrix()
    o.location.z = floor - min((m @ v.co).z for v in o.data.vertices)
    return o


def _ctx_stone(name, x0, x1, h=S.H_GROUND, h_face=None, t=S.T_STONE, door=None,
               seed=1, depth=.075, coping=0.120):
    """DEMO CONTEXT: the ground-floor wall the jetty projects over. Wall
    convention -- face on y = 0, body to +Y -- so it can be dropped in rotated.

    `h_face` stops the RUBBLE short of the wall head and leaves the top of the
    backing flat: the last 420 mm of the wall is behind the jetty plate and the
    joists, and stones bulging `depth` proud up there would poke through the
    underside of the overhang. `door` = (x0, x1, head_z) leaves a doorway for
    the porch and the lintel to stand in.

    `coping` -- ROUND 10, and the fault was in the RENDER, plainly. Everything
    above h_face used to be BARE BACKING: the `stone_dark` core ran the full
    height, so the last 420 mm of the wall was one flat grey slab and its TOP
    FACE sat 6 mm above the jetty's own deck. Behind the front run that is
    invisible (the bressummer covers it), but demo() deliberately leaves the
    flank corner unskinned so the joists can be read, and there it rendered as a
    raw grey plate laid over the masonry, standing proud of the floor it was
    supposed to carry. It read as an unfinished mesh, and it was the loudest
    thing in the corner of demo.png. Three changes, all measured:
      * the core now STOPS at hf + 0.165 -- 5 mm under the soffit of the joists
        that bed into this head -- so nothing of it can appear above the deck;
      * the band of wall FACE between the rubble and the overhang, which the
        core used to show bare, is a dressed upper course;
      * and the head is a coursed levelling band laid `coping` back from the
        face. 0.120 clears the jetty plate (0.095 proud, 0.042 housed) AND the
        joist bearing, which beds JETTY - INSET = 0.114 into this head (see
        JETTYING OVER A STONE STOREY in THE FRAME). So the coping meets the
        overhang instead of standing on top of it."""
    p = Part(name)
    hf = (h - .42) if h_face is None else h_face
    top = min(h, hf + .165) if coping else h
    p.plate(((x0 + x1) / 2, t / 2, top / 2), (x1 - x0, t, top), "stone_dark",
            tint=.03)
    spans = ([(x0, x1, 0.0)] if not door else
             [(x0, door[0], 0.0), (door[1], x1, 0.0), (door[0], door[1], door[2])])
    for i, (a, b, z0) in enumerate(spans):
        if b - a < .12 or hf - z0 < .12:
            continue
        p.stones((a, b), (z0, hf), y=0.0, depth=depth, mat="stone",
                 mat_alt="stone_pale", mat_warm="stone_warm", course=.36,
                 seed=seed * 10 + i, wobble=.26, mortar=.022, r_bevel=.045,
                 big=.22)
    if coping and h - hf > .06:
        r = rng(f"{name}/coping")
        # 1. THE UPPER COURSE on the wall FACE, from the top of the rubble up to
        #    the soffit of the overhang. Squared blocks, barely proud, because
        #    everything above this line is behind a jetty plate or a bressummer
        #    and a bulging rubble stone up here pokes through the underside.
        n = max(1, int(round((x1 - x0) / .44)))
        for i in range(n):
            a = lerp(x0, x1, i / n) + .010
            b = lerp(x0, x1, (i + 1) / n) - .010
            p.box(((a + b) / 2, .052, (hf + top) / 2 - .004),
                  (b - a, .128, top - hf + .008),
                  "stone_pale" if r.random() < .5 else "stone", bevel=.014,
                  seg=1, tint=.06, shade=.98 + r.uniform(-.07, .07))
        # 2. THE HEAD, as a coursed levelling band. It laps 45 mm down into the
        #    core rather than landing on its top face, and stands 4 mm above the
        #    storey line, so no horizontal face of it meets a face of anything.
        n = max(1, int(round((x1 - x0) / .38)))
        for i in range(n):
            a = lerp(x0, x1, i / n) + .011
            b = lerp(x0, x1, (i + 1) / n) - .011
            d = coping + r.uniform(0, .038)          # the front edge wanders
            z0 = top - .045
            p.box(((a + b) / 2, (d + t) / 2, (z0 + h + .004) / 2),
                  (b - a, t - d, h + .004 - z0),
                  "stone_pale" if r.random() < .55 else "stone", bevel=.018,
                  seg=1, tint=.06, shade=.94 + r.uniform(-.07, .07))
    return p.finish()


def _ctx_sole(name, x0, x1, t=S.T_TIMBER, h=0.150, seed=1):
    """DEMO CONTEXT: the SOLE PLATE of the storey above, with its studs started,
    laid on the jetty deck along the flank.

    A jetty deck with nothing standing on it reads as a balcony -- which is
    exactly how the unskinned flank corner of demo.png read, and it is the
    opposite of the point. One plate and a row of stub studs turns it into a
    floor with its wall begun on it, i.e. into the thing the overhang exists to
    carry, while still leaving the joists, the plate and the dragon beam under
    it in plain sight. Same 0.055 face offset as _ctx_upper, so the wall that
    finishes on the front and the wall that is starting on the flank stand on
    the same plane."""
    p = Part(name)
    r = rng(name)
    p.box(((x0 + x1) / 2, .055 + t / 2, h / 2), (x1 - x0, t * .88, h),
          "oak_dark", bevel=.016, seg=1, tint=.05)
    n = max(1, int(round((x1 - x0) / .62)))
    for i in range(n + 1):
        cx = lerp(x0 + .13, x1 - .13, i / max(1, n))
        p.box((cx, .055 + t / 2, h + .105), (.13, t * .58, .21), "oak_dark",
              bevel=.012, seg=1, tint=.05, shade=.96 + r.uniform(-.05, .05))
    return p.finish()


def _ctx_upper(name, x0, x1, h=1.30, t=S.T_TIMBER):
    """DEMO CONTEXT: the JETTIED storey, standing on the bressummer with its
    face flush to it -- i.e. JETTY proud of the stone below. That offset is the
    whole subject of the render; everything else here just holds it up."""
    p = Part(name)
    p.plate(((x0 + x1) / 2, .055 + t / 2, h / 2), (x1 - x0, t, h), "plaster",
            tint=.04)
    for z, d in ((.085, .17), (h - .105, .21)):        # sill rail, head rail
        p.box(((x0 + x1) / 2, .06, z), (x1 - x0, .12, d), "oak_dark",
              bevel=.014, seg=1, tint=.05)
    n = max(1, int(round((x1 - x0) / .62)))
    for i in range(n + 1):
        cx = lerp(x0 + .10, x1 - .10, i / max(1, n))
        p.box((cx, .06, h / 2), (.13, .12, h - .30), "oak_dark", bevel=.012,
              seg=1, tint=.05)
    return p.finish()


# ------------------------------------------------------------------- demo ----
def demo():
    """THE INTERFACE PROOF, and the thing to look at first.

    A jetty run built the way a level artist snaps one: SM_Corner_JettyJoint,
    then A, B, C, A in a straight line at exactly GRID spacing. All five present
    THE JETTY SILL PROFILE at every joint, so they have to read as ONE timber --
    no step and no crease in the silhouette at x = 0, 2, 4, 6, and none where
    the corner takes over. The repeat A at the far end is there on purpose: a
    variant has to line up with ITSELF two bays later as well as with its
    neighbours. A sixth sill on the corner's return leg shows the same section
    arriving from the other direction.

    Under it, brackets of both kinds: a scroll under each BAY CENTRE, where the
    swag brings the soffit down onto it, and a knee at each SEAM STATION packed
    up by SILL_BOW to meet the soffit where it has risen -- so the run reads as
    a beam bowing between its brackets, the way ref1's bressummer does. Then a
    pair of porch posts standing under the first bay (POST_H == H_GROUND -
    SILL_H, so a post takes the run directly at a bay centre) and the door
    lintel set in the wall below, ref1's arrangement at the front door.

    The girding beam, the eave and the porch's own bay used to stand out here as
    well, 3 m off the end of the run and 1.4 m above it. They framed the shot
    2.5x wider and 3x taller than the thing it exists to show, so the joints
    Shanee is pointing at rendered 40 pixels tall. They are in lineup.png, at
    full size, which is where a catalogue of the family belongs.

    AND THEN THE JETTY ITSELF, which is what this render is now mostly about:
    the ground floor in stone, the upper storey standing 0.33 m proud of it on
    the bressummer (JETTY less the 0.12 the stone storey itself stands out --
    see JETTYING OVER A STONE STOREY, and assemble_inn.py's own note), and
    between them the underside that makes that possible: the jetty plate on the
    wall head, a row of soffit tiles carrying the projecting joists and the
    boarded floor over them, brackets under, and the dragon corner turning the
    whole thing on to the flank.

    ROUND 10 -- THE CORNER NOW CARRIES SOMETHING. The upper wall used to stop
    dead at x = 8, so the dragon corner and the flank tile held nothing up and
    the whole turn read as a shelf -- which is the opposite of the one thing a
    dragon beam is for. The front wall runs across the corner module now and the
    flank's own wall is BEGUN on the flank tile (a sole plate and stub studs, in
    context), so the render says what the piece is for: two sides jettying at
    once, the storey above standing on the corner, and the joists still visible
    under it. The spare tile and spare corner that show the soffit are STOOD
    AGAINST THE WALL rather than laid flat, because every camera in this repo
    looks down and a soffit laid face-up is the one thing a downward camera
    cannot see. Read it against the run: the joints are still the other half of
    the job."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []

    def put(nm, loc, rz=0.0, rx=0.0):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (radians(rx), 0, radians(rz))
        out.append(o)
        return o

    SILL_Z = S.H_GROUND - SILL_H          # 2.52  top of the ground storey
    # A bracket's head lands on the soffit, so its z comes off the profile, not
    # off a typed-in number: at a BAY CENTRE the soffit is at SILL_SOF - SILL_BOW
    # (== 0, the piece's own floor) and at a SEAM STATION it is at SILL_SOF.
    CORB_Z = SILL_Z + (SILL_SOF - SILL_BOW) - CORBEL_H     # 1.92, bay centre
    CORB_S = SILL_Z + SILL_SOF - CORBEL_H                  # ... and at a seam

    # --- the run: corner joint, then A, B, C, A in a line at GRID spacing ----
    # The corner cell is T wide and sits in x [-T, 0], so the run starts at
    # x = 0 and the corner is placed one JETTY_BAND (0.80) below the storey
    # line, exactly as assemble_inn.py places it.
    for nm, x in (("SM_Beam_JettySill_2m_A", 1.0),
                  ("SM_Beam_JettySill_2m_B", 3.0),
                  ("SM_Beam_JettySill_2m_C", 5.0),
                  ("SM_Beam_JettySill_2m_A", 7.0)):
        put(nm, (x, 0, SILL_Z))
    corner = _demo_jetty_corner()
    corner.location = (0, 0, S.H_GROUND - 0.80)
    out.append(corner)
    # ... and the same section arriving along the corner's OTHER face: the
    # return wall's outer plane is x = -SILL_CELL, so this bay faces -X
    # (rz = -90) and its near end lands on the corner's y = SILL_JOINT_Y plane.
    # These two numbers are exactly how assemble_inn.py lays the return run out
    # (corner at blk.tb's corner + T_TIMBER, sills on blk.tb, 2m centres from
    # blk.st + T_STONE), which is the placement the old T_STONE corner cell
    # missed by 120mm.
    put("SM_Beam_JettySill_2m_A", (-SILL_CELL, 1.0 + SILL_CELL, SILL_Z), rz=-90)

    # --- brackets carrying the overhang, both kinds alternating --------------
    for x in (1.0, 3.0, 5.0, 7.0):
        put("SM_Beam_CorbelScroll", (x, 0, CORB_Z))
    for x in (2.0, 4.0, 6.0):
        put("SM_Beam_CorbelKnee", (x, 0, CORB_S))
    put("SM_Beam_CorbelKnee", (-SILL_CELL, 1.0 + SILL_CELL, CORB_Z), rz=-90)

    # --- two porch posts UNDER the first bay, carrying the run where its swag
    #     comes down to meet them, and the door lintel in the wall below. Both
    #     sit inside the run's own footprint, so they cost the framing nothing.
    for sx in (-1, 1):
        put("SM_Beam_PorchPost", (1.0 + sx * .70, -.25, 0))
    put("SM_Beam_LintelDoor", (1.0, -.25, 1.40))    # ... spanning the two posts

    # ---- THE JETTY ITSELF: the underside the run has been missing ----------
    # Everything below is placed at ONE line (the storey line, z = H_GROUND) and
    # on ONE of two planes -- the jettied wall's, y = -J, or the wall below's,
    # y = 0. That is the whole placement contract of THE FRAME above, and it is
    # what an assembler will do: soffit tiles on the jettied plane, the plate on
    # the plane below, the bressumer where it already goes.
    JZ = S.H_GROUND                      # the storey line the jetty carries
    # ROUND 10 -- THE GROUND STOREY STANDS `SO` PROUD, and it always did in the
    # real building. assemble_inn.py: "tb already sits INSET 0.12 behind the
    # stone face, so a 0.45 offset leaves the upper floors standing 0.33 m PROUD
    # of the ground floor". This demo had the stone flush with the timber cell
    # instead, and it showed: SM_Corner_JettyJoint's pale stone corbels are
    # measured off the STONE plane (corners.py, `so = TS - TT`), so with the
    # stone 120 mm too far back they hung in mid-air -- one of them is the white
    # block floating off the left end of the old demo.png. Everything on the
    # storey BELOW is placed on this plane now, so the corbels break out of real
    # masonry and the render shows the overhang the assembler actually gets.
    SO = S.T_STONE - S.T_TIMBER          # 0.12
    for x in (1.0, 3.0, 5.0, 7.0):
        put("SM_Beam_JettySoffit_2m", (x, -J, JZ))     # the overhang's underside
        put("SM_Beam_JettyPlate_2m", (x, -SO, JZ))     # what its joists bear on
    # ---- the DRAGON CORNER, turning the jetty on to the flank --------------
    # At the far end, where the run stops at x = 8, the jetty turns. The corner
    # square is x 8..8+J, y -J..0, so the piece is rotated 90: its outer planes
    # land on the flank's x = 8 + J and on the front's y = -J, its inner corner
    # on (8, 0) -- the outside corner of the storey below -- and its diagonal
    # runs between the two, which is exactly where a dragon beam goes.
    put("SM_Beam_DragonBeam_Corner", (8.0 + J, 0.0, JZ), rz=90)
    put("SM_Beam_JettySoffit_2m", (8.0 + J, 1.0, JZ), rz=90)   # the flank run
    put("SM_Beam_JettyPlate_2m", (8.0 + SO, 1.0, JZ), rz=90)
    # NO bressumer on that flank bay or over the corner, and that is deliberate:
    # a jetty with its bressumer on shows one deep beam and a shadow, so the run
    # in front of the camera is the finished thing and the corner behind it is
    # the SAME construction with the closing beam left off -- the joists, their
    # moulded noses, the boarded soffit between them, the plate they bear on and
    # the dragon beam on the diagonal. One render, both halves of the answer.

    # ---- THE TWO STOREYS, so that the OVERHANG can be read -----------------
    # Context, not kit pieces (see DEMO CONTEXT above). The ground floor in
    # stone, its face on y = -SO; the jettied storey standing on the bressummer
    # with its face on y = -JETTY. That 0.33 m step is the entire subject of
    # this render and of the round: the upper floor is a LARGER AREA than the
    # one below it, carried out there on joists, and every piece in this file's
    # section 7 exists to make the underside of that gained area real.
    # The three ctx walls WRAP BOTH CORNERS now (front -0.36..8.12, return
    # -0.12..1.90, flank 0.10..2.00). They used to stop 0.40 m short of the
    # front-left corner, which left SM_Corner_JettyJoint's return corbels with
    # no masonry to break out of at all.
    #
    # The demo is deliberately HALF BUILT, and that is the composition: the run
    # facing the camera is finished (stone, plate, bressummer, brackets, wall
    # above), while the corner NEAREST the camera is left with its bressummer
    # and its upper wall off, so the same construction is shown from the outside
    # AND with its skin off -- joists, moulded noses, boarded soffit, jetty
    # plate, and the dragon beam turning it on to the flank.
    fr = _ctx_stone("CTX_JettyGroundFront", -SILL_CELL - SO, 8.0 + SO,
                    door=(0.35, 1.65, 1.52), h_face=2.58, seed=1)
    fr.location = (0.0, -SO, 0.0)
    out.append(fr)
    fl = _ctx_stone("CTX_JettyGroundFlank", 0.10, 2.0, h_face=2.58, seed=2)
    fl.location, fl.rotation_euler = (8.0 + SO, 0.0, 0.0), (0, 0, radians(90))
    out.append(fl)
    rt = _ctx_stone("CTX_JettyGroundReturn", -1.90, SO, h_face=2.58, seed=3)
    rt.location = (-SILL_CELL - SO, 0.0, 0.0)
    rt.rotation_euler = (0, 0, radians(-90))
    out.append(rt)
    # The front wall of the jettied storey runs the whole front AND ACROSS THE
    # DRAGON CORNER, to x = 8 + J. That is the one thing the dragon beam exists
    # for -- "so TWO sides can jetty at once" -- and the demo did not show it:
    # the upper wall used to stop dead at x = 8, leaving the corner and the
    # flank carrying nothing, so the corner module read as a shelf rather than
    # as the thing holding the storey above up round the turn. Now the wall
    # stands ON the corner's deck, and the flank's own wall is begun on the
    # flank tile (see _ctx_sole) so the joists under it stay readable.
    up = _ctx_upper("CTX_JettyUpperWall", -SILL_CELL, 8.0 + J)
    up.location = (0.0, -J, S.H_GROUND)
    out.append(up)
    so = _ctx_sole("CTX_JettyUpperFlankSole", -0.30, 2.0)
    so.location, so.rotation_euler = (8.0 + J, 0.0, S.H_GROUND), (0, 0, radians(90))
    out.append(so)

    # ---- AND THE SOFFIT ITSELF, LAID OUT ON THE GROUND ---------------------
    # Every camera in this kit looks DOWN -- build_piece.py's four are at 10-26
    # degrees above horizontal, and both hero cameras are elevated -- and a
    # soffit is the one face a downward camera can never see. Once the jetty is
    # built, the piece the round is about is by definition hidden under it. So a
    # spare tile and a spare dragon corner lie SOFFIT UP on the ground in front
    # of the run, the way a framer lays members out before they are lifted: the
    # boarded soffit, the five square-set joists at G/5 centres with their
    # moulded noses standing proud of the fascia, and on the corner the dragon
    # beam on its diagonal with the short joists it carries. The identical
    # objects are in the wall above them, the right way up.
    #
    # ROUND 10 -- THEY ARE STOOD AGAINST THE WALL, not laid flat. Flat on the
    # ground (rx=180) the soffit faces straight UP and every camera in this repo
    # is 10-26 degrees ABOVE horizontal, so the one face they were laid out to
    # show was foreshortened to about 40% and they read as two small crates in
    # the corner of the frame. Leaned back against the ground storey (rx=-120)
    # the soffit's normal comes to 30 degrees off vertical FACING THE STREET,
    # i.e. almost square to the demo camera, and the wall visibly holds them up
    # -- a framer's members stacked against the building before they are lifted,
    # which is also what puts them at the foot of the very wall they belong to
    # instead of adrift on the ground. It tightens the shot as well: the pair no
    # longer reach y = -2.16, so the camera closes in on the jetty itself.
    _rest(put("SM_Beam_JettySoffit_2m", (4.55, -SO - .085, 0.0), rx=-120))
    _rest(put("SM_Beam_DragonBeam_Corner", (6.80, -SO - .085, 0.0), rx=-120))

    for nm in src:
        src[nm].location = (0, 60, 0)         # park the originals out of frame
    return out


def _demo_jetty_corner():
    """SM_Corner_JettyJoint, built here as DEMO CONTEXT ONLY (no SM_ prefix, so
    it can never be mistaken for a piece of this family). It belongs to
    kit/pieces/corners.py, which derives its two lapped sills from THE JETTY
    SILL PROFILE at the top of this file -- so putting the real thing at the end
    of the real run is the only honest way to prove the interface holds. Import
    is local: corners.py imports THIS module at load time."""
    from kit.pieces import corners as C
    return C.jetty_joint("_demo_JettyJoint")
