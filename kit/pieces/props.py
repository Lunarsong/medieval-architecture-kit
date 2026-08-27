"""Props -- the clutter that makes an inn look lived in. Measured off the refs:

  * ref1 barrels: coopered casks, and they are SQUAT. Measured off the crop,
    the height is 1.00-1.05x the belly diameter -- never the 1.25x a real
    hogshead has. Get that ratio wrong and the cask reads as an oil drum, and
    it is the first thing anyone notices. NARROW staves (~0.15m of arc each, so
    twenty of them round a 0.93m cask), each one a different tone --
    that stripe of tone variation IS the barrel. SIX narrow DARK-IRON hoops,
    each only ~2.6% of the cask height and clearly darker than any stave, in
    three close-set pairs: one pair at each chime -- the outer band of which is
    flush with the very end of the staves, capping their tips into a clean ring
    -- and one pair straddling the bilge. The head is sunk a little below that
    ring, so you look down into a dark lip rather than at a row of teeth.
  * ref2 shed: squatter golden-oak casks with thin dark iron hoops lying on their
    sides on wedges; slatted crates with corner posts and a diagonal brace;
    slumped canvas sacks; a 3m ladder against the wall; a pail on a trestle.
  * both refs: everything stands in a fringe of weeds -- narrow tapered blades
    fanning out, white daisies, small orange/gold flower heads -- and a creeper
    runs along the top of the porch beam then drops in SEPARATE tendrils of
    different lengths, never a solid curtain.

Conventions (spec.py, "FLOOR / PROP"): origin at the footprint centre, Z=0 on
the ground, interesting face toward -Y. Nothing here is welded into a wall --
the level artist decides where the mess goes.

NOTE (local workaround, see the task's `needs`): util.Part._emit loses a
primitive's own faces when it bevels them -- bmesh.ops.bevel replaces those
faces and only the new strip faces come back in `res["faces"]` -- so they keep
material slot 0 and no colour jitter. Every bevelled primitive in this module
therefore goes through _bev(), which repaints everything the call created.
"""
import bpy
from math import cos, sin, pi, sqrt, radians, degrees, asin, atan2
from mathutils import Vector, Euler
from kit import spec as S
from kit.util import Part, rng, lerp, clamp

FAMILY = "props"
COLLECTION = "12_Props"
TAU = 2 * pi


# ------------------------------------------------------------------ helpers --
def _bev(p, prim, args, mat, tint=.05, shade=1.0, **kw):
    """Bevelled primitive with every face it created actually painted."""
    before = set(p.bm.faces)
    getattr(p, prim)(*args, mat, tint=tint, shade=shade, **kw)
    new = [f for f in p.bm.faces if f.is_valid and f not in before]
    if new:
        p._paint(new, mat, tint, shade)
    return new


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _swz(axis):
    """(cross-section a, cross-section b, along-axis u) -> world xyz."""
    if axis == 'X':
        return lambda a, b, u: (u, a, b)
    if axis == 'Y':
        return lambda a, b, u: (a, u, b)
    return lambda a, b, u: (a, b, u)


def _pad(p, at, size, mat, seed=0, sides=7, shade=1.0, tint=.10, irregular=.30,
         dome=.35, bevel=.012, back=True, rock=(0.0, 0.0)):
    """A boulder / earth pad sitting ON the ground: blob(axis='Z') bulges toward
    -Z from a flat back, so it is flipped to grow upward from z = at[2].
    size = (width x, height up, depth y).

    `back=False` drops the flat underside -- pads laid on one plane all shared
    it, which is a coincident pair per overlapping pair of pads. `rock` tips the
    pad a couple of degrees so its crown is not a dead-flat plane either."""
    _bev(p, "blob", (at, size), mat, tint=tint, shade=shade, sides=sides,
         axis='Z', irregular=irregular, dome=dome, bevel=bevel, seg=1,
         back=back, rot=(180 + rock[0], rock[1], 0), seed=seed)


def _loft(p, rings, mat, tint=.05, shade=1.0, flip=False, cap0=True, cap1=True):
    """Sweep a four-corner section through `rings` as ONE solid.

    Why this exists. A curved timber built as a CHAIN of abutting p.beam()
    segments carries an interior butt joint at every kink, and because each
    beam's end cap is square to ITS OWN axis, the two caps meeting at a joint
    share a centre exactly and then splay apart by the kink angle. On the barrel
    staves that was measured as:
      * a 2.0-2.7 mm open slit running right round the belly of every cask, and
        the same depth of interpenetration on the inner face -- visible as a dark
        crack across every stave in a close render;
      * 3408 cm2 of pairs on check_zfight's 0.5 mm gate (100% of the props
        family's total, and the largest number in the kit), because the gate
        measures separation at the face CENTRES and for a hinge pair that is
        exactly zero.
    A lofted solid has no interior faces at all, mitres the joint so the outer
    surface runs through the kink unbroken, and costs 25% fewer tris.

    `rings` are four points each, ordered (-tangential,-out), (-t,+out),
    (+t,+out), (+t,-out), sweeping along the section axis. `flip` reverses every
    face for a mirrored (left-handed) coordinate swizzle."""
    m = len(rings)
    vs = [v for ring in rings for v in ring]
    F = []
    for k in range(m - 1):
        a, b = k * 4, (k + 1) * 4
        for i in range(4):
            j = (i + 1) % 4
            F.append((a + i, a + j, b + j, b + i))
    if cap0:
        F.append((3, 2, 1, 0))
    if cap1:
        o = (m - 1) * 4
        F.append((o, o + 1, o + 2, o + 3))
    if flip:
        F = [tuple(reversed(f)) for f in F]
    return p._emit(vs, F, mat, tint, 0, None, shade)


def _mitre(prof):
    """Per-section mitre frame for a 2D centreline `prof` = [(across, along)..].

    Returns, for every section, the OUTWARD unit normal of the section plane
    already divided by cos(half-kink) -- so offsetting a corner by
    normal * thickness/2 lands the two adjoining faces on one another instead of
    pinching at the joint."""
    seg = []
    for k in range(len(prof) - 1):
        dr = prof[k + 1][0] - prof[k][0]
        du = prof[k + 1][1] - prof[k][1]
        L = sqrt(dr * dr + du * du) or 1.0
        seg.append((dr / L, du / L))
    out = []
    for k in range(len(prof)):
        a_ = seg[max(0, k - 1)]
        b_ = seg[min(len(seg) - 1, k)]
        vr, vu = a_[0] + b_[0], a_[1] + b_[1]
        L = sqrt(vr * vr + vu * vu) or 1.0
        vr, vu = vr / L, vu / L
        c = max(.50, vr * b_[0] + vu * b_[1])      # cos of the half-kink
        out.append((vu / c, -vr / c))
    return out


def _hand(sw):
    """+1 if the cross-section swizzle is right-handed, -1 if mirrored. The
    loft's face winding follows it, or a whole barrel comes out inside-out."""
    a = Vector(sw(1, 0, 0))
    b = Vector(sw(0, 1, 0))
    return 1 if a.cross(b).dot(Vector(sw(0, 0, 1))) > 0 else -1


