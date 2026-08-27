"""Signage + lights: hanging inn signs on wrought-iron brackets, lanterns, a
painted door panel and a notice board. The kit's jewellery -- small, dark,
warm-glowing, and the thing that tells the player "this building is an inn".

READ OFF THE REFERENCE CROPS
  ref1 lantern (0.12-0.30 x 0.48-0.72) -- the iconic fitting:
    * the bracket is THIN flat strap iron, not a timber corbel. It leaves the
      wall almost horizontally, arcs down, and finishes in a double curl; the
      lantern hangs from the junction of the curls.
    * MEASURED OFF THE CROP (fantasy_inn.jpg, px): the cage sits in x 198-218,
      z 409-440 -> 21 wide by 31 tall, and the hood spans x 195-219, z 396-409.
      So the cage alone is ~1.5:1 and the WHOLE body -- hood apex to base -- is
      44 on 21, i.e. ~2:1, an upright slim box of light. Ours used to be a
      0.315-on-0.250 cube (1.26:1) with a 0.15 cone lid, which read as a squat
      carriage lamp. The cage is now 0.500 on 0.250 -- TWICE AS TALL AS WIDE.
    * the glazing is 2 panes wide by THREE high: one central mullion, rails at
      1/3 and 2/3. In the crop the amber breaks at z 422-423 and 430-431, which
      is exactly two intermediate rails. The frame is slim; glass is most of it.
    * the hood is a CONVEX BELL, not a cone: in the crop its half-width goes
      4.5, 7, 9, 11, 12.5 px over 13 px of drop -- fast at the apex, almost
      nothing at the shoulder. That is a dome. It stands 0.9x the cage width
      tall (0.22 on 0.25) and its lip flicks outward-and-down -- the same
      swept-eave language as the roofs. That flick is most of what makes the
      fitting read as part of THIS kit.
  ref1 door sconce (0.70-0.82 x 0.53-0.72) -- same 2x3 cage, hood flared into a
      little pyramid with a spike finial, on a shelf bracket against the wall.
  ref2/ref3 porch (0.52-0.75 x 0.58-0.85) -- how this world paints a sign: a
      golden foaming tankard on cream plaster, and a dark oak plank band under
      it carrying illegible gold glyph-marks. Copied here as geometry (no
      textures): gold prisms for glyphs, a tapered gold tankard with a plaster
      froth head. ref3's bargeboard also gives the house trim motif -- a run of
      little tapered scroll-teeth -- which is what the boards get along their
      bottom edge instead of a plain square dentil.

PLACEMENT CONVENTION (signage is wall furniture, so it follows the WALL plane)
    The mounting face lies on Y = 0 -- the same plane as a wall piece's outer
    face -- and every part of the fitting projects OUTWARD to -Y. X is centred
    on the piece. Z = 0 is the LOWEST point of the piece (prop convention), so a
    fitting stands on the ground in the lineup render and the level artist just
    raises it: place at z = (wanted height of the wall plate) - PLATE_Z. All
    three hanging signs share PLATE_Z and ARM_Z, so they are interchangeable.
    Fixing plates bite 0.01 into the wall so there is never a hairline gap.
    Hanging signs hang PERPENDICULAR to the wall (board faces +/-X) so they read
    down the street; lanterns, panel and notice board are wall-parallel.

LIBRARY NOTE (worked around locally, see `_solo`)
    util.Part._emit loses a primitive's original faces to bmesh.ops.bevel once
    the Part already holds geometry: the op rebuilds them, the `is_valid` filter
    drops them from the paint list, and they end up on material slot 0. Every
    beveled primitive after the first therefore renders in the wrong material.
    Here every beveled primitive is built in a scratch Part -- where it IS the
    first primitive, which is correct -- and merged in.
"""
import bpy
from math import radians, cos, sin, pi, ceil
from kit import spec as S
from kit.util import Part, rng, lerp, clamp, TAU

FAMILY = "signage"
COLLECTION = "11_Signage_Lights"

# ---- family constants (published so a level artist can snap to them) --------
PLATE_Z = 0.90      # z of the main wall-plate centre on all three hanging signs
ARM_Z   = 1.00      # z of the bracket arm / arch spring on all three
REACH   = 1.10      # how far a sign bracket projects from the wall face
LANT_W  = 0.250     # lantern cage width -- one fitting shared by all 3 lights
LANT_HG = 0.500     # lantern cage HEIGHT. 2.0 x LANT_W: ref1's cage is a slim
                    # upright box, not a cube. Change this and every light in
                    # the kit changes together.
LANT_HD = 0.220     # bell hood height = 0.88 x LANT_W (ref1)
LANT_H  = 1.320     # total height of SM_Light_LanternHanging (for beam hanging)
IRON_S  = 1.34      # value bump on iron: the palette iron is nearly black, and
                    # in ref1 the bracket still reads as a legible dark grey form
                    # against the sky rather than a silhouette hole.

# ---- why two overlapping solids in this family are never given the same plane --
# EVERY REPEATED-SOLID RUN IN THIS FAMILY STAGGERS ACROSS ITS OWN THICKNESS, and
# this constant is how far. A run of solids that overlap deliberately -- _rod's
# strap-iron segments, _crescent's carved blocks -- shares one cross-section, so
# with no stagger every consecutive pair's two cheeks are EXACTLY coplanar and only
# the wobble field keeps them apart. Measured on the shipped mesh, sign_b's arch:
# ten laps of 13.1-13.2 cm2 each, sitting 0.09-0.50 mm apart, 100% ray-reachable,
# because the arch is the outside of the piece. Family-wide it was 624 iron-on-iron
# pairs, 1131 cm2, 888 cm2 of it reachable. check_zfight reported NONE of it,
# because every individual lap is just under its 15 cm2 AREA_MIN floor -- which is
# exactly why the family read 0 cm2 and an auditor measuring without that floor
# read ~1035. Both numbers were arithmetic; only the second was about the geometry.
# 0.65 mm offsets consecutive cheek planes by 1.30 mm, above the 0.5 mm gate with
# room for the +/-0.5 mm of relative drift the wobble field adds, and on a 25 mm
# strap it is a 2.6% lateral wander nobody can see. Hand-forged iron wanders.
ROD_STAG = 0.00065


# ================================================== library work-around =====
def _solo(p, tag, fn):
    """Build ONE beveled primitive in a throwaway Part -- where it is the first
    primitive, so the bevel keeps its material -- and stamp it in. `tag` seeds
    the scratch Part's rng, so each primitive still gets its own colour jitter.
    Unbeveled primitives are unaffected and go straight onto `p`."""
    s = p.sub(f"{p.name}/{tag}")
    fn(s)
    p.merge(s)
    s.bm.free()
    s.bm = None


def _box(p, c, s, mat, tint=.05, shade=1.0, bevel=.010, seg=1, **kw):
    if not bevel:
        return p.box(c, s, mat, tint=tint, shade=shade, bevel=0, **kw)
    _solo(p, "b%.3f_%.3f_%.3f" % c,
          lambda q: q.box(c, s, mat, tint=tint, shade=shade, bevel=bevel,
                          seg=seg, **kw))


def _prism(p, pts, th, mat, tint=.05, shade=1.0, bevel=.008, seg=1, **kw):
    if not bevel:
        return p.prism(pts, th, mat, tint=tint, shade=shade, bevel=0, **kw)
    _solo(p, "p%.3f_%.3f_%d" % (pts[0][0], pts[0][1], len(pts)),
          lambda q: q.prism(pts, th, mat, tint=tint, shade=shade, bevel=bevel,
                            seg=seg, **kw))


# ============================================================== ironwork ====
def _rod(p, pts, r=.019, mat="iron", flat=.62, tint=.035, r_end=None,
         shade=IRON_S):
    """A forged bar following a polyline. `flat` squashes the bar across X so it
    reads as flat strap iron seen from the side -- which is exactly what ref1's
    bracket is. Segments overlap at the joints so the run looks continuous.
    Unbeveled on purpose: at 25mm across a chamfer is invisible and costs 4x.

    EVERY SEGMENT IS OFFSET ACROSS ITS OWN WIDTH, ALTERNATELY, BY ROD_STAG. All
    of this family's rod paths lie in the YZ plane, and beam() takes its width
    across z.cross(up), which for such a path is exactly +/-X -- so with no
    stagger every consecutive pair of segments, which overlap by `extend` ON
    PURPOSE so the run reads continuous, put both of their cheeks on one plane.
    See ROD_STAG for what that measured. Only consecutive segments overlap
    (extend is 0.85r a side against segment lengths of 45 mm and up), so
    alternating is enough, and the ends of the run do not move in Y or Z, so
    everything a rod lands on it still lands on."""
    out, n = [], max(1, len(pts) - 1)
    r1 = r if r_end is None else r_end
    for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
        rr = lerp(r, r1, (i + .5) / n)
        dx = ROD_STAG if i % 2 else -ROD_STAG
        out += p.beam((a[0] + dx, a[1], a[2]), (b[0] + dx, b[1], b[2]),
                      rr * 2 * flat, rr * 2, mat, bevel=0, tint=tint,
                      extend=rr * .85, shade=shade)
    return out


