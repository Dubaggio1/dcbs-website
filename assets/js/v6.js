// DCBS v6 — nieuws op de homepage in de v6-stijl (bron: window.DCBS_ARTICLES uit /nieuws-data.js)
document.addEventListener('DOMContentLoaded', function(){
  var grid = document.getElementById('v6-nieuws-home');
  if (!grid) return;
  var items = (window.DCBS_ARTICLES || []).slice(0, 3);
  var sectie = document.getElementById('v6-nieuws-sectie');
  if (!items.length) { if (sectie) sectie.style.display = 'none'; return; }
  function esc(s){ var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
  grid.innerHTML = items.map(function(a){
    var dest = a.url || a.link; var ext = dest && /^https?:/i.test(dest);
    var open = dest ? '<a class="card" href="' + esc(dest) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') : '<div class="card"';
    var close = dest ? '</a>' : '</div>';
    var media = a.img ? '<img src="' + esc(a.img) + '" alt="" loading="lazy" style="width:100%;height:200px;object-fit:cover;display:block">' : '<div class="bar"></div>';
    return open + ' style="flex:1 1 300px;display:flex;flex-direction:column">' + media +
      '<div style="padding:26px 28px;display:flex;flex-direction:column;gap:12px;flex:1">' +
      '<span class="chip" style="align-self:flex-start">' + esc(a.cat) + '</span>' +
      '<h3 style="font-size:21px">' + esc(a.title) + '</h3>' +
      '<span class="mut" style="font-size:13px;margin-top:auto">' + esc(a.date) + '</span></div>' + close;
  }).join('');
});