def _pole(p, pts, r0, r1, mat, sides=6, tint=.08, shade=1.0, seed=0, knob=.06,
          cap=True):
    """A round pole -- a shaved sapling -- following a polyline and tapering
    r0 -> r1 along it, with a little knuckle of radius jitter at every joint.

    ref2's ladder is made of exactly this: round in section, crooked, and much
    thinner at the top than at the foot. A straight extruded box cannot read as
    one, which is why the stiles used to look milled."""
    r = rng(f"{p.name}/pole/{seed}")
    n = len(pts) - 1
    for k in range(n):
        a, b = Vector(pts[k]), Vector(pts[k + 1])
        d = b - a
        if d.length < 1e-6:
            continue
        dn = d.normalized()
        # interior joints overlap slightly, so each cap ends up buried inside
        # the next segment rather than welding into a non-manifold seam
        ov = d.length * .06
        a2 = a - dn * (ov if k else 0.0)
        b2 = b + dn * (ov if k < n - 1 else 0.0)
        ra = lerp(r0, r1, k / n) * (1 + r.uniform(-knob, knob))
        rb = lerp(r0, r1, (k + 1) / n) * (1 + r.uniform(-knob, knob))
        p.cyl(tuple((a2 + b2) / 2), ra, (b2 - a2).length, mat, sides=sides,
              axis='Z', r_top=rb, cap=cap, tint=tint,
              rot=(degrees(-asin(clamp(dn.y, -1.0, 1.0))),
                   degrees(atan2(dn.x, dn.z)), 0.0),
              shade=shade * (1 + r.uniform(-.075, .06)))


# ------------------------------------------------------------------ barrels --
def _barrel(p, at=(0, 0, 0), axis='Z', h=.94, r_end=.298, r_belly=.375, n=16,
            stave="oak_mid", hoop="iron", seed=1, thick=.034,
            hoop_w=None, pair=None, sink=None,
            bung='head', tint=.075, shade=1.0, gap=.008, hoop_shade=1.55):
    """A coopered cask. Staves are laid one at a time, in four segments each so
    they follow the belly curve, and every stave carries its own tone. A dark
    inner shell closes the barrel and doubles as the two sunk heads, so the
    joints between staves read as shadow.

    Hooping follows the refs exactly: SIX bands, all dark iron (far darker than
    any stave tone -- that contrast is what makes a hoop read as a hoop), each
    only ~2.6% of the cask height, arranged in three close-set PAIRS. One pair
    sits at each chime, and the outer band of that pair is flush with the end of
    the staves so the chime is a clean iron ring instead of bare sawtooth stave
    tips; the third pair straddles the bilge. `hoop_w` is the band width, `pair`
    the centre-to-centre spacing inside a pair."""
    sw = _swz(axis)
    r = rng(f"{p.name}/barrel/{seed}")
    lv = (0.0, .245, .50, .755, 1.0)
    r_q = lerp(r_end, r_belly, .82)
    rad = (r_end, r_q, r_belly, r_q, r_end * .99)
    hw = hoop_w if hoop_w else h * .026     # quarter / bilge band width
    hwe = hw * 1.25                         # head band at the chime, a bit wider
    sp = pair if pair else h * .125         # centre-to-centre inside one pair

    # inner shell (its shadowed gaps are what makes the staves read) + the two
    # heads, sunk just below the chime ring like the refs
    inset = sink if sink else h * .042
    prof = [(rad[k] * (.955 if k in (0, 4) else .93), lv[k] * h)
            for k in range(5)]
    p.lathe(prof, stave, at=at, sides=n, axis=axis, tint=.04, shade=.40,
            close=False)
    for uf, sgn in ((0.0, 1), (1.0, -1)):
        p.cyl(_add(at, sw(0, 0, uf * h + sgn * (inset + .017))), r_end * .952,
              .034, stave, sides=n, axis=axis, cap=True, tint=.05, shade=.86)

    tip = min(.010, hwe * .40)   # how far short of each end the staves stop

    def gap_at(t):
        """Staves are jointed tight where the head hoop grips them and open up
        over the bilge, so each chime closes into a ring rather than a sawtooth
        of separate tips."""
        return gap * (.20 + .80 * clamp(2.9 * min(t, 1.0 - t)))

    # One stave is FIVE sections of the belly profile swept as a single solid.
    # It used to be four abutting p.beam()s, and every one of the three joints
    # between them left two square-cut caps sharing a centre and splaying apart
    # by the kink -- a 2.0-2.7 mm crack right round the belly of the cask, and
    # the whole of the props family's 3408 cm2 on the z-fight gate. See _loft().
    prof = [(rad[k], lv[k] * h) for k in range(5)]
    prof[0] = (rad[0], tip)                 # staves stop short of each chime
    prof[4] = (rad[4], h - tip)
    wid = [2 * rad[k] * sin(pi / n) - gap_at(lv[k]) for k in range(5)]
    mit = _mitre(prof)
    flip = _hand(sw) < 0
    for i in range(n):
        a0 = TAU * (i + .5) / n
        ca, sa = cos(a0), sin(a0)
        sh = shade * (1.0 + r.uniform(-.22, .15))
        rings = []
        for k in range(5):
            rk, uk = prof[k]
            mr, mu = mit[k]
            tw = wid[k] * .5
            rings.append([
                _add(at, sw(ca * (rk + sm * mr * thick * .5) - sa * st * tw,
                            sa * (rk + sm * mr * thick * .5) + ca * st * tw,
                            uk + sm * mu * thick * .5))
                for st, sm in ((-1, -1), (-1, 1), (1, 1), (1, -1))])
        _loft(p, rings, stave, tint=tint, shade=sh, flip=flip)

    def rad_at(u):
        """Stave centreline radius at along-axis position u."""
        t = clamp(u / h, 0.0, 1.0)
        for k in range(4):
            if t <= lv[k + 1] or k == 3:
                return lerp(rad[k], rad[k + 1],
                            clamp((t - lv[k]) / (lv[k + 1] - lv[k])))
        return rad[-1]

    def band(u, wide, mat=None, sides=None):
        """Hoop OUTSIDE the staves, tapered over its own width so it hugs the
        curve instead of punching through the flaring chime."""
        sd = sides or (n + 4)

        def rh_of(uu):
            rr = rad_at(uu)
            chord = 2 * rr * sin(pi / n)
            corner = sqrt((rr + thick / 2) ** 2 + (chord / 2) ** 2)
            return corner / cos(pi / sd) + .0055
        p.cyl(_add(at, sw(0, 0, u)), rh_of(u - wide / 2), wide, mat or hoop,
              sides=sd, axis=axis, r_top=rh_of(u + wide / 2), cap=False,
              tint=.045, bevel=0,
              shade=hoop_shade * (1.0 + r.uniform(-.05, .07)))

    # Three pairs -- chime, bilge, chime. The two outer bands run flush to the
    # ends of the staves (u from 0 to hwe, and h - hwe to h), so neither chime is
    # left as a bare fringe of stave tips.
    for u, wide in ((hwe * .5, hwe),
                    (hwe * .5 + sp, hw),
                    (h * .5 - sp * .58, hw),
                    (h * .5 + sp * .58, hw),
                    (h - hwe * .5 - sp, hw),
                    (h - hwe * .5, hwe)):
        band(u, wide)

    # board joints scored across each head
    # The battens STRADDLE the head's surface, 0.010 either side of it. Built
    # 0.014 thick starting exactly at the head's face, their only visible face
    # was coplanar with the head -- so a barrel end showed nothing but a
    # flicker where its board joints should be. Four barrels x two ends.
    for uf, sgn in ((0.0, 1), (1.0, -1)):
        uz = uf * h + sgn * inset
        for o in (-.06, .09):
            sz = sw(.016, 2 * (r_end - .055), .020)
            p.box(_add(at, sw(o, 0, uz)), (abs(sz[0]), abs(sz[1]), abs(sz[2])),
                  "oak_dark", bevel=0, tint=.04, shade=.60)
    if bung == 'head':
        # bedded 0.014 INTO the head instead of 0.001 above it
        p.cyl(_add(at, sw(r_end * .46, 0, h - inset + .008)), .034, .044,
              "oak_dark", sides=6, axis=axis, cap=True, tint=.05, shade=.62)
    elif bung == 'belly':
        p.cyl(_add(at, sw(0, r_belly - .012, h * .5)), .036, .060, "oak_dark",
              sides=6, axis='Z', cap=True, tint=.05, shade=.62)


