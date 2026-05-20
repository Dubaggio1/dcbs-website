#!/usr/bin/env python3
"""Genereer multi-file static site uit templates.json + per-pagina config.

Run: python tools/build_pages.py
Output: schrijft pagina's naar root + subfolders.

Scope nu: 14 core pagina's (7 NL + 7 EN). News article pages worden
toegevoegd na slug-confirmation door user.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEMPLATES = json.loads((ROOT / "tools" / "templates.json").read_text(encoding="utf-8"))

# ─────────────────────────────────────────────────────────────────────
#  PER-PAGINA CONFIG
# ─────────────────────────────────────────────────────────────────────
# Elke entry: { url, lang, title, description, keywords, og_title,
#               og_description, jsonld_extra (optional), template_key }
# `url` is het pad waar de pagina komt te wonen (zonder hostname).
# JSON-LD ProfessionalService wordt automatisch op homepages gezet.

NL = "nl"
EN = "en"

PAGES = [
    # ── NL core ────────────────────────────────────────────────────────
    {
        "url": "/", "lang": NL, "template": "home",
        "title": "Privacy & AI Compliance Consultant Utrecht | DPO as a Service | The Data Compliance Builders",
        "description": "Onafhankelijke privacy en AI compliance consultancy in Utrecht. Externe DPO, interim Functionaris Gegevensbescherming, AVG-audits, DPIA's, EU AI Act, ISO 42001, BC 5701 en data governance. Voor mkb, corporates en (semi-)publieke organisaties. Gratis kennismakingsgesprek.",
        "keywords": "privacy consultant Utrecht, externe DPO, interim DPO, functionaris gegevensbescherming, DPO as a service, AVG consultant, GDPR advies, privacy audit, DPIA, EU AI Act, AI compliance, ISO 42001, BC 5701, data management, data governance",
        "og_title": "Privacy & AI Compliance Consultant Utrecht | DCBS",
        "og_description": "Externe DPO, AVG-audits, EU AI Act en data governance — pragmatisch en bewezen effectief. Gevestigd in Utrecht.",
    },
    {
        "url": "/over-ons/", "lang": NL, "template": "over",
        "title": "Over Ons | Jeroen Dubach | The Data Compliance Builders",
        "description": "The Data Compliance Builders is een onafhankelijk Nederlands adviesbureau voor privacy en AI compliance, opgericht door Jeroen Dubach. Ervaring bij AFM, Gemeente Amsterdam, Evides, Athlon en SCOR.",
        "keywords": "Jeroen Dubach, privacy consultant Nederland, DCBS, The Data Compliance Builders, over ons",
        "og_title": "Over Ons | DCBS",
        "og_description": "Jeroen Dubach: onafhankelijk privacy en AI compliance consultant in Utrecht.",
    },
    {
        "url": "/diensten/", "lang": NL, "template": "diensten",
        "title": "Onze Diensten | Privacy, DPO, AI Act, Data Management | DCBS",
        "description": "Vier expertisegebieden: privacy / AVG compliance, DPO as a service, EU AI Act compliance en data management. Pragmatisch advies voor Nederlandse organisaties.",
        "keywords": "diensten DCBS, AVG advies, DPO uitbesteden, EU AI Act consultancy, data governance Nederland",
        "og_title": "Diensten | DCBS",
        "og_description": "Privacy, DPO, EU AI Act en data management — vier expertisegebieden.",
    },
    {
        "url": "/cases/", "lang": NL, "template": "cases",
        "title": "Cases en Referenties | DCBS Privacy Consultancy",
        "description": "Praktijkvoorbeelden van DCBS-opdrachten bij AFM, Gemeente Amsterdam, Evides, Athlon, SCOR, IKEA Supply AG en Ahold Delhaize.",
        "keywords": "privacy cases, AVG implementatie referenties, DPO opdrachten Nederland",
        "og_title": "Cases | DCBS",
        "og_description": "AFM, Gemeente Amsterdam, Evides, Athlon, SCOR, IKEA Supply AG, Ahold Delhaize.",
    },
    {
        "url": "/nieuws/", "lang": NL, "template": "nieuws",
        "title": "Nieuws en Inzichten | Privacy, AI Act, GDPR-jurisprudentie | DCBS",
        "description": "Analyses en updates over GDPR, EU AI Act, AVG-jurisprudentie en data governance. Geschreven door Jeroen Dubach.",
        "keywords": "AVG nieuws, EU AI Act updates, privacy jurisprudentie, GDPR analyses",
        "og_title": "Nieuws | DCBS",
        "og_description": "Analyses over GDPR, EU AI Act, AVG-jurisprudentie en data governance.",
        "extra_scripts": ["/assets/js/nieuws-form.js"],
    },
    {
        "url": "/contact/", "lang": NL, "template": "contact",
        "title": "Contact | Gratis Kennismakingsgesprek | DCBS Utrecht",
        "description": "Neem contact op met The Data Compliance Builders in Utrecht. Gratis kennismakingsgesprek over uw privacy of AI compliance vraagstuk.",
        "keywords": "contact DCBS, privacy consultant Utrecht contact, DPO inhuren",
        "og_title": "Contact | DCBS Utrecht",
        "og_description": "Gratis kennismakingsgesprek over uw privacy of AI compliance vraagstuk.",
        "extra_scripts": ["/assets/js/contact-form.js"],
    },
    {
        "url": "/privacybeleid/", "lang": NL, "template": "privacy",
        "title": "Privacybeleid | The Data Compliance Builders",
        "description": "Privacybeleid van The Data Compliance Builders: hoe wij omgaan met uw gegevens via deze website en bij onze dienstverlening.",
        "keywords": "privacybeleid DCBS, AVG verklaring The Data Compliance Builders",
        "og_title": "Privacybeleid | DCBS",
        "og_description": "Hoe wij omgaan met uw gegevens bij DCBS.",
        "robots": "index, follow",
    },

    # ── EN core ────────────────────────────────────────────────────────
    {
        "url": "/en/", "lang": EN, "template": "en-home",
        "title": "Privacy & AI Compliance Consultant Netherlands | DPO as a Service | The Data Compliance Builders",
        "description": "Independent privacy and AI compliance consultancy in Utrecht, Netherlands. External DPO, interim Data Protection Officer, GDPR audits, DPIAs, EU AI Act, ISO 42001, BC 5701 and data governance. Free intake call.",
        "keywords": "privacy consultant Netherlands, external DPO, interim DPO, Data Protection Officer, DPO as a service, GDPR consultant, GDPR advice, privacy audit, DPIA, EU AI Act, AI compliance, ISO 42001, BC 5701, data management, data governance",
        "og_title": "Privacy & AI Compliance Consultant Netherlands | DCBS",
        "og_description": "External DPO, GDPR audits, EU AI Act and data governance — pragmatic and effective. Based in Utrecht.",
    },
    {
        "url": "/en/over-ons/", "lang": EN, "template": "en-over",
        "title": "About Us | Jeroen Dubach | The Data Compliance Builders",
        "description": "The Data Compliance Builders is an independent Dutch consultancy for privacy and AI compliance, founded by Jeroen Dubach. Experience with AFM, City of Amsterdam, Evides, Athlon and SCOR.",
        "keywords": "Jeroen Dubach, privacy consultant Netherlands, DCBS, The Data Compliance Builders, about us",
        "og_title": "About Us | DCBS",
        "og_description": "Jeroen Dubach: independent privacy and AI compliance consultant in Utrecht.",
    },
    {
        "url": "/en/diensten/", "lang": EN, "template": "en-diensten",
        "title": "Our Services | Privacy, DPO, AI Act, Data Management | DCBS",
        "description": "Four areas of expertise: privacy / GDPR compliance, DPO as a service, EU AI Act compliance and data management. Pragmatic advice for Dutch organisations.",
        "keywords": "DCBS services, GDPR advice, outsource DPO, EU AI Act consultancy, data governance Netherlands",
        "og_title": "Services | DCBS",
        "og_description": "Privacy, DPO, EU AI Act and data management — four areas of expertise.",
    },
    {
        "url": "/en/cases/", "lang": EN, "template": "en-cases",
        "title": "Cases and References | DCBS Privacy Consultancy",
        "description": "Examples of DCBS engagements at AFM, City of Amsterdam, Evides, Athlon, SCOR, IKEA Supply AG and Ahold Delhaize.",
        "keywords": "privacy cases, GDPR implementation references, DPO engagements Netherlands",
        "og_title": "Cases | DCBS",
        "og_description": "AFM, City of Amsterdam, Evides, Athlon, SCOR, IKEA Supply AG, Ahold Delhaize.",
    },
    {
        "url": "/en/nieuws/", "lang": EN, "template": "en-nieuws",
        "title": "News and Insights | Privacy, AI Act, GDPR Case Law | DCBS",
        "description": "Analyses and updates on GDPR, EU AI Act, GDPR case law and data governance. Written by Jeroen Dubach.",
        "keywords": "GDPR news, EU AI Act updates, privacy case law, GDPR analyses",
        "og_title": "News | DCBS",
        "og_description": "Analyses on GDPR, EU AI Act, case law and data governance.",
        "extra_scripts": ["/assets/js/nieuws-form.js"],
    },
    {
        "url": "/en/contact/", "lang": EN, "template": "en-contact",
        "title": "Contact | Free Intake Call | DCBS Utrecht",
        "description": "Contact The Data Compliance Builders in Utrecht. Free intake call about your privacy or AI compliance question.",
        "keywords": "contact DCBS, privacy consultant Utrecht contact, hire DPO",
        "og_title": "Contact | DCBS Utrecht",
        "og_description": "Free intake call about your privacy or AI compliance question.",
        "extra_scripts": ["/assets/js/contact-form.js"],
    },
    {
        "url": "/en/privacy-statement/", "lang": EN, "template": "en-privacy",
        "title": "Privacy Statement | The Data Compliance Builders",
        "description": "Privacy statement of The Data Compliance Builders: how we handle your data via this website and during our engagements.",
        "keywords": "privacy statement DCBS, GDPR declaration The Data Compliance Builders",
        "og_title": "Privacy Statement | DCBS",
        "og_description": "How we handle your data at DCBS.",
        "robots": "index, follow",
    },
]

# Hreflang mapping NL ↔ EN op basis van URL-paren
HREFLANG_PAIRS = {
    "/":                       "/en/",
    "/over-ons/":              "/en/over-ons/",
    "/diensten/":              "/en/diensten/",
    "/cases/":                 "/en/cases/",
    "/nieuws/":                "/en/nieuws/",
    "/contact/":               "/en/contact/",
    "/privacybeleid/":         "/en/privacy-statement/",
}

# JSON-LD ProfessionalService — gebruikt op beide homepages
PROFSERVICE_JSONLD_NL = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "The Data Compliance Builders",
    "alternateName": "DCBS",
    "description": "Onafhankelijke privacy en AI compliance consultancy gespecialiseerd in AVG, DPO as a Service, EU AI Act en data governance.",
    "url": "https://www.dcbs.nl",
    "telephone": "+31-615234409",
    "email": "contact@dcbs.nl",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Bakemastraat 48",
        "postalCode": "3544MT",
        "addressLocality": "Utrecht",
        "addressCountry": "NL",
    },
    "founder": {"@type": "Person", "name": "Jeroen Dubach"},
    "areaServed": {"@type": "Country", "name": "Netherlands"},
    "serviceType": [
        "Privacy Compliance",
        "DPO as a Service",
        "AVG / GDPR Compliance",
        "EU AI Act Compliance",
        "Data Management",
        "Data Governance",
    ],
    "taxID": "KVK 66569346",
    "sameAs": ["https://www.linkedin.com/company/the-data-compliance-builders/"],
}

PROFSERVICE_JSONLD_EN = dict(PROFSERVICE_JSONLD_NL)
PROFSERVICE_JSONLD_EN["description"] = (
    "Independent privacy and AI compliance consultancy specialised in GDPR, "
    "DPO as a Service, EU AI Act and data governance."
)

# ─────────────────────────────────────────────────────────────────────
#  HEADER / NAV SNIPPETS
# ─────────────────────────────────────────────────────────────────────

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 90" style="height:44px;width:auto;display:block">
  <defs>
    <linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6b6ef5"/>
      <stop offset="100%" stop-color="#1de9d4"/>
    </linearGradient>
  </defs>
  <rect width="90" height="90" rx="18" fill="url(#lg)"/>
  <rect class="lb" style="animation-delay:0s"    x="14" y="14" width="54" height="11" rx="5.5" fill="white"/>
  <rect class="lb" style="animation-delay:.18s"  x="14" y="31" width="32" height="11" rx="5.5" fill="white"/>
  <rect class="lb" style="animation-delay:.36s"  x="50" y="31" width="26" height="11" rx="5.5" fill="white"/>
  <rect class="lb" style="animation-delay:.54s"  x="14" y="48" width="42" height="11" rx="5.5" fill="white"/>
  <rect class="lb" style="animation-delay:.72s"  x="60" y="48" width="16" height="11" rx="5.5" fill="white"/>
  <rect class="lb" style="animation-delay:.90s"  x="14" y="65" width="24" height="11" rx="5.5" fill="white"/>
  <rect class="lb" style="animation-delay:1.08s" x="42" y="65" width="34" height="11" rx="5.5" fill="white"/>
  <text x="106" y="34"  font-family="HN,Helvetica Neue,Helvetica,sans-serif" font-size="24" fill="white">The <tspan font-weight="900">Data</tspan></text>
  <text x="106" y="61"  font-family="HN,Helvetica Neue,Helvetica,sans-serif" font-size="24" font-weight="900" fill="white">Compliance</text>
  <text x="106" y="87"  font-family="HN,Helvetica Neue,Helvetica,sans-serif" font-size="24" fill="white">Builders</text>
</svg>"""

