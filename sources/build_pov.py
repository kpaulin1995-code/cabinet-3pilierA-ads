#!/usr/bin/env python3
"""Vidéo 2 « Pilier POV » : 3 plans Kling du pilier (tiroir → montre → tiroir ouvert), voix intérieure Algenib
en voix off, gros sous-titres style Reels, accroche POV, puis écrans comparaison / mais attention / CTA.

Usage : python3 build_pov.py   → out/POV_916
"""
import html, os, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "pov")
SFX = os.path.join(ROOT, "sfx_lib") if os.path.isdir(os.path.join(ROOT, "sfx_lib")) else os.path.join(ROOT, "out", "L_916", ".media", "audio", "sfx")
MUSIC = os.path.join(ROOT, "musique", "M2_ext52.wav") if os.path.isdir(os.path.join(ROOT, "musique")) else "/home/user/musique/M2_ext52.wav"
OUT = os.path.join(ROOT, "out", "POV_916")
A = os.path.join(OUT, "assets")
INK, CREAM, RED, GOLD = "#0B1426", "#F4F1EA", "#E63312", "#F2C879"
W, H = 1080, 1920
V0 = 0.25                       # départ de la voix
VDUR = 31.46
DUR = round(V0 + VDUR + 2.4, 2)
T = lambda x: V0 + x            # temps voix → temps vidéo

# plans : (fichier, début, fin, vitesse) — chaque clip Kling fait 5 s
C1 = ("p1.mp4", 0.0, T(7.6), 0.66)
C2 = ("p2.mp4", T(7.6), T(11.9), 1.0)
C3 = ("p3.mp4", T(11.9), T(17.95), 0.83)
T_CMP, T_BANK1, T_BANK2 = T(17.95), T(18.85), T(21.2)
T_ATT, T_CTA, T_TAP = T(22.9), T(28.2), T(30.9)

def r(x):
    return f"{x:.3f}"

# sous-titres : (début voix, fin voix, texte, mots en rouge)
SUBS = [
    (0.10, 1.55, "Ouh… Salut&nbsp;!", []),
    (1.56, 4.95, "C'est moi, ton 3ème pilier&nbsp;A.", ["3ème", "pilier&nbsp;A."]),
    (5.10, 6.76, "Tu m'as mis en assurance", ["assurance"]),
    (6.78, 7.98, "il y a des années…", ["années…"]),
    (8.40, 10.30, "Mais depuis, tu ne m'as jamais demandé", []),
    (10.32, 11.60, "comment j'allais.", []),
    (12.56, 15.10, "En assurance, tu paies une prime fixe,", ["prime", "fixe,"]),
    (15.29, 17.88, "et une partie sert à payer la couverture et les frais.", ["frais."]),
    (18.08, 20.95, "En banque&nbsp;? Tu verses ce que tu veux, quand tu veux,", ["banque&nbsp;?"]),
    (21.20, 22.75, "et les frais sont souvent plus bas.", ["souvent", "plus", "bas."]),
    (22.97, 23.70, "Mais attention,", ["attention,"]),
    (23.89, 26.06, "selon l'ancienneté et la valeur de rachat,", ["valeur", "de", "rachat,"]),
    (26.10, 28.10, "changer n'est pas toujours intéressant.", []),
    (28.33, 30.52, "Alors… fais-moi analyser gratuitement.", ["gratuitement."]),
    (30.74, 31.46, "Je t'en voudrai pas.", []),
]
sub_html, sub_js = [], []
for k, (a, b, txt, reds) in enumerate(SUBS):
    words = txt.split(" ")
    spans = []
    for j, w in enumerate(words):
        cls = "w red" if w in reds else "w"
        spans.append(f'<span class="{cls}" id="s{k}_{j}">{w}</span>')
    end = SUBS[k + 1][0] if k + 1 < len(SUBS) else VDUR + 1.2
    sub_html.append(f'<div class="sub clip" id="sb{k}" data-start="{r(T(a) - 0.05)}" data-duration="{r(min(end, b + 0.6) - a)}" data-track-index="9">{" ".join(spans)}</div>')
    n = len(words)
    for j in range(n):          # mots qui s'allument un à un, répartis sur la phrase
        tj = T(a) + (b - a) * j / max(1, n)
        sub_js.append(f'tl.fromTo("#s{k}_{j}", {{ opacity: 0.35, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {r(tj)});')

def vid(id_, c, track):
    f, a, b, sp = c
    return (f'<video id="{id_}" class="vid clip" data-start="{r(a)}" data-duration="{r(b - a + 0.05)}" data-media-start="0" '
            f'data-track-index="{track}" src="assets/{f}" muted playsinline></video>')