def _curl(p, at, a0, a1, r0, r1, n=7, rod=.019, rod_end=None, aspect=1.0,
          mat="iron", flat=.62, draw=True, shade=IRON_S):
    """Volute / arc of strap iron in the YZ plane -- every scroll and curved
    brace in the family. cos(a) maps to Y and sin(a) to Z, so: 90 deg = up,
    180 = outward (-Y), 270 = down. Angles near 0 point INTO the wall, so they
    are never used."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = radians(lerp(a0, a1, t))
        rr = lerp(r0, r1, t)
        pts.append((at[0], at[1] + cos(a) * rr, at[2] + sin(a) * rr * aspect))
    if draw:
        _rod(p, pts, r=rod, r_end=rod_end, mat=mat, flat=flat, shade=shade)
    return pts


def _ring(p, at, R=.034, r=.010, mat="iron", axis='X', sides=7, prof=5, tint=.03,
          shade=IRON_S):
    """Chain link / hanging eye: a small torus revolved from a circle profile."""
    profile = [(R + r * cos(TAU * i / prof), r * sin(TAU * i / prof))
               for i in range(prof + 1)]
    return p.lathe(profile, mat, at=at, sides=sides, axis=axis, tint=tint,
                   close=False, shade=shade)


def _plate(p, z0, z1, w=.105, y_out=-.036, mat="iron", bolts=2):
    """Fixing plate against the wall face, biting 0.01 into the wall."""
    _box(p, (0, y_out / 2 + .005, (z0 + z1) / 2), (w, abs(y_out) + .010, z1 - z0),
         mat, bevel=.010, seg=1, tint=.035, shade=IRON_S)
    zs = ([lerp(z0 + .055, z1 - .055, (i + .5) / bolts) for i in range(bolts)]
          if bolts > 1 else [(z0 + z1) / 2])
    for z in zs:
        p.cyl((0, y_out - .006, z), .018, .020, mat, sides=6, axis='Y',
              r_top=.012, tint=.03, shade=IRON_S)


def _hang(p, y, z_arm, z_board):
    """One hang point, read as a short CHAIN: links hooked through each other
    from the arm down to an eye bolted into the board's head rail. Rings only --
    a solid strap at this size read as a spike, not a hanger.

    THE LINK COUNT COMES FROM THE DROP. It used to be two fixed links under the
    arm plus one eye at the board, so the chain only closed when the drop
    happened to be about 0.19 m. Measured: on sign_b (drop 0.212 m) the second
    link's bottom arc stopped 21.9 mm SHORT of the eye and the board hung off
    nothing; on sign_a (drop 0.193) the same joint crossed by 1 mm, i.e. one
    vertex. Two coplanar links of radius R and bar r intersect while their
    centres are closer than 2(R+r) = 77 mm, so stepping at 2R = 60 mm leaves
    every joint 17 mm of engagement whatever the drop, and 10 mm into the eye."""
    R, r_ = .030, .0085
    z_top, z_eye = z_arm - .036, z_board + .026
    n = max(1, int(ceil((z_top - z_eye) / (2 * R))))
    for i in range(n):
        _ring(p, (0, y, lerp(z_top, z_eye, i / n)), R=R, r=r_, sides=7)
    _ring(p, (0, y, z_eye), R=.023, r=r_, sides=7)
    p.box((0, y, z_board - .004), (.026, .022, .034), "iron", bevel=0, tint=.03,
          shade=IRON_S)


# ============================================================ sign boards ====
def _teeth(p, y0, y1, z_top, n, mat, h=.046, th=.086, seed=0, axis='Y',
           ctr=0.0):
    """The house trim motif off ref3's bargeboard: a run of little tapered
    pendant teeth, tight under the board's bottom rail. Flipped about X so the
    narrow end points down. axis 'Y' runs them along Y, 'X' along X.

    `ctr` is the centre on the remaining axis -- X for a hung board (0 is right,
    the board is centred on x=0), Y for a wall-parallel run, where it MUST be
    given: left at 0 a wall-parallel tooth straddles the wall plane, so half of
    every tooth was buried in the wall and finish() flattened it back onto the
    seam. Measured overshoot 23.5 mm on the panel and 16.0 mm on the notice
    board -- 20 verts silently cut on each."""
    r = rng(f"{p.name}/teeth/{seed}")
    w = (abs(y1 - y0) / n) * .78
    for i in range(n):
        cu = lerp(y0, y1, (i + .5) / n)
        hh = h * r.uniform(.86, 1.10)
        c = (ctr, cu, z_top - hh / 2 + .006) if axis == 'Y' else \
            (cu, ctr, z_top - hh / 2 + .006)
        s = (th, w, hh) if axis == 'Y' else (w, th, hh)
        p.box(c, s, mat, bevel=0, tint=.07, rot=(180, 0, 0), taper=.46,
              taper_axis='XY', shade=1.0 + r.uniform(-.07, .07))


def _board(p, y0, y1, z0, z1, field, frame, th=.052, rail=.060, head=.076,
           proud=.016, nplank=4, seed=0, teeth=8, cornice=False, pegs=True):
    """Plank field in an oak frame, hung perpendicular to the wall (faces +/-X).
    Planks run vertically; head and sill rails are deeper than the stiles, the
    way a real framed board is put together, and the frame stands `proud` of the
    planks on both faces so the panel sits in shadow."""
    r = rng(f"{p.name}/board/{seed}")
    fw = th + proud * 2
    for i in range(nplank):
        cy = lerp(y0 + rail * .55, y1 - rail * .55, (i + .5) / nplank)
        w = (y1 - y0 - rail * 1.1) / nplank
        _box(p, (0, cy, (z0 + z1) / 2), (th * r.uniform(.94, 1.06), w - .010,
             z1 - z0 - head * .9), field, bevel=.009, seg=1, tint=.05,
             shade=1.0 + r.uniform(-.05, .05))
    # A BACK PLATE BEHIND THE PLANK JOINTS. The field is nplank boards with 10 mm
    # gaps and NOTHING behind them, on a sign built to hang across the street and
    # be read face-on: dead ahead you looked straight through it, three slots of
    # sky 10 x 597 mm on sign_a (rendered and checked, not assumed). At 24 mm
    # against the planks' 52 the plate cannot be coplanar with them, and its four
    # edges finish inside the frame.
    _box(p, (0, (y0 + y1) / 2, (z0 + z1) / 2),
         (.024, y1 - y0 - .080, z1 - z0 - .080), field, bevel=0, tint=.04,
         shade=.72)
    _box(p, (0, (y0 + y1) / 2, z1 - head / 2), (fw, y1 - y0, head), frame,
         bevel=.011, seg=1, tint=.06)
    _box(p, (0, (y0 + y1) / 2, z0 + head / 2), (fw, y1 - y0, head), frame,
         bevel=.011, seg=1, tint=.06)
    # STILES, tenoned BETWEEN the rails and held 4 mm in from their faces and
    # 6 mm in from their ends. Built flush -- same fw, same y0/y1 -- every stile
    # cheek and end landed on a rail plane: 4 x 6.5 cm2 of coincident end face
    # and 8 x 4.5 cm2 of coincident cheek per board. Those sit under
    # check_zfight's 15 cm2 floor, but they are on the board's visible faces,
    # and the notice board's version of the identical joint measured 292 cm2.
    stiles = (y0 + rail / 2 + .006, y1 - rail / 2 - .006)
    for sy in stiles:
        _box(p, (0, sy, (z0 + z1) / 2), (fw - .008, rail, z1 - z0 - head * 1.8),
             frame, bevel=.011, seg=1, tint=.06)
    if cornice:
        # 10mm into the head rail: sitting on it, the cornice's underside and
        # the rail's top face were 2mm apart over the board's whole length
        _box(p, (0, (y0 + y1) / 2, z1 + .016), (fw + .034, y1 - y0 + .050, .060),
             frame, bevel=.012, seg=1, tint=.06)
    if pegs:                              # forged pegs through the frame corners
        for sy in stiles:
            for zz in (z0 + head / 2, z1 - head / 2):
                for sx in (-1, 1):
                    p.cyl((sx * (fw / 2 - .004), sy, zz), .014, .016, "iron",
                          sides=5, axis='X', r_top=.009, tint=.03,
                          shade=IRON_S)
    if teeth:
        _teeth(p, y0 + .040, y1 - .040, z0 + .004, teeth, frame, th=fw * .78,
               seed=seed)


def _letters(p, y0, y1, z, x_face, n=7, mat="flower_gold", seed=0, h=.052, sgn=1,
             bed=.006, proud=.009):
    """Illegible gold glyph-marks, exactly like the lettered band in ref2's
    porch: a row of little raised blocks of uneven width and height.

    `x_face` IS THE PLANE OF THE SURFACE THE GLYPHS ARE APPLIED TO, and each
    block is cut `bed` into it and stands `proud` of it, so a glyph cannot float
    clear of its board. It used to be placed x_face + 0.007 with a 13 mm block,
    i.e. entirely in front of whatever was passed, and every caller but
    wall_panel then passed a plane in front of the field as well: measured, 32 of
    the 34 glyphs on the three hanging boards (10 of 10 on A, 6 of 8 on B, 16 of
    16 on C) touched nothing at all, standing 0.7-10.1 mm clear of the nearest
    solid."""
    r = rng(f"{p.name}/letters/{seed}")
    th = bed + proud
    for i in range(n):
        cy = lerp(y0, y1, (i + .5) / n)
        w = (y1 - y0) / n * r.uniform(.40, .68)
        p.box((x_face + sgn * (proud - th / 2), cy, z + r.uniform(-.004, .004)),
              (th, w, h * r.uniform(.72, 1.12)), mat, bevel=0, tint=.10,
              shade=1.0 + r.uniform(-.10, .10))


def _tankard(p, at, x_face, sgn, s=1.0, seed=0):
    """ref2's painted sign: a golden foaming tankard. A tall waisted vessel, a
    strap handle, and a head of plaster froth standing OVER the rim with one
    drip running down the side.

    `x_face` is the plane of the FIELD the emblem is painted on, and the vessel
    is bedded 5 mm into it. It used to be x_face + 0.008 with a 15 mm prism, so
    the whole emblem stood clear of whatever was passed: measured 7.0 mm of air
    behind sign_a's tankard and 3.5 mm behind the wall panel's, both of them
    hanging off the frame rail they happened to cross."""
    y, z = at
    xf = x_face + sgn * .0025
    bw, bh = .105 * s, .240 * s
    body = [(y - bw * .82, z - bh / 2), (y + bw * .82, z - bh / 2),
            (y + bw * .98, z - bh * .10), (y + bw * 1.06, z + bh / 2),
            (y - bw * 1.06, z + bh / 2), (y - bw * .98, z - bh * .10)]
    _prism(p, body, .015, "flower_gold", axis='X', at=(xf, 0, 0), bevel=.006,
           seg=1, tint=.07)
    _curl(p, (xf + sgn * .001, y + bw * 1.00, z - bh * .06), -78, 78, bh * .33,
          bh * .33, n=5, rod=.015, flat=.55, mat="flower_gold", shade=1.0)
    # froth: three low lumps sitting ON the rim, wider than the vessel
    r = rng(f"{p.name}/froth/{seed}")
    rot = (0, 180, 0) if sgn > 0 else None
    # ... and each lump is a DIFFERENT DEPTH. blob() finishes in one flat ngon at
    # full depth, so four lumps sharing a depth and a base plane put their proud
    # faces on ONE plane where they overlap: measured 7 pairs, 35.0 cm2, 0.025 mm
    # apart and 100% ray-reachable -- the froth head is the brightest thing on the
    # board.
    #
    # THE DEPTHS ARE CHOSEN AGAINST THREE OTHER PLANES, not just each other, and
    # the first attempt got that wrong: .0135 puts a lump's proud face EXACTLY on
    # the vessel's own front face (x_face + 0.0075), which the lumps overlap in
    # projection because the froth sits over the rim. That turned a 35 cm2
    # sub-floor sliver into a 29.5 cm2 pair the gate reports -- measured, not
    # guessed. In units of depth from the froth's base plane, the planes to avoid
    # are the vessel front at .0135, the handle's cheek at .0111 and the board
    # frame's cheek at .0195; only lumps 0-1, 1-2 and 2-3 overlap each other
    # (0-2, 1-3, 0-3 are clear by 0.11 x bw or more, jitter included), so three
    # values in the safe .0150-.0185 band are enough.
    for i, (dy, dz, sc, dp) in enumerate(((-.86, -.10, 1.00, .0157),
                                          (-.30, .10, 1.15, .0183),
                                          (.34, .13, 1.05, .0170),
                                          (.88, -.08, .88, .0157))):
        # back=False: the froth lumps overlap each other, so their flat backs
        # -- all four on one plane, and that plane a hair off the vessel's own
        # face -- were the loudest pair on the sign boards. The backs are
        # buried in the vessel and the board behind it: the lumps sit ABOVE the
        # rim, so the plane they open onto is the field, not the vessel, and
        # -0.004 is what puts it inside the field rather than 4 mm in front.
        p.blob((xf - sgn * .006, y + dy * bw, z + bh * .44 + dz * bh),
               (bw * 1.05 * sc, dp, bh * .42 * sc), "plaster", sides=6,
               axis='X', irregular=.16, dome=.5, bevel=0, seg=1, tint=.045,
               back=False, rot=rot, seed=seed * 7 + i,
               shade=1.0 + r.uniform(-.05, .04))
    p.blob((xf - sgn * .006, y + bw * 1.02, z + bh * .16), (bw * .38, .0122,
           bh * .40), "plaster", sides=5, axis='X', irregular=.20, dome=.5,
           bevel=0, seg=1, tint=.045, back=False, rot=rot, seed=seed * 31)


def _crescent(p, at, x_face, sgn, s=1.0, seed=0):
    """Crescent moon + star -- the other classic inn sign. The crescent is a run
    of tangentially rotated blocks, thick at the belly and tapering to the
    horns, so it reads as a drawn curve and not a staircase.

    `x_face` is the plane of the FIELD, and the blocks are bedded 5 mm into it.
    At x_face + 0.008 the whole crescent floated 1.0 mm off the shield's plaster
    -- close enough that wobble closed it to 0.14-0.48 mm on one face, which is
    the 75 cm2 of plaster-vs-gold check_zfight reports on this piece (sealed
    behind the crescent itself: 0% of it is reachable by a ray). Bedding the
    blocks makes their backs interior to the plaster instead."""
    y, z = at
    xf = x_face + sgn * .0025
    R, n, span = .165 * s, 13, 132.0
    step = radians(span) * R / n
    for i in range(n):
        adeg = lerp(90 - span / 2, 90 + span / 2, (i + .5) / n) + 90
        a = radians(adeg)
        t = abs((i + .5) / n - .5) * 2
        th = lerp(.072, .016, t ** 1.5) * s
        # STAGGERED ACROSS X, like _rod's segments and for the same reason: the
        # blocks overlap by design (step x 1.14) and rot is about X, which leaves
        # every block's two cheeks on one plane. Measured: 72 gold-on-gold pairs,
        # 275 cm2, 138 cm2 of it ray-reachable -- the FRONT of the emblem. The
        # 1.3 mm step also gives the run the hand-cut relief it should have.
        p.box((xf + (ROD_STAG if i % 2 else -ROD_STAG),
               y + cos(a) * R, z + sin(a) * R), (.015, step * 1.14, th),
              "flower_gold", bevel=0, tint=.07, rot=(adeg + 90, 0, 0),
              shade=1.0 + (.05 if i % 2 else -.04))
    pts = []
    for i in range(10):
        a = radians(90 + i * 36)
        rr = (.058 if i % 2 == 0 else .024) * s
        pts.append((y + R * .96 + cos(a) * rr, z + R * .30 + sin(a) * rr))
    # the star laps the horn blocks, so it is off both of their planes too
    p.prism(pts, .015, "flower_gold", axis='X', at=(xf + ROD_STAG * 2, 0, 0),
            bevel=0, tint=.07)


# =============================================================== lantern =====
# THE GLAZING IS Part.glazing() AND NOTHING ELSE.
# ---------------------------------------------------------------------------
# Shanee, across four different families: "the yellow glass pane and criss cross
# doesn't reach the window frame and there's a gap between the timber window
# frame and the plaster sides ... I suspect we should make sure all windows are
# proper as it's a common issue." He is right, and this family was one of the
# forks. What used to be here was `_panes()`: a glass box cut to the glazing
# bars' CENTRE line with a grid of bars laid on top of it and four separate
# corner posts around the lot. Nothing lapped anything; the pane's edge and the
# bar's centre coincided, so the amber ended exactly where the iron began and
# any wobble opened a line between them.
#
# util.Part.glazing() builds frame + glass + leading in one call and makes the
# three recurring faults impossible by construction: the pane is cut OVERSIZE
# (opening + rebate all round) with the frame lapped over its edge, the bars are
# generated across the whole opening and clipped to the pane, and the frame
# oversails onto what surrounds it instead of butting to it. It also holds the
# bars clear of the glass plane so the two are never coplanar.
#
# ONE THING NEEDS EXPLAINING -- THE SCALE. glazing() fixes its frame at 55 mm
# thick in Y and its bar stand-off at 2.6 x `lead`, because it is dimensioned
# for a window in a wall. A lantern cage is 250 mm across: a 55 mm frame would
# eat a fifth of the whole fitting and sink the glazing bars 40 mm behind its
# face. So each face is built at LANT_S : 1 in a scratch Part and merged back at
# 1 / LANT_S, which scales those two fixed numbers along with everything else
# and leaves an 11 mm iron frame with its bars close behind it. Same primitive,
# same guarantees, no fork -- and if that ever stops being true the answer is to
# say so, not to write a second _panes().
#
# LANT_S is 5 and not 3 for a measured reason. A cage is glazed on FOUR faces,
# and glazing() cuts every pane OVERSIZE by design, so the four panes have to
# cross each other somewhere inside the lantern. How far they cross is set by how
# far behind the face the pane sits, which is (2.889 x bar thickness + 0.055 /
# LANT_S). At LANT_S = 3 that came to 44 mm and each pane ran 40 mm past its
# neighbour's plane -- the front pane's bars showed up as loose horizontal tabs
# floating inside the SIDE pane, which reads as a modelling error. At 5, with a
# 30 mm frame face and a 12 mm rebate, the pane sits 31 mm back and overruns by
# 13 mm, which disappears behind the corner. The oversize pane stays: that is the
# guarantee, and the crossing is the price of a four-sided cage, not a bug.
LANT_S  = 5.0        # build scale for the lantern's glazed faces (see above)
LANT_FO = 0.030      # frame face width on the finished fitting = frame + overlap
GLZ_REB = 0.012      # rebate, as _glazed_cage passes it (x LANT_S, back at 1/LANT_S)

# WHERE THE OVERSIZE PANE'S EDGES ACTUALLY LAND. Anything that caps the cage must
# be dimensioned from THIS and not from the cage's nominal box, because the pane is
# not the cage: glazing() cuts it `rebate` proud of an opening already inset
# LANT_FO, so on the finished fitting the glass runs from z0 + GLZ_EDGE to
# z0 + hg - GLZ_EDGE. MEASURED on both cages this family builds and on a third
# probe size -- 0.0180 every time, and the frame 0.0050 every time, so the shared
# insert IS scale-consistent. What was NOT consistent was the two hosts' capping
# members: _bell's tuck-under lands on the hung lantern's pane top by construction,
# while the sconce's collar was dimensioned from z1 alone and stopped 2.1 mm above
# it, and nothing at all reached the pane's BOTTOM edge on either fitting (the pan
# stopped 1.5 mm below it). Result, measured with a contact graph over the finished
# mesh: the sconce's four panes and sixteen leading bars were a 20-component ISLAND
# touching nothing else in the piece. That is the fifth "insert pinned inside a
# host" and the fifth "member stops short" in one joint.
GLZ_EDGE = LANT_FO - GLZ_REB          # 0.018 -- pane edge inset from the cage end
GLZ_LAP  = 0.006                      # how far a capping member beds past it


def _bar_pitch(ow, oh):
    """Pitch for glazing()'s leading on a lantern face, in the LANT_S build.

    glazing() walks its bars out from k = -(gw + gh) in steps of `cell`, so a
    pitch that divides that reach exactly puts one bar dead on the centre line
    and the rest symmetrically either side. Aiming at 0.32 of the pane height
    and then snapping to the nearest exact divisor gives ONE bar across the
    width and THREE up the height on every cage size this family builds --
    ref1's 2-wide grid, and the same rhythm on the sconce as on the hung lamp."""
    gw = (ow + .024) * LANT_S                 # = size + 2 * rebate, as glazing cuts it
    gh = (oh + .024) * LANT_S
    reach = gw + gh
    return reach / max(1.0, round(reach / (gh * .32)))


