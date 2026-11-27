// [Professor Dev] Live server-authorized filters and group assignment dialog.
(() => {
  const filters = document.getElementById('catalog-filters');
  const results = document.getElementById('catalog-results');
  const filterError = document.getElementById('catalog-filter-error');
  const dialog = document.getElementById('catalog-assignment');
  const form = document.getElementById('catalog-assignment-form');
  const error = document.getElementById('catalog-assignment-error');
  let controller, sequence = 0, timer, opener, submitting = false;
  async function refresh() {
    clearTimeout(timer);
    const current = ++sequence;
    controller?.abort();
    controller = new AbortController();
    const url = new URL(filters.action || location.href);
    url.search = new URLSearchParams(new FormData(filters)).toString();
    const publicUrl = new URL(url);
    url.searchParams.set('fragment', '1');
    results.setAttribute('aria-busy', 'true');
    filterError.hidden = true;
    try {
      const response = await fetch(url, {signal: controller.signal, credentials: 'same-origin'});
      if (!response.ok || response.redirected) throw new Error('Filter request failed');
      const html = await response.text();
      if (current !== sequence) return;
      results.innerHTML = html;
      history.replaceState(null, '', publicUrl.pathname + publicUrl.search);
    } catch (problem) {
      if (current === sequence && problem.name !== 'AbortError') filterError.hidden = false;
    } finally {
      if (current === sequence) results.removeAttribute('aria-busy');
    }
  }
  if (filters) {
    filters.addEventListener('submit', (event) => { event.preventDefault(); refresh(); });
    filters.addEventListener('change', refresh);
    filters.querySelector('[name="q"]').addEventListener('input', () => {
      // Invalidate old results immediately, before the debounce starts.
      ++sequence; controller?.abort(); clearTimeout(timer);
      timer = setTimeout(refresh, 250);
    });
  }
  if (!dialog || !form) return;
  const assignmentActions = document.getElementById('exercise-assignment-actions') || results;
  assignmentActions.addEventListener('click', (event) => {
    const button = event.target.closest('[data-assign-url]');
    if (!button) return;
    opener = button;
    form.reset();
    form.action = button.dataset.assignUrl;
    error.hidden = true;
    document.getElementById('catalog-exercise-title').textContent = button.dataset.exerciseTitle;
    dialog.showModal();
  });
  dialog.querySelector('[data-close-assignment]').addEventListener('click', () => {
    if (!submitting) dialog.close();
  });
  dialog.addEventListener('cancel', (event) => { if (submitting) event.preventDefault(); });
  dialog.addEventListener('close', () => { if (opener?.isConnected) opener.focus(); });
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (submitting || !form.reportValidity()) return;
    submitting = true;
    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true;
    error.hidden = true;
    try {
      const response = await fetch(form.action, {method: 'POST', body: new FormData(form), credentials: 'same-origin'});
      if (response.redirected) throw new Error('Your session changed. Reload the page.');
      if (!response.headers.get('content-type')?.includes('application/json')) {
        throw new Error('This exercise is no longer available. Reload the catalog and try again.');
      }
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Could not assign the exercise.');
      const destination = new URL(data.redirect, location.origin);
      if (destination.origin !== location.origin) throw new Error('Invalid destination.');
      location.assign(destination.href);
    } catch (problem) {
      error.textContent = problem.message || 'Could not assign the exercise. Please try again.';
      error.hidden = false;
    } finally { submitting = false; submit.disabled = false; }
  });
})();
