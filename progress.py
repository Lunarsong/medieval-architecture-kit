#!/usr/bin/env python3
"""Generate the live progress page. Re-run it any time; it reads the real state
off disk (which modules exist, what has been rendered, how many blind judging
rounds each family has been through) and merges in verdicts from state.json.

    python3 progress.py     -> inn_kit_progress.html AND progress.html
                               (identical; either file:// bookmark works)
"""
import os, sys, json, base64, io, re, time, glob
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
REFS = {"ref1": "/Users/shanee/Downloads/fantasy_inn.jpg",
        "ref2": "/Users/shanee/Downloads/Inn.jpg",
        "ref3": "/Users/shanee/Downloads/inn - greyscale.jpg"}

FAM_ORDER = ["stone_walls", "timber_walls", "corners", "beams", "roofs", "gables",
             "dormers", "chimneys", "doors", "windows", "signage", "props", "ground"]
FAM_LABEL = {
    "stone_walls": "Stone walls", "timber_walls": "Half-timber walls",
    "corners": "Corners & posts", "beams": "Beams & corbels", "roofs": "Roof system",
    "gables": "Gables & bargeboards", "dormers": "Dormers", "chimneys": "Chimneys",
    "doors": "Doors & porches", "windows": "Windows & flower boxes",
    "signage": "Signs & lanterns", "props": "Barrels & clutter",
    "ground": "Steps, cobbles & well",
}


