"""Windows -- the inserts that fill the reveals cut by the wall families.

Measured off the reference crops, not guessed:

* ref1 (fantasy_inn), upper storey: lights are DARK, crossed by a fine
  **diamond lead lattice**. Leads are thin (~12mm) and the quarries small --
  roughly 13 per metre. The oak frame is chunky by comparison (~80mm), and the
  sash sits well back so the head throws a shadow across the top of the glass.
  One ground-floor light is lit: the same lattice, dark, over warm amber.
* ref2/ref3, upper storey: the light is WIDE. Measured off the ref3 linework
  (`compare.py crop --ref ref3:timber`) with the studs as the ruler: outer frame
  = 0.71 of the stud-to-stud bay, and 0.46 of the storey height, i.e. about
  **1.45 x 1.20 m in a 2.0 x 2.6 m bay -- 33% glazing**. Each light is split by
  one chunky mullion into two casements of two panes wide and five tall, glass a
  flat cool grey. Almost every one carries a **plank pent hood**: ~0.35x the
  window width deep, overhanging ~0.15 each side, dropping ~0.15 over that run
  (a lazy 26 degrees), carried on two straight raking struts whose tips poke out
  past the front fascia with a little pendant drop under each.
* ref2 dormer + gable lights: a small **carved crest** over the head, a
  projecting cill on two scroll corbels, open plank shutters laid back nearly
  flat with two dark iron ledgers each, and a planted box hung off the cill.
* ref2 ground floor: round-arched lights in a dressed stone surround -- radial
  voussoir ring about a quarter of the opening width thick, plain jamb blocks
  only a shade paler than the rubble, and a heavy weathered cill band that juts
  well past the reveal.

WHICH OPENING THE UPPER LIGHT USES -- read this before "fixing" it back.
Every upper-storey leaf here is built on spec.OPENINGS["win_upper"], 1.50 x 1.45,
because that is the ONLY upper-storey hole the kit actually cuts: timber_walls'
SM_Wall_TimberWin_2m, and nothing else. win_bay is not cut by any wall in the
kit (grep it), and assemble_inn drops all five casements -- A, B, Shuttered,
BayMullion, C -- into that one win_upper reveal.

A, B and the bay used to be built on win_bay, 1.50 x 1.10, back when win_upper
was 0.86 x 1.05 and too small to look at. spec has since widened win_upper to
exactly the reference proportion this family asked for, and building on the
narrower opening after that stopped being clever and started being a hole: in
a 1.45 m reveal a 1.06 m leaf leaves a quarter of a metre of the wall's own
recess showing across the whole width of the window, and the wall backs that
recess 140 mm deep, so it reads BLACK. That is the "gaps between the window
beams and the plasterboard/render" reported off the model, and it is measured,
not guessed -- see _head_close.

So: one opening, win_upper, for every leaf that goes in a timber wall. The pane
grid, mullion count and light count are all DERIVED (`_cols`/`_rows`, and n from
the width), so the leaves re-proportion themselves rather than needing tuning.
The head trim of each leaf is kept INSIDE the opening -- the wall's head plate
sits 20 mm over it at 2.42 -- and whatever the trim does not cover, _head_close
lines.

Conventions (spec.py): origin at footprint centre in X, Z=0 at the bottom of the
opening, outer wall face at Y=0, body runs +Y.

===========================================================================
ROUND 14 -- WHO OWNS WHAT, AND THE ONE RULE THAT DECIDES EVERY OTHER NUMBER
===========================================================================
Measured in the assembled inn, every leaf in this family was WIDER than the
hole it fills: A 1.70, B 1.76, C 1.60, the bay 1.57 x 1.67 against a
1.50 x 1.45 opening. None of that was glazing -- it was TRIM. Each leaf had
grown a projecting cill, a head board, a drip band or a pent hood and two jamb
architraves, and every one of those laps 100-260 mm PAST the opening onto the
wall face. Shanee, off the model: "SM_Win_LeadedCasement_A.002 doesn't seem to
fit SM_Wall_TimberWin_2m.007 properly and both add their own window sill and
there's various overlapping wood pieces that make it look strange."

They were right, and lapping was the wrong answer to a real problem. The lap was
grown round 9 to hide the 20 mm slot spec's INSERT_CLEAR leaves round every
insert. But INSERT_CLEAR is not a defect to be covered: it is the SHADOW GAP
that makes a window read as set INTO a wall. Covering it with a proud
architrave is what turned every opening into a flat panel stuck ON the wall --
which is exactly what the two blind critics measured ("openings read as decals
painted onto the wall").

    THE WALL OWNS THE SURROUND. THE INSERT OWNS THE JOINERY.

    wall   -- the sill and its nose, the head and its drip mould, the jamb
              linings, the reveal and its backing. SM_Wall_TimberWin_2m
              already builds every one of them (its sill rail's top face IS
              OPENINGS["win_upper"]["sill"]), stone_walls' window bay builds
              the stone cill, string course, jambs and voussoir ring, and the
              dormer family builds its own projecting sill plank. A wall with
              no insert in it still needs all of that; the same insert goes
              into more than one wall. So the wall carries it.
    insert -- frame, glass, leading, mullions, shutters, and whatever head
              treatment fits INSIDE the hole.

CONSEQUENCE, and it is a hard bound, checked by the piece's own seams:
NOTHING in a timber-wall leaf leaves the box x in [-0.73, 0.73],
z in [0.02, 1.43] -- that is the opening less INSERT_CLEAR all round, measured
in the OPENING frame (round 15; see `_seat`), and it is DECLARED AS THE PIECE'S
SEAMS, so util.check() proves the fit on every build -- at the sill as well as
at the head -- instead of a human eyeballing a render. No cills,
no head boards, no architraves, no pent hoods: they are the wall's, and where
this family drew one it was drawing the wall's member a second time, 70 mm
away from it. That is the "two window sills" and the "various overlapping wood
pieces". Relief may still stand out in -Y (an open casement, open shutters, the
bay's oriel box) because projecting outward is not lapping.

THE SASH IS SEATED IN THE REVEAL. spec.REVEAL is 0.10, and the glass now sits
at y = 0.112, with the frame's own face at y = 0.010 -- INSIDE the hole, where
it used to stand 10 mm PROUD of the wall face. Against SM_Wall_TimberWin_2m,
whose jamb lining stands at y = -0.046, that is 56 mm of visible reveal to the
sash face and 158 mm to the glass.

AND THE GLASS IS NOT A FLAT FILL. Each light is its own Part.glazing() unit,
built in a sub-Part and stamped in AJAR -- turned ~2.5 degrees about its own
centre line, alternately one way and the other (`_sash`) -- so no two lights in
a window share a surface normal and a leaded facade stops returning one grey.
Every frame also carries an OCCLUSION LINE: `_shadow`, a dark rebate band lapped
under the frame's back face and standing 17 mm into the aperture, so there is a
contact shadow between joinery and pane from any angle instead of glass butting
straight onto timber. And casement B is left OPEN, with `_interior` lining the
reveal behind it, because a kit with no transparent glass can show an interior
only through an opening that has no pane in it.

MEASURED, BEFORE AND AFTER (bounding box against a 1.50 x 1.45 hole):
    A   1.700 x 1.443  ->  1.460 x 1.410      B   1.764 x 1.443  ->  1.460 x 1.410
    C   1.600 x 1.444  ->  1.460 x 1.410      Shuttered 1.925 x 1.562 -> 1.460 x 1.410
    Bay 1.570 x 1.672  ->  1.460 x 1.394      Dormer 0.720 x 1.053 -> 0.580 x 0.740
                                              (win_dormer is 0.62 x 0.78)
    ArchStone 0.788 x 1.199 -> 0.760 x 1.195  (win_ground is 0.80 x 1.25)
check_zfight: 0 coincident pairs across the family.

Every piece still carries a dark interior blank so the clearance slot reads as
shadow and never as daylight.

===========================================================================
ROUND 15 -- FOUR MEASURED FAULTS, AND THE NUMBER EACH ONE GAVE BACK
===========================================================================
1. THE HEAD SLOT (high). "Datum z = 0 sits on the sill, so all vertical
   clearance goes to the head: 43.5 mm x 1.46 m of open 141 mm-deep reveal;
   sill clearance 1.5 mm." Both halves are fixed, and neither by cheating
   spec's 20 mm shadow gap:
     * the datum moved into the OPENING frame, so the clearance splits.
       Measured against spec.OPENINGS on every insert in the family:
       head slot 40.0 -> 20.0 mm, sill clearance 0.0 -> 20.0 mm; over the
       1.46 m light that is 584 -> 292 cm2 of gap. See `_seat`.
     * `_head_close` / `_head_lining` run the head trim back to Y_TRIM_BACK.
       Ray-cast through the head of all six timber-wall leaves: solid timber
       to y = 0.116, i.e. 24 mm of reveal left to SM_Wall_TimberWin_2m's
       backing plate, where casements A and B left 106 mm and the rest 64-68.
2. THE ARCH (medium). "Head band struck from a centre 20 mm low with radius
   21.5 mm small: crown gap 48 mm vs 17.5 mm at the springing." Now struck
   from the wall's own centre at r_in, on 14 segments so a vertex lands on the
   crown. Measured off the built mesh against spec's arc (R = 0.400 about
   z = 0.850): gap 20.0 mm at the springing, 20.0 mm at the crown, and 20.0 mm
   sampled every 10 degrees round the arc. It was 24 mm at the springing and
   44.6 at the crown.
3. THE GLASS (medium). "Panes are M_stone_dark, roughness 0.82, metallic 0 --
   matte stone, no specular." No material was added; the pane became geometry.
   Casement A: 18 glass faces and 10 distinct normals in the whole piece ->
   144 faces, 126 of them individually angled quarries. The widest angle
   between two glass normals in one casement: 4.4 -> 17.7 degrees. In the
   closeup render, clean glass patches (no lead, no shadow) inside one light:
   s.d. 1.8 -> 3.3 of 255, range 8.9 -> 18.2 -- and it now arrives as a STEP at
   every came instead of a gradient. See the block above GLAZE.
4. THE SHUTTERS (low). "Each shutter is 0.262 m wide; a quarter of the 1.46 m
   light is 0.365 m. The pair covers 36% of the opening." Two leaves became
   two BI-FOLD PAIRS of exactly W/4: 4 x 0.365 = 1.460 = 100.0% of the light,
   hung on the reveal edge so a closed pair spans +/-0.676 against a glazed
   aperture that ends at +/-0.678.

Still: every piece reports EMPTY, 1424-2364 tris against the 2600 budget
(casement A came DOWN, 2456 -> 2192, because the new leading is cheaper than
the boxed bars it replaces), check_zfight 0, and the mesh hashes identical
across two Blender processes.

===========================================================================
ROUND 16 -- THE GLASS IS A GLASS MATERIAL, AND THE QUARRIES FACE OUT
===========================================================================
1. THE PANE IS `glass_dark` NOW (#3B424C, roughness 0.11), not `stone_dark`.
   Round 15's answer to "matte stone, no specular" was to give the glass more
   NORMALS, because the palette had no dark glass to give it. It has one now, so
   both unlit looks take it -- and the geometry round 15 built is what makes it
   pay, because a specular material with one normal per light would be one
   highlight per light. See the block above GLAZE.

   MEASURED, and this is the part worth reading, because one of the three
   numbers went the WRONG WAY. Casement A in the real SM_Wall_TimberWin_2m,
   look_ref2 light, pixels attributed by ray cast, near-frontal (yaw 16):

       pane mean       167.6 -> 159.3      plaster behind it   213.6 (both)
       pane / wall     0.785 -> 0.746      pane s.d.  26.1 -> 21.1
       pane max        212.5 -> 211.3      lead mean  194.5 -> 193.8

   So the pane got 5% DARKER relative to the wall, not lighter, and 19% flatter.
   Separating the two changes (same harness, glass_dark tone at stone's own
   roughness) says exactly where that comes from:

       stone_dark  rough 0.82   mean 168.0  s.d. 25.18
       glass_dark  rough 0.82   mean 167.2  s.d. 25.14     <- tone alone: nothing
       glass_dark  rough 0.11   mean 159.7  s.d. 21.06     <- the gloss

   The TONE change is a hue change and nothing else -- #46433D and #3B424C are
   within 1 of each other in luminance -- and that is the whole point of it: the
   pane no longer shares its hue family with the oak around it, which is what
   made two critics call it a decal. The GLOSS is what costs 8 of value: a
   dielectric at roughness 0.11 moves energy out of the diffuse lobe into a
   specular lobe a few degrees wide, and in this kit's own lighting (a smooth
   two-tone world, one small sun, a stone ground plane) there is nothing bright
   for that lobe to find. Swept: roughness 0.11 / 0.22 / 0.34 / 0.50 measure
   159.9 / 160.1 / 161.2 / 164.2 -- i.e. the roughness number is nearly inert
   here, and no value of it recovers the diffuse.
   What DOES move it is tone, and it is a straight lever (frontal / oblique):
       #3B424C  pane/wall 0.747 / 0.747
       #444C58  pane/wall 0.791 / 0.790
       #4D5665  pane/wall 0.830 / 0.828   <- the audit's own 78:94 ratio
   Shanee owns the palette: if the 78-vs-94 figure is a target and not just
   evidence, `glass_dark` wants to be about #4D5665 and the roughness can stay
   at 0.11. Nothing in this module needs to change for that.

2. THE AJAR-LEAF TELL SURVIVES, and it was always weaker than this file claimed.
   Casement A's three lights, per-light mean, measured at three yaws:

       yaw 16   stone_dark 169.2/169.6/164.6 spread 4.96
                glass_dark 160.6/160.6/157.0 spread 3.68
       yaw 40   stone_dark 172.4/173.7/172.9 spread 1.25
                glass_dark 163.7/164.7/164.0 spread 1.03
       yaw 62   stone_dark 171.8/171.3/171.4 spread 0.56
                glass_dark 162.4/161.9/162.1 spread 0.48

   Same sign, same structure, and the spread scales with the pane mean -- so
   glass_dark does NOT do what `iron` did (collapse every light to one black).
   But 0.5-5 of 255 between neighbouring lights is not a tell anybody can see,
   and `_sash`'s docstring overstates it. +/-2.4 degrees is all the reveal allows
   (see `_sash`) and a cosine is flat there. What actually reads in the render is
   the QUARRY-to-quarry step inside each light: s.d. 21 of 255, range 103-182 at
   the 5th/95th. That is round 15's mechanism and it is the one carrying the
   piece; the leaf rotation is a garnish on it.

3. THE QUARRIES FACE OUT. 206 of 342 single-sided glass cards carried +Y
   normals -- invisible in EEVEE and Cycles, gone under backface culling. Fixed
   in `_cards_out`; read the block above it for why the winding could not be
   fixed in the generator. 206 -> 0, at zero tris.

4. NOTHING IN A LEAF PASSES y = 0.190 any more (it was 0.196), which is the
   contract timber_walls published when it moved its reveal backing plate to
   BACK_Y = 0.200. Ray-cast through the middle of every leaf: blank back 0.1900,
   wall plate front 0.2006 -- 10.6 mm of air where there were -4.

5. AND THREE THINGS ONLY THE ASSEMBLY COULD SHOW, found by casting each leaf
   against the REAL wall piece with a world-space BVH rather than by eye:
     * the interior blank's foot sat exactly on the top face of timber_walls'
       internal window board (z = sill + 0.030): 555 cm2 of back-to-back
       coincidence per window. `_blank`'s inset is 0.016 now.
     * casement B's `_interior` side liners buried 1 mm of themselves in that
       same board. They over-run by 1.5g instead of 2g.
     * arch_stone's interior blank was a full-height RECTANGLE in a ROUND-headed
       hole, so its top corners stood inside stone_walls' spandrels. It stops at
       the springing; the tympanum, already an arc segment, closes the head.
   Timber-wall leaves against SM_Wall_TimberWin_2m: 9-27 intersecting triangle
   pairs each -> 0, all six. check_zfight is a per-PIECE test and could not see
   any of this.
"""
import bpy, bmesh
from math import sqrt, sin, cos, atan2, degrees, radians, pi, floor, ceil, hypot
from mathutils import Matrix
from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "windows"
COLLECTION = "09_Windows"

T_T = S.T_TIMBER                    # 0.24 -- half-timber storey
T_S = S.T_STONE                    # 0.36 -- stone storey
CL = S.INSERT_CLEAR                # 0.02 all round

