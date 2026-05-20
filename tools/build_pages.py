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
    # Articles (NL slug == EN slug, prefix /en/)
    "/nieuws/vodafone-boete-45-miljoen/":              "/en/nieuws/vodafone-boete-45-miljoen/",
    "/nieuws/fria-fundamental-rights-impact-assessment/": "/en/nieuws/fria-fundamental-rights-impact-assessment/",
    "/nieuws/ai-literacy-verplichting/":               "/en/nieuws/ai-literacy-verplichting/",
    "/nieuws/claude-ai-governance-discipline/":        "/en/nieuws/claude-ai-governance-discipline/",
    "/nieuws/risicos-generatieve-ai/":                 "/en/nieuws/risicos-generatieve-ai/",
    "/nieuws/tesla-robotaxi-privacy/":                 "/en/nieuws/tesla-robotaxi-privacy/",
    "/nieuws/zeven-jaar-avg-handhaving-nederland/":    "/en/nieuws/zeven-jaar-avg-handhaving-nederland/",
    "/nieuws/ai2027-superintelligente-ai/":            "/en/nieuws/ai2027-superintelligente-ai/",
    "/nieuws/bc-5701-privacy-keurmerk/":               "/en/nieuws/bc-5701-privacy-keurmerk/",
    # Service landing pages (phase 4)
    "/diensten/dpo-as-a-service/":                     "/en/diensten/dpo-as-a-service/",
    "/diensten/avg-compliance/":                       "/en/diensten/gdpr-compliance/",
    "/diensten/ai-act-compliance/":                    "/en/diensten/ai-act-compliance/",
    "/diensten/data-management/":                      "/en/diensten/data-management/",
}

# ─────────────────────────────────────────────────────────────────────
#  ARTICLE CONFIG
# ─────────────────────────────────────────────────────────────────────
# Eén entry per artikel. NL pagina toont volledige template-body.
# EN-stub: kort EN-samenvattings-blok + disclaimer + volledige NL-body.

