const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { projectSnapshot } = require("../snapshot");
const { testCommand } = require("../test-command");

test("author snapshots include source edits and exclude workspace credentials", () => {
  const folder = fs.mkdtempSync(path.join(os.tmpdir(), "debug-gym-snapshot-"));
  try {
    fs.mkdirSync(path.join(folder, ".debug-gym"));
    fs.writeFileSync(path.join(folder, ".debug-gym", "config.json"), "secret");
    fs.writeFileSync(path.join(folder, "main.py"), "changed");
    assert.deepEqual(projectSnapshot(folder), { "main.py": "changed" });
    fs.writeFileSync(path.join(folder, "binary"), Buffer.from([255]));
    assert.throws(() => projectSnapshot(folder), /UTF-8/);
  } finally {
    fs.rmSync(folder, { recursive: true });
  }
});

test("Python and JavaScript commands produce the same JUnit report format", () => {
  const python = testCommand("python", "/tmp/result.xml", ["test_one.py"]);
  assert.equal(python.executable, "python");
  assert.ok(python.args.includes("--junitxml=/tmp/result.xml"));
  assert.ok(python.args.includes("test_one.py"));
  const node = testCommand("javascript", "/tmp/result.xml", []);
  assert.equal(node.executable, "/usr/lib/code-server/lib/node");
  assert.ok(node.args.includes("--test-reporter-destination=/tmp/result.xml"));
});