LOGO_SVG_FOOTER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 90" style="height:38px;width:auto;display:block">
  <defs><linearGradient id="lgf" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#6b6ef5"/><stop offset="100%" stop-color="#1de9d4"/>
  </linearGradient></defs>
  <rect width="90" height="90" rx="18" fill="url(#lgf)"/>
  <rect x="14" y="14" width="54" height="11" rx="5.5" fill="white"/>
  <rect x="14" y="31" width="32" height="11" rx="5.5" fill="white"/>
  <rect x="50" y="31" width="26" height="11" rx="5.5" fill="white"/>
  <rect x="14" y="48" width="42" height="11" rx="5.5" fill="white"/>
  <rect x="60" y="48" width="16" height="11" rx="5.5" fill="white"/>
  <rect x="14" y="65" width="24" height="11" rx="5.5" fill="white"/>
  <rect x="42" y="65" width="34" height="11" rx="5.5" fill="white"/>
  <text x="106" y="34"  font-family="HN,Helvetica Neue,Helvetica,sans-serif" font-size="24" fill="white">The <tspan font-weight="900">Data</tspan></text>
  <text x="106" y="61"  font-family="HN,Helvetica Neue,Helvetica,sans-serif" font-size="24" font-weight="900" fill="white">Compliance</text>
  <text x="106" y="87"  font-family="HN,Helvetica Neue,Helvetica,sans-serif" font-size="24" fill="white">Builders</text>
