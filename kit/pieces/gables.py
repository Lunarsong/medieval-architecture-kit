"""Gable ends -- the front gable of ref2 is the single most characterful shape in
either painting, so this family is mostly about getting ONE silhouette right and
then dressing it.

Read off the crops (ref3:bargeboard is the clearest -- greyscale linework):
  * The rake board is a PLANK, and its depth is a tenth of the gable's rise, not
    a fifth: re-measured on both crops it is 6-8% of the apex-to-foot height,
    with a scallop fringe under it worth another 4-5%. See the note by BW -- the
    board this file used to draw was twice that, and on the assembled inn (where
    the assembler amplifies this piece's perpendicular offsets by 1.24-1.29) it
    hung 0.84 m off the verge. Under it: a bold two-step OGEE roll worked along
    the lower edge -- tightened this round onto the edge itself, 124 mm of the
    board's 335 rather than 170 spread up its face -- and a fringe of PENDANT
    DENTILS hung off that edge at CUSP = 0.150 centres, so the gaps match the
    teeth. A DENTIL LADDER -- a run of small
    blocks -- is worked along the face below the top edge, where this file used
    to run a smooth cap bead; see the DENT note for the crops that settled it.
  * The bargeboard FOLLOWS THE ROOF ALL THE WAY DOWN and only then bends: the
    roof's own bell-cast flicks the last 0.4 m of rake up out of the 52 deg
    plane, the verge goes up with it (BELL), and the board's LOWER EDGE sweeps
    up with the eave (LOWSWEEP) instead of diving under it, so the board narrows
    from 0.42 m at the wall line to 0.28 m at the drip and runs into a carved
    scroll that SEATS on the eave course. See the BELL and LOWSWEEP notes -- the
    scroll used to hang 0.34 m below the last shingle. Its HEAD is cut on the ridge and dies into an upright apex block with
    a moulded cap, which is what carries the finial -- crop ref3:bargeboard and
    look at the top of the gable. The two boards LAP behind that block rather
    than crossing in front of it, and the block is SHORT: it stops on the boards
    (ZA-0.290), it does not hang down past them. See the AP_* table.
  * The board's top edge stands PROUD of the shingle surface, so the tile ends
    are covered by it and nothing ragged shows along the rake (see VERGE_LAP).
  * The verge is thick: you see shingle on top, a dark soffit under, and purlin
    ends poking out of the gable wall into that shadow.
  * The gable face is a half-timber truss: bottom tie beam, mid rail, two BIG
    CURVED BRACES arching around a small window, a king post with a collar over
    it, and a vertical-boarded tympanum at the top (sometimes pierced with
    diamonds). Timbers are narrow (0.13-0.15) against big cream panels. The
    window's SILL and LABEL MOULD belong to THIS piece -- see the WALL OWNS THE
    SURROUND note over `_face`'s cill -- and SM_Gable_WinFrame carries no trim
    of its own at all, so there is still exactly one sill and one head.
  * A BROAD SHALLOW ARC spans under the apex itself, and how it is trussed
    depends on how much triangle there is: on a wide gable the arc sits over the
    top rail with a king post and two struts on its crown, on a narrow one it
    springs off the rafters over the window and the rail rides up onto it as a
    collar. Both are in ref3; _apex_fit measures the gable and picks.
  * Ridge: a row of upright rounded pegs -- a dentil comb -- on a ridge board,
    running back from the gable apex, with a carved finial over the apex itself.

Conventions used here
---------------------
GABLE END (`_end`): wall-family rules. Origin = centre of the gable's base, on
    the wall line. X in [-W/2, W/2] with W = bays*GRID, Y in [0, T_TIMBER] with
    the OUTER FACE ON Y=0, Z in [0, ZA] where ZA = tan(PITCH)*W/2. Relief
    (timbers, purlin stubs, ledge) stands proud to -Y within PROUD_MAX. The
    triangle's edges ARE the rake lines, so a roof slope lands on them exactly.
BARGEBOARD (`_barge`): deliberate seam-spanning trim, and therefore a separate
    piece (spec.py). Same origin/orientation as the gable end it dresses -- drop
    it on with an identical transform -- but it projects VERGE_OVER outboard and
    a little past the rake feet, which is declared in its seams.
WINDOW FRAME: AN INSERT, and nothing but an insert. Origin at the bottom-centre
    of its opening, on the wall face (Y=0), so it snaps to any `win_attic`
    opening: `at=(0, 0, SILL_Z[bays])`. NOTHING in it leaves the box
    x in [-IW/2, IW/2], z in [0, IH] -- the opening less INSERT_CLEAR all round
    -- and that box is DECLARED AS ITS SEAMS, so `Part.check()` proves the fit on
    every build instead of a human eyeballing a render. See win_frame().
FINIAL: prop rules -- origin at footprint centre, Z=0 at the bottom.
RIDGE COMB: roof rules -- ridge along X, origin on the ridge line, tiles at GRID.
    (Not in the family table; the combs in ref2 run from every gable apex along
    every ridge, and nothing else in the kit provides them.)
"""
import bpy
from math import tan, sin, cos, sqrt, radians
from mathutils import Matrix, Vector
from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "gables"
COLLECTION = "05_Gables"

G = S.GRID
T = S.T_TIMBER
P, PD = S.PITCH, S.PITCH_DEG
SINP, COSP, TANP = sin(P), cos(P), tan(P)

VO = S.VERGE_OVER          # 0.30 -- verge projection outboard of the wall face
RT = 0.155                 # roof build-up thickness at the verge

# ---- the rake board. This is the family's signature and it has to be a PLANK,
# not an edge; but it was TWICE the plank the references draw, and on the
# assembled inn that is what left a thousand vertices of it hanging in air.
#
# RE-MEASURED off the crops (ref3:bargeboard and ref2:bargeboard at 1:1). Take
# the gable's own rise -- apex to the rake foot -- as the ruler, because it is
# the one length both the drawing and this piece agree on:
#     ref2  rise 233 px, board face 14 px, scallop fringe 10 px  ->  6.0% + 4.3%
#     ref3  rise 190 px, board face 15 px, scallop fringe 10 px  ->  7.9% + 5.3%
# i.e. board plus fringe is 10-13% of the rise, not the 25% this file used to
# assert (BW 0.460 + DAG 0.195 on a 2-bay's 2.56 m rise = 25.6%). The old
# docstring's "0.45-0.50 m of face" is simply not in the drawing.
#
# AND THE ASSEMBLER AMPLIFIES IT. assemble_inn places this piece (kx, 1, kx*ZK),
# which multiplies every offset PERPENDICULAR to the rake by 1.150*kx -- 1.288 on
# a 2-bay gable, 1.242 on the 3-bay as laid. So the authored 0.655 m of board +
# fringe came out 0.84 m of oak hanging off a verge, and every vertex of its
# lower half was half a metre clear of the nearest shingle. At 0.335 + 0.130 the
# board and its fringe measure 0.60 m assembled on the 2-bay's 4.80 m rise
# (12.5%) and 0.58 m on the hero's 6.95 m (8.3%) -- inside the references' 10-13%
# instead of at 17.6% -- and the fringe's lower edge comes in from 0.71 m below
# the roof plane to 0.47 m.
BW = 0.335                 # face depth, perpendicular to the rake
BT = 0.095                 # board thickness
BSWELL = 0.26              # extra face depth where the board swells into its foot
BFOOT = 0.95               # rake length over which the swell happens
DAG = 0.130                # pendant dentil drop below the board's lower edge
CUSP = 0.150               # dentil spacing along the rake. RE-MEASURED off
                           # ref3 rather than picked: crop the greyscale at
                           # (880,220)-(1010,400) and the fringe on the central
                           # gable's right rake runs 14 curls over ~80 source px
                           # of rake -- pitch 5.7 px against a fringe 5 px deep
                           # and a board face 9 px. So the reference's ratios are
                           #     pitch / fringe depth   1.14
                           #     tooth width / depth    ~0.9  (the curls touch)
                           # At 0.190 against DAG 0.130 this file was running
                           # 1.46 and a tooth 0.148 x 0.130 -- wider than deep,
                           # spaced with a visible gap, which is what made the
                           # row read as bolts on a plate in the street render
                           # rather than as a carved frill. 0.150 puts the pitch
                           # at 1.15 x the drop and the tooth at 0.117 x 0.130,
                           # i.e. ON the reference. NOTHING GETS SHALLOWER FOR
                           # THIS: DAG and BW are untouched, the fringe reaches
                           # exactly as far below the board as it did, and there
                           # are ~31 teeth per rake instead of ~25 (+364 tris on
                           # the 3-bay, which has 1632 of headroom).
LIPW = 0.200               # face depth of the kerb lip that laps the tile ends
LIP_DROP = 0.038           # the board's top edge sits this far BELOW the lip's
CAP_DROP = 0.035           # ... and the DENTIL LADDER this far below the board's
FOOT_STOP = (.016, .030, .044, .058, .072)   # where lip / (unused) / step / ogee
                           # / web stop short of the board's own end section.
                           # Index 1 was the cap BEAD's, and the bead is gone --
                           # see the DENT note. Left in place rather than
                           # re-indexed: these five numbers exist only to keep
                           # five end faces off one plane, and shuffling them
                           # would move four bands that are measured where they
                           # are.

# ===========================================================================
# THE VERGE READ AS CORDUROY: FIVE PARALLEL STRIPES OF SIMILAR WEIGHT.
# ---------------------------------------------------------------------------
# Measured on the board's own face, in v (perpendicular to the rake), reading
# down from the top edge at VERGE_LAP - LIP_DROP = +0.104 on a straight run:
#     +0.104 .. +0.069   plank            35 mm
#     +0.069 .. -0.031   CAP BEAD         100 mm  oak_mid, 26 mm proud
#     -0.031 .. -0.051   plank            20 mm
#     -0.051 .. -0.129   OGEE STEP        78 mm   oak_mid, 20 mm proud
#     -0.129 .. -0.221   OGEE ROLL        92 mm   oak_mid, 36 mm proud
# i.e. 270 of the board's 335 mm of face was moulding and 55 mm of it was board,
# in three pale oak_mid ribbons running the whole rake. Rendered from a 1.65 m
# street eye at 135 mm the rake came back as five bands of near-equal weight
# (kerb / plank strip / bead / step / roll) before the eye ever reached the
# fringe. That is the corduroy.
#
# WHAT THE REFERENCE ACTUALLY DRAWS -- and I re-cropped it rather than trusting
# the note that commissioned this. ref3 at (880,220)-(1010,400) is the central
# gable's right rake; at 15x on a clean stretch below the tympanum
# ((935,340)-(995,420)) it reads, outboard to inboard:
#     a thin kerb line
#     ONE BROAD PLAIN PLANK        ~17-18 source px of face
#     a run of small blocks on the lower edge, each a rounded lobe with a scroll
#       tail, pitch ~9 px, drop ~9 px, close-packed with narrow gaps
# and ref2 -- the colour painting of the SAME building, crop (836,143)-(1064,440)
# -- shows the identical arrangement in paint: a pale plain plank with a row of
# small pale blocks along its lower edge, running the ENTIRE rake, apex to foot.
# So against the board face the reference's ratios are
#     block pitch / board face   0.52     (ours: CUSP 0.150 / BW 0.335 = 0.45)
#     block drop  / board face   0.52     (ours: DAG  0.130 / BW 0.335 = 0.39)
# HONEST CORRECTION TO THE NOTE THAT ORDERED THIS WORK: that run of blocks down
# the whole rake IS the dagged lower edge, and this piece already carries it as
# its pendant fringe. There is no SECOND ladder worked on the plank's face in
# either painting -- the porch gable (ref3 (820,660)-(1080,840)) and the plain
# rear gable ((130,180)-(330,470)) both show one plain plank and one toothed
# edge, and the "ladder of cells" the earlier crop found inboard of the fringe
# is the tympanum's vertical boarding crossing behind the rake (visible at 17x,
# (898,250)-(948,315)). Where the reference DOES put rows of small blocks other
# than on a dagged edge is under a horizontal fascia: the porch eave in that
# same crop hangs four of them under its eave board.
#
# WHICH STILL LEAVES THE CAP BEAD WRONG, AND A DENTIL COURSE IS THE RIGHT THING
# TO PUT THERE. The bead is a 100 mm pale ribbon lying along the board's face,
# and the reference has no such ribbon anywhere. Broken into blocks on the same
# line it becomes the one ornament the reference does draw against a closing
# fascia, it is what BRIEF.md asks for by name ("Dentil courses: rows of small
# blocks under the eave fascia and under the verge"), and it costs nothing in
# proudness because it lives in the bead's own Y layer (Y_CAP).
DENT = 0.112               # pitch of the ladder along the rake. FINER than the
                           # fringe's CUSP 0.150 on purpose: two toothed rows at
                           # the same pitch on one board are a new corduroy of
                           # two, and a dentil course is characteristically
                           # squarer and closer than a dagged edge.
DENT_W = 0.062             # block width along the rake -> duty 0.55, so a 50 mm
                           # gap survives to the street camera instead of the
                           # row closing back up into the ribbon it replaced.
                           # (The fringe runs duty 0.78 and gets away with it
                           # because its teeth are 130 mm DEEP; these are flat.)
DENT_D = 0.086             # block depth across the section, in v: 14 mm inside
                           # the bead's 100 mm, so the plain face either side of
                           # the row grows rather than shrinks.
DENT_U0 = -0.095           # the ladder's foot station. The foot scroll's up-rake
                           # edge is at BOSS a = 0.238, which on the measured
                           # foot tangent t = (0.679, -0.733) is u = -0.178; a
                           # block below that is inside the scroll, invisible,
                           # and sharing 53 mm of Y with it. The scroll is what
                           # finishes the board at the foot -- same reason the
                           # fringe starts at FRINGE_U0.
DENT_BURY = 0.022          # ... and the row is CUT on a plane this far inside
                           # the apex post's flank, rather than stopped at the
                           # last whole block that clears it. The post is
                           # POST_W/2 = 0.160 in x and shares 70 mm of Y with
                           # Y_CAP, so a whole-block stop is phase-dependent and
                           # lands anywhere in a 69 mm window: measured, the last
                           # block of the 3-bay's row came out at |x| = 0.186,
                           # its head 7 mm OUTBOARD of the flank -- and a block
                           # half a pitch later would have sat 39 mm inside the
                           # post with its outer face 4 mm proud of the post's,
                           # a pad on the king post's cheek. Cutting the row on
                           # _mitre(Wh, POST_W/2 - DENT_BURY) instead makes the
                           # stop the same at any gable width: the last tooth is
                           # sliced flush, dies 22 mm into the flank, and the
                           # only thing standing off the post is a 22 x 86 mm
                           # sliver 4 mm proud of it.
DENT_KEEP = 0.30           # ... and a sliced tooth is dropped if less than this
                           # much of its area survived, so the row never ends in
                           # a 1 mm shard of oak.
#
# WHAT IT COST, AND WHAT IT DID NOT MOVE. Measured on the built meshes, the bead
# version against this one (43 blocks per rake on the 3-bay, 29 on the 2-bay,
# 12 tris each at bevel 0; the bead was one long bevelled prism worth ~776):
#     SM_Gable_Barge_3bay   5204 -> 5468 tris   (budget 6500, 1032 spare)
#     SM_Gable_Barge_2bay   4588 -> 4516 tris   -- the 2-bay's row is shorter
#                                                  than the bead it replaced
# and every number the last round settled is unchanged to the millimetre, which
# is the point of keeping the row in Y_CAP:
#     y_min            -0.4475 / -0.4474     both, before and after
#     proud of the tile cut at y = -VO      +0.1475 / +0.1474    both
#     z_min            -0.2219 / -0.2230     both  (declared seam -0.24)
#     z_max             2.7149 /  3.9905     both
#     v_max out of the roof plane on the straight run  +0.1454 / +0.1444  both
#         -- still the KERB LIP (VERGE_LAP + wobble), not the ladder, which tops
#            out at v = +0.069 against the plank's own top edge at +0.104.
# check_zfight: both barges report 0 cm2 at 0.2 mm AND at 0.5 mm (the family's
# 110 / 718 cm2 is all on the gable ends and the WinFrame, untouched here).
# check_layouts: L1 and L2 report the same barge depths to the millimetre
# (0.642 / 0.639 / 0.238 / 0.201). L3's cross-wing barge moved 1.944 -> 2.022 m
# with 59 FEWER verts through the roof, and that is the gate's documented blind
# spot, not a regression: it reports the max over whichever vertices qualify, a
# bead polygon carried vertices only at its ~16 stations while the row carries
# eight every 0.112 m, so the same envelope is simply sampled more densely. The
# envelope itself is the five numbers above, and none of them moved.
# ===========================================================================

# ===========================================================================
# THE FOOT FOLLOWS THE ROOF DOWN TO THE EAVE. IT USED TO FLY OFF IT.
# ---------------------------------------------------------------------------
# Shanee, on a close crop of the assembled inn: "the barge bay beams need to
# follow the roofline and then bend, or at least make sure it's covered properly
# and looks right on all sides ... this is true pretty much everywhere."
#
# What it was doing: `BKICK = 0.34` lifted the WHOLE verge assembly off the roof
# plane over the bottom BFOOT = 1.10 m of rake -- quadratically, so the lift was
# still 0.10 m half a metre up the rake -- and the boards then STOPPED at
# u = -0.075, i.e. 0.05 m of rake below the gable's base corner. Measured on
# out/inn_example.blend, in this piece's own rake frame (u along the rake from
# the base corner, v out of the nominal roof plane):
#     the kerb lip's top edge at the foot     v = +0.53
#     the roof surface under it               v = +0.13
#   so the board's foot stood 0.4 m clear of the shingles it is supposed to
#   cover, and the last 0.21 m of rake -- the eave overhang, which EAVE_OVER's
#   change to 0.14 did not remove, only shortened -- had no bargeboard on it at
#   all. That is both halves of "curls up and away" and "the roof line and the
#   barge do not meet".
#
# THE ROOF'S OWN EDGE, MEASURED, NOT GUESSED. roofs.eave() flares the bottom
# SWEEP_LEN of slope on a bell-cast (spec.SWEEP), so the roof surface at a verge
# is NOT a straight line: probed on the assembled inn along the outermost 0.10 m
# of field (y -0.34..-0.24), transformed back into this piece's rake frame, the
# top of the shingle field runs
#     u  +0.20 and up   v = 0.06-0.07      the flat field
#     u   0.00          v = 0.065
#     u  -0.05          v = 0.13
#     u  -0.10          v = 0.185
#     u  -0.15          v = 0.205
#     u  -0.20          v = 0.28
#     u  -0.25..-0.35   v = 0.32-0.34      the swept eave
#     u  -0.40          v = 0.33           the last material
# So the roof itself turns up 0.27 over its last 0.40 m of rake. RE-MEASURED
# THIS ROUND, over every roof object in the scene rather than a 0.10 m strip of
# field: the last material is at u = -0.399 on a 2-bay verge and -0.414 to
# -0.421 on the 3-bay, NOT the -0.32 this note used to assert, and its lowest
# world z is -0.151 (2-bay) / -0.156 (3-bay). Those two numbers are U_DRIP and
# Z_EAVE below and everything at the foot is now cut against them.
# A bargeboard on this must do the same thing: run to the drip and bend with it.
# BELL/BELL_U/BELL_P are fitted to that measured curve so the kerb lip laps the
# field from the drip to the apex, and U0 puts the board's centreline 0.06 m
# short of the last shingle instead of 0.25 m short of it.
BELL = 0.35                # lift of the verge out of the roof plane at the drip
BELL_U = 0.36              # rake length over which the bell-cast dies out
BELL_P = 1.15              # ... and its shape. Fitted so the kerb lip's top edge
                           # laps the measured field by 23-78 mm at EVERY station
                           # from the drip to the apex -- the same 60-80 mm kerb
                           # it keeps on the straight run, carried round the
                           # flare. A plain square law runs 40 mm UNDER the
                           # shingles at u = -0.25 and a steeper one lifts the
                           # foot 0.14 m off them, which is the fault being fixed.
U0 = -0.34                 # the foot, in rake units below the gable base corner.
SLAB_U0 = 0.10             # the verge slab's foot, and the rake length over
SLAB_TAP = 0.32            # which it tapers out: see the note in _rake_assembly
FRINGE_U0 = 0.10           # the pendant fringe starts here: above it the board's
                           # lower edge is straight, below it the bell-cast is
                           # swinging the section up and the scroll takes over

# ===========================================================================
# THE FOOT PADDLE HUNG BELOW THE EAVE. THE BOARD'S LOWER EDGE HAD TO SWEEP UP.
# ---------------------------------------------------------------------------
# Shanee, on a close crop of the west gable: the barge "terminates in a large
# rounded scroll at each end which projects outward and downward with nothing
# behind it".  Measured on the assembled inn (assemble_inn.build_inn(), every
# roof vertex transformed into THIS piece's rake frame -- u along the rake from
# the gable base corner, v perpendicular to it, world z off the gable base):
#
#                              roof, at the verge      barge          hangs
#     lowest world z                -0.151              -0.344      0.193 m
#     lowest rake station u         -0.399              -0.505      0.106 m
#
#   and the assembler multiplies this piece's z by kz = 1.81-1.88, so the
#   authored 0.19 m came out 0.34-0.36 m of oak below the last shingle. That is
#   the auditor's "0.331 m at the foot paddle" and it is what you see: the
#   scroll's whole lower half is under the eave line, in front of a wall it is
#   VERGE_OVER = 0.30 m away from.
#
# WHY IT WENT DOWN THERE, WHICH IS NOT WHERE THE PADDLE WAS DRAWN. Every band of
# this rake is the centreline offset along the SECTION NORMAL, and through the
# bell-cast that normal swings until it is all but vertical in world (measured:
# n.z = 0.997 at the drip).  So a board 0.422 m deep at the foot spans 0.42 m of
# world HEIGHT there, its centreline sits at z = -0.132, and its lower edge is
# therefore at -0.34 whatever the paddle does.  The board's lower edge DIVED
# through the flare -- z -0.222, -0.294, -0.312, -0.324, -0.334, -0.342 from the
# wall line to the drip -- and the scroll was built off that corner, so it dived
# with it.  ref1's swept eave does the opposite: the board's lower edge FLICKS
# UP.  ("the bargeboard is a wide flat plank that follows the roof edge and
# flicks upward at the bottom" -- BRIEF.md.)
#
# WHAT IT IS NOW: the board's lower half is swept away through the flare, so the
# lower edge lifts instead of diving -- z -0.222, -0.212, -0.207, -0.203, -0.201,
# -0.198 over the same six stations -- and the board narrows from 0.422 m at the
# wall line to 0.277 m at the drip, running INTO its scroll the way a swept eave
# does.  The scroll is rebuilt inside that: nothing below Z_FOOT, nothing past
# the drip in u, and its fullest projection lands at x = -0.47 against a roof
# whose own eave reaches -0.50.  It bears on the board over its whole up-rake
# edge and its toe is 0.018 m under the board's lower edge, not 0.15 m under the
# eave.
LOWSWEEP = 0.70            # fraction of the board's lower half swept away at the
LOWSWEEP_P = 0.34          # drip, and its shape in kt (= the bell-cast's own
                           # parameter, 0 above the flare and 1 at the drip). The
                           # exponent is low on purpose: the lift has to arrive
                           # as fast as the section rotates, and a square law
                           # leaves the edge diving for the first 0.1 m of flare.
