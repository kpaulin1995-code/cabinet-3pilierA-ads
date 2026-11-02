#!/usr/bin/env python3
"""Visuels fixes Meta (4:5 et 9:16) : image clé de la femme + hook + 3 puces + bouton.

Usage : python3 build_visuels.py  → PNG dans ../../creas/exports/visuels/
"""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "creas", "exports", "visuels")
INK, CREAM, RED = "#0B1426", "#F4F1EA", "#E63312"

VISUELS = {
    "V1-banque": dict(bg="v1_bg.png", pos="50% 0%",
                      hook=['Votre 3ème pilier A', 'est en <em>assurance</em>&nbsp;?', '<span class="red">Et la <em>banque</em>&nbsp;?</span>']),
    "V2-vendu": dict(bg="v2_bg.png", pos="50% 0%",
                     hook=['Votre 3ème pilier A,', 'vous l\'avez <em>choisi</em>…', '<span class="red">ou on vous l\'a <em>vendu</em>&nbsp;?</span>']),
}
PUCES = ["Moins de frais", "Versements libres", "Analyse par un expert"]
# bande utile : 9:16 → texte au-dessus des 400 px du bas ; 4:5 → marge de 64 px
FORMATS = {"9x16": dict(h=1920, bottom=420, size=96, grad=980), "4x5": dict(h=1350, bottom=60, size=78, grad=780)}


def page(v, f):
    hook = "".join(f'<div class="l">{l}</div>' for l in v["hook"])
    puces = "".join(f'<div class="p"><span class="ck">✓</span>{p}</div>' for p in PUCES)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: 'Inter Tight'; font-weight: 900; src: url('fonts/inter-tight-latin-900-normal.woff2'); }}
@font-face {{ font-family: 'Inter Tight'; font-weight: 700; src: url('fonts/inter-tight-latin-800-normal.woff2'); }}
@font-face {{ font-family: 'Inter Tight'; font-weight: 600; src: url('fonts/inter-tight-latin-600-normal.woff2'); }}
@font-face {{ font-family: 'Instrument Serif'; font-style: italic; src: url('fonts/instrument-serif-latin-400-italic.woff2'); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: {f['h']}px; overflow: hidden; background: {INK}; }}
.bg {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: {v['pos']}; }}
.shade {{ position: absolute; left: 0; right: 0; bottom: 0; height: {f['grad'] + f['bottom']}px;
  background: linear-gradient(to bottom, rgba(11,20,38,0) 0%, rgba(11,20,38,.82) 30%, rgba(11,20,38,.95) 58%, {INK} 100%); }}
.txt {{ position: absolute; left: 64px; right: 64px; bottom: {f['bottom']}px; color: {CREAM}; }}
.hook {{ font-family: 'Inter Tight'; font-weight: 900; font-size: {f['size']}px; line-height: .98; letter-spacing: -.035em; text-shadow: 0 2px 24px rgba(11,20,38,.55); }}
.hook em {{ font-family: 'Instrument Serif'; font-style: italic; font-weight: 400; letter-spacing: -.01em; font-size: 1.1em; }}
.red {{ color: {RED}; }}
.puces {{ display: flex; flex-wrap: wrap; gap: 14px; margin-top: 38px; }}
.p {{ font-family: 'Inter Tight'; font-weight: 600; font-size: 31px; padding: 12px 22px 12px 14px; border-radius: 999px;
  background: rgba(244,241,234,.12); border: 1.5px solid rgba(244,241,234,.28); display: flex; align-items: center; gap: 12px; }}
.ck {{ width: 34px; height: 34px; border-radius: 50%; background: {CREAM}; color: {INK}; font-size: 21px; font-weight: 900;
  display: inline-flex; align-items: center; justify-content: center; }}
.cta {{ display: inline-flex; align-items: center; gap: 16px; margin-top: 36px; background: {RED}; color: #fff;
  font-family: 'Inter Tight'; font-weight: 900; font-size: 40px; letter-spacing: -.01em; padding: 24px 40px; border-radius: 22px;
  box-shadow: 0 14px 40px rgba(230,51,18,.35); }}
</style></head><body>
<img class="bg" src="{v['bg']}"><div class="shade"></div>
<div class="txt"><div class="hook">{hook}</div><div class="puces">{puces}</div><div class="cta">Analyse gratuite <span>→</span></div></div>
</body></html>"""


os.makedirs(OUT, exist_ok=True)
# capture via Playwright (Node) : require('playwright') est disponible globalement
jobs = []
for vk, v in VISUELS.items():
    for fk, f in FORMATS.items():
        tmp = os.path.join(HERE, f"_{vk}_{fk}.html")
        open(tmp, "w").write(page(v, f))
        jobs.append(dict(html="file://" + tmp, h=f["h"], out=os.path.abspath(os.path.join(OUT, f"3emePilierA_{vk}_{fk}.png"))))
js = """const {chromium} = require('playwright');
(async () => { const b = await chromium.launch(); const jobs = JSON.parse(process.argv[1]);
  for (const j of jobs) { const p = await b.newPage({viewport: {width: 1080, height: j.h}});
    await p.goto(j.html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({path: j.out}); await p.close(); console.log(j.out); }
  await b.close(); })();"""
subprocess.run(["node", "-e", js, json.dumps(jobs)], check=True)
for j in jobs:
    os.remove(j["html"][7:])