</svg>"""

NAV_LABELS = {
    NL: {
        "home": "Home", "over": "Over ons", "diensten": "Diensten",
        "cases": "Cases", "nieuws": "Nieuws", "contact": "Gratis consult",
    },
    EN: {
        "home": "Home", "over": "About Us", "diensten": "Services",
        "cases": "Cases", "nieuws": "News", "contact": "Free consult",
    },
}
NAV_URLS = {
    NL: {
        "home": "/", "over": "/over-ons/", "diensten": "/diensten/",
        "cases": "/cases/", "nieuws": "/nieuws/", "contact": "/contact/",
    },
    EN: {
        "home": "/en/", "over": "/en/over-ons/", "diensten": "/en/diensten/",
        "cases": "/en/cases/", "nieuws": "/en/nieuws/", "contact": "/en/contact/",
    },
}


def build_nav(lang: str) -> str:
    labels = NAV_LABELS[lang]
    urls = NAV_URLS[lang]
    home_url = urls["home"]

    def desktop_link(k: str) -> str:
        cls = ' class="ncta"' if k == "contact" else ""
        return f'      <a href="{urls[k]}" data-path="{urls[k]}"{cls}>{labels[k]}</a>'

    def mobile_link(k: str) -> str:
        style = ' style="color:var(--tl)"' if k == "contact" else ""
        suffix = " &rarr;" if k == "contact" else ""
        return f'  <a href="{urls[k]}" data-path="{urls[k]}"{style}>{labels[k]}{suffix}</a>'

    order = ("home", "over", "diensten", "cases", "nieuws", "contact")
    desktop_links = "\n".join(desktop_link(k) for k in order)
    mobile_links = "\n".join(mobile_link(k) for k in order)
    nl_active = "act" if lang == NL else ""
    en_active = "act" if lang == EN else ""
    return f"""<nav>
  <a href="{home_url}" class="nlogo" style="cursor:pointer;text-decoration:none">
    {LOGO_SVG}
  </a>

  <!-- Desktop navigatie -->
  <div class="nav-inner" style="margin-left:auto;align-items:center;gap:2rem">
    <div class="nav-links" id="nav-links">
{desktop_links}
    </div>
    <div class="lang-sw">
      <button class="lbtn {nl_active}" id="btn-nl" onclick="setLang('nl')">NL</button>
      <button class="lbtn {en_active}" id="btn-en" onclick="setLang('en')">EN</button>
    </div>
  </div>

  <!-- Hamburger knop (mobiel) -->
  <button class="hamburger" id="hamburger" type="button" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</nav>

