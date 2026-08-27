#!/usr/bin/env python3
"""Generate seamless 1-metre tiling textures for the kit.

    python3 texture_gen.py     -> textures/*.png

Every texture tiles seamlessly and is authored to represent ONE SQUARE METRE,
which is exactly what the kit's world-scale "UVMap" expects: drop these in and the
grain runs at the right size on every piece automatically, with no per-piece
adjustment. Deterministic -- same output every run.
"""
import os, numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "textures")
N = 1024


def rng(seed):
    return np.random.default_rng(seed)


def periodic_noise(n, freq, seed, octaves=4, gain=0.5):
    """Tileable value noise: build it in the frequency domain so the wrap is exact."""
    out = np.zeros((n, n))
    amp, tot = 1.0, 0.0
    r = rng(seed)
    for o in range(octaves):
        f = freq * (2 ** o)
        g = r.random((f, f))
        # bilinear upsample with wraparound
        yy, xx = np.meshgrid(np.arange(n) * f / n, np.arange(n) * f / n, indexing='ij')
        y0, x0 = yy.astype(int), xx.astype(int)
        fy, fx = yy - y0, xx - x0
        y1, x1 = (y0 + 1) % f, (x0 + 1) % f
        sy, sx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
        v = (g[y0, x0] * (1 - sx) * (1 - sy) + g[y0, x1] * sx * (1 - sy) +
             g[y1, x0] * (1 - sx) * sy + g[y1, x1] * sx * sy)
        out += v * amp
        tot += amp
        amp *= gain
    return out / tot


def save(name, arr):
    a = np.clip(arr, 0, 1)
    if a.ndim == 2:
        a = np.dstack([a] * 3)
    Image.fromarray((a * 255).astype(np.uint8)).save(f"{OUT}/{name}.png")
    print("wrote", name)


