#!/usr/bin/env python3
"""Version C « 3D soft » : images FLORA animées en 2.5D + typo + sous-titres.

Usage: python3 build_soft.py 916|45
"""
import json, sys, os, shutil, html

FMT = sys.argv[1] if len(sys.argv) > 1 else "916"
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "out", f"C_{FMT}")
W = 1080
H = 1920 if FMT == "916" else 1350
# En 4:5 on garde la même mise en page et on décale tout vers le haut
DY = 0 if FMT == "916" else -210
INK, CREAM, RED = "#0B1426", "#F4F1EA", "#E63312"

words = json.load(open(os.path.join(SRC, "transcript_C.json")))
FIX = {1: "3ème", 2: "pilier,", 10: "vendu ?", 17: "3ème", 18: "pilier", 34: "part",
       49: "banque\u202f?", 51: "avantage", 52: "fiscal,", 67: "attention :", 89: "3ème", 90: "pilier", 91: "A",
       107: "à optimiser."}
for i, t in FIX.items():
    words[i]["text"] = t
DUR = 39.24

def s(i):
    return words[i]["start"]

def r(x):
    return f"{x:.3f}"

FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 900; src: url('assets/fonts/inter-tight-latin-900-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 600; src: url('assets/fonts/inter-tight-latin-600-normal.woff2') format('woff2'); }
@font-face { font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; src: url('assets/fonts/instrument-serif-latin-400-italic.woff2') format('woff2'); }
"""

BASE_CSS = f"""
{FONTS}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
.all {{ position: absolute; inset: 0; }}
.bg {{ position: absolute; inset: 0; }}
.cam {{ position: absolute; inset: 0; }}
.cam img {{ position: absolute; left: 0; top: {-7 + DY}px; width: 1080px; height: 1935px; }}
.t {{ position: absolute; left: 90px; right: 90px; font-family: 'Inter Tight'; font-weight: 900; letter-spacing: -0.045em; line-height: 0.95; white-space: nowrap; }}
.t em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; letter-spacing: -0.01em; font-size: 1.18em; }}
.w {{ display: inline-block; }}
.cream {{ color: {CREAM}; }} .ink {{ color: {INK}; }} .red {{ color: {RED}; }}
.kick {{ position: absolute; left: 90px; font-family: 'Inter Tight'; font-weight: 800; font-size: 30px; letter-spacing: 0.16em; text-transform: uppercase; }}
.chip {{ position: absolute; font-family: 'Inter Tight'; font-weight: 800; font-size: 32px; letter-spacing: 0.06em; text-transform: uppercase; padding: 12px 22px; border-radius: 40px; white-space: nowrap; }}
.chip.d {{ background: rgba(11, 20, 38, 0.82); color: {CREAM}; border: 2px solid rgba(244, 241, 234, 0.25); }}
.chip.r {{ background: {RED}; color: {CREAM}; }}
.badge {{ position: absolute; left: 90px; display: flex; gap: 16px; align-items: center; font-family: 'Inter Tight'; font-weight: 900; font-size: 52px; letter-spacing: -0.035em; color: {INK}; white-space: nowrap; }}
.badge i {{ display: inline-flex; width: 62px; height: 62px; border-radius: 50%; background: {RED}; color: {CREAM}; align-items: center; justify-content: center; font-style: normal; font-size: 36px; font-weight: 900; }}
"""

def scene(sid, start, dur, body, js, css=""):
    return f"""<template>
  <style>
    {BASE_CSS}
    {css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    {body}
  </div>
  <script>
    const S = {r(start)};
    const L = (g) => Math.max(0, g - S);
    const tl = gsap.timeline({{ paused: true }});
    {js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""

def words_html(prefix, idxs, extra_cls=""):
    return " ".join(f'<span id="{prefix}{i}" class="w {extra_cls}">{html.escape(words[i]["text"])}</span>' for i in idxs)

scenes = []

# ---------------------------------------------------------------- 1 · hook
s1_end = s(11) + 0.35
body = f"""
<div class="all" id="s1-all">
  <div class="cam" id="s1-cam"><img id="s1-img" src="assets/s1_hook.png" alt="" /></div>
  <div class="t cream" id="s1-l0" style="top:{280 + DY}px; font-size:104px">{words_html("h", [0, 1, 2])}</div>
  <div class="t cream" id="s1-l1" style="top:{380 + DY}px; font-size:104px">{words_html("h", [3, 4])} <em class="w" id="h5">choisi…</em></div>
  <div class="t red" id="s1-l2" style="top:{530 + DY}px; font-size:118px">{words_html("h", [6, 7, 8, 9])}</div>
  <div class="t red" id="s1-l3" style="top:{640 + DY}px; font-size:118px"><em class="w" id="h10">vendu&#8239;?</em></div>
</div>"""
js = []
for i in [1, 2, 3, 4, 5]:
    js.append(f'tl.fromTo("#h{i}", {{ opacity: 0.35 }}, {{ opacity: 1, duration: 0.12 }}, {r(s(i) - 0.04)});')
for i in [6, 7, 8, 9, 10]:
    js.append(f'tl.fromTo("#h{i}", {{ opacity: 0, y: -130, rotation: -4 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.42, ease: "back.out(1.9)" }}, {r(s(i) - 0.06)});')
js += [
    # la caméra se pose, puis punch sur « vendu »
    'tl.fromTo("#s1-cam", { scale: 1.06, transformOrigin: "60% 62%" }, { scale: 1, duration: 1.6, ease: "expo.out" }, 0);',
    f'tl.to("#s1-cam", {{ scale: 1.07, duration: 0.35, ease: "power3.out" }}, {r(s(10))});',
    f'tl.fromTo("#s1-img", {{ rotation: 0 }}, {{ rotation: 1.2, duration: 0.06, yoyo: true, repeat: 3, ease: "power1.inOut" }}, {r(s(10) + 0.05)});',
    f'tl.fromTo("#h10", {{ scale: 1.25, transformOrigin: "0% 50%" }}, {{ scale: 1, duration: 0.5, ease: "back.out(2.2)" }}, {r(s(10) - 0.06)});',
]
scenes.append(("s1", 0, s1_end, body, "\n    ".join(js), f"#s1-all {{ background: #171a2d; }}"))

# ---------------------------------------------------------------- 2 · foule de piliers emballés
s2_start, s2_end = s(11) - 0.08, s(27) + 0.35
body = f"""
<div class="all" id="s2-all">
  <div class="bg" style="background:#171a2d"></div>
  <div class="cam" id="s2-cam"><img src="assets/s2_foule.png" alt="" /></div>
  <div id="s2-a">
    <div class="kick cream" style="top:{270 + DY}px; opacity:.6">Aujourd'hui</div>
    <div class="t cream" style="top:{320 + DY}px; font-size:100px">Beaucoup de<br />3ème piliers…<br /><em>en assurance</em></div>
  </div>
  <div id="s2-b">
    <div class="t cream" style="top:{320 + DY}px; font-size:110px">Mais il y a<br />plusieurs<br /><span class="red">problèmes.</span></div>
  </div>
</div>"""
js = f"""
tl.fromTo("#s2-all", {{ clipPath: "inset(0% 0% 100% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }}, 0);
tl.fromTo("#s2-cam", {{ scale: 1.45, transformOrigin: "50% 64%" }}, {{ scale: 1, duration: 1.3, ease: "expo.out" }}, 0);
tl.fromTo("#s2-a", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, L({r(s(11))}));
tl.to("#s2-a", {{ opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }}, L({r(s(21) - 0.2)}));
tl.fromTo("#s2-b", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power2.out" }}, L({r(s(21) - 0.02)}));
tl.to("#s2-cam", {{ scale: 1.08, duration: 0.5, ease: "power3.out" }}, L({r(s(26))}));
"""
scenes.append(("s2", s2_start, s2_end, body, js))

# ---------------------------------------------------------------- 3 · mécanique assurance
s3_start, s3_end = s(27) - 0.08, s(40) + 0.4
body = f"""
<div class="all" id="s3-all">
  <div class="bg" style="background:#18192d"></div>
  <div class="cam" id="s3-cam">
    <img src="assets/s3_mecanique.png" alt="" />
    <div class="chip d" id="s3-c0" style="left:590px; top:{640 + DY}px">Montant fixe</div>
    <div class="chip d" id="s3-c1" style="left:120px; top:{1035 + DY}px">Couverture</div>
    <div class="chip r" id="s3-c2" style="left:500px; top:{1175 + DY}px">Frais</div>
    <div class="chip d" id="s3-c3" style="left:720px; top:{1255 + DY}px">Épargne</div>
  </div>
  <div class="kick cream" id="s3-k" style="top:{270 + DY}px; opacity:.6">Le problème</div>
  <div class="t cream" id="s3-t" style="top:{320 + DY}px; font-size:120px">En <em>assurance</em></div>
</div>"""
js = f"""
tl.fromTo("#s3-all", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.42, ease: "power3.inOut" }}, 0);
tl.fromTo("#s3-cam", {{ scale: 1.08, transformOrigin: "50% 62%" }}, {{ scale: 1, duration: 1.4, ease: "expo.out" }}, 0);
tl.fromTo("#s3-t", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "expo.out" }}, L({r(s(27))}));
tl.fromTo("#s3-k", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.3 }}, L({r(s(27))}));
tl.fromTo("#s3-c0", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, L({r(s(32))}));
tl.fromTo("#s3-c1", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, L({r(s(36))}));
tl.fromTo("#s3-c2", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.4)" }}, L({r(s(39))}));
tl.fromTo("#s3-c3", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, L({r(s(39) + 0.25)}));
tl.to("#s3-cam", {{ scale: 1.1, transformOrigin: "52% 70%", duration: 0.45, ease: "power3.out" }}, L({r(s(39))}));
"""
scenes.append(("s3", s3_start, s3_end, body, js))

# ---------------------------------------------------------------- 4 · pivot banque (crème)
s4_start, s4_end = s(40) - 0.1, s(66) + 0.35
body = f"""
<div class="all" id="s4-all">
  <div class="bg" style="background:#f6f1e5"></div>
  <div class="cam" id="s4-cam"><img src="assets/s4_banque.png" alt="" style="top:{70 + DY}px" /></div>
  <div class="t ink" id="s4-t" style="top:{280 + DY}px; font-size:92px">La même chose,<br /><em>en banque</em>&#8239;?</div>
  <div class="badge" id="s4-b1" style="top:{500 + DY}px"><i>✓</i>Même avantage fiscal</div>
  <div class="badge" id="s4-b2" style="top:{585 + DY}px"><i>↓</i>Moins de frais</div>
  <div class="badge" id="s4-b3" style="top:{670 + DY}px"><i>⇄</i>Versez librement</div>
</div>"""
js = f"""
tl.fromTo("#s4-all", {{ clipPath: "polygon(100% 0%, 140% 0%, 140% 100%, 100% 100%)" }}, {{ clipPath: "polygon(-40% 0%, 140% 0%, 140% 100%, 0% 100%)", duration: 0.5, ease: "power3.inOut" }}, 0);
tl.fromTo("#s4-cam", {{ scale: 1.1, transformOrigin: "55% 60%" }}, {{ scale: 1, duration: 1.6, ease: "expo.out" }}, 0);
tl.fromTo("#s4-t", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "expo.out" }}, L({r(s(40))}));
tl.to("#s4-t", {{ scale: 0.62, y: -40, transformOrigin: "0% 0%", duration: 0.5, ease: "power3.inOut" }}, L({r(s(50) - 0.25)}));
tl.fromTo("#s4-b1", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }}, L({r(s(50) - 0.05)}));
tl.fromTo("#s4-b2", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }}, L({r(s(53) - 0.05)}));
tl.fromTo("#s4-b3", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }}, L({r(s(58) - 0.1)}));
tl.to("#s4-cam", {{ scale: 1.07, transformOrigin: "50% 58%", duration: 0.5, ease: "power3.out" }}, L({r(s(58))}));
tl.to("#s4-cam", {{ scale: 1.0, duration: 0.8, ease: "power2.inOut" }}, L({r(s(62))}));
"""
scenes.append(("s4", s4_start, s4_end, body, js, "#s4-b1 i, #s4-b2 i, #s4-b3 i { line-height: 1; }"))

# ---------------------------------------------------------------- 5 · mais attention
s5_start, s5_end = s(66) - 0.08, s(86) + 0.5
TALL_Y, SHORT_Y, BX = 570 + DY, 1194 + DY, 965
body = f"""
<div class="all" id="s5-all">
  <div class="bg" style="background:#17182c"></div>
  <div class="cam" id="s5-cam">
    <div id="s5-grow" style="position:absolute; inset:0"><img src="assets/s5_tours.png" alt="" /></div>
    <svg id="s5-brk" style="position:absolute; left:0; top:0; overflow:visible" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
      <line id="s5-g1" x1="830" y1="{TALL_Y}" x2="{BX}" y2="{TALL_Y}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 9" />
      <line id="s5-g2" x1="300" y1="{SHORT_Y}" x2="{BX}" y2="{SHORT_Y}" stroke="{RED}" stroke-width="4" stroke-dasharray="10 9" />
      <path id="s5-b" d="M{BX - 18} {TALL_Y} H{BX} V{SHORT_Y} H{BX - 18}" fill="none" stroke="{RED}" stroke-width="8" />
    </svg>
    <div id="s5-ecart" class="red" style="position:absolute; right:60px; top:{TALL_Y - 120}px; font-family:'Instrument Serif'; font-style:italic; font-size:84px">l'écart</div>
  </div>
  <div class="t red" id="s5-mais" style="top:{300 + DY}px; font-size:170px; line-height:0.86">Mais<br /><em>attention</em></div>
  <div class="t cream" id="s5-sub" style="top:{290 + DY}px; font-size:84px">Toutes les banques<br /><em class="red">ne se valent pas</em></div>
  <div id="s5-flash" style="position:absolute; inset:0; background:{RED}"></div>
</div>"""
js = f"""
tl.fromTo("#s5-all", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.28, ease: "power3.inOut" }}, 0);
tl.fromTo("#s5-flash", {{ clipPath: "inset(0% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.32, ease: "power3.inOut" }}, 0.2);
tl.fromTo("#s5-mais", {{ scale: 1.3, opacity: 0, filter: "blur(10px)", transformOrigin: "0% 0%" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out" }}, L({r(s(66) + 0.05)}));
tl.to("#s5-mais", {{ opacity: 0, y: -40, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, L({r(s(68) - 0.25)}));
tl.fromTo("#s5-sub", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, L({r(s(68) - 0.05)}));
// les tours « poussent » : l'image se révèle de bas en haut
tl.fromTo("#s5-grow", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 1.6, ease: "power2.inOut" }}, L({r(s(68))}));
tl.fromTo("#s5-cam", {{ scale: 1.05, transformOrigin: "50% 60%" }}, {{ scale: 1, duration: 2.5, ease: "power2.out" }}, L({r(s(68))}));
tl.fromTo("#s5-b", {{ scaleY: 0, transformOrigin: "{BX}px {(TALL_Y + SHORT_Y) / 2}px" }}, {{ scaleY: 1, duration: 0.5, ease: "expo.out" }}, L({r(s(79))}));
tl.fromTo("#s5-g1, #s5-g2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, L({r(s(79))}));
tl.fromTo("#s5-ecart", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "expo.out" }}, L({r(s(79) + 0.15)}));
"""
scenes.append(("s5", s5_start, s5_end, body, js, "#s5-brk line, #s5-brk path { vector-effect: non-scaling-stroke; }"))

# ---------------------------------------------------------------- 6 · CTA
s6_start = s(86) - 0.1
IRIS = (BX, (TALL_Y + SHORT_Y) // 2)
body = f"""
<div class="all" id="s6-all">
  <div class="bg" style="background:linear-gradient(#eee2d5, #f0e9dd)"></div>
  <div class="cam" id="s6-cam"><img src="assets/s6_loupe.png" alt="" style="left:140px; top:{150 + DY}px; width:799px; height:1432px; -webkit-mask-image: radial-gradient(closest-side, #000 72%, transparent 100%); mask-image: radial-gradient(closest-side, #000 72%, transparent 100%);" /></div>
  <div class="t ink" id="s6-t" style="top:{270 + DY}px">
    <div><span class="w" id="s6-w1" style="font-size:150px">Analyse</span></div>
    <div><em class="w red" id="s6-w2" style="font-size:150px">gratuite</em></div>
    <div style="margin-top:14px"><span class="w" id="s6-w3" style="font-size:66px">de votre 3ème pilier A</span></div>
  </div>
  <div id="s6-btn" style="position:absolute; left:90px; top:{1205 + DY}px; width:900px; height:130px; border-radius:65px; background:{RED}; color:{CREAM}; display:flex; align-items:center; justify-content:center; gap:24px; font-family:'Inter Tight'; font-weight:900; font-size:52px; letter-spacing:-0.03em">
    <span>Réserver mon analyse</span>
    <svg id="s6-arrow" width="52" height="38" viewBox="0 0 56 40"><path d="M2 20 H50 M34 4 L52 20 L34 36" fill="none" stroke="{CREAM}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg>
  </div>
  <div id="s6-legal" style="position:absolute; left:90px; width:900px; top:{1440 + DY}px; font-family:'Inter Tight'; font-weight:600; font-size:28px; line-height:1.28; color:{INK}; opacity:.68">Analyse sans engagement. Les frais et résultats varient selon les produits, la stratégie et la durée de placement.</div>
</div>"""
js = f"""
tl.fromTo("#s6-all", {{ clipPath: "circle(0px at {IRIS[0]}px {IRIS[1]}px)" }}, {{ clipPath: "circle(2300px at {IRIS[0]}px {IRIS[1]}px)", duration: 0.55, ease: "power3.inOut" }}, 0);
tl.fromTo("#s6-cam", {{ scale: 1.12, transformOrigin: "50% 48%" }}, {{ scale: 1, duration: 1.8, ease: "expo.out" }}, 0);
tl.fromTo("#s6-w1", {{ y: -150, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, L({r(s(86))}));
tl.fromTo("#s6-w2", {{ y: -150, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, L({r(s(87))}));
tl.fromTo("#s6-w3", {{ y: -100, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, L({r(s(89) - 0.1)}));
tl.fromTo("#s6-btn", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.55, ease: "back.out(1.5)" }}, L({r(s(96))}));
tl.fromTo("#s6-arrow", {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "expo.out" }}, L({r(s(96) + 0.3)}));
tl.fromTo("#s6-legal", {{ opacity: 0 }}, {{ opacity: 0.68, duration: 0.4 }}, L({r(s(86) + 1.0)}));
"""
scenes.append(("s6", s6_start, DUR, body, js))

os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
for sc in scenes:
    sid, a, b, body, js = sc[:5]
    css = sc[5] if len(sc) > 5 else ""
    open(os.path.join(OUT, "compositions", f"{sid}.html"), "w").write(scene(sid, a, b - a, body, js, css))

# ---------------------------------------------------------------- sous-titres
skip = set(range(0, 11))
breaks = {11, 15, 21, 27, 29, 33, 37, 40, 45, 50, 53, 56, 59, 62, 66, 68, 71, 75, 79, 83, 86, 88, 92, 96, 98, 102, 105}
red = {26, 39, 55, 67, 97}
light_scene = [(0, "light"), (s4_start, "dark"), (s5_start, "light"), (s6_start, "dark")]
groups, cur = [], []
for i, wd in enumerate(words):
    if i in skip:
        continue
    if cur and (i in breaks or len(cur) >= 5):
        groups.append(cur); cur = []
    cur.append(i)
groups.append(cur)
cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.05, s(g[0]) - 0.08)
    nxt = s(groups[gi + 1][0]) - 0.08 if gi + 1 < len(groups) else DUR
    ge = min(nxt, words[g[-1]]["end"] + 0.5)
    tone = [t for a, t in light_scene if gs >= a - 1e-6][-1]
    late = " late" if gs >= s6_start else ""
    sp = []
    for i in g:
        cls = "cw red" if i in red else "cw"
        sp.append(f'<span id="c{i}" class="{cls}">{html.escape(words[i]["text"])}</span>')
        cap_js.append(f'tl.fromTo("#c{i}", {{ opacity: 0.3, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power3.out" }}, {r(s(i))});')
    cap_html.append(f'<div id="cg{gi}" class="cg clip {tone}{late}" data-start="{r(gs)}" data-duration="{r(ge - gs)}" data-track-index="0"><span class="pill">{" ".join(sp)}</span></div>')

cap = f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; }}
    .cg {{ position: absolute; left: 70px; right: 70px; top: {1405 + DY}px; height: 100px; display: flex; align-items: center; justify-content: center; column-gap: 0.26em; white-space: nowrap; overflow: visible;
      font-family: 'Inter Tight'; font-weight: 800; font-size: 58px; letter-spacing: -0.025em; }}
    .cg.light {{ color: {CREAM}; }}
    .cg.dark {{ color: {INK}; }}
    .cg.late {{ top: {1338 + DY}px; height: 90px; font-size: 50px; }}
    .pill {{ display: inline-flex; column-gap: 0.26em; padding: 8px 26px 12px; border-radius: 22px; }}
    .cg.light .pill {{ background: rgba(11, 20, 38, 0.8); }}
    .cg.dark .pill {{ background: rgba(244, 241, 234, 0.92); }}
    .cw {{ display: inline-block; }}
    .cw.red {{ color: {RED}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
    {"\n    ".join(cap_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {"\n    ".join(cap_js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open(os.path.join(OUT, "compositions", "captions.html"), "w").write(cap)

# ---------------------------------------------------------------- racine
hosts = "\n      ".join(
    f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{r(a)}" '
    f'data-duration="{r(b - a)}" data-track-index="{k + 1}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{k + 1}"></div>'
    for k, (sid, a, b, *_rest) in enumerate(scenes))
index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #base {{ position: absolute; inset: 0; background: {INK}; }}
      #grain {{ position: absolute; inset: 0; background-image: url('assets/grain.png'); background-size: 512px 512px; mix-blend-mode: overlay; opacity: 0.1; pointer-events: none; z-index: 50; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      <div id="base"></div>
      {hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{r(DUR)}" data-track-index="8" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:20"></div>
      <div id="grain" class="clip" data-start="0" data-duration="{r(DUR)}" data-track-index="9" data-layout-ignore></div>
      <audio id="mix" class="clip" src="assets/mix_C.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      for (let k = 0; k < {int(DUR * 12)}; k++) {{
        tl.set("#grain", {{ backgroundPosition: `${{(k * 173) % 512}}px ${{(k * 311) % 512}}px` }}, k / 12);
      }}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(index)

A = os.path.join(OUT, "assets")
os.makedirs(A, exist_ok=True)
shutil.copytree(os.path.join(SRC, "assets", "fonts"), os.path.join(A, "fonts"), dirs_exist_ok=True)
for f in ["grain.png", "mix_C.wav"]:
    shutil.copy(os.path.join(SRC, "assets", f), A)
SC = os.path.join(ROOT, "soft", "scenes")
for src_name, dst in [("s1_hook", "s1_hook"), ("s2_foule", "s2_foule"), ("s3_mecanique", "s3_mecanique"),
                      ("s4_banque_clean", "s4_banque"), ("s5_tours", "s5_tours"), ("s6_loupe", "s6_loupe")]:
    shutil.copy(os.path.join(SC, src_name + ".png"), os.path.join(A, dst + ".png"))
for f in ["hyperframes.json", "package.json"]:
    shutil.copy(os.path.join(SRC, f), OUT)
print("ok", OUT)
for g in groups:
    print("  ", r(s(g[0])), " ".join(words[i]["text"] for i in g))
