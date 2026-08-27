"""Render the whole kit as ONE compact contact sheet.

    blender -b --python kit_grid.py

`kit_sheet.py` lays the kit out in long rows by family, which is the right
instrument for comparing families against each other but a poor picture: at
whole-kit framing the pieces are specks and most of the frame is empty ground.

The trap this script exists to avoid: a UNIFORM cell. Size every cell to the
largest piece and the 4 m tie beam sets a 7.5 m cell for a 0.3 m bucket, so 182
pieces spread over 130 m and every one of them is a speck again. Cells are
therefore packed to each piece's OWN width, rows wrap at a target width, and
each row is only as deep as its deepest piece.

Writes renders/kit/grid.png
"""
import bpy
import os
import sys
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kit import render as R

ROW_W = 30.0               # wrap a row past this width, metres
PAD = 0.42                 # gap between pieces
ROW_PAD = 0.55             # gap between rows
SRC = os.path.join(ROOT, "out", "inn_kit.blend")
OUT = os.path.join(ROOT, "renders", "kit", "grid.png")

bpy.ops.wm.open_mainfile(filepath=SRC)


def wbb(ob):
    v = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    return (Vector((min(p.x for p in v), min(p.y for p in v), min(p.z for p in v))),
            Vector((max(p.x for p in v), max(p.y for p in v), max(p.z for p in v))))


def family(ob):
    for c in ob.users_collection:
        if c.name not in ("_library", "Scene Collection", "Collection"):
            return c.name
    return "zzz"


pieces = [o for o in bpy.data.objects
          if o.type == 'MESH' and o.name.startswith("SM_")]
pieces.sort(key=lambda o: (family(o), o.name))
print("GRID %d pieces in %d families"
      % (len(pieces), len({family(o) for o in pieces})))

# Anything that is not a kit piece -- a ground plane left by the source file --
# would sit under the grid at the wrong size. Hide it; this is a catalogue.
for o in bpy.data.objects:
    if o.type == 'MESH' and o not in pieces:
        o.hide_render = True

x, y, row_d, placed = 0.0, 0.0, 0.0, []
for o in pieces:
    lo, hi = wbb(o)
    w, d = hi.x - lo.x, hi.y - lo.y
    if x > 0.0 and x + w > ROW_W:          # wrap
        y -= row_d + ROW_PAD
        x, row_d = 0.0, 0.0
    ctr = (lo + hi) / 2.0
    o.location += Vector((x + w / 2.0 - ctr.x, y - d / 2.0 - ctr.y, -lo.z))
    placed.append(o)
    x += w + PAD
    row_d = max(row_d, d)
bpy.context.view_layer.update()
print("GRID packed into %.1f m x %.1f m" % (ROW_W, -y + row_d))

# Flat, even light: a catalogue, not a portrait. A hard sun throws one row's
# shadow across the next and the far rows go black.
R.engine(eevee=True, samples=64, res=(2400, 1500), transparent=False)
R.world(top=(0.78, 0.81, 0.85), bottom=(0.80, 0.78, 0.75), strength=3.6)
R.sun(energy=1.1, angle_deg=(42, 0, 28), softness=10.0)

lo, hi = R.bbox_of(placed)
tgt = (lo + hi) / 2.0
cam = R.camera(placed, yaw=-30, pitch=54, lens=70, margin=1.0, target=tgt)
R.fit(cam, placed, tgt, fill=(0.99, 0.975), centre=(0.5, 0.5))
sc = bpy.context.scene
sc.render.resolution_x = 2400
sc.render.resolution_y = 1500
R.save(OUT)
print("GRID wrote", OUT)
