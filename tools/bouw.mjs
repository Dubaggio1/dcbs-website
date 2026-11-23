// DCBS-site: afgeleide bestanden opnieuw maken. De Nederlandse pagina's zijn de bron.
//
//   node tools/bouw.mjs              alles bijwerken
//   node tools/bouw.mjs --ontbreekt  alleen tonen welke teksten nog geen vertaling hebben
//
// Wat dit script doet:
//   1. Nederlandse pagina's: taalwissel in de kop, hreflang, structured data, statische artikellijsten.
//   2. Engelse pagina's onder /en/: een exacte spiegel van de Nederlandse, vertaald met tools/vertalingen.json.
//      Staat er een Nederlandse tekst op een pagina die niet in dat bestand staat, dan stopt het script.
//   3. Artikelpagina's in beide talen, uit nieuws/<slug>/artikel.md en en/nieuws/<slug>/artikel.md.
//   4. Doorverwijzingen voor vervallen pagina's en de sitemap.
// Het beheer op /nieuws/#beheer doet stap 3 en de lijsten/sitemap zelf bij elke publicatie. Dit script
// is nodig na een wijziging in de tekst of opbouw van een gewone pagina. Het is veilig om vaker te draaien.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ALLEEN_ONTBREEKT = process.argv.includes('--ontbreekt');
const BASIS = 'https://www.dcbs.nl';
const ORG = BASIS + '/#organisatie';
const bestaat = p => fs.existsSync(path.join(REPO, p));
const lees = p => fs.readFileSync(path.join(REPO, p), 'utf8');
const uitvoer = new Map();
const schrijf = (p, t) => uitvoer.set(p, t);

// ---- site.js laden: dezelfde functies die de site en het beheer gebruiken ----
const stubEl = () => ({ style: { setProperty() {} }, setAttribute() {}, appendChild() {}, addEventListener() {}, set textContent(v) {}, children: [] });
const sandbox = { document: { addEventListener() {}, createElement: stubEl, head: { appendChild() {} }, getElementById: () => null } };
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(lees('site.js'), sandbox);
const S = sandbox.DCBS_STATISCH;
const dataCtx = { window: {} };
vm.createContext(dataCtx);
vm.runInContext(lees('nieuws-data.js'), dataCtx);
const ARTIKELEN = dataCtx.window.DCBS_ARTICLES;
const ARTIKELEN_EN = S.lijstEn(ARTIKELEN);
// Versienummer achter site.js en v6.js: verandert alleen als een van die twee bestanden verandert.
const VERSIE = String(parseInt(crypto.createHash('sha1').update(lees('site.js') + lees('assets/js/v6.js')).digest('hex').slice(0, 9), 16));

// ---- pagina's ----
const DIENSTEN = [
  ['avg-compliance', 'Privacy compliance'], ['ai-act-compliance', 'AI compliance'], ['nis2', 'NIS2 / Cyberbeveiligingswet'],
  ['information-security', 'Information security'], ['quantum-readiness', 'Quantum-readiness'], ['dpo-as-a-service', 'DPO-as-a-Service'],
  ['privacy-officer-as-a-service', 'Privacy Officer as a Service'], ['security-officer-as-a-service', 'Security Officer as a Service'],
  ['tprm-contractmanagement', 'TPRM- en contractmanagement'],
];
// pad van de pagina (zonder index.html); '' is de homepage
const PAGINAS = ['', 'diensten/', ...DIENSTEN.map(([s]) => `diensten/${s}/`), 'over-ons/', 'cases/', 'contact/', 'nieuws/', 'bedankt/', 'privacybeleid/'];
const NIET_IN_SITEMAP = new Set(['bedankt/']);
const enPad = p => p.startsWith('privacybeleid/') ? 'en/privacy-statement/' + p.slice(14) : 'en/' + p;
// Vervallen adressen: [oud pad, nieuw pad]. Worden een doorverwijspagina met noindex.
const VERHUISD = [
  ['en/diensten/gdpr-compliance/', 'en/diensten/avg-compliance/'],
  ['en/diensten/data-management/', 'en/diensten/'],
  ...['fria-fundamental-rights-impact-assessment', 'claude-ai-governance-discipline', 'tesla-robotaxi-privacy', 'risicos-generatieve-ai', 'ai-literacy-verplichting', 'bc-5701-privacy-keurmerk']
    .flatMap(s => [[`nieuws/${s}/`, 'nieuws/'], [`en/nieuws/${s}/`, 'en/nieuws/']]),
];

