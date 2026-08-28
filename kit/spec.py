"""
THE LAW. Every piece module obeys this file. Do not edit it in a builder task --
if a constant is wrong, say so, don't fork it. All units are metres (1 BU = 1 m).

===============================================================================
PLACEMENT CONVENTIONS  (this is what makes the kit snap)
===============================================================================

WALL-FAMILY pieces (stone walls, timber walls, half-walls, wall variants):
    origin at (0,0,0)
    X  in [-GRID/2, +GRID/2]      -> tiles along X at exactly GRID spacing
    Y  in [0, T]                   -> OUTER FACE LIES ON THE Y=0 PLANE, body goes +Y (inward)
    Z  in [0, H]                   -> sits on the floor plane, stacks at exactly H

    Decorative relief (timber posts, sills, corbels, mouldings) MAY protrude
    outward to negative Y, but never further than PROUD_MAX.
    Nothing may cross Y = T (the inner face) or X = +/-GRID/2 (the tiling seam),
    except deliberate seam-spanning trim which must be a SEPARATE piece.

CORNER pieces:
    footprint T x T, sitting in the void left where two perpendicular wall runs
    meet: X in [-T,0], Y in [0,T]. So an outer wall rectangle of n x m bays
    measures (n*GRID + 2T) x (m*GRID + 2T). Corner geometry may bulge outward
    (-X/-Y) up to PROUD_MAX. Zero gap, zero overlap, by construction.

ROOF-FAMILY pieces:
    Ridge runs along X. Origin at (0,0,0) = the piece's LOWER-EDGE, CENTRE in X,
    on the slope. Slope tiles: X in [-GRID/2, +GRID/2], and the panel climbs
    +Y (inward/up-slope) by SLOPE_SEG measured ALONG THE SLOPE, i.e. it ends at
    Y = SLOPE_SEG*cos(PITCH), Z = SLOPE_SEG*sin(PITCH). Roof panels therefore
    tile both along the ridge (X, step GRID) and up the slope (step SLOPE_SEG
    along the slope vector). Thickness grows -Z (underside).

FLOOR / PROP / DOOR / WINDOW pieces:
    origin at footprint centre, Z=0 at the bottom, front facing -Y.
    Doors and windows are INSERTS: they fill the reveal of the matching
    wall-with-opening piece, outer face on Y=0, same as walls.

===============================================================================
"""
from math import radians, cos, sin, tan

# ---------------------------------------------------------------- grid ------
GRID        = 2.0     # module width. Every wall / roof bay is this wide.
H_GROUND    = 3.0     # ground storey floor-to-floor
H_UPPER     = 2.6     # upper storey floor-to-floor
H_ATTIC     = 2.2     # attic knee-wall storey (rarely used, kept for layouts)

T_STONE     = 0.36    # stone wall thickness
T_TIMBER    = 0.24    # half-timber wall thickness (plaster panel face to face)
PROUD_MAX   = 0.16    # default: how far relief may stand outside the Y=0 plane.
                      # A piece may declare its own allowance with
                      # Part(..., proud=0.28) -- a chunky corner post head needs it --
                      # and it is still validated against that declared number.

JETTY       = 0.45    # upper storey overhang beyond the storey below (ref: both)

# ---------------------------------------------------------------- roof ------
PITCH_DEG   = 52.0    # ONE pitch for the whole kit. Non-negotiable: it is what
PITCH       = radians(PITCH_DEG)   # lets every roof piece meet every other one.
# THE PITCH THE ROOF IS PRESENTED AT, as distinct from the one it is AUTHORED at.
# Every roof piece is drawn at PITCH_DEG so any piece meets any other; the
# assembler then stretches the whole roof world in Z by
#   ZK = tan(PITCH_F) / tan(PITCH)
# placing each piece at z*ZK with scale (s, s, s*ZK), which leaves every seam
# meeting because a plane through a point scaled that way is unchanged.
# This constant lived in assemble_inn.py, which meant a PIECE could not read the
# pitch it was going to be placed at -- and a piece that is deliberately NOT
# stretched (a dormer) has to cut its back against the FIELD's pitch, not its
# own. Cutting for 52 when the field is 65 made the dormer 0.463 m too long and
# burst it through the main ridge on 10 of 11 placed instances.
# DO NOT "simplify" this to one pitch: PITCH_DEG is read for SIN_P/COS_P by
# roofs, ground, doors and the assembler, and they must all keep authoring at 52.
PITCH_F_DEG = 65.0
PITCH_F     = radians(PITCH_F_DEG)
TAN_F       = tan(PITCH_F)
SLOPE_SEG   = 1.6     # roof panel length measured along the slope
EAVE_OVER   = 0.14    # horizontal overhang of eave past the wall face.
                      # 0.55 -> 0.14, measured. At the kit's 52 deg pitch every metre
                      # of overhang drops 2.143 m, so 0.55 put the drip 1.18 m below the
                      # wall head -- 45% of a 2.60 storey -- and the roof cut a third to
                      # half way down the facade on every building the kit makes. The
                      # roofs family measured r6/r7 (a 3D render of a comparable
                      # building, so a reachable bar), ref1 and ref2 at 3.5-9x: the drip
                      # falls 4-8% of a storey below the wall head there, and the eave
                      # BAND is 0.24-0.26 m, not 0.64. Corroborated independently by the
                      # kit's own OPENINGS: win_upper's head sits at 2.40 in a 2.60
                      # storey, so anything dropping more than 0.20 stands in a window.
