// [Professor Dev] UI behavior checks without network calls or external DOM libraries.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');

class Element {
  constructor() {
    this.events = {}; this.attrs = {}; this.children = {}; this.dataset = {};
    this.classes = new Set(); this.isConnected = true;
    this.classList = {toggle: (name, active) => active ? this.classes.add(name) : this.classes.delete(name)};
  }
  addEventListener(name, callback) { (this.events[name] ??= []).push(callback); }
  fire(name, data = {}) { return Promise.all((this.events[name] || []).map(fn => fn({preventDefault() {}, ...data}))); }
  setAttribute(name, value) { this.attrs[name] = value; }
  getAttribute(name) { return this.attrs[name]; }
  removeAttribute(name) { delete this.attrs[name]; }
  querySelector(selector) { return this.children[selector]; }
  focus() { this.focused = true; }
}
function run(file, context) {
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../../static/js', file), 'utf8'), context);
}
function catalog(fetch, details = false) {
  const ids = Object.fromEntries(['catalog-filters', 'catalog-results', 'catalog-filter-error',
    'catalog-assignment', 'catalog-assignment-form', 'catalog-assignment-error',
    'catalog-exercise-title'].map(id => [id, new Element()]));
  const filters = ids['catalog-filters'], form = ids['catalog-assignment-form'];
  filters.values = {q: '', visibility: 'all', owner: 'all'};
  filters.children['[name="q"]'] = new Element();
  form.values = {group: '1', deadline: '', csrfmiddlewaretoken: 'local-test-csrf'};
  form.reset = () => {}; form.reportValidity = () => true;
  form.children['[type="submit"]'] = new Element();
  const dialog = ids['catalog-assignment'];
  dialog.showModal = () => { dialog.open = true; };
  dialog.close = () => { dialog.open = false; dialog.fire('close'); };
  dialog.children['[data-close-assignment]'] = new Element();
  const location = {href: 'http://localhost/professor/bugs/', origin: 'http://localhost', assign(url) { this.assigned = url; }};
  const context = {
    document: {getElementById: id => ids[id]}, location, fetch,
    URL, URLSearchParams, AbortController,
    FormData: class { constructor(form) { this.entries = Object.entries(form.values); } [Symbol.iterator]() { return this.entries[Symbol.iterator](); } },
    history: {replaceState(a, b, url) { this.url = url; }},
    setTimeout(fn) { context.timer = fn; return 1; }, clearTimeout() {},
  };
  if (details) {
    ids['exercise-assignment-actions'] = new Element();
    delete ids['catalog-filters'];
    delete ids['catalog-results'];
  }
  run('professor-catalog.js', context);
  return {ids, filters, form, dialog, context};
}
const response = html => ({ok: true, redirected: false, text: async () => html});

test('live filters discard stale responses and debounce title input', async () => {
  const pending = [];
  const ui = catalog((url, options) => new Promise(resolve => pending.push({url, options, resolve})));
  const old = ui.filters.fire('change');
  ui.filters.values.owner = 'others';
  const latest = ui.filters.fire('change');
  assert.equal(pending[0].options.signal.aborted, true);
  assert.equal(pending[1].url.searchParams.get('owner'), 'others');
  pending[1].resolve(response('new cards')); await latest;
  pending[0].resolve(response('stale cards')); await old;
  assert.equal(ui.ids['catalog-results'].innerHTML, 'new cards');
  assert.ok(!ui.context.history.url.includes('fragment='));
  ui.filters.values.q = 'counter';
  await ui.filters.children['[name="q"]'].fire('input');
  assert.equal(pending.length, 2);
  const typed = ui.context.timer();
  pending[2].resolve(response('counter cards')); await typed;
  assert.equal(ui.ids['catalog-results'].innerHTML, 'counter cards');
});

test('assignment dialog preserves errors, blocks duplicate requests and restores focus', async () => {
  let resolve, calls = 0;
  const ui = catalog(() => { calls++; return new Promise(done => { resolve = done; }); });
  const opener = new Element();
  opener.dataset = {assignUrl: '/professor/bugs/3/assign/', exerciseTitle: '<b>literal title</b>'};
  opener.closest = () => opener;
  await ui.ids['catalog-results'].fire('click', {target: opener});
  assert.equal(ui.dialog.open, true);
  assert.equal(ui.ids['catalog-exercise-title'].textContent, '<b>literal title</b>');
  const first = ui.form.fire('submit');
  await ui.form.fire('submit');
  assert.equal(calls, 1);
  resolve({ok: false, headers: {get: () => 'application/json'}, json: async () => ({error: 'Choose your group'})});
  await first;
  assert.equal(ui.ids['catalog-assignment-error'].textContent, 'Choose your group');
  assert.equal(ui.form.children['[type="submit"]'].disabled, false);
  assert.equal(ui.dialog.open, true);
  await ui.dialog.children['[data-close-assignment]'].fire('click');
  assert.equal(ui.dialog.open, false);
  assert.equal(opener.focused, true);
});

test('successful assignment redirects to the returned local group', async () => {
  const ui = catalog(async () => ({ok: true, headers: {get: () => 'application/json'},
    json: async () => ({redirect: '/professor/groups/1/'})}));
  ui.form.action = '/professor/bugs/3/assign/';
  await ui.form.fire('submit');
  assert.equal(ui.context.location.assigned, 'http://localhost/professor/groups/1/');
});

test('exercise detail assignment works without catalog filters', async () => {
  const ui = catalog(async () => ({ok: true, headers: {get: () => 'application/json'},
    json: async () => ({redirect: '/professor/groups/1/'})}), true);
  const opener = new Element();
  opener.dataset = {assignUrl: '/professor/bugs/3/assign/', exerciseTitle: 'Exercise'};
  opener.closest = () => opener;
  await ui.ids['exercise-assignment-actions'].fire('click', {target: opener});
  assert.equal(ui.dialog.open, true);
  await ui.form.fire('submit');
  assert.equal(ui.context.location.assigned, 'http://localhost/professor/groups/1/');
});

test('creation tabs support keyboard navigation and retain entered form data', async () => {
  const tabs = [new Element(), new Element()], panels = [new Element(), new Element()];
  tabs.forEach((tab, i) => tab.attrs['aria-controls'] = `panel-${i}`);
  panels[0].draft = 'unsaved upload title';
  const root = {querySelectorAll: () => tabs};
  run('professor-create.js', {document: {querySelector: () => root,
    getElementById: id => panels[Number(id.slice(-1))]}});
  await tabs[0].fire('keydown', {key: 'ArrowRight'});
  assert.equal(panels[0].hidden, true);
  assert.equal(tabs[1].attrs['aria-selected'], 'true');
  assert.equal(tabs[1].focused, true);
  await tabs[1].fire('keydown', {key: 'Home'});
  assert.equal(panels[0].hidden, false);
  assert.equal(panels[0].draft, 'unsaved upload title');
});
