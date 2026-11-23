// Deelafbeeldingen (1200x630) per pagina, voor het voorbeeld op LinkedIn en in berichten-apps.
// Elke afbeelding toont het logo, het onderwerp en de kop (h1) van de pagina, in beide talen.
//
//   node tools/deelafbeeldingen.mjs
//
// Draai dit na tools/bouw.mjs als de kop van een pagina is gewijzigd of er een pagina bij is gekomen.
// Vereist Playwright met Chrome (npm i playwright). De afbeeldingen komen in assets/deel/<taal>/.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let chromium;
try { ({ chromium } = await import('playwright')); }
catch { ({ chromium } = createRequire('/opt/npm-tools/node_modules/')('playwright')); }

const DIENSTEN = ['avg-compliance', 'ai-act-compliance', 'nis2', 'information-security', 'quantum-readiness', 'dpo-as-a-service', 'privacy-officer-as-a-service', 'security-officer-as-a-service', 'tprm-contractmanagement'];
const PAGINAS = ['', 'diensten/', ...DIENSTEN.map(s => `diensten/${s}/`), 'over-ons/', 'cases/', 'contact/', 'nieuws/'];
const naam = p => p === '' ? 'home' : p.replace(/\/$/, '').replace(/\//g, '-');
const b64 = f => fs.readFileSync(path.join(REPO, f)).toString('base64');
const kaal = s => s.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const kaart = (kick, kop) => `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Inter';font-weight:100 900;src:url(data:font/woff2;base64,${b64('assets/fonts/inter-latin-wght-normal.woff2')}) format('woff2')}
*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#fff;font-family:'Inter',sans-serif;color:#0B1F3A;position:relative;overflow:hidden}
.in{position:absolute;left:80px;right:80px;top:64px}
.logo{height:76px;display:block}
.kick{display:flex;align-items:center;gap:16px;margin-top:56px;font-size:22px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#1F4FD1}
.kick:before{content:"";flex:0 0 48px;height:6px;border-radius:3px;background:linear-gradient(90deg,#1F4FD1,#0FA88E)}
h1{margin:22px 0 0;font-weight:800;letter-spacing:-.025em;line-height:1.08;max-width:1000px}
svg{position:absolute;left:0;right:0;bottom:0;width:1200px;height:150px}
.voet{position:absolute;left:80px;bottom:26px;color:#fff;font-size:22px;font-weight:600}
</style></head><body><div class="in"><img class="logo" src="data:image/png;base64,${b64('assets/dcbs-logo-full.png')}" alt="">
<div class="kick">${esc(kick)}</div><h1 id="kop">${esc(kop)}</h1></div>
<svg viewBox="0 0 1440 200" preserveAspectRatio="none"><defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1F4FD1"/><stop offset="1" stop-color="#0FA88E"/></linearGradient><linearGradient id="b" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0FA88E" stop-opacity=".35"/><stop offset="1" stop-color="#1F4FD1" stop-opacity=".35"/></linearGradient></defs><path d="M0 80 C 300 0, 540 160, 840 90 S 1260 20, 1440 70 L 1440 200 L 0 200 Z" fill="url(#b)"/><path d="M0 120 C 360 50, 600 190, 910 120 S 1300 70, 1440 110 L 1440 200 L 0 200 Z" fill="url(#a)"/></svg>
<div class="voet">The Data Compliance Builders · dcbs.nl</div>
<script>var k=document.getElementById('kop'),s=76;do{k.style.fontSize=s+'px';s-=2}while(k.offsetHeight>232&&s>38);</script></body></html>`;

const browser = await chromium.launch({ executablePath: fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
let n = 0;
for (const lang of ['nl', 'en']) {
  fs.mkdirSync(path.join(REPO, 'assets/deel', lang), { recursive: true });
  for (const p of PAGINAS) {
    const html = fs.readFileSync(path.join(REPO, lang === 'en' ? 'en' : '', p, 'index.html'), 'utf8');
    const kop = kaal((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1] || '');
    const kick = kaal((html.match(/<div class="kick">([\s\S]*?)<\/div>/) || [])[1] || 'DCBS');
    if (!kop) throw new Error('geen h1 op ' + lang + '/' + p);
    await page.setContent(kaart(kick, kop)); await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(REPO, 'assets/deel', lang, naam(p) + '.jpg'), type: 'jpeg', quality: 90 });
    n++;
  }
}
await browser.close();
console.log(n + ' deelafbeeldingen gemaakt in assets/deel/');
