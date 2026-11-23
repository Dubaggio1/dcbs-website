// DCBS v6 — nieuws op de homepage in de v6-stijl (bron: window.DCBS_ARTICLES uit /nieuws-data.js)
document.addEventListener('DOMContentLoaded', function(){
  var grid = document.getElementById('v6-nieuws-home');
  if (!grid) return;
  var items = (window.DCBS_ARTICLES || []).slice(0, 3);
  var sectie = document.getElementById('v6-nieuws-sectie');
  if (!items.length) { if (sectie) sectie.style.display = 'none'; return; }
  // De kaarten komen uit site.js (DCBS_STATISCH.home), dezelfde functie die de statische versie
  // in index.html maakt. Zo blijven de versie voor bezoekers en die voor zoekmachines gelijk.
  if (window.DCBS_STATISCH) grid.innerHTML = window.DCBS_STATISCH.home(items);
});