# ---------------------------------------------------------------------------
# THE GLAZING IS NOT BUILT IN THIS FILE ANY MORE.
#
# util.Part.glazing() builds frame + glass + leading in ONE call, and it makes
# the three faults this family kept re-reporting impossible by construction:
# the pane is cut OVERSIZE and the frame laps its edge, so glass can never stop
# short of its opening; the leading is struck over the WHOLE opening and clipped
# to the pane, so every diamond meets the edge as a partial diamond instead of
# floating in mid-pane; and the frame oversails onto the surrounding wall rather
# than butting to it, so no line can open between frame and plaster. Read its
# docstring -- it is the contract. The local _sash / _glass / _lead_diamond /
# _lead_grid ladder that used to live here is GONE, and with it the reason five
# families diverged: each had forked the same code and re-grown the same bugs.
#
# WHAT THIS MODULE STILL OWNS is where a glazed unit sits and how deep.
#
# D_GLAZE -- the `depth` every timber-wall leaf passes. glazing() lays its whole
# stack relative to the pane, so this one number fixes the ladder. ROUND 14
# MOVED IT BACK 20 mm, out of the wall face and into the reveal:
#
#       +0.015 .. +0.070   frame                     (55 mm deep)
#       +0.068 .. +0.087   `_shadow` occlusion line  (lapped under the frame)
#       +0.089 .. +0.103   leading                   (never coplanar with glass)
#       +0.106 .. +0.118   glass
#
#   * THE FRAME'S FRONT PLANE IS +0.010, i.e. 10 mm INSIDE the hole. It used to
#     be -0.010 -- proud of the wall face -- because the frame was being used to
#     lap over the 20 mm insert slot. It is not any more (see the header): the
#     wall's jamb lining stands at y = -0.046 and its stud at -0.072, so with
#     nothing of ours in front of y = 0 the wall's own reveal is 56 mm deep to
#     the sash face and 158 mm to the glass. That depth is the whole point;
#   * the glass at +0.112 is spec.REVEAL + 12 mm behind the wall face, which is
#     what "seated in the reveal" means in numbers;
#   * everything glazed still stays well in front of y = 0.140, where
#     SM_Wall_TimberWin_2m backs its own reveal with an opaque plate that its
#     own wobble can pull 15 mm forward. The pane's back at 0.118 keeps 22 mm.
#
# REB -- the rebate. glazing()'s own reveal (glass front to frame back) is
# lead*2.6 - 6 mm = 33 mm, so the pane's lip must run further under the frame
# than that or an oblique view finds frame where glass should be. That
# inequality is the rule the last four rounds kept rediscovering; it is
# asserted below so it cannot quietly stop holding.
#
# LEAD_W may not be trimmed far to buy depth, and here is the arithmetic:
# glazing() stands the leading 0.55*lead in front of the pane's own front face,
# less the pane's 6 mm half-thickness, so at lead = 0.012 the bars clear the
# glass by 0.6 mm and flicker. 0.016 keeps 2.8 mm, which is twice this family's
# whole wobble amplitude and reads as the ~12 mm came ref1 actually draws. The
# stack is ~97 mm frame-face to glass-face and that is fixed by the primitive;
# all we get to choose is where it sits.
# ---------------------------------------------------------------------------
D_GLAZE = 0.110          # `depth` for a timber-wall leaf -- see the ladder above
D_STONE = 0.150          # ...and for the stone storey, whose wall is 360 mm and
                         # whose dressed reveal liner runs back to y = 0.166, so
                         # the sash sits at the BACK of it: frame face 0.048,
                         # glass 0.150, i.e. a 150 mm stone reveal
LEAD_W = 0.018           # lead section: 16 mm across the pane, near square. It
                         # may not go below this (see the note above): the bars
                         # clear the pane by 0.55*lead - 6 mm, which is 3.9 mm
                         # here, 2.8 mm at 0.016 -- where check_zfight scored
                         # 150 cm2 of stone_pale against stone_dark down the
                         # middle of casement A -- and 0.6 mm at 0.012.
FR = 0.0435              # glazing-bead face width
OV = 0.003               # bead oversail term (see REACH below)
FO = FR + OV             # what glazing() calls frame+overlap
REACH = FO - OV / 2      # 0.045: how far the bead really reaches past its own
                         # aperture edge -- the number every call site needs
# ---------------------------------------------------------------------------
# MULL_LAP -- ROUND 17, AND IT IS 899 OF THE FAMILY'S 936 cm2
# ---------------------------------------------------------------------------
# The applied mullion is a cover strip laid over the joint between two leaves,
# and where its CHEEK lands across the leaf frame it covers decides everything.
# glazing()'s jamb is FO (46.5 mm) wide, and its INNER face -- the one that
# faces the light, the one an oblique camera looks straight down -- sits FO in
# from the leaf's own edge, i.e. at `joint + gap/2 + FO`. The mullion's
# cheek sits at `joint + mull/2`. So the clearance between two large, parallel,
# X-facing oak faces is exactly
#
#       margin = gap/2 + FO - mull/2
#
# and NOBODY WAS COMPUTING IT. Measured, round 17, with the bucketing corrected:
#       casement A   mull .104  margin +1.5 mm  ->  899 cm2 at 0.24-0.27 mm
#       shuttered    mull .108  margin -0.5 mm  ->  cheek 0.5 mm PAST the jamb
#       casement B   mull .114  margin -3.5 mm  ->  cheek 3.5 mm PAST the jamb
#       C / bay .062, arch .050, dormer .048    ->  +19 to +22 mm, clean
# The three wide ones were all sitting within half a jamb-thickness of the plane
# they had to avoid, and A's 1.5 mm closed to 0.24 mm because the leaf is stamped
# AJAR: turning a leaf swag degrees about its own centre slides a face at y=0.036
# sideways by 0.036*sin(swag) = 1.6 mm, and both jambs at a joint swing the SAME
# way (the leaves splay open there), i.e. straight at the cheek. A margin smaller
# than the ajar swing is not a margin.
#
# NEGATIVE is not safe either -- it is the other failure. At margin < 0 the
# jamb's inner face is INSIDE the mullion solid: no z-fight, because the face is
# sealed in oak, which is the fault this project calls worse than the fight.
#
# So the cheek lands MULL_LAP inside the jamb, always, and the cap is derived:
#       mull <= gap + 2*FO - 2*MULL_LAP
# At 12 mm that is 7x the ajar swing and 20x WOB, and it leaves 12 mm of the
# leaf's own frame showing either side of the strip -- which is what a mullion
# post with two casement stiles beside it actually looks like, and is a better
# reading than a strip wide enough to swallow both stiles.
MULL_LAP = .012


def _mull_max(gap):
    """Widest cover strip whose cheek still lands MULL_LAP inside the jamb."""
    return gap + 2 * FO - 2 * MULL_LAP
WOB = 0.0006             # HAND-HEWN WOBBLE, HALVED, and this one is measured.
                         # Part.glazing() draws each pane as ONE box, so a light
                         # is a single quad with four vertices; wobble displaces
                         # those four independently and the quad stops being
                         # planar, while the leading in front of it -- dozens of
                         # short bars with their own vertices -- follows the
                         # noise field properly. At 0.0012 the two stopped being
                         # parallel and check_zfight found 44-150 cm2 of
                         # stone_pale lying in the pane's own plane down the
                         # middle of casement A, the piece with the most bars.
                         # At 0.0006 the family measures 0 cm2, and 0.6 mm of
                         # irregularity on a planed sash is all a sash should
                         # have anyway: the hand-hewn look in this family comes
                         # from the WALL around it.
REB = 0.043              # pane rebate -- two inequalities pin it, both asserted
# (1) the pane's lip must out-run glazing()'s own reveal (glass front to frame
#     back = lead*2.6 - 6 mm) or an oblique view finds bead where glass should be;
# (2) it must stay UNDER the bead, or the lip shows past the bead's outer edge
#     instead of being buried in it.
assert REB >= LEAD_W * 2.6 - 0.006, "pane rebate must out-run glazing()'s reveal"
assert REB <= REACH - 0.001, "pane lip must stay buried under the bead"
# WHY MULLIONS ARE NOT ASKED OF glazing(), and it is arithmetic, not taste.
# Its mullions sit at depth - lead*2.2 and are 30 mm thick, so a mullion's BACK
# face lands 0.015 - lead*0.75 from the leading's FRONT face: at any lead section
# between 14 and 26 mm that is under 5 mm of air, and at lead = 20 mm it is
# exactly zero. Both faces are large and Y-facing, and this family wobbles, so
# every crossing of a lead over a mullion becomes a coincident patch. The lead
# section is pinned from the other side (0.55*lead - 6 mm has to clear the pane),
# so there is no value that satisfies both. Mullions here are therefore an
# APPLIED cover strip standing proud of the bead -- see `_sash` -- and the
# leaded net runs unbroken behind it, which is what one leaded facade looks like.
#
# REACH is the whole of the width arithmetic, so it is worth stating once:
# glazing()'s jamb spans [-hw - FR - OV/2, -hw + OV/2] about the aperture it is
# given, i.e. its frame reaches exactly REACH past that aperture. `_sash` sizes
# every leaf from that, which is what makes a window measure the width it was
# asked for instead of REACH more -- the bug the whole round is about.

Y_IN = 0.152             # front of the dark interior blank
# ROUND 17 -- IT WAS THE PANE'S OWN BACK PLANE, TO THE MICROMETRE.
# 0.116 was written as a free choice and it is not one: glazing() beds its pane
# at `depth`, 12 mm thick, so the pane's BACK face is at D_GLAZE + 0.006 =
# 0.116 exactly. Every head lining and head close in the family therefore ended
# its board on the plane the glass ends on, and where the two overlap in z --
# the head band laps the pane's oversize top by 8 mm, by design -- that is two
# large parallel +Y faces with nothing between them: 37.4 cm2 at 0.075 mm on
# casement A's centre light, and the same configuration latent on the shuttered
# light and the dormer (their leaves are turned far enough off the lining's
# centre that the corrected tool's centre-projection reads them as far apart,
# which does not mean the faces are).
# So it is DERIVED off the pane now and can never sit on it again: 22 mm behind
# the pane's back face, which is still 20 mm clear of the interior blank at
# Y_IN and 58 mm clear of the wall's own backing plate at 0.200.
Y_TRIM_BACK = D_GLAZE + 0.022   # 0.132 -- how far a member may reach INTO the
                         # wall. The number below is the history of the bound;
                         # what pins it TODAY is the pane in front of it and the
                         # blank behind it, both named above.
                         # It WAS set by the
                         # WALL: SM_Wall_TimberWin_2m used to back its
                         # reveal with a plate whose front face was y = 0.140,
                         # and a back face at 0.136 is 4 mm off it over the whole
                         # width of the opening. Neither piece measures as
                         # fighting on its own, but snapped together (and with
                         # both pieces' wobble pulling in opposite directions)
                         # that pair measured 880-971 cm2 at 0.5-0.8mm -- the
                         # largest real coincidence ever found in this family.
                         # ROUND 16: the wall's plate moved back to BACK_Y =
                         # 0.200, so this member now has 68 mm rather than 24 mm
                         # of clear air behind it -- and it does NOT follow the
                         # wall all the way back, because what the head gap looks
                         # into is not that air but the leaf's own interior blank,
                         # which stands across the whole aperture 20 mm behind it
                         # at Y_IN = 0.152. Running the trim back to the wall's
                         # contract plane would drive it straight through that
                         # blank: solid buried in solid, which check_collisions
                         # calls, rightly, a worse fault than the z-fight it
                         # looks like it avoids.

# Three glazing looks, all taken off the refs. (glass_mat, lead_mat).
#
# ROUND 16 -- THE UNLIT PANE IS GLASS NOW, NOT STONE.
# For fifteen rounds mats.py had exactly one glass entry -- the emissive amber of
# a LIT window -- so every unlit quarry in the kit borrowed `stone_dark`, and an
# auditor measured the result exactly right: "panes are M_stone_dark, roughness
# 0.82, metallic 0 -- matte stone, no specular", with the pane mean DARKER than
# the bare plaster behind it. Two blind critics independently called the glazing
# a decal. They were describing the material, and the material has changed:
#
#     spec.PALETTE["glass_dark"] = "#3B424C"   cool, dark
#     mats.ROUGH["glass_dark"]   = 0.11        glossy, NOT emissive
#
# so both unlit looks take it. What that buys, and it is the thing stone could
# not do: at roughness 0.82 a surface returns ONE value per normal and the value
# changes as the smooth cosine of the angle, so tilting a quarry 9 degrees moves
# it 1-2%. At 0.11 the specular lobe is a few degrees wide, so a quarry either
# catches the sun and the sky or it does not -- the same tilt is the difference
# between a glint and a dark sheet. The 126 individually angled quarries this
# family already builds were the right geometry waiting for the right optics.
#
# `iron` STAYS REJECTED and the reasoning is unchanged: three BLACK lights return
# the same black whatever their normals do, which kills the ajar-leaf tell. What
# was missing was never more value contrast, it was glass optics -- dark AND
# glossy, not dark and matte. glass_dark is 20% brighter than iron in tone and
# 4x glossier, so the pane keeps enough diffuse body to read as a sheet and gains
# the specular that tells the eye it is glazed.
GLAZE = {
    "dark": ("glass_dark", "stone_pale"),   # ref1 unlit: dark cool quarries,
                                            # pale lead
    "cool": ("glass_dark", "oak_dark"),     # ref2 daylight: same glass, dark lead
    "lit":  ("glass", "iron"),              # ref1's one lit window (emissive)
}

# ---------------------------------------------------------------------------
# THE GLASS IS GEOMETRY, BECAUSE IT CANNOT BE MATERIAL -- ROUND 15
# ---------------------------------------------------------------------------
# Measured, and it is the third time two blind critics have said the same thing:
# "panes are M_stone_dark, roughness 0.82, metallic 0 -- matte stone, no
# specular", "the glazing reads as a decal painted on the wall". They are right
# about the cause. mats.py has ONE glass material and it is the emissive amber
# for a LIT window; every unlit pane in the kit therefore borrows a stone tone,
# and a matte stone surface returns exactly one value per normal. A flat pane
# has ONE normal. No amount of tinting fixes that, and the brief forbids adding
# a material.
#
# What a matte surface CAN do is return a different value per NORMAL, so the fix
# is to give the glass more than one normal -- one per QUARRY, which is the unit
# the eye reads a leaded light in. Measured on casement A before: 18 glass faces
# (three flat panes, six faces each) and 10 distinct normals in the whole piece.
#
# So `_leaded` strikes ONE lattice and hangs both things on it:
#   * every QUARRY is its own slightly bowed pane, set at its own angle: a quad
#     standing Q_SET out of the backing pane, tilted up to Q_TILT in a direction
#     of its own and warped a little across its diagonal, so no two quarries in a
#     light return the same grey. Each quarry is an ISLAND -- its rim is held
#     Q_INSET off the came line, which is more than finish()'s 0.6 mm weld -- and
#     that is the part that makes it READ: an island's boundary is a sharp edge
#     whatever spec.SMOOTH_ANG is, so the value change between two quarries lands
#     as a hard STEP at the came.
#     TRIED AND MEASURED AND REJECTED FIRST: a four-triangle CUSHION per quarry,
#     rim on the pane and apex 11 mm proud. Its four facets meet at 16 deg, well
#     inside spec's 34 deg auto-smooth angle, so they shade as ONE smooth dome --
#     and a smooth 7 deg dome on a matte surface is a 1-2% gradient, which is
#     invisible. Rendered, casement A came back as flat as the flat pane it
#     replaced, at twice the tris. Steps read; gradients do not.
#   * every CAME is a tent section rather than glazing()'s square bar: a ridge
#     standing CAME_H proud with two sloping cheeks dying into the glass, so the
#     lead reads as a rounded came catching a highlight on one cheek and shadow
#     on the other. Its cheeks bury themselves under the quarries' rims, so no
#     line can open between lead and glass.
#
# WHY THIS FILE STRIKES THE LEADING AND Part.glazing() NO LONGER DOES. glazing()
# still owns everything that made it worth centralising -- the OVERSIZE pane, the
# frame that laps its edge, the frame that oversails onto the wall -- and it is
# still called for every light, with `lead` still setting the whole depth ladder.
# Only `pattern` is turned off, and `_leaded` re-strikes the same lines with the
# same clip (its cames land where glazing()'s bars did, to the micrometre) with
# the quarries between them. They have to come off one generator: a came drawn by
# one routine and a quarry drawn by another drift apart the moment either changes.
#
# IT IS ALSO CHEAPER THAN WHAT IT REPLACES, which is why it fits the 2600-tri
# budget at all: glazing()'s leading is a solid BOX per bar (12 tris) and this is
# a tent (4) plus ONE quad per quarry (2). Measured on casement A: 2456 tris
# before, 2192 after, with 126 quarries in it that were not there.
#
# THE DEPTH LADDER inside a light, all relative to the pane's front face y_g:
#       y_g - 0.022   came ridge                     (CAME_H)
#       y_g - 0.018   quarry, highest corner         (Q_MAX, and it is a hard cap:
#                                                     the came's cheek stands
#                                                     CAME_H*(1 - Q_INSET/half-width)
#                                                     = 19 mm over a quarry's rim,
#                                                     and glass may not push
#                                                     through its own lead)
#       y_g - 0.010   quarry, mean                   (Q_SET)
#       y_g - 0.002   quarry, lowest corner          (Q_MIN)
#       y_g           pane (glazing()'s), and nothing of ours goes behind it
# The whole stack stands inside the 22 mm that `_shadow`'s back face leaves clear,
# so no came ever crosses the rebate band in front of it.
Q_INSET = .0011          # gap from a quarry's rim to its came line. Bigger than
                         # finish()'s 0.6 mm weld, so quarries stay islands and
                         # auto-smooth cannot run across a came -- which is the
                         # whole mechanism, see above.