def barrel_large_a():
    """The ref1 tun: a BIG SQUAT cask -- 0.94 high on a 0.93 belly, so 1.01x,
    which is what the reference crop measures (the old 1.25x read as a drum).
    Widening the belly instead of dropping the height keeps it the largest piece
    in the family and keeps it clearly apart from the paler, smaller B. Twenty
    staves, because a 2.9m belly hooped in sixteen gives planks, not staves."""
    p = Part("SM_Prop_Barrel_Large_A", budget="prop",
             seams=dict(x=(-.54, .54), y=(-.54, .54), z=(0, 1.00)))
    _barrel(p, h=.94, r_end=.372, r_belly=.465, n=20, stave="oak_mid",
            hoop="iron", seed=1, thick=.036, hoop_w=.026, pair=.126,
            tint=.085, hoop_shade=1.60)
    p.wobble(.005, freq=2.2, respect_seams=False)
    return p.finish()


def barrel_large_b():
    """The ref2 cask: squatter, pale golden oak, thin dark iron hoops."""
    p = Part("SM_Prop_Barrel_Large_B", budget="prop",
             seams=dict(x=(-.50, .50), y=(-.50, .50), z=(0, .92)))
    _barrel(p, h=.84, r_end=.328, r_belly=.404, n=17, stave="oak_pale",
            hoop="iron", seed=2, hoop_w=.021, pair=.114,
            tint=.08, shade=.88, hoop_shade=1.78)
    p.wobble(.005, freq=2.2, respect_seams=False)
    return p.finish()


def barrel_small_c():
    """Half-keg -- the short fat ones stacked at ref1's cellar door."""
    p = Part("SM_Prop_Barrel_Small_C", budget="prop",
             seams=dict(x=(-.36, .36), y=(-.36, .36), z=(0, .64)))
    _barrel(p, h=.56, r_end=.216, r_belly=.268, n=13, stave="oak_mid",
            hoop="iron", seed=3, thick=.030, hoop_w=.0165, pair=.081,
            tint=.095, shade=.93, gap=.007, hoop_shade=1.44)
    p.wobble(.004, freq=2.6, respect_seams=False)
    return p.finish()


def _chock(p, at, sy, w=.17, hh=.15, near=.30, far=.45, seed=0):
    """Wedge shoved under a lying cask so it cannot roll."""
    r = rng(f"{p.name}/chock/{seed}")
    if sy > 0:
        tri = [(near, 0), (far, 0), (near, hh)]
    else:
        tri = [(-far, 0), (-near, 0), (-near, hh)]
    _bev(p, "prism", (tri, w), "oak_dark", tint=.07,
         shade=.98 + r.uniform(-.10, .10), axis='X', at=at, bevel=.008, seg=1)


def barrel_lying_large():
    """Big cask on its side, wedged. The belly touches the ground and the ends
    float clear -- exactly how the pair under ref2's shed sit."""
    rb, re, L = .428, .339, .94
    p = Part("SM_Prop_Barrel_Lying_Large", budget="prop",
             seams=dict(x=(-L / 2 - .12, L / 2 + .12), y=(-.54, .54),
                        z=(0, rb * 2 + .08)))
    _barrel(p, at=(-L / 2, 0, rb - .004), axis='X', h=L, r_end=re, r_belly=rb,
            n=18, stave="oak_pale", hoop="iron", seed=4, thick=.036,
            hoop_w=.025, pair=.124, bung='belly', tint=.08, shade=.90,
            hoop_shade=1.66)
    for sx in (-.23, .25):
        for sy in (-1, 1):
            _chock(p, (sx, 0, 0), sy, w=.145, hh=.124, near=.300, far=.425,
                   seed=int(sx * 100) + sy)
    p.wobble(.004, freq=2.4, respect_seams=False)
    return p.finish()


def barrel_lying_small():
    """Keg on its side -- drops into the groove between two big ones."""
    rb, re, L = .268, .216, .56
    p = Part("SM_Prop_Barrel_Lying_Small", budget="prop",
             seams=dict(x=(-L / 2 - .06, L / 2 + .06), y=(-.34, .34),
                        z=(0, rb * 2 + .05)))
    _barrel(p, at=(-L / 2, 0, rb - .003), axis='X', h=L, r_end=re, r_belly=rb,
            n=13, stave="oak_mid", hoop="iron", seed=5, thick=.030,
            hoop_w=.0155, pair=.077, bung='belly', tint=.095, hoop_shade=1.44)
    p.wobble(.004, freq=2.8, respect_seams=False)
    return p.finish()


# ------------------------------------------------------------------- crates --
def _crate(p, at, size, seed=0, mat="oak_mid", mat2="oak_pale", slats=4,
           lid=False, brace=False, tilt=0.0, top=False):
    r = rng(f"{p.name}/crate/{seed}")
    w, d, h = size
    post, bd = .062, .024
    # dark interior, set back so the gaps between slats read as shadow
    p.plate(_add(at, (0, 0, h / 2)), (w - .17, d - .17, h - .05), "oak_dark",
            tint=.03, shade=.30)
    for sx in (-1, 1):
        for sy in (-1, 1):
            _bev(p, "box", (_add(at, (sx * (w / 2 - post / 2),
                                      sy * (d / 2 - post / 2), h / 2)),
                            (post, post, h)), mat, tint=.06,
                 shade=.96 + r.uniform(-.08, .08), bevel=.008, seg=1)
    gap = .042
    sh_ = (h - gap * (slats - 1) - .05) / slats
    for i in range(slats):
        cz = .022 + sh_ / 2 + i * (sh_ + gap)
        for sy in (-1, 1):
            _bev(p, "box", (_add(at, (0, sy * (d / 2 - bd / 2 - .006), cz)),
                            (w - post * 2 + .006, bd, sh_)), mat2, tint=.08,
                 shade=.98 + r.uniform(-.12, .10), bevel=.007, seg=1)
        for sx in (-1, 1):
            _bev(p, "box", (_add(at, (sx * (w / 2 - bd / 2 - .006), 0, cz)),
                            (bd, d - post * 2 + .006, sh_)), mat2, tint=.08,
                 shade=.93 + r.uniform(-.12, .10), bevel=.007, seg=1)
    # top rail: 1.25 x board thickness and pulled out to the post face. At
    # 1.6 x its inner face landed 1mm off the slats' inner face, so every slat
    # fought the rail where they cross.
    for sy in (-1, 1):
        _bev(p, "box", (_add(at, (0, sy * (d / 2 - .006), h - .024)),
                        (w, bd * 1.25, .048)), mat, tint=.05, shade=1.02,
             bevel=.007, seg=1)
    for sx in (-1, 1):
        _bev(p, "box", (_add(at, (sx * (w / 2 - .006), 0, h - .024)),
                        (bd * 1.25, d - .05, .048)), mat, tint=.05, shade=.97,
             bevel=.007, seg=1)
    if top:
        for cu in (-.325, 0, .325):
            _bev(p, "box", (_add(at, (0, cu * d, h - .056)),
                            (w - post * 2 + .01, d * .29, .032)), mat2,
                 tint=.08, shade=.99 + r.uniform(-.10, .09), bevel=.007, seg=1)
    if brace:
        p.beam(_add(at, (-w / 2 + .075, -d / 2 - .010, .07)),
               _add(at, (w / 2 - .075, -d / 2 - .010, h - .09)), .052, .022,
               mat, bevel=0, tint=.06, shade=1.06)
    if lid:
        for cu in (-.31, 0, .31):
            _bev(p, "box", (_add(at, (0, cu * d, h + .024)),
                            (w + .035, d * .31, .036)), mat, tint=.07,
                 shade=1.0 + r.uniform(-.08, .08), bevel=.008, seg=1,
                 rot=(0, tilt, 0))