def _glazed_cage(p, at, w, hg, tag=""):
    """The four glazed faces of a lantern cage, from the shared primitive.

    The four frames lap each other at the corners and ARE the cage's corner
    posts and its top and bottom rails -- there is nothing left for a separate
    post to do, and one solid at a corner cannot open a line the way a post
    butted against two panes could. `at` is the cage's bottom centre."""
    x0, y0, z0 = at
    hw = w / 2
    ow = w - 2 * LANT_FO                      # clear opening across a face
    oh = hg - 2 * LANT_FO                     # ... and up it
    for k in range(4):
        s = p.sub(f"{p.name}/glz{tag}{k}")
        # The bars are glazing()'s LEADING, not its `mullions` / `transoms`: a
        # lantern bar is a thin flat, and leading is what the primitive draws
        # thin. It is also what fits -- a mullion + two transoms are beveled
        # boxes at BEVEL_SEG segments and cost 324 tris a face against the
        # leading's 48, which over four faces is the whole "sign" budget again.
        # `cell` is chosen so one bar lands on the centre line and three run
        # across it: ref1's 2-wide cage, one row finer than its crop resolves.
        LEAD = .007 * LANT_S / .9      # glazing() cuts bars at 0.9 x lead -> 7 mm
        s.glazing((0.0, -hw * LANT_S, 0.0), (ow * LANT_S, oh * LANT_S),
                  depth=LEAD * 2.6 + .055, frame=.020 * LANT_S,
                  rebate=.012 * LANT_S, lead=LEAD, overlap=.010 * LANT_S,
                  pattern="square", cell=_bar_pitch(ow, oh),
                  mullions=0, transoms=0,
                  mat_frame="iron", mat_glass="glass", mat_lead="iron", tint=.03)
        # glazing() takes no `shade`, and this family's iron needs IRON_S or it
        # renders as a silhouette hole rather than ref1's legible dark grey
        # ironwork (see the note by IRON_S). Repaint only -- no geometry is
        # touched, so the primitive is still the single source of the form.
        gi = s._mats.index("glass")
        s._paint([f for f in s.bm.faces if f.material_index != gi], "iron",
                 .03, IRON_S)
        p.merge(s, at=(x0, y0, z0 + hg / 2), rot=(0, 0, 90 * k),
                scale=1.0 / LANT_S)
        s.bm.free()
        s.bm = None