CHECK = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 900; src: url('assets/fonts/inter-tight-latin-900-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 600; src: url('assets/fonts/inter-tight-latin-600-normal.woff2') format('woff2'); }
@font-face { font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; src: url('assets/fonts/instrument-serif-latin-400-italic.woff2') format('woff2'); }
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
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: 'Inter Tight', sans-serif; background: #000; }}
      .vid {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #grade {{ position: absolute; inset: 0; background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0) 28%, rgba(0,0,0,0.15) 42%, rgba(0,0,0,0.6) 75%, rgba(0,0,0,0.7)); pointer-events: none; }}
      #hook {{ position: absolute; left: 70px; right: 70px; top: 860px; color: #fff; font-weight: 900; font-size: 74px; line-height: 1.04; letter-spacing: -0.035em;
               text-shadow: 0 4px 24px rgba(0,0,0,0.6); }}
      #hook .pov {{ display: inline-block; background: #fff; color: #000; padding: 2px 18px 6px; border-radius: 14px; margin-bottom: 14px; font-size: 56px; text-shadow: none; }}
      #hook .red {{ color: {RED}; }}
      .sub {{ position: absolute; left: 70px; right: 70px; top: 1250px; text-align: center; color: #fff; font-weight: 900; font-size: 66px; line-height: 1.08;
              letter-spacing: -0.03em; text-shadow: 0 3px 0 rgba(0,0,0,0.55), 0 0 30px rgba(0,0,0,0.55); z-index: 40; }}
      .w {{ display: inline-block; }}
      .w.red {{ color: #FF5A3C; }}
      #bg2 {{ position: absolute; inset: 0; background: radial-gradient(90% 60% at 50% 40%, #2A2016 0%, #120F0C 55%, #050505 100%); opacity: 0; }}
      .panel {{ position: absolute; left: 70px; right: 70px; opacity: 0; }}
      #cmp {{ top: 360px; display: flex; gap: 22px; left: 50px; right: 50px; }}
      .col {{ flex: 1; border-radius: 36px; padding: 40px 32px 50px; min-height: 640px; }}
      .col h3 {{ font-weight: 800; font-size: 30px; letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 22px; }}
      .col .it {{ font-weight: 800; font-size: 52px; line-height: 1.1; letter-spacing: -0.02em; margin-top: 22px; display: flex; gap: 14px; align-items: flex-start; }}
      .col .it em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; }}
      #cA {{ background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.75); border: 2px solid rgba(255,255,255,0.12); }}
      #cB {{ background: {CREAM}; color: {INK}; box-shadow: 0 0 0 4px {RED}, 0 30px 70px rgba(0,0,0,0.5); }}
      #cB h3 {{ color: {RED}; }}
      .ck {{ flex: none; width: 50px; height: 50px; border-radius: 50%; background: {RED}; color: #fff; display: inline-flex; align-items: center; justify-content: center; margin-top: -2px; }}
      #att {{ top: 420px; border-radius: 40px; padding: 48px 50px; background: rgba(255,255,255,0.06); border: 3px solid {RED}; color: #fff; }}
      #att .lab {{ color: #FF5A3C; font-weight: 800; font-size: 34px; letter-spacing: 0.16em; text-transform: uppercase; }}
      #att p {{ font-weight: 800; font-size: 62px; line-height: 1.1; letter-spacing: -0.025em; margin-top: 20px; }}
      #att em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; }}
      #cta {{ top: 420px; color: #fff; }}
      #cta .t {{ font-weight: 900; font-size: 86px; line-height: 1; letter-spacing: -0.04em; }}
      #cta .t em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; color: {GOLD}; }}
      #btn {{ display: inline-flex; align-items: center; gap: 18px; margin-top: 54px; background: {RED}; color: #fff; font-weight: 900; font-size: 52px; padding: 32px 52px; border-radius: 28px; box-shadow: 0 18px 44px rgba(230,51,18,0.45); }}
      #sub2 {{ margin-top: 30px; font-weight: 600; font-size: 42px; opacity: 0.85; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      {vid("v1", C1, 1)}
      {vid("v2", C2, 2)}
      {vid("v3", C3, 3)}
      <div id="grade"></div>
      <div id="bg2"></div>
      <div id="hook"><span class="pov">POV</span><br>Tu es un 3ème pilier A en assurance… et personne ne t'a regardé depuis <span class="red">2014.</span></div>
      <div class="panel" id="cmp">
        <div class="col" id="cA"><h3>Assurance</h3><div class="it">Prime fixe imposée</div><div class="it">Une partie paie couverture et frais</div></div>
        <div class="col" id="cB"><h3>Banque</h3><div class="it" id="b1"><span class="ck">{CHECK}</span><span>Vous versez <em>quand</em> vous voulez</span></div>
          <div class="it" id="b2"><span class="ck">{CHECK}</span><span>Frais souvent <em>plus bas</em></span></div></div>
      </div>
      <div class="panel" id="att"><div class="lab">Mais attention</div><p>Selon l'ancienneté et la <em>valeur de rachat</em>, changer n'est pas toujours intéressant.</p></div>
      <div class="panel" id="cta"><div class="t">Faites analyser<br>votre 3ème pilier&nbsp;A <em>gratuitement.</em></div>
        <div id="btn">Analyse gratuite <span>→</span></div><div id="sub2">Un expert vous rappelle.</div></div>
      {chr(10).join("      " + s for s in sub_html)}
      <audio id="mix" class="clip" src="assets/mix_POV.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="22" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // lente poussée caméra sur chaque plan (parallaxe douce)
      tl.fromTo("#v1", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {r(C1[2])}, ease: "none" }}, 0);
      tl.fromTo("#v2", {{ scale: 1.06 }}, {{ scale: 1.0, duration: {r(C2[2] - C2[1])}, ease: "none" }}, {r(C2[1])});
      tl.fromTo("#v3", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {r(C3[2] - C3[1])}, ease: "none" }}, {r(C3[1])});
      tl.fromTo("#v2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {r(C2[1])});
      tl.fromTo("#v3", {{ opacity: 0, filter: "brightness(1.8)" }}, {{ opacity: 1, filter: "brightness(1)", duration: 0.6 }}, {r(C3[1])});
      // accroche (visible dès l'image 0)
      tl.set("#hook", {{ opacity: 1 }}, 0);
      tl.to("#hook", {{ opacity: 0, y: -24, duration: 0.4 }}, 3.4);
      // comparaison : les deux colonnes en même temps, la banque mise en valeur
      tl.to("#bg2", {{ opacity: 1, duration: 0.5 }}, {r(T_CMP - 0.2)});
      tl.fromTo("#cmp", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {r(T_CMP)});
      tl.fromTo("#b1", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {r(T_BANK1)});
      tl.fromTo("#b2", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {r(T_BANK2)});
      tl.to("#cmp", {{ opacity: 0, y: -30, duration: 0.35 }}, {r(T_ATT - 0.35)});
      tl.fromTo("#att", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {r(T_ATT)});
      tl.to("#att", {{ opacity: 0, y: -30, duration: 0.35 }}, {r(T_CTA - 0.35)});
      tl.fromTo("#cta", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {r(T_CTA)});
      tl.to("#btn", {{ scale: 0.95, duration: 0.12, yoyo: true, repeat: 1 }}, {r(T_TAP)});
      {chr(10).join("      " + j for j in sub_js)}
      tl.set({{}}, {{}}, {r(DUR)});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
os.makedirs(A, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(index)
shutil.copytree(os.path.join(ROOT, "src", "assets", "fonts"), os.path.join(A, "fonts"), dirs_exist_ok=True)
for f in ["hyperframes.json", "package.json"]:
    shutil.copy(os.path.join(ROOT, "src", f), OUT)
# clips au ralenti / à la vitesse voulue, sans son
for f, a, b, sp in (C1, C2, C3):
    src = os.path.join(P, f)
    if os.path.exists(src):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-an", "-vf", f"setpts=PTS/{sp},fps=30", "-c:v", "libx264", "-crf", "16",
                        "-pix_fmt", "yuv420p", os.path.join(A, f)], check=True)

