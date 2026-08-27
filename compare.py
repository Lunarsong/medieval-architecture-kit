#!/usr/bin/env python3
"""Blind comparison sheets. The critic sees ONLY the sheet; the answer key is
written to a separate file it is never given.

  # ours vs a matched crop of a reference painting
  python3 compare.py sheet --ours renders/roofs/demo.png --ref ref2:roof_field \
      --out cmp/roofs_r1.png --key cmp/roofs_r1.key.json

  # ours (this round) vs ours (last round) -- genuinely blind, catches regressions
  python3 compare.py ab --a prev.png --b new.png --out cmp/x.png --key cmp/x.key.json

  python3 compare.py regions          # list reference crops
  python3 compare.py crop --ref ref1:stone_base --out /tmp/x.png
"""
import json, os, sys, argparse, hashlib
from PIL import Image, ImageDraw, ImageFont

REFS = {
    "ref1": "/Users/shanee/Downloads/fantasy_inn.jpg",   # warm sunlit street view
    "ref2": "/Users/shanee/Downloads/Inn.jpg",           # big coaching inn, 3/4 aerial
    # Eight more Shanee supplied on 24 Aug, saved into the repo so they travel with it.
    # r6/r7 are the most useful of the set: they are a 3D RENDER of one building from
    # two angles, not a painting, so they show what is actually reachable in geometry --
    # white render dominant with narrow dark studs, fine grey slate courses, a stone
    # ground floor with an open arcade.
    "r4":  "refs/r4.jpg",    # moody night, half-timber over an arched door
    "r5":  "refs/r5.jpg",    # classic cream-panel inn, corner post, flower boxes
    "r6":  "refs/r6.jpg",    # 3D build, front: arcaded undercroft, slate roof, banner
    "r7":  "refs/r7.jpg",    # the same build, three-quarter
    "r8":  "refs/r8.jpg",    # timber gallery over an open ground floor, barrels
    "r9":  "refs/r9.jpg",    # round-arched arcade, lit lanterns, tables, cobbles
    "r10": "refs/r10.jpg",   # STRONG jetty + timber gallery, stone base, outside stair
    "r11": "refs/r11.jpg",   # steep multi-gable roofline, ground-level arcade
    "ref3": "/Users/shanee/Downloads/inn - greyscale.jpg",  # SAME building as ref2,
    # drawn as greyscale linework. This is the best FORM reference in the set: no
    # colour, no painterly texture, so structure reads plainly -- timber framing
    # layout, plank direction, dentil courses, bargeboard scallops, mullions. It is
    # also the fairest blind comparison for our grey renders, since neither side has
    # colour to win on.
}

# fractional crop boxes (l, t, r, b) -- compare like with like
REGIONS = {
    "ref1": {
        "whole":       (0.00, 0.00, 1.00, 1.00),
        "roof":        (0.15, 0.00, 0.88, 0.46),
        "eave":        (0.17, 0.02, 0.58, 0.32),
        "swept_eave":  (0.12, 0.18, 0.42, 0.42),
        "stone_base":  (0.20, 0.52, 0.58, 0.92),
        "timber":      (0.17, 0.18, 0.47, 0.56),
        "door":        (0.45, 0.50, 0.65, 0.82),
        "arch_door":   (0.24, 0.55, 0.42, 0.80),
        "lantern":     (0.12, 0.48, 0.26, 0.72),
        "barrels":     (0.53, 0.66, 0.95, 0.94),
        "windows":     (0.19, 0.26, 0.44, 0.50),
        "chimney":     (0.42, 0.00, 0.58, 0.22),
    },
    "ref2": {
        "whole":       (0.00, 0.00, 1.00, 1.00),
        "dormers":     (0.62, 0.40, 0.93, 0.70),
        "bargeboard":  (0.40, 0.08, 0.74, 0.42),
        "roof_field":  (0.08, 0.16, 0.56, 0.52),
        "timber":      (0.38, 0.32, 0.64, 0.70),
        "stone_arch":  (0.64, 0.62, 0.92, 0.88),
        "porch":       (0.52, 0.58, 0.72, 0.92),
        "chimney":     (0.30, 0.02, 0.50, 0.32),
        "shed":        (0.12, 0.64, 0.44, 0.97),
        "flowerbox":   (0.42, 0.52, 0.62, 0.70),
        "gable":       (0.40, 0.06, 0.70, 0.50),
        "whole_left":  (0.06, 0.10, 0.55, 0.98),
    },
}