def crate_a():
    """Slatted packing crate, the one under ref2's shed."""
    w, d, h = .66, .58, .56
    p = Part("SM_Prop_Crate_A", budget="prop",
             seams=dict(x=(-w / 2 - .05, w / 2 + .05),
                        y=(-d / 2 - .05, d / 2 + .05), z=(0, h + .03)))
    _crate(p, (0, 0, 0), (w, d, h), seed=1, slats=4, brace=True, top=True)
    p.wobble(.004, freq=2.0, respect_seams=False)
    return p.finish()


def crate_b():
    """Smaller crate, lid dropped on askew. Stacks on A."""
    w, d, h = .50, .44, .40
    p = Part("SM_Prop_Crate_B", budget="prop",
             seams=dict(x=(-w / 2 - .07, w / 2 + .07),
                        y=(-d / 2 - .07, d / 2 + .07), z=(0, h + .11)))
    _crate(p, (0, 0, 0), (w, d, h), seed=2, mat="oak_dark", mat2="oak_mid",
           slats=3, lid=True, tilt=2.5, top=True)
    p.wobble(.004, freq=2.0, respect_seams=False)
    return p.finish()


# -------------------------------------------------------------------- sacks --
def _sack(p, at, s=1.0, mat="rope", seed=0, sides=11, shade=1.0, lean=0.0,
          yaw=0.0, rot=None, tie=True, fold=.155, squash=1.0, cord="oak_dark",
          puddle=3, lobes=3):
    """A tied sack of grain, built as a lumpy ring lattice -- every panel of
    sacking its own quad, because revolving a smooth profile here gives a
    ceramic urn.

    Two things make cloth read as CLOTH rather than as a boulder, and the first
    version of this had neither:

      * creases that RUN VERTICALLY. Each panel column keeps its own radius
        offset AND its own tone from foot to neck, so the value bands follow the
        folds up the sack. Per-quad random shading speckles instead, and speckle
        on a lumpy blob is exactly how a rock is shaded.
      * a hard-cinched NECK. The profile pinches to a fifth of the belly radius,
        a dark cord bites round it, two cord ends hang, and the gathered mouth
        flops back OUT above the tie.

    Widest low down where the load slumps and spreads it; the foot ring is left
    flat and un-jittered so the sack sits ON the ground, and a little sacking
    puddles out where it meets it."""
    r = rng(f"{p.name}/sack/{seed}")
    # (height, radius): flat foot, heavy low belly, long throat, tie, then the
    # gathered mouth flaring back out above the cord.
    prof = [(.000, .234), (.016, .264), (.068, .282), (.146, .286),
            (.228, .272), (.310, .242), (.382, .196), (.438, .143),
            (.476, .097), (.500, .062), (.532, .092), (.556, .046)]
    tie_i = 9
    # a few BIG folds with smaller ones between them, not a regular flute: one
    # low-frequency lobe pattern plus noise, held constant up each column
    ph = r.uniform(0, TAU)
    crease = [sin(TAU * lobes * i / sides + ph) * .80 + r.uniform(-.55, .55)
              for i in range(sides)]
    tone = [1.0 + r.uniform(-.20, .15) for i in range(sides)]
    if rot is None:
        rot = (lean * .7, lean, yaw)
    mtx = Euler([radians(a) for a in rot], 'XYZ').to_matrix()
    base = Vector(at)

    def env(hh):
        """How loose the cloth is: squashed flat where it takes the load on the
        ground, slacker and slacker as it rises toward the gathered throat, and
        pulled hard tight in the inch where the cord bites."""
        return (clamp(hh / .055) * (.55 + .90 * clamp(hh / .44))
                * (1.0 - .82 * clamp(1.0 - abs(hh - prof[tie_i][0]) / .056)))

    rings = []
    for hh, rr in prof:
        e = env(hh)
        ring = []
        for i in range(sides):
            a = TAU * i / sides
            rad = rr * s * (1 + fold * crease[i] * e
                            + r.uniform(-.045, .045) * e)
            ring.append(mtx @ Vector((cos(a) * rad * squash, sin(a) * rad,
                                      (hh + r.uniform(-.009, .009) * e) * s))
                        + base)
        rings.append(ring)
    for li in range(len(rings) - 1):
        a0, a1 = rings[li], rings[li + 1]
        row = .80 + .34 * (li / (len(rings) - 2))   # top-lit, not noisy
        for i in range(sides):
            j = (i + 1) % sides
            # tint stays LOW on purpose: per-quad jitter speckles, and speckle
            # on a lumpy blob is precisely how stone is shaded
            p.quad(tuple(a0[i]), tuple(a0[j]), tuple(a1[j]), tuple(a1[i]), mat,
                   tint=.035, shade=shade * tone[i] * row)
    top = rings[-1]
    ctr = sum(top, Vector((0, 0, 0))) / len(top) + (mtx @ Vector((0, 0, .014 * s)))
    for i in range(sides):
        j = (i + 1) % sides
        p.quad(tuple(top[i]), tuple(top[j]), tuple(ctr), tuple(ctr), mat,
               tint=.035, shade=shade * tone[i] * 1.16)
    if tie:
        nz, nr = prof[tie_i]
        p.cyl(tuple(mtx @ Vector((0, 0, nz * s)) + base), nr * s + .013, .034,
              cord, sides=sides, cap=False, tint=.10, rot=rot,
              shade=.94 + r.uniform(-.07, .07))
        for k in range(5):        # the gathered mouth flopping over the cord
            a = TAU * (k + .30) / 5 + ph
            d = mtx @ Vector((cos(a) * 1.0, sin(a) * 1.0, -.30 * r.uniform(.4, 1.5)))
            o = mtx @ Vector((cos(a) * .050 * s, sin(a) * .050 * s,
                              (nz + .034) * s))
            _leaf(p, tuple(o + base), tuple(d), .120 * s, .125 * s, mat,
                  shade * r.uniform(.80, 1.02), fold=.46, tint=.05)
        for k in range(2):        # two cord ends left hanging
            a = TAU * (k + .18) / 2
            o = mtx @ Vector((cos(a) * (nr * s + .010),
                              sin(a) * (nr * s + .010), nz * s))
            e2 = mtx @ Vector((cos(a) * (nr * s + .034),
                               sin(a) * (nr * s + .034), (nz - .088) * s))
            p.beam(tuple(o + base), tuple(e2 + base), .014, .012, cord,
                   bevel=0, tint=.06, shade=.98)
    for k in range(puddle):       # sacking spilling out along the ground
        a = TAU * (k + .42) / max(1, puddle) + ph
        o = mtx @ Vector((cos(a) * .195 * s, sin(a) * .195 * s, .016 * s))
        d = mtx @ Vector((cos(a) * 1.0, sin(a) * 1.0, -.34))
        _leaf(p, tuple(o + base), tuple(d), .125 * s, .150 * s, mat,
              shade * r.uniform(.66, .86), fold=.22, tint=.05)


