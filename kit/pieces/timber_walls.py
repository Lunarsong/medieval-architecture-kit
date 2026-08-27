"""Half-timber upper-storey walling -- the cream-and-oak band that sits on top of
the stone base in both references.

THIRD PASS -- three named, reproducible defects fixed. The second pass got the
carpentry SIZES right (fat posts, few of them, shared horizontals, pillowed
plaster) and three things badly wrong:

  1. THE ARCHED BRACE FLOATED. It was a quarter-annulus whose radius was picked
     by eye (ro=0.8-1.05) and had nothing to do with the frame around it, so
     BOTH of its ends stopped in mid-panel: the foot kissed the post's inner
     face along a single line 0.77 m above the sole plate and the head kissed
     the rail above. A brace touching nothing at either end is worse than no
     brace, and in the assembled inn it read as a decal.
     Now `_brace_arc` fits an ELLIPSE to the frame it braces, and every cut face
     of the brace ends up inside another member:
        * the foot leaves the near post with a vertical tangent and is cut off
          55 mm BELOW the springing line, i.e. inside the rail it stands on;
        * the back of the curve runs 45 mm INTO the near post;
        * the head arrives with a horizontal tangent 22 mm INSIDE the rail
          above, and its end face is 45 mm inside the FAR post.
     That is what a mortice is. It also means the brace spans the bay, which is
     the only honest option at GRID=2.0: a 0.22 m member cut square cannot be
     tenoned invisibly into a 0.145 m rail, so the head has to land in a post.
     And it is now only on the pieces whose framing gives it something to do --
     A (the one big field) and the jettied A. B answers with an intermediate
     post, C with boarding; neither pretends to be braced.

  2. THE WINDOW BAYS WERE BUILT FOR THE OLD OPENING. win_upper was widened from
     0.86 x 1.05 to 1.50 x 1.45 (head 0.95+1.45 = 2.40). This module still
     assumed the old head at 2.00 -- which is exactly where the shared transom
     rail sits -- so the transom, the frieze studs AND the frieze's pillowed
     plaster panels were all drawn straight ACROSS the top 0.40 m of the window
     hole, and the 1.50 m opening left a 93 mm gap to the seam post which was
     filled with a pillowed plaster sliver AND a lining on top of it. That
     stretched sliver pattern at the bottom corners of the window is the
     "stretching in strange ways" in the report. Everything is now derived from
     spec.OPENINGS: no rail crosses the hole, the 105 mm between reveal and post
     is ONE oak jamb, the head plate IS the window head (2.42, 20 mm over the
     opening) with a proud drip mould under it, and the sill rail is the
     opening's sill.
     `_panel` also picks its grid from the panel's own proportions now (target
     ~0.34 m quads per axis) instead of taking n x n regardless of aspect, which
     is what made the frieze panels show bright stretched chevrons.

  3. Z-FIGHTING ON THE INSIDE. `_core` was a plate spanning y0..T PLUS a
     `plaster_dim` skim spanning T-0.028..T, so both ended on y = T -- the
     wall's visible inner face. Two opaque coplanar faces at the surface the
     camera sees, 51908 cm2 of it per plain bay. It is ONE solid now, with the
     darker inner tone painted onto its +Y faces, and its front face sits at
     CORE_Y = 0.074, BEHIND every timber back, so no frame member shares a
     snap-plane rectangle with the core either. Same treatment everywhere two
     solids butted on one plane: the rects around an opening overlap, the reveal
     backing is oversized and stops 4 mm short of the inner face, the bressumer
     and its bead interpenetrate, posts and studs are buried 15-20 mm into the
     plates they land on. What is left is the tiling seams themselves (x = +-1.0,
     z = 0 and z = H), where the kit's own conventions REQUIRE every member to
     be cut dead flat on the same plane.

Carried over from the second pass, still true:
  * POSTS ARE BIG AND FEW: 0.25-0.30 m at 1.3-1.6 m centres, measured off
    ref2:timber / ref3:timber at 74 px/m. Our 2.0 m bay is two 0.145 half-posts
    on the tiling seams leaving a single wide panel field (1.84 m since
    round 11) -- exactly the reference bay -- and only variant B gets an intermediate post.
  * Timber is oak_dark per the kit-wide table, oak_mid on secondary boarding and
    proud trim, oak_pale a rare highlight. In the greyscale reference the frame
    is clearly the dark element and the panels the light one.
  * plaster panels are bright warm cream and PILLOW outward between the frame,
    finishing ~0.06 behind the timber face, so the frame casts one thin shadow
    line instead of sitting on a flat sheet.
  * every bay shares the same horizontals -- sole, transom, head plate (and,
    since round 11, ONE sill line at APRON_TOP..SILL_TOP for every bay that has
    a band at window-sill height) -- so a run reads as one continuous frame and
    only what happens between them changes. (No rail crosses a window; that is
    the one exception, and it has to be.)
  * not every bay is plaster: ref3 has a lot of vertical boarding, so variant C
    and the jettied window bay carry it. But look at where ref3 puts it -- UNDER
    the window line, with render above -- which is what round 11 made them do.

Pieces
  SM_Wall_Timber_2m_A       plain bay: one big panel, one SEATED arch brace
  SM_Wall_Timber_2m_B       one intermediate post, two panels, lozenge
  SM_Wall_Timber_2m_C       boarded APRON + a plaster panel over it, and the
                            ledger between them is the family's sill line
  SM_Wall_TimberWin_2m      OPENINGS["win_upper"] 1.50x1.45: jambs, sill, drip
  SM_Wall_TimberJetty_2m_A  jettied storey, CREAM apron, shallow arch brace
  SM_Wall_TimberJetty_2m_B  jettied storey, boarded apron + window (ref2's bay,
                            and the one deliberately timber-heavy piece left)
  SM_Wall_TimberGable_2m    gable-end infill: king post + twin arch braces
  SM_Wall_TimberWinLow_2m   the same win_upper hole CENTRED (sill 0.530), so it
                            carries the transom and frieze the high bay cannot

... and, since round 19, NINE FRACTIONAL BAYS, which are AUTHORED at their size
and not scaled to it: SM_Wall_Timber_1m_A / _1m_B / _0m5_A,
SM_Wall_TimberWinAttic_1m, SM_Wall_TimberTall_2m_A / _2m_B,
SM_Wall_TimberTallWin_2m, SM_Wall_TimberKnee_2m and SM_Wall_TimberBand_2m.
See NINETEENTH PASS below for what each is and THE FRACTIONAL FOOTPRINTS, above
the constants, for why each is that rather than a squashed 2 m bay.

... and, since round 20, TWO PLATE BANDS -- SM_Wall_TimberBandEave_2m (0.850 m)
and SM_Wall_TimberBandGable_2m (1.000 m) -- the course between a timber storey's
head and the roof datum. See TWENTIETH PASS for the 0.70 m open slot they close
and for what beds on what.

and the same seven again with _Rough on the end -- SM_Wall_Timber_2m_A_Rough,
..._B_Rough, ..._C_Rough, SM_Wall_TimberWin_2m_Rough,
SM_Wall_TimberJetty_2m_A_Rough, ..._B_Rough, SM_Wall_TimberGable_2m_Rough --
hand-hewn siblings for a wall that should not look machined. Same footprints,
same rail heights, same openings, same seam faces to the millimetre, so a rough
bay and a regular bay can stand next to each other in any order and either can
be mirrored. See the section headed THE ROUGH HALF OF THE FAMILY, near the
bottom of this file, for what is allowed to move and what is not.

FOOTPRINT NOTE (deliberate, documented): the two jetty pieces declare
y = (0, T_TIMBER + JETTY). A jetty is by definition the one wall piece that
spans back to the storey below -- it carries the bressumer and the boarded
soffit over the overhang. Everything else obeys y = (0, T_TIMBER) exactly.
Corbel brackets, which hang BELOW the jetty line, are the beams family's.

===============================================================================
FOURTH PASS -- THE BAY SEAM, and readiness for X-MIRRORING.
===============================================================================
Feedback off the assembled inn: "there are some seam lines across wall
connections in places". There were, and in a timber wall they should be the
easiest seam in the kit to kill, because a half-timber bay boundary is supposed
to fall down the middle of a POST. Four separate causes, all of them real, none
of them visible in Solid viewport shading:

  1. A BEVEL GROOVE, and this was the loud one. util._emit bevels EVERY edge of
     a primitive, the two end edges included. A sole plate built from x = -1.0 to
     x = +1.0 therefore arrived at the seam with an 18 mm chamfer, its neighbour
     brought another, and the pair read as a 36 mm V-groove running the full
     height of the wall every 2.0 m -- through the wall plate, the frieze, the
     transom, the panel field and the sole plate, and straight down the middle
     of the post that was meant to hide the join. The timber was continuous; its
     ROUNDING was not, and rounding is what catches the light.
     `_mem` now builds any member that reaches a tiling plane SEAM_CUT wider
     than the bay and cuts it dead flat on that plane (`_cut`), which is exactly
     what Part.finish() does to a stone at a bay boundary. The chamfer collapses
     onto the seam, the front face crosses it at full width, and `_tidy` drops
     the zero-area faces left behind so they cannot pollute the smooth shading
     along the one line we are trying to make invisible.

  2. A TONAL STEP. Every shared band picked its material and its shade out of
     its own variant's rng stream, so bay A's sole plate could come out oak_mid
     at 1.03 against bay B's oak_dark at 0.96 -- a colour change at a join whose
     geometry was already perfect. Worse for the half-posts: the two halves that
     add up to ONE 0.29 m post were two independent draws, so half a post could
     be a different timber from its other half. `_band` / `_pin` / `_shared` key
     material, shade AND vertex-colour jitter to the member's NAME, so every
     variant's sole plate, wall plate, transom and half-post are identical and
     the only thing that changes along a run is what happens BETWEEN the posts.

  3. RAILS THAT STOPPED IN MID-AIR. The half-posts sat 6 mm BEHIND the rails, so
     the rails crossed in front of them. Both window bays legitimately carry no
     transom (a rail cannot pass through a 1.45 m casement), so next to a plain
     bay the transom ran to the seam and simply ended, a cut timber face floating
     at the join. POST_Y now puts the post 8 mm PROUD of the mid rails, the way
     ref3 frames its walls: posts run through, rails die into their sides. A
     missing rail dies into 0.29 m of post instead of stopping dead, and the
     transom's own seam join is hidden behind the post as well. The post's foot
     and head are in turn buried behind the sole bead and the wall plate, which
     are prouder still, so nothing pokes through anything.

  4. WOBBLE reached too close to the seam: at 100 mm from a tiling plane the
     fade still allowed 7.5 mm of noise, so two adjacent half-posts diverged
     immediately either side of a join that was itself flat. margin 0.16 -> 0.28
     leaves the panel field fully hand-hewn and flattens only the post and plate
     zone, which has to be flat anyway (see `_wob`).

MEASURED, because "the seam is gone" is worth proving rather than eyeballing.
Render a 14 m run as a flat orthographic elevation and take the mean absolute
horizontal luminance gradient down each column. Background level inside a band
of timber is 0.45. At the seven interior bay joins, before and after:

    post band     22.7 29.4 22.4 20.6 26.0 21.5   ->   0.5 0.5 0.5 0.5 0.5 0.5
    sole plate    13.0 13.4 11.8 10.3 12.1 14.4   ->   0.4 0.7 0.5 0.6 0.6 0.6
    wall plate     6.7  6.0  6.7  6.8  7.0  6.2   ->   0.6 0.5 0.5 0.6 0.6 0.5
    bressumer     24.4 31.3 19.7 22.0 27.2 19.0   ->   0.3 0.5 0.6 0.6 0.6 0.8

i.e. from 15-60x the background down to the background itself: there is no
longer a signal at the bay boundary at all. (The run's two OUTER edges still
read 14-77, correctly -- that is the silhouette against the void.)

MIRRORING. assemble_inn.py now mirrors these pieces in X for the second half of
a facade so the arched braces splay symmetrically instead of all leaning the
same way. Nothing in the family is handed in a way that reads wrong reversed --
no lettering, no latch, no one-way detail; the brace lean IS the point, and the
lozenges, pegs and boarding are all symmetric objects. The one thing that DID
break under mirroring was (2): a mirrored bay's half-posts are not the same two
rng draws as its unmirrored neighbour's, so a keyed tone is what makes a
mirrored piece still form one post with an unmirrored one. Verified by rendering
A | mirror(A) | B | mirror(B) | C | mirror(W) | W | mirror(C) as an elevation --
every mirrored/unmirrored join measures 0.5, the same as the rest -- and the
A | mirror(A) pair now forms a proper symmetric arcade over its shared post,
which is the whole point of the mirroring.

Also fixed here:
  * jetty_a's apron rail sat 20 mm below jetty_b's, so the two jettied variants
    stepped against each other at the seam. Both take APRON_TOP now, derived
    from the window sill they have to share.
  * the jetty soffit left a 22 mm gap at the bay join against 12 mm between its
    own boards; the run now lands the board gap exactly on the seam.
  * both jetty variants seeded their apron boarding "timber/apron", so every
    jettied bay in a run carried the identical sequence of board tones. Seeded
    per piece now -- with the seam gone that 2 m repeat was the most
    pattern-like thing left in the family.
  * pegs did not know what they were driven into (`_peg` had no `face`): the
    brace's two joint pegs ended up 36 mm INSIDE the post once the post came
    forward, wall C's four stood 60 mm out of a 0.104 board like spikes, and the
    bressumer's three had always been buried inside a beam standing at -0.135,
    i.e. three invisible cylinders.
  * DETERMINISM, and this one is kit-wide rather than ours: util.Part.wobble
    displaces by mathutils.noise.noise_vector, which Blender seeds PER PROCESS,
    so "same code, same mesh" was false for every family that wobbles -- these
    seven pieces differed by up to 15.6 mm between builds of identical code, and
    stone_walls, which nobody has touched, differs by up to 289 mm and does not
    even keep its vertex count. With wobble stubbed out these seven are
    bit-identical across processes, so the noise seed was the whole of it.
    `_wob` pins it with noise.seed_set() and the family is now byte-for-byte
    reproducible. The proper fix belongs in util.Part.wobble; see `_wob`.

===============================================================================
NINTH PASS (b) -- THE CARVING WAS THERE AND COULD NOT BE SEEN.
===============================================================================
Shanee, again, of the whole kit: "the wood overall still needs a texture or
detail" -- after the pass that built `_worked` and put a stop-chamfer, adze
facets, an uneven arris and a bow on every member in this family. So the
question was not "is there carving" but "why does none of it reach the eye",
and the answer, in the SOLID viewport shading the .blend is inspected in, is
specific and measurable:

  1. THE ADZE FACETS WERE PARALLEL. Each facet was the nominal face plane
     offset inward by `lvl[reg]*ADZE`. Offset, not rotated -- so two
     neighbouring facets had THE SAME NORMAL and shaded identically, and the
     hard 42-degree crease between them divided two equal values. A sharp edge
     is only visible if the faces it separates shade differently; this one
     bought the eye a single 10 mm sliver, sub-pixel at any distance a wall is
     looked at. `FACET_TILT` tilts alternate facets the other way, so
     consecutive flats differ by 2*atan(tilt/span) -- 8 degrees on a 0.185 rail,
     5 on a 0.29 post -- and the face of a timber reads as three axe flats
     instead of one board. Zero tris: it moves vertices `_sweep` was already
     emitting. (`_hexsec` takes a PAIR for its front depth now; `_arc_c` gets
     the same thing as a smooth wind along the curve, since a brace has no
     straight station to break a facet on.)
  2. THE CHAMFER STOP WAS A 30 mm KINK. CHAM_RET 0.030 -> 0.068, and a
     CHAM_SWELL lamb's tongue: the chamfer swells 30% wider just inboard of its
     return before dying square. Both are the standard ornament of the detail,
     both cost nothing, and both are zero at the end stations.

MEASURED, in Workbench/Solid at 2 m -- the mode Shanee inspects in, and where a
vertex-colour tint or an image texture does not exist at all. Mask = the brown
(timber) pixels only, so the plaster and the void cannot flatter the number.
Mean |luminance gradient| inside the timber, and the share of pixel pairs whose
step exceeds 2%:

    before 9b   std 0.0454   grad 3.34   edges over 2%  2.33 %
    after  9b   std 0.0494   grad 3.57   edges over 2%  2.66 %
                    (+8.8%)     (+6.9%)              (+14%)

THE BAY SEAM IS UNTOUCHED, and that is checked rather than argued, because this
pass reshapes every member that crosses it. Two tests:
  * every vertex on x = +-1.0 and on z = 0, for all 14 pieces: the pairwise
    "does P's +x section equal Q's -x section" matrix is IDENTICAL before and
    after (14/14 pieces still match themselves exactly, same 14 pairs overall).
    The tilt is across a member's WIDTH, which `env` -- a function of position
    ALONG it -- cannot fade, so `_worked` refuses to tilt any side that lies on
    a tiling plane: a half-post's high side is x = +G/2 and a sole plate's low
    side is z = 0. See `tm` in `_worked`.
  * three tiled copies rendered as a flat orthographic elevation, mean |d/dx|
    luminance per column, same measurement the fourth pass used. At both
    interior joins: post band 1.3-2.2 against a 4.9 background, sole plate
    0.5-2.4 against 1.4, wall plate 0.9-2.5 against 1.6, frieze 1.0-1.8 against
    1.6. i.e. still no signal at the bay boundary.

REJECTED, and worth recording so nobody spends the time again: widening CHAM
from 26 to 36 mm bought +1.6% std for a chamfer that no longer matches
beams.SILL_BEV, and a 1.9x multiplier on every arris bow measured as literally
zero change (it is a silhouette effect, and one bay is not enough of a run to
show it) while perturbing the seam sections of 24 of 42 planes. Both reverted.

===============================================================================
ELEVENTH PASS -- THE RATIO. "MOST WALLS IN THE 1ST FLOOR ARE WOOD."
===============================================================================
Shanee, of the assembled inn: "it seems like you replaced most walls in the 1st
floor with wood while the reference is the plaster/white ones". The diagnosis
was already written into assemble_inn.py -- THE FACADE IS A CREAM WALL WITH
TIMBER DRAWN ON IT, not a brown lattice -- and round 10 acted on it, slimmed the
frame and reported the plain bay down to ~30% timber. So why was the building
still brown? Because 30% was true of ONE PIECE and nobody had measured the rest.

MEASURED, all fourteen, head-on (`measure()` at the bottom of this file is the
harness, and it lives here so it cannot drift from the code it describes):

    piece                     timber   dark      piece                 timber
    SM_Wall_Timber_2m_A        32.7%   39.9%     ..._A_Rough            34.5%
    SM_Wall_Timber_2m_B        33.2%   41.1%     ..._B_Rough            33.9%
    SM_Wall_Timber_2m_C        87.6%   93.4%     ..._C_Rough            83.0%
    SM_Wall_TimberWin_2m       74.3%   79.9%     ...Win_Rough           74.4%
    SM_Wall_TimberJetty_2m_A   58.2%   64.6%     ...Jetty_A_Rough       57.8%
    SM_Wall_TimberJetty_2m_B   95.3%   98.9%     ...Jetty_B_Rough       94.0%
    SM_Wall_TimberGable_2m     63.3%   68.7%     ...Gable_Rough         60.4%
                                    FAMILY MEAN  63.0% timber, 69.5% dark

Three quarters of the family's timber was NOT IN THE FRAMING AT ALL. It was
BOARDING -- variant C boarded top to bottom, both jetty aprons boarded -- and
window LINING. Slimming studs could never have fixed that, which is why round
10's work did not show up on the building: the assembler's north elevation is
half `c`, and every elevation is a third `win`.

WHAT THIS PASS DID, in the order it pays:

  1. BOARDING BECAME AN APRON. Crop ref3:timber and look at where the boarded
     walling actually is: UNDER the window line, with render above it. So C's
     boarding now stops at the family's sill line and the 1.05 m above it is one
     plaster panel; C's ledger IS that sill line, so a run of `c` and `win`
     shares a horizontal instead of stepping. jetty_a -- the PLAIN jettied bay --
     takes a plaster apron, exactly as the window bay did in round 10 and for the
     same reason. jetty_b keeps ref2's boarded apron: it is the signature bay and
     the one piece deliberately left timber-heavy.
     C 87.6% -> 50.9%. jetty_a 58.2% -> 39.1%.
  2. EVERY SECTION SLIMMED AGAIN, ~0.78x. Post 0.195 -> 0.160, stud 0.170 ->
     0.130, thin 0.140 -> 0.105, brace 0.135 -> 0.100, sole plate 0.130 ->
     0.095, transom 0.105 -> 0.078, window jamb 0.086 -> 0.062, sill band 0.176
     -> 0.118, and the gable's own set with them. Z_HEAD is the one band that
     cannot move: the wall plate is the lintel over win_upper and has to run
     2.42 -> 2.60, i.e. 6.9% of every bay by construction.
  3. THE PLASTER CAME FORWARD, WHICH IS THE PROUD-DEPTH LEVER. The first attempt
     moved only the panel CROWN and measured no change, because `belly` is
     rim-to-crown and the cushion just got deeper. What throws the shadow is the
     step to the plaster immediately INSIDE the frame, which is down at the
     panel's RIM: PY 0.030 -> 0.000 puts the render flush with the wall plane
     where it meets the frame. Bay A's shadowed plaster 7.2% -> 4.7%.
  4. NOTHING TINTS THE PLASTER DOWN. Checked, per the brief. `_panel` was
     already clean after round 10; the GABLE was not -- it builds its cream out
     of two prisms at shade 0.92 and 0.98, the only sub-strength cream left in
     the family. Both at full tone now.

RESULT, same harness, same fourteen pieces:

    FAMILY MEAN   63.0% -> 50.7% timber,  69.5% -> 55.8% dark
    ... and on the WALL alone, dropping the win_upper opening (which a casement
    always fills, and whose reveal backing is deliberately dark oak):
                  59.9% -> 46.6%
    The four bays assemble_inn.py builds facades from -- a, b, c, win --
                  57.0% -> 43.6%, and 47.4% -> 37.8% on their wall alone.

ON THE REFERENCE, AND THIS IS WORTH BEING HONEST ABOUT. Measured off ref3's
linework at 49 px/m, its own studs run about 0.30 m at 2.1 m centres and its
rails about 0.27 m -- WIDER than ours were before this pass, let alone after.
That is not an argument for widening ours. ref3 draws its timber as light grey
outlined in ink; ours is oak_dark #3E2C22 against #E4D9BE plaster, so the same
width of our timber carries far more visual weight than the same width of
theirs, and spec.py's own palette note says the references run timber ~80
against cream ~220 while ours sits at 48. The palette is kit-wide and not this
module's to change, so the only lever left for matching the reference's VALUE
balance is to use less timber. Every section here is narrower than the thing it
is copying, deliberately.

WHAT DID NOT CHANGE, because it was accepted work: every brace, peg,
stop-chamfer, lamb's tongue, adze facet, lozenge and scarf. The rough half of
the family is retuned by the same constants and keeps all of its own hand-hewn
deviation. The bay seam is untouched -- the half-posts still meet as one post
(renders/timber_walls/tiled.png), the shared bands still key their tone to their
name, and W_POST is now read by the things that used to be measured in from it
(the post pegs, the brace's joint pegs, wall_a_rough's down-strut), so they
follow the section instead of having to be re-fitted by hand every time it moves.

===============================================================================
TWELFTH PASS -- THE LAST THREE COINCIDENT SURFACES.
===============================================================================
`check_zfight.py` still measured three pairs in this family, and two of them
were between DIFFERENT materials, which is the kind that flickers oak against
plaster as the camera moves rather than merely wasting a face:

    SM_Wall_Timber_2m_B_Rough    57 cm2 at [0.96,  0.055, 1.421]  oak_dark/plaster
    SM_Wall_TimberWin_2m_Rough   27 cm2 at [0.748, 0.158, 1.673]  plaster_dim/oak_dark
    SM_Wall_TimberJetty_2m_B     18 cm2 at [-0.889,-0.02,  0.03]  oak_mid/oak_mid

All three were the same bug wearing three hats: two solids GENERATED to planes a
few millimetres apart, then `_wob` closing the gap. Nudging either plane by a
millimetre would have moved the number without fixing anything, so each one was
separated by a real distance instead, in whichever axis had room.

  1. THE PANEL'S BACK RAN UNDER THE FRAME. `_panel` built its flat back on the
     SAME grown rectangle as its domed front, so the plane at PANEL_BACK (0.052)
     continued under every member the panel tucks beneath -- and the depth ladder
     leaves it 8 mm to POST_BACK and 14 mm to a rail back. On the hand-made bays,
     where `grow` is 40 mm, the +X half-post's back and the plaster's back became
     one plane. There is nowhere in the ladder for either plane to go, so the
     separation is taken in X and Z: the back grid now stops PANEL_BACK_IN (30 mm)
     INSIDE the frame line and the two are joined by a sloped rim strip the frame
     covers. 8 mm of y -> 30 mm of x, and no panel back lies under any timber at
     all now, so the rails and studs gain the same clearance for free.
  2. THE JAMB LAPPED THE REVEAL BY 6 mm. The core's hole was cut to the opening
     exactly, standing a plaster face on x = +-0.750, while the oak jamb lapping
     it stood one on +-0.744 -- parallel, 6 mm apart, overlapping over the 6 mm
     of y where the jamb's back is already inside CORE_Y. The lap cannot grow
     (spec's casement edge is at 0.730) and the jamb cannot get shallower
     (ending it on CORE_Y trades this fight for a bigger one), so the CORE moved:
     its hole is cut REV_SPLAY (20 mm) wider each side -- a rebated reveal, which
     is what a plastered wall does around a frame -- and `_reveal`'s backing plate
     is oversized to suit and closes the back of the rebate. 6 mm -> 26 mm.
     Nothing outside the wall moves: the aperture is still OPENINGS["win_upper"].
  3. THE BRESSUMER BEAD DID NOT LAP THE SOFFIT. `bress_low` was 0.060 deep, so
     its back landed on y = -0.017 against soffit boards whose front end grain is
     on -0.020: 3 mm, oak_mid against oak_mid. It is 0.095 deep now and sits
     38 mm INSIDE the soffit, the same lap the bressumer above it already has.
     (It also stops a 3 mm sliver of that back face showing through the board
     gaps, which is visible in a render of the underside.)

MEASURED, and this is a defect fix, so what did NOT change is the point:
  * check_zfight.py -- timber_walls: 3 pieces / 102 cm2 -> ZERO.
  * TILING. Two copies at exactly GRID, comparing each copy's faces against the
    OTHER'S (the butt plane itself excluded, since those cut faces are interior
    and face away from each other): zero coincident pairs on all 14 pieces, and
    zero even at a 2.5 mm tolerance. Both of the fixed defects that sat on a
    seam -- the panel back at x = 0.96 and the bead at x = -0.889 -- are now
    clear by more than the wobble amplitude on either side of the join, which is
    why PANEL_BACK_IN is 30 mm and not 8: a panel back that creeps past XE is
    under the NEIGHBOUR's half-post as well as its own.
  * THE RATIO IS UNTOUCHED. `measure()` returns the round-11 table to the
    decimal on all fourteen pieces: family mean 50.7% timber, 55.9% dark.
  * closeup.png, tiled.png and a grazing elevation are PIXEL-IDENTICAL before
    and after; lineup.png and demo.png differ by 0.04-0.06% of their pixels, all
    of it the sliver of reveal plaster that was doing the fighting. Braces,
    pegs, stop-chamfers, lamb's tongues, adze facets, lozenges and boarding are
    bit-identical: no primitive changed except the three planes named above.
  * Still deterministic (identical mesh hash across processes) and every piece
    still reports an EMPTY report, 794-2264 tris against the 5200 wall budget.

===============================================================================
THIRTEENTH PASS -- THE HOLE WAS NOT THE SIZE OF THE HOLE.
===============================================================================
Shanee, off the assembled inn: "SM_Win_LeadedCasement_A.002 doesn't seem to fit
SM_Wall_TimberWin_2m.007 properly and both add their own window sill and there's
various overlapping wood pieces that make it look strange."

Two separate faults, one of them ours, and this pass measures both rather than
arguing about either. `measure_opening()` at the bottom of this file is the
harness: it ray-casts the BUILT MESH, not the code -- a grid of +Y rays over the
face of each piece, marching outward from the middle of the hole and bisecting to
find where the first hit stops being deeper than spec.REVEAL. That is literally
"how big is the hole a casement has to fit through".

MEASURED, BEFORE:

    piece                             w        h      sill     head
    SM_Wall_TimberWin_2m           1.4855   1.4191   0.9809   2.4000
    SM_Wall_TimberJetty_2m_B       1.4884   1.4187   0.9811   2.3997
    SM_Wall_TimberWin_2m_Rough     1.4828   1.4192   0.9808   2.4000
    SM_Wall_TimberJetty_2m_B_Rough 1.4828   1.4166   0.9834   2.4000
    spec.OPENINGS["win_upper"]     1.5000   1.4500   0.9500   2.4000

Every hole in the family was 11.6-17.2 mm NARROW and 30.8-33.4 mm SHORT, and it
was short at the BOTTOM: the sill it actually presented stood 31-33 mm above the
one spec says an insert beds on. spec's insert is INSERT_CLEAR (20 mm) smaller
all round, so a 33 mm error does not eat into the clearance, it eats through it:
a correctly built casement lands ON the wall instead of IN it. Three causes:

  1. THE JAMB LAPPED THE OPENING, 6 mm each side. It was introduced to keep the
     oak jamb face off the core's plaster reveal face; round 12 solved that
     properly by standing the core's cheek back REV_SPLAY, so the lap had been
     dead weight for a round and was costing 12 mm of the aperture. JAMB_LAP 0.
  2. THE CILL STOOD 14-18 mm INSIDE THE HOLE. The projecting sill nose was built
     hz0 - 0.050 .. hz0 + 0.014, i.e. deliberately lapping UP over the sill line.
     It tucks CILL_DROP (8 mm) UNDER it now, so the sill of the reveal is the
     sill rail's own top face and the core's, both of which are already at
     exactly OPENINGS["win_upper"]["sill"].
  3. WOBBLE TREATED THE OPENING AS INTERIOR. `_wob` fades to zero at a tiling
     plane and nowhere else, so up to 15 mm of hand-hewn noise was free to wander
     INTO the reveal. `_open_fade` now fades it to zero at the aperture too, in
     exactly util's shape -- see that function for why it is a fade and not a
     clamp, which would have traded a fit problem for a z-fight.
  ... and on the two ROUGH bays, a fourth: `_scarf`'s hewn middle timber is
     `pad` taller than its band and took half of that upward. On a sill band
     "upward" is into the window: 8.5 mm of it, measured. `pad_up` directs the
     overshoot; the window bays send all of it down.

MEASURED, AFTER -- all four pieces, ray-cast the same way:

    SM_Wall_TimberWin_2m           1.5000   1.4500   0.9500   2.4000
    SM_Wall_TimberJetty_2m_B       1.5000   1.4500   0.9500   2.4000
    SM_Wall_TimberWin_2m_Rough     1.5000   1.4500   0.9500   2.4000
    SM_Wall_TimberJetty_2m_B_Rough 1.5000   1.4500   0.9500   2.4000

i.e. spec.OPENINGS to the micrometre on the regular bays and to 0.5 mm on the
worst single column of the rough ones (0.5 mm is the probe's own step). The
OTHER half of the misfit is not ours: the casements measure 1.60-1.76 wide
against a 1.50 hole and windows.py owns that.

THE SILL. See THE SILL BELONGS TO THE WALL, above the constants, for the contract
windows.py can build against. Short version: the wall keeps its cill, the insert
drops its; the wall's cill top is CILL_DROP under the sill line and its face is at
y = -0.100, 40 mm PROUDER than windows.py's own trim plane at -0.060, so an
insert's bottom rail may oversail down over the wall's cill without ever touching
it.

THE WHOLE FAMILY, AUDITED, because "any timber section overall" is what was
actually asked for. Two harnesses, on all fourteen pieces:
  * CLOSED-SOLID audit. Every primitive that is a closed manifold is surface-
    sampled at 35 mm and each sample is parity-tested against every other closed
    solid whose bounds it shares, which answers "is this piece of wood inside
    another piece of wood" and "does this member's end cap land on anything".
    Result: no member stops short of its rail, no brace lands on nothing, no
    board is doubled, and no solid is more than 90% buried -- with ONE
    exception, found and fixed: on SM_Wall_TimberWin_2m_Rough the sill scarf
    drove a peg into the middle of the band the CILL covers, so 103 cm2 of
    oak_pale head sat inside 30 mm of oak (x 0.16-0.20, z 0.90-0.94). `_scarf`
    takes `peg_z`/`peg_face` now and the window bays peg their cill instead,
    where the peg is the joint it is pretending to be. Verified visible after:
    head-on rays over the peg's own footprint return 15-20% oak_pale.
    ONE FALSE POSITIVE SURVIVES AND IS NOT A DEFECT, recorded so nobody spends
    the time again: the same audit reports jetty_b_rough's cill peg 90% buried.
    It is not -- the peg stands 20 mm out of the cill's face and head-on rays
    over its footprint come back 14.7% oak_pale. A hewn cill with roll and wane
    can be locally self-intersecting, which is exactly what breaks the audit's
    parity ("count crossings, odd means inside") test. Measure visibility with
    rays, not with parity, whenever the host is a `_hewn` member.
  * check_zfight.py: 0 pieces, 0 cm2, before and after. The three planes this
    pass could have made coincident by un-wobbling them were each separated by
    construction first -- the drip mould's soffit lifted 4 mm off the core's
    head band (406 cm2 avoided), the cill's top dropped CILL_DROP off the sill
    rail's top (1520 cm2 avoided), and `_reveal`'s internal window board pushed
    back behind spec.REVEAL, where it is also clear of windows.py's blank.

NOT REGRESSED, checked rather than asserted:
  * THE RATIO. `measure()`, all fourteen: 50.7% -> 50.8% timber, 55.9% -> 56.0%
    dark. The ten pieces without an opening are identical to the decimal; the
    0.1 is the four window bays' cill sitting 8-22 mm lower on the face.
  * braces, pegs, stop-chamfers, lamb's tongues, adze facets, lozenges and
    boarding: not one of those primitives changed. wall_a, wall_b, wall_c, both
    gables and both plain jetty bays are byte-identical.
  * THE BAY SEAM, which every previous pass had to defend and this one gets for
    free. `_open_fade`'s influence reaches at most `margin` from the aperture,
    i.e. |x| <= 0.85 and 0.85 <= z <= 2.50, so it cannot touch x = +-1.0, z = 0
    or z = H by construction -- and measured: collect every vertex on those three
    planes for all fourteen pieces, before and after, and the sets are IDENTICAL
    on 14/14, not merely close.
  * every piece still reports an EMPTY report, 794-2264 tris, and the family is
    still bit-identical across two separate Blender processes.

===============================================================================
FOURTEENTH PASS -- FOUR MEASURED DEFECTS, AND ALL FOUR WERE JOINTS THAT DID NOT
MEET.
===============================================================================
Reported by this module's own auditor at the end of round 13 and left unfixed
there, so every number below is a before -> after on the BUILT MESH, measured by
the same harnesses that found them (`measure_opening`, `measure`, and the ray
scans described at each fix).

  1. HIGH -- THE KING POST STOPPED 81 mm SHORT OF THE RAKE SOFFIT. Its head was
     cut to the soffit measured at the post's own SIDE and then 12 mm below that,
     but the rakes rise as they come in, so the soffit at the post's CENTRE is
     74 mm higher again. Head-on rays down the centre line came back CREAM from
     z = 1.085 to the apex. It lands in the V now, and a triangular head cut to
     the rake pitch closes the knife-edge notch the two rakes' own bevels leave
     on x = 0. See THE KING POST DID NOT REACH THE APEX and `_king_head`.
        plaster on the gable's centre line above z = 0.5
            SM_Wall_TimberGable_2m         81.4 mm + a run to the apex -> 9 mm
            SM_Wall_TimberGable_2m_Rough   87.0 mm + a run to the apex -> 9 mm
     The 9 mm that remains is the apex POINT itself, where three chamfered
     timbers converge; it was 15 mm before this pass, it is z = ZA (the plane the
     gables family's finial and bargeboards land on), and it is not this piece's
     to close.

  2. MEDIUM -- A CREAM HAIRLINE ACROSS THE HEAD OF EVERY OPENING. Round 13 lifted
     the drip mould's soffit 4 mm off the opening's head to stop it sharing a
     plane with the core band above the hole; that 4 mm was a window, and a ray
     at 2.400 < z < 2.404 flew past the mould onto the front face of the core at
     y = +0.074. The soffit is back ON the head -- it IS the head of the hole --
     and the shared plane is separated in Z instead, by starting the core's band
     HEAD_LAP (8 mm) higher. See THE DRIP MOULD IS THE HEAD OF THE HOLE.
        worst plaster band across the head, 31 columns over the 1.50 m opening
            SM_Wall_TimberWin_2m            5.6 mm, 31/31 columns -> 0.0, 0/31
            SM_Wall_TimberWin_2m_Rough      6.4 mm, 31/31        -> 0.0, 0/31
            SM_Wall_TimberJetty_2m_B        4.8 mm, 31/31        -> 0.0, 0/31
            SM_Wall_TimberJetty_2m_B_Rough  8.2 mm, 31/31        -> 0.0, 0/31
     THE HOLE GOT MORE EXACT, NOT LESS, and that took one more fix: the mould's
     soffit is 190 mm wider than the aperture, so `_open_fade` left its ears free
     to wobble and a quad drags its middle with them -- the head measured 2.3986
     against spec's 2.4000. `_open_fade` takes `head_x` now and holds the WHOLE
     soffit, and the head measures 2.4000 on all 41 columns of all four bays,
     which is better than round 13 left it.

  3. MEDIUM -- 115 dm3 OF DOUBLED SOLID BEHIND EVERY UPPER WINDOW. The wall's
     reveal backing plate spanned y = 0.140..0.237 and windows.py's leaf blank
     ran back to y = 0.196: 56 mm shared over the whole 1.46 x 1.41 aperture.
     THE WALL KEEPS THE PLATE and gets out of the insert's way -- see WHO OWNS
     THE SOLID BEHIND THE GLASS for the split and for the plane windows.py trims
     to. Measured in the built mesh, the first hit in the middle of the opening:
            y = 0.1401..0.1409  ->  0.1984..0.2014   (nominal BACK_Y = 0.200)
     so the doubled volume is 115 dm3 -> 0, with 4 mm of air still between the
     two. An empty opening is still opaque, and now reads as a 200 mm reveal in a
     240 mm wall, which is what it is.

  4. LOW -- THREE QUARTERS OF THE LOZENGE WAS INSIDE THE KING POST. A 199 mm
     diamond centred on a 116 mm post, its face 2 mm behind the post's: 742 of
     1130 cm3 buried, two 40 mm ears reading. It moves to where ref3 sets the
     motif -- into a panel -- one in each spandrel under the twin arch braces.
            volume inside the king post   742 cm3 (65.6%)  ->  0 cm3 (0.0%)
            inside a brace                                     0 cm3 (0.0%)
            diamond across the flats      199 mm -> 164 mm, and all of it reads
     See THE LOZENGE WAS INSIDE THE POST for the three measured clearances.

WHAT IT COST, measured with `measure()` and worth stating plainly: landing the
king post and putting two diamonds into the cream takes the gable from 50.6% to
53.2% timber, and the family mean from 50.8% to 51.2%. That is the price of the
two fixes and it is paid on one piece that appears once per roof end. Every other
piece in the family is unchanged to the decimal.

NOT REGRESSED, checked rather than asserted:
  * check_zfight.py -- timber_walls: ZERO pieces, before and after. One pair was
    introduced on the way and measured (66 cm2 on SM_Wall_TimberWin_2m at
    [0.024, 0.066, 2.508], the first attempt's shallower drip mould against the
    wall plate's back face) and the fix is recorded at DRIP_BACK so nobody puts
    a plane back into that 8 mm slot.
  * spec.OPENINGS: 1.5000 x 1.4500 at sill 0.9500, head 2.4000, on all four
    window bays, and 2.4000 on every one of 41 columns.
  * every piece reports an EMPTY report; 870-2264 tris against the 5200 budget.
  * bit-identical across two separate Blender processes.
  * THE BAY SEAM. Every piece still self-tiles on x = +-1.0 exactly, and the
    pairwise "P's +x section equals Q's -x section" matrix is the same 14 pairs
    the ninth pass measured. `head_x` reaches at most |x| <= 0.874 on the head
    plane only, and `_king_head` and the lozenges are 100 mm and 600 mm from a
    tiling plane, so none of this pass can touch one by construction.

===============================================================================
FIFTEENTH PASS -- THE ROUGH GABLE READ AS TWISTED, AND IT WAS ONE LINE.
===============================================================================
Shanee: "Things like SM_Wall_TimberGable_2m_Rough where the timber elements
looks a bit weird / twisted / broken."

It was, and the roughening was doing two separate things to it. Both are
measured on the BUILT MESH against the machined sibling built by the SAME
functions with the roughness turned off -- which is the right control, because
it isolates "what the roughening did" from "what the piece is".

  1. THE CURVE'S ROUGHNESS WAS ON ITS AXIS, NOT ITS SURFACE. `_arc_c` drew its
     radius jitter INDEPENDENTLY AT EVERY STATION and applied it to the whole
     cross-section, so the arch brace's centre line -- and with it both arrises
     -- took a fresh +-10 mm step at each of 13 stations. `_c_stations` puts its
     two tightest stations 45 mm of arc apart, so a single station could kink by
     atan(20/45) = 24 degrees. On a 2.4 m stud that would be a nick; on the one
     CURVE in the piece, whose arris the eye follows as a line, it is a member
     snapped in half. Worst member of each piece, in degrees:

         piece                            axis dev   axis kink   edge kink
         SM_Wall_TimberGable_2m              6.14        0.00        0.00
         SM_Wall_TimberGable_2m_Rough    23.90->6.78 33.67->2.98 36.81->6.39
         SM_Wall_Timber_2m_A                 4.41        0.32        0.32
         SM_Wall_Timber_2m_A_Rough       16.70->5.80 12.59->1.28 13.00->2.52
         SM_Wall_TimberJetty_2m_A            6.80        6.80        7.05
         SM_Wall_TimberJetty_2m_A_Rough  12.86->9.18 14.62->9.43 15.18->10.06

     (axis dev is measured against the LOCAL central-difference tangent, so the
     smooth pieces' 4-7 degrees is the 13-station discretisation of the arc
     itself and is the floor, not a fault -- jetty_a's brace is a 1.75:1 ellipse
     and has the highest floor of the three. Every rough brace is now inside a
     couple of degrees of its own machined twin.)
     THE ROUGHNESS IS NOT REMOVED, IT IS MOVED, which is the whole point: the
     radius still wanders the same +-jit, as a smooth two-harmonic function of
     the arc parameter inside a sin(pi t) envelope, so the arris undulates
     instead of zig-zagging and both ends land at their nominal radius. The
     per-station draw that used to do the damage is spent on the member's WIDTH
     instead, where an independent step moves only the concave inner arris. See
     THE WANDER IS COHERENT, NOT WHITE NOISE in `_arc_c`.

  2. THE PLASTER WAS PUNCHING THROUGH THE BRACE. `_arc_c` gives every worked
     member two INWARD deviations on its front face -- the adze facets (8 mm)
     and the facet tilt (11 mm) -- and both cut back from the member's own face
     plane. On a wall that is free, because a stud stands 50 mm proud of its
     panel. On the GABLE the brace stands 20 mm proud of the infill and 14 mm
     on `gable_rough`, whose hand-floated infill is 6 mm prouder again, so 19 mm
     of inward carving left the brace's deepest facet BEHIND the cream it is
     supposed to stand in front of. Measured by rastering the head-on face at
     1.5 mm and differencing before against after, plaster that turned back into
     oak INSIDE the braces' own footprint:

         SM_Wall_TimberGable_2m           37.2 cm2  (0.29% of the face)  -> 0
         SM_Wall_TimberGable_2m_Rough    165.6 cm2  (1.29% of the face)  -> 0

     and along the LEFT brace's own centre line, the longest run of non-oak:
     43.7 mm -> 0.0 mm on the rough gable, 0.0 -> 0.0 on the machined one.
     ADZE_G / TILT_G size the carving to the gable's relief budget; the facet
     STEP the eye reads is untouched, only the part of the excursion that had
     nowhere to be. See THE GABLE'S RELIEF BUDGET.

  3. THE APEX. The auditor's residual -- 9.0 mm of plaster on the centre line at
     z 1.2708..1.2799, 100% of it LIT at the kit sun -- was blamed in round 14
     on "three chamfered timbers converging". It was ONE chamfer: `_king_head`'s
     10 mm bevel on a 22-degree half-angle tip cuts the tip back by
     0.010*cos(22) = 9.3 mm of Z. Square-arrised now, so the king post lands
     exactly on z = ZA, which is the plane the gables family's finial and
     bargeboards sit on, and it cannot break that plane because the head rises
     2.478 per unit x against the rake line's 1.280.
         centre-line non-oak above z = 0.5, both gables:  9.0 mm -> 0.0 mm
     NOT FULLY CLOSED, and honestly: the apex-POINT cream AREA (|x| < 30 mm,
     top 50 mm) is 0.99 -> 0.64 cm2. What is left is two slivers at most 3 mm
     wide flanking the tip in the top 16 mm, and they are not the king post's:
     they are where the RAKES' own 16 mm arris chamfers cut both rakes off
     x = 0. Filling them means running the head to within 1-2 mm of the rake's
     upper face -- the bargeboard's bed -- which the snap plane does not allow,
     so they are left for the finial that lands on that point.

  4. THE ROUGH GABLE'S SOLE BEAD WAS BEING CUT AS A STRUCTURAL TIMBER. This one
     `_scarf` call took the function's DEFAULTS -- cham = CHAM (26 mm),
     cstop = .16, cfac = 2 -- on a 46 mm bead, where every other rough piece
     goes through `_rails_rough` and passes CHAM_BEAD (10 mm), a short stop and
     no adze facets. The 26 mm chamfer clamps to 19 mm (42% of the section) and
     then two facets are cut into what is left: the bead's top arris came out as
     a row of V-notches, which is a good part of what "broken" was pointing at.
     Matched to `_rails_rough`; the band's z, y, keyed tone, lap and seam stubs
     are all unchanged.

WHAT IT COST, and it is one number, stated plainly rather than hidden: the
family mean goes 51.15% -> 51.25% timber (56.32% -> 56.43% dark). TEN OF THE
FOURTEEN PIECES ARE BYTE-IDENTICAL and their ratios do not move in the fourth
decimal; the four that changed are the two gables and the two rough bays that
carry an arch brace. The raster difference above accounts for ALL of it: it is
the 37 cm2 and 166 cm2 of plaster that was standing in FRONT of the braces and
is now correctly behind them, plus 0.4 cm2 at each apex. That is not more timber
on the wall -- it is the same timber no longer being punctured -- and no member
in the family got wider. Nothing was slimmed to buy the number back, because
shaving an accepted section to flatter a ratio is exactly the kind of bookkeeping
this file exists to stop.

NOT REGRESSED, checked rather than asserted:
  * THE BAY SEAM. Every vertex on x = -1.0, x = +1.0 and z = 0, all fourteen
    pieces: the sections are IDENTICAL before and after, 14/14, not merely
    close. Nothing this pass touches is within 400 mm of a tiling plane except
    the bead's stubs, and `_worked` already arrives at a seam as a bare
    rectangle (ends = 0), so the chamfer argument cannot reach it.
  * check_zfight.py -- timber_walls: ZERO pieces, before and after.
  * every piece reports an EMPTY report; 846-2264 tris against the 5200 budget
    (the two gables got CHEAPER: 870 -> 846 and 1040 -> 932, the bead's two
    dropped adze facets).
  * bit-identical across two separate Blender processes, 14/14.
  * spec.OPENINGS untouched: nothing here goes near a window bay.

===============================================================================
NINETEENTH PASS -- FRACTIONAL BAYS. THE STRETCH WAS THE BUG.
===============================================================================
Shanee, twice, of the assembled inn:
  "SM_Wall_Timber_2m_A.002 and others have a strange z scaling making them
   taller than their neighbours (for example SM_Wall_Timber_2m_A.024)"
  "We should also include half tiles/quarter tiles as items that can be
   supported (both vertical and in the grid dimension, for example for half
   width walls, or half height walls as we used in with the gable, etc)"

MEASURED on the 852-object showpiece, and the first one is exactly what it looks
like:
    SM_Wall_Timber_2m_A     19 objects at scale (1.0, 1.0, 1.154)
    SM_Wall_Timber_2m_B     11 objects at scale (1.0, 1.0, 1.154)
    SM_Wall_TimberWin_2m    12 objects at scale (1.0, 1.0, 1.154)
                            -- 42 objects, every timber member on them 15.4%
                               taller than it was cut, in one axis only
1.154 is assemble_inn.py's own `zs = HG / HU = 3.00 / 2.60`. It is not a bug in
the assembler: until this pass there was not one authored fractional piece in the
kit -- every wall in every family is `_2m`, full GRID wide and full H_UPPER high
-- so filling a 3.00 m storey with 2.60 m of wall left the scale handle as the
only tool on the table. THE FIX BELONGS HERE: cut the wall the height it has to
stand at.

NINE NEW PIECES, and every one of them is AUTHORED at its size rather than
scaled to it. See THE FRACTIONAL FOOTPRINTS, above the constants, for what each
decided and why; the short version is that none of the family's numbers survives
a multiplier -- at half the width the stop-chamfer would be 13 mm, the adze
facets 5 mm and `_brace_arc`'s ellipse 1:2.13, which is a bent post and not an
arch -- so each footprint re-decides its own pattern:

    SM_Wall_Timber_1m_A         1.000 x 2.600  posts, all four horizontals, the
                                family's sill line and ONE arch brace fitted to
                                it (0.930 x 0.814, ratio 0.875 against the 2 m
                                bay's 1.027 -- the same quarter circle, smaller)
    SM_Wall_Timber_1m_B         1.000 x 2.600  close studded: one centre post,
                                two 0.355 panels, one lozenge
    SM_Wall_TimberWinAttic_1m   1.000 x 2.600  OPENINGS["win_attic"] 0.52 x 0.58
                                at sill 0.600 -- NOT win_upper, which is 1.50 m
                                wide and therefore wider than the whole bay
    SM_Wall_Timber_0m5_A        0.500 x 2.600  posts and infill, no brace, no
                                stud, no lozenge: at 0.340 m of field every
                                figure the family owns is bigger than the gap
    SM_Wall_TimberTall_2m_A     2.000 x 3.000  bay A cut to an H_GROUND storey
    SM_Wall_TimberTall_2m_B     2.000 x 3.000  bay B, ditto
    SM_Wall_TimberTallWin_2m    2.000 x 3.000  win_upper UNMOVED (1.500 x 1.450
                                at sill 0.950), and the only full-width window
                                bay in the family that carries all four shared
                                horizontals -- in 3.00 m there is finally room
                                for the mid rail to pass OVER the opening
    SM_Wall_TimberKnee_2m       2.000 x 1.300  a knee wall: sole plate, the
                                family's full 0.180 wall plate, and one 1.79:1
                                LANDSCAPE field with a flat segmental arch in it
                                (1.930 x 1.102, ratio 0.571)
    SM_Wall_TimberBand_2m       2.000 x 0.400  a plinth course, HG - H exactly.
                                It goes UNDER a 2.60 m wall, not over: the wall
                                plate has to be AT the storey head.

MEASURED, all of it on the BUILT MESH:
  * EVERY PIECE REPORTS AN EMPTY REPORT. 25 pieces, 448-2264 tris against the
    5200 wall budget; the nine new ones are 448-1484. Nothing clamped.
  * THE FOOTPRINTS ARE EXACT. Every piece's bounding box lands on its declared
    seams to 1e-4: x +-0.250 / +-0.500 / +-1.000, z 0..0.400 / 1.300 / 2.600 /
    3.000, y 0..0.240 with the deepest relief at -0.1168 (PROUD_MAX is 0.16).
  * THE OPENING CONTRACT HOLDS, ray-cast by `measure_opening` on the built mesh:
        SM_Wall_TimberTallWin_2m   w 1.5000  h 1.4500  sill 0.9500  head 2.4000
        spec.OPENINGS["win_upper"]   1.5000    1.4500       0.9500       2.4000
        SM_Wall_TimberWinAttic_1m  w 0.5200  h 0.5799  sill 0.6001  head 1.1800
        spec.OPENINGS["win_attic"]   0.5200    0.5800       0.6000       1.1800
    i.e. the tall bay is spec to the micrometre and the half bay to 0.2 mm, which
    is inside the probe's own 1.5 mm step. Both directions of the contract are
    checked -- see THE HALF BAY'S WINDOW IS NOT win_upper for the insert side.
  * THE SEAM. Vertex-identity is the wrong test across two different footprints,
    so this pass measures the SECTION each bay presents at the shared plane:
    collect every face lying wholly on it, rasterise the union at 2 mm, and
    difference the masks. Controls first -- a piece against itself is 0.0 cm2,
    a wall against a jetty (0.45 m deeper) is 267.4 cm2 -- then, against
    SM_Wall_Timber_2m_A's -x section:
        SM_Wall_Timber_1m_A          36.2 cm2   0.5 %
        SM_Wall_Timber_1m_B          55.9 cm2   0.7 %
        SM_Wall_TimberWinAttic_1m    31.5 cm2   0.4 %
        SM_Wall_Timber_0m5_A         47.1 cm2   0.6 %
      ... against the family's OWN existing spread, measured the same way:
        SM_Wall_Timber_2m_B          85.7 cm2   1.1 %
        SM_Wall_TimberWin_2m         73.2 cm2   0.9 %
        SM_Wall_Timber_2m_A_Rough    46.0 cm2   0.6 %
    A fractional bay therefore butts a full bay at least as well as two full bays
    butt each other, and better than most. In Z, a band's top against a wall's
    bottom is 74.2 cm2 (1.3%) where a WALL's top against a wall's bottom -- two
    ordinary stacked storeys, the family's own baseline -- is 529.2 cm2 (8.5%).
  * THE DETAIL IS REACHABLE, not buried. Head-on rays on a 2 mm grid, with the
    harness's controls stated: a panel's middle returns 100% plaster at mean
    y = -0.023 and never once reaches PANEL_BACK (deepest first hit -0.0143), and
    the core's front face behind a half-post returns 0% plaster (100% oak_dark at
    y = -0.072), i.e. a buried surface correctly reports as the thing in front of
    it. Then: all three new arch braces 100% oak along their own centre lines at
    y = -0.045 to -0.047, against the existing 2 m brace's -0.044; the three new
    lozenges 99.9-100% oak over their own inscribed square, standing at
    y = -0.047 to -0.051 in front of a panel crowned at -0.034, against the two
    existing lozenges' 99.8-100% (the control -- the same box moved sideways onto
    bare panel -- reads 0.0% and 2.6%); the new post pegs 51.2% / 50.7% oak_pale
    over their own
    footprint against the existing pegs' 48.8% / 48.0%; and the tall window bay's
    transom 100% oak right across the opening, which is the piece's whole claim.
  * check_zfight.py -- timber_walls: ZERO pieces at 0.2 mm, and NO NEW PIECE
    appears at 0.5 mm or 1.5 mm either. The two pairs those finer passes do
    report (SM_Wall_TimberGable_2m, SM_Wall_Timber_2m_C) are on pieces this pass
    proved bit-identical, so they are pre-existing and not this pass's.

NOT REGRESSED, checked rather than asserted:
  * ALL SIXTEEN EXISTING PIECES ARE BIT-IDENTICAL -- same vertex positions to
    1e-6, same face-to-material assignment, same topology, 16/16. That is the
    point of `_bay`: `_bw`/`_bh`/`_xe` fall back to G, H and XE, so every piece
    written before this round takes the identical code path.
  * THE RATIO. `measure()` returns the round-15 table to two decimals on the
    fourteen pieces it was quoted for: 51.24% timber against the docstring's
    51.25%. The nine new pieces measure 25.0-52.3% and pull the 25-piece mean to
    48.5%; the two 3.00 m plain bays are the LEAST timber in the whole family
    (25.0% and 26.2% against the 2.60 m bays' 27.1% and 28.0%), because the extra
    0.40 m is panel.
    `measure()` and `measure_opening()` both had to learn the piece's own
    footprint to say any of that -- see `_footprint`. On a 3.00 m bay the old
    fixed scan window missed the top 0.40 m outright, which is the frieze and the
    wall plate, i.e. the two most timber-dense bands on the piece.
  * NO ROUGH SIBLINGS, and that is a decision rather than an omission. See
    THE ROUGH HALF OF THE FAMILY.

===============================================================================
TWENTIETH PASS -- THE PLATE BAND, AND A 0.70 m SLOT ALONG EVERY EAVE.
===============================================================================
Found by the assembler's own auditor, not by this module, and quoted because the
fix is a piece rather than a patch. assemble_inn.storey() closes the gap between
a timber storey's head and the roof datum with a band:

    bh = band_h if proud else band_h - BAND_TUCK      # BAND_TUCK = 0.15
    if bh > 0.95:
        put(a 2.60 m wall, scale (1, 1, bh / HU))

The hero's top storey asks band_h = 1.00 on all four sides. On the three EAVE
faces bh is 0.85, which is not greater than 0.95, so the band was skipped in
silence and only the proud south face got one. MEASURED on the hero's west
flank: above z 7.5 there are two wall pieces and both top out at z = 9.050
against an eave at z = 9.747 -- a continuous 0.70 m OPEN SLOT the length of the
flank, 27 rays escaping from inside, and 56-69% see-through from a street
camera, every far hit landing on the inside face of the north wall 11 m away.
The `> 0.95` gate is not the bug either: it is there because the only band
available was a 2.60 m wall squashed to fit, and below about 0.95 the squash
stops being survivable. Author the two heights and the gate can go.

TWO PIECES, because the two faces need different things:

    SM_Wall_TimberBandEave_2m    2.000 x 0.850   the eave-face band
    SM_Wall_TimberBandGable_2m   2.000 x 1.000   the gable-face ("proud") band

Both are the same course -- the low attic band between a storey head and the
roof -- and both are built like the family's own frieze (Z_ATTIC): close studs,
small pillowed panels, one member over them. NEITHER HAS A SOLE PLATE. They are
placed at z + HU, straight onto the storey's own 0.180 m wall plate, so the
plate BELOW is this course's sill; a second one would put 0.275 m of unbroken
timber at the junction and read as a double course. What they get at the foot is
the family's sole BEAD, 0.052 m, which terminates the piece on z = 0 and gives
the panels' grown rim something to tuck under at a fifth of a plate's height.
(It is also why two stacked SM_Wall_TimberBand_2m are the wrong way to make
0.80: four rails in 0.8 m.)

THE ONE PLACE THEY DIFFER IS SET BY A BEAM, AND IT WAS MEASURED, NOT CHOSEN.
On a gable face assemble_inn lands SM_Beam_JettySill_2m_C on top of the band, at
band_top - 0.480. Measured on the BUILT beam: its housing block -- beams' own
SILL_TAIL, "how far the beam is HOUSED into the wall" -- is a full-bay-width
solid spanning y -0.116 .. +0.050, and its BACK is one flat 0.826 m2 quad on
y = +0.050 covering band-local z 0.579 .. 0.992. PANEL_BACK, where every pillowed
panel in this family puts its own flat back, is y = +0.052.
So the naive band -- standard 0.180 m wall plate at the head, field running up to
it -- lays panel back straight into the beam's housing. BOTH WERE BUILT AND BOTH
WERE MEASURED, closest parallel y-face pair and total area within 2.5 mm, band
against beam at its placed height:

    rejected: 0.180 plate at the top, field to 0.820
                          closest  1.0 mm over 579.1 cm2   within 2.5 mm: 1726.0 cm2
    shipped:  bressumer 0.579 .. 1.000, field stops at 0.579
                          closest  8.8 mm over  11.9 cm2   within 2.5 mm:    0.0 cm2

So the gable band's head member is a BRESSUMER, 0.421 m, starting exactly where
the housing starts -- which also makes it the thing the beam is housed INTO,
which is what a bressumer is and why BRESS_Y is in the depth ladder at all. The
panels' back grid, which insets PANEL_BACK_IN from the field line, tops out at
0.573, a clear 6 mm below the housing. The eave band has no beam over it and
takes the family's standard 0.180 m wall plate at its head.

WHY NOT ONE 0.85 PIECE AND LET THE BEAM BE THE REST, which is the cheaper
decomposition and was the first thing checked. The beam's body is in FRONT of
the wall -- nothing of it reaches back past y = +0.050 -- so an 0.85 m band under
a 1.00 m gable line leaves band-local z 0.850 .. 1.000 unfilled from y = 0.050
to y = T on every gable bay: a 0.19 x 0.15 m section, 28.5 dm3 per bay, of
exactly the void this pass exists to close, hidden behind a beam that does not
seal it. Both heights are authored.

MEASURED, on the built mesh:
  * BOTH BANDS ARE OPAQUE. Head-on rays at 4 mm over the whole face, marched
    through to the last hit: 0 open samples out of 99750 and 117800, deepest hit
    y = 0.2400 (the inner face) on every one. CONTROLS for that harness: a plain
    bay's body reads 0 open / 0.2400, a window bay read THROUGH ITS OPENING reads
    0 open / 0.2355 (the reveal backing -- so the harness measures "solid to the
    back", not "has no hole"), and SM_Wall_Timber_2m_A sampled above its own head
    over z 2.605..3.30 -- the slot itself -- reads 82650 open out of 82650, 100%.
  * THE FOOT IS CARRIED. Rasterising the section each piece presents at the joint
    and differencing: 99.2% of the eave band's bottom section and 99.0% of the
    gable band's lands inside the wall plate's top section beneath it. The 35 and
    43 cm2 that do not are edge quantisation at a 2 mm cell over ~10 m of section
    perimeter. The pieces present less than the plate does (4487 and 4481 cm2
    against 6256) because they have no sole plate -- that is the design, not a
    gap: everything they do present is bearing.
  * THE SEAM. Each band's +x section equals its own -x section EXACTLY (0.0 cm2
    mismatch, 2 mm raster, controls as in round 19).
  * check_zfight -- timber_walls: ZERO pieces at 0.2 mm; at 0.5 mm the only
    report is the pre-existing SM_Wall_TimberGable_2m pair, on a piece this pass
    leaves bit-identical.
  * both report an EMPTY report, 676 and 688 tris against the 5200 budget, and
    their bounding boxes land on their declared seams to 1e-4.
  * THE RATIO: eave band 40.5% timber, gable band 57.0%. The gable band is the
    fourth most timber-heavy piece in the family and that is what it is -- a
    bressumer band under a gable is mostly beam. Every other piece is unchanged
    to the decimal and the 27-piece family mean is 48.5%.

WHAT BEDS ON WHAT, since an assembler places these at z + HU and needs to know:

    SM_Wall_TimberBandEave_2m    bead 0.000..0.052 | field 0.052..0.670 |
                                 WALL PLATE 0.670..0.850, top face z = 0.850
    SM_Wall_TimberBandGable_2m   bead 0.000..0.052 | field 0.052..0.579 |
                                 BRESSUMER 0.579..1.000, top face z = 1.000
    both: seam half-posts from z = 0 up to 15 mm inside the head member, cut dead
    flat on z = 0 and on the top; y = 0..T; x = +-1.000; nothing clamped.

NOT REGRESSED: all 25 pieces from round 19 and before are BIT-IDENTICAL.
"""
import bpy, bmesh
from math import cos, sin, radians, tan, sqrt, pi
from mathutils import noise, Vector, Euler
from kit import spec as S
from kit.util import Part, rng, lerp, clamp, smoothstep

FAMILY = "timber_walls"
COLLECTION = "02_Walls_Timber"

G = S.GRID                 # 2.0  bay width
T = S.T_TIMBER             # 0.24 wall thickness
H = S.H_UPPER              # 2.6  storey height
J = S.JETTY                # 0.45 overhang

SEAMS = dict(x=(-G / 2, G / 2), y=(0, T), z=(0, H))
SEAMS_J = dict(x=(-G / 2, G / 2), y=(0, T + J), z=(0, H))

# =============================================================================
# ============= A PIECE'S OWN FOOTPRINT -- FRACTIONAL BAYS  (round 19) ========
# =============================================================================
# Shanee, twice, of the assembled inn:
#   "SM_Wall_Timber_2m_A.002 and others have a strange z scaling making them
#    taller than their neighbours (for example SM_Wall_Timber_2m_A.024)"
#   "We should also include half tiles/quarter tiles as items that can be
#    supported (both vertical and in the grid dimension, for example for half
#    width walls, or half height walls as we used in with the gable, etc)"
#
# MEASURED on the 852-object showpiece, and the first complaint is exactly what
# it looks like:
#     SM_Wall_Timber_2m_A     19 objects at scale (1.0, 1.0, 1.154)
#     SM_Wall_Timber_2m_B     11 objects at scale (1.0, 1.0, 1.154)
#     SM_Wall_TimberWin_2m    12 objects at scale (1.0, 1.0, 1.154)
# 1.154 is assemble_inn.py's own `zs = HG / HU = 3.00 / 2.60`: a wall authored at
# H_UPPER being stretched to fill an H_GROUND storey, so every timber member on
# 42 objects is 15.4% taller than it was cut. No amount of carving survives
# that -- the stop-chamfer, the adze facets and the arris wear are all sized in
# millimetres and all of them come out 15% long in one axis only.
# THE FIX IS NOT IN THE ASSEMBLER, IT IS HERE: a wall that has to stand in a
# 3.00 m storey should be CUT 3.00 m tall. Until this round there was not one
# authored fractional piece in the family -- every wall in every family is named
# `_2m`, full GRID wide and full H_UPPER high -- so the assembler had nothing to
# reach for but the scale handle.
#
# WHAT A FRACTIONAL PIECE HAS TO GET RIGHT. Six functions in this module were
# written when there was only ever one footprint and had `G / 2`, `XE` or `H`
# spelled into them: `_core` (its outer rect), `_posts` (where the half-posts
# are), `_rails` (the length of every band), `_frieze_x` (the stud spacing),
# `_mem`/`_cut` (which members get pushed back onto a tiling plane) and
# `_worked` (which SIDE of a member lies on a tiling plane and therefore may not
# be facet-tilted -- see `tm` in that function, and the ninth pass's measurement
# of why). Those are now read off the PART, not off the module:
#
#     p = _bay(_reserve(Part("...", seams=_seams(w=G_HALF))), w=G_HALF)
#
# and everything downstream asks `_bw(p)` / `_bh(p)` / `_xe(p)`. The defaults are
# G and H, so every one of the sixteen pieces that came before this round takes
# the identical code path and builds a bit-identical mesh -- checked, not
# asserted, by hashing all sixteen before and after.
#
# WHY A STAMP ON THE PART AND NOT A THREADED ARGUMENT. `p` is already the first
# argument of every builder in this file, so the bay travels with the thing it
# describes and there is no way to build a member for one footprint into a piece
# declared with another. Threading `bw=` through `_mem` -> `_worked` instead
# would have touched ~50 call sites to say something the Part already knows.
def _seams(w=G, h=H, jetty=0.0):
    """The three seam planes of a piece `w` wide, `h` tall. x is the bay tiling
    plane, z the storey stacking plane, y the wall's own thickness."""
    return dict(x=(-w / 2, w / 2), y=(0, T + jetty), z=(0, h))


def _bay(p, w=G, h=H):
    """Stamp the piece's OWN bay width and storey height onto the Part.

    Call it on every Part in this module, next to the `seams=` it must agree
    with. `_bw`/`_bh`/`_xe` are the only readers, and they fall back to the
    full-bay values so an unstamped Part behaves exactly as it did before this
    round existed.
    """
    p.bay_w, p.bay_h = w, h
    return p


def _bw(p):
    return getattr(p, "bay_w", G)


def _bh(p):
    return getattr(p, "bay_h", H)


def _xe(p):
    """Inner face of this piece's edge half-posts -- XE, for its own width."""
    return _bw(p) / 2 - W_POST / 2

# ---------------------------------------------------------------- depths -----
# core -> pillowed panel -> boarding -> timber face, each step a real shadow.
#
# The BACK of every layer matters as much as its front: two solids that end on
# the same y plane and overlap in x/z are a z-fight, so the back planes are
# deliberately staggered -- and so are the FRONT planes of members that cross
# each other, because the post used to face -0.094 against a rail at -0.096 and
# 2 mm apart is a fight too. The numbers below are the whole ladder:
#
#   -0.092  PLATE_Y     WALL PLATE face -- the proudest band on the wall, so the
#                       half-post's head is buried behind it, not poking through
#   -0.086  BEAD_Y      sole bead: proud of the post so its FOOT is buried too
#   -0.080  POST_Y      seam half-post face: PROUD of the mid rails, so a rail a
#                       variant does not carry dies into the post's side instead
#                       of stopping dead in mid-air at the seam
#   -0.070  BY          sole / transom / sill / apron / ledger rail face
#   -0.050  FY          stud / brace / frieze face
#   -0.046  JAMB_Y      window jamb face -- CROSS-FAMILY CONTRACT, see below
#   -0.032              boarding face
#   -0.026  PANEL_Y     plaster panel crown
#    0.030  PY          plaster panel RIM plane (where a panel meets the frame)
#    0.040  FY+FD       stud / brace back
#    0.052  PANEL_BACK  pillowed panel's flat back
#    0.060  POST_BACK   post back
#    0.066  BY+BD       rail back (sole, transom, head, sill, apron, ledger)
#    0.074  CORE_Y      plaster backing core FRONT -- behind every timber
#    0.086  CORE_Y+.012 the cream cheek plate's back (`_cheek`)
#    0.088+              boarding back, buried inside the core
#    0.098  DRIP_BACK   the drip mould's back
#    0.112  JAMB_Y+JAMB_D  jamb back -- ROUND 16 moved it here from 0.080. It
#                       was 6 mm inside CORE_Y and the HEWN jamb's depth jitter
#                       swings +-15 mm, so on the rough bays it landed ON the
#                       core's front face: 216 cm2 measured, plaster against
#                       oak_mid. See THE JAMB'S BACK HAD 6 mm AND USED 15.
#    0.240  T           inner face: the core, and ONLY the core
#
# ROUND 10 -- THE LADDER WAS COMPRESSED, and it is half the answer to "the wall
# reads as brown timber with cream slivers". The frame used to stand 58 mm (stud)
# to 106 mm (wall plate) in front of the plaster crown. At the kit's light angle
# that throws a shadow onto the panel roughly as wide as the relief is deep, so
# every 0.19 m member was painting a ~0.29 m dark band on the wall: the plaster
# was being eaten by shadow, not by timber. Every proud plane is now roughly
# halved -- stud 24 mm, rail 44, post 54, plate 66 -- while the GAPS BETWEEN
# consecutive planes are preserved to the millimetre (plate 6 bead 6 post 10 rail
# 20 stud / jamb 14 board 6 crown), because those gaps are what stop two crossing
# members sharing a face plane. Nothing about the frame's LAYOUT moved with it.
#
# CROSS-FAMILY CONTRACT, do not "tidy" it: windows.py._head sets its proud plane
# at y = -0.060 and says so in a comment, chosen to sit 14 mm clear of BOTH of
# this module's proud planes at the window -- the jamb at -0.046 and the stud at
# -0.072. So JAMB_Y IS PINNED AT -0.046 and is deliberately not derived from FY
# any more, and the compressed planes were picked to keep every one of them at
# least 10 mm off -0.060. A casement therefore still drops into a window bay with
# its head board standing correctly proud of the wall's jamb.
#
# ROUND 11 -- THE CROWN CAME FORWARD INSTEAD. Shanee, off the assembled inn:
# "it seems like you replaced most walls in the 1st floor with wood while the
# reference is the plaster/white ones". Measured head-on (see the RATIO block
# below for the harness) the family averaged 63% timber and, counting the
# plaster the frame's own relief shades, 70% dark. Round 10 attacked that by
# pulling the FRAME back, and it ran out of room: BY cannot come in past -0.070
# without breaking the 10 mm clearance windows.py needs at -0.060. So this pass
# takes the last 12 mm from the OTHER end -- the plaster crown moves OUT from
# -0.026 to -0.034, which shortens every shadow on the wall without moving one
# frame member. The GAPS between the frame's own planes are untouched, so
# nothing that stopped a z-fight has moved.
# ... AND THE RIM CAME WITH IT, which is the half of this that actually matters
# and which the first attempt got wrong. What throws the shadow is not the step
# from the frame face to the panel CROWN, it is the step to the plaster the eye
# sees FIRST -- the plaster immediately inside the frame, which is down at the
# panel's RIM. With PY at 0.030 that step was 80 mm at a stud and 100 mm at a
# rail: a trench round every panel, and moving only the crown made it worse, not
# better, because `belly` is measured rim-to-crown and the cushion simply got
# 12 mm deeper (measured: shadowed plaster 7.2% -> 7.4%, i.e. nothing).
# PY 0.030 -> 0.000 puts the render FLUSH WITH THE WALL PLANE where it meets the
# frame and bellies 38 mm out of it between -- so the frame stands 50 mm proud
# of the plaster at a stud and 70 at a rail instead of 80 and 100, the cushion
# is shallower than it was rather than deeper, and the timber reads as drawn ON
# a cream wall instead of as a lattice standing in front of one. Nothing else in
# the ladder moved, so every gap that stops a z-fight is where it was.
#   Measured, plain bay A, the rim move alone: shadowed plaster 7.4% -> 4.7% of
#   the face, and the piece's `dark` total 34.5% -> 31.8%.
#
# HOW FAR IS TOO FAR, because there is a floor under this. The frame still has
# to READ as timber in Solid shading, and what makes it read is the step from
# its face to the plaster beside it. The crown stops at -0.034 rather than going
# flush, which leaves 16 mm at an arch brace, 18 at a frieze stud (whose cushion
# is height-limited), 36 at a rail, 44 at a post and 58 at the wall plate. At
# -0.038 the brace was down to 12 mm and visibly sinking into the render, so the
# members that carry the frame's silhouette keep their relief and only the
# trench around the panel is gone.
PY = 0.000          # plaster panel RIM plane -- see below
PANEL_Y = -0.034    # pillowed panel crown (0.034 in front of the rim)
ROUGH_BELLY = 0.008 # how much further than PANEL_Y a HAND-FLOATED panel may
                    # crown. See `_panel`; it was 0.020 and had to come down
                    # when the rim moved to y = 0.
BOARD_Y = PANEL_Y - 0.004   # -0.038  vertical boarding face. Derived, so the
                            # boarding follows the crown; 4 mm behind it, and
                            # the boarded regions never overlap a jamb, which
                            # is the only other plane it comes near.
PANEL_BACK = 0.052  # the panel shell's flat back
PANEL_BACK_IN = 0.030
# ROUND 12 -- HOW FAR THE PANEL'S BACK STOPS SHORT OF ITS OWN FRAME LINE.
# The shell's back used to be built on the SAME grown rectangle as its front, so
# the flat plane at PANEL_BACK ran on UNDER every member the panel tucks beneath
# -- and the ladder above leaves it only 8 mm of air under a post (0.052 against
# POST_BACK 0.060) and 14 mm under a rail. On the hand-made bays, where `grow` is
# 40 mm and both surfaces then carry `_wob`, that 8 mm closed completely and the
# post's back and the plaster's back became ONE plane: 57 cm2 of oak_dark against
# plaster measured on SM_Wall_Timber_2m_B_Rough at y = 0.055, x = 0.96 -- i.e. in
# the +X half-post, on the bay seam, so it tiled into the next bay as well.
# DEPTH CANNOT FIX IT. Between the stud back at 0.040 and the rail back at 0.066
# there is nowhere left for a plane that is more than ~12 mm off something, and
# the panel's own rim (y = 0, +-0.009 on a rough bay) stops it moving forward.
# So the separation is taken in X and Z instead, where there is room: the back
# grid stops 30 mm INSIDE the frame line, front and back are joined by a sloped
# rim strip that the frame covers, and the panel's back no longer lies under any
# member at all. Clearance to the post back: 8 mm of y -> 30 mm of x.
# It also has to survive TILING, which is the reason 30 mm and not 8: two bays
# side by side make one W_POST post out of two half-posts, so a panel back that
# creeps past XE is under the neighbour's timber as well as its own.
CORE_Y = 0.074      # backing core front face: behind the deepest timber back
FY, FD = -0.050, 0.090      # post / stud / brace: outer face, depth
BY, BD = -0.070, 0.136      # sole / transom / sill / apron rail: outer face, depth
JAMB_Y = -0.046             # window jamb face. PINNED -- see the note above.
BEAD_Y = BY - 0.016         # -0.086  sole bead: 6 mm proud of the post
POST_Y = BY - 0.010         # -0.080  half-post face: 10 mm proud of the rails
POST_BACK = 0.060
PLATE_Y = BY - 0.022        # -0.092  wall plate face: 12 mm proud of the post
BRESS_Y = -0.100            # the jetty bressumer, the one band allowed to be
                            # bolder than the wall plate (it carries a storey)

# How far a seam-crossing member is built PAST the tiling plane before being cut
# flat on it. Must exceed the largest bevel any such member uses (S.BEVEL_W,
# 0.018) or a chamfer survives at the seam and the groove comes back.
SEAM_CUT = 0.030

# ---------------------------------------------------------------- frame ------
# THE FACADE IS A CREAM WALL WITH TIMBER DRAWN ON IT, not a brown lattice. That
# sentence was already written into assemble_inn.py as a diagnosis and this block
# is where it gets paid for, because a ratio is decided by member WIDTH before
# anything else.
#
# ===================== THE RATIO, MEASURED  (round 11) =======================
# THE HARNESS. Build the family headless, then for each piece ray-cast a 4 mm
# grid straight at its face -- from y = -2 along +Y, over x in [-1, 1] and
# z in [0, H] -- and ask which material the FIRST hit belongs to. That is
# literally "what fraction of the wall face, seen head-on, is timber". Every
# plaster hit then fires a second ray at the kit's sun (R.sun's (52, 0, 34)); a
# plaster sample the frame's own relief shades is plaster the eye reads as
# frame, so `dark` = timber + shadowed plaster is the number Shanee's complaint
# is actually about. It is deterministic, it needs no render, and it is the only
# way to argue about a ratio instead of eyeballing one.
#
# WHERE ROUND 10 LEFT IT, and it is much worse than round 10's own note claims,
# because that note only ever measured the PLAIN bay:
#
#     piece                     timber   plaster   shadow    dark
#     SM_Wall_Timber_2m_A        32.7%     67.3%     7.2%    39.9%
#     SM_Wall_Timber_2m_B        33.2%     66.8%     7.9%    41.1%
#     SM_Wall_Timber_2m_C        87.6%     12.4%     5.8%    93.4%   <- boarded
#     SM_Wall_TimberWin_2m       74.3%     25.7%     5.6%    79.9%
#     SM_Wall_TimberJetty_2m_A   58.2%     41.8%     6.3%    64.6%
#     SM_Wall_TimberJetty_2m_B   95.3%      4.7%     3.5%    98.9%
#     SM_Wall_TimberGable_2m     63.3%     36.7%     5.5%    68.7%
#     ... rough siblings within 2 points of their regular twins ...
#     FAMILY MEAN                63.0%     37.0%     6.4%    69.5%
#
# So the plain bay was fine and everything else was a plank wall. Three quarters
# of the family's timber was NOT in the framing at all: it was BOARDING (C, both
# jetty aprons) and window LINING. A facade built out of those bays is a brown
# building however narrow the studs are, which is exactly what Shanee is
# looking at. What this round changes, in the order it pays:
#
#   1. C and the jetty aprons stop being boarded TOP TO BOTTOM. ref3's boarded
#      walls are boarded UNDER a rail with render above (crop ref3:timber and
#      look under the windows) -- so boarding now stops at the family's sill
#      line and the bay above it is plaster. Character kept, area halved.
#   2. every section slimmed again, ~0.78x: post 0.195 -> 0.160, stud 0.170 ->
#      0.130, thin 0.140 -> 0.105, brace 0.135 -> 0.100, sole 0.130 -> 0.095,
#      transom 0.105 -> 0.078, and the gable's own set with them.
#   3. the plaster crown came out 12 mm (see PANEL_Y), which shortens every
#      shadow the frame throws without moving a single member.
#   4. checked, per the brief: nothing tints the panel down. `_panel` is the
#      palette tone; `plaster_dim` appears only on inner faces and reveals,
#      which is what spec says it is for. The gable's two plaster shades were
#      still at 0.92/0.98 and are now 0.96/1.00 -- it was the only piece in the
#      family whose cream was not full strength.
#
# ON THE REFERENCE, HONESTLY. Measured off ref3's linework at 49 px/m, its own
# studs run ~0.30 m at ~2.1 m centres and its rails ~0.27 m -- WIDER than ours,
# not narrower. That is not an argument for widening ours, because ref3 draws
# its timber as light grey outlined in ink while our oak_dark is #3E2C22 against
# #E4D9BE plaster: the same width of our timber carries far more visual weight
# than the same width of theirs. The palette is kit-wide and not ours to change,
# so the only lever left for matching the reference's VALUE balance is to use
# less timber. That is the whole argument for the sections below, and it is why
# they are narrower than the thing they are copying.
#
# WHAT MAY NOT MOVE: Z_HEAD[0]. The wall plate is the LINTEL over win_upper
# (head 2.40 + 20 mm of core) and it has to reach z = H, so 0.180 m of the bay is
# wall plate by construction and no ratio work can touch it.
W_POST = 0.160      # a bay-seam post = two 0.080 half-posts
W_STUD = 0.130      # the ONE intermediate post a bay ever gets
W_THIN = 0.105      # frieze studs, ledgers
W_BRACE = 0.100     # curved arch brace
Z_SOLE = (0.000, 0.095)
Z_TRAN = (2.000, 2.078)             # the mid rail
Z_HEAD = (2.420, H)                 # the wall plate -- PINNED, it is the lintel
Z_FIELD = (Z_SOLE[1], Z_TRAN[0])    # 0.095 .. 2.00, ONE panel tall
Z_ATTIC = (Z_TRAN[1], Z_HEAD[0])    # 2.078 .. 2.42, the frieze
XE = G / 2 - W_POST / 2             # 0.920, inner face of the edge half-posts
BURY = 0.020        # how far a member is sunk into the one it lands on, so the
                    # joint is a joint and not two faces kissing on one plane
OAK = "oak_dark"    # KIT-WIDE TABLE: every structural member. Named, not rolled.

OPEN = S.OPENINGS["win_upper"]      # 1.50 x 1.45, sill 0.95 -> head 2.40

# THE FAMILY'S ONE SILL LINE. Four pieces carry a horizontal band at the window
# sill -- the window bay, the jettied window bay, the jettied plain bay (whose
# apron rail has to line up with its neighbour's) and, since round 11, the
# boarded bay, whose ledger IS this band. One pair of numbers for all of them,
# so any two of those bays standing side by side share one line.
#   SILL_TOP is spec's own sill and may not move: the casement sits on it.
#   SILL_H came down from 0.176 to 0.118 -- it was the third-widest band in the
#   family and it crosses the bay at the height the eye is at.
SILL_TOP = OPEN["sill"]             # 0.95
SILL_H = 0.118
APRON_TOP = SILL_TOP - SILL_H       # 0.832: top of a boarded apron / of the
                                    # plaster under a sill. Boarding and panels
                                    # are grown 26 mm PAST it so the rail laps
                                    # them instead of butting on one plane.

# ===================== THE SILL BELONGS TO THE WALL  (round 13) ==============
# Shanee, of the assembled inn: "SM_Win_LeadedCasement_A.002 doesn't seem to fit
# SM_Wall_TimberWin_2m.007 properly and both add their own window sill and there's
# various overlapping wood pieces". Both families were building a cill under the
# same opening, so every upper window in the building carried two of them, one
# behind the other, 30-60 mm apart. Only one family can own it, and it is this
# one, for two reasons that are not preference:
#   * the cill is a piece of the WALL. It is bedded on the sill rail, it runs
#     wider than the opening, and it has to be continuous with the rail whether
#     or not anybody ever drops a casement into the hole. An empty win_upper
#     opening with no cill is a hole in a plastered wall; an insert-owned cill
#     leaves the wall unfinished the moment the level artist leaves the window out.
#   * an insert is INSERT_CLEAR smaller than its opening ALL ROUND, so an
#     insert-owned cill is 20 mm narrower than the reveal it is meant to shed
#     water past. It cannot oversail its own opening without oversailing the wall,
#     which is exactly what the measured casements do (+100 to +260 mm).
# WINDOWS.PY AGREES, and says so in its own header this round: "the wall owns the
# cill", and "NOTHING in a timber-wall leaf leaves the box x in [-0.73, 0.73],
# z in [0, 1.41] -- that is the opening less INSERT_CLEAR all round. No cills, no
# head boards, no architraves, no pent hoods: they are the wall's". That box is
# exactly this module's measured aperture (+-0.750 x 0.950..2.400) less spec's
# 20 mm, so the two halves of the fix meet.
# THE CONTRACT, so windows.py can drop its cill and know what it is landing on:
#   CILL_TOP    = 0.950 = OPENINGS["win_upper"]["sill"]. The wall's cill tucks
#                 CILL_DROP under it, and the top of the reveal's sill -- the
#                 surface an insert's bottom rail beds on -- is spec's own sill
#                 plane, cut by `_core` and the sill rail, dead flat, no wobble
#                 (see `_open_fade`).
#   the cill projects to y = -0.100, i.e. 40 mm PROUDER than windows.py's own
#   casing/head plane at -0.060, so the casement sits behind the wall's cill nose
#   and the two cannot fight for the same 60 mm of air.
CILL_DROP = 0.008   # how far the cill's top tucks UNDER the sill line. It may not
                    # be zero: the sill rail's top face IS z = SILL_TOP over
                    # y = -0.070..0.066 and the cill overlaps that band, so a cill
                    # top at 0.950 would lay 1520 cm2 of oak on oak in one plane --
                    # the largest z-fight this family has ever had. 8 mm reads as
                    # the bedding joint it is and is 40x check_zfight's tolerance.
CILL_H = 0.064      # depth of the cill member on the face of the wall
JAMB_W = 0.062      # oak lining each side of a win_upper opening (was 0.086);
                    # the rest of the 0.176 gap to the post is cream `_cheek`

# ===================== THE JAMB'S BACK HAD 6 mm AND USED 15  (round 16) ======
# MEASURED. Adding a second window bay put a second draw of the same dice on the
# table and it came up the other way: check_zfight at the 0.5 mm pass, on
# SM_Wall_TimberWinLow_2m_Rough, 216 cm2 at [0.885, 0.074, 1.259] -- M_plaster
# against M_oak_mid. Probed in the built mesh, the pair is
#     the core's cheek rect FRONT face   y 0.0739..0.0742  (x 0.769..1.000)
#     the hewn jamb's BACK face          y 0.0701..0.0900  (x 0.750..0.814)
# i.e. the jamb's back plane is NOMINALLY 6 mm inside CORE_Y -- the depth ladder
# has always said "buried inside the core" -- and `_hewn`'s depth jitter is
# dj * d * (0.30 + 1.00) = 0.09 * 0.126 * 1.30 = +-15 mm. A 15 mm excursion in a
# 6 mm slot lands on the plane roughly half the time, and WHICH half is decided
# by an rng seed. This is not a new defect: the same signature is the 180 cm2
# that SM_Wall_TimberJetty_2m_B_Rough reports at the 1.5 mm pass, at
# [0.885, 0.074, 1.679] -- the same two faces, the same 6 mm, a luckier draw.
# THE FIX IS BOTH HALVES OF THE ARITHMETIC, because either alone leaves it thin:
#   * the SLOT. JAMB_D puts the back at 0.112 -- 38 mm behind the core's front,
#     26 mm behind the cheek plate's back (0.086) and 14 mm behind the drip
#     mould's back (0.098), which are the only other planes in that strip. It is
#     still a lining buried in the core, as the ladder always said; it is buried
#     by 38 mm instead of by 6.
#   * the EXCURSION. `_hewn(djd=)` scales the DEPTH jitter only. `_jamb_rough`
#     passes 0, so the width and the lateral wander -- the hand-made character,
#     all of which `anchor` throws onto the free post-side arris -- are
#     completely unchanged, and the two planes that have contracts on them (the
#     front at JAMB_Y, pinned against windows.py at -0.060; the back) stop
#     moving. Same rng draws, so nothing else about the member shifts.
# This is round 15's rule applied to a plane instead of to a facet: scale the
# carving to the clearance the member actually has, and separate what is left.
JAMB_D = 0.158      # jamb depth: back face at JAMB_Y + JAMB_D = 0.112
JAMB_LAP = 0.000
CHEEK_END = 0.004   # how far the cream cheek beside a jamb stops SHORT of the
                    # jamb's own ends. Both members ran zj0..zj1 and the jamb
                    # laps the cheek in x, so their top faces -- and their bottom
                    # faces -- were one plane over an 8 x 86 mm rectangle: 7.0
                    # cm2 an end, 23% ray-reachable and face-on through the slot
                    # behind the transom. 4 mm is far more than the ~0.3 mm the
                    # local wobble differential can close, and both ends of the
                    # cheek are covered by the jamb, the post and the rails
                    # anyway. See `_jamb`.
# ROUND 13 -- THE JAMB NO LONGER LAPS THE OPENING, because the lap WAS the hole.
# The jamb used to stand its reveal face 6 mm inside the aperture on each side, so
# the hole this module actually cut measured 1.4855 x 1.4191 (SM_Wall_TimberWin_2m,
# ray-cast in the built mesh -- see `measure_opening` at the bottom of this file)
# against spec's 1.500 x 1.450. The lap was introduced to stop the oak jamb face
# and the core's plaster reveal face landing on one plane 6 mm apart; round 12
# already solved that a better way by standing the core's cheek back REV_SPLAY
# (20 mm), so the jamb face at +-0.750 is now 20 mm clear of plaster and the lap
# is pure loss. spec.OPENINGS is the law and the hole is the law's only visible
# expression: 1.50 x 1.45 at sill 0.95, measured, or the casement does not fit.
JAMB_X = OPEN["w"] / 2 - JAMB_LAP + JAMB_W / 2   # 0.781, the jamb's centre line

# ROUND 12 -- THE REVEAL IS REBATED, and this is the second of the three measured
# z-fights. The core's hole was cut to the opening EXACTLY, so its cheek stood a
# plaster face on x = +-0.750 running the full depth of the wall, while the oak
# jamb lapping that reveal stood its own face on x = +-0.744. Six millimetres
# apart, parallel, and overlapping over the 6 mm of y where the jamb's back
# (JAMB_Y + 0.126 = 0.080) is already inside the core front (CORE_Y = 0.074) --
# so on the hand-made bay `_wob` closed it and the two flickered plaster against
# oak down the whole 1.45 m of the opening (27 cm2 measured, at [0.748, 0.158,
# 1.673]).
# THE LAP CANNOT GROW TO FIX IT: spec's insert is INSERT_CLEAR smaller all round,
# so the casement's edge is at 0.730 and a jamb lapping more than ~10 mm starts
# fouling the window that drops into the hole. The jamb cannot get shallower
# either -- ending it ON CORE_Y just trades this fight for a much bigger one
# between its back face and the core's front.
# So the CORE moves. Its hole is cut REV_SPLAY wider than the opening on each
# side, which is a rebated reveal -- what a plastered wall actually does around a
# window frame -- and the plaster face lands 26 mm clear of the oak instead of
# 6 mm. Nothing on the outside of the wall moves: the aperture is still
# OPENINGS["win_upper"], set by the jamb, the nose and the head, and the 20 mm
# rebate behind the jamb is closed top and bottom by the core's own bands and at
# the back by `_reveal`'s backing plate, which is oversized to suit.
REV_SPLAY = 0.020   # how far the core's hole is cut PAST the opening, each side

# ===================== WHO OWNS THE SOLID BEHIND THE GLASS  (round 14) =======
# MEASURED, before: this module's reveal backing plate spanned y = 0.140..0.237
# and windows.py's leaf carried its own dark blank back to y = 0.196, so the two
# shared 56 mm through the WHOLE 1.46 x 1.41 aperture -- 115 dm3 of doubled
# opaque solid in every upper window of the building, two surfaces the renderer
# has to sort where one would do.
# Only one family can own that volume and it is split cleanly by WHERE it is:
#   * the front of the reveal (y < REVEAL) belongs to the INSERT. It is the
#     casement's own body -- frame, glass, leading, and whatever blank it wants
#     behind its glass.
#   * the BACK of the reveal belongs to the WALL, because an opening with no
#     casement in it must still not be a see-through hole in a plastered wall.
# So the wall keeps its plate and gets out of the insert's way: BACK_Y is the
# plane its FRONT face now sits on, 60 mm further back than the 0.140 it used to
# take, which is behind every number windows.py publishes for a timber-wall leaf
# (deepest trim 0.116, glass 0.112, interior blank 0.152, blank back 0.196).
# THE CONTRACT, so windows.py can trim to it: NOTHING in a leaf may pass
# y = 0.190. The wall's solid starts 10 mm behind that and runs to T - 0.004.
BACK_Y = 0.200      # front face of the reveal's backing plate
BOARD_BACK = BACK_Y + .010   # the internal window board laps 10 mm into it

# ===================== THE DRIP MOULD IS THE HEAD OF THE HOLE  (round 14) ====
# MEASURED, before: a 4.8-8.2 mm band of CORE PLASTER, at y = +0.074 and 152 mm
# behind the drip mould's nose, ran across the full 1.50 m head of all four
# win_upper bays. Not a shadow -- a cream hairline, the brightest material in
# the kit seen end-on at the darkest line of the wall.
# The cause was round 13's own fix. The drip's soffit was lifted 4 mm off the
# opening's head so that it would stop sharing a plane with the core band above
# the hole (406 cm2 of oak on plaster), and that 4 mm is a WINDOW: nothing else
# occupies it, so a head-on ray at 2.400 < z < 2.404 flies past the mould and
# lands on the front face of the core.
# THE SOFFIT COMES BACK DOWN TO THE HEAD -- it is the head, that is what a drip
# mould over an opening is -- and the plane it used to share is separated in Z
# instead, where there IS room: the CORE's band above the opening starts
# HEAD_LAP higher, so the two soffits are 8 mm apart and the mould keeps its
# full section. Nothing outside the wall moves: the mould's nose, back and top
# are exactly where they were, and the head of the reveal is now the mould's own
# soffit with the core's 8 mm behind and above it.
# THE 8 mm IS IN Z AND NOT IN Y BECAUSE Y HAS NO ROOM. The first attempt took it
# in y -- a 28 mm shallower mould stopping 4 mm short of CORE_Y -- and that puts
# the mould's back face into the 8 mm slot between the core's front (0.074) and
# the WALL PLATE's back (BY + BD = 0.066), which overlaps it over the 20 mm of z
# the two share. Measured: 66 cm2 flagged by check_zfight on
# SM_Wall_TimberWin_2m at [0.024, 0.066, 2.508]. There is no plane in that slot
# for it, so the mould goes back to being deeper than the core face, where its
# back is buried and has no parallel partner at all.
DRIP_Y = -0.082     # the mould's nose -- unchanged, and 78 mm inside PROUD_MAX
DRIP_BACK = CORE_Y + .024   # 0.098: buried inside the core, as it always was
DRIP_H = 0.040      # soffit on the opening's head, top inside the wall plate
HEAD_LAP = 0.008    # how far the core's band starts ABOVE an opening's head, so
                    # its soffit and the drip mould's are not one plane
DRIP_X = OPEN["w"] / 2 + .124   # 0.874: past the end of the widest mould in the
                    # family (the rough one oversails 120 mm on its long side),
                    # so `_open_fade` holds the WHOLE soffit and not just the
                    # part of it over the hole -- see `head_x` in that function

# ===================== THE WINDOW WAS JAMMED UNDER ITS HEAD  (round 16) ======
# Shanee, of the assembled inn: "SM_Wall_TimberWin_2m looks good. I'd like to see
# some other design that put the window more vertically centered or 2/3 -- for
# example in the gable SM_Wall_TimberWin_2m.015 it looks out of balance with the
# walls around it and a more central or lower window option there might look
# better."
#
# It IS out of balance, and the arithmetic says so before any render does.
# spec.OPENINGS["win_upper"] sets sill 0.95 and h 1.45, so the head lands at
# 2.40 in a 2.60 storey. Measured against the two plates -- which are the lines
# the eye actually reads, because they are the only full-width timbers -- the
# window sits
#       0.020 m of core above the head, then the wall plate;
#       0.855 m of plaster below the sill, then the sole plate,
# i.e. 2% of the field above it and 37% below. It is not "high", it is jammed:
# there is no plaster above the hole at all, only the drip mould and the lintel.
# In a gable position, where the triangle above adds another metre of wall, the
# eye reads the whole composition as top-heavy.
#
# WHY CENTRED AND NOT "2/3", MEASURED. The opening is 1.45 of a 2.60 storey --
# 55.8% of it -- so there is only 0.875 m of slack in the whole field
# (0.095 sole-plate top to 2.420 wall-plate soffit = 2.325, less 1.450). A
# "2/3 line" cannot be hit with a window that big: putting its CENTRE two thirds
# of the way up puts the sill at 1.008, i.e. HIGHER than it is now, and putting
# its centre on the lower third puts the sill at 0.142, which is inside the sole
# plate. Split the slack 2:1 in favour of the top and the sill lands at 0.387,
# which leaves 0.174 m under it -- not enough for a sill rail (0.118) plus any
# apron at all. So the only placement that is both available and balanced is the
# CENTRED one, and this variant takes it.
#
# WHERE THE HEAD GOES IS NOT A FREE CHOICE EITHER, and this is the part that
# makes the piece better than "the same bay, slid down". The drip mould over the
# opening is DRIP_H tall and it may not stop a few millimetres short of another
# horizontal: round 14 measured what that costs -- a 4.8-8.2 mm cream hairline of
# core plaster right across the head of every window bay in the family. So the
# mould has to either land ON a band or be buried BURY inside one. The family
# already has a band at exactly the right height: the transom, Z_TRAN, at
# 2.000..2.078. Tuck the mould's top BURY under the transom's soffit and the head
# is fixed:
#       LOW_HEAD = Z_TRAN[0] + BURY - DRIP_H = 1.980
#       LOW_SILL = LOW_HEAD - OPEN["h"]      = 0.530
# ... and that lands 0.435 of field below the sill against 0.440 above the head.
# The window is centred between the two plates to five millimetres, and it got
# there by being hung off the family's own mid rail rather than by being placed
# by eye. That is the whole design of the piece.
#
# WHAT IT BUYS, and why this is not just a lower window: with the head under the
# transom, THIS IS THE ONLY WINDOW BAY IN THE FAMILY THAT CARRIES THE WHOLE
# SHARED FRAME. The existing bay has to drop both the transom and the frieze
# above it, because a 1.45 m casement whose head is at 2.40 has the transom
# drawn straight through it -- so in a run it is the one bay where two of the
# four horizontals simply stop at the post. This one carries sole plate, transom
# AND frieze exactly as the plain bays do, with the window in the field between
# them and its hood tucked under the mid rail, which is precisely what ref3
# draws (crop ref3:timber: pent hood, mid rail over it, boarded frieze above).
#
# THE OPENING AND THE INSERT CONTRACT DO NOT MOVE. Same OPENINGS["win_upper"],
# same 1.500 x 1.450, same jambs, same cill, same drip mould, same reveal
# backing at BACK_Y, same 20 mm of INSERT_CLEAR. The ONLY number an insert has
# to be told is the sill height, and it is LOW_SILL:
#
#       SM_Wall_TimberWinLow_2m       sill z = 0.530,  head z = 1.980
#       SM_Wall_TimberWinLow_2m_Rough sill z = 0.530,  head z = 1.980
#
# so a casement built for SM_Wall_TimberWin_2m drops into this bay unchanged,
# placed 0.420 m lower. The wall still owns the cill, the head drip and the jamb
# linings, at the new height -- see THE SILL BELONGS TO THE WALL, which is
# unchanged except that CILL_TOP for this variant is LOW_SILL.
LOW_HEAD = Z_TRAN[0] + BURY - DRIP_H    # 1.980: mould's top BURY under the rail
LOW_SILL = LOW_HEAD - OPEN["h"]         # 0.530: THE NUMBER AN INSERT NEEDS
LOW_APRON_TOP = LOW_SILL - SILL_H       # 0.412: top of the plaster apron
# The jamb's head dies into the transom, and its own top face has to keep clear
# of the two horizontal planes either side of it: the drip mould's top at
# LOW_HEAD + DRIP_H (2.020) and the frieze panel's grown soffit at
# Z_ATTIC[0] - .020 - .010 (2.048). 2.034 is the middle of that 28 mm slot, so
# both clearances are 14 mm -- 28x check_zfight's 0.5 mm pass and comfortably
# more than the ~3 mm differential `_open_fade`'s ramp can put between two
# surfaces 14 mm apart in z at this height.
LOW_JAMB_TOP = Z_TRAN[0] + .034

# =============================================================================
# ============ THE FRACTIONAL FOOTPRINTS -- WHAT EACH ONE IS  (round 19) ======
# =============================================================================
# THEY ARE AUTHORED, NOT SCALED, and that distinction is the whole commission.
# A half-width wall is NOT a 2 m wall with its studs at half spacing: the studs
# would come out 0.065 wide, the stop-chamfer 13 mm, the adze facets 5 mm and
# the arch brace's ellipse 1:4 -- every one of those numbers was measured and
# argued for at full size and none of them survives a multiplier. So each
# footprint below decides, on its own, what the timber pattern should be at THAT
# size, and each of them is a piece of carpentry that would make sense if you
# cut it.
#
# ---------------------------------------------------------------- the widths -
# G_HALF = 1.00. Two 0.080 half-posts leave a panel field 0.840 wide against the
# full bay's 1.840, so:
#   * THE BRACE STAYS AND THE FIGURE GOES. `_brace_arc` fits its ellipse to the
#     frame, so at half the width and the SAME height it comes out 0.930 x 1.982
#     -- a 1:2.13 quarter ellipse, which is not an arch, it is a bent post. The
#     honest fix is not to drop the brace (the brief and the reference both want
#     one; a narrow bay is exactly where a brace earns its keep) but to give its
#     head a rail to die into at a height that makes the curve an arch again.
#     THE FAMILY ALREADY OWNS ONE AT THE RIGHT HEIGHT: the sill line, APRON_TOP
#     .. SILL_TOP (0.832 .. 0.950), which `c`, `win`, `jetty_a` and `jetty_b`
#     all carry. Landing the head under it gives 0.930 x 0.814, ratio 0.875,
#     against the 2 m bay's 1.930 x 1.982, ratio 1.027 -- both are near-quarter
#     circles and they read as the same detail at two sizes. The head laps
#     `into_rail` up into that rail's soffit exactly as the full bay's head laps
#     the transom's, so both ends of the brace are in solid timber and neither
#     is a floating cut face (which is the defect the third pass existed to fix).
#     The mid-rail FIGURE -- B's intermediate post and its lozenges -- is what
#     the half bay loses; the horizontals are not negotiable (see below).
#   * B ANSWERS WITH CLOSE STUDDING. One 0.130 post on the centre line splits the
#     field into two 0.355 x 1.905 panels: three verticals in a metre, which is
#     close studding, which is a real half-timber pattern and is what ref3 does
#     where its bays are narrow. One lozenge, not two -- there is room for one.
#   * EVERY SHARED HORIZONTAL STAYS. Sole plate, bead, transom, frieze and wall
#     plate all run the full 1.0 m at their full section. That is not decoration:
#     a half bay's whole job is to fill a gap in a RUN, and a filler that drops
#     the transom reads as a hole punched in the frame rather than as wall. The
#     bands cost the same fraction of a narrow bay's face as of a wide one.
#
# G_QTR = 0.50. Two 0.080 half-posts leave 0.340 -- and at that width the only
# honest answer is the one the brief names: POSTS AND INFILL. No brace (an
# ellipse 0.410 wide is a bracket, not an arch), no intermediate stud (the two
# panels would be 0.105 wide, narrower than the stud dividing them), no lozenge
# (a 0.180 diamond in a 0.340 panel is a blocked panel). What it keeps is the
# four horizontals and one 0.340 x 1.905 panel, plus a frieze of ONE panel with
# no stud in it -- `_frieze_x(0)` is legal for exactly this. It is 32% timber in
# the verticals alone before a rail is drawn, and that is simply what a quarter
# bay is; it exists to close a 0.5 m gap in a run without stretching anything.
#
# --------------------------------------------------------------- the heights -
# HG = 3.00, and this is the piece the first complaint asks for. Nothing about
# the wall's LAYOUT is stretched -- every section, chamfer, facet and peg is the
# number it always was -- so what has to be decided is where the two upper bands
# go in the extra 0.40 m. It is not a free choice, and the window settles it the
# same way it settled Z_TRAN and Z_HEAD for the 2.60 family:
#     TZ_HEAD  = (2.820, 3.000)   the wall plate is 0.180 tall and its top IS the
#                                 storey head, exactly as Z_HEAD is at 2.60
#     TZ_TRAN  = (2.420, 2.498)   the mid rail, 0.078 tall, and its SOFFIT is
#                                 BURY under the drip mould's top over a
#                                 win_upper head at 2.400 (2.400 + DRIP_H = 2.440,
#                                 less BURY = 2.420). Round 14 measured what a
#                                 mould that stops a few mm short of a horizontal
#                                 costs -- a 4.8-8.2 mm cream hairline across the
#                                 head of every window bay -- so the mould has to
#                                 land ON a band or be buried in one, and this
#                                 band is placed to bury it.
#     TZ_ATTIC = (2.498, 2.820)   the frieze, 0.322 tall against the 2.60 bay's
#                                 0.342: the same band, not a stretched one.
#     TZ_FIELD = (0.095, 2.420)   2.325 x 1.840, a 1.26:1 portrait panel against
#                                 the 2.60 bay's 1.04:1 square one.
# THE WINDOW BAY THEREFORE CARRIES THE WHOLE SHARED FRAME, like the centred bay
# and unlike SM_Wall_TimberWin_2m, whose head at 2.400 has the transom drawn
# straight through it. In a 3.00 m storey there is room for the mid rail ABOVE
# the window, which is the one thing the 2.60 storey could never give it, and it
# is also 0.420 m of plaster between the head plate and the mould -- the window
# stops being "jammed under its head" without moving one number of spec.OPENINGS.
#
# H_BAND = 0.40 = HG - H. A PLINTH COURSE, and it goes UNDERNEATH a 2.60 wall,
# not on top of it. That is measured rather than preferred: the wall plate is
# the member that carries the floor above and it has to be AT the storey head,
# so stacking [2.60 wall][0.40 band] puts the plate 0.40 m below the head and
# the storey has no head at all, while [0.40 band][2.60 wall] puts it at
# 2.820..3.000 -- exactly where TZ_HEAD puts it on the authored tall bay. What
# the band is, then, is the dwarf wall the framing stands on: posts running down
# to the ground, ONE rail at its top in the sole plate's own section (0.305 ..
# 0.400, keyed "sole", so it is the same stick of oak), and plaster between. The
# wall above lands its own sole plate on that rail, and the pair reads as the
# 0.190 m sill beam a frame is bedded on. Its bottom face is flat at z = 0 for
# the foundation or the stone storey under it.
#
# H_KNEE = 1.30 = H / 2. A KNEE WALL, which is a wall with a head and no middle:
# sole plate and bead at the bottom, the family's FULL 0.180 wall plate at the
# top (1.120 .. 1.300, the same section as every other wall plate in the family
# so a gable's sole plate or a roof eave beds on it unchanged), and ONE field
# 1.025 x 1.840 between them. No transom -- there is nothing to divide -- and no
# frieze, because a frieze is by definition the band between a mid rail and the
# plate. The field is 1.79:1 LANDSCAPE, which is the one proportion in this
# family that suits a flat segmental arch, so the brace is the same `_brace_arc`
# fitted to it: 1.930 x 1.102, ratio 0.571. Two knee walls stack to a full
# storey with a double plate at 1.30, and one under a gable is what the user
# meant by "half height walls as we used in with the gable".
G_HALF = G / 2      # 1.00  half-width bay
G_QTR = G / 4       # 0.50  quarter-width bay
HG = S.H_GROUND     # 3.00  the stone storey's floor-to-floor
# rounded because 3.0 - 2.6 is 0.3999999999999999 in binary and this number is a
# SEAM: it is stacked against, declared to `check()` and read by an assembler
H_BAND = round(HG - H, 9)   # 0.40  what an H_UPPER wall is SHORT of an H_GROUND storey
H_KNEE = H / 2      # 1.30  half a storey

Z_PLATE_H = Z_HEAD[1] - Z_HEAD[0]       # 0.180, the wall plate's own depth
Z_TRAN_H = Z_TRAN[1] - Z_TRAN[0]        # 0.078, the mid rail's

# --- the 3.00 m storey
TZ_TRAN = (SILL_TOP + OPEN["h"] + DRIP_H - BURY,
           SILL_TOP + OPEN["h"] + DRIP_H - BURY + Z_TRAN_H)     # 2.420 .. 2.498
TZ_HEAD = (HG - Z_PLATE_H, HG)                                  # 2.820 .. 3.000
TZ_ATTIC = (TZ_TRAN[1], TZ_HEAD[0])                             # 2.498 .. 2.820
TZ_FIELD = (Z_SOLE[1], TZ_TRAN[0])                              # 0.095 .. 2.420
TZ_POST_TOP = TZ_HEAD[0] + .015
# The jamb's head dies into the transom and its own top face has to keep clear
# of the two horizontal planes either side of it -- the drip mould's top at
# 2.440 and the frieze panel's grown soffit at TZ_ATTIC[0] - .030 = 2.468. 2.454
# is the middle of that 28 mm slot: 14 mm each way, the same arithmetic
# LOW_JAMB_TOP uses at 1.980.
TZ_JAMB_TOP = TZ_TRAN[0] + .034

# --- the 1.30 m knee wall
KZ_HEAD = (H_KNEE - Z_PLATE_H, H_KNEE)                          # 1.120 .. 1.300
KZ_FIELD = (Z_SOLE[1], KZ_HEAD[0])                              # 0.095 .. 1.120
KZ_POST_TOP = KZ_HEAD[0] + .015

# --- the 0.40 m plinth band
BZ_HEAD = (H_BAND - Z_SOLE[1], H_BAND)                          # 0.305 .. 0.400
BZ_POST_TOP = BZ_HEAD[0] + .015
# The panel's own `grow` is 0.014 and it may not cross z = 0, which is a declared
# seam plane and is checked as one: at z0 = 0.016 the grown rim lands on 0.002,
# 2 mm inside the piece, and `_wob` fades to nothing that close to a seam so
# nothing can push it back out. The 2 mm strip that leaves shows the core's own
# face and reads as the bedding joint onto whatever the band stands on.
BZ_FIELD = (0.016, BZ_HEAD[0])                                  # 0.016 .. 0.305

# ===================== THE PLATE BAND, AND THE HOLE IT CLOSES  (round 20) ====
# THE DEFECT, and it is the assembler's arithmetic rather than a piece's
# geometry, so it is quoted here as the reason these two exist rather than
# rediscovered later. assemble_inn.storey() fills the gap between a timber
# storey's head and the roof datum with a band:
#       bh = band_h if proud else band_h - BAND_TUCK      # BAND_TUCK = 0.15
#       if bh > 0.95:  put(a 2.60 m wall, scale (1, 1, bh / HU))
# The hero's top storey asks band_h = 1.00 on all four sides. On the three EAVE
# faces bh is 1.00 - 0.15 = 0.85, which is NOT greater than 0.95, so the band was
# silently skipped and only the proud south face got one. MEASURED on the hero's
# west flank: above z 7.5 there are two wall pieces and both top out at z = 9.050
# against an eave at z = 9.747 -- a continuous 0.70 m OPEN SLOT along the flank,
# 27 escaping rays from inside, 56-69% see-through from a street camera. That is
# the "gaps visible in the images" reported across the layouts.
# The `> 0.95` gate exists because the only band available was a 2.60 m wall
# squashed to fit, and below about 0.95 the squash stops being survivable. Author
# the two heights and the gate can go.
#
# TWO HEIGHTS, because the two faces genuinely need different pieces:
#       0.850   EAVE face  -- band_h 1.00 less the assembler's BAND_TUCK 0.15.
#                             Tucked under the swept eave; no beam over it.
#       1.000   GABLE face -- "proud". The gable sits on it, and assemble_inn
#                             lands SM_Beam_JettySill_2m_C on top of it.
#
# WHY NOT "ONE 0.85 PIECE PLUS THE EXISTING HEAD PLATE", which is the obvious
# cheaper decomposition and is what I was asked to check. MEASURED on the built
# beam: SM_Beam_JettySill_2m_C spans y -0.481 .. +0.050 and is placed at
# band_top - SILL_H (0.48), so it occupies band-local z 0.520 .. 1.000. Its body
# is in FRONT of the wall -- the deepest thing it has behind y = -0.11 is its
# housing block. So an 0.85 m band under a 1.00 m gable line would leave
# band-local z 0.850 .. 1.000 unfilled from y = 0.050 back to y = T: a
# 0.19 x 0.15 m section running the whole length of every gable face. That is
# 28.5 dm3 per bay of exactly the same void this pass exists to close, hidden
# behind a beam that does not reach back to seal it. So: author both.
#
# WHAT EACH PIECE IS. Both are the same course -- the low attic band between a
# storey head and the roof -- and both are built like the family's FRIEZE
# (Z_ATTIC), because that is what this band is: close studs, small pillowed
# panels, and a plate over them. Neither has a SOLE PLATE, and that is the one
# decision worth spelling out: the piece is placed at z + HU, i.e. directly on
# the storey's own wall plate (Z_HEAD, 0.180 m of oak at PLATE_Y), so the plate
# BELOW is this course's sill. Giving it one of its own would put 0.275 m of
# unbroken timber at the junction and read as a double course -- which is also
# why two stacked SM_Wall_TimberBand_2m (0.40) are the wrong way to make 0.80.
# What it does get at its foot is the family's SOLE BEAD, 0.052 m of moulding at
# BEAD_Y: enough to terminate the piece on z = 0 and to tuck the panels' grown
# rim under, at a fifth of the height of a plate.
#
# WHERE THE HEAD MEMBER GOES IS DECIDED BY THE BEAM, on the gable band, and it is
# the one place the two pieces differ:
#   * the EAVE band takes the family's standard 0.180 m wall plate at its head
#     (0.670 .. 0.850), because nothing is placed over it and the eave course
#     bears on it. Field 0.052 .. 0.670.
#   * the GABLE band's head member starts at 0.579 and runs to 1.000 -- 0.421 m,
#     a BRESSUMER rather than a plate. 0.579 is not chosen, it is measured: the
#     beam's housing block (beams.SILL_TAIL, "how far the beam is HOUSED into the
#     wall") is a full-bay-width solid spanning y -0.116 .. +0.050 over the
#     beam's own z 0.059 .. 0.472, i.e. band-local 0.579 .. 0.992. Its BACK is
#     one flat 0.826 m2 quad on y = +0.050 -- and PANEL_BACK, where every
#     pillowed panel in this family puts its own flat back, is y = +0.052. TWO
#     MILLIMETRES. Running the field up past 0.579 would lay ~0.31 m2 of panel
#     back 2 mm off the beam's housing back on every gable bay of the building.
#     So the field stops where the housing starts, the head member is the thing
#     the beam is housed INTO (which is what a bressumer is, and why BRESS_Y
#     exists in the ladder above), and the panels' own back grid -- which insets
#     PANEL_BACK_IN from the field line -- tops out at 0.573, a clear 6 mm below
#     the housing.
#     The member itself sits at PLATE_Y, so it is 24 mm BEHIND the beam's front
#     face (-0.116) and 16 mm of oak stands behind the housing's back. The gable
#     above lands on the beam's top face and on this member's, both at z = 1.000.
#
# WHAT BEDS ON WHAT, for an assembler placing these at z + HU:
#       piece                          origin z = 0 is the storey head
#       SM_Wall_TimberBandEave_2m      bead 0.000..0.052 | field 0.052..0.670 |
#                                      WALL PLATE 0.670..0.850 (top face = 0.850)
#       SM_Wall_TimberBandGable_2m     bead 0.000..0.052 | field 0.052..0.579 |
#                                      BRESSUMER 0.579..1.000 (top face = 1.000)
#       both: seam half-posts from z = 0 to 15 mm inside the head member, cut
#       dead flat on z = 0 and on the top, y = 0..T, x = +-1.000.
BAND_EAVE_H = 0.850     # band_h 1.00 less assemble_inn's BAND_TUCK 0.15
BAND_GABLE_H = 1.000    # the full band: the gable sits on it
BAND_BEAD = (0.000, 0.052)      # the family's sole bead, the course's own foot
# 0.579: SM_Beam_JettySill_2m_C is placed at band_top - 0.480 and its housing
# block starts 0.059 above its own origin. Measured on the built beam, not read
# off beams.py, because SILL_TAIL is a nominal and the block carries a bevel.
BAND_SILL_HOUSE = BAND_GABLE_H - 0.480 + 0.059                  # 0.579
EZ_HEAD = (BAND_EAVE_H - Z_PLATE_H, BAND_EAVE_H)                # 0.670 .. 0.850
EZ_FIELD = (BAND_BEAD[1], EZ_HEAD[0])                           # 0.052 .. 0.670
GZ_HEAD = (BAND_SILL_HOUSE, BAND_GABLE_H)                       # 0.579 .. 1.000
GZ_FIELD = (BAND_BEAD[1], GZ_HEAD[0])                           # 0.052 .. 0.579

# ===================== THE HALF BAY'S WINDOW IS NOT win_upper ================
# ARITHMETIC, and it is not close: OPENINGS["win_upper"] is 1.500 m wide and a
# half bay is 1.000 m wide. The opening is wider than the WALL, never mind the
# 0.840 m panel field left between its two half-posts, and `_core`'s own assert
# ("opening reaches a bay edge") refuses it rather than mis-building it. There
# is no version of a 1.0 m bay that carries the kit's upper casement.
#
# So the half bay takes the only other opening in spec.py that has an insert
# built for it and fits: OPENINGS["win_attic"], 0.52 x 0.58 at sill 0.60. The
# insert is gables.py's SM_Gable_WinFrame, whose own header says it fills "a
# `win_attic` opening ... on the wall face (Y=0), so it snaps to any `win_attic`"
# and whose seams are declared as x +-0.240, z 0 .. 0.540 -- the opening less
# INSERT_CLEAR all round, i.e. the fit is proved on every build of that family.
# CHECKED IN BOTH DIRECTIONS, which is what the contract means:
#   * the insert fits the hole: 0.480 x 0.540 in 0.520 x 0.580, 20 mm all round.
#   * the hole is not wider than the insert's frame: this module cuts 0.520 x
#     0.580 exactly (`measure_opening(key="win_attic")` proves it on the built
#     mesh), so there is no bare reveal for the frame to fail to cover.
#   * DEPTH. The insert's deepest plane is its glass at y = 0.109 and its front
#     is its frame at y = 0.004. This wall's reveal backing starts at BACK_Y =
#     0.200, so there is 91 mm of air behind the glass and nothing is doubled --
#     the same split round 14 wrote for win_upper (nothing in a leaf past 0.190).
#     Our jamb face is at JAMB_Y = -0.046, 50 mm proud of the frame, so the light
#     sits inside the reveal instead of on the wall.
#   * THE CILL IS THE WALL'S, as it is for every opening in this family:
#     SM_Gable_WinFrame carries none (gables.py moved its cill, corbels and label
#     mould out to the wall in its own round 14), so there is no second cill to
#     fight the one below.
# THE ONE NUMBER AN ASSEMBLER NEEDS: the insert's origin is the bottom centre of
# the opening on the wall face, so it is placed at z = SM_SILL_TOP = 0.600.
OPEN_S = S.OPENINGS["win_attic"]        # 0.52 x 0.58, sill 0.60, flat head
SM_SILL_TOP = OPEN_S["sill"]            # 0.600 -- spec's own sill, may not move
SM_HEAD = SM_SILL_TOP + OPEN_S["h"]     # 1.180
SM_APRON_TOP = SM_SILL_TOP - SILL_H     # 0.482: top of the plaster apron
# The jamb dies into the drip mould over it, and it is put in the MIDDLE of that
# mould rather than 5 mm under its top face: at 5 mm the two planes are inside
# what `_open_fade`'s ramp can still leave between them (28% and 35% of the
# wobble survive at those two heights, so up to 7 mm of differential), which is
# how a coincident pair gets made. 20 mm each way cannot close.
SM_JAMB_TOP = SM_HEAD + DRIP_H / 2      # 1.200
# `head_x` for `_open_fade`, by the same formula DRIP_X uses: half the mould
# (opening/2 + 0.095) plus 0.029, so the WHOLE soffit is pinned and not just the
# part of it over the hole. 0.384 against a post face at 0.420, so it cannot
# reach a tiling plane -- the constraint the round-14 note sets for DRIP_X.
SM_DRIP_X = OPEN_S["w"] / 2 + .124      # 0.384
# the jamb's own centre line, by JAMB_X's formula. The pegs holding the frame in
# take it rather than being measured in from the post, for the reason round 11
# gives at JAMB_X: measured from the post they walk into the cream cheek the
# moment either the post or the lining changes section.
SM_JAMB_X = OPEN_S["w"] / 2 - JAMB_LAP + JAMB_W / 2      # 0.291

# ------------------------------------------------------------ gable sections --
# The gable triangle is only 1.28 m tall, so it is the piece where a member eats
# the most infill per millimetre of width -- and its numbers were duplicated
# between `gable` and `gable_rough`, which is how they drifted apart. Hoisted.
G_SOLE = Z_SOLE[1]  # 0.095 -- the gable's sole plate IS a wall's sole plate
G_RAKE = 0.070      # width of a raking timber (was 0.098)
G_KING = 0.058      # HALF width of the king post (was 0.076)
G_ARC_R = 0.560     # outer radius of the twin apex braces
G_ARC_W = 0.084     # ... and their width (was 0.112)
G_INFILL_Y = -0.022 # the gable's cream face. NOT PANEL_Y, and this is the one
                    # place the round-11 crown move had to be given back: the
                    # gable's infill is a flat prism rather than a pillow, so
                    # its whole face sits on ONE plane -- there is no cushion to
                    # climb back out of the trench -- and at PANEL_Y the twin
                    # apex braces (which ride at FY + 0.008 = -0.042, clear of
                    # the king post they die into) stood 8 mm proud of it and
                    # simply vanished from the demo. At -0.022 they stand 20 mm,
                    # the king post 28 and the rakes 61: the framing reads again.
                    # It is not free -- a deeper infill means the rakes overhang
                    # it, so a head-on ray near a rake hits timber instead of
                    # cream, and the piece measured 44.5% -> 52.0% timber going
                    # from PANEL_Y to -0.014. -0.022 with G_RAKE at 0.070 is the
                    # compromise: the braces still read and the triangle is back
                    # under 48%.

# ===================== THE GABLE'S RELIEF BUDGET  (round 15) =================
# ... and 20 mm is ALL the brace has, which is what this pair of constants is
# about. `_arc_c` gives every worked member two INWARD deviations on its front
# face -- the adze facets (ADZE * 0.8 = 8 mm by default) and the facet tilt
# (FACET_TILT * 0.85 = 11 mm) -- and both cut back from the member's own face
# plane, never forward, because an adze removes wood and forward would spend
# PROUD_MAX. On a wall that is free: a stud stands 50 mm proud of its panel and a
# rail 70, so 19 mm of inward carving still leaves the member clearly in front of
# the plaster. On the GABLE the same 19 mm is spent against a 20 mm step, and on
# `gable_rough` -- whose hand-floated infill sits 6 mm prouder again -- against
# 14 mm. Measured on the built mesh before this pass, head-on rays down the LEFT
# brace's own centre line: a 43.7 mm run of CREAM at the foot, and after the
# radius wander was made coherent a 60.0 mm run at the crown, the plaster
# standing at y = -0.031 against a brace face cut back to -0.030. That is the
# plaster infill breaking THROUGH the arch brace, and at a glance it reads as a
# brace snapped in two -- the other half of "twisted / broken".
# The carving is not removed, it is scaled to the piece: the facet STEP between
# neighbouring flats is what the eye reads, and at 4.5 / 3.5 mm on an 84 mm
# member that step is still above SMOOTH_ANG and still catches the sun. What goes
# is the part of the excursion that had nowhere to be. Deepest facet is now
# -0.034, i.e. 12 mm clear of the machined gable's infill and 6 mm clear of the
# hand-floated one -- both comfortably more than the 1 mm differential `_wob`
# puts between two surfaces 20 mm apart at the same (x, z).
ADZE_G = 0.0045     # adze depth on a gable arch brace
TILT_G = 0.0035     # ... and its facet tilt


# ------------------------------------------------------- paint work-around ---
# util._emit paints only the faces bmesh.ops.bevel RETURNS; a beveled
# primitive's own six faces come back unpainted, i.e. left in material slot 0
# with white vertex colour. On the first pass that silently rendered every
# timber in the family as plaster. Until util.py is fixed (see `needs`), slot 0
# is reserved for a sentinel and anything that lands there is repainted here.
SENTINEL = "iron"


def _reserve(p):
    p._mi(SENTINEL)
    return p


def _pnt(p, mat, tint=0.05, shade=1.0):
    """Repaint whatever the last primitive left in the sentinel slot."""
    lost = [f for f in p.bm.faces if f.material_index == 0]
    if lost:
        p._paint(lost, mat, tint, shade)


def _unpainted(p):
    return sum(1 for f in p.bm.faces if f.material_index == 0)


# ------------------------------------------------------------- the bay seam ---
def _cut(p, faces, x=G / 2):
    """Cut a member's overshoot dead flat onto the tiling plane.

    THE seam fix. util._emit bevels every edge of a primitive, the two END edges
    included, so a rail that stopped exactly on x = +-G/2 handed the seam an
    18 mm chamfer and its neighbour handed it another: a 36 mm V-groove running
    the full height of the wall every 2.0 m, which is what "seam lines across
    wall connections" looks like. Building the member SEAM_CUT wider and pushing
    the overshoot back onto the plane collapses that chamfer flat, so the front
    face crosses the join at full width and the timber is continuous in shading
    as well as in outline. Same mechanism Part.finish() uses on a stone at a bay
    boundary -- done here so the piece's own clamp report stays clean.
    """
    for f in faces:
        for v in f.verts:
            if v.co.x > x:
                v.co.x = x
            elif v.co.x < -x:
                v.co.x = -x


def _tidy(p, tol=2e-7):
    """Drop the zero-area faces left where a seam chamfer collapsed onto the
    tiling plane. They cost nothing to look at but they carry no usable normal,
    and a few hundred of them per piece would pollute the smooth shading along
    exactly the line we are trying to make invisible."""
    dead = [f for f in p.bm.faces if f.calc_area() < tol]
    if dead:
        bmesh.ops.delete(p.bm, geom=dead, context='FACES')
    return len(dead)


def _done(p):
    """Every piece ends here: pull the inner face back onto y = T, sweep the
    collapsed seam chamfers, then bake."""
    _flatten_inner(p)
    _tidy(p)
    return p.finish()


# Fixed, arbitrary. Any non-zero constant will do -- zero means "seed from the
# clock", which is the behaviour we are here to stop.
NOISE_SEED = 20240823


def _wob(p, *passes, margin=0.28):
    """Hand-hewn wobble, made REPRODUCIBLE, and faded further from the seam.

    `util.Part.wobble` displaces every vertex by mathutils.noise.noise_vector,
    and Blender seeds that noise basis PER PROCESS. Probed with one fixed input
    vector, three separate Blender runs returned (-0.463, -0.329, -0.331),
    (0.125, 0.066, 0.097) and (0.125, 0.066, 0.097): not stable. So "same code,
    same mesh" was false for every family in the kit that wobbles. Measured on
    these seven pieces, two builds of identical code differed by up to 15.6 mm --
    which is the wobble amplitude itself -- and with wobble stubbed out the same
    seven came back bit-identical across processes, so the bevel and everything
    else in this module was already deterministic and the noise seed was the
    whole of it. noise.seed_set() pins it: seeded, the same probe returns
    (-0.107, -0.200, 0.376) in every process.

    The real fix belongs in util.Part.wobble, which this module may not edit;
    calling seed_set here costs nothing and is a no-op for anyone who does not
    wobble. It is also what makes a measured critique of this family repeatable.

    ROUND 19 -- THAT FIX HAS SINCE LANDED IN util.py AND THIS CALL IS NOW DEAD,
    which is worth saying rather than leaving a claim standing that the code no
    longer earns. `Part.wobble` seeds the basis itself, from an md5 of the piece
    name, on the line before its own vertex loop -- so the seed_set below is
    overwritten before a single vertex moves and NOISE_SEED has no effect on any
    mesh in this family. Determinism is unaffected and still measured (25/25
    pieces bit-identical across two separate Blender processes); the line is left
    in place only because removing it would be a no-op edit to a function every
    piece calls. Do not derive anything from NOISE_SEED.

    `margin` defaults to 0.28 rather than util's 0.16: at 0.16 the seam fade
    still allowed 7.5 mm of noise 100 mm from a tiling plane, so two adjacent
    half-posts diverged immediately either side of a join that was itself dead
    flat. 0.28 flattens the post-and-plate zone -- which has to be flat for the
    kit to snap anyway -- and leaves the panel field, a metre away, untouched.
    """
    noise.seed_set(NOISE_SEED)
    for amount, freq in passes:
        p.wobble(amount, freq=freq, margin=margin)


def _snap(p):
    """Vertex positions, for `_open_fade` to fade back toward."""
    return [v.co.copy() for v in p.bm.verts]


def _open_fade(p, hx0, hx1, hz0, hz1, snap, margin=0.10, head_x=None):
    """FADE THE HAND-HEWN WOBBLE TO ZERO AT A WINDOW REVEAL.

    `util.Part.wobble` already fades to zero at a TILING plane, for the reason
    that two bays cannot crack apart at the join. An opening is the same kind of
    plane and was not being treated as one: `_wob` displaces every vertex by up
    to 15 mm, so the four surfaces that define the hole -- the two jamb reveal
    faces, the core's head and the sill line -- wandered, and they wandered
    INWARD as often as out. Measured on the built mesh before this pass:

        SM_Wall_TimberWin_2m        1.4855 x 1.4191, sill 0.9809
        SM_Wall_TimberJetty_2m_B    1.4884 x 1.4187, sill 0.9811
        SM_Wall_TimberWin_2m_Rough  1.4828 x 1.4192, sill 0.9808
        SM_Wall_TimberJetty_2m_B_R  1.4828 x 1.4166, sill 0.9834
        spec.OPENINGS["win_upper"]  1.5000 x 1.4500, sill 0.9500

    i.e. every hole in the family was 12-17 mm narrow and 31-33 mm short, and the
    sill it presented was 31-33 mm above the one spec says an insert beds on. An
    insert built to spec is INSERT_CLEAR (20 mm) smaller all round, so a 33 mm
    error eats the whole clearance and then some: the casement lands ON the wall
    instead of IN it. That is half of "doesn't seem to fit", and it is this
    module's half.

    THE FIX IS A FADE, NOT A CLAMP, and the difference matters. Snapping strays
    onto the aperture plane makes flat patches, and a flat patch on one member
    that shares a plane with a flat patch on another is a z-fight -- this family
    measured zero of those and is not giving that up to fix a fit. So every
    vertex is blended back toward its PRE-WOBBLE position by a weight that is 0
    on the aperture boundary and 1 at `margin` away from it, in exactly the shape
    util uses at a seam. On the boundary the geometry is nominal, to the
    micrometre; 100 mm away it is as hand-hewn as it ever was; in between it
    ramps smoothly, so no new plane, crease or coincident face is created.

    Distance is measured in the vertex's ORIGINAL (x, z), so the weight field is
    a fixed function of the wall rather than of the noise, and it therefore
    treats a rough bay and a regular bay identically -- which is what lets both
    take the same casement. It is applied through the FULL depth of the wall, not
    just the reveal, because the core's own hole faces sit at y = 0.074, inside
    the depth spec.REVEAL says an insert occupies.

    ROUND 14 -- `head_x` PINS THE WHOLE SOFFIT, not only the part of it over the
    hole, and it exists because the drip mould's soffit is now the head of the
    opening. That soffit is one flat plane 1.69 m long, i.e. 190 mm WIDER than
    the aperture, and the fade above leaves the last 95 mm of it at each end (the
    ears, which are outside the hole in x) free to wobble by up to 6 mm. A quad
    interpolates between its corners, so a wobbling ear drags the soffit down
    INSIDE the aperture as well: measured 2.3986 against spec's 2.4000, i.e.
    1.4 mm of the casement's 20 mm clearance eaten by geometry that is not even
    over the hole. Any vertex whose PRE-WOBBLE z is the head and whose x is under
    the mould's own half-length is therefore held exactly, which costs nothing --
    a soffit is flat by definition, and this one is 8 mm clear of the core band's
    soffit above it, so pinning it cannot make a coincident plane.
    """
    for v, o in zip(p.bm.verts, snap):
        if head_x is not None and abs(o.z - hz1) < 1e-4 and abs(o.x) <= head_x:
            v.co = o.copy()
            continue
        dx = max(hx0 - o.x, o.x - hx1, 0.0)
        dz = max(hz0 - o.z, o.z - hz1, 0.0)
        if dx > 0.0 or dz > 0.0:
            d = (dx * dx + dz * dz) ** 0.5           # outside the aperture
        else:                                        # inside it
            d = min(o.x - hx0, hx1 - o.x, o.z - hz0, hz1 - o.z)
        if d >= margin:
            continue
        w = smoothstep(0.0, margin, d)
        v.co = o + (v.co - o) * w


class _pin:
    """Pin the Part's paint rng while a shared band is emitted.

    `_paint` draws its per-primitive vertex-colour jitter from the Part's own
    stream, in emission order, so the SAME sole plate came out up to 5% brighter
    in one variant than in the next. Material and shade are only two thirds of a
    tone; this is the third.
    """

    def __init__(self, p, key):
        self.p, self.key = p, key

    def __enter__(self):
        self.saved = self.p._rng
        self.p._rng = rng("timber/tone/" + self.key)
        return self.p

    def __exit__(self, *a):
        self.p._rng = self.saved
        return False


# ---------------------------------------------------------------- helpers ----
def _oak(r, pale=0.18):
    """Timber tone. KIT-WIDE TABLE: structural timber is `oak_dark`, secondary
    boards are `oak_mid`, `oak_pale` is a sparing highlight. `pale` is the
    chance of coming back lighter -- keep it low (0.10-0.22) on anything
    structural, high (0.7-0.9) on boarding and proud trim."""
    q = r.random()
    if q < pale * 0.09:
        return "oak_pale"
    return "oak_mid" if q < pale else "oak_dark"


def _sh(r, a=.10):
    return 1.0 + r.uniform(-a, a)


# =============================================================================
# ===================== THE WORKED TIMBER -- carving, as FORM ==================
# =============================================================================
# Round 9, Shanee, of the whole kit: "the wood overall still needs a texture or
# detail." It cannot be a texture: the .blend is inspected in SOLID viewport
# shading, where one material draws ONE FLAT COLOUR per face and an image
# texture or a vertex-colour tint is simply not there. So the answer has to be
# geometry that casts its own light and shade -- which is the better answer for
# a game asset anyway, because it survives every shading mode and it still reads
# at distance where a texture has resolved to mud.
#
# Until now every frame member in this family was `Part.box` with a uniform
# 18 mm bevel on all twelve edges. That is the shape of a soap bar: two long
# arrises rounded by the same amount as the eight corners, no facet anywhere
# wider than the bevel, and -- because bevel rounding is smooth-shaded at
# SMOOTH_ANG -- no hard line for the light to break on. `_worked` replaces it
# with a SWEPT SOLID whose cross-section changes along the member's length, for
# about the tri count the bevel was already spending, and that buys the four
# details a hand-cut frame actually has:
#
#   STOP-CHAMFER   A wide (CHAM = 26 mm) chamfer down the exposed arrises which
#                  STOPS CHAM_STOP short of each end, getting there over a
#                  CHAM_RET carved return. It is the single most characteristic
#                  joinery detail there is: a carpenter chamfers the length of a
#                  timber and squares the arris back up where the joint is, so
#                  the mortice has full wood and the stop itself becomes the
#                  ornament. A bmesh bevel CANNOT do it -- it rounds every arris
#                  equally, the two end faces included, which is also what used
#                  to hand the bay seam a V-groove (see `_cut`).
#   ADZE FACETS    The front face steps INWARD between hard creases, so a
#                  member's face is two or three shallow flats instead of one
#                  plane -- hand-hewn, not sawn. The crease is FACET_W (10 mm)
#                  wide against a ~9 mm step, i.e. ~40 deg, which clears
#                  SMOOTH_ANG (34) and therefore survives as a hard arris rather
#                  than being shade-smoothed into nothing. Inward only, for two
#                  reasons: an adze takes wood OFF, and outward would eat into
#                  what is left of PROUD_MAX.
#   ARRIS WEAR     The chamfer width is jittered per station AND per arris, so
#                  one timber's two long edges are neither the same width as each
#                  other nor constant along their own length. That is what
#                  "soften the long edges unevenly rather than a uniform bevel"
#                  means, and it is free -- it is a multiplier on a number the
#                  sweep was going to use anyway.
#   BOW / TAPER    Arrises displaced sin^2 along the length (`bow`), the whole
#                  section displaced out of plane the same way (`belly`), and a
#                  linear shrink toward one end (`narrow`). Nothing in a frame is
#                  straight; util.Part.bow() does this to a WHOLE part, which a
#                  wall piece cannot afford (its seam faces have to stay flat),
#                  so the curve belongs to the individual member instead.
#
# THE BAY SEAM IS SAFER THAN IT WAS, NOT RISKIER -- and that is worth stating
# plainly, because the fourth pass measured the seam down to background level and
# this pass rebuilds every member that crosses it. Every deviation above is zero
# AT THE TWO END STATIONS BY CONSTRUCTION:
#   * the chamfer dies before the end (`ends`=0 -- that is what a stop-chamfer
#     IS), so a seam-crossing member now arrives at x = +-G/2 as a dead square
#     rectangle of exactly its nominal section. That is a BETTER joint than
#     `_cut` gave, because there is no chamfer to collapse in the first place;
#   * the facet regions at both ends carry zero inset, so the face plane at the
#     seam is the nominal one to the micron;
#   * `bow` and `belly` are sin^2 -- zero displacement AND zero slope at both
#     ends, the same reason beams.py uses sin^2 on its run pieces -- so two bays
#     leave the join along one tangent;
#   * `narrow` (which is NOT symmetric) is left at 0 on anything that crosses a
#     seam, and `_shared`/`_posts` never pass it.
# Two bays therefore show a pair of chamfer stops either side of the post they
# share, which is exactly where a carpenter would stop them, and it is symmetric
# so it survives the X-mirroring assemble_inn.py does.
CHAM      = 0.026   # stop-chamfer width on an exposed structural arris
CHAM_BEAD = 0.010   # ... and on a small bead or moulding, which is only 50 mm
CHAM_STOP = 0.105   # how far short of its end a chamfer stops
CHAM_RET  = 0.068   # length of the carved return that gets it there. Was
                    # 0.030: at that length the stop was a 30 mm kink in one
                    # arris, geometrically present and, at any distance a wall
                    # is actually looked at, indistinguishable from a rounded
                    # corner. beams.oct_shaft's square stop uses a 90 mm return
                    # and is the most legible piece of carpentry in either
                    # family in Solid shading -- because a long return turns the
                    # chamfer face right through the light instead of nicking
                    # it. Still well inside CHAM_STOP, so the arris is square
                    # where the mortice is.
CHAM_SWELL = 0.30   # ... and the LAMB'S TONGUE: the chamfer swells this much
                    # wider than nominal just inboard of its return before
                    # dying. It is what a joiner's chisel actually leaves at a
                    # stop, it is the standard ornament of the detail, and it
                    # costs nothing -- it scales a number the sweep already
                    # uses. Zero at the end stations, like everything else here,
                    # so a seam-crossing member is unaffected.
ADZE      = 0.010   # how far an adze facet cuts INTO the face
FACET_W   = 0.010   # width of the crease between two facets. 9 mm of step over
                    # 10 mm is 42 deg: above SMOOTH_ANG, so it stays an arris.
FACET_TILT = 0.013  # ... and how much each facet's PLANE tilts across the
                    # member, alternating facet to facet.
                    #
                    # ROUND 9b, and this is the thing that stopped the adze
                    # facets being visible in the shading mode they exist for.
                    # The facets stepped inward in PARALLEL: each one was a
                    # plane offset from the nominal face by `lvl[reg]*ADZE`,
                    # normal unchanged. So two neighbouring facets shaded
                    # IDENTICALLY, the hard 42-degree crease between them
                    # divided two equal values, and all it cost the eye was one
                    # 10 mm sliver -- sub-pixel at any real viewing distance.
                    # A sharp edge is only visible if the faces it separates
                    # shade differently. Tilting alternate facets the other way
                    # makes consecutive facets differ by 2*atan(TILT/span):
                    # 8 deg on a 0.185 rail, 5 deg on a 0.29 post. Measured in
                    # Workbench/Solid at 2 m, that is the difference between a
                    # timber that reads as three axe flats and one that reads as
                    # a smooth board. Inward only (an adze removes wood, and
                    # outward would spend PROUD_MAX), zero at both end stations
                    # (env), so a seam-crossing member is untouched at the
                    # tiling plane. Costs ZERO tris: it moves vertices `_sweep`
                    # was going to emit anyway. beams.FACET_TILT is the same
                    # detail on the exposed beams, at the same scale.


def _c_stations(L, stop, ret, facets, seed, mids=2):
    """Station parameters along a worked member, and where its facets break.

    Both ends exactly, the two chamfer stops and their returns, `mids` interior
    stations to carry the bow, and a PAIR of stations FACET_W apart at every adze
    facet break -- the pair is what makes the step between two facets a hard
    crease instead of a slow ramp that shade-smooths away."""
    L = max(L, 1e-6)
    s = clamp(stop / L, 0.0, 0.30)
    rr = clamp(ret / L, 1e-4, max(1e-4, 0.34 - s))
    ts = [0.0, s, s + rr, 1 - s - rr, 1 - s, 1.0]
    for i in range(mids):
        ts.append(lerp(s + rr, 1 - s - rr, (i + 1) / (mids + 1)))
    r = rng(f"timber/worked/{seed}")
    lo, hi = s + rr + .05, 1 - s - rr - .05
    brk = []
    if facets >= 2 and hi > lo:
        for i in range(facets):
            brk.append(clamp(lerp(lo, hi, (i + .5 + r.uniform(-.22, .22))
                                  / facets), lo, hi))
    hw = FACET_W / L * .5
    for b in brk:
        ts += [b - hw, b + hw]
    ts = sorted(clamp(t) for t in ts)
    keep = [ts[0]]
    for t in ts[1:]:
        if t - keep[-1] > .005:
            keep.append(t)
    keep[-1] = 1.0
    return keep, sorted(brk)


def _hexsec(u0, u1, vf, vb, clo, chi, f):
    """ONE worked cross-section: a rectangle u0..u1 x vf..vb with the two FRONT
    arrises cut back by clo/chi. `f(u, v)` maps it into the world, which is what
    lets the same section be lofted down a straight member or round a curved
    brace. Six points, so a member costs 6 quads per station gap.

    Only the two FRONT arrises are chamfered: the back two are buried in the
    plaster core on every member in this family, and carving what is buried is
    the one thing this tri budget genuinely cannot afford.

    `vf` may be ONE number (a face parallel to the wall) or a PAIR
    (v_at_u0, v_at_u1) -- a face TILTED across the member, which is what makes
    an adze facet visible rather than merely present. See FACET_TILT."""
    span = max(u1 - u0, 1e-5)
    try:
        vlo, vhi = vf
    except TypeError:
        vlo = vhi = vf
    dep = max(vb - max(vlo, vhi), 1e-5)
    a = min(clo, span * .42, dep * .85)
    b = min(chi, span * .42, dep * .85)
    g = (vhi - vlo) / span
    return [f(u0 + a, vlo + g * a), f(u1 - b, vhi - g * b), f(u1, vhi + b),
            f(u1, vb), f(u0, vb), f(u0, vlo + a)]


def _loft(p, rings, mat, tint=.06, shade=1.0):
    """Close a run of equal-length sections into one solid, caps included."""
    n, m = len(rings[0]), len(rings)
    vs = [v for ring in rings for v in ring]
    F = []
    for i in range(m - 1):
        for j in range(n):
            k = (j + 1) % n
            F.append((i * n + j, i * n + k, (i + 1) * n + k, (i + 1) * n + j))
    F.append(tuple(range(n)))
    F.append(tuple(range((m - 1) * n, m * n)))
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _sweep(p, along, t0, t1, st, mat, tint=.06, shade=1.0):
    """Loft a worked section along one axis. `st` is a list of stations
    (t, u_lo, u_hi, v_front, v_back, c_lo, c_hi), so a chamfer that grows,
    waists, wears and dies is one list of numbers rather than a modifier.

    along='x' -> u is z and the member runs along X (a rail);
    along='z' -> u is x and it runs along Z (a post). v is y either way, i.e.
    the front face is always the one the street sees."""
    rings = []
    for (t, ulo, uhi, vf, vb, clo, chi) in st:
        tt = lerp(t0, t1, t)
        f = ((lambda u, v: (tt, v, u)) if along == 'x'
             else (lambda u, v: (u, v, tt)))
        rings.append(_hexsec(ulo, uhi, vf, vb, clo, chi, f))
    return _loft(p, rings, mat, tint=tint, shade=shade)


def _arc_c(p, cx, cz, ax, az, w, a0, a1, mat, n=12, y=FY, d=FD, cham=CHAM,
           stop=.14, ret=.045, ends=0.0, adze=ADZE * .8, wear=.30, swell=0.0,
           jit=0.0, bow=0.0, tilt=FACET_TILT * .85, tint=.06, shade=1.0,
           seed=0):
    """A CURVED BRACE, WORKED -- the same stop-chamfer and adze facets as a
    straight member, lofted round a quarter ellipse instead of along an axis.

    This is the one member in the family the eye lands on first (it is the only
    curve in a wall of straight lines), and it was the last one still built as a
    prism with a uniform 14 mm bevel on every edge, i.e. the soap-bar treatment
    this pass exists to end. Now the chamfer runs the length of the curve and
    dies at both ends -- which is not decoration but the truth of the joint: the
    brace's two ends are buried in a post and a rail, and a chamfer stops where
    the wood has to be full for a mortice.

    (cx, cz) is the ellipse centre, ax/az its semi-axes to the member's OUTER
    edge, w its width. `swell` fattens it at the haunch, `jit` wanders the
    radius, `bow` pushes it out of the wall plane at mid span -- the three things
    the hand-cut sibling wants, so the rough half of the family can use this too
    instead of prism + Part.bow() + merge()."""
    A0, A1 = radians(a0), radians(a1)
    L = abs(A1 - A0) * (ax + az) * .5              # arc length, near enough
    ts, brk = _c_stations(L, stop, ret, 0, f"{p.name}/arc/{seed}", mids=max(1, n - 5))
    r = rng(f"timber/arc/{p.name}/{seed}")
    s = clamp(stop / max(L, 1e-6), 0.0, .30)
    rr = clamp(ret / max(L, 1e-6), 1e-4, max(1e-4, .34 - s))
    ph, wv = r.uniform(0, 2 * pi), r.uniform(1.6, 3.0)
    # the facet tilt (see FACET_TILT), but UNDULATING rather than stepped: a
    # curved brace has no straight stations to break a facet on, and a hewn
    # brace really does wind along its length. Which edge is cut deeper swaps
    # over smoothly, so the brace's face turns through the light instead of
    # being one swept plane -- which is all it was, and it is the member the eye
    # lands on first.
    ph2, wv2 = r.uniform(0, 2 * pi), r.uniform(1.7, 2.9)
    # ===================== THE WANDER IS COHERENT, NOT WHITE NOISE ===========
    # ROUND 15. `jit` used to be drawn INDEPENDENTLY AT EVERY STATION
    # (jx = jit * r.uniform(-1, 1)) and it displaced the WHOLE cross-section
    # radially -- outer arris, inner arris and axis together. That is not
    # roughness on a timber, it is noise on the member's own centre line, and on
    # a curve it is the worst place to put it: `_c_stations` puts its two
    # tightest stations 0.051 of the arc apart (45 mm on the gable's braces), so
    # two neighbours could differ by the full 2*jit = 20 mm and the axis kinked
    # by atan(20/45) = 24 degrees at a single station. Measured on the built
    # mesh, worst member of each piece, against the smooth sibling built by the
    # same function with jit = 0:
    #
    #     piece                          axis dev   axis kink   edge kink
    #     SM_Wall_TimberGable_2m            0.00       0.00        0.00
    #     SM_Wall_TimberGable_2m_Rough     23.09      33.67       36.81
    #     SM_Wall_Timber_2m_A_Rough        10.67      12.59       13.00
    #     SM_Wall_TimberJetty_2m_A_Rough   23.00      14.62       15.18
    #
    # A vertical stud can carry that and read as hand-hewn, because a stud is
    # 2.4 m of nearly straight line and a 20 mm step in it is a nick. An arch
    # brace cannot: it is the only curve in the piece, the eye follows its arris
    # as a line, and a 24-degree kink in that line reads as a member that is
    # broken or twisted off its own axis -- which is exactly what was reported
    # of SM_Wall_TimberGable_2m_Rough.
    # THE ROUGHNESS IS NOT REMOVED, IT IS MOVED. The radius still wanders by the
    # same +-jit; it now does it as a SMOOTH two-harmonic function of the arc
    # parameter (the shape `_hewn` already uses for `wave`) inside a sin(pi t)
    # envelope, so:
    #   * the wander's SLOPE is bounded -- jit*pi*(1 + .62*jw1 + .38*jw2) per
    #     unit t, i.e. about 5 mm across the tightest station gap instead of
    #     20 mm, so the arris undulates instead of zig-zagging;
    #   * it is exactly ZERO at both ends, so the foot lands in the plate and
    #     the head in the post at their nominal radii -- the joints got tighter,
    #     not looser;
    #   * the per-station draw is KEPT and spent on the member's WIDTH instead,
    #     where an independent step moves only the concave inner arris by ~2 mm
    #     and the member is still not two copies of one machined arc.
    # Keeping the draw is not cosmetic: `wear` takes two draws per station from
    # the same stream, so removing it would have re-rolled every chamfer width
    # on the six braces built with jit = 0 and changed pieces this pass has no
    # business touching. `rj` is a separate stream for the same reason.
    rj = rng(f"timber/arcwave/{p.name}/{seed}")
    jw1, jp1 = rj.uniform(1.0, 1.8), rj.uniform(0, 2 * pi)
    jw2, jp2 = rj.uniform(2.2, 3.0), rj.uniform(0, 2 * pi)
    wj = min(jit * 2.2, .05)            # 0 when jit is 0 -> smooth braces are
    rings = []                          # bit-identical to before this pass
    for t in ts:
        aa = lerp(A0, A1, t)
        k = lerp(ends, 1.0, clamp(min((t - s) / rr, ((1 - s) - t) / rr)))
        env = smoothstep(0, .10, t) * smoothstep(0, .10, 1 - t)
        sw = 1.0 + swell * sin(pi * t)
        q = r.uniform(-1, 1)
        jx = jit * sin(pi * t) * (.62 * sin(jw1 * pi * t + jp1)
                                  + .38 * sin(jw2 * pi * t + jp2))
        xo, zo = cx + (ax + jx) * cos(aa), cz + (az + jx) * sin(aa)
        wi = w * sw * (1.0 + wj * q)
        xi, zi = (cx + (ax + jx - wi) * cos(aa), cz + (az + jx - wi) * sin(aa))
        dx, dz = xo - xi, zo - zi
        W = sqrt(dx * dx + dz * dz) or 1e-5
        ux, uz = dx / W, dz / W
        dv = -bow * sin(pi * t)
        vf = y + dv + adze * env * (.5 + .5 * sin(wv * pi * t + ph))
        s2 = sin(wv2 * pi * t + ph2)
        tl = tilt * env * abs(s2)
        vfp = (vf + (tl if s2 < 0 else 0.0), vf + (tl if s2 > 0 else 0.0))
        f = lambda u, v: (xi + ux * u, v, zi + uz * u)
        rings.append(_hexsec(0.0, W, vfp, y + d + dv,
                             cham * k * (1 + wear * r.uniform(-1, .5)),
                             cham * k * (1 + wear * r.uniform(-1, .5)), f))
    fs = _loft(p, rings, mat, tint=tint, shade=shade)
    _pnt(p, mat, tint, shade)
    return fs


def _worked(p, x0, x1, z0, z1, mat, y=FY, d=FD, along=None, cham=CHAM,
            arris=(1.0, 1.0), stop=CHAM_STOP, ret=CHAM_RET, ends=0.0,
            facets=2, adze=ADZE, tilt=FACET_TILT, swell=CHAM_SWELL,
            bow=(0.0, 0.0), belly=0.0,
            narrow=0.0, wear=.34, mids=2, tint=.06, shade=1.0, seed=0):
    """ONE WORKED TIMBER -- see THE WORKED TIMBER above for what it is for.

    Same rectangle-in-(x, z) language as `_mem`, so a member is converted by
    adding arguments and nothing about the frame's layout moves.

    arris   (lo, hi) multipliers on the chamfer for the member's two front
            arrises. (1, 0) chamfers ONLY the low side -- which is what a seam
            half-post needs, because its high side IS the tiling plane and the
            two halves either side of it add up to one W_POST post whose middle
            must stay square. Chamfering it would cut a 52 mm V down the centre
            of the post the fourth pass worked so hard to make invisible.
    ends    chamfer width at the two end stations, as a fraction of `cham`. 0 on
            anything that crosses a seam or dies into another member; a small
            number is a worn arris on a free end.
    bow     (lo, hi) sin^2 displacement of the two arrises: (0, .004) dips a
            plate's soffit without moving its top, which matters when the top IS
            a snap plane (the wall plate's is z = H).
    belly   sin^2 displacement of the whole section along v (outward, -y), i.e.
            a post that bellies out of plane at mid height.
    narrow  linear shrink of the section toward t=1 -- a stick cut from a tree.
            Not symmetric, so never on a seam-crossing member.
    """
    if along is None:
        along = 'x' if (x1 - x0) >= (z1 - z0) else 'z'
    if along == 'x':
        t0, t1, u0, u1 = x0, x1, z0, z1
    else:
        t0, t1, u0, u1 = z0, z1, x0, x1
    L, span = t1 - t0, u1 - u0
    if L <= 1e-6 or span <= 1e-6:
        return []
    ts, brk = _c_stations(L, stop, ret, facets, f"{p.name}/{seed}/{L:.3f}",
                          mids=mids)
    r = rng(f"timber/arris/{p.name}/{seed}/{L:.3f}")
    s = clamp(stop / L, 0.0, .30)
    rr = clamp(ret / L, 1e-4, max(1e-4, .34 - s))
    # per-region adze levels. The two END regions are ALWAYS 0, so a
    # seam-crossing member presents its nominal face plane at the butt plane;
    # the interior ones alternate hard, because it is the STEP between two
    # neighbouring facets that has to clear SMOOTH_ANG, not their depth.
    nreg = len(brk) + 1
    lvl = [0.0] * nreg
    for i in range(1, nreg - 1):
        lvl[i] = (1.0 if i % 2 else .28) * r.uniform(.86, 1.0)
    # ALTERNATING FACET TILT -- see FACET_TILT. Which SIDE a facet is cut deeper
    # on flips region to region, so the crease between two facets divides two
    # differently-shaded planes instead of two identical ones.
    flip = r.random() < .5
    tl = [tilt * r.uniform(.80, 1.0) for _ in range(nreg)]
    # ... but NEVER on a side that lies on a tiling plane. The section a
    # neighbouring bay (or the storey below) meets has to be identical, and the
    # tilt is across the member's WIDTH, which `env` -- a function of position
    # ALONG it -- cannot fade. A seam half-post's high side is x = +G/2 and a
    # sole plate's low side is z = 0; tilting either would put a step in the
    # face at exactly the joint the fourth pass measured down to background
    # level. `arris` already marks those sides (it is why a half-post passes
    # (1, 0)), and the coordinate test catches the rest.
    # ROUND 19: read off the PART, not the module, so a 1.0 m bay flattens the
    # tilt at x = +-0.500 and a 3.00 m storey at z = 3.000. `_bw`/`_bh` return
    # G and H for every piece authored before fractional bays existed.
    sp = (-_bw(p) / 2, _bw(p) / 2) if along == 'z' else (0.0, _bh(p))
    tm = [0.0 if (abs(u0 - sp[0]) < 1e-6 or arris[0] <= 0) else 1.0,
          0.0 if (abs(u1 - sp[1]) < 1e-6 or arris[1] <= 0) else 1.0]
    ph, wv = r.uniform(0, 2 * pi), r.uniform(1.4, 2.6)
    st = []
    for t in ts:
        dd = min(t, 1 - t)
        k = clamp(min((t - s) / rr, ((1 - s) - t) / rr))
        k = lerp(ends, 1.0, k)
        # the lamb's tongue: a swell in the chamfer just inboard of its return
        k *= 1.0 + swell * max(0.0, 1.0 - abs(dd - (s + rr * 1.30)) / (rr * 1.15))
        env = smoothstep(0, .09, t) * smoothstep(0, .09, 1 - t)
        w2 = sin(pi * t) ** 2
        reg = sum(1 for b in brk if t > b)
        # inward only: an adze cuts wood away, and outward spends PROUD_MAX
        dvf = adze * env * (lvl[reg] + .26 * (.5 + .5 * sin(wv * pi * t + ph)))
        dv = -belly * w2
        nl = narrow * t
        hi = ((reg % 2 == 0) != flip)      # which side this facet is cut deeper
        tt = tl[reg] * env
        vf = (y + dv + dvf + (0.0 if hi else tt * tm[0]),
              y + dv + dvf + (tt * tm[1] if hi else 0.0))
        st.append((t,
                   u0 + bow[0] * -w2 + nl * .5,
                   u1 + bow[1] * -w2 - nl * .5,
                   vf, y + d + dv,
                   cham * arris[0] * k * (1 + wear * r.uniform(-1, .6)),
                   cham * arris[1] * k * (1 + wear * r.uniform(-1, .6))))
    fs = _sweep(p, along, t0, t1, st, mat, tint=tint, shade=shade)
    _pnt(p, mat, tint, shade)
    return fs


def _mem(p, x0, x1, z0, z1, mat, y=FY, d=FD, seg=1, tint=.06, shade=1.0,
         bev=None, taper=1.0, skew=(0, 0), cham=None, **kw):
    """One axis-aligned frame timber, from its rectangle in (x, z). `taper` and
    `skew` give a hand-hewn lean -- worth using on free-standing studs, never on
    the edge half-posts (their outer face IS the tiling seam).

    A member whose rectangle REACHES a tiling plane is grown SEAM_CUT past it and
    cut flat again by `_cut`, which is what kills the bevel groove at the bay
    join. Nothing else about the call changes, so every existing
    `_mem(p, -G/2, G/2, ...)` gets the fix for free.

    PASS `cham` AND THE TIMBER IS WORKED instead of extruded: `_worked` builds it
    as a swept solid with a stop-chamfer, adze facets, an uneven arris and a bow
    (see THE WORKED TIMBER, below). Everything else about the call is unchanged,
    so a member is converted by adding one argument. A converted member needs no
    SEAM_CUT: its chamfer already dies before the tiling plane, so there is no
    chamfer there to collapse.
    """
    if cham is not None:
        if taper != 1.0 and 'narrow' not in kw:
            span = (z1 - z0) if (x1 - x0) >= (z1 - z0) else (x1 - x0)
            kw['narrow'] = (1.0 - taper) * span
        return _worked(p, x0, x1, z0, z1, mat, y=y, d=d, cham=cham, tint=tint,
                       shade=shade, **kw)
    xs = _bw(p) / 2                     # THIS piece's tiling plane, not G/2
    e0 = SEAM_CUT if x0 <= -xs + 1e-6 else 0.0
    e1 = SEAM_CUT if x1 >= xs - 1e-6 else 0.0
    x0, x1 = x0 - e0, x1 + e1
    fs = p.box(((x0 + x1) / 2, y + d / 2, (z0 + z1) / 2),
               (x1 - x0, d, z1 - z0), mat,
               bevel=S.BEVEL_W if bev is None else bev, seg=seg,
               tint=tint, shade=shade, taper=taper, skew=skew)
    if e0 or e1:
        _cut(p, fs, x=xs)
    _pnt(p, mat, tint, shade)
    return fs


def _band(key, pale=0.12, mat=None):
    """Material + shade for a member that CROSSES a bay seam, keyed to the
    member's NAME instead of drawn from the variant's rng stream.

    Pass `mat` for anything STRUCTURAL. The kit-wide material table puts posts,
    plates, sill beams and bressumers on `oak_dark` without exception, and a
    keyed draw is a single roll of the dice for the WHOLE family: at pale=0.10
    there is a one-in-ten chance that every seam post in the kit comes out
    oak_mid, and it would look deliberate rather than broken. The current keys
    all happen to roll oak_dark; saying so out loud costs nothing and stops the
    next person who edits a key string from silently changing the kit's timber.
    `pale` still governs the beads and mouldings, which are proud trim and are
    allowed to be oak_mid.

    A sole plate is one continuous timber running the length of a facade, and it
    was picking its timber and its tone per variant, so a run showed a colour
    step at every join even where the geometry met perfectly. The half-posts were
    worse: the two halves that add up to ONE seam post were two independent
    draws, so half a post could be a different timber from its other half -- and
    under the X-mirroring assemble_inn.py now does, the two halves that meet are
    not even the same pair of draws. Keyed tone is what makes a mirrored bay form
    one post with an unmirrored neighbour.
    """
    r = rng("timber/band/" + key)
    return (mat or _oak(r, pale)), _sh(r, .05)


def _shared(p, key, x0, x1, z0, z1, pale=.12, mat=None, **kw):
    """A seam-crossing band: keyed timber, keyed shade, keyed jitter, flat cut."""
    m, sh = _band(key, pale, mat)
    with _pin(p, key):
        return _mem(p, x0, x1, z0, z1, m, shade=sh, **kw)


def _brace(p, a, b, mat, w=W_BRACE, r=None, extend=0.0):
    """Straight diagonal timber between two (x, z) points. Used only where a
    curve will not fit; a wall bay gets `_brace_arc` instead."""
    y = FY + FD / 2
    sh = 1.0 + (r.uniform(-.06, .06) if r else 0.0)
    p.beam((a[0], y, a[1]), (b[0], y, b[1]), FD, w, mat,
           bevel=S.BEVEL_W, seg=1, tint=.06, extend=extend, shade=sh)
    _pnt(p, mat, .06, sh)


def _arc(p, cx, cz, r_in, r_out, a0, a1, mat, n=8, shade=1.0, d=FD, dy=0.0):
    """Curved brace: a circular sector, WORKED -- stop-chamfered on both arrises
    and adze-faceted on its face, via `_arc_c`. `d` under FD keeps the sector's
    flat sides clear of the member it dies into, so a buried end does not share
    that member's face plane. It was an annular prism with a uniform 14 mm bevel;
    the geometry it occupies has not moved.

    ROUND 15 -- THE ADZE AND THE TILT ARE SIZED TO THE GABLE'S RELIEF, which is
    the only place in the family where they were bigger than the step they had
    to survive. See ADZE_G below: a gable brace stands 20 mm proud of the infill
    behind it, and the default adze (8 mm) plus the default facet tilt (11 mm)
    both cut INWARD from the member's face, so 19 of those 20 mm were spent
    before `_wob` was even called and the cream came through the brace."""
    _arc_c(p, cx, cz, r_out, r_out, r_out - r_in, a0, a1, mat, n=max(9, n + 2),
           y=FY + dy + (FD - d) / 2, d=d, cham=CHAM * .58, stop=.12, shade=shade,
           adze=ADZE_G, tilt=TILT_G, seed=f"gable{cx:.2f}")


def _brace_arc(p, r, side, x_post, x_land, z_spring, z_land, w=W_BRACE,
               mat=None, n=13, into_post=0.045, into_rail=0.022, into_sill=0.055):
    """THE brace of this family, and both of its ends are SEATED.

    An arched brace in real half-timbering springs from a POST and dies into a
    BEAM: it carries load across the corner between them. This one is a quarter
    ELLIPSE fitted to the frame rather than a circle of arbitrary radius, which
    is what lets the springing, the crown and the head all land in timber:

      foot   leaves the near post with a VERTICAL tangent, cut off `into_sill`
             below the springing line -- inside the rail it stands on
      back   runs `into_post` into the near post, so the springing is buried
      crown  laps `into_rail` up into the soffit of the rail above
      head   arrives with a HORIZONTAL tangent, its end face `into_post` inside
             the FAR post

    side=-1 springs off the left-hand post and lands in the right-hand one.
    """
    x_foot = x_post + side * into_post          # outer edge, inside the near post
    cx = x_land - side * into_post              # head end face, inside the far post
    cz = z_spring - into_sill
    ax = abs(cx - x_foot)
    az = z_land + into_rail - cz
    w = min(w, ax - 0.06, az - 0.06)
    m = mat or _oak(r, .14)
    sh = _sh(r, .07)
    # WORKED, not extruded: the chamfer runs the whole curve and stops short of
    # both ends, where the brace is buried in a post and a rail and the wood has
    # to be full for the mortice. Same member, same seat, same ellipse.
    _arc_c(p, cx, cz, ax, az, w, 180.0 if side < 0 else 0.0, 90.0, m, n=n,
           cham=CHAM * .74, stop=.17, tint=.06, shade=sh, seed=f"brace{side}")
    # Pegs on the two joints the brace actually makes. Both land ON a seam
    # half-post, so they are driven into POST_Y; on the FY plane they used to
    # leave they are 36 mm inside it. Positioned from the POST rather than from
    # the brace: `cx - side*.010` was 0.9575 against a post starting at 0.9025,
    # and at W_POST = 0.160 the same expression puts a 0.027 peg 2 mm past the
    # tiling plane. G/2 - W_POST/4 is the half-post's own centre line, so these
    # follow the section instead of having to be re-fitted after it.
    hp = _bw(p) / 2 - W_POST / 4
    _peg(p, side * hp, z_spring + .095, face=POST_Y, r_=.022)
    _peg(p, -side * hp, z_land - .120, face=POST_Y, r_=.024)


def _peg(p, x, z, face=FY, r_=0.030, mat="oak_pale", stand=0.036, h=0.056,
         rot=None):
    """Hand-driven oak peg at a joint. Cheap, and it is most of what makes the
    frame read as pegged carpentry rather than a stack of extruded boxes.

    ROUND 9: IT WAS THERE AND IT COULD NOT BE SEEN. Two reasons, both fatal in
    Solid shading. It was oak_dark driven into oak_dark timber -- one flat tone
    against the same flat tone, so a 60 mm head had no edge to find; and it was
    an untapered 6-gon, so the little silhouette it did have was a smooth bump
    the smoothing angle then rounded off. It is now a peg TAPERED into its hole
    (the outer end is the fat one, which is how a riven peg is driven and which
    leaves the head standing on a shoulder of its own), in `oak_pale`, and
    oak_pale is right rather than a cheat: the kit-wide table gives it to
    "newly cut ends", and the end grain of a peg sawn off flush with a frame is
    precisely that. The heads are the only pale thing on the wall and they are
    54 mm across, so "sparingly" holds.

    `face` is the front plane of the member the peg is driven INTO, and it has to
    be passed: a peg left on the FY plane of a stud now sits 36 mm inside a
    half-post standing at POST_Y (the brace's two joint pegs were buried that
    way), and one left on FY over 0.104 boarding stood 60 mm out of it like a
    spike. `stand` is how far the head stands out of that face -- keep it small on
    anything already proud, because PROUD_MAX is only 0.16 and the bressumer
    alone spends 0.135 of it.
    """
    p.cyl((x, face - stand + h / 2, z), r_, h, mat, sides=6, axis='Y', tint=.07,
          phase=0.4, rot=rot, r_top=r_ * .78)


def _lozenge(p, r, x, z, s=0.200):
    """The diamond motif ref3 sets into its framing. One box on the diagonal."""
    m = _oak(r, .55)
    sh = _sh(r, .06)
    p.box((x, FY + .026, z), (s, .052, s), m, bevel=.014, seg=1, tint=.06,
          rot=(0, 45, 0), shade=sh)
    _pnt(p, m, .06, sh)


def _panel(p, x0, x1, z0, z1, r, mat=None, grow=0.014, tint=.075, cell=0.34,
           rough=0.0, py=None, seed=0):
    """Pillowed plaster infill -- a domed shell, not a slab.

    Both refs show lime plaster BULGING between the timbers: flush with the
    frame at the edges, proud in the middle. A beveled box cannot do that, so
    this is a small quad grid whose middle bellies out (in proportion to the
    panel -- a narrow one that bulges as far as a wide one reads as a bubble),
    welded into a closed slab so normals resolve. Corner shading is then written
    PER VERTEX into the Col layer, so the cushion still reads in flat light;
    doing it per face banded visibly.

    The grid is chosen from the panel's own proportions, ~`cell` metres per quad
    on EACH axis. It used to be n x n regardless of shape, so a 0.75 x 0.24
    frieze panel got 0.25 x 0.08 quads: 3:1 slivers whose diagonals caught the
    light as bright stretched chevrons, and the 0.09 x 1.07 cheek beside a
    widened window was worse still (that cheek is gone -- see `_jamb`).

    ROUGH SIBLINGS (`rough` > 0, and `py` to move the rim). A hand-floated lime
    panel is not a machined dome: `py` shifts the whole panel's rim plane, so two
    panels in a run are NOT flush with each other; the crown is allowed to belly
    a little further out (see ROUGH_BELLY); and every grid vertex is displaced -- hard in y in the
    middle of the panel, only a few mm on the rim, which the frame overlaps by
    `grow` and where a bigger move would crack the plaster off the timber.
    The grid is MEMOISED for that: F/B used to be recomputed per quad, which is
    free while they are a pure function of (i, k) and would tear the shell into
    confetti the moment they carry noise. Regular panels are bit-identical.
    """
    if x1 - x0 < 0.10 or z1 - z0 < 0.10:
        return
    # ROUND 10, AND THIS IS THE CHEAPEST OF THE FOUR FIXES: NOTHING TINTS THE
    # PANEL DOWN ANY MORE. A front-facing panel had a 22% chance of coming out
    # `plaster_dim` (#B8AB90, i.e. 19 L below `plaster`) -- a whole different
    # MATERIAL, so it is visible even in Solid shading where the vertex tint is
    # not, and measured on the family it was 8% of bay A's face and 21% of bay
    # B's. On top of that the tone was 0.86 with +-0.105 of jitter and then a
    # 0.80..1.02 corner ramp on every vertex, so the mean cream panel rendered at
    # about 0.77 of the palette's #E4D9BE and the darkest at 0.60. A "cream wall"
    # whose cream is three quarters strength cannot win against oak_dark.
    # plaster_dim is now what spec says it is -- recessed and shadowed surfaces
    # only, i.e. the reveals and the inner face, both painted in `_core` -- and
    # the panel is the palette tone with a shallow cushion ramp on top of it.
    m = mat or "plaster"
    base = (1.00 if m == "plaster" else 0.94) + r.uniform(-.055, .055)
    a0, a1 = x0 - grow, x1 + grow
    b0, b1 = z0 - grow, z1 + grow
    nu = max(2, min(6, int(round((a1 - a0) / cell))))
    nv = max(2, min(6, int(round((b1 - b0) / cell))))
    rim = PY if py is None else py
    # ROUGH_BELLY, and round 11 had to cut it. The extra allowance is measured
    # from PANEL_Y, so raising the RIM to y = 0 handed every rough panel the
    # same extra depth on top of a crown that had already come forward: a big
    # rough field crowned at -0.054, i.e. 4 mm PROUDER than the arch brace lying
    # across it at FY, and the brace was being swallowed by its own plaster at
    # mid-span. 8 mm keeps every rough crown at -0.042, a clear 8 mm behind the
    # frame face, and costs no character: on any panel bigger than about 0.5 m
    # this term binds for every `py`, so the crown was a constant depth either
    # way -- what makes two hand-floated panels differ is the RIM (`py`, which
    # is where the eye reads the panel against the timber) and the per-vertex
    # lumpiness below, neither of which is touched.
    belly = min(rim - (PANEL_Y - (ROUGH_BELLY if rough else 0.0)),
                .085 * min(a1 - a0, b1 - b0))
    yb = PANEL_BACK                      # flat back, in the void behind the panel
    # ... and it is INSET from the frame line by PANEL_BACK_IN (see the constant:
    # this is the round-12 z-fight fix). The front keeps its grown rectangle, so
    # the plaster still tucks under the timber exactly as before; only the hidden
    # back stops short, and the rim strip that joins the two is a slope instead of
    # a wall. Clamped to 30% of the panel so a frieze slot cannot invert.
    ins_u = min(PANEL_BACK_IN, (x1 - x0) * .30)
    ins_v = min(PANEL_BACK_IN, (z1 - z0) * .30)
    c0, c1 = x0 + ins_u, x1 - ins_u
    d0, d1 = z0 + ins_v, z1 - ins_v
    bump = lambda t: sin(pi * t)
    rr = rng(f"{p.name}/panel_rough/{seed}") if rough else None
    FP, BP = {}, {}
    for i in range(nu + 1):
        for k in range(nv + 1):
            u, v = i / nu, k / nv
            x, z = lerp(a0, a1, u), lerp(b0, b1, v)
            y = rim - belly * bump(u) * bump(v)
            if rough:
                edge = i in (0, nu) or k in (0, nv)
                lat = rough * (.005 if edge else .014)
                x += rr.uniform(-1, 1) * lat
                z += rr.uniform(-1, 1) * lat
                y += rr.uniform(-1, 1) * rough * (.007 if edge else .021)
            FP[(i, k)] = (x, y, z)       # front, domed
            BP[(i, k)] = (lerp(c0, c1, u), yb, lerp(d0, d1, v))
                                         # back, flat and inset -- same (u, v), so
                                         # the rim strips still close the shell
    F = lambda i, k: FP[(i, k)]
    B = lambda i, k: BP[(i, k)]

    # Per-quad jitter has to shrink as the grid grows or a big panel reads as a
    # patchwork quilt; the per-vertex dome shading below carries the variation.
    qt = tint / max(1.0, max(nu, nv) * 0.75)
    front = []
    for i in range(nu):
        for k in range(nv):
            front += p.quad(F(i, k), F(i + 1, k), F(i + 1, k + 1),
                            F(i, k + 1), m, tint=qt, shade=base)
            p.quad(B(i, k), B(i, k + 1), B(i + 1, k + 1), B(i + 1, k), m,
                   tint=.02, shade=base * .80)
    for i in range(nu):                  # rim strips close the shell
        p.quad(F(i, 0), B(i, 0), B(i + 1, 0), F(i + 1, 0), m, tint=.02,
               shade=base * .93)
        p.quad(F(i, nv), F(i + 1, nv), B(i + 1, nv), B(i, nv), m, tint=.02,
               shade=base * .93)
    for k in range(nv):
        p.quad(F(0, k), F(0, k + 1), B(0, k + 1), B(0, k), m, tint=.02,
               shade=base * .93)
        p.quad(F(nu, k), B(nu, k), B(nu, k + 1), F(nu, k + 1), m, tint=.02,
               shade=base * .93)
    # ---- per-vertex corner shading on the front face
    for f in front:
        for l in f.loops:
            co = l.vert.co
            u = (co.x - a0) / max(a1 - a0, 1e-6)
            v = (co.z - b0) / max(b1 - b0, 1e-6)
            # the cushion ramp: was 0.80..1.02, which cost the panel 20% of its
            # brightness at every edge just to say "domed". 0.93..1.03 still
            # reads as a cushion and no longer dims the cream.
            g = 0.93 + 0.10 * bump(min(max(u, 0.0), 1.0)) * bump(min(max(v, 0.0), 1.0))
            c = l[p.clay]
            l[p.clay] = (c[0] * g, c[1] * g, c[2] * g, 1.0)


def _boards(p, x0, x1, z0, z1, n, seed, y=BOARD_Y, d=.126, gap=.012,
            pale=.62):
    """Vertical board-and-gap cladding -- ref3's boarded walls, ref2's apron
    under the jetty windows. Boards are WIDE (0.18-0.22): fine boarding at this
    scale reads as corduroy, which was half the density problem.

    ROUND 11: BOARDING IS AN APRON, NOT A WALL. Every caller now stops it at
    APRON_TOP with plaster above, because that is what ref3 draws -- crop
    ref3:timber and the boarding is under the window line with render over it --
    and because a full-height boarded bay measured 87.6% timber, which is the
    single biggest reason the assembled facade reads brown. The boarding itself
    is unchanged: same widths, same tones, same seeded jitter.

    They are deep enough (0.104) that their backs land INSIDE the backing core
    instead of a millimetre or two in front of its face -- that near-miss was
    3216 cm2 of z-fighting on the boarded bay."""
    r = rng(seed)
    w = (x1 - x0) / n
    for i in range(n):
        a = x0 + w * i + gap / 2
        _mem(p, a, a + w - gap, z0, z1, _oak(r, pale),
             y=y + r.uniform(0, .010), d=d, seg=1, tint=.05,
             shade=1.0 + r.uniform(-.11, .07), bev=.012)


def _ring(p, x0, x1, z0, z1, ax0, ax1, az0, az1, y0, mat="plaster", tint=.04):
    """The backing core WITH AN OPENING IN IT, as ONE welded solid.

    Its two flat faces -- the front at `y0` and the wall's visible inner face at
    y = T -- are each FOUR MITRED TRAPEZOIDS, like a picture frame: outer corner
    to outer corner along the edge, then in to the two matching void corners. So
    the void is real geometry rather than the gap left between four plates that
    lap each other. Two coplanar faces that merely SHARE AN EDGE cannot z-fight,
    and the gate agrees: the clipped overlap of such a pair is exactly zero area,
    so check_zfight does not count it at all (probed on a synthetic ring: 0 pairs,
    0.0 cm2). That is the whole reason for building it this way -- see `_core`.

    MITRED RATHER THAN PINWHEELED, and this is not a style choice -- the first cut
    of this function laid the ring out as two full-width bands plus two cheeks,
    which tiles the ring just as well but puts each cheek's corner in the MIDDLE
    of a band's edge. That T-junction has no vertex to hold it: `_wob` displaces
    the cheek corner while the band's edge stays a straight line between its own
    two vertices, so on the rough bays the two faces sheared apart and the inner
    face grew a fresh sliver of coincidence -- measured, 0.2-0.4 cm2 at
    (0, 0.24, 2.504) on both jetty bays, 100% reachable, i.e. the same defect
    again three orders of magnitude smaller. With mitres every corner of every
    quad is a genuine shared vertex of the lattice: eight per plane, deduplicated
    below, so a wobble that moves one moves every face that uses it and nothing
    can shear. The mitre diagonals are invisible -- coplanar, one material, one
    `_paint` call.

    The winding is worked out, not guessed: in a y = const plane the vertex order
    (outer, next outer, that void corner, this void corner) has normal -Y, so the
    front ring takes it as written, the inner ring reversed; the outer side quads
    are reversed to face out of the solid and the four that bound the void are
    not, so they face INTO it -- which is what lets `_core` find them by centre
    and paint them the reveal tone.
    """
    out = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    inn = [(ax0, az0), (ax1, az0), (ax1, az1), (ax0, az1)]
    P, seen = [], {}

    def v(x, y, z):
        k = (round(x, 7), round(y, 7), round(z, 7))
        if k not in seen:
            seen[k] = len(P)
            P.append((x, y, z))
        return seen[k]

    F = []
    for y, flip in ((y0, False), (T, True)):
        for i in range(4):
            (ux, uz), (wx, wz) = out[i], out[(i + 1) % 4]
            (ix, iz), (jx, jz) = inn[i], inn[(i + 1) % 4]
            q = (v(ux, y, uz), v(wx, y, wz), v(jx, y, jz), v(ix, y, iz))
            F.append(q[::-1] if flip else q)
    for i in range(4):                      # the four outer sides, facing out
        (ux, uz), (wx, wz) = out[i], out[(i + 1) % 4]
        F.append(((v(ux, y0, uz), v(wx, y0, wz), v(wx, T, wz), v(ux, T, uz)))[::-1])
    for i in range(4):                      # the four that bound the void
        (ix, iz), (jx, jz) = inn[i], inn[(i + 1) % 4]
        F.append((v(ix, y0, iz), v(jx, y0, jz), v(jx, T, jz), v(ix, T, iz)))
    return p._emit(P, F, mat, tint, 0, None, 1.0)


def _core(p, holes=(), z_top=None, z0=0.0, y0=CORE_Y):
    """Solid plaster backing behind the frame, with a rectangular void for an
    opening (ONE solid, whether or not it has a void in it).

    ONE solid per rect, not two. This used to be a plate spanning y0..T PLUS a
    `plaster_dim` skim spanning T-0.028..T, so both of them ended on y = T --
    the wall's visible INNER FACE. Two opaque coplanar faces at the surface the
    camera sees is precisely z-fighting, and at 51908 cm2 per plain bay it was
    most of the family's total. The darker inner tone is now painted onto the
    +Y faces of the single plate: same look, no ambiguity, twelve fewer tris.

    ROUND 18 -- AND ONE SOLID FOR THE WHOLE RING, because the four plates that
    used to make it LAPPED, and a lap duplicates both flat faces over the lapped
    rectangle. The previous note here called that "the only shared plane left ...
    a 6 mm x 0.25 m strip at each of the four cheek ends" and treated it as
    small change. It was not, and it is the only thing in this family that a
    camera could actually see:

        cheek/band lap, RAY-MEASURED at 0.5 mm (128 directions per sample,
        full sphere, harness controls in the report):
          inner face, y = T      8 pairs  109.1 cm2  100% reachable, 100% face-on
          core front, y = 0.074 24 pairs  288.4 cm2   23% reachable,  mostly
                                                      grazing-only
        = 397 cm2 of the family's 628, and 163 of its 183 reachable cm2.

    The inner-face half is the same defect as the deleted skim, one order of
    magnitude smaller: two opaque coplanar plaster faces on the surface an
    interior floor butts against, in SM_Wall_TimberJetty_2m_B and its rough
    sibling, where y = T is not a declared seam plane and so nothing was hiding
    them. On the plain window bays the identical strips exist at y = T too and
    are simply excluded from the gate's count by the piece's own seam
    declaration -- so the count understated them; they are gone now as well.

    The rects therefore no longer lap: they TILE the ring, edge to edge, in one
    solid (`_ring`). Butting the old plates instead was the other obvious move
    and it is the wrong one -- that is what put "1971 cm2 of coplanar plaster on
    one plane", because two solids that butt face-to-face duplicate the whole
    interface. Sharing an EDGE duplicates nothing.

    y0 still sits behind the deepest timber back, so the core shares no
    seam-plane rectangle with a frame member either, and the void is still cut
    REV_SPLAY past the opening each side: the oak jamb lapping the reveal used to
    run 6 mm in front of this plaster face and the two fought. The rebate that
    leaves is closed by the bands above and below and by `_reveal`'s backing
    plate behind. The band over the void still starts HEAD_LAP above the head, so
    its soffit is not the same plane as the drip mould's -- which is ON the head,
    because the 4 mm gap between the two was showing a cream hairline of the
    band's front face right across the opening. See THE DRIP MOULD IS THE HEAD OF
    THE HOLE.
    """
    z_top = _bh(p) if z_top is None else z_top
    x0, x1 = -_bw(p) / 2, _bw(p) / 2
    hole = holes[0] if holes else None
    if hole is None:
        fs = p.plate((0.0, (y0 + T) / 2, (z0 + z_top) / 2),
                     (x1 - x0, T - y0, z_top - z0), "plaster", tint=.04)
    else:
        hx0, hx1, hz0, hz1 = hole
        ax0, ax1, zt = hx0 - REV_SPLAY, hx1 + REV_SPLAY, hz1 + HEAD_LAP
        # `_ring` needs plaster on all four sides of the void. The full-bay
        # openings are spec.OPENINGS["win_upper"], which leaves 0.230 m of cheek
        # each side, 0.920 / 0.500 m under the sill and 0.192 / 0.612 m over the
        # head; the half-bay one is spec.OPENINGS["win_attic"] in a 1.0 m bay,
        # which leaves 0.220 m of cheek, 0.600 under and 1.412 over. A hole taken
        # out to a bay edge would need the outer side quad splitting, so it is
        # refused here rather than mis-built -- and that assert is exactly what
        # stops anyone dropping the 1.50 m win_upper into a 1.0 m bay.
        assert (ax0 - x0 > .02 and x1 - ax1 > .02 and hz0 - z0 > .02
                and z_top - zt > .02), "opening reaches a bay edge"
        fs = _ring(p, x0, x1, z0, z_top, ax0, ax1, hz0, zt, y0)
    # the inner face gets the dim tone the deleted skim used to carry, and
    # the faces that BOUND an opening get it darker still: they are the
    # reveal, and left at full plaster brightness they drew a lit cream
    # outline round every window that read as a modelling slip.
    inner, reveal = [], []
    for f in fs:
        ctr = f.calc_center_median()
        if ctr.y > T - 1e-3:
            inner.append(f)
        elif hole and (abs(ctr.x - (hole[0] - REV_SPLAY)) < 1e-3
                       or abs(ctr.x - (hole[1] + REV_SPLAY)) < 1e-3
                       or abs(ctr.z - hole[2]) < 1e-3
                       or abs(ctr.z - (hole[3] + HEAD_LAP)) < 1e-3):
            reveal.append(f)
    if inner:
        p._paint(inner, "plaster_dim", .05, .90)
    if reveal:
        p._paint(reveal, "plaster_dim", .04, .60)


def _reveal(p, hx0, hx1, hz0, hz1, r, o=REV_SPLAY + .012):
    """Dark backing across the back of an opening plus an oak window board in
    the bottom of the reveal. The casement from the windows family drops into
    the front S.REVEAL of the hole and hides the backing.

    The backing is OVERSIZED by `o` and stops 4 mm short of the inner face, so
    all four of its edges are buried inside the core instead of sharing the
    core's four hole-face planes with it (1446 + 1496 + 1482 cm2, measured).
    ROUND 12: `o` follows REV_SPLAY, so the plate still laps 12 mm past the
    plaster cheek now that the cheek stands back from the opening -- it is what
    closes the back of that rebate.

    ROUND 14 -- IT WAS 60 mm INTO THE CASEMENT'S OWN BODY. At y0 = 0.140 this
    plate and windows.py's leaf blank (which runs back to 0.196) shared 56 mm
    over the whole 1.46 x 1.41 aperture: 115 dm3 of doubled solid per window,
    measured. The wall keeps the plate -- an empty opening still has to be
    opaque -- and it moves to the BACK of the reveal, front face on BACK_Y, so
    the insert has the entire depth in front of it. See WHO OWNS THE SOLID
    BEHIND THE GLASS, above the constants, for the plane windows.py trims to.
    """
    y0, y1 = BACK_Y, T - .004
    p.plate(((hx0 + hx1) / 2, (y0 + y1) / 2, (hz0 + hz1) / 2),
            (hx1 - hx0 + 2 * o, y1 - y0, hz1 - hz0 + 2 * o),
            "oak_dark", tint=.05, shade=.55)
    # ROUND 13: the INTERNAL window board stood at y = 0.090..0.150 and rises
    # 30 mm above the sill, so its front 10 mm reached into the front
    # spec.REVEAL of the hole -- it was one of the things blocking the aperture --
    # and it sat exactly where an insert's own body wants to be. It is held in
    # the BACK of the reveal now, at 0.120..0.150, which is a cross-family
    # contract with the numbers windows.py publishes: 4 mm behind its deepest
    # trim (Y_TRIM_BACK 0.116), 2 mm in front of its interior blank (Y_IN 0.152),
    # 8 mm behind its glass (0.112), and still lapping this module's own reveal
    # backing plate by 10 mm -- ROUND 14: that plate's front face moved from
    # 0.140 to BACK_Y, so the board is deepened to follow it rather than left
    # floating in the middle of the reveal with a 50 mm gap behind it. It is
    # also 20 mm narrower than the plate, so their +-X end faces (which are both
    # buried in the core anyway) cannot land on one plane.
    p.plate(((hx0 + hx1) / 2, (.120 + BOARD_BACK) / 2, hz0 + .010),
            (hx1 - hx0 + 2 * o - .020, BOARD_BACK - .120, .040), "oak_mid",
            tint=.06, shade=1.0 + r.uniform(-.05, .05))


def _jamb(p, r, hx0, hx1, hz0, hz1, w=JAMB_W, top=None):
    """The oak jamb between a reveal and the seam post, and the head member.

    win_upper is 1.50 m wide in the bay's panel field, which used to leave
    0.105 m each side. The old code filled that with a PILLOWED PLASTER CHEEK 0.09 x 1.07 --
    a 1:11 sliver whose quad grid stretched into visible chevrons -- and then
    drew an 0.086 lining on top of it, leaving a 19 mm strip of plaster showing
    at the post. That is the broken pattern at the bottom corners of the window.
    So the gap was made ONE jamb, exactly as wide as the gap.

    ROUND 10 SPLITS IT AGAIN, and the difference from the version that failed is
    that the CREAM PART IS ONE FLAT QUAD. The gap grows every time the seam post
    is slimmed (0.290 -> 0.195 -> 0.160, i.e. 0.105 -> 0.179 -> 0.194 each side
    of the opening), so filling all of it
    with oak spent 14% of the bay's face on lining -- and ref2 plainly shows a
    narrow strip of render between a window's casing and the corner post, not
    solid timber. So: `w` of oak lining lapping the reveal, and the rest a plain
    plaster PLATE at the panel rim plane. The old cheek's fault was that it was a
    PILLOWED PANEL -- a 0.09 x 1.07 dome subdivided into 1:9 quads whose diagonals
    lit up as chevrons -- and then had the lining drawn on top of it leaving a
    19 mm sliver showing. A single unsubdivided plate cannot chevron, and all four
    of its edges are buried: the jamb laps it by 8 mm, the seam post covers the
    other 20 mm, and the sill rail and the wall plate cover top and bottom.

    ROUND 11 KEEPS THE SPLIT AND MOVES THE LINE: 0.086 of oak -> JAMB_W 0.062,
    so the gap between reveal and post reads 0.062 lining + 0.114 cream instead
    of 0.086 + 0.093. The window bay was the second-heaviest piece in the family
    and this is 0.19 m2 of it. The lining still laps the reveal, still carries
    its stop-chamfer, and its centre line is JAMB_X, which is what the bay's
    pegs are now positioned from -- they used to be measured in from XE and
    landed in the plaster the moment the post got thinner.
    """
    lap = JAMB_LAP      # the jamb LAPS the reveal by 6 mm instead of ending
    zj0 = hz0 - BURY
    # ROUND 16 -- `top` EXISTS BECAUSE A JAMB DIES INTO WHATEVER IS OVER IT. With
    # the head at 2.400 the default lands the jamb 15 mm inside the wall plate,
    # which is the only thing up there. The centred bay's head is at 1.980 and
    # what is over IT is the transom, with a drip mould below and a frieze panel
    # above, so the caller says where the head goes -- see LOW_JAMB_TOP.
    zj1 = min(hz1 + .035, Z_HEAD[0] + .015) if top is None else top
    for sx in (-1, 1):  # flush on it: flush put oak and plaster on one plane
        edge = (hx1 - lap) if sx > 0 else (hx0 + lap)
        far = edge + sx * w
        a, b = sorted((edge, far))
        # chamfered on the REVEAL arris only -- the other one is lapped over the
        # plaster strip -- and the chamfer runs the height of the opening between
        # stops at the sill and the head, which is how a jamb is worked
        _mem(p, a, b, zj0, zj1,
             _oak(r, .50), y=JAMB_Y, d=JAMB_D, seg=1, tint=.06,
             shade=_sh(r, .07), bev=.012, cham=CHAM * .72,
             arris=(1.0, 0.0) if sx > 0 else (0.0, 1.0),
             stop=.085, facets=2, mids=2, seed=f"jamb{sx}")
        # THE CHEEK STOPS SHORT OF THE JAMB'S ENDS, by CHEEK_END. It used to run
        # zj0..zj1, exactly the jamb's own span, and the jamb LAPS it by 8 mm in
        # x -- so the two members' top faces, and their bottom faces, were the
        # same plane over an 8 x 86 mm rectangle. Ray-measured: 7.0 cm2 per end
        # on the centred bay, 23% reachable and face-on, the escape route being
        # the 8 mm slot between the transom's back and the core's front. Both
        # ends of the cheek are covered by other members (the jamb's lap, the
        # post, the rail above and the sill below -- see the docstring), so
        # dropping 4 mm off each end shows nothing and leaves no shared plane.
        _cheek(p, far - sx * .008, sx * (_xe(p) + BURY), zj0 + CHEEK_END,
               zj1 - CHEEK_END)
    # the drip mould over the head: ref3's pent hood read at PROUD_MAX. The
    # head plate above IS the lintel (2.42 against a 2.40 head), so a full
    # boarded canopy has nowhere to sit -- this is the shallow reading of it.
    # ROUND 13 lifted its soffit 4 mm off hz1 to stop it sharing a plane with the
    # core band over the opening, and ROUND 14 measured what that bought: a
    # 4.8-8.2 mm cream hairline of core plaster showing through the gap, right
    # across the head of every window bay in the family. The soffit is back on
    # hz1 -- it IS the head of the hole -- and the plane it used to share is
    # separated in y instead. See THE DRIP MOULD IS THE HEAD OF THE HOLE.
    m = _oak(r, .45)
    sh = _sh(r, .07)
    # ROUND 19 CHECKED THE 190 mm AGAINST A MUCH SMALLER OPENING AND LEFT IT
    # ALONE, which is worth recording because "scale it with the hole" is the
    # obvious wrong move. The oversail is not a fraction of the opening, it is
    # the JAMB COVER: 0.190/2 = JAMB_W + 0.033, i.e. the mould laps each jamb's
    # top face by 33 mm so the lining's end cap is buried rather than showing in
    # mid-panel. That is a constant in millimetres, so the half bay's 0.52 m
    # win_attic light takes the same 0.190 -- a 0.710 m mould whose half-width
    # (0.355) still clears the half bay's post face (0.420) by 65 mm. Scaled to
    # the opening instead it would have been 0.586, whose half-width (0.293) falls
    # 29 mm SHORT of the jamb's outer face at 0.322 -- it would not cover the lining
    # it exists to cap.
    p.box((0.0, (DRIP_Y + DRIP_BACK) / 2, hz1 + DRIP_H / 2),
          (hx1 - hx0 + .190, DRIP_BACK - DRIP_Y, DRIP_H), m,
          bevel=.012, seg=1, tint=.06, shade=sh)
    _pnt(p, m, .06, sh)


def _cheek(p, xa, xb, z0, z1, py=PY, tint=.035, shade=1.0):
    """The flat cream strip beside a window jamb -- ONE plate, no subdivision.

    It sits on the panel RIM plane, i.e. the depth a pillowed panel meets its
    frame at, so it reads as the same render carried on past the window rather
    than as a separate board; its back is 12 mm inside the plaster core, so no
    face of it is coplanar with the core's front. Deliberately NOT `_panel`: a
    1:15 strip has no business bellying, and a dome that narrow is the thing that
    used to chevron. See `_jamb`.
    """
    a, b = sorted((xa, xb))
    if b - a < .020 or z1 - z0 < .020:
        return
    p.plate(((a + b) / 2, (py + (CORE_Y + .012)) / 2, (z0 + z1) / 2),
            (b - a, (CORE_Y + .012) - py, z1 - z0), "plaster", tint=tint,
            shade=shade)


# ------------------------------------------------------------ shared bands ---
def _frieze_x(k, xe=None):
    """x centres of k evenly spaced frieze studs between the edge posts.

    `xe` is the piece's own XE. k = 0 is legal and returns [] -- a quarter bay's
    frieze is one 0.340 m panel and wants no stud in it at all.
    """
    xe = XE if xe is None else xe
    pw = (2 * xe - k * W_THIN) / (k + 1)
    return [-xe + pw * (i + 1) + W_THIN * (i + 0.5) for i in range(k)]


def _rails(p, r, sole=True, head=True, transom=True, attic=True, studs=1,
           z_tran=None, z_head=None, z_attic=None):
    """The horizontals every bay shares, so a run reads as one frame.

    All four are SHARED BANDS: keyed tone (`_shared`) so a run has no colour step
    at a join, and cut flat at the seam so it has no bevel groove either. The
    wall plate stands at PLATE_Y, proud of the half-posts, so a post's head is
    buried behind it rather than poking 2 mm through; the sole bead does the same
    for the post's foot.

    ROUND 19 -- THE BANDS' HEIGHTS ARE ARGUMENTS AND THEIR LENGTH IS THE PART'S.
    A 3.00 m storey needs the same four bands at four different heights; a 1.0 m
    bay needs the same four heights over half the length. Neither is a new kind
    of wall and neither should be a second copy of this function, so the z's
    default to the H_UPPER family's constants and the x's come off `_bw(p)`.
    THE TONE KEYS DO NOT CHANGE WITH THEM ("sole", "transom", "head", ...): that
    is deliberate and it is the whole point of `_band` -- a tall bay's sole plate
    and a half bay's sole plate are the same stick of oak as a 2 m bay's, so a
    run that mixes footprints still has no colour step at a join.
    """
    xs = _bw(p) / 2
    xe = _xe(p)
    z_tran = Z_TRAN if z_tran is None else z_tran
    z_head = Z_HEAD if z_head is None else z_head
    z_attic = Z_ATTIC if z_attic is None else z_attic
    # WHERE EACH CHAMFER STOPS is not one number: a stop wants to be VISIBLE,
    # and what hides it is whatever member is prouder at that height. The sole
    # plate and the wall plate are prouder than the seam half-post (or the post
    # does not reach them), so their stops read right up against the seam at
    # CHAM_STOP; the transom and the sill rails die into the SIDE of a post that
    # covers the last W_POST/2 of them, so their chamfers stop clear of it at
    # 0.185 instead of dying invisibly behind it.
    if sole:
        _shared(p, "sole", -xs, xs, Z_SOLE[0], Z_SOLE[1],
                mat=OAK, y=BY, d=BD, seg=2, tint=.055,
                cham=CHAM, arris=(.5, 1.0), bow=(0.0, .004), facets=2)
        _shared(p, "sole_bead", -xs, xs, Z_SOLE[1] - .034, Z_SOLE[1] + .018,
                pale=.52, y=BEAD_Y, d=.056, seg=1, tint=.07,
                cham=CHAM_BEAD, stop=.09, facets=0, mids=1)
    if transom:
        _shared(p, "transom", -xs, xs, z_tran[0], z_tran[1],
                mat=OAK, y=BY, d=BD, seg=2, tint=.055,
                cham=CHAM * .70, stop=.185, bow=(.004, .004), facets=2)
    if head:
        _shared(p, "head", -xs, xs, z_head[0], z_head[1], mat=OAK, pale=.10,
                y=PLATE_Y, d=BD + (BY - PLATE_Y), seg=2, tint=.055,
                cham=CHAM, arris=(1.0, .35), stop=.115, bow=(.005, 0.0),
                facets=2)
    if attic:
        fx = _frieze_x(studs, xe)
        for x in fx:                     # sunk into both plates, not kissing
            _mem(p, x - W_THIN / 2, x + W_THIN / 2,
                 z_attic[0] - .015, z_attic[1] + .015,
                 _oak(r, .16), seg=1, shade=_sh(r, .07),
                 cham=CHAM * .8, stop=.055, ret=.022, facets=0, mids=1,
                 narrow=.012, seed="frieze%.2f" % x)
        ed = ([-xe] + [v for x in fx for v in (x - W_THIN / 2, x + W_THIN / 2)]
              + [xe])
        for i in range(0, len(ed), 2):
            _panel(p, ed[i], ed[i + 1], z_attic[0] - .020, z_attic[1] + .024,
                   r, grow=.010, tint=.055)


def _posts(p, z0=None, z1=None, pegs=True, peg_z=None):
    """The half-posts on the tiling seams: two bays side by side make ONE 0.29 m
    post, and that post is the whole reason a timber wall should have no visible
    bay seam at all. Three things make the pair read as one timber:

      * ONE keyed tone for both halves and for every variant (`_band`), so the
        join is not a colour change -- and so a MIRRORED bay still pairs with an
        unmirrored one, which it could not when each half was its own rng draw;
      * `_mem` cuts the seam face dead flat, so the two 18 mm end chamfers that
        used to meet there stop making a groove down the middle of the post;
      * POST_Y stands the post 8 mm PROUD of the mid rails, the way ref3 frames
        its walls: posts run through, rails die into their sides. A rail a variant
        does not carry -- neither window bay can have a transom -- therefore dies
        into 0.29 m of post instead of ending in mid-air at the seam, and the
        transom's own join at the seam is hidden behind the post too.

    Foot and head are sunk into the sole bead and the wall plate, both of which
    are prouder still, so neither end shows. Never tapered, never skewed: the
    outer face IS the seam plane.
    """
    z0 = Z_SOLE[1] - BURY if z0 is None else z0
    z1 = Z_HEAD[0] + .015 if z1 is None else z1
    xs = _bw(p) / 2
    m, sh = _band("post", mat=OAK)
    for sx in (-1, 1):
        a, b = sorted((sx * xs, sx * xs - sx * W_POST / 2))
        with _pin(p, "post"):
            # THE CHAMFER IS ON THE INNER ARRIS ONLY. The half-post's outer
            # arris IS the tiling plane, and two bays' worth of it add up to one
            # W_POST post: chamfering it would cut a double-width V down the
            # middle of the very post the fourth pass spent its whole effort
            # making invisible. Chamfered on the inside, the finished post carries one
            # stop-chamfer on each of its two free arrises, which is what a post
            # in the reference has -- and it stays symmetric under mirroring.
            # CHAM * .72 rather than CHAM: the half-post is 0.080 wide now, and
            # a 26 mm chamfer on one of its two arrises would round away a third
            # of the face the stop-chamfer exists to ornament. 19 mm keeps the
            # detail in proportion to the member -- the same ratio it had at
            # 0.0975 -- and `_hexsec`'s span*.42 clamp is no longer what decides
            # it, which it would be at CHAM.
            _mem(p, a, b, z0, z1, m, y=POST_Y, d=POST_BACK - POST_Y, seg=2,
                 tint=.055, shade=sh, cham=CHAM * .72,
                 arris=(1.0, 0.0) if sx > 0 else (0.0, 1.0),
                 stop=.130, belly=.005, facets=2, mids=3, seed="post")
        # ONE peg where the transom tenons in, at the same x and z in EVERY
        # variant, so a finished post carries a symmetric pair either side of the
        # join. That pair is what says "one pegged post" rather than "two bays
        # touching", and being symmetric it survives mirroring. Only one pair:
        # the brace already pegs the springing and the landing on this same post
        # in the braced variants, and a second row turned the joint into a
        # scatter of nubs.
        if pegs:
            # ROUND 19 -- `peg_z`, because the transom is not at 2.000 in every
            # footprint. A 3.00 m storey's mid rail is at 2.420 and a 1.30 m knee
            # wall has none at all; the guard below already skipped the peg on a
            # piece the default height falls outside, which left the knee wall's
            # post unpegged rather than pegged in the wrong place.
            pz = (Z_TRAN[0] + .072) if peg_z is None else peg_z
            if z0 - .03 < pz < z1:
                # Centred on the half-post rather than measured in from the
                # seam, so it cannot walk off the post's inner face the next
                # time W_POST is trimmed: the half-post runs from G/2 - W_POST/2
                # to G/2, so its centre is G/2 - W_POST/4. At 0.160 that is
                # x = 0.960 and a 0.022 peg sits 0.930..0.982, clear both sides.
                _peg(p, sx * (xs - W_POST / 4), pz, face=POST_Y, r_=.022)


def _flatten_inner(p, eps=.050):
    """Pull the backing core's inner face back onto y = T after wobbling.

    y = T is the plane an interior floor or a wall above butts against, and the
    wobble bulges it by up to 11 mm. The two jetty pieces always needed this
    doing by hand, because they declare y = (0, T + JETTY) for their soffit and
    so nothing else stops them. The plain bays used to get it free from
    Part.finish()'s seam clamp -- correct, but it shows up in the report as a
    "clamped" row that reads like a fault, so `_done` now runs this on EVERY
    piece and the clamp has nothing left to do. Only verts within `eps` of T are
    touched, so the soffit boards (which legitimately reach T + JETTY) are left
    alone.
    """
    for v in p.bm.verts:
        if T < v.co.y < T + eps:
            v.co.y = T


def _shell(p, r, studs=1):
    _core(p)
    _posts(p)
    _rails(p, r, studs=studs)


# ================================================================ pieces =====
def wall_a():
    """The plain bay, and the one that sets the family's proportions: two fat
    seam posts, three rails, ONE 1.84 m plaster panel and ONE broad arch brace.
    No intermediate studs at all -- that is what the reference bays look like.

    The brace springs out of the sole plate hard against the left post and dies
    into the right post under the transom, lapping the transom's soffit on the
    way. It used to be a floating quarter-circle attached to nothing."""
    p = _reserve(Part("SM_Wall_Timber_2m_A", budget="wall", seams=SEAMS))
    r = rng("timber/A")
    _shell(p, r)
    f0, f1 = Z_FIELD
    _panel(p, -XE, XE, f0, f1, r)
    _brace_arc(p, r, -1, -XE, XE, f0, f1)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_b():
    """One intermediate post, two panels and the lozenge motif ref3 sets into
    its framing -- and NO brace.

    A brace has to span from a post to a rail, and in a 2 m bay the only place
    its head can be tenoned is the far post (see `_brace_arc`), which the
    intermediate post is standing in the middle of. So B answers A with framing
    instead of with a second arc: alternate A and B along a run and the wall
    gets a rhythm without a single brace that carries nothing."""
    p = _reserve(Part("SM_Wall_Timber_2m_B", budget="wall", seams=SEAMS))
    r = rng("timber/B")
    _shell(p, r)
    f0, f1 = Z_FIELD
    xk = -0.100                            # the one intermediate post
    ka, kb = xk - W_STUD / 2, xk + W_STUD / 2
    _mem(p, ka, kb, f0 - BURY, f1 + BURY, _oak(r, .14), seg=2, shade=_sh(r, .08),
         taper=0.94, cham=CHAM * .82, stop=.145, belly=.006, facets=3, mids=3,
         seed="Bpost")
    _panel(p, -XE, ka, f0, f1, r)
    _panel(p, kb, XE, f0, f1, r)
    _lozenge(p, r, (-XE + ka) / 2, 1.520, .215)
    _lozenge(p, r, (kb + XE) / 2, 0.700, .180)
    for z in (f0 + .16, f1 - .16):
        _peg(p, xk, z)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_c():
    """The BOARDED bay. ref3 shows plenty of upper walling that is vertical
    boarding rather than plaster, and the brief asks for both mixed -- so the
    third variant swaps material instead of piling on more sticks (the first
    pass answered 'make C busiest' with a herringbone thicket, which is exactly
    what made the family read as half-scale). Boarding plus a ledger is the
    feature here; a brace laid over boarding would only be a decal on top of a
    surface that is already doing the work.

    ROUND 11 -- THE BOARDING IS AN APRON NOW, AND THIS IS THE FAMILY'S SINGLE
    BIGGEST RATIO CHANGE. Measured head-on this bay was 87.6% timber: boarding
    ran the full 1.87 m field, so the only cream on it was four frieze slots.
    The assembler puts `c` on most of the north elevation and mixes it into the
    front runs, so one piece was making whole walls brown on its own.
    Go and look at ref3:timber before assuming that was faithful -- the boarded
    walling there is UNDER the window line, with render above it, exactly like
    the boarded apron on the jettied bays. So the boarding stops at the family's
    sill line, the ledger IS that line (which also puts C's one horizontal
    exactly where the window bays put theirs, so a run of `c` and `win` shares
    a line instead of stepping), and the 1.05 m above it is one plaster panel.
    Nothing about the boarding itself changed -- same widths, same tones, same
    seed -- there is just half as much of it."""
    p = _reserve(Part("SM_Wall_Timber_2m_C", budget="wall", seams=SEAMS))
    r = rng("timber/C")
    _core(p)
    _posts(p)
    _rails(p, r, studs=2)
    f0, f1 = Z_FIELD
    zl = (APRON_TOP, SILL_TOP)             # the ledger IS the family's sill line
    # boarding grown 26 mm PAST the ledger's soffit so the two lap instead of
    # butting on z = APRON_TOP, which would be two coplanar faces at the join
    _boards(p, -XE, XE, f0 - .012, zl[0] + .026, 8, "timber/C/boards")
    _panel(p, -XE, XE, zl[1], f1, r)
    _shared(p, "ledger", -G / 2, G / 2, zl[0], zl[1], mat=OAK, pale=.14,
            y=BY + .016, d=BD - .016, seg=2, tint=.055,
            cham=CHAM * .70, stop=.185, bow=(.003, .003), facets=2)
    # driven into the BOARDING, not the frame plane: on FY these stood 60 mm out
    # of a 0.104 board and read as spikes. Both rows are in the apron now -- the
    # upper pair used to sit at zl[1] + 0.21, which is plaster since the panel
    # arrived, and a peg floating in render is not a joint.
    for x in (-XE + .12, XE - .12):
        _peg(p, x, zl[0] - .21, face=BOARD_Y, r_=.026)
        _peg(p, x, zl[0] - .52, face=BOARD_Y, r_=.026)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_window():
    """OPENINGS['win_upper'] -- 1.50 x 1.45, sill 0.95, so the head is at 2.40.

    That is a big casement in a 2.0 x 2.6 bay and it dictates the whole bay:
      * NO transom and NO frieze. Both used to be drawn straight through the top
        0.40 m of the hole, because this piece was written when win_upper was
        0.86 x 1.05 and its head landed exactly on the transom's soffit.
      * the head plate at 2.42 IS the window head -- 20 mm of core above the
        opening -- with a proud drip mould under it standing in for ref3's
        pent hood, which no longer fits under the wall plate.
      * the gap each side is an oak JAMB, not a plaster cheek.
      * the sill rail's top face IS the opening's sill.

    ROUND 10: THE APRON UNDER THE SILL IS PLASTER, not vertical boarding, and on
    the measurement this is the single biggest change in the family. This bay had
    NO plaster on its face at all -- 98% of it was timber -- because the window
    ate the middle, boarding filled everything under the sill and the frame did
    the rest, and a facade is made mostly of window bays. Boarding under a sill
    is a JETTY detail in both references (it is the apron hung off the overhang,
    and SM_Wall_TimberJetty_2m_B still has it); on a wall standing flat on the
    storey below, ref2 and ref3 both run the cream straight down past the window
    to the rail below. The boarded look stays in the family as SM_Wall_Timber_2m_C.
    The sill band also now sits at exactly the jetty variant's apron rail
    (APRON_TOP - 0.026 .. APRON_TOP + 0.150), so the two window bays finally
    share one sill line instead of stepping 24 mm against each other.
    Every number here comes off spec.OPENINGS."""
    p = _reserve(Part("SM_Wall_TimberWin_2m", budget="wall", seams=SEAMS))
    r = rng("timber/W")
    ow, oh, sz = OPEN["w"], OPEN["h"], OPEN["sill"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, sz, sz + oh
    _core(p, holes=[(hx0, hx1, hz0, hz1)])
    _posts(p)
    _rails(p, r, transom=False, attic=False)
    _reveal(p, hx0, hx1, hz0, hz1, r)
    # the family's one sill band, APRON_TOP..SILL_TOP -- 0.118 tall where it was
    # 0.176, which is 0.116 m2 of this bay's face given back to the cream apron
    _panel(p, -XE, XE, Z_FIELD[0], APRON_TOP, r)
    _shared(p, "sill", -G / 2, G / 2, APRON_TOP, SILL_TOP, mat=OAK, pale=.14,
            y=BY, d=BD, seg=2, tint=.055, cham=CHAM, stop=.185,
            bow=(.004, .004), facets=2)
    # THE CILL, and the wall owns it -- see THE SILL BELONGS TO THE WALL. Its top
    # was at hz0 + 0.014, i.e. 14 mm INSIDE the opening, which is 14 mm of the
    # casement's 20 mm of clearance gone before the casement is even built.
    _mem(p, hx0 - .095, hx1 + .095, hz0 - CILL_DROP - CILL_H, hz0 - CILL_DROP,
         _oak(r, .58),
         y=BY - .030, d=.120, seg=2, tint=.07, cham=CHAM_BEAD * 1.6,
         stop=.10, facets=0, mids=1, seed="nose")
    _jamb(p, r, hx0, hx1, hz0, hz1)
    # driven into the JAMB -- these are the pegs holding the window frame in --
    # so they take the jamb's OWN centre line. Measured in from XE they walked
    # into the cream cheek the moment either the post or the lining got thinner.
    for sx in (-1, 1):
        _peg(p, sx * JAMB_X, hz0 + .16, face=JAMB_Y, r_=.020)
        _peg(p, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.020)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


def wall_window_low():
    """THE SAME OPENING, CENTRED IN THE WALL. OPENINGS['win_upper'] again --
    1.500 x 1.450 to the micrometre, so every casement the windows family built
    for SM_Wall_TimberWin_2m drops into this bay unchanged -- but with

        SILL z = 0.530      HEAD z = 1.980

    instead of 0.950 / 2.400. That is 0.435 m of plaster field under the sill
    against 0.440 m over the head: centred between the sole plate and the wall
    plate to five millimetres. See THE WINDOW WAS JAMMED UNDER ITS HEAD for why
    centred rather than a two-thirds line (the opening is 55.8% of the storey;
    there is no two-thirds line left to put it on) and for why the head is not a
    free choice.

    SM_Wall_TimberWin_2m IS KEPT. This is an additional option, not a
    replacement: the high bay reads as a tall storey with a big casement pushed
    up under the eave, which is right on a jettied front elevation, and it is
    what Shanee said looks good. This one is for the positions where the wall
    above the window is doing work -- a gable end, a band under a run of
    dormers -- and it is the one to reach for when a high window looks top-heavy.

    WHAT MAKES IT MORE THAN THE SAME BAY SLID DOWN: with the head under the
    transom, this is THE ONLY WINDOW BAY IN THE FAMILY THAT CARRIES THE WHOLE
    SHARED FRAME. `_rails` is called with every band switched on -- sole plate,
    transom, wall plate and the frieze between the last two -- exactly as the
    plain bays A and B call it, so a run of a/b/c/winlow shows FOUR continuous
    horizontals with no rail stopping at a post. The existing window bay cannot:
    its head at 2.400 has the transom drawn straight through it, so it drops the
    transom and the frieze and two of the four lines die at the seam.
    The drip mould's top is BURY inside the transom's soffit, so the hood reads
    as tucked under the mid rail -- ref3's own detail -- with no cream hairline
    between the two (round 14's defect) because there is no gap to show one.
    Everything else is the window bay verbatim: the cill is the wall's, at
    CILL_DROP under the new sill; the jambs are JAMB_W of oak with a cream cheek
    out to the post; the reveal backing sits at BACK_Y so the insert owns the
    front of the reveal."""
    p = _reserve(Part("SM_Wall_TimberWinLow_2m", budget="wall", seams=SEAMS))
    r = rng("timber/WL")
    ow, oh = OPEN["w"], OPEN["h"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, LOW_SILL, LOW_HEAD
    _core(p, holes=[(hx0, hx1, hz0, hz1)])
    _posts(p)
    _rails(p, r, studs=1)               # ALL FOUR BANDS -- see the docstring
    _reveal(p, hx0, hx1, hz0, hz1, r)
    # the apron: 0.317 m of plaster between the sole plate and the sill rail
    _panel(p, -XE, XE, Z_FIELD[0], LOW_APRON_TOP, r)
    _shared(p, "sill", -G / 2, G / 2, LOW_APRON_TOP, LOW_SILL, mat=OAK, pale=.14,
            y=BY, d=BD, seg=2, tint=.055, cham=CHAM, stop=.185,
            bow=(.004, .004), facets=2)
    # THE CILL, tucked CILL_DROP under the new sill line exactly as the high bay
    # tucks it under 0.950 -- the wall owns it, the insert does not build one
    _mem(p, hx0 - .095, hx1 + .095, hz0 - CILL_DROP - CILL_H, hz0 - CILL_DROP,
         _oak(r, .58),
         y=BY - .030, d=.120, seg=2, tint=.07, cham=CHAM_BEAD * 1.6,
         stop=.10, facets=0, mids=1, seed="nose")
    _jamb(p, r, hx0, hx1, hz0, hz1, top=LOW_JAMB_TOP)
    for sx in (-1, 1):
        _peg(p, sx * JAMB_X, hz0 + .16, face=JAMB_Y, r_=.020)
        _peg(p, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.020)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


# =============================================================================
# ============ THE FRACTIONAL BAYS  (round 19) ================================
# =============================================================================
# See THE FRACTIONAL FOOTPRINTS, above the constants, for what each one is and
# why it is that rather than a scaled copy of a 2 m bay. Every piece below
# declares its own seams with `_seams()` and stamps the same numbers on the Part
# with `_bay()`, and those two have to agree: the seams are what `check()`
# validates the built mesh against and the stamp is what every builder in this
# file reads to decide where the tiling planes are.
def wall_half_a():
    """SM_Wall_Timber_1m_A -- HALF a bay wide (1.000 m), full storey.

    THE PLAIN NARROW BAY. Two 0.080 half-posts on the seams leave one 0.840 m
    panel field, so this is bay A's argument at half the width: no intermediate
    studs, one arch brace, all four shared horizontals running through.

    WHY IT ALSO CARRIES THE SILL LINE, which A does not. `_brace_arc` fits its
    ellipse to the frame it braces, so the same call that gives the 2 m bay a
    1.930 x 1.982 quarter arc (ratio 1.027, a quarter circle -- the whole reason
    the third pass rebuilt it) gives a 1 m bay 0.930 x 1.982, ratio 2.13. That is
    not an arch, it is a bent post, and it would pass every numeric check in this
    file. A brace needs a rail at the right height to die into, and the family
    already owns one: APRON_TOP..SILL_TOP, the single sill line that `c`, `win`,
    `jetty_a` and `jetty_b` share. Landing the head under it gives
    0.930 x 0.814 -- ratio 0.875, the same near-quarter circle at half the size --
    with the head lapping `into_rail` into that rail's soffit and the foot cut
    `into_sill` down inside the sole plate, i.e. both ends in solid timber, which
    is the standard this family holds a brace to.
    The bay is then a 0.737 m apron with the arch in it and a 1.050 m panel over
    the sill -- and two of them side by side (the assembler mirrors alternate
    bays) put their two arches back to back over the post they share, which is
    the same arcade a mirrored pair of 2 m A bays makes, one storey smaller.
    """
    p = _bay(_reserve(Part("SM_Wall_Timber_1m_A", budget="wall",
                           seams=_seams(w=G_HALF))), w=G_HALF)
    r = rng("timber/1mA")
    xe, xs = _xe(p), G_HALF / 2
    _shell(p, r)
    _shared(p, "sill", -xs, xs, APRON_TOP, SILL_TOP, mat=OAK, pale=.14,
            y=BY, d=BD, seg=2, tint=.055, cham=CHAM, stop=.185,
            bow=(.004, .004), facets=2)
    _panel(p, -xe, xe, Z_FIELD[0], APRON_TOP, r)
    _panel(p, -xe, xe, SILL_TOP, Z_FIELD[1], r)
    _brace_arc(p, r, -1, -xe, xe, Z_FIELD[0], APRON_TOP)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_half_b():
    """SM_Wall_Timber_1m_B -- half a bay wide, CLOSE STUDDED.

    B's argument at half the width, and it is the same argument: answer A's arch
    with framing rather than with a second curve. One 0.130 post on the centre
    line makes three verticals in a metre -- posts at 0.080, a stud at 0.130,
    panels of 0.355 -- which is close studding, and close studding is exactly
    what ref3 does where its bays are narrow. The two panels are 0.355 x 1.905:
    tall and narrow, which is what close studding looks like and is the reason
    `_panel` picks its grid from the panel's own proportions (2 x 6 quads of
    0.19 x 0.32 here, not the 1:9 slivers that used to chevron).

    ONE lozenge, not B's two. A 0.110 box on the diagonal measures 0.156 across
    the flats, i.e. 44% of the panel it sits in, against 40% for the 0.215
    lozenge in the 2 m bay's 0.755 m panel -- the same motif at the same weight.
    A second one in the other panel would be a pattern rather than a motif at
    this width.
    """
    p = _bay(_reserve(Part("SM_Wall_Timber_1m_B", budget="wall",
                           seams=_seams(w=G_HALF))), w=G_HALF)
    r = rng("timber/1mB")
    xe = _xe(p)
    _shell(p, r)
    f0, f1 = Z_FIELD
    xk = 0.0                               # the one intermediate post
    ka, kb = xk - W_STUD / 2, xk + W_STUD / 2
    _mem(p, ka, kb, f0 - BURY, f1 + BURY, _oak(r, .14), seg=2, shade=_sh(r, .08),
         taper=0.94, cham=CHAM * .82, stop=.145, belly=.006, facets=3, mids=3,
         seed="1mBpost")
    _panel(p, -xe, ka, f0, f1, r)
    _panel(p, kb, xe, f0, f1, r)
    _lozenge(p, r, (kb + xe) / 2, 1.180, .110)
    for z in (f0 + .16, f1 - .16):
        _peg(p, xk, z)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_qtr_a():
    """SM_Wall_Timber_0m5_A -- a QUARTER bay wide (0.500 m). Posts and infill.

    At 0.5 m the two half-posts leave 0.340 m of field, and every figure the
    family owns is bigger than that gap. Measured, which is the only way to
    decide it rather than assert it:
        an arch brace  fits an ellipse 0.430 x 1.982 -- ratio 4.6, a bracket
        an intermediate stud  0.130 wide would leave two panels of 0.105, i.e.
                       narrower than the stud dividing them
        a lozenge      0.255 across the flats (s = 0.180) in a 0.340 panel is a
                       blocked panel, not a motif set into one
    So it carries what a quarter bay honestly has: the two seam posts, the four
    shared horizontals at their full sections, one 0.340 x 1.905 field and a
    frieze of ONE panel with no stud in it (`_frieze_x(0)` is legal for exactly
    this case). It is 32% timber in the verticals before a rail is drawn and that
    is simply what a 0.5 m bay is -- its job is to close a half-metre gap in a run
    without anything being stretched to do it.
    """
    p = _bay(_reserve(Part("SM_Wall_Timber_0m5_A", budget="wall",
                           seams=_seams(w=G_QTR))), w=G_QTR)
    r = rng("timber/0m5A")
    xe = _xe(p)
    _core(p)
    _posts(p)
    _rails(p, r, studs=0)
    _panel(p, -xe, xe, Z_FIELD[0], Z_FIELD[1], r)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_half_window():
    """SM_Wall_TimberWinAttic_1m -- the half bay with a light in it.

    THE OPENING IS OPENINGS["win_attic"], 0.520 x 0.580 at sill 0.600, and it is
    not win_upper for a reason that is arithmetic rather than taste: win_upper is
    1.500 m wide and this bay is 1.000 m wide. See THE HALF BAY'S WINDOW IS NOT
    win_upper for the full contract, including the check in both directions
    against gables.py's SM_Gable_WinFrame, which is the insert built for this
    hole and which that family declares snaps to any win_attic opening.
    AN ASSEMBLER PLACES THAT INSERT AT z = 0.600.

    THE BAY IS THE FAMILY'S WINDOW BAY, at a smaller size and with one change
    that the smaller light makes possible: it carries ALL FOUR shared
    horizontals. SM_Wall_TimberWin_2m cannot -- a 1.45 m casement whose head is
    at 2.400 has the transom drawn straight through it, so that bay drops the
    transom and the frieze. Here the head is at 1.180, well under the mid rail,
    so the sole plate, the transom, the frieze and the wall plate all run
    through and a half bay dropped into a run breaks none of the four lines.

    Everything else is this family's own detail at this size: the sill rail's top
    face IS the opening's sill (0.482..0.600, the standard SILL_H band), the wall
    owns the cill under it, the two jambs run from the sill rail up into the
    transom -- so they read as the studs framing the light, which is what they
    are -- a cream cheek fills the 0.126 m between each jamb and its post
    (0.128 m in the 2 m bay: the same strip), the drip mould is the head of the
    hole, and there is a pillowed panel over the hood and another under the sill.
    """
    p = _bay(_reserve(Part("SM_Wall_TimberWinAttic_1m", budget="wall",
                           seams=_seams(w=G_HALF))), w=G_HALF)
    r = rng("timber/1mWA")
    xe, xs = _xe(p), G_HALF / 2
    ow, oh = OPEN_S["w"], OPEN_S["h"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, SM_SILL_TOP, SM_HEAD
    _core(p, holes=[(hx0, hx1, hz0, hz1)])
    _posts(p)
    _rails(p, r, studs=1)
    _reveal(p, hx0, hx1, hz0, hz1, r)
    _panel(p, -xe, xe, Z_FIELD[0], SM_APRON_TOP, r)
    _shared(p, "sill", -xs, xs, SM_APRON_TOP, SM_SILL_TOP, mat=OAK, pale=.14,
            y=BY, d=BD, seg=2, tint=.055, cham=CHAM, stop=.185,
            bow=(.004, .004), facets=2)
    # THE CILL, and the wall owns it -- the same member as the 2 m bay's, tucked
    # the same CILL_DROP under the sill line and projecting the same 95 mm each
    # side, so the two bays' cills are the same detail at two opening widths.
    _mem(p, hx0 - .095, hx1 + .095, hz0 - CILL_DROP - CILL_H, hz0 - CILL_DROP,
         _oak(r, .58),
         y=BY - .030, d=.120, seg=2, tint=.07, cham=CHAM_BEAD * 1.6,
         stop=.10, facets=0, mids=1, seed="nose")
    # the jambs die into the TRANSOM, not into the mould over the head: a lining
    # that stopped 20 mm above a 0.58 m light would leave its own end cap showing
    # in mid-panel, and the honest member here is the stud that frames the light
    # and runs to the rail above it. Same JAMB_W, so the mould still oversails
    # each one by 33 mm exactly as it does in the 2 m bay.
    _jamb(p, r, hx0, hx1, hz0, hz1, top=Z_TRAN[0] + .015)
    # the panel over the hood: its grown rim is inside the mould below (which
    # runs to +-0.355, past this panel's +-0.274), inside the jambs at the sides
    # and inside the transom above, so no edge of it is in the open.
    _panel(p, hx0, hx1, SM_HEAD + DRIP_H, Z_FIELD[1], r)
    for sx in (-1, 1):
        _peg(p, sx * SM_JAMB_X, hz0 + .12, face=JAMB_Y, r_=.020)
        _peg(p, sx * SM_JAMB_X, hz1 - .16, face=JAMB_Y, r_=.020)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=SM_DRIP_X)
    return _done(p)


# ---------------------------------------------------- the 3.00 m storey ------
def wall_tall_a():
    """SM_Wall_TimberTall_2m_A -- bay A CUT 3.00 m TALL, not stretched to it.

    This is the piece the first of the two complaints asks for. 19 copies of
    SM_Wall_Timber_2m_A stand in the showpiece at scale (1, 1, 1.154), which is
    assemble_inn.py's `zs = H_GROUND / H_UPPER` doing the only thing it could:
    filling a 3.00 m storey with a wall cut 2.60 m tall. Every timber on those 19
    objects is 15.4% taller than it was cut in one axis only -- the stop-chamfer,
    the adze facets, the arris wear and the peg heads with it -- and no carving
    survives that.
    Here nothing is stretched. Every section, chamfer, facet, bow and peg is the
    number it has always been; what changed is where the two upper bands sit, and
    that was decided by the window rather than by eye (see THE FRACTIONAL
    FOOTPRINTS: TZ_TRAN's soffit is placed to bury the drip mould over a
    win_upper head at 2.400, exactly as Z_TRAN and Z_HEAD were placed for the
    2.60 family). The field comes out 2.325 x 1.840, a 1.26:1 portrait panel
    against the 2.60 bay's 1.04:1, with the same single arch brace fitted to it:
    1.930 x 2.402, ratio 1.24 against the shorter bay's 1.03.
    """
    p = _bay(_reserve(Part("SM_Wall_TimberTall_2m_A", budget="wall",
                           seams=_seams(h=HG))), h=HG)
    r = rng("timber/TA")
    _core(p)
    _posts(p, z1=TZ_POST_TOP, peg_z=TZ_TRAN[0] + .072)
    _rails(p, r, studs=1, z_tran=TZ_TRAN, z_head=TZ_HEAD, z_attic=TZ_ATTIC)
    f0, f1 = TZ_FIELD
    _panel(p, -XE, XE, f0, f1, r)
    _brace_arc(p, r, -1, -XE, XE, f0, f1)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_tall_b():
    """SM_Wall_TimberTall_2m_B -- bay B cut 3.00 m tall. Same argument as B:
    an intermediate post and two panels instead of a brace, with the lozenges at
    the same FRACTIONS of the field they sit at in the 2.60 bay (75% and 32% of
    the field's height, i.e. 1.835 and 0.835 here against 1.520 and 0.700
    there) so the motif is in the same place on the wall rather than at the same
    number of metres up it."""
    p = _bay(_reserve(Part("SM_Wall_TimberTall_2m_B", budget="wall",
                           seams=_seams(h=HG))), h=HG)
    r = rng("timber/TB")
    _core(p)
    _posts(p, z1=TZ_POST_TOP, peg_z=TZ_TRAN[0] + .072)
    _rails(p, r, studs=1, z_tran=TZ_TRAN, z_head=TZ_HEAD, z_attic=TZ_ATTIC)
    f0, f1 = TZ_FIELD
    xk = -0.100
    ka, kb = xk - W_STUD / 2, xk + W_STUD / 2
    _mem(p, ka, kb, f0 - BURY, f1 + BURY, _oak(r, .14), seg=2, shade=_sh(r, .08),
         taper=0.94, cham=CHAM * .82, stop=.145, belly=.006, facets=3, mids=4,
         seed="TBpost")
    _panel(p, -XE, ka, f0, f1, r)
    _panel(p, kb, XE, f0, f1, r)
    _lozenge(p, r, (-XE + ka) / 2, 1.835, .215)
    _lozenge(p, r, (kb + XE) / 2, 0.835, .180)
    for z in (f0 + .16, (f0 + f1) / 2, f1 - .16):
        _peg(p, xk, z)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_tall_window():
    """SM_Wall_TimberTallWin_2m -- the win_upper bay cut 3.00 m tall.

    THE OPENING DOES NOT MOVE: OPENINGS["win_upper"], 1.500 x 1.450 at sill
    0.950, head 2.400, the same jambs, the same cill, the same drip mould, the
    same reveal backing at BACK_Y and the same 20 mm of INSERT_CLEAR, so every
    casement the windows family built for SM_Wall_TimberWin_2m drops into this
    bay unchanged AND AT THE SAME z. That is the point of authoring the storey
    instead of scaling it: under `zs = 1.154` the opening stretched with the
    wall, 1.450 -> 1.673, and the leaf did not, which is the 263 mm of open
    reveal the windows audit measured over every casement on that storey.

    WHAT THE EXTRA 0.40 m BUYS, and it is the answer to the other half of the
    round-16 complaint ("the window ... looks out of balance with the walls
    around it"). In a 2.60 storey there are 20 mm of core between the head and
    the wall plate, so the transom cannot pass over the window and
    SM_Wall_TimberWin_2m has to drop both the transom and the frieze. Here there
    are 0.420 m: the mid rail runs OVER the opening with the hood tucked BURY
    under its soffit, the frieze runs over that, and this is the only full-width
    win_upper bay in the family that carries all four shared horizontals.
    """
    p = _bay(_reserve(Part("SM_Wall_TimberTallWin_2m", budget="wall",
                           seams=_seams(h=HG))), h=HG)
    r = rng("timber/TW")
    ow, oh, sz = OPEN["w"], OPEN["h"], OPEN["sill"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, sz, sz + oh
    _core(p, holes=[(hx0, hx1, hz0, hz1)])
    _posts(p, z1=TZ_POST_TOP, peg_z=TZ_TRAN[0] + .072)
    _rails(p, r, studs=1, z_tran=TZ_TRAN, z_head=TZ_HEAD, z_attic=TZ_ATTIC)
    _reveal(p, hx0, hx1, hz0, hz1, r)
    _panel(p, -XE, XE, Z_FIELD[0], APRON_TOP, r)
    _shared(p, "sill", -G / 2, G / 2, APRON_TOP, SILL_TOP, mat=OAK, pale=.14,
            y=BY, d=BD, seg=2, tint=.055, cham=CHAM, stop=.185,
            bow=(.004, .004), facets=2)
    _mem(p, hx0 - .095, hx1 + .095, hz0 - CILL_DROP - CILL_H, hz0 - CILL_DROP,
         _oak(r, .58),
         y=BY - .030, d=.120, seg=2, tint=.07, cham=CHAM_BEAD * 1.6,
         stop=.10, facets=0, mids=1, seed="nose")
    _jamb(p, r, hx0, hx1, hz0, hz1, top=TZ_JAMB_TOP)
    for sx in (-1, 1):
        _peg(p, sx * JAMB_X, hz0 + .16, face=JAMB_Y, r_=.020)
        _peg(p, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.020)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


# ------------------------------------------------- the fractional heights ----
def wall_knee():
    """SM_Wall_TimberKnee_2m -- a KNEE WALL, 1.300 m = half a storey.

    Not a squashed storey: a wall with a head and no middle. Sole plate and bead
    at the bottom, the family's FULL 0.180 m wall plate at the top (1.120..1.300,
    the same section, the same keyed tone and the same PLATE_Y as every other
    wall plate here, so a gable's sole plate, a roof eave or a tie beam beds on
    this one exactly as it beds on a full bay's), and ONE field between them. No
    transom -- there is nothing to divide -- and no frieze, because a frieze is
    by definition the band between a mid rail and the plate.

    THE FIELD IS THE POINT: 1.025 x 1.840 is the only LANDSCAPE panel in the
    family, 1.79:1, and a landscape panel is what a flat segmental arch wants.
    The same `_brace_arc` fitted to it comes out 1.930 x 1.102, ratio 0.571
    against the 2 m bay's 1.027 -- a low spandrel arch springing out of the sole
    plate and dying into the head plate's soffit, both ends in solid timber. That
    is what a knee wall or the spandrel under a gable actually carries, and it is
    also what makes two of them side by side (the assembler mirrors alternate
    bays) read as an arcade rather than as a row of leaning sticks.
    Two of these stack to a full 2.60 m storey with a double plate at 1.300.
    """
    p = _bay(_reserve(Part("SM_Wall_TimberKnee_2m", budget="wall",
                           seams=_seams(h=H_KNEE))), h=H_KNEE)
    r = rng("timber/knee")
    f0, f1 = KZ_FIELD
    _core(p)
    # the post peg goes to mid-field: its usual home is where the transom tenons
    # in and there is no transom, and the head plate is prouder than the post so
    # a peg up there would be driven into the back of it. (f0 + f1)/2 also keeps
    # it clear of the brace's own two joint pegs at 0.190 and 1.000.
    _posts(p, z1=KZ_POST_TOP, peg_z=(f0 + f1) / 2)
    _rails(p, r, transom=False, attic=False, z_head=KZ_HEAD)
    _panel(p, -XE, XE, f0, f1, r)
    _brace_arc(p, r, -1, -XE, XE, f0, f1)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_band():
    """SM_Wall_TimberBand_2m -- a 0.400 m PLINTH COURSE. HG - H, exactly.

    The other way to fill a 3.00 m storey with 2.60 m of authored wall, and it
    goes UNDERNEATH rather than on top. That is measured, not preferred: the wall
    plate is the member that carries the floor above and it has to be AT the
    storey head, so [2.60 wall][0.40 band] leaves the plate 0.40 m short of the
    head and the storey with no head at all, while [0.40 band][2.60 wall] puts it
    at 2.820..3.000 -- the same place TZ_HEAD puts it on the authored tall bay.

    So what it is, is the dwarf wall a frame stands on: the two seam posts
    running down to the ground, ONE rail at the top in the sole plate's own
    section and keyed "sole" (so it is the same stick of oak as the plate the
    wall above lands on it, and the pair reads as the 0.190 m sill beam a frame
    is bedded on), and plaster between. Its bottom face is flat at z = 0 for the
    foundation, the stone storey or the jetty beam under it.

    THE PANEL'S GROWN RIM IS THE ONE NUMBER THAT NEEDED CARE. `_panel` grows
    0.014 past its rectangle on all four sides and z = 0 is a declared seam that
    `check()` allows only 1 mm of slack on, so the field starts at 0.016 and the
    rim lands on 0.002. `_wob` fades to nothing that close to a seam, so it
    cannot be pushed back out; the 2 mm of core face that leaves reads as the
    bedding joint onto whatever the band stands on.
    """
    p = _bay(_reserve(Part("SM_Wall_TimberBand_2m", budget="wall",
                           seams=_seams(h=H_BAND))), h=H_BAND)
    r = rng("timber/band")
    _core(p)
    _posts(p, z0=0.0, z1=BZ_POST_TOP, peg_z=BZ_HEAD[0] - .050)
    # the head rail: the sole plate's section and the sole plate's keyed tone,
    # but arrised and bowed as a PLATE -- its top face is the z = 0.400 seam, so
    # the chamfer there is the wall plate's 0.35 and the sin^2 bow is taken
    # entirely on the soffit. Same reason Z_HEAD passes bow=(.005, 0.0).
    _shared(p, "sole", -G / 2, G / 2, BZ_HEAD[0], BZ_HEAD[1],
            mat=OAK, y=BY, d=BD, seg=2, tint=.055,
            cham=CHAM, arris=(1.0, .35), bow=(.004, 0.0), facets=2)
    _panel(p, -XE, XE, BZ_FIELD[0], BZ_FIELD[1], r)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def _plate_band(name, h, z_field, z_head, head_d=None, studs=2, seed="band"):
    """ONE PLATE BAND -- the low attic course between a storey head and the roof.

    Placed at z + HU, i.e. straight onto the storey's own wall plate, so it has
    NO sole plate of its own: the plate below is this course's sill and a second
    one would put 0.275 m of unbroken timber at the junction. It gets the
    family's sole BEAD instead, which terminates it on z = 0 and gives the
    panels' grown rim something to tuck under, for a fifth of a plate's height.

    Above that it is the family's FRIEZE verbatim -- `_rails(attic=...)`, the
    same W_THIN studs at the same spacing and the same pillowed panels -- and
    then one head member. Both callers are in THE PLATE BAND, AND THE HOLE IT
    CLOSES, above the constants, with the measurement that sets `z_head` on each.
    """
    p = _bay(_reserve(Part(name, budget="wall", seams=_seams(h=h))), h=h)
    r = rng("timber/" + seed)
    _core(p)
    # posts from the seam up into the head member, and their feet are behind the
    # bead (BEAD_Y is 6 mm prouder than POST_Y) exactly as they are on a full bay
    _posts(p, z0=0.0, z1=z_head[0] + .015,
           peg_z=(z_field[0] + z_field[1]) / 2)
    _shared(p, "sole_bead", -G / 2, G / 2, BAND_BEAD[0], BAND_BEAD[1],
            pale=.52, y=BEAD_Y, d=.056, seg=1, tint=.07,
            cham=CHAM_BEAD, arris=(.5, 1.0), stop=.09, facets=0, mids=1)
    _rails(p, r, sole=False, transom=False, head=True, attic=True, studs=studs,
           z_head=z_head, z_attic=z_field)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def band_eave():
    """SM_Wall_TimberBandEave_2m -- 2.000 x 0.850, the EAVE-face plate band.

    0.850 is not a round number by choice: it is assemble_inn's own
    `band_h - BAND_TUCK` = 1.00 - 0.15 for the hero's top storey, and until this
    piece existed that value fell through a `> 0.95` gate and the band was
    silently skipped on all three eave faces -- a measured 0.70 m open slot along
    the hero's west flank, 56-69% see-through from the street. See THE PLATE
    BAND, AND THE HOLE IT CLOSES.

    Nothing is placed over an eave band (assemble_inn's sill beam goes on the
    proud gable faces only), so it takes the family's standard 0.180 m wall plate
    at its head and the eave course bears on that. Field 0.618 x 1.840 with two
    frieze studs -- three panels of 0.543 x 0.618, which is the same close-studded
    band the family already carries at Z_ATTIC, one storey higher up.
    """
    return _plate_band("SM_Wall_TimberBandEave_2m", BAND_EAVE_H,
                       EZ_FIELD, EZ_HEAD, seed="band_eave")


def band_gable():
    """SM_Wall_TimberBandGable_2m -- 2.000 x 1.000, the GABLE-face plate band.

    The "proud" band: fully exposed, the gable sits on it, and assemble_inn lands
    SM_Beam_JettySill_2m_C on top of it as the projecting sill course ref3 draws
    under every gable.

    ITS HEAD MEMBER IS A BRESSUMER, 0.421 m from 0.579 to 1.000, and 0.579 is
    measured off that beam rather than chosen: the beam's housing block is a
    full-bay-width solid whose BACK is one flat 0.826 m2 quad on y = +0.050, and
    it occupies band-local z 0.579 .. 0.992. PANEL_BACK -- where every pillowed
    panel in this family puts its own flat back -- is y = +0.052, two millimetres
    away. Stopping the field at 0.579 keeps every panel out of it (their back
    grid tops out at 0.573) and makes the head member the thing the beam is
    HOUSED INTO, which is what a bressumer is. Field 0.527 x 1.840 with two
    studs: three panels of 0.543 x 0.527, the squarest in the family.
    """
    return _plate_band("SM_Wall_TimberBandGable_2m", BAND_GABLE_H,
                       GZ_FIELD, GZ_HEAD, seed="band_gable")


# ------------------------------------------------------------------ jetty ----
def _jetty_base(p, r):
    """Bressumer + boarded soffit over the overhang. z=0 is the upper floor.

    The soffit board run is laid out so the gap between boards falls EXACTLY on
    the bay seam: it used to start 5 mm in from each end, which left a 22 mm gap
    at the join against 12 mm between its own boards, so the one place the
    soffit's rhythm broke was the one place it should not.
    """
    rr = rng("timber/soffit/" + p.name)
    n, y0, y1, gap = 9, -.02, T + J, .012
    w = G / n
    for i in range(n):
        a = -G / 2 + w * i + gap / 2
        b = a + w - gap
        m = _oak(rr, .70)
        sh = 1.0 + rr.uniform(-.10, .06)
        p.box(((a + b) / 2, (y0 + y1) / 2, .030), (b - a, y1 - y0, .060), m,
              bevel=.010, seg=1, tint=.05, shade=sh)
        _pnt(p, m, .05, sh)
    # the bressumer: the heavy beam the storey above sits on. Its foot is buried
    # in the soffit boards and its top bead overlaps it by 18 mm -- the two used
    # to butt on z = 0.318 and fight over 1257 cm2. Keyed tone on all three: they
    # run the length of a jettied facade, and the bressumer is the boldest band
    # in the whole family, so a tonal step in it at every bay was the loudest of
    # them all.
    # the boldest band in the family, so it gets the fullest working: a wide
    # stop-chamfer on both arrises, three adze facets down its face and a 6 mm
    # sag between the bays it spans. Same numbers the beams family's bressummer
    # uses, so the two agree where they meet -- they are the same timber.
    _shared(p, "bressumer", -G / 2, G / 2, .044, .318, mat=OAK, y=BRESS_Y, d=.185, seg=2,
            tint=.055, cham=CHAM * 1.15, stop=.115, bow=(.006, .006), facets=3,
            mids=3)
    # ROUND 12 -- THE THIRD MEASURED Z-FIGHT, and it was 3 mm wide. This bead
    # stood at BRESS_Y + 0.023 and was 0.060 deep, so its BACK landed on
    # y = -0.017 while the soffit boards it crosses have their front end grain on
    # y = -0.020: two parallel oak_mid faces 3 mm apart, overlapping wherever a
    # board passes behind the bead, and `_wob` closed the gap at the -X seam
    # (18 cm2 at [-0.889, -0.02, 0.03]). A bead is a bead ON something -- it has
    # to lap what it covers, the way the bressumer above it already laps these
    # same boards by 105 mm -- so it is 0.095 deep now and its back sits 38 mm
    # INSIDE the soffit, a proper lap rather than two faces kissing. Its own
    # face, its chamfer and everything visible are untouched: only the hidden
    # back plane moved, and it moved a real distance.
    _shared(p, "bress_low", -G / 2, G / 2, .026, .074, pale=.58, y=BRESS_Y + .023,
            d=.095, seg=1, tint=.07, cham=CHAM_BEAD, stop=.09, facets=0,
            mids=1)
    # top bead at PLATE_Y, so the jetty half-post's FOOT is buried behind it the
    # same way the wall plate buries its head
    _shared(p, "bress_top", -G / 2, G / 2, .300, .366, pale=.58, y=PLATE_Y,
            d=.128, seg=1, tint=.07)
    # These three used to sit on the FY plane, which is 55 mm INSIDE a bressumer
    # standing at -0.135: three invisible cylinders. Driven into its face
    # instead, flush-ish -- 0.135 + wobble leaves only ~13 mm of PROUD_MAX and a
    # flush-driven peg in a heavy beam is what the reference shows anyway.
    for x in (-.60, 0.0, .60):
        _peg(p, x, .185, face=BRESS_Y, stand=.008, r_=.032)


def _jetty_shell(p, r, apron_top, studs=1, transom=True, attic=True,
                 boarded=True):
    """The jettied storey's frame. `boarded` decides what fills the apron
    between the bressumer and the sill rail.

    ROUND 11 GIVES IT A CHOICE, because a run of jettied bays was the darkest
    thing the kit could build: boarded aprons put jetty_a at 58% timber and
    jetty_b at 95%. ref2's jetty carries a boarded apron under its windows and
    that detail stays -- on jetty_b, the signature bay, and on wall_c. jetty_a
    is the PLAIN jettied bay and takes a plaster apron instead, exactly as
    SM_Wall_TimberWin_2m did in round 10 and for the same reason: on a wall the
    reference carries the cream straight down to the rail below, and a facade
    is mostly plain bays.
    """
    _posts(p, z0=.346)
    _rails(p, r, sole=False, studs=studs, transom=transom, attic=attic)
    _jetty_base(p, r)
    if boarded:
        # seeded per PIECE, not per family: both jetty variants shared the seed
        # "timber/apron", so every jettied bay in a run carried the identical
        # sequence of board tones -- a 2 m repeat, and the most pattern-like
        # thing left in the family once the seam was gone
        _boards(p, -XE, XE, .346, apron_top + .026, 8,
                "timber/apron/" + p.name)
    else:
        _panel(p, -XE, XE, .372, apron_top, r, tint=.06)
    _shared(p, "apron", -G / 2, G / 2, apron_top, apron_top + SILL_H,
            mat=OAK, pale=.14, y=BY, d=BD, seg=2, tint=.055, cham=CHAM,
            stop=.185, bow=(.004, .004), facets=2)


def jetty_a():
    """Plain jettied bay: CREAM apron, one big panel, and a SHALLOW arch brace
    over it -- 1.76 m of run against 1.05 m of rise, which is the best-looking
    arch in the family. Foot in the apron rail against the left post, head in
    the right post, crown lapped into the transom.

    ROUND 11: the apron is plaster rather than boarding (see `_jetty_shell`).
    That is what takes this piece from 58% timber to a bay that can carry a
    facade -- and it is what the assembler wanted when it dropped `j` from the
    bay specs. jetty_b keeps the boarded apron, so ref2's detail is still in the
    family and a level artist can still build a boarded jettied run."""
    p = _reserve(Part("SM_Wall_TimberJetty_2m_A", budget="wall", seams=SEAMS_J))
    r = rng("timber/JA")
    at = APRON_TOP          # shared with jetty_b: it used to be 0.78 by eye,
    _core(p, z_top=H, z0=.030)   # 20 mm below its neighbour's, and stepped
    _jetty_shell(p, r, at, boarded=False)
    f0, f1 = at + SILL_H, Z_TRAN[0]
    _panel(p, -XE, XE, f0, f1, r, tint=.06)
    _brace_arc(p, r, -1, -XE, XE, f0, f1)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def jetty_b():
    """The signature ref2 bay: jetty, boarded apron, and the wide window sitting
    straight on the apron rail -- that rail's top face IS the opening's sill, so
    the two pieces of the bay share one line. Same win_upper rules as
    SM_Wall_TimberWin_2m: no rail crosses the hole, jambs beside it, the wall
    plate over it."""
    p = _reserve(Part("SM_Wall_TimberJetty_2m_B", budget="wall", seams=SEAMS_J))
    r = rng("timber/JB")
    ow, oh, sz = OPEN["w"], OPEN["h"], OPEN["sill"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, sz, sz + oh
    _core(p, holes=[(hx0, hx1, hz0, hz1)], z_top=H, z0=.030)
    _jetty_shell(p, r, APRON_TOP, transom=False, attic=False)
    _reveal(p, hx0, hx1, hz0, hz1, r)
    _mem(p, hx0 - .095, hx1 + .095, hz0 - CILL_DROP - CILL_H, hz0 - CILL_DROP,
         _oak(r, .58),
         y=BY - .030, d=.124, seg=2, tint=.07, cham=CHAM_BEAD * 1.6,
         stop=.10, facets=0, mids=1, seed="nose")
    _jamb(p, r, hx0, hx1, hz0, hz1)
    for sx in (-1, 1):
        _peg(p, sx * (XE - .12), hz0 - .34, face=BOARD_Y, r_=.026)
        _peg(p, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.020)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


# ------------------------------------------------------------------ gable ----
ZA = (G / 2) * tan(S.PITCH)      # 1.2799, apex of a one-bay gable
G_DZ = G_RAKE / cos(S.PITCH)     # 0.1137, vertical thickness of a rake timber
G_SOFFIT = ZA - G_DZ             # 1.1662, where the two rake soffits MEET

# ===================== THE TWO RAKES BUTTED ON x = 0  (round 16) =============
# MEASURED, and it is the family's ONLY z-fight at the 0.5 mm pass: 68 cm2 on
# SM_Wall_TimberGable_2m_Rough at [0.000, -0.020, 1.226], oak_dark against
# oak_dark. Both rake timbers were drawn with their inner edge on the literal
# x = 0.0 -- pts [(fx, fz), (0.0, ZA), (0.0, sj), (xb, zs)] -- so each one stood
# a 0.11 x 0.12 m face on that plane and the two were EXACTLY coplanar, facing
# away from each other. (Probed: polygons 40 and 66, normals (0.9999, 0, -0.011)
# and (-0.9999, 0, +0.012), centres 0.4 mm apart.)
# THE MACHINED GABLE GOT AWAY WITH IT BY ACCIDENT and that is worth recording:
# there the two faces are not merely coplanar but IDENTICAL, so
# Part.finish()'s weld deletes one of them as a duplicate and a probe finds a
# single face (polygon 37) where there should be two. The rough gable jitters
# each rake's inner z and depth independently, so its pair survives the weld and
# fights. Depending on a weld to hide a pair of coincident faces is not a fix; it
# is the same pair, one build away from coming back.
# THE FIX IS THE JOINT THE MEMBERS ACTUALLY WANT. Two rake timbers at an apex are
# lapped past each other, not butted: the inner edge's LOWER vertex moves
# G_RAKE_LAP across the centre line while the APEX VERTEX STAYS ON x = 0 (it is
# the piece's snap point -- the gables family's finial and bargeboard land there
# and it may not move). So each inner face becomes a plane tilted
# atan(G_RAKE_LAP / (ZA - soffit)) = 7.0 deg off vertical, the two tilt OPPOSITE
# WAYS, and the pair is 14 deg apart: dot = 0.970, i.e. outside check_zfight's
# own 0.99 "roughly coplanar" test, and 13.9 mm apart on the true local
# separation measure. Nothing is buried to make the number go away -- the faces
# were interior before and after, and what changed is that they are no longer
# one plane. It also closes the apex V by 28 mm of overlap instead of leaving
# two faces kissing, which is the notch `_king_head` was written to cover.
# Applied to BOTH gables, because the numbers in this section exist precisely
# because `gable` and `gable_rough` had drifted apart once already.
G_RAKE_LAP = 0.014

# ===================== THE KING POST DID NOT REACH THE APEX  (round 14) ======
# MEASURED, before: on the centre line of SM_Wall_TimberGable_2m the king post's
# head stopped at z = 1.0845 and the two rake soffits meet at z = 1.1662, so
# 81.4 mm of the wall's centre line -- 87.0 mm on the _Rough sibling -- came back
# CREAM to a head-on ray. The whole point of the piece is a king post carrying
# the apex under a pair of arched braces, and it was floating a hand's width
# short of the thing it is holding up, with plaster showing through the joint.
# It was arithmetic, not intent: the head was cut to `soffit(w_kp) - 0.012`,
# i.e. to the rake soffit measured at the post's own SIDE (x = 0.058, z = 1.0920)
# and then 12 mm below that -- but the rakes rise as they go in, so the soffit at
# the post's CENTRE is 74 mm higher again. A rectangular post cut square meets
# the V of the two rakes at their meeting point, not at its own edge.
# The head now lands on G_SOFFIT + KP_SEAT, so its top face is buried inside both
# rakes: at x = 0 it is KP_SEAT above the soffit, at the post's edge it is 82 mm
# above it, and it is still 19 mm (perpendicular) below the rake's own upper
# face, which is the plane the bargeboard lands on and the one surface here that
# must not be broken. The post is also 20 mm DEEPER, so its back face passes
# clean through both rakes instead of stopping 1 mm inside the nearer one's back.
KP_SEAT = 0.008     # how far the king post's head is buried past the soffit
KP_DEEP = 0.020     # ... and how far its back passes through the rakes

# ===================== THE LOZENGE WAS INSIDE THE POST  (round 14) ===========
# MEASURED, before: the gable's lozenge is 199 x 199 mm across the diagonal and
# stood on x = 0 with its front face on y = -0.050 -- 2 mm BEHIND the king post's
# own bellied face, and centred on a post only 116 mm wide. 742 of its 1130 cm3
# (65.6%) was inside the post; all that reached the eye was a 40 mm triangular
# ear each side, and those read as a lump on the post rather than as a diamond.
# There is no depth fix. Standing it proud of the post face is a decal floating
# 30 mm off the plaster; shrinking it to fit inside a 116 mm post makes it a
# 100 mm bead. So it MOVES, to where ref3 actually sets the motif -- into a
# panel. The gable has two: the spandrels under the twin arch braces, which are
# the biggest areas of cream in the piece, and a diamond in each makes the pair
# of arches read as an arcade instead of as two loose curves.
# The placement is bounded on three sides and every clearance is measured:
# 128 mm from the king post's face, 149 mm above the sole bead, and its farthest
# corner is 380 mm from the braces' arc centre against an inner radius of 476,
# i.e. 96 mm of air even before the rough sibling's swell and jitter (worst case
# 54 mm). Nothing here is near a tiling plane.
G_LOZ_X = 0.220     # centre of each spandrel lozenge
G_LOZ_Z = 0.260
G_LOZ_S = 0.130     # box side; the diamond measures 184 mm across the flats

KP_HEAD_Y = FY + .006       # the king post's HEAD, 6 mm behind the post's face
KP_HEAD_D = FD + KP_DEEP - .012


def _king_head(p, w_kp, z_base, z_apex, mat, tint=.06, shade=1.0):
    """THE KING POST'S HEAD, cut to the pitch of the two rakes it lands between.

    A square-topped post seated in the apex still leaves the last of the centre
    line to the two rakes, and they meet there as a KNIFE EDGE -- each one's
    inner face is on x = 0, so the 16 mm bevel on that arris cuts both of them
    back off the centre line and the pair opens a notch. Measured on the built
    mesh after the head was seated: a 6 mm sliver of cream at z = 1.178 and a
    15 mm one at the apex point itself, both of them exactly on x = 0.
    A triangular head closes both, and it is the shape the member wants anyway:
    it rises far steeper than the rake line (2.48 against 1.28 per unit x), so it
    stays inside both rakes everywhere except at the apex point, where all three
    converge -- which is the joint. It sits 6 mm BEHIND the post's face so it
    does not share that face's plane, and its own front and back are buried
    inside the post over the 38 mm they overlap.

    ROUND 15 -- THE TIP IS NOT CHAMFERED, AND THAT IS THE WHOLE OF THE APEX
    RESIDUAL. Round 14 closed 81 mm of cream up the centre line, left 9.0 mm of
    it at the apex POINT, and blamed it on "three chamfered timbers converging".
    It was ONE chamfer and it was this one. The head's apex has a 44-degree
    included angle (it rises 2.478 per unit x), and bmesh.ops.bevel offsets each
    adjacent face by `offset` measured ALONG THAT FACE from the edge -- so a
    10 mm chamfer on a 22-degree half-angle tip cuts the tip back by
    0.010 * cos(22) = 9.3 mm of Z. Measured on the built mesh, both gables:
    cream on x = 0 from z = 1.2708 to ZA = 1.2799 -- 9.4 mm at the probe's own
    0.2 mm step -- and 100% of it LIT at the kit sun, i.e. the brightest
    material in the kit seen end-on at the darkest point of the piece, which is
    why 9 mm read at all.
    So the tip is square-arrised: bevel 0.010 -> 0. It costs nothing. Every
    millimetre of this triangle except the last 46 mm is buried inside the king
    post or the two rakes, so the chamfer was invisible everywhere it was not
    doing harm; no other vertex moves; and the member now lands exactly on
    z = ZA, which is this piece's snap plane and the plane the gables family's
    finial and bargeboards sit on. It cannot break that plane either: the head
    rises 2.478 per unit x against the rake line's 1.280, so it is strictly
    UNDER both rakes' upper faces everywhere except at x = 0, where all three
    are the same point. The gables family's finial lands on that point.
    """
    fs = p.prism([(-w_kp, z_base), (w_kp, z_base), (0.0, z_apex)],
                 KP_HEAD_D, mat, axis='Y',
                 at=(0, KP_HEAD_Y + KP_HEAD_D / 2, 0), bevel=0.0, seg=1,
                 tint=tint, shade=shade)
    _pnt(p, mat, tint, shade)
    return fs


def gable():
    """Gable-end infill: a CREAM triangle framed the way ref3 frames its big
    gable -- a king post from the sole plate to the apex with a broad curved
    brace either side of it, springing off the plate and landing on the post, so
    the two together read as one arch under the apex.

    A 2 m bay at 52 deg leaves only 1.28 m to the apex, which makes this the one
    piece where fat members can EAT the whole panel: the first pass filled it
    with vertical boarding and the second, at reference sections, came out a
    solid brown plaque with no infill visible at all. So the boarding is gone --
    the infill here is one proud plaster triangle at the same relief as a wall
    panel (one prism, no extra cost) -- and the gable's own members are the one
    place in the family that stay slim, because they are already spanning a
    third of the height they would on a wall.

    Both braces are now SEATED: 45 mm of the springing is inside the sole plate
    and each head is 35 mm inside the king post, where they used to stop dead on
    the plate's top face and the post's side face -- kissing, not jointed.

    Bargeboard and tooth trim lap the rakes from the gables/roof family."""
    p = _reserve(Part("SM_Wall_TimberGable_2m", budget="wall",
                      seams=dict(x=(-G / 2, G / 2), y=(0, T), z=(0, ZA))))
    r = rng("timber/GA")
    # ROUND 10. This triangle is only 1.28 m tall, so it is the piece where the
    # ratio is worst: measured head-on it was 78% timber against 22% cream, i.e.
    # a brown plaque with a sliver of infill -- the exact failure the second pass
    # recorded and only half-fixed. Rake 0.135 -> 0.098, sole plate 0.160 ->
    # 0.125, king post 0.220 -> 0.152, brace 0.170 -> 0.112, arc radius 0.62 ->
    # 0.56. Same members, same joints, same twin-arch reading under the apex; the
    # cream triangle they sit on is now the thing you see first.
    #
    # ROUND 11 took the same set again -- rake 0.076, sole G_SOLE (the wall's own
    # sole plate height, so a gable sitting on a wall run continues its band),
    # king post 0.116, brace 0.084 -- and HOISTED THEM to G_SOLE/G_RAKE/G_KING/
    # G_ARC_*, because `gable_rough` carried its own copy of all five numbers and
    # that is how the two halves of a piece drift apart. The arc geometry is
    # unchanged: the braces still spring off the sole plate at 180/0 deg and
    # still arrive vertical at x = +-(G_KING - 0.035), i.e. inside the king post.
    zs = G_SOLE                         # top of the sole plate
    w_rake = G_RAKE
    dz = w_rake / cos(S.PITCH)          # 0.123 vertical thickness of a rake
    soffit = lambda x: ZA * (1.0 - abs(x)) - dz
    # --- plaster core: the triangle itself, ONE solid with a painted inner face
    # shade 0.96, not 0.92. THE BRIEF'S FOURTH LEVER -- "the panel itself must
    # stay bright: check nothing is tinting the plaster down". Round 10 cleaned
    # `_panel` and missed the gable, which builds its cream out of two prisms
    # rather than a panel, at 0.92 and 0.98. On the piece with the worst ratio in
    # the family, the cream was also the only cream in the family below palette
    # strength. Both are at full tone now.
    fs = p.prism([(-G / 2, 0.0), (G / 2, 0.0), (0.0, ZA)], T - CORE_Y, "plaster",
                 axis='Y', at=(0, (CORE_Y + T) / 2, 0), bevel=0, tint=.04,
                 shade=.96)
    _pnt(p, "plaster", .04, .96)
    inner = [f for f in fs if f.calc_center_median().y > T - 1e-3]
    if inner:
        p._paint(inner, "plaster_dim", .05, .90)
    # --- the proud infill: cream, standing to the same plane a wall panel does
    # deep enough that its BACK is buried inside the core rather than stopping
    # in mid-air: with the rim now on y = 0 a shallow infill would leave a 74 mm
    # cavity behind the cream triangle, open at the rake edge where the rakes'
    # own backs stop at 0.041. Burying it 10 mm into the core closes that and
    # shares no plane with anything.
    p.prism([(-G / 2 + .018, .018), (G / 2 - .018, .018), (0.0, ZA - .040)],
            CORE_Y + .010 - G_INFILL_Y, "plaster", axis='Y',
            at=(0, (G_INFILL_Y + CORE_Y + .010) / 2, 0),
            bevel=0, tint=.05, shade=1.0)
    _pnt(p, "plaster", .05, 1.0)
    # --- rake timbers, clipped where they run into the sole plate
    for sx in (-1, 1):
        xa = sx * (1.0 - zs / ZA)
        xb = sx * (1.0 - (zs + dz) / ZA)
        # the inner edge LAPS past the centre line ALONG THE SOFFIT LINE -- see
        # THE TWO RAKES BUTTED ON x = 0. The apex vertex does not move, and
        # neither does the soffit: extending the soffit's own line rather than
        # sliding its top end sideways is what keeps the rake exactly G_RAKE
        # wide everywhere.
        s_ = G_RAKE_LAP / abs(xb)
        pts = [(xa, zs), (0.0, ZA),
               (-sx * G_RAKE_LAP, (ZA - dz) + ((ZA - dz) - zs) * s_),
               (xb, zs)]
        m = _oak(r, .12)
        sh = _sh(r, .07)
        p.prism(pts if sx > 0 else pts[::-1], FD + .034, m, axis='Y',
                at=(0, FY + FD / 2 - .016, 0), bevel=.016, seg=1, tint=.06,
                shade=sh)
        _pnt(p, m, .06, sh)
    # --- sole plate (the wall plate the rakes land on) + its bead. Keyed to the
    # same tone the wall pieces use, and cut flat at x = +-G/2 like theirs, so a
    # pair of gable infills reads as one plate across the join.
    _shared(p, "sole", -G / 2, G / 2, 0.0, zs, mat=OAK, y=BY, d=BD, seg=2,
            tint=.055)
    _shared(p, "sole_bead", -G / 2, G / 2, zs - .030, zs + .016, pale=.52,
            y=BEAD_Y, d=.054, seg=1, tint=.07)
    # --- king post + the twin curved braces that make the apex read as arched
    # THE HEAD LANDS IN THE APEX. See THE KING POST DID NOT REACH THE APEX: the
    # top is cut to where the two rake SOFFITS MEET (G_SOFFIT, on the centre
    # line) rather than to the soffit measured out at the post's own side, which
    # left 81 mm of cream showing straight up the middle of the piece.
    w_kp = G_KING                       # half-width: a 0.116 post
    m_kp, sh_kp = _oak(r, .12), _sh(r, .07)
    _mem(p, -w_kp, w_kp, zs - .02, G_SOFFIT + KP_SEAT, m_kp,
         d=FD + KP_DEEP, seg=2,
         tint=.06, shade=sh_kp, cham=CHAM * .55, stop=.10, facets=2,
         mids=2, belly=.004, seed="king")
    _king_head(p, w_kp, G_SOFFIT - .030, ZA, m_kp, shade=sh_kp)
    ro, wb = G_ARC_R, G_ARC_W
    for sx in (-1, 1):
        _arc(p, sx * (w_kp - .035), zs - .045, ro - wb, ro,
             180.0 if sx < 0 else 0.0, 90.0, _oak(r, .16), n=10,
             shade=_sh(r, .07), d=FD - .016)
        _peg(p, sx * (w_kp + ro - .12), zs + .10)
        # THE LOZENGE IS IN THE PLASTER NOW, one in each spandrel under the
        # arch, which is where ref3 sets the motif -- into a PANEL. See THE
        # LOZENGE WAS INSIDE THE POST.
        _lozenge(p, r, sx * G_LOZ_X, G_LOZ_Z, G_LOZ_S)
    # ONE PEG WHERE THE TWO BRACE HEADS LAND, not one per side, and this is a
    # measured fault rather than a tidy-up. The landing peg used to be drawn
    # inside the `sx` loop at x = +-(G_KING - 0.05), and G_KING is a HALF width:
    # 0.058, so the two pegs sat 16 mm apart on a post 116 mm wide and their
    # 60 mm heads overlapped. Ray-measured on the built piece, the pair of head
    # faces at y = -0.088 was 14.5 cm2 of coincident surface, 100% reachable and
    # 100% face-on -- the only fully visible z-fight in the family, and on the
    # proudest, palest thing on the wall, where a shimmer would be unmissable.
    # Two 60 mm pegs cannot sit side by side in a 116 mm post anyway; a brace
    # pair landing on a king post is pinned by ONE peg driven through it, which
    # is both the carpentry and 20 fewer tris. The springing peg each side is
    # untouched -- those are 1.0 m apart.
    _peg(p, 0.0, zs + ro - .13)
    _peg(p, 0.0, soffit(w_kp) - .11)
    # only 1.28 m of z here, so the seam fade gets 0.22 rather than the walls'
    # 0.28 -- enough to flatten the plate zone without ironing out the apex
    _wob(p, (.0075, 1.3), (.0035, 3.4), margin=.22)
    return _done(p)


# =============================================================================
# ============ THE ROUGH HALF OF THE FAMILY -- the "_Rough" siblings ===========
# =============================================================================
# "Similarly the wood on the walls and doors is too regular, let's add more
# irregular versions as well (but keep the regular ones as options just in case)."
#
# So this is ADDITIVE. Every piece above keeps its name and its mesh, byte for
# byte, and each one gains a hand-hewn sibling with _Rough on the end. A level
# artist mixes them: mostly rough on an old wing, mostly regular on a newer one,
# and both in the same run when they want the wall to look patched.
#
# ROUND 19 -- THE NINE FRACTIONAL BAYS DO NOT HAVE ROUGH SIBLINGS, and that is a
# decision, not an oversight, so here is the reasoning and the number behind it.
#   * WHAT IT WOULD COST. The rough machinery is a second set of functions with
#     the same numbers spelled into them -- `_scarf` builds its two stubs at
#     -G/2 and +G/2, `_frieze_rough` and `_rails_rough` take XE and Z_TRAN/
#     Z_HEAD directly -- so a rough half bay is not "one more call", it is the
#     same parameterisation done again over four more functions, and nine more
#     pieces on top of that.
#   * WHAT IT WOULD BUY, measured: `grep -c _Rough assemble_inn.py` is 0 and
#     `grep -c _Rough assemble_layouts.py` is 0. Neither assembler places a
#     single rough piece today; the sixteen regular pieces are what the building
#     is made of, and the fractional bays exist to fix a defect in that building.
#   * WHAT IT COSTS TO SKIP: a run that is rough throughout cannot be closed with
#     a fractional bay in the same hand. A rough bay and a regular bay already
#     stand next to each other by design -- that is what the keyed tones and the
#     flat seam sections are for, and the section measurement above puts a
#     fractional bay against SM_Wall_Timber_2m_A_Rough in the same 0.4-0.7 % band
#     as against the machined one -- so the join works; it is the CHARACTER that
#     is inconsistent, not the geometry.
# If the rough siblings are wanted, the parameterisation to repeat is exactly the
# one `_rails` took: bands' z as arguments, x off `_bw(p)`, XE off `_xe(p)`.
#
# WHAT MAKES A PIECE ROUGH HERE IS FORM, NEVER COLOUR -- the .blend is inspected
# in Solid shading, where one material draws one flat tone and vertex-colour
# variation is invisible:
#   `_hewn`         replaces the beveled box for every member free to move: a
#                   SWEPT section, so one primitive can wander sideways, bow out
#                   of plane, taper along its length, carry a waney (non-
#                   rectangular) face and be twisted out of square;
#   `_scarf`        breaks a shared band into three timbers lapped together --
#                   which is how a long wall plate was actually built, nobody
#                   having a straight 14 m oak -- so the band shows a real step
#                   and a pegged joint a third of the way along the bay;
#   `_panel(rough=)` floats the plaster by hand: neighbouring panels sit at
#                   different depths, the crown bellies further, the surface is
#                   lumpy instead of a perfect sine dome;
#   `_boards_rough` saws boarding to uneven widths with uneven gaps, bows and
#                   tapers every board, throws a few out of plumb and lets the
#                   butt line wander;
#   `_peg_r`        drives pegs by eye: they wander, they tilt, they are not all
#                   the same size, and there are more of them -- every scarf and
#                   every lap gets one, which is the joint detail that says
#                   "pegged carpentry" rather than "extruded boxes".
#
# WHAT MAY NOT MOVE, AND WHY. A rough bay must stand next to a regular one with
# no step, and assemble_inn.py MIRRORS these pieces in X for the second half of a
# run. So the rough half obeys the same seam discipline as the regular half:
#
#   * THE SEAM HALF-POSTS ARE THE SAME `_posts()` CALL. Same keyed tone, same
#     dead-flat seam face, same profile, so the two halves that add up to one
#     post still make one post whichever variant -- and whichever handing -- is
#     on either side of the join.
#   * EVERY RAIL KEEPS ITS EXACT BAND, whatever those bands currently are: both
#     halves read Z_SOLE / Z_TRAN / Z_HEAD and the APRON_TOP..SILL_TOP sill line
#     from the same constants, and the openings come off spec.OPENINGS. Only the MIDDLE of a band is hewn; the last 30 mm at each end is
#     the regular `_mem` stub, chamfer collapsed onto the tiling plane by `_cut`.
#     A hewn member taken all the way to the seam would arrive with a sharp
#     arris against its neighbour's 18 mm chamfer, i.e. a one-sided groove down
#     the join -- the exact defect the fourth pass measured away.
#   * A BAND THAT TOUCHES A Z SEAM IS NOT SCARFED AT ALL. The sole plate lands on
#     z = 0 and the wall plate on z = H, and a scarf's middle timber is deliberately
#     taller than its band; taller at z = 0 is out of bounds, and cut flush it
#     would lay two coplanar faces on the storey plane. The sole plate shows its
#     scarf in the BEAD instead, and the wall plate stays one timber, which is
#     what a wall plate honestly is.
#   * THE WOBBLE AMPLITUDE IS UNCHANGED. Turning it up is the obvious move and it
#     is wrong: wobble fades to zero at a tiling plane, so a bigger amplitude
#     leaves a steeper gradient just inside the join than the bay opposite has --
#     a shading crease down the middle of a shared post. Roughness here is
#     geometry, which can be kept away from the seam exactly.
#   * OPENINGS ARE UNTOUCHED. spec.OPENINGS["win_upper"] to the millimetre, so
#     the windows family's casement drops into the rough bay as well.
#   * NOTHING IS HANDED. Wander, bow, roll and taper are symmetric noise; there
#     is no lettering and no one-way detail, so a mirrored rough bay reads the
#     same as an unmirrored one.


def _hewn(p, a, b, w, d, mat, seed=0, y=FY, k=4, bow=0.0, wave=0.0, taper=1.0,
          wane=0.10, roll=0.0, dj=0.05, tint=.06, shade=1.0, pin=0.0,
          anchor=0.0, wane_side=None, djd=1.0):
    """ONE HAND-HEWN TIMBER, from (x, z) to (x, z): swept, not extruded.

    `Part.box` can give a member a taper and a skew and nothing else, and that is
    not how a riven timber behaves. This walks `k + 1` sections along the
    member's own axis and lets every one of them differ, so for 8k + 4 tris in a
    single primitive a member gets:

      wave    lateral wander in the wall plane -- its arris is not a straight
              line, which is the first thing the eye reads in the reference
      bow     out-of-plane bend, deepest at mid-span. Part.bow() does this to a
              whole part; here it belongs to the one member
      taper   the far end is narrower, the way a stick cut from a tree is
      wane    the FRONT face is narrower than the back, by a different amount at
              every station: the section is a trapezoid that changes shape along
              the length, i.e. "not perfectly rectangular in section"
      roll    front face shifted sideways against the back -- twisted out of square
      dj      per-station jitter of width and depth
      pin     1.0 fades every deviation to nothing at BOTH ends, for a member
              whose ends must land exactly; 0.0 lets the ends move too
      anchor  -1/+1 holds ONE arris straight while the other wanders. A window
              jamb needs it: its reveal edge may not move into the opening.
      djd     scales `dj`'s effect on the DEPTH (front/back planes) only,
              without touching the width jitter or the rng stream. 0 for a
              member whose front or back plane has a clearance contract on it
      wane_side  which arris the wane and the roll are allowed to eat. Defaults
              to the opposite of `anchor`, because an anchored arris that then
              gets waned is not anchored at all -- that mistake showed up as a
              sliver of bright core plaster down the reveal of the rough window
              bay, where the jamb's front face had shrunk 10 mm off the edge it
              was supposed to be covering.

    Sharp arrises on purpose -- the wane facet is what catches the light on a hewn
    timber, and a bevel would cost more than the whole primitive.
    """
    r = rng(f"{p.name}/hewn/{seed}")
    if wane_side is None:
        wane_side = 0 if anchor == 0 else (-1 if anchor > 0 else 1)
    ax, az = b[0] - a[0], b[1] - a[1]
    L = sqrt(ax * ax + az * az)
    if L < 1e-6:
        return []
    ux, uz = ax / L, az / L
    nx, nz = -uz, ux                     # perpendicular, in the wall plane
    ph = [r.uniform(0, 2 * pi) for _ in range(3)]
    hw0 = w / 2
    vs, F = [], []
    for i in range(k + 1):
        t = i / k
        env = lerp(1.0, sin(pi * t), pin)
        cx, cz = a[0] + ax * t, a[1] + az * t
        lat = wave * (.62 * sin(2.1 * pi * t + ph[0])
                      + .38 * sin(3.7 * pi * t + ph[1])) * env
        hw = hw0 * lerp(1.0, taper, t) * (1 + r.uniform(-dj, dj) * env)
        lat += anchor * (hw0 - hw)       # hold one arris, move the other
        hwf = hw * (1 - wane * (.55 + .9 * r.random()) * env)
        sk = roll * hw * env * sin(1.9 * pi * t + ph[2])
        # `djd` scales the DEPTH jitter alone. The two draws are still made, so
        # the width/lateral stream downstream is bit-identical at any djd, and
        # djd=1.0 is the historical behaviour. A member whose FRONT or BACK plane
        # has a contract on it passes 0 -- see THE JAMB'S BACK HAD 6 mm AND
        # USED 15.
        y0 = y + bow * sin(pi * t) + r.uniform(-dj, dj) * djd * d * .30 * env
        y1 = y0 + d * (1 + r.uniform(-dj, dj) * djd * env)
        # the wane (and the roll with it) eats only the arris it is allowed to:
        # wane_side 0 -> both, -1 -> the -n arris only, +1 -> the +n arris only
        dneg = (hw - hwf) if wane_side <= 0 else 0.0
        dpos = (hw - hwf) if wane_side >= 0 else 0.0
        oa = -(hw - dneg) + (sk if wane_side <= 0 else 0.0)
        ob = (hw - dpos) + (sk if wane_side >= 0 else 0.0)
        px, pz = cx + nx * lat, cz + nz * lat
        for (o, yy) in ((oa, y0), (ob, y0), (hw, y1), (-hw, y1)):
            vs.append((px + nx * o, yy, pz + nz * o))
    for i in range(k):
        q, s = 4 * i, 4 * (i + 1)
        F += [(q, q + 1, s + 1, s), (q + 1, q + 2, s + 2, s + 1),
              (q + 2, q + 3, s + 3, s + 2), (q + 3, q, s, s + 3)]
    F += [(0, 1, 2, 3), (4 * k + 3, 4 * k + 2, 4 * k + 1, 4 * k)]
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _peg_r(p, r, x, z, face=FY, r_=.027, stand=.026, mat="oak_pale", jit=.024):
    """A peg driven by eye: the position wanders, the head tilts, and no two are
    the same size. `stand` is under the regular family's 0.036 on purpose -- the
    rough pieces put pegs on prouder members, and PROUD_MAX is only 0.16.

    oak_pale for the same reason `_peg` is (the sawn end grain of a peg), and it
    matters more here: the rough half of the family carries MORE pegs -- every
    scarf and every lap gets one -- so a rough bay was spending its whole peg
    budget on heads nobody could see.

    `jit` is how far the position is allowed to wander, and it has to be PASSED
    DOWN on anything driven into the seam half-post or the gable's king post.
    Round 10 halved the post sections, and a peg whose centre wanders 24 mm with
    a head up to 32 mm across no longer fits inside a half-post (0.0975 then,
    0.080 since round 11) -- it hung out over the plaster, and one draw put a
    head 18 mm past the tiling plane and got clamped. On a wide member the wander
    is what makes the peg look driven by hand, so it stays the default; on a post
    it comes down to 6-8 mm, and the position itself is taken from the post's own
    centre line (G/2 - W_POST/4) rather than measured in from the seam."""
    _peg(p, x + r.uniform(-jit, jit), z + r.uniform(-jit * 1.33, jit * 1.33),
         face=face, r_=r_ * r.uniform(.80, 1.20),
         stand=stand * r.uniform(.75, 1.10),
         h=.056 * r.uniform(.90, 1.20), mat=mat,
         rot=(r.uniform(-7, 7), 0, r.uniform(-7, 7)))


def _scarf(p, key, z0, z1, xm, y=BY, d=BD, pale=.12, mat=None, seg=2, tint=.055,
           lap=.075, pad=.014, step=None, bow=-.004, pegs=True, seed=0,
           cham=CHAM, cstop=.16, cfac=2, peg_z=None, peg_face=None,
           peg_r=.024, peg_jit=.024, pad_up=None):
    """A shared band built as THREE timbers scarfed together, and the reason the
    rough half of this family can stand next to the regular half.

    The two OUTER stubs are the regular member verbatim -- `_band`/`_pin` keyed
    tone, `_mem` construction, `_cut` collapsing the chamfer onto the tiling
    plane -- so what a neighbouring bay sees at the seam is exactly what it sees
    from a regular bay. Only the MIDDLE timber is hand-hewn, and it touches no
    seam: it is `pad` bigger in section than the band so it swallows both stubs'
    end faces (no floating cut ends), `step` prouder so the join reads as a lap
    rather than a crack, and `pad * 1.6` deeper so its back plane cannot land on
    the stubs' back plane and z-fight there. The two stubs never overlap each
    other, for the same reason.

    z0/z1 must be clear of the piece's z seams -- see the section header.
    """
    step = pad * .45 if step is None else step
    m, sh = _band(key, pale, mat)
    r = rng(f"{p.name}/scarf/{key}/{seed}")
    h, zc = z1 - z0, (z0 + z1) / 2
    with _pin(p, key):
        # ROUND 9: the two stubs are WORKED like the regular family's bands --
        # same CHAM, same stops -- because a rough bay standing next to a regular
        # one has to be the same timber cut by a rougher hand, not a different
        # species. Their chamfers die at both ends: at the tiling plane (so the
        # section a neighbour meets is still the bare rectangle) and at the lap,
        # where the hewn middle swallows them, which is exactly where a chamfer
        # stops on a real scarf.
        _mem(p, -G / 2, xm - lap * .40, z0, z1, m, y=y, d=d, seg=seg, tint=tint,
             shade=sh, cham=cham, stop=cstop, facets=cfac, mids=2,
             seed=f"{key}/s0")
        _mem(p, xm + lap * .40, G / 2, z0, z1, m, y=y, d=d, seg=seg, tint=tint,
             shade=sh, cham=cham, stop=cstop, facets=cfac, mids=2,
             seed=f"{key}/s1")
        # ROUND 13 -- `pad_up`: WHERE THE OVERSIZE GOES. The hewn middle is `pad`
        # taller than the band so it swallows both stubs' end faces, and it took
        # that height half above the band and half below. Half above is fine on a
        # sole plate and is a defect on a sill: this band's top face IS
        # OPENINGS["win_upper"]["sill"], so 6 mm of pad plus the member's own
        # wander put the scarf 8.5 mm INSIDE the window hole on both rough window
        # bays (measured: SM_Wall_TimberWin_2m_Rough at x = +0.185,
        # SM_Wall_TimberJetty_2m_B_Rough at x = +0.140). The overshoot is now
        # directed: `pad_up` is how far the middle stands above the band top, and
        # a caller with an opening over the band sends the whole of it downward.
        pu = pad * .5 if pad_up is None else pad_up
        zm = z1 + pu - (h + pad) / 2
        _hewn(p, (xm - lap * 1.55, zm + r.uniform(-.004, .004)),
              (xm + lap * 1.55, zm + r.uniform(-.004, .004)), h + pad,
              d + pad * 1.6, m, seed=f"{key}/{seed}", y=y - step, k=3,
              bow=bow, wave=.003, taper=.99, wane=.05, roll=.06, dj=.022,
              pin=.60, tint=tint, shade=sh * .985)
    if pegs:
        # ROUND 13 -- `peg_z` EXISTS BECAUSE A SCARF DOES NOT KNOW WHAT IS BOLTED
        # OVER IT. On the two window bays the sill/apron band carries the projecting
        # CILL, which stands 30 mm prouder than the band and covers 68 mm of its
        # height, and the scarf was driving its pegs straight into the middle of
        # that: measured on SM_Wall_TimberWin_2m_Rough, one peg was 90.4% inside
        # the cill (103 cm2 of oak_pale head, at x 0.16-0.20, z 0.90-0.94, buried).
        # A peg nobody can see is worse than no peg -- it is a tri budget spent on
        # nothing -- and it is the same class of bug the fourth pass fixed by giving
        # `_peg` a `face`. So a caller that puts something over the band says where
        # its pegs go instead.
        pz = zc if peg_z is None else peg_z
        pf = (y - step) if peg_face is None else peg_face
        for sx in (-1, 1):
            _peg_r(p, r, xm + sx * lap * 1.1, pz, face=pf, r_=peg_r,
                   jit=peg_jit)


def _boards_rough(p, x0, x1, z0, z1, n, seed, y=BOARD_Y, d=.132,
                  pale=.62, k=3):
    """Hand-sawn vertical boarding: widths vary hard, gaps with them, every board
    is bowed and tapered, a few are out of plumb, and the butt line at top and
    bottom wanders instead of ruling a line across the bay.

    Depth is 0.112 rather than `_boards`' 0.104 so a board's BACK still lands
    inside the plaster core once its bow has moved it: 8 mm of clearance is what
    stops the two surfaces meeting on one plane."""
    r = rng(seed)
    ws = [r.uniform(.80, 1.24) for _ in range(n)]
    kk = (x1 - x0) / sum(ws)
    ph = (r.uniform(0, 2 * pi), r.uniform(0, 2 * pi))
    u = x0
    for i, w in enumerate(v * kk for v in ws):
        g = w * r.uniform(.05, .085)                 # uneven gap
        a, b = u + g / 2, u + w - g / 2
        u += w
        # THE LEAN IS COHERENT ACROSS THE RUN, not per board. Independent leans
        # make neighbours splay away from each other, so a 15 mm gap opens to
        # 60 mm at the far end and the boarding reads as a derelict fence. A
        # slow wave through the run leans them together, which is what a boarded
        # wall on a moving frame actually does.
        cx = (a + b) / 2
        ln = .013 * sin(ph[0] + i * .5)
        # THE BUTT WANDERS INWARDS ONLY. z0/z1 are already BURY inside the rails
        # above and below, and a board cut SHORT of them leaves a slot open onto
        # the core -- which is what the first look at this rendered as, a row of
        # dark wedges along the transom. Varying how DEEP each board is buried
        # gives the same hand-sawn butt line with nothing to see through.
        _hewn(p, (cx - ln, z0 - r.uniform(0, .028)),
              (cx + ln, z1 + r.uniform(0, .032)), b - a, d, _oak(r, pale),
              seed=f"{seed}/{i}", y=y + r.uniform(.002, .014), k=k,
              bow=.009 * sin(ph[1] + i * .5), wave=.004,
              taper=r.uniform(.87, 1.05), wane=r.uniform(.10, .30),
              roll=r.uniform(-.20, .20), dj=.05, tint=.05,
              shade=1.0 + r.uniform(-.12, .08))


def _frieze_rough(p, r, studs=1, seed=0):
    """The frieze out of true: studs unevenly spaced, not one of them plumb, and
    panels of unequal width sitting at different depths.

    `grow` is 0.036 on those panels and not the regular 0.010 for a reason worth
    writing down: the plaster is grown INTO the frame, so the panel's rim has to
    stay hidden behind the timber at every height. A hewn stud's edge moves by
    lean + wander + taper, and if the rim ever gets outside that swing the panel
    opens a slot onto the core. grow >= that swing is the rule everywhere a rough
    panel meets a hewn member."""
    rr = rng(f"{p.name}/frieze/{seed}")
    z0, z1 = Z_ATTIC
    xs = sorted(x + rr.uniform(-.070, .070) for x in _frieze_x(studs))
    edges = [-XE]
    for i, x in enumerate(xs):
        w = W_THIN * rr.uniform(.84, 1.16)
        ln = rr.uniform(-1, 1) * .016
        _hewn(p, (x - ln, z0 - .015), (x + ln, z1 + .015), w, FD,
              _oak(rr, .16), seed=f"{seed}/fs{i}", y=FY - rr.uniform(0, .005),
              k=2, wave=.003, taper=rr.uniform(.90, 1.02), wane=.20, roll=.15,
              dj=.05, shade=_sh(rr, .08))
        edges += [x - w / 2, x + w / 2]
    edges.append(XE)
    for i in range(0, len(edges), 2):
        _panel(p, edges[i], edges[i + 1], z0 - .010, z1 + .014, rr, grow=.036,
               tint=.055, rough=1.0, py=PY + rr.uniform(-.008, .008),
               seed=f"{seed}/fp{i}")


def _rails_rough(p, r, xs=(-.26, .24), sole=True, head=True, transom=True,
                 attic=True, studs=1):
    """The horizontals, hand-built. Same four bands at the same four heights as
    `_rails` -- that is what lets a rough bay sit against a regular one -- but
    the two that are clear of a z seam are scarfed, and the frieze is out of
    true. See the section header for why the sole plate and the wall plate stay
    single sticks."""
    if sole:
        _shared(p, "sole", -G / 2, G / 2, Z_SOLE[0], Z_SOLE[1],
                mat=OAK, y=BY, d=BD, seg=2, tint=.055,
                cham=CHAM, arris=(.5, 1.0), bow=(0.0, .004), facets=3)
        _scarf(p, "sole_bead", Z_SOLE[1] - .034, Z_SOLE[1] + .018, xs[0],
               pale=.52, y=BEAD_Y, d=.056, seg=1, tint=.07, lap=.062,
               pad=.010, step=.003, pegs=False, cham=CHAM_BEAD, cstop=.08,
               cfac=0)
    if transom:
        _scarf(p, "transom", Z_TRAN[0], Z_TRAN[1], xs[1], mat=OAK, y=BY, d=BD,
               seg=2, tint=.055, cstop=.19, cham=CHAM * .70)
    if head:
        _shared(p, "head", -G / 2, G / 2, Z_HEAD[0], Z_HEAD[1], mat=OAK, pale=.10,
                y=PLATE_Y, d=BD + (BY - PLATE_Y), seg=2, tint=.055,
                cham=CHAM, arris=(1.0, .35), stop=.115, bow=(.005, 0.0),
                facets=3)
    if attic:
        _frieze_rough(p, r, studs=studs)


def _brace_arc_rough(p, r, side, x_post, x_land, z_spring, z_land, w=W_BRACE,
                     mat=None, n=11, into_post=.045, into_rail=.022,
                     into_sill=.055, seed=0):
    """`_brace_arc`'s hand-cut twin. Same seated ellipse -- foot inside the near
    post and the rail it stands on, crown lapped into the rail above, head buried
    in the far post -- but the arris wanders, the member is deepest at the haunch
    and thinner at both ends, and the whole brace is BOWED out of the wall plane
    with Part.bow(), which is what that tool is for. The bow has to happen to the
    brace alone, so it is built in a sub-Part and merged."""
    x_foot = x_post + side * into_post
    cx = x_land - side * into_post
    cz = z_spring - into_sill
    ax = abs(cx - x_foot)
    az = z_land + into_rail - cz
    w0 = min(w, ax - 0.06, az - 0.06)
    rr = rng(f"{p.name}/brace/{seed}")
    m = mat or _oak(rr, .14)
    sh = _sh(rr, .07)
    # `_arc_c` carries all three of the hand-cut deviations this used to need a
    # sub-Part for -- a wandering radius, a section that swells at the haunch and
    # a bow out of the wall plane -- AND gives it the stop-chamfer and the adze
    # facets its machined sibling now has. So the prism + Part.bow() + merge()
    # round trip is gone: one primitive, no scratch Part, and the two braces are
    # unmistakably the same member cut by two different hands.
    _arc_c(p, cx, cz, ax, az, w0 * .86, 180.0 if side < 0 else 0.0, 90.0, m,
           n=n, d=FD - .006, cham=CHAM * .74, stop=.15, ends=.22, swell=.34,
           jit=.009, bow=rr.uniform(.006, .014), adze=ADZE, wear=.42,
           tint=.06, shade=sh, seed=f"rough{seed}")
    # positioned off the half-post's own centre line for the reason given in
    # `_brace_arc`: measured from the brace they walk off a slimmer post
    hp = G / 2 - W_POST / 4
    _peg_r(p, rr, side * hp, z_spring + .100, face=POST_Y, r_=.019, jit=.007)
    _peg_r(p, rr, -side * hp, z_land - .125, face=POST_Y, r_=.019, jit=.007)


def _lozenge_r(p, r, x, z, s=0.200):
    """The diamond motif, set by hand: off square, off centre, off depth."""
    m = _oak(r, .55)
    sh = _sh(r, .06)
    p.box((x + r.uniform(-.02, .02), FY + .026 + r.uniform(-.008, .008),
           z + r.uniform(-.03, .03)),
          (s * r.uniform(.88, 1.12), .052, s * r.uniform(.88, 1.12)), m,
          bevel=.014, seg=1, tint=.06,
          rot=(0, 45 + r.uniform(-7, 7), 0), shade=sh)
    _pnt(p, m, .06, sh)


# ------------------------------------------------------------- rough pieces ---
def wall_a_rough():
    """A's hand-hewn sibling: the same frame lines, not one of them dead
    straight. Scarfed bead and transom, a lumpy hand-floated panel, an arch brace
    whose arris wanders and which bows out of the wall, and a straight
    down-brace in the corner the arch leaves empty -- both ends of it seated,
    foot in the left post, head in the transom."""
    p = _reserve(Part("SM_Wall_Timber_2m_A_Rough", budget="wall", seams=SEAMS))
    r = rng("timber/A_rough")
    _core(p)
    _posts(p)
    _rails_rough(p, r, xs=(-.30, .22))
    f0, f1 = Z_FIELD
    _panel(p, -XE, XE, f0, f1, r, grow=.040, rough=1.0, py=PY - .006, seed="A")
    _brace_arc_rough(p, r, -1, -XE, XE, f0, f1, seed="A")
    # Both END FACES have to be BEHIND something prouder, or a cut face shows in
    # mid-panel. ROUND 11 re-fits it to the 0.080 half-post: the strut runs at
    # 49 deg, so a member of width w presents an end cap w*sin(49) = 0.76w across
    # in x, and it has to fit between the tiling plane and the post's inner face
    # at G/2 - W_POST/2. At w = 0.092 that cap is 0.070 wide and, centred 0.042
    # in from the seam, sits 0.923..0.993 inside a post running 0.920..1.0. The
    # post still stands 30 mm proud of the strut so the cap is hidden behind it,
    # and the head still sits 60 mm INTO the transom for the same reason.
    _hewn(p, (-G / 2 + .042, f1 - .58), (-.395, f1 + .060), .092, FD - .008,
          _oak(r, .16), seed="A/strut", y=FY - .003, k=3, wave=.006, taper=.88,
          wane=.22, roll=.16, dj=.05, shade=_sh(r, .08))
    _peg_r(p, r, -G / 2 + .042, f1 - .53, face=POST_Y, r_=.018, jit=.006)
    _peg_r(p, r, -.55, f1 - .13, face=FY - .003, r_=.024)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_b_rough():
    """B's sibling: the intermediate post is visibly OUT OF PLUMB -- 32 mm of
    lean over 1.8 m, plus wander, taper and a waney face -- the two panels it
    divides are unequal and sit at different depths, and the lozenges are set by
    eye. The lean is capped at the panels' `grow`, or the plaster would open a
    slot onto the core at the height where the post leans away from it."""
    p = _reserve(Part("SM_Wall_Timber_2m_B_Rough", budget="wall", seams=SEAMS))
    r = rng("timber/B_rough")
    _core(p)
    _posts(p)
    _rails_rough(p, r, xs=(.31, -.19), studs=2)
    f0, f1 = Z_FIELD
    xk = -0.055
    ka, kb = xk - W_STUD / 2, xk + W_STUD / 2
    ln = .016
    _hewn(p, (xk - ln, f0 - BURY), (xk + ln, f1 + BURY), W_STUD, FD,
          _oak(r, .14), seed="B/post", y=FY, k=4, wave=.004, taper=.92,
          wane=.24, roll=.17, dj=.05, shade=_sh(r, .08))
    _panel(p, -XE, ka, f0, f1, r, grow=.040, rough=1.0, py=PY + .008, seed="B0")
    _panel(p, kb, XE, f0, f1, r, grow=.040, rough=1.0, py=PY - .009, seed="B1")
    _lozenge_r(p, r, (-XE + ka) / 2, 1.520, .215)
    _lozenge_r(p, r, (kb + XE) / 2, 0.700, .180)
    for z in (f0 + .17, (f0 + f1) / 2, f1 - .15):
        _peg_r(p, r, xk, z)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_c_rough():
    """C's sibling: the boarded bay resawn. Board widths and gaps vary hard, each
    board bows and tapers, several are out of plumb, and the butt line wanders
    where the boarding dies into the plates. The ledger across it is scarfed and
    pegged."""
    p = _reserve(Part("SM_Wall_Timber_2m_C_Rough", budget="wall", seams=SEAMS))
    r = rng("timber/C_rough")
    _core(p)
    _posts(p)
    _rails_rough(p, r, xs=(-.19, .29), studs=2)
    f0, f1 = Z_FIELD
    # same apron-not-wall change as SM_Wall_Timber_2m_C, and the same laps: the
    # boarding is grown 26 mm past the ledger's soffit, the panel starts on the
    # ledger's top face and its own `grow` carries it under the timber
    zl = (APRON_TOP, SILL_TOP)
    _boards_rough(p, -XE, XE, f0 - .012, zl[0] + .026, 8,
                  "timber/C_rough/boards")
    _panel(p, -XE, XE, zl[1], f1, r, grow=.040, rough=1.0, py=PY - .007,
           seed="Cr")
    _scarf(p, "ledger", zl[0], zl[1], .16, mat=OAK, pale=.14, y=BY + .016,
           d=BD - .016, seg=2, tint=.055, lap=.070, pad=.012)
    for x in (-XE + .13, XE - .11):
        _peg_r(p, r, x, zl[0] - .22, face=BOARD_Y, r_=.025, stand=.024)
        _peg_r(p, r, x, zl[0] - .53, face=BOARD_Y, r_=.025, stand=.024)
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def wall_window_rough():
    """The window bay, hand-built. The OPENING is untouched -- 1.50 x 1.45, sill
    0.95, head 2.40 straight off spec.OPENINGS, so the same casement drops in --
    and everything around it is rough: hewn jambs whose reveal arris is ANCHORED
    (a wandering jamb would eat into the opening and foul the insert), a bowed
    sill nose, a scarfed sill and bead, and -- since round 10 -- a hand-floated
    PLASTER apron under the sill instead of resawn boarding, for the reason given
    on SM_Wall_TimberWin_2m."""
    p = _reserve(Part("SM_Wall_TimberWin_2m_Rough", budget="wall", seams=SEAMS))
    r = rng("timber/W_rough")
    ow, oh, sz = OPEN["w"], OPEN["h"], OPEN["sill"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, sz, sz + oh
    _core(p, holes=[(hx0, hx1, hz0, hz1)])
    _posts(p)
    _rails_rough(p, r, xs=(-.24, 0), transom=False, attic=False)
    _reveal(p, hx0, hx1, hz0, hz1, r)
    _panel(p, -XE, XE, Z_FIELD[0], APRON_TOP, r, grow=.040, rough=1.0,
           py=PY + .006, seed="Wap")
    # the scarf's pegs are driven through the CILL that covers this band, not
    # into the band behind it -- see `_scarf`, and the 103 cm2 of invisible peg
    # this used to make
    _scarf(p, "sill", APRON_TOP, SILL_TOP, .26, mat=OAK, pale=.14, y=BY, d=BD,
           seg=2, tint=.055, lap=.072, pad=.012,
           peg_z=hz0 - CILL_DROP - CILL_H / 2, peg_face=BY - .026,
           peg_r=.018, peg_jit=.006, pad_up=-.020)
    # the cill's TOP arris is anchored: it is what covers the core's reveal face
    # under the sill line, and a waney front face there uncovers it
    _hewn(p, (hx0 - .095, hz0 - CILL_DROP - .035),
          (hx1 + .095, hz0 - CILL_DROP - .035), .070, .120,
          _oak(r, .58), seed="W/nose", y=BY - .026, k=4, bow=-.005, wave=.004,
          taper=.98, wane=.16, roll=.10, dj=.035, anchor=1, tint=.07,
          shade=_sh(r, .07))
    _jamb_rough(p, r, hx0, hx1, hz0, hz1)
    for sx in (-1, 1):
        _peg_r(p, r, sx * JAMB_X, hz0 + .16, face=JAMB_Y, r_=.018, jit=.010)
        _peg_r(p, r, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.018, jit=.010)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


def _jamb_rough(p, r, hx0, hx1, hz0, hz1, top=None):
    """`_jamb`, hewn. The jamb's INNER arris -- the one that makes the reveal --
    is anchored dead straight with `_hewn(anchor=)`, because that edge already
    laps 6 mm into the opening and anything wandering further would foul the
    casement. All the movement is on the post side, where it is free.

    `top` for the same reason `_jamb` has one -- see LOW_JAMB_TOP."""
    zj0 = hz0 - BURY
    zj1 = min(hz1 + .035, Z_HEAD[0] + .015) if top is None else top
    for sx in (-1, 1):
        edge = (hx1 - JAMB_LAP) if sx > 0 else (hx0 + JAMB_LAP)
        far = edge + sx * JAMB_W
        a, b = sorted((edge, far))
        cx = (a + b) / 2
        # ROUND 13: wave is ZERO here, not "tiny". `lat` displaces the WHOLE
        # section, anchored arris included, so 2 mm of wave was 2 mm of wander on
        # the one face in this piece that spec.OPENINGS fixes -- and it showed up
        # as the last 0.7-2.2 mm of error in the measured hole after everything
        # else was exact. The hand-made wander is taken on the POST side instead
        # (`dj` moves the section's width, which `anchor` then absorbs entirely
        # into the free arris), so the jamb is still visibly hand-cut and the
        # reveal is dead straight, which is what a casement needs.
        # `djd=0` -- the DEPTH jitter only. See THE JAMB'S BACK HAD 6 mm AND
        # USED 15: the width jitter, the taper, the wane and the roll are
        # untouched, and `anchor` still throws all of the width wander onto the
        # post-side arris, so the member is exactly as hand-cut as it was.
        _hewn(p, (cx, zj0), (cx, zj1),
              b - a, JAMB_D, _oak(r, .50), seed=f"W/jamb{sx}", y=JAMB_Y, k=3,
              wave=.0, taper=.94, wane=.18, roll=.12, dj=.09, djd=0.0,
              anchor=sx, shade=_sh(r, .07))
        # the hand-floated cream strip. Its rim sits a few mm off its opposite
        # number's, the way two hand-floated bays never match; the jamb's wander
        # is on the post side, and the strip is grown 14 mm under it so a jamb
        # that wanders away cannot uncover the core behind. See `_cheek`.
        _cheek(p, far - sx * .014, sx * (XE + BURY), zj0 + CHEEK_END,
               zj1 - CHEEK_END,
               py=PY + r.uniform(-.006, .006), tint=.045,
               shade=1.0 + r.uniform(-.03, .03))
    m = _oak(r, .45)
    sh = _sh(r, .07)
    # ROUND 14: the SOFFIT IS ANCHORED and the wave is zero, for the reason the
    # jambs above are anchored -- this arris is now the head of the opening
    # itself, so it may not wander down into the hole (`_open_fade` fades the
    # WOBBLE back to nominal at the aperture, but a hewn deviation is baked in
    # before the snapshot is taken and it would survive). All the hand-made
    # movement is taken on the top arris, where it is free; the mould is 28 mm
    # shallower so its soffit clears the core band's in y. See THE DRIP MOULD IS
    # THE HEAD OF THE HOLE.
    _hewn(p, (-(hx1 - hx0 + .240) / 2, hz1 + DRIP_H / 2),
          ((hx1 - hx0 + .190) / 2, hz1 + DRIP_H / 2), DRIP_H,
          DRIP_BACK - DRIP_Y, m, seed="W/drip",
          y=DRIP_Y, k=4, bow=-.004, wave=.0, taper=.97, wane=.14, roll=.08,
          dj=.026, anchor=-1, tint=.06, shade=sh)


def wall_window_low_rough():
    """The centred window bay, hand-built. Same hole to the micrometre -- 1.500 x
    1.450 at sill LOW_SILL (0.530), head LOW_HEAD (1.980) -- so the same casement
    drops into either sibling, and everything around it is hewn: scarfed sole
    bead and sill, a scarfed TRANSOM (which this bay has and the high one cannot),
    an out-of-true frieze, hand-floated plaster apron, bowed cill, waney jambs
    with their reveal arris anchored.

    `xs` puts the sole bead's scarf and the transom's scarf on opposite sides of
    the bay, and neither lap is over the window: the transom's is at x = +0.26,
    i.e. 100 mm clear of the drip mould's end, so the hewn middle timber never
    reaches the part of the rail the hood covers."""
    p = _reserve(Part("SM_Wall_TimberWinLow_2m_Rough", budget="wall",
                      seams=SEAMS))
    r = rng("timber/WL_rough")
    ow, oh = OPEN["w"], OPEN["h"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, LOW_SILL, LOW_HEAD
    _core(p, holes=[(hx0, hx1, hz0, hz1)])
    _posts(p)
    _rails_rough(p, r, xs=(-.22, .26), studs=1)
    _reveal(p, hx0, hx1, hz0, hz1, r)
    _panel(p, -XE, XE, Z_FIELD[0], LOW_APRON_TOP, r, grow=.040, rough=1.0,
           py=PY + .006, seed="WLap")
    # the scarf's pegs go through the CILL that covers this band, not into the
    # band behind it -- see `_scarf` and the 103 cm2 of invisible peg that taught
    # it -- and `pad_up` sends the middle timber's whole oversize DOWNWARD,
    # because upward here is into the window
    _scarf(p, "sill", LOW_APRON_TOP, LOW_SILL, .26, mat=OAK, pale=.14, y=BY,
           d=BD, seg=2, tint=.055, lap=.072, pad=.012,
           peg_z=hz0 - CILL_DROP - CILL_H / 2, peg_face=BY - .026,
           peg_r=.018, peg_jit=.006, pad_up=-.020)
    # the cill's TOP arris is anchored: it covers the core's reveal face under
    # the sill line, and a waney front face there uncovers it
    _hewn(p, (hx0 - .095, hz0 - CILL_DROP - .035),
          (hx1 + .095, hz0 - CILL_DROP - .035), .070, .120,
          _oak(r, .58), seed="WL/nose", y=BY - .026, k=4, bow=-.005, wave=.004,
          taper=.98, wane=.16, roll=.10, dj=.035, anchor=1, tint=.07,
          shade=_sh(r, .07))
    _jamb_rough(p, r, hx0, hx1, hz0, hz1, top=LOW_JAMB_TOP)
    for sx in (-1, 1):
        _peg_r(p, r, sx * JAMB_X, hz0 + .16, face=JAMB_Y, r_=.018, jit=.010)
        _peg_r(p, r, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.018, jit=.010)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


# ------------------------------------------------------------- rough jetty ----
def _jetty_base_rough(p, r):
    """Bressumer + boarded soffit, hand-built. The soffit boards are resawn to
    uneven widths and sit at slightly different depths, the bressumer is scarfed
    (its middle timber only 3 mm proud, because at y = -0.135 that beam has
    almost none of PROUD_MAX left), and its pegs are driven by eye.

    The board run still lands a GAP on the bay seam and every board still ends
    dead on y = T + JETTY: that plane is the jetty's snap face."""
    rr = rng("timber/soffit_rough/" + p.name)
    n, y0, y1 = 9, -.02, T + J
    ws = [rr.uniform(.78, 1.26) for _ in range(n)]
    kk = G / sum(ws)
    u = -G / 2
    for i, w in enumerate(v * kk for v in ws):
        g = w * rr.uniform(.05, .11)
        a, b = u + g / 2, u + w - g / 2
        u += w
        m = _oak(rr, .70)
        sh = 1.0 + rr.uniform(-.11, .07)
        th = .060 * rr.uniform(.85, 1.20)
        # the board's UNDERSIDE stays on z = 0 -- that is the jetty's floor
        # plane -- so an uneven soffit is uneven upwards only
        p.box(((a + b) / 2, (y0 + y1) / 2, th / 2),
              (b - a, y1 - y0, th), m, bevel=.010, seg=1, tint=.05, shade=sh,
              skew=(rr.uniform(-1, 1) * .010, 0))
        _pnt(p, m, .05, sh)
    _scarf(p, "bressumer", .044, .318, -.21, mat=OAK, y=BRESS_Y, d=.185, seg=2,
           tint=.055, lap=.085, pad=.012, step=.004, bow=.002, pegs=False)
    _shared(p, "bress_low", -G / 2, G / 2, .026, .074, pale=.58, y=BRESS_Y + .023,
            d=.060, seg=1, tint=.07)
    _shared(p, "bress_top", -G / 2, G / 2, .300, .366, pale=.58, y=PLATE_Y,
            d=.128, seg=1, tint=.07)
    for x in (-.62, -.02, .58):
        _peg_r(p, r, x, .185, face=BRESS_Y, stand=.008, r_=.032)


def _jetty_shell_rough(p, r, apron_top, studs=1, transom=True, attic=True,
                       xs=(-.26, .24), boarded=True, peg=None):
    """`_jetty_shell`, hand-built -- including its `boarded` choice, so the
    rough half of the family splits the same way: jetty_a_rough carries a
    hand-floated cream apron, jetty_b_rough keeps ref2's resawn boarding."""
    _posts(p, z0=.346)
    _rails_rough(p, r, xs=xs, sole=False, studs=studs, transom=transom,
                 attic=attic)
    _jetty_base_rough(p, r)
    if boarded:
        _boards_rough(p, -XE, XE, .346, apron_top + .026, 8,
                      "timber/apron_rough/" + p.name)
    else:
        _panel(p, -XE, XE, .372, apron_top, r, grow=.040, tint=.06, rough=1.0,
               py=PY - .005, seed="JAap")
    # `peg` is the window bay's cill saying where its band may still be pegged --
    # see `_scarf`. The plain jettied bay carries nothing over this rail and
    # keeps the default.
    _scarf(p, "apron", apron_top, apron_top + SILL_H, .18, mat=OAK,
           pale=.14, y=BY, d=BD, seg=2, tint=.055, lap=.072, pad=.012,
           **(peg or {}))


def jetty_a_rough():
    """The plain jettied bay, hand-built: resawn soffit and apron, scarfed
    bressumer and apron rail, a lumpy panel and a bowed arch brace over it."""
    p = _reserve(Part("SM_Wall_TimberJetty_2m_A_Rough", budget="wall",
                      seams=SEAMS_J))
    r = rng("timber/JA_rough")
    at = APRON_TOP
    _core(p, z_top=H, z0=.030)
    _jetty_shell_rough(p, r, at, xs=(-.30, .21), boarded=False)
    f0, f1 = at + SILL_H, Z_TRAN[0]
    _panel(p, -XE, XE, f0, f1, r, grow=.040, tint=.06, rough=1.0,
           py=PY + .007, seed="JA")
    _brace_arc_rough(p, r, -1, -XE, XE, f0, f1, seed="JA")
    _wob(p, (.0110, 1.25), (.0048, 3.4))
    return _done(p)


def jetty_b_rough():
    """The signature bay, hand-built: jetty, resawn apron, and the wide window
    sitting on the apron rail whose top face IS the opening's sill. Opening
    untouched; jambs, sill nose and drip hewn."""
    p = _reserve(Part("SM_Wall_TimberJetty_2m_B_Rough", budget="wall",
                      seams=SEAMS_J))
    r = rng("timber/JB_rough")
    ow, oh, sz = OPEN["w"], OPEN["h"], OPEN["sill"]
    hx0, hx1, hz0, hz1 = -ow / 2, ow / 2, sz, sz + oh
    _core(p, holes=[(hx0, hx1, hz0, hz1)], z_top=H, z0=.030)
    _jetty_shell_rough(p, r, APRON_TOP, transom=False, attic=False,
                       xs=(-.22, 0),
                       peg=dict(peg_z=hz0 - CILL_DROP - CILL_H / 2,
                                peg_face=BY - .026, peg_r=.018, peg_jit=.006,
                                pad_up=-.020))
    _reveal(p, hx0, hx1, hz0, hz1, r)
    _hewn(p, (hx0 - .095, hz0 - CILL_DROP - .034),
          (hx1 + .095, hz0 - CILL_DROP - .034), .068, .124,
          _oak(r, .58), seed="JB/nose", y=BY - .026, k=4, bow=-.005, wave=.004,
          taper=.98, wane=.16, roll=.10, dj=.035, anchor=1, tint=.07,
          shade=_sh(r, .07))
    _jamb_rough(p, r, hx0, hx1, hz0, hz1)
    for sx in (-1, 1):
        _peg_r(p, r, sx * (XE - .12), hz0 - .34, face=BOARD_Y, r_=.025,
               stand=.024)
        _peg_r(p, r, sx * JAMB_X, hz1 - .22, face=JAMB_Y, r_=.018, jit=.010)
    snap = _snap(p)
    _wob(p, (.0105, 1.25), (.0045, 3.4))
    _open_fade(p, hx0, hx1, hz0, hz1, snap, head_x=DRIP_X)
    return _done(p)


# ------------------------------------------------------------- rough gable ----
def gable_rough():
    """The gable infill, hand-built. Rakes hewn to a wandering outline and set at
    two different depths so the pair is visibly not one machined V; king post out
    of plumb; the twin arch braces cut to varying width; the cream infill
    triangle floated by hand with a lumpy face.

    The APEX POINT ITSELF IS EXACT. z = ZA is this piece's snap plane -- the
    bargeboard and the finial from the gables family land on it -- so the rakes
    may wander anywhere except there."""
    p = _reserve(Part("SM_Wall_TimberGable_2m_Rough", budget="wall",
                      seams=dict(x=(-G / 2, G / 2), y=(0, T), z=(0, ZA))))
    r = rng("timber/GA_rough")
    rr = rng("timber/GA_rough/hew")
    zs = G_SOLE
    w_rake = G_RAKE
    dz = w_rake / cos(S.PITCH)
    soffit = lambda x: ZA * (1.0 - abs(x)) - dz
    fs = p.prism([(-G / 2, 0.0), (G / 2, 0.0), (0.0, ZA)], T - CORE_Y, "plaster",
                 axis='Y', at=(0, (CORE_Y + T) / 2, 0), bevel=0, tint=.04,
                 shade=.96)
    _pnt(p, "plaster", .04, .96)
    inner = [f for f in fs if f.calc_center_median().y > T - 1e-3]
    if inner:
        p._paint(inner, "plaster_dim", .05, .90)
    # the proud infill, floated by hand: its two rake edges and its foot wander,
    # and the face is broken into two planes so it is not one flat plate
    j = lambda a: rr.uniform(-a, a)
    tri = [(-G / 2 + .018, .018), (G / 2 - .018, .018), (0.0, ZA - .040)]
    ctr = (sum(q[0] for q in tri) / 3.0, sum(q[1] for q in tri) / 3.0)
    poly = []
    for i in range(3):
        q0, q1 = tri[i], tri[(i + 1) % 3]
        poly.append((q0[0] + j(.009), q0[1] + j(.005)))
        # every edge gets a mid point pulled a few mm INTO the panel: a floated
        # edge is not a straight line, and pulling it in (never out) keeps the
        # plaster under the rake timber instead of climbing over it
        mx, mz = (q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2
        k_ = .016
        poly.append((mx + (ctr[0] - mx) * k_ + j(.006),
                     mz + (ctr[1] - mz) * k_ + j(.006)))
    p.prism(poly, CORE_Y + .010 - G_INFILL_Y, "plaster", axis='Y',
            at=(0, (G_INFILL_Y + CORE_Y + .010) / 2 - .006, 0), bevel=0,
            tint=.05, shade=1.0)
    _pnt(p, "plaster", .05, 1.0)
    # THE HEWN RAKES ARE MEASURED, NOT ASSUMED. The king post below has to land
    # in the V these two make, and on this piece that V is jittered: the soffit's
    # apex point moves up to 14 mm and each rake's foot moves in x and z, which
    # tilts its upper face. So both are recorded as they are drawn -- `apex` is
    # the HIGHER of the two soffit apexes, i.e. the one that would leave plaster
    # showing, and `ceil` is each rake's foot, from which its upper face (the
    # plane the bargeboard lands on, the one surface here that may not be broken)
    # can be evaluated at any x. Guessing either from the nominal geometry is how
    # a head cut to fit ends up 14 mm short or 9 mm out through the rake.
    apex, ceil = ZA - dz, []
    for i, sx in enumerate((-1, 1)):
        xa = sx * (1.0 - zs / ZA)
        xb = sx * (1.0 - (zs + dz) / ZA)
        fx, fz = xa + j(.012), zs + j(.008)
        sj = ZA - dz + j(.014)
        bx, bz = xb + j(.012), zs + j(.008)
        apex = max(apex, sj)
        ceil.append((abs(fx), fz))
        # the inner edge LAPS past the centre line ALONG THIS RAKE'S OWN
        # (jittered) SOFFIT LINE -- see THE TWO RAKES BUTTED ON x = 0, which is
        # the defect this piece is where it was measured. The apex vertex does
        # not move (z = ZA on x = 0 is this piece's snap point) and the soffit
        # line is extended rather than rotated, so the rake's width does not
        # change anywhere. `bx`/`bz` are hoisted out of the list literal to keep
        # the j() draw order -- and therefore the mesh -- exactly as it was.
        s_ = G_RAKE_LAP / max(abs(bx), 1e-6)
        pts = [(fx, fz), (0.0, ZA),
               (-sx * G_RAKE_LAP, sj + (sj - bz) * s_), (bx, bz)]
        m = _oak(r, .12)
        sh = _sh(r, .07)
        p.prism(pts if sx > 0 else pts[::-1], FD + .034 + j(.006), m, axis='Y',
                at=(0, FY + FD / 2 - .016 - .004 * i, 0), bevel=.016, seg=1,
                tint=.06, shade=sh)
        _pnt(p, m, .06, sh)
    _shared(p, "sole", -G / 2, G / 2, 0.0, zs, mat=OAK, y=BY, d=BD, seg=2,
            tint=.055)
    # ROUND 15 -- THE BEAD IS A BEAD, not a structural timber. This call took
    # `_scarf`'s DEFAULTS -- cham=CHAM (26 mm), cstop=.16, cfac=2 -- on a member
    # 46 mm tall, where `_hexsec` clamps the chamfer to 42% of the section
    # (19 mm) and then cuts two adze facets into what is left. Every other rough
    # piece in the family builds the same bead through `_rails_rough` with
    # CHAM_BEAD (10 mm), a short stop and NO facets, precisely because a 50 mm
    # moulding cannot carry a structural arris; the gable was the one copy of
    # the call that never got the arguments, and the result was a top edge cut
    # into visible V-notches -- part of the "broken" read. Matched to
    # `_rails_rough` now. Nothing else about the band moves: same z, same y,
    # same keyed tone, same lap, same stubs cut flat on the tiling planes.
    _scarf(p, "sole_bead", zs - .030, zs + .016, -.24, pale=.52, y=BEAD_Y,
           d=.054, seg=1, tint=.07, lap=.060, pad=.010, step=.003, pegs=False,
           cham=CHAM_BEAD, cstop=.08, cfac=0)
    w_kp = G_KING
    # The head is seated in the apex the rakes actually built (see above), and
    # capped 20 mm clear of the lower of the two rake upper faces at the widest
    # its own tapered, waney, wandering head can reach -- the post must reach the
    # soffit, and it must not break out through the rake line doing it. Taper
    # 0.90 -> 0.80 is what buys the clearance to do both: a king post narrowing
    # to its head is also the right shape for the member.
    kx0, kx1, ktap = -.016, .006, .80
    hw_top = w_kp * ktap * 1.05 + .004
    zcap = min(ZA + (fz - ZA) * ((abs(kx1) + hw_top) / max(fx, 1e-6))
               for fx, fz in ceil) - .020
    ztop = max(apex + .002, min(apex + KP_SEAT, zcap))
    m_kp, sh_kp = _oak(r, .12), _sh(r, .07)
    _hewn(p, (kx0, zs - .02), (kx1, ztop), 2 * w_kp, FD + KP_DEEP,
          m_kp, seed="GA/king", y=FY, k=3, wave=.003, taper=ktap,
          wane=.22, roll=.16, dj=.05, shade=sh_kp)
    _king_head(p, w_kp, apex - .030, ZA, m_kp, shade=sh_kp)
    ro, wb = G_ARC_R, G_ARC_W
    for sx in (-1, 1):
        _arc_rough(p, rr, sx * (w_kp - .035), zs - .045, ro, wb,
                   180.0 if sx < 0 else 0.0, 90.0, _oak(r, .16), n=10,
                   shade=_sh(r, .07))
        _peg_r(p, r, sx * (w_kp + ro - .12), zs + .10)
        _lozenge_r(p, r, sx * G_LOZ_X, G_LOZ_Z, G_LOZ_S)
    # ONE landing peg, as on the machined twin above -- and the rough half needs
    # it for the same reason even though the gate cannot see it here. `_peg_r`
    # jitters position by up to 10 mm, which is enough to keep the two heads off
    # each other's plane (measured: 1 pair, 0.0 cm2 on this piece) but not enough
    # to stop two 44 mm pegs 16 mm apart interpenetrating on the post centre
    # line. A defect that only reads as clean because the noise moved it is still
    # the defect, and letting the two halves of a piece disagree about a joint is
    # how they drift apart.
    _peg_r(p, r, 0.0, zs + ro - .13, r_=.022, jit=.010)
    _peg_r(p, r, 0.0, soffit(w_kp) - .11, r_=.022, jit=.010)
    _wob(p, (.0075, 1.3), (.0035, 3.4), margin=.22)
    return _done(p)


def _arc_rough(p, r, cx, cz, ro, wb, a0, a1, mat, n=10, shade=1.0):
    """`_arc`, hand-cut: the sector's radius wanders and its width swells at the
    haunch, so the pair of braces under a gable apex are not two copies of one
    machined arc. `adze`/`tilt` come down to the gable's own relief budget for
    the reason given at ADZE_G -- and it matters more here than on the machined
    twin, because this piece's infill is floated 6 mm prouder still."""
    _arc_c(p, cx, cz, ro, ro, wb * .88, a0, a1, mat, n=n + 2,
           y=FY + .008 + r.uniform(-.004, .004), d=FD - .016, cham=CHAM * .58,
           stop=.11, ends=.25, swell=.30, jit=.010, bow=r.uniform(.004, .010),
           wear=.42, adze=ADZE_G, tilt=TILT_G, shade=shade,
           seed=f"garough{cx:.2f}")

# ================================================================== build ====
def build():
    """Seven regular bays, then the same seven hand-hewn. The regular ones come
    first and keep their exact names: they are the family's default and a level
    artist who wants a crisp, newly built wall picks from them."""
    out = [wall_a(), wall_b(), wall_c(), wall_window(), wall_window_low(),
           jetty_a(), jetty_b(), gable(),
           wall_a_rough(), wall_b_rough(), wall_c_rough(), wall_window_rough(),
           wall_window_low_rough(),
           jetty_a_rough(), jetty_b_rough(), gable_rough(),
           # ROUND 19 -- the fractional footprints, so a run does not have to be
           # a whole number of 2.0 x 2.6 bays and a 3.00 m storey does not have
           # to be filled by stretching one. See THE FRACTIONAL FOOTPRINTS.
           wall_half_a(), wall_half_b(), wall_half_window(), wall_qtr_a(),
           wall_tall_a(), wall_tall_b(), wall_tall_window(),
           wall_knee(), wall_band(),
           # ROUND 20 -- the two PLATE BAND heights assemble_inn's storey() needs
           # between a timber storey's head and the roof datum. See THE PLATE
           # BAND, AND THE HOLE IT CLOSES.
           band_eave(), band_gable()]
    return out


def demo():
    """A composed corner of an inn rather than a row: four bays of ground
    framing, a jettied upper storey oversailing it by spec.JETTY with the window
    bays in it, a gable infill over the centre bay, and a lower single-storey
    return wing running back on the right. The T x T corner void where two runs
    meet is where SM_Corner_* goes; here the return simply butts the front
    wall's inner face so the arris closes.

    IT NOW MIXES THE REGULAR AND THE ROUGH HALVES OF THE FAMILY DELIBERATELY, and
    that is the thing to judge in demo.png: every join in this arrangement is
    rough-against-regular or rough-against-MIRRORED-rough, which is the case the
    seam discipline exists for. The upper storey's right-hand bay is a mirrored
    rough jetty (mirroring is what assemble_inn.py does to the second half of a
    facade), so its half-post pairs with an unmirrored rough one at the join.
    Read down each bay boundary: the sole plate, the transom, the wall plate and
    the post must run through without a step, a groove or a tonal change.

    ROUND 10 also changed WHICH pieces it picks, and that was a real fault of its
    own. The ground row was A, W_Rough, C_Rough, W -- one plaster bay against a
    boarded bay and two window bays -- so demo.png, the image that gets judged,
    was mostly the family's two deliberately wooden pieces and read as a brown
    building even where the plaster bays were fine. A facade in either reference
    is mostly plain plaster panel with windows punched into it, so that is what
    the demo shows now: five plaster bays, two window bays, one boarded bay kept
    on the return wing so the boarded variant is still on show."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []

    def put(nm, loc, rz=0.0, mirror=False):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (0, 0, radians(rz))
        if mirror:
            o.scale = (-1.0, 1.0, 1.0)
        out.append(o)
        return o

    A, B = "SM_Wall_Timber_2m_A", "SM_Wall_Timber_2m_B"
    AR, CR = "SM_Wall_Timber_2m_A_Rough", "SM_Wall_Timber_2m_C_Rough"
    BR = "SM_Wall_Timber_2m_B_Rough"
    W, WR = "SM_Wall_TimberWin_2m", "SM_Wall_TimberWin_2m_Rough"
    WL, WLR = "SM_Wall_TimberWinLow_2m", "SM_Wall_TimberWinLow_2m_Rough"
    JA, JB = "SM_Wall_TimberJetty_2m_A", "SM_Wall_TimberJetty_2m_B"
    JBR = "SM_Wall_TimberJetty_2m_B_Rough"
    JAR = "SM_Wall_TimberJetty_2m_A_Rough"
    # ground storey: plaster, window-rough, window-CENTRED, plaster. ROUND 16
    # put the two window bays SIDE BY SIDE deliberately, because the thing to
    # judge in demo.png is now the pair: the same 1.50 x 1.45 hole at sill 0.950
    # and at sill 0.530, and what each does to the balance of the wall around it.
    # It is also the hardest seam in the family -- the centred bay carries a
    # transom and a frieze, its neighbour on the left carries neither -- so read
    # down that join and check the rail dies into the post instead of stopping in
    # mid-air, which is what POST_Y is for.
    for i, nm in enumerate((A, WR, WL)):
        put(nm, ((i - 1) * G, 0, 0))
    # ROUND 19 -- the FOURTH bay of that run is now ONE 2 m module built out of
    # TWO HALF BAYS, the second mirrored, because that is the seam the fractional
    # pieces have to be judged on: a 1.0 m bay against a 2.0 m one on the left,
    # and a mirrored half against an unmirrored half in the middle. Read down
    # both joins -- the sole plate, the transom, the frieze and the wall plate
    # must run through without a step, and the two half-posts in the middle must
    # read as one post with the pair of arches springing off it.
    put("SM_Wall_Timber_1m_A", (2 * G - G / 4, 0, 0))
    put("SM_Wall_Timber_1m_A", (2 * G + G / 4, 0, 0), mirror=True)
    # jettied storey: the right-hand bay is MIRRORED, as the assembler does
    for i, (nm, mir) in enumerate(((JA, False), (JAR, False), (JB, False),
                                   (JAR, True))):
        put(nm, ((i - 1) * G, -J, H), mirror=mir)
    # ... and the gable stands on a KNEE WALL, which is the composition Shanee
    # described ("half height walls as we used in with the gable"): 1.30 m of
    # framed spandrel with its own flat arch, then the triangle on top of it.
    put("SM_Wall_TimberKnee_2m", (0, -J, 2 * H))
    put("SM_Wall_TimberGable_2m_Rough", (0, -J, 2 * H + H_KNEE))
    # the return wing carries the boarded variant, so C is still on show, and
    # the ROUGH centred bay -- and, since round 19, a third module made of a
    # QUARTER bay, the half bay with the win_attic light in it and another
    # quarter bay: 0.5 + 1.0 + 0.5 = one 2 m module, which is the whole claim.
    for i, nm in enumerate((WLR, CR)):
        put(nm, (2 * G + G / 2, T + G / 2 + i * G, 0), rz=90)
    ry = T + G / 2 + 2 * G
    for dy, nm in ((-G / 4 - G / 8, "SM_Wall_Timber_0m5_A"),
                   (0.0, "SM_Wall_TimberWinAttic_1m"),
                   (G / 4 + G / 8, "SM_Wall_Timber_0m5_A")):
        put(nm, (2 * G + G / 2, ry + dy, 0), rz=90)
    # THE 3.00 m RANGE, running west off the main mass, and it is here because
    # the first of Shanee's two complaints is about exactly this storey: 42
    # objects in the showpiece are H_UPPER walls stretched (1, 1, 1.154) to fill
    # an H_GROUND one. Three of these four bays are CUT 3.00 m tall; the fourth
    # is the other way of getting there -- a 0.40 m plinth band with an ordinary
    # 2.60 m bay standing on it -- so the judged image carries both compositions
    # side by side and neither of them is scaled.
    put("SM_Wall_TimberTall_2m_A", (-2 * G, 0, 0))
    put("SM_Wall_TimberTallWin_2m", (-3 * G, 0, 0))
    put("SM_Wall_TimberTall_2m_B", (-4 * G, 0, 0))
    put("SM_Wall_TimberBand_2m", (-5 * G, 0, 0))
    put(B, (-5 * G, 0, H_BAND))
    # ROUND 20 -- THE PLATE BANDS, in the two places they are actually used.
    # The EAVE band caps the three jettied bays that do not carry the gable: that
    # is its real position, the course between a storey head and the eave, and
    # until it existed assemble_inn skipped it and left a 0.70 m open slot along
    # every eave face. The GABLE band caps the tall range's window bay and the
    # gable stands ON it -- in the assembler a projecting SM_Beam_JettySill_2m_C
    # goes between the two, which this demo cannot place because build_piece.py
    # builds one family at a time; see renders in the round-20 note for the stack
    # with the beam in it.
    for x in (-G, G, 2 * G):
        put("SM_Wall_TimberBandEave_2m", (x, -J, 2 * H))
    put("SM_Wall_TimberBandGable_2m", (-3 * G, 0, HG))
    put("SM_Wall_TimberGable_2m", (-3 * G, 0, HG + BAND_GABLE_H))

    for nm in src:
        src[nm].location = (0, 60, 0)
    return out


# ============================================================== the ratio ====
def _footprint(ob):
    """(x0, x1, z0, z1) of a BUILT piece's face, off its own declared seams.

    Both harnesses below used to scan a fixed 2.0 x 2.6 rectangle, which was the
    only footprint in the family until round 19. `finish()` stores the seams the
    piece was built with and `check()` has already proved the mesh lies inside
    them, so this is the piece's face by definition rather than by assumption.
    Falls back to the full bay for anything that has not declared any.
    """
    sm = ob.get("kit_seams")
    sm = eval(sm) if sm else {}
    x0, x1 = sm.get("x", (-G / 2, G / 2))
    z0, z1 = sm.get("z", (0.0, H))
    return x0, x1, z0, z1


def measure(objs=None, step=0.004, sun_deg=(52, 0, 34)):
    """HOW MUCH OF THIS WALL IS TIMBER, measured rather than argued about.

    Round 11 exists because Shanee looked at the assembled inn and said the
    upper storeys had been "replaced with wood while the reference is the
    plaster/white ones". That is a RATIO, so it needs a number, and it lives in
    this module rather than in a scratch script because a number that can drift
    away from the code it describes is worse than no number.

        blender -b --python build_piece.py -- timber_walls --no-render
        # then, in the same session:
        from kit.pieces import timber_walls as tw; tw.measure()

    or, standalone:

        import bpy, sys; sys.path.insert(0, "<inn_kit>")
        from kit import mats as M, util as U
        from kit.pieces import timber_walls as tw
        U.clear_scene(); M.build_all(); tw.measure(tw.build())

    WHAT IT DOES. For every piece, fire a `step` grid of rays STRAIGHT AT THE
    FACE -- from y = -2 along +Y, over the bay's full x and z -- and ask which
    material the first hit belongs to. That is exactly "what fraction of the
    wall face, seen head-on, is timber": no camera, no lighting, no render, and
    the same answer every run.

    Then a second question, because the brief is right that relief matters:
    every sample that landed on plaster fires one more ray at the kit's sun
    (kit.render.sun's default (52, 0, 34)). Plaster that the frame's own relief
    shades reads to the eye as more frame, so `dark` = timber + shadowed
    plaster is what the complaint is actually about, and it is the column that
    moves when a proud plane moves rather than a width.

    `ex-open` drops the win_upper opening, whose reveal backing is deliberate
    dark oak and which a casement fills in every real use, so the window bays
    can be compared with the plain ones on their WALL alone.

    ROUND 11, before -> after (regular pieces; the _Rough siblings track their
    twins within 2 points throughout):

        piece                     timber           dark          ex-open
        SM_Wall_Timber_2m_A       32.7 -> 27.1   39.9 -> 31.8   32.7 -> 27.1
        SM_Wall_Timber_2m_B       33.2 -> 28.0   41.1 -> 33.1   33.2 -> 28.0
        SM_Wall_Timber_2m_C       87.6 -> 50.9   93.4 -> 56.2   87.6 -> 50.9
        SM_Wall_TimberWin_2m      74.3 -> 68.2   79.9 -> 71.9   55.8 -> 45.3
        SM_Wall_TimberJetty_2m_A  58.2 -> 39.1   64.6 -> 44.1   58.2 -> 39.1
        SM_Wall_TimberJetty_2m_B  95.3 -> 92.8   98.9 -> 95.7   91.9 -> 87.7
        SM_Wall_TimberGable_2m    63.3 -> 50.6   68.7 -> 57.4   63.3 -> 50.6
        FAMILY MEAN (all 14)      63.0 -> 50.7   69.5 -> 55.8   59.9 -> 46.6

    The four bays assemble_inn.py actually builds facades out of -- a, b, c,
    win -- go 57.0 -> 43.6 as a group, and 47.4 -> 37.8 on their wall alone.

    STILL HEAVY, AND DELIBERATELY: SM_Wall_TimberJetty_2m_B. Its face is a
    bressumer band, a boarded apron and a 1.50 x 1.45 window, and ref2's
    signature jettied bay genuinely has almost no render in it. It is the one
    piece in the family kept timber-heavy on purpose; jetty_a is the plain
    jettied bay and carries the cream.
    """
    if objs is None:
        objs = [o for o in bpy.data.objects
                if o.type == 'MESH' and o.name.startswith("SM_Wall_Timber")]
    sun = (Euler([radians(a) for a in sun_deg], 'XYZ').to_matrix()
           @ Vector((0, 0, -1))).normalized()
    rows = []
    print(f"{'piece':34s} {'timber':>8s} {'plaster':>8s} {'shadow':>8s}"
          f" {'dark':>8s} {'ex-open':>8s}")
    for ob in objs:
        has_hole = "Win" in ob.name or "Jetty_2m_B" in ob.name
        # ROUND 19 -- THE SCAN IS THE PIECE'S OWN FACE, not a 2.0 x 2.6 rectangle.
        # A ratio measured over the wrong window is not a ratio: on a 3.00 m bay
        # the fixed z range missed the top 0.40 m outright (the frieze AND the
        # wall plate, i.e. the two most timber-dense bands), and on a 1.0 m bay
        # half the samples fell in the void beside the piece. The footprint comes
        # off the object's own declared seams, which `finish()` writes and which
        # are the same numbers `check()` validated the mesh against.
        fx0, fx1, fz0, fz1 = _footprint(ob)
        o_ = S.OPENINGS["win_attic"] if "WinAttic" in ob.name else OPEN
        hole = (-o_["w"] / 2, o_["w"] / 2, o_["sill"], o_["sill"] + o_["h"])
        nx, nz = int((fx1 - fx0) / step), int((fz1 - fz0) / step)
        tim = pla = tot = shd = nhole = thole = 0
        for i in range(nx):
            x = fx0 + (i + .5) * step
            for k in range(nz):
                z = fz0 + (k + .5) * step
                hit, loc, nrm, idx = ob.ray_cast(Vector((x, -2.0, z)),
                                                 Vector((0, 1, 0)))
                if not hit:
                    continue
                tot += 1
                mi = ob.data.polygons[idx].material_index
                nm = (ob.material_slots[mi].material.name
                      if mi < len(ob.material_slots) else "")
                nm = nm[2:] if nm.startswith("M_") else nm
                inh = (has_hole and hole[0] < x < hole[1]
                       and hole[2] < z < hole[3])
                nhole += inh
                if nm.startswith("oak"):
                    tim += 1
                    thole += inh
                elif nm.startswith("plaster"):
                    pla += 1
                    h2, _, _, _ = ob.ray_cast(loc + nrm * 1e-4, -sun)
                    shd += bool(h2)
        if not tot:
            continue
        wall = ((tim - thole) / (tot - nhole)) if tot > nhole else 0.0
        rows.append((ob.name, tim / tot, pla / tot, shd / tot,
                     (tim + shd) / tot, wall))
        print(f"{ob.name:34s} {tim/tot*100:7.1f}% {pla/tot*100:7.1f}%"
              f" {shd/tot*100:7.1f}% {(tim+shd)/tot*100:7.1f}%"
              f" {wall*100:7.1f}%")
    if rows:
        n = len(rows)
        print(f"{'FAMILY MEAN':34s} {sum(r[1] for r in rows)/n*100:7.1f}%"
              f" {sum(r[2] for r in rows)/n*100:7.1f}%"
              f" {sum(r[3] for r in rows)/n*100:7.1f}%"
              f" {sum(r[4] for r in rows)/n*100:7.1f}%"
              f" {sum(r[5] for r in rows)/n*100:7.1f}%")
    return rows


def measure_opening(objs=None, key="win_upper", step=0.0015, y_lim=None):
    """HOW BIG IS THE HOLE, measured in the BUILT MESH rather than read off the
    code that built it. This is the harness the thirteenth pass ran; it lives
    here so it cannot drift from the module it is measuring.

        blender -b --python - <<'EOF'
        import sys; sys.path.insert(0, "."); import bpy
        from kit import mats as M, util as U
        U.clear_scene(); M.build_all()
        from kit.pieces import timber_walls as TW
        TW.build(); TW.measure_opening()
        EOF

    A point (x, z) is IN THE APERTURE if a ray fired straight at the wall from
    outside meets nothing before spec.REVEAL -- i.e. if an insert occupying the
    front of the reveal would pass through there. Trusting the code instead is
    how the hole got 33 mm smaller than spec without anyone noticing: three of
    the four causes (a 6 mm jamb lap, a 14 mm cill lap, 15 mm of wobble) are each
    individually defensible in the source and only add up in the mesh.

    Edges are found by MARCHING outward from the middle of the hole to the first
    blocked sample and then bisecting. Marching matters: past the edge of the
    piece there is no geometry at all, so a plain bisection walks out of the wall
    and reports the bay width.

    Prints, per piece, the aperture's bounds and its narrowest/shortest column,
    against spec.OPENINGS[key]. Returns the rows.
    """
    from mathutils.bvhtree import BVHTree
    if objs is None:
        objs = [o for o in bpy.data.objects
                if o.type == 'MESH' and o.name.startswith("SM_Wall_Timber")]
    o_ = S.OPENINGS[key]
    yl = S.REVEAL if y_lim is None else y_lim
    zc0 = o_["sill"] + o_["h"] / 2
    rows = []
    print(f'spec {key}: w={o_["w"]:.4f} h={o_["h"]:.4f} sill={o_["sill"]:.4f} '
          f'head={o_["sill"] + o_["h"]:.4f}')
    for ob in objs:
        # ROUND 19: the march bounds are THIS piece's, not the module's. `edge`
        # returns None the moment it runs off the geometry, so a bounded hole was
        # always found correctly -- but on a fractional bay the limits were
        # outside the piece, which is the one condition that makes "ran off the
        # piece" and "found the far side of a hole" hard to tell apart.
        XL, XR, ZB, ZT = _footprint(ob)
        me = ob.data
        bvh = BVHTree.FromPolygons([v.co.copy() for v in me.vertices],
                                   [tuple(f.vertices) for f in me.polygons],
                                   all_triangles=False, epsilon=0.0)

        def clear(x, z):
            loc = bvh.ray_cast(Vector((x, -0.9, z)), Vector((0, 1, 0)), 4.0)[0]
            return loc is None or loc.y > yl - 1e-6

        def edge(fixed, start, limit, axis):
            stp = step if limit > start else -step
            a, b, u = start, None, start
            while (u < limit) if stp > 0 else (u > limit):
                u += stp
                if (clear(u, fixed) if axis == "x" else clear(fixed, u)):
                    a = u
                else:
                    b = u
                    break
            if b is None:
                return None                 # ran off the piece: not a bounded hole
            for _ in range(26):
                m = (a + b) / 2
                if (clear(m, fixed) if axis == "x" else clear(fixed, m)):
                    a = m
                else:
                    b = m
            return (a + b) / 2

        if not clear(0.0, zc0):
            continue
        xl = edge(zc0, 0.0, XL, "x")
        xr = edge(zc0, 0.0, XR, "x")
        zb = edge(0.0, zc0, ZB - 0.02, "z")
        zt = edge(0.0, zc0, ZT + 0.02, "z")
        if None in (xl, xr, zb, zt):
            continue
        wmin, hmin = xr - xl, zt - zb
        for i in range(1, 40):
            z = zb + (zt - zb) * i / 40
            a, b = edge(z, 0.0, XL, "x"), edge(z, 0.0, XR, "x")
            if a is not None and b is not None:
                wmin = min(wmin, b - a)
        for i in range(1, 40):
            x = xl + (xr - xl) * i / 40
            a, b = edge(x, zc0, ZB - 0.02, "z"), edge(x, zc0, ZT + 0.02, "z")
            if a is not None and b is not None:
                hmin = min(hmin, b - a)
        rows.append((ob.name, xr - xl, zt - zb, zb, zt, wmin, hmin))
        print(f"{ob.name:34s} w={xr - xl:.4f} h={zt - zb:.4f} "
              f"sill={zb:.4f} head={zt:.4f}   "
              f"narrowest {wmin:.4f}  shortest {hmin:.4f}")
    return rows