Q_MIN, Q_MAX = .002, .018   # depth band a quarry's corners live in
Q_SET = .010             # mean stand-off: how far the glass sits out of the pane
Q_TILT = .160            # max tilt, as rise per metre: 9.1 deg. A quarry's corner
                         # is 85 mm from its centre on casement A, so this asks for
                         # up to 13.6 mm of corner travel and the band above clamps
                         # what it cannot have. MEASURED on the built mesh: the
                         # widest angle between two glass normals in one casement
                         # went 4.4 deg (the three ajar leaves, and that was all
                         # the variation the family had) to 17.7 deg.
Q_WARP = .0016           # extra out-of-plane twist per corner, so a quarry is a
                         # slightly bowed sheet and not a flat plate
CAME_H = .022            # came ridge, proud of the pane
Q_HEM = .026             # how far inside the PANE the quarries stop -- see
                         # _leaded. The pane's outer 60 mm is under frame and
                         # rebate, so quarries out there are invisible tris.


def _leaded(p, cx, cz, gw, gh, depth, cell, pattern, mat_glass, mat_lead,
            tint=.05, seed=0, tilt=Q_TILT, quarries=True):
    """The leaded net and the glass surface, struck on ONE lattice.

    `gw` x `gh` is the PANE -- glazing()'s oversize rectangle, not the aperture
    -- centred on (cx, cz), and every line is clipped to it exactly the way
    glazing() clips its own, so each came meets the frame as a partial quarry
    instead of floating in mid-pane. Read the block above for what it is for.
    """
    if pattern == "none" or cell < 1e-4:
        return
    r = rng(f"leaded/{p.name}/{seed}")
    hw, hh = gw / 2.0, gh / 2.0
    y_g = depth - .006                      # glazing()'s pane, front face
    lw = LEAD_W * .9                        # came width across the pane

    def clip(a, b, c):
        """Clip a*u + b*v = c to the pane; return its two endpoints."""
        pts = []
        if abs(b) > 1e-9:
            for u in (-hw, hw):
                v = (c - a * u) / b
                if -hh - 1e-9 <= v <= hh + 1e-9:
                    pts.append((u, v))
        if abs(a) > 1e-9:
            for v in (-hh, hh):
                u = (c - b * v) / a
                if -hw - 1e-9 <= u <= hw + 1e-9:
                    pts.append((u, v))
        uniq = []
        for q in pts:
            if not any(abs(q[0] - t[0]) < 1e-6 and abs(q[1] - t[1]) < 1e-6
                       for t in uniq):
                uniq.append(q)
        return uniq[:2] if len(uniq) >= 2 else None

    # ---- the lattice: index (i, j) -> a point, and the two line families -----
    if pattern == "diamond":
        st = cell * sqrt(2.0)
        node = lambda i, j: ((i + j) * st / 2.0, (i - j) * st / 2.0)
        n0 = int(floor((-hw - hh) / st)) - 1
        n1 = int(ceil((hw + hh) / st)) + 1
        rng_i = rng_j = (n0, n1)
        fams = ((1.0, 1.0, st, rng_i), (1.0, -1.0, st, rng_j))
    else:
        node = lambda i, j: (i * cell, j * cell)
        rng_i = (int(floor(-hw / cell)) - 1, int(ceil(hw / cell)) + 1)
        rng_j = (int(floor(-hh / cell)) - 1, int(ceil(hh / cell)) + 1)
        fams = ((1.0, 0.0, cell, rng_i), (0.0, 1.0, cell, rng_j))

    # ---- the cames: a tent per line -----------------------------------------
    for (a, b, stp, (k0, k1)) in fams:
        for k in range(k0, k1 + 1):
            seg = clip(a, b, k * stp)
            if not seg:
                continue
            (u0, v0), (u1, v1) = seg
            du, dv = u1 - u0, v1 - v0
            L = hypot(du, dv)
            if L < 2 * lw:
                continue                    # a corner nick, not a came
            px, pz = -dv / L * lw / 2, du / L * lw / 2
            sh = 1.0 + r.uniform(-.05, .05)
            A0 = (cx + u0 - px, y_g, cz + v0 - pz)
            A1 = (cx + u1 - px, y_g, cz + v1 - pz)
            B0 = (cx + u0 + px, y_g, cz + v0 + pz)
            B1 = (cx + u1 + px, y_g, cz + v1 + pz)
            R0 = (cx + u0, y_g - CAME_H, cz + v0)
            R1 = (cx + u1, y_g - CAME_H, cz + v1)
            # two cheeks off one ridge. They shade differently by construction,
            # which is the whole reason a came is not a flat bar here.
            p.quad(A0, A1, R1, R0, mat_lead, tint=tint, shade=sh * 1.05)
            p.quad(R0, R1, B1, B0, mat_lead, tint=tint, shade=sh * .93)

    if not quarries or tilt <= 0:
        return
    # ---- the quarries: one quad per cell -------------------------------------
    # They are cut to a rect Q_HEM inside the PANE, not to the pane itself, and
    # a cell with less than a third of its area left is dropped. The pane is REB
    # (43 mm) oversize under the frame and `_shadow` stands 17 mm further in, so
    # the outer 60 mm of every pane is covered from any angle: quarries out
    # there are tris that cannot change a pixel. MEASURED on casement A: 2300
    # tris with the hem off and the sliver test at 2%, 2192 with both -- 54
    # quarries, none of which is ever in frame.
    qw, qh = hw - Q_HEM, hh - Q_HEM
    cell_a = cell * cell
    for i in range(rng_i[0], rng_i[1]):
        for j in range(rng_j[0], rng_j[1]):
            cor = [node(i, j), node(i + 1, j), node(i + 1, j + 1), node(i, j + 1)]
            cor = [(clamp(u, -qw, qw), clamp(v, -qh, qh)) for (u, v) in cor]
            ar = abs(sum(cor[k][0] * cor[(k + 1) % 4][1]
                         - cor[(k + 1) % 4][0] * cor[k][1] for k in range(4))) / 2
            if ar < cell_a * .32:
                continue                    # a sliver, under the frame anyway
            mu = sum(q[0] for q in cor) / 4.0
            mv = sum(q[1] for q in cor) / 4.0
            rim = []
            for (u, v) in cor:              # pull the rim off the came line
                d = hypot(u - mu, v - mv)
                t = 1.0 if d < 1e-6 else max(0.0, 1.0 - Q_INSET * 1.42 / d)
                rim.append((mu + (u - mu) * t, mv + (v - mv) * t))
            # ONE quad, set at its own angle: the tilt is what changes the value,
            # the island rim is what makes the change land as a step. Direction
            # and amount are both jittered, so a run of quarries never repeats.
            ang = r.uniform(0, 2 * pi)
            g = tilt * r.uniform(.30, 1.0)
            tu, tv = cos(ang) * g, sin(ang) * g
            set_ = Q_SET * r.uniform(.55, 1.35)
            sh = 1.0 + r.uniform(-.055, .055)
            q3 = []
            for k, (u, v) in enumerate(rim):
                d = set_ + tu * (u - mu) + tv * (v - mv) \
                    + Q_WARP * (1 if k % 2 else -1) * r.uniform(.2, 1.0)
                q3.append((cx + u, y_g - clamp(d, Q_MIN, Q_MAX), cz + v))
            p.quad(q3[0], q3[1], q3[2], q3[3], mat_glass, tint=tint, shade=sh)


# ---------------------------------------------------------------------------
# ROUND 16 -- THE QUARRIES FACE OUT. THIS MATTERS IN AN ENGINE, NOT IN BLENDER.
# ---------------------------------------------------------------------------
# MEASURED: "234 of 401 glass faces (58.4%) carry +Y normals pointing into the
# wall". True, and here is the whole mechanism, measured island by island on the
# built meshes (`p.finish()` output, every piece in the family):
#
#     1-face islands   342   ALL of them glass quarries   206 faced +Y  (60.2%)
#     2-face islands   ...   the came tents               0 faced +Y
#     6+-face islands  ...   closed solids (boxes, prisms, cyls)  correct
#
# A quarry is a single-sided CARD by design -- that is what makes it read (see
# the block above: an island's rim is a hard edge whatever SMOOTH_ANG is, so the
# value change between two quarries lands as a STEP at the came). Its winding is
# then decided by `Part.finish()`, which runs
# `bmesh.ops.recalc_face_normals` over the whole mesh. That operator orients
# CLOSED shells outward correctly and is the reason every box in the kit is
# right -- but for an isolated face there is no inside to be outside of, so it
# picks a side from the face's own position and plane. Verified in isolation: the
# same quad, wound both ways, comes back +Y either way at one position and -Y
# either way at another. So the winding `_leaded` hands it is not what survives,
# and re-winding the quad in the generator -- the obvious fix -- provably does
# nothing.
#
# Invisible in EEVEE and Cycles, which shade a back-facing normal as if it were
# front-facing. NOT invisible with BACKFACE CULLING ON, which is the default for
# opaque single-sided geometry in every game engine the kit targets: 206 of 342
# quarries simply DROP OUT, and what is left is a lattice with holes in it over a
# flat pane. This family cannot fix it inside the bmesh, so it fixes it on the
# mesh, after finish(), where recalc has already had its say.
#
# THE RULE, and it is narrow on purpose: only faces that are a WHOLE island on
# their own are touched -- every edge a boundary edge, nobody else's neighbour --
# because those are exactly the faces recalc_face_normals cannot reason about.
# Closed solids are left alone; so are the 2-face came tents, which measure 0
# wrong. Every card in this family is a glazing quarry and every glazing quarry
# faces the street, i.e. -Y in the piece frame (the most a light is ever turned
# is casement B's leaf, thrown open 15 degrees, so -Y stays the front). Cards
# whose normal has a +Y component are therefore reversed, and nothing else is.
# Zero tris, zero vertices moved: it is a winding change.
def _cards_out(ob, tol=0.0):
    """Reverse any single-face island whose normal points into the wall.

    Called on the way out of every builder. Records the count on the object as
    `kit_cards_flipped` so the number is measurable from the .blend rather than
    taken on trust, and returns the object so builders can `return
    _cards_out(p.finish())`.
    """
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.normal_update()
    bad = [f for f in bm.faces
           if f.normal.y > tol and all(len(e.link_faces) == 1 for e in f.edges)]
    if bad:
        bmesh.ops.reverse_faces(bm, faces=bad)
        bm.to_mesh(me)
    bm.free()
    ob["kit_cards_flipped"] = len(bad)
    return ob


# The opening each family member fills. See the module note: the upper-storey
# workhorse deliberately uses the WIDE opening, because that is what the
# references measure at.
K_UP = "win_upper"      # 1.50 x 1.45 -- THE upper-storey reveal, the only one
                        # any wall in the kit cuts. See the module note.
K_SMALL = "win_upper"   # same hole: every timber-wall leaf fills it completely



def _ins(key):
    """Insert size for an opening: INSERT_CLEAR smaller all round."""
    o = S.OPENINGS[key]
    return o["w"] - 2 * CL, o["h"] - 2 * CL


# THE ENVELOPE, hoisted so every leaf is measured against one pair of numbers
# rather than each re-deriving them and drifting. OW/OH is the hole,
# W/H is the insert, XO is the insert's own outer edge in x. NOTHING that
# belongs to a timber-wall leaf may leave x in [-XO, XO], z in [0, H];
# each piece declares exactly that as its seams, so util.check() proves the fit
# instead of a human eyeballing it.
OW, OH = S.OPENINGS[K_UP]["w"], S.OPENINGS[K_UP]["h"]     # 1.50 x 1.45
W, H = OW - 2 * CL, OH - 2 * CL                            # 1.46 x 1.41
XO = W / 2                                                 # 0.73


# ===========================================================================
# ROUND 15 -- WHERE THE 20 mm OF CLEARANCE GOES, AND IT IS NOT ALL AT THE HEAD
# ===========================================================================
# THE FAULT, measured in the assembled inn: "datum z = 0 sits on the sill, so all
# vertical clearance goes to the head: 43.5 mm x 1.46 m (572 cm2) of open,
# 141 mm-deep reveal; sill clearance 1.5 mm." True, and the arithmetic is plain:
# every builder below drew its leaf from z = 0 to z = H = 1.41, and the assembler
# seats it at `z + 0.95*zs`, which IS spec's sill line. A 1.41 m leaf standing on
# the sill of a 1.45 m hole leaves 40 mm in ONE slot along the head, and behind
# that slot the wall's reveal runs back 140 mm to its backing plate. Every window
# in the building had a black letterbox over it.
#
# spec.INSERT_CLEAR is "gap all round between an insert and its reveal" -- ALL
# ROUND, i.e. 20 mm at the head AND 20 mm at the sill, not 40 and 0. So the datum
# changes, and only the datum: every builder still draws in the INSERT frame
# (z = 0 at the leaf's own foot, which is what every number below reads as), and
# `_seat` lifts the finished piece by CL into the OPENING frame -- z = 0 on the
# wall's sill, which is exactly where assemble_inn and the demo put it. The seams
# are then declared as the CLEARANCE ENVELOPE in that frame, z = (CL, OH - CL),
# so util.check() proves the 20 mm at the SILL on every build instead of a human
# eyeballing a render: geometry below z = 0.020 now fails the z-min check as
# loudly as geometry above 1.430 fails z-max.
#
# The other half of the fault is DEPTH, and that is `_head_lining`. Splitting the
# clearance is all spec allows -- 20 mm of shadow gap is the law, and a window
# with no gap at its head reads as a panel stuck on the wall. What the gap LOOKS
# INTO is ours, though, and it was 106 mm of empty reveal.
Z0, Z1 = CL, CL + H       # 0.020 .. 1.430 -- the leaf's band in the OPENING frame


def _seat(p, z0=CL):
    """Lift a built insert from the INSERT frame into the OPENING frame.

    Everything below is drawn with z = 0 at the leaf's own foot, because that is
    how a leaf reads: bands, sash, crest and lintel are all measured off it. The
    piece is PLACED, though, on the opening's SILL. One translation at the end of
    each builder is the whole difference between 40 mm of slot over every window
    in the building and 20 mm over it and 20 mm under it. Call it before
    wobble(), so the seam fade still measures against the declared snap planes.
    """
    p.transform(Matrix.Translation((0.0, 0.0, z0)))


def _head_lining(p, w, z_top, y0, h=None, mat="oak_mid", shade=.60, tint=.04):
    """Line the head of the reveal BEHIND the piece's own head trim.

    The other half of the head-slot fault, and the half spec does not fix for us.
    Above every leaf's head band there was nothing at all: the band is 30 mm deep
    and the wall backs its reveal at y = 0.140, so from anywhere below the head --
    which is where a street camera always is -- the eye went over the band and
    straight into 106 mm of empty reveal. Measured on casement A: head trim back
    face y = 0.034, wall backing y = 0.140.

    This is a plain board filling that void, from the trim's back to
    Y_TRIM_BACK, so what the head gap looks into is a soffit 24 mm off the
    wall's own backing instead of a hole. 12 tris, on every piece in the family.
    """
    p.plate((0, (y0 + Y_TRIM_BACK) / 2, z_top - (h or Z_BAND) / 2),
            (w, Y_TRIM_BACK - y0, h or Z_BAND), mat, tint=tint, shade=shade)


# THE DEEPEST PLANE A LEAF MAY REACH, and it is the WALL's number, not ours.
# timber_walls owns the solid at the back of a win_upper reveal -- an opening with
# no casement in it must still not be a see-through hole -- and it moved that
# plate's front face out of our way, from y = 0.140 to BACK_Y = 0.200, publishing
# the contract in the same commit: "NOTHING in a leaf may pass y = 0.190. The
# wall's solid starts 10 mm behind that."
# Our blank ran to 0.196. That is 4 mm PAST the contract and 4 mm short of the
# wall's plate over the whole 1.46 x 1.41 aperture: two large parallel Y-facing
# faces, in two pieces that both wobble, which is the same pair that measured
# 880-971 cm2 in the assembly the last time this family parked a face 4 mm off a
# timber_walls plane. It is now 0.190 on the nose -- 10 mm of air -- and the
# number lives in one constant so no caller can drift past it again.
Y_LEAF_BACK = 0.190


def _blank(p, w, h, z0=0.0, y=Y_IN, d=None, inset=.016):
    """Dark interior blank. There is nothing behind a game window, but the
    reveal slit must never show sky.

    `d` defaults to whatever reaches Y_LEAF_BACK from `y`, so a timber-wall leaf
    cannot be given a blank that crosses the wall's contract plane. The stone
    storey passes its own `d`: stone_walls plugs the back of its own reveal at
    y = 0.286 and this blank floats in the void in front of that, so its bound is
    a different one (see arch_stone).

    Two of its faces used to be somebody else's:
      * its FRONT landed exactly on the back of the glazing -- the single biggest
        coincident surface in the family (1.58 m2 on the shuttered light);
      * its BOTTOM landed exactly on the sill of the wall's reveal, because both
        are z = 0 in the same snapped frame. That one only shows up when the
        insert is in a wall, and it was 715 cm2 on EVERY casement -- most of the
        "z-fighting on the inside/backside" reported off the model.
    So it is held `inset` clear of the reveal's sill and head.

    ROUND 16 GREW `inset` 6 mm, and the number is timber_walls' again. Its
    reveal carries an INTERNAL WINDOW BOARD, oak_mid, spanning y 0.120..0.210 --
    which straddles this blank in y -- and rising to z = sill + 0.030. With
    `_seat` lifting us by INSERT_CLEAR, an inset of 0.010 put this plate's
    bottom face on z = sill + 0.030 exactly: 1.46 m x 38 mm = 555 cm2 of
    back-to-back coincident face across the whole aperture, in every upper
    window of the building. Invisible to check_zfight, which measures one piece
    at a time, and found only by running a world-space BVH of the leaf against
    the real SM_Wall_TimberWin_2m. At 0.016 the blank's foot clears the board's
    top face by 6 mm, and the 6 mm slot it opens looks at the wall's own backing
    plate 10 mm behind it, not at daylight."""
    if d is None:
        d = Y_LEAF_BACK - y
    assert d > 0.010, "interior blank has to be a board, not a film"
    p.plate((0, y + d / 2, z0 + h / 2), (w, d, h - 2 * inset), "oak_dark",
            tint=.03, shade=.22)