Z_EAVE = -0.151            # MEASURED: the lowest world z the assembled roof
                           # reaches at a verge, in this piece's own frame.
U_DRIP = -0.399            # ... and the lowest rake station it reaches.
Z_FOOT = -0.234            # the level cut every rake band now takes at its foot:
                           # 12 mm under the board's own lower edge where that
                           # edge is deepest (the wall line, z = -0.222), so it
                           # is a backstop that only catches the scroll's toe and
                           # stray wobble, never the board itself.
FOOT_Z = (.000, .014, .028, .042, .056)   # ... staggered per band, so the five
                           # horizontal end faces it can make are never coplanar
DAG_FADE = 0.55            # the pendants shorten over this much rake above the
DAG_MIN = 0.55             # flare, to DAG_MIN of their length, and die into the
                           # scroll instead of hanging their full drop off a
                           # board that is itself narrowing into it.
# The scroll, in the board's own end-section frame at station 0: `a` runs up the
# rake (0 = the board's end section) and `b` across it (0 = the centreline,
# +BW/2 the top edge). At the foot that frame is all but a world elevation --
# t.z = +0.079, n.z = +0.997 -- so `a` reads as horizontal and `b` as vertical,
# which is why the shape can be drawn straight against the measured eave.
BOSS = ((0.238, -0.052),   # springs off the board's swept lower edge, 64 mm
                           #   up inside it, so the whole of this edge bears
        (0.104, -0.066),   # a short LEVEL SEAT under the board's end -- this is
                           #   the face that sits down on the eave course
        (0.048, -0.092),   # the toe of the volute, its lowest point (z = -0.220)
        (-0.004, -0.056),  # the nick where the scroll curls back on itself
        (-0.046, 0.006),   # ... and out again
        (-0.082, 0.086),   # the fullest projection: x = -0.472, u = -0.332
        (-0.062, 0.196),   # coming back in
        (0.012, 0.266),    # over the kerb lip's own end cut
        (0.142, 0.284),    # dying back onto the lip
        (0.238, 0.120))    # ... and onto the board's face
# ===========================================================================

# ===========================================================================
# THE VERGE IS A BOARD ON EDGE, NOT A PLANK LYING ON THE ROOF.
# ---------------------------------------------------------------------------
# Shanee, on the assembled inn: "The gable end/barge pieces like
# SM_Gable_Barge_2bay.001 and SM_Gable_Barge_3bay.001 join the roof quite badly,
# with the wood seems to go straight out from the shingles in a strange way."
#
# WHAT IT ACTUALLY WAS -- measured, not guessed. Two rounds ago the question was
# whether a slope run dying at a gable needs its own END TILE ("perhaps we need
# an end piece for SM_Roof_Slope_2m_B.017 ... or is that the barge bay?"). The
# answer then was "it is the barge", and that answer is still right: assemble_inn
# lays the field over run = (wall face - VERGE_OVER, wall face + VERGE_OVER), so
# the outermost panel's x seam falls EXACTLY on y = -VERGE_OVER and _field cuts
# its tabs flush there (lo/hi are clamped to the panel seam, and finish()'s
# clamp_to_seams flattens the rest). There is nothing ragged for an end tile to
# tidy. So no new roof piece -- but the barge was not covering the cut either.
#
# What it WAS doing: every layer of this rake is a ribbon extruded in Y, so its
# outer face is PARALLEL TO THE ROOF PLANE by construction. The cap bead was
# 0.216 m thick in Y and rode the board's top edge, which laid a flat 0.22 m wide
# oak_mid face at v = 0.166 along the whole rake -- lapping 85 mm over the field
# and hanging 131 mm past it into thin air. A wide flat face parallel to the roof
# takes the same light as the roof, so it read as a pale plank lying IN the
# shingle field and running out of it. Measured off out/inn_example.blend in the
# assembled 65 deg world (probe: v out of the roof plane vs w outboard of the
# wall face) the west wing's verge was one shelf, v = +0.214 for w = 0.20..0.44,
# against a field whose proudest tab reaches +0.095. Proud, yes -- and totally
# flat, which is why it read as roof rather than as trim.
#
# WHAT IT IS NOW: the top of the verge is a KERB that steps DOWN outboard in
# three treads, so nothing wide is parallel to the roof and the highest thing on
# the rake is the inboard lip that laps the tile ends:
#
#   field butts 0.063 (proudest tab 0.082)
#          | LIP  v = VERGE_LAP        80 mm of tread, laps the cut ends 60 mm
#          | board top  -LIP_DROP      68 mm of tread
#          | dentils    -CAP_DROP      48 mm of tread, below the field's butts
#   ...so from any direction outboard the LIP is the highest thing and hides the
#   course ends behind a real riser (58 mm authored, 75 mm on a 2-bay gable and
#   94 mm on the stretched hero), and the outer edge of the verge sits BELOW the
#   field instead of hovering over it. The lip and the board are oak_dark, and
#   only the small bead is oak_mid: the pale ribbon is gone.
#
# The numbers survive the assembler's stretch, which is why they are set off
# roofs.py's own build-up rather than picked by eye: assemble_inn scales a roof
# piece's perpendicular offsets by 1.150 and THIS piece's by 1.150*kx (kx = 1.12
# on a 2-bay gable, 1.41 on the stretched hero), so the barge's relief grows
# FASTER than the field's and a lap that holds here holds there.
FIELD_BUILD = 0.0632       # = roofs.BUILD, the outer face of a course butt
FIELD_PROUD = 0.0823       # ... and the proudest tab in a measured field, which
                           # is what the lip actually has to clear
VERGE_LAP = 0.142          # THE LIP's top edge, out of the nominal roof plane.
                           # 60 mm over the proudest tab, and the board's own top
                           # edge is LIP_DROP below it, so the lip is the only
                           # thing the field can meet.
# ===========================================================================

# ===========================================================================
# NO TWO OPAQUE FACES IN A PIECE MAY SHARE A PLANE.
# ---------------------------------------------------------------------------
# That is what Shanee's "a lot of z-fighting on the inside/backside" is: two
# coplanar overlapping faces, and the renderer cannot decide which is in front,
# so it flickers -- worst of all when it happens on a face you can actually see.
# It came from layers that ABUT: a backing whose front face lands exactly on the
# back face of the skim in front of it.
#
# The rule every layer table below obeys: any two solids that overlap in plan
# either INTERPENETRATE by >= 12 mm or clear each other by >= 12 mm. Never
# abut. check_zfight.py buckets planes 2.5 mm apart together, and wobble() is
# coherent noise (neighbouring vertices move together), so a 12 mm relative
# offset survives both. Members that CROSS each other -- a stud over a rail, a
# brace over a rake plate -- each get their own front/back pair, which is also
# why the frame now reads as hand-hewn timber of varying thickness instead of
# one flat sheet.
#
# After touching any of these numbers, re-measure:
#   blender -b --python check_zfight.py -- gables
# ===========================================================================

# Y layers of the rake assembly (Y is world Y throughout; -Y is outboard).
# The board face is the outermost plane, the ogee roll and its pendants stand a
# little proud of it, and a dark web closes the slot behind the deep board.
# These layers all overlap each other in plan along the whole rake, so they are
# spread 20 mm apart minimum: the rake assembly gets wobble(.006) and its faces
# are up to 4 m long, and a long wobbled face's measured plane wanders by a few
# mm either way, so 12 mm was not enough here (measured).
# The Y ladder is ALSO the plan-view profile of the verge, which is what went
# wrong: read the four top members outboard from the field's cut at y = -0.300
# and they now step DOWN, lip -> board -> bead, instead of presenting one flat
# 0.22 m shelf. Nothing at the top of the rake is wider than 80 mm in Y.
#
# AND THE LADDER IS ALSO HOW FAR THIS PIECE STANDS PROUD OF THE VERGE. The roof
# field is cut dead on y = -VERGE_OVER = -0.300; measured on the assembled inn
# the barge's outermost geometry sat at y = -0.513, so 0.213 m of it -- the
# rolls, the swept tail, the king-post head and the saddle over it -- stood
# outboard of the roof edge with nothing behind them, a 0.5 m thick fin on a
# 0.3 m verge. The BOARD was never the problem (its face is only 0.09-0.10 m
# proud, which is a board thickness); the mouldings piled up on top of it were.
# Every layer outboard of the plank is pulled in below, keeping the 20 mm
# minimum between any two planes that can overlap in plan, and the extreme
# is now 0.450 -- 0.150 past the verge cut instead of 0.213.
Y_LIP = (-VO - .020, -VO + .060)              # the kerb lip: laps the tile ends
                                              # (cut at -VO) by 60 mm and is the
                                              # highest thing on the rake
Y_PLANK = (-VO - .092, -VO + .010)            # the broad board face, 12 mm into
                                              # the field and 72 mm outboard of
                                              # the lip's own outer plane
Y_OGEE = (-VO - .128, -VO - .046)             # fat lower roll of the ogee: 36 mm
                                              # proud of the board's face
Y_STEP = (-VO - .112, -VO - .022)             # the step above it. 20 mm proud of
                                              # the board, 16 mm inside the roll,
                                              # and its inner face is outboard of
                                              # the web's so the web can bite into
                                              # the board without landing on the
                                              # roll's plane.
Y_DAG = (-VO - .072, -VO - .024)              # THE FRINGE IS THE BOARD'S OWN
                                              # DAGGED EDGE, NOT A ROW OF BLOCKS
                                              # NAILED TO ITS FACE.
                                              #
                                              # It was (-VO-.108, -VO-.066): a
                                              # 42 mm fin whose outer plane stood
                                              # 16 mm PROUD of the plank's own
                                              # face (-VO-.092) and 108 mm proud
                                              # of the tile cut -- the second
                                              # proudest thing in the piece after
                                              # the foot scroll, and measured on
                                              # out/inn_example.blend the worst
                                              # roof-clearance vertex on BOTH
                                              # placed barges was a tooth tip
                                              # (3-bay local (-0.73,-0.407,2.304)
                                              # = 0.417 m; 2-bay (1.29,-0.38,
                                              # 0.296) = 0.436 m), not the foot.
                                              # Rendered end-on down the rake it
                                              # read as a comb of thin fins in
                                              # front of the mouldings; rendered
                                              # from the street it read as a row
                                              # of bolts on a plate.
                                              #
                                              # ref3 does not draw an applied
                                              # course there. It draws the fringe
                                              # CUT IN the board's lower edge --
                                              # crop the greyscale tight on the
                                              # rake and every curl is part of
                                              # the plank, with the plank's own
                                              # thickness behind it and its face
                                              # oversailing it.
                                              #
                                              # So the teeth now live INSIDE the
                                              # plank's Y span (-VO-.092 ..
                                              # -VO+.010), inset 20 mm from its
                                              # outer face and 34 mm from its
                                              # inner: 48 mm of oak housed in a
                                              # 102 mm board, the board's face
                                              # standing 20 mm over them and
                                              # throwing the shadow a carved
                                              # fringe has. Every clearance in
                                              # the ladder holds at >= 20 mm --
                                              # plank outer 20, plank inner 34,
                                              # web outer 22 (Y_WEB[0] = -VO-.002
                                              # ... measured: -0.302 vs -0.324),
                                              # ogee roll 26 outer / 22 inner --
                                              # and the fringe's plan projection
                                              # past the tile cut falls 108 -> 72
                                              # mm. Nothing changes depth: the
                                              # teeth hang exactly as far below
                                              # the board as before.
Y_CAP = (-VO - .118, -VO - .044)              # THE DENTIL LADDER's layer, and
                                              # before it the cap BEAD's -- 74 mm
                                              # in Y, not 216,
                                              # and it rides CAP_DROP below the
                                              # board's top edge instead of
                                              # straddling it, so it reads as a
                                              # moulding on the face and never
                                              # as a shelf on the roof. CAP_DROP
                                              # came down with the board (see BW):
                                              # at 0.052 on a 0.335 plank the bead
                                              # ran 21 mm into the upper ogee step
                                              # in v, and two mouldings sharing a
                                              # strip of face is how a moulding
                                              # stops reading as one. At 0.035
                                              # with a 100 mm bead there is 20 mm
                                              # of clear face between them.
Y_TAIL = (-VO - .146, -VO - .065)             # the scroll at the foot. Its INNER
                                              # face used to be written -VO-.030,
                                              # the same plane as the cap bead's,
                                              # and the two overlap in plan over
                                              # the whole scroll: 63 cm2 of
                                              # coincident oak measured at the
                                              # right rake's foot. It is 21 mm
                                              # off the bead now and 19 mm off
                                              # the roll's inner face.
                                              #
                                              # AND HOW MUCH OF THE PIECE'S
                                              # PROUD IS THE SCROLL'S. Measured
                                              # local y_min against the roof's
                                              # verge cut at y = -0.300:
                                              #   board face      0.092  (a board
                                              #                          thickness)
                                              #   + ogee roll     0.128  (the
                                              #                          moulding
                                              #                          that runs
                                              #                          the WHOLE
                                              #                          rake)
                                              #   + this scroll   0.146
                                              # so of the 0.146 that stands
                                              # outboard of the verge cut, 0.128
                                              # is board and its running
                                              # moulding, and 0.018 -- 12 % -- is
                                              # the scroll. It was 0.150; the
                                              # ladder below it, not the scroll,
                                              # is what sets this number, and the
                                              # scroll cannot come further in
                                              # without landing on the roll's own
                                              # plane (they overlap in plan over
                                              # the whole boss).
Y_WEB = (-VO - .002, .030)                    # dark soffit behind the board: 12
                                              # mm into the board's inner face
Y_SLAB = (-VO + .042, .205)                   # verge slab: inboard of the web's
                                              # outer face, and short of y=T so
                                              # finish() never clamps it flat
RAKE_LAP = 0.024        # the right rake is set this far inboard of the left one,
                        # so no layer of one rake is ever at the same depth as
                        # the same layer of the other. With the apex now MITRED
                        # (see below) the two never overlap in plan either, but
                        # the offset stays: it makes the two sides read as two
                        # separately fitted boards rather than one folded sheet.

# ===========================================================================
# THE TWO RAKE BOARDS MEET IN A JOINT. THEY USED TO JUST CROSS.
# ---------------------------------------------------------------------------
# Shanee, on the assembled inn: "The top of SM_Gable_Barge_3bay.001 also has
# weird issues with how the beams meet."
#
# They did. Every band of each rake -- board, ogee roll, step, cap, soffit web,
# and the slab under them -- was run 0.11 PAST the apex, so each one crossed its
# opposite number and came out through the OTHER slope of the roof. Round the
# finial that is a starburst of loose plank ends, and it is the first thing you
# see at the top of the hero gable.
#
# A real bargeboard is cut on the ridge. Every band is now MITRED on the VERTICAL
# PLANE through the ridge line, which in rake-local (u, v) is the single straight
# cut u*cos P - v*sin P = W/2 - inset whatever the band's height, and the joint is
# covered by ONE apex block: a king-post head standing proud of both boards with
# a moulded saddle over it, carrying the finial. That is ref3's apex exactly --
# crop ref3:bargeboard and look at the top: two boards dying into an upright
# block with a cap, not an X.
#
# Because the cut is VERTICAL, a band that stands further out of the roof plane
# reaches further up the ridge line (z = ZA + v/cos P - inset*tan P), so the
# insets are staggered to keep every head inside the solid that covers it. And
# the two rakes never use the SAME inset: two mitre faces on one plane would be
# the worst z-fight in the piece, and check_zfight also scores a symmetric pair
# against itself, so left and right differ by ~26 mm everywhere.
# ===========================================================================
# THE APEX BLOCK MUST LAND ON THE BOARDS. IT USED TO HANG OFF THEM.
# ---------------------------------------------------------------------------
# Shanee: "the gable also still has strange floating beam at the top that clips
# geometry etc."  Measured, on SM_Gable_Barge_3bay dropped on SM_Gable_End_3bay_A
# at the same origin, which is how the assembler always places them:
#
#   * the apex post ran ZA-0.720 .. ZA+0.150 -- 0.870 m of 0.34 m square oak
#     hanging DOWN the middle of the gable, and a ray cast straight down from
#     the centre of its bottom face hit nothing at all within 8 m. It ended in
#     mid air, and its blunt foot was silhouetted against the tympanum;
#   * it hid 75 % of the 3-bay's visible tympanum and 100 % of every 2-bay's --
#     which is the "open dark void with a lone diamond in it": the king post,
#     both apex struts and the top of the arch were all BEHIND that slab.
#
# WHY IT WAS THAT LONG. Every band was mitred on the ridge plane with a POSITIVE
# inset, so the left board stopped at x = -0.060 and the right started at
# x = +0.088: a 0.148 m vertical SLOT straight through the verge from the apex
# down to the boards' feet. The post existed to plug that slot, so it had to be
# as long as the slot -- and the slot runs the full depth of a 0.46 m board, so
# the post had to reach 0.72 m below the apex, i.e. well below the point where
# the two boards' lower edges cross the centre line (ZA - 0.747). Under that
# line there is no board for it to stand on, only air.
#
# WHAT IT IS NOW: the boards LAP. The insets go NEGATIVE, so each band runs a
# couple of centimetres past the ridge plane and its mitre face is buried inside
# the opposite board instead of facing an open gap. The two rakes are RAKE_LAP
# apart in Y, so the lapped faces are 24 mm off each other and nothing is
# coplanar. With no slot left to plug, the block becomes what ref3 actually
# draws: a SHORT king-post head, ZA-0.290 .. ZA+0.128, standing on the two
# boards with a moulded stop at its foot and the saddle over its head. Its
# bottom edge lies 0.30-0.50 m ABOVE the boards' lower edge across its whole
# width, so every millimetre of it is bearing on timber.
#
# A vertical mitre throws a head UP the ridge line (z = ZA + v/cos P - inset*
# tan P), and a lapping inset throws it higher still, so the two bands that
# reach highest -- the plank and the kerb lip -- also take a square HEAD CUT
# (see _head) under the saddle. That is how a bargeboard is really finished:
# mitred on the ridge, cut off square under the apex block.
AP_PLANK = (0.004, -0.022)  # (left, right) inset of the mitre from the ridge
                            # plane, in world x. The lap is DELIBERATELY one
                            # sided: the left rake is the one in front (the
                            # right is set RAKE_LAP inboard), so the LEFT board
                            # is stopped on the ridge and the RIGHT runs 22 mm
                            # past BEHIND it. Run both past and the front board
                            # ends in a square 24 mm step standing over the back
                            # one, which is a new loose plank end at the apex --
                            # exactly what this whole joint is meant to stop.
AP_LIP = (0.002, -0.034)    # the kerb lip laps the same way (36 mm), so the
                            # closing edge of the roof is continuous over the
                            # ridge instead of stopping 0.23 m short on both.
AP_WEB = (0.008, 0.032)     # dark soffit web: buried deepest, behind everything.
                            # It lies wholly INSIDE the plank's own depth, so its
                            # 24 mm apex slot never sees daylight and it is left
                            # alone -- the one band that gains nothing by lapping.
AP_ROLL = (-0.008, -0.050)  # ogee + step rolls: lapped the same way, so the
                            # two-step moulding runs unbroken round the apex.
                            # Their heads land 0.05-0.18 m below ZA, in the post.
                            # The LEFT inset went from +0.006 to -0.008 on a
                            # measurement: at +0.006 the rolls' mitre plane stood
                            # 2 mm off the left plank's at +0.004 and 4 mm off the
                            # left kerb lip's at +0.002, all three overlapping in
                            # plan, and ZFIGHT_TOL=0.0005 scored 102 cm2 of
                            # oak_mid on oak_dark there -- the whole of what this
                            # family had left at that tolerance on the barge.
                            # Lapped 8 mm PAST the ridge instead it is 14 mm off
                            # the plank and 14 mm off the lip. The RIGHT inset
                            # moved the same way and for the same reason: its
                            # mitre stood 6 mm off the right plank's at -0.022
                            # with 70 mm of y overlap between them, which is the
                            # pair check_zfight was actually naming. Both heads
                            # are still buried in the apex post (|x| <= 0.16).
AP_STEP = (-0.026, -0.068)  # ... and the UPPER step of the ogee now takes its own
                            # inset instead of sharing AP_ROLL. It shared it for
                            # rounds, and that put the two rolls' mitre faces on
                            # ONE plane -- 0 mm apart, not 2 or 14 -- overlapping
                            # by their 66 mm of common Y wherever their v spans
                            # crossed. It was 14.5 cm2 and check_zfight never
                            # named it, because AREA_MIN is 15: measured (probe:
                            # the two +X faces at x = 0.0076, y -0.387 and -0.367,
                            # areas 103.7 and 96.3 cm2, overlapping over 66 x 22
                            # mm). Tightening the two rolls onto the board's lower
                            # edge moved their z extents 33 mm closer and the same
                            # coincidence came out at 21.8 cm2 -- over the floor,
                            # and reported as 43 cm2 on each barge. Shrinking the
                            # overlap back under 15 cm2 would only hide it, so the
                            # planes are separated instead: 18 mm off AP_ROLL on
                            # both hands, 30/46 mm off the plank's and 28/34 mm
                            # off the kerb lip's, and both heads still buried in
                            # the apex post (x = +0.026 and -0.068 against
                            # |x| <= 0.160).
                            # For the record on reachability, since area is not
                            # the point: the overlap sat in y [-0.412, -0.346],
                            # wholly inside the post's own y span (-0.414 ..
                            # -0.262), so it was behind the king-post head and
                            # nothing could see it flicker. It is fixed at its
                            # cause anyway -- it costs two numbers and no
                            # triangles, and a coincidence that only fails to
                            # report because it is 0.5 cm2 under a floor is not a
                            # coincidence that has been dealt with.
# Square head cuts, as world z above ZA, (left, right). A lapping vertical mitre
# throws a band's top corner up the ridge line -- the plank's would reach
# ZA + 0.189 and the lip's ZA + 0.244, both of them through the saddle -- so the
# two are cut off square underneath it. Left and right differ by 14 mm so the two
# flat tops, which do overlap in the lap zone, are never coplanar.
AP_HEAD_PLANK = (0.058, 0.044)
AP_HEAD_LIP = (0.030, 0.016)
AP_CAPU = (0.020, -0.012)   # how far past the apex station the dentil ladder's
                            # own centreline is SAMPLED. It was the cap bead's
                            # square stop, back when this layer carried a
                            # continuous band that a vertical mitre would have
                            # thrown a 0.15 m head up the ridge line with. A row
                            # of separate blocks has no head to throw, so it is
                            # cut on the post's flank instead (DENT_BURY) and
                            # this number only has to reach past that cut --
                            # which it does by 0.18 m of rake.
AP_SLAB = (0.22, 0.30)      # verge slab, measured ALONG the rake: it is a box,
                            # so it cannot take an angled cut, and it is under
                            # the roof field and behind the post either way.
AP_FRINGE = 0.10            # the pendant fringe runs on until its last tooth is
                            # this close to the ridge plane in x -- i.e. the
                            # scallops die INTO the post's flank (the post stands
                            # 37 mm proud of them), instead of stopping short and
                            # leaving a bald patch either side of the apex.
