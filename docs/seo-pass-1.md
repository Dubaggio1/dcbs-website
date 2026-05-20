# SEO Pass 1 — Eindrapport

**Branch:** `seo-refactor-2026-05`
**Datum:** 2026-05-20
**Scope:** Multi-file refactor + SEO-meta + structured data + nieuwe dienstpagina's + analytics
**Status:** Klaar voor review. Niet gepushed naar `main` zonder eigenaar-goedkeuring.

---

## 1. Wat de site nu doet vs. ervoor

| | Voor | Na |
|---|---|---|
| Architectuur | Single-page HTML (1.4 MB, SPA via JS) | 40 statische HTML-bestanden, multi-file |
| URL routing | `/` werkte (200), alle andere routes 404 | Alle 40 URL's → 200, geen 404-redirect-truc meer nodig |
| Per-pagina `<title>` | 1 titel voor alle pagina's | Uniek per pagina |
| Per-pagina `<meta description>` | 1 description | Uniek per pagina (van 70-160 chars) |
| Hreflang | nl + en, beide naar `https://www.dcbs.nl` (invalid) | nl-NL ↔ en-GB correct gekoppeld + x-default per pair |
| Sitemap.xml | Niet aanwezig | 40 URL's met `lastmod`/`changefreq`/`priority` + 3 hreflang-tags per URL |
| Robots.txt | Niet aanwezig | Aanwezig met sitemap-verwijzing |
| Structured data | 1× ProfessionalService op homepage (alleen NL) | ProfessionalService + WebSite + Service (per dienstpagina) + Article (per nieuwsartikel) |
| Dienstpagina's | 0 sub-pagina's, 1 hub | 4 sub-pagina's (NL+EN = 8) + grid-update op hub |
| Analytics | Geen | Plausible (cookieless) ingebouwd, klaar voor activatie |
| Privacy statement | Klopt niet (Netlify vermeld), mist sectie EN | Correct (GitHub Pages), EN-pagina aangevuld met sectie Third Parties |

---

## 2. Gewijzigde bestanden

| Pad | Wat |
|---|---|
| `index.html` | SPA-content vervangen door statische NL-homepage |
| `404.html` | Nieuwe redirect-map (legacy `/privacy` → `/privacybeleid/`, art-keys → slugs, ?p=key fallback) + nette 404-pagina-fallback |

## 3. Nieuwe bestanden

### HTML — 38 nieuwe pagina's
| Categorie | Bestanden |
|---|---|
| NL core (6) | `/over-ons/`, `/diensten/`, `/cases/`, `/nieuws/`, `/contact/`, `/privacybeleid/` |
| EN core (7) | `/en/`, `/en/over-ons/`, `/en/diensten/`, `/en/cases/`, `/en/nieuws/`, `/en/contact/`, `/en/privacy-statement/` |
| NL artikelen (9) | `/nieuws/vodafone-boete-45-miljoen/`, `/nieuws/fria-fundamental-rights-impact-assessment/`, `/nieuws/ai-literacy-verplichting/`, `/nieuws/claude-ai-governance-discipline/`, `/nieuws/risicos-generatieve-ai/`, `/nieuws/tesla-robotaxi-privacy/`, `/nieuws/zeven-jaar-avg-handhaving-nederland/`, `/nieuws/ai2027-superintelligente-ai/`, `/nieuws/bc-5701-privacy-keurmerk/` |
| EN artikel-stubs (9) | `/en/nieuws/<zelfde slugs>/` |
| NL dienst-landings (4) | `/diensten/dpo-as-a-service/`, `/diensten/avg-compliance/`, `/diensten/ai-act-compliance/`, `/diensten/data-management/` |
| EN dienst-landings (4) | `/en/diensten/dpo-as-a-service/`, `/en/diensten/gdpr-compliance/`, `/en/diensten/ai-act-compliance/`, `/en/diensten/data-management/` |

