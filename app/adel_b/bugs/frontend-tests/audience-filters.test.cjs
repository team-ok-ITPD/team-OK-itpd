const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

function app(fetcher) {
  const source = fs.readFileSync(path.join(__dirname, "../static/bugs/app.js"), "utf8").split("/* Events */")[0];
  const elements = new Map();
  const querySelector = (selector) => {
    if (!elements.has(selector)) {
      elements.set(selector, { value: "", hidden: true, innerHTML: "", classList: { toggle() {} } });
    }
    return elements.get(selector);
  };
  const context = vm.createContext({
    URL, structuredClone, setTimeout, clearTimeout,
    document: {
      body: { classList: { toggle() {} }, dataset: {} },
      currentScript: { src: "http://localhost/static/bugs/app.js" },
      querySelector,
      querySelectorAll: () => [],
    },
    window: { open: () => ({ document: { body: {} }, close() {} }) },
    fetcher,
  });
  vm.runInContext(source, context);
  vm.runInContext("apiFetch = fetcher", context);
  return { elements, run: (code) => vm.runInContext(code, context) };
}

test("audience filter requests only the authorized server view", async () => {
  const calls = [];
  const page = app(async (url) => {
    calls.push(url);
    return {
      ok: true,
      json: async () => ({ filter: "group", bugs: [{ id: "assigned", buggyCode: "code", audience: "group" }] }),
    };
  });
  await page.run('loadExercises("group")');
  assert.deepEqual(calls, ["/api/bugs/?filter=group"]);
  assert.equal(page.run("EXERCISES.map((item) => item.id).join(',')"), "assigned");
  assert.equal(page.elements.get("#filter-audience").value, "group");
});

test("switching audience responses replaces rather than extends the catalog", async () => {
  let filter = "public";
  const page = app(async () => ({
    ok: true,
    json: async () => ({ filter, bugs: [{ id: filter, buggyCode: "code", audience: filter }] }),
  }));
  await page.run('loadExercises("public")');
  filter = "my";
  await page.run('loadExercises("my")');
  assert.equal(page.run("EXERCISES.map((item) => item.id).join(',')"), "my");
});