ARTICLES = [
    {
        "key": "art-vodafone",
        "slug": "vodafone-boete-45-miljoen",
        "nl_title": "Recordboete Vodafone Duitsland: €45 miljoen — lessen voor uw compliance-programma | DCBS",
        "nl_desc": "Vodafone Duitsland kreeg een AVG-boete van €45 miljoen. Wat ging er mis met bewaarplichten, technische maatregelen en datalekafhandeling? Lessen voor uw compliance-programma.",
        "nl_keywords": "Vodafone AVG boete, GDPR boete Duitsland, AVG handhaving, bewaartermijn schending, datalek afhandeling, AVG technische maatregelen",
        "en_title": "Vodafone Germany Record Fine: €45 Million — Compliance Lessons | DCBS",
        "en_desc": "Vodafone Germany received a €45 million GDPR fine. Lessons on retention obligations, technical measures and breach handling for your compliance programme.",
        "en_keywords": "Vodafone GDPR fine, GDPR fine Germany, GDPR enforcement, data retention violation, breach handling, GDPR technical measures",
        "en_summary": (
            "<p>The German supervisory authority fined Vodafone Germany €45 million — one of the largest "
            "GDPR penalties in Germany's enforcement history. The case combined breaches of retention "
            "obligations, insufficient technical measures and a failing complaints-handling process.</p>"
            "<p>This article unpacks what went wrong and translates the findings into concrete actions "
            "for your own compliance programme: how to evidence retention discipline, what 'state of the "
            "art' technical measures actually look like in audits, and why complaints handling is now a "
            "front-line enforcement target.</p>"
        ),
    },
    {
        "key": "art-fria",
        "slug": "fria-fundamental-rights-impact-assessment",
        "nl_title": "AI & Grondrechten: een gestructureerde aanpak onder de EU AI Act | DCBS",
        "nl_desc": "De EU AI Act vereist Fundamental Rights Impact Assessments (FRIA) voor bepaalde hoog-risico AI-systemen. DCBS legt het framework uit en hoe u het uitvoert.",
        "nl_keywords": "FRIA EU AI Act, Fundamental Rights Impact Assessment, AI grondrechten, hoog-risico AI, AI Act impactbeoordeling",
        "en_title": "AI & Fundamental Rights: A Structured FRIA Approach Under the EU AI Act | DCBS",
        "en_desc": "The EU AI Act requires Fundamental Rights Impact Assessments (FRIA) for certain high-risk AI systems. DCBS explains the framework and how to execute it.",
        "en_keywords": "FRIA EU AI Act, Fundamental Rights Impact Assessment, AI fundamental rights, high-risk AI, AI Act impact assessment",
        "en_summary": (
            "<p>The EU AI Act introduces a new instrument for high-risk AI systems: the Fundamental "
            "Rights Impact Assessment (FRIA). Unlike a traditional DPIA, the FRIA reaches beyond data "
            "protection into discrimination, autonomy, dignity and access to public services.</p>"
            "<p>This article presents a structured FRIA approach: who needs one, what the methodology "
            "looks like in practice, and how to integrate it with existing DPIA and risk management "
            "processes so that you build one defensible record instead of three parallel ones.</p>"
        ),
    },
    {
        "key": "art-ailliteracy",
        "slug": "ai-literacy-verplichting",
        "nl_title": "AI-geletterdheid en verboden AI-praktijken onder de EU AI Act | DCBS",
        "nl_desc": "De EU AI Act introduceert een AI-geletterdheidsplicht én een lijst verboden praktijken. Wat betekent dit voor uw organisatie? DCBS legt het uit.",
        "nl_keywords": "AI geletterdheid EU AI Act, AI literacy plicht, verboden AI praktijken, AI Act artikel 4, AI training medewerkers",
        "en_title": "AI Literacy Obligation and Prohibited AI Practices Under the EU AI Act | DCBS",
        "en_desc": "The EU AI Act introduces both an AI literacy obligation and a list of prohibited practices. What this means for your organisation — explained by DCBS.",
        "en_keywords": "AI literacy EU AI Act, AI literacy obligation, prohibited AI practices, AI Act Article 4, AI staff training",
        "en_summary": (
            "<p>The EU AI Act introduces two distinct but related obligations: an AI literacy duty "
            "(Article 4) that applies to virtually every organisation deploying AI, and a list of "
            "outright prohibited practices that took effect early in the rollout schedule.</p>"
            "<p>This article unpacks both: what 'sufficient AI literacy' means for your workforce, how "
            "to evidence it during inspections, and which practices — from social scoring to certain "
            "emotion-recognition use cases — are now off-limits regardless of consent.</p>"
        ),
    },
    {
        "key": "art-claude",
        "slug": "claude-ai-governance-discipline",
        "nl_title": "Wanneer Claude brutaal wordt: AI-nieuwsgierigheid en governance-discipline | DCBS",
        "nl_desc": "Een onverwachte interactie met Claude toont waarom AI-managementsystemen onmisbaar zijn. DCBS over governance, ISO 42001 en het beheersen van onvoorspelbaar AI-gedrag.",
        "nl_keywords": "AI governance, ISO 42001, Claude AI incident, AI managementsysteem, onvoorspelbaar AI gedrag, AI compliance",
        "en_title": "When Claude Gets Cheeky: Turning AI Curiosity Into Governance Discipline | DCBS",
        "en_desc": "An unexpected Claude interaction shows why AI management systems are indispensable. DCBS on governance, ISO 42001 and managing unpredictable AI behaviour.",
        "en_keywords": "AI governance, ISO 42001, Claude AI incident, AI management system, unpredictable AI behaviour, AI compliance",
        "en_summary": (
            "<p>An unexpected interaction with Claude reveals something fundamental about AI governance: "
            "unpredictable behaviour is exactly why management systems are indispensable. A single "
            "surprising response is not a scandal — but the absence of a process to log, triage and "
            "learn from it is.</p>"
            "<p>This article uses one concrete incident to illustrate why ISO 42001 and lightweight "
            "internal-incident workflows belong in every organisation that deploys generative AI, even "
            "(and especially) those that are not classified as high-risk under the AI Act.</p>"
        ),
    },
    {
        "key": "art-genai",
        "slug": "risicos-generatieve-ai",
        "nl_title": "De Risico's van Generatieve AI: Wat Uw Organisatie Moet Weten | DCBS",
        "nl_desc": "Generatieve AI brengt juridische, privacy- en operationele risico's. DCBS zet de belangrijkste risico-categorieën en mitigerende maatregelen op een rij.",
        "nl_keywords": "generatieve AI risico's, GenAI compliance, ChatGPT risico organisatie, AI risico mitigatie, GenAI privacy",
        "en_title": "The Risks of Generative AI: What Your Organisation Needs to Know | DCBS",
        "en_desc": "Generative AI introduces legal, privacy and operational risks. DCBS sets out the main risk categories and mitigations for your organisation.",
        "en_keywords": "generative AI risks, GenAI compliance, ChatGPT organisational risk, AI risk mitigation, GenAI privacy",
        "en_summary": (
            "<p>Generative AI is proliferating across the workplace, often faster than governance "
            "frameworks can keep up. This article maps the legal, privacy and operational risks "
            "your organisation now faces — from input-side data leakage and IP concerns to "
            "output-side hallucinations and discriminatory outcomes.</p>"
            "<p>For each risk category we propose a proportionate response: contractual, technical "
            "and process-level controls that protect the organisation without freezing innovation. "
            "The goal is not 'no GenAI', but defensible GenAI.</p>"
        ),
    },
    {
        "key": "art-tesla",
        "slug": "tesla-robotaxi-privacy",
        "nl_title": "Tesla Robotaxi Pilot — Privacy-Risico's van Autonome Voertuigen | DCBS",
        "nl_desc": "Tesla's Robotaxi pilot is van start. Wat doet de AVG met biometrische data, camera's en bystander-privacy in de openbare ruimte? DCBS analyseert.",
        "nl_keywords": "Tesla Robotaxi privacy, autonome voertuigen AVG, biometrische data openbare ruimte, robotaxi GDPR, autonome voertuigen privacy",
        "en_title": "Tesla Robotaxi Pilot Begins — But What About Your Privacy? | DCBS",
        "en_desc": "Tesla's Robotaxi pilot has started. What does the GDPR say about biometric data, cameras and bystander privacy in public space? DCBS analysis.",
        "en_keywords": "Tesla Robotaxi privacy, autonomous vehicles GDPR, biometric data public space, robotaxi GDPR, autonomous vehicle privacy",
        "en_summary": (
            "<p>Tesla's Robotaxi public pilot is now operational. Behind the engineering achievement "
            "sits a privacy question that scales with every vehicle on the road: autonomous "
            "vehicles continuously capture biometric and contextual data about people who never "
            "consented to being recorded.</p>"
            "<p>This article works through the GDPR analysis: legal basis for bystander recording, "
            "limits on biometric processing, retention and onward sharing, and the practical question "
            "of how (or whether) Article 6 and 9 can be reconciled with a moving sensor platform in "
            "European cities.</p>"
        ),
    },
    {
        "key": "art-gdpr7",
        "slug": "zeven-jaar-avg-handhaving-nederland",
        "nl_title": "Zeven Jaar AVG-Handhaving in Nederland: De Balans | DCBS",
        "nl_desc": "Zeven jaar AVG: wat heeft de Autoriteit Persoonsgegevens gedaan, welke sectoren zijn het hardst geraakt, en wat staat organisaties te wachten? DCBS-analyse.",
        "nl_keywords": "AVG handhaving Nederland, Autoriteit Persoonsgegevens boetes, AVG zeven jaar, GDPR enforcement Nederland, AP statistieken",
        "en_title": "Seven Years of GDPR Enforcement in the Netherlands: A Stocktake | DCBS",
        "en_desc": "Seven years of GDPR: what has the Dutch DPA done, which sectors took the hardest hits, and what is coming next? DCBS analysis.",
        "en_keywords": "GDPR enforcement Netherlands, Dutch DPA fines, GDPR seven years, AP enforcement statistics",
        "en_summary": (
            "<p>Seven years after the GDPR took effect on 25 May 2018, it is time for a stocktake. "
            "The Dutch Data Protection Authority (Autoriteit Persoonsgegevens) has shifted from "
            "guidance to active enforcement, and the pattern of fines now reveals clearly which "
            "sectors and which failures attract attention.</p>"
            "<p>This article reviews the headline enforcement actions, identifies the recurring "
            "compliance gaps that the AP has called out, and projects forward: what organisations "
            "should expect from supervisory priorities in the next enforcement cycle.</p>"
        ),
    },
    {
        "key": "art-ai2027",
        "slug": "ai2027-superintelligente-ai",
        "nl_title": "AI2027: Superintelligente AI Binnen Twee Jaar — Compliance-Implicaties | DCBS",
        "nl_desc": "Het AI2027-scenario schetst transformatieve AI binnen twee jaar. Ongeacht uw tijdlijn-overtuiging: de compliance-implicaties zijn aanzienlijk. DCBS-analyse.",
        "nl_keywords": "AI2027, superintelligente AI, AGI compliance, transformatieve AI compliance, AI Act voorbereiding, AI governance toekomst",
        "en_title": "AI2027: Superintelligent AI Within Two Years — Compliance Implications | DCBS",
        "en_desc": "The AI2027 scenario projects transformative AI within two years. Regardless of your timeline view, the compliance implications are significant. DCBS analysis.",
        "en_keywords": "AI2027, superintelligent AI, AGI compliance, transformative AI compliance, AI Act preparation, AI governance future",
        "en_summary": (
            "<p>The AI2027 scenario sketches a plausible path to transformative AI systems by 2027. "
            "Whether or not you find that timeline credible, the compliance implications are "
            "substantial and largely independent of the exact pace of development.</p>"
            "<p>This article isolates the parts of an AI governance posture that are robust under "
            "multiple scenarios: management systems that work for narrow AI today and scale to "
            "frontier AI tomorrow, contracting clauses that survive capability jumps, and the "
            "human-oversight controls that regulators will expect regardless of model size.</p>"
        ),
    },
    {
        "key": "art-bc5701",
        "slug": "bc-5701-privacy-keurmerk",
        "nl_title": "Waarom het BC 5701 Privacy Keurmerk Essentieel Is voor Gegevensverwerkers | DCBS",
        "nl_desc": "BC 5701 is de Nederlandse AVG-certificeringsstandaard, goedgekeurd door de Autoriteit Persoonsgegevens. DCBS legt uit waarom dit keurmerk de markstandaard wordt.",
        "nl_keywords": "BC 5701, BC 5701 keurmerk, AVG certificering Nederland, privacy keurmerk, BC 5701 implementatie, gegevensverwerker certificering",
        "en_title": "Why the BC 5701 Privacy Seal Is Essential for Data Processors | DCBS",
        "en_desc": "BC 5701 is the Dutch GDPR certification standard, approved by the Dutch DPA. DCBS explains why this seal is becoming the market standard.",
        "en_keywords": "BC 5701, BC 5701 seal, GDPR certification Netherlands, privacy seal, BC 5701 implementation, data processor certification",
        "en_summary": (
            "<p>The BC 5701 Privacy Seal has emerged as the market standard for trustworthy data "
            "processors in the Netherlands. It is the first Dutch GDPR certification standard "
            "formally approved by the Dutch Data Protection Authority under Article 42 GDPR.</p>"
            "<p>This article explains what BC 5701 actually evidences, why a growing number of "
            "controllers now ask processors to hold it, and what a realistic implementation path "
            "looks like — including how DCBS positions itself as an implementation partner "
            "(certification itself is performed by Brand Compliance).</p>"
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────
#  SERVICE PAGES (Phase 4)
# ─────────────────────────────────────────────────────────────────────
# Vier nieuwe dienst-landingspagina's. Body wordt als raw HTML doorgegeven
# (geen P[key] template; geschreven direct in deze file). Visual identity
# blijft consistent: hergebruikt .ph/.sec/.svc-grid/.sc-card classes uit
# bestaande /diensten/ pagina.

SERVICE_PAGES_DATA = [
    # ── 1. DPO as a Service ──────────────────────────────────────────
    {
        "slug": "dpo-as-a-service",
        "nl_slug_path": "/diensten/dpo-as-a-service/",
        "en_slug_path": "/en/diensten/dpo-as-a-service/",
        "nl_title": "Externe DPO en Interim Functionaris Gegevensbescherming | DCBS Utrecht",
        "nl_desc": "Externe DPO of interim Functionaris Gegevensbescherming nodig? DCBS levert ervaren privacy officers voor mkb, corporates en (semi-)publieke organisaties. Pragmatisch, onafhankelijk, aantoonbaar compliant.",
        "nl_keywords": "externe DPO, interim DPO, externe Functionaris Gegevensbescherming, DPO as a service, FG inhuren, privacy officer extern, DPO uitbesteden mkb, interim functionaris gegevensbescherming",
        "en_title": "External DPO and Interim Data Protection Officer | DCBS Netherlands",
        "en_desc": "External DPO or interim Data Protection Officer needed? DCBS delivers experienced privacy officers for SMEs, corporates and public sector organisations in the Netherlands. Pragmatic, independent, demonstrably compliant.",
        "en_keywords": "external DPO, interim DPO, external Data Protection Officer, DPO as a service, hire a DPO, external privacy officer, outsource DPO SME, interim Data Protection Officer",
        "service_type_nl": "DPO as a Service",
        "service_type_en": "DPO as a Service",
    },
    # ── 2. AVG / GDPR Compliance ─────────────────────────────────────
    {
        "slug": "avg-compliance",
        "nl_slug_path": "/diensten/avg-compliance/",
        "en_slug_path": "/en/diensten/gdpr-compliance/",
        "nl_title": "AVG Compliance, DPIA's en BC 5701 Certificering | DCBS",
        "nl_desc": "AVG-audits, DPIA's, verwerkingsregisters, datalekprocedures en BC 5701-certificeringstrajecten. DCBS bouwt aantoonbare AVG-compliance — niet alleen op papier, ook in de praktijk.",
        "nl_keywords": "AVG consultancy, AVG advies bedrijf, privacy compliance advies, privacy audit, DPIA uitvoeren, DPIA privacy impact assessment, datalek meldprocedure, verwerkingsregister opstellen, privacybeleid opstellen, Autoriteit Persoonsgegevens advies, BC 5701 certificering, BC 5701 implementatie, BC 5701 gap analyse",
        "en_title": "GDPR Compliance, DPIAs and BC 5701 Certification | DCBS Netherlands",
        "en_desc": "GDPR audits, DPIAs, processing records, breach procedures and BC 5701 certification trajectories. DCBS builds demonstrable GDPR compliance — not just on paper, but in practice.",
        "en_keywords": "GDPR consultancy, GDPR advice, privacy compliance advice, privacy audit, DPIA execution, Data Protection Impact Assessment, breach procedure, processing records, privacy policy, Dutch DPA advice, BC 5701 certification, BC 5701 implementation, BC 5701 gap analysis",
        "service_type_nl": "AVG / GDPR Compliance",
        "service_type_en": "GDPR Compliance",
    },
    # ── 3. EU AI Act Compliance ──────────────────────────────────────
    {
        "slug": "ai-act-compliance",
        "nl_slug_path": "/diensten/ai-act-compliance/",
        "en_slug_path": "/en/diensten/ai-act-compliance/",
        "nl_title": "EU AI Act Compliance en AI Governance | DCBS",
        "nl_desc": "Bereid uw organisatie voor op de EU AI Act. Risicoclassificatie van AI-systemen, AI governance frameworks, FRIA-impactbeoordelingen en ISO 42001-implementatie. Praktisch en juridisch onderbouwd.",
        "nl_keywords": "EU AI Act consultancy, EU AI Act naleving, AI Act advies, AI compliance advies, AI governance framework, risicoclassificatie AI systeem, impactbeoordeling AI hoog risico, FRIA fundamental rights AI, ISO 42001 AI managementsysteem, ISO 42001 implementatie, AI Act high-risk classificatie",
        "en_title": "EU AI Act Compliance and AI Governance | DCBS Netherlands",
        "en_desc": "Prepare your organisation for the EU AI Act. AI system risk classification, AI governance frameworks, FRIA impact assessments and ISO 42001 implementation. Practical and legally grounded.",
        "en_keywords": "EU AI Act consultancy, EU AI Act compliance, AI Act advice, AI compliance advice, AI governance framework, AI system risk classification, high-risk AI impact assessment, FRIA fundamental rights AI, ISO 42001 AI management system, ISO 42001 implementation, AI Act high-risk classification",
        "service_type_nl": "EU AI Act Compliance",
        "service_type_en": "EU AI Act Compliance",
    },
    # ── 4. Data Management ───────────────────────────────────────────
    {
        "slug": "data-management",
        "nl_slug_path": "/diensten/data-management/",
        "en_slug_path": "/en/diensten/data-management/",
        "nl_title": "Data Management en Data Governance | DCBS",
        "nl_desc": "Data governance frameworks, datavolwassenheidsassessments en data quality management. DCBS bouwt structuur in uw data-organisatie volgens DAMA-DMBOK en sluit aan op AVG- en AI-compliance.",
        "nl_keywords": "data management consultancy, data governance advies, data governance framework, datavolwassenheid assessment, data maturity assessment, data quality management, DAMA DMBOK implementatie, data strategie advies, master data management consultant",
        "en_title": "Data Management and Data Governance | DCBS Netherlands",
        "en_desc": "Data governance frameworks, data maturity assessments and data quality management. DCBS structures your data organisation along DAMA-DMBOK and aligns with GDPR and AI compliance.",
        "en_keywords": "data management consultancy, data governance advice, data governance framework, data maturity assessment, data quality management, DAMA DMBOK implementation, data strategy advice, master data management consultant",
        "service_type_nl": "Data Management",
        "service_type_en": "Data Management",
    },
]


def service_body_dpo_nl() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/diensten/" style="color:var(--mu);text-decoration:none">Diensten</a> / Externe DPO</p>
  <h2>Externe DPO en Interim <span class="g">Functionaris Gegevensbescherming</span></h2>
  <p class="sub">Een onafhankelijke DPO die uw organisatie kent &mdash; direct operationeel, zonder consultancy-trechter. Voor mkb, corporates en (semi-)publieke organisaties.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">Een Functionaris Gegevensbescherming (FG) &mdash; ook wel Data Protection Officer (DPO) &mdash; is voor veel organisaties wettelijk verplicht onder de AVG. Maar de functie intern beleggen is vaak duur en de juiste expertise is schaars. DCBS levert een <strong>externe DPO</strong> of <strong>interim FG</strong> die direct operationeel inzetbaar is, met ervaring bij toezichthouders, gemeentes, nutsbedrijven en private organisaties.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">Een externe DPO van DCBS werkt vanuit volledige onafhankelijkheid, zoals de AVG voorschrijft. Geen consultancy-trechter met juniors, maar &eacute;&eacute;n vast aanspreekpunt dat uw organisatie kent &mdash; en blijft kennen, ook als de samenstelling van uw team verandert.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; Wat het inhoudt</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">Wat een <span class="g">externe DPO</span> levert</h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Volwaardige FG-vervulling: signalerend, adviserend, toezichthoudend &mdash; en als enige escalatiepad naar de Autoriteit Persoonsgegevens. Schaalbaar van enkele uren per maand tot vaste aanwezigheid.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" style="cursor:default"><div class="sct">DPO-vervulling met volledige onafhankelijkheid</div><p class="scb">Externe DPO-rol conform AVG artikel 38: onafhankelijk, niet ge&iuml;nstrueerd door management, met directe escalatielijn naar de hoogste leiding van uw organisatie.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Interim FG bij overbrugging</div><p class="scb">Interim functionaris gegevensbescherming tijdens werving, langdurige afwezigheid of reorganisatie. Direct inzetbaar, zonder onboarding-traject van drie maanden.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Privacy officer extern voor signalering</div><p class="scb">Wekelijkse aanwezigheid voor advies aan project- en lijnmanagers, review van nieuwe verwerkingen, monitoring van datalekafhandeling en beoordeling van DPIA-uitkomsten.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">DPO uitbesteden mkb &mdash; flexibel</div><p class="scb">Van &eacute;&eacute;n dagdeel per maand tot drie dagen per week. Voor mkb-organisaties die wel verplicht zijn een DPO te benoemen, maar nog niet de schaal hebben voor een fulltime functie.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Kennisdeling en escalatielijn AP</div><p class="scb">Doorlopende kennisoverdracht aan uw interne privacyteam. Vast contactpunt voor de Autoriteit Persoonsgegevens bij vragen, klachten of inspecties.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; Wanneer DCBS voor u relevant is</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Wettelijke DPO-plicht niet ingevuld</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">U bent een (semi-)publieke organisatie of een bedrijf dat structureel grootschalige verwerkingen of bijzondere categorie&euml;n verwerkt. Een DPO is verplicht onder AVG artikel 37, maar nog niet aangesteld &mdash; of de aanstelling voldoet niet aan de onafhankelijkheidsvereiste.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Overdracht na vertrek FG</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Uw FG vertrekt en de werving van een opvolger duurt drie tot zes maanden. In de tussentijd moet de DPO-functie operationeel blijven: verwerkingsregister bijgehouden, DPIA-reviews uitgevoerd, datalekafhandeling onveranderd.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Capaciteitspiek of complex traject</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Uw interne FG heeft te maken met een uitzonderlijke piek: implementatie van een nieuw kernsysteem, AI-rollout, AVG-handhavingstraject door de AP, of een complex datalek met bestuurlijke impact. Externe versterking voor specifieke fase.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start">
    <div>
      <span class="ew">03 &mdash; Wat u krijgt</span>
      <h2 class="sh" style="margin-top:.8rem">Concrete <span class="g">deliverables</span></h2>
      <ul style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem">
        <li style="margin-bottom:.6rem">Operationeel inzetbare DPO of FG binnen vijf werkdagen</li>
        <li style="margin-bottom:.6rem">&Eacute;&eacute;n vast aanspreekpunt &mdash; geen wisselende juniors</li>
        <li style="margin-bottom:.6rem">Jaarplan met prioriteiten en kwartaalrapportages aan directie</li>
        <li style="margin-bottom:.6rem">Verwerkingsregister bijgehouden, datalekprotocol getest, DPIA-overzicht actueel</li>
        <li style="margin-bottom:.6rem">Adviesnotities en escalatielijn richting Autoriteit Persoonsgegevens</li>
        <li>Vaste maandprijs &mdash; geen verrassende uurtjes-factuurtjes</li>
      </ul>
    </div>
    <div>
      <span class="ew">04 &mdash; Werkwijze</span>
      <h2 class="sh" style="margin-top:.8rem">Vier <span class="g">stappen</span></h2>
      <ol style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem;list-style:decimal">
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Intake &amp; nulmeting</strong> &mdash; gesprek met opdrachtgever en huidige privacy-stakeholders. Beoordeling van de stand van verwerkingsregister, DPIA-archief, datalekprocedure en lopende AP-zaken.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Onboarding &amp; overdracht</strong> &mdash; toegang tot relevante systemen, kennismaking met sleutelpersonen, formalisering van de DPO-aanstelling en aanmelding bij de Autoriteit Persoonsgegevens.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Operationele DPO-fase</strong> &mdash; vaste werkritme: wekelijkse aanwezigheid, maandelijkse rapportage aan directie, kwartaalreview van risico's. Direct escaleerbaar bij incidenten.</li>
        <li><strong style="color:var(--wh)">Rapportage &amp; doorontwikkeling</strong> &mdash; jaarrapportage aan directie en RvT. Doorlopende verbetering van privacy-managementsysteem; afbouw of opvolging bij interne aanstelling.</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">05 &mdash; Voor wie</span>
  <h2 class="sh" style="margin-top:.8rem">Sectoren waar DCBS <span class="g">DPO-rollen vervult</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS werkt voor toezichthouders, gemeentes, nutsbedrijven, verzekeraars en private organisaties. Voor concrete praktijkvoorbeelden &mdash; bekijk <a href="/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">onze cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Externe DPO inzetten?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Gratis kennismakingsgesprek van 30 minuten. In het gesprek wordt beoordeeld of er een match is, en zo ja, hoe een externe DPO of interim FG-traject er voor uw organisatie uit zou kunnen zien.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Plan kennismaking &rarr;</a>
      <a href="/contact/" class="btn bg">Contact via formulier</a>
    </div>
  </div>
</section>"""


def service_body_dpo_en() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/en/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/en/diensten/" style="color:var(--mu);text-decoration:none">Services</a> / External DPO</p>
  <h2>External DPO and Interim <span class="g">Data Protection Officer</span></h2>
  <p class="sub">An independent DPO who actually knows your organisation &mdash; operational from day one, no consultancy funnel. For SMEs, corporates and public sector organisations.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">A Data Protection Officer (DPO) &mdash; in Dutch &lsquo;Functionaris Gegevensbescherming&rsquo; or FG &mdash; is legally required under the GDPR for many organisations. Filling the role internally is often expensive, and the right expertise is scarce. DCBS delivers an <strong>external DPO</strong> or <strong>interim Data Protection Officer</strong> who is operational from day one, with experience at supervisory authorities, municipalities, utilities and private organisations.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">An external DPO from DCBS operates with the full independence the GDPR requires. No consultancy funnel staffed with juniors, but a single point of contact who actually learns your organisation &mdash; and stays with you, even when your internal team changes.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; What it covers</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">What an <span class="g">external DPO</span> delivers</h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Full DPO function: signalling, advising, supervising &mdash; with a direct escalation route to the Dutch Data Protection Authority. Scalable from a few hours per month to a continuous presence.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" style="cursor:default"><div class="sct">DPO role with full independence</div><p class="scb">External DPO under GDPR Article 38: independent, not instructed by management, with a direct escalation line to the highest level of your organisation.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Interim DPO for bridging</div><p class="scb">Interim Data Protection Officer during recruitment, prolonged absence or reorganisation. Operational immediately, no three-month onboarding.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">External privacy officer for signalling</div><p class="scb">Weekly presence advising project and line managers, reviewing new processing activities, monitoring breach handling and assessing DPIA outcomes.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Outsource DPO for SMEs &mdash; flexible</div><p class="scb">From one half-day per month to three days per week. For SMEs that are legally required to appoint a DPO but don't yet have the scale for a full-time role.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Knowledge sharing &amp; supervisory contact</div><p class="scb">Continuous knowledge transfer to your internal privacy team. Permanent contact point for the Dutch DPA on inquiries, complaints or inspections.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; When DCBS is relevant to you</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Statutory DPO requirement unmet</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">You are a public sector organisation or a company that structurally processes data at scale or processes special categories. A DPO is required under GDPR Article 37 but has not yet been appointed &mdash; or the existing appointment does not meet the independence requirement.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Handover after DPO departure</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Your DPO is leaving and recruiting a successor takes three to six months. In the interim the DPO function must remain operational: processing records maintained, DPIA reviews completed, breach handling uninterrupted.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Capacity peak or complex programme</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Your internal DPO faces an exceptional peak: implementation of a new core system, AI rollout, GDPR enforcement track by the supervisory authority, or a complex breach with board-level impact. External reinforcement for a defined phase.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start">
    <div>
      <span class="ew">03 &mdash; What you get</span>
      <h2 class="sh" style="margin-top:.8rem">Concrete <span class="g">deliverables</span></h2>
      <ul style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem">
        <li style="margin-bottom:.6rem">Operational DPO or interim DPO within five working days</li>
        <li style="margin-bottom:.6rem">One permanent point of contact &mdash; no rotating juniors</li>
        <li style="margin-bottom:.6rem">Annual plan with priorities and quarterly board reports</li>
        <li style="margin-bottom:.6rem">Processing records maintained, breach protocol tested, DPIA register current</li>
        <li style="margin-bottom:.6rem">Advisory notes and escalation route to the supervisory authority</li>
        <li>Fixed monthly fee &mdash; no surprise hourly invoices</li>
      </ul>
    </div>
    <div>
      <span class="ew">04 &mdash; Approach</span>
      <h2 class="sh" style="margin-top:.8rem">Four <span class="g">steps</span></h2>
      <ol style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem;list-style:decimal">
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Intake &amp; baseline</strong> &mdash; conversation with the client and current privacy stakeholders. Assessment of processing records, DPIA archive, breach procedure and any pending supervisory matters.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Onboarding &amp; handover</strong> &mdash; access to relevant systems, introductions to key people, formalisation of the DPO appointment and registration with the Dutch DPA.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Operational DPO phase</strong> &mdash; fixed rhythm: weekly presence, monthly board reporting, quarterly risk review. Direct escalation in case of incidents.</li>
        <li><strong style="color:var(--wh)">Reporting &amp; continuous improvement</strong> &mdash; annual report to board and supervisory board. Ongoing improvement of the privacy management system; phase-out or handover on internal appointment.</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">05 &mdash; For whom</span>
  <h2 class="sh" style="margin-top:.8rem">Sectors where DCBS <span class="g">fills DPO roles</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS works for regulators, municipalities, utilities, insurers and private organisations. For specific case examples &mdash; see <a href="/en/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">our cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Engage an external DPO?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Free 30-minute intake call. The conversation assesses whether there is a match and, if so, what an external DPO or interim DPO engagement could look like for your organisation.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Book intake &rarr;</a>
      <a href="/en/contact/" class="btn bg">Contact via form</a>
    </div>
  </div>
</section>"""


def service_body_avg_nl() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/diensten/" style="color:var(--mu);text-decoration:none">Diensten</a> / AVG Compliance</p>
  <h2>AVG Compliance, DPIA's en <span class="g">BC 5701 Certificering</span></h2>
  <p class="sub">Aantoonbare AVG-compliance &mdash; niet alleen op papier, ook in de praktijk. Audits, DPIA's, verwerkingsregisters, datalekprocedures en BC 5701-trajecten.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">De AVG werkt pas wanneer beleid, processen en techniek samen sluiten. Een verwerkingsregister dat niet aansluit op werkelijke verwerkingen, een datalekprotocol dat alleen op papier bestaat, of een DPIA-archief zonder follow-up &mdash; dat zijn de bevindingen waarmee de Autoriteit Persoonsgegevens een handhavingstraject opent.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">DCBS bouwt aan privacy-managementsystemen die werken in de praktijk: documentatie die klopt met operatie, controles die daadwerkelijk worden uitgevoerd, en bewijslast die overeind blijft tijdens een inspectie.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; Wat het inhoudt</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">AVG-bouwstenen <span class="g">in samenhang</span></h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Vijf onderdelen die elkaar versterken: DPIA, datalekbeheer, verwerkingsregister, BC 5701-certificering en privacy audits. Geen losse projecten, maar een samenhangend managementsysteem.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" id="dpia" style="cursor:default"><div class="sct">DPIA uitvoeren</div><p class="scb">Data Protection Impact Assessment (privacy impact assessment) voor hoog-risico verwerkingen: nieuwe AI-toepassingen, biometrie, profiling, grootschalige monitoring. Methodisch onderbouwd, met concrete mitigerende maatregelen en een toetsbaar restrisico-oordeel.</p></div>
      <div class="sc" id="datalek" style="cursor:default"><div class="sct">Datalek meldprocedure en afhandeling</div><p class="scb">Datalek meldprocedure die de 72-uurs termijn van AVG art. 33 haalbaar maakt: triagepad, beslisbomen voor wel/niet melden, vaste rolverdeling tussen FG, juridisch en business. Inclusief tabletop-oefening om de procedure te testen.</p></div>
      <div class="sc" id="verwerkingsregister" style="cursor:default"><div class="sct">Verwerkingsregister opstellen</div><p class="scb">Verwerkingsregister opstellen volgens AVG art. 30 dat actueel blijft: gekoppeld aan business-processen, met een vaste cyclus voor bijwerken en review. Geen Excel-document dat na vier maanden achterhaald is.</p></div>
      <div class="sc" id="bc-5701" style="cursor:default"><div class="sct">BC 5701 implementatie en gap-analyse</div><p class="scb">Implementatiepartner voor het BC 5701 Privacy Keurmerk &mdash; de eerste Nederlandse AVG-certificeringsstandaard, ontwikkeld door Brand Compliance en goedgekeurd door de Autoriteit Persoonsgegevens onder AVG art. 42. DCBS begeleidt het traject; de certificering zelf wordt uitgevoerd door Brand Compliance.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Privacy audit en privacybeleid</div><p class="scb">Onafhankelijke privacy audit van bestaande processen, beleid en documentatie. Privacybeleid opstellen of herzien zodat het aansluit op de werkelijke verwerkingen &mdash; en stand houdt bij toetsing.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; Wanneer DCBS voor u relevant is</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Nieuwe hoog-risico verwerking</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Een nieuwe verwerking (AI-systeem, biometrie, profiling, grootschalige monitoring) staat in de pijplijn en vereist een DPIA voor go-live. De interne capaciteit ontbreekt of de methodiek is niet eerder toegepast in dit type traject.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">AVG-handhavingstraject of audit</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">De Autoriteit Persoonsgegevens heeft een informatieverzoek gestuurd, een klacht is in behandeling, of een interne audit toonde gaten in beleid en documentatie. Snel een verdedigbare bewijslast nodig.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Marktvraag om BC 5701-keurmerk</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Opdrachtgevers vragen om een aantoonbare AVG-certificering bij aanbestedingen of leveranciersaudits. BC 5701 is daar de Nederlandse marktstandaard voor &mdash; alleen de implementatie ontbreekt.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start">
    <div>
      <span class="ew">03 &mdash; Wat u krijgt</span>
      <h2 class="sh" style="margin-top:.8rem">Concrete <span class="g">deliverables</span></h2>
      <ul style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem">
        <li style="margin-bottom:.6rem">DPIA-rapport met methodische onderbouwing en restrisico-oordeel</li>
        <li style="margin-bottom:.6rem">Datalek meldprocedure inclusief tabletop-test en draaiboek</li>
        <li style="margin-bottom:.6rem">Verwerkingsregister gekoppeld aan business-processen, met onderhoudscyclus</li>
        <li style="margin-bottom:.6rem">BC 5701 gap-analyse + implementatieplan + audit-readiness</li>
        <li style="margin-bottom:.6rem">Privacybeleid opgesteld of herzien en intern goedgekeurd</li>
        <li>Adviesnotities voor specifieke AP-vragen of -inspecties</li>
      </ul>
    </div>
    <div>
      <span class="ew">04 &mdash; Werkwijze</span>
      <h2 class="sh" style="margin-top:.8rem">Vier <span class="g">stappen</span></h2>
      <ol style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem;list-style:decimal">
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Nulmeting &amp; scope</strong> &mdash; gesprek met opdrachtgever, juridisch en privacy-eigenaren. Bepalen welk onderdeel (DPIA, datalek, register, BC 5701) als eerste opgepakt wordt.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Inventarisatie &amp; analyse</strong> &mdash; bestaande documentatie, processen en techniek doorlichten. Gat tussen huidige situatie en AVG-vereisten in kaart brengen, met prioritering op risico.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Implementatie &amp; vastlegging</strong> &mdash; documentatie wordt gebouwd, processen worden ingericht en getest, sleutelfiguren krijgen training. Audit-trail blijft compleet.</li>
        <li><strong style="color:var(--wh)">Borging &amp; overdracht</strong> &mdash; jaarcyclus, review-momenten en eigenaarschap belegd intern. Opvolging bij toetsing of certificering.</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">05 &mdash; Voor wie</span>
  <h2 class="sh" style="margin-top:.8rem">Sectoren waar DCBS <span class="g">AVG-trajecten uitvoert</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS werkt voor toezichthouders, gemeentes, nutsbedrijven, verzekeraars, retail-organisaties en internationale productiebedrijven. Voor concrete praktijkvoorbeelden &mdash; bekijk <a href="/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">onze cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Aan de slag met AVG-compliance?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Gratis kennismakingsgesprek van 30 minuten. In het gesprek wordt verkend welk onderdeel het meeste oplevert &mdash; en welk traject voor uw organisatie haalbaar is.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Plan kennismaking &rarr;</a>
      <a href="/contact/" class="btn bg">Contact via formulier</a>
    </div>
  </div>
</section>"""


def service_body_avg_en() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/en/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/en/diensten/" style="color:var(--mu);text-decoration:none">Services</a> / GDPR Compliance</p>
  <h2>GDPR Compliance, DPIAs and <span class="g">BC 5701 Certification</span></h2>
  <p class="sub">Demonstrable GDPR compliance &mdash; not just on paper, but in practice. Audits, DPIAs, processing records, breach procedures and BC 5701 certification.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">The GDPR only works when policy, processes and technology line up. A processing record that doesn't match actual processing activities, a breach protocol that exists only on paper, or a DPIA archive without follow-up &mdash; these are the findings that open an enforcement track at the Dutch Data Protection Authority.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">DCBS builds privacy management systems that work in practice: documentation that matches operations, controls that are actually executed, and audit evidence that holds up during inspection.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; What it covers</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">GDPR building blocks <span class="g">in concert</span></h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Five components that reinforce each other: DPIA, breach management, processing records, BC 5701 certification and privacy audits. Not separate projects, but a coherent management system.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" id="dpia" style="cursor:default"><div class="sct">DPIA execution</div><p class="scb">Data Protection Impact Assessment for high-risk processing: new AI applications, biometrics, profiling, large-scale monitoring. Methodologically grounded, with concrete mitigations and a defensible residual-risk judgement.</p></div>
      <div class="sc" id="datalek" style="cursor:default"><div class="sct">Breach notification procedure and handling</div><p class="scb">A breach notification procedure that makes the 72-hour deadline of GDPR Art. 33 actually workable: triage path, decision trees for notify/no-notify, and clear role allocation between DPO, legal and business. Includes a tabletop exercise to test the procedure.</p></div>
      <div class="sc" id="verwerkingsregister" style="cursor:default"><div class="sct">Processing records (Art. 30)</div><p class="scb">A processing record under GDPR Art. 30 that stays current: linked to business processes, with a fixed cycle for updates and review. Not an Excel document that goes stale within four months.</p></div>
      <div class="sc" id="bc-5701" style="cursor:default"><div class="sct">BC 5701 implementation and gap analysis</div><p class="scb">Implementation partner for the BC 5701 Privacy Seal &mdash; the first Dutch GDPR certification standard, developed by Brand Compliance and approved by the Dutch DPA under GDPR Art. 42. DCBS guides the implementation track; the certification itself is performed by Brand Compliance.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Privacy audit and policy</div><p class="scb">Independent privacy audit of existing processes, policy and documentation. Privacy policy drafted or revised so that it actually matches the processing activities &mdash; and holds up under scrutiny.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; When DCBS is relevant to you</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">New high-risk processing activity</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">A new processing activity (AI system, biometrics, profiling, large-scale monitoring) is in the pipeline and requires a DPIA before go-live. Internal capacity is missing or the methodology has not been applied to this type of project before.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Supervisory enforcement or audit</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">The Dutch DPA has issued an information request, a complaint is in process, or an internal audit revealed gaps in policy and documentation. Defensible evidence needed quickly.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Market demand for BC 5701 seal</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Clients are asking for demonstrable GDPR certification in tenders and vendor audits. BC 5701 is the Dutch market standard for this &mdash; only the implementation is missing.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start">
    <div>
      <span class="ew">03 &mdash; What you get</span>
      <h2 class="sh" style="margin-top:.8rem">Concrete <span class="g">deliverables</span></h2>
      <ul style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem">
        <li style="margin-bottom:.6rem">DPIA report with methodological grounding and residual-risk judgement</li>
        <li style="margin-bottom:.6rem">Breach notification procedure including tabletop test and runbook</li>
        <li style="margin-bottom:.6rem">Processing record linked to business processes, with maintenance cycle</li>
        <li style="margin-bottom:.6rem">BC 5701 gap analysis + implementation plan + audit-readiness</li>
        <li style="margin-bottom:.6rem">Privacy policy drafted or revised and internally approved</li>
        <li>Advisory notes for specific supervisory inquiries or inspections</li>
      </ul>
    </div>
    <div>
      <span class="ew">04 &mdash; Approach</span>
      <h2 class="sh" style="margin-top:.8rem">Four <span class="g">steps</span></h2>
      <ol style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem;list-style:decimal">
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Baseline &amp; scope</strong> &mdash; conversation with the client, legal and privacy owners. Determining which component (DPIA, breach, record, BC 5701) is tackled first.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Inventory &amp; analysis</strong> &mdash; existing documentation, processes and technology reviewed. Gap between current state and GDPR requirements mapped, with prioritisation by risk.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Implementation &amp; documentation</strong> &mdash; documentation is built, processes are set up and tested, key staff receive training. Audit trail remains complete.</li>
        <li><strong style="color:var(--wh)">Embedding &amp; handover</strong> &mdash; annual cycle, review moments and ownership assigned internally. Follow-up on assessment or certification.</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">05 &mdash; For whom</span>
  <h2 class="sh" style="margin-top:.8rem">Sectors where DCBS <span class="g">runs GDPR engagements</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS works for regulators, municipalities, utilities, insurers, retail organisations and international manufacturers. For specific case examples &mdash; see <a href="/en/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">our cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Start a GDPR compliance track?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Free 30-minute intake call. The conversation explores which component delivers the most value &mdash; and what a realistic track for your organisation looks like.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Book intake &rarr;</a>
      <a href="/en/contact/" class="btn bg">Contact via form</a>
    </div>
  </div>
</section>"""


def service_body_aiact_nl() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/diensten/" style="color:var(--mu);text-decoration:none">Diensten</a> / EU AI Act</p>
  <h2>EU AI Act Compliance en <span class="g">AI Governance</span></h2>
  <p class="sub">Risicoclassificatie van AI-systemen, AI governance frameworks, FRIA-impactbeoordelingen en ISO 42001-implementatie. Praktisch en juridisch onderbouwd.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">De EU AI Act is van kracht en de eerste verplichtingen zijn al actief. Een AI-portfolio inventariseren, risico's classificeren, een AI governance framework neerzetten en &mdash; voor hoog-risico systemen &mdash; een Fundamental Rights Impact Assessment uitvoeren: dat is geen optioneel projectplan, maar de wettelijke realiteit voor organisaties die AI inzetten of leveren.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">DCBS combineert juridische analyse van de AI Act-tekst met operationele implementatie via ISO 42001 als managementsysteem. Inhoudelijke verdieping: bekijk het artikel over <a href="/nieuws/fria-fundamental-rights-impact-assessment/" style="color:var(--tl);text-decoration:none;font-weight:700">FRIA-uitvoering onder de EU AI Act</a>.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; Wat het inhoudt</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">AI Act <span class="g">in de praktijk</span></h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Vijf bouwstenen: risicoclassificatie, AI governance framework, FRIA, ISO 42001-managementsysteem en doorlopend AI compliance advies. Aansluitend op uw bestaande AVG- en data-governance structuur.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" style="cursor:default"><div class="sct">Risicoclassificatie AI-systeem</div><p class="scb">Systematische classificatie van AI-systemen onder AI Act: verboden, hoog-risico, beperkt risico of minimaal risico. Inclusief AI Act high-risk classificatie voor systemen in Annex III en GPAI-beoordeling voor general-purpose AI.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">AI governance framework opzetten</div><p class="scb">AI governance framework met beleid, rolverdeling (AI-owner, technische verantwoordelijke, FG), inventarisatieprocessen en escalatiepaden. Schaalbaar van &eacute;&eacute;n AI-systeem tot een portfolio van tientallen.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">FRIA: impactbeoordeling AI hoog risico</div><p class="scb">Fundamental Rights Impact Assessment voor hoog-risico AI-systemen: identificatie van getroffen grondrechten, risicobeoordeling, mitigaties en verantwoording. Conform AI Act art. 27.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">ISO 42001 implementatie</div><p class="scb">ISO 42001 AI-managementsysteem &mdash; het internationale managementsysteem voor verantwoorde AI. Implementatie aansluitend op ISO 27001 of bestaande management-cyclus. Audit-ready zonder dubbele documentatie-trajecten.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">AI compliance advies en monitoring</div><p class="scb">Doorlopend AI compliance advies bij nieuwe AI-implementaties: leveranciersbeoordeling, contractanalyse, gebruiks-impact en verantwoording naar toezicht. Inclusief voorbereiding op AI Act-handhaving.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; Wanneer DCBS voor u relevant is</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">AI-portfolio niet geclassificeerd</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Een groeiend aantal AI-systemen wordt ingezet in operatie, maar er is geen inventarisatie, geen risicoclassificatie en geen helder zicht op welke systemen onder welke AI Act-categorie vallen.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Hoog-risico AI-systeem voor go-live</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Een AI-systeem onder Annex III (kritieke infrastructuur, onderwijs, werkgelegenheid, toegang tot publieke diensten, rechtshandhaving) gaat live en vereist een FRIA + voldoen aan de hoog-risico verplichtingen v&oacute;&oacute;r marktintroductie.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">ISO 42001-traject overwogen</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Opdrachtgevers of de organisatie zelf willen een aantoonbaar AI-managementsysteem. ISO 42001-implementatie is de richting, maar er is hulp nodig bij de gap-analyse en aansluiting op bestaande ISO 27001-structuur.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start">
    <div>
      <span class="ew">03 &mdash; Wat u krijgt</span>
      <h2 class="sh" style="margin-top:.8rem">Concrete <span class="g">deliverables</span></h2>
      <ul style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem">
        <li style="margin-bottom:.6rem">AI-portfolio inventarisatie met risicoclassificatie per systeem</li>
        <li style="margin-bottom:.6rem">AI governance framework: beleid, rolverdeling, escalatiepaden</li>
        <li style="margin-bottom:.6rem">FRIA-rapport voor hoog-risico systemen, conform AI Act art. 27</li>
        <li style="margin-bottom:.6rem">ISO 42001 gap-analyse + implementatie-roadmap</li>
        <li style="margin-bottom:.6rem">Trainingsmateriaal AI-geletterdheid voor sleutelfunctionarissen</li>
        <li>Doorlopend adviespad bij nieuwe AI-implementaties</li>
      </ul>
    </div>
    <div>
      <span class="ew">04 &mdash; Werkwijze</span>
      <h2 class="sh" style="margin-top:.8rem">Vier <span class="g">stappen</span></h2>
      <ol style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem;list-style:decimal">
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Discovery &amp; portfolio-scan</strong> &mdash; AI-systemen in gebruik inventariseren, inclusief shadow-AI (productiviteitstools, embedded AI in SaaS). Eerste classificatie onder AI Act-categorie&euml;n.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Risicoclassificatie &amp; prioritering</strong> &mdash; per systeem een definitieve classificatie, met bijbehorende verplichtingen. Prioritering op basis van risico en go-live datum.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Implementatie governance &amp; FRIA's</strong> &mdash; governance framework opzetten, FRIA's uitvoeren voor hoog-risico systemen, ISO 42001-controles inrichten.</li>
        <li><strong style="color:var(--wh)">Borging &amp; AI-geletterdheid</strong> &mdash; doorlopende monitoring, AI-geletterdheidstraining voor relevante medewerkers, voorbereiding op AI Act-handhaving en eventuele audits.</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">05 &mdash; Voor wie</span>
  <h2 class="sh" style="margin-top:.8rem">Organisaties die <span class="g">AI inzetten of leveren</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS werkt voor organisaties met AI-systemen in productie of pijplijn: financi&euml;le instellingen, (semi-)publieke organisaties, kritieke infrastructuur en internationale corporates. AI-aanbieders en AI-deployers met verplichtingen onder de EU AI Act vinden hier de combinatie van juridische analyse en operationele implementatie. Voor concrete praktijkvoorbeelden &mdash; bekijk <a href="/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">onze cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">AI Act-compliance opzetten?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Gratis kennismakingsgesprek van 30 minuten. In het gesprek wordt verkend waar uw AI-portfolio staat onder de Act &mdash; en welke prioriteiten haalbaar zijn.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Plan kennismaking &rarr;</a>
      <a href="/contact/" class="btn bg">Contact via formulier</a>
    </div>
  </div>
</section>"""


def service_body_aiact_en() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/en/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/en/diensten/" style="color:var(--mu);text-decoration:none">Services</a> / EU AI Act</p>
  <h2>EU AI Act Compliance and <span class="g">AI Governance</span></h2>
  <p class="sub">AI system risk classification, AI governance frameworks, FRIA impact assessments and ISO 42001 implementation. Practical and legally grounded.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">The EU AI Act is in force and the first obligations are already active. Inventorying an AI portfolio, classifying risks, putting an AI governance framework in place and &mdash; for high-risk systems &mdash; running a Fundamental Rights Impact Assessment: this is no longer optional. It is the legal reality for organisations that deploy or supply AI.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">DCBS combines legal analysis of the AI Act text with operational implementation through ISO 42001 as a management system. For further reading: see the article on <a href="/en/nieuws/fria-fundamental-rights-impact-assessment/" style="color:var(--tl);text-decoration:none;font-weight:700">FRIA execution under the EU AI Act</a>.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; What it covers</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">AI Act <span class="g">in practice</span></h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Five building blocks: risk classification, AI governance framework, FRIA, ISO 42001 management system and ongoing AI compliance advice. Designed to align with your existing GDPR and data governance structure.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" style="cursor:default"><div class="sct">AI system risk classification</div><p class="scb">Systematic classification of AI systems under the AI Act: prohibited, high-risk, limited risk or minimal risk. Includes AI Act high-risk classification for Annex III systems and GPAI assessment for general-purpose AI.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">AI governance framework setup</div><p class="scb">AI governance framework with policy, role allocation (AI owner, technical lead, DPO), inventory processes and escalation paths. Scalable from one AI system to a portfolio of dozens.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">FRIA: high-risk AI impact assessment</div><p class="scb">Fundamental Rights Impact Assessment for high-risk AI systems: identification of affected fundamental rights, risk assessment, mitigations and accountability. In line with AI Act Article 27.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">ISO 42001 implementation</div><p class="scb">ISO 42001 AI management system &mdash; the international management system for responsible AI. Implementation that builds on ISO 27001 or existing management cycles. Audit-ready without duplicate documentation tracks.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">AI compliance advice and monitoring</div><p class="scb">Ongoing AI compliance advice on new AI implementations: vendor assessment, contract review, deployment-impact and accountability towards supervision. Includes preparation for AI Act enforcement.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; When DCBS is relevant to you</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">AI portfolio not classified</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">A growing number of AI systems are deployed in operations, but there is no inventory, no risk classification and no clear view of which systems fall under which AI Act category.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">High-risk AI system before go-live</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">An AI system under Annex III (critical infrastructure, education, employment, access to public services, law enforcement) is approaching go-live and requires a FRIA plus high-risk obligations met before market introduction.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">ISO 42001 track under consideration</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Clients or the organisation itself want a demonstrable AI management system. ISO 42001 implementation is the direction, but help is needed on gap analysis and alignment with existing ISO 27001 structure.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start">
    <div>
      <span class="ew">03 &mdash; What you get</span>
      <h2 class="sh" style="margin-top:.8rem">Concrete <span class="g">deliverables</span></h2>
      <ul style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem">
        <li style="margin-bottom:.6rem">AI portfolio inventory with per-system risk classification</li>
        <li style="margin-bottom:.6rem">AI governance framework: policy, role allocation, escalation paths</li>
        <li style="margin-bottom:.6rem">FRIA report for high-risk systems, in line with AI Act Article 27</li>
        <li style="margin-bottom:.6rem">ISO 42001 gap analysis + implementation roadmap</li>
        <li style="margin-bottom:.6rem">AI literacy training material for key staff</li>
        <li>Ongoing advisory line for new AI deployments</li>
      </ul>
    </div>
    <div>
      <span class="ew">04 &mdash; Approach</span>
      <h2 class="sh" style="margin-top:.8rem">Four <span class="g">steps</span></h2>
      <ol style="color:var(--bd);line-height:1.85;font-size:1rem;padding-left:1.2rem;margin-top:1rem;list-style:decimal">
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Discovery &amp; portfolio scan</strong> &mdash; inventory of AI systems in use, including shadow AI (productivity tools, embedded AI in SaaS). First-pass classification under AI Act categories.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Risk classification &amp; prioritisation</strong> &mdash; final per-system classification with corresponding obligations. Prioritisation by risk and go-live date.</li>
        <li style="margin-bottom:.8rem"><strong style="color:var(--wh)">Governance implementation &amp; FRIAs</strong> &mdash; setting up the governance framework, executing FRIAs for high-risk systems, deploying ISO 42001 controls.</li>
        <li><strong style="color:var(--wh)">Embedding &amp; AI literacy</strong> &mdash; ongoing monitoring, AI literacy training for relevant staff, preparation for AI Act enforcement and possible audits.</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">05 &mdash; For whom</span>
  <h2 class="sh" style="margin-top:.8rem">Organisations that <span class="g">deploy or supply AI</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS works for organisations with AI systems in production or in the pipeline: financial institutions, public sector organisations, critical infrastructure and international corporates. AI providers and AI deployers with obligations under the EU AI Act find here the combination of legal analysis and operational implementation. For specific case examples &mdash; see <a href="/en/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">our cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Set up AI Act compliance?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Free 30-minute intake call. The conversation explores where your AI portfolio stands under the Act &mdash; and which priorities are feasible.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Book intake &rarr;</a>
      <a href="/en/contact/" class="btn bg">Contact via form</a>
    </div>
  </div>
</section>"""


def service_body_datamgmt_nl() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/diensten/" style="color:var(--mu);text-decoration:none">Diensten</a> / Data Management</p>
  <h2>Data Management en <span class="g">Data Governance</span></h2>
  <p class="sub">De brug tussen privacy en AI compliance. Data governance frameworks, datavolwassenheidsassessments en data quality management volgens DAMA-DMBOK.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">Zonder schone datahuishouding geen AVG-naleving en geen werkbare AI governance. Een DPIA of FRIA bouwt op data lineage die u moet kennen, een verwerkingsregister steunt op een datacatalogus die actueel is, en ISO 42001 vereist dat AI-systemen op gecontroleerde data draaien. Data management is daarmee niet een naast-traject &mdash; het is de basis waarop privacy- en AI-compliance functioneren.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">DCBS bouwt aan deze basis volgens internationale standaarden (DAMA-DMBOK) en verbindt het expliciet met uw AVG- en AI Act-trajecten. Niet als losse data-strategie-exercitie, maar als compliance-enabler.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; Wat het inhoudt</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">Data governance <span class="g">in samenhang</span></h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Vier inhoudelijke gebieden: data governance framework, datavolwassenheid, data quality en data strategie. Aansluitend op uw privacy- en AI-compliance, niet als parallel spoor.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" style="cursor:default"><div class="sct">Data governance framework</div><p class="scb">Data governance framework met data-eigenaarschap, stewards, beleid en besluitvormingsstructuur. Aansluitend op DAMA-DMBOK domeinen en gekoppeld aan privacy- en AI-governance.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Datavolwassenheid assessment</div><p class="scb">Data maturity assessment volgens een gevalideerd model (CMMI for Data Management of vergelijkbaar). Resultaat: scorekaart per DAMA-domein met concrete prioriteiten voor de komende 12&ndash;24 maanden.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Data quality management</div><p class="scb">Data quality management programma: dimensies (volledigheid, juistheid, consistentie, tijdigheid), meetcadans, dashboards en escalatiepaden. Voor datasets die AVG- of AI Act-impact hebben.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">DAMA-DMBOK implementatie</div><p class="scb">DAMA-DMBOK implementatie als gemeenschappelijke taal en structuur. Niet een 1-op-1 boekvertaling, maar selectieve toepassing van de domeinen die voor uw organisatie waarde leveren.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Master data management consultant</div><p class="scb">Master data management consultancy voor organisaties met meerdere systemen die kritieke entiteiten (klant, leverancier, product) niet eenduidig benoemen. Vaak een blokkade voor AVG-rechten-uitvoering (inzage, vergetelheid) en AI-trainingsdata-kwaliteit.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; Wanneer DCBS voor u relevant is</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Verwerkingsregister leunt op data die niemand bezit</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Het AVG-verwerkingsregister noemt verwerkingen op datasets waarvoor geen duidelijke eigenaar bekend is, geen kwaliteits-bewaking bestaat en geen lineage gedocumenteerd is. Privacy en data management lopen uit elkaar.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">AI-systeem op ongecontroleerde data</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Een AI-systeem (in productie of in ontwikkeling) draait op datasets waarvan de herkomst, kwaliteit en governance niet sluitend zijn. ISO 42001 of een FRIA brengt dit aan het licht en vereist een fix.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Data governance is gestart, maar stokt</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">Een data governance-initiatief is enkele jaren geleden opgestart, maar is blijven hangen op presentatie-niveau zonder operationele inbedding. Externe versterking nodig om het over de finish te krijgen.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">03 &mdash; Typische opdrachtvormen</span>
  <h2 class="sh" style="margin-top:.8rem">Data management <span class="g">is maatwerk</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px;margin-bottom:2rem">Data management leent zich slecht voor een SKU-lijst. De vorm volgt uit volwassenheidsniveau, organisatie-omvang en de bottleneck die geadresseerd wordt. Een paar typische opdrachtvormen:</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem">
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Data governance framework opzetten</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Greenfield-traject: data-eigenaren benoemen, stewards aanwijzen, beleid en besluitvormings-structuur ontwerpen, eerste data-domeinen onder governance brengen. Typisch 4&ndash;6 maanden.</p>
    </div>
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Datavolwassenheidsassessment</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Gestructureerde scan van bestaande data-organisatie: scorekaart per DAMA-domein, prioriteiten voor de komende 12&ndash;24 maanden, business case voor opvolging. Typisch 4&ndash;8 weken.</p>
    </div>
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">DAMA-DMBOK implementatie-traject</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Selectieve implementatie van DAMA-DMBOK-domeinen die het meeste waarde leveren voor uw organisatie. Geen boekvertaling, wel methodische onderbouwing. Typisch een meerjarig traject met faseplanning.</p>
    </div>
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Compliance-gedreven data quality programma</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Programma met focus op datasets die directe AVG- of AI Act-impact hebben: kwaliteits-dimensies definiëren, meetcadans inrichten, dashboards en escalatiepaden bouwen. Maakt audit-trail mogelijk. Typisch 6&ndash;12 maanden.</p>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">04 &mdash; Werkwijze</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">1. Discovery</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Gesprek met business-, IT- en privacy-stakeholders. Bepalen waar de pijn zit: AVG, AI compliance, audit-bevindingen, of strategische ambitie.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">2. Assessment</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Volwassenheidsmeting op de relevante DAMA-domeinen, met scorekaart en gap-rapport. Geen open-einde studie &mdash; vaste doorlooptijd.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">3. Implementatie</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Roadmap-uitvoering met heldere mijlpalen. Stuurgroep, eigenaarschap intern belegd, externe versterking waar de capaciteit te kort schiet.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">4. Borging</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Doorlopende monitoring, jaarcyclus, koppeling aan privacy- en AI-governance. Externe rol bouwt zichzelf gefaseerd af.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">05 &mdash; Voor wie</span>
  <h2 class="sh" style="margin-top:.8rem">Organisaties waar data <span class="g">de bottleneck is</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS werkt voor organisaties waar data management een blokkade vormt voor AVG- of AI-compliance: financi&euml;le instellingen, (semi-)publieke organisaties, kritieke infrastructuur en internationale corporates met complexe data-landschappen. Voor concrete praktijkvoorbeelden &mdash; bekijk <a href="/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">onze cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Data management op orde krijgen?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Gratis kennismakingsgesprek van 30 minuten. In het gesprek wordt verkend of een assessment, een framework of een specifieker traject de meeste impact heeft.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Plan kennismaking &rarr;</a>
      <a href="/contact/" class="btn bg">Contact via formulier</a>
    </div>
  </div>
</section>"""


def service_body_datamgmt_en() -> str:
    return """<div class="ph rev">
  <p class="crumb"><a href="/en/" style="color:var(--mu);text-decoration:none">Home</a> / <a href="/en/diensten/" style="color:var(--mu);text-decoration:none">Services</a> / Data Management</p>
  <h2>Data Management and <span class="g">Data Governance</span></h2>
  <p class="sub">The bridge between privacy and AI compliance. Data governance frameworks, data maturity assessments and data quality management along DAMA-DMBOK.</p>
</div>

<section class="sec rev">
  <div style="max-width:780px">
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem;margin-bottom:1.2rem">Without a clean data foundation, there is no working GDPR compliance and no defensible AI governance. A DPIA or FRIA depends on data lineage that you actually know; a processing record relies on a current data catalogue; ISO 42001 requires AI systems to run on controlled data. Data management is therefore not a parallel track &mdash; it is the foundation that lets privacy and AI compliance function.</p>
    <p style="color:var(--bd);line-height:1.85;font-size:1.05rem">DCBS builds that foundation along international standards (DAMA-DMBOK) and ties it explicitly to your GDPR and AI Act tracks. Not as a standalone data strategy exercise, but as a compliance enabler.</p>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">01 &mdash; What it covers</span>
  <div class="svc-grid" style="display:grid;grid-template-columns:1fr 1.5fr;gap:4rem;align-items:start;margin-bottom:3rem">
    <div>
      <h2 class="sh">Data governance <span class="g">in concert</span></h2>
      <p style="color:var(--bd);line-height:1.85;font-size:1rem">Four substantive areas: data governance framework, data maturity, data quality and data strategy. Aligned with your privacy and AI compliance, not as a parallel programme.</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;background:var(--br)">
      <div class="sc" style="cursor:default"><div class="sct">Data governance framework</div><p class="scb">Data governance framework with data ownership, stewards, policy and decision-making structure. Aligned with DAMA-DMBOK domains and linked to privacy and AI governance.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Data maturity assessment</div><p class="scb">Data maturity assessment against a validated model (CMMI for Data Management or equivalent). Output: scorecard per DAMA domain with concrete priorities for the next 12&ndash;24 months.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Data quality management</div><p class="scb">Data quality management programme: dimensions (completeness, accuracy, consistency, timeliness), measurement cadence, dashboards and escalation paths. For datasets with GDPR or AI Act impact.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">DAMA-DMBOK implementation</div><p class="scb">DAMA-DMBOK implementation as a shared language and structure. Not a one-to-one book translation, but selective adoption of the domains that deliver value for your organisation.</p></div>
      <div class="sc" style="cursor:default"><div class="sct">Master data management consultancy</div><p class="scb">Master data management consultancy for organisations with multiple systems that do not consistently identify critical entities (customer, supplier, product). Often the blocker for GDPR rights execution (access, erasure) and for AI training-data quality.</p></div>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">02 &mdash; When DCBS is relevant to you</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Processing record relies on unowned data</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">The GDPR processing record refers to datasets that have no clear owner, no quality oversight and no documented lineage. Privacy and data management have drifted apart.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">AI system on uncontrolled data</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">An AI system (in production or in development) runs on datasets whose provenance, quality and governance do not hold up. ISO 42001 or a FRIA surfaces this and requires a fix.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1.1rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Data governance started, then stalled</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.95rem">A data governance initiative started some years ago but has remained at presentation level without operational embedding. External reinforcement needed to bring it across the line.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">03 &mdash; Typical engagement shapes</span>
  <h2 class="sh" style="margin-top:.8rem">Data management <span class="g">is bespoke work</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px;margin-bottom:2rem">Data management does not lend itself to an SKU list. The shape follows from maturity level, organisation size and the bottleneck being addressed. A few typical engagement shapes:</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem">
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Stand up a data governance framework</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Greenfield track: name data owners, assign stewards, design policy and decision-making structure, bring the first data domains under governance. Typically 4&ndash;6 months.</p>
    </div>
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Data maturity assessment</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Structured scan of the existing data organisation: scorecard per DAMA domain, priorities for the next 12&ndash;24 months, business case for follow-up. Typically 4&ndash;8 weeks.</p>
    </div>
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">DAMA-DMBOK implementation track</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Selective implementation of the DAMA-DMBOK domains that deliver the most value for your organisation. Not a book translation, but methodological grounding. Typically a multi-year programme with phased planning.</p>
    </div>
    <div style="background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.06);padding:1.5rem;border-radius:8px">
      <h3 style="font-size:1.05rem;font-weight:900;color:var(--wh);margin:0 0 .8rem">Compliance-driven data quality programme</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Programme focused on datasets with direct GDPR or AI Act impact: define quality dimensions, set up measurement cadence, build dashboards and escalation paths. Enables audit trail. Typically 6&ndash;12 months.</p>
    </div>
  </div>
</section>

<section class="sec rev">
  <span class="ew">04 &mdash; Approach</span>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;margin-top:2rem">
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">1. Discovery</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Conversation with business, IT and privacy stakeholders. Locating the pain: GDPR, AI compliance, audit findings, or strategic ambition.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">2. Assessment</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Maturity scoring on the relevant DAMA domains, with scorecard and gap report. Not an open-ended study &mdash; fixed lead time.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">3. Implementation</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Roadmap execution with clear milestones. Steering committee, ownership assigned internally, external reinforcement where capacity falls short.</p>
    </div>
    <div style="border-left:3px solid var(--tl);padding:.5rem 0 .5rem 1.5rem">
      <h3 style="font-size:1rem;font-weight:900;color:var(--wh);margin:0 0 .6rem">4. Embedding</h3>
      <p style="color:var(--bd);line-height:1.7;font-size:.93rem">Ongoing monitoring, annual cycle, linkage with privacy and AI governance. External role phases itself out gradually.</p>
    </div>
  </div>
</section>

<section class="sec rev2">
  <span class="ew">05 &mdash; For whom</span>
  <h2 class="sh" style="margin-top:.8rem">Organisations where data <span class="g">is the bottleneck</span></h2>
  <p style="color:var(--bd);line-height:1.85;font-size:1rem;margin-top:1rem;max-width:780px">DCBS works for organisations where data management is a blocker for GDPR or AI compliance: financial institutions, public sector organisations, critical infrastructure and international corporates with complex data landscapes. For specific case examples &mdash; see <a href="/en/cases/" style="color:var(--tl);text-decoration:none;font-weight:700">our cases</a>.</p>
</section>

<section class="sec rev2" style="padding-bottom:5rem">
  <div style="background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.05);padding:3rem 2.5rem;border-radius:12px;text-align:center;max-width:780px;margin:0 auto">
    <h2 style="font-size:1.8rem;font-weight:900;color:var(--wh);margin:0 0 1rem">Get data management in order?</h2>
    <p style="color:var(--bd);line-height:1.7;font-size:1.05rem;margin-bottom:2rem;max-width:560px;margin-left:auto;margin-right:auto">Free 30-minute intake call. The conversation explores whether an assessment, a framework or a more specific track delivers the most impact.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
      <a href="https://calendly.com/dubach-legal/30min" target="_blank" rel="noopener" class="btn bp">Book intake &rarr;</a>
      <a href="/en/contact/" class="btn bg">Contact via form</a>
    </div>
  </div>
</section>"""


SERVICE_BODY_BUILDERS = {
    "dpo-as-a-service":    (service_body_dpo_nl,      service_body_dpo_en),
    "avg-compliance":      (service_body_avg_nl,      service_body_avg_en),
    "ai-act-compliance":   (service_body_aiact_nl,    service_body_aiact_en),
    "data-management":     (service_body_datamgmt_nl, service_body_datamgmt_en),
}


def build_service_pages() -> list[dict]:
    """Page-configs voor de vier nieuwe dienst-landingspagina's.

    Phase 4 iteratie: alleen pagina's met body-builders in
    SERVICE_BODY_BUILDERS worden gegenereerd. Rest blijft pending tot
    user-bevestiging na review van pagina 1.
    """
    out: list[dict] = []
    for entry in SERVICE_PAGES_DATA:
        slug = entry["slug"]
        if slug not in SERVICE_BODY_BUILDERS:
            continue
        nl_body, en_body = SERVICE_BODY_BUILDERS[slug]
        # NL
        out.append({
            "url": entry["nl_slug_path"], "lang": NL,
            "template": None,
            "body_html_raw": nl_body(),
            "title": entry["nl_title"],
            "description": entry["nl_desc"],
            "keywords": entry["nl_keywords"],
            "og_title": entry["nl_title"].split(" | ")[0],
            "og_description": entry["nl_desc"][:200],
            "service_type": entry["service_type_nl"],
            "service_page": True,
        })
        # EN
        out.append({
            "url": entry["en_slug_path"], "lang": EN,
            "template": None,
            "body_html_raw": en_body(),
            "title": entry["en_title"],
            "description": entry["en_desc"],
            "keywords": entry["en_keywords"],
            "og_title": entry["en_title"].split(" | ")[0],
            "og_description": entry["en_desc"][:200],
            "service_type": entry["service_type_en"],
            "service_page": True,
        })
    return out


def build_article_pages() -> list[dict]:
    """Bouw page-configs voor NL artikelen + EN-stubs.

    NL: gebruikt extracted template body (templates.json[art-xxx]).
    EN-stub: combineert EN-samenvatting + disclaimer + NL-template-body
    + translate.js script voor optionele runtime-vertaling.
    """
    out: list[dict] = []
    for art in ARTICLES:
        slug = art["slug"]
        nl_url = f"/nieuws/{slug}/"
        en_url = f"/en/nieuws/{slug}/"

        # NL pagina — standaard template_body
        out.append({
            "url": nl_url, "lang": NL, "template": art["key"],
            "title": art["nl_title"],
            "description": art["nl_desc"],
            "keywords": art["nl_keywords"],
            "og_title": art["nl_title"].split(" | ")[0],
            "og_description": art["nl_desc"][:200],
            "article_type": True,
        })

        # EN-stub — body = summary + disclaimer + NL-content
        # We bouwen een synthetische template door key te overriden + body-prefix
        disclaimer = (
            '<div style="background:rgba(255,255,255,.04);border-left:3px solid var(--tl);'
            'padding:1rem 1.25rem;margin:1.5rem 0;font-size:.9rem;color:var(--mu);line-height:1.6">'
            '<strong style="color:var(--wh);display:block;margin-bottom:.35rem">Original article in Dutch</strong>'
            "Full English translation coming soon. The summary above captures the key points. "
            "The full Dutch text follows below."
            '</div>'
        )
        en_body_prefix = (
            '<div class="art" style="margin-bottom:0">' +
            art["en_summary"] +
            disclaimer +
            '<hr style="border:0;border-top:1px solid rgba(255,255,255,.08);margin:1.5rem 0">' +
            '<p style="font-size:.85rem;color:var(--mu);font-style:italic;margin-bottom:1rem">' +
            'Dutch original / Nederlandse versie:' +
            '</p>' +
            '</div>'
        )

        out.append({
            "url": en_url, "lang": EN, "template": art["key"],
            "title": art["en_title"],
            "description": art["en_desc"],
            "keywords": art["en_keywords"],
            "og_title": art["en_title"].split(" | ")[0],
            "og_description": art["en_desc"][:200],
            "article_type": True,
            "en_stub_prefix": en_body_prefix,
            "extra_scripts": ["/assets/js/translate.js"],
        })
    return out

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

# Mapping van P[key] naar URL. Article slugs confirmed by owner 2026-05-20.
KEY_TO_URL = {
    "home": "/", "over": "/over-ons/", "diensten": "/diensten/",
    "cases": "/cases/", "nieuws": "/nieuws/", "contact": "/contact/",
    "privacy": "/privacybeleid/",
    "en-home": "/en/", "en-over": "/en/over-ons/", "en-diensten": "/en/diensten/",
    "en-cases": "/en/cases/", "en-nieuws": "/en/nieuws/", "en-contact": "/en/contact/",
    "en-privacy": "/en/privacy-statement/",
    "art-vodafone":    "/nieuws/vodafone-boete-45-miljoen/",
    "art-fria":        "/nieuws/fria-fundamental-rights-impact-assessment/",
    "art-ailliteracy": "/nieuws/ai-literacy-verplichting/",
    "art-claude":      "/nieuws/claude-ai-governance-discipline/",
    "art-genai":       "/nieuws/risicos-generatieve-ai/",
    "art-tesla":       "/nieuws/tesla-robotaxi-privacy/",
    "art-gdpr7":       "/nieuws/zeven-jaar-avg-handhaving-nederland/",
    "art-ai2027":      "/nieuws/ai2027-superintelligente-ai/",
    "art-bc5701":      "/nieuws/bc-5701-privacy-keurmerk/",
}


def transform_go_links(html: str) -> str:
    """Vervang inline `onclick="go('key')"` (en variants met ;cm()) door
    `href="/url/"`. Indien al een href bestaat: laat staan en strip alleen
    de onclick.
    """
    def repl_with_href(match):
        prefix = match.group(1)
        key = match.group(2)
        url = KEY_TO_URL.get(key, "#")
        prefix = re.sub(r'\s*href="[^"]*"', "", prefix)
        return f'{prefix} href="{url}"'

    pattern = re.compile(
        r'(<(?:a|div|span|button)\b[^>]*?)\s+onclick="go\([\'\"]([a-z0-9-]+)[\'\"]\)(?:;[a-z()]+)?"',
        re.IGNORECASE,
    )
    return pattern.sub(repl_with_href, html)


def strip_embedded_footer(html: str) -> str:
    """Strip de in elk P[key] template ingebakken <footer>...</footer> blok.

    Reden: nieuwe multi-file architectuur heeft ONE shared footer per
    pagina (build_footer). Templates bevatten de OUDE footer met
    hardcoded 2025 copyright en zonder dienst-sublinks.
    """
    return re.sub(r"<footer\b[\s\S]*?</footer>\s*", "", html)


def strip_breadcrumb_articles_only(html: str) -> str:
    """News-article templates beginnen met <p class="crumb">Home / Nieuws / Artikel</p>.
    Bij refactor is de breadcrumb redundant: nav heeft al de Nieuws-link.
    Plus de <span href> die transform_go_links produceert is geen valide
    HTML (span heeft geen href). Vervangen door echte <a href>-breadcrumb."""
    pattern = re.compile(
        r'<p class="crumb">\s*<span\s+href="([^"]+)">([^<]+)</span>\s*/\s*<span\s+href="([^"]+)">([^<]+)</span>\s*/\s*([^<]+?)</p>',
        re.IGNORECASE,
    )
    return pattern.sub(
        lambda m: (
            f'<p class="crumb">'
            f'<a href="{m.group(1)}" style="color:var(--mu);text-decoration:none">{m.group(2)}</a> / '
            f'<a href="{m.group(3)}" style="color:var(--mu);text-decoration:none">{m.group(4)}</a> / '
            f'{m.group(5).strip()}</p>'
        ),
        html,
    )


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

    # Body content uit template OF raw HTML (voor service pages)
    if cfg.get("body_html_raw"):
        body_html = cfg["body_html_raw"]
    else:
        body_html = transform_go_links(TEMPLATES[cfg["template"]])
        body_html = strip_embedded_footer(body_html)
        body_html = strip_breadcrumb_articles_only(body_html)
        # EN-stub: prepend Engelse samenvatting + disclaimer voor NL-template
        if cfg.get("en_stub_prefix"):
            body_html = cfg["en_stub_prefix"] + body_html

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

    # Service JSON-LD voor dienst-landingspagina's
    if cfg.get("service_page"):
        service_jsonld = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": cfg["og_title"],
            "provider": {
                "@type": "ProfessionalService",
                "name": "The Data Compliance Builders",
                "url": "https://www.dcbs.nl",
            },
            "areaServed": {"@type": "Country", "name": "Netherlands"},
            "serviceType": cfg.get("service_type", ""),
            "description": cfg["description"],
            "url": canonical,
        }
        jsonld_blocks.append(
            '<script type="application/ld+json">\n' +
            json.dumps(service_jsonld, ensure_ascii=False, indent=2) +
            '\n</script>'
        )

    # Article JSON-LD voor nieuws-pagina's
    if cfg.get("article_type"):
        article_jsonld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": cfg["og_title"],
            "description": cfg["description"],
            "author": {"@type": "Person", "name": "Jeroen Dubach"},
            "publisher": {
                "@type": "ProfessionalService",
                "name": "The Data Compliance Builders",
                "url": "https://www.dcbs.nl",
            },
            "inLanguage": "nl-NL" if lang == NL else "en-GB",
            "url": canonical,
        }
        jsonld_blocks.append(
            '<script type="application/ld+json">\n' +
            json.dumps(article_jsonld, ensure_ascii=False, indent=2) +
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

{footer_html}

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
    all_pages = list(PAGES) + build_article_pages() + build_service_pages()
    for cfg in all_pages:
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
