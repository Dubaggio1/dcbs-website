/*!
 * The Data Compliance Builders — news admin (loaded only on /nieuws/ + /en/nieuws/)
 *
 * Bevat:
 *   - 3-click admin trigger (rechter-onderhoek)
 *   - openAdmin / closeAdmin (modal-bg toggle)
 *   - saveArticle (localStorage 'dcbs_articles' + optionele API-vertaling)
 *   - renderCustomNews (toont user-added articles na statische artikelen)
 *   - showCustomArt (toont één custom article inline op /nieuws/)
 *
 * SECURITY: saveArticle doet fetch naar api.anthropic.com vanuit browser.
 *           Dit was bestaand gedrag. Volgende sessie: verplaatsen naar
 *           server-side / pre-generation. Zie /docs/seo-pass-1.md.
 */

// 3-click admin trigger
(function () {
  function init() {
    var trigger = document.getElementById('admin-trigger');
    if (!trigger) return;
    var clicks = 0, timer;
    trigger.addEventListener('click', function () {
      clicks++;
      clearTimeout(timer);
      timer = setTimeout(function () { clicks = 0; }, 500);
      if (clicks >= 3) { clicks = 0; openAdmin(); }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

function openAdmin() {
  var pw = prompt('Wachtwoord:');
  if (pw !== 'dcbs2025!') { if (pw !== null) alert('Ongeldig wachtwoord'); return; }
  var m = document.getElementById('modal-bg');
  if (m) m.classList.add('open');
}

function closeAdmin(e) {
  var m = document.getElementById('modal-bg');
  if (!m) return;
  if (!e || e.target === m) m.classList.remove('open');
}

function saveArticle(e) {
  e.preventDefault();
  var artLang  = document.getElementById('a-lang').value;
  var artCat   = document.getElementById('a-cat').value;
  var artDate  = document.getElementById('a-date').value;
  var artTitle = document.getElementById('a-title').value;
  var artExc   = document.getElementById('a-exc').value;
  var artBody  = document.getElementById('a-body').value;
  var artTc    = artCat === 'Privacy' ? 'tpr' : 'tai';
  var artId    = 'custom-' + Date.now();
  var artLi    = document.getElementById('a-li') ? document.getElementById('a-li').value.trim() : '';

  var art = {
    id: artId, lang: artLang, cat: artCat, date: artDate,
    title: artTitle, exc: artExc, body: artBody, tc: artTc, li: artLi
  };

  var arts = JSON.parse(localStorage.getItem('dcbs_articles') || '[]');
  arts.unshift(art);
  localStorage.setItem('dcbs_articles', JSON.stringify(arts));
  closeAdmin();
  e.target.reset();
  renderCustomNews();

  // ── Auto-translate naar de andere taal ────────────────────────────
  // SECURITY: API-key staat in browser. Move naar server-side ASAP.
  var otherLang  = artLang === 'nl' ? 'en' : 'nl';
  var otherLabel = otherLang === 'en' ? 'Engels' : 'Nederlands';

  var notice = document.createElement('div');
  notice.style.cssText = 'position:fixed;bottom:5rem;right:1.5rem;background:var(--cd);border:1px solid var(--bl);padding:1rem 1.5rem;z-index:500;font-size:.85rem;color:var(--mu);max-width:280px';
  notice.innerHTML = '&#8987; Automatisch vertalen naar ' + otherLabel + '...';
  document.body.appendChild(notice);

  var toTranslate = 'Title: ' + artTitle + '\n\nSummary: ' + artExc + '\n\nBody:\n' + artBody;
  var targetLangName = otherLang === 'en' ? 'English' : 'Dutch';
  var prompt = 'Translate this article from ' + (artLang === 'nl' ? 'Dutch' : 'English') +
    ' to ' + targetLangName + '. Return ONLY a JSON object with keys: title, exc, body. ' +
    'Keep names, acronyms (AVG, GDPR, DPO, DPIA, FRIA, ISO, EU AI Act, BC 5701) unchanged.  ' + toTranslate;

  fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }]
    })
  })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var text = data.content && data.content[0] && data.content[0].text || '';
      var jsonMatch = text.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        notice.innerHTML = '&#10004; Opgeslagen (vertaling overgeslagen)';
        setTimeout(function () { notice.remove(); }, 3000);
        return;
      }
      var translated;
      try { translated = JSON.parse(jsonMatch[0]); } catch (e2) { notice.remove(); return; }
      var translArt = {
        id: 'custom-' + Date.now(), lang: otherLang, cat: artCat,
        date: artDate, title: translated.title || artTitle,
        exc: translated.exc || artExc, body: translated.body || artBody,
        tc: artTc, li: artLi
      };
      var arts2 = JSON.parse(localStorage.getItem('dcbs_articles') || '[]');
      arts2.unshift(translArt);
      localStorage.setItem('dcbs_articles', JSON.stringify(arts2));
      notice.innerHTML = '&#10004; Opgeslagen in NL &amp; automatisch vertaald naar ' + otherLabel + '!';
      setTimeout(function () { notice.remove(); }, 4000);
    })
    .catch(function () {
      notice.innerHTML = '&#10004; Opgeslagen (vertaling mislukt)';
      setTimeout(function () { notice.remove(); }, 3000);
    });
}

