"""
Geometry toolkit. EVERY piece in the kit is built with this. Read this header
before building anything; it is the whole API you need.

    from kit.util import Part, rng, lerp
    from kit import spec as S

    def build():
        p = Part("SM_Wall_StoneRubble_2m_A", budget="wall",
                 seams=dict(x=(-S.GRID/2, S.GRID/2), y=(0, S.T_STONE), z=(0, S.H_GROUND)))
        p.box((0, S.T_STONE/2, 1.5), (S.GRID, S.T_STONE, 3.0), "stone_dark", bevel=0.02)
        p.stones((-1, 1), (0, 3.0), y=0.0, depth=0.10, mat="stone")
        return p.finish()

`seams` declares the piece's snap bounds. Two things use it:
  * hand-made wobble fades to zero near those planes, so tiled copies never crack;
  * p.finish() validates that no geometry escapes them (PROUD_MAX slack outward).

Colour: every primitive takes `tint` (default 0.05) = amount of per-primitive
value/hue jitter written into the "Col" vertex-colour layer. The material
multiplies by it. Small numbers (.03-.10) read as natural material variation;
larger (.15+) reads as deliberately mismatched stones/shingles.

Coordinates: metres. +Z up. For wall-family pieces the OUTER FACE IS Y=0 and
the body runs to +Y. "Outward" is therefore -Y.
"""
import bpy, bmesh, hashlib, math
from math import pi, sin, cos, radians, sqrt, atan2
from mathutils import Vector, Matrix, Euler, noise
from . import spec as S
from . import mats as M

TAU = 2 * pi