def _pan(p, at, hw, h=.020, sides=4, pane_z=None):
    """The cage's BASE PAN. _glazed_cage builds four glazed WALLS and nothing
    else, so the cage had no floor: measured, the four frames were their own
    island 5.9 mm clear of the hood, their sill rails oversailed the stepped
    foot by 33 mm in plan, the flame stood on nothing 20.0 mm up in the air, and
    a camera below looked straight into the lantern. The pan is sized so its
    flats land ON the frame band -- hw - 0.011 out to hw -- which is what the
    rails actually bear on, and it doubles as the drip tray the sconce's finial
    hangs from.

    `pane_z` IS THE Z OF THE GLASS'S BOTTOM EDGE, and given it the pan grows
    UPWARD to bed GLZ_LAP past it, so the glazing stands on its floor instead of
    hovering 1.5 mm over it (see GLZ_EDGE -- that hover is why the sconce's whole
    glazed panel was a floating island). Only the TOP face moves: the pan's
    underside, which is the moulding you see below the sill rail, stays put, and
    the extra height is inside the cage behind the rail. The pan's top face
    already covers the pane's footprint -- its flats sit at 0.962 x hw against a
    pane plane at hw - 0.031 and pane corners at 0.94 x hw -- so height was the
    only thing missing."""
    z0, z1 = at[2] - h / 2, at[2] + h / 2
    if pane_z is not None:
        z1 = max(z1, pane_z + GLZ_LAP)
    return p.cyl((at[0], at[1], (z0 + z1) / 2), hw * 1.48, z1 - z0, "iron",
                 sides=sides, phase=pi / 4, r_top=hw * 1.36, tint=.03,
                 shade=IRON_S)


def _bell(p, at, hw, ch, sides=8, dome=1.04, lip=1.36):
    """The lantern hood as a CONVEX BELL. ref1's hood gains half-width fast at
    the apex and almost none at the shoulder (4.5, 7, 9, 11, 12.5 px over 13 px
    of drop) -- that is a dome, and a cone is the one shape it is not. So the
    dome is swept on a quarter-circle IN THE ANGLE, which puts the profile
    points where the curvature actually is. Two things stop the dome reading as
    a smooth rubber cap: the shoulder only just oversails the cage (`dome` is
    barely over 1.0, so the bell continues the line of the corner posts), and
    below it a short vertical SKIRT cuts a hard shadow line before the lip
    flicks outward-and-down and tucks back under -- the roofs' swept eave, which
    is what ties this fitting to the rest of the kit.
    `ch` is total height; `at` sits at the tip of the flicked lip, so a caller
    just drops it on the cage's top rail -- and the profile then RETURNS 14 mm
    below that tip at hw*0.94, which is inside the frame band (hw-0.011 .. hw)
    of the rail underneath. Without that return the hood met the cage nowhere:
    the lip flares outboard of the cage's faces and inboard of its corner posts,
    the tuck-under ended at hw*0.91, and the whole hood cleared the cage's top
    face by 1 mm -- glazing() insets its head rail by overlap/2, so the cage
    actually stops 5 mm short of z1.

    ONE FIXED BAND, AND IT IS NOT SCALED BY `ch`: the skirt/lip/tuck profile below
    the shoulder is authored in absolute metres (0.070 down to -0.014), so the dome
    gets ch - 0.092 and the flick gets the rest. Radius scales with `hw` throughout,
    so a smaller CAGE is fine; a smaller ch is not. Measured on probes: ch 0.220 ->
    dome height 0.128, 0.180 -> 0.088, 0.140 -> 0.048, 0.100 -> 0.008, i.e. the dome
    is gone by ch 0.10 and inverts below 0.092. The family's only caller passes
    LANT_HD = 0.220, so this is a limit and not a live fault -- but it is the
    "fixed dimension inside a scaled host" pattern, so: do not call _bell with
    ch < 0.13 without rewriting the band as fractions of ch."""
    Rd, Hd = hw * dome, ch - .092
    prof = [(.006, ch)]
    for a in (26, 46, 64, 79, 90):
        t = radians(a)
        prof.append((Rd * sin(t), ch - Hd * (1 - cos(t))))   # ends at the shoulder
    prof += [(Rd * .98, .070),                # skirt: a crisp shadow line ...
             (hw * lip, .042),                # ... before the lip flicks OUT
             (hw * (lip - .13), .000),        # the tip drops below the flare
             (hw * (lip - .45), .036),        # and tucks back under
             (hw * .94, -.014)]               # ... onto the cage's top rail
    return p.lathe(prof, "iron", at=at, sides=sides, tint=.035, shade=IRON_S)


def _lantern(host, w=LANT_W, hg=LANT_HG, ch=LANT_HD, tag="", lit=True):
    """THE lantern fitting. One body shared by all three lights so the inn's
    lamps match. Proportion straight off ref1: the glass cage is TWICE as tall
    as it is wide (0.250 x 0.500) and glazed 2 wide, so the fitting is a slim
    upright box of light; over it a convex bell hood 0.9x the cage width tall.
    The bar pitch comes from _bar_pitch(), which lands one bar on the centre
    line and three across it -- ref1's 2-wide cage, one row finer than the crop
    it was measured from resolves.
    Bottom at z=0, centred on x=y=0. Returned as a sub-Part for merge()."""
    s = host.sub(host.name + "_lant" + tag)
    hw = w / 2
    z0, z1 = .052, .052 + hg
    # stepped square foot: a cage this tall needs a base broad enough to stand on
    s.cyl((0, 0, .018), hw * 1.30, .036, "iron", sides=4, phase=pi / 4,
          r_top=hw * 1.12, tint=.03, shade=IRON_S)
    # the upper step is bedded 11mm INTO the lower one. Stacked so their faces
    # only touched, the whole 370 cm2 disc of the foot z-fought -- the single
    # worst pair in this family, on the fitting the family is judged on.
    s.cyl((0, 0, .041), hw * 1.08, .032, "iron", sides=4, phase=pi / 4,
          r_top=hw * .92, tint=.03, shade=IRON_S)
    _pan(s, (0, 0, z0 + .006), hw, pane_z=z0 + GLZ_EDGE)   # the floor -- see _pan
    if lit:
        # the flame inside the cage, STANDING ON THE PAN (it used to start
        # 20.0 mm above the foot, a candle floating inside the glass). Its base
        # is 10 mm up into the pan -- deep enough that its bottom cap is not
        # sitting a millimetre off the foot's top face, which reads as 27 cm2 at
        # a 1.5 mm tolerance. The AMBER PANES themselves come from
        # _glazed_cage / Part.glazing() -- do not add a glass box here.
        zc0, zc1 = z0 + .010, z0 + hg * .43
        s.cyl((0, 0, (zc0 + zc1) / 2), .032, zc1 - zc0, "glass", sides=6,
              tint=.02, r_top=.009)
    _glazed_cage(s, (0, 0, z0), w, hg, tag=tag or "L")
    _bell(s, (0, 0, z1 - .004), hw, ch)      # lip tip lands on the top rail
    s.cyl((0, 0, z1 + ch + .010), .024, .032, "iron", sides=6, r_top=.013,
          tint=.03, shade=IRON_S)
    _ring(s, (0, 0, z1 + ch + .056), R=.032, r=.010, sides=6, prof=5)
    s.top = z1 + ch + .088
    return s