<!-- Mobiel menu -->
<div class="mobile-menu" id="mobile-menu">
{mobile_links}
  <div class="mob-lang">
    <button class="lbtn {nl_active}" id="mob-btn-nl" onclick="setLang('nl')">NL</button>
    <button class="lbtn {en_active}" id="mob-btn-en" onclick="setLang('en')">EN</button>
  </div>
</div>"""


# ─────────────────────────────────────────────────────────────────────
#  FOOTER SNIPPET
# ─────────────────────────────────────────────────────────────────────

def build_footer(lang: str) -> str:
    if lang == NL:
        return f"""<footer>
  <div class="fi">
    <div class="fb">
      <div class="fbr">{LOGO_SVG_FOOTER}</div>
      <p>Onafhankelijk adviesbureau voor privacy, AI en data management compliance. Gevestigd in Utrecht.</p>
    </div>
    <div class="fcol"><h4>Diensten</h4><ul>
      <li><a href="/diensten/dpo-as-a-service/">Externe DPO</a></li>
      <li><a href="/diensten/avg-compliance/">AVG Consultancy</a></li>
      <li><a href="/diensten/ai-act-compliance/">EU AI Act Advies</a></li>
      <li><a href="/diensten/data-management/">Data Management</a></li>
      <li><a href="/diensten/avg-compliance/#dpia">DPIA uitvoeren</a></li>
      <li><a href="/diensten/avg-compliance/#bc-5701">BC 5701 certificering</a></li>
      <li><a href="/diensten/ai-act-compliance/">ISO 42001 implementatie</a></li>
    </ul></div>
    <div class="fcol"><h4>Bedrijf</h4><ul>
      <li><a href="/over-ons/">Over ons</a></li>
      <li><a href="/cases/">Cases</a></li>
      <li><a href="/nieuws/">Nieuws</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener">Afspraak plannen</a></li>
    </ul></div>
    <div class="fcol"><h4>Contact</h4><ul>
      <li><a href="mailto:contact@dcbs.nl" class="plausible-event-name=Email+Click">contact@dcbs.nl</a></li>
      <li><a href="tel:+31615234409" class="plausible-event-name=Phone+Click">+31 (0)6 15 23 44 09</a></li>
      <li>Bakemastraat 48, Utrecht</li>
      <li>KVK: 66569346</li>
      <li><a href="https://linkedin.com/company/the-data-compliance-builders/" target="_blank" rel="noopener">LinkedIn &rarr;</a></li>
    </ul></div>
  </div>
  <div class="fbot">
    <span class="fcp">&copy; <span data-copyright-year>2026</span> The Data Compliance Builders B.V. &middot; Utrecht &middot; <a href="/privacybeleid/" style="color:var(--mu);text-decoration:none">Privacybeleid</a></span>
  </div>
