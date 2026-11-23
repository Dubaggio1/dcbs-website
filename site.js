// DCBS site.js — gedeelde functionaliteit voor de statische site
(function(){
  'use strict';

  // ---- Consent Mode v2 ----------------------------------------------------
  // Google Ads-tag: vervang AW-XXXXXXXXXX door uw conversie-ID en verwijder de
  // commentaartekens in loadAds() hieronder.
  // ADS_ACTIEF: zolang de Ads-code uit staat, wordt er geen advertentiecookie geplaatst en is er
  // niets om toestemming voor te vragen. De cookiebanner blijft dan verborgen. Zet dit op true
  // op het moment dat loadAds() wordt ingeschakeld, en werk dan ook het privacybeleid bij.
  var ADS_ACTIEF = false;
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('consent', 'default', {
    ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    analytics_storage: 'denied', wait_for_update: 500
  });
  function loadAds(){
    // var s = document.createElement('script');
    // s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX';
    // document.head.appendChild(s);
    // gtag('js', new Date()); gtag('config', 'AW-XXXXXXXXXX');
  }
  function applyConsent(v){
    if (v === 'all') {
      gtag('consent', 'update', { ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted' });
      loadAds();
    }
  }
  var consent = null;
  try { consent = localStorage.getItem('dcbs-consent'); } catch(e){}
  if (consent && ADS_ACTIEF) applyConsent(consent);

  document.addEventListener('DOMContentLoaded', function(){
    // ---- Mobiele opschoning (alleen <=720px; desktop ongewijzigd) ----
    enhanceMobile();

    // ---- Cookiebanner ----
    var banner = document.getElementById('cookie-banner');
    if (banner && ADS_ACTIEF && !consent) banner.style.display = 'flex';
    function choose(v){
      try { localStorage.setItem('dcbs-consent', v); } catch(e){}
      if (banner) banner.style.display = 'none';
      applyConsent(v);
    }
    var acc = document.getElementById('cb-accept'), dec = document.getElementById('cb-decline');
    if (acc) acc.addEventListener('click', function(){ choose('all'); });
    if (dec) dec.addEventListener('click', function(){ choose('functional'); });

    // ---- Data waves (home hero) ----
    var canvas = document.getElementById('waves');
    if (canvas) startWaves(canvas);

    // ---- Nieuws ----
    var lijst = document.getElementById('nieuws-lijst');
    if (lijst) initNieuws(lijst);
    var home = document.getElementById('nieuws-home');
    if (home) initNieuwsHome(home);
    initLeesOok();
  });

  function enhanceMobile(){
    if (window.__dcbsMobile) return; window.__dcbsMobile = true;

    // Stylesheet — uitsluitend voor <=720px; desktop blijft exact ongewijzigd
    var css = document.createElement('style');
    css.textContent =
      '@media(max-width:720px){' +
      ' header{position:relative!important;flex-wrap:nowrap!important;height:auto!important;min-height:56px;padding:10px 20px!important;gap:12px!important}' +
      ' header>a:first-child span{display:none!important}' +
      ' header nav{display:none!important}' +
      ' header nav.dcbs-open{display:flex!important;flex-direction:column;align-items:stretch!important;position:absolute;top:100%;left:0;right:0;margin:0;padding:6px 20px 14px;gap:0!important;z-index:60;box-shadow:0 12px 26px rgba(0,0,0,.16)}' +
      ' header nav.dcbs-open a{width:100%;padding:14px 2px!important;font-size:16px!important;border-top:1px solid rgba(140,140,140,.22)}' +
      ' header nav.dcbs-open a:first-child{border-top:none}' +
      ' .dcbs-burger{display:inline-flex!important}' +
      ' html,body{overflow-x:hidden}' +
      '}';
    document.head.appendChild(css);

    // DOM-mutaties UITSLUITEND op mobiel (<=720px); desktop blijft volledig ongemoeid.
    var mq = window.matchMedia('(max-width:720px)');
    function build(){
      if (window.__dcbsMenuBuilt || !mq.matches) return;
      var header = document.querySelector('header');
      var nav = header && header.querySelector('nav');
      if (!header || !nav) return;
      window.__dcbsMenuBuilt = true;

      // Losse header-CTA's (bijv. "Plan een gesprek") in het menu opnemen
      var logo = header.querySelector('a');
      Array.prototype.slice.call(header.children).forEach(function(el){
        if (el.tagName === 'A' && el !== logo) nav.appendChild(el);
      });

      // Kleuren afleiden van de nav-link (licht op donkere hero, donker op lichte pagina's)
      var link = nav.querySelector('a');
      var col = link ? getComputedStyle(link).color : 'rgb(20,24,26)';
      var m = (col.match(/\d+/g) || [20,24,26]).map(Number);
      var dark = (0.299*m[0] + 0.587*m[1] + 0.114*m[2]) > 150;
      nav.style.setProperty('background', dark ? '#0A3937' : '#FBFAF7', 'important');
      nav.querySelectorAll('a').forEach(function(a){
        if (/background/i.test(a.getAttribute('style') || '')) return; // CTA met eigen achtergrond behoudt eigen kleuren
        a.style.setProperty('color', dark ? '#FBFAF7' : '#14181A', 'important');
      });

      // Hamburgerknop
      var burger = document.createElement('button');
      burger.className = 'dcbs-burger';
      burger.setAttribute('aria-label', 'Menu');
      burger.setAttribute('aria-expanded', 'false');
      burger.style.cssText = 'display:none;flex:none;width:42px;height:42px;align-items:center;justify-content:center;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:0;color:' + col;
      for (var k = 0; k < 3; k++){
        var bar = document.createElement('span');
        bar.style.cssText = 'display:block;width:24px;height:2px;background:currentColor;transition:.2s';
        burger.appendChild(bar);
      }
      function closeMenu(){
        nav.classList.remove('dcbs-open'); burger.setAttribute('aria-expanded','false');
        var b = burger.children; b[0].style.transform=''; b[1].style.opacity=''; b[2].style.transform='';
      }
      burger.addEventListener('click', function(){
        var open = nav.classList.toggle('dcbs-open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        var b = burger.children;
        b[0].style.transform = open ? 'translateY(7px) rotate(45deg)' : '';
        b[1].style.opacity = open ? '0' : '';
        b[2].style.transform = open ? 'translateY(-7px) rotate(-45deg)' : '';
      });
      nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', closeMenu); });
      header.appendChild(burger);
    }
    build();
    if (mq.addEventListener) mq.addEventListener('change', build); else if (mq.addListener) mq.addListener(build);
  }

  function startWaves(canvas){
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5), W = 0, H = 0;
    function resize(){
      var r = canvas.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize);
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var COLS = 150, ROWS = 44;
    function draw(ms){
      var t = ms * 0.00028;
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      for (var r = 0; r < ROWS; r++){
        var z = r / (ROWS - 1);
        var persp = 0.38 + 0.62 * z;
        var rowY = H * (0.40 + 0.68 * z);
        for (var c = 0; c < COLS; c++){
          var u = c / (COLS - 1);
          var x = W * 0.5 + (u - 0.5) * W * 1.18 * persp;
          var env = 0.5 + 0.5 * Math.sin(u * Math.PI) * (0.7 + 0.3 * Math.sin(u * 3.1 + t * 0.4));
          var wave =
            Math.sin(z * 5.5 + t * 2.2 + u * 2.8) * 0.62 +
            Math.sin(z * 9.5 + t * 3.1 + u * 4.6) * 0.2 +
            Math.sin(u * 4.2 - t * 0.7 + z * 1.5) * 0.24;
          wave = wave > 0 ? Math.pow(wave, 1.35) : wave * 0.55;
          var y = rowY - wave * env * H * 0.14 * persp - u * u * H * 0.16 * persp;
          var crest = Math.max(0, wave * env);
          var a = (0.20 + 0.52 * z) * (0.45 + 0.65 * crest);
          var size = (1.0 + 2.2 * z) * (0.8 + 0.7 * crest);
          var g = Math.round(190 + 60 * crest);
          var b = Math.round(200 + 55 * crest);
          ctx.fillStyle = 'rgba(150,' + g + ',' + b + ',' + Math.min(a, 0.95).toFixed(3) + ')';
          ctx.fillRect(x, y, size, size);
        }
      }
      if (!reduced) requestAnimationFrame(draw);
    }
    if (reduced) draw(0); else requestAnimationFrame(draw);
  }

  // ---- Artikeltekst: eenvoudige opmaak naar HTML ---------------------------
  // ## Kop, ### Subkop, - opsomming, 1. genummerd, > citaat, **vet**, *cursief*, [tekst](url),
  // en een afbeelding op een eigen regel: ![bijschrift](/assets/nieuws/...). Dezelfde opmaak
  // gebruikt LinkedIn (kop, subkop, lijsten, citaat), zodat beide versies gelijk zijn.
  function mdEsc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function mdInline(t){
    t = mdEsc(t);
    t = t.replace(/\[([^\]]+)\]\(((?:https?:\/\/|\/|mailto:)[^)\s]+)\)/g, function(m, txt, url){
      var ext = /^https?:/i.test(url) && url.indexOf('dcbs.nl') < 0;
      return '<a href="' + url + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + txt + '</a>';
    });
    t = t.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/(^|[^*])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>');
    return t;
  }
  function mdNaarHtml(src, absoluut){
    var blokken = String(src || '').replace(/\r/g, '').split(/\n\s*\n/), out = [];
    blokken.forEach(function(b){
      b = b.replace(/^\n+|\s+$/g, ''); if (!b) return;
      var regels = b.split('\n'), m;
      if ((m = b.match(/^!\[([^\]]*)\]\(([^)\s]+)\)$/))){
        var src2 = m[2]; if (absoluut && src2.charAt(0) === '/') src2 = 'https://www.dcbs.nl' + src2;
        out.push('<figure><img src="' + mdEsc(src2) + '" alt="' + mdEsc(m[1]) + '" loading="lazy">' + (m[1] ? '<figcaption>' + mdEsc(m[1]) + '</figcaption>' : '') + '</figure>');
      } else if (/^### /.test(b)) out.push('<h3>' + mdInline(b.slice(4)) + '</h3>');
      else if (/^## /.test(b)) out.push('<h2>' + mdInline(b.slice(3)) + '</h2>');
      else if (regels.every(function(r){ return /^[-*] /.test(r); })) out.push('<ul>' + regels.map(function(r){ return '<li>' + mdInline(r.slice(2)) + '</li>'; }).join('') + '</ul>');
      else if (regels.every(function(r){ return /^\d+[.)] /.test(r); })) out.push('<ol>' + regels.map(function(r){ return '<li>' + mdInline(r.replace(/^\d+[.)] /, '')) + '</li>'; }).join('') + '</ol>');
      else if (regels.every(function(r){ return /^> ?/.test(r); })) out.push('<blockquote><p>' + regels.map(function(r){ return mdInline(r.replace(/^> ?/, '')); }).join('<br>') + '</p></blockquote>');
      else out.push('<p>' + regels.map(mdInline).join('<br>') + '</p>');
    });
    return out.join('\n');
  }
  window.DCBS_MD = mdNaarHtml;

  // ---- Nieuws: publieke weergave -------------------------------------------
  // Bron: window.DCBS_ARTICLES uit /nieuws-data.js (bovenaan = nieuwste). Dat bestand wordt beheerd
  // via de nieuwspagina (/nieuws/#beheer), die het via de GitHub-API publiceert; zie initBeheer hieronder.
  function nieuwsEsc(s){ var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
  // ---- Tweetalig: de Engelse pagina's staan onder /en/, met dezelfde paden als de Nederlandse ----
  // Een artikel heeft een Engelse versie als het een veld en = { title, summary } heeft; de Engelse
  // pagina staat dan op /en/nieuws/<slug>/. Onderwerp en datum worden hieronder vertaald.
  var EN = typeof location !== 'undefined' && /^\/en(\/|$)/.test(location.pathname);
  function T(nl, en){ return EN ? en : nl; }
  var MAANDEN_EN = { januari: 'January', februari: 'February', maart: 'March', april: 'April', mei: 'May', juni: 'June', juli: 'July',
    augustus: 'August', september: 'September', oktober: 'October', november: 'November', december: 'December' };
  function datumEn(d){ return String(d || '').replace(/[A-Za-z]+/g, function(w){ return MAANDEN_EN[w.toLowerCase()] || w; }); }
  var CAT_EN = { 'NIS2 / Cyberbeveiligingswet': 'NIS2 / Cybersecurity Act', 'TPRM- en contractmanagement': 'TPRM and contract management' };
  function catEn(c){ return CAT_EN[c] || c; }
  function artikelEn(a){
    var e = { id: a.id, cat: catEn(a.cat), catNl: a.cat, date: datumEn(a.date), link: a.link || '', title: a.en.title, summary: a.en.summary, slug: a.slug, url: '/en' + a.url };
    if (a.img) e.img = a.img;
    if (a.pub) e.pub = a.pub;
    if (a.mod) e.mod = a.mod;
    return e;
  }
  function lijstEn(list){ return list.filter(function(a){ return a.en && a.url && a.url.charAt(0) === '/'; }).map(artikelEn); }
  function alleArtikelen(){ var l = window.DCBS_ARTICLES || []; return EN ? lijstEn(l) : l; }

  // ---- Nieuws: statische versie voor zoekmachines ---------------------------
  // De artikellijst staat ook als gewone HTML in /nieuws/index.html en /index.html (tussen de
  // markeringen hieronder) en de artikelpagina's staan in /sitemap.xml. Zo vinden zoekmachines en
  // AI-crawlers die geen JavaScript uitvoeren de artikelen ook. Het beheer werkt die drie bestanden
  // bij na elke publicatie (zie werkStatischBij). De functies hieronder maken exact dezelfde HTML
  // als de bezoeker te zien krijgt, zodat er maar één bron voor de opmaak is.
  var ST_START = '<!--nieuws:statisch-->', ST_EIND = '<!--/nieuws:statisch-->';
  var SM_START = '<!--artikelen-->', SM_EIND = '<!--/artikelen-->';
  function vervangTussen(tekst, start, eind, inhoud){
    var a = tekst.indexOf(start), b = tekst.indexOf(eind);
    if (a < 0 || b < a) return null;   // markering ontbreekt: bestand ongemoeid laten
    return tekst.slice(0, a + start.length) + inhoud + tekst.slice(b);
  }
  function nieuwsRij(a, i, n, knoppen){
    var esc = mdEsc;
    var top = i === 0 ? '#14181A' : '#E2DFD6';
    var bottom = i === n - 1 ? ';border-bottom:1px solid #E2DFD6' : '';
    var dest = a.url || a.link;
    var isExt = dest && /^https?:/i.test(dest);
    var href = dest ? ' href="' + esc(dest) + '"' + (isExt ? ' target="_blank" rel="noopener"' : '') : '';
    var media = a.img
      ? '<img src="' + esc(a.img) + '" alt="" loading="lazy" style="width:320px;max-width:100%;height:190px;object-fit:contain;background:#F4F7FB;border:1px solid #E4E8EF;border-radius:12px">'
      : '<div style="width:320px;max-width:100%;height:190px;background:linear-gradient(135deg,#E9E5DA,#DDD8CA)"></div>';
    return '<div style="position:relative">' +
      '<a' + href + ' style="display:grid;grid-template-columns:minmax(200px,320px) minmax(0,1fr) 110px;gap:44px;align-items:center;padding:36px 0;border-top:1px solid ' + top + bottom + ';color:#14181A" class="nieuwsrij">' +
      media +
      '<span><span style="display:block;font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:#0E5654">' + esc(a.cat) + '</span>' +
      '<span style="display:block;font-family:\'Petrona\',Georgia,serif;font-size:29px;line-height:1.22;margin-top:12px">' + esc(a.title) + '</span>' +
      '<span style="display:block;font-size:14px;line-height:1.6;color:#4E5552;margin-top:12px;max-width:64ch">' + esc(a.summary) + '</span></span>' +
      '<span style="font-size:12.5px;color:#6B716E;text-align:right">' + esc(a.date) + '</span></a>' +
      (knoppen || '') + '</div>';
  }
  function nieuwsLijstHtml(list){ return list.map(function(a, i){ return nieuwsRij(a, i, list.length, ''); }).join(''); }
  function nieuwsKaart(a){   // kaart op de homepage (v6-stijl); /assets/js/v6.js gebruikt deze functie ook
    var esc = mdEsc, dest = a.url || a.link, ext = dest && /^https?:/i.test(dest);
    var open = dest ? '<a class="card" href="' + esc(dest) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') : '<div class="card"';
    var close = dest ? '</a>' : '</div>';
    var media = a.img ? '<img src="' + esc(a.img) + '" alt="" loading="lazy" style="width:100%;height:220px;object-fit:contain;background:#F4F7FB;display:block;border-bottom:1px solid #E4E8EF">' : '<div class="bar"></div>';
    return open + ' style="flex:1 1 300px;display:flex;flex-direction:column">' + media +
      '<div style="padding:26px 28px;display:flex;flex-direction:column;gap:12px;flex:1">' +
      '<span class="chip" style="align-self:flex-start">' + esc(a.cat) + '</span>' +
      '<h3 style="font-size:21px">' + esc(a.title) + '</h3>' +
      '<span class="mut" style="font-size:13px;margin-top:auto">' + esc(a.date) + '</span></div>' + close;
  }
  function nieuwsHomeHtml(list){ return list.slice(0, 3).map(nieuwsKaart).join(''); }
  // Sitemap: alleen artikelen met een eigen pagina op de site. mod/pub = datum (jjjj-mm-dd).
  function sitemapArtikelen(list){
    return '\n' + list.filter(function(a){ return a.url && a.url.charAt(0) === '/'; }).map(function(a){
      var d = a.mod || a.pub, lm = d ? '<lastmod>' + mdEsc(d) + '</lastmod>' : '';
      return '  <url><loc>https://www.dcbs.nl' + mdEsc(a.url) + '</loc>' + lm + '</url>\n' +
        (a.en ? '  <url><loc>https://www.dcbs.nl/en' + mdEsc(a.url) + '</loc>' + lm + '</url>\n' : '');
    }).join('') + '  ';
  }
  // Structured data (schema.org) voor een artikelpagina. Komt in het sjabloon op de plek van <!--JSONLD-->.
  function artikelJsonLd(item, lang){   // item = het artikel in de taal van de pagina (voor Engels: artikelEn(a))
    var en = lang === 'en', basis = 'https://www.dcbs.nl' + (en ? '/en' : '');
    var url = basis + '/nieuws/' + item.slug + '/', org = 'https://www.dcbs.nl/#organisatie';
    var art = { '@type': 'Article', '@id': url + '#artikel', headline: item.title, description: item.summary, inLanguage: en ? 'en' : 'nl-NL',
      mainEntityOfPage: url, articleSection: item.cat,
      author: { '@type': 'Person', name: 'Jeroen Dubach', url: basis + '/over-ons/' },
      publisher: { '@type': 'Organization', '@id': org, name: 'The Data Compliance Builders',
        logo: { '@type': 'ImageObject', url: 'https://www.dcbs.nl/assets/dcbs-logo-full.png' } } };
    if (item.img) art.image = ['https://www.dcbs.nl' + item.img];
    if (item.pub) art.datePublished = item.pub;
    if (item.mod) art.dateModified = item.mod;
    var kruimel = { '@type': 'BreadcrumbList', itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: basis + '/' },
      { '@type': 'ListItem', position: 2, name: en ? 'News' : 'Nieuws', item: basis + '/nieuws/' },
      { '@type': 'ListItem', position: 3, name: item.title, item: url } ] };
    return '<script type="application/ld+json" id="ld-dcbs">' +
      JSON.stringify({ '@context': 'https://schema.org', '@graph': [art, kruimel] }).replace(/</g, '\\u003c') + '</' + 'script>';
  }
  // Artikelpagina maken uit het sjabloon (/nieuws/_template.html of /en/nieuws/_template.html).
  // tweetalig = er bestaat ook een pagina in de andere taal: dan komen de hreflang-verwijzingen erin
  // en wijst de taalwissel in de kop naar het artikel zelf in plaats van naar het overzicht.
  // De plekken <!--JSONLD--> en <!--HREFLANG--> zijn commentaren, zodat een browser met een oudere
  // site.js in de cache hooguit een onzichtbaar commentaar laat staan.
  function artikelPagina(tpl, item, md, lang, tweetalig){
    var e = mdEsc, en = lang === 'en', pad = '/nieuws/' + item.slug + '/', url = 'https://www.dcbs.nl' + (en ? '/en' : '') + pad;
    var cover = item.img ? '<figure class="cover"><img src="' + e(item.img) + '" alt=""></figure>' : '';
    var og = item.img ? 'https://www.dcbs.nl' + item.img : 'https://www.dcbs.nl/assets/dcbs-logo-full.png';
    var lk = item.link ? '<a href="' + e(item.link) + '" target="_blank" rel="noopener">LinkedIn</a>' : '';
    var li = item.link ? '<p class="mut" style="margin-top:32px;font-size:15px">' + (en ? 'Also published on ' + lk + ' (in Dutch).' : 'Ook verschenen op ' + lk + '.') + '</p>' : '';
    var hreflang = tweetalig
      ? '<link rel="alternate" hreflang="nl" href="https://www.dcbs.nl' + pad + '">\n<link rel="alternate" hreflang="en" href="https://www.dcbs.nl/en' + pad + '">\n<link rel="alternate" hreflang="x-default" href="https://www.dcbs.nl' + pad + '">'
      : '';
    var vervang = { TITLE: e(item.title), DESC: e(item.summary), URL: url, OGIMG: e(og), CAT: e(item.cat), DATE: e(item.date), COVER: cover, BODY: mdNaarHtml(md) + li };
    var html = tpl.replace(/\{\{(TITLE|DESC|URL|OGIMG|CAT|DATE|COVER|BODY)\}\}/g, function(m, k){ return vervang[k]; })
      .replace('<!--JSONLD-->', function(){ return artikelJsonLd(item, lang); })
      .replace('<!--HREFLANG-->', function(){ return hreflang; });
    if (tweetalig) html = html.replace(/href="((?:\/en)?\/nieuws\/)"([^>]*\bdata-taal\b)/g, function(m, basis, rest){ return 'href="' + basis + item.slug + '/"' + rest; });
    return html;
  }
  window.DCBS_STATISCH = { rij: nieuwsRij, lijst: nieuwsLijstHtml, kaart: nieuwsKaart, home: nieuwsHomeHtml,
    artikelen: alleArtikelen, leesOok: leesOokHtml, lijstEn: lijstEn, artikelEn: artikelEn, catEn: catEn, datumEn: datumEn, pagina: artikelPagina, md: mdNaarHtml,
    sitemap: sitemapArtikelen, artikelJsonLd: artikelJsonLd, vervangTussen: vervangTussen,
    ST_START: ST_START, ST_EIND: ST_EIND, SM_START: SM_START, SM_EIND: SM_EIND };

  // Homepage: de 3 nieuwste artikelen, zelfde bron en volgorde als de nieuwspagina.
  // Zonder artikelen blijft de hele sectie (#nieuws-sectie) verborgen.
  // Een artikel zonder link (bijv. LinkedIn-URL nog niet ingevuld) wordt als niet-klikbare kaart getoond.
  function initNieuwsHome(grid){
    var sectie = document.getElementById('nieuws-sectie');
    var items = alleArtikelen().slice(0, 3);
    if (!items.length){ if (sectie) sectie.style.display = 'none'; return; }
    if (sectie) sectie.style.display = '';
    grid.innerHTML = items.map(function(a){
      var dest = a.url || a.link;
      var isExt = dest && /^https?:/i.test(dest);
      var media = a.img
        ? '<img src="' + nieuwsEsc(a.img) + '" alt="" loading="lazy" style="width:100%;height:250px;object-fit:cover;background:#E9E5DA">'
        : '<div style="width:100%;height:250px;background:linear-gradient(135deg,#E9E5DA,#DDD8CA)"></div>';
      return '<a' + (dest ? ' href="' + nieuwsEsc(dest) + '"' + (isExt ? ' target="_blank" rel="noopener"' : '') + ' class="hv7"' : '') +
        ' style="color:#14181A;display:flex;flex-direction:column;min-width:0">' +
        media +
        '<div style="display:flex;justify-content:space-between;font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:#0E5654;margin-top:20px"><span>' + nieuwsEsc(a.cat) + '</span><span style="color:#8E938F">' + nieuwsEsc(a.date) + '</span></div>' +
        '<div style="font-family:\'Petrona\',Georgia,serif;font-size:24px;line-height:1.25;margin-top:12px">' + nieuwsEsc(a.title) + '</div>' +
        '</a>';
    }).join('');
  }

  // ---- Onderwerpen: vaste volgorde (gelijk aan de diensten) en de dienstpagina die erbij hoort ----
  var NIEUWS_CATS = [
    ['Privacy compliance', '/diensten/avg-compliance/'],
    ['AI compliance', '/diensten/ai-act-compliance/'],
    ['NIS2 / Cyberbeveiligingswet', '/diensten/nis2/'],
    ['Information security', '/diensten/information-security/'],
    ['Quantum-readiness', '/diensten/quantum-readiness/'],
    ['DPO-as-a-Service', '/diensten/dpo-as-a-service/'],
    ['Privacy Officer as a Service', '/diensten/privacy-officer-as-a-service/'],
    ['Security Officer as a Service', '/diensten/security-officer-as-a-service/'],
    ['TPRM- en contractmanagement', '/diensten/tprm-contractmanagement/']
  ];
  function catVolgorde(cat){ for (var i = 0; i < NIEUWS_CATS.length; i++) if (NIEUWS_CATS[i][0] === cat || catEn(NIEUWS_CATS[i][0]) === cat) return i; return 99; }
  function catSlug(cat){ return String(cat || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
  (function(){
    var st = document.createElement('style');
    st.textContent =
      '#nieuws-filter{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}' +
      '.nf{font-family:inherit;font-size:14px;font-weight:600;line-height:1;color:#0B1F3A;background:#fff;border:1.5px solid #CBD3E1;border-radius:999px;padding:10px 16px;min-height:40px;cursor:pointer;transition:background .2s,border-color .2s,color .2s}' +
      '.nf span{font-weight:500;color:#6B7890;margin-left:4px}' +
      '.nf:hover{border-color:#1F4FD1;color:#1F4FD1}' +
      '.nf.aan{background:#0B1F3A;border-color:#0B1F3A;color:#fff}.nf.aan span{color:#B9C4D6}' +
      '.leesook{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:36px}' +
      '@media (max-width:980px){.leesook{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:620px){.leesook{grid-template-columns:1fr}}' +
      '.leesook a{display:flex;flex-direction:column;color:#0B1F3A}' +
      '.leesook img{width:100%;aspect-ratio:1200/627;object-fit:cover;background:#F4F7FB;border-bottom:1px solid #E4E8EF}' +
      '.leesook .lo-t{padding:20px 22px 24px;display:flex;flex-direction:column;gap:10px}' +
      '.leesook .lo-d{font-size:12.5px;color:#6B7890}' +
      '.leesook .lo-k{font-size:19px;font-weight:800;line-height:1.25;letter-spacing:-.015em}' +
      '@media (max-width:760px){#nieuws-filter{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:6px;margin-right:-20px;padding-right:20px}.nf{flex:0 0 auto}}';
    document.head.appendChild(st);
  })();

  // ---- Dienstpagina's: "Lees ook" met de nieuwste artikelen over dat onderwerp ----------------
  // Zonder artikelen over het onderwerp verschijnt er niets. Staat boven het kennismakingsblok.
  // Inhoud van het blok "Lees ook" op een dienstpagina: de drie nieuwste artikelen over die dienst.
  // lijst = de artikelen in de taal van de pagina; cat = de Nederlandse naam van de dienst.
  // Het bouwscript zet dezelfde HTML alvast in de pagina, zodat zoekmachines de links ook zien.
  function leesOokHtml(cat, lijst, en){
    var t = function(nl, e){ return en ? e : nl; }, e = mdEsc;
    var alleCat = lijst.filter(function(a){ return (a.catNl || a.cat) === cat; });
    var items = alleCat.filter(function(a){ return a.url || a.link; }).slice(0, 3);   // alleen artikelen die ergens naartoe gaan
    if (!items.length) return '';
    var meer = alleCat.length > items.length;
    return '<div class="wrap pad"><div style="display:flex;flex-wrap:wrap;gap:16px 32px;justify-content:space-between;align-items:flex-end">' +
      '<div><div class="kick">' + t('Lees ook', 'Read more') + '</div><h2 style="margin-top:16px">' + t('Artikelen over dit onderwerp', 'Articles on this topic') + '</h2></div>' +
      '<a class="b b-o" href="' + t('/nieuws/', '/en/nieuws/') + (meer ? '?onderwerp=' + encodeURIComponent(catSlug(t(cat, catEn(cat)))) : '') + '">' +
      (meer ? t('Alle ' + alleCat.length + ' artikelen', 'All ' + alleCat.length + ' articles') : t('Alle artikelen', 'All articles')) + '</a></div>' +
      '<div class="leesook">' + items.map(function(a){
        var dest = a.url || a.link, ext = /^https?:/i.test(dest);
        return '<a class="card" href="' + e(dest) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' +
          (a.img ? '<img src="' + e(a.img) + '" alt="" loading="lazy">' : '') +
          '<span class="lo-t"><span class="lo-d">' + e(a.date) + '</span><span class="lo-k">' + e(a.title) + '</span></span></a>';
      }).join('') + '</div></div>';
  }
  function initLeesOok(){
    var pad = location.pathname.replace(/index\.html$/, '').replace(/^\/en(?=\/)/, '');   // Engelse pagina's: zelfde pad onder /en/
    if (pad.charAt(pad.length - 1) !== '/') pad += '/';
    var cat = '';
    NIEUWS_CATS.forEach(function(c){ if (c[1] === pad) cat = c[0]; });
    if (pad === '/diensten/leveranciersrisico-as-a-service/') cat = 'TPRM- en contractmanagement';
    if (!cat) return;
    function toon(){
      var html = leesOokHtml(cat, alleArtikelen(), EN);
      var sec = document.getElementById('lees-ook');   // staat al in de pagina (statische versie): verversen
      if (sec){ if (html) sec.innerHTML = html; else sec.parentNode.removeChild(sec); return; }
      if (!html) return;
      var secties = document.querySelectorAll('section');
      var cta = secties[secties.length - 1];
      if (!cta || !cta.parentNode) return;
      sec = document.createElement('section');
      sec.id = 'lees-ook';
      sec.style.background = '#F4F7FB';
      sec.style.marginBottom = 'clamp(40px,6vw,88px)';
      sec.innerHTML = html;
      cta.parentNode.insertBefore(sec, cta);
    }
    if (window.DCBS_ARTICLES) return toon();
    var sc = document.createElement('script');
    sc.src = '/nieuws-data.js';
    sc.onload = toon;
    document.head.appendChild(sc);
  }

  function initNieuws(lijst){
    var esc = nieuwsEsc;
    var publiek = alleArtikelen();
    var beheer = null;        // { items, sha } zodra de beheerder de lijst uit GitHub heeft geladen
    var beheerOpen = false;   // beheerpaneel open: toon bewerk-/verwijderknoppen

    function rij(a, i, n){
      var dest = a.url || a.link;
      var knoppen = beheerOpen
        ? '<span style="position:absolute;top:36px;right:0;display:flex;gap:8px">' +
          (dest ? '<button type="button" data-copy="' + esc(/^https?:/i.test(dest) ? dest : 'https://www.dcbs.nl' + dest) + '" style="font-family:Inter,sans-serif;font-size:12px;font-weight:600;color:#fff;background:#1F4FD1;border:1px solid #1F4FD1;border-radius:999px;padding:6px 14px;cursor:pointer">Kopieer link</button>' : '') +
          '<button type="button" data-edit="' + esc(a.id) + '" style="font-family:Archivo,sans-serif;font-size:12px;color:#0E5654;background:#FBFAF7;border:1px solid #A9C4C1;padding:6px 12px;cursor:pointer">Bewerken</button>' +
          '<button type="button" data-del="' + esc(a.id) + '" style="font-family:Archivo,sans-serif;font-size:12px;color:#8E938F;background:#FBFAF7;border:1px solid #D6D2C6;padding:6px 12px;cursor:pointer">Verwijderen</button></span>'
        : '';
      return nieuwsRij(a, i, n, knoppen);
    }
    // ---- Filter op onderwerp: de lijst blijft op datum, de knoppen tonen alleen onderwerpen met artikelen.
    // Ook bereikbaar via /nieuws/?onderwerp=<slug>, zodat dienstpagina's naar hun eigen artikelen linken.
    var filterCat = '';
    var balk = document.createElement('div');
    balk.id = 'nieuws-filter';
    balk.setAttribute('role', 'group');
    balk.setAttribute('aria-label', T('Filter op onderwerp', 'Filter by topic'));
    lijst.parentNode.insertBefore(balk, lijst);
    (function(){
      var m = /[?&]onderwerp=([^&#]+)/.exec(location.search);
      if (!m) return;
      var gezocht = decodeURIComponent(m[1]);
      alleArtikelen().forEach(function(a){ if (catSlug(a.cat) === gezocht) filterCat = a.cat; });
    })();
    function renderFilter(alle){
      var telling = {}, cats = [];
      alle.forEach(function(a){ if (!a.cat) return; if (!telling[a.cat]){ telling[a.cat] = 0; cats.push(a.cat); } telling[a.cat]++; });
      cats.sort(function(x, y){ return catVolgorde(x) - catVolgorde(y); });
      if (filterCat && !telling[filterCat]) filterCat = '';
      if (cats.length < 2){ balk.innerHTML = ''; balk.style.display = 'none'; return; }
      balk.style.display = '';
      function knop(cat, label, n){
        var aan = filterCat === cat;
        return '<button type="button" class="nf' + (aan ? ' aan' : '') + '" data-cat="' + esc(cat) + '" aria-pressed="' + (aan ? 'true' : 'false') + '">' + esc(label) + ' <span>' + n + '</span></button>';
      }
      balk.innerHTML = knop('', T('Alles', 'All'), alle.length) + cats.map(function(c){ return knop(c, c, telling[c]); }).join('');
    }
    balk.addEventListener('click', function(e){
      var b = e.target.closest ? e.target.closest('button[data-cat]') : null;
      if (!b) return;
      filterCat = b.getAttribute('data-cat') || '';
      try {
        var u = location.pathname + (filterCat ? '?onderwerp=' + encodeURIComponent(catSlug(filterCat)) : '') + location.hash;
        history.replaceState(null, '', u);
      } catch(err){}
      render();
    });

    function render(){
      var alle = beheer ? beheer.items : publiek;
      renderFilter(alle);
      var list = filterCat ? alle.filter(function(a){ return a.cat === filterCat; }) : alle;
      if (!list.length){
        lijst.innerHTML = '<p style="font-family:\'Petrona\',Georgia,serif;font-size:24px;line-height:1.4;color:#4E5552;margin:0;padding:36px 0;border-top:1px solid #14181A">' + T('Er zijn nog geen artikelen gepubliceerd. Nieuwe artikelen verschijnen hier automatisch.', 'No articles have been published yet. New articles will appear here automatically.') + '</p>';
        return;
      }
      lijst.innerHTML = list.map(function(a, i){ return rij(a, i, list.length); }).join('');
    }
    render();
    initBeheer();

    // ---- Beheer: toevoegen, bewerken, verwijderen; publiceert rechtstreeks naar GitHub ------------
    // Zichtbaar via /nieuws/#beheer of zodra er een token in deze browser staat. Het token is een
    // fine-grained GitHub-token met alleen 'Contents: read and write' op de repository van de site.
    function initBeheer(){
      var REPO = 'Dubaggio1/dcbs-website', BRANCH = 'main', DATAPAD = 'nieuws-data.js', TOKENKEY = 'dcbs-github-token';
      var API = window.DCBS_GITHUB_API || 'https://api.github.com';
      var $ = function(id){ return document.getElementById(id); };
      var knop = $('beheer-knop'), paneel = $('beheer-paneel'), login = $('beheer-login'), werk = $('beheer-werk'),
          status = $('beheer-status'), form = $('artikel-form'), formtitel = $('beheer-formtitel'), uitloggen = $('beheer-uitloggen'),
          tokenInput = $('beheer-token'), tokenOpslaan = $('beheer-token-opslaan'), annuleren = $('artikel-annuleren');
      if (!knop || !paneel || !form) return;
      function fld(n){ return form.querySelector('[name="' + n + '"]'); }
      function token(){ try { return localStorage.getItem(TOKENKEY) || ''; } catch(e){ return ''; } }
      function setToken(t){ try { if (t) localStorage.setItem(TOKENKEY, t); else localStorage.removeItem(TOKENKEY); } catch(e){} }
      if (location.hash !== '#beheer' && !token()) return;   // bezoekers zien niets van het beheer
      knop.style.display = '';

      function melding(t, isFout){ if (status){ status.textContent = t || ''; status.style.color = isFout ? '#A33A2A' : '#0E5654'; } }
      function fout(e){ melding('Mislukt: ' + (e && e.message ? e.message : e), true); }
      function bezig(b){
        form.querySelectorAll('button, input, select, textarea').forEach(function(el){ el.disabled = b; });
        lijst.querySelectorAll('button[data-edit],button[data-del]').forEach(function(el){ el.disabled = b; });
      }
      function slug(s){ return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60).replace(/-[^-]*$/, function(m, i, all){ return all.length >= 60 ? '' : m; }) || 'artikel'; }
      function b64enc(str){ return btoa(unescape(encodeURIComponent(str))); }
      function b64dec(b){ return decodeURIComponent(escape(atob(String(b).replace(/\s/g, '')))); }
      function parseData(src){
        try { return new Function('window', src + '\nreturn window.DCBS_ARTICLES || [];')({}) || []; }
        catch(e){ throw new Error('nieuws-data.js kon niet gelezen worden (' + e.message + ')'); }
      }
      function serialize(list){
        return '// DCBS nieuwsartikelen — beheerd via https://www.dcbs.nl/nieuws/#beheer (niet met de hand bewerken).\n' +
               '// Bovenaan = nieuwste. cat = een van de diensten. url = artikelpagina op de site. link = LinkedIn-post (optioneel). img = omslagafbeelding.\n' +
               '// en = Engelse titel en samenvatting (de Engelse pagina staat op /en + url). pub/mod = datum van publicatie en laatste wijziging.\n' +
               'window.DCBS_ARTICLES = [\n' + list.map(function(a){ return '  ' + JSON.stringify(a); }).join(',\n') + '\n];\n';
      }
      function api(method, pad, body){
        var url = API + '/repos/' + REPO + '/contents/' + pad + (method === 'GET' ? '?ref=' + BRANCH + '&t=' + Date.now() : '');
        return fetch(url, {
          method: method,
          headers: { 'Authorization': 'Bearer ' + token(), 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json' },
          body: body ? JSON.stringify(body) : undefined
        }).then(function(r){
          if (r.status === 404 && method === 'GET') return null;
          return r.text().then(function(t){
            var j = null; try { j = t ? JSON.parse(t) : null; } catch(e){}
            if (!r.ok){
              if (r.status === 401) throw new Error('token ongeldig of verlopen (401)');
              if (r.status === 409) throw new Error('de lijst is intussen elders gewijzigd; laad opnieuw (409)');
              throw new Error((j && j.message) || ('HTTP ' + r.status));
            }
            return j;
          });
        });
      }
      function laad(){
        melding('Laden…');
        return api('GET', DATAPAD).then(function(j){
          beheer = j ? { items: parseData(b64dec(j.content)), sha: j.sha } : { items: [], sha: null };
          render(); melding('');
        });
      }
      function publiceer(list, message){
        var body = { message: message, content: b64enc(serialize(list)), branch: BRANCH };
        if (beheer && beheer.sha) body.sha = beheer.sha;
        return api('PUT', DATAPAD, body).then(function(j){
          beheer = { items: list, sha: j && j.content ? j.content.sha : null };
          render();
        });
      }
      function uploadAfbeelding(file, naam){
        return new Promise(function(res, rej){
          var r = new FileReader();
          r.onload = function(){ res(String(r.result).split(',')[1]); };
          r.onerror = function(){ rej(new Error('afbeelding kon niet gelezen worden')); };
          r.readAsDataURL(file);
        }).then(function(b64){
          var ext = (file.name.match(/\.([a-z0-9]+)$/i) || [0, 'jpg'])[1].toLowerCase().replace('jpeg', 'jpg');
          var pad = 'assets/nieuws/' + slug(naam) + '-' + Date.now().toString(36) + '.' + ext;
          return api('PUT', pad, { message: 'Nieuws: afbeelding ' + pad, content: b64, branch: BRANCH }).then(function(){ return '/' + pad; });
        });
      }
      function verwijderAfbeelding(pad){   // alleen eigen bestanden onder /assets/nieuws/, fouten negeren
        if (!pad || pad.indexOf('/assets/nieuws/') !== 0) return Promise.resolve();
        var p = pad.slice(1);
        return api('GET', p).then(function(j){
          if (j && j.sha) return api('DELETE', p, { message: 'Nieuws: afbeelding verwijderd ' + p, sha: j.sha, branch: BRANCH });
        }).catch(function(){});
      }

      // ---- Volledige artikelen op de site: nieuws/<slug>/index.html + artikel.md ----
      function sha(pad){ return api('GET', pad).then(function(j){ return j && j.sha ? j.sha : null; }); }
      function zetBestand(pad, inhoud, bericht){
        return sha(pad).then(function(s){
          var body = { message: bericht, content: b64enc(inhoud), branch: BRANCH }; if (s) body.sha = s;
          return api('PUT', pad, body);
        });
      }
      function verwijderBestand(pad, bericht){
        return sha(pad).then(function(s){ if (s) return api('DELETE', pad, { message: bericht, sha: s, branch: BRANCH }); }).catch(function(){});
      }
      function vrijeSlug(basis, eigen){
        if (eigen) return Promise.resolve(eigen);
        var probeer = function(n){
          var sl = basis + (n ? '-' + (n + 1) : '');
          return sha('nieuws/' + sl + '/index.html').then(function(s){ return s ? probeer(n + 1) : sl; });
        };
        return probeer(0);
      }
      function bouwPagina(item, md, lang, tweetalig){
        var bron = (lang === 'en' ? '/en' : '') + '/nieuws/_template.html';
        return fetch(bron + '?t=' + Date.now()).then(function(r){
          if (!r.ok) throw new Error('artikelsjabloon ontbreekt (' + bron + ')');
          return r.text();
        }).then(function(tpl){ return artikelPagina(tpl, lang === 'en' ? artikelEn(item) : item, md, lang, tweetalig); });
      }
      // ---- Statische artikellijsten en sitemap bijwerken (voor zoekmachines) ----
      // Na elke publicatie, bewerking of verwijdering. Eén bestand tegelijk, zodat GitHub geen
      // conflicten meldt. Lukt dit niet, dan staat het artikel wel gewoon op de site; alleen de
      // statische lijst loopt dan achter tot de volgende publicatie.
      function werkBlokBij(pad, start, eind, inhoud, bericht){
        return api('GET', pad).then(function(j){
          if (!j || !j.content) return;
          var oud = b64dec(j.content), nieuw = vervangTussen(oud, start, eind, inhoud);
          if (nieuw === null || nieuw === oud) return;
          return api('PUT', pad, { message: bericht, content: b64enc(nieuw), sha: j.sha, branch: BRANCH });
        });
      }
      function werkStatischBij(list){
        return werkBlokBij('nieuws/index.html', ST_START, ST_EIND, nieuwsLijstHtml(list), 'Nieuws: statische artikellijst bijgewerkt')
          .then(function(){ return werkBlokBij('index.html', ST_START, ST_EIND, nieuwsHomeHtml(list), 'Nieuws: artikelen op homepage bijgewerkt'); })
          .then(function(){ return werkBlokBij('en/nieuws/index.html', ST_START, ST_EIND, nieuwsLijstHtml(lijstEn(list)), 'Nieuws: Engelse artikellijst bijgewerkt'); })
          .then(function(){ return werkBlokBij('en/index.html', ST_START, ST_EIND, nieuwsHomeHtml(lijstEn(list)), 'Nieuws: artikelen op Engelse homepage bijgewerkt'); })
          .then(function(){ return werkBlokBij('sitemap.xml', SM_START, SM_EIND, sitemapArtikelen(list), 'Nieuws: sitemap bijgewerkt'); })
          .then(function(){ return true; }, function(){ return false; });
      }
      var bodyVeld = form.querySelector('[name="body"]'), voorbeeld = $('artikel-voorbeeld');
      function invoegen(tekst){
        if (!bodyVeld) return;
        var a = bodyVeld.selectionStart || bodyVeld.value.length, v = bodyVeld.value;
        var voor = v.slice(0, a).replace(/\s*$/, ''), na = v.slice(a).replace(/^\s*/, '');
        bodyVeld.value = (voor ? voor + '\n\n' : '') + tekst + (na ? '\n\n' + na : '\n\n');
        bodyVeld.focus();
      }
      // Plakken met opmaak: tekst uit een document (Claude, Word, Google Docs) of van LinkedIn
      // wordt omgezet naar de opmaak hierboven. Een kop 1 bovenaan wordt de titel.
      function htmlNaarMd(html){
        var doc = new DOMParser().parseFromString(html, 'text/html'), titel = '';
        function inl(n){
          if (n.nodeType === 3) return n.nodeValue.replace(/\s+/g, ' ');
          if (n.nodeType !== 1) return '';
          var t = n.tagName.toLowerCase(), st = (n.getAttribute('style') || '').toLowerCase();
          var kind = Array.prototype.map.call(n.childNodes, inl).join('');
          if (t === 'br') return '\n';
          if (t === 'img'){ var src = n.getAttribute('src') || ''; return /^(https?:|\/)/.test(src) ? '\n\n![' + (n.getAttribute('alt') || '') + '](' + src + ')\n\n' : ''; }
          if (!kind.trim()) return kind;
          var lead = kind.match(/^\s*/)[0], trail = kind.match(/\s*$/)[0], kern = kind.trim();
          if (t === 'a' && /^(https?:|mailto:|\/)/.test(n.getAttribute('href') || '')) return lead + '[' + kern + '](' + n.getAttribute('href') + ')' + trail;
          var vet = t === 'strong' || t === 'b' || /font-weight:\s*(bold|[6-9]00)/.test(st);
          var cur = t === 'em' || t === 'i' || /font-style:\s*italic/.test(st);
          if (t === 'b' && /font-weight:\s*normal/.test(st)) vet = false;   // Google Docs-omhulsel
          if (vet && cur) return lead + '***' + kern + '***' + trail;
          if (vet) return lead + '**' + kern + '**' + trail;
          if (cur) return lead + '*' + kern + '*' + trail;
          return kind;
        }
        function schoon(t){ return t.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim(); }
        var uit = [];
        function blok(n){
          if (n.nodeType === 3){ var tx = n.nodeValue.trim(); if (tx) uit.push(tx); return; }
          if (n.nodeType !== 1) return;
          var t = n.tagName.toLowerCase();
          if (t === 'h1'){ var h = schoon(inl(n)); if (!titel && !uit.length) titel = h.replace(/\*/g, ''); else uit.push('## ' + h.replace(/\*\*/g, '')); return; }
          if (t === 'h2'){ uit.push('## ' + schoon(inl(n)).replace(/\*\*/g, '')); return; }
          if (t === 'h3'){ uit.push('### ' + schoon(inl(n)).replace(/\*\*/g, '')); return; }
          if (t === 'h4' || t === 'h5' || t === 'h6'){ uit.push('#### ' + schoon(inl(n)).replace(/\*\*/g, '')); return; }
          if (t === 'ul' || t === 'ol'){
            var i = 0;
            Array.prototype.forEach.call(n.children, function(li){
              if (li.tagName.toLowerCase() !== 'li') return; i++;
              uit.push((t === 'ol' ? i + '. ' : '- ') + schoon(inl(li)).replace(/\n+/g, ' '));
            });
            uit.push(''); return;
          }
          if (t === 'blockquote'){ uit.push(schoon(inl(n)).split('\n').map(function(r){ return '> ' + r; }).join('\n')); return; }
          if (t === 'hr'){ return; }
          if (t === 'p' || t === 'figure' || t === 'figcaption' || t === 'pre'){ var p = schoon(inl(n)); if (p) uit.push(p); return; }
          var heeftBlok = n.querySelector && n.querySelector('p,h1,h2,h3,h4,ul,ol,blockquote,figure,div,table');
          if (heeftBlok){ Array.prototype.forEach.call(n.childNodes, blok); return; }
          var r = schoon(inl(n)); if (r) uit.push(r);
        }
        Array.prototype.forEach.call(doc.body.childNodes, blok);
        // Kopniveaus gelijktrekken: het hoogste kopniveau in de tekst wordt ##, het niveau daaronder ###.
        // Een kop helemaal bovenaan (voor de eerste alinea) is de titel en gaat niet mee in de tekst.
        while (uit.length && /^#{2,4} /.test(uit[0])){ if (!titel) titel = uit[0].replace(/^#+ /, '').replace(/\*/g, ''); uit.shift(); }
        var niveaus = uit.filter(function(b){ return /^#{2,4} /.test(b); }).map(function(b){ return b.match(/^#+/)[0].length; });
        var verschuif = niveaus.length ? Math.min.apply(null, niveaus) - 2 : 0;
        uit = uit.map(function(b){
          var m = b.match(/^(#{2,4}) /); if (!m) return b;
          var n = Math.max(2, Math.min(3, m[1].length - verschuif));
          return new Array(n + 1).join('#') + b.slice(m[0].length - 1);
        });
        // lijstregels bij elkaar houden, andere blokken met een witregel scheiden
        var md = '';
        uit.forEach(function(b, k){
          if (b === '') { md += '\n'; return; }
          var lijst = /^(- |\d+\. )/.test(b), vorigeLijst = k > 0 && /^(- |\d+\. )/.test(uit[k - 1]);
          md += (md ? (lijst && vorigeLijst ? '\n' : '\n\n') : '') + b;
        });
        return { titel: titel, md: md.replace(/\n{3,}/g, '\n\n').trim() };
      }
      if (bodyVeld) bodyVeld.addEventListener('paste', function(e){
        var cd = e.clipboardData, html = cd && cd.getData('text/html'), plat = cd ? cd.getData('text/plain') : '';
        var r;
        if (html && /<(p|h[1-6]|ul|ol|li|strong|b|em|blockquote|br|div)\b/i.test(html)) r = htmlNaarMd(html);
        else if (plat){   // platte tekst, eventueel al met # en ## opmaak
          var t = plat.replace(/\r/g, ''), m = t.match(/^\s*# (.+)\n/);
          r = { titel: m ? m[1].trim() : '', md: m ? t.slice(m[0].length) : t };
          r.md = r.md.replace(/^#{4,6} /gm, '### ').trim();
        } else return;
        e.preventDefault();
        if (r.titel && !fld('title').value) fld('title').value = r.titel;
        invoegen(r.md);
        toonVoorbeeld();
        melding('Geplakt met opmaak. Controleer het voorbeeld hieronder.');
      });
      window.__dcbsHtmlNaarMd = htmlNaarMd;   // testhaak

      var inlineKnop = $('artikel-inline-img'), inlineFile = $('artikel-inline-file');
      if (inlineKnop && inlineFile){
        inlineKnop.addEventListener('click', function(){ inlineFile.click(); });
        inlineFile.addEventListener('change', function(){
          var f = inlineFile.files && inlineFile.files[0]; if (!f) return;
          if (f.size > 1500000){ fout('afbeelding is te groot (max 1,5 MB)'); inlineFile.value = ''; return; }
          bezig(true); melding('Afbeelding uploaden…');
          uploadAfbeelding(f, (fld('title').value || 'artikel') + '-tekst').then(function(p){
            invoegen('![Bijschrift (optioneel)](' + p + ')'); melding('Afbeelding toegevoegd aan de tekst. Pas eventueel het bijschrift aan.');
          }).catch(fout).then(function(){ bezig(false); inlineFile.value = ''; });
        });
      }
      function toonVoorbeeld(){
        if (!voorbeeld) return;
        voorbeeld.style.display = 'block';
        voorbeeld.innerHTML = '<h1>' + mdEsc(fld('title').value || 'Titel') + '</h1>' + mdNaarHtml(bodyVeld ? bodyVeld.value : '');
      }
      var vbTimer = null;
      if (bodyVeld) bodyVeld.addEventListener('input', function(){ clearTimeout(vbTimer); vbTimer = setTimeout(toonVoorbeeld, 300); });
      if (form.querySelector('[name="title"]')) form.querySelector('[name="title"]').addEventListener('input', function(){ if (voorbeeld && voorbeeld.style.display === 'block') toonVoorbeeld(); });
      var vbKnop = $('artikel-voorbeeld-knop'), liKnop = $('artikel-linkedin-knop');
      if (vbKnop) vbKnop.addEventListener('click', toonVoorbeeld);
      if (liKnop) liKnop.addEventListener('click', function(){
        var html = mdNaarHtml(bodyVeld ? bodyVeld.value : '', true);
        var tekst = (bodyVeld ? bodyVeld.value : '');
        var klaar = function(){ melding('Tekst gekopieerd. Plak hem in het LinkedIn-artikel onder de titel. Voeg afbeeldingen daar opnieuw in op dezelfde plek.'); };
        try {
          if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write){
            navigator.clipboard.write([new ClipboardItem({ 'text/html': new Blob([html], { type: 'text/html' }), 'text/plain': new Blob([tekst], { type: 'text/plain' }) })]).then(klaar, function(e){ fout(e); });
          } else { navigator.clipboard.writeText(tekst).then(klaar, function(e){ fout(e); }); }
        } catch(e){ fout(e); }
      });

      var enBlok = $('artikel-en');
      var publiceerKnop = $('artikel-publiceer'), imgVerwijderWrap = $('artikel-imgverwijder-wrap'), imgHuidig = $('artikel-img-huidig');
      function resetForm(){
        form.reset(); fld('id').value = '';
        if (enBlok) enBlok.open = false;
        if (formtitel) formtitel.textContent = 'Nieuw artikel';
        if (annuleren) annuleren.style.display = 'none';
        if (imgVerwijderWrap) imgVerwijderWrap.style.display = 'none';
        if (publiceerKnop) publiceerKnop.textContent = 'Publiceren';
        if (voorbeeld){ voorbeeld.style.display = 'none'; voorbeeld.innerHTML = ''; }
      }
      function verwijderEn(sl){
        return verwijderBestand('en/nieuws/' + sl + '/index.html', 'Nieuws: Engelse artikelpagina verwijderd ' + sl)
          .then(function(){ return verwijderBestand('en/nieuws/' + sl + '/artikel.md', 'Nieuws: Engelse artikeltekst verwijderd ' + sl); });
      }
      function bewerk(id){
        var a = beheer && beheer.items.filter(function(x){ return x.id === id; })[0];
        if (!a) return;
        form.reset();
        fld('id').value = a.id; fld('cat').value = a.cat || ''; fld('date').value = a.date || '';
        fld('title').value = a.title || ''; fld('summary').value = a.summary || ''; fld('link').value = a.link || '';
        if (fld('title_en')){
          fld('title_en').value = a.en ? a.en.title || '' : ''; fld('summary_en').value = a.en ? a.en.summary || '' : ''; fld('body_en').value = '';
          if (enBlok) enBlok.open = !!a.en;
          if (a.en && a.slug) api('GET', 'en/nieuws/' + a.slug + '/artikel.md').then(function(j){ fld('body_en').value = j ? b64dec(j.content) : ''; }).catch(fout);
        }
        if (formtitel) formtitel.textContent = 'Artikel bewerken';
        if (imgVerwijderWrap){ imgVerwijderWrap.style.display = a.img ? 'flex' : 'none'; if (imgHuidig) imgHuidig.textContent = a.img || ''; }
        if (annuleren) annuleren.style.display = '';
        if (publiceerKnop) publiceerKnop.textContent = 'Wijzigingen publiceren';
        melding('');
        if (bodyVeld){
          bodyVeld.value = '';
          if (a.slug){
            melding('Artikeltekst laden…');
            api('GET', 'nieuws/' + a.slug + '/artikel.md').then(function(j){ bodyVeld.value = j ? b64dec(j.content) : ''; melding(''); }).catch(fout);
          }
        }
        paneel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      function verwijder(id){
        var a = beheer && beheer.items.filter(function(x){ return x.id === id; })[0];
        if (!a) return;
        if (!window.confirm('Dit artikel verwijderen van de site?\n\n' + a.title)) return;
        bezig(true); melding('Verwijderen…');
        publiceer(beheer.items.filter(function(x){ return x.id !== id; }), 'Nieuws: verwijderd: ' + a.title)
          .then(function(){ return verwijderAfbeelding(a.img); })
          .then(function(){ if (a.slug) return verwijderBestand('nieuws/' + a.slug + '/index.html', 'Nieuws: artikelpagina verwijderd ' + a.slug).then(function(){ return verwijderBestand('nieuws/' + a.slug + '/artikel.md', 'Nieuws: artikeltekst verwijderd ' + a.slug); }); })
          .then(function(){ if (a.slug && a.en) return verwijderEn(a.slug); })
          .then(function(){ return werkStatischBij(beheer.items); })
          .then(function(){ if (fld('id').value === id) resetForm(); melding('Verwijderd en gepubliceerd. De site is binnen 1 tot 3 minuten bijgewerkt.'); })
          .catch(fout).then(function(){ bezig(false); });
      }
      function bewaar(){
        if (!beheer) return;
        var f = new FormData(form), id = (f.get('id') || '').trim();
        var bestaand = id ? beheer.items.filter(function(x){ return x.id === id; })[0] : null;
        var item = { id: bestaand ? id : 'news-' + Date.now().toString(36), cat: f.get('cat') || '', date: (f.get('date') || '').trim(),
                     link: (f.get('link') || '').trim(), title: (f.get('title') || '').trim(), summary: (f.get('summary') || '').trim() };
        // pub = eerste publicatie, mod = laatste wijziging (jjjj-mm-dd); voor de sitemap en structured data.
        var vandaag = new Date().toISOString().slice(0, 10);
        var pub = bestaand ? bestaand.pub : vandaag;
        if (pub) item.pub = pub;
        item.mod = vandaag;
        var oudeImg = bestaand && bestaand.img ? bestaand.img : '';
        var imgWeg = !!(bestaand && f.get('imgverwijder'));
        if (oudeImg && !imgWeg) item.img = oudeImg;
        var fileInput = form.querySelector('input[type="file"]'), file = fileInput && fileInput.files && fileInput.files[0];
        if (file && file.size > 1500000){ fout('afbeelding is te groot (max 1,5 MB); kies een kleinere afbeelding'); return; }
        var md = bodyVeld ? bodyVeld.value.trim() : '';
        if (!md && !item.link){ fout('vul de artikeltekst in, of een link naar LinkedIn'); return; }
        // Engelse versie: alle drie de velden of geen. Zonder Nederlandse artikeltekst is er geen Engelse pagina.
        var enT = (f.get('title_en') || '').trim(), enS = (f.get('summary_en') || '').trim(), enMd = (f.get('body_en') || '').trim();
        var metEn = !!(enT || enS || enMd);
        if (metEn && !(enT && enS && enMd)){ fout('vul voor de Engelse versie de titel, de samenvatting en de tekst in, of laat ze alle drie leeg'); return; }
        if (metEn && !md){ fout('een Engelse versie kan alleen bij een artikel met een eigen artikeltekst'); return; }
        if (metEn) item.en = { title: enT, summary: enS };
        var hadEn = !!(bestaand && bestaand.en && bestaand.slug);
        bezig(true); melding(file ? 'Afbeelding uploaden…' : 'Publiceren…');
        (file ? uploadAfbeelding(file, item.title).then(function(p){ item.img = p; }) : Promise.resolve())
          .then(function(){
            if (!md){
              if (bestaand && bestaand.slug){   // tekst leeggemaakt: artikelpagina weghalen
                return verwijderBestand('nieuws/' + bestaand.slug + '/index.html', 'Nieuws: artikelpagina verwijderd ' + bestaand.slug)
                  .then(function(){ return verwijderBestand('nieuws/' + bestaand.slug + '/artikel.md', 'Nieuws: artikeltekst verwijderd ' + bestaand.slug); })
                  .then(function(){ if (hadEn) return verwijderEn(bestaand.slug); });
              }
              return;
            }
            melding('Artikelpagina maken…');
            return vrijeSlug(slug(item.title), bestaand && bestaand.slug).then(function(sl){
              item.slug = sl; item.url = '/nieuws/' + sl + '/';
              return bouwPagina(item, md, 'nl', metEn).then(function(html){
                return zetBestand('nieuws/' + sl + '/artikel.md', md + '\n', 'Nieuws: artikeltekst ' + sl)
                  .then(function(){ return zetBestand('nieuws/' + sl + '/index.html', html, 'Nieuws: artikelpagina ' + sl); });
              }).then(function(){
                if (!metEn) return hadEn ? verwijderEn(sl) : null;   // Engelse versie leeggemaakt: Engelse pagina weghalen
                melding('Engelse artikelpagina maken…');
                return bouwPagina(item, enMd, 'en', true).then(function(html){
                  return zetBestand('en/nieuws/' + sl + '/artikel.md', enMd + '\n', 'Nieuws: Engelse artikeltekst ' + sl)
                    .then(function(){ return zetBestand('en/nieuws/' + sl + '/index.html', html, 'Nieuws: Engelse artikelpagina ' + sl); });
                });
              });
            });
          })
          .then(function(){
            melding('Publiceren…');
            var list = bestaand ? beheer.items.map(function(x){ return x.id === item.id ? item : x; }) : [item].concat(beheer.items);
            return publiceer(list, (bestaand ? 'Nieuws: bewerkt: ' : 'Nieuws: nieuw artikel: ') + item.title);
          })
          .then(function(){ if (oudeImg && item.img !== oudeImg) return verwijderAfbeelding(oudeImg); })   // oude afbeelding opruimen
          .then(function(){ melding('Artikellijst en sitemap bijwerken…'); return werkStatischBij(beheer.items); })
          .then(function(statischOk){
            resetForm();
            var na = statischOk ? '' : ' Let op: de lijst voor zoekmachines is niet bijgewerkt; dat gebeurt bij de volgende publicatie.';
            if (item.url){
              var link = 'https://www.dcbs.nl' + item.url;
              melding('Gepubliceerd. Over 1 tot 3 minuten staat het artikel op ' + link + ' (link gekopieerd voor je LinkedIn-post).' + na);
              try { navigator.clipboard.writeText(link); } catch(e){}
            } else melding('Gepubliceerd. De site is binnen 1 tot 3 minuten bijgewerkt; hieronder staat al de nieuwe stand.' + na);
          })
          .catch(fout).then(function(){ bezig(false); });
      }

      function toonLogin(){ login.style.display = 'block'; werk.style.display = 'none'; uitloggen.style.display = 'none'; }
      function start(){
        login.style.display = 'none'; werk.style.display = 'block'; uitloggen.style.display = '';
        laad().catch(function(e){ fout(e); if (/401/.test(e.message)){ setToken(''); toonLogin(); } });
      }
      function open(){ beheerOpen = true; paneel.style.display = 'block'; knop.textContent = 'Sluit beheer'; render(); if (token()) start(); else toonLogin(); }
      function sluit(){ beheerOpen = false; paneel.style.display = 'none'; knop.textContent = 'Beheren'; render(); }

      knop.addEventListener('click', function(){ if (beheerOpen) sluit(); else open(); });
      if (tokenOpslaan) tokenOpslaan.addEventListener('click', function(){
        var t = (tokenInput.value || '').trim(); if (!t){ fout('plak eerst het token'); return; }
        setToken(t); tokenInput.value = ''; start();
      });
      if (tokenInput) tokenInput.addEventListener('keydown', function(e){ if (e.key === 'Enter'){ e.preventDefault(); tokenOpslaan.click(); } });
      if (uitloggen) uitloggen.addEventListener('click', function(){ setToken(''); beheer = null; render(); toonLogin(); melding('Token verwijderd uit deze browser.'); });
      if (annuleren) annuleren.addEventListener('click', function(){ resetForm(); melding(''); });
      form.addEventListener('submit', function(e){ e.preventDefault(); bewaar(); });
      lijst.addEventListener('click', function(e){
        var c = e.target.closest ? e.target.closest('button[data-copy]') : null;
        if (c){
          e.preventDefault();
          var lk = c.getAttribute('data-copy');
          var ok = function(){ c.textContent = 'Gekopieerd'; setTimeout(function(){ c.textContent = 'Kopieer link'; }, 2000); melding('Link gekopieerd: ' + lk); };
          if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(lk).then(ok, function(){ window.prompt('Kopieer deze link:', lk); });
          else window.prompt('Kopieer deze link:', lk);
          return;
        }
        var b = e.target.closest ? e.target.closest('button[data-edit],button[data-del]') : null;
        if (!b || b.disabled) return;
        e.preventDefault();
        if (b.hasAttribute('data-edit')) bewerk(b.getAttribute('data-edit')); else verwijder(b.getAttribute('data-del'));
      });
      window.__dcbsBeheer = { items: function(){ return beheer ? beheer.items : null; }, laad: laad, open: open };   // testhaak
      if (location.hash === '#beheer') open();
    }
  }

  // ---- Bezoekersstatistieken (Plausible, zonder cookies): klikken op contact meten ----
  window.plausible = window.plausible || function(){ (window.plausible.q = window.plausible.q || []).push(arguments); };
  document.addEventListener('click', function(e){
    var a = e.target.closest ? e.target.closest('a') : null; if (!a) return;
    var h = a.getAttribute('href') || '';
    if (/^mailto:/i.test(h)) window.plausible('Email Click');
    else if (/^tel:/i.test(h)) window.plausible('Phone Click');
    else if (/\/contact\/?$/.test(h) && /b-p/.test(a.className)) window.plausible('Gratis Consult Click');
    else if (/linkedin\.com|lnkd\.in/i.test(h)) window.plausible('LinkedIn Click');
  });
  document.addEventListener('submit', function(e){
    if (e.target && /formsubmit\.co/.test(e.target.getAttribute('action') || '')) window.plausible('Contact Form Submit');
  });
})();