def _cage(p, at, w=.215, hg=.430):
    """The same 2 x 3 cage built in place (for the sconce, which is not hung).
    Same 2:1 proportion as the hung lantern, just a touch smaller all over --
    and the same shared glazing, so the two fittings cannot drift apart."""
    x0, y0, z0 = at
    _pan(p, (x0, y0, z0 + .006), w / 2, pane_z=z0 + GLZ_EDGE)   # floor + finial fixing
    zc0, zc1 = z0 + .010, z0 + hg * .43
    p.cyl((x0, y0, (zc0 + zc1) / 2), .028, zc1 - zc0, "glass", sides=6,
          r_top=.008, tint=.02)
    _glazed_cage(p, at, w, hg, tag="B")


# ========================================================= hanging signs ====
def sign_a():
    """A -- the standard inn board: straight strap-iron arm, an elliptical knee
    brace bowing up into its root, a volute at the tip, cream field, ref2's
    golden tankard."""
    p = Part("SM_Sign_InnBoard_A", budget="sign",
             seams=dict(x=(-.090, .090), y=(-1.24, .022), z=(0, 1.34)))
    ARM, az = REACH, ARM_Z
    y0, y1 = -1.035, -.125
    bz0, bz1 = .058, .795
    _plate(p, .660, 1.140, bolts=2)
    # the arm's root sits ON the wall plane, not 12 mm inside it: _rod extends
    # each end by 0.85r, which took it to y = +0.031 and finish() then clamped
    # 4 verts back onto the y = 0.022 seam. It still runs through the plate.
    _rod(p, [(0, .000, az), (0, -ARM, az)], r=.022, flat=.60)
    # THE BRACE BOWS UP OVER THE BOARD, not down into it. Centred on the arm at
    # (0, az) with aspect 0.50 the quarter-ellipse was concave the wrong way: its
    # belly ran at z 0.781 through a board whose head is at 0.795, so it entered
    # the head rail at y=-0.125 and 0.34 m of the piece's signature member -- 22 mm
    # of strap iron at x +/-0.011, inside a 52 mm plank field -- was buried where
    # nothing could see it, and the brace read as CUT OFF by the board (rendered
    # and looked at). Re-centred at the far end so the arc rises from the plate at
    # z 0.70 to the arm's underside at y=-0.24, belly 60 mm clear of the board.
    _curl(p, (0, -.45, az - .30), 0, 62, .45, .45, n=8, aspect=.667, rod=.018,
          rod_end=.015)
    _curl(p, (0, -ARM + .014, az - .114), 88, 428, .118, .020, n=8, rod=.016,
          rod_end=.010)
    _curl(p, (0, -.102, az + .108), 250, -26, .094, .018, n=6, rod=.015,
          rod_end=.010)
    p.box((0, -.052, az), (.062, .070, .070), "iron", bevel=0, tint=.03, shade=IRON_S)
    for y in (lerp(y0, y1, .16), lerp(y0, y1, .84)):
        _hang(p, y, az - .012, bz1)
    _board(p, y0, y1, bz0, bz1, "plaster", "oak_mid", th=.052, rail=.058,
           head=.078, nplank=4, seed=1, teeth=9)
    for sgn in (-1, 1):
        # x_face is the PLANK FIELD's own face (th/2), not a plane out in front
        # of it: the emblem and the glyphs are bedded into the planks.
        _tankard(p, ((y0 + y1) / 2, (bz0 + bz1) / 2 + .098), sgn * .026, sgn,
                 s=1.20, seed=3)
        _letters(p, y0 + .180, y1 - .180, bz0 + .150, sgn * .026, n=5, seed=4,
                 h=.050, sgn=sgn)
    p.wobble(.0055, freq=2.4, respect_seams=False)
    return p.finish()


def sign_b():
    """B -- a shield board under an ARCHED arm with a diagonal stay: cream
    field, iron edge-strapping and rivets, gold crescent and star."""
    p = Part("SM_Sign_InnBoard_B", budget="sign",
             seams=dict(x=(-.098, .098), y=(-1.20, .022), z=(0, 1.44)))
    ARM = 1.06
    _curl(p, (0, -ARM / 2, ARM_Z - .335), 171, 9, ARM / 2, ARM / 2, n=9,
          aspect=.62, rod=.020)
    _plate(p, .545, .860, bolts=2)
    _plate(p, 1.150, 1.330, w=.095, bolts=1)
    # the stay LANDS ON THE ARCH. It used to stop at ARM_Z + 0.048, which is
    # 35 mm above the arch's crown, and the upper plate + stay were measured as
    # their own island: nothing they touched touched the sign.
    _rod(p, [(0, -.018, 1.272), (0, -ARM / 2 + .03, ARM_Z)], r=.016,
         flat=.58)
    _curl(p, (0, -ARM / 2 - .050, ARM_Z), 62, 330, .070, .016, n=5, rod=.013,
          rod_end=.009)
    _curl(p, (0, -ARM + .050, ARM_Z - .375), 96, 400, .080, .018, n=7, rod=.016,
          rod_end=.010)
    # ---- shield board
    cy, top, bot, hw = -.530, .760, .050, .350
    out = [(-hw, top), (hw, top), (hw, top - .315), (hw * .78, bot + .145),
           (0., bot), (-hw * .78, bot + .145), (-hw, top - .315)]
    _prism(p, [(u + cy, v) for (u, v) in out], .058, "oak_mid", axis='X',
           bevel=.012, seg=1, tint=.05)
    mid = (top + bot) / 2
    inn = [(u * .84 + cy, lerp(mid, v, .84)) for (u, v) in out]
    _prism(p, inn, .080, "plaster", axis='X', bevel=.010, seg=1, tint=.045)
    ring = [(0, u + cy, v) for (u, v) in out] + [(0, out[0][0] + cy, out[0][1])]
    _rod(p, ring, r=.015, flat=1.60, mat="iron", tint=.03)
    # RIVETS THROUGH THE STRAPPING, so on the strap's own line (the outline) and
    # at x = +/-0.028, which beds 4 mm into the 48 mm-wide strap. At 0.90 of the
    # outline and x = +/-0.052 all 14 of them floated: measured 12.7-16.3 mm from
    # the nearest solid, gold-headed pegs hanging in mid-air off the shield.
    for (u, v) in out:
        for sx in (-.028, .028):
            p.cyl((sx, u + cy, v), .015, .018, "iron",
                  sides=5, axis='X', r_top=.010, tint=.03, shade=IRON_S)
    for sgn in (-1, 1):
        # x_face is the plaster field's own face: the inner prism is 0.080
        # thick, so +/-0.040, and emblem and glyphs are bedded into it.
        _crescent(p, (cy, mid + .058), sgn * .040, sgn, s=1.05, seed=5)
        _letters(p, cy - .175, cy + .175, bot + .155, sgn * .040, n=4, seed=8,
                 h=.040, sgn=sgn)
    for t in (.235, .765):
        _hang(p, lerp(-.058, -ARM + .058, t), ARM_Z - .038, top - .010)
    p.wobble(.0055, freq=2.4, respect_seams=False)
    return p.finish()