def b64(path, w=760, q=80, fmt="JPEG"):
    im = Image.open(path).convert("RGB")
    if im.width > w:
        im = im.resize((w, max(1, int(im.height * w / im.width))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, fmt, quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def family_state(fam, state):
    d = {"key": fam, "label": FAM_LABEL.get(fam, fam), "rounds": 0, "status": "queued",
         "tris": 0, "pieces": 0, "gap": "", "why": "", "shot": None, "shot_kind": ""}
    if os.path.exists(f"{ROOT}/kit/pieces/{fam}.py"):
        d["status"] = "building"
    rounds = set()
    for p in glob.glob(f"{ROOT}/cmp/{fam}_r*_*.png"):
        m = re.search(rf"{fam}_r(\d+)_", os.path.basename(p))
        if m:
            rounds.add(int(m.group(1)))
    if rounds:
        d["rounds"] = max(rounds)
        d["status"] = "judging"
    for kind in ("demo", "closeup", "lineup", "tiled"):
        p = f"{ROOT}/renders/{fam}/{kind}.png"
        if os.path.exists(p):
            d["shot"], d["shot_kind"] = p, kind
            break
    st = (state.get("families") or {}).get(fam)
    if st:
        d.update({k: v for k, v in st.items() if v not in (None, "")})
    man = state.get("_manifest") or {}
    ps = [m for m in man.get("pieces", []) if m["family"] == fam]
    if ps:
        d["pieces"] = len(ps)
        d["tris"] = sum(m["tris"] for m in ps)
        d["fails"] = sum(1 for m in ps if m["report"])
    return d


CSS = """
:root{
  --ground:#E7E3DA; --surface:#F3F0EA; --sunk:#DBD6CB; --line:#C9C2B4;
  --ink:#24272B; --muted:#6B6A64; --faint:#8D8B83;
  --accent:#7A5232; --good:#4E6B2C; --warn:#9E7220; --cool:#4F6270;
  --shadow:0 1px 2px rgba(36,39,43,.07), 0 8px 24px -16px rgba(36,39,43,.28);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#17191A; --surface:#212426; --sunk:#111314; --line:#33383A;
  --ink:#E7E3DA; --muted:#9B9A93; --faint:#7C7B75;
  --accent:#C48E5E; --good:#8FA758; --warn:#D8A845; --cool:#7C909C;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.7);
}}
:root[data-theme="dark"]{
  --ground:#17191A; --surface:#212426; --sunk:#111314; --line:#33383A;
  --ink:#E7E3DA; --muted:#9B9A93; --faint:#7C7B75;
  --accent:#C48E5E; --good:#8FA758; --warn:#D8A845; --cool:#7C909C;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.7);
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:38px 24px 80px}
.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}
h1{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:clamp(34px,5vw,58px);
  line-height:1.02;letter-spacing:-.01em;margin:0 0 10px;text-wrap:balance}
h2{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:27px;margin:0 0 4px}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint)}
.lede{color:var(--muted);max-width:66ch;margin:0 0 6px}
header{border-bottom:1px solid var(--line);padding-bottom:26px;margin-bottom:26px}

.tally{display:flex;flex-wrap:wrap;gap:0;margin:22px 0 0;border:1px solid var(--line);
  border-radius:3px;background:var(--surface);overflow:hidden}
.tally div{flex:1 1 130px;padding:13px 16px;border-right:1px solid var(--line)}
.tally div:last-child{border-right:none}
.tally b{display:block;font-family:"IBM Plex Mono",monospace;font-size:23px;
  font-variant-numeric:tabular-nums;line-height:1.2}
.tally span{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);
  font-family:"IBM Plex Mono",monospace}

section{margin:44px 0 0}
.bar{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
.bar3{grid-template-columns:1.25fr 1fr 1fr}
.bar figcaption b{font-family:"IBM Plex Sans",sans-serif;color:var(--ink);font-weight:600}
.bar figure{margin:0;border:1px solid var(--line);background:var(--surface);border-radius:3px;
  overflow:hidden}
.bar img{display:block;width:100%;height:auto}
.bar figcaption{padding:9px 12px;font-size:12px;color:var(--muted);
  font-family:"IBM Plex Mono",monospace;border-top:1px solid var(--line)}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(322px,1fr));gap:16px;margin-top:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:3px;
  box-shadow:var(--shadow);overflow:hidden;display:flex;flex-direction:column;
  border-left:3px solid var(--cool)}
.card.won{border-left-color:var(--good)}
.card.judging{border-left-color:var(--warn)}
.card.building{border-left-color:var(--accent)}
.card.queued{border-left-color:var(--line)}
.card .top{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  padding:13px 15px 9px}
.card h3{margin:0;font-size:16px;font-weight:600;letter-spacing:-.01em}
.chip{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 7px;border-radius:2px;white-space:nowrap;
  border:1px solid currentColor}
.chip.won{color:var(--good)} .chip.judging{color:var(--warn)}
.chip.building{color:var(--accent)} .chip.queued{color:var(--faint)}
.shot{background:var(--sunk);border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  aspect-ratio:16/10;display:flex;align-items:center;justify-content:center;overflow:hidden}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.shot .empty{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);
  letter-spacing:.1em;text-transform:uppercase}
.meta{display:flex;gap:14px;padding:10px 15px 2px;font-family:"IBM Plex Mono",monospace;
  font-size:11.5px;color:var(--muted);font-variant-numeric:tabular-nums}
.pips{display:flex;gap:4px;align-items:center;padding:8px 15px 0}
.pip{width:7px;height:7px;border-radius:50%;background:var(--line)}
.pip.on{background:var(--warn)} .pip.win{background:var(--good)}
.pips small{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--faint);
  letter-spacing:.08em;margin-left:5px;text-transform:uppercase}
.gap{padding:9px 15px 15px;font-size:13px;color:var(--muted);border-top:0}
.gap b{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint);display:block;margin-bottom:2px;font-weight:400}
.hero img{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:3px}
.files{margin-top:18px;border:1px solid var(--line);border-radius:3px;background:var(--surface)}
.files div{padding:11px 15px;border-bottom:1px solid var(--line);display:flex;gap:12px;
  align-items:baseline;flex-wrap:wrap}
.files div:last-child{border-bottom:none}
.files code{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink)}
.files em{font-style:normal;color:var(--faint);font-size:12px}
footer{margin-top:52px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);
  font-size:12px;font-family:"IBM Plex Mono",monospace}
@media (max-width:640px){.bar{grid-template-columns:1fr}}
"""


def render(state):
    fams = [family_state(f, state) for f in FAM_ORDER]
    won = [f for f in fams if f["status"] == "won"]
    judging = [f for f in fams if f["status"] == "judging"]
    building = [f for f in fams if f["status"] == "building"]
    total_tris = sum(f["tris"] for f in fams)
    total_pieces = sum(f["pieces"] for f in fams)
    stamp = time.strftime("%H:%M")

    cards = []
    for f in fams:
        st = f["status"]
        shot = (f'<img src="{b64(f["shot"], 700, 78)}" alt="{f["label"]} render">'
                if f.get("shot") else '<span class="empty">no render yet</span>')
        pips = "".join(
            f'<i class="pip {"win" if (st == "won" and i + 1 == f["rounds"]) else "on"}"></i>'
            for i in range(f["rounds"])) or '<i class="pip"></i>'
        note = f.get("gap") or f.get("why") or ""
        note_label = "Verdict" if st == "won" else "Critic's biggest gap"
        meta = []
        if f["pieces"]:
            meta.append(f'{f["pieces"]} pieces')
            meta.append(f'{f["tris"]:,} tris')
        if f.get("fails"):
            meta.append(f'{f["fails"]} failing checks')
        cards.append(f"""
      <article class="card {st}">
        <div class="top"><h3>{f['label']}</h3><span class="chip {st}">{st}</span></div>
        <div class="shot">{shot}</div>
        <div class="pips">{pips}<small>{f['rounds'] or 0} blind round{'' if f['rounds']==1 else 's'}{' · ' + f['shot_kind'] if f.get('shot_kind') else ''}</small></div>
        {f'<div class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</div>' if meta else ''}
        {f'<div class="gap"><b>{note_label}</b>{note}</div>' if note else ''}
      </article>""")

    hero = ""
    for name, cap in (("inn_ref1.png", "Assembled inn — warm street view, matched to reference 1"),
                      ("inn_ref2.png", "Assembled inn — elevated 3/4, matched to reference 2")):
        p = f"{ROOT}/renders/inn/{name}"
        if os.path.exists(p):
            hero += (f'<figure style="margin:0 0 16px"><img src="{b64(p, 1100, 82)}" alt="{cap}">'
                     f'<figcaption class="eyebrow" style="padding-top:8px">{cap}</figcaption></figure>')
    hero_sec = f"""
    <section class="hero">
      <span class="eyebrow">Assembled from kit pieces only</span>
      <h2>The example inn</h2>
      {hero}
    </section>""" if hero else ""

    # ---- the full reference wall Shanee has supplied over the project ----------
    ref_files = [("refs/r6.jpg",  "r6 — a 3D <em>render</em>, not a painting: shows what is reachable in geometry. White render dominant, narrow dark studs, fine slate courses, arcaded ground floor."),
                 ("refs/r7.jpg",  "r7 — the same build three-quarter on. Multiple roof wings at different heights."),
                 ("refs/r10.jpg", "r10 — the clearest jetty in the set: upper floor cantilevered on brackets, timber gallery, outside stair, stone base."),
                 ("refs/r9.jpg",  "r9 — round-arched arcade, lit lanterns, tables out front, cobbles."),
                 ("refs/r11.jpg", "r11 — steep multi-gable roofline over a ground-level arcade."),
                 ("refs/r5.jpg",  "r5 — classic cream-panel inn: corner post, flower boxes, timber as a drawn lattice."),
                 ("refs/r8.jpg",  "r8 — gallery over an open ground floor, barrels stacked beneath."),
                 ("refs/r4.jpg",  "r4 — night, half-timber over an arched door.")]
    ref_cards = ""
    for rel, cap in ref_files:
        fp = os.path.join(ROOT, rel)
        if os.path.exists(fp):
            ref_cards += (f'<figure><img src="{b64(fp, 560, 78)}" alt="{rel}">'
                          f'<figcaption>{cap}</figcaption></figure>')
    refwall = f"""
    <section>
      <span class="eyebrow">Added 24 August</span>
      <h2>Eight more references</h2>
      <p class="lede">Saved into the repo at <code>refs/</code> so they travel with it, and
      wired into <code>compare.py</code> so a critic can be pointed at any of them. Two
      features recur across these that the kit could not build at all — an arcaded
      undercroft at ground level, and a timber gallery over it. Both are now being built.</p>
      <div class="grid">{ref_cards}</div>
    </section>""" if ref_cards else ""

    # ---- what the loop actually found, with the evidence ------------------------
    findings = [
      ("The paving was never missing",
       "Three of my diagnoses were wrong — absent, then mis-placed, then low contrast. "
       "Two agents independently traced it to one number in <code>render.py</code>: the "
       "ref1 backdrop plane sat at exactly z=0.0, the same plane the paving's top is "
       "pinned to, burying all 83 patches. Every other preset already used −0.02.",
       "renders/inn/inn_ref1.png"),
      ("The facade was brown because of a boarded variant, not the studs",
       "Wall variant <code>C</code> is the boarded-siding one. When I removed the "
       "wood-heavy fake-jetty panels I replaced them with <code>c</code> — trading one "
       "timber-heavy variant for another. Separately the pieces were measured at 63.0% "
       "timber face and slimmed to 50.7%, and the assembler was darkening the bottom "
       "0.55 m of every panel to 0.70, undoing it.", None),
      ("Jettying is a cantilever, not an offset",
       "Sliding wall planes by a sub-grid amount is not jettying and broke the grid the "
       "kit rests on. The glossary names the members: a jetty plate on the wall head, "
       "joists cantilevered over it, a bressumer closing their ends carrying the wall "
       "above, brackets beneath, and a dragon beam diagonally at corners. The kit had "
       "the bressumer and brackets but nothing to close the underside — which is why it "
       "could not be assembled from tiles.",
       "renders/beams/demo.png"),
      ("Two measuring tools, and both of mine were wrong first",
       "<code>check_zfight.py</code> finds coplanar faces; <code>check_collisions.py</code> "
       "finds solids pushed through each other. The z-fight tool once reported a chimney "
       "at 177,748 cm² when the truth was zero — a term in its distance test matched the "
       "two outward faces of any origin-centred box. The collision tool needed a depth "
       "discriminator, because kit pieces are <em>designed</em> to butt and a BVH counts "
       "that as intersecting.", None),
      ("&ldquo;The roof goes through the walls&rdquo; was not the roof",
       "Shanee reported it and my first measurement agreed for the wrong reason: I "
       "compared bounding-box heights and concluded the wall stood 0.9&nbsp;m through "
       "the roof. Ray-casting the actual surfaces found something far smaller and far "
       "more specific &mdash; 38 vertices on 2 pieces of 824. The swept eave course "
       "curls down steeply, so where it crosses the wall plane its shingle surface sits "
       "at 9.84 against a roof datum of 9.95. The wall was built to the datum, so its "
       "flat top face was left standing 40&ndash;110&nbsp;mm out on the shingles, and "
       "from above that reads as a loose dark beam lying along the roof. A gable face "
       "wants that full height &mdash; the gable sits on it &mdash; so only "
       "<em>eave</em>-face bands now stop short of it. Protrusion measured back to zero."
       "<br><br>The same frame carries the other half of the story. The valley had been "
       "reported twice as &ldquo;2 pieces separated&rdquo;, and I had tried to hide the "
       "join by widening each length 12&nbsp;% and lifting it 55&nbsp;mm. The roofs agent "
       "measured what that actually did: the widened piece advances 1.103 per step while "
       "the assembler steps 0.985, so every length splayed 2.6&deg; off the true valley "
       "line and overlapped its neighbour by 12&nbsp;% &mdash; a 0.19&nbsp;m step every "
       "2.53&nbsp;m, upper sheet floating 0.178&nbsp;m clear. My fix <em>was</em> the "
       "defect. Once the piece learned to lap on its own, dropping the widen and the lift "
       "gave one continuous lead gutter with a welt at each lap.",
       "renders/analysis/junction_ba.png"),
      ("Determinism was false for every family that wobbles",
       "<code>mathutils.noise</code> is seeded per Blender <em>process</em>, and "
       "<code>Part.wobble</code> displaces every vertex by it — so identical code produced "
       "different meshes each run, measurements would not repeat, and bugs flickered in "
       "and out between builds. Three lines in <code>util.py</code>; now byte-identical "
       "across processes.", None),
    ]
    fcards = ""
    for title, body, img in findings:
        shot = ""
        fp = os.path.join(ROOT, img) if img else None
        if fp and os.path.exists(fp):
            shot = f'<div class="shot"><img src="{b64(fp, 700, 78)}" alt="{title}"></div>'
        fcards += (f'<article class="card building"><div class="top"><h3>{title}</h3></div>'
                   f'{shot}<div class="gap">{body}</div></article>')
    analysis = f"""
    <section>
      <span class="eyebrow">What the loop found</span>
      <h2>Analysis</h2>
      <p class="lede">The useful output of this process was not only fixes — it was
      diagnoses, several of which corrected me. These are the ones that changed how the
      kit is built.</p>
      <div class="grid">{fcards}</div>
    </section>"""

    ta = f"{ROOT}/renders/texture/untextured.png"
    tb = f"{ROOT}/renders/texture/textured.png"
    LAYOUTS = [("market_row.png", "Market Row", "319 pieces",
                "An arcaded undercroft on six open arches with stalls and barrels under "
                "it, a bressumer string course over them, and a timber gallery turning "
                "the corner on turned balusters, reached by an outside stair."),
               ("cottage.png", "Cottage", "103 pieces",
                "Two bays, one deep: a stone storey, an attic band, one dormer, one "
                "chimney. This is the harder direction &mdash; a kit that only makes one "
                "big showpiece is not modular."),
               ("l_plan.png", "L-Plan", "369 pieces",
                "Two wings at a right angle, so the corners, the valley where the roofs "
                "meet and the inner corner all get exercised at a plan the inn never "
                "uses. It was put in to find bugs, and it did.")]
    lay_cards = ""
    for fn, title, count, body in LAYOUTS:
        fp = f"{ROOT}/renders/layouts/{fn}"
        if not os.path.exists(fp):
            continue
        lay_cards += (f'<article class="card building"><div class="top"><h3>{title}</h3>'
                      f'<span class="pill">{count}</span></div>'
                      f'<div class="shot"><img src="{b64(fp, 700, 78)}" alt="{title}"></div>'
                      f'<div class="gap">{body}</div></article>')
    lay_all = f"{ROOT}/renders/layouts/all.png"
    lay_sec = ""
    if lay_cards:
        sheet = ""
        if os.path.exists(lay_all):
            sheet = (f'<div class="bar" style="grid-template-columns:1fr"><figure>'
                     f'<img src="{b64(lay_all, 1500, 82)}" alt="All three layouts at the same scale">'
                     f'<figcaption>the three at the same scale, so the shared vocabulary '
                     f'is obvious &mdash; same carpenter, three buildings</figcaption>'
                     f'</figure></div>')
        lay_sec = f"""
    <section>
      <span class="eyebrow">Different layouts, same kit</span>
      <h2>It makes more than one building</h2>
      <p class="lede">The brief asked for pieces that combine into different layouts, and
      for a long time that was a claim rather than a demonstration: 144 pieces and exactly
      one inn. These are three more buildings assembled from the same parts, by a script
      that imports the inn's assembler as a library rather than copying it. Every one
      reports no missing pieces.</p>
      {sheet}
      <div class="grid">{lay_cards}</div>
    </section>"""

    tex_sec = ""
    if os.path.exists(ta) and os.path.exists(tb):
        tex_sec = f"""
    <section>
      <span class="eyebrow">Colour and texture</span>
      <h2>Texturable, not locked</h2>
      <p class="lede">Every piece ships with two UV sets — one at world scale, where
      1 UV unit is 1 metre, so a tiling texture lands at the same density on a barrel
      as on a wall; and one packed into 0–1 for baking or hand-painting. Each material
      has a texture slot already wired and switched off, so texturing the kit means
      loading an image, not rewiring shaders. Seven seamless 1&nbsp;m textures are
      included as a starting set.</p>
      <div class="bar" style="grid-template-columns:1fr">
        <figure><img src="{b64(ta, 1000, 82)}" alt="Kit pieces with vertex colour only">
          <figcaption>palette colour × per-piece vertex-colour jitter — no textures at all</figcaption></figure>
        <figure><img src="{b64(tb, 1000, 82)}" alt="Kit pieces with tiling textures">
          <figcaption>the same pieces with the tiling textures switched on — grain on
          the timber, tooth on the plaster, grain inside each modelled stone</figcaption></figure>
      </div>
    </section>"""

    return f"""<title>Inn Kit Gauntlet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <span class="eyebrow">Modular 3D asset kit · procedural Blender build</span>
    <h1>A medieval inn, built piece by piece<br>until it beats the painting</h1>
    <p class="lede">Every family of parts is built by one agent, then judged by a
    different one that sees our render and a crop of the reference side by side with
    the labels stripped. If the painting wins, it goes back to the builder. These are
    the actual renders coming out of that loop.</p>
    <div class="tally">
      <div><b style="color:var(--good)">{len(won)}</b><span>won blind</span></div>
      <div><b style="color:var(--warn)">{len(judging)}</b><span>in judging</span></div>
      <div><b style="color:var(--accent)">{len(building)}</b><span>building</span></div>
      <div><b>{total_pieces or '—'}</b><span>kit pieces</span></div>
      <div><b>{f'{total_tris:,}' if total_tris else '—'}</b><span>triangles</span></div>
    </div>
  </header>

  <section>
    <span class="eyebrow">The bar</span>
    <h2>Three references</h2>
    <p class="lede">Nothing is compared against a description of these. Each critic
    gets pixel crops of the regions that matter to its family — the dormer run for the
    dormer builder, the bargeboard for the gable builder.</p>
    <div class="bar bar3">
      <figure><img src="{b64(REFS['ref3'], 700, 80)}" alt="Greyscale line reference">
        <figcaption><b>ref3 · the form reference</b> — same building as ref2 in
        linework. No colour to win on, so it is the fairest comparison for our grey
        renders, and it reads like a construction drawing: framing layout, ridge
        cresting, scalloped bargeboards, dentil courses.</figcaption></figure>
      <figure><img src="{b64(REFS['ref2'], 700, 80)}" alt="Reference painting 2">
        <figcaption>ref2 · coaching inn — mossy shingles, dormer run, flower boxes</figcaption></figure>
      <figure><img src="{b64(REFS['ref1'], 700, 80)}" alt="Reference painting 1">
        <figcaption>ref1 · warm sunlit street view — swept eaves, rubble base, barrels</figcaption></figure>
    </div>
  </section>

  <section>
    <span class="eyebrow">13 families · builder and critic per family, fresh context each round</span>
    <h2>The gauntlet</h2>
    <div class="grid">{''.join(cards)}</div>
  </section>
{hero_sec}
{refwall}
{analysis}
{lay_sec}
{tex_sec}
  <section>
    <span class="eyebrow">Deliverables</span>
    <h2>What you open</h2>
    <div class="files">
      <div><code>inn_kit/out/inn_kit.blend</code><em>the whole kit, one file, pieces laid
        out in rows by family</em></div>
      <div><code>inn_kit/out/inn_kit.glb</code><em>same kit as glTF — Unity, Unreal,
        Godot, three.js, or straight back into Blender. Carries vertex colours.</em></div>
      <div><code>inn_kit/out/inn_example.blend</code><em>the example inn, assembled
        from kit pieces only</em></div>
      <div><code>inn_kit/kit/pieces/*.py</code><em>every piece is code — regenerate or
        tweak any of it and rebuild</em></div>
    </div>
  </section>

  <footer>Page regenerated {stamp} · 1 Blender unit = 1 metre · {2.0}m grid module ·
  52° roof pitch across every roof piece</footer>
</div>"""


if __name__ == "__main__":
    state = {}
    sp = os.path.join(ROOT, "state.json")
    if os.path.exists(sp):
        state = json.load(open(sp))
    mp = os.path.join(ROOT, "out", "manifest.json")
    if os.path.exists(mp):
        state["_manifest"] = json.load(open(mp))
    html = render(state)
    # Write BOTH filenames with identical content. They diverged only because the
    # Artifact tool binds a file path to one published artifact, so when the first
    # artifact errored the output path had to change to claim a new URL -- which left
    # progress.html orphaned and silently 14 hours stale while it was still a
    # perfectly valid-looking file:// bookmark. Never again: either path is current.
    for name in ("inn_kit_progress.html", "progress.html"):
        out = os.path.join(ROOT, name)
        open(out, "w").write(html)
    print(f"wrote inn_kit_progress.html and progress.html ({len(html)/1024:.0f} KB each)")