# THE APEX BLOCK. Short, and bearing on the boards over its whole width.
# Its foot is ZA-0.290; the two lapped rake boards' faces cover the centre line
# from ZA-0.578 up and |x| = POST_W/2 from ZA-0.796 up, so the block's bottom
# edge lies 0.29 m (at its corners: 0.51 m) above the nearest open air. Its back
# is 14 mm clear of the plank's own back plane, so it no longer punches out
# behind the boards either -- that was the other half of "clips geometry".
# POST_Y / SAD_Y pulled in 68 mm with the rest of the outboard ladder (see the
# note by Y_TAIL): the saddle used to be the single proudest thing in the family
# at y = -0.518, i.e. 0.218 m outboard of the roof it caps.
POST_W, POST_Y = 0.320, (-0.414, -0.262)     # king-post head at the apex
POST_Z = (-0.290, 0.128)                     # relative to ZA
SAD_W, SAD_Y = 0.404, (-0.438, -0.150)       # the moulded saddle over the joint.
                                             # 24 mm proud of the post rather
                                             # than 32: at -0.446 it TIED with
                                             # the foot scroll for the piece's
                                             # outermost plane, so pulling the
                                             # scroll in would have moved the
                                             # measured y_min by nothing at all.
SAD_Z = (0.002, 0.152)                       # relative to ZA

WIN = S.OPENINGS["win_attic"]          # 0.52 x 0.58, the gable/attic light
SILL_Z = {2: 0.98, 3: 1.34}            # opening sill height above the gable base

# ===========================================================================
# THE WALL OWNS THE SURROUND. THE INSERT OWNS THE JOINERY.
# ---------------------------------------------------------------------------
# Round 15's audit measured SM_Gable_WinFrame against the gable ends it is
# always dropped into -- they share an origin, so the numbers are exact -- and
# found FOUR collisions, all of them one fault: the insert had grown a surround
# that laps onto the wall, and the wall it laps onto is a half-timber TRUSS with
# its own members in that exact band.
#
#   * the insert's cill lapped the gable's mid rail: 93 mm of vertical overlap
#     over the cill's full 0.725 m width on the 3-bay, 96 mm on the 2-bays,
#     with their front faces only 69 mm apart;
#   * its label-mould lintel drove straight through the apex arch on every
#     2-bay variant: lintel z 1.540-1.620 against arch z 1.545-1.864;
#   * its two cill corbels hung 48 mm BELOW the mid rail's underside and ended
#     square in open air -- the third time this family has been reported for a
#     member that stops in mid air;
#   * and the whole insert measured 0.819 x 1.044 against a 0.520 x 0.580 hole.
#
# That is the fault the windows family was held to in the same round, and it
# takes the same answer:
#
#     wall   -- the projecting cill and its brackets, the label mould and its
#               crest, the reveal, its lining and its dark backing. A bare gable
#               with no insert in it still needs every one of them.
#     insert -- frame, glass, leading, and the bead that holds the pane in.
#
# CONSEQUENCE, and it is a HARD BOUND checked by the piece's own seams: nothing
# in SM_Gable_WinFrame leaves x in [-IW/2, IW/2], z in [0, IH]. No cill, no
# lintel, no corbels, no crest -- they are the wall's, and where the insert drew
# one it was drawing the wall's member a second time, a few centimetres away
# from it and through whatever else the truss had at that height.
IW = WIN["w"] - 2 * S.INSERT_CLEAR     # 0.480 -- the insert envelope in x
IH = WIN["h"] - 2 * S.INSERT_CLEAR     # 0.540 -- ... and in z
# ===========================================================================

# ===========================================================================
# EVERY MEMBER LANDS ON SOMETHING. NOTHING STOPS IN MID-AIR.
# ---------------------------------------------------------------------------
# Shanee, on the assembled inn: "SM_Gable_End_3bay_A.001 has some strange side
# pieces just under the middle half vertically that I'm not sure what they're
# doing." They were the ENDS OF THE MID RAIL. The rail was laid out with wall
# extents (-W/2+0.12 .. +W/2-0.12), which is right for a rectangular wall panel
# and wrong for a triangle: at its own height the gable is only ~2/3 as wide as
# its base, so 0.9 m of beam shot out past each rake line and stopped, blunt, in
# open air -- and out there it is not even inside the building, that is where the
# roof slope comes down over the verge.
#
# A gable's horizontal timbers are HOUSED INTO THE PRINCIPAL RAFTERS: ref3 draws
# every rail dying into the raking timber. So every horizontal member is now cut
# on the rake (hbeam(..., housed=HOUSE)) and buried in the rake plate, and the
# only full-width timber left is the bottom tie beam, which is the wall plate the
# whole gable stands on.
#
# HOUSE is measured in x, not perpendicular: _clip() offsets its cut line in
# (x + z*W/2ZA), so `inset` moves the line SINP * inset perpendicular to the
# rake. HOUSE = 0.13 x-units = 0.102 m perpendicular, which leaves the cut face
# 0.138 m deep inside the RAKE_W-wide plate -- well past the 12 mm the layer
# rules want, and far enough in that no wobble can push the end back into
# daylight.
# ===========================================================================
RAKE_W = 0.240          # face width of the gable's own rake plate, perpendicular
                        # to the rake line -- on the WIDE gable. See rake_w().
RAKE_W_MIN = 0.205      # ... and on the narrow one. The plate closes over the
                        # apex RAKE_W/cos P below the peak whatever the gable is
                        # worth: 0.390 m of a 3-bay's 3.84 m rise is 10% of it,
                        # but 0.390 m of a 2-bay's 2.56 m is 15%, and it is
                        # taken out of the one part of the triangle the eye
                        # actually goes to. Slimming the narrow gable's rafter
                        # by 35 mm lifts the closing line 57 mm and gives back
                        # 44 mm of visible face at EVERY height on EACH side --
                        # a fifth of the room the apex arch has to live in.
HOUSE = 0.130           # how far (in x) a horizontal member is cut back from the
                        # rake line, so its end dies inside the rake plate
TENON = 0.024           # how far a member that DIES INTO another is buried in
                        # it. Over the 12 mm the layer rules want (so a shoulder
                        # can never open under wobble(.007)) and under the depth
                        # of anything it is housed in, so no tenon comes out the
                        # far side. Every split member in _face uses it.
BOARD_LAP = 0.050       # ... and how far a BOARD is housed on the member that
                        # carries it. Deeper than TENON because a board is thin
                        # and clipped, so a shallow housing on one does not read
                        # -- and because the member over it stands 24-32 mm proud
                        # of it, so the lap is never in daylight either way.
RAKE_HOUSE = 0.055      # ... and how far (in z) a STUD is cut back from the rake
                        # line. It was 0.010, i.e. the stud ran to the OUTER face
                        # of the rake plate -- the roof plane -- with 10 mm of
                        # margin against 7 mm of wobble. The plate is 0.31-0.39 m
                        # deep measured in z, so 0.055 is still well inside it.

# ===========================================================================
# THE APEX ARCH IS FITTED TO THE TRIANGLE IT SITS IN, NOT TO A CONSTANT.
# ---------------------------------------------------------------------------
# Measured on the 2-bay ends: "the apex arch degenerates -- aw clamps to 0.085,
# span +/-0.28 m, crown z 2.177 vs rake plates closing at 2.170 and standing
# 30 mm proud, so it is buried; only stub ends show."  Both halves of that are
# the same mistake. The arc was fitted by a rule written off the 3-BAY numbers
# --  aw = .215 * x_rk / .985, and .985 is literally the 3-bay's own x_rk at
# its own springing -- and then CLAMPED when the 2-bay came out smaller. A
# clamp is not a fit: it is the code saying "this does not work here" and
# drawing it anyway.
#
# THE GEOMETRY THAT ACTUALLY DECIDES WHETHER AN APEX ARCH READS. Two lines
# bound the visible apex, and both come off the rake PLATE, not the rake line:
#
#   z_close = ZA - rake_w/cos P            2.235 on a 2-bay, 3.450 on a 3-bay
#       the height where the two plates' inner edges cross on the centre line.
#       The plates stand 30 mm proud of the arch (Y_RAKE vs Y_ARCH), so
#       anything drawn above z_close is simply covered over. The old 2-bay
#       crown at 2.177 was 7 mm THE WRONG SIDE of that line.
#
#   x_in(z) = (ZA - z)/tan P - rake_w/sin P        the visible face's own edge
#       |x| beyond it is inside the plate. On a 2-bay that plate eats 0.305 m
#       of x on EACH side -- of a triangle only 0.39 m wide at the old
#       springing. There was no apex left to put an arch in.
#
# An arc z = z_cr - rise*(x/x_sp)^2 shows only where |x| < x_in(z), and because
# the arc is SHALLOW and the triangle is STEEP that test, not the span, is what
# kills a badly placed arc. Three consequences, all measured, all now built in:
#
#   * THE SPRINGING WANTS TO BE LOW. Dropping it widens the span AND lowers the
#     crown (z_cr = ZA - (1 - ARCH_RISE/tan P)(ZA - z_sp) - ...), so it buys
#     clearance at z_close and visible width at x_in in the same move.
#   * THE FEET BELONG ON THE PLATE'S INNER EDGE plus a bite, not on the rake
#     LINE less an inset. Setting a foot back from the rake line buries the
#     first 0.15 m of arc before it has started; springing off x_in + a 90 mm
#     bite houses the end cut and shows the rest.
#   * A FLATTER ARC IS A MORE VISIBLE ARC, which is a happy accident: ref3
#     draws a broad shallow arc anyway, and a shallow one climbs away from the
#     closing plates more slowly than a steep one.
#
# Fitted this way the arc measures (visible half-width / rise / band depth):
#     3-bay  0.729 / 0.275 / 0.219      was 0.69 / 0.318 / 0.215 (at its clamp)
#     2-bay  0.471 / 0.200 / 0.159      was 0.10 / 0.112 / 0.085 -- two stubs
# -- 23.5% of the 2-bay's width against 24.3% of the 3-bay's, i.e. the same arch
# on both, which is the point: one gable should not read as a different building
# from the one beside it.
# ===========================================================================
ARCH_RISE = 0.34        # crown rise as a fraction of the half span. BROAD and
                        # SHALLOW is what ref3 draws under every apex; 1.0 would
                        # be a pointed arch and read as a second roof inside the
                        # gable.
ARCH_BITE = 0.090       # how far PERPENDICULAR each foot is housed inside the
                        # rake plate, so its square end cut is covered. The
                        # plate stands 30 mm proud of the arch and is 0.240 wide
                        # on a 3-bay / 0.205 on a 2-bay, so this leaves 0.150 /
                        # 0.115 m of plate outboard of the cut: the end cannot
                        # work its way into daylight under wobble(.007), and
                        # nothing of the arc is buried needlessly.
ARCH_DEEP = 0.270       # band depth at the feet as a fraction of the half span
ARCH_W = (0.118, 0.225)  # ... held between "still reads as one timber" and
                        # "still reads as an arc". NOT a fallback: the fit below
                        # is chosen so neither end of this range is reached.
ARCH_HEAD = 0.110       # air wanted between the top of the arc and z_close. The
                        # 2-bay used to have MINUS 7 mm.
ARCH_MIN = 0.45         # visible half-width under which springing off the top
                        # rail is not worth doing and the truss is rearranged
                        # (see _apex_fit). Sprung off its own top rail the 3-bay
                        # measures 0.729 and keeps the rail; the 2-bay measures
                        # 0.116 -- and its crown lands at 2.184 against a closing
                        # line of 2.227, so it fails on head room too -- and it
                        # takes the collar.
RAIL_H = 0.170          # depth of the gable's top rail
COLLAR_H = 0.155        # ... and of the collar beam that replaces it when the
                        # arc has to spring below that rail

# Face layering. Plaster panels sit back, timbers stand proud of Y=0, and every
# plane is 12 mm or more off every other plane it can overlap (see the note
# above). The old table had Y_SKIN's back, Y_CORE's front and Y_BRACE's back ALL
# on y=0.085: three coplanar layers over the whole gable, which was 87 % of this
# family's measured z-fighting.
Y_CORE = (0.150, T)          # ONE solid backing triangle, inner face on y=T
Y_SKIN = (0.035, 0.164)      # plaster infill, buried 14 mm into the core
SKIN_GAP = 0.014             # each panel pulled in this far at every x joint,
                             # so no two panels share a side plane. The joints
                             # land under the timbers, and a slightly recessed
                             # panel edge is what the references show anyway.
# Timber levels. Members that cross each other must not share a plane, so the
# frame is split into four depths -- which also gives the hand-hewn variation in
# timber thickness the brief asks for (16-56 mm proud, PROUD_MAX is 160).
Y_HORIZ = (-0.056, 0.108)    # tie beam, mid rail, upper rail, dentil course
Y_STUD = (-0.032, 0.052)     # studs + king post
Y_RAKE = (-0.044, 0.136)     # rake plates
Y_BRACE = (-0.020, 0.082)    # curved braces
Y_BOARD = (0.010, 0.076)     # tympanum boarding
Y_LEDGE = (-0.134, 0.070)    # THE WINDOW SURROUND: the projecting cill, its two
                             # brackets, and the label mould over the head. It is
                             # the proudest band on the gable face -- 78 mm in
                             # front of the mid rail it is housed into, 102 mm in
                             # front of the jamb posts its ends die in, and 18 mm
                             # clear of the stud plane's own back face -- and it
                             # is the wall's, not the insert's. The insert is
                             # bounded to the hole (see the note by IW/IH), so
                             # nothing of it reaches this band at all.
Y_DENT = (-0.074, 0.070)     # pendant dentil course under the upper rail. It is
                             # now HOUSED 24 mm into the rail's lower edge (it
                             # used to hang 32 mm clear of it, a row of teeth
                             # floating on the plaster), so it must not share the
                             # rail's front plane any more: 18 mm proud of it,
                             # 42 mm off the stud plane it also crosses.
Y_LOZ = (-0.008, 0.058)      # applied lozenge motif (variant B). Bites 23 mm
                             # into the plaster skin / 48 mm into the tympanum
                             # boarding, so it is carried by the panel behind it.
Y_LINER = (0.020, 0.176)     # window reveal lining, and it now runs the WHOLE
                             # depth of the reveal, from 15 mm in front of the
                             # plaster face right back to the core. It used to
                             # start at 0.094 and leave the reveal's outer 60 mm
                             # as bare plaster return, which is what put a bright
                             # cream halo in the 20 mm shadow gap all round the
                             # insert -- the gap spec leaves round every insert
                             # has to read as SHADOW, never as daylight. Still
                             # clear of every plane it crosses: 15 mm off the
                             # plaster skin's face, 32 mm off the stud's back,
                             # 50 mm off the surround's.
Y_PANE = (0.146, 0.192)      # dark attic pane, standing at the very BACK of the
                             # reveal, 4 mm proud of the core. Moved back 16 mm
                             # in round 15 to buy the insert's glass its air:
                             # SM_Gable_WinFrame's pane BACK lands at y = 0.121,
                             # so there is 25 mm between the two sheets and this
                             # piece's wobble (7 mm) plus the insert's (2.2 mm)
                             # cannot close it. At 0.132 it was 11 mm and they
                             # could. Its back was also 2 mm off the plaster
                             # skin's own back plane, which is a coincidence
                             # waiting to be found; it is 28 mm now.
Y_ARCH = (-0.014, 0.094)     # THE APEX ARCH -- the broad shallow arc ref3 draws
                             # under every gable apex, and since assemble_inn.py
                             # stopped laying collar ties across the gables it is
                             # this piece's job to carry it. It crosses the rake
                             # plates at its feet (18 mm behind their face, so
                             # they cover its ends), the tympanum boarding behind
                             # it and the king post in front of it, and it is
                             # 12 mm or more off every one of those planes.
Y_CUSP = (-0.052, 0.064)     # cusps on the apex arch's soffit. They are CARRIED
                             # by the arch, so they bite 30 mm up into it and
                             # stand 38 mm proud of its face; behind them is the
                             # plaster skin, 29 mm further in again, and the
                             # window jambs they can pass are 20 mm back. Used
                             # where the collar leaves no rail to hang a tooth
                             # course from -- see _arc_cusps().
Y_STRUT = (-0.076, 0.030)    # the two apex struts that stand on the arch's crown
                             # -- or on the collar, where there is one -- and die
                             # into the rakes: ref3's apex truss. They cross the
                             # king post, the boarding, the rake plates and (on
                             # the collar arrangement) the collar itself, so they
                             # take their own depth in front of ALL of those: 20
                             # mm proud of the collar, 32 mm proud of the rake
                             # plate, 44 mm proud of the king post. It was -0.062,
                             # which is 6 mm off Y_HORIZ's front face -- fine
                             # while the struts stood on an arch, a z-fight the
                             # moment they stand on a beam.
PURL_SH = 0.030              # the purlin's shoulder, in y: where its full section
                             # stops and the diminished nose goes on through the
                             # rake plate. Inside the plate (-0.044 .. 0.136) by
                             # 74 mm, so the shoulder is never in daylight.
Y_PURL = (-0.142, 0.196)     # purlin ends: they run right THROUGH the wall, from
                             # 46 mm inside the backing triangle out past the
                             # rake plate. See _purlin() for why. The inner end
                             # was at 0.170, which is 6 mm off the plaster skin's
                             # own back plane at Y_SKIN[1] -- two +Y faces, 196
                             # cm2 of overlap, and wobble(.007) to close them.


# ------------------------------------------------------- material workaround --
class _Fix:
    """Proxy round `Part` that repaints every face a primitive actually created.

    WHY: the shared toolkit's `Part._emit` paints `fs | bevel_result["faces"]`,
    but `bmesh.ops.bevel` REBUILDS the primitive's original faces -- the six big
    flat ones you actually look at on a box -- and does not return them. They are
    dropped by the `f.is_valid` filter, so they keep material slot 0 and a blank
    vertex colour. Measured on a fresh Part: a beveled box paints 20 of its 26
    faces and leaks 6 to slot 0.

    The visible result in this family was that EVERY beveled timber on a gable
    end -- tie beam, rails, studs, braces, rake plates, dentils, purlin stubs --
    rendered as `plaster_dim`, because that is the first material a gable end
    registers. The whole half-timber truss read as one flat sheet of cream.

    The bug is in kit/util.py, which a piece module must not edit, so repaint
    here. When the toolkit is fixed this becomes a no-op that only re-rolls the
    per-primitive tint.
    """
    _WRAP = ("box", "prism", "cyl", "lathe", "plate", "beam", "blob", "quad")

    def __init__(self, part):
        self.__dict__["_part"] = part

    def __getattr__(self, name):
        attr = getattr(self._part, name)
        if name not in self._WRAP:
            return attr

        def call(*a, **kw):
            p = self._part
            before = set(p.bm.faces)
            res = attr(*a, **kw)
            mat = kw.get("mat") or next((x for x in a if isinstance(x, str)), None)
            if mat:
                new = [f for f in p.bm.faces if f not in before]
                if new:
                    p._paint(new, mat, kw.get("tint", 0.05), kw.get("shade", 1.0))
            return res
        return call


# --------------------------------------------------------------- geometry ----
def apex_z(bays):
    return TANP * (bays * G) / 2


def _rake_z(x, W, ZA):
    """Height of the rake line above the gable base at a given |x|."""
    return ZA * (1.0 - 2.0 * abs(x) / W)


def _on_face(cx, cz, half, W, ZA, clear=0.05):
    """True if a square motif of half-diagonal `half` centred at (cx, cz) sits
    wholly on the VISIBLE gable face -- inboard of the rake plate's inner edge,
    not half-buried under it and not hanging over the rake into the roof. Used to
    guard applied ornament, which has nothing structural holding it up and so
    must never be placed where the panel behind it has run out."""
    return abs(cx) + half <= _face_x(cz + half, W, ZA) - clear


# How far the bargeboard hangs DOWN over the gable face, measured in z on the
# centre line: the board's own lower edge plus its pendant fringe, taken off the
# rake line and divided by cos P to turn a perpendicular offset into a height.
# = -(0.142 - 0.038 - 0.335 - 0.130)/cos P = -0.586 m (was -0.895, on a
# board half again as deep -- see the note by BW).
VERGE_DROP = (VERGE_LAP - LIP_DROP - BW - DAG) / COSP


def _verge_z(x, W, ZA):
    """Height at |x| below which the gable face is clear of the bargeboard.

    SM_Gable_Barge_Nbay is always dropped on this piece at the same origin, and
    it is a 0.335 m plank with a 0.130 m fringe under it: it covers a band
    0.586 m deep (in z, VERGE_DROP) inside the rake all the way round. Structure may run up behind
    that -- a strut dying into a rafter under the verge is what a verge is FOR --
    but APPLIED ORNAMENT put up there is simply invisible, and worse, it is
    invisible ASYMMETRICALLY: on the 3-bay the lozenge row's outer two diamonds
    landed 0.10 m behind the fringe and the middle one did not, which is exactly
    Shanee's "open dark void with a lone diamond motif floating in it". One
    diamond of a row of three is not a motif, it is the survivor of one."""
    return ZA - TANP * abs(x) + VERGE_DROP


def _seen(cx, cz, half, W, ZA, clear=0.05):
    """_on_face AND out from under the bargeboard. The test point is the motif's
    top OUTER corner, which is the corner the verge line reaches first."""
    return (_on_face(cx, cz, half, W, ZA, clear)
            and cz + half <= _verge_z(abs(cx) + half, W, ZA) - 0.035)


def _dedupe(poly, tol=1e-4):
    out = []
    for q in poly:
        if not out or abs(q[0] - out[-1][0]) > tol or abs(q[1] - out[-1][1]) > tol:
            out.append(q)
    if len(out) > 2 and abs(out[0][0] - out[-1][0]) < tol and abs(out[0][1] - out[-1][1]) < tol:
        out.pop()
    return out


def _clip(poly, W, ZA, inset=0.0):
    """Clip a polygon in (x, z) to the gable triangle, `inset` in from the rakes."""
    k = W / (2.0 * ZA)
    for sgn in (1.0, -1.0):
        n = len(poly)
        if n < 3:
            return []
        out = []
        f = lambda q: k * q[1] + sgn * q[0] - (W / 2.0 - inset)
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            fa, fb = f(a), f(b)
            if fa <= 0:
                out.append(a)
            if (fa > 0) != (fb > 0):
                t = fa / (fa - fb)
                out.append((lerp(a[0], b[0], t), lerp(a[1], b[1], t)))
        poly = _dedupe(out)
    return poly if len(poly) > 2 else []


def _area(poly):
    """Unsigned area of a 2D polygon. Used to throw away a clipped dentil that
    came back as a shard -- a 12-tri solid 1 mm wide is worse than no solid."""
    a = 0.0
    for i, (u, v) in enumerate(poly):
        w, z = poly[(i + 1) % len(poly)]
        a += u * z - w * v
    return abs(a) * 0.5


def _clip_half(poly, f):
    """Clip a polygon to the half plane f(q) <= 0. Same Sutherland-Hodgman walk
    as _clip, but against one arbitrary line -- this is what mitres a rake band
    on the vertical plane through the ridge."""
    n = len(poly)
    if n < 3:
        return []
    out = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        fa, fb = f(a), f(b)
        if fa <= 0.0:
            out.append(a)
        if (fa > 0.0) != (fb > 0.0):
            t = fa / (fa - fb)
            out.append((lerp(a[0], b[0], t), lerp(a[1], b[1], t)))
    out = _dedupe(out)
    return out if len(out) > 2 else []