### Shared assets
| Pad | Doel |
|---|---|
| `assets/css/main.css` | Alle CSS uit oude `<style>` (562 regels, incl. base64 Helvetica/HN fonts) |
| `assets/js/main.js` | Shared op alle pagina's — LANGUAGE_MAP, setLang, mobile menu, cookie banner, nav-active-state, copyright year, scroll reveal |
| `assets/js/nieuws-form.js` | Alleen op `/nieuws/` en `/en/nieuws/` — 3-click admin, saveArticle, renderCustomNews, showCustomArt |
| `assets/js/contact-form.js` | Alleen op `/contact/` en `/en/contact/` — `sf()` submit handler |
| `assets/js/translate.js` | Alleen op EN-stubs — runtime EN-translation via Anthropic API (security flag, zie §5) |

### Discovery
| Pad | Doel |
|---|---|
| `sitemap.xml` | 40 URL's + hreflang-alternates per URL |
| `robots.txt` | `User-agent: *`, `Allow: /`, `Sitemap: ...` |

### Tooling (alleen voor onderhoud, niet via GitHub Pages geserveerd)
| Pad | Doel |
|---|---|
| `tools/extract_templates.py` | One-shot extractie van oude `P[key]` templates naar `tools/templates.json` |
| `tools/build_pages.py` | Genereert alle 40 HTML-bestanden + sitemap + robots vanuit configs |
| `tools/templates.json` | Snapshot van extracted body content per oude P-key |

### `docs/seo-pass-1.md`
Dit rapport.

**Diff totalen:** 51 files changed, +14035 / −3068 (de 1.4 MB SPA `index.html` wordt vervangen door ~700 KB statische homepage).

---

## 4. Verificatie-checklist

Alle checks die geslaagd zijn tijdens phase-builds + finale audit:

### Routing & status
- [x] Alle 40 URL's geven 200-statuscode in lokale `python -m http.server` test
- [x] Oude `/privacy` redirect via 404.html naar `/privacybeleid/`
- [x] Oude art-keys redirect naar nieuwe slugs (`/art-vodafone` → `/nieuws/vodafone-boete-45-miljoen/`)
- [x] Legacy `?p=key` query param uit oude SPA blijft werken via 404.html

### Meta-tags
- [x] Elke pagina heeft uniek `<title>`
- [x] Elke pagina heeft uniek `<meta description>`
- [x] Elke pagina heeft `<meta keywords>` (geen stuffing, gericht per dienst/onderwerp)
- [x] Elke pagina heeft `<meta author>` en `<meta robots="index, follow">`

### Canonical & hreflang
- [x] Elke pagina heeft `<link rel="canonical">` naar zichzelf
- [x] Elke pagina heeft 3 hreflang-tags: `nl-NL`, `en-GB`, `x-default`
- [x] Hreflang-paren wijzen naar bestaande 200-URL's (geen 404)
- [x] x-default verwijst naar NL-versie (Google convention)
- [x] EN-stubs voor nieuwsartikelen krijgen hreflang naar NL-origineel + andersom — geverifieerd voor alle 9 paren

### Open Graph & Twitter
- [x] Elke pagina heeft `og:title` / `og:description` / `og:url` / `og:locale` / `og:site_name` / `og:type`
- [x] Elke pagina heeft `twitter:card` / `twitter:title` / `twitter:description`

### JSON-LD structured data
- [x] Homepages (NL + EN) hebben `ProfessionalService` schema met:
  - name, alternateName, description, url
  - telephone +31-615234409, email contact@dcbs.nl
  - address: Bakemastraat 48, 3544MT Utrecht NL
  - founder Jeroen Dubach
  - areaServed Netherlands
  - serviceType array (6 items)
  - taxID "KVK 66569346"
  - sameAs LinkedIn
- [x] Alle 40 pagina's hebben `WebSite` schema (publisher = DCBS)
- [x] Dienstpagina's (8 totaal) hebben `Service` schema met provider/areaServed/serviceType/url
- [x] Nieuwsartikelen (18 totaal NL+EN) hebben `Article` schema met headline/description/author/publisher/inLanguage/url