</footer>"""
    else:
        return f"""<footer>
  <div class="fi">
    <div class="fb">
      <div class="fbr">{LOGO_SVG_FOOTER}</div>
      <p>Independent consultancy for privacy, AI and data management compliance. Based in Utrecht, the Netherlands.</p>
    </div>
    <div class="fcol"><h4>Services</h4><ul>
      <li><a href="/en/diensten/dpo-as-a-service/">External DPO</a></li>
      <li><a href="/en/diensten/gdpr-compliance/">GDPR Consultancy</a></li>
      <li><a href="/en/diensten/ai-act-compliance/">EU AI Act Advice</a></li>
      <li><a href="/en/diensten/data-management/">Data Management</a></li>
      <li><a href="/en/diensten/gdpr-compliance/#dpia">DPIA execution</a></li>
      <li><a href="/en/diensten/gdpr-compliance/#bc-5701">BC 5701 certification</a></li>
      <li><a href="/en/diensten/ai-act-compliance/">ISO 42001 implementation</a></li>
    </ul></div>
    <div class="fcol"><h4>Company</h4><ul>
      <li><a href="/en/over-ons/">About us</a></li>
      <li><a href="/en/cases/">Cases</a></li>
      <li><a href="/en/nieuws/">News</a></li>
      <li><a href="/en/contact/">Contact</a></li>
      <li><a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener">Book a meeting</a></li>
    </ul></div>
    <div class="fcol"><h4>Contact</h4><ul>
      <li><a href="mailto:contact@dcbs.nl" class="plausible-event-name=Email+Click">contact@dcbs.nl</a></li>
      <li><a href="tel:+31615234409" class="plausible-event-name=Phone+Click">+31 (0)6 15 23 44 09</a></li>
      <li>Bakemastraat 48, Utrecht</li>
      <li>Dutch Chamber of Commerce: 66569346</li>
      <li><a href="https://linkedin.com/company/the-data-compliance-builders/" target="_blank" rel="noopener">LinkedIn &rarr;</a></li>
    </ul></div>
  </div>
  <div class="fbot">
    <span class="fcp">&copy; <span data-copyright-year>2026</span> The Data Compliance Builders B.V. &middot; Utrecht &middot; <a href="/en/privacy-statement/" style="color:var(--mu);text-decoration:none">Privacy Statement</a></span>
  </div>
</footer>"""


# ─────────────────────────────────────────────────────────────────────
#  COOKIE BANNER + ADMIN MODAL
# ─────────────────────────────────────────────────────────────────────

def build_cookie_banner(lang: str) -> str:
    if lang == NL:
        return """<div id="cookie-banner" role="dialog" aria-label="Cookie-melding">
  <p>Wij gebruiken geen tracking- of advertentiecookies. Alleen functioneel noodzakelijke cookies voor de werking van de website. <a href="/privacybeleid/" style="cursor:pointer">Meer informatie</a></p>
  <div class="cookie-btns">
    <button class="cookie-decline" onclick="cookieDecline()">Alleen noodzakelijk</button>
    <button class="cookie-accept" onclick="cookieAccept()">Akkoord</button>
  </div>