def sacks():
    """Three sacks slumped together, and they must not read as one another:
    three sizes, three values, none of them cream. A big brown hessian one, a
    smaller olive one leaning back on it, and a grubby grey canvas half-sack
    tipped over against the pile at the front. Every one of them keeps its
    cinched neck UP and visible in silhouette -- the old third sack was laid
    flat, so all you could see was a pale foreshortened lump, and a pale
    foreshortened lump is a boulder."""
    p = Part("SM_Prop_Sacks", budget="prop",
             seams=dict(x=(-.74, .74), y=(-.70, .68), z=(0, .70)))
    _sack(p, (-.30, .14, 0), s=1.06, mat="oak_pale", seed=1, sides=11,
          shade=1.00, lean=-7, yaw=15, lobes=3)
    _sack(p, (.26, .28, 0), s=.90, mat="rope", seed=2, sides=10, shade=.92,
          lean=9, yaw=140, fold=.135, lobes=2)
    # DARK sacking, not pale canvas: whatever sits at the front of the pile is
    # what gets read, and a pale lump at the front reads as a boulder
    _sack(p, (.02, -.26, 0), s=.80, mat="oak_mid", seed=3, sides=11,
          shade=1.06, lean=20, yaw=-150, fold=.195, lobes=3)
    p.wobble(.010, freq=4.6, respect_seams=False)
    return p.finish()


# ------------------------------------------------------------------- ladder --
def ladder():
    """3m yard ladder. ref2's is a pair of shaved SAPLINGS: round in section,
    crooked over their whole length, and clearly thinner at the top than at the
    foot, with the rungs driven through and left standing proud on both sides.
    The old stiles were straight parallel boxes, which is why the thing read as
    a milled part instead of something a yardman knocked together.
    Built upright -- lean it on a wall in the level."""
    H, wb, wt = 3.00, .50, .335
    p = Part("SM_Prop_Ladder", budget="prop",
             seams=dict(x=(-.41, .41), y=(-.21, .21), z=(0, H + .05)))
    r = rng("ladder")

    def path(sx, by, bx, ph, ph2):
        """Stile centreline: converging hard toward the top, and crooked in BOTH
        planes -- one long belly plus a slower S-bend, at different phases on
        the two stiles, so the ladder is nowhere straight and nowhere parallel.
        `bx` is signed: one stile bellies out where the other waists in, which
        is what makes every rung a slightly different length."""
        out = []
        for k in range(8):
            t = k / 7.0
            hw = (lerp(wb / 2, wt / 2, t) + bx * sin(pi * t)
                  + .018 * sin(TAU * 1.5 * t + ph2))
            out.append((sx * hw,
                        by * sin(pi * t) + .032 * sin(TAU * t + ph) + .016 * t,
                        t * H))
        return out

    stiles = (path(-1, .066, .058, .4, 1.1), path(1, .042, -.034, 3.2, 4.4))
    for si, pts in enumerate(stiles):
        _pole(p, pts, .050 - si * .004, .0265 - si * .0015, "oak_mid",
              sides=7, tint=.075, seed=10 + si, knob=.085,
              shade=1.0 + (si * 2 - 1) * .06)

    def at_t(pts, t):
        f = clamp(t) * (len(pts) - 1)
        k = min(int(f), len(pts) - 2)
        u = f - k
        return [lerp(pts[k][i], pts[k + 1][i], u) for i in range(3)]

    z = .215
    while z < H - .17:
        t = z / H
        a, b = at_t(stiles[0], t), at_t(stiles[1], t)
        dz = r.uniform(-.013, .013)
        rr = .0265 * r.uniform(.92, 1.10)
        ov0 = .058 + r.uniform(-.016, .018)      # rung ends left proud
        ov1 = .058 + r.uniform(-.016, .018)
        _pole(p, [(a[0] - ov0, a[1] + r.uniform(-.009, .009), a[2] - dz),
                  (b[0] + ov1, b[1] + r.uniform(-.009, .009), b[2] + dz)],
              rr, rr * r.uniform(.86, .98), "oak_pale", sides=6, tint=.09,
              seed=int(z * 1000), knob=.05, shade=1.0 + r.uniform(-.13, .09))
        z += .292 + r.uniform(-.026, .026)
    p.wobble(.008, freq=1.3, respect_seams=False)
    return p.finish()


# ------------------------------------------------------------------- bucket --
def bucket():
    """Staved pail with an iron bail -- on ref2's trestle, by ref1's door."""
    h, rb, rt, n = .285, .114, .146, 11
    p = Part("SM_Prop_Bucket", budget="prop",
             seams=dict(x=(-.22, .22), y=(-.22, .22), z=(0, .50)))
    r = rng("bucket")
    p.lathe([(rb * .90, .014), (rt * .92, h - .02)], "oak_dark", at=(0, 0, 0),
            sides=n, tint=.04, shade=.44)
    for i in range(n):
        a = TAU * (i + .5) / n
        ca, sa = cos(a), sin(a)
        w0 = 2 * rb * sin(pi / n) - .005
        w1 = 2 * rt * sin(pi / n) - .005
        p.beam((ca * rb, sa * rb, 0), (ca * rt, sa * rt, h), w0, .024,
               "oak_mid", bevel=0, tint=.09, up=(ca, sa, 0), taper=w1 / w0,
               shade=1.0 + r.uniform(-.16, .12))
    for zf in (.09, .86):
        rr = lerp(rb, rt, zf)
        chord = 2 * rr * sin(pi / n)
        rh = sqrt((rr + .012) ** 2 + (chord / 2) ** 2) / cos(pi / (n + 3)) + .003
        p.cyl((0, 0, zf * h), rh, .030, "iron", sides=n + 3, cap=False,
              tint=.05, shade=1.0 + r.uniform(-.06, .06))
    # water: 0.030 thick and pushed 0.012 clear of the dark shell's top cap
    # (at 2mm apart the whole water surface -- 500 cm2, the thing you look
    # straight down at -- flickered against it)
    p.cyl((0, 0, h - .023), rt - .014, .030, "stone_dark", sides=n, cap=True,
          tint=.04, shade=.42)
    # The bail is ONE lofted bar, not seven butted beams. Butted, each of its
    # six interior joints opened a V on the OUTSIDE of the arc: a 0.015 section
    # at a 26 deg kink gaps 3.4 mm, nearly a quarter of the bar, and you could
    # see daylight straight through every joint in a close render. Below the
    # z-fight gate's 8 deg coplanarity guard, so it never showed in a number --
    # same defect as the barrel staves, found by looking.
    segs = 7
    rr = rt + .030
    arc = [(cos(pi * i / segs) * rr, h * .80 + sin(pi * i / segs) * .185)
           for i in range(segs + 1)]
    mit = _mitre(arc)
    bw, bt = .015, .015
    rings = [[(bx + sm * mit[k][0] * bt * .5, st * bw * .5,
               bz + sm * mit[k][1] * bt * .5)
              for st, sm in ((-1, -1), (-1, 1), (1, 1), (1, -1))]
             for k, (bx, bz) in enumerate(arc)]
    _loft(p, rings, "iron", tint=.04, shade=1.0)
    p.wobble(.003, freq=3.0, respect_seams=False)
    return p.finish()