def _shadow(p, cx, cz, aw, ah, depth, g=.017, mat="oak_dark", shade=.16,
            tint=.03):
    """THE OCCLUSION LINE, and it is the answer to a measured critique: "leaded
    glass is a flat grey lozenge fill: no sky reflection, no reveal depth, no
    interior, so openings read as decals painted onto the wall".

    Two of those three are depth (see the header ladder). This is the third. A
    real sash has a REBATE: the pane is bedded behind the frame and the timber
    stands over its edge, so there is a hard dark line all the way round every
    light where no light can reach. Ours had none -- glass butted straight onto
    bead on one plane -- and without it the pane reads as paint on the frame.

    So: a band of dark timber lapped 2 mm under the frame's back face, standing
    `g` into the aperture and `g` out under the frame (so it cannot open a gap
    at the frame's edge whatever the wobble does), and stopping 2 mm short of
    the leading, which is the one thing in the stack it must not touch.

    Cheap on purpose -- two unbevelled boxes and two unbevelled 4-gon prisms,
    48 tris, the same as the four boxes it used to be -- because it goes into
    every light of every leaf of every piece in the family.

    ROUND 18: THE HEAD AND FOOT BARS RUN THROUGH, THE SIDE BARS STOP UNDER THEM
    AND TAPER OFF. This was 904 of the family's 1734 cm2.

    The ring used to be four boxes on ONE y span, head and foot full width and
    the sides full height, so every corner carried a 2g x g patch of DOUBLED
    solid whose front faces, back faces AND outer cheeks were all coplanar:
    three pairs a corner, twelve a light, 168 across the family. Measured at
    0.5 mm with NO area floor: 646.7 cm2 of Y-facing lap (34 x 17 mm each) plus
    196.9 cm2 X-facing (21 x 17), and 576.5 cm2 of it RAY-REACHABLE -- the inner
    half of every corner patch stands in the open aperture, in view. It read
    ZERO to check_zfight for four rounds because each lap is ~5.8 cm2 against a
    15 cm2 floor; this ring is precisely the death-of-a-thousand-cuts that the
    tool's ZFIGHT_ALL_PAIRS line was added to catch.

    The corner was pure redundancy -- the head bar already spans the full width,
    corners included -- so this removes solid rather than adding it, and the
    dark ring an eye sees through the aperture is unchanged.

    WHY TAPERED AND NOT JUST SHORTENED. Cutting the side bar level at z = hh - g
    butts two 34 x 21 mm faces on one plane, which is the same coincidence
    relabelled (~370 cm2, and only 0% reachable because it is interior), and
    sinking it a millimetre further seals that face inside the head bar, which
    this project rates worse than the fight. Taking the OUTER edge back by
    `taper` instead stands the end face 6.7 deg off the head bar's underside --
    6x check_zfight's 1 deg GUARD, with 4 mm of separation across the overlap
    against an 0.5 mm gate -- so the two can neither pair nor bury, and they
    still meet on the inner edge line, which is the edge that shows.
    """
    y0 = depth - LEAD_W * 2.6 - .002          # 2 mm inside the frame's back
    y1 = depth - LEAD_W * 1.45 - .002         # 2 mm short of the leading
    ym, dy = (y0 + y1) / 2, y1 - y0
    hw, hh = aw / 2, ah / 2
    for (bx, bz, bw, bh) in ((0.0, hh, aw + 2 * g, 2 * g),
                             (0.0, -hh, aw + 2 * g, 2 * g)):
        p.box((cx + bx, ym, cz + bz), (bw, dy, bh), mat, bevel=0, tint=tint,
              shade=shade)
    zi = hh - g                               # head/foot bar owns everything above
    taper = min(.004, zi * .4)                # stays valid on a tiny light too
    for sx in (-1, 1):
        prof = [(sx * (hw - g), -zi), (sx * (hw + g), -zi + taper),
                (sx * (hw + g), zi - taper), (sx * (hw - g), zi)]
        if sx < 0:
            prof.reverse()                    # keep the profile wound CCW
        p.prism(prof, dy, mat, axis='Y', at=(cx, ym, cz), bevel=0, tint=tint,
                shade=shade)


def _sash(p, x0, x1, z0, z1, cols, cell, pattern, glaze, y=0.0, depth=D_GLAZE,
          seed=0, swag=2.4, gap=.014, tint=.05, swing=None, mull=.096,
          mull_front=.002, mull_mat="oak_dark"):
    """A glazed SASH filling [x0,x1] x [z0,z1] of the reveal in `cols` leaves,
    with an applied mullion over every joint. Returns the joint x positions.

    ONE Part.glazing() PER LEAF, not one per window, and this is the second half
    of the "flat grey lozenge fill" fix. A single pane spanning a 1.46 m opening
    is one quad with one normal: every quarry in it returns the same grey, at
    every time of day, from every angle, which is why five critics in a row have
    called this family's glass painted-on. Real casements are separate leaves
    hung on separate hinges and no two of them sit in quite the same plane.

    So each leaf is built in its own sub-Part and stamped in AJAR: rotated
    `swag` degrees about its own vertical centre line, alternately one way and
    the other and by a jittered amount. The cost is zero tris and the effect is
    that a three-light window returns three different greys -- adjacent leaves
    differ by twice `swag` in surface normal -- so a leaded facade reads as
    glazing rather than as one sheet.

    IT IS A RIGID ROTATION AND THAT IS THE POINT. The first version of this
    CAMBERED the leaf with `Part.bow`, which was wrong twice over. glazing()
    draws the pane as ONE box, so its only vertices are its four corners -- and
    `bow` pins the ends, so the pane did not move AT ALL while the leading, whose
    bars have vertices spread right across the light, bowed up to 11 mm into it.
    check_zfight measured the result: 145 cm2 of M_glass against M_iron at
    y = 0.106, and 95 cm2 of stone_dark against stone_pale, i.e. the cames
    sinking through the glass in the middle of every light. A rigid rotation
    moves frame, leading, shadow and pane together and cannot do that.

    HOW BIG `swag` MAY BE is set by the REVEAL, and round 16 corrected the reason
    without changing the number. Turning a leaf about its centre swings each
    stile lw/2 * sin(swag) in y. This used to say the cap came from the back --
    from the plate SM_Wall_TimberWin_2m backed its reveal with at y = 0.140 --
    and that stopped being true when the wall moved the plate to 0.200; the leaf
    now has 190 mm behind it, not 126. The cap comes from the FRONT and always
    did: glazing()'s frame face sits at y = +0.010, ten millimetres inside the
    hole, and the whole point of that is the wall's 56 mm of visible reveal. A
    leaf at lw = 0.47 turned by t degrees pushes one stile 0.2363*sin(t) proud,
    so y = 0 is reached at t = 2.43 -- and casement A measures y-min = -0.0011,
    i.e. it is already there. 2.5 is the number, 5 degrees between neighbours.

    AND IT IS A SMALL TELL, measured, so do not spend anything else on it: over
    three camera yaws the three lights' means differ by 0.5 to 5.0 of 255 (see
    ROUND 16 in the module docstring). A cosine is flat at 2.4 degrees. The thing
    that actually makes a leaded light read is the per-QUARRY step, s.d. 21 of
    255 inside one light; this rotation is a garnish on top of it.

    `swing` = {leaf_index: degrees} throws a leaf OPEN on its outer stile. It
    projects in -Y, which is not lapping, and it is the only way this kit can
    show an INTERIOR: behind an open leaf you see the blank, not a pane.

    WHY THE MULLION IS APPLIED and not asked of glazing(): its own mullions sit
    at depth - lead*2.2 and are 30 mm thick, so a mullion's BACK face lands
    0.015 - lead*0.75 from the leading's FRONT face -- under 5 mm of air at any
    usable lead section, and exactly zero at lead = 0.020. Both faces are large
    and Y-facing and this family wobbles, so every crossing of a lead over a
    mullion became a coincident patch. Here the leaves are physically apart by
    `gap` and the mullion is the post that covers the joint: it stands 6 mm
    proud of the sash face and runs back to the frame's own back plane, so it
    reads as structure in silhouette and the leaded net runs unbroken behind it.
    """
    r = rng(f"sash/{p.name}/{seed}")
    gm, gl = GLAZE[glaze]
    pitch = (x1 - x0) / cols
    # THE CAP IS THE INVARIANT, not the call site's taste. Read MULL_LAP: a
    # cover strip whose cheek lands within a millimetre or two of the jamb face
    # it covers is 899 cm2 of z-fight, and one that lands PAST it seals that face
    # inside oak. Every call site below is set to a width that already satisfies
    # this, so nothing is silently clamped today -- the clamp is here so a future
    # widening cannot quietly re-open the fault.
    mull = min(mull, _mull_max(gap)) if mull else mull
    lw = pitch - gap                       # a leaf's outer frame width
    aw, ah = lw - 2 * REACH, (z1 - z0) - 2 * REACH
    zc = (z0 + z1) / 2
    swing = swing or {}
    for i in range(cols):
        cx = x0 + pitch * (i + .5)
        phi = swing.get(i, 0.0)
        left = (i == 0)                    # which stile carries the hinges
        # A leaf that is THROWN open turns about its hinge; one that is merely
        # ajar turns about its own centre, so it stays inside the reveal.
        hx = ((-lw / 2) if left else (lw / 2)) if abs(phi) > 1e-6 else 0.0
        s = p.sub(f"{p.name}_leaf{seed}_{i}")
        # glazing() lays the frame, the oversize pane and the whole depth
        # ladder; `pattern="none"` hands the LEADING to _leaded, which re-strikes
        # the same lines and hangs a cushioned quarry between every four of them.
        # See the block above GLAZE for why the glass has to be geometry.
        s.glazing((-hx, 0.0, 0.0), (aw, ah), depth=depth, frame=FR, overlap=OV,
                  rebate=REB, lead=LEAD_W, cell=cell, pattern="none",
                  mullions=0, mat_glass=gm, mat_lead=gl, tint=tint)
        _leaded(s, -hx, 0.0, aw + 2 * REB, ah + 2 * REB, depth, cell, pattern,
                gm, gl, tint=tint, seed=seed * 17 + i,
                # a LIT light is emissive: emission ignores the normal, so a
                # cushion on it is tris that cannot change a pixel. Cames only.
                quarries=(glaze != "lit"))
        _shadow(s, -hx, 0.0, aw, ah, depth)
        ang = (-phi if left else phi) if abs(phi) > 1e-6 else \
              swag * (1 if i % 2 else -1) * r.uniform(.72, 1.0)
        p.merge(s, at=(cx + hx, y, zc), rot=(0, 0, ang))
    joints = [x0 + pitch * (i + 1) for i in range(cols - 1)]
    if mull:
        # THE MULLION'S BACK DIES AT THE FRAME'S MID-DEPTH -- ROUND 17.
        #
        # It went 10 mm PAST the frame's back plane, which was right about the
        # thing it was fixing (cut level with `depth - lead*2.6` it landed ON
        # that plane: 3166 cm2 across the family) and wrong about where it landed
        # instead. Behind the frame's back the strip runs into the one member
        # this family cannot move: `_shadow`'s occlusion band, whose own back
        # face sits at `depth - lead*1.45 - 0.002`, 8.7 mm further in. 8.7 mm
        # sounds like clearance until you remember the leaf is AJAR: the band's
        # side bars stand hw out from the leaf's centre line, so swag degrees of
        # rotation slides their back plane hw*sin(swag) = 8.0 mm in y. Measured,
        # casement A: mullion back 0.0732, band back swung to 0.0742 -- 1.02 mm
        # apart over 154 cm2, and it is only outside the 0.5 mm gate by luck of
        # the jitter draw.
        #
        # There is no room to go FURTHER back either: the band stops 2 mm short
        # of the came ridges at `depth - CAME_H`, so the whole corridor from the
        # frame's back to the glass is 10 mm wide and full.
        #
        # So the strip stops half way through the timber it laps, at glazing()'s
        # own frame-centre plane. Nothing else in the leaf has a face there:
        # ajar swing included, the nearest are the jamb's back at 0.054 and the
        # band's front at 0.053, both 18 mm off, and its own front face at
        # `mull_front` is clear of the jamb's swung front face.
        #
        # ROUND 18 MOVED `mull_front` 2 mm FORWARD, off the trim plane. At .004
        # it was the SAME plane as `_cover`'s front face, and the strip laps
        # every head/foot band by the 10 mm those bands lap the sash: two large
        # Y-facing oak faces, coplanar by construction, wherever they cross.
        # Measured at 0.5 mm: 8.5 cm2 on the shuttered light (sep 0.128 mm) and
        # 2.2 cm2 on the dormer (0.151 mm, and the most OPEN pair in the family
        # -- 48.7% of a hemisphere escapes it). A, B and C were outside the gate
        # by nothing but the jitter draw, which is the same "only outside by luck"
        # this function's own MULL_LAP note was written about. At .002 the strip
        # stands 2 mm PROUD of the band -- which is what an applied mullion post
        # over a cover band looks like anyway -- and still sits 3 mm behind the
        # furthest a jamb swings forward (measured y-min -0.0011 on casement A).
        # SEALED, AND SAYING SO: over the 34.5 mm it laps each jamb, this back
        # face is now inside that jamb's timber rather than in the air behind it.
        # That is a lapped joint and not a hidden fight -- the face it used to
        # nearly-coincide with is still there, still visible, 38 mm away -- but
        # it is a face buried in a solid and it is the one place in this round
        # where that is the answer.
        # WHAT IS LEFT HERE, MEASURED, AND WHY IT IS STILL HERE. The strip runs
        # the full sash band, z0..z1, and glazing() puts its frame's outer edge
        # on that same z -- so where the strip crosses the frame's head or sill
        # member, the strip's END face and that member's END face are one plane.
        # Round 18 measured it at 0.5 mm with no area floor: 10 pairs, 44.6 cm2,
        # of which 12.9 cm2 is ray-reachable (C 3.7, bay 4.0, arch 5.2, patches
        # of 1.3-2.1 cm2 each) and it is ALL of the reachable coincidence left in
        # the family. It was left, deliberately:
        #   * SHORTENING the strip puts its end face inside the frame member --
        #     sealing a fight, which this project rates worse than the fight;
        #   * LENGTHENING it past z1 pokes it into five different pieces' head
        #     trim (C's dentil course at z1+0.020, the dormer's 0.032 band, the
        #     arch's stone head), i.e. new interpenetration in geometry that is
        #     not the fault. In A and B the head/foot bands already lap the strip
        #     by 10 mm, which is why those two carry the same joint at 0%;
        #   * the plane itself is glazing()'s (`fo`/`yf` in util.py), the same
        #     one as its deliberate jamb-butts-between-head-and-sill joint, which
        #     is 666 cm2 of this family's 788 and 0.0% reachable.
        # A chamfered end would clear it for +8 tris a strip. Say so, do not do
        # it blind: it is 1.6% of the family and two oak faces 3% apart in tint.
        mb = depth - LEAD_W * 2.6 - .0275
        for x in joints:
            p.box((x, y + (mull_front + mb) / 2, zc),
                  (mull, mb - mull_front, z1 - z0),
                  mull_mat, bevel=.008, seg=1, tint=tint, shade=1.04)
    return joints


def _cover(p, cx, cz, w, h, y=.004, d=.030, mat="oak_dark", tint=.05,
           shade=1.02, bevel=.009):
    """A flat cover band across the head or the foot of a sash, INSIDE the
    reveal. It is what ties a run of separate leaves into one window, and it is
    the modest, in-the-hole descendant of the head board and the cill this
    family used to hang on the wall face outside the opening. Its back laps into
    the frame it covers; its front never crosses y = 0."""
    p.box((cx, y + d / 2, cz), (w, d, h), mat, bevel=bevel, seg=1, tint=tint,
          shade=shade)


