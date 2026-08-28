# Medieval Architecture Kit

A **modular half-timber building kit**, generated procedurally in Blender. Every piece is a
Python function on a shared 2 m grid, so the parts snap together into different buildings
rather than making one fixed model.

**184 pieces · 14 families · 276k triangles · 4 example buildings**

![The inn](images/inn.jpg)

---

## What's in it

Every piece in the kit. 1 Blender unit = 1 metre, one bay = 2 m:

![The whole kit](images/kit.jpg)

The red cube is 1 m:

![Kit at scale](images/kit-scale.jpg)

## The same parts make different buildings

![Three more buildings from the same kit](images/layouts.jpg)

A market row with an arcade and a gallery, a cottage, and an L-plan with a cross wing —
all from the pieces above, no new geometry:

| | |
|---|---|
| ![Market row](images/market-row.jpg) | ![Cottage](images/cottage.jpg) |

![L-plan with a cross wing](images/l-plan.jpg)

## Detail that survives a close-up

![Close detail](images/detail.jpg)

Where the range's roof meets the taller cross wing, the two eave lines sit **0.80 m apart**
— deliberately. The wing's datum has to stand above the range's or its roof planes never
cross the range's, and there is no valley line to lay:

![The two-eave junction](images/junction.jpg)

![Aerial](images/inn-aerial.jpg)

---

## Open it

```
models/inn_kit.blend       the library -- all 184 pieces, browsable, laid out by family
models/inn_kit.glb         the same, portable (Unity, Unreal, Godot, three.js, Maya)
models/inn_example.blend   the inn, assembled
models/inn_example.glb     the same, portable
models/layouts.blend       market row + cottage + L-plan
models/manifest.json       every piece with its family and triangle count
```

Each piece's **mesh** carries the canonical kit origin, so zeroing an object's location
snaps it to its convention position. That is how you assemble with them.

## Build it yourself

Needs Blender 4.x or 5.x. Nothing else — no addons, no dependencies.

```bash
blender -b --python build_kit.py                    # the whole kit -> out/inn_kit.blend + .glb
blender -b --python assemble_inn.py                 # the showpiece inn
blender -b --python assemble_layouts.py             # the other three buildings
blender -b --python build_piece.py -- roofs         # one family, with its own renders
blender -b --python kit_grid.py                     # the whole-kit image above
blender -b --python kit_sheet.py                    # per-family comparison sheets
```

The first three are self-contained — each builds the pieces it needs. `kit_grid.py` and
`kit_sheet.py` read `out/inn_kit.blend`, so run `build_kit.py` before them.

Builds land in `out/` and renders in `renders/`, both gitignored. `models/` holds the
prebuilt output so you don't have to run anything.

---

## How it fits together

Four conventions do all the work. They live in `kit/spec.py` and every piece obeys them.

**A wall** has its origin at the bay centre, `x ∈ [−1, +1]`, its outer face on `y = 0` with
the body toward `+y`. Two copies side by side tile with no seam.

**A corner** fills the `T × T` void *between* two wall runs. This is why any offset that is
not a whole multiple of the grid breaks a corner — it moves the corner piece out of the void
it exists to fill.

**One roof pitch, kit-wide.** Every roof piece is authored at 52° so any piece meets any
other. The assembler then presents the roof at 65° by stretching the whole roof world in Z
by `ZK = tan(65)/tan(52) = 1.675`, placing each piece at `z·ZK` with scale `(s, s, s·ZK)`.
A plane through a point scaled that way is unchanged, so every seam still meets — and one
constant changes the building's apparent pitch without re-authoring a single piece.

**Fractions are authored, not scaled.** A stretched moulding is a defect even when nothing
intersects, so the kit ships real part-pieces:

```
walls    2 m / 1 m / 0.5 m wide
         2.60 / 3.00 / 1.30 / 1.00 / 0.85 / 0.40 m tall
roof     panels of 13 / 7 / 3 shingle courses  (13 is odd, so a "half" cannot be
         half -- 7 + 3 + 3 = 13 exactly, and any remainder composes with no residue)
         eaves, ridges and valleys at 2 m / 1 m / 0.5 m
corners  the T x T void piece, inner and outer
```

