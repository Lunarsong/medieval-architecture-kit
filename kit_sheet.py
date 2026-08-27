"""Render the WHOLE kit as one sheet: every piece, same light, same camera scale,
laid out in rows by family, with a 1-metre reference cube.

    blender -b --python kit_sheet.py

This is the instrument for spotting cross-family problems -- a family whose timber
is a different brown, or whose pieces are secretly half-scale -- which is invisible
when you only ever look at one family at a time.

Writes renders/kit/sheet_<n>.png (one per row band, so nothing is too small to see)
      renders/kit/sheet_all.png
"""
import bpy, sys, os, json, importlib, traceback
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kit import spec as S, mats as M, util as U, render as R
from kit.registry import FAMILIES, ORDER

U.clear_scene()
M.build_all()

rows, row_y = [], 0.0
for fam in ORDER:
    mod_name, coll_name, budget = FAMILIES[fam]
    try:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
        objs = mod.build()
    except Exception:
        print(f"SKIP {fam}")
        continue
    objs = [o for o in (objs if isinstance(objs, (list, tuple)) else [objs])
            if o and o.type == 'MESH']
    if not objs:
        continue
    bpy.context.view_layer.update()
    x, depth, hi_z = 0.0, 0.0, 0.0
    for o in objs:
        lo, hi = R.bbox_of([o])
        o.location.x += x - lo.x
        o.location.y += row_y - lo.y
        o.location.z += -lo.z
        x += (hi.x - lo.x) + 0.6
        depth = max(depth, hi.y - lo.y)
        hi_z = max(hi_z, hi.z - lo.z)
    rows.append(dict(family=fam, objs=objs, y=row_y, w=x, h=hi_z, d=depth))
    row_y += depth + 1.8
    print(f"ROW {fam}: {len(objs)} pieces, {x:.1f}m wide, {hi_z:.1f}m tall")

# 1-metre reference cube so scale errors are unmissable
ref = U.Part("_ScaleRef_1m", seams=None)
ref.box((0.5, 0.5, 0.5), (1, 1, 1), "flower_red", bevel=0.02, tint=0.0)
cube = ref.finish()
cube.location = (-2.2, -1.6, 0.0)

os.makedirs(os.path.join(ROOT, "renders", "kit"), exist_ok=True)
allobjs = [o for r in rows for o in r["objs"]] + [cube]

R.studio(allobjs, res=(2000, 1250), samples=40, bg="pale")
R.camera(allobjs, yaw=22, pitch=68, lens=70, margin=1.06)
R.save(os.path.join(ROOT, "renders", "kit", "sheet_all.png"))

# per-band renders so detail is legible
band, i = [], 0
for r in rows:
    band.append(r)
    if sum(len(b["objs"]) for b in band) >= 10 or r is rows[-1]:
        i += 1
        objs = [o for b in band for o in b["objs"]] + [cube]
        R.clear_stage()
        R.studio(objs, res=(1800, 800), samples=36, bg="pale")
        R.camera(objs, yaw=26, pitch=72, lens=68, margin=1.05)
        R.save(os.path.join(ROOT, "renders", "kit", f"sheet_{i}.png"))
        print("BAND", i, [b["family"] for b in band])
        band = []

print("SHEET_JSON " + json.dumps([dict(family=r["family"], pieces=len(r["objs"]),
                                       w=round(r["w"], 2), h=round(r["h"], 2)) for r in rows]))