# ---------------------------------------------------------------- son : voix -15 LUFS, ambiance, tiroir, whoosh doux, musique minimale
amb = os.path.join(A, "room.wav"); drawer = os.path.join(A, "drawer.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anoisesrc=c=brown:a=0.08:d={DUR}:r=48000", "-af", "lowpass=f=500,highpass=f=60", amb], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anoisesrc=c=pink:a=0.5:d=0.9:r=48000",
                "-af", "bandpass=f=900:w=700,volume='if(lt(t,0.75),0.6+0.4*sin(30*t),0)':eval=frame,afade=t=in:d=0.08,afade=t=out:st=0.6:d=0.3", drawer], check=True)
WHOOSH = os.path.join(SFX, "sfx_002.mp3"); CLICK = os.path.join(SFX, "sfx_001.mp3")
events = [(drawer, C3[1] - 0.35, 0.6), (WHOOSH, T_CMP - 0.2, 0.18), (WHOOSH, T_ATT - 0.3, 0.15), (WHOOSH, T_CTA - 0.3, 0.15), (CLICK, T_TAP, 0.5)]
inputs = ["-i", os.path.join(P, "voix_POV_f.wav"), "-i", MUSIC, "-i", amb]
chains = []
for k, (f, t, vol) in enumerate(events):
    inputs += ["-i", f]
    ms = int(t * 1000)
    chains.append(f"[{k + 3}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
d0 = int(V0 * 1000)
filt = (f"[0]aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=9,adelay={d0}|{d0},apad=whole_dur={DUR},asplit=2[v][sc];"
        f"[1]atrim=0:{DUR},asetpts=N/SR/TB,aresample=48000,loudnorm=I=-24:TP=-3:LRA=11,volume='if(lt(t,{C3[1]:.2f}),0.35,1)':eval=frame,"
        f"afade=t=in:d=1.5,afade=t=out:st={DUR - 1.8}:d=1.8[m];"
        "[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=500:makeup=1[md];"
        f"[2]aresample=48000,volume=0.5,afade=t=out:st={C3[1]:.2f}:d=2[a];"
        + ";".join(chains) + ";[v][md][a]" + "".join(f"[e{k}]" for k in range(len(events)))
        + f"amix=inputs={len(events) + 3}:normalize=0:duration=first,alimiter=limit=0.89")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-ar", "48000", "-ac", "2", "-t", str(DUR), os.path.join(A, "mix_POV.wav")], check=True)
print("ok", OUT, DUR, "s")
