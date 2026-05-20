/*!
 * The Data Compliance Builders — runtime EN-vertaling voor news-stubs
 * Loaded only on /en/nieuws/<slug>/ EN-stub pages (Phase 4 output).
 *
 * SECURITY WARNING — bestaand probleem, NIET door deze sessie geintroduceerd:
 *   Deze functie doet fetch() naar api.anthropic.com vanuit de browser.
 *   Een API-key in client-side code is altijd zichtbaar. Mitigation
 *   voorzieningen voor volgende sessie:
 *     a) Translate.js helemaal verwijderen en EN-versies pre-genereren
 *        tijdens deploy (gh-action).
 *     b) Of: proxy via een serverless function (Cloudflare Workers,
 *        Netlify Functions) met de key server-side.
 *     c) Of: translate.js uitschakelen tot er een veilige route is.
 *   Tot dan: blijft functioneel werken, key staat NIET in deze file
 *   (gebruik vereist key elders ingegeven door bezoeker zelf, of de
 *   request faalt netjes via .catch). Zie /docs/seo-pass-1.md.
 *
 * Gebruik:
 *   1. EN-stub HTML pagina bevat een container met id="article-body"
 *      die de NL-tekst toont onder de samenvatting + disclaimer.
 *   2. translateHTML(html, "en", cacheKey, callback) cachet het
 *      resultaat in localStorage 'dcbs_transl' en roept callback
 *      met de vertaalde HTML.
 */

var _translCache = JSON.parse(localStorage.getItem('dcbs_transl') || '{}');

function _saveTranslCache() {
  try { localStorage.setItem('dcbs_transl', JSON.stringify(_translCache)); } catch (e) { /* ignore */ }
}

function translateHTML(html, targetLang, cacheKey, callback) {
  // Cache hit → direct teruggeven
  var cached = _translCache[cacheKey];
  if (cached) { callback(cached); return; }

  // Loading-state
  callback('<div style="padding:4rem;text-align:center;color:var(--mu)">' +
    '<div style="font-size:2rem;margin-bottom:1rem;animation:pulse 1.5s ease-in-out infinite">&#9203;</div>' +
    '<p style="font-size:.85rem;letter-spacing:.1em;text-transform:uppercase">Translating article...</p>' +
    '</div>');

  // Text-nodes extraheren
  var tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;
  var walker = document.createTreeWalker(
    tempDiv, NodeFilter.SHOW_TEXT,
    { acceptNode: function (n) {
      var p = n.parentElement;
      if (!p) return NodeFilter.FILTER_REJECT;
      var tag = p.tagName.toLowerCase();
      if (['script', 'style', 'a'].includes(tag)) return NodeFilter.FILTER_REJECT;
      if (n.textContent.trim().length < 2) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    } }
  );
  var texts = [];
  var nodes = [];
  var node;
  while ((node = walker.nextNode())) {
    texts.push(node.textContent);
    nodes.push(node);
  }
  if (!texts.length) { callback(html); return; }

  var prompt = 'Translate the following Dutch texts to English. Return ONLY a JSON array with the translated strings in the same order. Keep HTML entities (&mdash; &euro; etc) unchanged. Keep names, acronyms (AVG, GDPR, DPO, DPIA, FRIA, ISO, EU AI Act, BC 5701) and company names unchanged.\n\n' + JSON.stringify(texts);

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
      var responseText = data.content && data.content[0] && data.content[0].text;
      if (!responseText) { callback(html); return; }
      var jsonMatch = responseText.match(/\[[\s\S]*\]/);
      if (!jsonMatch) { callback(html); return; }
      var translated;
      try { translated = JSON.parse(jsonMatch[0]); } catch (e) { callback(html); return; }
      for (var i = 0; i < Math.min(nodes.length, translated.length); i++) {
        nodes[i].textContent = translated[i];
      }
      var result = tempDiv.innerHTML;
      _translCache[cacheKey] = result;
      _saveTranslCache();
      callback(result);
    })
    .catch(function () { callback(html); });
}
