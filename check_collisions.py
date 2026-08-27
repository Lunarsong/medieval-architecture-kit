"""Find PLACED pieces that interpenetrate in the assembled inn.

    blender -b --python check_collisions.py            # builds the inn, then checks
    blender -b out/inn_example.blend --python check_collisions.py -- --loaded

Different problem from check_zfight.py. That one finds two faces in the SAME plane
(flicker). This one finds two SOLIDS pushed through each other -- a porch post
standing inside a barrel, a dormer buried in an eave. Kit pieces are meant to TOUCH,
so touching is not the signal; depth of mutual penetration is.

Reports object pairs ranked by how many face pairs actually intersect, with the two
piece names, so a placement bug can be found by name rather than by hunting.
"""
import bpy, sys, os, json
from mathutils.bvhtree import BVHTree
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

if "--loaded" not in argv:
    import assemble_inn                      # builds the inn into the scene
    if hasattr(assemble_inn, "build_inn"):
        assemble_inn.build_inn()

MIN_PAIRS = 6          # below this, pieces are just touching or grazing
MIN_DEPTH = 0.020      # metres of mutual bbox overlap on the SHALLOWEST axis.
# This is the discriminator that matters. Kit pieces are DESIGNED to butt, and two
# butted pieces share coincident faces which a BVH counts as intersecting -- so face
# count alone flags every cobble against its neighbour and every roof course against
# the next. A butt joint has ~0 overlap on the axis it butts along; a post standing
# inside a barrel overlaps on all three. Require real depth.
bpy.context.view_layer.update()

objs = [o for o in bpy.data.objects
        if o.type == 'MESH' and o.data.polygons
        and not any(c.name == "_library" for c in o.users_collection)
        and not o.name.startswith(("Ground", "KeySun", "Fill", "Cam"))]
print(f"COLLISION checking {len(objs)} placed pieces")

# world-space bounds + BVH per object
info = []
for o in objs:
    mw = o.matrix_world
    vs = [mw @ v.co for v in o.data.vertices]
    if not vs:
        continue
    lo = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    hi = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    polys = [tuple(p.vertices) for p in o.data.polygons]
    info.append((o, lo, hi, vs, polys))

def boxes_overlap(a_lo, a_hi, b_lo, b_hi, pad=-0.004):
    # negative pad: require real overlap, not a shared face
    return all(min(a_hi[i], b_hi[i]) - max(a_lo[i], b_lo[i]) > pad for i in range(3))

trees = {}
def tree_for(idx):
    t = trees.get(idx)
    if t is None:
        _, _, _, vs, polys = info[idx]
        t = BVHTree.FromPolygons(vs, polys, all_triangles=False, epsilon=0.0)
        trees[idx] = t
    return t

hits = []
n = len(info)
for i in range(n):
    oi, lo_i, hi_i, _, _ = info[i]
    for j in range(i + 1, n):
        oj, lo_j, hi_j, _, _ = info[j]
        if not boxes_overlap(lo_i, hi_i, lo_j, hi_j):
            continue
        depth = min(min(hi_i[k], hi_j[k]) - max(lo_i[k], lo_j[k]) for k in range(3))
        if depth < MIN_DEPTH:
            continue                       # butting, not interpenetrating
        ov = tree_for(i).overlap(tree_for(j))
        if len(ov) >= MIN_PAIRS:
            hits.append((len(ov), oi.name, oj.name,
                         tuple(round(c, 2) for c in ((lo_i + hi_i) / 2)), round(depth, 3)))

hits.sort(reverse=True)
print(f"\nCOLLISION {len(hits)} interpenetrating pairs "
      f"(>= {MIN_PAIRS} faces AND >= {MIN_DEPTH*1000:.0f}mm depth on every axis)\n")
for cnt, a, b, at, dep in hits[:40]:
    print(f"  {cnt:5d} faces {dep*1000:5.0f}mm  {a:32s} x  {b:32s} near {at}")

# group by the piece TYPES involved, which is what points at a placement rule
from collections import Counter
def base(nm):
    return nm.split('.')[0]
byk = Counter()
for cnt, a, b, _, _d in hits:
    byk[tuple(sorted((base(a), base(b))))] += 1
print("\nCOLLISION_BY_TYPE")
for k, v in byk.most_common(20):
    print(f"  {v:4d} placements   {k[0]}  x  {k[1]}")
json.dump([dict(faces=c, a=a, b=b, at=list(t), depth=d) for c, a, b, t, d in hits],
          open(os.path.join(ROOT, "out", "collisions.json"), "w"), indent=1)
