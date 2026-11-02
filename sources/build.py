#!/usr/bin/env python3
"""Génère un projet HyperFrames pour une version (A/B/C/D) et un format (916/45).

Usage: python3 build.py A 916
Les temps viennent de la transcription mot à mot (assets/transcript_<V>.json).
"""
import json, sys, os, shutil, html

V, FMT = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "out", f"{V}_{FMT}")

W = 1080
H = 1920 if FMT == "916" else 1350
# Bande utile de 1270 px : 250..1520 en 9:16 (zones Reels), 40..1310 en 4:5
STAGE_TOP = 250 if FMT == "916" else 40
STAGE_H = 1270

INK, CREAM, RED = "#0B1426", "#F4F1EA", "#E63312"

words = json.load(open(os.path.join(SRC, f"transcript_{V}.json")))
cfg = json.load(open(os.path.join(SRC, "versions.json")))[V]
for i, t in cfg.get("fix", {}).items():
    words[int(i)]["text"] = t
DUR = cfg["duration"]

def w(i):
    return words[i]

def anchor(name):
    a = cfg["anchors"][name]
    return w(a)["start"] if isinstance(a, int) else a

FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 900; src: url('assets/fonts/inter-tight-latin-900-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 600; src: url('assets/fonts/inter-tight-latin-600-normal.woff2') format('woff2'); }
@font-face { font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; src: url('assets/fonts/instrument-serif-latin-400-italic.woff2') format('woff2'); }
"""

def fill(tpl, **kv):
    for k, v in kv.items():
        tpl = tpl.replace("{{" + k + "}}", str(v))
    return tpl

def r(x):
    return f"{x:.3f}"

# ---------------------------------------------------------------- scènes
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

common = dict(FONTS=FONTS, INK=INK, CREAM=CREAM, RED=RED, STAGE_TOP=STAGE_TOP,
              STAGE_H=STAGE_H, W=W, H=H)

# Scène 1 : hook (spécifique à chaque version)
hook = cfg["hook"]
s1_start, s1_end = 0, anchor("act1b") + 0.35
spans, tweens = [], []
for li, line in enumerate(hook["lines"]):
    parts = []
    for wi, (txt, idx, style) in enumerate(line["words"]):
        sid = f"h{li}_{wi}"
        cls = "hw " + style
        parts.append(f'<span id="{sid}" class="{cls}">{html.escape(txt)}</span>')
        t = w(idx)["start"] if isinstance(idx, int) else idx
        tweens.append((sid, t, line.get("mode", "light")))
    spans.append(f'<div class="hl {line.get("cls", "")}" id="hl{li}">{" ".join(parts)}</div>')
hook_lines_1 = "\n".join(s for s, l in zip(spans, hook["lines"]) if l.get("block", 1) == 1)
hook_lines_2 = "\n".join(s for s, l in zip(spans, hook["lines"]) if l.get("block", 1) == 2)
js = []
for sid, t, mode in tweens:
    if mode == "light" and t < 0.1:
        continue  # déjà allumé à la première image (vignette)
    if mode == "light":
        js.append(f'tl.fromTo("#{sid}", {{opacity: 0.4}}, {{opacity: 1, duration: 0.12, ease: "power2.out"}}, {r(max(0, t - 0.05))});')
    else:  # drop : le mot tombe et rebondit légèrement
        js.append(f'tl.fromTo("#{sid}", {{opacity: 0, y: -140, rotation: -4}}, {{opacity: 1, y: 0, rotation: 0, duration: 0.42, ease: "back.out(1.9)"}}, {r(max(0, t - 0.06))});')
compress_at = anchor("hook_compress") if "hook_compress" in cfg["anchors"] else None
fill_kw = dict(common, S1_DUR=r(s1_end - s1_start), HOOK1=hook_lines_1, HOOK2=hook_lines_2,
               HOOK_JS="\n    ".join(js), HOOK_SIZE=hook.get("size", 132),
               COMPRESS=r(compress_at) if compress_at is not None else "-1",
               EXIT=r(anchor("act1b") - 0.08), SPECIAL_JS=hook.get("js", ""),
               SPECIAL_CSS=hook.get("css", ""))
open(os.path.join(OUT, "compositions", "hook.html"), "w").write(
    fill(open(os.path.join(SRC, "hook.html")).read(), **fill_kw))

# Scène 2 : contrat en assurance
s2_start = anchor("act1b") - 0.1
s2_end = anchor("pivot") + 0.5
open(os.path.join(OUT, "compositions", "contrat.html"), "w").write(fill(
    open(os.path.join(SRC, "contrat.html")).read(), **common,
    S=r(s2_start), DUR=r(s2_end - s2_start),
    T_IN=r(anchor("act1b")), T_PRIME=r(anchor("primes")),
    T_COUV=r(anchor("couverture")), T_FRAIS=r(anchor("frais"))))

# Scène 3 : banque
s3_start = anchor("pivot") - 0.12
s3_end = anchor("attention") + 0.4
open(os.path.join(OUT, "compositions", "banque.html"), "w").write(fill(
    open(os.path.join(SRC, "banque.html")).read(), **common,
    S=r(s3_start), DUR=r(s3_end - s3_start), T_TITLE=r(anchor("pivot")),
    TITLE_HTML=cfg["pivot_title"],
    T_FISCAL=r(anchor("fiscal")), T_MOINS=r(anchor("moins")), T_VERSEZ=r(anchor("versez")),
    T_OPEN=r(anchor("open")), T_SL1=r(anchor("sl1")), T_SL2=r(anchor("sl2")),
    T_SL3=r(anchor("sl3")), T_SLEND=r(anchor("attention") - 0.15)))

# Scène 4 : mais attention
s4_start = anchor("attention") - 0.08
s4_end = anchor("cta") + 0.45
open(os.path.join(OUT, "compositions", "attention.html"), "w").write(fill(
    open(os.path.join(SRC, "attention.html")).read(), **common,
    S=r(s4_start), DUR=r(s4_end - s4_start), T_MAIS=r(anchor("attention")),
    T_TOUTES=r(anchor("toutes")), T_RETRAITE=r(anchor("retraite")),
    T_ECART=r(anchor("ecart")), T_CURVES_END=r(anchor("cta") - 0.6)))

# Scène 5 : CTA
s5_start = anchor("cta") - 0.08
IRIS_X, IRIS_Y = 90 + 705, STAGE_TOP + 400 + 240
open(os.path.join(OUT, "compositions", "cta.html"), "w").write(fill(
    open(os.path.join(SRC, "cta.html")).read(), **common,
    S=r(s5_start), DUR=r(DUR - s5_start), T_IN=r(anchor("cta")),
    T_PILIER=r(anchor("cta_pilier")), T_BTN=r(anchor("gratuit")),
    T_END=r(DUR), IRIS_X=IRIS_X, IRIS_Y=IRIS_Y))

# ---------------------------------------------------------------- sous-titres
skip = set(range(*cfg["caption_skip"]))
breaks = set(cfg["caption_breaks"])  # index de mot qui commence forcément un groupe
red_words = set(cfg["caption_red"])
nobreak = set(cfg.get("caption_nobreak", []))
acts = [(0, "light"), (s3_start, "dark"), (s4_start, "light"), (s5_start, "dark")]

groups, cur = [], []
for i, wd in enumerate(words):
    if i in skip:
        continue
    if cur and i not in nobreak and (i in breaks or len(cur) >= 5 or wd["start"] - words[cur[-1]]["end"] >= 0.25
                or words[cur[-1]]["text"][-1] in ".?!,:…"):
        groups.append(cur); cur = []
    cur.append(i)
if cur:
    groups.append(cur)
# évite les mots isolés : on fusionne un groupe d'un mot avec le précédent si possible
merged = []
for g in groups:
    if merged and len(g) == 1 and len(merged[-1]) < 5 and g[0] not in breaks \
            and words[g[0]]["start"] - words[merged[-1][-1]]["end"] < 0.25:
        merged[-1] = merged[-1] + g
    else:
        merged.append(g)
groups = merged

cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.05, words[g[0]]["start"] - 0.08)
    nxt = words[groups[gi + 1][0]]["start"] - 0.08 if gi + 1 < len(groups) else DUR
    ge = min(nxt, words[g[-1]]["end"] + 0.5)
    tone = [a[1] for a in acts if gs >= a[0] - 1e-6][-1]
    late = " late" if gs >= s5_start else ""
    spans = []
    for k, i in enumerate(g):
        txt = words[i]["text"]
        txt = txt.replace("?", " ?").replace(":", " :")
        cls = "cw red" if i in red_words else "cw"
        spans.append(f'<span id="c{i}" class="{cls}">{html.escape(txt)}</span>')
        cap_js.append(f'tl.fromTo("#c{i}", {{opacity: 0.3, y: 10}}, {{opacity: 1, y: 0, duration: 0.14, ease: "power3.out"}}, {r(words[i]["start"])});')
    cap_html.append(f'<div id="cg{gi}" class="cg clip {tone}{late}" data-start="{r(gs)}" data-duration="{r(ge - gs)}" data-track-index="0">{" ".join(spans)}</div>')

open(os.path.join(OUT, "compositions", "captions.html"), "w").write(fill(
    open(os.path.join(SRC, "captions.html")).read(), **common, DUR=r(DUR),
    GROUPS="\n    ".join(cap_html), CAP_JS="\n    ".join(cap_js),
    CAP_TOP=STAGE_TOP + 1010, CAP_TOP_LATE=STAGE_TOP + 935))

# ---------------------------------------------------------------- racine
grain_js = [f"for (let k = 0; k < {int(DUR * 12)}; k++) {{",
            "  tl.set(\"#grain\", { backgroundPosition: `${(k * 173) % 512}px ${(k * 311) % 512}px` }, k / 12);",
            "}"]

hosts = [("hook", 0, s1_end, 1), ("contrat", s2_start, s2_end, 2), ("banque", s3_start, s3_end, 3),
         ("attention", s4_start, s4_end, 4), ("cta", s5_start, DUR, 5)]
host_html = "\n      ".join(
    f'<div id="{n_}" data-composition-id="{n_}" data-composition-src="compositions/{n_}.html" '
    f'data-start="{r(a)}" data-duration="{r(b - a)}" data-track-index="{ti}" data-track-kind="graphics" '
    f'data-width="{W}" data-height="{H}" style="z-index:{ti}"></div>' for n_, a, b, ti in hosts)

open(os.path.join(OUT, "index.html"), "w").write(fill(
    open(os.path.join(SRC, "index.html")).read(), **common, DUR=r(DUR), HOSTS=host_html,
    AUDIO=f"assets/mix_{V}.wav", GRAIN_JS="\n      ".join(grain_js)))

# assets
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
for f in ["grain.png", f"mix_{V}.wav"]:
    shutil.copy(os.path.join(SRC, "assets", f), os.path.join(OUT, "assets", f))
shutil.copytree(os.path.join(SRC, "assets", "fonts"), os.path.join(OUT, "assets", "fonts"), dirs_exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    if os.path.exists(os.path.join(SRC, f)):
        shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
print("ok", OUT, "groups:", len(groups))
for g in groups:
    print("  ", r(words[g[0]]["start"]), " ".join(words[i]["text"] for i in g))
