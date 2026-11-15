const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

function app(fetcher) {
  const source = fs.readFileSync(path.join(__dirname, "../static/bugs/app.js"), "utf8").split("/* Events */")[0];
  const elements = new Map();
  const querySelector = (selector) => {
    assert(!selector.includes("code-input"), "actions must not depend on an editor");
    if (!elements.has(selector)) elements.set(selector, { disabled: false, hidden: true, innerHTML: "" });
    return elements.get(selector);
  };
  const context = vm.createContext({
    URL, structuredClone, setTimeout, clearTimeout,
    document: { currentScript: { src: "http://localhost/static/bugs/app.js" }, querySelector, querySelectorAll: () => [] },
    window: { open: () => ({ document: { body: {} }, close() {} }) },
    fetcher,
    exercise: { id: "demo", code: "original", tests: [{ input: [], expected: [] }] },
  });
  vm.runInContext(source, context);
  vm.runInContext(`apiFetch = fetcher; renderTests = () => {}; toast = () => {};
    state.user = { username: "learner" }; state.practiceId = "demo"; EXERCISES = [exercise];`, context);
  return { context, run: (code) => vm.runInContext(code, context) };
}

test("saved code replaces stale browser state, including an empty source", async () => {
  const a = app(async () => ({ ok: true, json: async () => ({ draft: { code: "", tests: null } }) }));
  a.run('state.drafts.demo = "stale"');
  assert.equal(await a.run("loadDraft(exercise)"), true);
  assert.equal(a.run("currentCode(exercise)"), "");
});

test("deleted drafts reset the cached source and edited tests", async () => {
  const a = app(async () => ({ ok: true, json: async () => ({ draft: null }) }));
  a.run('state.drafts.demo = "stale"; state.tests.demo = [{input: [1], expected: [1]}]');
  assert.equal(await a.run("loadDraft(exercise)"), true);
  assert.equal(a.run("currentCode(exercise)"), "original");
  assert.equal(a.run("state.tests.demo"), undefined);
});

test("a failed draft read prevents running stale code", async () => {
  const a = app(async () => ({ ok: false, status: 503, json: async () => ({ error: "unavailable" }) }));
  a.run('state.drafts.demo = "stale"; runInPython = () => { throw new Error("stale code executed"); }');
  await a.run("handleRunTests()");
  assert.equal(a.run("state.busy"), false);
});

test("late draft responses are discarded after account changes", async () => {
  let resolve;
  const a = app(() => new Promise((done) => { resolve = done; }));
  const loading = a.run("loadDraft(exercise)");
  a.run('state.user = { username: "other" }');
  resolve({ ok: true, json: async () => ({ draft: { code: "private source" } }) });
  assert.equal(await loading, false);
  assert.equal(a.run("state.drafts.demo"), undefined);
});

test("opening VS Code never uploads the cached browser draft", async () => {
  const calls = [];
  const a = app(async (url, options) => {
    calls.push([url, options.method]);
    return { ok: true, json: async () => ({ url: "http://localhost:8080" }) };
  });
  a.run('state.drafts.demo = "stale browser source"');
  await a.run("openWorkspace()");
  assert.deepEqual(calls, [["/api/bugs/demo/vscode/", "POST"]]);
});


test("a new submission reruns saved code once, updates history and skips unchanged snapshots", async () => {
  let options;
  const runs = [];
  let histories = 0;
  const a = app(async () => ({ ok: true, json: async () => ({}) }));
  a.context.DebugGymSubmissionSync = { createSubmissionSync(value) { options = value; return { refresh() {}, stop() {} }; } };
  a.context.runMock = async (_, code) => { runs.push(code); return [{ input: [], expected: [], passed: true }]; };
  a.context.historyMock = async () => { histories += 1; };
  a.run('runInPython = runMock; loadHistory = historyMock; showTestList = () => {}; startSubmissionSync(exercise)');
  const first = { draft: { code: "buggy", tests: null, updatedAt: "first" }, attempt: null };
  await options.apply(first);
  await options.apply(first);
  assert.deepEqual(runs, ["buggy"]);
  const next = { draft: { code: "fixed", tests: null, updatedAt: "next" }, attempt: { id: 12 } };
  await options.apply(next);
  await options.apply(next);
  assert.deepEqual(runs, ["buggy", "fixed"]);
  assert.equal(histories, 2);
  assert.equal(a.run('state.results.demo[0].passed'), true);
  assert.equal(a.run('state.busy'), false);
});

test("live refresh pauses while tests are edited and ignores late runs after navigation", async () => {
  let options;
  let resolve;
  const a = app(async () => ({ ok: true, json: async () => ({}) }));
  a.context.DebugGymSubmissionSync = { createSubmissionSync(value) { options = value; return { refresh() {}, stop() {} }; } };
  a.context.runMock = () => new Promise((done) => { resolve = done; });
  a.run('runInPython = runMock; loadHistory = async () => {}; showTestList = () => {}; startSubmissionSync(exercise)');
  assert.equal(options.isActive(), true);
  a.run('state.editingTest = { id: "demo", index: 0 }');
  assert.equal(options.isActive(), false);
  a.run('state.editingTest = null');
  const updating = options.apply({ draft: { code: "fixed" }, attempt: { id: 1 } });
  a.run('stopSubmissionSync(); state.practiceId = "another"');
  resolve([{ passed: true }]);
  await updating;
  assert.notEqual(a.run('state.results.demo?.[0]?.passed'), true);
});
