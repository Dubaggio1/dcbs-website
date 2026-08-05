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
  });

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

  function initNieuws(lijst){
    var LSKEY = 'dcbs-local-articles';
    function getLocal(){ try { return JSON.parse(localStorage.getItem(LSKEY) || '[]'); } catch(e){ return []; } }
    function setLocal(v){ try { localStorage.setItem(LSKEY, JSON.stringify(v)); } catch(e){} }
    function esc(s){ var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
    function render(){
      var items = getLocal().map(function(a){ a = Object.assign({}, a); a._local = true; return a; })
        .concat(window.DCBS_ARTICLES || []);
      lijst.innerHTML = items.map(function(a, i){
        var top = i === 0 ? '#14181A' : '#E2DFD6';
        var bottom = i === items.length - 1 ? ';border-bottom:1px solid #E2DFD6' : '';
        var href = a.link ? ' href="' + esc(a.link) + '" target="_blank" rel="noopener"' : '';
        return '<div style="position:relative">' +
          '<a' + href + ' style="display:grid;grid-template-columns:minmax(200px,320px) minmax(0,1fr) 110px;gap:44px;align-items:center;padding:36px 0;border-top:1px solid ' + top + bottom + ';color:#14181A" class="nieuwsrij">' +
          '<div style="width:320px;max-width:100%;height:190px;background:linear-gradient(135deg,#E9E5DA,#DDD8CA)"></div>' +
          '<span><span style="display:block;font-size:11px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:#0E5654">' + esc(a.cat) + '</span>' +
          '<span style="display:block;font-family:\'Petrona\',Georgia,serif;font-size:29px;line-height:1.22;margin-top:12px">' + esc(a.title) + '</span>' +
          '<span style="display:block;font-size:14px;line-height:1.6;color:#4E5552;margin-top:12px;max-width:64ch">' + esc(a.summary) + '</span></span>' +
          '<span style="font-size:12.5px;color:#6B716E;text-align:right">' + esc(a.date) + '</span></a>' +
          (a._local ? '<button data-del="' + esc(a.id) + '" title="Verwijderen" style="position:absolute;top:36px;right:0;font-family:Archivo,sans-serif;font-size:12px;color:#8E938F;background:none;border:1px solid #D6D2C6;padding:6px 12px;cursor:pointer">Verwijderen</button>' : '') +
          '</div>';
      }).join('');
      lijst.querySelectorAll('button[data-del]').forEach(function(btn){
        btn.addEventListener('click', function(){
          setLocal(getLocal().filter(function(x){ return x.id !== btn.getAttribute('data-del'); }));
          render();
        });
      });
    }
    render();
    var toggle = document.getElementById('toggle-form'), formwrap = document.getElementById('artikel-formwrap');
    if (toggle && formwrap){
      toggle.addEventListener('click', function(){
        var open = formwrap.style.display !== 'none';
        formwrap.style.display = open ? 'none' : 'block';
        toggle.textContent = open ? '+ Artikel toevoegen' : 'Sluit formulier';
      });
    }
    var form = document.getElementById('artikel-form');
    if (form) form.addEventListener('submit', function(e){
      e.preventDefault();
      var f = new FormData(form);
      var item = { id: 'local-' + Date.now(), cat: f.get('cat'), date: f.get('date'), title: f.get('title'), summary: f.get('summary'), link: (f.get('link') || '').trim() };
      setLocal([item].concat(getLocal()));
      form.reset();
      if (formwrap) formwrap.style.display = 'none';
      if (toggle) toggle.textContent = '+ Artikel toevoegen';
      render();
    });
  }
})();