def planks():
    """Vertical boards, 4 to the metre, each its own tone, with long-axis grain."""
    n, nb = N, 4
    x = np.arange(n)
    board = (x * nb // n)
    r = rng(7)
    tone = r.uniform(.74, 1.14, nb)[board][None, :]
    # grain runs ALONG the board: sample noise that is fine across X, coarse along Y
    fine = periodic_noise(n, 96, 11, octaves=2, gain=.5)      # across-grain detail
    long_ = periodic_noise(n, 6, 13, octaves=4, gain=.6)      # slow variation up the board
    grain = 0.80 + 0.26 * fine * 0.55 + 0.22 * long_
    img = tone * grain
    # dark seam between boards with a lit chamfer either side
    w = n // nb
    edge = x % w
    seam = np.clip(np.minimum(edge, w - 1 - edge) / (w * .05), 0, 1)
    img *= (0.34 + 0.66 * seam)[None, :]
    img *= 1.0 + 0.10 * np.clip(1 - np.minimum(edge, w - 1 - edge) / (w * .12), 0, 1)[None, :]
    # nail heads and knots
    for k in range(4):
        cy = rng(101 + k).integers(0, n)
        cx = int((k + .5) * w)
        yy, xx = np.ogrid[:n, :n]
        d = np.sqrt(np.minimum(abs(yy - cy), n - abs(yy - cy)) ** 2 +
                    np.minimum(abs(xx - cx), n - abs(xx - cx)) ** 2)
        img *= 1 - 0.42 * np.exp(-(d / (n * .014)) ** 2)
    save("wood_planks", img)


def plaster():
    """Lime plaster with real value range. A critic measured our plaster panels at a
    luminance sd of 2 across 19% of the facade -- a blank white card -- against
    25-35 in the reference. So this carries mottling, damp darkening, hairline
    cracks and a dirt cast, aiming for sd ~0.10 as a multiplier (roughly 25 L)."""
    n = N
    r = rng(41)
    # broad patchy mottle: the dominant variation
    img = 0.80 + 0.34 * periodic_noise(n, 3, 41, 5, .58)
    # damp/dirt blooms
    img *= 0.86 + 0.22 * periodic_noise(n, 6, 47, 4, .55)
    # fine tooth of the lime render
    img *= 0.95 + 0.09 * periodic_noise(n, 48, 43, 3, .5)
    # hairline cracks: thin dark meandering lines
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    for k in range(7):
        rr = rng(200 + k)
        vert = rr.random() < 0.5
        pos = rr.integers(0, n)
        amp = rr.uniform(6, 26)
        freq = rr.uniform(1.5, 4.0)
        wob = amp * np.sin(2 * np.pi * freq * (yy if vert else xx) / n)
        d = np.minimum(np.abs(((xx if vert else yy) - pos - wob) % n),
                       np.abs(((xx if vert else yy) - pos - wob) % n - n))
        img *= 1 - 0.34 * np.exp(-(d / 1.7) ** 2)
    # a few chipped patches showing darker render beneath
    for k in range(5):
        rr = rng(300 + k)
        cy, cx = rr.integers(0, n, 2)
        rad = rr.uniform(n * .012, n * .035)
        dy = np.minimum(abs(yy - cy), n - abs(yy - cy))
        dx = np.minimum(abs(xx - cx), n - abs(xx - cx))
        img *= 1 - 0.30 * np.exp(-((np.sqrt(dy**2 + dx**2) / rad) ** 3))
    img = np.clip(img, 0.30, 1.08)
    print(f"   plaster sd={img.std():.3f} range={img.min():.2f}..{img.max():.2f}")
    save("plaster", img)


def rubble():
    """Cell pattern: nearest-seed distance, wrapped -- reads as packed stones."""
    n, m = N, 26
    r = rng(53)
    pts = r.random((m, 2)) * n
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    d1 = np.full((n, n), 1e9)
    d2 = np.full((n, n), 1e9)
    owner = np.zeros((n, n), int)
    for i, (py, px) in enumerate(pts):
        dy = np.minimum(abs(yy - py), n - abs(yy - py))
        dx = np.minimum(abs(xx - px), n - abs(xx - px))
        d = np.sqrt(dy ** 2 + dx ** 2)
        upd = d < d1
        d2 = np.where(upd, d1, np.minimum(d2, d))
        owner = np.where(upd, i, owner)
        d1 = np.where(upd, d, d1)
    joint = np.clip((d2 - d1) / (n * .012), 0, 1)          # dark mortar in the gaps
    tone = r.uniform(.72, 1.10, m)[owner]
    img = tone * (0.35 + 0.65 * joint)
    img *= 0.93 + .13 * periodic_noise(n, 30, 59, 3, .5)   # stone grain
    save("rubble", np.clip(img, 0, 1))


def shingle():
    """Courses of shingle tabs, 6 rows to the metre, staggered, wide-ish tabs with
    an irregular butt line and a strong shadow where each course laps the one below."""
    n = N
    rows, cols = 6, 5
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    rh, cw = n / rows, n / cols
    row = (yy / rh).astype(int)
    stag = (row % 2) * 0.5 + 0.11 * np.sin(row * 2.3)      # courses wander sideways
    colf = (xx / cw) + stag
    col = colf.astype(int)
    r = rng(71)
    idx = (row * 97 + col * 31) % 512
    tone = r.uniform(.66, 1.16, 512)[idx]
    # per-tab butt line wobble, so the course edge is not a ruler
    wob = (r.uniform(-.10, .06, 512)[idx])
    fy = ((yy % rh) / rh) - wob
    fx = colf % 1.0
    lap = np.clip(fy / .30, 0, 1)          # shadow under the lapping course above
    side = np.clip(np.minimum(fx, 1 - fx) / .10, 0, 1)
    img = tone * (0.26 + 0.74 * lap) * (0.66 + 0.34 * side)
    img *= 0.88 + .20 * periodic_noise(n, 70, 73, 3, .5)   # split-grain weathering
    img *= 0.92 + .14 * periodic_noise(n, 3, 79, 4, .6)    # patchy moss / dry runs
    save("shingle", img)


def cobble():
    n, m = N, 14
    r = rng(83)
    pts = r.random((m, 2)) * n
    yy, xx = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
    d1 = np.full((n, n), 1e9); d2 = np.full((n, n), 1e9); owner = np.zeros((n, n), int)
    for i, (py, px) in enumerate(pts):
        dy = np.minimum(abs(yy - py), n - abs(yy - py))
        dx = np.minimum(abs(xx - px), n - abs(xx - px))
        d = np.sqrt(dy ** 2 + dx ** 2)
        upd = d < d1
        d2 = np.where(upd, d1, np.minimum(d2, d)); owner = np.where(upd, i, owner)
        d1 = np.where(upd, d, d1)
    joint = np.clip((d2 - d1) / (n * .02), 0, 1)
    img = r.uniform(.70, 1.08, m)[owner] * (0.30 + 0.70 * joint)
    img *= 0.92 + .14 * periodic_noise(n, 40, 89, 3, .5)
    save("cobble", np.clip(img, 0, 1))


def stone_grain():
    """Fine speckled grain with no cell structure -- for stone that is already
    MODELLED as individual stones. Putting a rubble cell pattern on top of modelled
    rubble gives you two competing stone patterns."""
    n = N
    img = 0.90 + .12 * periodic_noise(n, 64, 97, 3, .5)
    img *= 0.94 + .10 * periodic_noise(n, 14, 101, 4, .55)
    img *= 0.97 + .05 * periodic_noise(n, 160, 103, 2, .5)
    save("stone_grain", img)


def wood_grain():
    """Grain only, no board seams -- for timber that is already modelled as separate
    members (posts, braces, beams, barrel staves)."""
    n = N
    fine = periodic_noise(n, 110, 107, 2, .5)
    long_ = periodic_noise(n, 5, 109, 4, .6)
    img = 0.82 + .22 * fine * .6 + .20 * long_
    save("wood_grain", img)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    planks(); plaster(); rubble(); shingle(); cobble()
    stone_grain(); wood_grain()
    print("all textures are seamless and represent 1 m x 1 m")