# ------------------------------------------------------------------ helpers --
def rng(seed):
    """Deterministic RNG from any string/int. Same seed -> same asset, always."""
    import random
    h = hashlib.md5(str(seed).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else hi if v > hi else v


def smoothstep(e0, e1, x):
    t = clamp((x - e0) / (e1 - e0) if e1 != e0 else 1.0)
    return t * t * (3 - 2 * t)


def _euler(rot):
    if rot is None:
        return Matrix.Identity(4)
    if isinstance(rot, Matrix):
        return rot
    return Euler([radians(a) for a in rot], 'XYZ').to_matrix().to_4x4()


def slope_matrix(extra_deg=0.0):
    """Rotation that lays a flat XY object onto the kit's roof slope."""
    return Matrix.Rotation(S.PITCH + radians(extra_deg), 4, 'X')


# --------------------------------------------------------------------- Part --
class Part:
    """One kit piece under construction. Accumulates primitives into one bmesh,
    then finish() bakes it into a single game-ready mesh object."""

    def __init__(self, name, budget=None, seams=None, smooth=True, proud=None,
                 outward="y"):
        self.name = name
        self.budget = budget
        self.seams = seams or {}
        # How far this piece may stand proud of its outer plane. Defaults to
        # spec.PROUD_MAX; a chunky corner post head legitimately needs more, so a
        # piece can declare its own allowance and still be validated against it.
        self.proud = proud
        # Which axes this piece legitimately faces OUTWARD on, i.e. where relief may
        # stand proud of the lower bound. A wall faces out on -y only; its x planes
        # are TILING seams and must be cut dead flat on BOTH sides or a wall run
        # shows a lump at one edge and a razor cut at the next. An outside corner
        # faces out on two sides, so corner pieces pass outward="xy".
        self.outward = outward
        self.smooth = smooth
        self.bm = bmesh.new()
        self.clay = self.bm.loops.layers.float_color.new("Col")
        self._mats = []          # material name -> slot order
        self._rng = rng(name)

    # ---- internals ----------------------------------------------------------
    def _mi(self, mat):
        if mat not in self._mats:
            self._mats.append(mat)
        return self._mats.index(mat)

    def _paint(self, faces, mat, tint, shade=1.0):
        """Write per-primitive jittered colour into the Col layer."""
        mi = self._mi(mat)
        r = self._rng
        j = 1.0 + r.uniform(-tint, tint)
        warm = 1.0 + r.uniform(-tint, tint) * 0.55
        col = (clamp(j * shade * 1.0, 0, 4), clamp(j * shade * warm, 0, 4),
               clamp(j * shade * (2 - warm), 0, 4), 1.0)
        for f in faces:
            f.material_index = mi
            f.smooth = self.smooth
            for l in f.loops:
                l[self.clay] = col
        return faces

    def _emit(self, verts, faces_idx, mat, tint, bevel, seg, shade=1.0):
        """Build a primitive from vert positions + face index tuples.

        NOTE on bevelling: bmesh.ops.bevel REPLACES the faces it touches, so the
        BMFace objects we created become invalid and only the new bevel strips come
        back in res["faces"]. Collecting faces by identity therefore loses the
        primitive's own six sides -- they keep material slot 0 and no vertex colour.
        So we snapshot the bmesh's faces first and take the difference afterwards,
        which is correct whether or not we bevel.
        """
        before = set(self.bm.faces)
        bvs = [self.bm.verts.new(v) for v in verts]
        for idx in faces_idx:
            try:
                self.bm.faces.new([bvs[i] for i in idx])
            except ValueError:
                pass   # duplicate face, skip
        self.bm.normal_update()
        if bevel:
            # DETERMINISM: this used to build `geom` as a Python set. Sets of BMesh
            # elements iterate in memory-address order, so bevel received its input
            # in a different order on every run and vertices landed up to ~1mm
            # apart between builds of identical code. That broke the kit's
            # "same code, same mesh" guarantee and made measurements unrepeatable
            # (the same module measured 44981 / 42945 / 29104 cm2 of coincident
            # surface on three runs). Collect in creation order with a seen-set for
            # de-duplication instead, so the input order is stable.
            geom, seen = [], set()
            for f in self.bm.faces:
                if f in before:
                    continue
                for seq in (f.edges, f.verts):
                    for el in seq:
                        k = (el.__class__.__name__, id(el))
                        if k not in seen:
                            seen.add(k)
                            geom.append(el)
            bmesh.ops.bevel(self.bm, geom=geom, offset=bevel,
                            segments=seg or S.BEVEL_SEG, affect='EDGES',
                            profile=0.5, clamp_overlap=True, miter_outer='ARC')
        fs = [f for f in self.bm.faces if f.is_valid and f not in before]
        self._paint(fs, mat, tint, shade)
        return fs

    # ---- primitives ---------------------------------------------------------
    def box(self, center, size, mat, bevel=None, seg=None, tint=0.05, rot=None,
            taper=1.0, taper_axis='X', shade=1.0, skew=(0, 0)):
        """Axis-aligned (or rotated) box. `taper` scales the +Z face; `skew`
        shifts the +Z face in (x, y) -- both give hand-built lean."""
        cx, cy, cz = center
        sx, sy, sz = (size[0] / 2, size[1] / 2, size[2] / 2)
        tx = sx * taper if taper_axis in ('X', 'XY') else sx
        ty = sy * taper if taper_axis in ('Y', 'XY') else sy
        kx, ky = skew
        vs = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
              (-tx + kx, -ty + ky, sz), (tx + kx, -ty + ky, sz),
              (tx + kx, ty + ky, sz), (-tx + kx, ty + ky, sz)]
        mtx = _euler(rot)
        vs = [tuple(mtx @ Vector(v) + Vector((cx, cy, cz))) for v in vs]
        F = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2),
             (2, 6, 7, 3), (3, 7, 4, 0)]
        b = S.BEVEL_W if bevel is None else bevel
        return self._emit(vs, F, mat, tint, b, seg, shade)


    def blob(self, center, size, mat, sides=7, axis='Y', irregular=0.30, dome=0.35,
             bevel=0.012, seg=1, tint=0.07, rot=None, shade=1.0, seed=0, back=True):
        """Irregular cushion solid -- a STONE. Not a box: the outline is a
        jittered polygon and the face bulges forward in two steps, so it reads
        as a rounded boulder and still shades cleanly. This is what makes rubble
        look like rubble instead of tiles glued to a wall.
        `axis` = facing normal ('Y' for wall pieces; the stone bulges toward -Y).
        size = (width, depth, height).
        """
        r = rng(f"{self.name}/blob/{seed}/{center[0]:.3f}{center[2]:.3f}")
        w, d, h = size[0] / 2, size[1], size[2] / 2
        jit = [1.0 + r.uniform(-irregular, irregular) for _ in range(sides)]
        def ring(depth_frac, scale):
            out = []
            for i in range(sides):
                a_ = TAU * (i + 0.5) / sides
                u = clamp(cos(a_) * w * jit[i], -w, w) * scale
                v = clamp(sin(a_) * h * jit[i], -h, h) * scale
                out.append((u, -d * depth_frac, v))
            return out
        r0 = ring(0.0, 1.0)                       # flat back, in the wall plane
        r1 = ring(0.42, 1.03)                     # shoulder, bulging slightly
        r2 = ring(1.0, 1.0 - 0.40 * dome)         # proud face, drawn in
        n = sides
        vs = r0 + r1 + r2
        F = []
        for i in range(n):
            j = (i + 1) % n
            F.append((i, j, j + n, i + n))                    # flank
            F.append((i + n, j + n, j + 2 * n, i + 2 * n))    # shoulder roll
        F.append(tuple(range(2 * n, 3 * n)))                  # proud face
        if back:
            F.append(tuple(range(n))[::-1])
        if axis == 'X':
            vs = [(v[1], v[0], v[2]) for v in vs]
        elif axis == 'Z':
            vs = [(v[0], v[2], v[1]) for v in vs]
        mtx = _euler(rot)
        vs = [tuple(mtx @ Vector(v) + Vector(center)) for v in vs]
        return self._emit(vs, F, mat, tint, bevel, seg, shade)

    def plate(self, center, size, mat, tint=0.05, rot=None, shade=1.0):
        """Cheap un-beveled box for panels/planes hidden behind other geo."""
        return self.box(center, size, mat, bevel=0, tint=tint, rot=rot, shade=shade)

    def beam(self, p0, p1, w, h, mat, bevel=None, seg=None, tint=0.05,
             up=(0, 0, 1), extend=0.0, taper=1.0, shade=1.0):
        """Timber of cross-section w x h running from p0 to p1. `extend` lengthens
        both ends (use it to bury a beam into whatever it joins)."""
        a, b = Vector(p0), Vector(p1)
        d = b - a
        L = d.length
        if L < 1e-6:
            return []
        z = d.normalized()
        u = Vector(up)
        if abs(z.dot(u.normalized())) > 0.999:
            u = Vector((0, 1, 0))
        x = z.cross(u).normalized()
        y = z.cross(x).normalized()
        mtx = Matrix((x, y, z)).transposed().to_4x4()
        mtx.translation = (a + b) / 2
        sx, sy, sz = w / 2, h / 2, L / 2 + extend
        tx, ty = sx * taper, sy * taper
        vs = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
              (-tx, -ty, sz), (tx, -ty, sz), (tx, ty, sz), (-tx, ty, sz)]
        vs = [tuple(mtx @ Vector(v)) for v in vs]
        F = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2),
             (2, 6, 7, 3), (3, 7, 4, 0)]
        bv = S.BEVEL_W if bevel is None else bevel
        return self._emit(vs, F, mat, tint, bv, seg, shade)

    def prism(self, verts2d, thickness, mat, axis='Y', at=(0, 0, 0), bevel=None,
              seg=None, tint=0.05, rot=None, shade=1.0):
        """Extrude a 2D polygon (list of (u,v), CCW) by `thickness` along `axis`.
        The workhorse for gable triangles, brackets, corbels, arch spandrels."""
        n = len(verts2d)
        half = thickness / 2
        if axis == 'Y':
            f = lambda u, v, s: (u, s, v)
        elif axis == 'X':
            f = lambda u, v, s: (s, u, v)
        else:
            f = lambda u, v, s: (u, v, s)
        vs = [f(u, v, -half) for (u, v) in verts2d] + [f(u, v, half) for (u, v) in verts2d]
        mtx = _euler(rot)
        vs = [tuple(mtx @ Vector(v) + Vector(at)) for v in vs]
        F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
        for i in range(n):
            j = (i + 1) % n
            F.append((i, j, j + n, i + n))
        b = S.BEVEL_W if bevel is None else bevel
        return self._emit(vs, F, mat, tint, b, seg, shade)

    def cyl(self, center, r, h, mat, sides=10, axis='Z', bevel=None, seg=None,
            tint=0.05, rot=None, r_top=None, cap=True, shade=1.0, phase=0.0):
        """Low-poly cylinder / truncated cone. Posts, barrels, pots, chimney pots."""
        rt = r if r_top is None else r_top
        ring0, ring1 = [], []
        for i in range(sides):
            a = TAU * (i / sides) + phase
            ring0.append((r * cos(a), r * sin(a), -h / 2))
            ring1.append((rt * cos(a), rt * sin(a), h / 2))
        if axis == 'Y':
            sw = lambda v: (v[0], v[2], v[1])
        elif axis == 'X':
            sw = lambda v: (v[2], v[1], v[0])
        else:
            sw = lambda v: v
        vs = [sw(v) for v in ring0 + ring1]
        mtx = _euler(rot)
        vs = [tuple(mtx @ Vector(v) + Vector(center)) for v in vs]
        F = []
        for i in range(sides):
            j = (i + 1) % sides
            F.append((i, j, j + sides, i + sides))
        if cap:
            F.append(tuple(range(sides))[::-1])
            F.append(tuple(range(sides, 2 * sides)))
        b = 0 if bevel is None else bevel
        return self._emit(vs, F, mat, tint, b, seg, shade)

    def lathe(self, profile, mat, at=(0, 0, 0), sides=12, axis='Z', tint=0.05,
              rot=None, shade=1.0, close=True):
        """Revolve a 2D profile [(radius, height), ...] around the axis.
        Barrels, buckets, flower pots, lantern bodies, chimney pots, well rims."""
        n = len(profile)
        vs, F = [], []
        for i in range(sides):
            a = TAU * i / sides
            for (r, hh) in profile:
                v = (r * cos(a), r * sin(a), hh)
                if axis == 'Y':
                    v = (v[0], v[2], v[1])
                elif axis == 'X':
                    v = (v[2], v[1], v[0])
                vs.append(v)
        for i in range(sides):
            j = (i + 1) % sides
            for k in range(n - 1):
                F.append((i * n + k, j * n + k, j * n + k + 1, i * n + k + 1))
        if close:
            F.append(tuple(i * n for i in range(sides))[::-1])
            F.append(tuple(i * n + (n - 1) for i in range(sides)))
        mtx = _euler(rot)
        vs = [tuple(mtx @ Vector(v) + Vector(at)) for v in vs]
        return self._emit(vs, F, mat, tint, 0, None, shade)

    def quad(self, a, b, c, d, mat, tint=0.05, shade=1.0):
        """One free quad from four points. Leaf cards, banners, flat trim."""
        return self._emit([a, b, c, d], [(0, 1, 2, 3)], mat, tint, 0, None, shade)

    # ---- compound generators ------------------------------------------------
    def planks(self, u_range, v_range, at_w, n, mat, axis='Y', thick=0.05,
               gap=0.008, bevel=0.012, tint=0.06, seed=0, jitter=0.35, rot=None,
               at=(0, 0, 0)):
        """A run of boards -- doors, shutters, siding, floors, fences, cart beds.
        Boards run along `v`, are divided across `u`. `at_w` is the offset on the
        third axis. Each board gets its own tint and a little depth jitter."""
        r = rng(f"{self.name}/planks/{seed}")
        u0, u1 = u_range
        v0, v1 = v_range
        w = (u1 - u0) / n
        out = []
        for i in range(n):
            cu = u0 + w * (i + 0.5)
            cv = (v0 + v1) / 2
            d = thick * (1 + r.uniform(-jitter, jitter) * 0.5)
            if axis == 'Y':
                c, s = (cu, at_w + d / 2, cv), (w - gap, d, v1 - v0)
            elif axis == 'X':
                c, s = (at_w + d / 2, cu, cv), (d, w - gap, v1 - v0)
            else:
                c, s = (cu, cv, at_w + d / 2), (w - gap, v1 - v0, d)
            c = tuple(a + b for a, b in zip(c, at))
            out += self.box(c, s, mat, bevel=bevel, tint=tint, rot=rot,
                            shade=1.0 + r.uniform(-.06, .06))
        return out

    def stones(self, u_range, v_range, y, depth, mat, course=0.34, axis='Y',
               tint=0.13, seed=0, mortar=0.022, wobble=0.22, r_bevel=0.045,
               mat_alt=None, at=(0, 0, 0), big=0.18, chink=0.30, irregular=0.30,
               dome=0.40, shade_var=0.20, overfill=1.07, mat_warm=None):
        """Chunky rubble/ashlar facing -- the ground-floor look in both refs.
        Fills the u x v rect with irregular stones standing `depth` proud of the
        plane at `y` (growing -Y, i.e. outward, for wall pieces). Put a dark
        backing box behind it; the gaps between stones ARE the mortar.

        `big`   fraction of stones promoted to double-width boulders
        `chink` chance of a small packing stone dropped into a joint
        Coursing is preserved (that is what makes it read as a built wall) but
        widths, shapes and depths vary hard.
        """
        r = rng(f"{self.name}/stones/{seed}")
        u0, u1 = u_range
        v0, v1 = v_range
        rows = max(1, int(round((v1 - v0) / course)))
        ch = (v1 - v0) / rows
        out = []
        for ri in range(rows):
            cv = v0 + ch * (ri + 0.5)
            # walk the course laying stones of varied width
            u = u0
            guard = 0
            while u < u1 - 0.04 and guard < 40:
                guard += 1
                base = course * r.uniform(0.85, 1.7)
                if r.random() < big:
                    base *= r.uniform(1.5, 2.1)
                w = min(base, u1 - u)
                if u1 - (u + w) < course * 0.45:      # avoid a sliver at the end
                    w = u1 - u
                cu = u + w / 2
                sw = max((w - mortar) * overfill, 0.05)
                sh = max((ch - mortar) * overfill - r.uniform(0, ch * .12 * wobble), 0.05)
                dd = depth * (1 + r.uniform(-.35, .30) * wobble)
                m = mat
                q = r.random()
                if mat_alt and q > .74:
                    m = mat_alt
                elif mat_warm and q < .16:
                    m = mat_warm
                tilt = r.uniform(-1, 1) * 2.6 * wobble
                if axis == 'Y':
                    c = (cu + r.uniform(-1, 1) * .008, y, cv + r.uniform(-1, 1) * .014)
                    sz = (sw, dd, sh)
                    rt = (tilt, 0, r.uniform(-1, 1) * 1.2 * wobble)
                else:
                    c = (y, cu + r.uniform(-1, 1) * .008, cv)
                    sz = (dd, sw, sh)
                    rt = (0, tilt, 0)
                c = tuple(x + o for x, o in zip(c, at))
                out += self.blob(c, sz, m, sides=6 if sw < course * .8 else 7,
                                 axis=axis, irregular=irregular * r.uniform(.7, 1.3),
                                 dome=dome * r.uniform(.6, 1.25),
                                 bevel=min(r_bevel * .45, sh * .18, sw * .18),
                                 seg=1, tint=tint, rot=rt, seed=seed * 97 + guard,
                                 shade=1.0 + r.uniform(-shade_var, shade_var))
                # pack a small chinking stone into the joint above
                if r.random() < chink and w > course * .9:
                    cw = w * r.uniform(.22, .38)
                    cz = cv + sh / 2 * r.choice((-1, 1)) * .85
                    if v0 < cz < v1:
                        cc = (cu + r.uniform(-1, 1) * w * .25, y, cz)
                        cc = tuple(x + o for x, o in zip(cc, at))
                        out += self.blob(cc, (cw, dd * .8, ch * r.uniform(.22, .34)), m,
                                         sides=6, axis=axis, irregular=.4, dome=.5,
                                         bevel=.008, seg=1, tint=tint,
                                         seed=seed * 131 + guard,
                                         shade=1.0 + r.uniform(-shade_var, shade_var))
                u += w
        return out

    def shingles(self, width, n_rows, mat, at=(0, 0, 0), rot=None, row=0.20,
                 tab=0.16, thick=0.035, tint=0.09, seed=0, jitter=0.5,
                 overhang=1.55, mat_alt=None):
        """Rows of wood shingles on a flat XY patch (build flat, then rot onto
        the slope with util.slope_matrix()). Rows run along X and climb +Y.
        `overhang` = each row's exposure multiplier vs `row` so rows overlap.
        This is the single most important texture in the kit -- both refs read
        as 'shingle roof' from silhouette + row rhythm alone."""
        r = rng(f"{self.name}/shingles/{seed}")
        out = []
        for ri in range(n_rows):
            v = ri * row
            n = max(1, int(round(width / tab)))
            tw = width / n
            off = (ri % 2) * tw * 0.5 + r.uniform(-1, 1) * tw * .08 * jitter
            for i in range(n + 1):
                cu = -width / 2 + tw * (i + 0.5) - off
                if cu - tw / 2 < -width / 2 - tw * .6 or cu + tw / 2 > width / 2 + tw * .6:
                    continue
                cu = clamp(cu, -width / 2 + tw * .12, width / 2 - tw * .12)
                h = row * overhang * (1 + r.uniform(-.07, .05) * jitter)
                lift = r.uniform(0, thick * 1.1) * jitter
                m = mat if (mat_alt is None or r.random() > .18) else mat_alt
                c = (cu, v + h / 2 - row * (overhang - 1) * .5, thick / 2 + lift)
                out += self.box(tuple(a + b for a, b in zip(c, at)),
                                (tw - .012, h, thick), m, bevel=.010, seg=1,
                                tint=tint, rot=rot,
                                skew=(r.uniform(-1, 1) * .012 * jitter, 0),
                                shade=1.0 + r.uniform(-.13, .10))
        return out

    def dentil(self, u_range, v, w_axis, mat, n=None, step=0.16, size=(0.06, 0.10, 0.055),
               at=(0, 0, 0), tint=0.05, rot=None, seed=0):
        """The little repeating tooth-blocks under ref 2's bargeboards and eaves.
        Cheap, and it is most of what makes that roofline read as 'crafted'."""
        r = rng(f"{self.name}/dentil/{seed}")
        u0, u1 = u_range
        n = n or max(1, int(round((u1 - u0) / step)))
        out = []
        for i in range(n):
            cu = lerp(u0, u1, (i + 0.5) / n)
            c = (cu, w_axis, v)
            c = tuple(a + b for a, b in zip(c, at))
            out += self.box(c, size, mat, bevel=.008, seg=1, tint=tint, rot=rot,
                            shade=1.0 + r.uniform(-.07, .07))
        return out

    def arch(self, center, r_out, depth, mat, thickness=0.22, segs=9, axis='Y',
             tint=0.07, span=180.0, start=0.0, tint_seed=0, bevel=0.02,
             wedge_gap=0.012):
        """Voussoir arch ring built from individual wedge stones -- the arched
        doorways and windows in both refs. `center` is the arch's spring centre."""
        r = rng(f"{self.name}/arch/{tint_seed}")
        out = []
        a0 = radians(start)
        a1 = a0 + radians(span)
        for i in range(segs):
            m0 = lerp(a0, a1, i / segs)
            m1 = lerp(a0, a1, (i + 1) / segs)
            mm = (m0 + m1) / 2
            ri, ro = r_out - thickness, r_out
            g = wedge_gap
            p = [(ri * cos(m0 + g), ri * sin(m0 + g)), (ro * cos(m0 + g), ro * sin(m0 + g)),
                 (ro * cos(m1 - g), ro * sin(m1 - g)), (ri * cos(m1 - g), ri * sin(m1 - g))]
            out += self.prism(p, depth, mat, axis=axis, at=center, bevel=bevel, seg=2,
                              tint=tint, shade=1.0 + r.uniform(-.08, .08))
        return out

    def leafy(self, at, size, mat, n=14, mat_alt=None, seed=0, card=0.20, droop=0.5):
        """Cheap foliage clump from crossed cards -- creepers, moss tufts, window
        boxes, weeds at the plinth. Both refs lean on these to soften edges."""
        r = rng(f"{self.name}/leafy/{seed}")
        out = []
        sx, sy, sz = size
        for i in range(n):
            px = at[0] + r.uniform(-1, 1) * sx / 2
            py = at[1] + r.uniform(-1, 1) * sy / 2
            pz = at[2] + r.uniform(-1, 1) * sz / 2
            c = card * r.uniform(.6, 1.25)
            yaw = r.uniform(0, 180)
            pitch = r.uniform(-30, 30) - droop * 30
            m = mat if (mat_alt is None or r.random() > .3) else mat_alt
            out += self.box((px, py, pz), (c, c * .12, c * .75), m, bevel=0,
                            rot=(pitch, 0, yaw), tint=.14,
                            shade=1.0 + r.uniform(-.22, .16))
        return out


    def glazing(self, center, size, depth=0.06, frame=0.055, rebate=0.020,
                lead=0.015, cell=0.17, pattern="diamond", overlap=0.012,
                mat_frame="oak_dark", mat_glass="glass", mat_lead="iron",
                tint=0.04, rot=None, mullions=0, transoms=0):
        """A COMPLETE glazed opening: frame, glass and leading in one call.

        Built so the three faults that kept recurring across five families cannot
        happen by construction:

        1. THE GLASS ALWAYS FILLS ITS OPENING. The pane is cut OVERSIZE -- the full
           opening plus `rebate` on every side -- and the frame laps over its edge.
           A pane sized to the visible aperture leaves a hairline of background
           showing at any grazing angle; an oversize pane cannot.
        2. THE LEADING ALWAYS REACHES THE FRAME, AND STOPS THERE. Diagonals are
           generated across the WHOLE opening and clipped to the frame's own inner
           faces, so every diamond meets the edge as a partial diamond -- which is
           what real leaded glazing does. Generating them inside an inset rectangle
           left them floating in mid-pane; clipping them to the OVERSIZE PANE ran
           them out under the frame into the host's own boarding, which made one
           z-fight class a function of `lead` rather than of construction.
        3. NO GAP BETWEEN FRAME AND SURROUNDING WALL. The frame's outer edge oversails
           the opening by `overlap`, so it laps onto the plaster/masonry around it
           instead of butting to it. A butt joint opens into a visible line as soon as
           anything wobbles.

        It also keeps the leading `lead` clear of the glass plane, so the bars and the
        pane are never coplanar -- that coincidence was measured at 300 face pairs on
        one casement and read as flicker in the pattern.

        center  centre of the opening; the glazing faces -Y (outward), like walls
        size    (width, height) of the OPENING
        depth   how far back from Y=0 the glass sits
        frame   face width of the frame members
        cell    diamond pitch; pattern "diamond" | "square" | "none"
        mullions/transoms  extra vertical/horizontal bars across the opening
        """
        w, h = size[0], size[1]
        cx, cy, cz = center
        hw, hh = w / 2.0, h / 2.0
        out = []

        # ---- glass: OVERSIZE by the rebate, so the frame laps its edge ----------
        gw, gh = w + 2 * rebate, h + 2 * rebate
        out += self.box((cx, cy + depth, cz), (gw, 0.012, gh), mat_glass,
                        bevel=0, tint=0.0, rot=rot)

        # ---- leading: clipped to the FRAME'S INNER OPENING, not to the pane ----
        # The pane is deliberately oversize (rebate), and the frame oversails the
        # opening (overlap), so clipping the cames to the PANE ran every came
        # rebate+overlap past the visible aperture -- out under the frame and into
        # whatever the host piece has there. On a boarded door that is the boards,
        # whose back faces `wobble` spreads across exactly the band the cames
        # occupy, so whether a came's back plane landed on a board's back plane was
        # decided by the value of `lead`: measured 0.0 cm2 at 0.015, 3.1 cm2 at
        # 0.023, 7.2 cm2 at 0.045. That is luck, not construction.
        # The cames now stop at the frame's inner faces (+ a 4 mm tuck so the end
        # grain is hidden under the frame instead of ending in open air), which is
        # also where real leaded glazing stops: at the rebate, not past it.
        # The tuck is a FRACTION of the frame's lap, not an absolute: signage
        # builds its lantern glazing at LANT_S = 5, where a flat 4 mm tuck is
        # 1/12 of what it should be and pushed that piece over its tri budget.
        tuck = 0.35 * overlap
        cw, ch = w - overlap + 2 * tuck, h - overlap + 2 * tuck
        if pattern != "none" and cell > 1e-4:
            zb = cy + depth - lead              # strictly in FRONT of the pane
            def clip_line(a, b, c):
                """Clip a*u + b*v = c to the came rect; return the two endpoints."""
                pts = []
                if abs(b) > 1e-9:
                    for u in (-cw / 2, cw / 2):
                        v = (c - a * u) / b
                        if -ch / 2 - 1e-9 <= v <= ch / 2 + 1e-9:
                            pts.append((u, v))
                if abs(a) > 1e-9:
                    for v in (-ch / 2, ch / 2):
                        u = (c - b * v) / a
                        if -cw / 2 - 1e-9 <= u <= cw / 2 + 1e-9:
                            pts.append((u, v))
                # de-duplicate corner hits
                uniq = []
                for p in pts:
                    if not any(abs(p[0] - q[0]) < 1e-6 and abs(p[1] - q[1]) < 1e-6
                               for q in uniq):
                        uniq.append(p)
                return uniq[:2] if len(uniq) >= 2 else None

            step = cell * (2 ** 0.5) if pattern == "diamond" else cell
            reach = (cw + ch)
            dirs = ((1.0, 1.0), (1.0, -1.0)) if pattern == "diamond" else ((1.0, 0.0), (0.0, 1.0))
            # ANCHOR THE GRID ON THE CENTRE LINE (k = 0), not on -reach.
            # Starting at -reach makes every bar's POSITION a function of `reach`,
            # i.e. of the clip rectangle -- so changing the rectangle by 160 mm
            # reshuffled the whole pattern and took one lantern from 4 bars to 6
            # while the rectangle got SMALLER. The count stopped being monotonic in
            # the opening size, and this family's own comment ("cell is chosen so
            # one bar lands on the centre line") was true only by coincidence.
            # Enumerating m * step outward from zero makes it true by construction
            # and makes the pattern symmetric about both axes.
            for m in range(-(int(reach / step) + 1), int(reach / step) + 2):
                k = m * step
                for (a, b) in dirs:
                    seg = clip_line(a, b, k)
                    if seg:
                        (u0, v0), (u1, v1) = seg
                        if (u1 - u0) ** 2 + (v1 - v0) ** 2 > 1e-6:
                            out += self.beam((cx + u0, zb, cz + v0),
                                             (cx + u1, zb, cz + v1),
                                             lead * 0.9, lead * 0.9, mat_lead,
                                             bevel=0, tint=tint)

        # ---- mullions and transoms, in front of the leading --------------------
        for i in range(mullions):
            u = -hw + w * (i + 1) / (mullions + 1)
            out += self.box((cx + u, cy + depth - lead * 2.2, cz),
                            (frame * 0.8, 0.030, ch), mat_frame,
                            bevel=0.006, tint=tint, rot=rot)
        for i in range(transoms):
            v = -hh + h * (i + 1) / (transoms + 1)
            out += self.box((cx, cy + depth - lead * 2.2, cz + v),
                            (cw, 0.030, frame * 0.8), mat_frame,
                            bevel=0.006, tint=tint, rot=rot)

        # ---- frame: laps the glass edge AND oversails onto the wall around it ---
        fo = frame + overlap                   # how far the frame reaches outward
        fd = 0.055                             # frame thickness in Y
        yf = cy + depth - lead * 2.6 - fd / 2
        for (bx, bz, bw, bh) in (
                (0.0, hh + fo / 2 - overlap / 2, w + 2 * fo, fo),      # head
                (0.0, -hh - fo / 2 + overlap / 2, w + 2 * fo, fo),     # sill
                # JAMBS FIT BETWEEN HEAD AND SILL -- height h - overlap, not
                # h + 2*fo. At full height they ran THROUGH the head and the sill,
                # leaving an fo x fo square of doubled solid at all four corners with
                # coplanar front faces: a z-fighting corner lap on every glazed opening
                # in the kit, since five families call this primitive. The gables
                # auditor traced its family's entire residual to exactly this and noted
                # it "cannot be fixed inside a piece module" -- correct, it is here.
                # Head and sill now run through; the jambs butt between them, which is
                # also how the joint is actually made.
                #
                # EXPECTED, DO NOT CHASE: a butt joint between two solids has
                # coincident faces BY DEFINITION. The jamb's end face lands exactly
                # on the head's underside (z = +/-(h - overlap)/2) and on the sill's
                # top face -- (fo - 2*bevel)^2 ~ 24.6 cm2 per corner, ~341 cm2 over
                # a family, and it is 0.00 ray-reachable on every piece because it
                # is inside solid timber. Two auditors on two different families
                # each traced this from scratch and each concluded it "cannot be
                # fixed inside a piece module"; both were right, and there is
                # nothing here to fix. Shortening the jamb would open a slot at
                # every frame corner to remove coincidence nothing can see.
                # If your z-fight report shows this plane, it is construction.
                (-hw - fo / 2 + overlap / 2, 0.0, fo, h - overlap),     # left jamb
                (hw + fo / 2 - overlap / 2, 0.0, fo, h - overlap)):     # right jamb
            out += self.box((cx + bx, yf, cz + bz), (bw, fd, bh), mat_frame,
                            bevel=0.008, tint=tint, rot=rot)
        return out

    # ---- deformation --------------------------------------------------------
    def _seam_fade(self, v, axes="xz", margin=0.16):
        """1.0 deep inside the piece, 0.0 on the snap planes named in `axes`.

        Only fade on axes that actually TILE. For a wall that is x (bay to bay) and
        z (storey to storey). y is the OUTER FACE -- the visible timber frame lives
        there, and fading it meant the entire visible surface of the kit got no
        hand-hewn irregularity at all. Corner pieces, which abut walls on two sides,
        should pass axes="xyz".
        """
        f = 1.0
        for ax, i in (('x', 0), ('y', 1), ('z', 2)):
            if ax in axes and ax in self.seams:
                lo, hi = self.seams[ax]
                f = min(f, smoothstep(0, margin, v[i] - lo),
                        smoothstep(0, margin, hi - v[i]))
        return clamp(f)

    def wobble(self, amount=None, freq=1.7, respect_seams=True, axes="xz",
               margin=0.16):
        """Coherent hand-made irregularity. Smooth position noise, so adjacent
        primitives move together (no cracks), faded out only at the planes that
        have to stay flat for the kit to snap -- by default x (bay tiling) and
        z (storey stacking), NOT y, which is the visible outer face.
        Pass axes="xyz" for corner pieces, which must stay flat on two sides."""
        a = S.WOBBLE if amount is None else amount
        if a <= 0:
            return
        # DETERMINISM, and this one was serious: mathutils.noise is seeded PER BLENDER
        # PROCESS, so noise_vector() returned a different field on every run. Because
        # wobble displaces every vertex by it, "same code, same mesh" -- which BRIEF.md
        # promises and the whole kit's reproducibility rests on -- was simply false for
        # every family that wobbles. Two builds of identical code produced different
        # meshes, and even different vertex counts once remove_doubles saw different
        # positions. It also made measurements unrepeatable and left latent bugs
        # flickering on and off between builds (geometry that clamps on some runs and
        # not others). Seeding from the part name makes each piece reproducible and
        # still distinct from its neighbours.
        noise.seed_set(int(hashlib.md5(self.name.encode()).hexdigest()[:8], 16)
                       % 0x7fffffff)
        for v in self.bm.verts:
            f = self._seam_fade(v.co, axes, margin) if respect_seams else 1.0
            if f <= 0:
                continue
            n = noise.noise_vector(v.co * freq)
            v.co += Vector(n) * a * f

    def bow(self, amount, axis='Y', along='X', span=None, shape='sine', ramps=True):
        """Bend the whole part: displace along `axis` as a function of position
        along `along`. This is the curved-timber tool every family was
        reimplementing locally -- curved braces, bowed bargeboards, sagging
        ridges, the bell-cast flick at an eave.

        amount  peak displacement (signed)
        shape   'sine'  sin(pi t)      -- smooth, zero at both ends
                'arc'   4t(1-t)        -- flatter top, parabolic
                'ramp'  t              -- straight lean, no return
        ramps   keep the two ends exactly in place (needed if the ends are a
                snap seam); set False to bend the ends too.
        """
        i_ax = 'xyz'.index(axis.lower())
        i_al = 'xyz'.index(along.lower())
        vs = list(self.bm.verts)
        if not vs or abs(amount) < 1e-9:
            return
        lo = span[0] if span else min(v.co[i_al] for v in vs)
        hi = span[1] if span else max(v.co[i_al] for v in vs)
        if hi - lo < 1e-6:
            return
        for v in vs:
            t = clamp((v.co[i_al] - lo) / (hi - lo))
            if shape == 'arc':
                w = 4 * t * (1 - t)
            elif shape == 'ramp':
                w = t
            else:
                w = sin(pi * t)
            if ramps and shape != 'ramp':
                w *= smoothstep(0, .08, t) * smoothstep(0, .08, 1 - t)
            v.co[i_ax] += amount * w

    def sag(self, amount=None, axis='X', span=None, seams=True):
        """Droop a long horizontal member in the middle. Ridges, lintels, beams."""
        a = S.SAG if amount is None else amount
        if a <= 0:
            return
        i = 'xyz'.index(axis)
        vs = [v for v in self.bm.verts]
        if not vs:
            return
        lo = span[0] if span else min(v.co[i] for v in vs)
        hi = span[1] if span else max(v.co[i] for v in vs)
        if hi - lo < 1e-6:
            return
        for v in vs:
            t = clamp((v.co[i] - lo) / (hi - lo))
            v.co.z -= a * sin(pi * t)

    def transform(self, mtx):
        bmesh.ops.transform(self.bm, matrix=mtx, verts=list(self.bm.verts))

    def merge(self, other, at=(0, 0, 0), rot=None, scale=1.0, mirror=None):
        """Stamp another Part's geometry into this one. Build a detail once
        (corbel, shutter, finial) and repeat it. `mirror` e.g. 'X' flips it."""
        tmp = bmesh.new()
        other_me = bpy.data.meshes.new("_tmp_merge")
        other.bm.to_mesh(other_me)
        tmp.from_mesh(other_me)
        cl = tmp.loops.layers.float_color.get("Col") or tmp.loops.layers.float_color.new("Col")
        mtx = Matrix.Translation(at) @ _euler(rot) @ Matrix.Scale(scale, 4)
        if mirror:
            s = [1, 1, 1]
            s['xyz'.index(mirror.lower())] = -1
            mtx = mtx @ Matrix.Diagonal(s + [1]).to_4x4()
        bmesh.ops.transform(tmp, matrix=mtx, verts=list(tmp.verts))
        # remap material indices from other's slot order into ours
        remap = {i: self._mi(nm) for i, nm in enumerate(other._mats)}
        for f in tmp.faces:
            f.material_index = remap.get(f.material_index, 0)
        me2 = bpy.data.meshes.new("_tmp_merge2")
        tmp.to_mesh(me2)
        self.bm.from_mesh(me2)
        if mirror:
            bmesh.ops.recalc_face_normals(self.bm, faces=list(self.bm.faces))
        bpy.data.meshes.remove(other_me)
        bpy.data.meshes.remove(me2)
        tmp.free()

    def sub(self, name=None):
        """A scratch Part for building a detail you intend to merge()."""
        return Part(name or (self.name + "_sub"), smooth=self.smooth)

    # ---- output -------------------------------------------------------------
    def stats(self):
        return dict(tris=sum(len(f.verts) - 2 for f in self.bm.faces),
                    verts=len(self.bm.verts), faces=len(self.bm.faces))

    def clamp_to_seams(self, proud=None, axes="xyz", slack_axes=None):
        """Push any vertex that escaped the declared snap planes back onto them.
        Stones cut at a module boundary then meet their neighbour exactly --
        which is what a tiling wall does in reality anyway.

        Returns (n_moved, worst_overshoot, worst_axis) so finish() can WARN. This
        silently deformed geometry before, which is far worse than failing loudly:
        it flattened a lantern hood's octagon face while the report stayed clean.

        axes         which axes to clamp at all
        slack_axes   which axes allow PROUD_MAX outward relief past the lower bound
        """
        pr = (self.proud if self.proud is not None else S.PROUD_MAX) if proud is None else proud
        slack_axes = self.outward if slack_axes is None else slack_axes
        moved, worst, worst_ax = 0, 0.0, ""
        for v in self.bm.verts:
            for ax, i in (('x', 0), ('y', 1), ('z', 2)):
                if ax not in axes or ax not in self.seams:
                    continue
                lo, hi = self.seams[ax]
                slack = pr if ax in slack_axes else 0.0
                lo_lim = lo - slack
                if v.co[i] < lo_lim:
                    d = lo_lim - v.co[i]
                    if d > worst: worst, worst_ax = d, ax + "-min"
                    v.co[i] = lo_lim; moved += 1
                elif v.co[i] > hi:
                    d = v.co[i] - hi
                    if d > worst: worst, worst_ax = d, ax + "-max"
                    v.co[i] = hi; moved += 1
        return moved, worst, worst_ax

    def finish(self, collection=None, validate=True, weld=0.0006):
        """Bake to a real object: welds doubles, assigns materials, writes the
        Col layer, sets sharp edges by angle, validates bounds + tri budget."""
        clamp_note = ""
        if self.seams:
            n_moved, worst, worst_ax = self.clamp_to_seams()
            if worst > 0.004:
                clamp_note = (f"{n_moved} verts cut, worst {worst:.3f}m on {worst_ax}")
                print(f"  CLAMP {self.name}: {clamp_note}")
        if weld:
            bmesh.ops.remove_doubles(self.bm, verts=list(self.bm.verts), dist=weld)
        bmesh.ops.recalc_face_normals(self.bm, faces=list(self.bm.faces))
        me = bpy.data.meshes.new(self.name)
        self.bm.to_mesh(me)
        st = dict(tris=sum(len(p.vertices) - 2 for p in me.polygons),
                  verts=len(me.vertices))
        self.bm.free()
        self.bm = None
        for nm in self._mats:
            me.materials.append(M.get(nm))
        ob = bpy.data.objects.new(self.name, me)
        (collection or bpy.context.scene.collection).objects.link(ob)
        ob["kit_tris"] = st["tris"]
        ob["kit_budget"] = self.budget or ""
        ob["kit_seams"] = str(self.seams)
        if self.smooth:
            prev = bpy.context.view_layer.objects.active
            for o in bpy.context.selected_objects:
                o.select_set(False)
            bpy.context.view_layer.objects.active = ob
            ob.select_set(True)
            try:
                bpy.ops.object.shade_smooth_by_angle(angle=radians(S.SMOOTH_ANG))
            except Exception:
                for p in me.polygons:
                    p.use_smooth = True
            ob.select_set(False)
            bpy.context.view_layer.objects.active = prev
        ob["kit_proud"] = -1.0 if self.proud is None else self.proud
        ob["kit_outward"] = self.outward
        # Clamping is reported SEPARATELY from failures. Cutting a stone flat where
        # it crosses a bay seam is exactly how tiling is supposed to work; deforming
        # a dormer roof by 100mm is a bug. Same mechanism, so the number is surfaced
        # and a human judges it, rather than every wall reading as broken forever.
        ob["kit_clamped"] = clamp_note
        ob["kit_report"] = "; ".join(check(ob, self.budget, self.seams,
                                           self.proud, self.outward)) or "ok"
        return ob


