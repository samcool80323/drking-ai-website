(() => {
  'use strict';

  const forms = [...document.querySelectorAll('form[data-drking-form]')];
  if (!forms.length) return;

  const valueEntries = (form) => {
    const entries = {};
    for (const [name, rawValue] of new FormData(form)) {
      if (!name || name === 'website') continue;
      const value = String(rawValue).trim();
      if (!value) continue;
      if (entries[name]) entries[name] = `${entries[name]}, ${value}`;
      else entries[name] = value;
    }
    form.querySelectorAll('input[type="tel"][name]').forEach((input) => {
      const control = input.closest('[data-international-phone]');
      const country = control?.querySelector('select')?.value || 'AU';
      const normalised = window.DrKingPhone?.normalisePhone(input.value, country);
      if (normalised) entries[input.name] = normalised;
    });
    return entries;
  };

  const statusElement = (form) => {
    const generated = form.querySelector('[data-drking-status]');
    if (generated) return generated;
    const existing = form.querySelector('[role="status"]');
    if (existing && !existing.parentElement?.closest('[hidden]')) return existing;
    const status = document.createElement('p');
    status.hidden = true;
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.dataset.drkingStatus = '';
    form.append(status);
    return status;
  };

  const showStatus = (form, message, { error = false, fallback = null } = {}) => {
    const status = statusElement(form);
    if (!status) return;
    status.hidden = false;
    status.dataset.state = error ? 'error' : 'success';
    status.replaceChildren(document.createTextNode(message));
    if (fallback) {
      const link = document.createElement('a');
      link.href = fallback;
      link.textContent = ' Send it by email instead.';
      status.append(link);
    }
  };

  const fallbackEmail = (type, fields) => {
    const title = type.replaceAll('-', ' ');
    const lines = Object.entries(fields).map(([key, value]) => `${key}: ${value}`);
    const subject = `DrKing website — ${title}`;
    const body = `Hello DrKing,\n\n${lines.join('\n')}\n\nPlease contact me about this enquiry.`;
    return `mailto:info@drking.ai?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  };

  document.addEventListener('submit', async (event) => {
    const form = event.target.closest?.('form[data-drking-form]');
    if (!form) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    if (!form.reportValidity()) return;

    const fields = valueEntries(form);
    const fallback = fallbackEmail(form.dataset.drkingForm, fields);
    const button = form.querySelector('button[type="submit"], input[type="submit"]');
    if (button) {
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
    }

    try {
      const response = await fetch('/api/enquiries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          type: form.dataset.drkingForm,
          source: window.location.pathname,
          pageTitle: document.title,
          fields,
          website: '',
        }),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.error || 'The enquiry could not be recorded.');
      showStatus(form, 'Thanks — your enquiry has been received. The DrKing team will be in touch.');
      form.reset();
    } catch {
      showStatus(form, 'We could not send this automatically. Your details have not been lost.', { error: true, fallback });
    } finally {
      if (button) {
        button.disabled = false;
        button.removeAttribute('aria-busy');
      }
    }
  }, true);
})();