VERGE_OVER  = 0.30    # gable-end overhang past the wall face
SWEEP       = 0.22    # bell-cast: how much the lowest ~0.5m of slope flattens out.
                      # This upturned "swept eave" is the kit's signature stylisation.

COS_P, SIN_P = cos(PITCH), sin(PITCH)

def slope_vec(n=1.0):
    """Offset from the bottom of a slope panel to the top, n segments up."""
    return (0.0, SLOPE_SEG * n * COS_P, SLOPE_SEG * n * SIN_P)

# ------------------------------------------------------------ stylisation ---
# "Slightly stylised": chunky readable forms, generous bevels, hand-hewn wobble,
# exaggerated silhouette curves. NOT photoreal. NOT flat low-poly.
BEVEL_W     = 0.018   # default bevel on structural timber / stone
BEVEL_SEG   = 2
WOBBLE      = 0.012   # per-vertex noise amplitude on hand-made things
SAG         = 0.03    # droop on long horizontal timbers / roof ridges
SMOOTH_ANG  = 34.0    # auto-smooth angle, degrees

# --------------------------------------------------------------- budgets ----
# Tri budgets per piece. A critic rejects anything over. Whole kit target 70k.
TRI_BUDGET = {
    "wall":   5200,
    "corner": 1800,
    "roof":   5200,
    "gable":  6500,
    "dormer": 4800,
    "chimney":3000,
    "door":   2800,
    "window": 2600,
    "beam":   1600,
    "sign":   2600,
    "prop":   2400,
    "ground": 3200,
    "found":  4200,
}
# Whole-kit target ~160k tris across ~55 pieces. That is comfortable for a
# stylised PC/console kit; the point of the per-piece cap is to stop any one
# piece eating the budget, not to chase mobile numbers.

# ---------------------------------------------------------------- palette ---
# sRGB hex. mats.py converts to linear. Vertex-colour jitter adds variation on
# top of these, so keep them as the *mean* tone of each surface.
PALETTE = {
    # Retoned on measured critic evidence (round 3). The kit's value STRUCTURE was
    # wrong, not its hues: the stone base rendered as one of the lightest masses when
    # in the references it is the heaviest and darkest, and timber sat only ~30L from
    # its own plaster panel so half-timbering disappeared at thumbnail size. The
    # references run timber ~80 against cream plaster ~220.
    #
    # NOTE on the numbers: critics measuring ref1 asked for stone x0.55 (to ~#4E4941).
    # Applied literally that breaks ref2/ref3, whose ground floor is a PALE ashlar.
    # So stone is darkened substantially but not to ref1's shadowed extreme, and
    # stone_pale is kept genuinely pale for the ashlar look.
    "oak_dark":    "#3E2C22",   # structural timber, posts, braces, bargeboards
    "oak_mid":     "#513A2A",   # doors, shutters, planks, barrels
    "oak_pale":    "#6B5340",   # fresh-cut trim, ladder rungs (use sparingly)
    "plaster":     "#E4D9BE",   # half-timber infill -- stays bright, it is the
                                # contrast partner that makes the framing read
    "plaster_dim": "#B8AB90",   # shadowed / weathered plaster
    "stone":       "#6E6A62",   # rubble base course -- now clearly the heavy mass
    "stone_dark":  "#46433D",   # mortar bed, plinth, wet lower stones
    "stone_pale":  "#A39D91",   # ashlar, chimney stack, quoins, window surrounds
    "stone_warm":  "#7A6C5A",   # the tan stones scattered through a rubble wall
    "shingle":     "#614A34",   # warm wood shingle (ref 1 roof)
    "shingle_moss":"#5A5648",   # mossy shingle: hue ~35, low sat, L in the 85-95
                                # band the critics measured off the reference roof
    "moss":        "#4C5434",   # moss patches, creeper foliage -- desaturated, so
                                # roof moss reads as tone rather than green confetti
    "iron":        "#26241F",   # lantern frames, hinges, brackets, nails
    "glass":       "#FFB65E",   # warm lit window glass (emissive)
    # UNLIT glass. The windows family had to use `stone_dark` for unlit quarries
    # because nothing else existed, and an auditor then measured the result exactly
    # right: "panes are M_stone_dark, roughness 0.82, metallic 0 -- matte stone, no
    # specular", with the pane mean (78) DARKER than the bare wall behind it (94).
    # Their reasoning for rejecting `iron` was sound and is preserved -- three black
    # lights return the same black whatever their normal does, which kills the
    # ajar-leaf tell. What was missing was a dark material with GLASS optics rather
    # than stone optics. Cool, because glass reflects sky.
    # #3B424C -> #4D5665, on the windows family's measurement, not my guess. They
    # separated tone from gloss in a harness: stone_dark r0.82 pane mean 168.0,
    # glass_dark r0.82 167.2, glass_dark r0.11 159.7. So the TONE swap is a pure hue
    # change -- which is the win, the pane no longer shares a hue family with the oak
    # -- and the GLOSS costs 8 of value for nothing, because a few-degree specular
    # lobe finds nothing bright in this kit's world (one small sun, a two-tone
    # gradient, a stone ground). Roughness is near-inert here: 0.11/0.22/0.34/0.50
    # measure 159.9/160.1/161.2/164.2. Their answer was "keep roughness 0.11 and
    # lighten the tone", with the pane-to-plaster ratio measured per candidate:
    #     #3B424C 0.747   #444C58 0.791   #4D5665 0.830  <- lands on the target 78:94
    # Nothing in windows.py changes for it.
    "glass_dark":  "#4D5665",   # unlit window glass: dark, cool, glossy
    "terracotta":  "#8E4E30",   # flower pots
    "flower_red":  "#B04434",
    "flower_gold": "#D9A63F",
    "rope":        "#8A7549",
    "thatch":      "#A88C55",
}