# ------------------------------------------------------------ validation -----
def check(ob, budget=None, seams=None, proud=None, outward="y"):
    """Hard checks so 'no gaps or floating seams' is provable, not eyeballed."""
    bad = []
    me = ob.data
    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    if budget and budget in S.TRI_BUDGET and tris > S.TRI_BUDGET[budget]:
        bad.append(f"OVER BUDGET {tris}>{S.TRI_BUDGET[budget]} tris")
    if not me.vertices:
        return ["EMPTY MESH"]
    seams = seams or {}
    for ax, i in (('x', 0), ('y', 1), ('z', 2)):
        if ax not in seams:
            continue
        lo, hi = seams[ax]
        vs = [v.co[i] for v in me.vertices]
        # outward (-Y for walls, and -X/-Y for corners) may stand proud
        pr = S.PROUD_MAX if proud is None else proud
        slack_lo = pr if ax in outward else 0.001
        if min(vs) < lo - slack_lo - 1e-4:
            bad.append(f"{ax}-min {min(vs):.3f} < {lo - slack_lo:.3f}")
        if max(vs) > hi + 1e-4:
            bad.append(f"{ax}-max {max(vs):.3f} > {hi:.3f}")
    # loose geometry / non-manifold-ish sanity
    loose = sum(1 for v in me.vertices if not any(v.index in e.vertices for e in me.edges))
    if loose:
        bad.append(f"{loose} loose verts")
    return bad


# --------------------------------------------------------------- scene util --
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for blk in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for b in list(blk):
            if b.users == 0:
                blk.remove(b)


def get_collection(name, parent=None):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c
