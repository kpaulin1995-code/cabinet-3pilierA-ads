#!/usr/bin/env python3
"""Vidéo 3 v2 : conversation de messagerie plein écran, look natif (2 variantes : « imessage » / « whatsapp »).
Aucun logo, nom d'appli, barre système (heure, batterie), notification ni appel entrant.

Usage : python3 build_chat.py imessage|whatsapp   → out/CHAT_<style>
"""
import html, math, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(ROOT, "sfx_lib") if os.path.isdir(os.path.join(ROOT, "sfx_lib")) else os.path.join(ROOT, "out", "L_916", ".media", "audio", "sfx")
STYLE = sys.argv[1] if len(sys.argv) > 1 else "imessage"
OUT = os.path.join(ROOT, "out", f"CHAT_{STYLE}")
A = os.path.join(OUT, "assets")
W, H = 1080, 1920

MSGS = [
    ("papa", "Ton 3ème pilier A, il est où ?"),
    ("moi", "À la banque, je crois ?"),
    ("papa", "Non. En assurance. Depuis 2014 😬"),
    ("moi", "…et c'est grave ?"),
    ("papa", "Pas forcément. Mais en assurance, tu paies une prime fixe chaque année."),
    ("papa", "Et une partie sert à payer la couverture et les frais."),
    ("moi", "Et en banque ?"),
    ("papa", "Tu verses ce que tu veux, quand tu veux. Et les frais sont souvent plus bas."),
    ("moi", "Ok, je résilie demain alors !"),
    ("papa", "Non ! Ne fais rien tout seul. Selon l'ancienneté et la valeur de rachat, changer n'est pas toujours intéressant."),
    ("moi", "Je fais comment alors ?"),
    ("papa", "Fais-le analyser gratuitement par un expert. Il te rappelle."),
    ("card", ""),
    ("moi", "👍"),
]

S = {
    "imessage": dict(bg="#FFFFFF", head_bg="rgba(249,249,249,0.96)", head_line="#D8D8DC", name="#000000", sub="#8E8E93",
                     in_bg="#E9E9EB", in_fg="#000000", out_bg="#0A84FF", out_fg="#FFFFFF", radius=46, tail=True,
                     font="'Inter Tight', 'Emoji', sans-serif", weight=500, ticks=False, wall=None, input_bg="#FFFFFF",
                     input_border="#D1D1D6", card_bg="#E9E9EB", btn="#0A84FF", avatar_bg="linear-gradient(#8A909C, #5F6570)"),
    "whatsapp": dict(bg="#EFE7DE", head_bg="#F0F2F5", head_line="#D1D7DB", name="#111B21", sub="#667781",
                     in_bg="#FFFFFF", in_fg="#111B21", out_bg="#D9FDD3", out_fg="#111B21", radius=22, tail=True,
                     font="'Inter Tight', 'Emoji', sans-serif", weight=500, ticks=True, wall=True, input_bg="#FFFFFF",
                     input_border="#FFFFFF", card_bg="#FFFFFF", btn="#00A884", avatar_bg="linear-gradient(#7F8F9A, #5E6C76)"),
}[STYLE]

FS, LH, PADX, PADY, MAXC = 50, 64, 38, 24, 28      # police, interligne, marges, caractères max par ligne
TOP, BOTTOM = 420, 1500                           # zone des messages (sous l'en-tête, au-dessus des 400 px du bas)
GAP_SAME, GAP_SWITCH = 10, 26

def r(x):
    return f"{x:.3f}"

def wrap(t):
    t = t.replace(" ?", "\u00a0?").replace(" !", "\u00a0!")   # pas de « ? » seul en début de ligne
    words, lines, cur = t.split(" "), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > MAXC:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines

# ---------------------------------------------------------------- mise en page déterministe (hauteurs calculées ici)
items, y, t, prev = [], 0, 0.0, None
for k, (who, txt) in enumerate(MSGS):
    gap = 0 if prev is None else (GAP_SAME if who == prev else GAP_SWITCH)
    y += gap
    if who == "card":
        h = 560
        read = 2.8
    elif txt == "👍":
        h = 150
        read = 1.4
    else:
        lines = wrap(txt)
        h = len(lines) * LH + 2 * PADY + (26 if S["ticks"] else 0)
        read = min(2.8, max(1.3, 0.9 + 0.025 * len(txt)))
    typing = 0.0 if k == 0 else (0.5 if who in ("papa", "card") else 0.0)   # 1re bulle visible dès l'image 0 (vignette)
    items.append(dict(k=k, who=who, txt=txt, y=y, h=h, t_type=t, t_show=t + typing))
    t = t + typing + read
    y += h
    prev = "papa" if who == "card" else who
DUR = t + 0.6
VIEW = BOTTOM - TOP

bubbles, js = [], []
TYPE_W, TYPE_H = 190, 2 * PADY + LH
for it in items:
    k, who = it["k"], it["who"]
    side = "l" if who in ("papa", "card") else "r"
    if who == "card":
        body = (f'<div class="card" id="m{k}"><div class="cimg"><div class="cimg-t">3ème pilier A</div><div class="cimg-s">Assurance ou banque ?</div></div>'
                f'<div class="ctxt"><div class="ctit">Analyse gratuite de votre 3ème pilier&nbsp;A</div><div class="cdesc">Un expert vérifie votre contrat et vous rappelle.</div></div>'
                f'<div class="cbtn" id="btn{k}">Demander mon analyse</div></div>')
    elif it["txt"] == "👍":
        body = f'<div class="emo" id="m{k}">👍</div>'
    else:
        lines = "<br>".join(html.escape(l) for l in wrap(it["txt"]))
        meta = '<span class="meta">14:0{}{}</span>'.format(min(9, k // 2), ' <span class="tick">✓✓</span>' if side == "r" else "") if S["ticks"] else ""
        body = f'<div class="bub {side}" id="m{k}"><span class="tx">{lines}</span>{meta}</div>'
    bubbles.append(f'<div class="row {side}" style="top:{it["y"]}px; height:{it["h"]}px">{body}</div>')
    # indicateur de saisie (seulement côté Papa : c'est lui qui « écrit » ; côté Moi, la bulle part directement)
    if side == "l" and k > 0:
        bubbles.append(f'<div class="row l" style="top:{it["y"]}px; height:{TYPE_H}px"><div class="typing" id="t{k}"><i></i><i></i><i></i></div></div>')
        js.append(f'tl.fromTo("#t{k}", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(2)" }}, {r(it["t_type"])});')
        for d in range(3):
            js.append(f'tl.fromTo("#t{k} i:nth-child({d + 1})", {{ opacity: 0.35 }}, {{ opacity: 1, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {r(it["t_type"] + 0.05 + d * 0.13)});')
        js.append(f'tl.to("#t{k}", {{ opacity: 0, duration: 0.06 }}, {r(it["t_show"] - 0.05)});')
    origin = "0% 100%" if side == "l" else "100% 100%"
    if k == 0:
        js.append(f'tl.set("#m{k}", {{ opacity: 1 }}, 0);')
        continue
    js.append(f'tl.fromTo("#m{k}", {{ opacity: 0, scale: 0.6, y: 24, transformOrigin: "{origin}" }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.8)" }}, {r(it["t_show"])});')
    # défilement : le bas du dernier message reste en bas de la zone
    bottom = it["y"] + max(it["h"], TYPE_H if side == "l" else 0)
    if bottom > VIEW:
        js.append(f'tl.to("#list", {{ y: {-(bottom - VIEW)}, duration: 0.32, ease: "power2.out" }}, {r(it["t_type"] if side == "l" else it["t_show"] - 0.05)});')
card = [it for it in items if it["who"] == "card"][0]
js.append(f'tl.to("#btn{card["k"]}", {{ scale: 0.94, duration: 0.1, yoyo: true, repeat: 1 }}, {r(card["t_show"] + 1.6)});')

wall = ""
if S["wall"]:
    # papier peint discret générique (motifs ronds), pas celui d'une appli
    wall = ("background-image: radial-gradient(rgba(0,0,0,0.035) 2px, transparent 2.5px), radial-gradient(rgba(0,0,0,0.03) 1.5px, transparent 2px);"
            "background-size: 46px 46px, 31px 31px; background-position: 0 0, 15px 20px;")

FONTS = """
@font-face { font-family: 'Inter Tight'; font-weight: 500; src: url('assets/fonts/inter-tight-latin-600-normal.woff2') format('woff2'); }
@font-face { font-family: 'Inter Tight'; font-weight: 800; src: url('assets/fonts/inter-tight-latin-800-normal.woff2') format('woff2'); }
@font-face { font-family: 'Emoji'; src: url('assets/fonts/NotoColorEmoji.ttf') format('truetype'); }
"""
tail_l = tail_r = ""
if S["tail"]:
    if STYLE == "imessage":
        tail_l = f'.bub.l::before {{ content: ""; position: absolute; left: -9px; bottom: 0; width: 30px; height: 30px; background: {S["in_bg"]}; border-bottom-right-radius: 18px; }}' \
                 f'.bub.l::after {{ content: ""; position: absolute; left: -22px; bottom: 0; width: 22px; height: 30px; background: {S["bg"]}; border-bottom-right-radius: 14px; }}'
        tail_r = f'.bub.r::before {{ content: ""; position: absolute; right: -9px; bottom: 0; width: 30px; height: 30px; background: {S["out_bg"]}; border-bottom-left-radius: 18px; }}' \
                 f'.bub.r::after {{ content: ""; position: absolute; right: -22px; bottom: 0; width: 22px; height: 30px; background: {S["bg"]}; border-bottom-left-radius: 14px; }}'
    else:
        tail_l = f'.bub.l {{ border-top-left-radius: 0; }} .bub.l::before {{ content: ""; position: absolute; left: -16px; top: 0; border-top: 18px solid {S["in_bg"]}; border-left: 18px solid transparent; }}'
        tail_r = f'.bub.r {{ border-top-right-radius: 0; }} .bub.r::before {{ content: ""; position: absolute; right: -16px; top: 0; border-top: 18px solid {S["out_bg"]}; border-right: 18px solid transparent; }}'

index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      {FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {S["bg"]}; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: {S["font"]}; background: {S["bg"]}; {wall} }}
      #head {{ position: absolute; left: 0; right: 0; top: 0; height: 400px; background: {S["head_bg"]}; border-bottom: 2px solid {S["head_line"]}; z-index: 5; }}
      #who {{ position: absolute; left: 0; right: 0; top: 262px; display: flex; flex-direction: column; align-items: center; gap: 10px; }}
      #ava {{ width: 92px; height: 92px; border-radius: 50%; background: {S["avatar_bg"]}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 42px; }}
      #name {{ font-weight: 800; font-size: 34px; color: {S["name"]}; }}
      #view {{ position: absolute; left: 0; right: 0; top: {TOP}px; height: {VIEW}px; overflow: hidden; }}
      #list {{ position: absolute; left: 0; right: 0; top: 0; }}
      .row {{ position: absolute; left: 44px; right: 44px; display: flex; align-items: flex-start; }}
      .row.r {{ justify-content: flex-end; }}
      .bub {{ position: relative; padding: {PADY}px {PADX}px; border-radius: {S["radius"]}px; font-size: {FS}px; line-height: {LH}px; font-weight: {S["weight"]}; white-space: nowrap; opacity: 0;
              letter-spacing: -0.01em; box-shadow: {"0 2px 2px rgba(11,20,38,0.08)" if STYLE == "whatsapp" else "none"}; }}
      .bub.l {{ background: {S["in_bg"]}; color: {S["in_fg"]}; }}
      .bub.r {{ background: {S["out_bg"]}; color: {S["out_fg"]}; }}
      {tail_l} {tail_r}
      .tx {{ display: block; }}
      .meta {{ display: block; text-align: right; font-size: 24px; line-height: 26px; color: {S["sub"]}; margin-top: 2px; }}
      .tick {{ color: #53BDEB; }}
      .typing {{ display: flex; gap: 14px; padding: {PADY + 14}px {PADX}px; border-radius: {S["radius"]}px; background: {S["in_bg"]}; opacity: 0; }}
      .typing i {{ width: 20px; height: 20px; border-radius: 50%; background: {S["sub"]}; display: block; }}
      .emo {{ font-size: 120px; line-height: 150px; opacity: 0; }}
      .card {{ width: 760px; border-radius: {S["radius"]}px; overflow: hidden; background: {S["card_bg"]}; opacity: 0; box-shadow: 0 2px 4px rgba(11,20,38,0.1); }}
      .cimg {{ height: 250px; background: linear-gradient(135deg, #0B1426, #24375E); color: #F4F1EA; display: flex; flex-direction: column; justify-content: center; padding: 0 44px; }}
      .cimg-t {{ font-weight: 800; font-size: 60px; letter-spacing: -0.03em; }}
      .cimg-s {{ font-weight: 500; font-size: 34px; opacity: 0.8; margin-top: 6px; }}
      .ctxt {{ padding: 26px 34px 10px; color: {S["in_fg"]}; }}
      .ctit {{ font-weight: 800; font-size: 40px; line-height: 1.15; letter-spacing: -0.02em; }}
      .cdesc {{ font-weight: 500; font-size: 30px; color: {S["sub"]}; margin-top: 8px; }}
      .cbtn {{ margin: 18px 34px 30px; padding: 22px 0; border-radius: 18px; background: {S["btn"]}; color: #fff; text-align: center; font-weight: 800; font-size: 38px; }}
      #input {{ position: absolute; left: 0; right: 0; top: 1540px; bottom: 0; background: {S["head_bg"]}; border-top: 2px solid {S["head_line"]}; }}
      #field {{ position: absolute; left: 44px; right: 44px; top: 40px; height: 92px; border-radius: 46px; background: {S["input_bg"]}; border: 2px solid {S["input_border"]}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUR)}" data-width="{W}" data-height="{H}">
      <div id="head" data-layout-allow-occlusion><div id="who"><div id="ava">P</div><div id="name">Papa</div></div></div>
      <div id="view" data-layout-allow-occlusion><div id="list">
        {chr(10).join("        " + b for b in bubbles)}
      </div></div>
      <div id="input"><div id="field"></div></div>
      <audio id="mix" class="clip" src="assets/mix_chat.wav" data-start="0" data-duration="{r(DUR)}" data-track-index="22" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + j for j in js)}
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

# ---------------------------------------------------------------- sons de message génériques (pas ceux d'une appli)
recv = os.path.join(A, "recv.wav"); sent = os.path.join(A, "sent.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                "aevalsrc='0.5*(sin(2*PI*880*t)+0.6*sin(2*PI*1320*t))*exp(-18*t)+0.4*sin(2*PI*1175*(t-0.07))*exp(-20*(t-0.07))*gte(t,0.07)':s=48000:d=0.35", recv], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                "aevalsrc='0.45*sin(2*PI*(500+900*t)*t)*exp(-22*t)':s=48000:d=0.25", sent], check=True)
events = []
for it in items:
    if it["who"] == "moi":
        events.append((sent, it["t_show"], 0.6))
    else:
        events.append((recv, it["t_show"], 0.55))
events.append((os.path.join(SFX, "sfx_001.mp3"), card["t_show"] + 1.6, 0.6))
inputs, chains = ["-f", "lavfi", "-t", str(DUR), "-i", "anullsrc=r=48000:cl=stereo"], []
for k, (f, tt, vol) in enumerate(events):
    inputs += ["-i", f]
    ms = int(tt * 1000)
    chains.append(f"[{k + 1}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
filt = ";".join(chains) + ";[0]" + "".join(f"[e{k}]" for k in range(len(events))) + f"amix=inputs={len(events) + 1}:normalize=0:duration=first,alimiter=limit=0.89"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt,
                "-ar", "48000", "-ac", "2", "-t", str(DUR), os.path.join(A, "mix_chat.wav")], check=True)
print("ok", OUT, f"{DUR:.1f} s")