def sign_c():
    """C -- the long lettered board (ref2's porch band) held INSIDE a
    rectangular iron frame: arm out, drop rod at the tip, spike finial. Same
    plate and arm height as A and B, completely different silhouette."""
    p = Part("SM_Sign_InnBoard_C", budget="sign",
             seams=dict(x=(-.098, .098), y=(-1.22, .022), z=(0, 1.28)))
    ARM, az = 1.115, ARM_Z
    y0, y1 = -1.035, -.175
    bz0, bz1 = .215, .800
    _plate(p, .660, 1.140, bolts=2)
    # the stay's wall plate dropped to 0.105-0.285 with the stay itself: from
    # z 0.322 the stay entered the board's bottom rail at y = -0.654 and ran
    # 0.48 m INSIDE the planks before coming out under them -- a brace that
    # vanishes for half its length. From 0.190 it passes 32 mm clear underneath.
    _plate(p, .105, .285, w=.090, bolts=1)
    # arm and stay roots pulled back to the wall plane; _rod's 0.85r end
    # extension put them 5.2 mm and 2.4 mm past the y = 0.022 seam and finish()
    # clamped 6 verts.
    _rod(p, [(0, .000, az), (0, -ARM, az)], r=.021, flat=.60)
    # flat .52: at .60 the tip rod is 22.8 mm across X against the arm's 25.2, so
    # their cheeks ran 1.2 mm apart over the 15 cm2 where they cross at the elbow.
    _rod(p, [(0, -ARM, az + .020), (0, -ARM, bz0 - .085)], r=.019, flat=.52)
    # flat .80, not .58: at 17.4 mm across X this stay's cheeks sat 0.35 mm from
    # the frame hangers' 18.0 mm ones where it passes through them. 24.9 mm gives
    # 3.5 mm of nominal clearance there and 2.5 mm from the tip rod's 19.8 -- and
    # it matches the arm above, which is 25.2. (.66 was tried first and was the
    # worst of the three: it put the stay within 0.02 mm of the TIP ROD, adding
    # two 5.9 cm2 reachable pairs. Measured, not reasoned.)
    _rod(p, [(0, .004, .190), (0, -ARM + .012, bz0 - .070)], r=.015, flat=.80)
    p.cyl((0, -ARM, az + .062), .028, .080, "iron", sides=6, r_top=.004,
          tint=.03, shade=IRON_S)
    _curl(p, (0, -ARM + .078, bz0 - .092), 182, -136, .078, .016, n=6, rod=.014,
          rod_end=.009)
    _curl(p, (0, -.118, az - .100), 92, 352, .095, .018, n=7, rod=.015, rod_end=.010)
    for y in (lerp(y0, y1, .13), lerp(y0, y1, .87)):
        # the frame's two hangers RUN INTO the arm above and the cornice below.
        # At height az-bz1-0.040 the top of each stopped at z 0.970 -- 9 mm short
        # of the arm's underside -- and only lapped the cornice by 2 mm, so the
        # board hung from a pair of straps that reached neither end.
        # 18 mm across X, not 24: the arm is 25.2 mm, so a 24 mm strap running
        # 31 mm up inside it put two cheeks 0.6 mm apart.
        #
        # AND EACH STRAP LEANS 1.6 deg, WHICH IS THE ONLY RELIABLE FIX FOR A
        # CROSSING PAIR IN THIS FAMILY. Measured, and it is worth writing down:
        # p.wobble(.0055) displaces a whole SMALL solid by up to 2.8 mm in x --
        # this strap's 18.0 mm section comes out of the build spanning
        # x[-0.0065,+0.0120], i.e. shifted +2.75 mm -- while a long solid like the
        # stay it crosses gets a different displacement. So the separation between
        # two crossing members is drawn from the noise field, not from the design:
        # widening the stay from 17.4 to 24.9 mm took its nominal clearance from
        # 0.35 mm to 3.5 mm and the MEASURED separation went 0.477 -> 0.189 mm.
        # A nominal nudge is a coin toss; a 1.6 deg lean is not, because it takes
        # the cheek's NORMAL off +/-X (0.9996 against check_zfight's 0.99985 guard)
        # and makes the two faces genuinely splay 2.5 mm across a 90 mm lap. A
        # forged strap is not plumb to a tenth of a degree anyway.
        p.box((0, y, (bz1 + az) / 2), (.018, .028, az - bz1 + .020),
              "iron", bevel=0, tint=.03, shade=IRON_S, rot=(0, 1.6, 0))
        p.box((0, y, bz0 - .040), (.018, .028, .090), "iron", bevel=0, tint=.03,
              shade=IRON_S, rot=(0, -1.6, 0))
    _board(p, y0, y1, bz0, bz1 - .034, "oak_pale", "oak_dark", th=.052, rail=.056,
           head=.062, nplank=3, seed=6, teeth=9, cornice=True, pegs=False)
    for sgn in (-1, 1):
        _letters(p, y0 + .110, y1 - .110, (bz0 + bz1) / 2 - .006, sgn * .026,
                 n=8, seed=7, h=.100, sgn=sgn)
    p.wobble(.0055, freq=2.4, respect_seams=False)
    return p.finish()


# ================================================================ lights ====
def wall_lantern_a():
    """ref1's hero fitting: a slender iron crook off the wall with the double
    curl at its head, and the bell lantern hanging under it. The whole crook
    rides at `az`, which is set from the lantern's own top -- in ref1 the hood
    apex sits right up under the curl junction, so the drop link is short."""
    p = Part("SM_Light_WallLantern_A", budget="sign",
             seams=dict(x=(-.21, .21), y=(-.76, .022), z=(0, 1.34)))
    lant = _lantern(p, tag="A")
    hy = -.430
    p.merge(lant, at=(0, hy, 0.0))
    top = lant.top
    az = top + .100                       # crook head: one short link above the hood
    _plate(p, az - .150, az + .324, w=.100, bolts=2)
    _curl(p, (0, 0, az - .064), 90, 180, abs(hy), abs(hy), n=8, aspect=.80,
          rod=.019, rod_end=.016)
    _curl(p, (0, hy + .058, az), 200, -95, .098, .020, n=7, rod=.015, rod_end=.010)
    _curl(p, (0, hy - .062, az - .018), -30, 240, .074, .016, n=5, rod=.013,
          rod_end=.009)
    # flat .92, not .72: at .72 this link is 18.7 mm across X and the scrolls it
    # hangs between are 12.4-18.6 mm, so its cheeks sat 0.1-1.3 mm off theirs
    # wherever they crossed -- 22 cm2 measured at 0.67 mm, and fully reachable.
    # Wider than every strap around it, the faces cannot line up.
    _rod(p, [(0, hy, az), (0, hy, top + .010)], r=.013, flat=.92)
    _ring(p, (0, hy, top - .004), R=.034, r=.010, sides=7, prof=5)
    p.wobble(.0045, freq=2.6, respect_seams=False)
    return p.finish()


def wall_lantern_b():
    """The door sconce from ref1: the same 2 x 3 cage under a little canopy
    bracket with scrolled stays, hood flared into a pyramid with a spike finial.
    Hugs the wall. In the ref crop (0.68-0.84 x 0.50-0.74) this lantern HANGS
    off its bracket on a short link -- it does not stand on a shelf -- and its
    cage measures 75 x 145 px, ~1.9:1, the same slim upright as the hung one.
    So the piece reads bottom-up: drip finial on z = 0, cage, pyramid, link,
    canopy; the stays reach only 0.20 so they stay clear of the lantern."""
    p = Part("SM_Light_WallLantern_B", budget="sign",
             seams=dict(x=(-.21, .21), y=(-.46, .022), z=(0, .94)))
    w, hg = .215, .430              # same 2:1 cage as the hung lantern
    hw = w / 2
    yc = -.205
    # the finial is 32 mm tall so its head is INSIDE the cage's base pan (which
    # spans z0-0.004 .. z0+0.016). At 30 mm it stopped 21.4 mm below the flame
    # and under a cage with no floor at all, hanging off nothing.
    p.cyl((0, yc, .016), .022, .032, "iron", sides=6, r_top=.032, tint=.03,
          shade=IRON_S)             # drip finial: the lowest point of the piece
    z0 = .030
    _cage(p, (0, yc, z0), w=w, hg=hg)
    z1 = z0 + hg
    # THE HOOD STACK BEDS INTO WHAT IT SITS ON. Measured on the built mesh, the
    # collar's underside was 1.5 mm above the cage (glazing() insets its head
    # rail by overlap/2, so the cage stops 5 mm short of z1), the pyramid 2.0 mm
    # above the collar and the spike 3.2 mm above the pyramid: three daylight
    # slits straight through the hood. Each now laps ~10 mm into the one below.
    # ... and the collar beds past THE PANE'S TOP EDGE, not the cage's nominal
    # top: dimensioned from z1 alone its underside stopped 2.1 mm above the glass
    # (GLZ_EDGE), which with nothing under the pane either left the sconce's four
    # panes and sixteen leading bars a floating island. Its TOP is unchanged at
    # z1+0.029, so the pyramid above still laps it by 12 mm and the fitting's
    # silhouette does not move; only the hidden underside reaches further down.
    col_t, col_b = z1 + .029, z1 - GLZ_EDGE - GLZ_LAP
    p.cyl((0, yc, (col_t + col_b) / 2), hw * 1.40, col_t - col_b, "iron", sides=4,
          phase=pi / 4, r_top=hw * 1.00, tint=.035, shade=IRON_S)
    p.cyl((0, yc, z1 + .073), hw * 1.00, .112, "iron", sides=4, phase=pi / 4,
          r_top=hw * .24, tint=.035, shade=IRON_S)
    p.cyl((0, yc, z1 + .145), .024, .056, "iron", sides=6, r_top=.004,
          tint=.03, shade=IRON_S)
    zt = z1 + .173                  # spike tip: where the hanging link starts
    az = .830                       # canopy underside
    _ring(p, (0, yc, zt + .010), R=.026, r=.009, sides=6, prof=5)
    _rod(p, [(0, yc, zt + .002), (0, yc, az - .004)], r=.013, flat=.72)
    _plate(p, az - .247, az, w=.092, bolts=2)
    # The canopy is bedded 12 mm DOWN into the fixing plate below it. Sat on top
    # of it, its underside and the plate's top face landed on the same z plane
    # and check_zfight measured 19 cm2 of coincident iron there.
    # ... and it reaches the wall WITHOUT crossing it: at yc*0.50 x 1.30 deep it
    # ran to y = +0.031, 8.7 mm past the seam, and finish() clamped 10 verts.
    _box(p, (0, yc * .545, az + .006), (.126, abs(yc) * 1.225, .036), "iron",
         bevel=.010, seg=1, tint=.03, shade=IRON_S)
    for sx in (-1, 1):
        _curl(p, (sx * .042, 0, az), 268, 182, .200, .200, n=6, aspect=.80,
              rod=.013, rod_end=.010)
    p.wobble(.0045, freq=2.6, respect_seams=False)
    return p.finish()


def lantern_hanging():
    """Hangs under a porch beam: the same lantern on a rope with an iron strap
    yoke and a top eye (ref1's porch lantern). Total height LANT_H."""
    p = Part("SM_Light_LanternHanging", budget="sign",
             seams=dict(x=(-.21, .21), y=(-.21, .21), z=(0, LANT_H + .01)))
    lant = _lantern(p, tag="H")
    p.merge(lant, at=(0, 0, 0))
    zt = lant.top
    _curl(p, (0, 0, zt - .100), 157, 23, .140, .140, n=6, aspect=.90, rod=.015,
          flat=1.00)
    _ring(p, (0, 0, zt + .040), R=.036, r=.011, sides=7, prof=5)
    p.cyl((0, 0, zt + .092), .034, .046, "iron", sides=6, r_top=.028, tint=.03,
          shade=IRON_S)
    # two rope lengths, not three: the lantern itself got 0.26 taller, and the
    # whole fitting has to stay a sane hang under a porch beam
    for k, (dz, dy, rr) in enumerate(((.150, .004, .031), (.288, -.006, .029))):
        p.cyl((0, dy, zt + dz), rr, .148, "rope", sides=6, r_top=rr * .93,
              tint=.09, shade=.90)
    p.cyl((0, 0, zt + .356), .032, .044, "iron", sides=6, r_top=.028, tint=.03,
          shade=IRON_S)
    _ring(p, (0, 0, zt + .404), R=.040, r=.012, sides=7, prof=5)
    p.wobble(.0045, freq=2.6, respect_seams=False)
    return p.finish()


