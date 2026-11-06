// Génère les visuels 1080x1350 des posts organiques Tellancia.
// Usage : node sources/build_visuels.js   (depuis organique-tellancia/)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const F = (n) => 'file://' + path.join(ROOT, 'sources/fonts', n);
const BLASON = 'file://' + path.join(ROOT, 'brand/blason.png');

// theme: 'nuit' (anthracite) ou 'ivoire'
const visuels = [
  { id: '01_cabinet', theme: 'nuit', kicker: 'Cabinet de courtage · Genève',
    title: 'Le conseil,<br><em>sur mesure.</em>',
    sub: 'Courtier indépendant en assurance et prévoyance.<br>Une équipe à taille humaine.',
    foot: '5.0 sur Google · 99 avis' },
  { id: '02_3pilierA_3112', theme: 'ivoire', kicker: '3ème pilier A',
    title: '<span class="big">31.12</span>',
    sub: 'Votre versement doit être crédité<br><em>avant la fin de l’année.</em>',
    foot: 'Tellancia.ch' },
  { id: '03_lamal', theme: 'nuit', kicker: 'Assurance maladie · LAMal',
    title: 'Primes 2027 :<br><em>faites le point<br>avant le 30 novembre.</em>',
    sub: 'Assurance de base, complémentaires :<br>chaque situation mérite une analyse.',
    foot: 'Tellancia.ch' },
  { id: '04_certificat_lpp', theme: 'ivoire', kicker: 'Prévoyance professionnelle',
    title: 'Votre certificat LPP,<br><em>ligne par ligne.</em>',
    sub: 'Avoir de vieillesse · rente projetée ·<br>couverture invalidité et décès.',
    foot: 'Tellancia.ch' },
  { id: '05_libre_passage', theme: 'nuit', kicker: 'Libre passage',
    title: 'Entre deux emplois,<br><em>votre 2ème pilier<br>vous attend.</em>',
    sub: 'Encore faut-il savoir où il se trouve<br>et comment le placer.',
    foot: 'Tellancia.ch' },
  { id: '06_methode', theme: 'ivoire', kicker: 'Notre méthode',
    title: 'Écouter.<br>Analyser.<br><em>Recommander.</em>',
    sub: 'Le temps qu’il faut,<br>pour chaque client.',
    foot: 'Tellancia.ch' },
  { id: '07_3pilier_A_ou_B', theme: 'nuit', kicker: 'Prévoyance privée',
    title: '3ème pilier A<br>ou 3ème pilier B ?<br><em>Deux logiques.</em>',
    sub: 'Souplesse, fiscalité, disponibilité :<br>bien les distinguer avant de choisir.',
    foot: 'Tellancia.ch' },
  { id: '08_protection_famille', theme: 'ivoire', kicker: 'Protection de la famille',
    title: 'Et si demain<br>vous ne pouviez plus<br><em>travailler ?</em>',
    sub: 'Invalidité, décès :<br>ce que vos proches recevraient vraiment.',
    foot: 'Tellancia.ch' },
];

function html(v) {
  const dark = v.theme === 'nuit';
  const bg = dark ? '#1A2126' : '#F3F1EC';
  const ink = dark ? '#F3F5F6' : '#1A2126';
  const muted = dark ? '#8C9AA1' : '#6A7980';
  const line = dark ? 'rgba(243,245,246,.28)' : 'rgba(26,33,38,.28)';
  const guil = dark ? 'rgba(255,255,255,.025)' : 'rgba(26,33,38,.03)';
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Corm;font-weight:300;src:url(${F('cormorant-garamond-latin-300-normal.woff2')})}
@font-face{font-family:Corm;font-weight:300;font-style:italic;src:url(${F('cormorant-garamond-latin-300-italic.woff2')})}
@font-face{font-family:Corm;font-weight:500;src:url(${F('cormorant-garamond-latin-500-normal.woff2')})}
@font-face{font-family:Mont;font-weight:400;src:url(${F('montserrat-latin-400-normal.woff2')})}
@font-face{font-family:Mont;font-weight:500;src:url(${F('montserrat-latin-500-normal.woff2')})}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{background:${bg};color:${ink};position:relative;overflow:hidden;font-family:Corm}
.guil{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% 46%, ${guil} 0deg .6deg, transparent .6deg 1.8deg);}
.vign{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, transparent 35%, ${dark ? 'rgba(0,0,0,.35)' : 'rgba(26,33,38,.06)'} 100%)}
.frame{position:absolute;inset:44px;border:1px solid ${line}}
.frame2{position:absolute;inset:52px;border:1px solid ${line};opacity:.5}
.top{position:absolute;top:118px;left:0;right:0;text-align:center}
.top img{height:92px;${dark ? 'filter:invert(1) brightness(.96);' : 'opacity:.9;'}}
.kicker{margin-top:30px;font-family:Mont;font-weight:500;font-size:20px;letter-spacing:.42em;text-transform:uppercase;color:${muted}}
.mid{position:absolute;top:400px;left:110px;right:110px;bottom:300px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
h1{font-variant-numeric:lining-nums;font-weight:300;font-size:84px;line-height:1.06;letter-spacing:-.005em}
h1 em{font-style:italic}
h1 .big{font-size:250px;font-weight:300;letter-spacing:.02em;line-height:1}
.rule{width:90px;height:1px;background:${line};margin:52px auto 44px}
.sub{font-family:Corm;font-weight:500;font-size:34px;line-height:1.38;color:${dark ? '#C9D1D5' : '#3A464D'}}
.sub em{font-style:italic;font-weight:300}
.foot{position:absolute;bottom:118px;left:0;right:0;text-align:center;font-family:Mont;font-weight:400;font-size:19px;letter-spacing:.5em;text-transform:uppercase;color:${muted}}
</style></head><body>
<div class="guil"></div><div class="vign"></div><div class="frame"></div><div class="frame2"></div>
<div class="top"><img src="${BLASON}"><div class="kicker">${v.kicker}</div></div>
<div class="mid"><h1>${v.title}</h1><div class="rule"></div><div class="sub">${v.sub}</div></div>
<div class="foot">${v.foot}</div>
</body></html>`;
}

(async () => {
  const only = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  fs.mkdirSync(path.join(ROOT, 'visuels'), { recursive: true });
  for (const v of visuels) {
    if (only && v.id !== only) continue;
    const tmp = path.join(ROOT, 'visuels', `.${v.id}.html`);
    fs.writeFileSync(tmp, html(v));
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(ROOT, 'visuels', `${v.id}.png`) });
    fs.unlinkSync(tmp);
    console.log('ok', v.id);
  }
  await browser.close();
})();
