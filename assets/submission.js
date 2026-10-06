(() => {
  const form = document.querySelector('#submissionForm, #contactForm');
  if (!form) return;
  const feedback = document.querySelector('#formFeedback');
  const start = document.querySelector('#start-date'), end = document.querySelector('#end-date');
  const image = document.querySelector('#image-url'), permission = document.querySelector('#image-permission');
  const button = form.querySelector('button[type="submit"]'), originalLabel = button.textContent;
  function validate() {
    if (permission) permission.required = !!image.value.trim();
    if (end) end.setCustomValidity(start.value && end.value && end.value < start.value ? 'The last date must be on or after the first date.' : '');
  }
  [start, end, image].filter(Boolean).forEach(field => {
    field.addEventListener('input', validate); field.addEventListener('change', validate);
  });
  const params = new URLSearchParams(location.search);
  if (form.id === 'submissionForm' && params.has('event')) {
    const name = params.get('event'); document.querySelector('#event-name').value = name;
    document.querySelector('#submission-kind').value = 'Correct a listing';
    const event = window.SITE_DATA.events.find(e => e['Event / attraction'] === name);
    if (event) document.querySelector('#official-url').value = event.Website;
  }
  if (form.id === 'contactForm' && ['sponsorship', 'accessibility', 'privacy'].includes(params.get('topic'))) document.querySelector('#contact-topic').value = params.get('topic');
  function show(message) { feedback.hidden = false; feedback.replaceChildren(document.createTextNode(message)); feedback.focus(); }
  form.addEventListener('submit', async event => {
    event.preventDefault(); validate(); if (!form.reportValidity()) return;
    if (!navigator.onLine) { show('You’re offline. Your message has not been sent. Keep this page open and try again when you’re connected.'); return; }
    button.disabled = true; button.textContent = 'Sending…'; const data = new FormData(form);
    try {
      const response = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data).toString() });
      if (!response.ok) throw new Error('Submission unavailable');
      const result = await response.text();
      if ((response.url && /login|signin|identity|netlify\.com/i.test(response.url)) || /id=["'](?:submissionForm|contactForm|eventCards)/i.test(result)) throw new Error('Form handler is not active');
      show(form.id === 'submissionForm' ? 'Suggestion received. Thanks! We review event submissions before publication.' : 'Message received. Thanks for getting in touch.');
      form.reset(); validate();
    } catch {
      show('Your message could not be confirmed as received. Your details are still here. Try again, or copy them below to keep a backup.');
      const copy = document.createElement('textarea'); copy.readOnly = true; copy.setAttribute('aria-label', 'Your message to copy');
      copy.value = [...data].filter(([key]) => !['bot-field', 'form-name'].includes(key)).map(([key, value]) => `${key}: ${value}`).join('\n\n'); feedback.append(copy);
    } finally { button.disabled = false; button.textContent = originalLabel; }
  });
})();