# ------------------------------------------------------------------- trough --
def trough():
    """Plank water trough on two stone blocks: heavy boards, iron straps over
    the rim, dark green water, moss at the waterline."""
    L, W = 1.62, .60
    zb, sd = .20, .29                 # stone block height, side board depth
    p = Part("SM_Prop_Trough", budget="prop",
             seams=dict(x=(-L / 2 - .10, L / 2 + .10),
                        y=(-W / 2 - .12, W / 2 + .12), z=(0, zb + sd + .16)))
    r = rng("trough")
    for sx in (-1, 1):
        _pad(p, (sx * .52, 0, 0), (.46, zb, .50), "stone", seed=9 + sx,
             sides=6, irregular=.22, dome=.12, tint=.11,
             shade=.80 + sx * .06, bevel=.024)
    # The floor and side boards are HOUSED BEHIND the end boards, so they stop
    # 0.035 short of the end board's outer face instead of running dead flush
    # with it. Flush was a genuine z-fight the 0.5 mm gate cannot see: measured
    # pointwise, the lower side board's end grain sat 0.08-0.50 mm from the end
    # board's outer face over 25 cm2, four times over, and all of it visible from
    # the end of the trough. The gate misses it because the two face centres are
    # 0.27 m apart and wobble leaves their normals 0.3 deg apart, so projecting
    # one centre onto the other's plane reads 1.45 mm. It also makes the end
    # boards actually stand proud of the sides, which the comment below always
    # claimed and the numbers never delivered.
    Lb = L - .07
    # floor: two boards
    for sy in (-1, 1):
        # ...including the floor, which sat exactly on the stone blocks' crowns
        _bev(p, "box", ((0, sy * W / 4, zb + .032), (Lb, W / 2, .096)),
             "oak_mid", tint=.06, shade=.90 + r.uniform(-.06, .06),
             bevel=.010, seg=1)
    # sides: two boards each, the lower one leaning out a touch
    zc = zb + .080
    # Every board's foot sinks 0.016 into whatever it stands on. Butted exactly
    # -- floor top = side board foot, lower board top = upper board foot,
    # side board top = rim cap foot -- this trough carried the biggest pile of
    # coincident timber in the family: 0.22 m2 of it.
    for sy in (-1, 1):
        for k in range(2):
            bot = zc + (sd / 2) * k - .016
            top = zc + (sd / 2) * (k + 1)
            _bev(p, "box", ((0, sy * (W / 2 - .038 - (1 - k) * .012),
                             (bot + top) / 2), (Lb, .076, top - bot)),
                 "oak_mid", tint=.075, shade=(1.0 + sy * .05) *
                 (1.0 + r.uniform(-.09, .07)), bevel=.010, seg=1)
    # ends: thick boards standing proud of the sides, like a real trough
    for sx in (-1, 1):
        _bev(p, "box", ((sx * (L / 2 - .045), 0, zc + sd / 2 + .012),
                        (.090, W - .10, sd + .056)), "oak_pale", tint=.07,
             shade=.96 + r.uniform(-.07, .07), bevel=.010, seg=1)
    # rim caps on the long sides
    for sy in (-1, 1):
        _bev(p, "box", ((0, sy * (W / 2 - .042), zc + sd + .018),
                        (L - .12, .100, .060)), "oak_pale", tint=.07,
             shade=1.0 + r.uniform(-.06, .06), bevel=.010, seg=1)
    # iron straps wrapping over the rim
    for sx in (-.44, .46):
        for sy in (-1, 1):
            # 0.120 deep, so the strap's cheeks clear the two side boards'
            # faces and the rim cap's instead of landing 3mm off them.
            # It also has to CLEAR THE RIM CAP'S CROWN: at sd+.076 the strap top
            # stood 2.0 mm over the cap top and the two horizontal faces ran
            # parallel across 41 cm2, reachable from directly above. Now the
            # strap is 10 mm proud, which is also what an iron band bent over a
            # timber rim actually looks like.
            p.box((sx, sy * (W / 2 - .036), zc + sd / 2 + .016),
                  (.052, .120, sd + .084), "iron", bevel=0, tint=.04,
                  shade=1.0 + r.uniform(-.06, .06))
        p.box((sx, 0, zb + .085), (.052, W - .09, .022), "iron", bevel=0,
              tint=.04, shade=.96)
    # water, sunk below the rim. Y is W-.20, not W-.19: at .19 the water's own
    # side face ran 1.0 mm from the inner cheek of every iron strap.
    p.box((0, 0, zc + sd - .062), (L - .21, W - .20, .030), "shingle_moss",
          bevel=0, tint=.04, shade=.52)
    _weeds(p, (-.40, -W / 2 - .02, zc + sd - .10), 5, .09, .07, seed=71,
           lean=(48, 96), w=.013)
    _leaves(p, (-.30, -W / 2 - .03, zc + sd - .12), (.30, .02, .05), 16,
            seed=7, size_=.055, droop=.9)
    _leaves(p, (.56, W / 2 + .03, zb * .5), (.10, .02, .09), 10, seed=8,
            size_=.05, droop=.6)
    _weeds(p, (-.58, -W / 2 + .05, .01), 12, .21, .09, seed=73, lean=(8, 54))
    _weeds(p, (.66, W / 2 - .02, .01), 9, .17, .07, seed=74, lean=(8, 60))
    p.wobble(.005, freq=1.8, respect_seams=False)
    return p.finish()


# ----------------------------------------------------------------- greenery --
def _leaf(p, at, d, L, W, mat, shade, fold=.22, tint=.13):
    """One leaf: a non-planar diamond quad (2 tris) so it creases along its
    midrib and catches light on one half only."""
    d = Vector(d).normalized()
    up = Vector((0, 0, 1)) if abs(d.z) < .93 else Vector((0, 1, 0))
    s = d.cross(up).normalized()
    nrm = d.cross(s).normalized()
    a = Vector(at)
    tip = a + d * L
    sh = a + d * (L * .42) - nrm * (W * fold)
    p.quad(tuple(a), tuple(sh + s * (W / 2)), tuple(tip),
           tuple(sh - s * (W / 2)), mat, tint=tint, shade=shade)


def _leaves(p, at, size, n, mat="moss", mat2="shingle_moss", mat3=None, seed=0,
            size_=None, droop=.45, bright=1.34, dark=.60, tint=.13, size2=1.0):
    """A clump of leaves scattered in a box, mostly splaying outward/down."""
    r = rng(f"{p.name}/leaves/{seed}")
    sx, sy, sz = size
    lsz = size_ if size_ is not None else .085
    for i in range(n):
        base = (at[0] + r.uniform(-1, 1) * sx, at[1] + r.uniform(-1, 1) * sy,
                at[2] + r.uniform(-1, 1) * sz)
        a = r.uniform(0, TAU)
        el = lerp(r.uniform(-.15, .95), r.uniform(-1.5, -.35), droop)
        d = (cos(a), sin(a), el)
        q = r.random()
        m = mat if q < .58 else mat2
        if mat3 and q > .93:
            m = mat3
        L = lsz * r.uniform(.7, 1.35) * size2
        _leaf(p, base, d, L, L * .62, m, r.uniform(dark, bright), tint=tint)


