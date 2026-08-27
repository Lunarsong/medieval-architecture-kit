"""Ground / yard family: what the inn stands on, steps up to it, and fences it in.

Measured off the reference crops, not guessed:

  * `ref1:barrels` / the street below it -- irregular five- and six-sided plans,
    cool pale grey with the occasional warm tan block, packed TIGHT: the joints
    are thin dark lines, never mortar beds, and the field never shows bare
    ground between stones. Against a 0.62m barrel a typical flag is a bit over
    half a barrel wide. But the plans are not what makes it read: every stone is
    CAMBERED, crowned in the middle and falling away to a dark recessed joint,
    which is what gives the painted street a lit edge on every stone and a
    shadow between every pair. Our two variants sit either side of the
    reference's size -- A on a 0.29m lattice, B on 0.22m, both a tenth bigger
    again once the assembler lays them oversize.
  * ref1's doorstep is a rustic stoop: one course of chunky ROUNDED rubble per
    riser (~0.14m of stone under a ~0.06m cap slab), a generous 0.45m tread, and
    a deliberately BROKEN front edge -- no two blocks project the same amount.
  * `ref2:porch` is completely different masonry doing the same job: dressed
    pale grey blocks, riser ~0.16-0.20, tread ~0.31, three or four blocks per
    tread with visible vertical joints, and the flight SPLAYS -- each lower step
    is wider than the one above. Oak handrail: chunky newel with a cap and a
    little ball finial, two raked rails, no balusters.
  * ref2's boundary is a close-boarded paling fence, boards ~0.18m wide butted
    tight, tops cut off at ragged heights, weathered dark brown.

Conventions: FLOOR/PROP-class pieces -- origin at footprint centre, Z=0 at the
bottom, front facing -Y. Steps climb toward +Y.
  * Every riser in the family is RISE = 0.20, so the three flights hand a level
    artist platform heights of 0.40 / 0.60 / 0.80 and can be mixed on one site.
    0.80 is ref2's porch height.
  * Cobble patches tile at exactly GRID in BOTH X and Y, and rotate in 90 degree
    steps. Their wearing surface is at z = COB_T, so everything standing ON the
    paving sits at z = COB_T (that is what demo() does). Border stones are cut
    dead flat on all four seam planes (outward="" -- no PROUD_MAX slack on any
    axis), which is what lets assemble_inn lay them 1.10 OVERSIZE and bury the
    cut under the neighbour's stones. Both cases are proven, not assumed: at
    exact GRID the seam reads as one more straight joint in the flagging, and at
    1.10 it is invisible.
  * GardenWall and Fence tile along X at GRID like wall pieces.

===========================================================================
PAVING -- the 20mm budget, and how it is spent
===========================================================================
Round 7's paving still did not read as paving: in the heroes the street was
invisible and the ground read as bare dirt. Everything below is measured --
ray-cast height fields over a whole tile, and pixels sampled off
renders/inn/inn_ref2.png -- not eyeballed. Re-measure with the harness rather
than trusting these numbers if you change anything.

THE BUDGET. assemble_inn lays each patch at z = -(its own bbox top), so the
paving's highest vertex lands exactly on z = 0 -- props stand at z = 0 and must
not be buried, which is correct and is not ours to change. The hero backdrop
plane then sits at z = -0.02 (render.ground's default). So the ENTIRE read of
this piece in a hero is the top 20 millimetres of it, and every millimetre has
to be spent on purpose:

    crown ---------------------------------------------  0 mm   the datum
      | camber (`dome`)                                   11-14 mm
    arris (the hard break, `shoulder`) ----------------- 11-14 mm
      | steep collar (`skirt`, 45-55 deg)
    groove bottom, where two collars meet -------------- ~20 mm  the backdrop

Round 7 measured 1.17 degrees of MEDIAN slope over the visible band (i.e. the
stones were flat) and 60 % cover (i.e. two fifths of the "paving" in the hero
was the dirt plane showing between chips). It is now 5.6 degrees and 97 %.
Three changes did it, and all three are in `_domestone` and `_flagstones`:

1. A REAL CAMBER, not a chamfer ring. The top is a surface of revolution over
   the stone's own plan with only a token crown facet, so the whole wearing
   face is tilted a few degrees and one stone is a different value from the
   next under a raking sun. See `_domestone`.

2. THE STONES LAP. Adjacent lattice cells share their vertices exactly, so
   growing every stone `root` metres past its own cell makes neighbours overlap
   all the way down. The joint stops being a hole the backdrop can fill and
   becomes a GROOVE cut into one continuous stone surface. This is what took
   cover from 60 % to 97 %, and it is why the bed courses are no longer dark:
   nothing sees them except through a worn hollow.

3. NOTHING WASTES REVEAL. `_domestone` self-levels each stone against its own
   rock, and `_cobble` ceilings every vertex at the datum after the wobble.
   Round 7 gave 4.4mm of its 20 away to single outlier vertices; it is now 3.

   Height variation still goes DOWNWARD only (`sink`), for the same reason: a
   stone standing proud does not make the field taller, it pushes every other
   stone further under the backdrop.

TONE, and this was half the fault. assemble_inn.texture_stone multiplies every
stone material by a soiling field keyed on world Z, and at pavement level that
is x0.50 with a warm cast -- and it hits the hero's backdrop plane (M_stone at
z = -0.02) exactly as hard as it hits us. Sampled off inn_ref2.png, round 7's
paved field measured median L=126 against the dirt plane's L=123-127: the SAME
VALUE, and warmer than the dirt (red-blue spread 34 against 29). A street that
is the same value as the earth it sits on is not a street.
So the field's value histogram now STRADDLES the ground with a gap at it --
dark stones at ~0.8x the backdrop, mid at 1.4x, pale at 2.1x, mean ~1.6x -- and
`stone_warm`, much the warmest tone in the palette, is cut to ref1's literal
"occasional tan block" at 3 %. See the tone block in `_flagstones`.

WHAT THIS MODULE STILL CANNOT FIX: render.look_ref1 lays ITS backdrop at
z = 0.0, exactly the plane the assembler pins the paving's top vertex to, so in
the ref1 hero the entire field -- all 83 patches, world z -0.086..0.000 -- is at
or below the backdrop and renders as bare plane. That is measured, not inferred:
renders/inn/inn_ref1.png contains the full cobbled street and not one stone of
it is visible. No geometry here can fix it; any relief we add only lowers the
rest of the field further under the plane. The one-word fix belongs in
render.py -- give look_ref1's ground the z = -0.02 that every other preset uses
-- or in assemble_inn.py, and neither is ours to edit.

Bevels: util's bevel path drops each primitive's ORIGINAL faces out of the paint
set, so they land in material slot 0 with a flat white vertex colour. Everything
here is therefore built with bevel=0 and gets its rounding from geometry
instead -- blob's shoulder rings, box tapers, and the two-tier `_cslab` whose
inset top course reads as a worn chamfer and catches the light exactly like the
bright stone arrises in ref1.

No greenery, no moss, no clutter here on purpose -- weeds between the flags and
barrels on the step belong to props/.
"""
import bpy
from math import radians, degrees, sin, cos, tan, pi, hypot
from mathutils import Matrix, Vector, Euler
from kit import spec as S
from kit.util import Part, rng, lerp, clamp, slope_matrix

FAMILY = "ground"
COLLECTION = "13_Ground_Stairs"

G = S.GRID
RISE = 0.20          # one riser, shared by every flight in the family
COB_T = 0.09         # paving thickness; the wearing surface is at this height

GW_T = 0.40          # garden wall total thickness (coping face to coping face)
GW_H = 0.94          # garden wall height incl. coping
FN_H = 1.62          # tallest paling


# ============================================================== helpers ======
def _inset(poly, off):
    """Mitred inward offset of a (roughly convex, CCW) XY polygon."""
    n = len(poly)
    nrm = []
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        L = hypot(ex, ey) or 1.0
        nrm.append((-ey / L, ex / L))              # inward for CCW
    out = []
    for i in range(n):
        n0, n1 = nrm[i - 1], nrm[i]
        dot = clamp(n0[0] * n1[0] + n0[1] * n1[1], -0.5, 1.0)
        s = off / (1.0 + dot)
        out.append((poly[i][0] + (n0[0] + n1[0]) * s,
                    poly[i][1] + (n0[1] + n1[1]) * s))
    return out


def _mtilt(r, amp, lo=0.34):
    """A slab tilt that is never SMALL. check_zfight buckets a plane by its
    normal rounded to 2dp, so a stone lying within ~0.3 degrees of dead flat
    shares its bucket with every axis-aligned plate in the piece -- and then a
    face 1.5m from the origin only needs a hair of rotation for its plane
    offset to drift the ~10mm that a slab bed is set by. Every slab therefore
    keeps at least `lo` degrees of rock, which is what stops a paving flag from
    ever fighting the bed course under it. It also happens to be what laid
    stone does."""
    return r.choice((-1, 1)) * (lo + abs(amp) * r.uniform(.5, 1.0))


def _cslab(p, poly, z_bot, thick, mat, chamf=0.014, cap=None, tilt=(0., 0.),
           tint=0.07, shade=1.0):
    """Stone slab with a worn top arris: full-size body plus an inset top
    course. The exposed ring of the body is the chamfer and takes the highlight
    exactly like the bright stone arrises in ref1. Two prisms, bevel=0, so every
    face keeps its own tint. Keep `chamf` SMALL relative to the joints between
    slabs, or the arrises read as loose paving instead of fitted stone."""
    n = len(poly)
    cx = sum(q[0] for q in poly) / n
    cy = sum(q[1] for q in poly) / n
    loc = [(q[0] - cx, q[1] - cy) for q in poly]
    cap = thick * 0.34 if cap is None else cap
    body = max(thick - cap, 0.010)
    rot = (tilt[0], tilt[1], 0)
    p.prism(loc, body, mat, axis='Z', at=(cx, cy, z_bot + body / 2), bevel=0,
            tint=tint, rot=rot, shade=shade)
    top = _inset(loc, chamf)
    # The top course roots 12mm INTO the body, not 6mm. At 6mm the body's top
    # plane and the course's underside landed in the same 2.5mm coincidence
    # band, so every slab in the family could flicker along its own arris.
    p.prism(top, cap + .012, mat, axis='Z',
            at=(cx, cy, z_bot + body + cap / 2 - .006), bevel=0, tint=tint,
            rot=rot, shade=shade * 1.03)


def _pshrink(poly, s):
    """Scale an XY polygon about its own centroid. The dome rings on a paving
    stone use this rather than `_inset`: a mitred offset self-intersects once the
    offset approaches the inradius, and a paving cell can be long and thin, so a
    fixed offset that reads well on a 0.45m flag folds a 0.18m cobble inside
    out. A centroid scale can never invert a convex cell and it makes the crown
    facet a constant FRACTION of the stone, which is what keeps a 7x7 patch and
    a 9x9 patch looking like the same masonry at different sizes."""
    n = len(poly)
    cx = sum(q[0] for q in poly) / n
    cy = sum(q[1] for q in poly) / n
    return [(cx + (q[0] - cx) * s, cy + (q[1] - cy) * s) for q in poly]


def _meanr(poly):
    """Mean distance from a polygon's centroid to its vertices. Used to turn a
    joint width in METRES into the plan-scale factor `_pshrink` wants, so a
    13mm joint is 13mm on a 0.45m flag and on a 0.20m cobble alike."""
    n = len(poly)
    cx = sum(q[0] for q in poly) / n
    cy = sum(q[1] for q in poly) / n
    return max(sum(hypot(q[0] - cx, q[1] - cy) for q in poly) / n, 1e-4)