def _interior(p, cx, cz, aw, ah, y0=.068, y1=Y_IN - .004, g=.030,
              mat="oak_dark", tint=.03):
    """What you see through an OPEN leaf. A flat plate at the back of the reveal
    is a wall, not a room, so this is a shallow open-fronted box: four splayed
    inner faces running back from the sash line to the blank, each catching a
    different amount of light, with the blank closing it. From 3 m it reads as
    depth into the building, which is the "no interior" half of the critique."""
    hw, hh = aw / 2, ah / 2
    # The four liners are at four DIFFERENT depths. They meet at the corners --
    # any box lining a rectangle does -- and cut to one y span the head and the
    # side shared both of their y planes there, which check_zfight scored at
    # 24 cm2 a corner. Stepping them 5 mm apart in y makes every corner a lap,
    # and it costs nothing: it also gives the four faces of the recess four
    # slightly different shadow lines, which is what makes a hole read as a room.
    # ROUND 18 STOPPED THE SIDE LINERS BETWEEN THE HEAD AND FOOT ONES, 3 mm
    # CLEAR, and the y step above is no longer what keeps the corner honest.
    # The side liners used to over-run by 1.5g so the corner read as a lap, and
    # the 5 mm y step meant their FRONT faces were not coplanar with the head's.
    # Their BACK faces were: all four ran to y1, so every corner carried a
    # 30 x 30 mm patch of coplanar back face -- 4 pairs, 36.0 cm2, and the
    # harness scored all 36 RAY-REACHABLE through the 4 mm slot in front of the
    # blank. Stepping the backs apart the same way would only swap the fight for
    # a face sealed inside the neighbouring liner, and shortening them onto the
    # head liner's underside would butt two 30 x 70 mm faces instead. So the side
    # liners now stop 3 mm short at BOTH ends: no shared plane, nothing buried,
    # and the 3 mm slot at each corner looks at the blank 4 mm behind it. It also
    # raises their bottoms well clear of timber_walls' internal window board
    # (they used to reach z = 0.044 against a board rising to 0.030, and the
    # reason that 14 mm mattered is the note below).
    for k, (bx, bz, bw, bh, sh) in enumerate(
            ((0.0, hh + g / 2, aw + 2 * g + .020, g, .30),
             (0.0, -hh - g / 2, aw + 2 * g + .020, g, .46),
             (-hw - g / 2, 0.0, g, ah - .006, .38),
             (hw + g / 2, 0.0, g, ah - .006, .22))):
        ya = y0 + .005 * k
        p.box((cx + bx, (ya + y1) / 2, cz + bz), (bw, y1 - ya, bh), mat,
              bevel=0, tint=tint, shade=sh)


def _head_close(p, w, z0, z1, y0=.010, d=Y_TRIM_BACK - .010, mat="oak_mid",
                shade=.74, tint=.05):
    """Close the top of the reveal above the window's own head trim.

    FAULT 3, THE OTHER HALF OF IT. An insert whose head trim stops short of the
    opening's head leaves the WALL's reveal showing across the full width of the
    hole -- and the wall backs its reveal 140 mm deep, so what shows is a black
    band. Measured against the real SM_Wall_TimberWin_2m: 254 mm of it over the
    old casement A, 170 over the bay, 300 over the shuttered light beside its
    crest, 121 over casement C above its lintel. In a render that is not a
    shadow line, it is a hole between the window and the wall, and it is what
    reads as "gaps between the window beams and the render".

    So every leaf now lines its own head: a plain board across the opening,
    sitting just inside the reveal (10 mm) so it catches the same light as the
    wall face, well in front of the wall's own backing plate at 0.140, and
    behind all of the proud trim that laps over it.

    ROUND 15 MADE IT A FULL-DEPTH LINING. It was 62 mm deep, which closed the
    reveal's FACE and left 78 mm of void behind it -- and the head-slot audit
    ("looking straight into a 141 mm-deep hole") is about exactly that void, not
    about the face. It now runs back to Y_TRIM_BACK, the deepest this family may
    reach without meeting the wall's backing plate, so the void behind any head
    trim in the family is 24 mm instead of 78-106. Same 12 tris."""
    if z1 - z0 < .012:
        return
    p.plate((0, y0 + d / 2, (z0 + z1) / 2), (w, d, z1 - z0), mat, tint=tint,
            shade=shade)



def _crest(p, cx, cz, cw, mat="oak_mid", tint=.06, y_front=-.042, depth=.068,
           tall=.46):
    """The carved crest over ref2's dormer and gable lights. Off the ref3
    linework it is NOT a wide pediment: a narrow moulded base band, two small
    volutes stepping in, then a pointed centre spike with a boss on it."""
    h = cw * tall
    hx = cw / 2
    prof = [(-hx, 0.0), (hx, 0.0),
            (hx, .19 * h), (.74 * hx, .25 * h), (.68 * hx, .50 * h),
            (.44 * hx, .55 * h), (.30 * hx, .70 * h), (.135 * hx, .75 * h),
            (.105 * hx, .90 * h), (0.0, h),
            (-.105 * hx, .90 * h), (-.135 * hx, .75 * h), (-.30 * hx, .70 * h),
            (-.44 * hx, .55 * h), (-.68 * hx, .50 * h), (-.74 * hx, .25 * h),
            (-hx, .19 * h)]
    p.prism(prof, depth, mat, axis='Y', at=(cx, y_front + depth / 2, cz),
            bevel=.005, seg=1, tint=tint, shade=1.05)
    # The boss is let INTO the crest -- sat on its face, its back and the crest's
    # front were 2mm apart. It is now 44mm deep rather than 30mm with the same
    # front plane, so its back cap dies 21mm inside the crest instead of 7mm:
    # at 7mm its back plane landed within 0.3mm of a timber-wall member once the
    # piece was snapped into a wall, which is 18 cm2 of coincidence that only
    # exists in the assembly.
    p.cyl((cx, y_front - .001, cz + h * .40), cw * .062, .044, mat, sides=7,
          axis='Y', tint=tint, shade=1.12)
    return h


def _corbel(p, x, z_top, out, drop, thick, mat="oak_mid", tint=.06, rake=0.0,
            y0=0.0, shade=1.0):
    """Scroll corbel under a cill or bay floor. `rake` drops the tip so the same
    profile also tucks under a sloping hood."""
    prof = [(y0, z_top), (y0, z_top - drop),
            (y0 - out * .26, z_top - drop * .93 - rake * .26),
            (y0 - out * .52, z_top - drop * .66 - rake * .52),
            (y0 - out * .74, z_top - drop * .36 - rake * .74),
            (y0 - out * .91, z_top - drop * .13 - rake * .91),
            (y0 - out, z_top - rake)]
    return p.prism(prof, thick, mat, axis='X', at=(x, 0, 0), bevel=.007, seg=1,
                   tint=tint, shade=shade)


def _strut(p, x, z_top, out, drop, thick, mat="oak_mid", tint=.07, y0=0.0,
           w=.056, over=.058, shade=.93):
    """ref3's hood bracket is NOT a scroll corbel: it is a straight raking strut
    from the wall down to the hood's front edge, its tip cut off square and
    poking `over` past the fascia, with a short pendant drop hanging under the
    tip. Read straight off the greyscale linework."""
    a = (x, y0 - .010, z_top)
    L = sqrt(out * out + drop * drop)
    ux, uz = -out / L, -drop / L
    b = (x, y0 - .010 + ux * (L + over), z_top + uz * (L + over))
    p.beam(a, b, thick, w, mat, bevel=.008, seg=1, tint=tint, shade=shade)
    # pendant drop and wall pad are deliberately 8mm narrower / wider than the
    # strut: at thick*0.84 and thick*1.05 their cheeks sat 1-2mm off its own
    p.box((x, b[1] + .012, b[2] - .052), (thick * .70, .050, .108), mat,
          bevel=.008, seg=1, tint=tint, shade=shade * .96)
    p.box((x, y0 + .012, z_top - .026), (thick * 1.30, .058, .092), mat,
          bevel=.008, seg=1, tint=tint, shade=shade * 1.06)


def _hood(p, cx, z_back, width, out, drop, mat="oak_mid", n=4, thick=.042,
          y_back=.015, tint=.075, brackets=True, seed=0, verge=True,
          strut=False, inset=.150):
    """Plank pent hood -- ref2's signature over an upper-storey light. Boards run
    along X and lie on the slope, a deep fascia caps the front edge, raking
    verge boards close the ends, two brackets carry it off the wall."""
    r = rng(f"hood/{seed}/{cx:.2f}")
    ang = atan2(drop, out)
    L = sqrt(out * out + drop * drop)
    tilt = degrees(ang)
    F = (cx, y_back - out, z_back - drop)
    uy, uz = cos(ang), sin(ang)             # front -> back, up the slope
    ny, nz = -sin(ang), cos(ang)            # outward normal of the boards
    bl = L / n
    for i in range(n):
        s = bl * (i + .5)
        c = (F[0], F[1] + uy * s + ny * thick * .5, F[2] + uz * s + nz * thick * .5)
        p.box(c, (width, bl - .019, thick), mat,
              bevel=.009, seg=1, tint=tint, rot=(tilt, 0, 0),
              shade=1.0 + r.uniform(-.10, .07))
    # front fascia -- a thin lip, not a beam: ref3's hood edge is a board edge.
    # It runs 10mm UP the slope past the first board's front edge so that edge
    # dies inside it: level with it, the two shared a plane and fought (113 cm2
    # of it on casement B, and the same on the bay's pent roof).
    p.box((F[0], F[1] + ny * .014, F[2] - .026 + nz * .014),
          (width + .026, .062, .068), mat, bevel=.009, seg=1, tint=tint,
          rot=(tilt, 0, 0), shade=.90)
    if verge:
        ext = .072                       # verge boards poke out past the fascia
        for sx in (-1, 1):
            s = L * .5 - ext * .5
            # lapped 8mm over the board ends: flush, they shared a plane with
            # them, and stepping the board widths just moved the problem around
            c = (F[0] + sx * (width / 2 + .007),
                 F[1] + uy * s + ny * thick * .55, F[2] + uz * s + nz * thick * .55)
            p.box(c, (.030, L + ext, thick * 2.3), mat, bevel=.008, seg=1,
                  tint=tint, rot=(tilt, 0, 0), shade=.95)
    # back flashing board against the wall -- wider than the boards so its ends
    # are not in the same plane as theirs
    p.box((cx, y_back - .026, z_back + .020), (width + .030, .052, .046), mat,
          bevel=.008, seg=1, tint=tint, shade=1.05)
    if brackets:
        for sx in (-1, 1):
            if strut:
                _strut(p, cx + sx * (width / 2 - inset), z_back - .030,
                       out - .014, drop, .054, mat=mat, tint=tint, y0=y_back)
            else:
                _corbel(p, cx + sx * (width / 2 - .085), z_back - .022,
                        out * .80, .275, .052, mat=mat, tint=tint,
                        rake=drop * .80, y0=y_back, shade=.93)
    return z_back + .044


def _shutter(p, hinge_x, z0, z1, sw, phi, side, mat="oak_mid", seed=0,
             at_w=None, u0=.010, ledgers=True, pintles=True, planks=2,
             hinge_y=0.0, face=1):
    """One plank leaf, hinged at (hinge_x, hinge_y) and swung `phi` degrees off
    the wall plane. Local x runs out along the leaf from the hinge, local -y is
    away from the wall, so a leaf's direction is (side*cos phi, -sin phi) and a
    FOLDED partner is the same call at phi + 180 hung on this one's tip.

    The iron ledgers are let 6mm INTO the boards. Sitting them 2mm off the board
    face -- which is what they did -- is a coincident pair with the whole plank
    face behind it.

    THE BOARDS ARE NOT util.planks(), and it is a tri-budget decision, measured:
    planks() takes no `seg`, so every board is a 2-segment bevel at 108 tris.
    A shuttered light now carries FOUR leaves rather than two (see shuttered()),
    and at 108 a board that is 432 tris of bevel on a piece with 236 to spare.
    Same board, same jitter, seg=1: 44. Everything else about them is planks().
    """
    s = p.sub(f"{p.name}_shut{seed}")
    r = rng(f"shutter/{p.name}/{seed}")
    th = .040
    fs = 1 if face >= 0 else -1             # which side of the leaf is boarded
    w0 = fs * (-th - .004) if at_w is None else at_w
    sh = z1 - z0
    bw = sw / planks
    for i in range(planks):
        d = th * (1 + r.uniform(-.15, .15) * .5)
        s.box((u0 + bw * (i + .5), w0 + fs * d / 2, sh / 2), (bw - .012, d, sh),
              mat, bevel=.009, seg=1, tint=.075,
              shade=1.0 + r.uniform(-.06, .06))
    if ledgers:
        # 20 mm of iron, 4 mm of it let INTO the boards. It used to be a 44 mm
        # slab standing 34 mm off the face -- which is not a ledger, it is a
        # beam, and on a folded leaf standing square to the wall those 34 mm
        # came straight off the piece's x envelope (measured: 62 mm over).
        for f in (.16, .81):
            s.box((u0 + sw * .50, w0 - fs * .006, sh * f), (sw * .96, .020, .026),
                  "iron", bevel=.005, seg=1, tint=.04)
    if pintles:
        for f in (.16, .81):                   # hinge pintles on the jamb edge
            s.cyl((u0 - .006, w0 + fs * th * .45, sh * f), .021, .070, "iron",
                  sides=6, axis='X', tint=.04)
    p.merge(s, at=(hinge_x, hinge_y, z0), rot=(0, 0, phi if side < 0 else -phi),
            mirror='X' if side < 0 else None)
    a = radians(phi)
    return (hinge_x + side * (u0 + sw) * cos(a), hinge_y - (u0 + sw) * sin(a))


def _planting(p, at, size, seed, n=30, nf=16, drape=0, mat="moss"):
    """Foliage mound for a flower box: cards laid on a squashed dome (golden
    angle so it never stripes), then flower dots on the outer shell. Cheap, and
    from 3m it reads exactly like ref2's boxes."""
    r = rng(f"plant/{seed}")
    sx, sy, sz = size
    for i in range(n):
        t = (i + .5) / n
        a = 2.39996 * i
        rad = sqrt(t)
        px = at[0] + cos(a) * rad * sx
        py = at[1] + sin(a) * rad * sy
        pz = at[2] + (1.0 - rad * rad * .85) * sz - r.uniform(0, sz * .30)
        c = .092 * (1.22 - .40 * rad) * r.uniform(.76, 1.24)
        p.box((px, py, pz), (c, c * .12, c * .74), mat, bevel=0,
              rot=(r.uniform(-52, 8), 0, r.uniform(0, 180)), tint=.18,
              shade=.90 + r.uniform(-.28, .40))
    for i in range(drape):                     # trailing strands down the front
        tx = at[0] + lerp(-sx, sx, (i + .5) / max(drape, 1)) + r.uniform(-.03, .03)
        ln = r.uniform(.16, .34)
        for k in range(3):
            c = .086 * r.uniform(.72, 1.12)
            p.box((tx + r.uniform(-.03, .03), at[1] - sy * .85 - .012,
                   at[2] - .02 - ln * (k + .5) / 3),
                  (c, c * .12, c * .80), mat, bevel=0,
                  rot=(r.uniform(-80, -40), 0, r.uniform(0, 180)), tint=.16,
                  shade=1.0 + r.uniform(-.28, .26))
    for i in range(nf):
        a = 2.39996 * (i + .37)
        rad = sqrt((i + .6) / nf) * .95
        fx = at[0] + cos(a) * rad * sx
        fy = at[1] + sin(a) * rad * sy
        fz = at[2] + (1.0 - rad * rad * .8) * sz + r.uniform(-.02, .05)
        m = "flower_red" if i % 3 else "flower_gold"
        c = r.uniform(.028, .042)
        p.box((fx, fy, fz), (c, c * .60, c), m, bevel=0,
              rot=(r.uniform(-34, 34), 0, r.uniform(0, 180)), tint=.10,
              shade=1.0 + r.uniform(-.12, .16))


# ------------------------------------------------------- leaded casements ----
# EVERY LEAF BELOW IS BUILT TO THE SAME ENVELOPE, and the layout numbers are
# shared so a change of mind is one edit rather than five. Z_S0/Z_S1 is the sash
# band; the head and foot bands LAP it by 10 mm in z rather than butting to it,
# because two members meeting on one plane inside a 20 mm reveal is exactly the
# coincident pair this family has spent four rounds hunting.
Z_BAND = .034                    # head / foot cover band height
Z_S0, Z_S1 = .024, H - .024      # 0.024 .. 1.386: the sash band
SH_W = W / 4                     # 0.365 -- a shutter leaf is A QUARTER of the
                                 # light, so a bi-fold pair a side closes it
SH_HINGE = .686                  # ...hung on the reveal edge, not the sash stile
SH_FOLD = 12.0                   # how far the folded leaf splays off its partner
SH_LAP = .066                    # and how far off its partner's centreline it
                                 # hangs: one slab plus 6 mm of air


def _frame_bands(p, top=H, w=W, tint=.05):
    """The head and foot bands that tie a run of separate leaves into one
    window. NOT a cill and NOT a head board: both live at y = 0.004..0.034, i.e.
    INSIDE the hole, and neither projects past the wall face or past the
    opening's edge. The wall carries the cill, its nose, the head and its drip
    mould -- see the header. This is the sash's own bottom rail and head rail,
    which is a different member in a different place."""
    _cover(p, 0, Z_BAND / 2, w, Z_BAND, tint=tint, shade=.94)
    _cover(p, 0, top - Z_BAND / 2, w, Z_BAND, tint=tint, shade=1.06)
    # ...and the board that closes what is BEHIND the head rail. Lapped 4 mm
    # inside the rail's own back face rather than butted to it.
    _head_lining(p, w, top, .030)


