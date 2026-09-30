// DCBS site.js — gedeelde functionaliteit voor de statische site
(function(){
  'use strict';

  // ---- Consent Mode v2 ----------------------------------------------------
  // Google Ads-tag: vervang AW-XXXXXXXXXX door uw conversie-ID en verwijder de
  // commentaartekens in loadAds() hieronder.
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
  if (consent) applyConsent(consent);

  document.addEventListener('DOMContentLoaded', function(){
    // ---- Mobiele opschoning (alleen <=720px; desktop ongewijzigd) ----
    enhanceMobile();

    // ---- Cookiebanner ----
    var banner = document.getElementById('cookie-banner');
    if (banner && !consent) banner.style.display = 'flex';
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

  // ---- Nieuws: publieke weergave -------------------------------------------
  // Bron: window.DCBS_ARTICLES uit /nieuws-data.js (bovenaan = nieuwste). Dat bestand wordt beheerd
  // via de nieuwspagina (/nieuws/#beheer), die het via de GitHub-API publiceert; zie initBeheer hieronder.
  function nieuwsEsc(s){ var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
  function alleArtikelen(){ return window.DCBS_ARTICLES || []; }

  // Homepage: de 3 nieuwste artikelen, zelfde bron en volgorde als de nieuwspagina.
  // Zonder artikelen blijft de hele sectie (#nieuws-sectie) verborgen.
  // Een artikel zonder link (bijv. LinkedIn-URL nog niet ingevuld) wordt als niet-klikbare kaart getoond.
  function initNieuwsHome(grid){
    var sectie = document.getElementById('nieuws-sectie');
    var items = alleArtikelen().slice(0, 3);
    if (!items.length){ if (sectie) sectie.style.display = 'none'; return; }
    if (sectie) sectie.style.display = '';
    grid.innerHTML = items.map(function(a){
      var isExt = a.link && /^https?:/i.test(a.link);
      var media = a.img
        ? '<img src="' + nieuwsEsc(a.img) + '" alt="" loading="lazy" style="width:100%;height:250px;object-fit:cover;background:#E9E5DA">'
        : '<div style="width:100%;height:250px;background:linear-gradient(135deg,#E9E5DA,#DDD8CA)"></div>';
      return '<a' + (a.link ? ' href="' + nieuwsEsc(a.link) + '"' + (isExt ? ' target="_blank" rel="noopener"' : '') + ' class="hv7"' : '') +
        ' style="color:#14181A;display:flex;flex-direction:column;min-width:0">' +
        media +
        '<div style="display:flex;justify-content:space-between;font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:#0E5654;margin-top:20px"><span>' + nieuwsEsc(a.cat) + '</span><span style="color:#8E938F">' + nieuwsEsc(a.date) + '</span></div>' +
        '<div style="font-family:\'Petrona\',Georgia,serif;font-size:24px;line-height:1.25;margin-top:12px">' + nieuwsEsc(a.title) + '</div>' +
        '</a>';
    }).join('');
  }

  function initNieuws(lijst){
    var esc = nieuwsEsc;
    var publiek = alleArtikelen();
    var beheer = null;        // { items, sha } zodra de beheerder de lijst uit GitHub heeft geladen
    var beheerOpen = false;   // beheerpaneel open: toon bewerk-/verwijderknoppen

    function rij(a, i, n){
      var top = i === 0 ? '#14181A' : '#E2DFD6';
      var bottom = i === n - 1 ? ';border-bottom:1px solid #E2DFD6' : '';
      var isExt = a.link && /^https?:/i.test(a.link);
      var href = a.link ? ' href="' + esc(a.link) + '"' + (isExt ? ' target="_blank" rel="noopener"' : '') : '';
      var media = a.img
        ? '<img src="' + esc(a.img) + '" alt="" loading="lazy" style="width:320px;max-width:100%;height:190px;object-fit:cover;background:#E9E5DA">'
        : '<div style="width:320px;max-width:100%;height:190px;background:linear-gradient(135deg,#E9E5DA,#DDD8CA)"></div>';
      var knoppen = beheerOpen
        ? '<span style="position:absolute;top:36px;right:0;display:flex;gap:8px">' +
          '<button type="button" data-edit="' + esc(a.id) + '" style="font-family:Archivo,sans-serif;font-size:12px;color:#0E5654;background:#FBFAF7;border:1px solid #A9C4C1;padding:6px 12px;cursor:pointer">Bewerken</button>' +
          '<button type="button" data-del="' + esc(a.id) + '" style="font-family:Archivo,sans-serif;font-size:12px;color:#8E938F;background:#FBFAF7;border:1px solid #D6D2C6;padding:6px 12px;cursor:pointer">Verwijderen</button></span>'
        : '';
      return '<div style="position:relative">' +
        '<a' + href + ' style="display:grid;grid-template-columns:minmax(200px,320px) minmax(0,1fr) 110px;gap:44px;align-items:center;padding:36px 0;border-top:1px solid ' + top + bottom + ';color:#14181A" class="nieuwsrij">' +
        media +
        '<span><span style="display:block;font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:#0E5654">' + esc(a.cat) + '</span>' +
        '<span style="display:block;font-family:\'Petrona\',Georgia,serif;font-size:29px;line-height:1.22;margin-top:12px">' + esc(a.title) + '</span>' +
        '<span style="display:block;font-size:14px;line-height:1.6;color:#4E5552;margin-top:12px;max-width:64ch">' + esc(a.summary) + '</span></span>' +
        '<span style="font-size:12.5px;color:#6B716E;text-align:right">' + esc(a.date) + '</span></a>' +
        knoppen + '</div>';
    }
    function render(){
      var list = beheer ? beheer.items : publiek;
      if (!list.length){
        lijst.innerHTML = '<p style="font-family:\'Petrona\',Georgia,serif;font-size:24px;line-height:1.4;color:#4E5552;margin:0;padding:36px 0;border-top:1px solid #14181A">Er zijn nog geen artikelen gepubliceerd. Nieuwe artikelen verschijnen hier automatisch.</p>';
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
      function slug(s){ return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 50) || 'artikel'; }
      function b64enc(str){ return btoa(unescape(encodeURIComponent(str))); }
      function b64dec(b){ return decodeURIComponent(escape(atob(String(b).replace(/\s/g, '')))); }
      function parseData(src){
        try { return new Function('window', src + '\nreturn window.DCBS_ARTICLES || [];')({}) || []; }
        catch(e){ throw new Error('nieuws-data.js kon niet gelezen worden (' + e.message + ')'); }
      }
      function serialize(list){
        return '// DCBS nieuwsartikelen — beheerd via https://www.dcbs.nl/nieuws/#beheer (niet met de hand bewerken).\n' +
               '// Bovenaan = nieuwste. cat = een van de diensten. link = LinkedIn-post. img = pad onder /assets/nieuws/.\n' +
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

      var publiceerKnop = $('artikel-publiceer'), imgVerwijderWrap = $('artikel-imgverwijder-wrap'), imgHuidig = $('artikel-img-huidig');
      function resetForm(){
        form.reset(); fld('id').value = '';
        if (formtitel) formtitel.textContent = 'Nieuw artikel';
        if (annuleren) annuleren.style.display = 'none';
        if (imgVerwijderWrap) imgVerwijderWrap.style.display = 'none';
        if (publiceerKnop) publiceerKnop.textContent = 'Publiceren';
      }
      function bewerk(id){
        var a = beheer && beheer.items.filter(function(x){ return x.id === id; })[0];
        if (!a) return;
        form.reset();
        fld('id').value = a.id; fld('cat').value = a.cat || ''; fld('date').value = a.date || '';
        fld('title').value = a.title || ''; fld('summary').value = a.summary || ''; fld('link').value = a.link || '';
        if (formtitel) formtitel.textContent = 'Artikel bewerken';
        if (imgVerwijderWrap){ imgVerwijderWrap.style.display = a.img ? 'flex' : 'none'; if (imgHuidig) imgHuidig.textContent = a.img || ''; }
        if (annuleren) annuleren.style.display = '';
        if (publiceerKnop) publiceerKnop.textContent = 'Wijzigingen publiceren';
        melding('');
        paneel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      function verwijder(id){
        var a = beheer && beheer.items.filter(function(x){ return x.id === id; })[0];
        if (!a) return;
        if (!window.confirm('Dit artikel verwijderen van de site?\n\n' + a.title)) return;
        bezig(true); melding('Verwijderen…');
        publiceer(beheer.items.filter(function(x){ return x.id !== id; }), 'Nieuws: verwijderd: ' + a.title)
          .then(function(){ return verwijderAfbeelding(a.img); })
          .then(function(){ if (fld('id').value === id) resetForm(); melding('Verwijderd en gepubliceerd. De site is binnen 1 tot 3 minuten bijgewerkt.'); })
          .catch(fout).then(function(){ bezig(false); });
      }
      function bewaar(){
        if (!beheer) return;
        var f = new FormData(form), id = (f.get('id') || '').trim();
        var bestaand = id ? beheer.items.filter(function(x){ return x.id === id; })[0] : null;
        var item = { id: bestaand ? id : 'news-' + Date.now().toString(36), cat: f.get('cat') || '', date: (f.get('date') || '').trim(),
                     link: (f.get('link') || '').trim(), title: (f.get('title') || '').trim(), summary: (f.get('summary') || '').trim() };
        var oudeImg = bestaand && bestaand.img ? bestaand.img : '';
        var imgWeg = !!(bestaand && f.get('imgverwijder'));
        if (oudeImg && !imgWeg) item.img = oudeImg;
        var fileInput = form.querySelector('input[type="file"]'), file = fileInput && fileInput.files && fileInput.files[0];
        if (file && file.size > 1500000){ fout('afbeelding is te groot (max 1,5 MB); kies een kleinere afbeelding'); return; }
        bezig(true); melding(file ? 'Afbeelding uploaden…' : 'Publiceren…');
        (file ? uploadAfbeelding(file, item.title).then(function(p){ item.img = p; }) : Promise.resolve())
          .then(function(){
            melding('Publiceren…');
            var list = bestaand ? beheer.items.map(function(x){ return x.id === item.id ? item : x; }) : [item].concat(beheer.items);
            return publiceer(list, (bestaand ? 'Nieuws: bewerkt: ' : 'Nieuws: nieuw artikel: ') + item.title);
          })
          .then(function(){ if (oudeImg && item.img !== oudeImg) return verwijderAfbeelding(oudeImg); })   // oude afbeelding opruimen
          .then(function(){ resetForm(); melding('Gepubliceerd. De site is binnen 1 tot 3 minuten bijgewerkt; hieronder staat al de nieuwe stand.'); })
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
        var b = e.target.closest ? e.target.closest('button[data-edit],button[data-del]') : null;
        if (!b || b.disabled) return;
        e.preventDefault();
        if (b.hasAttribute('data-edit')) bewerk(b.getAttribute('data-edit')); else verwijder(b.getAttribute('data-del'));
      });
      window.__dcbsBeheer = { items: function(){ return beheer ? beheer.items : null; }, laad: laad, open: open };   // testhaak
      if (location.hash === '#beheer') open();
    }
  }
})();