// ---- vertalen ----
const WOORDENBOEK = JSON.parse(lees('tools/vertalingen.json'));
const ontbreekt = new Map();
const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', euro: '€', mdash: '—', ndash: '–', rarr: '→', larr: '←', middot: '·', copy: '©', hellip: '…', eacute: 'é', euml: 'ë', iuml: 'ï', egrave: 'è', ouml: 'ö', lsquo: '‘', rsquo: '’', ldquo: '“', rdquo: '”' };
const decodeer = s => s.replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, (m, c) => c[0] === '#' ? String.fromCodePoint(c[1].toLowerCase() === 'x' ? parseInt(c.slice(2), 16) : parseInt(c.slice(1), 10)) : (ENT[c] ?? m));
const codeer = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const codeerAttr = s => codeer(s).replace(/"/g, '&quot;');
const sleutel = s => decodeer(s).replace(/\s+/g, ' ').trim();
function tr(nl, waar) {
  if (!/[A-Za-zÀ-ÿ]/.test(nl)) return nl;                                  // cijfers en leestekens
  if (/^(?:[^A-Za-zÀ-ÿ{]*\{\{[A-Z]+\}\})+[^A-Za-zÀ-ÿ{]*(?:DCBS)?$/.test(nl)) return nl;   // alleen sjabloonvelden
  if (Object.hasOwn(WOORDENBOEK, nl)) return WOORDENBOEK[nl];
  if (!ontbreekt.has(nl)) ontbreekt.set(nl, waar);
  return nl;
}
const TOKEN = /(<!--[\s\S]*?-->|<script\b[\s\S]*?<\/script>|<style\b[\s\S]*?<\/style>|<svg\b[\s\S]*?<\/svg>|<[^>]+>)/;
const enUrl = u => /^\/(assets\/|site\.js|nieuws-data\.js|en\/)/.test(u) ? u : u.startsWith('/privacybeleid/') ? '/en/privacy-statement/' + u.slice(15) : '/en' + u;
function vertaal(html, waar) {
  const delen = html.split(TOKEN);
  for (let i = 0; i < delen.length; i++) {
    let d = delen[i];
    if (i % 2 === 0) {                                                       // tekst
      const k = sleutel(d);
      if (k) delen[i] = d.match(/^\s*/)[0] + codeer(tr(k, waar)) + d.match(/\s*$/)[0];
      continue;
    }
    if (/^<(!--|script\b[^>]*>[\s\S]|style|svg)/.test(d) && !/^<script\b[^>]*><\/script>$/.test(d)) continue;   // commentaar, inline script, stijl, svg
    if (/\bdata-taal\b/.test(d)) continue;                                  // taalwissel: links staan al goed
    d = d.replace(/\b(alt|aria-label|placeholder)="([^"]*)"/g, (m, a, v) => v.trim() ? `${a}="${codeerAttr(tr(sleutel(v), waar))}"` : m);
    if (/^<meta\b/.test(d) && /\b(name="(description|twitter:title|twitter:description)"|property="og:(title|description)")/.test(d))
      d = d.replace(/\bcontent="([^"]*)"/, (m, v) => `content="${codeerAttr(tr(sleutel(v), waar))}"`);
    if (/^<input\b/.test(d) && /name="_subject"/.test(d)) d = d.replace(/\bvalue="([^"]*)"/, (m, v) => `value="${codeerAttr(tr(sleutel(v), waar))}"`);
    d = d.replace(/\bhref="(\/[^"]*)"/g, (m, u) => `href="${enUrl(u)}"`)
         .replace(/"https:\/\/www\.dcbs\.nl(\/[^"]*)"/g, (m, u) => `"${BASIS}${enUrl(u)}"`);
    if (/^<html\b/.test(d)) d = d.replace(/lang="nl"/, 'lang="en"');
    delen[i] = d;
  }
  return delen.join('');
}