</div>"""
    else:
        return """<div id="cookie-banner" role="dialog" aria-label="Cookie notice">
  <p>We don't use tracking or advertising cookies. Only functionally necessary cookies for the website to operate. <a href="/en/privacy-statement/" style="cursor:pointer">More information</a></p>
  <div class="cookie-btns">
    <button class="cookie-decline" onclick="cookieDecline()">Only necessary</button>
    <button class="cookie-accept" onclick="cookieAccept()">Accept</button>
  </div>
</div>"""


def build_admin_modal(lang: str) -> str:
    """Admin modal voor news-form. Alleen op /nieuws/ + /en/nieuws/ ingesloten."""
    if lang == NL:
        return """<!-- admin: triple-click bottom-right corner to open --><div id="admin-trigger" style="position:fixed;bottom:0;right:0;width:40px;height:40px;z-index:300;cursor:default"></div>
<div class="modal-bg" id="modal-bg" onclick="closeAdmin(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-hd">
      <h3>&#128221; Nieuw artikel toevoegen</h3>
      <button class="modal-close" onclick="closeAdmin()">&times;</button>
    </div>
    <div class="modal-tip">
      <strong>Hoe werkt dit?</strong> Vul het formulier in en klik op Opslaan. Het artikel verschijnt direct op de Nieuws-pagina. Artikelen worden bewaard in uw browser (localStorage) &mdash; ze blijven staan na het herladen van de pagina.
    </div>
    <form onsubmit="saveArticle(event)">
      <div class="fg"><label>Taal van uw artikel / post (de andere taal wordt automatisch vertaald)</label>
        <select id="a-lang"><option value="nl">Nederlands</option><option value="en">English</option></select>
      </div>
      <div class="frow">
        <div class="fg"><label>Categorie</label>
          <select id="a-cat">
            <option value="Privacy">Privacy</option>
            <option value="AI Compliance">AI Compliance</option>
            <option value="Data Management">Data Management</option>
          </select>
        </div>
        <div class="fg"><label>Datum</label><input id="a-date" type="text" placeholder="bijv. Maart 2026" required></div>
      </div>
      <div class="fg"><label>Titel</label><input id="a-title" type="text" placeholder="Titel van het artikel" required></div>
      <div class="fg">
        <label>LinkedIn URL <span style="font-weight:400;color:var(--mu);font-size:.8rem">(optioneel — voeg link naar de LinkedIn post toe)</span></label>
        <input type="url" id="a-li" placeholder="https://www.linkedin.com/posts/the-data-compliance-builders-...">
      </div>
      <div class="fg"><label>Samenvatting (kort, voor de nieuwsoverzichtspagina)</label>
        <textarea id="a-exc" style="min-height:80px" placeholder="Korte samenvatting..." required></textarea>
      </div>
      <div class="fg"><label>Volledige tekst (gebruik een lege regel tussen alinea's)</label>
        <textarea id="a-body" style="min-height:200px" placeholder="Schrijf hier de volledige artikeltekst..."></textarea>
      </div>
      <button class="btn bp" type="submit">Artikel opslaan &rarr;</button>
    </form>
  </div>
</div>"""
    else:
        return """<!-- admin: triple-click bottom-right corner to open --><div id="admin-trigger" style="position:fixed;bottom:0;right:0;width:40px;height:40px;z-index:300;cursor:default"></div>
<div class="modal-bg" id="modal-bg" onclick="closeAdmin(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-hd">
      <h3>&#128221; Add new article</h3>
      <button class="modal-close" onclick="closeAdmin()">&times;</button>
    </div>
    <div class="modal-tip">
      <strong>How does this work?</strong> Fill in the form and click Save. The article appears immediately on the News page. Articles are stored in your browser (localStorage) &mdash; they persist across reloads.
    </div>
    <form onsubmit="saveArticle(event)">
      <div class="fg"><label>Article language (the other language is auto-translated)</label>
        <select id="a-lang"><option value="en">English</option><option value="nl">Nederlands</option></select>
      </div>
      <div class="frow">
        <div class="fg"><label>Category</label>
          <select id="a-cat">
            <option value="Privacy">Privacy</option>
            <option value="AI Compliance">AI Compliance</option>
            <option value="Data Management">Data Management</option>
          </select>
        </div>
        <div class="fg"><label>Date</label><input id="a-date" type="text" placeholder="e.g. March 2026" required></div>
      </div>
      <div class="fg"><label>Title</label><input id="a-title" type="text" placeholder="Article title" required></div>
      <div class="fg">
        <label>LinkedIn URL <span style="font-weight:400;color:var(--mu);font-size:.8rem">(optional — link to LinkedIn post)</span></label>
        <input type="url" id="a-li" placeholder="https://www.linkedin.com/posts/the-data-compliance-builders-...">
      </div>
      <div class="fg"><label>Summary (short, shown on the news overview)</label>
        <textarea id="a-exc" style="min-height:80px" placeholder="Short summary..." required></textarea>
      </div>
      <div class="fg"><label>Full text (separate paragraphs with a blank line)</label>
        <textarea id="a-body" style="min-height:200px" placeholder="Write the full article here..."></textarea>
      </div>
      <button class="btn bp" type="submit">Save article &rarr;</button>
    </form>
  </div>
</div>"""


# ─────────────────────────────────────────────────────────────────────
#  GO() -> HREF transformation
# ─────────────────────────────────────────────────────────────────────

# Mapping van P[key] naar URL. News articles krijgen later slugs (PHASE-3B).
# Voor nu: alle art-* keys mappen naar /nieuws/ overview (fallback) zodat
# we geen broken links produceren tijdens core-pagina refactor.
KEY_TO_URL = {
    "home": "/", "over": "/over-ons/", "diensten": "/diensten/",
    "cases": "/cases/", "nieuws": "/nieuws/", "contact": "/contact/",
    "privacy": "/privacybeleid/",
    "en-home": "/en/", "en-over": "/en/over-ons/", "en-diensten": "/en/diensten/",
    "en-cases": "/en/cases/", "en-nieuws": "/en/nieuws/", "en-contact": "/en/contact/",
    "en-privacy": "/en/privacy-statement/",
    # Articles: placeholder mapping. Final slugs in Phase 3b (na slug-confirm).
    "art-vodafone":    "/nieuws/vodafone-boete-45-miljoen/",
    "art-fria":        "/nieuws/fria-fundamental-rights-impact-assessment/",
    "art-ailliteracy": "/nieuws/ai-literacy-verplichting/",
    "art-claude":      "/nieuws/",  # slug TBD
    "art-genai":       "/nieuws/",  # slug TBD
    "art-tesla":       "/nieuws/",  # slug TBD
    "art-gdpr7":       "/nieuws/",  # slug TBD
    "art-ai2027":      "/nieuws/",  # slug TBD
    "art-bc5701":      "/nieuws/",  # slug TBD
}


def transform_go_links(html: str) -> str:
    """Vervang inline `onclick="go('key')"` (en variants met ;cm()) door
    `href="/url/"`. Indien al een href bestaat: laat staan en strip alleen
    de onclick.
    """
    # Pattern: <tag ... onclick="go('key')..." ... >
    def repl_with_href(match):
        prefix = match.group(1)  # tag opener tot vlak voor onclick
        key = match.group(2)
        url = KEY_TO_URL.get(key, "#")
        # Strip eventuele bestaande href in prefix
        prefix = re.sub(r'\s*href="[^"]*"', "", prefix)
        return f'{prefix} href="{url}"'

    # Pattern: alles tussen openingtag-start en `onclick="go('key')[;cm()]"`
    # We grijpen ALLEEN <a en <div en <span met onclick="go('...')".
    pattern = re.compile(
        r'(<(?:a|div|span|button)\b[^>]*?)\s+onclick="go\([\'\"]([a-z0-9-]+)[\'\"]\)(?:;[a-z()]+)?"',
        re.IGNORECASE,
    )
    return pattern.sub(repl_with_href, html)


# ─────────────────────────────────────────────────────────────────────
#  PAGE BUILDER
# ─────────────────────────────────────────────────────────────────────

FAVICON_SVG_B64 = (
    "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MCA5MCI+CiAgPGRlZnM+"
    "PGxpbmVhckdyYWRpZW50IGlkPSJmZyIgeDE9IjAiIHkxPSIwIiB4Mj0iMSIgeTI9IjEiPgogICAgPHN0b3Agb2Zmc2V0"
    "PSIwJSIgc3RvcC1jb2xvcj0iIzZiNmVmNSIvPjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzFkZTlkNCIv"
    "PgogIDwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPgogIDxyZWN0IHdpZHRoPSI5MCIgaGVpZ2h0PSI5MCIgcng9IjE4IiBm"
    "aWxsPSJ1cmwoI2ZnKSIvPgogIDxyZWN0IHg9IjE0IiB5PSIxNCIgd2lkdGg9IjU0IiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgogIDxyZWN0IHg9IjE0IiB5PSIzMSIgd2lkdGg9IjMyIiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgogIDxyZWN0IHg9IjUwIiB5PSIzMSIgd2lkdGg9IjI2IiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgogIDxyZWN0IHg9IjE0IiB5PSI0OCIgd2lkdGg9IjQyIiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgogIDxyZWN0IHg9IjYwIiB5PSI0OCIgd2lkdGg9IjE2IiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgogIDxyZWN0IHg9IjE0IiB5PSI2NSIgd2lkdGg9IjI0IiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgogIDxyZWN0IHg9IjQyIiB5PSI2NSIgd2lkdGg9IjM0IiBoZWlnaHQ9IjExIiByeD0iNS41"
    "IiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4="
)


def build_page(cfg: dict) -> str:
    lang = cfg["lang"]
    url = cfg["url"]
    nl_url = url if lang == NL else (
        {v: k for k, v in HREFLANG_PAIRS.items()}.get(url, "/")
    )
    en_url = HREFLANG_PAIRS.get(nl_url, "/en/")
    canonical = f"https://www.dcbs.nl{url}"
    nl_canon = f"https://www.dcbs.nl{nl_url}"
    en_canon = f"https://www.dcbs.nl{en_url}"
    html_lang = "nl-NL" if lang == NL else "en-GB"
    og_locale = "nl_NL" if lang == NL else "en_GB"
    robots = cfg.get("robots", "index, follow")

    # Body content uit template (go-links vertaald)
    body_html = transform_go_links(TEMPLATES[cfg["template"]])

    # JSON-LD: homepage krijgt ProfessionalService
    is_home = url in ("/", "/en/")
    jsonld_blocks: list[str] = []
    if is_home:
        ps = PROFSERVICE_JSONLD_NL if lang == NL else PROFSERVICE_JSONLD_EN
        jsonld_blocks.append(
            '<script type="application/ld+json">\n' +
            json.dumps(ps, ensure_ascii=False, indent=2) +
            '\n</script>'
        )

    # WebSite JSON-LD voor alle pagina's
    site_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "The Data Compliance Builders",
        "url": "https://www.dcbs.nl",
        "publisher": {"@type": "ProfessionalService", "name": "The Data Compliance Builders"},
    }

    extra_scripts = cfg.get("extra_scripts", [])
    # Admin modal alleen op nieuws-pagina's
    needs_admin_modal = cfg["template"] in ("nieuws", "en-nieuws")
    admin_modal = build_admin_modal(lang) if needs_admin_modal else ""

    extra_script_tags = "\n".join(
        f'<script src="{src}" defer></script>' for src in extra_scripts
    )

    head_jsonld = "\n".join(jsonld_blocks)

    head = f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cfg["title"]}</title>
<meta name="description" content="{cfg["description"]}">
<meta name="keywords" content="{cfg["keywords"]}">
<meta name="author" content="Jeroen Dubach, The Data Compliance Builders">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">

<!-- Hreflang -->
<link rel="alternate" hreflang="nl-NL" href="{nl_canon}">
<link rel="alternate" hreflang="en-GB" href="{en_canon}">
<link rel="alternate" hreflang="x-default" href="{nl_canon}">

<!-- Open Graph -->
<meta property="og:title" content="{cfg["og_title"]}">
<meta property="og:description" content="{cfg["og_description"]}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="The Data Compliance Builders">

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{cfg["og_title"]}">
<meta name="twitter:description" content="{cfg["og_description"]}">

<!-- Icons -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{FAVICON_SVG_B64}">
<link rel="apple-touch-icon" href="data:image/svg+xml;base64,{FAVICON_SVG_B64}">

<!-- Stylesheet -->
<link rel="stylesheet" href="/assets/css/main.css">

<!-- JSON-LD -->
{head_jsonld}
<script type="application/ld+json">
{json.dumps(site_jsonld, ensure_ascii=False, indent=2)}
</script>

<!-- Plausible Analytics (cookieless, EU-hosted) -->
<script defer data-domain="dcbs.nl" src="https://plausible.io/js/script.js"></script>
</head>
<body>"""

    nav_html = build_nav(lang)
    footer_html = build_footer(lang)
    cookie_html = build_cookie_banner(lang)

    body = f"""{nav_html}

<main id="news-content" style="padding-top:72px">
{body_html}
</main>

{admin_modal}

{cookie_html}

<script src="/assets/js/main.js" defer></script>
{extra_script_tags}
</body>
</html>
"""
    return head + "\n" + body


# ─────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    for cfg in PAGES:
        url = cfg["url"]
        # Bepaal output-pad
        # / → /index.html, /over-ons/ → /over-ons/index.html, enz.
        rel = url.strip("/")
        if rel == "":
            outpath = ROOT / "index.html"
        else:
            outpath = ROOT / rel / "index.html"
        outpath.parent.mkdir(parents=True, exist_ok=True)
        html = build_page(cfg)
        outpath.write_text(html, encoding="utf-8")
        size_kb = outpath.stat().st_size / 1024
        print(f"  WROTE {url:35s} -> {outpath.relative_to(ROOT)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