REGIONS["ref3"] = dict(REGIONS["ref2"])
for _r in ("r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11"):
    REGIONS[_r] = {"whole": (0.0, 0.0, 1.0, 1.0)}

# which reference crop each family should be judged against
# ref3 (greyscale linework) leads wherever FORM is the thing being judged, because
# it strips the colour advantage the paintings would otherwise win on.
FAMILY_REGION = {
    "stone_walls":  ["ref3:stone_arch", "ref1:stone_base", "ref2:stone_arch"],
    "timber_walls": ["ref3:timber", "ref2:timber", "ref1:timber"],
    "corners":      ["ref3:timber", "ref1:timber"],
    "roofs":        ["ref3:roof_field", "ref2:roof_field", "ref1:roof"],
    "gables":       ["ref3:bargeboard", "ref2:bargeboard", "ref1:eave"],
    "dormers":      ["ref3:dormers", "ref2:dormers"],
    "chimneys":     ["ref3:chimney", "ref2:chimney"],
    "doors":        ["ref3:porch", "ref1:door"],
    "windows":      ["ref3:flowerbox", "ref2:flowerbox", "ref1:windows"],
    "beams":        ["ref3:porch", "ref1:swept_eave"],
    "signage":      ["ref1:lantern"],
    "props":        ["ref1:barrels", "ref3:shed"],
    "ground":       ["ref3:porch", "ref1:barrels"],
    "inn":          ["ref3:whole", "ref2:whole", "ref1:whole"],
}


def load_region(spec):
    ref, _, reg = spec.partition(":")
    path = REFS[ref]
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    im = Image.open(path).convert("RGB")
    l, t, r, b = REGIONS[ref][reg or "whole"]
    W, H = im.size
    return im.crop((int(l * W), int(t * H), int(r * W), int(b * H)))


def fit(im, h):
    w = max(1, int(im.width * h / im.height))
    return im.resize((w, h), Image.LANCZOS)


def label(im, letter):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
    except Exception:
        f = ImageFont.load_default()
    d.rectangle([0, 0, 52, 48], fill=(16, 16, 16))
    d.text((16, 4), letter, fill=(255, 255, 255), font=f)
    return im


def sheet(paths, out, key_path, seed=None, height=860):
    """paths: [(tag, PIL.Image)] -- order is randomised, tags recorded in the key."""
    import random
    h = hashlib.md5((seed or out).encode()).hexdigest()
    rnd = random.Random(int(h[:12], 16))
    items = list(paths)
    rnd.shuffle(items)
    ims = [fit(im, height) for _, im in items]
    gap = 16
    W = sum(i.width for i in ims) + gap * (len(ims) + 1)
    canvas = Image.new("RGB", (W, height + gap * 2), (30, 30, 32))
    x = gap
    key = {}
    for (tag, _), im, letter in zip(items, ims, "ABCDEFG"):
        canvas.paste(label(im.copy(), letter), (x, gap))
        key[letter] = tag
        x += im.width + gap
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    canvas.save(out, quality=94)
    if key_path:
        os.makedirs(os.path.dirname(os.path.abspath(key_path)), exist_ok=True)
        json.dump(key, open(key_path, "w"), indent=1)
    return key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["sheet", "ab", "regions", "crop", "family"])
    ap.add_argument("--ours"); ap.add_argument("--ref"); ap.add_argument("--a")
    ap.add_argument("--b"); ap.add_argument("--out"); ap.add_argument("--key")
    ap.add_argument("--seed"); ap.add_argument("--height", type=int, default=860)
    a = ap.parse_args()
    if a.mode == "regions":
        for r, d in REGIONS.items():
            print(r, "->", ", ".join(sorted(d)))
        print("\nfamily -> regions:")
        for k, v in FAMILY_REGION.items():
            print(f"  {k:14s} {v}")
        return
    if a.mode == "crop":
        load_region(a.ref).save(a.out, quality=95)
        print("wrote", a.out)
        return
    if a.mode == "sheet":
        items = [("OURS", Image.open(a.ours).convert("RGB")),
                 ("REF:" + a.ref, load_region(a.ref))]
    else:
        items = [("A_FILE:" + a.a, Image.open(a.a).convert("RGB")),
                 ("B_FILE:" + a.b, Image.open(a.b).convert("RGB"))]
    k = sheet(items, a.out, a.key, seed=a.seed, height=a.height)
    print("wrote", a.out, "| key ->", a.key or "(none)")


if __name__ == "__main__":
    main()