def _blade(p, base, h, w, yaw, lean0, lean1, mat, shade, tint=.13, fold=.34):
    """One tapered grass blade, bending further over as it rises. Each segment is
    a folded pair of quads (a shallow V cross-section) so a blade seen edge-on is
    still a blade and not a stray hair."""
    yr = radians(yaw)
    hz = Vector((cos(yr), sin(yr), 0))
    side = Vector((-sin(yr), cos(yr), 0))
    pts, ws = [Vector(base)], [w]
    cur = Vector(base)
    for k, ln in enumerate((h * .55, h * .45)):
        lean = radians(lerp(lean0, lean1, (k + 1) / 2.0))
        cur = cur + (hz * sin(lean) + Vector((0, 0, cos(lean)))) * ln
        pts.append(cur.copy())
        ws.append(w * (.45 if k == 0 else .10))
    for k in range(2):
        a, b = pts[k], pts[k + 1]
        d = (b - a)
        if d.length < 1e-6:
            continue
        nrm = d.normalized().cross(side).normalized()
        wa, wb = ws[k] / 2, ws[k + 1] / 2
        am, bm = a + nrm * (wa * fold * 2), b + nrm * (wb * fold * 2)
        sh2 = shade * .88
        p.quad(tuple(a - side * wa), tuple(am), tuple(bm),
               tuple(b - side * wb), mat, tint=tint, shade=shade)
        p.quad(tuple(am), tuple(a + side * wa), tuple(b + side * wb),
               tuple(bm), mat, tint=tint, shade=sh2)
    return tuple(pts[-1])


def _weeds(p, at, n, h, spread, seed=0, lean=(7, 52), w=.016,
           mats=("moss", "moss", "moss", "moss", "shingle_moss")):
    r = rng(f"{p.name}/weeds/{seed}")
    tips = []
    for i in range(n):
        yaw = r.uniform(0, 360)
        rr = spread * r.uniform(0, 1) ** .65
        ar = radians(yaw)
        base = (at[0] + cos(ar) * rr, at[1] + sin(ar) * rr, at[2])
        m = mats[int(r.random() * len(mats))]
        tips.append(_blade(p, base, h * r.uniform(.62, 1.12),
                           w * r.uniform(.8, 1.25), yaw,
                           r.uniform(lean[0] * .3, lean[0] * 1.7),
                           r.uniform(lean[1] * .70, lean[1] * 1.08), m,
                           shade=r.uniform(.66, 1.10) *
                           (.82 if m == "thatch" else 1.0)))
    return tips


def _daisies(p, at, spread, n, seed=0, z=.03, mat="plaster",
             core="flower_gold", size=.026):
    r = rng(f"{p.name}/daisy/{seed}")
    for i in range(n):
        a = r.uniform(0, TAU)
        rr = spread * r.uniform(.15, 1.0)
        c = (at[0] + cos(a) * rr, at[1] + sin(a) * rr,
             at[2] + z * r.uniform(.4, 1.5))
        s = size * r.uniform(.8, 1.3)
        p.box(c, (s, s, .007), mat, bevel=0, tint=.05,
              rot=(r.uniform(-24, 24), r.uniform(-24, 24), r.uniform(0, 90)),
              shade=r.uniform(.95, 1.2))
        p.box(c, (s * .32, s * .32, .011), core, bevel=0, tint=.06, shade=1.08)


def _florets(p, tip, mat, seed=0, n=4, size=.040):
    r = rng(f"{p.name}/floret/{seed}")
    for k in range(n):
        p.box((tip[0] + r.uniform(-.03, .03), tip[1] + r.uniform(-.03, .03),
               tip[2] + r.uniform(-.05, .01)), (size, size, .016), mat,
              bevel=0, tint=.09, rot=(r.uniform(-35, 35), 0, r.uniform(0, 90)),
              shade=r.uniform(.92, 1.22))


def weed_tuft_a():
    """Small fan of weeds -- tuck one against a plinth or a barrel foot."""
    p = Part("SM_Prop_WeedTuft_A", budget="prop",
             seams=dict(x=(-.36, .36), y=(-.36, .36), z=(0, .48)))
    _pad(p, (0, 0, 0), (.22, .038, .18), "moss", seed=2, sides=7, shade=.70,
         bevel=.010)
    _weeds(p, (0, 0, .012), 46, .27, .10, seed=1, w=.021)
    _leaves(p, (0, 0, .048), (.11, .10, .030), 30, seed=1, size_=.062,
            droop=.80, bright=1.14, dark=.54)
    _daisies(p, (0, 0, .040), .15, 3, seed=1, size=.021)
    return p.finish()


def weed_tuft_b():
    """Bigger flowering clump -- ref2 has these at every wall foot."""
    p = Part("SM_Prop_WeedTuft_B", budget="prop",
             seams=dict(x=(-.50, .50), y=(-.50, .50), z=(0, .70)))
    r = rng("wb")
    _pad(p, (-.02, .01, 0), (.36, .042, .29), "moss", seed=3, sides=8,
         shade=.68, bevel=.010)
    _weeds(p, (-.04, .02, .012), 56, .36, .15, seed=2, lean=(6, 46), w=.022)
    _leaves(p, (.05, -.04, .09), (.16, .14, .055), 44, seed=2, size_=.072,
            bright=1.16, dark=.52)
    _weeds(p, (.06, -.02, .012), 6, .44, .13, seed=5, lean=(4, 26), w=.014,
           mats=("thatch", "thatch", "shingle_moss"))
    _daisies(p, (-.02, 0, .045), .24, 4, seed=2, size=.022)
    for i in range(5):
        a = r.uniform(0, TAU)
        rr = .15 * r.uniform(.2, 1.0)
        tip = _blade(p, (cos(a) * rr, sin(a) * rr, .02),
                     .33 * r.uniform(.7, 1.15), .015, a * 57.3,
                     r.uniform(2, 9), r.uniform(9, 24), "moss",
                     shade=r.uniform(.78, 1.15))
        _florets(p, tip, "flower_gold" if r.random() < .6 else "flower_red",
                 seed=i, n=3, size=.030)
    return p.finish()


def moss_patch():
    """Flat mossy ground patch -- breaks the foot of a wall or a cobble join."""
    W, D = .92, .68
    p = Part("SM_Prop_MossPatch", budget="prop",
             seams=dict(x=(-W / 2 - .05, W / 2 + .05),
                        y=(-D / 2 - .05, D / 2 + .05), z=(0, .32)))
    r = rng("moss_patch")
    for i, (cx, cy, s) in enumerate(((-.25, -.10, 1.0), (.12, .12, .92),
                                     (.31, -.15, .76), (-.07, -.21, .60),
                                     (.02, .19, .66))):
        # each pad a different thickness, rocked, and open underneath: laid
        # identically they stacked five coincident undersides on z = 0 and five
        # coincident crowns on z = 0.024
        _pad(p, (cx, cy, -.005), (.42 * s, .022 + .005 * i, .34 * s), "moss",
             seed=20 + i, sides=7, irregular=.46, dome=.22, tint=.12,
             shade=.66 + r.uniform(-.08, .14), bevel=.008, back=False,
             rock=(r.uniform(-2, 2), r.uniform(-2, 2)))
    _leaves(p, (0, 0, .036), (.37, .27, .016), 96, seed=4, size_=.062,
            droop=1.0, bright=1.14, dark=.52)
    for i in range(6):
        _weeds(p, (r.uniform(-.34, .34), r.uniform(-.24, .24), .010), 9,
               .17, .055, seed=30 + i, lean=(12, 64), w=.019)
    _daisies(p, (0, 0, .042), .33, 7, seed=3, size=.021)
    return p.finish()