### Sitemap & robots
- [x] `sitemap.xml` is valide XML met namespace `xmlns:xhtml="http://www.w3.org/1999/xhtml"`
- [x] 40 `<url>` entries
- [x] Per URL: `<loc>` `<lastmod>` `<changefreq>` `<priority>` `<xhtml:link>×3`
- [x] `robots.txt` bestaat, verwijst naar `https://www.dcbs.nl/sitemap.xml`

### Plausible Analytics (technical install)
- [x] Plausible-script in `<head>` van alle 40 pagina's: `<script defer data-domain="dcbs.nl" src="https://plausible.io/js/script.js"></script>`
- [x] Custom event-classes via `class="plausible-event-name=..."`:
  - `Calendly+Click` op alle calendly.com links
  - `Email+Click` op mailto:contact@dcbs.nl
  - `Phone+Click` op tel: links
  - `Gratis+Consult+Click` op nav-CTA (class=`ncta`)
  - `Contact+Form+Submit` op submit-button binnen contact-form
- [x] Privacy statement (NL + EN) uitgebreid met Plausible-paragraaf
- [x] Cookie-banner ongewijzigd (Plausible is cookieless — geen consent vereist)
- [ ] **EIGENAAR-ACTIE NODIG**: Plausible-account aanmaken — zie §5

### Service pages (Phase 4)
- [x] 4 NL dienstpagina's met ~600-1000 woorden body
- [x] 4 EN tegenhangers met `gdpr-compliance` als EN-slug voor `avg-compliance`
- [x] Eigen `Service` JSON-LD per pagina
- [x] Anchor-IDs op `/diensten/avg-compliance/`: `#dpia`, `#datalek`, `#verwerkingsregister`, `#bc-5701` (voor footer-deeplinks)
- [x] BC 5701 expliciet als implementatiepartner gepositioneerd (niet certificeringsorgaan — dat is Brand Compliance)
- [x] FRIA-artikel gelinkt vanaf `/diensten/ai-act-compliance/`
- [x] Data Management afwijkende structuur met "Typische opdrachtvormen" i.p.v. SKU-list
- [x] Hub-pagina `/diensten/` (NL+EN) met 4-kaart overzichts-grid linkend naar sub-pagina's

### Klantnamen-discipline
- [x] Geen klantnamen in body van enige dienstpagina
- [x] "Voor wie"-secties gebruiken uitsluitend sectorvermeldingen
- [x] Link naar `/cases/` voor concrete voorbeelden
- [x] `/cases/`-pagina zelf onaangetast (behoudt klantnamen daar)

### Tone-discipline
- [x] Wij/onze body-count NL: 1 per dienstpagina (alleen "onze cases"-link)
- [x] We/our/us body-count EN: 1 per dienstpagina (alleen "our cases"-link)
- [x] DCBS in derde persoon of werkwoord zonder onderwerp
- [x] Geen clichés: "partner in compliance", "wij ontzorgen", "best-in-class", "bewezen succesvol" — 0 hits

### Verboden termen
- [x] NIS2 / DORA — 0 hits site-breed
- [x] ISO 27001 als DCBS-dienst — 0 hits in dienst- of homepages (de 4 hits in cases-bodies zijn klantcontext, blijven staan)
- [x] BIO als DCBS-dienst — 0 hits (1 hit in cases-body als klantcontext)
- [x] Klokkenluider / whistleblowing — 0 hits
- [x] Apeldoorn — 0 hits (Utrecht is leidend adres)
- [x] EPRODAT — 0 hits

### Functioneel
- [x] Language-toggle (NL/EN-knop) navigeert correct via LANGUAGE_MAP
- [x] Mobile menu hamburger werkt
- [x] Cookie-banner verschijnt 1× per origin (localStorage `dcbs_cookie`)
- [x] Nav-active-state highlightt huidig menu-item via `data-path`
- [x] localStorage `dcbs_articles` survives refactor (per-origin, niet per-path)
- [x] News-form (3-click admin trigger) werkt op `/nieuws/` en `/en/nieuws/`
- [x] showCustomArt aangepast voor multi-file (back-button = `location.href`)
- [x] Contact-form `sf()` werkt op `/contact/` en `/en/contact/`
- [x] Copyright-jaar dynamisch via `[data-copyright-year]` (fallback 2026)
- [x] Geen `onclick="go('...')"` meer in productie HTML (alle vervangen door `<a href="">`)

