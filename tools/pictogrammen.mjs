// Pictogrammen in de huisstijl (lijntekeningen, 24x24). Gebruikt door tools/bouw.mjs voor het blok
// "Verwante diensten"; dezelfde pictogrammen staan in de pagina's zelf bij de diensten en schema's.
const PAD = {
  schild: '<path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6l7-3z"></path><path d="M9 12l2 2 4-4"></path>',
  chip: '<rect x="7" y="7" width="10" height="10" rx="2"></rect><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"></path>',
  netwerk: '<circle cx="12" cy="5" r="2.5"></circle><circle cx="5" cy="18" r="2.5"></circle><circle cx="19" cy="18" r="2.5"></circle><path d="M12 7.5v4M12 11.5l-5.2 4.6M12 11.5l5.2 4.6"></path>',
  slot: '<rect x="5" y="11" width="14" height="10" rx="2"></rect><path d="M8 11V8a4 4 0 0 1 8 0v3M12 15v2"></path>',
  atoom: '<circle cx="12" cy="12" r="1.5"></circle><ellipse cx="12" cy="12" rx="9.5" ry="4"></ellipse><ellipse cx="12" cy="12" rx="9.5" ry="4" transform="rotate(60 12 12)"></ellipse><ellipse cx="12" cy="12" rx="9.5" ry="4" transform="rotate(120 12 12)"></ellipse>',
  klembord: '<rect x="6" y="4" width="12" height="17" rx="2"></rect><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h3"></path>',
  vergrootglas: '<circle cx="11" cy="11" r="6.5"></circle><path d="M16 16l4.5 4.5"></path>',
  document: '<path d="M7 3h7l4 4v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"></path><path d="M14 3v4h4M9 12h6M9 16h6"></path>',
  waarschuwing: '<path d="M12 4l9 16H3l9-16z"></path><path d="M12 10v4M12 17v.5"></path>',
  mensen: '<circle cx="9" cy="8" r="3"></circle><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"></path><circle cx="17" cy="9" r="2.3"></circle><path d="M16 14.2c2.9.3 5 2.6 5 5.8"></path>',
  vink: '<circle cx="12" cy="12" r="9"></circle><path d="M8 12.5l2.8 2.8L16 9.5"></path>',
  meter: '<path d="M4 17a8 8 0 1 1 16 0"></path><path d="M12 17l4-5M3 20h18"></path>',
  vlag: '<path d="M6 21V4M6 5h11l-2.5 3.5L17 12H6"></path>',
  keten: '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"></path><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"></path>',
  gebouw: '<path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16M16 9h2a2 2 0 0 1 2 2v10M3 21h18M8 7h4M8 11h4M8 15h4"></path>',
  herhaal: '<path d="M4 12a8 8 0 0 1 13.7-5.7L20 8.5M20 4v4.5h-4.5"></path><path d="M20 12a8 8 0 0 1-13.7 5.7L4 15.5M4 20v-4.5h4.5"></path>',
  badge: '<circle cx="12" cy="9" r="5.5"></circle><path d="M8.5 13.5L7 21l5-2.5 5 2.5-1.5-7.5"></path>',
  oog: '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"></path><circle cx="12" cy="12" r="3"></circle>',
  klok: '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3.5 2"></path>',
};
export const svg = (naam, maat = 24) => {
  if (!PAD[naam]) throw new Error('onbekend pictogram: ' + naam);
  return `<svg width="${maat}" height="${maat}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${PAD[naam]}</svg>`;
};
export const pic = naam => `<span class="pic">${svg(naam)}</span>`;
// pictogram per dienst
export const DIENST_PIC = {
  'avg-compliance': 'schild', 'ai-act-compliance': 'chip', 'nis2': 'netwerk', 'information-security': 'slot', 'quantum-readiness': 'atoom',
  'dpo-as-a-service': 'oog', 'privacy-officer-as-a-service': 'klembord', 'security-officer-as-a-service': 'vink', 'tprm-contractmanagement': 'keten',
};