# Material names. Use these exact strings; mats.get(name) builds on demand.
MATS = tuple(PALETTE.keys())

# ---------------------------------------------------------------- naming ----
# SM_<Family>_<Thing>_<Variant>   e.g. SM_Wall_StoneRubble_2m_A
# Variants are A/B/C -- same footprint, different detail, so a level artist can
# break up repetition without breaking the grid.
PREFIX = "SM_"

# Collection each family lands in inside the master .blend
COLLECTIONS = (
    "01_Walls_Stone", "02_Walls_Timber", "03_Corners_Posts", "04_Roof",
    "05_Gables", "06_Dormers", "07_Chimneys", "08_Doors", "09_Windows",
    "10_Beams_Corbels", "11_Signage_Lights", "12_Props", "13_Ground_Stairs",
    "14_Foundations",
)


# ---------------------------------------------------------------- openings ---
# Walls with holes and the inserts that fill them MUST use these numbers, or
# doors rattle in their frames. (w, h, sill_z, head) where head is 'arch' or
# 'flat'. An insert is built 0.02 smaller all round than its opening.
OPENINGS = {
    "door_main":   dict(w=1.10, h=2.20, sill=0.00, head="arch"),   # inn front door
    "door_side":   dict(w=0.95, h=2.05, sill=0.00, head="flat"),   # back / kitchen door
    "door_cellar": dict(w=1.30, h=2.05, sill=0.00, head="arch"),   # ref 1's big arch
    "win_ground":  dict(w=0.80, h=1.25, sill=1.05, head="arch"),   # stone storey
    # Widened on the windows builder's evidence: the reference's upper windows are
    # wide mullioned casements, and a head at 2.40 sits just under timber_walls'
    # head plate at 2.43. Wall pieces with win_upper openings must match this.
    "win_upper":   dict(w=1.50, h=1.45, sill=0.95, head="flat"),   # half-timber storey
    "win_bay":     dict(w=1.50, h=1.10, sill=0.95, head="flat"),   # wide mullioned bay
    "win_dormer":  dict(w=0.62, h=0.78, sill=0.55, head="flat"),
    "win_attic":   dict(w=0.52, h=0.58, sill=0.60, head="flat"),
}
INSERT_CLEAR = 0.02   # gap all round between an insert and its reveal

REVEAL = 0.10         # how deep an opening is recessed from the outer face

# --------------------------------------------------------------- foundations --
# Both references sit the building on a visible base that lifts it off the ground and
# steps out beyond the wall above it, and the terrain is terraced rather than flat.
# A foundation course is therefore its own layer in the kit: walls stack ON it.
H_FOUND    = 0.45     # height of one foundation course
FOUND_OUT  = 0.11     # how far the foundation projects PROUD of the wall it carries
FOUND_STEP = 0.30     # vertical step between adjacent terrace levels

# Foundation pieces follow the WALL convention (outer face on Y=0, body to +Y, X in
# [-GRID/2, GRID/2]) but are FOUND_OUT proud, so declare proud=FOUND_OUT+0.05.
# A storey sitting on a foundation starts at z = H_FOUND.