**Openings are a contract.** `spec.py` declares each opening's width, height, sill and head;
walls cut them and inserts fill them, so any casement drops into any window bay unchanged.

---

## Checks

Every piece validates its own seams, bounds and triangle budget on build — a non-empty
report is a failure. On top of that:

```bash
blender -b --python check_holes.py      -- out/inn_example.blend   # see-through holes
blender -b --python check_layouts.py    -- out/layouts.blend       # through-roof + run gaps
blender -b --python check_collisions.py -- out/inn_example.blend   # interpenetration
ZFIGHT_TOL=0.0005 blender -b --python check_zfight.py -- roofs     # coincident surfaces
```

`check_holes.py` casts from *inside* the building outward: a ray that escapes is a hole you
could see through. It found one that twelve other checks and a dozen renders had missed.

For the defect it *can't* see — an inside face pointing outward, which is not a hole — swap
the back-face material for a flat emission colour and render from outside. Anything that
glows is facing the wrong way. That found the L-plan's inner corner, and cleared the rest of
the building in the same frame.

Current state of the four buildings:

```
inn          751 pieces placed, 0 missing
layouts      865 pieces placed, 0 missing
holes        0 escaping rays on the layouts; 4 (0.05%) on the inn, all at the
             foundation course, no visible gap
eave laps    12 pairs, all at 0.0000 m -- seam contact, no interpenetration
ridge        slope runs 0.127 m UNDER the cap -- a lap, not a gap
glTF         both .glb clean: every primitive carries UVs and COLOR_0
porch        shingle faces moved from a 0-10 deg cluster (39% of area) to
             20-30 deg (46%) -- the same structure as the main roof's 60-70
chimneys     all 8 stacks on their own haunch; the shaft-against-roof cut line
             measured 2,280 px before and 0 after, and its loose-stone fringe
             10,801 px before and 0 after
```

`build_piece.py` also reports a `clamped` count per family. A clamp is where a piece's
relief is cut flat at a seam — which is how tiling is *supposed* to work for a stone wall
(12 of 12 clamp by design) and a bug when it deforms a roof. It is deliberately separate
from `fails`, and it is now printed, because it was possible to quote "every piece reports
EMPTY" while 37 pieces across the kit were silently crushing vertices.

---

## Known issues

Measured, not guessed. These are open:

- **Six 1–3 px pale slivers** show on two dormer cheeks at oblique angles. Measured: they are
  not back faces at all — every pixel is a *front* face, the window's backing plate seen
  through its own jamb past a 72 mm unlined void behind the glazing frame, which opens at 31°
  off the face normal. The fix is two lines in `Part.glazing`, but it adds 562 cm² of
  near-coplanar surface to `SM_Gable_WinFrame`, so it is not landed until that is resolved.
- **`Blk.zsurf()` returns the NOMINAL roof plane, not the shingle surface.** Measured over 17
  raycasts, the skin stands **0.091–0.190 m in z above it** (0.038–0.080 perpendicular). The
  chimney haunch now compensates with its own `ROOF_SKIN`, but anything else bedded on
  `zsurf()` — dormers, moss drifts — is buried 38–80 mm deeper than intended. That is the safe
  direction (buried, not floating), which is why it is here and not in the fix list.
- **`SM_Chimney_Cap_Roof`, `SM_Roof_Flash_Wall_2m` and `SM_Dormer_Flash_Valley` are still
  placed zero times.** The first is an alternative to the pots the buildings use; the other two
  are for conditions the four example buildings do not have.
- Bargeboards on a cross-wing gable legitimately rise above the roof they cross;
  `check_layouts.py` annotates those rows rather than filtering them.

---

## How this was built

Procedurally, by a loop of builder / auditor / blind-critic agents that had to prove each
fix with a measurement rather than assert it. The reusable version of that apparatus — the
validators, the fault taxonomy and the loop — is a Claude Code skill:

**→ [Lunarsong/architecture-kit](https://github.com/Lunarsong/architecture-kit)** — build a
kit like this one for any architectural style.

MIT licensed.
