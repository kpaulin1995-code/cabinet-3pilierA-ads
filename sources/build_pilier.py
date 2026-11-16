#!/usr/bin/env python3
"""Vidéo 2 « Le pilier qui parle », version bonds (sans lip-sync) : le personnage détouré se déplace en bonds
(squash & stretch, ombre au sol), parle bouche fermée et rebondit au rythme de sa voix (enveloppe audio),
répliques dans des bulles de BD. Voix Algenib.

Usage : python3 build_pilier.py jet1   → out/P_jet1 (premier jet ~15 s)
"""
import array, html, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "pilier")
SFX = os.path.join(ROOT, "sfx_lib") if os.path.isdir(os.path.join(ROOT, "sfx_lib")) else os.path.join(ROOT, "out", "L_916", ".media", "audio", "sfx")
VERSION = sys.argv[1] if len(sys.argv) > 1 else "jet1"
OUT = os.path.join(ROOT, "out", f"P_{VERSION}")
A = os.path.join(OUT, "assets")
INK, CREAM, RED = "#0B1426", "#F4F1EA", "#E63312"
W, H = 1080, 1920
V0 = 1.30                  # la voix démarre après l'entrée en bonds
VOICE = os.path.join(P, "voix_Algenib.wav")
VDUR = 13.40
DUR = V0 + VDUR + 1.2
PW, PH = 470, 884          # taille du pilier à l'écran (détourage 868×1632)
FLOOR = 1470               # y du sol (bas du socle), au-dessus des 400 px du bas
CX = 540

def r(x):
    return f"{x:.3f}"

# répliques (temps dans la voix, d'après la transcription)
LINES = [(0.10, 1.95, "Ouh… Salut&nbsp;!"), (1.88, 6.05, "C'est moi, ton 3ème pilier&nbsp;A."),
         (6.00, 8.75, "Tu m'as mis en assurance il y a des années…"),
         (8.80, 13.30, "Mais depuis, tu ne m'as jamais demandé comment j'allais.")]

# enveloppe de la voix à 15 i/s → petit rebond « parlé »
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", VOICE, "-ac", "1", "-ar", "15000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
a = array.array("h"); a.frombytes(raw)
hop = 1000
env = [sum(abs(x) for x in a[i:i + hop]) / hop for i in range(0, len(a) - hop, hop)]
mx = sorted(env)[int(len(env) * 0.97)] or 1
env = [min(1.0, e / mx) for e in env]
talk_js = []
for k, e in enumerate(env):
    t = V0 + k / 15
    talk_js.append(f'tl.to("#body", {{ scaleY: {1 + 0.025 * e:.3f}, scaleX: {1 - 0.012 * e:.3f}, y: {-8 * e:.1f}, duration: 0.066, ease: "sine.out" }}, {r(t)});')