def _mitre(Wh, inset):
    """The apex cut for a rake band, in RAKE-LOCAL (u, v): the world x of a point
    on the left rake is (u*cos P - v*sin P) - W/2, so cutting at x = -inset is the
    one straight line u*cos P - v*sin P = W/2 - inset. The right rake is the same
    sub-part mirrored in X, so the same function serves both.

    A NEGATIVE inset therefore runs the band PAST the ridge plane, which is how
    the two boards now LAP instead of leaving a slot between them -- see the
    AP_* table."""
    return lambda q: q[0] * COSP - q[1] * SINP - (Wh - inset)


def _head(z_max):
    """Cut a rake band on a HORIZONTAL plane at world height z_max.

    In rake-local (u, v) a point's world height is u*sin P + v*cos P, so `z <=
    z_max` is one straight line and _clip_half takes it exactly like the mitre.
    This is what stops a board's top corner spearing up past the apex block once
    the mitre is allowed to reach the ridge: a real bargeboard's head is cut
    square under the block, not left as a point in the air."""
    return lambda q: q[0] * SINP + q[1] * COSP - z_max


def _foot(z_min):
    """Cut a rake band on a HORIZONTAL plane at world height z_min, keeping what
    is ABOVE it. The mirror of _head(), and the level cut a bargeboard really
    takes where it dies into the eave fascia.

    It is a BACKSTOP, not the shape: LOWSWEEP is what lifts the board's lower
    edge through the flare (see the note by it). This exists so that no amount of
    wobble, no stretch the assembler applies and no future change to the profile
    can put a millimetre of this piece below the eave again without the metric
    saying so."""
    return lambda q: z_min - (q[0] * SINP + q[1] * COSP)


def _panel(p, x0, x1, z0, z1, W, ZA, y, mat, inset=0.0, bevel=0.014, tint=0.05,
           shade=1.0):
    """One plaster/board panel, clipped to the gable triangle."""
    poly = _clip([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], W, ZA, inset)
    if len(poly) < 3:
        return []
    return p.prism(poly, y[1] - y[0], mat, axis='Y', at=(0, (y[0] + y[1]) / 2, 0),
                   bevel=bevel, seg=1, tint=tint, shade=shade)


def _bez(a, b, c, n=8):
    out = []
    for i in range(n):
        t = i / (n - 1.0)
        out.append((lerp(lerp(a[0], b[0], t), lerp(b[0], c[0], t), t),
                    lerp(lerp(a[1], b[1], t), lerp(b[1], c[1], t), t)))
    return out


def _frames(pts):
    """Unit tangent + left normal at every vertex of a polyline."""
    n = len(pts)
    out = []
    for i, (u, v) in enumerate(pts):
        if i == 0:
            tu, tv = pts[1][0] - u, pts[1][1] - v
        elif i == n - 1:
            tu, tv = u - pts[-2][0], v - pts[-2][1]
        else:
            tu, tv = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        m = sqrt(tu * tu + tv * tv) or 1.0
        out.append((tu / m, tv / m, -tv / m, tu / m))
    return out


def _off(pts, off):
    """Offset a polyline along its own left normal. `off` may be a list."""
    fr = _frames(pts)
    out = []
    for i, ((u, v), (_, _, nu, nv)) in enumerate(zip(pts, fr)):
        o = off[i] if isinstance(off, (list, tuple)) else off
        out.append((u + nu * o, v + nv * o))
    return out


def _band_poly(pts, width, dn=None):
    """The outline of a curved timber band: the centreline offset +-width/2 along
    its own normal. Split out of _band because members that have to be CUT ROUND
    a brace -- the close studding, the tympanum boarding -- need the same outline
    to test against, and a stud that dodges a brace drawn from different numbers
    is a stud that dodges the wrong thing.

    `dn` makes the band ASYMMETRIC: `width` is then the offset ABOVE the
    centreline and `dn` the offset BELOW it, both along the same normal. The rake
    board needs that once its lower edge sweeps up through the bell-cast while
    its top edge stays welded to the kerb -- see LOWSWEEP."""
    fr = _frames(pts)
    L, R = [], []
    for i, (u, v) in enumerate(pts):
        _, _, nu, nv = fr[i]
        w = width[i] if isinstance(width, (list, tuple)) else width
        up = w if dn is not None else w / 2
        lo = (dn[i] if isinstance(dn, (list, tuple)) else dn) if dn is not None else w / 2
        L.append((u + nu * up, v + nv * up))
        R.append((u - nu * lo, v - nv * lo))
    return _dedupe(L + R[::-1])


def _strip_band(poly, c, half):
    """The z range a polygon occupies inside the vertical strip |x - c| <= half,
    or None. This is how one member finds out where another crosses it."""
    q = _clip_half(poly, lambda t: (c - half) - t[0])
    if len(q) < 3:
        return None
    q = _clip_half(q, lambda t: t[0] - (c + half))
    if len(q) < 3:
        return None
    return (min(t[1] for t in q), max(t[1] for t in q))


def _band(p, pts, width, mat, y, bevel=0.010, tint=0.05, shade=1.0, axis='Y',
          cut=None, dn=None):
    """Extrude a curved centreline into a timber band. `width` may be a list.
    `cut` is an optional half-plane test (see _clip_half): the band is trimmed to
    f <= 0, which is how a rake band gets its apex mitre. `dn` makes the section
    asymmetric about the centreline -- see _band_poly."""
    poly = _band_poly(pts, width, dn)
    if cut is not None:
        # `cut` may be ONE half-plane test or several: a rake band's head now
        # takes both its ridge mitre and a square head cut (see _head).
        for f in (cut if isinstance(cut, (list, tuple)) else (cut,)):
            poly = _clip_half(poly, f)
            if len(poly) < 3:
                return []
    if len(poly) < 3:
        return []
    return p.prism(poly, y[1] - y[0], mat, axis=axis, at=(0, (y[0] + y[1]) / 2, 0),
                   bevel=bevel, seg=1, tint=tint, shade=shade)


def _cusp_poly(w, d):
    """One pendant dentil of the rake fringe -- hangs in -v. Round-lobed with a
    pinched neck, so the row reads as the carved scallops of ref3 rather than as
    a sawtooth: the gaps between the lobes are what makes it look cut by hand."""
    return [(-w * .30, .030), (-w * .50, -d * .26), (-w * .50, -d * .62),
            (-w * .25, -d * .97), (w * .25, -d * .97), (w * .50, -d * .62),
            (w * .50, -d * .26), (w * .30, .030)]


def _peg_poly(w, h):
    """Ridge-comb peg: a rounded-top upright tab."""
    return [(-w * .5, 0.0), (w * .5, 0.0), (w * .5, h * .62),
            (w * .30, h * .94), (0.0, h), (-w * .30, h * .94), (-w * .5, h * .62)]


# ------------------------------------------------------------- gable ends ----
def _studs(jamb, hw, bays):
    """The stud lines of the LOWER tier, as |x|, jamb first.

    THE GAPS IN THE LOWER MIDDLE PLASTER. Shanee, on SM_Gable_End_3bay_A:
    "strange geometric errors and gaps in the lower middle plaster". They were
    real and they were here. The lower tier used to cut its panels on a
    hand-written list of x stations that included |x| = jamb - 0.02, and the
    only stud anywhere near that line ran in the tier ABOVE it (z_mid .. z_up).
    So each of those two joints opened a SKIN_GAP either side -- a 28 mm slot,
    116 mm deep, straight through the plaster to the dark backing triangle --
    and ran the full 0.97 m height of the tier, one on each side of the middle
    of the gable. Exactly "gaps in the lower middle plaster".

    The fix is structural, not a patch: the panels are now cut FROM this list
    and a stud is drawn on every line in it, so a plaster joint with no timber
    over it cannot exist. The pitch is ref3's -- close studding, verticals at
    roughly 0.6 m, dying into the principal rafters as the triangle narrows."""
    xs = [jamb]
    x = jamb + (0.42 if bays == 2 else 0.40)
    while x < hw - 0.14:
        xs.append(x)
        x += 0.62
    return xs


def _purlin(p, cx, cz, r, w=.145, h=.135, y0=None, shade=.88):
    """One purlin end.

    THE STRANGE BLOCKS. Shanee: "some strange wooden blocks in places which
    might be trying to emulate support beams but just looks like strange
    blocks." He is describing these. They were boxes 0.155 x 0.205 x 0.135 laid
    0.19 perpendicular inboard of the rake line at y = -0.050, i.e. floating
    0.11 m PROUD of the rake plate's own face, overlapping nothing, touching
    nothing, and landing on nothing -- six of them scattered up the two rakes
    plus one at the apex. Read on a bare gable end that is not a purlin, it is
    a block stuck to a triangle.

    A purlin end is a BEAM THROUGH A WALL. So each one now starts 20 mm inside
    the backing triangle, runs out through the plaster skin and through the rake
    plate, and is centred on the rake plate's own centre line so it is visibly
    housed in the principal rafter. Its outer end is cut on a chamfer -- the
    profile is drawn in (y, z) and extruded along X, so that chamfer is a real
    cut face rather than a taper of the whole beam, which is how ref3 stops a
    purlin. Nothing about it is a floating block any more: it comes out of the
    wall, and the rafter it passes through is drawn over it."""
    y0 = Y_PURL[0] if y0 is None else y0
    y1 = Y_PURL[1]
    sh = shade + r.uniform(-.05, .05)
    # THE NOSE IS REDUCED WHERE IT GOES THROUGH THE RAFTER, and that is the
    # joint. A purlin end really is a beam passing through a principal rafter, so
    # neither member can end in the crossing and a full-section beam driven
    # through one is 3.5 litres of oak with nothing cut -- the largest remaining
    # crossing in every variant when the frame was measured. Diminished to a
    # shouldered tenon at PURL_SH (which is inside the rake plate, y -0.044 to
    # +0.136), the body dies against the rafter and only the tenon comes through
    # it: both members now END in the joint, and what shows outside the wall is
    # the stopped, chamfered nose ref3 draws under a verge.
    p.box((cx, (PURL_SH + y1) / 2, cz), (w, y1 - PURL_SH, h), "oak_mid",
          bevel=.010, seg=1, tint=.06, shade=sh * .96)
    hn = h * .74
    prof = [(PURL_SH + .040, -hn / 2), (y0 + .030, -hn / 2),
            (y0, -hn / 2 + .034), (y0, hn / 2 - .038), (y0 + .034, hn / 2),
            (PURL_SH + .040, hn / 2)]
    return p.prism([(a, b + cz) for (a, b) in prof], w * .88, "oak_mid",
                   axis='X', at=(cx, 0, 0), bevel=.010, seg=1, tint=.06,
                   shade=sh)


def rake_w(W):
    """Face width of this gable's rake plate. Scaled with the gable so a narrow
    apex is not simply swallowed by its own rafters -- see RAKE_W_MIN."""
    return clamp(.040 * W, RAKE_W_MIN, RAKE_W)


def _face_x(z, W, ZA):
    """|x| out to which the VISIBLE gable face reaches at height z: the rake
    plate's inner edge. Everything beyond it is inside the plate, which stands
    30 mm proud of the face and therefore covers it. This is the line the apex
    arch used to be fitted without."""
    return _rake_z_x(z, W, ZA) - rake_w(W) / SINP


def _arc_span(W, ZA, z_sp):
    """The arc that springs at z_sp: (half span, band depth at the feet, crown).

    The feet land ARCH_BITE perpendicular INSIDE the rake plate, measured from
    the plate's inner edge -- so the square end cut is covered and the rest of
    the arc is in daylight. The old rule measured the same inset from the rake
    LINE instead, which starts the arc 0.15 m inside the plate and then wonders
    where it went."""
    x_sp = max(0.14, _face_x(z_sp, W, ZA) + ARCH_BITE / SINP)
    aw = clamp(ARCH_DEEP * x_sp, ARCH_W[0], ARCH_W[1])
    return x_sp, aw, z_sp + ARCH_RISE * x_sp


def _arc_z(u, z_sp, z_cr):
    """Height of the arc's centre line at u = x/x_sp. The quadratic Bezier
    _bez((-x_sp, z_sp), (0, 2*z_cr - z_sp), (x_sp, z_sp)) is exactly the
    parabola z = z_cr - (z_cr - z_sp)*u^2, which is what lets everything else
    here -- cusps, king post foot, lozenge row -- be placed on the curve by
    arithmetic instead of by searching the polyline."""
    return z_cr - (z_cr - z_sp) * u * u


def _arc_visible(W, ZA, z_sp, x_sp, aw, z_cr):
    """|x| out to which the arc's SOFFIT still shows in front of the rake
    plates. This is the number that says whether an apex arch reads at all, and
    it is why the 2-bay arch had to be re-fitted rather than merely un-clamped.

    Walked over 40 stations rather than solved: the band's depth varies along
    the curve, so the closed form is only approximate, and an approximate
    closed form that is wrong at the ends is worse than a walk that is right."""
    vis = 0.0
    for i in range(41):
        u = i / 40.0
        x = x_sp * u
        z = _arc_z(u, z_sp, z_cr) - lerp(aw * .70, aw, u) * .5
        if x <= _face_x(z, W, ZA):
            vis = x
    return vis


def _apex_fit(W, ZA, z_h, z_rail_top):
    """Fit the apex truss to the triangle THIS gable actually has.

    Two arrangements, and the gable is measured to decide which it can carry:

    (a) RAIL THEN ARCH -- ref3's 3-bay apex. The top rail sits over the window,
        the arc springs off the principal rafters just above it, and the king
        post and its two struts stand on the crown. Wants a wide triangle above
        the rail: the 3-bay has 0.98 m of half width there and the arc measures
        0.729 m of visible half span.

    (b) ARCH THEN COLLAR -- ref3's arch-braced collar truss, and what a 2-bay
        gable can actually hold. Above the 2-bay's top rail the visible face is
        0.131 m wide and an arc fitted there shows 0.116 m of itself: no arch of
        any size fits up there, which is precisely why the old code clamped one
        and buried it. So the arc springs straight off the rakes over the window
        head, where the triangle is still 0.47 m of visible half width, and THE
        RAIL RIDES UP ONTO ITS CROWN as a collar. The king post and the two
        apex struts then stand on the collar, which is what stops the last
        triangle being the empty one with two stub ends in it.

    Returns the numbers the rest of _face lays itself out against."""
    z_close = ZA - rake_w(W) / COSP
    # THE BAND HAS DEPTH, AND THE SPRINGING IS THE BAND'S CENTRE LINE. At
    # z_rail_top + 0.030 the arc's centre cleared the top rail by 30 mm and its
    # SOFFIT -- half a band lower -- ran 80 mm down through it: measured on the
    # 3-bay, the rail (z 2.36..2.53) and the arc's foot (z 2.45..2.67) shared
    # 2.2 litres of oak with neither member ending in the joint. Two passes: fit
    # once to learn the band depth, then spring aw*0.55 higher so the soffit
    # itself clears. Costs the 3-bay 0.12 m of visible arc (0.729 -> 0.608, still
    # well over ARCH_MIN) and buys an arch that springs off the rafters ABOVE its
    # rail, which is what ref3 draws.
    z_sp = z_rail_top + .030
    x_sp, aw, z_cr = _arc_span(W, ZA, z_sp)
    z_sp = z_rail_top + .030 + aw * .55
    x_sp, aw, z_cr = _arc_span(W, ZA, z_sp)
    vis = _arc_visible(W, ZA, z_sp, x_sp, aw, z_cr)
    if vis >= ARCH_MIN and z_cr + .35 * aw + ARCH_HEAD <= z_close:
        return dict(collar=False, z_sp=z_sp, x_sp=x_sp, aw=aw, z_cr=z_cr,
                    z_close=z_close, vis=vis,
                    z_up=z_rail_top - RAIL_H, z_up_t=z_rail_top)
    # (b). The springing clears the window head by 60 mm; the feet are out at
    # the rakes, a good half metre either side of the window, so there is
    # nothing up there for them to foul.
    z_sp = z_h + .060
    x_sp, aw, z_cr = _arc_span(W, ZA, z_sp)
    vis = _arc_visible(W, ZA, z_sp, x_sp, aw, z_cr)
    # The collar lands ON the crown, biting 20 mm down into the band so the two
    # are jointed rather than stacked, and its ends are housed in the rafters
    # like every other horizontal member here.
    z_up = z_cr + .35 * aw - .020
    return dict(collar=True, z_sp=z_sp, x_sp=x_sp, aw=aw, z_cr=z_cr,
                z_close=z_close, vis=vis, z_up=z_up, z_up_t=z_up + COLLAR_H)


def _arc_cusps(p, W, ZA, z_sp, x_sp, aw, z_cr, r):
    """Cusping hung off the apex arch's soffit -- the foliated arch head ref3
    cuts into its curved timbers, and the same lobe profile as the bargeboard's
    pendant fringe so the two rhyme.

    It is also WHERE THE 2-BAY GABLE'S TOOTH MOTIF GOES. With the collar riding
    on the arc's crown there is no rail left underneath to hang a dentil course
    from, and hanging one on the window head instead would put a row of small
    loose blocks 50 mm over the glass -- which is the exact thing this family
    has already been reported for twice. The row is pitched at 0.13 like a
    dentil course rather than divided into the span, and each lobe is drawn only
    where it is WHOLLY in front of the rake plate -- so it dies out on its own
    where the plate takes over, five lobes on a 2-bay, and there are no
    half-buried teeth anywhere in it."""
    lw, ld, pitch = .078, .058, .130
    for k in range(-6, 7):
        x = k * pitch
        u = abs(x) / x_sp
        if u > .96:
            continue        # NOT break: k walks from -6, so the first station
                            # is the far one and a break here drew nothing
        z = _arc_z(u, z_sp, z_cr) - lerp(aw * .70, aw, u) * .5
        # tested at the lobe's TOP corner, where the plate edge is tightest --
        # the soffit falls away from the crown faster than the plate edge does,
        # which is what stops the row before it reaches the springing.
        if abs(x) + lw * .5 > _face_x(z + .040, W, ZA) - .012:
            continue
        poly = [(x + a, z + b + .015) for (a, b) in _cusp_poly(lw, ld)]
        p.prism(poly, Y_CUSP[1] - Y_CUSP[0], "oak_dark", axis='Y',
                at=(0, sum(Y_CUSP) / 2, 0), bevel=.006, seg=1, tint=.05,
                shade=.88 + r.uniform(-.05, .05))


