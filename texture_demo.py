"""Prove the kit is texturable: render the same pieces with the texture slots off
and on, changing nothing but a Mix factor.

    blender -b --python texture_demo.py

Writes renders/texture/untextured.png and textured.png
"""
import bpy, sys, os, importlib, fnmatch
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kit import spec as S, mats as M, util as U, render as R, finalize as F
from kit.registry import FAMILIES, ORDER

# which tiling texture belongs on which kit material
# Modelled detail gets GRAIN; only flat surfaces get a pattern with its own cells,
# otherwise you end up with two competing stone patterns fighting each other.
ASSIGN = {
    "wood_grain":  ["oak_dark", "oak_mid", "oak_pale"],
    "wood_planks": ["thatch"],
    "plaster":     ["plaster", "plaster_dim"],
    "stone_grain": ["stone", "stone_dark", "stone_pale", "stone_warm"],
    "shingle":     ["shingle", "shingle_moss"],
    "rubble":      [],      # for flat/ashlar stone surfaces
    "cobble":      [],      # for flat ground patches
}

WANT = ["SM_Wall_Stone*", "SM_Wall_Timber*", "SM_Door_*", "SM_Prop_Barrel*",
        "SM_Roof_Slope*", "SM_Roof_Shingle*", "SM_Chimney_Stack*", "SM_Window_*"]

U.clear_scene()
M.build_all()
picked = []
for fam in ORDER:
    mod_name, coll, budget = FAMILIES[fam]
    try:
        mod = importlib.import_module(mod_name)
        objs = mod.build()
    except Exception:
        continue
    for o in (objs if isinstance(objs, (list, tuple)) else [objs]):
        if not o or o.type != 'MESH':
            continue
        if any(fnmatch.fnmatch(o.name, w) for w in WANT) and \
                not any(fnmatch.fnmatch(p.name, o.name) for p in picked):
            picked.append(o)
        else:
            bpy.data.objects.remove(o, do_unlink=True)

# one per pattern, so the lineup stays readable
seen, keep = set(), []
for w in WANT:
    for o in picked:
        if fnmatch.fnmatch(o.name, w) and w not in seen:
            keep.append(o); seen.add(w); break
for o in picked:
    if o not in keep:
        bpy.data.objects.remove(o, do_unlink=True)
print("DEMO pieces:", [o.name for o in keep])

F.finalize(objs=keep)

# load the textures into the slots finalize() wired up
for tex, mats in ASSIGN.items():
    path = os.path.join(ROOT, "textures", f"{tex}.png")
    if not os.path.exists(path):
        continue
    img = bpy.data.images.load(path, check_existing=True)
    for mn in mats:
        m = bpy.data.materials.get("M_" + mn)
        if not m or not m.use_nodes:
            continue
        node = m.node_tree.nodes.get("TEX_image")
        if node:
            node.image = img

R.lineup(keep, gap=0.6)
out = os.path.join(ROOT, "renders", "texture")
os.makedirs(out, exist_ok=True)

def shoot(factor, name):
    for m in bpy.data.materials:
        mix = m.node_tree.nodes.get("TEX_mix") if m.use_nodes else None
        if mix:
            mix.inputs[0].default_value = factor
    R.save(os.path.join(out, name))

R.studio(keep, res=(1800, 700), samples=48)
R.camera(keep, yaw=30, pitch=76, lens=58, margin=1.06)
shoot(0.0, "untextured.png")
shoot(1.0, "textured.png")
print("TEXTURE_DEMO done")