def casement_a():
    """THE upper-storey workhorse, and the piece this family gets judged on.

    Three TALL narrow diamond-leaded lights -- ref1's proportion -- dark glass
    and pale leads, in one 1.46 x 1.41 sash that fills SM_Wall_TimberWin_2m's
    reveal and stops dead at its edge.

    ROUND 14 TOOK THE WALL'S TRIM OFF IT. It measured 1.70 m wide in a 1.50 m
    hole, and none of the 200 mm was glazing: an 0.082 architrave down each side
    lapping 35 mm onto the plaster, a 1.62 m cill standing 86 mm proud of the
    wall face directly over the wall's OWN sill nose, a 1.64 m head board and a
    1.70 m moulded drip band over the wall's own drip mould. Every one of those
    is a member SM_Wall_TimberWin_2m already builds, drawn a second time 70 mm
    away from it -- which is the doubled sill and the "various overlapping wood
    pieces". They are gone. What is left is joinery: three leaves hung ajar, two
    mullion posts and the head and foot bands, all inside the hole. Nothing of
    it laps the wall face: the furthest forward anything reaches is 1 mm, where
    a leaf hung ajar swings its stile past y = 0."""
    p = Part("SM_Win_LeadedCasement_A", budget="window",
             seams=dict(x=(-XO, XO), y=(0.0, T_T), z=(Z0, Z1)))
    _blank(p, W, H)
    _sash(p, -XO, XO, Z_S0, Z_S1, 3, .120, "diamond", "dark", seed=1,
          swag=2.5, mull=_mull_max(.014))     # .083 -- see MULL_LAP
    _frame_bands(p)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())


def casement_b():
    """THE OPEN CASEMENT, and that is this piece's new job.

    B used to be A under a plank pent hood, and the hood is exactly what the
    measurement caught: 1.76 m of projecting roof over a 1.50 m hole, hung
    250 mm proud of the wall on two raking struts -- straight through the wall's
    own drip mould, which SM_Wall_TimberWin_2m builds at the head of every
    win_upper opening BECAUSE ref3's pent hood no longer fits under the wall
    plate. Two hoods, 70 mm apart. The wall's stays; ours goes.

    That left B needing an identity, and the critics named the one thing the
    whole family was missing: "no interior". A kit with no transparent glass can
    only show an interior through an opening with no glass in it -- so B's left
    leaf is thrown OPEN 15 degrees on its outer stile, and `_interior` lines the
    reveal behind it with a splayed dark box instead of a flat plate. Open, the
    leaf projects 185 mm in -Y and its free stile swings INWARD to x = -0.04, so
    the piece still measures 1.46 across. Swinging out is not lapping."""
    p = Part("SM_Win_LeadedCasement_B", budget="window",
             seams=dict(x=(-XO, XO), y=(-.21, T_T), z=(Z0, Z1)))
    _blank(p, W, H)
    # the interior goes in FIRST, so the open leaf is stamped over it. y0 is
    # behind the frame's own back plane (0.065) so it can never share a plane
    # with the mullion post standing beside it.
    aw = W / 2 - .014 - 2 * REACH
    _interior(p, -XO + W / 4, (Z_S0 + Z_S1) / 2, aw, Z_S1 - Z_S0 - 2 * REACH,
              y0=.068)
    _sash(p, -XO, XO, Z_S0, Z_S1, 2, .155, "square", "cool", seed=2,
          swag=2.5, mull=_mull_max(.014), swing={0: 15.0})
    _frame_bands(p)
    # the casement stay -- the iron bar that holds a leaf open. Small, and it is
    # what tells the eye the leaf is OPEN rather than missing.
    p.beam((-.20, .016, Z_S0 + .086), (-.06, -.140, Z_S0 + .062),
           .018, .018, "iron", bevel=0, tint=.04)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())


def casement_c():
    """The LIT variant -- ref1's one lit window: slim diamond quarries over warm
    amber, under a heavy oak lintel with a dentil tooth course.

    C measured 1.60 in a 1.50 hole, and the 100 mm was its two architraves plus
    a 1.60 m cill laid over the wall's sill. THE LINTEL STAYS, because a heavy
    head is what makes this variant read at distance -- but it is carried in the
    top 0.22 m OF THE HOLE now, at y = 0.004..0.076, instead of hung across the
    wall face above it where SM_Wall_TimberWin_2m's head plate already is."""
    p = Part("SM_Win_LeadedCasement_C", budget="window",
             seams=dict(x=(-XO, XO), y=(0.0, T_T), z=(Z0, Z1)))
    _blank(p, W, H)
    z1 = H - .215                              # 1.195: top of the sash
    _sash(p, -XO, XO, Z_S0, z1, 2, .106, "diamond", "lit", seed=3,
          swag=2.4, mull=.062, mull_mat="oak_mid")
    _cover(p, 0, Z_BAND / 2, W, Z_BAND, shade=.94)
    # tooth course over the sash, lapping BOTH the sash head below it and the
    # lintel above it, so neither joint is two faces meeting on one plane
    p.dentil((-W / 2 + .050, W / 2 - .050), z1 + .020, .030, "oak_dark",
             step=.112, size=(.050, .056, .056), tint=.05)
    # the lintel: full width of the insert, dying on the reveal's edge
    p.box((0, .040, H - .085), (W, .072, .170), "oak_dark", bevel=.013, seg=1,
          tint=.055, shade=1.05)
    # ...and the lining behind it, lapped 4 mm inside the lintel's back face
    _head_lining(p, W, H, .072, h=.170)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())


# ------------------------------------------------------------- shuttered -----
def shuttered():
    """Ref2's shuttered light: a carved crest over the sash head and plank
    shutters standing open, with iron ledgers and pintles.

    THE SHUTTERS ARE IN THE REVEAL NOW. Thrown back flat against the wall they
    reached x = +/-0.96 -- two thirds of the way into the neighbouring bay,
    where the next window's shutters are -- and the bi-fold pair that replaced
    them still measured 1.93 across a 1.50 hole. Hinged on the sash stiles
    instead and swung back nearly square to the wall, each leaf projects
    ~370 mm in -Y and the pair's tip lands inside x = 0.72: open shutters
    standing in the mouth of the opening, which is what a 100 mm reveal does to
    a shutter anyway. The crest came down inside the hole with them, and
    `_head_close` lines the strip of reveal it does not cover.

    ROUND 15 MADE THEM SHUTTERS THAT COULD SHUT -- two bi-fold pairs of W/4
    rather than one 0.262 leaf a side. The arithmetic is under the loop."""
    p = Part("SM_Win_Shuttered", budget="window",
             seams=dict(x=(-XO, XO), y=(-.40, T_T), z=(Z0, Z1)))
    _blank(p, W, H)
    zh = H - .268                              # the crest sits over the sash
    _sash(p, -XO, XO, Z_S0, zh, 2, .165, "square", "cool", seed=4,
          swag=2.4, mull=_mull_max(.014))
    _cover(p, 0, Z_BAND / 2, W, Z_BAND, shade=.94)
    _head_close(p, W, zh - .008, H)
    _cover(p, 0, zh - .010, W, .040, shade=1.06)
    _crest(p, 0, zh + .006, .58, tall=.44, y_front=.004, depth=.056)
    # ---- THE SHUTTERS, AND THEY CLOSE NOW --------------------------------
    # MEASURED FAULT: "each shutter is 0.262 m wide; a quarter of the 1.46 m
    # light is 0.365 m. The pair covers 36% of the opening and could never close
    # it." The docstring above has claimed "a quarter of the light each so a
    # folded pair could still close it" since round 14 -- but there was no folded
    # pair, only one leaf a side, and each measured 0.262 rather than a quarter.
    # Two leaves at 0.262 is 0.524 of a 1.460 light: 35.9%.
    #
    # A BI-FOLD PER SIDE fixes it, and it is what a 100 mm reveal wants anyway:
    # two leaves of exactly W/4, jamb-leaf-to-leaf, so shut the four of them
    # measure 4 x 0.365 = 1.460 = the light, dead on.
    #
    # THREE NUMBERS DECIDE THE REST, and they are coupled:
    #   * SH_HINGE. Coverage is set by the HINGE, not by the leaf width: a closed
    #     leaf runs inward from its pintles, so a pair reaches SH_HINGE - u0
    #     whatever it measures. Hung off the sash stile at 0.598 the old leaves
    #     could not have covered the glass even at double the width. They hang on
    #     the reveal edge now and reach +/-0.676, against a glazed aperture that
    #     ends at +/-0.678: the shutters cover the glass.
    #   * the swing angle. Nothing may leave x = +/-XO (round 14's envelope, and
    #     it is what keeps a shutter out of the next bay), and a leaf reaches
    #     SH_HINGE + (u0 + sw)*cos(phi). At sw = W/4 that forces 84 deg -- which
    #     is roughly where the old 73 deg leaves already were in silhouette, and
    #     it is the price of a leaf that is half a light instead of a fifth.
    #   * SH_LAP. The folded leaf hangs off its partner's FACE, not its
    #     centreline -- offset by the slab thickness along the way the boards
    #     look, which is what a real knuckle does. Cut to the centreline the two
    #     leaves' boards occupied the same 44 mm of space for their whole length
    #     (they fold at 12 deg, so the lines stay inside a slab of each other),
    #     AND the folded leaf hung 62 mm outside the piece's x envelope. Offset,
    #     it folds BACK-TO-BACK -- ledgers outward, the way a shutter has to fold
    #     if it is to fold at all -- clear of its partner by 6 mm and clear of
    #     the envelope by 10.
    lz0, lz1 = .062, zh - .026
    for sx, phi, sd in ((-1, 84.5, 3), (1, 83.5, 5)):
        tip = _shutter(p, sx * SH_HINGE, lz0, lz1, SH_W, phi, sx, seed=sd)
        a = radians(phi)
        _shutter(p, tip[0] - sx * sin(a) * SH_LAP, lz0, lz1, SH_W,
                 180.0 + phi - SH_FOLD, sx, seed=sd + 40,
                 hinge_y=tip[1] - cos(a) * SH_LAP, pintles=False, face=-1)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())


# -------------------------------------------------------------- bay window ----
def bay():
    """The wide mullioned bay: a shallow oriel stepping out 0.215, three lights
    under one head, boarded splay cheeks and a plank pent roof.

    THE ONE PIECE THE BRIEF LETS OVERSAIL -- but only in -Y. It measured
    1.57 x 1.67 against a 1.50 x 1.45 hole and neither number was the oriel: the
    width was a 1.54 m cill and two jambs lapping 35 mm onto the plaster, and the
    220 mm of extra height was a pent roof standing above the opening plus two
    corbels hanging 230 mm BELOW it, over the wall's own sill band. The part of a
    bay that enters the wall has to fit the hole, so:

      * the corbels are gone and the bay is CANTED instead -- its underside
        rakes from the reveal at z = 0 out and up to the front at z = 0.115,
        which is how a shallow oriel is carried anyway and needs nothing hung on
        the wall below the sill (which is the wall's member, not ours);
      * the pent roof lives in the top 0.25 m OF THE HOLE and oversails forward,
        not upward;
      * the cheeks die on the reveal edge at x = +/-0.73 with spec's 20 mm
        shadow gap, instead of lapping past it onto the plaster.

    1.46 x 1.41 in the wall plane; 0.34 m of projection in front of it."""
    proj = .215
    fx = .500                                  # half-width of the flat face
    fz0, fz1 = .188, H - .262
    p = Part("SM_Win_BayMullion", budget="window",
             seams=dict(x=(-XO, XO), y=(-.34, T_T), z=(Z0, Z1)))
    _blank(p, W, H)

    # ---- the canted bottom: one wedge from the reveal out to the oriel floor
    p.prism([(.014, .002), (-proj - .030, .116), (-proj - .030, .178),
             (.014, .178)], W - .022, "oak_mid", axis='X', at=(0, 0, 0),
            bevel=.010, seg=1, tint=.06, shade=.92)
    # front nosing, lapped 14 mm back over the wedge so no face is shared
    p.box((0, -proj - .036, .146), (2 * fx + .120, .050, .066), "oak_mid",
          bevel=.010, seg=1, tint=.06, shade=1.04)

    # ---- three-light face, out at y = -proj
    # TWO lights, not three, and it is the tri budget that says so: a leaf's
    # frame is four bevelled boxes = 432 tris, so a third light costs 610 and
    # this piece also has to pay for two splay cheeks and a pent roof. Two
    # lights either side of one chunky mullion is ref2's own reading of
    # a bay anyway, and it leaves 250 tris of headroom instead of 140 over.
    _sash(p, -fx, fx, fz0, fz1, 2, .140, "square", "cool", y=-proj, seed=5,
          swag=2.6, mull=.062, mull_front=-.030, mull_mat="oak_mid")
    _cover(p, 0, fz1 + .012, 2 * fx + .078, .046, y=-proj - .014, d=.042,
           mat="oak_mid", shade=1.05)

    # ---- boarded splay cheeks, reveal edge to face
    for sx in (-1, 1):
        a = (sx * (XO - .006), 0.0)
        b = (sx * (fx + .026), -proj)
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = sqrt(dx * dx + dy * dy)
        th = degrees(atan2(dy, dx))
        nx, ny = (dy / L) * sx, (-dx / L) * sx   # outward normal of the cheek
        for k in range(3):
            t = (k + .5) / 3.0
            cx_, cy_ = lerp(a[0], b[0], t), lerp(a[1], b[1], t)
            p.box((cx_ + nx * .021, cy_ + ny * .021, (fz0 + fz1) / 2),
                  (L / 3 - .009, .042, fz1 - fz0 - .044), "oak_mid",
                  bevel=.008, seg=1, tint=.075, rot=(0, 0, th),
                  shade=.90 + .05 * k)
        for z, sh in ((fz0 + .044, .92), (fz1 - .044, 1.04)):
            p.box((a[0] + dx / 2 + nx * .042, a[1] + dy / 2 + ny * .042, z),
                  (L * 1.02, .052, .062), "oak_mid", bevel=.008, seg=1,
                  tint=.065, shade=sh, rot=(0, 0, th))
        # the reveal return: the cheek dies into a board standing in the mouth
        # of the opening whose OUTER face IS the insert's own edge. It laps
        # nothing -- spec's 20 mm clearance to the wall's reveal is the shadow
        # gap that makes the bay read as set into the wall rather than on it.
        p.box((sx * (XO - .042), .076, (fz0 - .014 + H - .010) / 2),
              (.084, .144, H - .010 - fz0 + .014), "oak_mid", bevel=.009,
              seg=1, tint=.065)

    # ---- plank pent roof, inside the hole in x and z, oversailing in -Y
    _head_close(p, W - .008, fz1 + .026, H)
    _hood(p, 0, H - .078, W - .076, proj + .092, .150, n=4, thick=.040,
          brackets=False, seed=2)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())



