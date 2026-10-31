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
