#!/usr/bin/env python3
"""Vidéo 3 « La conversation » : messagerie générique (Papa / Moi) puis cartes motion et bouton.

Usage : python3 build_v3.py   → out/V3_916 (9:16) + assets/mix_V3.wav (musique + bruitages, pas de voix)
"""
import html, os, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out", "V3_916")
SFX = os.path.join(ROOT, "sfx_lib")
MUSIC = os.path.join(ROOT, "musique", "M2_ext52.wav")
INK, CREAM, RED, SLATE = "#0B1426", "#F4F1EA", "#E63312", "#8C96A8"
W, H, DUR = 1080, 1920, 18.5

# (qui, texte, début de la saisie, apparition de la bulle)
MSGS = [
    ("papa", "Ton 3ème pilier A, il est où ?", None, 0.0),
    ("moi", "À la banque, je crois ?", 2.40, 3.00),
    ("papa", "Non. En assurance. Depuis 2014. 😬", 3.90, 4.90),
    ("moi", "…et c'est grave ?", 6.30, 6.80),
    ("papa", "Pas forcément. Mais fais-le vérifier.", 7.60, 8.50),
]
T_MOTION = 10.40      # passage aux cartes
T_SWITCH = 11.20      # prime fixe → versements libres
T_FRAIS = 12.00
T_ATT = 13.20         # « Mais attention »
T_CTA = 16.00
T_TAP = 17.00

def r(x):
    return f"{x:.3f}"

slots, js = [], []
for k, (who, txt, t_type, t_msg) in enumerate(MSGS):
    side = "l" if who == "papa" else "r"
    slots.append(f"""
      <div class="slot {side}" id="s{k}">
        <div class="typing {side}" id="t{k}"><i></i><i></i><i></i></div>
        <div class="bub {side}" id="b{k}">{html.escape(txt)}</div>
      </div>""")
    if t_type is None:   # 1re bulle déjà affichée à l'image 0 (vignette = la question)
        js.append(f'tl.set("#b{k}", {{ opacity: 1 }}, 0);')
        continue
    js.append(f'tl.fromTo("#t{k}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {r(t_type)});')
    for d in range(3):
        js.append(f'tl.fromTo("#t{k} i:nth-child({d + 1})", {{ y: 0 }}, {{ y: -10, duration: 0.18, yoyo: true, repeat: {int((t_msg - t_type) / 0.36)}, ease: "sine.inOut" }}, {r(t_type + 0.1 + d * 0.12)});')
    js.append(f'tl.to("#t{k}", {{ opacity: 0, duration: 0.08 }}, {r(t_msg - 0.04)});')
    js.append(f'tl.fromTo("#b{k}", {{ opacity: 0, scale: 0.7, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "back.out(2.2)" }}, {r(t_msg)});')

FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 900; src: url('assets/fonts/inter-tight-latin-900-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 600; src: url('assets/fonts/inter-tight-latin-600-normal.woff2') format('woff2'); }
@font-face { font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; src: url('assets/fonts/instrument-serif-latin-400-italic.woff2') format('woff2'); }
@font-face { font-family: 'Emoji'; src: url('assets/fonts/NotoColorEmoji.ttf') format('truetype'); }
"""
CHECK = '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOCK = '<svg viewBox="0 0 24 24" width="30" height="30"><rect x="5" y="10.5" width="14" height="10" rx="2.5" fill="currentColor"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" fill="none" stroke="currentColor" stroke-width="2.6"/></svg>'

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
      #root {{ position: relative; width: 100%; height: 100%; font-family: 'Inter Tight', 'Emoji', sans-serif; }}
      #base {{ position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 35%, #16233D 0%, {INK} 70%); }}
      #grain {{ position: absolute; inset: 0; background-image: url('assets/grain.png'); background-size: 512px 512px; mix-blend-mode: overlay; opacity: 0.08; pointer-events: none; z-index: 50; }}

      /* messagerie générique : aucune marque, aucune barre système */
      #chat {{ position: absolute; left: 70px; right: 70px; top: 300px; height: 1150px; border-radius: 56px; background: {CREAM};
              box-shadow: 0 40px 90px rgba(0,0,0,0.45); overflow: hidden; }}
      #head {{ height: 150px; display: flex; align-items: center; gap: 26px; padding: 0 44px; border-bottom: 2px solid rgba(11,20,38,0.08); }}
      #ava {{ width: 88px; height: 88px; border-radius: 50%; background: {INK}; color: {CREAM}; display: flex; align-items: center; justify-content: center;
              font-weight: 900; font-size: 42px; }}
      #name {{ font-weight: 900; font-size: 46px; color: {INK}; letter-spacing: -0.02em; }}
      #list {{ position: absolute; left: 36px; right: 36px; top: 190px; display: flex; flex-direction: column; gap: 26px; }}
      .slot {{ position: relative; display: flex; }}
      .slot.r {{ justify-content: flex-end; }}
      .bub {{ max-width: 800px; padding: 28px 38px; border-radius: 44px; font-weight: 600; font-size: 54px; line-height: 1.22; letter-spacing: -0.01em; opacity: 0; }}
      .bub.l {{ background: #FFFFFF; color: {INK}; border-bottom-left-radius: 12px; box-shadow: 0 6px 18px rgba(11,20,38,0.08); transform-origin: 0% 100%; }}
      .bub.r {{ background: {INK}; color: {CREAM}; border-bottom-right-radius: 12px; transform-origin: 100% 100%; }}
      .typing {{ position: absolute; top: 0; display: flex; gap: 12px; padding: 40px 38px; border-radius: 40px; opacity: 0; }}
      .typing.l {{ left: 0; background: #FFFFFF; border-bottom-left-radius: 12px; }}
      .typing.r {{ right: 0; background: {INK}; border-bottom-right-radius: 12px; }}
      .typing i {{ width: 18px; height: 18px; border-radius: 50%; background: {SLATE}; display: block; }}

      /* cartes motion */
      #mo {{ position: absolute; inset: 0; background: {INK}; clip-path: inset(100% 0% 0% 0%); }}
      .card {{ position: absolute; left: 90px; right: 90px; border-radius: 44px; background: {CREAM}; color: {INK}; padding: 46px 52px; box-shadow: 0 30px 70px rgba(0,0,0,0.4); }}
      .lab {{ font-weight: 800; font-size: 30px; letter-spacing: 0.14em; text-transform: uppercase; color: {SLATE}; }}
      .big {{ font-weight: 900; font-size: 88px; letter-spacing: -0.035em; line-height: 1; margin-top: 18px; display: flex; align-items: center; gap: 22px; }}
      .big em, .title em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }}
      .ico {{ width: 74px; height: 74px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; flex: none; }}
      #c1 {{ top: 640px; }}
      #c1a, #c1b {{ position: relative; }}
      #c1b {{ position: absolute; left: 52px; top: 46px; right: 52px; opacity: 0; }}
      #pill {{ position: absolute; left: 90px; top: 1010px; padding: 24px 36px; border-radius: 999px; background: {RED}; color: #fff; font-weight: 800; font-size: 44px;
               display: flex; align-items: center; gap: 16px; opacity: 0; box-shadow: 0 16px 36px rgba(230,51,18,0.35); }}
      #att {{ top: 690px; background: {INK}; color: {CREAM}; border: 3px solid {RED}; opacity: 0; }}
      #att .lab {{ color: {RED}; font-size: 34px; }}
      #att p {{ font-weight: 800; font-size: 60px; line-height: 1.12; letter-spacing: -0.025em; margin-top: 22px; }}
      #att p em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; color: {CREAM}; }}
      #cta {{ position: absolute; left: 90px; right: 90px; top: 640px; opacity: 0; }}
      .title {{ white-space: nowrap; font-weight: 900; font-size: 92px; line-height: 0.98; letter-spacing: -0.04em; color: {CREAM}; }}
      .title .red {{ color: {RED}; }}
      #btn {{ display: inline-flex; align-items: center; gap: 20px; margin-top: 56px; background: {RED}; color: #fff; font-weight: 900; font-size: 54px;
              padding: 34px 56px; border-radius: 30px; box-shadow: 0 18px 44px rgba(230,51,18,0.4); }}
      #sub {{ margin-top: 34px; font-weight: 600; font-size: 42px; color: {CREAM}; opacity: 0.85; }}
      #finger {{ position: absolute; left: 0; top: 0; width: 90px; height: 90px; border-radius: 50%; background: rgba(244,241,234,0.85); border: 4px solid #fff; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      <div id="base"></div>
      <div id="chat">
        <div id="head"><div id="ava">P</div><div id="name">Papa</div></div>
        <div id="list">{"".join(slots)}
        </div>
      </div>
      <div id="mo">
        <div class="card" id="c1">
          <div id="c1a"><div class="lab">En assurance</div><div class="big"><span class="ico" style="background:{INK}; color:{CREAM}">{LOCK}</span>Prime <em>fixe</em></div></div>
          <div id="c1b"><div class="lab" style="color:{RED}">En banque</div><div class="big"><span class="ico" style="background:{RED}; color:#fff">{CHECK}</span>Versements <em>libres</em></div></div>
        </div>
        <div id="pill"><span class="ico" style="width:52px; height:52px; background:#fff; color:{RED}">{CHECK}</span>Frais souvent plus bas en banque</div>
        <div class="card" id="att"><div class="lab">Mais attention</div><p>Selon l'ancienneté et la <em>valeur de rachat</em>, changer n'est pas toujours intéressant.</p></div>
        <div id="cta">
          <div class="title">Votre 3ème pilier A,<br><span class="red">faites-le <em>vérifier.</em></span></div>
          <div id="btn">Analyse gratuite <span>→</span></div>
          <div id="sub">Un expert vous rappelle.</div>
          <div id="finger" data-layout-allow-overflow></div>
        </div>
      </div>
      <div id="grain" class="clip" data-start="0" data-duration="{r(DUR)}" data-track-index="21" data-layout-ignore></div>
      <audio id="mix" class="clip" src="assets/mix_V3.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="22" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#chat", {{ scale: 0.985 }}, {{ scale: 1, duration: 0.6, ease: "expo.out" }}, 0);   // visible dès l'image 0 (vignette)
      {chr(10).join("      " + j for j in js)}
      // passage aux cartes
      tl.to("#chat", {{ scale: 0.94, opacity: 0.4, duration: 0.4, ease: "power2.in" }}, {r(T_MOTION - 0.1)});
      tl.fromTo("#mo", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }}, {r(T_MOTION)});
      tl.set("#chat", {{ visibility: "hidden" }}, {r(T_MOTION + 0.45)});
      tl.fromTo("#c1", {{ y: 90, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.55, ease: "expo.out" }}, {r(T_MOTION + 0.2)});
      tl.to("#c1a", {{ opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }}, {r(T_SWITCH)});
      tl.fromTo("#c1b", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, {r(T_SWITCH + 0.18)});
      tl.fromTo("#pill", {{ opacity: 0, scale: 0.7, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2.2)" }}, {r(T_FRAIS)});
      tl.to(["#c1", "#pill"], {{ opacity: 0, y: -60, duration: 0.3, ease: "power2.in" }}, {r(T_ATT - 0.3)});
      tl.fromTo("#att", {{ opacity: 0, x: 120 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }}, {r(T_ATT)});
      tl.to("#att", {{ opacity: 0, y: -60, duration: 0.3, ease: "power2.in" }}, {r(T_CTA - 0.3)});
      tl.fromTo("#cta", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {r(T_CTA)});
      tl.fromTo("#btn", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2.4)" }}, {r(T_CTA + 0.25)});
      tl.fromTo("#finger", {{ opacity: 0, x: 640, y: 560 }}, {{ opacity: 1, x: 330, y: 255, duration: 0.5, ease: "power2.out" }}, {r(T_TAP - 0.55)});
      tl.to("#finger", {{ scale: 0.8, duration: 0.1, yoyo: true, repeat: 1 }}, {r(T_TAP)});
      tl.to("#btn", {{ scale: 0.95, duration: 0.1, yoyo: true, repeat: 1 }}, {r(T_TAP)});
      tl.to("#finger", {{ opacity: 0, duration: 0.3 }}, {r(T_TAP + 0.5)});
      for (let k = 0; k < {int(DUR * 12)}; k++) {{
        tl.set("#grain", {{ backgroundPosition: `${{(k * 173) % 512}}px ${{(k * 311) % 512}}px` }}, k / 12);
      }}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
shutil.copytree(os.path.join(ROOT, "src", "assets", "fonts"), os.path.join(OUT, "assets", "fonts"), dirs_exist_ok=True)
shutil.copy(os.path.join(ROOT, "src", "assets", "grain.png"), os.path.join(OUT, "assets"))
for f in ["hyperframes.json", "package.json"]:
    shutil.copy(os.path.join(ROOT, "src", f), OUT)
open(os.path.join(OUT, "index.html"), "w").write(index)

# ---------------------------------------------------------------- audio : musique + bruitages
CLICK, WHOOSH, POP = "sfx_001.mp3", "sfx_002.mp3", "sfx_003.mp3"
events = [(POP, t, 0.55) for _, _, _, t in MSGS]
events += [(WHOOSH, T_MOTION - 0.05, 0.35), (CLICK, T_SWITCH + 0.15, 0.6), (POP, T_FRAIS, 0.5),
           (WHOOSH, T_ATT - 0.05, 0.25), (WHOOSH, T_CTA - 0.05, 0.25), (CLICK, T_TAP, 0.85)]
inputs, chains = ["-i", MUSIC], []
for k, (f, t, vol) in enumerate(events):
    inputs += ["-i", os.path.join(SFX, f)]
    ms = int(t * 1000)
    chains.append(f"[{k + 1}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
filt = (f"[0]atrim=0:{DUR},asetpts=N/SR/TB,aresample=48000,loudnorm=I=-19:TP=-3:LRA=11,afade=t=in:d=0.3,afade=t=out:st={DUR - 1.6}:d=1.6,apad=whole_dur={DUR}[m];"
        + ";".join(chains) + ";[m]" + "".join(f"[e{k}]" for k in range(len(events)))
        + f"amix=inputs={len(events) + 1}:normalize=0:duration=first,alimiter=limit=0.89")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-ar", "48000", "-ac", "2", "-t", str(DUR), os.path.join(OUT, "assets", "mix_V3.wav")], check=True)
print("ok", OUT)
