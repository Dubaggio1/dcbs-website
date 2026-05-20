/*!
 * The Data Compliance Builders — shared JS (main)
 * Loaded on every page via <script defer src="/assets/js/main.js">.
 *
 * Contents:
 *   - LANGUAGE_MAP (NL <-> EN URL mapping)
 *   - setLang(lang)          : button-toggle that navigates to mapped URL
 *   - mopen/mclose/mtoggle   : mobile menu controls
 *   - initHamburger          : DOM-ready event wiring
 *   - cookieAccept/Decline   : cookie-banner controls + first-visit auto-show
 *   - Nav-active-state       : highlight current menu-item via pathname
 *   - Copyright year         : populate [data-copyright-year] with current year
 */

// ─────────────────────────────────────────────────────────────────────
//  LANGUAGE MAP — NL pad ↔ EN pad
//  Per route 1:1 paar. Custom news-pages (geen EN-versie) vallen
//  terug op /en/nieuws/ (overzicht).
// ─────────────────────────────────────────────────────────────────────
var LANGUAGE_MAP = {
  // NL -> EN
  '/':                                     '/en/',
  '/over-ons/':                            '/en/over-ons/',
  '/diensten/':                            '/en/diensten/',
  '/diensten/dpo-as-a-service/':           '/en/diensten/dpo-as-a-service/',
  '/diensten/avg-compliance/':             '/en/diensten/gdpr-compliance/',
  '/diensten/ai-act-compliance/':          '/en/diensten/ai-act-compliance/',
  '/diensten/data-management/':            '/en/diensten/data-management/',
  '/cases/':                               '/en/cases/',
  '/nieuws/':                              '/en/nieuws/',
  '/contact/':                             '/en/contact/',
  '/privacybeleid/':                       '/en/privacy-statement/',
  // News article slugs (set in Phase 4)
  '/nieuws/vodafone-boete-45-miljoen/':              '/en/nieuws/vodafone-boete-45-miljoen/',
  '/nieuws/fria-fundamental-rights-impact-assessment/': '/en/nieuws/fria-fundamental-rights-impact-assessment/',
  '/nieuws/ai-literacy-verplichting/':               '/en/nieuws/ai-literacy-verplichting/',
  // (Drie overige nieuws-slugs nog te bevestigen door eigenaar — placeholders)
  // EN -> NL (reverse, auto-generated below)
};
(function () {
  var keys = Object.keys(LANGUAGE_MAP);
  for (var i = 0; i < keys.length; i++) {
    var nl = keys[i];
    var en = LANGUAGE_MAP[nl];
    if (en && !LANGUAGE_MAP[en]) LANGUAGE_MAP[en] = nl;
  }
})();

// ─────────────────────────────────────────────────────────────────────
//  Language toggle. Button is a <button onclick="setLang('en')">.
//  Lookup huidige pathname in LANGUAGE_MAP; navigeer naar tegenhanger.
//  Bij ontbrekende mapping (bv. custom-news artikel): fallback naar
//  taalkeuze-homepage (/en/ of /).
// ─────────────────────────────────────────────────────────────────────
function setLang(targetLang) {
  var current = window.location.pathname;
  if (current.length > 1 && current.charAt(current.length - 1) !== '/') current += '/';
  var target = LANGUAGE_MAP[current];
  if (target) {
    window.location.href = target;
    return;
  }
  // Fallback: ga naar taalhomepage
  window.location.href = targetLang === 'en' ? '/en/' : '/';
}

// ─────────────────────────────────────────────────────────────────────
//  Mobile menu
// ─────────────────────────────────────────────────────────────────────
function mopen() {
  var m = document.getElementById('mobile-menu');
  var h = document.getElementById('hamburger');
  if (m) m.classList.add('open');
  if (h) h.setAttribute('aria-expanded', 'true');
}
function mclose() {
  var m = document.getElementById('mobile-menu');
  var h = document.getElementById('hamburger');
  if (m) m.classList.remove('open');
  if (h) h.setAttribute('aria-expanded', 'false');
}
function mtoggle() {
  var m = document.getElementById('mobile-menu');
  if (!m) return;
  if (m.classList.contains('open')) { mclose(); } else { mopen(); }
}
// Legacy aliases (referenced in inline onclick van oude templates)
function tm() { mtoggle(); }
function cm() { mclose(); }