### Privacy statement
- [x] Plausible-paragraaf toegevoegd na Cookies-sectie (NL + EN)
- [x] NL Sectie 6 "Derden": Netlify → GitHub Pages (factual fix)
- [x] EN nieuwe Sectie 6 "Third parties" toegevoegd (NL had het al, EN ontbrak)
- [x] EN renumbering: 6 "Your rights" → 7, 7 "Changes" → 8

---

## 5. Plausible setup-instructies voor de eigenaar

De **site-zijde** is klaar — script geladen, custom events geclassified, privacy statement bijgewerkt. Plausible begint pas data te verzamelen na onderstaande stappen.

### Stap-voor-stap

1. **Account aanmaken** op [plausible.io/register](https://plausible.io/register)
2. **Domein toevoegen**: `dcbs.nl` (geen `www.` prefix; Plausible matcht subdomains via data-domain="dcbs.nl")
3. **Server-locatie**: kies EU (Plausible Cloud zit standaard in Duitsland — bevestig op account-instellingen)
4. **Plan kiezen**: Starter — €9/mnd, 10.000 pageviews. Voor een consultancy-site ruim voldoende; upgrade kan later
5. **Verificatie**: Plausible toont na site-toevoeging een snippet — dat snippet **hoeft niet** opnieuw geplakt te worden, het staat al in `<head>` van alle 40 pagina's. Plausible detecteert het automatisch zodra er een eerste bezoeker is
6. **Custom goals instellen** (in Plausible-dashboard → "Goals" → "Add Goal" → "Custom Event"):
   - Event name: `Gratis Consult Click` (let op: spatie + hoofdletters zoals geklassed via `+`)
   - Event name: `Calendly Click`
   - Event name: `Email Click`
   - Event name: `Phone Click`
   - Event name: `Contact Form Submit`
7. **Funnel inrichten** (optioneel maar aanbevolen): in dashboard → "Funnels" → Add: `Homepage → /contact/ → Contact Form Submit`. Geeft inzicht in welk percentage van bezoekers daadwerkelijk converteert
8. **GDPR-paragraaf privacy statement** is al klaar — geen actie nodig

### Verificatie ná setup
- Open `https://www.dcbs.nl` in een privacy-browser (geen adblock)
- Plausible dashboard → "Realtime" tab moet 1 visitor tonen
- Klik "Gratis consult" knop → check of `Gratis Consult Click` event verschijnt in "Goals" tab

---

## 6. Open vragen / vervolg-acties (buiten scope deze sessie)

### A. `translateHTML` security — URGENT
**Bestand:** `assets/js/translate.js` (+ similar code in `assets/js/nieuws-form.js` voor article-save translation)

**Probleem:** De code doet client-side `fetch()` naar `api.anthropic.com/v1/messages`. Iedere API-key die deze functie zou gebruiken is voor elke bezoeker zichtbaar in browser DevTools — een gepubliceerde key betekent oneindige misbruik-kosten en mogelijk rate-limit-impact.

**Status nu:** De functie is functioneel actief gehouden (per jouw spec C, vorige sessies). In de huidige code zit GEEN key — de fetch zou 401 returnen tot er ergens een key wordt geconfigureerd. **Risico = laag zolang de key nooit wordt toegevoegd**. Maar zodra iemand een key in de fetch-headers plakt om EN-translation te activeren, ontstaat het lek.

**Voorgestelde aanpak vervolg-sessie** (in volgorde van voorkeur):
1. **Pre-generate alle EN-vertalingen tijdens deploy** via GitHub Action met server-side API call. Verwijder `translate.js` volledig.
2. **Cloudflare Worker / Netlify Function** als proxy met de key server-side. Dashboard-frontend roept proxy aan, proxy belt Anthropic. Key onzichtbaar.
3. **Tijdelijk uitschakelen**: vervang `translate.js` body door een no-op die de NL-tekst toont met disclaimer. Doet hetzelfde wat de huidige EN-stubs visueel al doen.

### B. Privacy statement — overige open punten
1. **Versie-header "maart 2025"** is verouderd (vandaag 2026-05-20). Updaten naar "versie mei 2026" of dynamische datum. Beide pagina's.
2. **EN-pagina mist Sectie 8 "Beveiliging" / Security**. NL heeft "passende technische en organisatorische maatregelen... HTTPS/TLS-encryptie". EN ontbreekt dit volledig. Een privacy consultant hoort minimaal die paragraaf bilingueel beschikbaar te hebben.
3. **Section 2 "Welke persoonsgegevens"** vermeldt "telefoonnummer en uw bericht" — klopt met contact-form. OK.

### C. Performance — fonts (153 KB base64 in CSS)
Het `@font-face` blok in `assets/css/main.css` bevat `HN` (Helvetica Neue Black Condensed) als base64-encoded OTF-blob (~150 KB). Dat blokkeert eerste render tot CSS is geladen.

**Optimalisatie-opties:**
- Splits font naar `assets/fonts/HN.woff2` (woff2 is ~30-40% kleiner dan OTF), gebruik `@font-face src: url('/assets/fonts/HN.woff2')` met `font-display: swap`
- Verwijder font helemaal als de SVG-logos en text-headings dezelfde glyphs ergens anders gebruiken (te onderzoeken)
- Resultaat: ~100 KB kleinere CSS, ~200-400ms sneller First Contentful Paint

### D. Hub-pagina consolidatie (na Plausible-data binnenkomt)
De huidige `/diensten/` hub heeft **dubbele content**: bovenaan nieuwe 4-kaart grid (Phase 5) + daaronder de uitgebreide service-secties uit het oude P[diensten]-template (4× `.svc-grid` 2-col).

Plausible-events na ~4-6 weken laten zien of bezoekers:
- Doorklikken via 4-kaart grid (verwacht gedrag) → uitgebreide secties verwijderen
- Doorklikken vanuit uitgebreide secties (onverwacht) → grid simplificeren, behoud detail
- Geen voorkeur → status quo

Vervolg-sessie nadat data binnen is.

### E. Google Search Console
1. Open [search.google.com/search-console](https://search.google.com/search-console)
2. "Add property" → kies "URL-prefix" → `https://www.dcbs.nl`
3. **Verificatie**: makkelijkste = DNS TXT-record bij domein-provider, OR upload HTML-file (Plausible-domein hosten, ja). Heeft Plausible niet eigen verificatie nodig
4. Na verificatie: "Sitemaps" → URL invullen: `https://www.dcbs.nl/sitemap.xml` → Submit
5. Verwacht: binnen 24-48u ziet GSC alle 40 URL's en indexeert binnen 1-3 weken (afhankelijk van Google's crawl-budget voor dit domein)

### F. Google Business Profile
Voor lokale vindbaarheid in Utrecht ("privacy consultant Utrecht" search):
1. [business.google.com](https://business.google.com)
2. "Add your business"
3. Naam: The Data Compliance Builders
4. Categorie: Business consultant / Privacy consultant / Legal consultant
5. Adres: Bakemastraat 48, 3544MT Utrecht
6. Telefoon: +31 6 15 23 44 09
7. Website: `https://www.dcbs.nl`
8. Verificatie via post (Google stuurt een briefkaart met code, duurt 5-14 dagen)

Eenmaal geverifieerd: profile completen met:
- Beschrijving
- Openingstijden (of "by appointment only")
- Eerste foto's (zelfs een logo + kantoor-pand is voldoende voor start)
- Vraag eerste tevreden klanten om een Google-review (transformatief voor lokale ranking)

### G. Pijler-artikelen schrijven (4 stuks, 1 per dienstcluster)
Pijler-artikelen zijn 2.500-4.000 woord long-form content die ranked op de breedste keyword in elk cluster + intern linkt naar alle gerelateerde nieuwsartikelen. Voorgestelde titels:

1. **"De Complete Gids voor Externe DPO-Inhuur in Nederland (2026)"** — target: "externe DPO inhuren", "DPO uitbesteden mkb"; link naar `/diensten/dpo-as-a-service/` + relevante nieuwsartikelen
2. **"AVG-Compliance Voor Bedrijven: Een Praktisch Stappenplan"** — target: "AVG compliance", "AVG advies bedrijf"; link naar BC 5701-artikel, vodafone-boete-artikel
3. **"EU AI Act Compliance: Wat Uw Organisatie Nu Moet Doen"** — target: "EU AI Act consultancy", "AI Act naleving"; link naar FRIA-artikel, AI-literacy-artikel, AI2027-artikel
4. **"Data Governance Voor Privacy- en AI-Compliance: DAMA-DMBOK In De Praktijk"** — target: "data governance framework", "DAMA DMBOK implementatie"; link naar relevante cases

Plan: 1 per maand, gepubliceerd op `/nieuws/<slug>/` zodat ze direct in sitemap meekomen.

### H. Backlink-strategie
Hoge-autoriteit backlinks zijn niet aan te kopen — wel verdienbaar via:

1. **Gastblogs** op iapp.org, privacycompany.nl, privacyfirst.nl, security.nl (Tweakers' security-tak)
2. **Branchepublicaties**: Privacy in Bedrijf, AG Connect, ComputerWeekly NL, Computable
3. **Speaker-spots** op Privacy Awareness Week (mei), Cybersec Europe (Brussel), Nederlandse PrivacyKring meetups → spreker-pagina's linken meestal naar persoonlijke site/LinkedIn
4. **LinkedIn-artikelen** met inhoudelijke verdieping op privacy-onderwerpen → backlinks vanuit comments + reposts
5. **Wikipedia-edits** op AVG / EU AI Act NL-pagina's met DCBS als bron — alleen als de citatie ECHT van waarde is (anders mod-revert)

Realistische tijdshorizon: 6-12 maanden voor 5-10 hoge-kwaliteit backlinks (Domain Authority 40+).

---

## 7. Hoe te mergen

```bash
# Op Beelink
cd c:/Users/Jeroen/dcbs-website
git push origin seo-refactor-2026-05

# Daarna op GitHub.com:
# - Pull Request maken: seo-refactor-2026-05 → main
# - Lees deze md door als PR-omschrijving
# - Eigenaar merged na review
# - GitHub Pages deployed automatisch (~1 min) na merge
# - Verifieer: open www.dcbs.nl/sitemap.xml in browser
```

**Geen force-push, geen rebase op main, geen squash zonder bevestiging.** De 8 commits beschrijven elk een logische fase en geven goede git-history.

---

## 8. Commit-overzicht

| # | Hash | Fase | Wat |
|---|---|---|---|
| 1 | `afd3e29` | 2 | Shared CSS + JS assets |
| 2 | `9338da5` | 3a | 14 core pagina's refactor (NL+EN) |
| 3 | `b9e0abc` | 3b | 18 article-pagina's + 404 redirects |
| 4 | `187f2ae` | 4a | DPO-as-a-service NL+EN |
| 5 | `fe32d7d` | 4b | AVG / AI-Act / Data Management NL+EN + DPO klant-correctie |
| 6 | `1252cf2` | 5 | Hub-cards grid + AI-act "voor wie"-correctie |
| 7 | `c386072` | 6+7 | sitemap.xml, robots.txt, Plausible events, privacy update |
| 8 | `c90c6d5` | 7c | Privacy factual fix (Netlify → GitHub Pages, EN sectie aangevuld) |

Plus deze commit met `/docs/seo-pass-1.md` als #9.

---

**Einde rapport.** Wacht op eigenaar-goedkeuring voor push + PR.