# ======================================================= wall-flat signage ===
def wall_panel():
    """Not in the family table, but both refs need it: ref2's porch tympanum --
    a flat painted panel for over a door or in a gable, cream plaster in an oak
    frame with the tankard and a lettered band, capped by a little cornice and a
    tooth course. Wall-parallel, no bracket."""
    p = Part("SM_Sign_WallPanel", budget="sign",
             seams=dict(x=(-.50, .50), y=(-.20, .022), z=(0, .74)))
    W, hw = .900, .450
    z0, z1 = .055, .600
    # field + frame, built in the wall plane (thin in Y).
    # EVERY MEMBER'S BACK BITES PAST Y=0. Measured on the built mesh, not one of
    # this piece's 483 verts reached the wall plane: the deepest was the field at
    # y = -0.0038, so the whole panel hung 4-5 mm off the wall it mounts on, with
    # a shadow gap round the frame. Front faces are unchanged -- only the depths
    # grew -- so nothing about the panel's face moves.
    _box(p, (0, -.020, (z0 + z1) / 2), (W - .120, .070, z1 - z0 - .110),
         "plaster", bevel=.010, seg=1, tint=.045)
    for z, h in ((z0 + .046, .092), (z1 - .040, .080)):
        _box(p, (0, -.030, z), (W, .086, h), "oak_mid", bevel=.011, seg=1, tint=.06)
    # stiles 5 mm in from both rail faces -- flush, they lapped the rails with
    # both cheeks coplanar (5.8 cm2 a corner after the bevel, under the gate's
    # floor but the same joint as the one that measured 292 cm2 on the notice
    # board).
    # ... and 4 mm in from the rails' ENDS as well, which was missed: at
    # hw - 0.040 an 80 mm stile ran out to exactly x = +/-hw, the same plane as
    # the rails' own end faces. Measured 2 x 5.5 cm2 of coincident oak 0.10-0.12 mm
    # apart, 100% ray-reachable -- it is the panel's side elevation -- and under
    # check_zfight's 15 cm2 floor, so nothing reported it. Same joint as the one
    # that measured 292 cm2 on the notice board.
    for sx in (-1, 1):
        _box(p, (sx * (hw - .044), -.030, (z0 + z1) / 2), (.080, .076,
             z1 - z0 - .120), "oak_mid", bevel=.011, seg=1, tint=.06)
    for sy in (-1, 1):                    # forged pegs in the frame corners
        for zz in (z0 + .046, z1 - .040):
            p.cyl((sy * (hw - .044), -.076, zz), .015, .018, "iron", sides=5,
                  axis='Y', r_top=.010, tint=.03, shade=IRON_S)
    # emblem + lettering: built facing +X in a scratch part, then turned to -Y
    em = p.sub(p.name + "_em")
    # x_face .055 for both: that IS the plaster field's front plane in the
    # scratch part's frame (the field is 0.050 thick about y=-0.030). _tankard
    # and _letters bed themselves into the plane they are given, so the tankard
    # no longer stands 3.5 mm off the field hanging from the frame rail it
    # happens to cross.
    # THE EMBLEM FITS INSIDE THE FRAME'S OPENING. Bedded into the field (rather
    # than floating 3.5 mm in front of everything and hanging off the one rail it
    # crossed) it sits 18 mm behind the frame's face, so anything running past the
    # top rail is hidden BY it rather than standing over it -- and at s=1.22,
    # z+0.100 the emblem was 0.384 tall in a 0.410 opening whose lower band is
    # already spoken for by the glyphs, so its whole froth head crossed the rail.
    # s=0.92 about z+0.003 measures 0.290 and lands clear of both: froth top
    # 0.509 against a rail edge at 0.520, vessel foot 0.220 against a glyph band
    # topping out at 0.197.
    _tankard(em, (0.0, (z0 + z1) / 2 + .003), .055, 1, s=.92, seed=15)
    _letters(em, -.300, .300, z0 + .136, .055, n=7, seed=16, h=.052, sgn=1)
    p.merge(em, rot=(0, 0, -90))
    em.bm.free()
    em.bm = None
    # cornice + tooth course, the same trim as the boards
    # 12 mm lower and 20 mm deeper: at z1+.034 the cornice's underside stopped
    # 8 mm above the top rail and the two were joined only by the tooth course,
    # leaving a 8 x 970 mm slot through the panel between them. Now it beds 4 mm
    # into the rail and its back reaches the wall like everything else.
    _box(p, (0, -.052, z1 + .022), (W + .070, .130, .052), "oak_dark", bevel=.012,
         seg=1, tint=.06)
    # ctr=-.062 keeps the teeth inside the cornice they hang off (y -0.117 ..
    # -0.007) instead of straddling the wall plane, where the back half of every
    # tooth was 23.5 mm inside the wall and finish() clamped 20 verts flat.
    _teeth(p, -(W - .06) / 2, (W - .06) / 2, z1 + .010, 10, "oak_dark", h=.048,
           th=.086, seed=17, axis='X', ctr=-.062)
    p.wobble(.0050, freq=2.4, respect_seams=False)
    return p.finish()


def notice_board():
    """Wall-parallel oak notice board under a steep shingled pent roof -- roof,
    fascia and tooth course tie it to the rest of the kit. The pinned notices
    are cream cards, deliberately crooked. The roof's drip projects 0.22 from the
    wall so it shades the notices without hiding them from a high camera, and its
    head bites 15 mm past the wall plane rather than stopping short of it."""
    p = Part("SM_Sign_NoticeBoard", budget="sign",
             seams=dict(x=(-.54, .54), y=(-.34, .022), z=(0, 1.08)))
    W, hw = .900, .450
    bz0, bz1 = .095, .820
    r = rng(p.name + "/nb")
    # The plank field runs 4 mm INTO the stiles either side. Stopping at
    # +/-0.370 against a stile at 0.386 left a 16 mm slot straight through the
    # board at each end, with the wall showing through it.
    for i in range(5):
        cx = lerp(-hw + .055, hw - .055, (i + .5) / 5)
        _box(p, (cx, -.026, (bz0 + bz1) / 2), ((W - .11) / 5 - .010, .044,
             bz1 - bz0 - .085), "oak_mid", bevel=.009, seg=1, tint=.075,
             shade=1.0 + r.uniform(-.06, .06))
    for z, h in ((bz0 + .034, .068), (bz1 - .030, .060)):    # rails run through
        _box(p, (0, -.034, z), (W, .072, h), "oak_dark", bevel=.011, seg=1, tint=.06)
    # STILES TENONED BETWEEN THE RAILS, and set 8 mm in from their ends, 6 mm
    # behind their front face and 4 mm in front of their back. THIS JOINT WAS THE
    # FAMILY'S ENTIRE REPORTED Z-FIGHT BAR 75 cm2. Full height, full width and
    # full depth, each stile doubled a solid with the rail it crossed and every
    # one of the corner's six planes was coincident: 15 pairs, 292 cm2, of which
    # ray-sampling found 257 cm2 (88%) reachable -- the board's own outer faces,
    # not something buried. The stile ends are now interior to the rails.
    for sx in (-1, 1):
        _box(p, (sx * (hw - .036), -.033, (bz0 + bz1) / 2), (.056, .062,
             bz1 - bz0 - .100), "oak_dark", bevel=.011, seg=1, tint=.06)
    # ---- pinned notices
    notes = ((-.268, .600, .190, .225, "plaster"), (-.086, .552, .150, .165, "thatch"),
             (.128, .612, .175, .205, "plaster"), (.302, .548, .140, .175, "thatch"),
             (-.216, .318, .195, .175, "plaster"), (.020, .296, .150, .150, "thatch"),
             (.256, .322, .165, .165, "plaster"))
    # PINNED ON, not floating in front. At y=-0.062 a 10 mm card's back sat
    # 9 mm clear of the plank field it is pinned to -- measured, four of the
    # seven notices touched nothing at all in the piece. Now the card is bedded
    # 3 mm into the planks, the folded corner strips bite into the card, and the
    # nail runs through both into the board.
    for i, (nx, nz, nw, nh, mt) in enumerate(notes):
        rot = (0, r.uniform(-8, 8), 0)
        p.box((nx, -.050, nz), (nw, .010, nh), mt, bevel=0, tint=.05, rot=rot,
              shade=1.0 + r.uniform(-.10, .04))
        for k in range(2):
            p.box((nx + r.uniform(-.015, .015), -.0565, nz + nh * (.22 - .30 * k)),
                  (nw * r.uniform(.44, .70), .006, .010), "stone_dark", bevel=0,
                  tint=.12, rot=rot, shade=.95)
        p.cyl((nx + nw * .32, -.056, nz + nh * .40), .013, .018, "iron", sides=5,
              axis='Y', r_top=.008, tint=.03, shade=IRON_S)
    for i in range(7):                    # gold lettering on the head rail
        cx = lerp(-hw + .095, hw - .095, (i + .5) / 7)
        # -0.072, not -0.076: a 12 mm glyph at -0.076 has its back face EXACTLY
        # on the rail's front plane, ~18 cm2 of coincidence per glyph that only
        # wobble is currently keeping out of check_zfight. Bedded 4 mm instead.
        p.box((cx, -.072, bz1 - .028), ((W - .19) / 7 * r.uniform(.34, .60), .012,
              .038 * r.uniform(.8, 1.15)), "flower_gold", bevel=0, tint=.10,
              shade=1.0 + r.uniform(-.10, .10))
    # ---- pent roof: two brackets, 6 shingle rows, fascia, tooth course
    # THE BRACKETS RUN OUTWARD, from the board's head rail to under the fascia.
    # (.20, 0) put the horizontal leg at y = +0.140 -- 140 mm INSIDE the wall --
    # so finish() clamped 4 verts per bracket (119.5 mm, the worst overshoot in
    # the family) and, with the brackets pointing backwards, nothing connected
    # the hood to the board: roof + fascia measured 94.2 mm from the nearest
    # board member. Each bracket now laps 15 mm into the head rail and dies into
    # the fascia, and its top edge stays under the 46 deg soffit.
    for sx in (-1, 1):
        p.prism([(0, 0), (-.160, -.035), (0, -.160)], .055, "oak_dark", axis='X',
                at=(sx * (hw - .050), -.055, bz1 + .040), bevel=0, tint=.05)
    sub = p.sub(p.name + "_sh")
    rs = rng(p.name + "/sh")
    RW = W + .05
    for row in range(6):
        v = row * .048
        n, tw = 12, RW / 12
        off = (row % 2) * tw * .5
        for i in range(n + 1):
            cu = -RW / 2 + tw * (i + .5) - off
            if cu < -RW / 2 + .012 or cu > RW / 2 - .012:
                continue
            h = .048 * 2.0 * rs.uniform(.97, 1.02)
            # Alternate rows sit 10mm higher, and every tab is rocked a couple
            # of degrees. Laid flat and level, each row overlaps the row below
            # by half its length with its two big faces on the same planes:
            # 29 coincident pairs, and the whole of this roof's z-fighting.
            sub.box((cu, v + h / 2 - .048 * .50,
                     .012 + (row % 2) * .010 + rs.uniform(0, .002)),
                    (tw - .007, h, .020),
                    # EVERY TAB IS shingle_moss. It used to scatter 10% warm
                    # brown `shingle` through the roof, and BRIEF.md reserves
                    # that material for a deliberate _Warm variant piece --
                    # scattered it is the same mistake as scattering `moss`:
                    # a hue that reads as damage or a bug rather than as age,
                    # and visible as tan tabs in this family's lineup shot.
                    # The wander stays, as VALUE: tint .09 plus a slightly
                    # wider shade spread, which is what "moss is a tone, not a
                    # colour" means.
                    "shingle_moss",
                    bevel=0, tint=.09, skew=(rs.uniform(-1, 1) * .004, 0),
                    rot=(rs.choice((-1, 1)) * rs.uniform(1.0, 2.4),
                         rs.choice((-1, 1)) * rs.uniform(1.0, 2.4), 0),
                    shade=1.0 + rs.uniform(-.14, .09))
    # 30 mm further back than it was: the roof's head stopped 36 mm short of the
    # wall plane, so a high camera looked down a slot between the two. It now
    # bites 15 mm past y=0 at its back edge while its drip stays 0.218 out.
    p.merge(sub, at=(0, -.200, bz1 + .002), rot=(46, 0, 0))
    sub.bm.free()
    sub.bm = None
    _box(p, (0, -.216, bz1 + .020), (W + .09, .044, .060), "oak_dark", bevel=.010,
         seg=1, tint=.06)
    # ctr/th keep the teeth inside the head rail they hang off (y -0.070..0.002):
    # centred on y=0 and 72 mm deep they straddled the wall plane, 16.0 mm of
    # every tooth buried and clamped, and a 72 mm tooth would have put its front
    # face on the rail's front plane as well.
    # The tooth course HANGS BELOW THE HEAD RAIL, in front of the plank field.
    # At z_top = bz1-0.004 every tooth was 6 mm shorter than the rail is deep and
    # sat entirely INSIDE it -- 10 boxes, 120 tris, of dead geometry -- while its
    # top face stood 2 mm above the rail's own top face, 10 near-parallel pairs of
    # 36 cm2 open to a camera from above. Now the head is 6 mm up inside the rail
    # and 30 mm of tooth shows against the planks, clear of the top notices.
    _teeth(p, -(W + .02) / 2, (W + .02) / 2, bz1 - .060, 10, "oak_dark", h=.034,
           th=.044, seed=13, axis='X', ctr=-.044)
    p.wobble(.0060, freq=2.2, respect_seams=False)
    return p.finish()