# ------------------------------------------------------ arched stone light ----
def arch_stone():
    """Ground-storey light for OPENINGS.win_ground -- AN INSERT ONLY.

    This piece used to carry its own dressed stone surround: nine voussoirs, a
    keystone, three jamb blocks a side, two spandrel stones and a heavy cill
    band. But SM_Wall_StoneWindow_2m already builds exactly that -- toothed
    ashlar jambs, a stone_pale voussoir ring, keystone and the sill string
    course -- because the WALL is what carries the masonry. Snapped together you
    got two arch rings 25mm apart, two cills and two sets of jambs, which is the
    doubled arc and the weird visuals reported off the model. Everything stone
    is gone from here; the wall provides it.

    What is left is the joinery that fills the reveal: a square-headed
    Part.glazing() unit up to the springing, a bent timber head band with a
    radiating fan over it, and a dark blank behind. Sized to the opening less
    INSERT_CLEAR all round (0.76 x 1.21), with its arched head struck concentric
    with the wall's so the 20mm clearance is even the whole way round the arc.

    THE 20 mm SHADOW GAP ROUND THIS PIECE IS DELIBERATE AND STAYS. spec's
    INSERT_CLEAR is law, and the stone families carry their own dressed surround,
    so unlike the timber-wall leaves this one does NOT lap a timber lip out onto
    the masonry: the glazing frame's outer edge stops dead on r_in, 20 mm inside
    the wall's reveal, all the way round.

    WHY THE HEAD IS NOT GLAZED BY Part.glazing(). The primitive strikes
    RECTANGULAR openings, and this light's head is a semicircle. Rather than fork
    it (which is how five families grew five different glazing bugs), the glazed
    part is the square-headed light below the springing and the arch above it is
    joinery: the bent head band, a radiating fan on a hub, and a dark recessed
    tympanum behind them, which is what an unlit fanlight reads as anyway.

    Rendered against the real SM_Wall_StoneWindow_2m there is now ONE arch: the
    wall's stone ring, a 20 mm shadow gap, then the window's own bent head. The
    two things that still doubled it were subtler than the old stone surround
    and both are gone -- the head was built as a ring of oak VOUSSOIRS (jointed
    wedges echoing the masonry outside it), and the fan bars floated clear of
    everything, which is the second half of the "weird visuals".
    """
    ow, oh = S.OPENINGS["win_ground"]["w"], S.OPENINGS["win_ground"]["h"]
    w, h = _ins("win_ground")                # 0.76 x 1.21
    r_in = w / 2                             # 0.38, vs the wall's 0.40 reveal
    spring = h - r_in                        # 0.83; the wall springs at 0.85
    # WHAT THE WALL LEAVES US, read out of stone_walls.py rather than guessed:
    # SM_Wall_StoneWindow_2m lines the opening with dressed stone to REV_D =
    # 0.166, keeps the core void clear (and 16 mm oversize) back to y = 0.350,
    # and plugs the back with its own dark blank at y = 0.286-0.312. So this
    # insert owns y = 0 .. 0.166 for anything visible, and nothing of ours may
    # reach 0.286 -- the wall wobbles that plate by up to 6 mm, so a face of
    # ours parked 2 mm off it (which is where our blank used to sit, 0.240-0.288)
    # becomes coincident with it in the assembled inn even though neither piece
    # measures as fighting on its own.
    # The stone storey is a 360 mm wall lined with dressed stone to y = 0.166,
    # so the glazed unit sits DEEPER than a timber-wall leaf, and round 14 pushed
    # it deeper still: `depth` 0.150 puts glazing()'s frame at 0.048..0.103, its
    # leading at 0.124..0.140 and its pane at 0.144..0.156 -- the whole assembly
    # inside the stone reveal, the sash face 150 mm behind the masonry face, and
    # well in front of the wall's own backing plate.
    #
    # ROUND 14, JOB 4 -- CHECKED THE SAME WAY AS THE CASEMENTS. Measured, this
    # piece was 0.788 x 1.199 in an 0.80 x 1.25 hole: inside the opening, so it
    # never showed as a lapped frame, but 28 mm WIDER than the insert envelope
    # (0.76), because the interior blank was cut to `ow - 0.012` to cover the
    # clearance slot. It does not need to: SM_Wall_StoneWindow_2m plugs the back
    # of its own reveal. The blank is the insert's width now, and the seams below
    # are the insert envelope exactly, so util.check() proves the fit.
    #
    # AND THE TIMBER SUB-CILL IS GONE. It was the ground-floor half of the
    # doubled sill: stone_walls thickens its string course into a projecting
    # stone cill under every win_ground opening whose TOP FACE IS the reveal
    # floor, and this piece then laid a second, timber one on top of it. Same
    # rule as the casements -- the wall owns the cill. glazing()'s own sill
    # member is what the sash lands on, and it lands on the stone.
    p = Part("SM_Win_ArchStone", budget="window",
             seams=dict(x=(-w / 2, w / 2), y=(0, T_S), z=(CL, CL + h)))
    # our blank floats in the void between the wall's stone lining and the wall's
    # own blank, 22 mm clear of the latter -- three times the wall's wobble.
    #
    # ROUND 16 CUT IT TO THE SPRINGING, and this is the fault a world-space BVH
    # of the insert against the real SM_Wall_StoneWindow_2m turns up: the hole is
    # ROUND-HEADED and the blank was a full-height RECTANGLE, so above the
    # springing its two upper corners stood in the wall's spandrel stone --
    # 30-odd triangle pairs of oak_dark buried inside stone_dark at z 2.03..2.15,
    # a solid inside a solid. It stops at the springing now, and the head is
    # closed the way an arched head has to be: by the tympanum, which is already
    # struck as an ARC SEGMENT (see below) and sits 46 mm in front of this plane.
    # Above the tympanum the wall's own spandrels are solid stone, so nothing can
    # show sky.
    _blank(p, w, spring, y=.226, d=.038)

    # ---- the glazed light: square-headed, up to just under the springing. Its
    # frame's outer corner has to stay inside the arc, so the head member tops
    # out 14 mm below the springing rather than crossing it.
    gz0, gz1 = .052, spring - .060
    _sash(p, -r_in, r_in, gz0, gz1, 2, .118, "square", "cool", depth=D_STONE,
          seed=6, swag=2.6, gap=.012, mull=.050, mull_front=.014,
          mull_mat="oak_mid")
    bm = GLAZE["cool"][1]
    # ---- tympanum: a dark recessed panel struck as an ARC SEGMENT, not a plate.
    # A rectangle here poked 70 mm out of the arc into the wall's voussoirs at
    # the haunches, which was part of the doubled-arch mess. It sits on the same
    # plane the pane below it uses, so the fan and the band in front of it read
    # against a shadow the way an unlit fanlight does.
    rg = r_in - .026
    seg = [(rg * cos(radians(6.0)), gz1 + .030)]
    for i in range(9):
        a = radians(lerp(6.0, 174.0, i / 8.0))
        seg.append((rg * cos(a), spring + rg * sin(a)))
    seg.append((-rg * cos(radians(6.0)), gz1 + .030))
    p.prism(seg, .012, "oak_dark", axis='Y', at=(0, D_STONE + .024, 0), bevel=0,
            tint=.04, shade=.30)   # 0.168..0.180: 12 mm behind the pane
    # ---- the arched head: ONE continuous bent timber, not a voussoir ring.
    # p.arch() lays jointed WEDGES, and a wedge ring in oak 24 mm inside the
    # wall's stone voussoirs is a second arch ring with its own joint lines --
    # which is most of what still read as the doubled arc, even after the stone
    # surround came out of this piece. A window head is one member, so it is
    # struck as a single band: no joints to echo the masonry, and enough segments
    # that auto-smooth carries the curve rather than showing 36 deg facets. Its
    # ends run 7 deg PAST the springing and die inside the jambs, so no end face
    # lands on a jamb's top face.
    #
    # ROUND 15 -- THE BAND IS ACTUALLY CONCENTRIC NOW, and it was not. Measured
    # against the wall's own arc (spec: R = 0.400 about z = 0.850 in the OPENING
    # frame): "head band struck from a centre 20 mm low with radius 21.5 mm
    # small: crown gap 48 mm vs 17.5 mm at the springing, not the docstring's
    # even 20 mm". Three separate causes, all of them removable:
    #   1. THE DATUM. The whole piece stood on the sill, so its springing sat at
    #      0.830 where the wall's is at 0.850 -- the 20 mm is the head clearance
    #      that used to live entirely at the top of the piece. `_seat` fixes it
    #      for the arch exactly as it does for the casements.
    #   2. TWO FUDGE FACTORS, +6 mm on the centre and -4 mm on the radius, which
    #      between them cost another 10 mm of gap and tilted it. Both gone: the
    #      band is struck from the springing, at r_in, which IS the insert
    #      envelope -- i.e. spec's 20 mm clearance and not a millimetre more.
    #   3. THE POLYGON. 9 segments over 194 deg is 21.6 deg a facet, and an
    #      INSCRIBED polygon's mid-facet sags r*(1-cos(half)) = 6.7 mm below its
    #      circle -- with no vertex at 90 deg, the crown was a facet middle, so
    #      the crown gap measured 6.7 mm wider than the springing gap before any
    #      of the above. 14 segments both halves the sag and puts a vertex dead
    #      on the crown, so the two numbers the audit compares are the same one.
    cz = spring                              # concentric with the wall's arc
    r_o, r_i = r_in, r_in - .044             # 0.380 / 0.336: a 44 mm head
    a0, a1, ns = radians(-7.0), radians(187.0), 14
    band = [(r_o * cos(lerp(a0, a1, i / ns)), cz + r_o * sin(lerp(a0, a1, i / ns)))
            for i in range(ns + 1)]
    band += [(r_i * cos(lerp(a1, a0, i / ns)), cz + r_i * sin(lerp(a1, a0, i / ns)))
             for i in range(ns + 1)]
    p.prism(band, .022, "oak_mid", axis='Y', at=(0, D_STONE - .045, 0),
            bevel=0, tint=.06, shade=1.02)   # 0.094..0.116
    # ---- the fan. The two bars used to start at r = 0.075 from a spring centre
    # they did not share, so both ended in mid-air 60 mm above the head rail and
    # read as two broken sticks hanging in the glass. A fan needs a HUB: the
    # bars now radiate from a half-round spring block whose lower half is buried
    # in the head rail, they are let 30 mm INTO it, and their tips lap 14 mm into
    # the head band. Three of them, the middle one carrying the mullion's line
    # up through the tympanum. Same depth slab as the glazing bars below, 6 mm
    # proud of hub and band so every meeting is a lap and not a shared plane.
    y_bar = D_STONE - .053                   # bars 0.084..0.110
    r0, r1 = .030, r_i + .014
    p.cyl((0, D_STONE - .064, cz), .058, .032, "oak_mid", sides=9, axis='Y',
          tint=.06, shade=1.06)             # hub 0.070..0.102
    for ang in (45.0, 90.0, 135.0):
        a = radians(ang)
        if abs(ang - 90.0) < 1e-6:           # p.beam swaps w/h on a vertical run
            p.box((0, y_bar, cz + (r0 + r1) / 2), (.026, .026, r1 - r0), bm,
                  bevel=0, tint=.06)
            continue
        p.beam((r0 * cos(a), y_bar, cz + r0 * sin(a)),
               (r1 * cos(a), y_bar, cz + r1 * sin(a)),
               .026, .026, bm, bevel=0, tint=.06)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())


# ----------------------------------------------------------- dormer light ----
def dormer():
    """Small dormer light -- ref2's run of gabled dormers. Narrow sash, carved
    crest over the head.

    SAME RULE AS THE CASEMENTS, and it needed it worst of all: this light
    measured 0.72 x 1.05 in an 0.62 x 0.78 hole -- 35% too wide and 35% too
    tall -- because it carried a projecting cill on two corbels, two jamb
    architraves lapping the plaster and a crest standing a quarter of a metre
    ABOVE the opening. The dormers family builds its own chunky sill BOARD whose
    top face is exactly OPENINGS["win_dormer"]["sill"] ("so the windows family's
    casement sits on it"), lines its own reveal and carries its own head beam
    and dentil course, so every one of those was the dormer's member drawn
    twice. 0.58 x 0.74 now: sash, mullion, bands, and the crest brought down
    inside the head."""
    w, h = _ins("win_dormer")                # 0.58 x 0.74
    p = Part("SM_Win_Dormer", budget="window",
             seams=dict(x=(-w / 2, w / 2), y=(0.0, T_T), z=(CL, CL + h)))
    _blank(p, w, h)                          # 0.152 .. Y_LEAF_BACK
    zh = h - .200                            # the crest sits over the sash
    _sash(p, -w / 2, w / 2, .022, zh, 2, .118, "square", "cool", seed=7,
          swag=2.6, gap=.012, mull=.048, mull_mat="oak_mid")
    _cover(p, 0, .015, w, .030, shade=.94)
    _head_close(p, w, zh - .008, h)
    _cover(p, 0, zh - .008, w, .032, shade=1.06)
    _crest(p, 0, zh + .006, w * .70, tall=.42, y_front=.004, depth=.052)
    _seat(p)
    p.wobble(WOB)
    return _cards_out(p.finish())


# ------------------------------------------------------------- flower box ----
def flower_box():
    """Planted box hung off a cill -- ref2 puts one under nearly every window.
    Place it with its rim (z = 0.24) on the cill line. Plank trough, two
    battens, iron straps and hangers, foliage mounded over the rim and trailing
    down the front."""
    bw, bd, bh = .74, .200, .240
    # y-min / z-min carry the greenery: the planting trails below and in front of
    # the trough, which is the whole point of the piece. Clamped to (0, -.28) the
    # trailing strands were folded flat onto those two planes.
    p = Part("SM_Win_FlowerBox", budget="window",
             seams=dict(x=(-.46, .46), y=(-.34, .06), z=(-.16, .50)))
    y0, y1 = -bd - .014, -.014               # the box hangs outside the wall
    ym = (y0 + y1) / 2
    # the front boards run 10mm PAST the trough's front plane so their inner
    # faces die inside the end boards instead of landing on y0 with them
    p.planks((-bw / 2, bw / 2), (.026, bh), y0 - .026, 4, "oak_mid", axis='Y',
             thick=.040, gap=.007, bevel=.009, tint=.075, seed=11, jitter=.15)
    for sx in (-1, 1):
        p.box((sx * (bw / 2 - .016), ym, bh * .52), (.032, bd, bh * .94),
              "oak_mid", bevel=.009, seg=1, tint=.06, shade=.93)
    # floor plate. Its ENDS matter as much as its faces: at bw - .010 they landed
    # inside the end boards but only 5 mm short of their outer face, and wobble
    # moves a plate this size by up to 2.5 mm at each end. Cut to bw - .100 it
    # dies 18 mm inside the boards, where the pair can never be frontmost.
    p.plate((0, ym, .020), (bw - .100, bd - .056, .040), "oak_dark", tint=.04,
            shade=.72)
    # back board LAPS over the trough's back plane (y1) instead of butting it:
    # flush, its front face sat 1mm off the floor plate and both end boards,
    # which is 1800 cm2 of coincident timber on a piece this small
    p.box((0, y1 + .011, bh * .52), (bw, .042, bh * .94), "oak_mid",
          bevel=.008, seg=1, tint=.05, shade=1.06)
    for f in (-.27, .27):                    # battens, let 8mm into the boards
        p.box((bw * f, y0 - .034, bh * .52), (.048, .028, bh * .96), "oak_dark",
              bevel=.007, seg=1, tint=.05)
    for z in (bh * .20, bh * .84):           # iron straps, riding over the battens
        p.box((0, y0 - .048, z), (bw * .96, .024, .022), "iron", bevel=.005,
              seg=1, tint=.04)
    for sx in (-1, 1):                       # hangers back to the wall
        p.box((sx * (bw / 2 - .055), ym + .018, bh * .07),
              (.028, bd * .95, .028), "iron", bevel=.004, seg=1, tint=.04,
              rot=(26, 0, 0))
    # the earth surface. Same reason: at bw - .070 its ends sat 2.8 mm off the
    # end boards' inner faces -- the one pair in this family that a 2.5 mm
    # wobble could actually close -- so it is cut back to a 23 mm shadow gap.
    p.plate((0, ym, bh - .020), (bw - .110, bd - .045, .046), "oak_dark",
            tint=.05, shade=.48)
    _planting(p, (0, ym, bh + .014), (bw * .47, bd * .42, .098), seed=12,
              n=36, nf=26, drape=7)
    p.wobble(.0012)
    return _cards_out(p.finish())


# ------------------------------------------------------------------ build ----
def build():
    return [casement_a(), casement_b(), casement_c(), shuttered(), bay(),
            arch_stone(), dormer(), flower_box()]


# ================================================================== demo =====
# The demo needs something to be a window IN. These staging slabs are NOT kit
# pieces -- no SM_ prefix, no budget, no seams. They exist only so the family
# can be judged in the context it is built for; real walls come from the
# stone_walls / timber_walls families, real roofs and dormers from theirs.

def _slab(p, x0, x1, z0, z1, y0, t, mat, holes, tint=.05, shade=1.0):
    """Plain slab with rectangular holes punched through.
    holes: [(cx, half_w, hz0, hz1), ...]"""
    x = x0
    for (cx, hw, hz0, hz1) in sorted(holes, key=lambda q: q[0]):
        a, b = cx - hw, cx + hw
        if a - x > .002:
            p.plate(((x + a) / 2, y0 + t / 2, (z0 + z1) / 2), (a - x, t, z1 - z0),
                    mat, tint=tint, shade=shade)
        if hz0 - z0 > .002:
            p.plate(((a + b) / 2, y0 + t / 2, (z0 + hz0) / 2), (b - a, t, hz0 - z0),
                    mat, tint=tint, shade=shade)
        if z1 - hz1 > .002:
            p.plate(((a + b) / 2, y0 + t / 2, (hz1 + z1) / 2), (b - a, t, z1 - hz1),
                    mat, tint=tint, shade=shade)
        x = b
    if x1 - x > .002:
        p.plate(((x + x1) / 2, y0 + t / 2, (z0 + z1) / 2), (x1 - x, t, z1 - z0),
                mat, tint=tint, shade=shade)


def _arched_head(p, cx, hw, zsill, ztop, t, n=9):
    """Turn a rectangular staging hole into a ROUND-HEADED one: two spandrels
    filling the corners above the springing, plus a dressed ring and jamb blocks
    on the face.

    The staging wall used to punch a plain rectangle for win_ground, so the
    arched insert sat in a square hole with two black corners over its head --
    which reads in the demo exactly like the doubled-arch bug this piece was
    fixed for. SM_Wall_StoneWindow_2m carries a real dressed ring, so the
    staging has to as well, or the demo cannot show that the insert no longer
    duplicates it. Inner radius is the OPENING half-width, so the insert's 0.38
    head keeps its even 20 mm clearance the whole way round the arc.
    """
    spring = ztop - hw
    for sx in (-1, 1):                        # spandrel: corner minus the arc
        prof = [(cx + sx * hw, spring)]
        for i in range(n + 1):
            a = radians(lerp(90.0, 0.0, i / n))
            prof.append((cx + sx * hw * cos(a), spring + hw * sin(a)))
        prof += [(cx, ztop), (cx + sx * hw, ztop)]
        p.prism(prof, t, "stone_dark", axis='Y', at=(0, t / 2, 0),
                bevel=0, tint=.03, shade=.55)
    p.arch((cx, .020, spring), hw + .165, .180, "stone_pale", thickness=.165,
           segs=9, span=180.0, tint=.05, tint_seed=7, bevel=.014)
    for sx in (-1, 1):                        # dressed jambs up to the springing
        p.box((cx + sx * (hw + .082), .024, (zsill + spring) / 2),
              (.165, .172, spring - zsill), "stone_pale", bevel=.014, seg=1,
              tint=.05, shade=.94)


