#!/usr/bin/env python3
"""Version longue : femme face caméra (clips FLORA) + motion « interface d'app ».

Usage: python3 build_long.py 916|45
"""
import json, sys, os, shutil, html

FMT = sys.argv[1] if len(sys.argv) > 1 else "916"
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "out", f"L_{FMT}")
W = 1080
H = 1920 if FMT == "916" else 1350
DY = 0 if FMT == "916" else -210          # décalage vertical de la mise en page
VY = 0 if FMT == "916" else -230          # recadrage des clips en 4:5 (on garde la tête)
INK, CREAM, RED, SLATE = "#0B1426", "#F4F1EA", "#E63312", "#8B93A5"

words = json.load(open(os.path.join(SRC, "transcript_L.json")))
FIX = {1: "3ème", 2: "pilier,", 10: "vendu ?", 16: "Suisse romande", 19: "3ème", 41: "part", 42: "en",
       44: "et", 68: "banque ?", 70: "avantage", 71: "fiscal,", 86: "attention :", 132: "3ème"}
for i, t in FIX.items():
    words[i]["text"] = t
DUR = 52.0

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
#root {{ position: absolute; inset: 0; overflow: hidden; font-family: 'Inter Tight'; }}
.all {{ position: absolute; inset: 0; }}
.dark {{ background: radial-gradient(120% 80% at 50% 40%, #16223D 0%, {INK} 70%); }}
.light {{ background: radial-gradient(120% 80% at 50% 40%, #FBF9F4 0%, #ECE7DC 80%); }}
.t {{ position: absolute; left: 90px; right: 90px; font-weight: 900; letter-spacing: -0.045em; line-height: 0.95; }}
.t em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; letter-spacing: -0.01em; font-size: 1.18em; }}
.cream {{ color: {CREAM}; }} .ink {{ color: {INK}; }} .red {{ color: {RED}; }}
.kick {{ position: absolute; left: 90px; font-weight: 800; font-size: 30px; letter-spacing: 0.16em; text-transform: uppercase; }}
.card {{ position: absolute; background: {CREAM}; border-radius: 34px; box-shadow: 0 30px 60px rgba(0,0,0,0.28), 0 2px 0 rgba(255,255,255,0.6) inset; color: {INK}; }}
.lcard {{ position: absolute; background: #FFFFFF; border-radius: 34px; box-shadow: 0 24px 50px rgba(11,20,38,0.14); color: {INK}; }}
.pill {{ position: absolute; border-radius: 999px; font-weight: 800; white-space: nowrap; }}
.sticker {{ position: absolute; background: {RED}; color: {CREAM}; font-weight: 900; font-size: 46px; letter-spacing: -0.02em; padding: 16px 30px; border-radius: 18px; box-shadow: 0 16px 34px rgba(230,51,18,0.35); white-space: nowrap; }}
.vid {{ position: absolute; left: 0; top: {VY}px; width: 1080px; height: 1920px; object-fit: cover; }}
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

LOCK = '<svg viewBox="0 0 60 72" width="{w}" height="{h}"><path {extra} d="M15 34 V21 a15 15 0 0 1 30 0 V34" fill="none" stroke="{c}" stroke-width="7"/><rect x="4" y="32" width="52" height="38" rx="7" fill="{c}"/></svg>'
CHECK = f'<svg viewBox="0 0 60 60" width="56" height="56"><circle cx="30" cy="30" r="28" fill="{RED}"/><path d="M17 31 L26 40 L44 21" fill="none" stroke="{CREAM}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
scenes = []

# ---------------------------------------------------------------- clips face caméra
def face(sid, start, dur, src, overlay="", js_extra="", enter="", media_start=0):
    body = f"""
<div class="all" id="{sid}-all" style="background:{INK}">
  <div id="{sid}-cam" style="position:absolute; inset:0">
    <video id="{sid}-v" class="vid clip" data-start="0" data-duration="{r(dur)}" data-media-start="{r(media_start)}" src="assets/{src}" muted playsinline></video>
  </div>
  {overlay}
</div>"""
    js = enter + "\n" + js_extra
    scenes.append((sid, start, start + dur, body, js))

# 1 · hook (le texte du hook est incrusté en bas, la voix est la voix originale)
F1_END = 4.05
hook_overlay = f"""
  <div style="position:absolute; left:0; right:0; bottom:0; height:{900 if FMT == '916' else 620}px; background:linear-gradient(rgba(11,20,38,0), rgba(11,20,38,0.78))"></div>
  <div class="t cream" style="top:{1105 + DY}px; font-size:76px; text-shadow:0 4px 24px rgba(0,0,0,0.35)">
    <span id="h0">Votre 3ème pilier,</span><br /><span id="h1">vous l'avez <em>choisi…</em></span>
  </div>
  <div class="t red" id="h2" style="top:{1290 + DY}px; font-size:92px; text-shadow:0 4px 24px rgba(0,0,0,0.35)">ou on vous l'a <em>vendu&#8239;?</em></div>"""
hook_js = f"""
tl.fromTo("#h0", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, 0.05);
tl.fromTo("#h1", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, {r(s(3) - 0.1)});
tl.fromTo("#h2", {{ opacity: 0, y: -90, scale: 1.15, transformOrigin: "0% 50%" }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2)" }}, {r(s(6) - 0.06)});
tl.fromTo("#f1-cam", {{ scale: 1 }}, {{ scale: 1.06, transformOrigin: "50% 30%", duration: 0.35, ease: "power3.out" }}, {r(s(10))});
"""
face("f1", 0, F1_END + 0.25, "f1_hook.mp4", hook_overlay, hook_js)

# ---------------------------------------------------------------- M1 · contrats signés il y a des années
m1_start, m1_end = F1_END - 0.1, s(34) + 0.35
cards = [("2011", 0), ("2014", 1), ("2009", 2), ("2016", 3)]
card_html = ""
for yr, k in cards:
    card_html += f"""
    <div class="card m1c" id="m1-c{k}" style="left:110px; width:860px; height:160px; top:{620 + DY}px">
      <div style="position:absolute; left:30px; top:30px; width:100px; height:100px; border-radius:26px; background:{INK}; display:flex; align-items:center; justify-content:center">
        <svg viewBox="0 0 48 56" width="48" height="56"><path d="M24 2 L44 10 V28 C44 42 34 50 24 54 C14 50 4 42 4 28 V10 Z" fill="none" stroke="{CREAM}" stroke-width="5"/></svg>
      </div>
      <div style="position:absolute; left:160px; top:34px; font-weight:900; font-size:44px; letter-spacing:-0.03em">Contrat 3ème pilier A</div>
      <div style="position:absolute; left:160px; top:92px; font-weight:600; font-size:32px; color:#5A6273">Assurance · <span id="m1-y{k}">signé en {yr}</span></div>
      <div style="position:absolute; right:34px; top:40px; font-weight:800; font-size:26px; color:#8B93A5">il y a {2026 - int(yr)} ans</div>
    </div>"""
body = f"""
<div class="all dark" id="m1-all">
  <div class="pill" id="m1-k" style="left:90px; top:{285 + DY}px; padding:10px 22px; font-size:28px; letter-spacing:0.12em; text-transform:uppercase; background:rgba(244,241,234,0.12); color:{CREAM}">Suisse romande</div>
  <div class="t cream" id="m1-t" style="top:{355 + DY}px; font-size:92px">Beaucoup de 3ème<br />piliers… <em class="red" id="m1-em">en assurance</em></div>
  {card_html}
  <div class="pill" id="m1-btn" style="left:110px; top:{1185 + DY}px; width:860px; height:110px; border:4px dashed rgba(244,241,234,0.35); color:rgba(244,241,234,0.45); font-size:44px; display:flex; align-items:center; justify-content:center">Comparer les offres</div>
  <svg id="m1-cur" viewBox="0 0 40 52" width="54" height="70" style="position:absolute; left:700px; top:{1240 + DY}px"><path d="M4 4 L4 42 L14 32 L22 50 L29 47 L21 29 L36 29 Z" fill="{CREAM}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></svg>
  <div class="sticker" id="m1-st" style="left:560px; top:{1115 + DY}px">Jamais comparé&#8239;?</div>
</div>"""
js = f"""
tl.fromTo("#m1-all", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }}, 0);
tl.fromTo("#m1-k", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0.15);
tl.fromTo("#m1-t", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 0.2);
tl.fromTo("#m1-em", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.2 }}, L({r(s(22))}));
// les contrats tombent comme des notifications et s'empilent
const stack = [[0, 4.4], [1, 5.0], [2, 5.7], [3, 6.4]];
stack.forEach(([k, at], n) => {{
  tl.fromTo("#m1-c" + k, {{ y: -260, opacity: 0, scale: 0.92 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.55, ease: "back.out(1.6)" }}, L(at));
  for (let j = 0; j < k; j++) {{
    const depth = k - j;
    tl.to("#m1-c" + j, {{ y: 120 * depth, scale: 1 - 0.035 * depth, opacity: 1 - 0.18 * depth, duration: 0.5, ease: "power3.out" }}, L(at));
  }}
}});
tl.fromTo("#m1-y3", {{ color: "#5A6273" }}, {{ color: "{RED}", duration: 0.2 }}, L({r(s(25))}));
tl.fromTo("#m1-btn", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, L({r(s(31) - 0.3)}));
tl.fromTo("#m1-cur", {{ opacity: 0, x: 180, y: 120 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.6, ease: "power3.out" }}, L({r(s(31) - 0.2)}));
tl.fromTo("#m1-st", {{ opacity: 0, scale: 1.8, rotation: -14 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.35, ease: "back.out(2.6)" }}, L({r(s(33))}));
"""
scenes.append(("m1", m1_start, m1_end, body, js, ".m1c { transform-origin: 50% 0%; }"))

# ---------------------------------------------------------------- M2 · le relevé décortiqué
m2_start, m2_end = s(34) - 0.08, s(59) + 0.35
months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
month_html = "".join(
    f'<div class="mo" id="m2-mo{k}" style="left:{40 + (k % 3) * 176}px; top:{(k // 3) * 92}px"><b>{m}</b><i></i></div>' for k, m in enumerate(months))
body = f"""
<div class="all dark" id="m2-all">
  <div class="kick cream" style="top:{285 + DY}px; opacity:.6">En assurance</div>
  <div id="m2-phone" style="position:absolute; left:220px; top:{345 + DY}px; width:640px; height:1000px; border-radius:70px; background:#0E1730; padding:16px; box-shadow:0 40px 80px rgba(0,0,0,0.5)">
    <div style="position:relative; width:100%; height:100%; border-radius:56px; background:{CREAM}; overflow:hidden">
      <div id="m2-screen" style="position:absolute; left:0; top:0; width:100%">
        <div style="position:absolute; left:40px; top:56px; font-weight:800; font-size:24px; letter-spacing:0.14em; color:#8B93A5; text-transform:uppercase">Relevé annuel</div>
        <div style="position:absolute; left:40px; top:94px; font-weight:900; font-size:44px; letter-spacing:-0.03em; color:{INK}">3ème pilier A</div>
        <div style="position:absolute; left:40px; top:186px; font-weight:800; font-size:30px; color:{INK}">Vos primes</div>
        <div style="position:absolute; left:40px; top:236px; width:528px; height:76px; border-radius:20px; background:{INK}; overflow:hidden">
          <div id="m2-cov" style="position:absolute; right:0; top:0; bottom:0; width:200px; background:{SLATE}; transform-origin:100% 50%"></div>
          <div id="m2-fee" style="position:absolute; right:0; top:0; bottom:0; width:110px; background:{RED}; transform-origin:100% 50%"></div>
        </div>
        <div class="lg" style="top:350px"><span style="background:{INK}"></span>Épargne</div>
        <div class="lg" id="m2-l1" style="top:420px"><span style="background:{SLATE}"></span>Couverture</div>
        <div class="lg" id="m2-l2" style="top:490px"><span style="background:{RED}"></span>Frais</div>
        <svg id="m2-circle" viewBox="0 0 300 110" width="300" height="110" style="position:absolute; left:20px; top:468px; overflow:visible"><path d="M40 70 C 20 30, 120 8, 210 16 C 290 24, 296 80, 220 96 C 150 110, 40 104, 22 74" fill="none" stroke="{RED}" stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/></svg>
        <div style="position:absolute; left:40px; top:640px; font-weight:800; font-size:30px; color:{INK}">Versements</div>
        <div id="m2-fixe" class="pill" style="left:300px; top:630px; padding:8px 18px; background:{RED}; color:{CREAM}; font-size:24px; letter-spacing:0.06em; text-transform:uppercase">Montant fixe</div>
        <div id="m2-months" style="position:absolute; left:0; top:710px; width:100%">{month_html}</div>
      </div>
    </div>
  </div>
  <div id="m2-lock" style="position:absolute; left:780px; top:{915 + DY}px; width:130px; height:130px; border-radius:40px; background:{RED}; display:flex; align-items:center; justify-content:center; box-shadow:0 20px 40px rgba(230,51,18,0.4)">{LOCK.format(w=62, h=74, c=CREAM, extra='id="m2-shk"')}</div>
</div>"""
css = f"""
.lg {{ position: absolute; left: 40px; display: flex; align-items: center; gap: 18px; font-weight: 800; font-size: 34px; color: {INK}; }}
.lg span {{ display: inline-block; width: 30px; height: 30px; border-radius: 9px; }}
.mo {{ position: absolute; width: 160px; height: 76px; border-radius: 18px; background: #E4DED2; }}
.mo b {{ position: absolute; left: 16px; top: 10px; font-size: 22px; font-weight: 800; color: #5A6273; }}
.mo i {{ position: absolute; left: 16px; right: 16px; bottom: 14px; height: 14px; border-radius: 7px; background: {INK}; }}
"""
js = f"""
tl.fromTo("#m2-all", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.42, ease: "power3.inOut" }}, 0);
tl.fromTo("#m2-phone", {{ y: 420, rotation: 6, scale: 0.9 }}, {{ y: 0, rotation: 0, scale: 1, duration: 0.8, ease: "expo.out" }}, 0.1);
tl.fromTo("#m2-cov", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "expo.out" }}, L({r(s(43) - 0.05)}));
tl.fromTo("#m2-l1", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.2 }}, L({r(s(43))}));
tl.fromTo("#m2-fee", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "expo.out" }}, L({r(s(46) - 0.05)}));
tl.fromTo("#m2-l2", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.2 }}, L({r(s(46))}));
tl.fromTo("#m2-circle path", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }}, L({r(s(46) + 0.15)}));
tl.fromTo("#m2-phone", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.3, ease: "power3.out" }}, L({r(s(46))}));
tl.to("#m2-phone", {{ scale: 1, duration: 0.5, ease: "power2.inOut" }}, L({r(s(47))}));
// défilement vers les versements : tous les mois identiques, verrouillés
tl.fromTo("#m2-screen", {{ y: 0 }}, {{ y: -420, duration: 0.7, ease: "power3.inOut" }}, L({r(s(47))}));
tl.fromTo(".mo", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, stagger: 0.04, ease: "power3.out" }}, L({r(s(48))}));
tl.fromTo("#m2-fixe", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }}, L({r(s(51))}));
tl.fromTo("#m2-lock", {{ opacity: 0, scale: 0.3, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.2)" }}, L({r(s(51) + 0.1)}));
tl.fromTo("#m2-shk", {{ y: -14 }}, {{ y: 0, duration: 0.25, ease: "back.out(3)" }}, L({r(s(52))}));
"""
scenes.append(("m2", m2_start, m2_end, body, js, css))

# ---------------------------------------------------------------- F2 · « en banque ? »
F2_START = 18.80
face("f2", F2_START, 2.45, "f2_banque.mp4", "", "",
     enter=f'tl.fromTo("#f2-all", {{ clipPath: "circle(0px at 540px {r(845 + DY)}px)" }}, {{ clipPath: "circle(2300px at 540px {r(845 + DY)}px)", duration: 0.45, ease: "power3.inOut" }}, 0);')

# ---------------------------------------------------------------- M3 · la bascule en banque (clair)
m3_start, m3_end = s(69) - 0.1, s(85) + 0.35
body = f"""
<div class="all light" id="m3-all">
  <div id="m3-tog" style="position:absolute; left:140px; top:{300 + DY}px; width:800px; height:140px; border-radius:70px; background:#FFFFFF; box-shadow:0 20px 44px rgba(11,20,38,0.14)">
    <div id="m3-knob" style="position:absolute; left:10px; top:10px; width:390px; height:120px; border-radius:60px; background:{SLATE}"></div>
    <div id="m3-la" style="position:absolute; left:10px; top:10px; width:390px; height:120px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:46px; color:{CREAM}">Assurance</div>
    <div id="m3-lb" style="position:absolute; left:400px; top:10px; width:390px; height:120px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:46px; color:{INK}">Banque</div>
  </div>
  <div class="lcard" id="m3-card" style="left:110px; top:{520 + DY}px; width:860px; height:800px">
    <div class="row" id="m3-r1" style="top:50px">{CHECK}<span>Même avantage fiscal</span></div>
    <div class="sep" style="top:180px"></div>
    <div class="row" id="m3-r2" style="top:220px">{CHECK}<span>Moins de frais</span></div>
    <div id="m3-fbar" style="position:absolute; left:126px; top:320px; width:600px; height:26px; border-radius:13px; background:{RED}; transform-origin:0 50%"></div>
    <div style="position:absolute; left:126px; top:358px; font-weight:800; font-size:26px; letter-spacing:0.12em; color:#8B93A5; text-transform:uppercase">frais</div>
    <div class="sep" style="top:430px"></div>
    <div class="row" id="m3-r3" style="top:470px">{CHECK}<span>Versements libres</span></div>
    <div id="m3-track" style="position:absolute; left:126px; top:600px; width:640px; height:10px; border-radius:5px; background:#E4DED2">
      <div id="m3-fill" style="position:absolute; left:0; top:0; height:10px; width:640px; border-radius:5px; background:{INK}; transform-origin:0 50%"></div>
      <div id="m3-kn" style="position:absolute; left:-30px; top:-25px; width:60px; height:60px; border-radius:50%; background:{INK}; border:8px solid #FFFFFF; box-shadow:0 0 0 3px {INK}"></div>
    </div>
    <div style="position:absolute; left:126px; top:660px; font-weight:800; font-size:26px; letter-spacing:0.1em; color:#8B93A5; text-transform:uppercase">Quand vous voulez · ce que vous voulez</div>
  </div>
</div>"""
css = f"""
.row {{ position: absolute; left: 40px; display: flex; gap: 30px; align-items: center; font-weight: 900; font-size: 60px; letter-spacing: -0.04em; color: {INK}; white-space: nowrap; }}
.sep {{ position: absolute; left: 40px; right: 40px; height: 2px; background: #ECE7DC; }}
"""
js = f"""
tl.fromTo("#m3-all", {{ clipPath: "polygon(100% 0%, 140% 0%, 140% 100%, 100% 100%)" }}, {{ clipPath: "polygon(-40% 0%, 140% 0%, 140% 100%, 0% 100%)", duration: 0.5, ease: "power3.inOut" }}, 0);
tl.fromTo("#m3-tog", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "expo.out" }}, 0.15);
// l'interrupteur bascule d'assurance vers banque
tl.fromTo("#m3-knob", {{ x: 0, backgroundColor: "{SLATE}" }}, {{ x: 390, backgroundColor: "{RED}", duration: 0.45, ease: "back.out(1.6)" }}, 0.6);
tl.fromTo("#m3-la", {{ color: "{CREAM}" }}, {{ color: "{SLATE}", duration: 0.3 }}, 0.6);
tl.fromTo("#m3-lb", {{ color: "{INK}" }}, {{ color: "{CREAM}", duration: 0.3 }}, 0.65);
tl.fromTo("#m3-card", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "expo.out" }}, 0.5);
[["#m3-r1", {r(s(69))}], ["#m3-r2", {r(s(72))}], ["#m3-r3", {r(s(75))}]].forEach(([id, at]) => {{
  tl.fromTo(id, {{ opacity: 0.18 }}, {{ opacity: 1, duration: 0.2 }}, L(at) - 0.05);
  tl.fromTo(id + " svg", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.4, ease: "back.out(2.6)" }}, L(at));
}});
tl.fromTo("#m3-fbar", {{ scaleX: 1 }}, {{ scaleX: 0.22, duration: 0.9, ease: "expo.inOut" }}, L({r(s(73))}));
tl.fromTo("#m3-kn", {{ x: 60 }}, {{ x: 520, duration: 0.8, ease: "power2.inOut" }}, L({r(s(77))}));
tl.fromTo("#m3-fill", {{ scaleX: 60 / 640 }}, {{ scaleX: 520 / 640, duration: 0.8, ease: "power2.inOut" }}, L({r(s(77))}));
tl.to("#m3-kn", {{ x: 200, duration: 0.7, ease: "power2.inOut" }}, L({r(s(81))}));
tl.to("#m3-fill", {{ scaleX: 200 / 640, duration: 0.7, ease: "power2.inOut" }}, L({r(s(81))}));
tl.to("#m3-kn", {{ x: 440, duration: 0.6, ease: "power2.inOut" }}, L({r(s(84))}));
tl.to("#m3-fill", {{ scaleX: 440 / 640, duration: 0.6, ease: "power2.inOut" }}, L({r(s(84))}));
"""
scenes.append(("m3", m3_start, m3_end, body, js, css))

# ---------------------------------------------------------------- M4 · toutes les offres ne se valent pas
m4_start, m4_end = s(85) - 0.08, s(108) + 0.4
ends = [(30, "A"), (78, "B"), (118, "C")]   # hauteur finale des courbes (px dans la carte)
offer_html = ""
for k, (yend, name) in enumerate(ends):
    top = 620 + k * 230
    offer_html += f"""
  <div class="card off" id="m4-o{k}" style="left:110px; top:{top + DY}px; width:860px; height:200px">
    <div style="position:absolute; left:34px; top:30px; font-weight:900; font-size:46px; letter-spacing:-0.03em">Offre {name}</div>
    <div class="pill tg" id="m4-f{k}" style="left:34px; top:110px">Frais</div>
    <div class="pill tg" id="m4-s{k}" style="left:160px; top:110px">Stratégie</div>
    <svg viewBox="0 0 400 150" width="400" height="150" style="position:absolute; right:30px; top:25px; overflow:visible">
      <line x1="0" y1="140" x2="380" y2="140" stroke="#D6D0C4" stroke-width="3"/>
      <path class="spk" d="M0 140 C 140 138, 250 {(140 + yend) / 2}, 380 {yend}" fill="none" stroke="{INK if k < 2 else RED}" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1"/>
      <circle class="dot" cx="380" cy="{yend}" r="11" fill="{INK if k < 2 else RED}"/>
    </svg>
  </div>"""
BRX = 990
body = f"""
<div class="all dark" id="m4-all">
  <div id="m4-alert" style="position:absolute; left:90px; right:90px; top:{290 + DY}px; height:120px; border-radius:30px; background:{RED}; display:flex; align-items:center; gap:24px; padding:0 34px; box-shadow:0 20px 40px rgba(230,51,18,0.4)">
    <svg viewBox="0 0 60 54" width="62" height="56"><path d="M30 4 L57 50 H3 Z" fill="none" stroke="{CREAM}" stroke-width="6" stroke-linejoin="round"/><path d="M30 20 V34 M30 41 V43" stroke="{CREAM}" stroke-width="6" stroke-linecap="round"/></svg>
    <span style="font-weight:900; font-size:56px; letter-spacing:-0.03em; color:{CREAM}">Mais attention</span>
  </div>
  <div class="t cream" id="m4-t" style="top:{442 + DY}px; font-size:58px; white-space:nowrap">Toutes les banques<br /><em class="red">ne se valent pas</em></div>
  {offer_html}
  <div id="m4-ret" class="pill" style="left:790px; top:{575 + DY}px; padding:6px 16px; background:rgba(244,241,234,0.14); color:{CREAM}; font-size:24px; letter-spacing:0.12em; text-transform:uppercase">Retraite</div>
  <svg id="m4-brk" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:0; top:0; overflow:visible">
    <path d="M{BRX - 22} {645 + 30 + DY} H{BRX} V{1080 + 118 + DY} H{BRX - 22}" fill="none" stroke="{RED}" stroke-width="7"/>
  </svg>
  <div id="m4-ecart" class="red" style="position:absolute; left:820px; top:{1335 + DY}px; font-family:'Instrument Serif'; font-style:italic; font-size:64px">l'écart</div>
  <div id="m4-flash" style="position:absolute; inset:0; background:{RED}"></div>
</div>"""
css = f".tg {{ padding: 8px 18px; background: #E4DED2; color: {INK}; font-size: 26px; }}"
js = f"""
tl.fromTo("#m4-all", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.28, ease: "power3.inOut" }}, 0);
tl.fromTo("#m4-flash", {{ clipPath: "inset(0% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.32, ease: "power3.inOut" }}, 0.2);
tl.fromTo("#m4-alert", {{ y: -200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.8)" }}, L({r(s(85))}));
tl.fromTo("#m4-t", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }}, L({r(s(87) - 0.05)}));
[0, 1, 2].forEach((k) => {{
  tl.fromTo("#m4-o" + k, {{ x: 900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.55, ease: "expo.out" }}, L({r(s(88))}) + k * 0.12);
  tl.fromTo("#m4-o" + k + " .spk", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 2.4, ease: "power2.inOut" }}, L({r(s(90))}) + k * 0.08);
  tl.fromTo("#m4-o" + k + " .dot", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, L({r(s(90))}) + 2.3 + k * 0.08);
  tl.fromTo("#m4-f" + k, {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }}, L({r(s(94))}) + k * 0.06);
  tl.fromTo("#m4-s" + k, {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.4)" }}, L({r(s(95))}) + k * 0.06);
}});
tl.fromTo("#m4-ret", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, L({r(s(100))}));
tl.fromTo("#m4-brk path", {{ scaleY: 0, transformOrigin: "{BRX}px {r((675 + 1198) / 2 + DY)}px" }}, {{ scaleY: 1, duration: 0.5, ease: "expo.out" }}, L({r(s(101))}));
tl.fromTo("#m4-ecart", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, L({r(s(101) + 0.15)}));
"""
scenes.append(("m4", m4_start, m4_end, body, js, css))

# ---------------------------------------------------------------- F3 · « parfois, le garder reste la bonne option »
F3_START = 34.80
face("f3", F3_START, 6.25, "f3_assise.mp4", "", "",
     enter=f'tl.fromTo("#f3-all", {{ clipPath: "circle(0px at {BRX}px {r(915 + DY)}px)" }}, {{ clipPath: "circle(2300px at {BRX}px {r(915 + DY)}px)", duration: 0.5, ease: "power3.inOut" }}, 0);')

# ---------------------------------------------------------------- F4 · CTA face caméra, en deux plans
# Chaque clip commence par un court silence (ajouté pour la synchro) que l'on saute avec data-media-start.
F4A_START, F4B_START = 41.00, 44.48
face("f4a", F4A_START, F4B_START - F4A_START, "f4a_cta.mp4", "", "", media_start=0,
     enter=f'tl.fromTo("#f4a-all", {{ clipPath: "inset(0% 0% 0% 100%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }}, 0);')
f4_overlay = f"""
  <div class="pill" id="f4-a" style="left:90px; top:{1215 + DY}px; padding:14px 28px; background:{RED}; color:{CREAM}; font-size:40px; letter-spacing:-0.02em; box-shadow:0 14px 30px rgba(230,51,18,0.35)">Analyse gratuite</div>
  <div class="pill" id="f4-b" style="left:470px; top:{1215 + DY}px; padding:14px 28px; background:{CREAM}; color:{INK}; font-size:40px; letter-spacing:-0.02em">Sans engagement</div>"""
f4_js = f"""
tl.fromTo("#f4b-cam", {{ scale: 1.08 }}, {{ scale: 1, transformOrigin: "50% 40%", duration: 0.6, ease: "expo.out" }}, 0);
tl.fromTo("#f4-a", {{ opacity: 0, y: 30, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2.2)" }}, L({r(s(138))}));
tl.fromTo("#f4-b", {{ opacity: 0, y: 30, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2.2)" }}, L({r(s(140))}));
"""
face("f4b", F4B_START, 49.0 - F4B_START, "f4b_cta.mp4", f4_overlay, f4_js, media_start=0.48)

# ---------------------------------------------------------------- M5 · carte de fin : réservation
m5_start = 48.85
days = ["Lun", "Mar", "Mer", "Jeu", "Ven"]
day_html = "".join(f'<div class="day" id="m5-d{k}" style="left:{40 + k * 158}px">{d}</div>' for k, d in enumerate(days))
body = f"""
<div class="all light" id="m5-all">
  <div class="t ink" style="top:{290 + DY}px">
    <div id="m5-w1" style="font-size:132px">Analyse</div>
    <div id="m5-w2" style="font-size:132px"><em class="red">gratuite</em></div>
    <div id="m5-w3" style="font-size:62px; margin-top:16px">de votre 3ème pilier A</div>
  </div>
  <div class="lcard" id="m5-cal" style="left:110px; top:{735 + DY}px; width:860px; height:330px">
    <div style="position:absolute; left:40px; top:34px; font-weight:800; font-size:26px; letter-spacing:0.14em; color:#8B93A5; text-transform:uppercase">Choisissez un créneau</div>
    <div style="position:absolute; left:0; top:96px; width:100%">{day_html}</div>
    <div class="slot" style="left:40px">9:00</div><div class="slot" id="m5-pick" style="left:310px">12:30</div><div class="slot" style="left:580px">17:45</div>
  </div>
  <div id="m5-btn" style="position:absolute; left:110px; top:{1105 + DY}px; width:860px; height:130px; border-radius:65px; background:{RED}; color:{CREAM}; display:flex; align-items:center; justify-content:center; gap:22px; font-weight:900; font-size:50px; letter-spacing:-0.03em; box-shadow:0 20px 40px rgba(230,51,18,0.35)">
    Réserver mon analyse
    <svg width="50" height="36" viewBox="0 0 56 40"><path d="M2 20 H50 M34 4 L52 20 L34 36" fill="none" stroke="{CREAM}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>
  <div id="m5-tap" style="position:absolute; left:{700 - 60}px; top:{1170 + DY - 60}px; width:120px; height:120px; border-radius:50%; border:6px solid rgba(255,255,255,0.9)"></div>
  <div style="position:absolute; left:110px; width:860px; top:{1275 + DY}px; font-weight:600; font-size:28px; line-height:1.28; color:{INK}; opacity:.68">Analyse sans engagement. Les frais et résultats varient selon les produits, la stratégie et la durée de placement.</div>
</div>"""
css = f"""
.day {{ position: absolute; width: 140px; height: 70px; border-radius: 18px; background: #F2EEE6; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 30px; color: {INK}; }}
.slot {{ position: absolute; top: 200px; width: 240px; height: 86px; border-radius: 22px; border: 3px solid #E4DED2; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 38px; color: {INK}; }}
"""
js = f"""
tl.fromTo("#m5-all", {{ clipPath: "circle(0px at 540px {r(700 + DY)}px)" }}, {{ clipPath: "circle(2300px at 540px {r(700 + DY)}px)", duration: 0.55, ease: "power3.inOut" }}, 0);
tl.fromTo("#m5-w1", {{ y: -120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, 0.25);
tl.fromTo("#m5-w2", {{ y: -120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, 0.4);
tl.fromTo("#m5-w3", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.7)" }}, 0.55);
tl.fromTo("#m5-cal", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "expo.out" }}, 0.6);
tl.fromTo("#m5-d2", {{ backgroundColor: "#F2EEE6", color: "{INK}" }}, {{ backgroundColor: "{INK}", color: "{CREAM}", duration: 0.2 }}, 1.1);
tl.fromTo("#m5-pick", {{ backgroundColor: "rgba(0,0,0,0)", borderColor: "#E4DED2", color: "{INK}" }}, {{ backgroundColor: "{INK}", borderColor: "{INK}", color: "{CREAM}", duration: 0.2 }}, 1.35);
tl.fromTo("#m5-btn", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }}, 0.8);
// tap sur le bouton
tl.fromTo("#m5-btn", {{ scale: 1 }}, {{ scale: 0.95, duration: 0.1, ease: "power2.out" }}, 1.8);
tl.to("#m5-btn", {{ scale: 1, duration: 0.25, ease: "back.out(3)" }}, 1.9);
tl.fromTo("#m5-tap", {{ scale: 0.3, opacity: 0.9 }}, {{ scale: 1.6, opacity: 0, duration: 0.6, ease: "power2.out" }}, 1.8);
"""
scenes.append(("m5", m5_start, DUR, body, js, css))

os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
for sc in scenes:
    sid, a, b, body, js = sc[:5]
    css = sc[5] if len(sc) > 5 else ""
    open(os.path.join(OUT, "compositions", f"{sid}.html"), "w").write(scene(sid, a, b - a, body, js, css))

# ---------------------------------------------------------------- sous-titres
skip = set(range(0, 11))
breaks = {11, 15, 17, 24, 29, 31, 34, 36, 41, 47, 51, 54, 59, 63, 69, 72, 75, 78, 81, 85, 87, 90, 94, 98, 101, 105,
          108, 112, 116, 119, 122, 125, 129, 131, 135, 138, 140, 142, 145, 149}
red = {46, 74, 86, 139}
light_at = [(0, "light"), (m3_start, "dark"), (m4_start, "light")]
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
    nxt = s(groups[gi + 1][0]) - 0.08 if gi + 1 < len(groups) else m5_start
    ge = min(nxt, words[g[-1]]["end"] + 0.5, m5_start)
    tone = [t for a, t in light_at if gs >= a - 1e-6][-1]
    sp = []
    for i in g:
        cls = "cw red" if i in red else "cw"
        sp.append(f'<span id="c{i}" class="{cls}">{html.escape(words[i]["text"])}</span>')
        cap_js.append(f'tl.fromTo("#c{i}", {{ opacity: 0.3, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power3.out" }}, {r(s(i))});')
    cap_html.append(f'<div id="cg{gi}" class="cg clip {tone}" data-start="{r(gs)}" data-duration="{r(ge - gs)}" data-track-index="0"><span class="pill">{" ".join(sp)}</span></div>')

cap = f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; }}
    .cg {{ position: absolute; left: 70px; right: 70px; top: {1405 + DY}px; height: 100px; display: flex; align-items: center; justify-content: center; white-space: nowrap; overflow: visible;
      font-family: 'Inter Tight'; font-weight: 800; font-size: 56px; letter-spacing: -0.025em; }}
    .cg.light {{ color: {CREAM}; }}
    .cg.dark {{ color: {INK}; }}
    .pill {{ display: inline-flex; column-gap: 0.26em; padding: 8px 26px 12px; border-radius: 22px; }}
    .cg.light .pill {{ background: rgba(11, 20, 38, 0.8); }}
    .cg.dark .pill {{ background: rgba(255, 255, 255, 0.94); }}
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
      #grain {{ position: absolute; inset: 0; background-image: url('assets/grain.png'); background-size: 512px 512px; mix-blend-mode: overlay; opacity: 0.08; pointer-events: none; z-index: 50; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      <div id="base"></div>
      {hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{r(DUR)}" data-track-index="20" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:30"></div>
      <div id="grain" class="clip" data-start="0" data-duration="{r(DUR)}" data-track-index="21" data-layout-ignore></div>
      <audio id="mix" class="clip" src="assets/mix_L.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="22" data-volume="1"></audio>
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
for f in ["grain.png", "mix_L.wav"]:
    shutil.copy(os.path.join(SRC, "assets", f), A)
for f in ["f1_hook.mp4", "f2_banque.mp4", "f3_assise.mp4", "f4a_cta.mp4", "f4b_cta.mp4"]:
    shutil.copy(os.path.join(ROOT, "clips", f), A)
for f in ["hyperframes.json", "package.json"]:
    shutil.copy(os.path.join(SRC, f), OUT)
print("ok", OUT)
for g in groups:
    print("  ", r(s(g[0])), " ".join(words[i]["text"] for i in g))