// ─────────────────────────────────────────────────────────────────────
//  renderCustomNews — toont user-added articles in #custom-news
//  Wordt aangeroepen op DOMContentLoaded (init) en na saveArticle.
//  Filter op huidige paginataal (afgeleid uit <html lang>).
// ─────────────────────────────────────────────────────────────────────
function renderCustomNews() {
  var el = document.getElementById('custom-news');
  if (!el) return;
  var arts = JSON.parse(localStorage.getItem('dcbs_articles') || '[]');
  if (!arts.length) { el.innerHTML = ''; return; }
  var pageLang = (document.documentElement.lang || 'nl').toLowerCase().slice(0, 2);
  var html = '<div style="margin-top:2px;background:var(--br)" class="g3">';
  arts.forEach(function (a) {
    if (a.lang !== pageLang) return;
    var liLinkHtml = '';
    if (a.li) {
      liLinkHtml = '<a href="' + a.li + '" target="_blank" rel="noopener" onclick="event.stopPropagation()"' +
        ' style="display:inline-flex;align-items:center;gap:.35rem;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#0077b5;text-decoration:none;margin-top:.5rem">' +
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width:13px;height:13px"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>' +
        'LinkedIn &rarr;</a>';
    }
    html += '<div class="nc on" data-artid="' + a.id + '" onclick="showCustomArt(this.dataset.artid)">' +
      '<span class="ntag ' + a.tc + '">' + a.cat + '</span>' +
      '<div class="ndate">' + a.date + '</div>' +
      '<h3>' + a.title + '</h3>' +
      '<p>' + a.exc.substring(0, 120) + '...</p>' +
      '<span class="nm">Lees artikel &rarr;</span>' +
      liLinkHtml +
      '</div>';
  });
  html += '</div>';
  el.innerHTML = html;
}
(function () {
  function init() { renderCustomNews(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// ─────────────────────────────────────────────────────────────────────
//  showCustomArt — toont één custom article inline op /nieuws/.
//  Vervangt #news-content. Back-button doet location.reload() zodat
//  het overzicht weer wordt opgebouwd uit static HTML + render().
// ─────────────────────────────────────────────────────────────────────
function showCustomArt(id) {
  var arts = JSON.parse(localStorage.getItem('dcbs_articles') || '[]');
  var a = null;
  for (var i = 0; i < arts.length; i++) { if (arts[i].id === id) { a = arts[i]; break; } }
  if (!a) return;

  var pageLang  = (document.documentElement.lang || 'nl').toLowerCase().slice(0, 2);
  var newsUrl   = pageLang === 'en' ? '/en/nieuws/' : '/nieuws/';
  var btnLabel1 = pageLang === 'en' ? 'Discuss with Jeroen' : 'Bespreek met Jeroen';
  var btnLabel2 = pageLang === 'en' ? 'Back to news' : 'Terug naar overzicht';
  var crumbLbl  = pageLang === 'en' ? ['Home', 'News', 'Article'] : ['Home', 'Nieuws', 'Artikel'];
  var homeUrl   = pageLang === 'en' ? '/en/' : '/';

  var body = a.body.split('\n\n').map(function (p) { return '<p>' + p + '</p>'; }).join('');
  var liHtml = '';
  if (a.li) {
    liHtml = '<a href="' + a.li + '" target="_blank" rel="noopener"' +
      ' style="display:inline-flex;align-items:center;gap:.5rem;font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#0077b5;text-decoration:none;margin-bottom:1.5rem;padding:.6rem 1.2rem;border:1px solid rgba(0,119,181,.4)">' +
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>' +
      (pageLang === 'en' ? 'View original post on LinkedIn' : 'Bekijk originele post op LinkedIn') +
      '</a>';
  }

  var container = document.getElementById('news-content') || document.querySelector('main') || document.body;
  container.innerHTML = [
    '<div class="ph">',
      '<p class="crumb">',
        '<a href="' + homeUrl + '"><span>' + crumbLbl[0] + '</span></a> / ',
        '<a href="' + newsUrl + '"><span>' + crumbLbl[1] + '</span></a> / ' + crumbLbl[2],
      '</p>',
      '<span class="ntag ' + a.tc + '" style="margin-bottom:1.5rem;display:inline-block">' + a.cat + '</span>',
      '<h2>' + a.title + '</h2>',
      '<p class="sub" style="font-size:.9rem;margin-top:1rem">' + a.date + ' &middot; Jeroen Dubach</p>',
    '</div>',
    '<section class="sec">',
      '<div class="art">',
        liHtml,
        body,
        '<div style="display:flex;gap:1rem;margin-top:2rem;flex-wrap:wrap">',
          '<a href="https://calendly.com/dubach-legal/30min" target="_blank" class="btn bp">' + btnLabel1 + ' &rarr;</a>',
          '<a href="' + newsUrl + '" class="btn bg">&larr; ' + btnLabel2 + '</a>',
        '</div>',
      '</div>',
    '</section>'
  ].join('');

  window.scrollTo(0, 0);
  setTimeout(function () {
    var revs = document.querySelectorAll('.rev,.rev2,.rev3');
    for (var i = 0; i < revs.length; i++) revs[i].classList.add('on');
  }, 80);
}