(function () {
  function initHamburger() {
    var btn = document.getElementById('hamburger');
    if (!btn) return;
    // Vervang event-listeners (voorkomt dubbele bind bij re-init)
    var newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
    newBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      mtoggle();
    });
    document.addEventListener('click', function (e) {
      var menu = document.getElementById('mobile-menu');
      var ham = document.getElementById('hamburger');
      if (menu && ham && menu.classList.contains('open')) {
        if (!menu.contains(e.target) && !ham.contains(e.target)) {
          mclose();
        }
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHamburger);
  } else {
    initHamburger();
  }
})();

// ─────────────────────────────────────────────────────────────────────
//  Cookie banner
//  Plausible plaatst geen cookies, dus alleen functioneel
//  noodzakelijke localStorage-key 'dcbs_cookie' (banner-keuze).
// ─────────────────────────────────────────────────────────────────────
function cookieAccept() {
  localStorage.setItem('dcbs_cookie', 'accepted');
  var b = document.getElementById('cookie-banner');
  if (b) b.classList.add('hidden');
}
function cookieDecline() {
  localStorage.setItem('dcbs_cookie', 'declined');
  var b = document.getElementById('cookie-banner');
  if (b) b.classList.add('hidden');
}
(function () {
  function init() {
    if (!localStorage.getItem('dcbs_cookie')) {
      setTimeout(function () {
        var b = document.getElementById('cookie-banner');
        if (b) b.style.display = 'flex';
      }, 1500);
    } else {
      var b = document.getElementById('cookie-banner');
      if (b) b.classList.add('hidden');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// ─────────────────────────────────────────────────────────────────────
//  Nav-active-state
//  Highlight het menu-item dat overeenkomt met window.location.pathname.
//  Werkt op zowel desktop nav (.nav-links a) als mobile menu
//  (.mobile-menu a). Vereist data-path-attribuut op de <a>.
// ─────────────────────────────────────────────────────────────────────
(function () {
  function init() {
    var path = window.location.pathname;
    if (path.length > 1 && path.charAt(path.length - 1) !== '/') path += '/';
    var items = document.querySelectorAll('a[data-path]');
    for (var i = 0; i < items.length; i++) {
      var target = items[i].getAttribute('data-path');
      if (!target) continue;
      // Active = exact match OR pad valt onder /diensten/ submap voor "Diensten"-link
      var isActive = target === path ||
                     (target === '/diensten/' && path.indexOf('/diensten/') === 0) ||
                     (target === '/en/diensten/' && path.indexOf('/en/diensten/') === 0) ||
                     (target === '/nieuws/' && path.indexOf('/nieuws/') === 0) ||
                     (target === '/en/nieuws/' && path.indexOf('/en/nieuws/') === 0);
      if (isActive) items[i].classList.add('active');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// ─────────────────────────────────────────────────────────────────────
//  Copyright year — populeert <span data-copyright-year>YYYY</span>
//  Fallback (statisch jaartal in HTML) is voor non-JS crawlers.
// ─────────────────────────────────────────────────────────────────────
(function () {
  function init() {
    var year = String(new Date().getFullYear());
    var nodes = document.querySelectorAll('[data-copyright-year]');
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = year;
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// ─────────────────────────────────────────────────────────────────────
//  Scroll reveal — voegt .on toe aan elementen met .rev/.rev2/.rev3
//  zodra ze in viewport komen (CSS doet de animatie).
// ─────────────────────────────────────────────────────────────────────
(function () {
  function check() {
    var els = document.querySelectorAll('.rev:not(.on),.rev2:not(.on),.rev3:not(.on)');
    for (var i = 0; i < els.length; i++) {
      if (els[i].getBoundingClientRect().top < window.innerHeight - 80) {
        els[i].classList.add('on');
      }
    }
  }
  function init() {
    check();
    window.addEventListener('scroll', check, { passive: true });
    window.addEventListener('resize', check, { passive: true });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