// ---- taalwissel in de kop ----
const WISSEL_D = /<span(?: data-taal="d")? style="font-size:13px;font-weight:600;color:#3A4A63">(?:<span style="color:#0B1F3A">NL<\/span> \/ (?:EN|<a [^>]*>EN<\/a>)|<a [^>]*>NL<\/a> \/ <span style="color:#0B1F3A">EN<\/span>)<\/span>/g;
const WISSEL_M = /<a href="[^"]*"(?: hreflang="(?:en|nl)" data-taal)?>NL \/ EN<\/a>/g;
function taalwissel(html, lang, nlPad, enPadVan) {   // paden zonder voorloop-slash
  const nl = '/' + nlPad, en = '/' + enPadVan;
  const d = lang === 'nl'
    ? `<span data-taal="d" style="font-size:13px;font-weight:600;color:#3A4A63"><span style="color:#0B1F3A">NL</span> / <a href="${en}" hreflang="en" data-taal>EN</a></span>`
    : `<span data-taal="d" style="font-size:13px;font-weight:600;color:#3A4A63"><a href="${nl}" hreflang="nl" data-taal>NL</a> / <span style="color:#0B1F3A">EN</span></span>`;
  const m = lang === 'nl' ? `<a href="${en}" hreflang="en" data-taal>NL / EN</a>` : `<a href="${nl}" hreflang="nl" data-taal>NL / EN</a>`;
  if (!WISSEL_D.test(html) || !WISSEL_M.test(html)) throw new Error('taalwissel niet gevonden in ' + nlPad);
  WISSEL_D.lastIndex = WISSEL_M.lastIndex = 0;
  return html.replace(WISSEL_D, d).replace(WISSEL_M, m);
}