# ================================================================= build ====
def build():
    # The crook lantern leads: it is ref1's hero fitting and the crop this whole
    # family is judged against (compare.py -> signage: ref1:lantern), so it is
    # what build_piece.py should point its closeup camera at.
    # Shallow, wall-hugging pieces first and the three deep hanging boards last,
    # so the lineup shot does not stack a 1.1m-deep board in front of a lantern.
    return [wall_lantern_a(), wall_lantern_b(), lantern_hanging(),
            wall_panel(), notice_board(), sign_a(), sign_b(), sign_c()]


# ============================================================ demo shot =====
def _ctx():
    """Context ONLY for the demo shot -- a deliberately plain corner of inn
    frontage so the signage has something to be mounted on. NOT kit pieces:
    these objects are named CTX_ and are never returned by build().

        front wall  x in [-2.8, 0.8], face on y = 0, 3.0 high
        return wall y in [0, 3.0] at x = 0.8, facing +X
    """
    out = []
    T = S.T_STONE

    def wall(tag, span, loc, rotz):
        p = Part("CTX_" + tag, seams=None)
        h = 3.0
        p.plate((0, T / 2, h / 2), (span, T, h), "stone_dark", tint=.03, shade=.55)
        p.stones((-span / 2, span / 2), (0, .24), y=0.0, depth=.085, mat="stone_dark",
                 mat_alt="stone", course=.24, seed=21, wobble=.28, mortar=.020,
                 r_bevel=0, tint=.11, big=.08, shade_var=.14)
        p.stones((-span / 2, span / 2), (.24, h), y=0.0, depth=.065, mat="stone",
                 mat_alt="stone_dark", mat_warm="stone_warm", course=.205, seed=22,
                 wobble=.24, mortar=.018, big=.08, chink=.20, r_bevel=0, tint=.10,
                 shade_var=.13)
        # jetty sill beam + a band of half-timber above, to cap the wall
        p.box((0, -S.JETTY / 2 + .16, h + .090), (span, S.JETTY + .06, .18),
              "oak_dark", bevel=0, tint=.05, shade=.80)
        p.plate((0, .09, h + .36), (span, .20, .36), "plaster_dim", tint=.05, shade=.88)
        n = max(3, int(round(span / .52)))
        for i in range(n + 1):
            p.box((lerp(-span / 2 + .055, span / 2 - .055, i / n), -.010, h + .36),
                  (.105, .09, .36), "oak_dark", bevel=0, tint=.05, shade=.85)
        ob = p.finish()
        ob.location = loc
        ob.rotation_euler = (0, 0, radians(rotz))
        out.append(ob)

    wall("Front", 3.6, (-1.00, 0.0, 0.0), 0.0)
    wall("Side", 3.0, (0.80, 1.50, 0.0), 90.0)
    p = Part("CTX_Corner", seams=None)
    p.box((0, 0, 1.63), (.18, .18, 3.26), "oak_dark", bevel=0, tint=.05,
          shade=.85)
    ob = p.finish()
    ob.location = (0.70, -0.09, 0.0)
    out.append(ob)
    # doorway + porch beam, so something can hang over the door
    p = Part("CTX_Door", seams=None)
    p.plate((0, .30, 1.12), (1.14, .40, 2.24), "oak_dark", tint=.04, shade=.65)
    for i in range(5):
        p.box((lerp(-.50, .50, (i + .5) / 5), .12, 1.06), (.19, .07, 2.10),
              "oak_mid", bevel=0, tint=.07, shade=.9)
    p.arch((0, .16, 2.18), .76, .34, "stone_pale", thickness=.19, segs=8, span=180,
           tint=.05, bevel=0)
    ob = p.finish()
    ob.location = (-0.05, 0.0, 0.0)
    out.append(ob)
    p = Part("CTX_PorchBeam", seams=None)
    p.beam((-.86, -.50, 2.38), (0.86, -.50, 2.38), .14, .17, "oak_dark", bevel=0,
           tint=.05, shade=.9)
    for sx in (-1, 1):
        p.beam((sx * .70, .02, 2.36), (sx * .70, -.50, 2.38), .12, .14, "oak_dark",
               bevel=0, tint=.05, shade=.9)
        p.prism([(0, 0), (.28, 0), (0, -.34)], .12, "oak_dark", axis='X',
                at=(sx * .70, -.50, 2.28), bevel=0, tint=.05, shade=.9)
    ob = p.finish()
    ob.location = (-0.05, 0.0, 0.0)
    out.append(ob)
    return out


def demo():
    """A corner of the inn's frontage, dressed. Composed as a shot: the big
    board out on the left catching the light, a second sign further down the
    street, the ref1 crook lantern turning the corner, sconce and porch lantern
    at the door with the painted panel over it, notices low down where a
    passer-by would read them."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = _ctx()

    def put(nm, loc, rz=0.0):
        o = src[nm].copy()
        o.data = src[nm].data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (0, 0, radians(rz))
        out.append(o)
        return o

    # ---- front wall (faces -Y)
    put("SM_Sign_InnBoard_A", (-2.10, 0.0, 2.74 - PLATE_Z))
    put("SM_Sign_NoticeBoard", (-1.22, 0.0, 0.94))
    put("SM_Sign_WallPanel", (-0.10, 0.0, 2.42))
    put("SM_Light_LanternHanging", (-0.10, -0.50, 2.29 - LANT_H))
    put("SM_Light_WallLantern_B", (0.46, 0.0, 1.50))
    # ---- return wall (faces +X after the 90 deg turn)
    put("SM_Light_WallLantern_A", (0.80, 0.62, 1.48), rz=90)
    put("SM_Sign_InnBoard_C", (0.80, 1.55, 2.62 - PLATE_Z), rz=90)
    put("SM_Sign_InnBoard_B", (0.80, 2.62, 2.26 - PLATE_Z), rz=90)
    for nm in src:
        src[nm].location = (0, 40, 0)        # park the originals out of frame
    return out