def creeper():
    """The vine over ref1's porch beam: a woody runner along the top, a mound of
    leaves sitting on the beam, and separate tendrils of different lengths
    dropping down the front. The runner line -- i.e. the top face of the beam it
    drapes over -- is the TOP of the piece, z = 0.64; tendrils hang to z = 0."""
    G, TOP = S.GRID, .64
    p = Part("SM_Prop_Creeper_2m", budget="prop",
             seams=dict(x=(-G / 2 - .02, G / 2 + .02), y=(-.36, .30),
                        z=(0, TOP + .22)))
    r = rng("creeper")
    n = 8
    pts = [(-G / 2 + G * i / n, .05 + r.uniform(-.07, .07),
            TOP - .025 + r.uniform(-.02, .03)) for i in range(n + 1)]
    for a, b in zip(pts, pts[1:]):
        p.beam(a, b, .032, .028, "oak_dark", bevel=0, tint=.07, shade=.80)
    # the mound of foliage riding the beam
    for i in range(11):
        cx = -G / 2 + G * (i + .5) / 11
        _leaves(p, (cx + r.uniform(-.05, .05), .04, TOP + .050),
                (.105, .09, .060), 19, seed=40 + i, size_=.092,
                droop=.20, mat3="flower_gold", bright=1.40, dark=.52)
    # tendrils: irregular lengths, some long, some barely started
    xs = (-.95, -.79, -.60, -.44, -.24, -.05, .13, .33, .49, .68, .86, .97)
    lns = (.55, .21, .43, .12, .50, .30, .60, .17, .38, .26, .47, .19)
    for i, cx in enumerate(xs):
        ln = lns[i] * (1 + r.uniform(-.12, .12))
        y0 = -.10 + r.uniform(-.06, .05)
        steps = max(2, int(ln / .115))
        for k in range(steps):
            f = k / steps
            z = TOP - .045 - ln * f
            sway = sin(f * 3.1 + i * 1.7) * .055
            p.beam((cx + sway * .55, y0 + sway * .30, z),
                   (cx + sway * .85, y0 + sway * .55, z - ln / steps), .015,
                   .013, "oak_dark", bevel=0, tint=.06, shade=.72)
            _leaves(p, (cx + sway * .7, y0 + sway * .42, z - ln / steps * .5),
                    (.048, .042, .048), 7, seed=60 + i * 9 + k, size_=.082,
                    droop=.85, mat3="flower_gold", bright=1.42, dark=.50)
    p.wobble(.010, freq=1.6)
    return p.finish()


def planter():
    """Clay pot with a mound of flowering greenery spilling over the rim, like
    the potted ones on ref2's sills and trestle."""
    p = Part("SM_Prop_Planter", budget="prop",
             seams=dict(x=(-.36, .36), y=(-.36, .36), z=(0, .60)))
    r = rng("planter")
    prof = [(.0, 0), (.094, 0), (.101, .022), (.129, .130), (.141, .200),
            (.153, .225), (.167, .238), (.164, .262), (.140, .264), (.0, .258)]
    p.lathe(prof, "terracotta", at=(0, 0, 0), sides=12, tint=.06, shade=1.0)
    p.cyl((0, 0, .246), .134, .020, "stone_dark", sides=12, cap=True, tint=.05,
          shade=.40)
    for i in range(8):
        a = TAU * i / 8
        _leaves(p, (cos(a) * .105, sin(a) * .105, .30), (.085, .08, .05), 19,
                seed=80 + i, size_=.088, droop=.35, mat3="flower_gold",
                bright=1.38, dark=.54)
    _leaves(p, (0, 0, .355), (.075, .075, .045), 18, seed=90, size_=.080,
            droop=.05, bright=1.42, dark=.60)
    for i in range(10):
        a = r.uniform(0, TAU)
        rr = r.uniform(.09, .21)
        _florets(p, (cos(a) * rr, sin(a) * rr, .31 + r.uniform(-.05, .09)),
                 "flower_red" if r.random() < .60 else "flower_gold",
                 seed=100 + i, n=3, size=.044)
    # strands spilling over the rim and down the pot
    for i, a in enumerate((0.5, 2.2, 4.4)):
        for k in range(6):
            f = k / 6
            _leaves(p, (cos(a) * (.175 + f * .045), sin(a) * (.175 + f * .045),
                        .27 - f * .225), (.035, .03, .032), 4,
                    seed=120 + i * 6 + k, size_=.072, droop=1.0, bright=1.38,
                    dark=.56)
    return p.finish()


# --------------------------------------------------------------------- build --
def build():
    return [barrel_large_a(), barrel_large_b(), barrel_small_c(),
            barrel_lying_large(), barrel_lying_small(),
            crate_a(), crate_b(), sacks(), ladder(), bucket(), trough(),
            weed_tuft_a(), weed_tuft_b(), moss_patch(), creeper(), planter()]


def demo():
    """A corner of the inn yard, composed as a shot: ladder leaning back on the
    left, the cask stack centre, crates towering right with a pot on top, the
    trough coming forward into the foreground with a vine over its rim, and
    weeds threading through everything."""
    src = {o.name: o for o in bpy.data.objects if o.name.startswith("SM_Prop_")}
    out = []

    def put(nm, loc, rz=0.0, rx=0.0, ry=0.0):
        s = src[nm]
        o = s.copy()
        o.data = s.data
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (radians(rx), radians(ry), radians(rz))
        out.append(o)
        return o

    put("SM_Prop_Ladder", (-1.86, 1.08, 0), rz=-8, rx=-19)
    put("SM_Prop_Barrel_Lying_Large", (-.88, .34, 0), rz=4)
    put("SM_Prop_Barrel_Lying_Large", (-.96, 1.32, 0), rz=-3)
    put("SM_Prop_Barrel_Lying_Small", (-.92, .83, .653), rz=11)
    put("SM_Prop_Barrel_Large_A", (.26, 1.34, 0), rz=14)
    put("SM_Prop_Barrel_Large_B", (1.26, 1.50, 0), rz=-24)
    put("SM_Prop_Barrel_Small_C", (1.02, .60, 0), rz=20)
    put("SM_Prop_Crate_A", (2.14, 1.06, 0), rz=-16)
    put("SM_Prop_Crate_B", (2.10, 1.10, .565), rz=9)
    put("SM_Prop_Planter", (2.06, 1.06, .985))
    put("SM_Prop_Sacks", (-1.46, -.34, 0), rz=26)
    put("SM_Prop_Bucket", (.54, .06, 0), rz=34)
    put("SM_Prop_Trough", (.42, -1.12, 0), rz=8)
    put("SM_Prop_Creeper_2m", (.42, -1.42, 0), rz=8)
    put("SM_Prop_MossPatch", (.66, .74, 0), rz=18)
    put("SM_Prop_MossPatch", (-1.92, -1.02, 0), rz=-40)
    put("SM_Prop_WeedTuft_B", (1.66, .20, 0), rz=30)
    put("SM_Prop_WeedTuft_A", (2.52, .54, 0), rz=-20)
    put("SM_Prop_WeedTuft_A", (-2.06, .60, 0), rz=50)
    put("SM_Prop_WeedTuft_B", (-.32, .40, 0), rz=-70)
    put("SM_Prop_WeedTuft_A", (.90, 1.88, 0), rz=120)
    for nm in src:
        src[nm].location = (0, 40, 0)
    return out