def _stage_stone(name, x0, x1, z0, z1, t, holes, sill=None, arch=False):
    p = Part(name)
    _slab(p, x0, x1, z0, z1, 0.0, t, "stone_dark", holes, tint=.03, shade=.55)
    if arch:
        for (cx, hw, hz0, hz1) in holes:
            _arched_head(p, cx, hw, hz0, hz1, t)
    xs = [x0] + [v for (cx, hw, _, _) in sorted(holes, key=lambda q: q[0])
                 for v in (cx - hw, cx + hw)] + [x1]
    for i in range(0, len(xs) - 1, 2):
        if xs[i + 1] - xs[i] > .16:
            p.stones((xs[i], xs[i + 1]), (z0, z1), y=0.0, depth=.062,
                     mat="stone", mat_alt="stone_dark", mat_warm="stone_warm",
                     course=.32, seed=int(abs(xs[i]) * 17) + 3, wobble=.16,
                     tint=.085, r_bevel=0, shade_var=.15, chink=.16)
    for (cx, hw, hz0, hz1) in holes:
        if hz1 < z1 - .10:
            p.stones((cx - hw, cx + hw), (hz1 + .02, z1), y=0.0, depth=.058,
                     mat="stone", mat_alt="stone_dark", course=.34, seed=31,
                     wobble=.14, tint=.08, r_bevel=0, shade_var=.13)
        if hz0 > z0 + .10:
            p.stones((cx - hw, cx + hw), (z0, hz0 - .02), y=0.0, depth=.058,
                     mat="stone", mat_alt="stone_dark", course=.32, seed=37,
                     wobble=.14, tint=.08, r_bevel=0, shade_var=.13)
    if sill is not None:                       # projecting string course
        p.box(((x0 + x1) / 2, -.030, sill - .048), (x1 - x0, .140, .086),
              "stone_pale", bevel=.013, seg=1, tint=.05, shade=.86)
    return p.finish()


def _stage_timber(name, x0, x1, z0, z1, t, holes, studs=.62, rails=(),
                  brace=True):
    """Cream plaster panels set back behind narrow mid-brown framing, at the
    proportion the brief calls for (timbers ~0.14 wide, panels recessed). Rails
    at the cill and head lines break the field the way both refs do -- without
    them a 2.6m storey reads as one enormous blank panel.

    ROUND 14 GIVES EVERY HOLE THE SURROUND THE REAL WALL BUILDS, and it has to,
    because the surround is now the WALL's job (see the header) and a demo that
    leaves it out is a demo of half the joint. The numbers are read straight out
    of timber_walls.SM_Wall_TimberWin_2m rather than invented:

        sill nose   z hz0-0.050 .. hz0+0.014, y -0.100 .. 0.020, hw + 0.095
        oak jamb    x +/-(hw - 0.006), 0.062 wide, y -0.046 .. 0.080
        drip mould  z hz1+0.000 .. hz1+0.036, y -0.082 .. 0.098, hw + 0.095
        backing     y BACK_Y .. T - 0.004 = 0.200 .. 0.236, oversized 0.032
                    past the hole (round 16: it was 0.140 .. 0.200)

    Snap a casement into that and the two together are ONE window: the wall's
    cill, the wall's drip, the wall's jambs, spec's 20 mm shadow gap, and the
    insert's sash 56 mm back inside it."""
    p = Part(name)
    _slab(p, x0, x1, z0, z1, .050, t - .050, "plaster", holes, tint=.055,
          shade=.80)
    p.plate(((x0 + x1) / 2, t - .008, (z0 + z1) / 2), (x1 - x0, .016, z1 - z0),
            "plaster_dim", tint=.03, shade=.7)
    tw, td = .148, .104
    zs = [z0 + tw / 2, z1 - tw / 2]
    for z, sh in ((zs[0], .95), (zs[1], 1.04)):
        p.box(((x0 + x1) / 2, td / 2 - .002, z), (x1 - x0, td, tw), "oak_dark",
              bevel=.012, seg=1, tint=.055, shade=sh)
    for z in rails:                            # cill / head rails
        p.box(((x0 + x1) / 2, td / 2 - .004, z), (x1 - x0, td * .94, tw * .86),
              "oak_dark", bevel=.012, seg=1, tint=.055, shade=1.0)
    bands = [zs[0]] + sorted(rails) + [zs[1]]
    n = max(1, int(round((x1 - x0) / studs)))
    for i in range(n + 1):
        x = lerp(x0, x1, i / n)
        if any(cx - hw - .13 < x < cx + hw + .13 for (cx, hw, _, _) in holes):
            continue
        for a, b in zip(bands[:-1], bands[1:]):
            p.box((x, td / 2 - .004, (a + b) / 2), (tw, td, b - a),
                  "oak_dark", bevel=.012, seg=1, tint=.055,
                  shade=.96 + .06 * ((i + int(a)) % 2))
    for (cx, hw, hz0, hz1) in holes:           # posts + head over each opening
        for sx in (-1, 1):
            p.box((cx + sx * (hw + tw / 2 + .008), td / 2 - .004,
                   (zs[0] + zs[1]) / 2), (tw, td, zs[1] - zs[0]), "oak_dark",
                  bevel=.012, seg=1, tint=.055)
        p.box((cx, td / 2 - .004, hz1 + tw / 2 + .014),
              (2 * hw + 2 * tw, td, tw), "oak_dark", bevel=.012, seg=1, tint=.055)
        # ---- THE WALL'S OWN WINDOW SURROUND (see the docstring) -------------
        # THE REVEAL BACKING, ON THE WALL'S OWN PLANE. It used to be y =
        # 0.140..0.200, which is where timber_walls put it until it moved the
        # plate back to BACK_Y = 0.200 to get out of the insert's way. Left at
        # 0.140 the staging would swallow the leaf's whole interior blank
        # (0.152..0.190) inside itself -- a face buried in a solid, which is a
        # worse fault than the z-fight it looks like it avoids -- and the demo
        # would be a demo of a joint nobody assembles. 0.200 .. T - 0.004.
        p.plate((cx, (.200 + T_T - .004) / 2, (hz0 + hz1) / 2),
                (2 * hw + .064, T_T - .004 - .200, hz1 - hz0 + .064), "oak_dark",
                tint=.05, shade=.52)
        for sx in (-1, 1):                                   # oak reveal jambs
            p.box((cx + sx * (hw - .006 + .031), .017, (hz0 + hz1) / 2 + .008),
                  (.062, .126, hz1 - hz0 + .050), "oak_dark", bevel=.010,
                  seg=1, tint=.06, shade=.98)
        p.box((cx, -.040, hz0 - .018), (2 * hw + .190, .120, .064),
              "oak_dark", bevel=.012, seg=1, tint=.065, shade=1.02)   # sill nose
        p.box((cx, .008, hz1 + .018), (2 * hw + .190, .180, .036),
              "oak_dark", bevel=.012, seg=1, tint=.06, shade=1.05)    # drip
    p.plate(((x0 + x1) / 2, t / 2, z1 - .014), (x1 - x0, t, .028), "oak_dark",
            tint=.04, shade=.62)
    if brace:                                  # curved braces, ref1's motif
        for sx, xe in ((1, x0 + tw), (-1, x1 - tw)):
            z_a, z_b = zs[0] + tw / 2, bands[1] if len(bands) > 2 else zs[1]
            span = 1.05
            pts = []
            for k in range(5):
                u = k / 4.0
                pts.append((xe + sx * span * u,
                            z_a + (z_b - z_a) * (1.0 - (1.0 - u) ** 2)))
            for a, b in zip(pts[:-1], pts[1:]):
                p.beam((a[0], td / 2 - .004, a[1]), (b[0], td / 2 - .004, b[1]),
                       tw * .92, td * .95, "oak_dark", bevel=.011, seg=1,
                       tint=.055, shade=.99, extend=.02)
    return p.finish()


def _jetty(name, x0, x1, z, out, n=4):
    """Sill beam + corbels carrying the jettied storey. Staging: the real thing
    lives in the beams family."""
    p = Part(name)
    p.box(((x0 + x1) / 2, -out / 2 + .03, z + .082), (x1 - x0, out + .14, .164),
          "oak_dark", bevel=.015, seg=1, tint=.05)
    for i in range(n):
        x = lerp(x0 + .45, x1 - .45, i / max(n - 1, 1))
        _corbel(p, x, z, out + .05, .38, .125, mat="oak_dark", tint=.05,
                shade=.95)
    p.sag(.010, axis='x')
    return p.finish()


def _place(src, name, at, rot=None):
    o = src[name].copy()
    o.data = src[name].data
    bpy.context.scene.collection.objects.link(o)
    o.location = at
    if rot:
        o.rotation_euler = [radians(a) for a in rot]
    return o


def demo():
    """A corner of the inn, composed for the ref2 camera (elevated 3/4 from
    +X/-Y): stone ground storey with arched lights, a jettied half-timber storey
    above it, and the gable end over the front holding the dormer light.

    The upper storey is laid out the way ref3's is: WIDE lights, one per framing
    bay, each filling about three quarters of the bay between its jamb studs,
    with a single stud left standing in the gap between neighbours -- so the wall
    reads as a glazed facade rather than plaster with holes punched in it. The
    narrow casement C and the shuttered gable light are the exceptions, as they
    are in the paintings. Ground and upper openings share centre lines, and
    flower boxes hang in pairs under the wide lights."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []
    GS, US, J = S.H_GROUND, S.H_UPPER, S.JETTY
    gs_ = S.OPENINGS["win_ground"]["sill"]
    gh_ = S.OPENINGS["win_ground"]["h"]
    us_ = S.OPENINGS["win_upper"]["sill"]
    uh_ = S.OPENINGS["win_upper"]["h"]
    bs_ = S.OPENINGS[K_UP]["sill"]
    bh_ = S.OPENINGS[K_UP]["h"]
    ds_ = S.OPENINGS["win_dormer"]["sill"]
    dh_ = S.OPENINGS["win_dormer"]["h"]
    XL, XR, DP = -2.3, 2.3, 3.4               # front span, and return depth
    BW = S.OPENINGS[K_UP]["w"] / 2             # 0.75 -- the wide upper light
    NW = S.OPENINGS[K_SMALL]["w"] / 2         # 0.43 -- the narrow one
    # cill rail low, head rail up under the 2.43 storey plate, so the wide
    # lights and their hoods have the whole middle of the panel to themselves
    RAILS = (bs_ - .12, 2.40)
    FX = (-1.42, 0.50, 2.10)                  # front upper centre lines
    RX = (0.80, 2.48)                         # return centre lines

    # ---------------- ground storey: stone, front faces -Y, return faces +X
    gx = FX[:2]                               # aligned under the wide lights
    out.append(_stage_stone("DEMO_StoneFront", XL, XR, 0, GS, T_S,
                            [(x, .40, gs_, gs_ + gh_) for x in gx], sill=gs_,
                            arch=True))
    o = _stage_stone("DEMO_StoneReturn", 0.0, DP, 0, GS, T_S,
                     [(y, .40, gs_, gs_ + gh_) for y in RX], sill=gs_,
                     arch=True)
    o.rotation_euler = (0, 0, radians(90))
    o.location = (XR, 0, 0)
    out.append(o)

    # ---------------- jetty beams
    out.append(_jetty("DEMO_JettyFront", XL - .05, XR + J, GS, J, n=4))
    o = _jetty("DEMO_JettyReturn", 0.0, DP, GS, J, n=4)
    o.rotation_euler = (0, 0, radians(90))
    o.location = (XR, 0, 0)
    out.append(o)

    # ---------------- upper storey: half-timber, jettied to y = -J / x = XR+J
    uw = [(FX[0], BW, bs_, bs_ + bh_), (FX[1], BW, bs_, bs_ + bh_),
          (FX[2], NW, us_, us_ + uh_)]
    o = _stage_timber("DEMO_TimberFront", XL - .08, XR + J, 0, US, T_T, uw,
                      rails=RAILS)
    o.location = (0, -J, GS)
    out.append(o)
    rw = [(RX[0], NW, us_, us_ + uh_), (RX[1], BW, bs_, bs_ + bh_)]
    o = _stage_timber("DEMO_TimberReturn", 0.0, DP, 0, US, T_T, rw,
                      rails=RAILS, brace=False)
    o.rotation_euler = (0, 0, radians(90))
    o.location = (XR + J, 0, GS)
    out.append(o)

    # ---------------- gable end over the front, holding the dormer light
    gp = Part("DEMO_Gable")
    ghx, apex = (XR - XL + J) / 2, 1.66
    tw, td = .148, .104
    ow2 = S.OPENINGS["win_dormer"]["w"] / 2
    zt = apex * (1.0 - ow2 / ghx)              # hypotenuse height at the jamb
    ztop = ds_ + dh_
    pt = T_T - .050
    yp = pt / 2 + .050
    # plaster in four pieces so the dormer light has a real hole to sit in
    gp.prism([(-ghx, 0), (-ow2, 0), (-ow2, zt)], pt, "plaster", axis='Y',
             at=(0, yp, 0), tint=.055, shade=.80)
    gp.prism([(ow2, 0), (ghx, 0), (ow2, zt)], pt, "plaster", axis='Y',
             at=(0, yp, 0), tint=.055, shade=.80)
    gp.prism([(-ow2, 0), (ow2, 0), (ow2, ds_), (-ow2, ds_)], pt, "plaster",
             axis='Y', at=(0, yp, 0), tint=.055, shade=.80)
    gp.prism([(-ow2, ztop), (ow2, ztop), (ow2, zt), (0, apex), (-ow2, zt)], pt,
             "plaster", axis='Y', at=(0, yp, 0), tint=.055, shade=.80)
    for a in ((-ghx, 0), (ghx, 0)):            # rakers / bargeboard line
        gp.beam((a[0], td / 2 - .004, a[1]), (0, td / 2 - .004, apex), tw, td,
                "oak_dark", bevel=.012, seg=1, tint=.055)
    gp.box((0, td / 2 - .004, tw / 2), (2 * ghx, td, tw), "oak_dark",
           bevel=.012, seg=1, tint=.055)
    gp.box((0, td / 2 - .004, ztop + tw / 2 + .012), (2 * ow2 + 2 * tw, td, tw),
           "oak_dark", bevel=.012, seg=1, tint=.055)
    for sx in (-1, 1):                         # jamb posts + collar tie
        gp.box((sx * (ow2 + tw / 2 + .008), td / 2 - .004, (tw + ztop) / 2),
               (tw, td, ztop - tw), "oak_dark", bevel=.012, seg=1, tint=.055)
    go = gp.finish()
    go.location = (ghx - (XR + J), -J, GS + US)
    out.append(go)

    # ---------------- the windows
    # ON THE SILL, not CL above it. Round 15 moved the inserts' datum to the
    # OPENING frame (see `_seat`), which is where the assembler has always put
    # them -- `z + 0.95*zs` IS spec's sill line -- so the demo has to place them
    # the same way or it is a demo of a joint nobody assembles.
    zb, zn = GS + bs_, GS + us_                # wide / narrow cill lines
    # THE BOXES HANG UNDER THE CILL, which is where both references put them and
    # what assemble_inn now does (`z + 0.95*zs - 0.42`). The box is 0.403 from
    # its origin to the top of its planting, so dropping it FB clears the sill
    # nose by 17 mm and the greenery reads against the plaster, not the glass.
    FB = -.420
    front = [("SM_Win_ArchStone", (x, 0, gs_)) for x in gx] + [
        ("SM_Win_LeadedCasement_A", (FX[0], -J, zb)),
        ("SM_Win_FlowerBox", (FX[0] - .34, -J, zb + FB)),
        ("SM_Win_LeadedCasement_B", (FX[1], -J, zb)),
        ("SM_Win_FlowerBox", (FX[1] + .32, -J, zb + FB)),
        ("SM_Win_LeadedCasement_C", (FX[2], -J, zn)),
        ("SM_Win_FlowerBox", (FX[2], -J, zn + FB)),
        ("SM_Win_Dormer", (ghx - (XR + J), -J, GS + US + ds_)),
        ("SM_Win_FlowerBox", (ghx - (XR + J), -J, GS + US + ds_ + FB)),
    ]
    for nm, at in front:
        if nm in src:
            out.append(_place(src, nm, at))
    ret = [("SM_Win_ArchStone", (XR, RX[0], gs_)),
           ("SM_Win_ArchStone", (XR, RX[1], gs_)),
           ("SM_Win_Shuttered", (XR + J, RX[0], zn)),
           ("SM_Win_BayMullion", (XR + J, RX[1], zb))]
    for nm, at in ret:
        if nm in src:
            out.append(_place(src, nm, at, (0, 0, 90)))

    for o in src.values():
        o.location = (0, 80, 0)               # park the originals out of frame
    return out
