/*!
 * The Data Compliance Builders — contact-form submit handler
 * Loaded only on /contact/ + /en/contact/.
 *
 * sf(e) wordt aangeroepen via <form onsubmit="sf(event)">.
 * Toont een bevestiging + verwijst naar Calendly. Geen backend.
 */

function sf(e) {
  e.preventDefault();
  var msg = (document.documentElement.lang || 'nl').toLowerCase().indexOf('en') === 0
    ? 'Thanks for your message! We will get back to you within 1 working day.\n\nOr book directly: calendly.com/dubach-legal/30min'
    : 'Bedankt voor uw bericht! Wij nemen binnen 1 werkdag contact op.\n\nOf plan direct: calendly.com/dubach-legal/30min';
  alert(msg);
}
