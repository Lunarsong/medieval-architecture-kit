"""Build the WHOLE kit into one file.

    blender -b --python build_kit.py

Writes out/inn_kit.blend  (open this in Blender)
       out/inn_kit.glb    (open this in anything: Unity, Unreal, Godot, Blender,
                           Maya, Windows 3D Viewer, three.js)
Prints a kit manifest.

Layout note: pieces are spread out in rows by family so the file is browsable.
Each piece's MESH still carries the canonical kit origin, so zeroing an object's
location snaps it to its convention position -- that is how you assemble with them.
"""
import bpy, sys, os, json, importlib, traceback
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kit import spec as S, mats as M, util as U, render as R
from kit import finalize as F
from kit.registry import FAMILIES, ORDER

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
no_gltf = "--no-gltf" in argv

U.clear_scene()
M.build_all()

manifest, row_y, missing = [], 0.0, []
for fam in ORDER:
    mod_name, coll_name, budget = FAMILIES[fam]
    try:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
    except Exception:
        missing.append(fam)
        print(f"SKIP {fam}: not built yet")
        continue
    coll = U.get_collection(coll_name)
    try:
        objs = mod.build()
    except Exception:
        traceback.print_exc()
        missing.append(fam + " (build error)")
        continue
    objs = [o for o in (objs if isinstance(objs, (list, tuple)) else [objs])
            if o and o.type == 'MESH']
    # move into the family collection
    for o in objs:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
    # lay the family out in a row, spaced by actual width
    bpy.context.view_layer.update()
    x = 0.0
    depth = 0.0
    for o in objs:
        lo, hi = R.bbox_of([o])
        w = max(hi.x - lo.x, 0.4)
        o.location.x += x - lo.x
        o.location.y += row_y - lo.y
        x += w + 0.7
        depth = max(depth, hi.y - lo.y)
        pr = o.get("kit_proud")
        pr = None if pr is None or pr < 0 else pr
        errs = U.check(o, o.get("kit_budget") or budget, eval(o.get("kit_seams") or "{}"), pr,
                    o.get("kit_outward") or "y")
        manifest.append(dict(family=fam, name=o.name, tris=int(o.get("kit_tris") or 0),
                             report=errs))
    row_y += depth + 2.2
    print(f"BUILT {fam}: {len(objs)} pieces")

# UVs + switched-off texture slots, so the kit can be textured in any DCC/engine
F.finalize(objs=[o for o in bpy.data.objects if o.type == 'MESH'])

os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
blend = os.path.join(ROOT, "out", "inn_kit.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print("SAVED", blend)

if not no_gltf:
    glb = os.path.join(ROOT, "out", "inn_kit.glb")
    kw = dict(filepath=glb, export_format='GLB', export_apply=True,
              export_yup=True, export_materials='EXPORT',
              export_texcoords=True, export_normals=True,
              # Keep export_all_vertex_colors ON. It emits "Col" twice (COLOR_0 and
              # COLOR_1, ~4MB of duplicate payload), but it is the ONLY setting that
              # exports vertex colour at all here: both 'MATERIAL' and 'ACTIVE' with
              # the flag off produced a GLB with no COLOR_0, because the exporter does
              # not recognise our Vertex Color -> Mix -> Base Color node pattern. The
              # colour variation IS the kit's look, so correctness wins over filesize.
              # (Converting Col to BYTE_COLOR would shrink it, but harmonisation
              # scales some pieces above 1.0 and byte colour would clamp them darker.)
              export_all_vertex_colors=True)
    try:
        bpy.ops.export_scene.gltf(**kw)
    except TypeError:
        bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB')
    print("SAVED", glb)

total = sum(m["tris"] for m in manifest)
fails = [m for m in manifest if m["report"]]
json.dump(dict(pieces=manifest, total_tris=total, families_missing=missing),
          open(os.path.join(ROOT, "out", "manifest.json"), "w"), indent=1)
print(f"KIT_TOTAL pieces={len(manifest)} tris={total} failing={len(fails)} missing={missing}")
for m in fails:
    print("  FAIL", m["name"], m["report"])
