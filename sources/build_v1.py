#!/usr/bin/env python3
"""Vidéo 1 « Courte face caméra » (~19,6 s, 9:16) : face caméra (hook) → motion prime/frais/versements
→ face caméra « Mais attention » → bouton. Clips FLORA muets, voix off d'origine.

Usage : python3 build_v1.py   → out/V1_916 + assets/mix_V1.wav
"""
import html, json, os, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out", "V1_916")
A = os.path.join(OUT, "assets")
SFX = os.path.join(ROOT, "sfx_lib") if os.path.isdir(os.path.join(ROOT, "sfx_lib")) else os.path.join(ROOT, "out", "L_916", ".media", "audio", "sfx")
MUSIC = os.path.join(ROOT, "musique", "M2_ext52.wav") if os.path.isdir(os.path.join(ROOT, "musique")) else "/home/user/musique/M2_ext52.wav"
INK, CREAM, RED, SLATE = "#0B1426", "#F4F1EA", "#E63312", "#8C96A8"
W, H, DUR = 1080, 1920, 19.6

words = json.load(open(os.path.join(ROOT, "v1", "tx_V1.json")))
FIX = {1: "3ème", 6: "assurance ?", 42: "bas,", 43: "et", 54: "attention !"}
for i, t in FIX.items():
    words[i]["text"] = t
s = lambda i: words[i]["start"]

# découpe : fins de phrase mesurées sur la voix (silencedetect), pas sur Whisper
F1_END = 4.97          # fin de « pour vous. »
F2_START = 11.99       # « Mais attention » (le clip B a 0,01 s de silence en tête)
F2_END = 15.98         # fin de « intéressant. »
T_BANK = s(35)         # « En banque »
T_CTA = F2_END

def r(x):
    return f"{x:.3f}"

FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 900; src: url('assets/fonts/inter-tight-latin-900-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 600; src: url('assets/fonts/inter-tight-latin-600-normal.woff2') format('woff2'); }
@font-face { font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; src: url('assets/fonts/instrument-serif-latin-400-italic.woff2') format('woff2'); }
"""
CHECK = '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOCK = '<svg viewBox="0 0 24 24" width="30" height="30"><rect x="5" y="10.5" width="14" height="10" rx="2.5" fill="currentColor"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" fill="none" stroke="currentColor" stroke-width="2.6"/></svg>'

# ---------------------------------------------------------------- sous-titres (le hook est déjà écrit à l'écran)
skip = set(range(0, 7))
breaks = {7, 13, 17, 22, 24, 29, 35, 37, 43, 46, 50, 53, 55, 59, 62}
red = {34, 40, 45, 61, 71}
groups, cur = [], []
for i in range(len(words)):
    if i in skip:
        continue
    if i >= 67:        # après « intéressant », le texte est déjà à l'écran (carte de fin)
        break
    if cur and (i in breaks or len(cur) >= 6):
        groups.append(cur); cur = []
    cur.append(i)
groups.append(cur)
cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    gs = max(0.05, s(g[0]) - 0.08)
    nxt = s(groups[gi + 1][0]) - 0.08 if gi + 1 < len(groups) else T_CTA
    ge = min(nxt, words[g[-1]]["end"] + 0.5, T_CTA)
    sp = []
    for i in g:
        cls = "cw red" if i in red else "cw"
        sp.append(f'<span id="c{i}" class="{cls}">{html.escape(words[i]["text"])}</span>')
        cap_js.append(f'tl.fromTo("#c{i}", {{ opacity: 0.3, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power3.out" }}, {r(s(i))});')
    cap_html.append(f'<div id="cg{gi}" class="cg clip" data-start="{r(gs)}" data-duration="{r(ge - gs)}" data-track-index="9"><span class="pill">{" ".join(sp)}</span></div>')

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
      #base {{ position: absolute; inset: 0; background: {INK}; }}
      #grain {{ position: absolute; inset: 0; background-image: url('assets/grain.png'); background-size: 512px 512px; mix-blend-mode: overlay; opacity: 0.08; pointer-events: none; z-index: 50; }}
      .vid {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .layer {{ position: absolute; inset: 0; overflow: hidden; }}
      em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }}
      /* hook */
      #hook {{ position: absolute; left: 70px; right: 70px; top: 1090px; color: {CREAM}; font-weight: 900; font-size: 98px; line-height: 0.98; letter-spacing: -0.04em;
               text-shadow: 0 4px 30px rgba(0,0,0,0.45); }}
      #hook .red {{ color: {RED}; }}
      #shade1 {{ position: absolute; left: 0; right: 0; bottom: 0; height: 1000px; background: linear-gradient(rgba(11,20,38,0), rgba(11,20,38,0.82)); }}
      /* motion */
      .card {{ position: absolute; left: 90px; right: 90px; border-radius: 44px; background: {CREAM}; color: {INK}; padding: 44px 52px; box-shadow: 0 30px 70px rgba(0,0,0,0.4); }}
      .lab {{ font-weight: 800; font-size: 30px; letter-spacing: 0.14em; text-transform: uppercase; color: {SLATE}; }}
      .big {{ font-weight: 900; font-size: 84px; letter-spacing: -0.035em; line-height: 1; margin-top: 16px; display: flex; align-items: center; gap: 22px; }}
      .ico {{ width: 72px; height: 72px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; flex: none; }}
      #mA {{ top: 330px; }}
      #bar {{ display: flex; height: 92px; border-radius: 22px; overflow: hidden; margin-top: 36px; }}
      #bar div {{ height: 100%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 30px; color: #fff; }}
      #b1 {{ background: {INK}; flex: 4.6; }} #b2 {{ background: #5F6B80; flex: 3.4; }} #b3 {{ background: {RED}; flex: 2; }}
      #mB {{ top: 520px; }}
      .row {{ display: flex; align-items: center; gap: 20px; font-weight: 800; font-size: 50px; letter-spacing: -0.02em; margin-top: 26px; }}
      #cta {{ position: absolute; left: 90px; right: 90px; top: 560px; }}
      .title {{ font-weight: 900; font-size: 92px; line-height: 0.98; letter-spacing: -0.04em; color: {CREAM}; white-space: nowrap; }}
      .title .red {{ color: {RED}; }}
      #btn {{ display: inline-flex; align-items: center; gap: 20px; margin-top: 56px; background: {RED}; color: #fff; font-weight: 900; font-size: 54px;
              padding: 34px 56px; border-radius: 30px; box-shadow: 0 18px 44px rgba(230,51,18,0.4); }}
      #sub {{ margin-top: 34px; font-weight: 600; font-size: 44px; color: {CREAM}; opacity: 0.9; }}
      #finger {{ position: absolute; left: 0; top: 0; width: 90px; height: 90px; border-radius: 50%; background: rgba(244,241,234,0.85); border: 4px solid #fff; opacity: 0; }}
      #att {{ position: absolute; left: 70px; top: 330px; padding: 16px 30px; border-radius: 999px; background: {RED}; color: #fff; font-weight: 900; font-size: 46px; opacity: 0; }}
      /* sous-titres */
      .cg {{ position: absolute; left: 60px; right: 60px; top: 1405px; height: 100px; display: flex; align-items: center; justify-content: center; white-space: nowrap;
             font-weight: 800; font-size: 54px; letter-spacing: -0.025em; color: {CREAM}; z-index: 40; }}
      .pill {{ display: inline-flex; column-gap: 0.26em; padding: 8px 26px 12px; border-radius: 22px; background: rgba(11,20,38,0.82); }}
      .cw {{ display: inline-block; }}
      .cw.red {{ color: {RED}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      <div id="base"></div>

      <div class="layer" id="L1" style="z-index:1">
        <video id="v1" class="vid clip" data-start="0" data-duration="{r(F1_END + 0.1)}" data-media-start="0" data-track-index="1" src="assets/v1_A.mp4" muted playsinline></video>
        <div id="shade1"></div>
        <div id="hook"><div id="h0">Votre 3ème pilier A</div><div id="h1">est en <em>assurance&#8239;?</em></div></div>
      </div>

      <div class="layer" id="M1" style="z-index:2; background:{INK}; clip-path: inset(100% 0% 0% 0%)">
        <div class="card" id="mA">
          <div class="lab">En assurance · chaque prime</div>
          <div class="big"><span class="ico" style="background:{INK}; color:{CREAM}">{LOCK}</span>Prime <em>fixe</em></div>
          <div id="bar"><div id="b1">Épargne</div><div id="b2">Couverture</div><div id="b3">Frais</div></div>
        </div>
        <div class="card" id="mB" style="background:{INK}; color:{CREAM}; border: 3px solid rgba(244,241,234,0.18)">
          <div class="lab" style="color:{RED}">En banque</div>
          <div class="row" id="r1"><span class="ico" style="background:{RED}; color:#fff">{CHECK}</span>Frais souvent <em>plus bas</em></div>
          <div class="row" id="r2"><span class="ico" style="background:{CREAM}; color:{INK}">{CHECK}</span>Versements <em>libres</em></div>
        </div>
      </div>

      <div class="layer" id="L2" style="z-index:3; clip-path: circle(0px at 540px 760px)">
        <video id="v2" class="vid clip" data-start="{r(F2_START)}" data-duration="{r(F2_END - F2_START + 0.1)}" data-media-start="0" data-track-index="2" src="assets/v1_B.mp4" muted playsinline></video>
        <div id="att">Mais attention&#8239;!</div>
      </div>

      <div class="layer" id="M2" style="z-index:4; background:{INK}; clip-path: inset(0% 0% 0% 100%)">
        <div id="cta">
          <div class="title">Faites analyser<br><span class="red">votre <em>contrat.</em></span></div>
          <div id="btn">Analyse gratuite <span>→</span></div>
          <div id="sub">Un expert vous rappelle.</div>
          <div id="finger"></div>
        </div>
      </div>

      {chr(10).join("      " + c for c in cap_html)}
      <div id="grain" class="clip" data-start="0" data-duration="{r(DUR)}" data-track-index="21" data-layout-ignore></div>
      <audio id="mix" class="clip" src="assets/mix_V1.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="22" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // hook, visible dès l'image 0
      tl.set(["#h0", "#h1"], {{ opacity: 1 }}, 0);
      tl.fromTo("#h1", {{ scale: 1 }}, {{ scale: 1.04, transformOrigin: "0% 50%", duration: 0.3, yoyo: true, repeat: 1 }}, {r(s(6))});
      tl.to("#hook", {{ opacity: 0, y: -30, duration: 0.3 }}, {r(s(7) - 0.1)});
      // M1 : couvre le visage pile à la fin de la phrase
      tl.fromTo("#M1", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.2, ease: "power3.inOut" }}, {r(F1_END - 0.2)});
      tl.fromTo("#mA", {{ y: 90, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "expo.out" }}, {r(F1_END)});
      tl.fromTo("#bar div", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.35, stagger: 0.12, ease: "back.out(2)" }}, {r(s(28))});
      tl.fromTo("#b2", {{ filter: "brightness(1)" }}, {{ filter: "brightness(1.35)", duration: 0.2, yoyo: true, repeat: 1 }}, {r(s(31))});
      tl.fromTo("#b3", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }}, {r(s(34))});
      tl.fromTo("#mB", {{ y: 90, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "expo.out" }}, {r(T_BANK - 0.05)});
      tl.fromTo("#r1", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }}, {r(s(38))});
      tl.fromTo("#r2", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }}, {r(s(45))});
      tl.to("#mA", {{ opacity: 0, y: -80, duration: 0.3, ease: "power2.in" }}, {r(T_BANK - 0.3)});
      // F2 : « Mais attention »
      tl.fromTo("#L2", {{ clipPath: "circle(0px at 540px 760px)" }}, {{ clipPath: "circle(2300px at 540px 760px)", duration: 0.35, ease: "power3.inOut" }}, {r(F2_START - 0.05)});
      tl.fromTo("#att", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }}, {r(s(53))});
      tl.to("#att", {{ opacity: 0, duration: 0.25 }}, {r(s(56))});
      // M2 : bouton, couvre F2 pile à la fin de « intéressant »
      tl.fromTo("#M2", {{ clipPath: "inset(0% 0% 0% 100%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.2, ease: "power3.inOut" }}, {r(F2_END - 0.2)});
      tl.fromTo("#cta", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {r(F2_END)});
      tl.fromTo("#btn", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2.4)" }}, {r(s(71) - 0.2)});
      tl.fromTo("#finger", {{ opacity: 0, x: 640, y: 560 }}, {{ opacity: 1, x: 330, y: 255, duration: 0.5, ease: "power2.out" }}, {r(s(75) - 0.1)});
      tl.to(["#finger", "#btn"], {{ scale: 0.88, duration: 0.1, yoyo: true, repeat: 1 }}, {r(s(75) + 0.45)});
      tl.to("#finger", {{ opacity: 0, duration: 0.3 }}, {r(s(75) + 1.0)});
      {chr(10).join("      " + j for j in cap_js)}
      for (let k = 0; k < {int(DUR * 12)}; k++) {{
        tl.set("#grain", {{ backgroundPosition: `${{(k * 173) % 512}}px ${{(k * 311) % 512}}px` }}, k / 12);
      }}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
os.makedirs(A, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(index)
shutil.copytree(os.path.join(ROOT, "src", "assets", "fonts"), os.path.join(A, "fonts"), dirs_exist_ok=True)
shutil.copy(os.path.join(ROOT, "src", "assets", "grain.png"), A)
for f in ["hyperframes.json", "package.json"]:
    shutil.copy(os.path.join(ROOT, "src", f), OUT)
for f in ["v1_A.mp4", "v1_B.mp4"]:
    if os.path.exists(os.path.join(ROOT, "v1", f)):
        shutil.copy(os.path.join(ROOT, "v1", f), A)

# ---------------------------------------------------------------- mix : voix -15 LUFS, musique -22 baissée sous la voix, bruitages
CLICK, WHOOSH, POP = "sfx_001.mp3", "sfx_002.mp3", "sfx_003.mp3"
events = [(WHOOSH, F1_END - 0.25, 0.3), (POP, s(28), 0.4), (POP, s(34), 0.45), (WHOOSH, T_BANK - 0.1, 0.25),
          (POP, s(38), 0.45), (POP, s(45), 0.45), (WHOOSH, F2_START - 0.1, 0.28), (POP, s(53), 0.5),
          (WHOOSH, F2_END - 0.25, 0.3), (CLICK, s(75) + 0.45, 0.85)]
inputs = ["-i", os.path.join(ROOT, "v1", "voix_V1.wav"), "-i", MUSIC]
chains = []
for k, (f, t, vol) in enumerate(events):
    inputs += ["-i", os.path.join(SFX, f)]
    ms = int(t * 1000)
    chains.append(f"[{k + 2}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
filt = (f"[0]aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=7,apad=whole_dur={DUR},asplit=2[v][sc];"
        f"[1]atrim=0:{DUR},asetpts=N/SR/TB,aresample=48000,loudnorm=I=-22:TP=-3:LRA=11,afade=t=in:d=0.3,afade=t=out:st={DUR - 1.5}:d=1.5[m];"
        "[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450:makeup=1[md];"
        + ";".join(chains) + ";[v][md]" + "".join(f"[e{k}]" for k in range(len(events)))
        + f"amix=inputs={len(events) + 2}:normalize=0:duration=first,alimiter=limit=0.89")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-ar", "48000", "-ac", "2", "-t", str(DUR), os.path.join(A, "mix_V1.wav")], check=True)
print("ok", OUT, "groupes :", len(groups))
for g in groups:
    print("  ", r(s(g[0])), " ".join(words[i]["text"] for i in g))