def _face(p, W, ZA, var, seed):
    """Half-timber truss on the gable triangle. Everything is expressed as a
    fraction of ZA so the 2-bay and 3-bay gables read as the same building.

    Layout, read straight off ref3 (crop ref3:gable and look):
      tie beam / CLOSE STUDDING with a boarded panel in the middle cell /
      mid rail / the window between two full-height posts with a big curved
      brace arching over it each side / THE APEX ARCH -- and then whichever of
      ref3's two apex trusses this gable's triangle can carry (see _apex_fit):
      a 3-bay gets rail, arch, king post and struts under a boarded tympanum;
      a 2-bay gets the arch springing straight off the rafters with the rail
      riding on its crown as a collar, cusping on the arch's soffit where the
      3-bay's tooth course goes, and the king post standing on the collar."""
    r = rng(f"gable/{p.name}/{seed}")
    ow, oh = WIN["w"], WIN["h"]
    bays = int(round(W / G))
    z_s = SILL_Z[bays]
    z_h = z_s + oh
    z_tie = 0.21                                # bottom tie beam top edge
    z_mid = z_s - 0.20                          # mid rail bottom edge
    z_mid_t = z_s - 0.02                        # mid rail top edge
    hw = W / 2.0
    jamb = ow / 2 + 0.085                       # window jamb centre |x|
    xs = _studs(jamb, hw, bays)                 # lower-tier stud lines, |x|
    boarded = var != "C"

    # ---- THE APEX TRUSS, worked out FIRST, because on a narrow gable it is
    # what decides where the top rail can go -- not the other way round. That
    # inversion is the whole fix: the rail used to be pinned at z_h + 0.30 and
    # the arch was then squeezed into whatever was left above it, which on a
    # 2-bay is 0.086 m of visible face. See _apex_fit() and the note by
    # ARCH_RISE for the measurements.
    fit = _apex_fit(W, ZA, z_h, z_h + (0.30 if bays == 2 else 0.44) + RAIL_H)
    z_sp, x_sp, aw, z_cr = fit["z_sp"], fit["x_sp"], fit["aw"], fit["z_cr"]
    z_close, collar = fit["z_close"], fit["collar"]
    z_up, z_up_t = fit["z_up"], fit["z_up_t"]   # top rail, or the collar

    # ---- THE THINGS EVERY OTHER MEMBER HAS TO BE CUT AGAINST ----------------
    # Shanee: "SM_Gable_End_2bay_A still has many beams overlapping without
    # proper joints and other such gables also have similar issues in different
    # numbers." Measured -- each member built as its own solid, every pair
    # intersected, and a pair counted when NEITHER member ends inside the joint
    # (i.e. two beams crossing with nothing cut) -- the four variants scored
    # 11 / 15 / 11 / 22.
    #
    # Nearly all of it was one habit: a member was laid out against a CONSTANT
    # (the tier heights, the wall extents) instead of against the members it
    # actually meets, so it ran through them. The arc's soffit, the apex truss's
    # own heights and the braces' outlines are therefore worked out HERE, before
    # anything is drawn, and the studs, the boarding, the king post and the
    # label mould are all cut against them instead of guessing.
    def _soffit(x):
        """Underside of the apex arc's band at |x| -- the ceiling over the head."""
        u = min(1.0, abs(x) / max(x_sp, 1e-6))
        return _arc_z(u, z_sp, z_cr) - lerp(aw * .70, aw, u) * .5

    def _arc_top(x):
        """... and the back of the same band."""
        u = min(1.0, abs(x) / max(x_sp, 1e-6))
        return _arc_z(u, z_sp, z_cr) + lerp(aw * .70, aw, u) * .5

    # The apex truss. z_st is what the struts and the king post stand on, cz2
    # where the struts die into the rakes, z_col the upper collar if the gable is
    # wide enough to carry one.
    z_st = (z_up_t - .020) if collar else (z_cr + aw * .20)
    cz2 = min(lerp(z_st, ZA, .52), z_close - .040)
    # 0.50 rather than 0.62: the collar has to leave a run of strut ABOVE it as
    # well as below, or the struts cannot be cut on it and go back to crossing it.
    z_col = lerp(z_st, cz2, .50) if (not collar and cz2 - z_st > .40) else None
    COL_H = .132

    # The braces, as (centreline, widths, shade, bevel). They are LAID OUT here
    # and DRAWN further down, because the close studding has to be cut against
    # them and a stud that dodges a brace drawn from a second copy of these
    # numbers is a stud that dodges the wrong thing.
    #
    # Where the window brace dies into the rake: normally the top rail; on the
    # collar arrangement the rail is up on the arch's crown and the ARCH is what
    # occupies the rake at that height, so the brace stops 85 mm under the
    # arch's springing instead. Left at z_up + .02 the two would meet in the
    # plate with their front planes 6 mm apart (Y_BRACE vs Y_ARCH).
    brace_top = (z_sp - .085) if collar else (z_up + .02)
    braces = []
    if var in ("A", "C") or bays == 3:
        # the big arch over the window: springs off the mid rail, curves out and
        # dies into the rake at the upper rail. It used to run on to 0.62 of the
        # way up the WHOLE gable, i.e. straight through the upper rail and up
        # into the tympanum, where it read as a pair of loose diagonals with no
        # job. The tympanum has the apex arch now; this one belongs to the
        # window, as it does in ref3.
        for sgn in (-1, 1):
            a = (sgn * (jamb + .04), z_mid_t - .04)
            c = (sgn * (_rake_z_x(brace_top, W, ZA) - .085), brace_top)
            b = (sgn * (jamb + .05), brace_top - .12)        # pulls the curve in
            braces.append((_bez(a, b, c, 9),
                           [lerp(.235, .155, i / 8.0) for i in range(9)],
                           .92, .010))
        # short foot braces down to the tie beam
        for sgn in (-1, 1):
            a = (sgn * (jamb + .02), z_mid + .03)
            c = (sgn * (hw - .30), z_tie - .02)
            braces.append((_bez(a, (sgn * (hw - .55), z_mid - .12), c, 6),
                           .155, .90, .010))
    else:
        # variant B: straight braces, cranked -- a different rhythm on a run
        for sgn in (-1, 1):
            braces.append(([(sgn * (jamb + .05), z_mid_t - .04),
                            (sgn * (_rake_z_x(brace_top, W, ZA) - .085),
                             brace_top)], .18, .93, .012))
            braces.append(([(sgn * (hw - .22), z_tie - .02),
                            (0.0, z_mid + .04)], .15, .90, .012))
    brace_polys = [_band_poly(pts, wds) for pts, wds, _sh, _bv in braces]

    # The apex arc, laid out here for the same reason: the tympanum boarding
    # behind it has to be cut round it.
    arc_pts = _bez((-x_sp, z_sp), (0.0, 2 * z_cr - z_sp), (x_sp, z_sp), 11)
    arc_wds = [lerp(aw * .70, aw, abs(i / 5.0 - 1.0)) for i in range(11)]
    arc_poly = _band_poly(arc_pts, arc_wds)

    def _board_runs(cx, half, z0, z1):
        """Split a tympanum board's z run round the frame members that cross it.

        Boarding is CUT ROUND a frame member, not laid through it -- and on the
        3-bay this was eight of the measured through-lapped pairs: every board
        over the window ran straight through the apex arc (2.3-3.5 litres each)
        and three of them through the upper collar as well. Y_BOARD sits inside
        Y_ARCH and Y_HORIZ, so those boards were not behind the arch, they were
        IN it. Each run laps TENON into the member that stops it, so the cut ends
        are buried under a member that stands 24-32 mm proud of them."""
        # BOARD_LAP, not TENON: a board is thin, and it is CLIPPED to the gable
        # triangle, so near the rakes it is a trapezoid whose own long axis runs
        # diagonally. A 24 mm housing on a member like that is inside the noise
        # -- measured, four such laps still read as crossings. 50 mm is a housing
        # a carpenter would cut anyway for a board carried on an arch brace.
        bands = []
        b = _strip_band(arc_poly, cx, half)
        if b:
            bands.append(b)
        if z_col is not None and abs(cx) + half < _rake_z_x(z_col + COL_H, W, ZA):
            bands.append((z_col, z_col + COL_H))
        runs = [(z0, z1)]
        for (lo, hi) in bands:
            out = []
            for (a, c) in runs:
                if hi - BOARD_LAP <= a or lo + BOARD_LAP >= c:
                    out.append((a, c))
                    continue
                if a < lo + BOARD_LAP:
                    out.append((a, lo + BOARD_LAP))
                if hi - BOARD_LAP < c:
                    out.append((hi - BOARD_LAP, c))
            runs = out
        return [(a, c) for (a, c) in runs if c - a > .13]

    def _brace_band(cx, half):
        """The z band a brace occupies on the stud line at cx, or None."""
        lo, hi = 1e9, -1e9
        for poly in brace_polys:
            b = _strip_band(poly, cx, half)
            if b:
                lo, hi = min(lo, b[0]), max(hi, b[1])
        return None if lo > hi else (lo, hi)

    # ---- core: ONE solid backing triangle ---------------------------------
    # This was four panels stacked around the window opening, and their abutment
    # faces were coplanar ON THE INNER WALL PLANE (y=T) -- the exact fault in
    # Shanee's report. One prism has no internal joints to fight, costs ~90
    # fewer tris, and the attic light is a dark pane standing in the reveal
    # (Y_PANE) rather than a hole, which is what it already was.
    p.prism([(-hw, 0.0), (hw, 0.0), (0.0, ZA)], Y_CORE[1] - Y_CORE[0],
            "plaster_dim", axis='Y', at=(0, sum(Y_CORE) / 2, 0), bevel=0,
            tint=.03, shade=.62)

    # ---- LOWER TIER. Panels are cut between consecutive stud lines, so every
    # joint has a stud over it by construction (see _studs). The middle cell is
    # not plaster at all: ref3 fills exactly that cell -- the one under the
    # window, between the two posts -- with narrow vertical boards, which is
    # both the richest thing in the lower half of the reference gable and the
    # one panel that now cannot have a joint in it.
    z0l, z1l = z_tie - .02, z_mid + .02
    edges = [-hw] + [-v for v in reversed(xs)] + list(xs) + [hw]
    ci = len(xs)                                # left edge of the middle cell
    for i in range(len(edges) - 1):
        if i == ci:
            continue
        m = "plaster" if r.random() > .22 else "plaster_dim"
        _panel(p, edges[i] + SKIN_GAP, edges[i + 1] - SKIN_GAP, z0l, z1l, W, ZA,
               Y_SKIN, m, inset=.02, bevel=.012, tint=.055,
               shade=1.0 + r.uniform(-.07, .05))
    nb = max(3, int(round(2 * jamb / .145)))
    bwd = (2 * jamb - 2 * SKIN_GAP) / nb
    for i in range(nb):
        cx = -jamb + SKIN_GAP + bwd * (i + .5)
        p.box((cx, sum(Y_BOARD) / 2, (z0l + z1l) / 2),
              (bwd - .013, Y_BOARD[1] - Y_BOARD[0], z1l - z0l), "oak_mid",
              bevel=.009, seg=1, tint=.075, shade=.95 + r.uniform(-.09, .10))

    # ---- UPPER TIER: a big panel each side of the window column, the two
    # reveal cheeks, and the head and sill strips inside the column. Every x
    # joint here lands either on a jamb post or on the window reveal itself.
    for (a, b) in ((-hw, -jamb), (jamb, hw)):
        m = "plaster" if r.random() > .22 else "plaster_dim"
        _panel(p, a + SKIN_GAP, b - SKIN_GAP, z_mid_t - .02, z_up + .02, W, ZA,
               Y_SKIN, m, inset=.02, bevel=.012, tint=.055,
               shade=1.0 + r.uniform(-.07, .05))
    for (a, b) in ((-jamb, -ow / 2), (ow / 2, jamb)):
        _panel(p, a + SKIN_GAP, b - SKIN_GAP, z_mid_t - .02, z_up + .02, W, ZA,
               Y_SKIN, "plaster", inset=.02, bevel=.012, tint=.05,
               shade=.99 + r.uniform(-.05, .05))
    # ... and these two stop 30 mm SHORT of the opening at top and bottom, so
    # their cut faces end up buried inside the reveal lining instead of shining
    # out through the insert's 20 mm shadow gap. See the liner block below.
    _panel(p, -ow / 2 + SKIN_GAP, ow / 2 - SKIN_GAP, z_mid_t - .02, z_s - .03,
           W, ZA, Y_SKIN, "plaster", inset=.02, bevel=.012, shade=.97)
    _panel(p, -ow / 2 + SKIN_GAP, ow / 2 - SKIN_GAP, z_h + .03, z_up + .02,
           W, ZA, Y_SKIN, "plaster", inset=.02, bevel=.012, shade=1.02)

    # ---- tympanum: vertical boarding (A/B) or plaster + vent (C) ----------
    if boarded:
        # The boards are CLIPPED TO THE TRIANGLE, not dropped when they no
        # longer fit inside it. Laid as plain rectangles and skipped whenever
        # `top - z_up_t < 0.12`, the boarding stopped dead at |x| = 0.90 on a
        # 3-bay gable whose tympanum is 2.05 wide, and the two triangles left
        # over showed the dark backing straight through: a second pair of gaps,
        # in the apex this time. Clipped, the run dies under the rake plates.
        n = max(5, int(round(W / 0.29)))
        bw = W / n
        for i in range(n):
            x0 = -hw + bw * i + .008
            sh = .95 + r.uniform(-.09, .10)
            for (za, zb) in _board_runs(x0 + bw / 2 - .008, bw / 2,
                                        z_up_t - .02, ZA - .012):
                _panel(p, x0, x0 + bw - .016, za, zb, W, ZA,
                       Y_BOARD, "oak_mid", inset=.055, bevel=.009, tint=.075,
                       shade=sh)
    else:
        # variant C: a plastered tympanum instead of boarding. It used to carry
        # two louvre slats here as well, and they were a third set of Shanee's
        # loose blocks: two 0.30 x 0.055 bars tilted 14 deg, standing 20 mm proud
        # of the plaster with no frame, no reveal and nothing behind them -- and
        # pinned at z_up_t + 0.30, which on the only gable that HAS a variant C
        # (the 2-bay) is 0.18 m from the apex, where the triangle is narrower
        # than the slats are long. There is no room for a framed vent up there
        # once the apex arch and the king post are in, so the vent is gone
        # rather than faked; C now reads as the plain plastered gable of the
        # three, which is difference enough on a wall run.
        _panel(p, -hw, hw, z_up_t - .02, ZA, W, ZA, Y_SKIN, "plaster", inset=.02,
               bevel=.012, shade=1.0)

    # ---- lozenge / diamond motifs. ref3 sets a row of diamonds into the gable
    # framing just over the upper rail, and this piece only ever carried them on
    # variant B. Every gable gets the row now -- it is one of the cheapest
    # things in the reference and one of the most legible. It is APPLIED
    # ornament, so `_on_face` throws out any position that would hang over a
    # rake or vanish under a rake plate: the old row was pinned at x = +-0.44
    # whatever the bay count, and on the 2-bay gable the outer two landed clean
    # OUTSIDE the triangle, two diamonds floating in the air beside the roof.
    d = .125
    half = d * .7071 + .012
    czt = z_up_t + (.12 if bays == 3 else .10)
    if not collar:
        # The row sits in the spandrel between the rail and the arc, so it is
        # pinned off THE ARC's soffit as well, not off the rail alone. Fitted,
        # the 3-bay crown drops 63 mm, and the old fixed offset would then have
        # laid the diamonds' top corners 9 mm under it -- Y_LOZ and Y_ARCH have
        # their front planes 6 mm apart, so that is a z-fight, not a joint.
        czt = min(czt, z_cr - .35 * aw - half - .045)
    row = [(k * d * 2.05, czt) for k in (-1, 0, 1)]
    # _seen, not _on_face: a diamond that is on the face but under the verge is
    # not ornament, it is a hidden box. See _verge_z.
    row = [q for q in row if _seen(q[0], q[1], half, W, ZA)]
    def _panel_loz(t):
        """One lozenge in the lower-tier cell NEXT TO THE WINDOW, each side.

        Only that cell: it is the one lower-tier panel that no brace crosses,
        in either variant. Every cell outboard of it has either the curved foot
        brace (A/C) or the long cranked one (B) sweeping through the middle of
        it, and a lozenge is applied ornament -- Y_LOZ sits 12 mm BEHIND
        Y_BRACE, so a diamond placed on a brace does not decorate it, it is
        eaten by it. That is what happened the moment the rake plate slimmed
        down and `_on_face` let the outer cells through: four diamonds instead
        of two, and the two new ones half under a brace.

        `t` is where in the tier the row sits, and it has to know which brace
        it is dodging: A and C carry the foot brace high and near the centre,
        B rakes one right down across this cell, so B's row drops."""
        cz2 = lerp(z_tie, z_mid, t)
        out = []
        if len(xs) < 2:
            return out
        for sgn in (-1, 1):
            cx = sgn * (xs[0] + xs[1]) / 2
            if _seen(cx, cz2, half, W, ZA) and abs(cx) - half > jamb + .04:
                out.append((cx, cz2))
        return out

    if len(row) < 3:
        # A 2-bay tympanum is nearly all rake plate and king post -- at the height
        # the row wants, the panel between the plate's inner edge and the post is
        # narrower than one diamond -- so the motif drops into the lower-tier
        # panels, which is also where ref3 sets diamonds on its narrower bays.
        # The 3-bay used to fall down here too, for the other reason: measured
        # against the OLD 0.895 m verge drop its outer two diamonds sat 0.26 m up
        # behind the bargeboard's fringe. With the board and its fringe cut to the
        # references' proportion (see BW) the drop is 0.586 m and all three are
        # seen in the spandrel, which is where ref3 draws them; the test decides,
        # not the bay count.
        row = _panel_loz(.52 if (var in ("A", "C") or bays == 3) else .34)
    elif var == "B":
        # variant B doubles the motif down into the lower tier as well, low
        # enough to clear the foot brace crossing above it
        row += _panel_loz(.34)
    for (cx, cz) in row:
        p.box((cx, sum(Y_LOZ) / 2, cz), (d, Y_LOZ[1] - Y_LOZ[0], d),
              "oak_dark", bevel=.006, seg=1, rot=(0, 45, 0), tint=.04, shade=.7)

    # ---- rake plates: the gable's own timber along both rake lines. Wide,
    # because a bare gable end has to read as a rake even with no barge on it.
    # The foot starts 18 mm up so its underside is buried in the tie beam rather
    # than sharing the tie beam's bottom plane on z=0.
    rw = rake_w(W)
    for sgn in (-1, 1):
        quad = [(sgn * hw, 0.018), (sgn * (hw - rw / SINP), 0.018),
                (0.0, ZA - rw / COSP), (0.0, ZA)]
        p.prism(quad, Y_RAKE[1] - Y_RAKE[0], "oak_dark", axis='Y',
                at=(0, sum(Y_RAKE) / 2, 0), bevel=.012, seg=1, tint=.05,
                shade=.94 + r.uniform(-.04, .04))

    # ---- horizontal members ----------------------------------------------
    def hbeam(z0, z1, x0, x1, mat="oak_dark", y=Y_HORIZ, proud=0.0, sh=1.0,
              housed=None):
        """One horizontal timber. With `housed` the ends are cut ON THE RAKE and
        buried that far (in x) inside the rake plate, so the member visibly dies
        into the principal rafter instead of running out past it -- see the note
        at the top of this file. Without it the member spans x0..x1 square, which
        is only correct for the bottom tie beam, whose full width IS the wall
        plate under the gable."""
        yy = (y[0] - proud, y[1])
        if housed is None:
            p.box(((x0 + x1) / 2, sum(yy) / 2, (z0 + z1) / 2),
                  (x1 - x0, yy[1] - yy[0], z1 - z0), mat, bevel=.014, seg=1,
                  tint=.05, shade=sh)
            return
        poly = _clip([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], W, ZA, housed)
        if len(poly) < 3:
            return
        p.prism(poly, yy[1] - yy[0], mat, axis='Y', at=(0, sum(yy) / 2, 0),
                bevel=.014, seg=1, tint=.05, shade=sh)

    # ---- bottom tie beam. It is the wall plate the whole gable stands on, so
    # it keeps its FULL width at z = 0 -- but its top corners are now CUT BACK ON
    # THE RAKE. Square, a 0.21 m deep beam running out to x = +-W/2 puts its two
    # top-outer corners 0.129 m OUT OF THE ROOF PLANE (0.152 m once
    # assemble_inn's kx/kz stretch has amplified this piece's perpendicular
    # offsets), i.e. two lumps of oak_dark standing through the shingle field at
    # the foot of each rake -- more wood going straight out of the shingles, in
    # the same junction, and measured on out/inn_example.blend at both gables and
    # all four rakes. The cut stops 0.05 (in x) short of the rake at the top and
    # runs to the corner at z = 0, so the end face is TILTED off the roof plane
    # rather than lying in it: nothing to fight with the boarding either.
    xt = _rake_z_x(z_tie, W, ZA) - .05
    p.prism([(-hw, 0.0), (hw, 0.0), (xt, z_tie), (-xt, z_tie)],
            Y_HORIZ[1] - Y_HORIZ[0], "oak_dark", axis='Y',
            at=(0, sum(Y_HORIZ) / 2, 0), bevel=.014, seg=1, tint=.05, shade=.90)
    hbeam(z_mid, z_mid_t, -hw, hw, sh=.97, housed=HOUSE)     # mid rail
    hbeam(z_up, z_up_t, -hw, hw, sh=.95, housed=HOUSE)       # upper rail

    # dentil course hung off the upper rail -- echoes the bargeboard fringe.
    # The teeth are HOUSED 30 mm up into the rail's own lower edge, and they are
    # FINE: 58 mm on a 0.132 pitch, not 72 on 0.185. A coarse row of chunky
    # blocks under a rail is exactly the thing Shanee read as "strange blocks";
    # a fine, even, close-pitched row reads as the moulded course it is.
    # It is drawn only where there is a rail to hang it from. On the collar
    # arrangement the arc's crown is directly under that beam, so the teeth
    # would hang into the arch; the tooth motif moves onto the arch's own
    # soffit instead (_arc_cusps).
    if not collar:
        dtop, dh = z_up + .030, .092
        dx = _rake_z_x(z_up_t, W, ZA) - .06
        nd = max(1, int(round(2 * dx / .132)))
        for i in range(nd):
            p.box((lerp(-dx, dx, (i + .5) / nd), sum(Y_DENT) / 2, dtop - dh / 2),
                  (.058, Y_DENT[1] - Y_DENT[0], dh), "oak_dark", bevel=.007,
                  seg=1, tint=.05, shade=1.0 + r.uniform(-.07, .07))

    # ---- studs ------------------------------------------------------------
    # A STUD DIES INTO WHATEVER CROSSES IT. `dodge` cuts it on the brace it
    # meets, leaving TENON of it buried in that brace at each shoulder, which is
    # how close studding is really framed round a principal brace -- and it is
    # most of the through-lapped pairs this piece was measured with: on
    # SM_Gable_End_2bay_B six pairs were a stud or a jamb post simply crossing
    # the cranked brace, 1.3-1.8 litres of oak each.
    #
    # The top cut moved too. It was `rake line - 0.010`, i.e. the stud ran to the
    # OUTER face of the rake plate -- the roof plane itself -- with 10 mm to
    # spare against a wobble of 7 mm. RAKE_HOUSE buries it properly.
    def stud(cx, z0, z1, w=0.135, mat="oak_dark", sh=1.0, dodge=False):
        top = min(z1, _rake_z(abs(cx) + w / 2, W, ZA) - RAKE_HOUSE)
        segs = [(z0, top)]
        b = _brace_band(cx, w / 2) if dodge else None
        if b and b[0] - TENON > z0 and b[1] + TENON < top:
            segs = [(z0, b[0] + TENON), (b[1] - TENON, top)]
        elif b and b[0] - TENON <= z0 < b[1]:
            segs = [(b[1] - TENON, top)]
        elif b and z0 < b[0] < top <= b[1] + TENON:
            segs = [(z0, b[0] + TENON)]
        for (a, c) in segs:
            if c - a < .10:
                continue
            p.box((cx, sum(Y_STUD) / 2, (a + c) / 2),
                  (w, Y_STUD[1] - Y_STUD[0], c - a), mat, bevel=.012, seg=1,
                  tint=.05, shade=sh, skew=(r.uniform(-1, 1) * .006, 0))

    # THE WINDOW JAMBS ARE TWO POSTS, TENONED INTO THE MID RAIL, NOT ONE POST
    # THROUGH IT. As one 1.7 m stick from the tie beam to the upper rail the post
    # drove straight through the mid rail -- 2.2 litres of oak, the largest
    # crossing in every variant, and the one a carpenter would notice first,
    # because the rail is the member that runs (it is housed into both rafters).
    # Split, each post's end dies TENON inside the rail and the lower-tier and
    # upper-tier plaster joints on that line still each have timber over them,
    # which is what the single post was there for.
    #
    # AND THE UPPER ONE STOPS UNDER THE APEX ARCH. On the collar arrangement the
    # arc springs straight off the rafters over the window head, so a post run to
    # z_up + 0.02 came out through the top of it. It is housed into the soffit
    # instead, and the upper tier's plaster is closed over the post's head by a
    # single full-width panel rather than by two panels with a joint in the air.
    z_jt = z_up + .02
    if collar:
        z_jt = min(z_jt, _soffit(jamb + .075) + TENON)
    for sgn in (-1, 1):
        stud(sgn * jamb, z_tie - .02, z_mid + TENON, w=.15, sh=.98, dodge=True)
        stud(sgn * jamb, z_mid_t - TENON, z_jt, w=.15, sh=.98)
    # and a SHORT STUD ON TOP OF THE ARCH where the post has been stopped under
    # it, so the upper tier's plaster joint on that line still has timber over it
    # for its whole height -- the thing the continuous post was there for. Its
    # foot is housed in the arc's back, its head in the rail above.
    if collar:
        z_ss = _arc_top(jamb + .075) - TENON
        for sgn in (-1, 1):
            stud(sgn * jamb, z_ss, z_up + .02, w=.15, sh=.96)
    # close studding: one stud over EVERY remaining joint in the lower tier.
    for sgn in (-1, 1):
        for i, xv in enumerate(xs[1:]):
            stud(sgn * xv, z_tie - .02, z_mid + .02, dodge=True,
                 w=.125 if i == 0 else .115, sh=.93 + r.uniform(-.04, .05))

    # ---- THE APEX ARCH ----------------------------------------------------
    # ref3 draws a broad shallow arc of timber spanning under every gable apex,
    # and assemble_inn.py no longer lays a collar tie across the gables (those
    # were the loose beams lying on the roof beside the bargeboard), so the
    # piece has to carry its own -- on BOTH widths, which is what _apex_fit is
    # for. Both feet are housed inside the principal rafters (the rake plate
    # stands 30 mm proud of the arch, so it covers the cut); the arc is deepest
    # at the springing and slimmest at the crown; and the crown carries either
    # the king post directly or, on the collar arrangement, the collar beam that
    # the king post and the struts then stand on.
    _band(p, arc_pts, arc_wds, "oak_dark", Y_ARCH, bevel=.011, tint=.05,
          shade=.97)
    if collar:
        # ARCH-BRACED COLLAR: the arc carries the cusping that a rail would
        # otherwise carry as a tooth course under it.
        _arc_cusps(p, W, ZA, z_sp, x_sp, aw, z_cr, r)
    # ---- the two apex struts, ref3's and r6's apex truss. They stand on
    # whatever closes the truss under them -- the collar where there is one,
    # otherwise the arch's crown -- and die into the rakes, and they are the
    # thing that stops the last triangle above the collar from being the empty
    # one this piece was reported for. Their feet BITE into what they stand on:
    # at z_cr + .40 * aw they used to float 11 mm clear of the arch, which on a
    # piece that gets wobble(.007) is a hairline gap under a bearing member.
    # cz2 is held under z_close, so a strut can never run up into the zone where
    # the rake plates cover everything.
    # AND THEY ARE CUT ON THE COLLAR WHERE THERE IS ONE, tenoned into it from
    # below and standing on it above -- ref3's queen struts. Run past it they
    # were two more beams crossing a beam, 1.35 litres each.
    for sgn in (-1, 1):
        cx2 = sgn * (_rake_z_x(cz2, W, ZA) - .055)
        if abs(cx2) <= .15 or cz2 - z_st <= .14:
            continue
        runs = [(z_st, cz2)]
        if z_col is not None and z_st + .09 < z_col and z_col + COL_H < cz2 - .09:
            runs = [(z_st, z_col + TENON), (z_col + COL_H - TENON, cz2)]
        for (za, zb) in runs:
            fa = (za - z_st) / (cz2 - z_st)
            fb = (zb - z_st) / (cz2 - z_st)
            _band(p, [(lerp(sgn * .075, cx2, fa), za),
                      (lerp(sgn * .075, cx2, fb), zb)], .128, "oak_dark",
                  Y_STRUT, bevel=.010, tint=.05, shade=.90)
    # ---- THE UPPER COLLAR, and why the apex needed one.
    # With the bargeboard's 0.87 m pendant gone (see the AP_* note) the whole
    # tympanum is in view for the first time, and on a WIDE gable what it shows
    # between the arch's crown and the rake plates is a 0.9 m triangle carrying
    # a king post and two struts that meet nothing at the top -- three members
    # radiating into flat boarding. Measured on 3bay_A, 40 % of the visible
    # tympanum was unrelieved panel.
    # A collar tie closes that triangle: the king post and the two struts now
    # frame a real apex truss instead of a fan. It is HOUSED into the rafters
    # like every other horizontal member here, so its ends die inside the rake
    # plates, and it sits at Y_HORIZ -- 20 mm BEHIND the struts that cross it
    # (Y_STRUT) and 24 mm proud of the king post, which is the order a carpenter
    # would assemble them in and keeps all three off each other's planes.
    # The collar arrangement (narrow gables) already has its collar: the top
    # rail IS one, riding on the arch's crown, and above it there is 0.22 m of
    # visible face -- no room for a second, so it does not get one.
    if z_col is not None:
        hbeam(z_col, z_col + COL_H, -hw, hw, sh=.94, housed=HOUSE)
    # King post. It stands on whatever is directly under it -- the collar where
    # there is one, otherwise the arch's crown -- and its foot is buried in that
    # member rather than stopped on its surface: at z_cr - .09 it used to hang
    # 15 mm THROUGH the arc's soffit and out the bottom.
    # Widened from 0.16 to 0.19: it is the member the whole apex now hangs its
    # reading on, and at 0.16 it was narrower than the studs three metres below
    # it. 0.19 is still under the 0.24 rake plate it dies into.
    # WHERE THERE IS AN UPPER COLLAR THE POST IS IN TWO PIECES, tenoned into it
    # top and bottom, for the same reason the jamb posts are split at the mid
    # rail: the collar is the member that runs, and a post through it is a beam
    # lapping a beam with nothing cut. (On the collar arrangement -- the narrow
    # gables -- the post already starts inside the top rail, so it is one piece.)
    k_foot = (z_up_t - .030) if collar else (z_cr - .10 * aw)
    if z_col is None:
        stud(0.0, k_foot, ZA - .04, w=.19, sh=1.02)
    else:
        stud(0.0, k_foot, z_col + TENON, w=.19, sh=1.02)
        stud(0.0, z_col + COL_H - TENON, ZA - .04, w=.19, sh=1.02)

    # ---- braces (DRAWN here, LAID OUT above -- see `braces`) ---------------
    for pts, wds, sh, bv in braces:
        _band(p, pts, wds, "oak_dark", Y_BRACE, bevel=bv, tint=.05, shade=sh)

    # ---- window opening: THE REVEAL IS LINED ALL THE WAY TO THE FACE ------
    # spec leaves INSERT_CLEAR (20 mm) all round every insert, and that gap is
    # the SHADOW that makes a window read as set into a wall rather than stuck
    # on it -- but only if what stands behind it is dark. With the liner starting
    # 94 mm back, what stood behind it here was the plaster skin's own return and
    # the pale core, and the fitted insert came out ringed by a bright cream halo
    # 20 mm wide on three sides. So the lining now runs from y = 0.020 (15 mm
    # PROUD of the plaster) back to the core, and it is wide enough to swallow
    # the plaster panels' cut edges: jambs 80 mm on the reveal's own line, head
    # and sill 0.010 narrower than the jambs so their ends die INSIDE them. The
    # plaster strips over and under the opening are pulled 30 mm clear of it (see
    # the UPPER TIER above) so their bright cut faces are buried in the lining
    # too. The dark pane overshoots the opening 50 mm all round behind all of it.
    yl = (sum(Y_LINER) / 2, Y_LINER[1] - Y_LINER[0])
    for sgn in (-1, 1):
        p.box((sgn * (ow / 2 + .040), yl[0], (z_s + z_h) / 2),
              (.080, yl[1], oh + .16), "oak_dark", bevel=.008, seg=1,
              tint=.04, shade=.72)
    for z in (z_s - .040, z_h + .040):
        p.box((0, yl[0], z), (ow + .14, yl[1], .070), "oak_dark", bevel=.008,
              seg=1, tint=.04, shade=.72)
    # The blank behind the reveal. It overshoots the opening 90 mm top and
    # bottom and 95 mm each side, so its own edges are buried inside the lining
    # and the plaster beyond it rather than landing on the plaster strips' cut
    # faces -- at oh + 0.06 its bottom edge sat exactly on the strip's new top
    # edge, 59 cm2 of plaster lying on oak_dark.
    p.plate((0, sum(Y_PANE) / 2, (z_s + z_h) / 2),
            (ow + .10, Y_PANE[1] - Y_PANE[0], oh + .18), "oak_dark", tint=.02,
            shade=.18)

    # ---- THE WINDOW SURROUND: ONE CILL, ONE LABEL MOULD, AND THEY ARE THE
    # WALL'S. See the note by IW/IH. Round 14 had this the other way round --
    # the insert carried the cill and the mould, the wall carried nothing -- and
    # every one of the four collisions the round-15 audit measured came out of
    # it. Both members are drawn HERE now, against geometry this piece owns and
    # can therefore measure itself against, and the insert is bounded to the
    # hole so it cannot reach either of them.
    #
    # THE CILL IS HOUSED IN THE MID RAIL, not laid across its face. Its back
    # face stands at y = 0.070, buried in the rail; its underside SLOPES from
    # the front drip back and down INTO the rail, so it crosses the rail's front
    # plane (y = -0.056) 124 mm under the opening and there is no horizontal
    # face anywhere in daylight and no bottom edge stopping in air. Its top is
    # weathered -- 44 mm of fall over the 204 mm from the plaster line to the
    # drip -- so it shares no plane with the rail's flat top either. Measured
    # against the insert: the insert's lowest geometry is its frame sill at
    # z_s + 0.005, which is 6 mm above the cill's highest point, so the two
    # cannot lap at any wobble amplitude this piece uses.
    yc0, yc1 = Y_LEDGE
    cxh = ow / 2 + .105                 # 0.365: ends housed 95 mm inside the
                                        # jamb posts, which run 0.270..0.420
    p.prism([(yc1, z_s - .006), (yc0, z_s - .050), (yc0, z_s - .096),
             (yc1, z_s - .168)], 2 * cxh, "oak_mid", axis='X', at=(0, 0, 0),
            bevel=.010, seg=1, tint=.05, shade=1.02)
    # Two brackets under it. THEIR FEET ARE INSIDE THE MID RAIL: the profile's
    # last two points are at y = -0.048 and y = +0.070, both BEHIND the rail's
    # front face, so the visible outline dies into the rail and the square end
    # cut is 12 mm above the rail's own underside where nothing can see it. The
    # pair this replaces hung 48 mm BELOW that underside and ended in open air.
    # Their tops run 8-80 mm up into the cill, so they bear on it rather than
    # touching it.
    # The bracket's back plane is 16 mm DEEPER than the cill's, not on it: at
    # y = 0.070 the two shared a plane over the whole 0.10 x 0.05 of each
    # bracket's back, and only wobble's 0.22 mm was keeping that off
    # check_zfight's books. 0.086 is inside the mid rail either way.
    for sgn in (-1, 1):
        p.prism([(.086, z_s - .088), (-.122, z_s - .088), (-.098, z_s - .146),
                 (-.048, z_s - .172), (.086, z_s - .188)], .080, "oak_dark",
                axis='X', at=(sgn * (ow / 2 + .020), 0, 0), bevel=.008, seg=1,
                tint=.05, shade=.86)

    # ---- THE LABEL MOULD over the head, ref2/ref3's drip stone -- AND IT IS
    # FITTED TO THE TRUSS IT SITS IN rather than pinned at a constant.
    # The lintel this replaces was 0.82 wide, 80 mm deep, pinned 26 mm under the
    # insert's own head, and on a 2-bay gable that put it at z 1.540..1.620 --
    # straight through an apex arch whose feet spring at 1.545 (52/48/48
    # intersecting face pairs, 45 mm proud of the arc). The arch's springing is
    # not a constant: _apex_fit drops it onto the rafters over the window head on
    # a narrow gable and lifts it above the top rail on a wide one, a difference
    # of a metre. So the mould asks the arc where its soffit is and takes what is
    # left, and where that is less than a mould's worth it is not drawn.
    mxh = ow / 2 + .080                 # 0.340: ends housed in the jamb posts
    z_lab = z_h + .006
    room = min(_soffit(mxh), _soffit(0.0), z_up - .010) - z_lab
    if room > .095:
        mh = min(.096, room - .040)     # 40 mm of daylight under the arc, at
                                        # least, on the tightest gable in the set
        p.prism([(yc1, z_lab + mh), (yc0, z_lab + mh - .020), (yc0, z_lab + .026),
                 (-.070, z_lab), (yc1, z_lab)], 2 * mxh, "oak_mid", axis='X',
                at=(0, 0, 0), bevel=.010, seg=1, tint=.05, shade=1.04)
        # The carved crest of ref2/ref3, standing IN FRONT of the mould and
        # bedded 34 mm into its face. Same test again: it is only drawn where
        # the arc leaves a whole one room, which on a 2-bay it does not.
        if min(_soffit(0.0), z_up - .010) - (z_lab + mh) > .245:
            crest = [(-.19, 0.0), (-.15, .055), (-.105, .038), (-.075, .095),
                     (-.032, .062), (0.0, .155), (.032, .062), (.075, .095),
                     (.105, .038), (.15, .055), (.19, 0.0)]
            zc = z_lab + mh - .030
            p.prism([(a, b + zc) for (a, b) in crest], .052, "oak_pale", axis='Y',
                    at=(0, -.126, 0), bevel=.007, seg=1, tint=.05, shade=1.07)
            p.box((0, -.126, zc + .171), (.055, .026, .075), "oak_pale",
                  bevel=.008, seg=1, tint=.05, taper=.4, shade=1.06)

    # ---- purlin ends, and the ridge beam under the apex -------------------
    # See _purlin(): these were the loose blocks. They run through the wall now.
    # The heights are chosen so a purlin's own top and bottom faces land clear of
    # every horizontal panel edge on the gable. At f = 0.34 the purlin's underside
    # sat 4 mm above the lower tier's top edge at z_mid + 0.02, and wobble closed
    # that into 130 cm2 of plaster lying on oak -- the biggest coincident pair in
    # the family. These land mid-panel, 50 mm clear of the nearest panel edge.
    for sgn in (-1, 1):
        for f in ((.410, .566) if bays == 3 else (.46,)):
            zr = ZA * f
            xr = _rake_z_x(zr, W, ZA)
            n_in = rake_w(W) / 2               # dead on the rafter's centre line
            _purlin(p, sgn * (xr - n_in * SINP), zr - n_in * COSP, r)
    # NO RIDGE-BEAM END AT THE APEX ANY MORE.
    # A 0.150 x 0.150 chamfered beam end used to sit on the king post at
    # ZA - 0.28. Measured against _verge_z it is 0.66 m up behind the
    # bargeboard, so the only place it can be seen from is the 0.20 m gap the
    # fringe leaves either side of the ridge (AP_FRINGE) -- and seen through
    # that gap, with no beam and no wall visible around it, it reads as one more
    # loose block at the top of the gable, which is the report this family has
    # already had twice. The other purlin ends above still read, because they
    # come out of the wall in daylight halfway down the rake. This one cannot,
    # at either width: on a 2-bay the whole apex is under the verge, so there is
    # no height at which it could be both on the king post and visible. So it
    # goes, and the king post runs clean to the apex block instead.


