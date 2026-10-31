const test = require("node:test");
const assert = require("node:assert/strict");
const { createSubmissionSync } = require("../static/bugs/submission-sync.js");

function setup(overrides = {}) {
  const timers = new Map();
  let next = 0;
  let reads = 0;
  const applied = [];
  const errors = [];
  const options = {
    read: async () => { reads += 1; return { version: reads }; },
    apply: async (value) => applied.push(value),
    isActive: () => true,
    onError: (error) => errors.push(error.message),
    setTimer: (fn) => { timers.set(++next, fn); return next; },
    clearTimer: (id) => timers.delete(id),
    ...overrides,
  };
  const sync = createSubmissionSync(options);
  return { sync, timers, applied, errors, reads: () => reads };
}

test("serial reads coalesce focus/timer refresh and schedule exactly one retry", async () => {
  let resolve;
  let reads = 0;
  const a = setup({ read: () => { reads += 1; return new Promise((done) => { resolve = done; }); } });
  const first = a.sync.refresh();
  const second = a.sync.refresh();
  assert.equal(first, second);
  await Promise.resolve();
  assert.equal(reads, 1);
  resolve({ version: 1 });
  await first;
  assert.equal(a.applied.length, 1);
  assert.equal(a.timers.size, 1);
  a.sync.stop();
  assert.equal(a.timers.size, 0);
});

test("inactive pages pause reads and resume immediately on focus", async () => {
  let active = false;
  const a = setup({ isActive: () => active });
  await a.sync.refresh();
  assert.equal(a.reads(), 0);
  assert.equal(a.timers.size, 1);
  active = true;
  await a.sync.refresh();
  assert.equal(a.reads(), 1);
  assert.equal(a.timers.size, 1);
  a.sync.stop();
});

test("a snapshot is discarded if the page becomes inactive during its request", async () => {
  let active = true;
  let resolve;
  const a = setup({ read: () => new Promise((done) => { resolve = done; }), isActive: () => active });
  const request = a.sync.refresh();
  await Promise.resolve();
  active = false;
  resolve({ version: 1 });
  await request;
  assert.equal(a.applied.length, 0);
  a.sync.stop();
});

test("navigation/logout abort pending reads and reject late results", async () => {
  let resolve;
  let signal;
  const a = setup({ read: (value) => { signal = value; return new Promise((done) => { resolve = done; }); } });
  const request = a.sync.refresh();
  await Promise.resolve();
  a.sync.stop();
  assert.equal(signal.aborted, true);
  resolve({ version: 1 });
  await request;
  await a.sync.refresh();
  assert.equal(a.applied.length, 0);
  assert.equal(a.timers.size, 0);
});

test("temporary failures retry and do not stop future updates", async () => {
  let failed = true;
  const a = setup({ read: async () => { if (failed) throw new Error("offline"); return { version: 2 }; } });
  await a.sync.refresh();
  assert.deepEqual(a.errors, ["offline"]);
  assert.equal(a.timers.size, 1);
  failed = false;
  await a.sync.refresh();
  assert.equal(a.applied.length, 1);
  a.sync.stop();
});
