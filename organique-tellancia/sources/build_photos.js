// Habille les photos (FLORA) avec la DA Tellancia : 1080x1350.
// Usage : node sources/build_photos.js   (depuis organique-tellancia/)
// Photos sources : photos/<id>.png ; sortie : visuels/<id>.png
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const F = (n) => 'file://' + path.join(ROOT, 'sources/fonts', n);
const BLASON = 'file://' + path.join(ROOT, 'brand/blason.png');

const visuels = [
  { id: 'P1_cabinet', kicker: 'Cabinet de courtage · Genève', line: 'Le conseil, <em>sur mesure.</em>' },
  { id: 'P3_lamal', kicker: 'Assurance maladie · LAMal', line: 'Faire le point <em>avant le 30 novembre.</em>' },
  { id: 'P5_libre_passage', kicker: 'Libre passage', line: 'Entre deux emplois, <em>votre 2ème pilier vous attend.</em>' },
  { id: 'P1_cabinet_alt', kicker: 'Cabinet de courtage · Genève', line: 'Le conseil, <em>sur mesure.</em>' },
  { id: 'P5_libre_passage_alt', kicker: 'Libre passage', line: 'Entre deux emplois, <em>votre 2ème pilier vous attend.</em>' },
  { id: 'P7_3pilier_A_ou_B', kicker: 'Prévoyance privée', line: '3ème pilier A ou B : <em>deux chemins.</em>' },
];

const html = (v, src) => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F('cormorant-garamond-latin-300-normal.woff2')})}
@font-face{font-family:Corm;font-weight:300;font-style:italic;src:url(${F('cormorant-garamond-latin-300-italic.woff2')})}
@font-face{font-family:Mont;font-weight:500;src:url(${F('montserrat-latin-500-normal.woff2')})}
@font-face{font-family:Mont;font-weight:400;src:url(${F('montserrat-latin-400-normal.woff2')})}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;background:#1A2126}
.ph{position:absolute;inset:0;background:url(${src}) center/cover no-repeat}
.grad{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,33,38,.62) 0%,rgba(26,33,38,.08) 28%,rgba(26,33,38,0) 50%,rgba(26,33,38,.25) 66%,rgba(26,33,38,.85) 100%)}
.frame{position:absolute;inset:44px;border:1px solid rgba(243,245,246,.38)}
.frame2{position:absolute;inset:52px;border:1px solid rgba(243,245,246,.2)}
.top{position:absolute;top:110px;left:0;right:0;text-align:center;color:#F3F5F6}
.top img{height:84px;filter:invert(1) brightness(.97) drop-shadow(0 2px 10px rgba(0,0,0,.3))}
.kicker{margin-top:26px;font-family:Mont;font-weight:500;font-size:19px;letter-spacing:.42em;text-transform:uppercase;color:rgba(243,245,246,.85);text-shadow:0 1px 8px rgba(0,0,0,.35)}
.bot{position:absolute;left:100px;right:100px;bottom:120px;text-align:center;color:#F3F5F6}
.line{font-family:Corm;font-weight:300;font-size:60px;line-height:1.12;font-variant-numeric:lining-nums;text-shadow:0 2px 18px rgba(0,0,0,.35)}
.line em{font-style:italic}
.rule{width:80px;height:1px;background:rgba(243,245,246,.5);margin:36px auto 30px}
.foot{font-family:Mont;font-weight:400;font-size:18px;letter-spacing:.5em;text-transform:uppercase;color:rgba(243,245,246,.8)}
</style></head><body><div class="ph"></div><div class="grad"></div><div class="frame"></div><div class="frame2"></div>
<div class="top"><img src="${BLASON}"><div class="kicker">${v.kicker}</div></div>
<div class="bot"><div class="line">${v.line}</div><div class="rule"></div><div class="foot">Tellancia.ch</div></div>
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const v of visuels) {
    const srcFile = path.join(ROOT, 'photos', v.id + '.png');
    if (!fs.existsSync(srcFile)) { console.log('absent', v.id); continue; }
    const tmp = path.join(ROOT, 'visuels', `.${v.id}.html`);
    fs.writeFileSync(tmp, html(v, 'file://' + srcFile));
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    await page.screenshot({ path: path.join(ROOT, 'visuels', v.id + '.png') });
    fs.unlinkSync(tmp);
    console.log('ok', v.id);
  }
  await browser.close();
})();