def _rake_z_x(z, W, ZA):
    """|x| of the rake line at height z."""
    return max(0.0, (1.0 - z / ZA) * W / 2.0)


def _end(bays, var):
    W = bays * G
    ZA = apex_z(bays)
    name = f"SM_Gable_End_{bays}bay_{var}"
    p = _Fix(Part(name, budget="gable",
                  seams=dict(x=(-W / 2, W / 2), y=(0, T), z=(0, ZA))))
    _face(p, W, ZA, var, seed={"A": 1, "B": 2, "C": 3}[var] + bays * 10)
    p.wobble(.007, freq=1.5)
    p.sag(.012, axis='x', span=(-W / 2, W / 2))
    return p.finish()


# -------------------------------------------------------------- bargeboard ---
def _barge_profile(u):
    """(v of the KERB LIP's top edge, board face depth) at station `u` up the
    rake. v lies in the gable-wall plane, perpendicular to the rake: 0 is the
    roof surface, + is out of it. The board's own top edge is LIP_DROP below the
    first number and the dentil ladder CAP_DROP below that, so the three step
    down outboard (see the VERGE note at the top).

    TWO SEPARATE TAPERS, and they used to be one. The board FATTENS toward its
    foot over BFOOT -- that is the mass ref1's swept eave has. The verge LIFTS
    out of the roof plane only over BELL_U, because that is all the roof itself
    does (see the BELL note): the bell-cast flare is 0.36 m of rake, not 1.10,
    and tying the lift to the swell put 0.10 m of lift half a metre up the rake
    where the shingles are still dead flat. Above u = 0 the lift is exactly zero,
    so the lip's top edge rides VERGE_LAP over the field for the whole rake.

    There is a THIRD taper, and it is not here: LOWSWEEP takes the board's LOWER
    edge back up through the flare. It is applied in _rake_assembly rather than
    in this function because everything hung off that edge -- the two ogee rolls,
    the soffit web, the pendant fringe -- has to move with it."""
    kt = clamp(-u / BELL_U)                # 0 above the flare, 1 at the drip
    st = clamp(1.0 - u / BFOOT)
    return VERGE_LAP + BELL * kt ** BELL_P, BW * (1.0 + BSWELL * st * st)


def _stations(L):
    """Sample stations up the rake: dense through the bell-cast at the foot and
    through the swell above it, sparse over the straight run, and running PAST
    the apex at the head -- the bands are mitred on the ridge plane afterwards
    (see _mitre), and a vertical cut needs material on both sides of it to bite
    into.

    IT STARTS AT U0, BELOW THE GABLE'S BASE CORNER. It used to start at -0.075,
    which is 0.046 m of plan -- so the bargeboard stopped a third of the way
    along the eave overhang and the outer 0.09 m of every verge had its tile
    ends in open air. The roof's last material is at u = -0.399 measured (see
    the BELL note), so the board's centreline runs to -0.34 and, once its own
    depth is added, the assembly reaches u = -0.386 -- inside the drip rather
    than 0.10 m past it, which is where the old swept tail ended up.

    0.26 at the head rather than 0.14, because the mitres LAP. A band's cut
    reaches u = L - inset/cos P + v*tan P, and with the insets negative the worst
    case is the kerb lip's top edge: L + 0.010/cos P + 0.142*tan P = L + 0.198.
    Left at 0.14 the polygon simply ran out before the cut line and the lap
    silently did not happen."""
    us = [lerp(U0, 0.0, i / 5.0) for i in range(5)]          # the bell-cast
    us += [lerp(0.0, BFOOT, i / 6.0) for i in range(7)]      # the swell
    return us + [lerp(BFOOT, L + .26, (i + 1) / 4.0) for i in range(4)]


