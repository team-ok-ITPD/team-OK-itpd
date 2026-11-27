// Run with: node --test app/v2/ide/vscode-extension/test/*.test.js
const assert = require("node:assert/strict");
const fs = require("fs");
const os = require("os");
const path = require("path");
const test = require("node:test");
const { normalizePairingCode, validateBundle, writeWorkspace } = require("../local-workspace");

function bundle(overrides = {}) {
  return {
    token: "session-secret",
    site: "http://localhost:8000/student/assignments/1/",
    exercise: {
      id: 1,
      title: "List mutation",
      language: "python",
      entryFile: "main.py",
      tests: true,
      testRoot: ".",
      revision: 1,
    },
    files: {
      "main.py": "def remove_negatives(numbers): return numbers\n",
      "test_main.py": "from main import remove_negatives\n",
      ".gitignore": "build/\n",
    },
    ...overrides,
  };
}

test("normalizes the displayed pairing code and rejects malformed codes", () => {
  assert.equal(normalizePairingCode("abcd-ef01-2345-6789-abcd-ef01"), "ABCDEF0123456789ABCDEF01");
  assert.throws(() => normalizePairingCode("too-short"), /24-character pairing code/);
});

test("validates relative files and rejects paths that can escape or overwrite metadata", () => {
  assert.throws(
    () => validateBundle(bundle({ files: { "main.py": "safe", "../outside.py": "bad" } })),
    /unsafe or invalid file path/,
  );
  assert.throws(
    () => validateBundle(bundle({ files: { "main.py": "safe", ".debug-gym/config.json": "bad" } })),
    /unsafe or invalid file path/,
  );
  assert.throws(
    () => validateBundle(bundle({ files: { "main.py": "safe", ".vscode/launch.json": "bad" } })),
    /unsafe or invalid file path/,
  );
});

test("writes a fresh connected workspace without persisting the bearer token", (t) => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "debug-gym-pairing-"));
  t.after(() => fs.rmSync(parent, { recursive: true, force: true }));

  const python = path.join(parent, "extension-storage", "python-env", "bin", "python");
  const created = writeWorkspace(parent, bundle(), "http://localhost:8000", "connection-id", python);
  assert.equal(fs.readFileSync(path.join(created.folder, "main.py"), "utf8"), bundle().files["main.py"]);
  const config = JSON.parse(fs.readFileSync(path.join(created.folder, ".debug-gym/config.json"), "utf8"));
  assert.equal(config.connectionId, "connection-id");
  assert.equal(config.protocol, 3);
  assert.equal(config.python, python);
  assert.equal(JSON.parse(fs.readFileSync(path.join(created.folder, ".vscode/settings.json"), "utf8"))["python.defaultInterpreterPath"], python);
  assert.equal(fs.existsSync(path.join(created.folder, ".venv")), false);
  assert.equal(Object.hasOwn(config, "token"), false);
  assert.equal(fs.readFileSync(path.join(created.folder, ".gitignore"), "utf8").includes(".venv/"), true);

  const next = writeWorkspace(parent, bundle(), "http://localhost:8000", "second-connection", python);
  assert.notEqual(created.folder, next.folder);
  assert.equal(next.python, python);
  assert.equal(fs.existsSync(path.join(created.folder, "test_main.py")), true);
});
