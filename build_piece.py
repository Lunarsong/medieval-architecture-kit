"""Build + render ONE family. This is the builder's inner loop.

    blender -b --python build_piece.py -- stone_walls
    blender -b --python build_piece.py -- stone_walls --cycles

Writes: renders/<family>/lineup.png, tiled.png, closeup.png, demo.png
        out/<family>.blend
Prints: a JSON report (per piece: tris + validation errors). NON-EMPTY "report"
        FIELDS ARE FAILURES -- fix them, don't ignore them.
"""
import bpy, sys, os, json, importlib, traceback
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kit import spec as S, mats as M, util as U, render as R
from kit.registry import FAMILIES

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
fam = argv[0] if argv else "stone_walls"
cyc = "--cycles" in argv
norender = "--no-render" in argv
mod_name, coll_name, budget = FAMILIES[fam]

U.clear_scene()
M.build_all()
mod = importlib.import_module(mod_name)
importlib.reload(mod)

objs = mod.build()
if not isinstance(objs, (list, tuple)):
    objs = [objs]
objs = [o for o in objs if o and o.type == 'MESH']

report = {"family": fam, "n_pieces": len(objs), "pieces": [], "total_tris": 0, "fails": 0}
for o in objs:
    pr = o.get("kit_proud")
    pr = None if pr is None or pr < 0 else pr
    errs = U.check(o, o.get("kit_budget") or budget, eval(o.get("kit_seams") or "{}"), pr,
                    o.get("kit_outward") or "y")
    t = int(o.get("kit_tris") or 0)
    report["total_tris"] += t
    if errs:
        report["fails"] += 1
    row = {"name": o.name, "tris": t, "report": errs}
    cl = o.get("kit_clamped")
    if cl:
        # not a failure -- but if this number is large on an axis your piece is not
        # meant to tile on, your geometry is being deformed to fit its seams
        row["clamped"] = cl
    report["pieces"].append(row)

outdir = os.path.join(ROOT, "renders", fam)
os.makedirs(outdir, exist_ok=True)

if not norender:
    home = [o.location.copy() for o in objs]
    # ---- 1. lineup: every piece in the family, side by side, studio light
    R.lineup(list(objs), gap=0.55)
    R.studio(objs, res=(1600, 700), samples=32, eevee=not cyc)
    R.camera(objs, yaw=34, pitch=76, lens=55, margin=1.10)
    R.save(os.path.join(outdir, "lineup.png"))
    # ---- 2. closeup of the first piece, 3/4 view
    R.clear_stage()
    R.studio([objs[0]], res=(900, 900), samples=48, eevee=not cyc)
    R.camera([objs[0]], yaw=42, pitch=74, lens=65, margin=1.06)
    R.save(os.path.join(outdir, "closeup.png"))
    for o, h in zip(objs, home):
        o.location = h
    # ---- 3. tiling proof: 3 linked copies at exact GRID spacing.
    # Every OTHER piece must be hidden: they are all sitting back at their home
    # location (the origin), so they render as a pile of overlapping geometry behind
    # the tiles and read as rubbish stuffed into window and arch openings.
    R.clear_stage()
    tiles = R.tile_copies(objs[0], 3)
    hidden = [o for o in objs if o is not objs[0]]
    for o in hidden:
        o.hide_render = True
    R.studio(tiles, res=(1300, 800), samples=32, eevee=not cyc)
    R.camera(tiles, yaw=28, pitch=80, lens=60, margin=1.06)
    R.save(os.path.join(outdir, "tiled.png"))
    for o in hidden:
        o.hide_render = False
    for t in tiles[1:]:
        bpy.data.objects.remove(t, do_unlink=True)
    for o, h in zip(objs, home):
        o.location = h
    # ---- 4. demo assembly in reference light, if the module provides one
    if hasattr(mod, "demo"):
        R.clear_stage()
        try:
            demo = [o for o in (mod.demo() or []) if o and o.type == 'MESH']
            if demo:
                R.look_ref2()
                R.camera(demo, yaw=44, pitch=64, lens=80, margin=1.10)
                R.save(os.path.join(outdir, "demo.png"))
        except Exception:
            traceback.print_exc()
            report["demo_error"] = traceback.format_exc()[-800:]

os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "out", f"{fam}.blend"))
print("REPORT_JSON " + json.dumps(report))