def _rake_assembly(p, name, L, seed, tail=True, hand=0):
    """One rake's worth of verge, built in RAKE-LOCAL coordinates:
       +X runs up the rake (0 at the foot, L at the apex)
       +Y is world Y  (-VO = outboard face of the verge)
       +Z is perpendicular to the rake in the gable plane (0 = the roof surface)
    Returned as a sub-Part for the caller to rotate into place.

    Layered outward from the wall: dark soffit web, the broad rake BOARD, a
    two-step ogee roll along its lower edge, a fringe of pendant dentils hung off
    that roll, the KERB LIP that laps the tile ends along the board's top edge, a
    DENTIL LADDER worked on the face below it, and a carved SCROLL where the board
    seats on the eave. Every one of those bands takes three cuts: the ridge mitre at its
    head (_mitre / _head), its own stagger short of the end section (_stop), and
    the level cut at the eave (_foot)."""
    r = rng(f"barge/{name}/{seed}")
    raw = p.sub(f"{name}_r{seed}")
    s = _Fix(raw)

    us = _stations(L)
    prof = [_barge_profile(u) for u in us]
    # The lip's top edge is `vt`; the board hangs LIP_DROP under it, so `mid` is
    # the board's centreline.
    wid = [w for (_, w) in prof]
    mid = [(u, vt - LIP_DROP - w / 2.0) for u, (vt, w) in zip(us, prof)]
    # THE LOWER EDGE IS NO LONGER -w/2. It is swept up through the bell-cast, so
    # the board narrows into its scroll instead of diving under the eave -- see
    # the LOWSWEEP note. `hlo` is the half-depth BELOW the centreline at each
    # station; above it the board still runs to +w/2, welded to the kerb.
    hlo = [(w / 2.0) * (1.0 - LOWSWEEP * clamp(-u / BELL_U) ** LOWSWEEP_P)
           for u, w in zip(us, wid)]
    low = _off(mid, [-h for h in hlo])                # the board's lower edge
    # The kerb's centreline. It keeps its full section RIGHT DOWN TO THE DRIP.
    # It used to sink LIP_DROP back onto the board's own top edge over the last
    # LIPFADE of rake so that the two merged at the tail -- which mattered while
    # the board stopped 0.05 m below the base corner and the lip's end was a bare
    # step in the air. Now that the board runs on to the eave the tail scroll
    # covers that end, and the fade was costing the one thing the lip is for:
    # through the bell-cast it put the lip's top edge 1-15 mm BELOW the measured
    # shingle field, i.e. the course ends came out over the top of the kerb along
    # the whole flare. Held at the profile's own `vt` it laps them everywhere.
    #
    # AND IT IS OFFSET ALONG THE SECTION NORMAL, NOT STRAIGHT DOWN IN v. Both
    # this and the Y_CAP band used to be written (u, vt - something), i.e. the same
    # station with a plain vertical drop. That is identical to a normal offset
    # while the rake is straight -- and wrong the moment it curves. Through the
    # bell-cast the section is tilted ~45 deg, so a point at the same u and a
    # higher v lies 0.15 m PAST the board's end plane: the kerb lip's foot stood
    # out beyond the swept tail as a loose 0.20 x 0.08 block, which is precisely
    # the "strange blocks" report again, arriving by a new route. Offset along
    # the normal like `low` and the rolls, every band ends flush on one plumb cut
    # and the tail boss covers it.
    lip = _off(mid, [w / 2.0 + LIP_DROP - LIPW / 2.0 for w in wid])

    # ---- THE FOOT CUTS. Every band's centreline is offset from `mid` along the
    # SECTION NORMAL, which preserves the along-rake coordinate exactly -- so
    # every one of them ends on ONE plumb plane through station 0. That is what
    # put 63 cm2 of coincident oak at the right rake's foot: the plank's end face
    # (y -0.392..-0.290) and the ogee roll's (y -0.428..-0.346) on the same plane
    # to a tenth of a millimetre, overlapping over 46 mm of y. Mouldings are not
    # stopped flush with the board anyway -- they die into the scroll boss short
    # of it -- so each band takes its own stop, staggered 14 mm apart, the same
    # way the bands are staggered at the apex mitre. The tail boss (a from -0.14
    # to +0.24 along the section) covers every one of them.
    ft0, fm0 = _frames(mid)[0], mid[0]

    def _stop(off):
        """Cut a rake band `off` short of the board's own end section."""
        return lambda q: off - ((q[0] - fm0[0]) * ft0[0] + (q[1] - fm0[1]) * ft0[1])

    # ... AND THE LEVEL CUT UNDER ALL OF THEM. Staggered by FOOT_Z so the five
    # horizontal faces it can leave are never coplanar, exactly like the mitre
    # insets at the apex.
    fz = lambda i: _foot(Z_FOOT + FOOT_Z[i])

    # ---- the apex cuts. Wh is half the gable width, so the ridge plane is the
    # line u*cos P - v*sin P = Wh and every band is mitred `inset` short of it.
    # `hand` picks the left or right inset, which are never equal.
    Wh = L * COSP
    ZA = L * SINP                     # the apex height this rake climbs to
    mt = lambda ap: _mitre(Wh, ap[hand])
    hd = lambda ah: _head(ZA + ah[hand])

    # ---- verge slab: the dark boarding + soffit under the verge -----------
    # y1 stops short of T so finish() never clamps the slab flat onto the inner
    # plane (it used to overshoot by 17 mm, and the crushed faces fought).
    # It stops AP_SLAB short of the apex: it is a box, so it cannot take the
    # angled cut the bands get, and running it to L drove one rake's boarding
    # through the other's right under the finial.
    #
    # IT NO LONGER CARRIES SHINGLES. It used to be capped with two courses of its
    # own, laid at v = -0.02 -- i.e. 85 mm BELOW the level roofs.py's field
    # actually sits at (course butts at BUILD = 0.063). Since assemble_inn runs
    # the field right out to y = -VERGE_OVER, those courses were buried inside
    # the slope panels' own boarding along the whole rake: invisible, ~720 tris on
    # the 3-bay, and the only coincident surface check_zfight could find in this
    # family (43 cm2, shingle_moss against shingle_moss). The field is the roof;
    # this piece's job is to close its edge, not to re-lay it.
    #
    # ITS FOOT IS TAPERED OUT, AND ITS TOP BITES INTO THE ROOF'S OWN BOARDING.
    # Both are the bell-cast. As a plain box running to u = -0.09 with its top
    # edge 20 mm under the NOMINAL roof plane, the slab was 0.14 m below the real
    # (flared) eave soffit by the time it got there, and its square end read as a
    # loose dark block hanging off the corner of every verge -- rendered from
    # below it is the most obvious thing at the foot. It is a prism in (u, v) now
    # rather than a box, which costs nothing and lets the foot die out: the
    # underside rises to meet the boarding over SLAB_TAP of rake and the last
    # 0.10 m of the flare is left to roofs' own soffit, which is already there.
    # The top edge is lifted so it runs 30 mm INTO that 0.05 m boarding (which
    # sits at v = -0.050 .. +0.002) instead of stopping 2 mm short of it.
    y0, y1 = Y_SLAB
    su = L - AP_SLAB[hand]
    vt, vb = -.020, -.020 - (RT - .035)
    s.prism([(SLAB_U0, vt), (su, vt), (su, vb), (SLAB_U0 + SLAB_TAP, vb)],
            y1 - y0, "oak_dark", axis='Y', at=(0, (y0 + y1) / 2, 0), bevel=.012,
            seg=1, tint=.04, shade=.52)

    # ---- dark soffit web: closes the slot behind a board this deep, and gives
    # the verge the black shadow-line it has in every reference -------------
    # 24 mm SHORT of the plank's lower edge, deliberately: at -0.5w + 0.36w with
    # width 0.72w the web's lower edge landed on exactly the same plane as the
    # plank's, and those two faces overlap along the whole rake -- 110 cm2 of the
    # 151 cm2 check_zfight measured on this piece.
    # It rides the SWEPT lower edge too (dn = hlo - .024), so it stays 24 mm
    # inside the board at the foot instead of dropping out of the back of it once
    # the board narrows.
    _band(s, mid, [w * .22 for w in wid], "oak_dark", Y_WEB,
          dn=[h - .024 for h in hlo], bevel=0, tint=.03, shade=.42,
          cut=(mt(AP_WEB), _stop(FOOT_STOP[4]), fz(4)))

    # ---- THE RAKE BOARD: one broad plank, welded to the kerb along its top
    # edge and SWEPT UP along its lower one, MITRED on the ridge plane at its
    # head and cut level at its foot ----------------------------------------
    _band(s, mid, [w / 2.0 for w in wid], "oak_dark", Y_PLANK, dn=hlo,
          bevel=.011, tint=.055, shade=1.08,
          cut=(mt(AP_PLANK), hd(AP_HEAD_PLANK), fz(0)))

    # ---- bold ogee moulding worked along the lower edge (two steps of relief
    # read as a cyma section and throw two hard shadow lines) --------------
    # The two rolls overlap each other by 20 mm and sit 14 mm apart in Y: they
    # used to abut edge to edge on one plane AND share their back plane, which
    # was ~4000 cm2 of fighting along both rakes. The lower roll also keeps
    # 10 mm clear of the board's own lower edge for the same reason.
    # Anchored to `hlo`, not to -w/2, so the moulding follows the swept edge to
    # the drip instead of being left behind under it.
    #
    # PULLED DOWN ONTO THE EDGE, AND NARROWED. This is the other half of the
    # corduroy (see the DENT note): the pair used to run +0.010 .. +0.180 above
    # the board's lower edge -- 170 mm of a 335 mm board, so with the cap bead
    # above them 270 mm of the face was moulding and 55 mm was board, and the
    # two rolls read as two more stripes ACROSS the face rather than as one
    # section worked ON the edge. Measured off ref3 at 15x ((935,340)-(995,420))
    # the reference carries ONE narrow roll between the toothed edge and the
    # plank, about 0.20 of the board's face -- 67 mm here. Held at two steps
    # (the cyma is authored, and two shadow lines at the edge is what makes it
    # read as a moulding rather than a chamfer) but tightened to +0.010 ..
    # +0.134, i.e. 124 mm instead of 170: the roll's lower edge does not move at
    # all, so nothing about the fringe, the foot scroll or the swept edge
    # changes, and 80 mm of plain plank opens up between the moulding and the
    # dentil row where there used to be 20 mm.
    _band(s, _off(mid, [-h + .049 for h in hlo]), .078, "oak_mid", Y_OGEE,
          bevel=0, tint=.05, shade=1.16,
          cut=(mt(AP_ROLL), _stop(FOOT_STOP[3]), fz(3)))
    _band(s, _off(mid, [-h + .101 for h in hlo]), .066, "oak_mid", Y_STEP,
          bevel=0, tint=.05, shade=1.02,
          cut=(mt(AP_STEP), _stop(FOOT_STOP[2]), fz(2)))

    # ---- THE KERB LIP. This is the piece that closes the roof edge, and it is
    # the whole answer to "the wood goes straight out from the shingles".
    # It is 80 mm thick in Y and its top edge is the highest thing on the rake
    # (VERGE_LAP, 60 mm over the proudest measured field tab), so:
    #   * its INNER face at y = -0.240 stands 60 mm INSIDE the field's cut plane
    #     at y = -VERGE_OVER: every course's cut end dies inside this solid, and
    #     since the lip runs from v = VERGE_LAP down to VERGE_LAP - LIPW it is
    #     solid right through the courses and down into the boarding, so nothing
    #     can poke past it however the field wanders;
    #   * the 60 mm of it that stands above the field is a real riser, which is
    #     the shadow line down the rake that the old flat cap had nowhere to put.
    # Mitred on the ridge plane at its own (deep) insets -- see AP_LIP.
    # Shaded well DOWN (.72, against the board's 1.08): the lip's top face looks
    # at the sky like the roof does, so at the same shade as the board it came
    # back as another lit plank lying in the field. Dark, it reads as the shadowed
    # top edge of a board -- which is exactly the line ref3's linework draws
    # between shingle and bargeboard.
    _band(s, lip, LIPW, "oak_dark", Y_LIP, bevel=.016, tint=.04, shade=.72,
          cut=(mt(AP_LIP), hd(AP_HEAD_LIP), _stop(FOOT_STOP[0]), fz(1)))

    # ---- THE DENTIL LADDER on the board's FACE, CAP_DROP below its top edge.
    # This line used to carry a continuous 100 mm oak_mid BEAD, and the bead was
    # one of the five parallel stripes that made the verge read as corduroy from
    # the street -- see the DENT note for the measured section and for what the
    # references actually draw here. Same line, same Y layer (Y_CAP), so the
    # piece stands not one millimetre prouder for it: the blocks bite 48 mm into
    # the plank and stand 26 mm off its face, exactly as the bead did, and the
    # outermost plane in the piece is still the foot scroll's at -VO - 0.146.
    #
    # Walked in ARC LENGTH along the line, not in u, so the pitch stays even
    # through the bell-cast where the section is swinging -- same walk as the
    # fringe, for the same reason.
    u_cap = L + AP_CAPU[hand]
    lad = [q for u, q in zip(us, _off(mid, [w / 2.0 - CAP_DROP - DENT_D / 2.0
                                            for w in wid])) if u < u_cap]
    # The last point is at the apex, where the rake is dead straight and the
    # normal offset and the vertical drop are the same thing.
    vt_end, w_end = _barge_profile(u_cap)
    lad.append((u_cap, vt_end - LIP_DROP - CAP_DROP - DENT_D / 2.0))
    larc = [0.0]
    for i in range(1, len(lad)):
        larc.append(larc[-1] + sqrt((lad[i][0] - lad[i - 1][0]) ** 2 +
                                    (lad[i][1] - lad[i - 1][1]) ** 2))
    lfr = _frames(lad)
    lcut = _mitre(Wh, POST_W / 2 - DENT_BURY)      # the plane the row dies on
    d_at = 0.0
    for i in range(1, len(lad)):
        if lad[i][0] >= DENT_U0:
            f = clamp((DENT_U0 - lad[i - 1][0]) /
                      max(lad[i][0] - lad[i - 1][0], 1e-6))
            d_at = lerp(larc[i - 1], larc[i], f) + DENT * .5
            break
    k = 1
    while d_at < larc[-1]:
        while k < len(larc) - 1 and larc[k] < d_at:
            k += 1
        f = (d_at - larc[k - 1]) / max(larc[k] - larc[k - 1], 1e-6)
        pu = lerp(lad[k - 1][0], lad[k][0], f)
        pv = lerp(lad[k - 1][1], lad[k][1], f)
        tu = lerp(lfr[k - 1][0], lfr[k][0], f)
        tv = lerp(lfr[k - 1][1], lfr[k][1], f)
        m = sqrt(tu * tu + tv * tv) or 1.0
        tu, tv = tu / m, tv / m
        bw = DENT_W * .5 * (1 + r.uniform(-.06, .06))
        bd = DENT_D * .5 * (1 + r.uniform(-.05, .05))
        poly = [(pu + tu * a - tv * b, pv + tv * a + tu * b)
                for (a, b) in ((-bw, -bd), (bw, -bd), (bw, bd), (-bw, bd))]
        clipped = _clip_half(poly, lcut)
        if len(clipped) < 3 or _area(clipped) < DENT_KEEP * _area(poly):
            break
        s.prism(clipped, Y_CAP[1] - Y_CAP[0], "oak_mid", axis='Y',
                at=(0, sum(Y_CAP) / 2, 0), bevel=0, seg=1, tint=.06,
                shade=1.16 + r.uniform(-.09, .07))
        d_at += DENT * (1 + r.uniform(-.04, .04))

    # ---- pendant dentils hung off the ogee, walked by arc length so the
    # spacing stays even round the swept foot ------------------------------
    arc = [0.0]
    for i in range(1, len(low)):
        arc.append(arc[-1] + sqrt((low[i][0] - low[i - 1][0]) ** 2 +
                                  (low[i][1] - low[i - 1][1]) ** 2))
    fr = _frames(low)
    # The fringe walks up the board's lower edge and stops where that edge
    # reaches the apex block: AP_FRINGE short of the ridge plane in world x, so
    # the last tooth dies against the post's flank. It used to stop a fixed 0.36
    # of arc short of the last station, which meant nothing once the stations
    # changed -- the teeth ran straight into the crossing and one rake's
    # pendants landed on top of the other's.
    # It STARTS above the swept foot. Now that the board runs down to the drip,
    # its lower edge through the bell-cast is swinging up at ~45 deg, and a
    # pendant hung on it there points out along the eave instead of down. The
    # scroll is what finishes the board at the foot, exactly as it does in ref2 --
    # scallops on the straight run, a carved boss where it lands.
    lim = Wh - AP_FRINGE
    d_at = .055
    for i in range(1, len(low)):
        if low[i][0] >= FRINGE_U0:
            f = clamp((FRINGE_U0 - low[i - 1][0]) /
                      max(low[i][0] - low[i - 1][0], 1e-6))
            d_at = lerp(arc[i - 1], arc[i], f) + .040
            break
    k = 1
    while d_at < arc[-1]:
        while k < len(arc) - 1 and arc[k] < d_at:
            k += 1
        f = (d_at - arc[k - 1]) / max(arc[k] - arc[k - 1], 1e-6)
        pu = lerp(low[k - 1][0], low[k][0], f)
        pv = lerp(low[k - 1][1], low[k][1], f)
        if pu * COSP - pv * SINP > lim:
            break
        tu = lerp(fr[k - 1][0], fr[k][0], f)
        tv = lerp(fr[k - 1][1], fr[k][1], f)
        m = sqrt(tu * tu + tv * tv) or 1.0
        tu, tv = tu / m, tv / m
        w = CUSP * .78 * (1 + r.uniform(-.05, .05))
        # THE PENDANTS SHORTEN INTO THE SCROLL. The deepest tooth on the whole
        # rake used to be the FIRST one, hung at full DAG off the fattest part of
        # the swell: measured on the assembled inn it was the single worst vertex
        # in the piece for clearance from the roof (0.485 m on the 2-bay, 0.456 on
        # the 3-bay -- both of them this tooth, not the foot). It is also the one
        # place the fringe has to give way, because the board under it is
        # narrowing into the scroll. Faded to DAG_MIN over DAG_FADE of rake the
        # row dies into the boss the way a carved fringe does.
        d = DAG * lerp(DAG_MIN, 1.0, clamp(pu / DAG_FADE)) \
            * (1 + r.uniform(-.07, .09))
        tip = (pu - tv * (-d * .97), pv + tu * (-d * .97))
        if tip[0] * SINP + tip[1] * COSP < Z_FOOT:
            d_at += CUSP * (1 + r.uniform(-.03, .03))
            continue
        s.prism([(pu + tu * a - tv * b, pv + tv * a + tu * b)
                 for (a, b) in _cusp_poly(w, d)], Y_DAG[1] - Y_DAG[0],
                "oak_dark", axis='Y', at=(0, sum(Y_DAG) / 2, 0), bevel=0, seg=1,
                tint=.06, shade=1.04 + r.uniform(-.10, .08))
        d_at += CUSP * (1 + r.uniform(-.03, .03))

    # ---- THE SCROLL AT THE FOOT, AND IT BEARS ON SOMETHING NOW ------------
    # It is drawn in the board's own end-section frame -- `a` up the rake from
    # the end cut, `b` across the section from the centreline -- which at the
    # foot is all but a world elevation (t.z = +0.079, n.z = +0.997), so the
    # BOSS table above is readable as a drawing and its numbers can be checked
    # straight against the measured eave. What changed and why:
    #
    #   * IT IS ANCHORED TO `mid`, NOT TO `low[0]`. The old boss hung off the
    #     board's lower CORNER, so it inherited the dive: every millimetre the
    #     lower edge fell through the flare, the scroll fell with it. Anchored
    #     to the centreline it stays where the board's section is, and the
    #     LOWSWEEP fix lifts the corner out from under it instead.
    #   * IT IS SMALLER: 0.32 x 0.37 of section against 0.38 x 0.52, i.e. 40 %
    #     less area, and its lowest point is 0.018 m under the board's lower
    #     edge instead of 0.15 m under the eave.
    #   * IT STAYS INSIDE THE ROOF IT TERMINATES: u_min -0.386 against the
    #     measured drip at U_DRIP = -0.399, x_min -0.471 against an eave that
    #     reaches -0.50, z_min -0.216 against Z_EAVE = -0.151 and the board's
    #     own lower edge at -0.222.
    #   * its up-rake edge (a = 0.238) runs the full depth of the section, so
    #     the whole of that edge is bearing on the board, and it still swallows
    #     the kerb lip's square end at the top (b = 0.266..0.284 against the
    #     lip's own 0.249) -- which is what the old boss was made tall for.
    #
    # The two clips are belt and braces: the polygon is authored inside them, and
    # _clip_half proves it on every build rather than trusting the table.
    if tail:
        tu, tv, nu, nv = _frames(mid)[0]
        mu, mv = mid[0]
        Pb = lambda a, b: (mu + tu * a + nu * b, mv + tv * a + nv * b)
        poly = [Pb(a, b) for (a, b) in BOSS]
        poly = _clip_half(poly, _foot(Z_FOOT))
        poly = _clip_half(poly, lambda q: U_DRIP - q[0])
        if len(poly) > 2:
            s.prism(poly, Y_TAIL[1] - Y_TAIL[0], "oak_dark",
                    axis='Y', at=(0, sum(Y_TAIL) / 2, 0), bevel=.014, seg=1,
                    tint=.05, shade=1.02)
    return raw


def _barge(bays):
    W = bays * G
    ZA = apex_z(bays)
    L = (W / 2) / COSP
    name = f"SM_Gable_Barge_{bays}bay"
    # Deliberate seam-spanning trim: it hangs below the rake feet and swings
    # outboard of them, and that is declared here rather than clamped away.
    # EVERY BOUND IS NOW 10-20 mm OFF THE MEASURED EXTENT, which is the point:
    # the declaration is the piece's own claim about how far it hangs, so it has
    # to move when the geometry does. Measured on the built meshes:
    #     x  +-(W/2 + 0.470)   z  -0.223 .. ZA + 0.155   y  -0.4475 .. +0.229
    # z-min was declared -0.46 while the foot really reached -0.345, and after
    # the swept-foot fix it reaches -0.223: a bound 0.24 m below anything in the
    # piece is not a bound, it is a licence. Tightened, `check()` fails the build
    # the next time something is left hanging under the eave.
    # AND THE Y BOUND IS WRITTEN OFF VERGE_OVER, NOT AS A LITERAL. It was
    # y=(-.458, T), a number tuned to VERGE_OVER = 0.30 while every layer of the
    # assembly is an offset from -VERGE_OVER. Measured, by overriding
    # spec.VERGE_OVER in memory and rebuilding this piece (spec.py untouched):
    #     VERGE_OVER 0.30   y_min -0.4474   0.147 m proud of the tile cut
    #     VERGE_OVER 0.45   y_min -0.5982   0.148 m proud of the tile cut
    #     VERGE_OVER 0.60   y_min -0.6180   0.018 m proud  <-- CRUSHED
    # The third row is not the piece behaving: -0.618 is the declared seam
    # (-0.458) plus the default PROUD_MAX slack (0.16), so clamp_to_seams was
    # flattening the ogee roll, the dentil ladder, the pendant fringe and the foot
    # scroll onto ONE plane -- a guaranteed z-fight, arriving silently, the
    # moment VERGE_OVER went past ~0.46. Anchored to VO the bound tracks the
    # verge it belongs to and the piece stays honest at any overhang:
    #     -(VO + .158) = -0.458 at VERGE_OVER 0.30, i.e. today's number exactly.
    p = _Fix(Part(name, budget="gable",
                  seams=dict(x=(-(W / 2 + .48), W / 2 + .48),
                             y=(-(VO + .158), T),
                             z=(-.24, ZA + .17))))
    # left rake: local +X -> up-right along the rake, mitred on the ridge plane
    p.merge(_rake_assembly(p, name, L, 1, hand=0), at=(-W / 2, 0, 0),
            rot=(0, -PD, 0))
    # right rake: mirrored, so the two sides are not clones, set RAKE_LAP inboard
    # and mitred at its own (different) insets, so no face of one rake is ever
    # on a plane with the same face of the other
    p.merge(_rake_assembly(p, name, L, 2, hand=1), at=(W / 2, RAKE_LAP, 0),
            rot=(0, PD, 0), mirror='X')

    # ---- THE APEX. The two rake boards now LAP across the ridge plane and are
    # cut off square under the block (AP_* table), so there is no slot to plug
    # and no head to swallow: the block is a SHORT king-post head bearing on both
    # boards, with a moulded stop at its foot and the saddle over it, carrying
    # the finial. ref3's apex exactly -- and, unlike the 0.87 m slab that was
    # here, every part of it is standing on timber.
    p.box((0, sum(POST_Y) / 2, ZA + sum(POST_Z) / 2),
          (POST_W, POST_Y[1] - POST_Y[0], POST_Z[1] - POST_Z[0]), "oak_dark",
          bevel=.014, seg=1, tint=.05, shade=1.02)
    # a moulded stop at the post's foot: the block's lower end finishes against
    # the boards with a moulding, the way a real king-post head is stopped,
    # instead of a blunt cut hanging over the tympanum
    # Its y faces are set 30 and 35 mm inside the post's own, not 14 mm: at
    # 14 mm the inboard pair came within 0.2 mm of each other once wobble had
    # moved them, and check_zfight measured 25 cm2 of fighting on it.
    p.box((0, (POST_Y[0] + .030 + POST_Y[1] - .035) / 2,
           ZA + POST_Z[0] + .028),
          (POST_W + .046, (POST_Y[1] - .035) - (POST_Y[0] + .030), .076),
          "oak_mid", bevel=.012, seg=1, tint=.05, shade=.92)
    # the saddle: it swallows both cap-bead heads and the top of both mitres,
    # and carries the finial. 42 mm proud of the post's own face, so the two
    # never share a plane.
    p.box((0, sum(SAD_Y) / 2, ZA + sum(SAD_Z) / 2),
          (SAD_W, SAD_Y[1] - SAD_Y[0], SAD_Z[1] - SAD_Z[0]), "oak_mid",
          bevel=.020, seg=2, tint=.05, shade=1.12, taper=.86, taper_axis='XY')
    p.wobble(.006, freq=1.3, respect_seams=False)
    return p.finish()


# ------------------------------------------------------------- ridge comb ----
# WHERE THIS PIECE SITS ON A REAL ROOF, and it is not a guess: roofs.py's header
# states it. "RIDGE: ridge along X, origin ON the ridge line, Z = 0 there -- the
# same frame as gables.ridge_comb, so the two swap. It LAPS the field (its
# underside sits at t = BUILD + 0.008, clear of the highest course butt) instead
# of replacing it, so a slope panel may run its top course right up to the
# ridge." BUILD there is LIFT + THICK = 0.45*RELIEF + THICK = 0.0632, the height
# of a shingle course's butt above the roof boarding. So:
ROOF_LAP = 0.0712        # underside of ridge trim, measured along the NORMAL out
                         # of the nominal 52 deg roof plane. The same number
                         # roofs.ridge() uses, so SM_Gable_RidgeComb_2m and
                         # SM_Roof_Ridge_2m are interchangeable on one ridge
                         # with no step where a level artist swaps them.


def _surf(sgn, s, t):
    """(y, z) of a point on the roof surface frame of this family's ridge pieces:
    `s` runs DOWN the `sgn` slope from the ridge line, `t` stands out of the roof
    along its normal. Ridge along X, origin on the ridge line, so s = t = 0 is
    the origin and the nominal 52 deg plane is t = 0."""
    return (sgn * (s * COSP + t * SINP), -s * SINP + t * COSP)


