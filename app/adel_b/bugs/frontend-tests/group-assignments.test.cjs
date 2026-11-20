const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

function app() {
  const source = fs.readFileSync(path.join(__dirname, "../static/bugs/app.js"), "utf8").split("/* Events */")[0];
  const elements = new Map();
  const querySelector = (selector) => {
    if (!elements.has(selector)) elements.set(selector, { hidden: true, innerHTML: "", classList: { toggle() {} } });
    return elements.get(selector);
  };
  const context = vm.createContext({
    URL, structuredClone, setTimeout, clearTimeout,
    document: { currentScript: { src: "http://localhost/static/bugs/app.js" }, querySelector, querySelectorAll: () => [] },
    window: { open: () => ({ document: { body: {} }, close() {} }) },
  });
  vm.runInContext(source, context);
  return { elements, run: (code) => vm.runInContext(code, context) };
}

test("group choices identify assigned groups and member counts", () => {
  const page = app();
  page.run(`renderGroupChoices(
    [{ id: 1, name: "CS-101", memberCount: 2 }, { id: 2, name: "CS-102", memberCount: 1 }],
    [{ groupId: 2 }]
  )`);
  const html = page.elements.get("#student-list").innerHTML;
  assert.match(html, /name="groups" value="1"/);
  assert.match(html, /2 students/);
  assert.match(html, /CS-102/);
  assert.match(html, /1 student · Assigned/);
});

test("duplicate exercise assignments keep the earliest deadline first", () => {
  const page = app();
  const result = page.run(`sortAssignments([
    { bugId: "same", groupName: "Late", deadline: "2026-12-10", status: "not-started", title: "Exercise" },
    { bugId: "same", groupName: "Early", deadline: "2026-12-01", status: "not-started", title: "Exercise" }
  ]).map((item) => item.groupName).join(",")`);
  assert.equal(result, "Early,Late");
});

test("practice note names every group and identifies the earliest deadline", () => {
  const page = app();
  page.run(`state.assignments = sortAssignments([
    { bugId: "same", groupName: "Late", assignedBy: "prof", deadline: "2026-12-10", overdue: false, status: "not-started", title: "Exercise" },
    { bugId: "same", groupName: "Early", assignedBy: "prof", deadline: "2026-12-01", overdue: false, status: "not-started", title: "Exercise" }
  ]); renderAssignedNote("same")`);
  const note = page.elements.get("#practice-assigned");
  assert.equal(note.hidden, false);
  assert.match(note.textContent, /Early, Late/);
  assert.match(note.textContent, /earliest deadline shown/);
});