// ---- head: hreflang, structured data, versienummers ----
const ont = s => decodeer(s.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
const description = html => { const m = html.match(/<meta name="description" content="([^"]*)"/); return m ? ont(m[1]) : ''; };
const kaal = html => html.replace(/<script type="application\/ld\+json" id="ld-dcbs">[\s\S]*?<\/script>\n?/g, '').replace(/<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?/g, '');
const ldScript = graph => '<script type="application/ld+json" id="ld-dcbs">' + JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }).replace(/</g, '\\u003c') + '</script>';
function zetHead(html, p, graph) {
  if ((html.match(/<\/head>/g) || []).length !== 1) throw new Error('verwacht precies één </head> in ' + p);
  const hl = `<link rel="alternate" hreflang="nl" href="${BASIS}/${p}">\n<link rel="alternate" hreflang="en" href="${BASIS}/${enPad(p)}">\n<link rel="alternate" hreflang="x-default" href="${BASIS}/${p}">\n`;
  html = html.replace(/(<link rel="canonical" href="[^"]*">\n)/, '$1' + hl);
  if (graph && graph.length) html = html.replace('</head>', ldScript(graph) + '\n</head>');
  return html.replace(/\/site\.js\?v=\d+/g, '/site.js?v=' + VERSIE).replace(/\/assets\/js\/v6\.js\?v=\d+/g, '/assets/js/v6.js?v=' + VERSIE);
}
function structuredData(html, lang, p) {
  const en = lang === 'en', t = s => en ? tr(s, 'structured data') : s;
  const u = pad => BASIS + '/' + (en ? enPad(pad) : pad);
  const kruimels = lijst => ({ '@type': 'BreadcrumbList', itemListElement: lijst.map(([naam, pad], i) => ({ '@type': 'ListItem', position: i + 1, name: t(naam), item: u(pad) })) });
  const land = { '@type': 'Country', name: en ? 'Netherlands' : 'Nederland' }, orgRef = { '@id': ORG }, taal = en ? 'en' : 'nl-NL';
  if (p === '') return [
    { '@type': 'ProfessionalService', '@id': ORG, name: 'The Data Compliance Builders', alternateName: 'DCBS', legalName: 'The Data Compliance Builders B.V.',
      url: BASIS + '/', description: description(html), logo: BASIS + '/assets/dcbs-logo-full.png', image: BASIS + '/assets/dcbs-logo-full.png',
      email: 'contact@dcbs.nl', telephone: '+31615234409',
      address: { '@type': 'PostalAddress', streetAddress: 'Berkenlaan 6', postalCode: '7313 GN', addressLocality: 'Apeldoorn', addressCountry: 'NL' },
      identifier: { '@type': 'PropertyValue', propertyID: 'KVK', value: '66569346' },
      founder: { '@type': 'Person', '@id': BASIS + '/over-ons/#jeroen-dubach', name: 'Jeroen Dubach' }, areaServed: land,
      knowsAbout: en ? ['GDPR', 'Data Protection Officer', 'EU AI Act', 'NIS2', 'Dutch Cybersecurity Act', 'ISO 27001', 'Third Party Risk Management']
                     : ['AVG', 'Functionaris Gegevensbescherming', 'EU AI Act', 'NIS2', 'Cyberbeveiligingswet', 'ISO 27001', 'Third Party Risk Management'],
      sameAs: ['https://www.linkedin.com/company/the-data-compliance-builders/'] },
    { '@type': 'WebSite', '@id': u('') + '#website', url: u(''), name: 'The Data Compliance Builders', alternateName: 'DCBS', inLanguage: taal, publisher: orgRef },
  ];
  if (p === 'diensten/') return [
    { '@type': 'ItemList', name: en ? 'DCBS services' : 'Diensten van DCBS', itemListElement: DIENSTEN.map(([s, naam], i) => ({ '@type': 'ListItem', position: i + 1, name: t(naam), url: u(`diensten/${s}/`) })) },
    kruimels([['Home', ''], ['Diensten', 'diensten/']]) ];
  const dienst = DIENSTEN.find(([s]) => p === `diensten/${s}/`);
  if (dienst) {
    const naam = t(dienst[1]), vragen = [];
    for (const m of html.matchAll(/<details(?![^>]*class="nav-m")[^>]*>\s*<summary[^>]*>\s*<span>([\s\S]*?)<\/span>[\s\S]*?<\/summary>([\s\S]*?)<\/details>/g)) {
      const v = ont(m[1]), a = ont(m[2]);
      if (v && a) vragen.push({ '@type': 'Question', name: v, acceptedAnswer: { '@type': 'Answer', text: a } });
    }
    const g = [ { '@type': 'Service', '@id': u(p) + '#dienst', name: naam, serviceType: naam, description: description(html), url: u(p), provider: orgRef, areaServed: land },
      kruimels([['Home', ''], ['Diensten', 'diensten/'], [dienst[1], p]]) ];
    if (vragen.length) g.push({ '@type': 'FAQPage', '@id': u(p) + '#faq', mainEntity: vragen });
    return g;
  }
  if (p === 'over-ons/') {
    const persoon = { '@type': 'Person', '@id': BASIS + '/over-ons/#jeroen-dubach', name: 'Jeroen Dubach', jobTitle: en ? 'Founder and external DPO' : 'Oprichter en externe FG', worksFor: orgRef, url: u(p),
      alumniOf: [{ '@type': 'CollegeOrUniversity', name: 'Tilburg University' }, { '@type': 'CollegeOrUniversity', name: en ? 'University of Amsterdam' : 'Universiteit van Amsterdam' }],
      hasCredential: [{ '@type': 'EducationalOccupationalCredential', name: 'CIPP/E (IAPP)' }, { '@type': 'EducationalOccupationalCredential', name: 'BC 5701 Lead Implementor' }],
      knowsLanguage: ['nl', 'en', 'de'] };
    return [ { '@type': 'AboutPage', '@id': u(p), url: u(p), name: en ? 'About DCBS' : 'Over DCBS', inLanguage: taal, about: orgRef, mainEntity: { '@id': persoon['@id'] } }, persoon, kruimels([['Home', ''], ['Over ons', p]]) ];
  }
  if (p === 'cases/') return [kruimels([['Home', ''], ['Cases', p]])];
  if (p === 'contact/') return [ { '@type': 'ContactPage', '@id': u(p), url: u(p), name: en ? 'Contact DCBS' : 'Contact met DCBS', inLanguage: taal, about: orgRef }, kruimels([['Home', ''], ['Contact', p]]) ];
  if (p === 'nieuws/') {
    const lijst = (en ? ARTIKELEN_EN : ARTIKELEN).filter(a => a.url && a.url.startsWith('/'));
    return [ { '@type': 'CollectionPage', '@id': u(p), url: u(p), name: en ? 'DCBS news and insights' : 'Nieuws en inzichten van DCBS', inLanguage: taal, publisher: orgRef,
      mainEntity: { '@type': 'ItemList', itemListElement: lijst.map((a, i) => ({ '@type': 'ListItem', position: i + 1, name: a.title, url: BASIS + a.url })) } }, kruimels([['Home', ''], ['Nieuws', p]]) ];
  }
  if (p === 'privacybeleid/') return [kruimels([['Home', ''], ['Privacybeleid', p]])];
  return [];
}
function statisch(html, p, lijst) {
  if (p !== '' && p !== 'nieuws/') return html;
  const inhoud = p === '' ? S.home(lijst) : S.lijst(lijst);
  const blok = S.vervangTussen(html, S.ST_START, S.ST_EIND, inhoud);
  if (blok !== null) return blok;
  const doel = p === '' ? /(<div id="v6-nieuws-home"[^>]*>)(<\/div>)/ : /(<div id="nieuws-lijst"[^>]*>)(<\/div>)/;
  if (!doel.test(html)) throw new Error('plek voor de artikellijst niet gevonden in ' + p);
  return html.replace(doel, (m, a, b) => a + S.ST_START + inhoud + S.ST_EIND + b);
}

// ---- 1 en 2. Gewone pagina's, Nederlands en Engels ----
for (const p of PAGINAS) {
  const f = p + 'index.html';
  let nl = taalwissel(kaal(lees(f)), 'nl', p, enPad(p));
  if (p === 'nieuws/') nl = nl.replace('<div id="beheer-paneel" style="display:none">', '<div id="beheer-paneel" data-nosnippet style="display:none">');
  // Engels: vertalen vanaf de Nederlandse pagina, vóór de taalafhankelijke onderdelen erin gaan
  let bron = nl;
  if (p === 'nieuws/') {   // het beheer staat alleen op de Nederlandse pagina
    const a = bron.indexOf('<div style="display:flex;justify-content:flex-end"><button id="beheer-knop"'), b = bron.indexOf('<div id="nieuws-lijst"');
    if (a < 0 || b < a) throw new Error('beheerpaneel niet gevonden');
    bron = bron.slice(0, a) + bron.slice(b);
  }
  if (S.vervangTussen(bron, S.ST_START, S.ST_EIND, '') !== null) bron = S.vervangTussen(bron, S.ST_START, S.ST_EIND, '');
  let en = taalwissel(vertaal(bron, f), 'en', p, enPad(p));
  nl = statisch(nl, p, ARTIKELEN);
  en = statisch(en, p, ARTIKELEN_EN);
  schrijf(f, zetHead(nl, p, structuredData(nl, 'nl', p)));
  schrijf(enPad(p) + 'index.html', zetHead(en, p, structuredData(en, 'en', p)));
}

// ---- 3. Artikelsjablonen en artikelpagina's ----
let tplNl = taalwissel(lees('nieuws/_template.html'), 'nl', 'nieuws/', 'en/nieuws/').replace(/\/site\.js\?v=\d+/g, '/site.js?v=' + VERSIE);
schrijf('nieuws/_template.html', tplNl);
const tplEn = taalwissel(vertaal(tplNl, 'nieuws/_template.html'), 'en', 'nieuws/', 'en/nieuws/');
schrijf('en/nieuws/_template.html', tplEn);
for (const a of ARTIKELEN.filter(a => a.slug)) {
  schrijf(`nieuws/${a.slug}/index.html`, S.pagina(tplNl, a, lees(`nieuws/${a.slug}/artikel.md`).trim(), 'nl', !!a.en));
  if (a.en) schrijf(`en/nieuws/${a.slug}/index.html`, S.pagina(tplEn, S.artikelEn(a), lees(`en/nieuws/${a.slug}/artikel.md`).trim(), 'en', true));
}

// ---- 4. Doorverwijzingen en sitemap ----
for (const [van, naar] of VERHUISD) {
  const en = van.startsWith('en/');
  schrijf(van + 'index.html', `<!DOCTYPE html>\n<html lang="${en ? 'en' : 'nl'}">\n<head>\n<meta charset="utf-8">\n<title>${en ? 'Moved' : 'Verhuisd'} | DCBS</title>\n<meta name="robots" content="noindex">\n<link rel="canonical" href="${BASIS}/${naar}">\n<meta http-equiv="refresh" content="0; url=/${naar}">\n</head>\n<body>\n<p>${en ? 'This page has moved to' : 'Deze pagina is verhuisd naar'} <a href="/${naar}">${BASIS}/${naar}</a>.</p>\n</body>\n</html>\n`);
}
{
  const vandaag = new Date().toISOString().slice(0, 10);
  const oud = bestaat('sitemap.xml') ? lees('sitemap.xml') : '';
  const datum = (loc, inhoudGewijzigd) => { const m = oud.match(new RegExp('<loc>' + loc.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '</loc><lastmod>([^<]+)</lastmod>')); return m && !inhoudGewijzigd ? m[1] : vandaag; };
  const regels = [];
  for (const p of PAGINAS.filter(p => !NIET_IN_SITEMAP.has(p))) for (const pad of [p, enPad(p)]) {
    const f = pad + 'index.html', gewijzigd = !bestaat(f) || lees(f) !== uitvoer.get(f);
    regels.push(`  <url><loc>${BASIS}/${pad}</loc><lastmod>${datum(BASIS + '/' + pad, gewijzigd)}</lastmod></url>\n`);
  }
  schrijf('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + regels.join('') + '  ' + S.SM_START + S.sitemap(ARTIKELEN) + S.SM_EIND + '\n</urlset>\n');
}

// ---- klaar: alleen schrijven als alles vertaald is ----
if (ontbreekt.size) {
  console.error(`${ontbreekt.size} tekst(en) zonder vertaling in tools/vertalingen.json:`);
  if (ALLEEN_ONTBREEKT) console.log(JSON.stringify([...ontbreekt.keys()], null, 0));
  else for (const [k, waar] of ontbreekt) console.error(`  [${waar}] ${k}`);
  process.exit(ALLEEN_ONTBREEKT ? 0 : 1);
}
let n = 0;
for (const [p, t] of uitvoer) {
  const doel = path.join(REPO, p);
  if (fs.existsSync(doel) && fs.readFileSync(doel, 'utf8') === t) continue;
  fs.mkdirSync(path.dirname(doel), { recursive: true }); fs.writeFileSync(doel, t); n++;
}
console.log(`${uitvoer.size} bestanden gecontroleerd, ${n} bijgewerkt. Artikelen: ${ARTIKELEN.length} (Engels: ${ARTIKELEN_EN.length}).`);