def ridge_comb():
    """Dentil cresting for the ridge: runs back from a gable apex along the
    ridge, tiling at GRID. Ridge along X, origin on the ridge line, on the roof
    plane -- roofs.ridge()'s frame exactly, so the two pieces swap.

    IT CARRIES NO SHINGLES OF ITS OWN, and that is the fix, not an omission. It
    used to bring two courses up each slope and they were wrong twice over.
    Their box centres did follow the 52 deg line, but each box was tilted
    PITCH*0.55 = 28.6 deg, so no course lay IN the roof plane; and because the
    centres stepped at 52 deg while the boxes lay at 28.6, consecutive courses
    could not overlap -- the outer course (16 boxes) hung with a 90 mm slot
    above it, touching nothing whatever in the piece, and on a real roof it
    would have floated over the slope or punched through it depending on where
    the comb landed. Bedding them on the plane would not have saved them
    either: the roof's own field runs its top course right up to the ridge line
    UNDER this piece (roofs.slope / roofs.eave), so a course here is a second
    roof surface in the same place -- and the header quoted above is explicit
    that ridge trim laps that field rather than duplicating it. So the courses
    are gone and the piece beds on the real thing instead: both saddle boards
    sit at t = ROOF_LAP out of the 52 deg plane, exactly where roofs.ridge()
    puts its own, and every solid here is buried in its neighbour.
    """
    p = _Fix(Part("SM_Gable_RidgeComb_2m", budget="gable",
                  seams=dict(x=(-G / 2, G / 2), y=(-.30, .30), z=(-.22, .40))))
    r = rng("ridgecomb")
    # The saddle, laid out in the roof surface frame (see _surf): a board laid on
    # each slope with a batten showing along its lower edge. ref3's ridge is that
    # two-line band, and it is the same pair roofs.ridge() lays at the same two
    # heights, so the band runs on unbroken through a swap.
    # BD is roofs.ridge()'s own board width, not a number of our own: a run that
    # mixes the two pieces then shows one continuous band with no step in it.
    # BD and BTH are roofs.ridge()'s own numbers, not ours -- a ridge run that
    # mixes SM_Gable_RidgeComb_2m with SM_Roof_Ridge_2m must show one continuous
    # band with no step in it. BTH went 0.056 -> 0.080 with roofs.ridge, so the
    # board's outer face clears the field's PROUDEST tab (a curled or wobbled one
    # reaches ~0.088, and assemble_inn's RIDGE_S = 0.62 shrinks a ridge cap's
    # stand-off to 0.713x while stretching the field's relief by 1.302) instead
    # of only its mean. The underside stays on ROOF_LAP, so nothing opens up
    # along the board's lower edge.
    BS0, BD, BTH = -.010, .255, .080       # board: s of its head, s width, thick
    for sgn in (-1, 1):
        # The OUTWARD NORMAL of this slope, which is what beam() lays its cross
        # section against. Note the z term does NOT flip with the slope: it is
        # (0, +-SIN, +COS), and it used to be written (0, +-SIN, +-COS) -- for the
        # -Y slope that vector points DOWN INTO the roof, so beam() built that
        # board with the OTHER slope's tilt, 76 deg out of the plane it is
        # supposed to lie on. It was invisible while the boards were buried in
        # the fake shingle courses; with them gone the -Y board missed the apex
        # roll altogether, which is how it was caught.
        up = (0.0, sgn * SINP, COSP)
        yc, zc = _surf(sgn, BS0 + BD / 2, ROOF_LAP + BTH / 2)
        p.beam((-G / 2, yc, zc), (G / 2, yc, zc), BD, BTH, "oak_mid", up=up,
               bevel=.012, seg=1, tint=.05, shade=.95)
        # the batten: buried 13 mm into the board's outer face (so the board
        # carries it) and standing 37 mm proud of it, which is the dark second
        # line of ref3's ridge band. It keeps 14 mm clear of the board's lower
        # edge so no two of their planes come near each other.
        yc, zc = _surf(sgn, BS0 + BD - .052, ROOF_LAP + BTH + .012)
        p.beam((-G / 2, yc, zc), (G / 2, yc, zc), .075, .050, "oak_dark", up=up,
               bevel=.010, seg=1, tint=.05, shade=.78)
    # The roll over the apex, bridging the two boards' heads. Its lower corners
    # land 16 mm under each board's outer face and 26 mm inboard of its head, so
    # roll and boards are one solid assembly; before this it stood 20 mm clear of
    # both of them with the pegs balanced on top.
    ROLL_T, ROLL_H = .056, .094            # underside z at the ridge, height
    p.box((0, 0, ROLL_T + ROLL_H / 2), (G, .196, ROLL_H), "oak_pale",
          bevel=.016, seg=2, tint=.05, shade=1.05)
    # the pegs, standing on that roll, 20 mm inside its top face
    n = int(round(G / .225))
    pz = ROLL_T + ROLL_H - .020
    for i in range(n):
        cx = lerp(-G / 2, G / 2, (i + .5) / n)
        w = .105 * (1 + r.uniform(-.05, .05))
        h = .175 * (1 + r.uniform(-.07, .07))
        p.prism([(a + cx, b + pz) for (a, b) in _peg_poly(w, h)], .105,
                "oak_pale", axis='Y', at=(0, r.uniform(-1, 1) * .006, 0),
                bevel=.007, seg=1, tint=.06, shade=1.0 + r.uniform(-.10, .08))
    # x is the only axis this piece tiles on, so it is the only one wobble has to
    # leave flat; fading z as well left the boards' lower edge stiff.
    p.wobble(.005, freq=2.0, axes="x")
    p.sag(.014, axis='x', span=(-G / 2, G / 2))
    return p.finish()


# ----------------------------------------------------------- window frame ----
def win_frame():
    """THE INSERT that fills a `win_attic` opening: frame, glass, leading, and
    the bead that holds the pane. Origin at the bottom-centre of the opening, on
    the wall face; `at=(0, 0, SILL_Z[bays])` on any gable end in this file.

    IT IS BOUNDED TO THE HOLE, AND THE BOUND IS THE SEAMS.
    x in [-IW/2, IW/2] = [-0.240, 0.240], z in [0, IH] = [0, 0.540] -- the
    0.520 x 0.580 opening less INSERT_CLEAR all round -- declared as this Part's
    seams so `check()` proves the fit on every build. Round 14's piece measured
    0.819 x 1.044 and lapped 37-44 mm of wall on every side, and everything that
    made it that big has moved to the gable end where it belongs: the projecting
    cill, its two corbels, the label mould and the carved crest. See the note by
    IW/IH for the four collisions that came out of carrying them here.

    WHAT IS LEFT IS Part.glazing() AND A BEAD, and the bead is the answer to the
    fourth fault. Measured on round 14's piece: "glazed light touches nothing --
    0 contacts with any frame member, the pane 55 mm behind the frame". That is
    not a bug in the call, it is the shape of the primitive: glazing() lays its
    frame at `depth - 2.6*lead - 0.055 .. depth - 2.6*lead` and its pane at
    `depth +/- 0.006`, so there is ALWAYS 2.6*lead - 6 mm of pure air between the
    back of the frame and the face of the glass, and no argument closes it. A
    real window closes it with the glazing bead that beds the pane into the
    rebate, so this piece builds one: a ring lapping 14 mm INTO the frame's
    rebate at the front and 6 mm INTO the pane at the back, which is why the
    light now reads as glass held in timber instead of a picture hung behind a
    hole. Every one of its planes is 12 mm or more off every plane it laps.

    THE DEPTH LADDER, and every number in it is pinned by something:
        y  0.004 .. 0.059   frame          (glazing()'s own 55 mm section, its
                                            face 4 mm inside the hole)
        y  0.045 .. 0.103   BEAD           (laps the frame, laps the pane)
        y  0.079 .. 0.094   leading        (buried in the bead round the rim)
        y  0.097 .. 0.109   glass
    The back of that stack is fixed by the WALL: the gable end backs its reveal
    with a dark pane at Y_PANE, whose front is y = 0.146, so the glass has 36 mm
    of air behind it and both pieces' wobble together cannot close it. The front
    is fixed by the gable's own framing: the jamb posts stand at y = -0.032 and
    the plaster panels sit back at y = 0.035, so a frame face at 0.004 is nested
    between the two, which is what "seated in the reveal" means here."""
    p = _Fix(Part("SM_Gable_WinFrame", budget="window",
                  seams=dict(x=(-IW / 2, IW / 2), y=(0.0, T), z=(0.0, IH)),
                  proud=0.03))
    # ---- the frame section, and why the aperture is what it is.
    # glazing()'s head and sill span `aperture + 2*(frame+overlap)` and its jambs
    # span `aperture + 2*(frame+overlap)` in z, so the OUTER size of the whole
    # unit is aperture + 2*FO exactly. Turn that round -- aperture = envelope -
    # 2*FO -- and the unit fills the insert box to the millimetre instead of
    # overrunning it, which is the arithmetic round 14 never did.
    FR, OVL = .050, .010
    FO = FR + OVL                       # 0.060
    AW, AH = IW - 2 * FO, IH - 2 * FO   # 0.360 x 0.420 of glazed light
    CZ = IH / 2                         # 0.270
    # LEAD is 17 mm. glazing() stands the bars 0.55*lead in front of the pane's
    # own face, so the clear air there is 0.55*lead - 6 mm = 3.4 mm, which
    # measures 4.7 mm once this piece's wobble has run (the field is smooth, so
    # bar and pane take nearly the same displacement). It
    # cannot go far below this (the gap closes) and it cannot go far above,
    # because REB has to out-run 2.6*lead and REB is what decides how far the
    # pane oversails the frame -- see the note on the bead's outer edge.
    LEAD = .017
    # REB is pinned from both sides, like windows.py's: it must out-run
    # glazing()'s own reveal (glass face to frame back = 2.6*lead - 6 mm = 38.2
    # mm) or an oblique view finds frame where glass should be, and it must stay
    # under the frame's reach (FR + OVL/2 = 55 mm) or the pane's lip shows past
    # the frame's outer edge. 38.5 mm sits between them, hard against the first
    # bound, because the SMALLER it is the less pane there is for the bead to
    # have to cover -- see the bead's outer edge below.
    REB = .0385
    assert REB >= LEAD * 2.6 - .006, "pane rebate must out-run glazing()'s reveal"
    assert REB <= FR + OVL / 2 - .001, "pane lip must stay buried under the frame"
    Y_F0 = .004                         # front face of the frame
    DEPTH = Y_F0 + .055 + LEAD * 2.6    # -> the pane's centre plane
    # `cell` divides glazing()'s own bar reach (gw + gh) exactly NINE ways. It has
    # to be an exact divisor or nothing lands on a centre line -- glazing() walks
    # its bars out from -(gw + gh) -- and it has to be THIS divisor because the
    # BEAD, not the frame, bounds the light the eye actually sees: at 0.1036 the
    # bars fall at 0 and +/-0.1036, four columns and four rows inside the bead's
    # 0.320 x 0.380 aperture, and the next pair out is hidden behind the bead
    # itself. At (gw + gh)/7 the outer pair landed 19 mm inside that aperture and
    # the light read as 3 x 3 lights with a sliver round the edge. No `mullions`:
    # a mullion would sit on the same centre line as a bar and run the height of
    # the light 5 mm in front of it.
    gw, gh = AW + 2 * REB, AH + 2 * REB
    p.glazing((0.0, 0.0, CZ), (AW, AH), depth=DEPTH, frame=FR, rebate=REB,
              lead=LEAD, cell=(gw + gh) / 9.0, pattern="square", overlap=OVL,
              mat_frame="oak_mid", mullions=0, transoms=0, tint=.045)
    # ---- THE GLAZING BEAD. It bites 14 mm into the frame's rebate at the front
    # and 6 mm into the pane at the back, so frame, bead and glass are ONE
    # continuous solid stack with no air anywhere in it, and it stands 20 mm into
    # the light on every side -- the contact shadow that tells the eye the pane
    # is bedded rather than floating.
    #
    # ITS OUTER EDGE IS SET BY THE PANE, NOT BY THE FRAME. glazing() cuts the
    # pane REB oversize, so the pane reaches AW/2 + REB while the frame's JAMB
    # only reaches AW/2 + FR + OVL/2, and the pane lies 38 mm behind the jamb.
    # Sight down the light from 14 degrees off axis -- which is what a gable is
    # normally seen from -- and the line of sight clears the jamb's inner arris
    # 11 mm out at the pane's depth, so every millimetre of pane between the
    # bead's outer edge and the jamb's shows as a lit strip of bare glass. At
    # bo_x = AW/2 + 0.016 that strip was 34 mm wide and read as a crack of
    # daylight down the side of the window. The bead now oversails the pane by
    # 4 mm instead, which is what a bead does, and it is still 12 mm clear of
    # both of the jamb's own planes.
    #
    # The bead's back face stops on the pane's CENTRE plane, not on its back one:
    # at DEPTH + 0.006 the two are the same plane to a tenth of a millimetre, and
    # check_zfight scored 91 cm2 of glass lying on oak_dark straight down the
    # middle of the light. On the centre plane it is 6 mm off both of the pane's
    # own faces and still laps it properly.
    #
    # Head and sill run the full width; the jambs stop 53 mm short of the outer
    # corner and LAP them by 10 mm. Run full height instead they would lap over
    # the whole 63 x 63 corner -- 40 cm2 of coincident front face per corner,
    # nearly three times what check_zfight counts. At 63 x 10 it is 6 cm2.
    BY = (.045, DEPTH)                             # 0.045 .. 0.103
    bi_x, bo_x = AW / 2 - .020, AW / 2 + .043      # 0.160 .. 0.223
    bi_z, bo_z = AH / 2 - .020, AH / 2 + .0425     # 0.190 .. 0.2525
    yb, db = sum(BY) / 2, BY[1] - BY[0]
    for sgn in (-1, 1):
        p.box((0.0, yb, CZ + sgn * (bi_z + bo_z) / 2), (2 * bo_x, db,
              bo_z - bi_z), "oak_dark", bevel=.006, seg=1, tint=.04, shade=.80)
        p.box((sgn * (bi_x + bo_x) / 2, yb, CZ), (bo_x - bi_x, db,
              2 * (bi_z + .010)), "oak_dark", bevel=.006, seg=1, tint=.04,
              shade=.80)
    # 2.2 mm, and BOTH bounds on it are measured. glazing()'s own head and jambs
    # lap in a 60 x 60 mm square at every corner -- 36 cm2 of coincident front
    # AND back face per corner, unavoidable, every family that calls the
    # primitive carries it -- and the only thing that breaks those planes is this
    # wobble: at 0.0012 check_zfight scored 58 cm2 across the two sill corners,
    # at 0.0022 it scores nothing. The other bound is the 3.4 mm the primitive
    # leaves between the leading and the pane. Those two are only compatible
    # because the noise field is SMOOTH: bar and pane are 3 mm apart in space, so
    # they take nearly the same displacement and the gap measures 2.7 mm at an
    # amplitude of 2.2 -- not 1.2, which is what independent jitter would give.
    p.wobble(.0022, freq=2.4, respect_seams=False)
    return p.finish()



# ----------------------------------------------------------------- finial ----
def finial():
    """The carved ridge/apex finial of ref2: turned shaft, lobed knop, a pair of
    swept arms and a spike. Origin at the footprint centre, Z=0 at the bottom."""
    p = _Fix(Part("SM_Gable_Finial", budget="beam",
                  seams=dict(x=(-.20, .20), y=(-.20, .20), z=(0, 1.16))))
    prof = [(.000, .000), (.105, .010), (.115, .105), (.080, .150),
            (.062, .200), (.098, .255), (.112, .310), (.070, .365),
            (.046, .430), (.040, .620), (.058, .690), (.044, .745),
            (.030, .800), (.036, .880), (.024, .935), (.000, 1.010)]
    p.lathe(prof, "oak_mid", at=(0, 0, 0), sides=9, tint=.05, shade=1.0)
    # arms: a flat carved plate, seen face-on from -Y like the painting
    arms = [(-.165, .830), (-.105, .905), (-.040, .878), (-.030, .955),
            (0.0, 1.150), (.030, .955), (.040, .878), (.105, .905),
            (.165, .830), (.075, .795), (.030, .820), (0.0, .760),
            (-.030, .820), (-.075, .795)]
    p.prism(arms, .062, "oak_pale", axis='Y', at=(0, 0, 0), bevel=.008, seg=1,
            tint=.05, shade=1.06)
    # collar rings
    for z, rr in ((.150, .085), (.365, .075), (.745, .050)):
        p.cyl((0, 0, z), rr, .034, "oak_pale", sides=9, bevel=.008, seg=1,
              tint=.05, shade=1.08)
    p.wobble(.004, freq=2.4, respect_seams=False)
    return p.finish()


# ------------------------------------------------------------------ build ----
def build():
    return [ridge_comb(),
            _end(2, "A"), _end(2, "B"), _end(2, "C"), _end(3, "A"),
            _barge(2), _barge(3), win_frame(), finial()]


# -------------------------------------------------- demo-only roof context ---
def _ctx_roof(bays, depth, name="CTX_Roof"):
    """DEMO CONTEXT ONLY -- not a kit piece. build() never returns it and nothing
    in the kit references it; roofs.py's demo does the same with its CTX_Walls.

    It is the pair of roof planes a gable end IMPLIES: they rise from the gable's
    own rake lines (the triangle's edges ARE those lines) to the ridge, and run
    `depth` back into the building. Drop it on with the SAME transform as its
    gable end and it lands on the rake by construction.

    It is here because ridge trim and rake boards can only be judged against a
    real 52 degree surface. This family shipped a ridge comb carrying a shingle
    course tilted 28.6 degrees with a 90 mm slot above it, and the demo render
    could not show that, because there was nothing under the ridge but sky.

    The field IS roofs.py's field, not an imitation of it: this calls
    roofs._field on roofs.FLAT, so the demo carries the real gauge, the real
    4-phase stagger, the real course step and the real per-tab curl and wobble.
    That matters because what is being judged along this edge is whether the rake
    board laps the PROUDEST tab of the actual roof, and a stand-in built with a
    different build-up cannot answer that. (Demo context only -- the import is
    local to this function so nothing in the kit's build path depends on it.)
    """
    from kit.pieces import roofs as R
    W = bays * G
    SL = (W / 2) / COSP                       # slope length, wall face to ridge
    ES = S.EAVE_OVER / COSP                   # 0.227 -- the drip, below the foot
    # The field runs out to y = -VO, which is where assemble_inn actually cuts
    # it: its roof run is (wall face - VERGE_OVER, wall face + VERGE_OVER), so on
    # the real building the tile ends land on the bargeboard's own plane, not
    # 60 mm inboard of it. The demo has to show that, because whether the barge
    # laps those tile ends is the thing being judged here.
    y0, y1 = -VO, depth
    p = _Fix(Part(name))
    for sgn in (-1, 1):
        ex = Vector((0.0, float(sgn), 0.0))           # along the ridge
        ey = Vector((-sgn * COSP, 0.0, SINP))         # up the slope
        ez = Vector((sgn * SINP, 0.0, COSP))          # out of the roof
        M = Matrix((ex, ey, ez)).transposed().to_4x4()
        foot = Vector((sgn * W / 2, (y0 + y1) / 2, 0.0))   # the gable's rake foot
        # THE DRIP IS BELOW THE FOOT, AND THE SURFACE IS BELL-CAST.
        # The ctx roof used to be R.FLAT run from the rake foot up, i.e. a roof
        # with no overhang and no swept eave -- so the demo could not show the
        # one junction this family is judged on. The real thing: assemble_inn
        # lays the slope out to half + EAVE_OVER, so the drip is ES of slope
        # BELOW the foot, and roofs' own surface flares over the bottom
        # SWEEP_LEN on spec.SWEEP. Putting the surface origin ES down the rake
        # LINE (where s = 0 is the drip and d(s) = 0 for s >= SWEEP_LEN) lands
        # every course above the flare exactly on the rake, as before, and gives
        # the bargeboard's foot the upturned eave it actually has to sit on.
        sf = R._Surf(sweep=S.SWEEP)
        org = foot + M @ Vector((0.0, -ES, 0.0))
        wid = y1 - y0
        # roofs._slab / _field build in ROOFS' OWN frame -- their tabs come out
        # already laid on the 52 deg slope (x along the ridge, +Y inboard/up-
        # slope, +Z up), not on a flat patch. So the sub-part is merged with the
        # rotation that turns that frame's slope direction onto THIS plane, which
        # works out to a plain 90 deg about Z; rotating by M as well would double
        # the pitch.
        f = R._Part(f"{name}_field{sgn}")
        R._slab(f, sf, -wid / 2, wid / 2, -0.085, SL + ES - .02, -R.SLAB, .002,
                n=9)
        R._field(f, sf, -wid / 2, wid / 2, 0.0, SL + ES - .04,
                 seed=f"ctx{bays}{sgn}")
        Mf = Matrix((ex, Vector((-float(sgn), 0.0, 0.0)),
                     Vector((0.0, 0.0, 1.0)))).transposed().to_4x4()
        p.merge(f, at=tuple(org), rot=Mf)
    return p.finish()


# ------------------------------------------------------------------- demo ----
def demo():
    """A roofscape, not a row: the big 3-bay front gable with its bargeboard,
    window frame and finial, its ridge combing marching back into depth, and a
    2-bay cross-wing gable set behind and to the side -- the same read as the
    top third of ref2. Each gable gets the two roof planes it implies as demo
    context (_ctx_roof), so the rake boards and the ridge combs are seen doing
    their job on a real 52 degree surface. The whole group is swung `YAW` degrees
    so the hero gable meets the demo camera at about the angle ref3 draws it
    from; end-on the rake board reads as a blade and its mass is the point of
    the family."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    src["CTX_Roof_3bay"] = _ctx_roof(3, 3.85, "CTX_Roof_3bay")
    src["CTX_Roof_2bay"] = _ctx_roof(2, 2.30, "CTX_Roof_2bay")
    out = []
    YAW = 13.0
    ca, sa = cos(radians(YAW)), sin(radians(YAW))

    def put(nm, at, rot=(0, 0, 0)):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = (at[0] * ca - at[1] * sa, at[0] * sa + at[1] * ca, at[2])
        o.rotation_euler = [radians(a) for a in (rot[0], rot[1], rot[2] + YAW)]
        out.append(o)
        return o

    def on(base, yaw, off):
        """World position of a point given in the LOCAL frame of a gable placed
        at `base` with yaw `yaw`. The combs and finials used to carry hand-fitted
        world offsets, which put the rear gable's comb 0.12 m off its own ridge
        -- invisible until the roof planes above arrived under it."""
        c, s = cos(radians(yaw)), sin(radians(yaw))
        return (base[0] + off[0] * c - off[1] * s,
                base[1] + off[0] * s + off[1] * c, base[2] + off[2])

    Z3, Z2 = apex_z(3), apex_z(2)

    # --- main gable, facing -Y ------------------------------------------
    m = (0.0, 0.0, 0.0)
    put("CTX_Roof_3bay", m)
    put("SM_Gable_End_3bay_A", m)
    put("SM_Gable_Barge_3bay", m)
    put("SM_Gable_WinFrame", on(m, 0, (0, 0, SILL_Z[3])))
    put("SM_Gable_Finial", on(m, 0, (0, -VO + .03, Z3 + SAD_Z[1] - .022)))
    # The comb is 2 m long about its own origin, so the first one goes at
    # -VO + G/2: its outboard end then lands exactly on the tile-end plane
    # (y = -VERGE_OVER), which is where assemble_inn's spans() cuts the ridge
    # run. It used to start at 0.34 and overshoot the bargeboard by 0.36, so the
    # demo showed cresting marching out into the air past the apex block.
    for i in range(2):                       # ridge running back from the apex
        put("SM_Gable_RidgeComb_2m", on(m, 0, (0, -VO + G / 2 + G * i, Z3)),
            rot=(0, 0, 90))

    # --- cross wing: 2-bay gable, turned 90deg, set back and lower -------
    w, wr = (-3.35, 1.30, 0.34), 90
    put("CTX_Roof_2bay", w, rot=(0, 0, wr))
    put("SM_Gable_End_2bay_B", w, rot=(0, 0, wr))
    put("SM_Gable_Barge_2bay", w, rot=(0, 0, wr))
    put("SM_Gable_WinFrame", on(w, wr, (0, 0, SILL_Z[2])), rot=(0, 0, wr))
    put("SM_Gable_Finial", on(w, wr, (0, -VO + .03, Z2 + SAD_Z[1] - .022)),
        rot=(0, 0, wr))
    for i in range(1):
        put("SM_Gable_RidgeComb_2m", on(w, wr, (0, -VO + G / 2 + G * i, Z2)),
            rot=(0, 0, wr + 90))

    # --- a third, smaller gable further back: reads as a rear range -------
    b, br = (2.80, 2.60, -0.30), -22
    put("CTX_Roof_2bay", b, rot=(0, 0, br))
    put("SM_Gable_End_2bay_C", b, rot=(0, 0, br))
    put("SM_Gable_Barge_2bay", b, rot=(0, 0, br))
    put("SM_Gable_Finial", on(b, br, (0, -VO + .03, Z2 + SAD_Z[1] - .022)),
        rot=(0, 0, br))
    for i in range(1):
        put("SM_Gable_RidgeComb_2m", on(b, br, (0, -VO + G / 2 + G * i, Z2)),
            rot=(0, 0, br + 90))

    for nm in src:
        src[nm].location = (0, 60, 0)
    return out