# bouche : 4 poses (fermée / « eh » / « oh » / « ah ») choisies image par image sur le volume de la voix (24 i/s)
FPS = 24
raw24 = subprocess.run(["ffmpeg", "-v", "error", "-i", VOICE, "-ac", "1", "-ar", "24000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
b24 = array.array("h"); b24.frombytes(raw24)
e24 = [sum(abs(x) for x in b24[i:i + 1000]) / 1000 for i in range(0, len(b24) - 1000, 1000)]
m24 = sorted(e24)[int(len(e24) * 0.97)] or 1
e24 = [min(1.0, e / m24) for e in e24]
state = []
for k, e in enumerate(e24):
    nxt = e24[k + 1] if k + 1 < len(e24) else 0
    v = max(e, nxt)                       # la bouche s'ouvre une image avant le son
    st = 0 if v < 0.14 else (1 if v < 0.42 else (2 if v < 0.72 else 3))
    if st == 3 and k % 3 == 1:            # variété : « oh » sur certaines syllabes fortes
        st = 2
    state.append(st)
for k in range(1, len(state) - 1):        # pas de pose tenue une seule image
    if state[k] != state[k - 1] and state[k] != state[k + 1]:
        state[k] = state[k - 1]
mouth_js, cur = [], 0
for k, st in enumerate(state):
    if st != cur:
        t = V0 + k / FPS
        mouth_js.append(f'tl.set("#mE", {{ opacity: {1 if st == 1 else 0} }}, {r(t)}); tl.set("#mO", {{ opacity: {1 if st == 2 else 0} }}, {r(t)}); tl.set("#mA", {{ opacity: {1 if st == 3 else 0} }}, {r(t)});')
        cur = st
mouth_js.append(f'tl.set(["#mE", "#mO", "#mA"], {{ opacity: 0 }}, {r(V0 + len(state) / FPS)});')

# entrée : 3 bonds de la droite vers le centre
hops = [(1250, 980, 0.0), (980, 760, 0.42), (760, CX, 0.84)]
hop_js, boings = [], []
for x0, x1, t in hops:
    hop_js.append(f'tl.fromTo("#pil", {{ x: {x0 - CX} }}, {{ x: {x1 - CX}, duration: 0.38, ease: "none" }}, {r(t)});')
    hop_js.append(f'tl.fromTo("#jump", {{ y: 0 }}, {{ y: -230, duration: 0.19, ease: "power2.out", yoyo: true, repeat: 1 }}, {r(t)});')
    hop_js.append(f'tl.fromTo("#body", {{ scaleY: 1.12, scaleX: 0.92 }}, {{ scaleY: 1, scaleX: 1, duration: 0.16, ease: "power1.out" }}, {r(t)});')
    hop_js.append(f'tl.to("#body", {{ scaleY: 0.8, scaleX: 1.14, duration: 0.06, ease: "power2.in", yoyo: true, repeat: 1 }}, {r(t + 0.38)});')
    hop_js.append(f'tl.fromTo("#shadow", {{ scaleX: 1 }}, {{ scaleX: 0.55, opacity: 0.25, duration: 0.19, ease: "power2.out", yoyo: true, repeat: 1 }}, {r(t)});')
    boings.append(t + 0.36)

# réactions
T_SIGH = V0 + 0.15
T_HOP = V0 + 8.62           # petit saut indigné sur « des années »
T_TILT = V0 + 11.4          # tête qui penche sur « comment j'allais »
T_END = V0 + VDUR - 0.1
react_js = [
    f'tl.to("#body", {{ scaleY: 0.93, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }}, {r(T_SIGH)});',
    f'tl.fromTo("#jump", {{ y: 0 }}, {{ y: -110, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }}, {r(T_HOP)});',
    f'tl.to("#body", {{ scaleY: 0.86, scaleX: 1.1, duration: 0.05, yoyo: true, repeat: 1 }}, {r(T_HOP + 0.28)});',
    f'tl.to("#tilt", {{ rotation: -7, duration: 0.45, ease: "back.out(2)" }}, {r(T_TILT)});',
    f'tl.to("#tilt", {{ rotation: 0, duration: 0.4, ease: "power2.inOut" }}, {r(T_END + 0.2)});',
    f'tl.fromTo("#jump", {{ y: 0 }}, {{ y: -160, duration: 0.17, ease: "power2.out", yoyo: true, repeat: 1 }}, {r(T_END + 0.35)});',
    f'tl.to("#body", {{ scaleY: 0.82, scaleX: 1.12, duration: 0.06, yoyo: true, repeat: 1 }}, {r(T_END + 0.69)});',
]

bub_html, bub_js = [], []
for k, (a0, a1, txt) in enumerate(LINES):
    bub_html.append(f'<div class="bub" id="q{k}">{txt}</div>')
    bub_js.append(f'tl.fromTo("#q{k}", {{ opacity: 0, scale: 0.6, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.4)" }}, {r(V0 + a0)});')
    bub_js.append(f'tl.to("#q{k}", {{ opacity: 0, scale: 0.9, duration: 0.15 }}, {r(V0 + a1)});')

FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 900; src: url('assets/fonts/inter-tight-latin-900-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
"""
index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      {FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: 'Inter Tight', sans-serif; }}
      #bg {{ position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 62%, #1F3157 0%, #142243 45%, {INK} 100%); }}
      #floor {{ position: absolute; left: 0; right: 0; top: {FLOOR - 20}px; height: 500px; background: linear-gradient(rgba(255,255,255,0.04), rgba(255,255,255,0)); }}
      #pil {{ position: absolute; left: {CX - PW // 2}px; top: {FLOOR - PH}px; width: {PW}px; height: {PH}px; }}
      #shadow {{ position: absolute; left: {PW // 2 - 190}px; top: {PH - 34}px; width: 380px; height: 60px; border-radius: 50%; background: rgba(0,0,0,0.55); filter: blur(10px); }}
      #jump, #tilt, #body {{ position: absolute; inset: 0; }}
      #body {{ transform-origin: 50% 100%; }}
      #tilt {{ transform-origin: 50% 85%; }}
      #body img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; }}
      #body img.full, #body img.patch {{ opacity: 0; }}
      #body img.patch {{ left: 30.645%; top: 45.221%; width: 39.171%; height: 17.157%; }}
      .bub {{ position: absolute; left: 90px; right: 90px; top: 300px; padding: 30px 40px; border-radius: 42px; background: {CREAM}; color: {INK};
              font-weight: 800; font-size: 58px; line-height: 1.12; letter-spacing: -0.02em; text-align: center; opacity: 0; box-shadow: 0 20px 50px rgba(0,0,0,0.35); }}
      .bub::after {{ content: ""; position: absolute; left: 50%; bottom: -34px; margin-left: -10px; border: 22px solid transparent; border-top: 30px solid {CREAM}; border-bottom: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      <div id="bg"></div><div id="floor"></div>
      <div id="pil">
        <div id="shadow"></div>
        <div id="jump"><div id="tilt"><div id="body"><img src="assets/pilier_cut.png" alt="" /><img id="mA" class="full" src="assets/pilier_ah_cut.png" alt="" /><img id="mE" class="patch" src="assets/mouth_eh_patch.png" alt="" /><img id="mO" class="patch" src="assets/mouth_oh_patch.png" alt="" /></div></div></div>
      </div>
      {"".join(bub_html)}
      <audio id="mix" class="clip" src="assets/mix_P.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="22" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#pil", {{ x: {1250 - CX} }}, 0);
      {chr(10).join("      " + j for j in hop_js)}
      {chr(10).join("      " + j for j in talk_js)}
      {chr(10).join("      " + j for j in mouth_js)}
      {chr(10).join("      " + j for j in react_js)}
      {chr(10).join("      " + j for j in bub_js)}
      tl.set({{}}, {{}}, {r(DUR)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
os.makedirs(A, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(index)
shutil.copytree(os.path.join(ROOT, "src", "assets", "fonts"), os.path.join(A, "fonts"), dirs_exist_ok=True)
for f in ["pilier_cut.png", "pilier_ah_cut.png", "mouth_eh_patch.png", "mouth_oh_patch.png"]:
    shutil.copy(os.path.join(P, f), A)
for f in ["hyperframes.json", "package.json"]:
    shutil.copy(os.path.join(ROOT, "src", f), OUT)

# ---------------------------------------------------------------- bruitages : boing synthétisé + pop / tap de la bibliothèque
boing = os.path.join(A, "boing.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                "aevalsrc='0.6*sin(2*PI*(170*t+260*t*t+5*sin(2*PI*16*t)))*exp(-7*t)':s=48000:d=0.42", boing], check=True)
CLICK, POP = os.path.join(SFX, "sfx_001.mp3"), os.path.join(SFX, "sfx_003.mp3")
events = [(boing, t, 0.55) for t in boings] + [(POP, V0 + a0, 0.35) for a0, _, _ in LINES] + \
         [(boing, T_HOP + 0.25, 0.4), (CLICK, T_TILT, 0.4), (boing, T_END + 0.66, 0.5)]
inputs, chains = ["-i", VOICE], []
for k, (f, t, vol) in enumerate(events):
    inputs += ["-i", f]
    ms = int(t * 1000)
    chains.append(f"[{k + 1}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
d0 = int(V0 * 1000)
filt = (f"[0]aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=9,adelay={d0}|{d0},apad=whole_dur={DUR}[v];" + ";".join(chains)
        + ";[v]" + "".join(f"[e{k}]" for k in range(len(events))) + f"amix=inputs={len(events) + 1}:normalize=0:duration=first,alimiter=limit=0.89")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-ar", "48000", "-ac", "2", "-t", str(DUR), os.path.join(A, "mix_P.wav")], check=True)
print("ok", OUT, f"{DUR:.1f} s")