def _domestone(p, cell, z_bot, z_top, mat, dome=0.010, skirt=0.011, gap=0.0065,
               root=0.004, crown=0.26, power=1.6, rings=(0.70, 0.44),
               tilt=(0., 0.), tint=0.09, shade=1.0):
    """ONE CAMBERED COBBLE, as a single closed solid.

    THE SECTION IS THE PIECE. Round 7's stone was a flat plate with a chamfer
    ring: 54-74 % of its plan was a dead-horizontal facet and all of the relief
    lived in a narrow rim. Ray-cast over a whole tile, the MEDIAN slope of the
    surface the hero can see measured 1.17 degrees -- i.e. flat -- and a
    flat-grey (Solid-shading) render of a laid field came back as cracked mud
    plates. A stone that is flat on top catches no edge light and throws no
    shadow onto its neighbour, however deep the joint around it is.

    A cobble has three parts to its section and it needs all three. `cell` is
    the stone's FULL lattice cell -- the joint is cut out of it here, not by the
    caller -- and every ring is a plan-scale of it:

        z_bot                    cell + `root`   underside, buried in the bed
        z_top - dome - skirt     cell + `root`   the ROOT: laps its neighbour
        z_top - dome             cell - `gap`    THE ARRIS -- a hard break
        z_top - dome*f(rings[i]) shrinking       |  the camber, sampled and
        z_top                    `crown`         |  smooth-shaded into a dome

    with f(s) = (s**power - crown**power)/(shoulder**power - crown**power), so
    the crown facet lands exactly ON the paving datum and the arris exactly
    `dome` below it -- the datum arithmetic the assembler depends on stays exact
    while the shape between them is free.

      * `dome` is the CAMBER, spread over the whole top by `power` and `rings`
        rather than banked into the rim. On a 0.29 m stone a 11-14 mm camber is
        6-9 degrees of tilt across the entire wearing face: that is what makes
        one stone a different value from the next under a raking sun.
      * `skirt` is the STEEP COLLAR under the arris -- 45-55 degrees, because a
        first attempt that ran the camber all the way out to the full plan
        measured beautifully and looked like rumpled cloth: with no break in the
        surface, smooth shading ran one stone straight into the next and the
        joints disappeared. The collar is deliberately steeper than SMOOTH_ANG
        away from the camber band above it, so shade_smooth_by_angle leaves the
        arris SHARP -- that hard line is the stone's edge.
      * `root` is why the field is CLOSED. Adjacent cells share their lattice
        vertices exactly, so growing every stone `root` metres PAST its own cell
        makes neighbours lap rather than butt, all the way down to z_bot. The
        joint therefore stops being a hole and becomes a GROOVE cut into one
        continuous stone surface -- two skirts meeting.

    That last one is the fix for the second half of the complaint, and it is
    geometric rather than tonal. assemble_inn pins the patch's top vertex to
    z = 0 and the hero backdrop sits at z = -0.02, so ANY daylight between two
    stones is filled by the backdrop -- i.e. by the dirt, at the dirt's own
    value. Round 7 left `joint`-wide gaps and measured only 60 % of a tile inside
    that 20 mm band: two fifths of the "paving" in the hero was literally the
    dirt plane showing between chips, which is exactly what "the ground looks
    like bare dirt" describes. Stones that lap cannot do that: the groove
    bottoms out on stone about 17 mm down, above the backdrop, and the field
    covers ~97 % of its tile.

    Cost is (8 + 2*len(rings))n - 4 tris: 50 on a 6-sided stone with one camber
    ring, 61 with two, against the flat plate's 8n-4 = 44.

    `tilt` is degrees of rock about X and Y and is never zero: see `_mtilt`.
    """
    n = len(cell)
    cx = sum(q[0] for q in cell) / n
    cy = sum(q[1] for q in cell) / n
    loc = [(q[0] - cx, q[1] - cy) for q in cell]
    rm = _meanr(cell)
    # never eat the whole stone: a sunk stone is thinner than a proud one
    room = max((z_top - z_bot) * 0.72, 0.006)
    if dome + skirt > room:
        k = room / (dome + skirt)
        dome, skirt = dome * k, skirt * k
    crown = clamp(crown, 0.14, 0.52)
    shoulder = clamp(1.0 - gap / rm, crown + 0.12, 0.985)
    out = 1.0 + root / rm
    ck, sk = crown ** power, shoulder ** power
    den = max(sk - ck, 1e-6)
    scales = [shoulder] + [clamp(s, crown + .04, shoulder - .04) for s in rings] + [crown]
    base = _pshrink(loc, out)
    vs = [(u, v, z_bot) for (u, v) in base]
    vs += [(u, v, z_top - dome - skirt) for (u, v) in base]     # the root
    for s in scales:
        ring = _pshrink(loc, s)
        z = z_top - dome * (s ** power - ck) / den
        vs += [(u, v, z) for (u, v) in ring]
    nb = len(scales) + 2                             # rings incl. the underside
    F = [tuple(range(n))[::-1]]                      # underside
    for k in range(nb - 1):
        a, b = k * n, (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            F.append((a + i, a + j, b + j, b + i))
    F.append(tuple(range((nb - 1) * n, nb * n)))     # crown facet
    mtx = Euler((radians(tilt[0]), radians(tilt[1]), 0.0), 'XYZ').to_matrix().to_4x4()
    vs = [tuple(mtx @ Vector(v)) for v in vs]
    # SELF-LEVEL. Rocking a stone about its own centre lifts one side of its
    # crown above the datum, and assemble_inn pins the patch's HIGHEST vertex to
    # z = 0 -- so one millimetre of lift on one stone costs EVERY other stone a
    # millimetre of the 20 mm the hero backdrop leaves visible. Measured, round
    # 7 threw away 4.4 mm of a 20 mm reveal that way, a fifth of the whole read.
    # Dropping each stone so its highest point is exactly its intended crown
    # height makes the rock free, and it also lowers a hard-rocked stone bodily,
    # which is itself the height variation a laid street has.
    lift = max(v[2] for v in vs) - z_top
    off = Vector((cx, cy, -lift))
    vs = [tuple(Vector(v) + off) for v in vs]
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _rubble(p, u_range, z_range, y_face, depth, course=0.26, seed=0,
            axis='Y', flip=False, mat="stone", mat_alt="stone_pale",
            mat_warm="stone_warm", mat_dark="stone_dark", warm_p=0.15,
            dark_p=0.09, big=0.26, wide=(1.0, 1.85), jy=0.014, tilt=2.6,
            tint=0.115, shade_var=0.17, mortar=0.004, overfill=1.26,
            vfill=1.06, irregular=0.30, dome=0.44, ragged=0.0, sides=6,
            batter=0.0, chink=0.42, grade=0.30, pack=0.55, seam=False,
            back=True, bed=False):
    """Coursed rounded rubble facing standing `depth` proud of the plane at
    `y_face`. `axis` is the face normal ('Y' faces -Y, 'X' faces -X); `flip`
    turns it round to face +Y / +X so both sides of a freestanding wall come
    from one helper.

    PACKING is the whole game. ref1's rubble has HAIRLINE creases between
    stones and never shows a bare mortar bed, and a blob only covers ~65% of
    its own slot (it is a jittered hexagon, not a rectangle), so the slot has
    to be over-filled hard and the leftovers wedged:

      * `overfill` (1.26) makes every stone a quarter wider than its slot, so
        neighbours interpenetrate along the course and the vertical joints come
        out as thin dark creases instead of 0.10 m mortar beds;
      * `vfill` does the same vertically. Pass it high on a multi-course face
        so the beds close too; leave it near 1.0 on a single-course riser,
        where a cap slab sits directly on the course band;
      * `pack` wedges a stone into every joint CROSSING (where four stones
        meet) -- the last place bare core can show once the joints are thin;
      * `seam=True` lays one stone centred ON each end of the run, the -X copy
        an EXACT mirror of the +X one (axis='Y' and a symmetric u_range only).
        finish()'s seam clamp cuts both in half on the module plane, so a run
        of tiles laps one whole stone across every 2 m joint instead of
        stacking a bare full-height crack there;
      * `bed` packs the bottom edge as well, killing the scalloped dark line
        that the hexagonal bottoms of the lowest course leave along the floor;
      * `chink` wedges a small stone into the joint at the end of a block,
        `grade` makes the bottom course taller than the top one so boulders sit
        low and finer stones pack in above, `ragged` adds random extra
        projection (ref1's broken stoop edge), `batter` leans the wall back.
    """
    r = rng(f"{p.name}/rub/{seed}")
    u0, u1 = u_range
    z0, z1 = z_range
    span = z1 - z0
    rows = max(1, int(round(span / course)))
    # course heights graded big -> small going up
    wts = [1.0 + grade * (1.0 - 2.0 * i / max(rows - 1, 1)) for i in range(rows)]
    tot = sum(wts)
    hs = [span * w / tot for w in wts]
    zrot = 180.0 if flip else 0.0
    sgn = -1.0 if flip else 1.0

    def pick(q):
        if mat_alt and q > .68:
            return mat_alt
        if mat_warm and q < warm_p:
            return mat_warm
        if mat_dark and q < warm_p + dark_p:
            return mat_dark
        return mat

    def at(cu, yy, cz):
        return (cu, yy, cz) if axis == 'Y' else (yy, cu, cz)

    out = []
    cross = []                      # joint crossings to pack afterwards
    zc = z0
    for ri in range(rows):
        ch = hs[ri]
        cz = zc + ch / 2
        zc += ch
        lean = batter * (1.0 - ri / max(rows - 1, 1))
        chz = max((ch - mortar) * vfill, 0.05)
        if ri == 0:
            # the bottom course is over-filled downward like every other one,
            # which drove its stones through the floor plane -- where the seam
            # clamp flattened them ONTO it, both as silently deformed stone and
            # as coincident faces under the piece. Sit the course on z0.
            cz += max(chz - ch, 0.0) * .5
        pad = 0.0
        # ---- the stone that straddles the module joint (see `seam` above)
        if seam:
            ws = ch * r.uniform(1.35, 2.05) * overfill
            dd = depth * (1 + r.uniform(-.10, .10)) + lean
            yy = y_face + sgn * r.uniform(-jy, jy) * .5
            sub = p.sub(f"{p.name}/seam{seed}/{ri}")
            sub.blob(at(u1, yy, cz), (ws, dd, chz * 1.04), pick(r.random()),
                     sides=sides + 1, axis=axis, irregular=irregular * .85,
                     dome=dome * r.uniform(.8, 1.1), bevel=0, seg=1, tint=tint,
                     rot=(r.uniform(-1, 1) * tilt * .5, 0, zrot), back=back,
                     seed=seed * 977 + ri,
                     shade=1.0 + r.uniform(-shade_var, shade_var))
            p.merge(sub)                       # +X half
            p.merge(sub, mirror='X')           # -X half, exact mirror image
            pad = ws * .40
        u = u0 + pad
        u_end = u1 - pad
        guard = 0
        # the two junctions with the seam stones are joints like any other, and
        # the widest pockets left in the face were sitting right on them
        edges = [u0 + pad, u1 - pad] if seam else []
        while u < u_end - 0.05 and guard < 30:
            guard += 1
            w = ch * r.uniform(*wide)
            if r.random() < big:
                w *= r.uniform(1.4, 1.9)
            w = min(w, u_end - u)
            if u_end - (u + w) < ch * 0.5:
                w = u_end - u
            cu = u + w / 2
            sw = max((w - mortar) * overfill, 0.06)
            sh = max(chz - r.uniform(0, ch * .05), 0.05)
            dd = depth * (1 + r.uniform(-.20, .20)) + lean + r.uniform(0, ragged)
            yy = y_face + sgn * r.uniform(-jy, jy)
            m = pick(r.random())
            tx = r.uniform(-1, 1) * tilt
            out += p.blob(at(cu, yy, cz), (sw, dd, sh), m,
                          sides=sides if sw < ch * 1.35 else sides + 1,
                          axis=axis, irregular=irregular * r.uniform(.75, 1.25),
                          dome=dome * r.uniform(.7, 1.2), bevel=0, seg=1,
                          tint=tint, back=back,
                          rot=(tx, 0, zrot + r.uniform(-1, 1) * 1.4),
                          seed=seed * 61 + guard + ri * 13,
                          shade=1.0 + r.uniform(-shade_var, shade_var))
            # packing stone wedged into the joint at the end of this block
            if r.random() < chink and w > ch * 1.05:
                cw = w * r.uniform(.24, .40)
                czz = cz + sh / 2 * r.choice((-1, 1)) * .78
                if z0 + .02 < czz < z1 - .02:
                    out += p.blob(at(cu + r.uniform(-1, 1) * w * .30, yy, czz),
                                  (cw, dd * .86, ch * r.uniform(.26, .40)),
                                  m, sides=5, axis=axis, irregular=.40, dome=.55,
                                  bevel=0, seg=1, tint=tint, back=back,
                                  rot=(0, 0, zrot + r.uniform(-8, 8)),
                                  seed=seed * 131 + guard + ri * 7,
                                  shade=1.0 + r.uniform(-shade_var, shade_var))
            u += w
            if u < u_end - .05:
                edges.append(u)
        if not edges:
            # a face only one stone wide still has corner pockets either side
            # of that stone's crown, and no block boundary to hang them on
            edges = [lerp(u0 + pad, u_end, .26), lerp(u0 + pad, u_end, .74)]
        if ri < rows - 1:
            cross += [(e, zc, ch) for e in edges]
        if bed and ri == 0:
            # 0.12/0.82 threw these packing stones ~0.06 below the floor plane,
            # where the seam clamp flattened them ONTO it -- so they arrived as
            # coincident horizontal faces under the wall. 0.30/0.68 keeps them
            # inside the piece.
            cross += [(e, z0 + ch * .34, ch * .62) for e in edges]
    # ---- wedge a stone into every joint crossing: four big stones meeting
    #      leave a small pocket, and a pocket is where bare core shows.
    for (ju, jz, jch) in cross:
        if r.random() > pack:
            continue
        cw = jch * r.uniform(.56, .88)
        chh = jch * r.uniform(.42, .62)
        yy = y_face + sgn * r.uniform(-jy, jy) * .7
        out += p.blob(at(ju + r.uniform(-1, 1) * cw * .28, yy,
                         jz + r.uniform(-1, 1) * chh * .34),
                      (cw, depth * r.uniform(.74, .96), chh), pick(r.random()),
                      sides=5, axis=axis, irregular=.44, dome=.58, bevel=0,
                      seg=1, tint=tint, back=back,
                      rot=(0, 0, zrot + r.uniform(-12, 12)),
                      seed=seed * 313 + int(ju * 997) + int(jz * 131),
                      shade=1.0 + r.uniform(-shade_var, shade_var))
    return out


def _cap_course(p, x0, x1, y0, y1, z_top, thick, n, mat, seed=0, mat_alt=None,
                ragged=0.0, tint=0.075, joint=0.009, shade_var=0.12, tilt=0.9,
                chamf=0.014, cap=None, align='top'):
    """A row of flat cap slabs over a tread or a coping. `ragged` pulls the
    front (-Y) edge of each slab out by a random amount -- ref1's broken stoop
    edge; it stays 0 for ref2's dressed flight. `align='bottom'` beds every slab
    on the same plane and lets the thickness vary upward, which is what a coping
    course does: dead flat where it sits, slightly uneven along the top."""
    r = rng(f"{p.name}/cap/{seed}")
    cuts = [lerp(x0, x1, i / n) for i in range(n + 1)]
    for i in range(1, n):
        cuts[i] += r.uniform(-1, 1) * (x1 - x0) / n * 0.17
    for i in range(n):
        a, b = cuts[i] + joint / 2, cuts[i + 1] - joint / 2
        f0 = y0 - r.uniform(0, ragged)
        f1 = y0 - r.uniform(0, ragged)
        poly = [(a, f0), (b, f1), (b, y1), (a, y1)]
        m = mat if (mat_alt is None or r.random() > .32) else mat_alt
        th = thick * (1 + r.uniform(-.07, .10))
        zb = (z_top - thick) if align == 'bottom' else (z_top - th)
        _cslab(p, poly, zb, th, m, chamf=chamf, cap=cap,
               tilt=(_mtilt(r, tilt), _mtilt(r, tilt)),
               tint=tint, shade=1.0 + r.uniform(-shade_var, shade_var))


DIP = 0.034          # how far a shingle's root sinks below the sarking face


def _shingle_rows(sp, width, rows, row_h, tab, mat, mat_alt, thick=0.030,
                  seed=0, tint=0.10):
    """Flat patch of shingle rows (rows run along X, climb +Y). Built flat and
    merged onto the slope, same recipe as the roof family; bevel=0 so each
    shingle keeps its own tint and the row rhythm stays the read."""
    r = rng(f"{sp.name}/sh/{seed}")
    for ri in range(rows):
        v = ri * row_h
        n = max(1, int(round(width / tab)))
        tw = width / n
        off = (ri % 2) * tw * 0.5
        prev = None
        for i in range(n + 1):
            cu = -width / 2 + tw * (i + .5) - off
            if cu + tw / 2 < -width / 2 or cu - tw / 2 > width / 2:
                continue
            cu = clamp(cu, -width / 2 + tw * .10, width / 2 - tw * .10)
            if prev is not None and cu - prev < tw * .92:
                # the tab that overhung the end of the row was clamped back
                # INTO the row, landing 60% on top of the one before it: two
                # coplanar shingles in one slot, and the biggest single
                # coincident pair left on this roof.
                continue
            prev = cu
            h = row_h * 1.62 * (1 + r.uniform(-.07, .05))
            # the lift is stepped by ROW (0 / 9 / 18mm) with only a little
            # jitter on top: drawn freely, two shingles from neighbouring rows
            # -- which always overlap -- kept landing on the same plane.
            lift = (ri % 2) * .014 + r.uniform(0, thick * .10)
            m = mat if r.random() > .13 else mat_alt
            # every shingle roots DIP below the sarking's top face instead of
            # sitting on it: with lift able to be ~0, a shingle's underside
            # landed exactly on the boarding, and on the row below's top face
            # ...and each one is rocked ~1 degree on both axes. Laid dead
            # parallel to the boarding, a shingle's two big faces sat in the
            # same plane bucket as the sarking AND as every shingle in the row
            # above (a roof face 1.5m from the origin needs only a hair of
            # rotation to drift its plane offset by 10mm), which is most of
            # what this roof's z-fighting was.
            sp.box((cu, v + h / 2 - row_h * .31, lift + (thick - DIP) / 2),
                   (tw - .011, h, thick + DIP), m, bevel=0, tint=tint,
                   skew=(r.uniform(-1, 1) * .013, 0),
                   rot=(r.choice((-1, 1)) * r.uniform(.9, 2.3),
                        r.choice((-1, 1)) * r.uniform(.9, 2.3), 0),
                   shade=1.0 + r.uniform(-.15, .11))


# ============================================================== paving =======
# The paving's own datums are derived per variant from `t` (the wearing surface)
# and `joint_z` (how far the joint floor sits below it) -- see _flagstones.


def _flagstones(p, nx, ny, w=G, d=G, t=COB_T, joint=0.014, seed=0,
                mat="stone", mat_alt="stone_pale", mat_warm="stone_warm",
                mat_dark="stone_dark", merge_p=0.26, crack_p=0.20, gap_p=0.05,
                jitter=0.26, bulge=0.055, tint=0.092, shade_var=0.28,
                sink=0.012, dome=0.010, skirt=0.011, root=0.004,
                crown=0.26, power=1.6, rings=(0.70, 0.44), rock=1.15,
                joint_z=0.017, grit=9, warm_p=0.03, dark_p=0.11, pale_p=0.40,
                pale_s=1.00, mid_s=1.50, dark_s=1.80, warm_s=1.25):
    """Cambered pavement that tiles at (w, d).

    A jittered lattice of cells is laid over the patch. Lattice points on the
    boundary may only slide ALONG the boundary, never across it, so every joint
    lands exactly on x=+-w/2 / y=+-d/2 and a run of patches reads as one
    continuous pavement -- the seam is just another straight joint, which is
    what real flagging does anyway. Alternate rows are offset so joints run
    rather than stack, cells are merged in pairs for size variation, edges get
    optional bulged mid-points so plans come out five- and six-sided like ref1
    rather than a grid of rectangles, and a few cells are left out as worn
    hollows packed with small stones.

    Each cell is then raised as a CAMBERED stone (`_domestone`) whose crown sits
    at the paving datum `t`, whose widest line is `dome` below it, and whose
    joint floor is `joint_z` down. That section, not the plan, is what makes the
    field read as paving at a grazing angle -- see the header.

    `joint` is the width of the GROOVE between two stones at the paving datum,
    and it is now small (11-14 mm, was 22-28) and no longer a hole: the cells
    are handed to `_domestone` whole and it laps each stone `root` past its own
    cell, so the joint is cut out of a continuous surface. See _domestone.
    """
    r = rng(f"{p.name}/flag/{seed}")
    cw, cd = w / nx, d / ny
    zj = t - joint_z                     # the joint floor / top of the bed
    zb = max(zj - 0.040, 0.004)          # stones are rooted well into the bed
    P = {}
    for j in range(ny + 1):
        roff = (j % 2) * cw * 0.40 + r.uniform(-1, 1) * cw * .10
        for i in range(nx + 1):
            x = -w / 2 + cw * i
            y = -d / 2 + cd * j
            if 0 < i < nx:
                x = clamp(x + roff + r.uniform(-1, 1) * cw * jitter,
                          -w / 2 + cw * .30, w / 2 - cw * .30)
            if 0 < j < ny:
                y += r.uniform(-1, 1) * cd * jitter
            P[(i, j)] = (x, y)

    # mid-points shared by both cells either side of an edge, bulged sideways
    MID = {}

    def mid(a, b):
        k = (a, b) if a <= b else (b, a)
        if k not in MID:
            (x0, y0), (x1, y1) = P[k[0]], P[k[1]]
            if r.random() < 0.64:
                MID[k] = None
            else:
                ex, ey = x1 - x0, y1 - y0
                L = hypot(ex, ey) or 1.0
                s = r.uniform(-1, 1) * bulge
                tt = r.uniform(.40, .60)
                MID[k] = (x0 + ex * tt - ey / L * s, y0 + ey * tt + ex / L * s)
        return MID[k]

    def cell_poly(i0, i1, j):
        corners = [(i0, j), (i1, j), (i1, j + 1), (i0, j + 1)]
        out = []
        for k in range(4):
            a = corners[k]
            b = corners[(k + 1) % 4]
            out.append(P[a])
            # never bulge a boundary edge -- that is the tiling seam
            on_edge = (a[1] == b[1] and a[1] in (0, ny)) or \
                      (a[0] == b[0] and a[0] in (0, nx))
            if not on_edge:
                m = mid(a, b)
                if m:
                    out.append(m)
        return out

    taken, holes = set(), []
    for j in range(ny):
        for i in range(nx):
            if (i, j) in taken:
                continue
            i1 = i + 1
            if i + 1 < nx and (i + 1, j) not in taken and r.random() < merge_p:
                i1 = i + 2
                taken.add((i + 1, j))
            taken.add((i, j))
            if r.random() < gap_p:
                holes.append(cell_poly(i, i1, j))
                continue
            # a merged cell is sometimes emitted as two stones split by a
            # hairline joint: one big flag with a crack across it, as in ref1
            if i1 == i + 2 and r.random() < crack_p:
                parts = [cell_poly(i, i + 1, j), cell_poly(i + 1, i1, j)]
                jn = joint * 0.30
            else:
                parts = [cell_poly(i, i1, j)]
                jn = joint
            wide = len(parts) == 1 and i1 == i + 2      # a full merged flag
            for quad in parts:
                # TONE, and it is MEASURED, because this is the second half of
                # why the street vanished. assemble_inn.texture_stone multiplies
                # every stone material by a soiling field keyed on world Z, and
                # at pavement level that is x0.50 with a warm cast -- and it hits
                # the hero's backdrop plane (M_stone, z = -0.02) exactly as hard
                # as it hits us. So the two are dragged toward the same grey by
                # construction and only our own reflectance can separate them.
                # Sampled off renders/inn/inn_ref2.png, round 7's paved field
                # measured median L=126 against the dirt plane's L=123-127: the
                # SAME VALUE, which is the whole "the ground looks like bare
                # dirt" complaint. It also came out WARMER than the dirt
                # (red-blue spread 34 against 29) when a paved street should read
                # cooler and harder than earth.
                #
                # THE RULE THAT FIXES IT: the field's value histogram must
                # STRADDLE the ground's value with a GAP at it. `stone` is the
                # very material render.ground paints the backdrop with, so a
                # cobble painted `stone` at shade 1.0 is, by construction,
                # invisible -- and round 7 made that 38 % of its flags, which is
                # why the first pass of this rebuild still rendered as pale chips
                # scattered on dirt: only the stone_pale half of the field could
                # be seen at all. So every bucket is shaded to a band that clears
                # the backdrop on one side or the other:
                #
                #   dark   x0.72 of the backdrop -- reads as a dark STONE, and
                #          it is lifted a long way off black (shade 2.00 on a
                #          material whose palette entry is #46433D) so it is a
                #          stone and not a hole: at x0.58 the field rendered as
                #          harlequin patchwork rather than as masonry
                #   mid    x1.50                 -- clear of the dirt, not pale
                #   warm   x1.35                 -- ref1's occasional tan block,
                #          cut to ~1 stone a tile: it is much the warmest tone we
                #          have and at 15 % it was what made paving read as mud
                #   pale   x2.4                  -- ref1's bright lit flags
                #
                # Measured area-weighted over the surface a downward ray-cast
                # actually hits (the only honest way to weight it -- the bed plate
                # is 3.6 m2 of dark and nothing can see it), the field now sits at
                # 1.43x the backdrop's soil-matched 0.139 with a p95/p05 spread of
                # 5.2, and no stone sits ON the dirt value. In a hero-lit render
                # of a laid field that reads as median L=145 against the dirt
                # plane's 137, with the field spanning L=110..166 where the plane
                # is flat to +-1. The jitter below is RELATIVE (+-28 % of each
                # bucket's own base) so the four buckets spread into a continuum
                # instead of reading as four recognisable steps -- which is also
                # the answer to the repeat worry that made round 7 squash its
                # extremes flat: contrast is fine, a *signature* is not.
                #
                # ...and the DARK bucket is biased to SMALL stones. A merged cell
                # is twice the area of a plain one, so a dark draw on one puts a
                # 0.35 m2 dark slab in a 4 m2 tile -- and the tile is stamped 83
                # times, so that slab IS the repeat. Measured area-weighted over
                # the surface a ray-cast can actually see, an unbiased draw pulled
                # variant A's field down to 1.30x the backdrop against variant B's
                # 1.39x purely because A's stones are bigger. In ref1 the dark
                # things in a street are its small stones and its joints, never
                # its big flags, so this is what the reference does anyway.
                q = r.random()
                dkp = dark_p * (.35 if wide else 1.0)
                if q < warm_p:
                    m, base = mat_warm, warm_s
                elif q < warm_p + dkp:
                    m, base = mat_dark, dark_s
                elif q > 1.0 - pale_p:
                    m, base = mat_alt, pale_s
                else:
                    m, base = mat, mid_s
                # HEIGHT VARIATION GOES DOWN. assemble_inn pins the patch's
                # highest vertex to z = 0, so a stone standing proud does not
                # make the field taller -- it pushes every other stone further
                # under the hero backdrop plane, and only the top 20mm of the
                # field is above it. Squared rather than ^1.7 so the spread is
                # wider for the same mean: most stones sit at the datum, and the
                # few that have settled drop far enough to read as settled.
                dz = -sink * r.random() ** 2.0
                # Rooted INTO the earth course, not standing on z = 0: with
                # every flag's underside on the ground plane they all shared it
                # with the bed plate's own underside (~1 m2 of coincident
                # surface per patch), and the tilt pushed verts through it too.
                # CAMBER VARIATION. A proud sixth carry half again the camber --
                # those are cut by the backdrop below their widest line, so they
                # read as smaller, rounder, prouder stones -- and a flat-worn
                # tenth carry barely half of it. Three different sections in one
                # field is most of what stops it reading as a stamped pattern.
                qc = r.random()
                cf = (r.uniform(1.24, 1.55) if qc < .17 else
                      r.uniform(.52, .76) if qc > .90 else
                      r.uniform(.84, 1.16))
                _domestone(p, quad, zb, t + dz, m,
                           dome=dome * cf, skirt=skirt * cf,
                           gap=jn / 2 * r.uniform(.85, 1.20), root=root,
                           power=power * r.uniform(.92, 1.10),
                           crown=clamp(crown * r.uniform(.80, 1.20), .16, .48),
                           rings=rings,
                           # the rock is 3x round 7's, because _domestone now
                           # self-levels: a hard-rocked stone costs the field
                           # nothing in reveal and gives the joint between two
                           # stones a real step instead of a hairline
                           tilt=(_mtilt(r, rock), _mtilt(r, rock)),
                           tint=tint,
                           shade=base * (1.0 + r.uniform(-shade_var, shade_var)))
    # ---- grit: the small packing stones ref1 wedges into its worn hollows ----
    # WHERE they go is the whole point, and it changed with the closed field.
    # Round 6 scattered them over the whole patch, which buried most of them
    # inside a flag's own body: 180 tris of invisible geometry per tile. Round 7
    # moved them to the lattice NODES, which was right while the joints were
    # 28mm holes -- but the stones now LAP each other, so a node is solid stone
    # and a chip put there is invisible again. The only openings left in the
    # field are the worn hollows (`gap_p`), so that is where all of the grit
    # goes: `grit` extra chips are dealt round-robin into them on top of the
    # four each hollow gets, and a hollow packed with small stones is what ref1
    # actually shows where a flag has gone.
    spots = []
    hole_pack = []
    for q in holes:
        cx = sum(v[0] for v in q) / len(q)
        cy = sum(v[1] for v in q) / len(q)
        sx = (max(v[0] for v in q) - min(v[0] for v in q)) * .5
        sy = (max(v[1] for v in q) - min(v[1] for v in q)) * .5
        hole_pack.append((cx, cy, sx, sy))
    for k in range(len(hole_pack) * 4 + max(0, grit)):
        if not hole_pack:
            break
        cx, cy, sx, sy = hole_pack[k % len(hole_pack)]
        spots.append((cx + r.uniform(-1, 1) * sx * .58,
                      cy + r.uniform(-1, 1) * sy * .58,
                      clamp(min(sx, sy) * r.uniform(.26, .48), .022, .062)))
    for (cx, cy, rr) in spots:
        gh = r.uniform(.026, .046)
        # Crowns are pitched against the datum directly now rather than against
        # the joint depth: a hollow is a hole in the wearing surface, and the
        # chips wedged into it sit anywhere from flush with the stones around it
        # to a good 30mm down. The shallow end of that range is deliberate --
        # it is the only high-frequency detail the hero's 20mm reveal can see.
        top = t - r.uniform(.006, .030)
        gh = clamp(gh, .020, max(top - .014, .014))
        q = r.random()
        # cool, dark grit. A street should read harder and cooler than the
        # ground around it, and mat_warm on half the grit did the opposite.
        # It is also weighted DARKER than round 7's (0.55 stone_dark, and the
        # whole set shaded x0.88): grit lives in the joints, and the joint
        # network is the thing that has to read as a net of dark lines over a
        # pale field. Grit at the backdrop's own value is grit you cannot see.
        gm = mat_dark if q < .55 else (mat if q < .85 else mat_alt)
        gs = {mat_dark: 1.30, mat: 0.86, mat_alt: 0.42}[gm]
        # back=False: the flat ring is the grit stone's underside, buried in the
        # earth course. Built, every one of them sat on z = 0 with the bed
        # plate and with each other.
        # each one tipped a few degrees as well: dead flat, their crowns were
        # horizontal planes that could land on a flag's own courses
        p.blob((cx, cy, top - gh), (rr * 2, gh, rr * 1.7), gm, sides=5, axis='Z',
               irregular=.36, dome=.55, bevel=0, seg=1, tint=.12, back=False,
               rot=(180 + r.uniform(-6, 6), r.uniform(-6, 6),
                    r.uniform(0, 180)), seed=seed * 7 + int(cx * 91),
               shade=gs * (1.0 + r.uniform(-.18, .14)))


def _cobble(name, nx, ny, seed, **kw):
    # outward="": a paving patch has NO outward face. It tiles on x AND y, so
    # both pairs of seam planes must be cut dead flat -- the default outward="y"
    # gave the -Y seam PROUD_MAX of slack, so stones bulged out of one edge and
    # were razored off the other and a run of patches had a lump at every second
    # joint. Border stones are cut at the seam and meet their neighbour exactly,
    # which is what laid paving does anyway.
    p = Part(name, budget="ground", outward="",
             seams=dict(x=(-G / 2, G / 2), y=(-G / 2, G / 2), z=(0, COB_T + .05)))
    t = kw.get("t", COB_T)
    zj = t - kw.get("joint_z", .017)          # top of the bed course
    # Earth bed. Laid in ABSOLUTE z, and the upper course is SUNK 13mm into the
    # lower one rather than stacked on it: stacked, the two shared a 3.8 m2
    # plane. Every stone is rocked by at least a third of a degree (see _mtilt)
    # so no stone underside shares a bucket with them either. It used to:
    # 0.3 m2 per patch, on the piece a level artist lays dozens of.
    p.plate((0, 0, (zj - .012) / 2), (G, G, zj - .012), "stone_dark",
            tint=.03, shade=.70)
    # ...and the upper course is LIT now, not near-black. It used to be the
    # thing you saw down every joint, so it had to be dark; the stones LAP each
    # other now (see _domestone's `root`), so the only place it shows is the
    # floor of a worn hollow -- and at shade .52 every hollow read as a pothole
    # punched through the street. A scoured bed is dark stone, not a hole.
    p.plate((0, 0, zj - .013), (G - .10, G - .10, .026), "stone_dark",
            tint=.05, shade=1.30)
    # TRIED AND REJECTED, so the next round does not spend a day on it: patches
    # of raised silt standing 10-14mm below the crowns, so that the share of the
    # joint network crossing one would show OUR dark bed rather than the hero
    # backdrop. It works as described and it looks worse -- five big patches put
    # a 0.7 m tonal blotch in a 2 m tile and the tile repeats, so the field read
    # as a stamped decal; twenty small ones read as debris scattered over the
    # street. It is also moot now: lapping the stones closed the joints, so the
    # backdrop no longer reaches them and there is nothing for silt to hide.
    _flagstones(p, nx, ny, seed=seed, **kw)
    # axes="xy", not the default xz: x and y are the tiling seams here and z is
    # the free face. Fading on z instead let the wobble move seam verts by the
    # full 4mm, which clamp_to_seams then cut back -- a lump at every joint.
    # Amplitude down from 3.5mm to 2.2: wobble displaces by a noise VECTOR, so a
    # third of it lands on Z, and Z is the axis the whole read is rationed on.
    p.wobble(.0022, axes="xy", margin=.11)
    # ---- CEILING THE CROWNS AT THE PAVING DATUM ---------------------------
    # assemble_inn lays every patch at z = -(its own bbox top), so the SINGLE
    # highest vertex in this mesh defines where z=0 lands, and the hero backdrop
    # sits 20mm under that. One wobble-lifted vertex standing 5mm proud
    # therefore steals a quarter of the reveal from all 30-odd stones in the
    # tile -- measured, round 7 gave away 4.4mm of 20 on variant A and 5.7 on B.
    # _domestone already self-levels each stone against its own rock; this
    # catches what the wobble adds afterwards. Nothing here is a snap plane, so
    # this is a datum clamp, not a seam clamp, and it flattens only the handful
    # of verts that broke the ceiling.
    for v in p.bm.verts:
        if v.co.z > t:
            v.co.z = t
    return p.finish()


def cobble_a():
    """ref1's street: big cambered flags, five and six sided, crowned in the
    middle and falling away to a dark recessed joint. The coarse variant.

    7x7 rather than 5x5. The assembled street stamps this tile 83 times and the
    brief asks the field to read as MANY stones; 0.40 m cells read as a handful
    of slabs per tile, 0.29 m ones read as paving. It costs 900 tris of a 2200
    tri headroom, which is what the headroom was for."""
    return _cobble("SM_Ground_Cobble_2m_A", 7, 7, seed=11, joint=.012,
                   merge_p=.30, crack_p=.28, gap_p=.034, grit=5, bulge=.038,
                   dome=.014, skirt=.010, root=.004, crown=.26, power=1.6,
                   rings=(.70, .44), rock=1.70, joint_z=.019, sink=.012)


def cobble_b():
    """Smaller yard cobbles -- same tiling, three quarters the stone size, a
    tighter joint and a single-band (coned) camber, so a paved area built from
    both variants reads as two courses of masonry rather than one repeated
    stamp. The coned top is also what pays for the finer lattice: 8n-4 tris a
    stone against A's 12n-4, which is what keeps 60-odd stones inside budget."""
    return _cobble("SM_Ground_Cobble_2m_B", 9, 9, seed=23, joint=.009,
                   merge_p=.34, crack_p=.18, gap_p=.026, t=COB_T * .90,
                   jitter=.26, grit=6, sink=.010, bulge=.022,
                   dome=.011, skirt=.0085, root=.0032, crown=.26, power=1.5,
                   rings=(), rock=1.90, joint_z=.016,
                   pale_p=.43, pale_s=1.02, mid_s=1.52)


# ============================================================== steps ========
def steps_a():
    """ref1's rustic stoop: one course of rounded rubble per riser under flat
    cap slabs, a broken front edge, generous 0.45 treads. Rise 2 x RISE = 0.40."""
    W, D, TRD = 1.78, 0.92, 0.42
    y0, y1 = -D / 2, D / 2
    p = Part("SM_Ground_Steps_A", budget="ground",
             seams=dict(x=(-1.05, 1.05), y=(-.56, .50), z=(0, .46)))
    noses = [y0, y0 + TRD]
    for i, ny_ in enumerate(noses):
        z0, z1 = i * RISE, (i + 1) * RISE
        hw = W / 2 - i * .045
        cap_t = .052
        # core stops 0.024 BELOW the tread: level with it, the tilt on the cap
        # slabs lets the dark core surface through and the tread reads holed
        # ...and 0.030 short of the back face on the step that HAS a back
        # facing: the proud face of a rubble blob is flat and parallel to the
        # wall, so a core face at the same depth fights it stone for stone.
        yb_core = y1 - (.030 if i == 1 else 0.0)
        p.plate((0, (ny_ + .07 + yb_core) / 2, (z0 + z1 - .040) / 2),
                (hw * 2 - .05, yb_core - ny_ - .07, z1 - z0 - .040),
                "stone_dark", tint=.03, shade=.56)
        # riser: one course of chunky rounded boulders, front edge broken
        # back=False on all four facings: a blob's flat back ring lands ON the
        # core's own face (that is where the facing is bedded), which is a
        # coincident pair per stone. The ring is buried, so it can just go.
        _rubble(p, (-hw + .01, hw - .01), (z0, z1 - cap_t + .012), ny_ + .07,
                .090, course=z1 - z0 - cap_t, seed=40 + i, wide=(1.1, 2.1),
                big=.34, ragged=.040, jy=.020, tilt=3.4, dome=.50,
                irregular=.34, batter=.014, chink=.55, grade=.0,
                shade_var=.19, back=False)
        # sides, and the back too: a free-standing stoop doubles as the yard's
        # mounting block, so all four faces have to be built
        for sx in (-1, 1):
            _rubble(p, (ny_ + .12, y1 - .02), (z0, z1 - cap_t + .012),
                    sx * (hw - .06), .075, course=z1 - z0 - cap_t,
                    seed=60 + i * 3 + sx, flip=(sx > 0), axis='X',
                    wide=(1.0, 1.9), big=.24, ragged=.020, tilt=2.6, chink=.3,
                    grade=.0, back=False)
        if i == 1:
            _rubble(p, (-hw + .02, hw - .02), (z0, z1 - cap_t + .012),
                    y1 - .075, .070, course=z1 - z0 - cap_t, seed=70,
                    flip=True, wide=(1.1, 2.0), big=.24, tilt=2.4, chink=.35,
                    grade=.0, back=False)
        # cap slabs over the tread, projecting a broken nosing
        yb = (noses[1] + .055) if i == 0 else y1 - .008
        _cap_course(p, -hw, hw, ny_ + .008, yb, z1, cap_t, 3, "stone",
                    mat_alt="stone_pale", seed=80 + i, ragged=.026, tilt=1.4,
                    chamf=.014, joint=.014)
    p.wobble(.008)
    return p.finish()


def _newel(p, x, y, z_base, h, mat="oak_dark", seed=0):
    """ref2's handrail newel: tapered post, chamfered cap, ball finial."""
    r = rng(f"{p.name}/newel/{seed}")
    p.box((x, y, z_base + h / 2), (.112, .112, h), mat, bevel=0, taper=.88,
          taper_axis='XY', tint=.05, shade=1.0 + r.uniform(-.05, .05))
    # the cap sinks 8mm onto the post instead of sitting exactly on its top
    # face (four newels x 100 cm2 of coincident oak)
    p.box((x, y, z_base + h + .008), (.126, .126, .048), mat, bevel=0,
          taper=1.20, taper_axis='XY', tint=.05)
    p.box((x, y, z_base + h + .046), (.152, .152, .028), mat, bevel=0,
          taper=.86, taper_axis='XY', tint=.05, shade=1.03)
    p.lathe([(0, 0), (.034, .014), (.050, .042), (.043, .072), (.017, .092),
             (0, .098)], mat, at=(x, y, z_base + h + .058), sides=7, tint=.05)


def steps_b():
    """ref2's porch flight: four dressed courses, three or four blocks per
    tread with visible joints, splayed so each step is wider than the one
    above, oak handrail each side. Rise 4 x RISE = 0.80 -- ref2's porch."""
    TRD = 0.32
    p = Part("SM_Ground_Steps_B", budget="ground",
             seams=dict(x=(-1.05, 1.05), y=(-.88, .86), z=(0, 1.92)))
    y_back = 0.82
    noses = [-0.82 + i * TRD for i in range(4)]
    hws = [0.96, 0.912, 0.872, 0.838]
    r = rng("steps_b")
    # Each step is a run of dressed blocks running the WHOLE depth of the
    # flight, front nose to back face, in one solid apiece. It used to be a
    # 0.32 deep tread slab in front of a dark backing plate, with a course of
    # cheek blocks dressing the plate's flanks -- and that backing plate's top
    # face landed exactly on the bed of the step above, on the tread slabs of
    # the step above, and on the cheek blocks' feet: 4 m2 of coincident stone
    # in one piece, the worst in the kit. Full-depth blocks have no such plane,
    # they cost fewer triangles, and the flanks now read as the ends of real
    # dressed blocks rather than as a plate with strips glued to it -- which is
    # what ref2's porch actually shows.
    for i, (ny_, hw) in enumerate(zip(noses, hws)):
        z1 = (i + 1) * RISE
        # bed each course 12mm INSIDE the one below (never level with its top),
        # and step the back faces 8mm so no two of them are coplanar either
        zb = i * RISE - (.030 if i else 0.0)
        yb = y_back - .008 * i
        n = 4 if hw > .89 else 3
        cuts = [lerp(-hw, hw, k / n) for k in range(n + 1)]
        for k in range(1, n):
            cuts[k] += r.uniform(-1, 1) * (2 * hw / n) * .11
        for k in range(n):
            a, b = cuts[k] + .006, cuts[k + 1] - .006
            m = "stone" if r.random() > .34 else "stone_pale"
            _cslab(p, [(a, ny_), (b, ny_ + r.uniform(-.008, .008)),
                       (b, yb), (a, yb)], zb, z1 - zb, m,
                   chamf=.013, cap=.056, tilt=(_mtilt(r, .30), _mtilt(r, .30)),
                   tint=.055, shade=.95 + r.uniform(-.07, .07))
    # ---- oak handrails
    z_low = RISE + 0.90                       # rail top over the bottom tread
    slope = RISE / TRD
    y_lo, y_hi = noses[0] + TRD * .46, noses[3] + TRD * .42
    z_hi = z_low + slope * (y_hi - y_lo)
    for sx in (-1, 1):
        xr, xt = sx * (hws[0] - .13), sx * (hws[3] - .13)
        # newel feet sink 14mm into the tread they stand on, so their
        # undersides are not level with the tread surface
        _newel(p, xr, y_lo, RISE - .014, z_low - RISE - .060, seed=1 + sx)
        _newel(p, xt, y_hi, 4 * RISE - .014, z_hi - 4 * RISE - .060,
               seed=3 + sx)
        for dz, wh in ((0.0, (.078, .056)), (-0.32, (.062, .046))):
            p.beam((xr, y_lo - .11, z_low + dz - slope * .11),
                   (xt, y_hi + .12, z_hi + dz + slope * .12),
                   wh[0], wh[1], "oak_dark", bevel=0, tint=.05, shade=.98)
        # short level return along the landing edge, as in ref2
        p.beam((xt, y_hi + .10, z_hi), (xt, y_back - .02, z_hi), .070, .052,
               "oak_dark", bevel=0, tint=.05)
    p.wobble(.004)
    return p.finish()


def steps_c():
    """Three risers: rubble risers, dressed cap slabs, and a low stone cheek
    wall on one side -- a third silhouette, and the flight that reaches ref1's
    0.60 threshold. Rise 3 x RISE = 0.60."""
    TRD, W = 0.34, 1.60
    p = Part("SM_Ground_Steps_C", budget="ground",
             seams=dict(x=(-1.12, 1.12), y=(-.72, .70), z=(0, 1.10)))
    y_back = 0.68
    noses = [-0.68 + i * TRD for i in range(3)]
    for i, ny_ in enumerate(noses):
        z0, z1 = i * RISE, (i + 1) * RISE
        hw = W / 2 - i * .022
        cap_t = .058
        # (as steps_a: keep the core clear of the tread's underside -- and
        # 0.012 clear of the BACK face, which the landing slabs own)
        p.plate((0, (ny_ + .05 + y_back - .012) / 2, (z0 + z1 - .042) / 2),
                (hw * 2 - .04, y_back - .012 - ny_ - .05, z1 - z0 - .042),
                "stone_dark", tint=.03, shade=.72)
        _rubble(p, (-hw + .01, hw - .01), (z0, z1 - cap_t + .010), ny_ + .05,
                .066, course=z1 - z0 - cap_t, seed=120 + i, wide=(1.2, 2.3),
                big=.24, ragged=.012, jy=.010, tilt=2.0, dome=.42,
                irregular=.26, chink=.45, grade=.0, back=False)
        _rubble(p, (ny_ + .08, y_back - .02), (z0, z1 - cap_t + .010),
                -(hw - .05), .058, course=z1 - z0 - cap_t, seed=140 + i,
                axis='X', wide=(1.1, 2.0), big=.20, tilt=1.8, chink=.25,
                grade=.0, back=False)
        y_t = min(ny_ + TRD, y_back)
        _cap_course(p, -hw, hw, ny_ + .008, y_t + (.042 if i < 2 else 0.0), z1,
                    cap_t, 4, "stone_pale", mat_alt="stone", seed=160 + i,
                    ragged=.014, tilt=1.0, chamf=.014, joint=.011)
    _cap_course(p, -W / 2 + .04, W / 2 - .04, noses[2] + TRD - .012, y_back,
                3 * RISE, .054, 3, "stone", mat_alt="stone_pale", seed=175,
                tilt=.7, chamf=.014)
    # ---- cheek wall on +X, stepping up with the flight, capped with coping.
    # ONE stepped core, not a plate per block: consecutive blocks lap 0.048 in
    # Y, so three plates shared both of their X faces and their z = 0
    # undersides across every lap. The core's front edges also stand 0.014
    # BEHIND each block's nose, and its back 0.012 in front of the last
    # block's end, so the facing stones and the backing skins own those planes.
    cx0, cx1 = W / 2 - .015, W / 2 + .225
    blocks = [(ny_, min(ny_ + TRD, y_back) + (.048 if i < 2 else 0.0),
               (i + 1) * RISE + .32) for i, ny_ in enumerate(noses)]
    prof = [(blocks[0][0] + .014, 0.0), (blocks[-1][1] - .012, 0.0)]
    for k in range(len(blocks) - 1, -1, -1):
        yf, _yt, top = blocks[k]
        prof.append((prof[-1][0], top - .014))
        prof.append((yf + .014, top - .014))
    p.prism(prof, cx1 - cx0, "stone_dark", axis='X',
            at=((cx0 + cx1) / 2, 0, 0), bevel=0, tint=.03, shade=.7)
    # ---- inner parapet skin: ONE stepped prism, for the same reason the core
    # is one. It stands 0.018 proud of the core's face so the facing stones on
    # the parapet have something mid-tone behind them instead of dark core --
    # but as three plates, one per block, it shared BOTH of its X planes with
    # itself across every 0.048 lap. Measured at 0.5 mm: 2 x 28.1 cm2, and the
    # -X pair is the parapet you look straight at from the flight, 100 %
    # ray-reachable (the +X pair is buried in the core, 0 %). The lap itself is
    # deliberate and is NOT the bug -- so this prism is the exact UNION of the
    # same three rectangles, identical volume, no plane shared with itself.
    #   bottom steps up where a block ENDS, top steps up where the next BEGINS,
    #   which is what makes the union a single staircase and not two pieces.
    par = [(blocks[0][0], RISE)]
    for k in range(len(blocks) - 1):
        par.append((blocks[k][1], (k + 1) * RISE))
        par.append((blocks[k][1], (k + 2) * RISE))
    par.append((blocks[-1][1], len(blocks) * RISE))
    par.append((blocks[-1][1], blocks[-1][2] - .062))
    for k in range(len(blocks) - 1, 0, -1):
        par.append((blocks[k][0], blocks[k][2] - .062))
        par.append((blocks[k][0], blocks[k - 1][2] - .062))
    par.append((blocks[0][0], blocks[0][2] - .062))
    p.prism(par, .030, "stone", axis='X', at=(cx0 - .003, 0, 0), bevel=0,
            tint=.04, shade=.66)
    for i, ny_ in enumerate(noses):
        top = (i + 1) * RISE + .32
        y_t = min(ny_ + TRD, y_back) + (.048 if i < 2 else 0.0)
        _rubble(p, (ny_ + .01, y_t), (0.0, top - .062), cx1 - .010, .052,
                course=.215, seed=190 + i, axis='X', flip=True, wide=(1.2, 2.2),
                big=.18, tilt=1.6, jy=.008, chink=.70, grade=.25,
                overfill=1.34, vfill=1.30, pack=1.0, bed=True, back=False)
        # the stepped FRONT end of each cheek block: left bare it reads as a
        # dark staircase punched into the wall, so face it as well. Only the
        # band above the block below is ever seen, so one course does it.
        z_lo = 0.0 if i == 0 else (i * RISE + .32 - .022)
        # Both secondary faces get a mid-tone backing skin flush with the core
        # BEFORE the stones go on: these faces are only 0.24 wide, one stone
        # per course, so what is left between stones reads as light mortar
        # instead of a hole punched through the wall.
        # It only ever backs the front-end stones, which run x 0.799..1.017,
        # so it starts INSIDE the core at cx0 + .015. It used to start 0.008
        # OUTSIDE the core, which put it across the inner parapet skin and
        # gave the two of them a shared top plane at top - .062 wherever they
        # crossed: 3 x 6 cm2 at 0.5 mm, one of them half reachable through the
        # tilt gap under the coping. Now nothing of it is coplanar with the
        # parapet, and its +X face is where it was, buried in the outer stones.
        xf0, xf1 = cx0 + .015, cx1 + .008
        p.plate(((xf0 + xf1) / 2, ny_ + .020, (z_lo + top - .062) / 2),
                (xf1 - xf0, .030, top - .062 - z_lo), "stone", tint=.04,
                shade=.70)
        _rubble(p, (cx0 + .014, cx1 - .008), (z_lo, top - .062), ny_ + .048,
                .046, course=max((top - .062 - z_lo) * .55, .17),
                seed=232 + i, axis='Y', wide=(.85, 1.5), big=.10, tilt=1.6,
                jy=.006, chink=.60, grade=.20, dark_p=.0, back=False,
                overfill=1.34, vfill=1.36, pack=1.0)
        # ...and its INNER face, the parapet you see from the flight itself:
        # everything above the tread is in plain view and was bare core too
        _rubble(p, (ny_ + .012, y_t - .008), ((i + 1) * RISE + .004,
                top - .062), cx0 + .012, .044, course=.20, seed=262 + i,
                axis='X', wide=(.9, 1.7), big=.12, tilt=1.5, jy=.006,
                chink=.55, grade=.18, dark_p=.0, mat="stone_pale",
                mat_alt="stone", back=False, overfill=1.34, vfill=1.24,
                pack=1.0)
        # one coping slab per cheek block. NOTE the argument order: this
        # coping runs along Y, so the slab is cut across X (n=1) and spans the
        # block in Y -- passing them the other way round threw the slab out
        # over the middle of the flight and left the cheek top bare.
        _cap_course(p, cx0 - .022, cx1 + .012, ny_ - .010, y_t, top, .062, 1,
                    "stone_pale", seed=210 + i, tilt=.6, chamf=.016,
                    align='bottom')
    p.wobble(.005)
    return p.finish()


# =========================================================== threshold ======
def threshold():
    """One big worn doorstep on a bedding course, with packing stones where it
    beds into the paving. Sits under any door opening; 1.52 wide clears the
    widest opening in spec.OPENINGS."""
    W, D, T = 1.52, 0.64, 0.18
    p = Part("SM_Ground_ThresholdSlab", budget="ground",
             seams=dict(x=(-.92, .92), y=(-.46, .40), z=(0, .24)))
    r = rng("threshold")
    p.prism([(-W / 2, -D / 2 + .035), (W / 2, -D / 2 + .022), (W / 2, D / 2),
             (-W / 2, D / 2)], .080, "stone_dark", axis='Z',
            at=(0, 0, .040), bevel=0, tint=.05, shade=.78)
    # the wearing stone, split in two like every real threshold
    xs = 0.21
    poly_l = [(-W / 2 + .015, -D / 2 + .050), (xs - .014, -D / 2 + .038),
              (xs - .014, D / 2 - .012), (-W / 2 + .022, D / 2 - .016)]
    poly_r = [(xs + .014, -D / 2 + .038), (W / 2 - .015, -D / 2 + .058),
              (W / 2 - .026, D / 2 - .014), (xs + .014, D / 2 - .012)]
    for poly in (poly_l, poly_r):
        # bedded 0.062, not 0.076: sitting 4mm inside the bedding course its
        # underside shared that course's top plane
        _cslab(p, poly, .062, T - .062, "stone_pale", chamf=.020,
               tilt=(_mtilt(r, .7), _mtilt(r, .7)), tint=.05,
               shade=.97 + r.uniform(-.06, .06))
    # kerb / packing stones along the front and the two ends
    for i in range(8):
        cx = lerp(-W / 2 + .07, W / 2 - .07, (i + .5) / 8) + r.uniform(-.03, .03)
        # back=False on every kerb stone: the ring is its underside, and on
        # z = 0 it shared that plane with the bedding course and with its
        # neighbours (a tenth of a square metre of coincident faces)
        p.blob((cx, -D / 2 - .008, 0.0),
               (r.uniform(.14, .24), r.uniform(.062, .092), r.uniform(.15, .22)),
               "stone" if r.random() > .38 else "stone_warm", sides=6, axis='Z',
               irregular=.34, dome=.52, bevel=0, seg=1, tint=.12, back=False,
               rot=(180 + r.uniform(-4, 4), r.uniform(-4, 4),
                    r.uniform(-16, 16)), seed=300 + i,
               shade=1.0 + r.uniform(-.17, .13))
    for sx in (-1, 1):
        for j in range(2):
            p.blob((sx * (W / 2 + .010),
                    lerp(-D / 2 + .14, D / 2 - .10, (j + .5) / 2), 0.0),
                   (.24, .075, .20), "stone", sides=6, axis='Z', irregular=.30,
                   dome=.46, bevel=0, seg=1, tint=.11, back=False,
                   rot=(180 + r.uniform(-4, 4), r.uniform(-4, 4),
                        90 + r.uniform(-12, 12)),
                   seed=320 + j * 2 + sx, shade=1.0 + r.uniform(-.15, .12))
    p.wobble(.006)
    return p.finish()


# ========================================================== garden wall =====
def garden_wall():
    """Low rubble boundary wall, faced BOTH sides and battered so it leans back
    as it rises, with a flat coping course that oversails ~0.025 each way.
    Tiles along X at GRID.

    Both faces are packed rubble in ref1's sense -- 0.02-0.03 creases, no bare
    hearting anywhere -- which needs three things working together:
      * the hearting is only 0.075 back from each face, so a crease is a thin
        dark line rather than a 0.08 deep hole;
      * the courses are over-filled in BOTH directions (vfill) and every joint
        crossing is packed, so the leftovers are pocket-sized;
      * `seam=True` lays a mirrored half-stone on x = +-1.0 in every course, so
        a tiled run laps one whole stone over each module joint. Without it
        every course butts the seam and the run gets a bare full-height column
        of hearting every 2 m -- the single most obvious tiling tell there is.
    Both rubble faces are built with back=False: the back ring of every stone
    is buried inside the hearting block, so those faces can never be seen.
    """
    p = Part("SM_Ground_GardenWall_2m", budget="ground",
             seams=dict(x=(-G / 2, G / 2), y=(0, GW_T), z=(0, GW_H)))
    z_cop = GW_H - .120
    # hearting: wide, so the packed stones sit only ~0.06 proud of it
    p.plate((0, GW_T / 2, z_cop / 2), (G - .060, GW_T - .150, z_cop),
            "stone_dark", tint=.03, shade=.52)
    # ...but its cut ENDS are pale, so the end of a run (or a lone panel) reads
    # as the sawn cross-section of packed rubble instead of a dark hole. Buried
    # between two tiles in a run, where nothing can see them.
    for sx in (-1, 1):
        # held 0.008 back off the module plane: flush with it, this plate's
        # face was coplanar with every seam stone the x-clamp had cut, so the
        # end of a run flickered all the way up
        # ...and stopped 0.008 SHORT of z_cop. At z_cop its top face sat on the
        # hearting's own top face, 0.008 x 0.25 of overlap each end -- 2 x 19.9
        # cm2 at 0.5 mm. Both are inside the coping bed (0.802..0.858) so a ray
        # reaches neither of them (measured 0 %), but the fix is a constant and
        # costs no geometry, and the top 8 mm of this plate was never doing any
        # work: the bed is what you see there.
        p.plate((sx * (G / 2 - .023), GW_T / 2, (z_cop - .008) / 2),
                (.030, GW_T - .130, z_cop - .008), "stone", tint=.05, shade=.86)
    # rubble runs UP INTO the coping zone so no mortar band shows under it
    _rubble(p, (-G / 2, G / 2), (0, z_cop + .055), .095, .080, course=.225,
            seed=401, wide=(1.05, 1.95), big=.30, tilt=2.4, jy=.007,
            batter=.020, chink=.50, grade=.42, shade_var=.19, dark_p=.05,
            overfill=1.38, vfill=1.34, pack=1.0, seam=True, back=False,
            bed=True)
    # the back face is set 0.013 deeper than it was: at GW_T - .105 the
    # crowns of its stones reached the coping bed's back plane and fought it
    _rubble(p, (-G / 2, G / 2), (0, z_cop + .055), GW_T - .118, .075,
            course=.250, seed=402, flip=True, wide=(1.15, 2.0), big=.26,
            tilt=2.2, jy=.007, batter=.016, chink=.45, grade=.32,
            mat="stone_pale", mat_alt="stone", shade_var=.17, dark_p=.04,
            overfill=1.38, vfill=1.34, pack=1.0, seam=True, back=False,
            bed=True)
    # coping bed + coping OVERSAIL the front face, so no stone nose pokes out
    # in front of the coping line -- the coping is what reads as the top edge
    # the bed spans the wall's own thickness: at (GW_T - .020) its front face
    # was on the coping slabs' front plane, and its back on their back plane
    p.plate((0, GW_T / 2, z_cop + .010), (G, GW_T, .056),
            "stone", tint=.04, shade=.82)
    _cap_course(p, -G / 2, G / 2, -.014, GW_T - .006, GW_H, .120, 4,
                "stone", mat_alt="stone_pale", seed=403, tilt=1.0, joint=.008,
                tint=.06, chamf=.010, align='bottom')
    p.wobble(.007)
    # cut the seam stones dead on the module planes (no PROUD_MAX slack in X):
    # each becomes a true half-stone, and two of them make one stone in a run.
    keep, p.seams = p.seams, dict(x=(-G / 2, G / 2))
    p.clamp_to_seams(proud=0.0)
    p.seams = keep
    return p.finish()


# ============================================================== fence =======
def fence():
    """ref2's boundary: close-boarded riven palings butted tight, tops cut off
    at ragged heights, nailed to two lapped rails, one hewn post per bay. Tiles
    along X at GRID -- the post sits inside the seam so a run gives one post
    every 2m."""
    p = Part("SM_Ground_Fence_2m", budget="ground",
             seams=dict(x=(-G / 2, G / 2), y=(0, .22), z=(0, FN_H + .16)))
    r = rng("fence")
    # slot 0 must be the boards' material: util's paint set is what it is, and
    # anything that slips through wants to look like a board, not like iron.
    z_r0, z_r1 = 0.40, 1.16
    # rails at .090, not .118: they used to hang 0.02 clear BEHIND the boards
    # they are supposedly nailed to. Now they bite into them, and their front
    # plane (0.044) is clear of every board's back plane (0.052 and deeper).
    for zr, sg in ((z_r0, 1), (z_r1, -1)):
        p.beam((-G / 2, .070, zr), (G / 2, .070, zr - sg * .014), .092, .070,
               "oak_mid", bevel=0, tint=.06, shade=.90)
    # ---- palings
    n = 11
    pitch = G / n
    for i in range(n):
        cx = -G / 2 + pitch * (i + .5)
        bw = pitch * r.uniform(.93, .99)
        top = FN_H - r.uniform(0, .30) ** 1.4 * .95
        bot = r.uniform(.015, .075)
        lean = r.uniform(-1, 1) * .014
        a, b = -bw / 2, bw / 2
        k = r.random()
        if k < .28:                          # chopped to a rough point
            poly = [(a, bot), (b, bot + r.uniform(-.02, .02)),
                    (b, top - r.uniform(.10, .20)),
                    (r.uniform(-.25, .25) * bw, top),
                    (a, top - r.uniform(.10, .20))]
        elif k < .62:                        # one slanting axe cut
            poly = [(a, bot), (b, bot + r.uniform(-.02, .02)),
                    (b + lean, top - r.uniform(.06, .18)), (a + lean, top)]
        else:                                # squared off, slightly uneven
            poly = [(a, bot), (b, bot + r.uniform(-.02, .02)),
                    (b + lean, top - r.uniform(0, .035)),
                    (a + lean, top - r.uniform(0, .035))]
        d = .050 * r.uniform(.85, 1.15)
        m = "oak_mid" if r.random() > .34 else ("oak_dark" if r.random() > .4
                                               else "oak_pale")
        # riven boards do not come off the pit all one thickness: every third
        # one stands 7mm further out. Flush, all eleven front faces were ONE
        # plane, and the boards' 1-degree lean was enough to make neighbours
        # overlap in it and fight.
        yo = (i % 3) * .007
        p.prism(poly, d, m, axis='Y', at=(cx, d / 2 + .002 + yo, 0), bevel=0,
                tint=.085, rot=(0, r.uniform(-1, 1) * 1.1, 0),
                shade=1.0 + r.uniform(-.13, .10))
        for zr in (z_r0, z_r1):
            if bot + .05 < zr < top - .05:
                p.box((cx + r.uniform(-1, 1) * bw * .24, .012 + yo,
                       zr + r.uniform(-1, 1) * .028), (.030, .028, .026),
                      "iron", bevel=0, tint=.05)
    # ---- hewn post just inside the left seam, split top
    px = -G / 2 + .105
    # y = .110, not .086: the post used to stand with its front face on the
    # boards' own front plane (0.003 against 0.002), so the whole 0.27 m2 of it
    # fought the first paling. A close-boarded fence has its posts BEHIND the
    # boards anyway -- that is what the boards are nailed to.
    p.box((px, .110, FN_H * .50), (.168, .166, FN_H), "oak_dark", bevel=0,
          taper=.87, taper_axis='XY', tint=.05, skew=(.014, -.006))
    # the split top sinks 0.014 into the post: sitting exactly on FN_H its
    # underside was coplanar with the post's top face
    p.prism([(-.076, 0), (.078, 0), (.034, .125), (-.052, .088)], .152,
            "oak_dark", axis='Y', at=(px, .110, FN_H - .014), bevel=0,
            tint=.055, shade=.94)
    p.wobble(.007)
    return p.finish()


# =============================================================== well =======
def well():
    """Yard well. Coursed rubble drum on a dressed coping ring, two oak posts
    carrying a steep shingled gablet at the kit pitch, and an iron-strapped
    windlass. The roof deliberately borrows the roof family's row rhythm and
    verge teeth so the well reads as built by the same hands. (Bucket, rope
    coil and moss are props/.)"""
    p = Part("SM_Ground_Well", budget="ground",
             seams=dict(x=(-1.0, 1.0), y=(-1.0, 1.0), z=(0, 2.35)))
    r = rng("well")
    R_OUT, H_DRUM = 0.60, 0.78
    # ---- drum: a tube of mortar with three courses of rubble laid round it
    p.cyl((0, 0, H_DRUM / 2), R_OUT - .075, H_DRUM, "stone_dark", sides=14,
          cap=False, tint=.03, shade=.60)
    p.cyl((0, 0, H_DRUM / 2), R_OUT - .215, H_DRUM, "stone_dark", sides=12,
          cap=False, tint=.03, shade=.32)
    # the water disc's rim is buried in the drum wall. At R_OUT - .215 it had
    # the same radius AND the same facet count as the shaft lining, so its
    # twelve side facets were exactly coincident with the lining's.
    p.cyl((0, 0, .085), R_OUT - .175, .03, "iron", sides=12, tint=.03, shade=.42)
    ncr = 3
    for ci in range(ncr):
        ch = H_DRUM / ncr
        cz = ch * (ci + .5)
        nst = 8
        a0 = r.uniform(0, 1)
        for k in range(nst):
            a = 2 * pi * (k + a0 + r.uniform(-.16, .16)) / nst
            # over-filled the same way _rubble packs a flat face: a hexagonal
            # blob only covers ~65% of its slot, so the slot has to be beaten
            # or the drum shows mortar between every stone
            w = 2 * pi * R_OUT / nst * r.uniform(1.16, 1.42)
            dd = .080 * (1 + r.uniform(-.16, .16)) + .012 * (ncr - 1 - ci)
            m = "stone" if r.random() > .40 else (
                "stone_pale" if r.random() > .38 else "stone_warm")
            p.blob(((R_OUT - .075) * cos(a), (R_OUT - .075) * sin(a),
                    cz + r.uniform(-.012, .012)),
                   (w, dd, ch * 1.20), m, sides=6, axis='Y', irregular=.32,
                   dome=.48, bevel=0, seg=1, tint=.115,
                   rot=(r.uniform(-3, 3), 0, degrees(a) + 90 + r.uniform(-2, 2)),
                   seed=500 + ci * 20 + k, shade=1.0 + r.uniform(-.17, .14))
    # ---- coping: eight dressed slabs, chamfered, oversailing the drum
    nco, r_i, r_o = 8, R_OUT - .185, R_OUT + .070
    for i in range(nco):
        a0 = 2 * pi * i / nco + .015
        a1 = 2 * pi * (i + 1) / nco - .015
        am = (a0 + a1) / 2
        poly = [(r_i * cos(a0), r_i * sin(a0)), (r_o * cos(a0), r_o * sin(a0)),
                (r_o * cos(am), r_o * sin(am)), (r_o * cos(a1), r_o * sin(a1)),
                (r_i * cos(a1), r_i * sin(a1)), (r_i * cos(am), r_i * sin(am))]
        _cslab(p, poly, H_DRUM - .020, .150,
               "stone_pale" if r.random() > .34 else "stone", chamf=.016,
               tilt=(r.uniform(-1, 1) * .8, r.uniform(-1, 1) * .8),
               tint=.06, shade=.97 + r.uniform(-.09, .08))
    z_cop = H_DRUM + .130
    # ---- posts, head beam, braces
    px, z_eave = 0.44, 1.44
    for sx in (-1, 1):
        # foot sunk 12mm into the coping (its underside used to sit 2mm off
        # the coping's top face)
        p.box((sx * px, 0, (z_cop - .012 + z_eave) / 2),
              (.155, .155, z_eave - z_cop + .012),
              "oak_dark", bevel=0, taper=.90, taper_axis='XY', tint=.05,
              shade=1.0 + r.uniform(-.05, .05))
        p.prism([(0, 0), (.34, 0), (0, .34)], .105, "oak_dark", axis='Y',
                at=(sx * (px + .062), 0, z_eave - .40), bevel=0, tint=.05,
                rot=(0, 0 if sx > 0 else 180, 0), shade=.97)
    p.beam((-px - .19, 0, z_eave - .085), (px + .19, 0, z_eave - .085), .115,
           .125, "oak_dark", bevel=0, tint=.05)
    # ---- windlass
    zw = 1.10
    p.cyl((0, 0, zw), .080, .84, "oak_mid", sides=8, axis='X', tint=.06)
    for sx in (-1, 1):
        p.cyl((sx * .27, 0, zw), .090, .050, "iron", sides=8, axis='X', tint=.04)
        p.cyl((sx * .43, 0, zw), .032, .080, "iron", sides=6, axis='X', tint=.04)
    p.beam((.45, 0, zw), (.45, 0, zw + .18), .044, .044, "iron", bevel=0, tint=.04)
    p.beam((.45, 0, zw + .162), (.45, .20, zw + .162), .040, .040, "iron",
           bevel=0, tint=.04)
    p.cyl((.45, .225, zw + .162), .032, .110, "oak_pale", sides=6, axis='Y',
          tint=.06)
    p.cyl((0, -.012, .60), .020, 1.02, "rope", sides=5, tint=.07)
    # ---- roof: steep gablet at the kit pitch, small shingles, verge teeth
    half_d, rw = 0.58, 1.32
    L = half_d / S.COS_P
    z_ridge = z_eave + half_d * S.SIN_P / S.COS_P
    # sarking boards under the shingles, so no daylight between the rows
    sub = p.sub("well_slope")
    sub.box((0, L / 2, -.026), (rw, L, .052), "oak_dark", bevel=0, tint=.04,
            shade=.70)
    _shingle_rows(sub, rw, 6, L / 6 * .99, .142, "shingle_moss", "shingle",
                  thick=.028, seed=3)
    # LEFT ALONE, DELIBERATELY, and this is the note for whoever measures next.
    # The two slopes come off ONE sub, so laid symmetrically their sarking
    # boards' side faces are both on x = +-rw/2 and the two raking quads cross
    # at the apex: 27.9 cm2 at 0.5 mm, x2 counting the mirror at 1.5 mm. It is
    # SEALED -- ray-sampled over the clipped overlap it is 0 % reachable,
    # because the -Y verge beam covers the apex -- so there is nothing to see
    # and nothing to gain. I tried the free fix anyway (4 mm of X on the -Y
    # slope alone) and it was strictly worse: the shingle tabs reach x = 0.713
    # (cu clamps to width/2 - tab*.10, plus half a tab), the verge cheeks are
    # on 0.710, and 4 mm walked one row of tabs straight onto that plane --
    # 147.8 cm2 at 0.66 mm and 100 % ray-reachable, i.e. five times the sealed
    # overlap it removed, out in plain view. Any global X offset of this slope
    # has to clear 0.650 / 0.668 / 0.710 / 0.728 AND the per-shingle skew and
    # rock, so there is no safe constant. Leave it sealed.
    for m, at in ((slope_matrix(), (0, -half_d, z_eave)),
                  (Matrix.Rotation(pi, 4, 'Z') @ slope_matrix(),
                   (0, half_d, z_eave))):
        p.merge(sub, at=at, rot=m)
    for sy in (-1, 1):
        # eave fascia: without it the slope reads as a floating board.
        # It runs to +-(rw/2 + .020), NOT + .050. At .050 its end grain landed
        # on x = +-0.71 -- exactly the OUTER cheek of the verge beam beside it
        # (xv -+ .030), so 69.0 cm2 of fascia end sat 0.34 mm off the verge face
        # and 100 % of it was ray-reachable: much the largest real fight in the
        # family. A fascia butts INTO the verge board anyway, so end it inside
        # the verge (0.68 is within 0.650..0.710 and within 0.668..0.728, the
        # two verges' spans) and let the verge overhang it as it should.
        p.beam((-rw / 2 - .020, sy * (half_d + .028), z_eave - .045),
               (rw / 2 + .020, sy * (half_d + .028), z_eave - .045), .075, .095,
               "oak_dark", bevel=0, tint=.05)
        for sx in (-1, 1):
            # the two rakes of a verge meet at the apex, so they overlap: 0.007
            # of X between them keeps their cheeks off one shared plane
            xv = sx * (rw / 2 + .020 + (.018 if sy > 0 else 0.0))
            p.beam((xv, sy * (half_d + .040), z_eave - .058),
                   (xv, 0, z_ridge - .058), .060, .150,
                   "oak_dark", bevel=0, tint=.05, extend=.030)
    p.beam((-rw / 2 - .07, 0, z_ridge + .022), (rw / 2 + .07, 0, z_ridge + .022),
           .090, .090, "oak_dark", bevel=0, tint=.05)
    p.wobble(.005)
    return p.finish()


# ================================================================ build =====

def steps_flight():
    """A SHORT FLIGHT that climbs exactly one foundation course.

    steps_a is a two-riser rustic stoop with 0.42 m treads over 0.92 m of depth --
    deliberately generous, and correct for a free-standing mounting block. But at the
    inn's entrance it reads as flagstones lying flat rather than stairs, because a
    0.40 m rise spread over 0.92 m is a ramp: about 23 degrees. This piece is the
    stair version, sized so its top tread lands DEAD ON the foundation:

        3 risers x (S.H_FOUND / 3) = S.H_FOUND exactly, on 0.29 m goings
        -> about 27 degrees of pitch and three readable nosings

    steps_a is untouched and still the right piece for a yard stoop.
    """
    n = 3
    rise = S.H_FOUND / n                     # .150, so the flight matches the course
    GO = 0.29
    W = 1.90
    depth = n * GO
    y0 = -depth / 2
    p = Part("SM_Ground_StepsFlight_2m", budget="ground",
             seams=dict(x=(-1.05, 1.05), y=(y0 - .06, -y0 + .16),
                        z=(0, S.H_FOUND + .02)))
    for i in range(n):
        z0, z1 = i * rise, (i + 1) * rise
        ny = y0 + i * GO                      # this tread's nosing
        hw = W / 2 - i * .035                 # flight narrows slightly as it climbs
        cap_t = .046
        # solid core behind the facing, stopping just under the tread so the cap
        # slabs sit proud and the dark core cannot show through the joint
        yb = -y0 + .10
        p.plate((0, (ny + .05 + yb) / 2, (z0 + z1 - .034) / 2),
                (hw * 2 - .05, yb - ny - .05, z1 - z0 - .034),
                "stone_dark", tint=.03, shade=.56)
        # riser face: one course of rounded boulders, front edge broken
        _rubble(p, (-hw + .01, hw - .01), (z0, z1 - cap_t + .010), ny + .05,
                .075, course=z1 - z0 - cap_t, seed=170 + i, wide=(1.0, 1.9),
                big=.30, ragged=.034, jy=.018, tilt=3.0, dome=.52,
                irregular=.32, batter=.012, chink=.50, grade=.0,
                shade_var=.18, back=False)
        # cheeks
        for sx in (-1, 1):
            _rubble(p, (ny + .10, yb - .02), (z0, z1 - cap_t + .010),
                    sx * (hw - .05), .065, course=z1 - z0 - cap_t,
                    seed=190 + i * 2 + (sx > 0), wide=(1.0, 1.7), big=.24,
                    ragged=.030, jy=.016, tilt=2.6, dome=.46, irregular=.30,
                    batter=.010, chink=.45, grade=.0, shade_var=.16,
                    axis='X', back=False)
        # tread: two or three cap slabs with a broken front nosing
        r = rng(f"stepsflight/tread/{i}")
        nslab = 3 if i < 2 else 2
        for k in range(nslab):
            u0 = -hw + (2 * hw) * k / nslab
            u1 = -hw + (2 * hw) * (k + 1) / nslab
            over = .035 + r.uniform(0, .022)          # nosing oversail
            p.box(((u0 + u1) / 2, (ny - over + yb) / 2,
                   z1 - cap_t / 2),
                  (u1 - u0 - .012, yb - ny + over, cap_t),
                  "stone_pale" if r.random() < .45 else "stone",
                  bevel=.010, seg=1, tint=.06,
                  rot=(r.uniform(-.9, .9), 0, r.uniform(-.6, .6)),
                  shade=1.0 + r.uniform(-.07, .07))
    p.wobble(.005, axes="xz")
    return p.finish()

def build():
    # cobble_a FIRST on purpose: build_piece.py aims closeup.png and tiled.png at
    # objs[0], and the paving is both the piece under review and the one whose
    # tiling has to be provable (it is the only piece in the family that tiles on
    # two axes AND gets laid 1.10 oversize by the assembler). lineup.png still
    # shows the whole family, and nothing outside this module depends on the
    # order -- the assembler and the registry look pieces up by name.
    return [cobble_a(), cobble_b(), garden_wall(), fence(), steps_a(), steps_b(),
            steps_c(), steps_flight(), threshold(), well()]


# ================================================================= demo =====
def _stamp(src, name, loc, rz=0.0):
    o = src[name].copy()
    o.data = src[name].data
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (0, 0, radians(rz))
    return o


def demo():
    """A corner of the inn's yard, composed for the ref2 camera (elevated 3/4
    from the front-right). Two level changes, one for each masonry language:

      * the porch flight (dressed, handrailed) climbs 0.80 from the yard to the
        terrace behind the boundary wall, with the threshold slab at its head;
      * the cheek-walled flight climbs 0.60 out to the left onto a kerbed bank,
        which carries the paling fence as the yard's back boundary;
      * the rustic stoop stands free in the yard as a mounting block -- what a
        low two-riser stoop is actually for in a coaching yard;
      * the well is the foreground focal point, off centre and turned.

    Everything standing on paving sits at z = COB_T, because that is where the
    paving's wearing surface is. The kerb along the bank is the SAME garden wall
    piece, dropped 0.34 so only its top 0.60 shows -- a level artist's move, and
    the reason the coping is built as a separate course.
    """
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_")}
    out = []
    r = rng("ground_demo_v3")
    W = COB_T                                   # the walk plane

    def pave(x0, x1, y0, y1, z):
        nx = int(round((x1 - x0) / G))
        ny = int(round((y1 - y0) / G))
        for i in range(nx):
            for j in range(ny):
                nm = "SM_Ground_Cobble_2m_B" if (i * 2 + j + r.randrange(3)) % 3 \
                    else "SM_Ground_Cobble_2m_A"
                out.append(_stamp(src, nm,
                                  (x0 + G * (i + .5), y0 + G * (j + .5), z),
                                  rz=90 * r.randrange(4)))

    def wall(loc, rz=0.0, sink=0.0):
        out.append(_stamp(src, "SM_Ground_GardenWall_2m",
                          (loc[0], loc[1], W - sink), rz=rz))

    # ---- levels: yard 0, bank 0.60 (3 x RISE), terrace 0.80 (4 x RISE)
    pave(-4.0, 4.0, -2.0, 2.0, 0.0)
    pave(-4.0, 4.0, 2.4, 4.4, 0.80)
    pave(-6.4, -4.4, -2.0, 2.0, 0.60)

    # ---- terrace boundary wall along y = 2.0, 2m gap at x in (0, 2)
    for cx in (-3.0, -1.0, 3.0):
        wall((cx, 2.0))
    # ---- kerb retaining the left bank: same piece, sunk so 0.60 shows,
    #      open where the cheek-walled flight comes through
    wall((-4.4, 1.0), rz=90, sink=.34)
    wall((-5.4, -2.0), sink=.34)

    # ---- the two flights, and the doorway they serve
    out.append(_stamp(src, "SM_Ground_Steps_B", (1.0, 1.58, W)))
    out.append(_stamp(src, "SM_Ground_ThresholdSlab", (1.0, 3.05, W + .80)))
    out.append(_stamp(src, "SM_Ground_Steps_C", (-3.68, -1.0, W), rz=90))

    # ---- rustic stoop as a free-standing mounting block
    out.append(_stamp(src, "SM_Ground_Steps_A", (2.35, -1.00, W), rz=-30))

    # ---- well, foreground focal point
    out.append(_stamp(src, "SM_Ground_Well", (-1.40, -0.60, W), rz=-26))

    # ---- paling fence on the bank: a run along Y and a return along X
    for cy in (-1.0, 1.0):
        out.append(_stamp(src, "SM_Ground_Fence_2m", (-6.4, cy, W + .60), rz=90))

    for nm in src:
        src[nm].location = (0, 60, 0)
    return out
