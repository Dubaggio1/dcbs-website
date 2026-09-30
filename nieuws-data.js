// DCBS nieuwsartikelen — dít bestand is de bron voor de nieuwspagina (/nieuws/) én de homepage.
//
// Nieuw artikel plaatsen: voeg bovenaan de lijst een item toe en publiceer de site (git push).
//   - De homepage toont automatisch de bovenste 3 items; de nieuwspagina toont alles, in deze volgorde.
//   - Velden: id (uniek), cat, date (vrije tekst, bijv. 'Oktober 2026'), title, summary,
//     link (URL van de LinkedIn-post; externe links openen in een nieuw tabblad), img (optioneel: pad naar een afbeelding in assets/nieuws/).
//   - cat is altijd een van de diensten (zelfde lijst als het formulier op de nieuwspagina): 'Privacy compliance',
//     'AI compliance', 'NIS2 / Cyberbeveiligingswet', 'Information security', 'Quantum-readiness',
//     'DPO as a Service', 'Privacy Officer as a Service', 'Security Officer as a Service'.
//   - Tip: na "Artikel toevoegen" op de nieuwspagina verschijnt een paneel "Publiceren" met de kant-en-klare regel voor dit bestand.
//   - Laat link leeg ('') zolang de URL nog niet bekend is: de kaart is dan zichtbaar maar niet klikbaar.
// De knop "Artikel toevoegen" op de nieuwspagina bewaart alleen in uw eigen browser en publiceert niets.
//
// 30 sep 2026: de links naar de artikelpagina's van de oude site (/nieuws/<slug>/, oude opmaak) zijn vervangen
// door links naar de LinkedIn-posts. Alleen de AI2027-post was zonder LinkedIn-login te vinden; vul de overige
// acht in (LinkedIn > post openen > "Link naar post kopiëren") — de site werkt zonder verdere aanpassing.
window.DCBS_ARTICLES = [
  { id: 'news-2026-09-ap-ict-leverancier', cat: 'Privacy compliance', date: 'September 2026', link: 'https://www.linkedin.com/posts/the-data-compliance-builders_de-ap-klopt-aan-bij-uw-ict-leverancier-bent-activity-7508433991608385536-mimb', title: 'De AP klopt aan bij uw ICT-leverancier. Is uw bestuur voorbereid?', summary: 'In april kondigde de Autoriteit Persoonsgegevens (AP) aan dat zij preventief gaat controleren bij ICT-leveranciers die grote hoeveelheden persoonsgegevens verwerken namens hun klanten. Dat klinkt als een probleem van de leverancier. Maar wie goed kijkt, ziet dat de verantwoordelijkheid voor het grootste deel bij de opdrachtgever ligt, en onder de Cyberbeveiligingswet en DORA zelfs persoonlijk bij het bestuur. In dit artikel leggen we uit wat er verandert, hoe de drie regimes in elkaar grijpen, en hoe u leveranciersbeheer inricht dat een kritische blik van elke toezichthouder kan doorstaan.', img: '/assets/nieuws/ap-ict-leverancier.webp' },
  { id: 'news-1', cat: 'AI compliance', date: 'Maart 2025', link: 'https://www.linkedin.com/posts/jeroendubach_ai-2027-a-realistic-scenario-of-ai-takeover-activity-7345686481031577600-liD5', title: 'AI2027: Superintelligente AI binnen twee jaar — zijn we er klaar voor?', summary: 'Het AI2027-scenario beschrijft een geloofwaardig pad naar transformatieve AI. Wat zijn de governance- en compliance-implicaties voor organisaties die vandaag al AI-systemen inzetten?' },
  { id: 'news-2', cat: 'Privacy compliance', date: '2025', link: '' /* TODO: LinkedIn-post-URL */, title: 'Recordboete Vodafone Duitsland: €45 miljoen — lessen voor uw compliance-programma', summary: 'De grootste AVG-boete in Duitsland tot nu toe. Wat ging er mis bij Vodafone en welke concrete stappen kunt u zetten?' },
  { id: 'news-3', cat: 'AI compliance', date: '2025', link: '' /* TODO: LinkedIn-post-URL */, title: 'AI & Grondrechten: een gestructureerde aanpak onder de EU AI Act', summary: 'De EU AI Act vereist Fundamental Rights Impact Assessments voor bepaalde hoog-risico AI-systemen. Een gestructureerde aanpak, stap voor stap.' },
  { id: 'news-4', cat: 'Privacy compliance', date: '2025', link: '' /* TODO: LinkedIn-post-URL */, title: 'Zeven jaar AVG-handhaving in Nederland: wat hebben we geleerd?', summary: 'Zeven jaar AVG-handhaving door de AP. Welke sectoren werden het hardst geraakt en wat betekent dit voor uw compliance-programma?' },
  { id: 'news-5', cat: 'AI compliance', date: '2025', link: '' /* TODO: LinkedIn-post-URL */, title: 'Wanneer Claude brutaal wordt: AI-nieuwsgierigheid omzetten in governance-discipline', summary: 'Een onverwachte interactie met Claude onthult iets fundamenteels over AI-governance: onvoorspelbaar gedrag is geen incident, maar een ontwerpgegeven.' },
  { id: 'news-6', cat: 'Privacy compliance', date: '2025', link: '' /* TODO: LinkedIn-post-URL */, title: 'Tesla Robotaxi publieke pilot van start — maar wat met uw privacy?', summary: 'Autonome voertuigen verzamelen ongekende hoeveelheden data. Wat zegt de AVG over biometrische gegevens in de openbare ruimte?' },
  { id: 'news-7', cat: 'AI compliance', date: '2024', link: '' /* TODO: LinkedIn-post-URL */, title: 'De risico’s van Generatieve AI: wat uw organisatie moet weten', summary: 'Generatieve AI prolifereert op de werkvloer. De juridische, privacy- en operationele risico’s op een rij.' },
  { id: 'news-8', cat: 'AI compliance', date: '2024', link: '' /* TODO: LinkedIn-post-URL */, title: 'AI-geletterdheid en verboden AI-praktijken onder de EU AI Act', summary: 'De EU AI Act introduceert een AI-geletterdheidsplicht én een lijst verboden praktijken. Wat beide betekenen voor uw organisatie.' },
  { id: 'news-9', cat: 'Privacy compliance', date: '2024', link: '' /* TODO: LinkedIn-post-URL */, title: 'Waarom het BC 5701 Privacy Keurmerk essentieel is voor gegevensverwerkers', summary: 'Het BC 5701 Privacy Keurmerk is uitgegroeid tot de marktstandaard voor betrouwbare gegevensverwerkers.' }
];
