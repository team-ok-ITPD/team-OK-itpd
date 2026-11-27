const assert = require("node:assert/strict");
const fs = require("fs");
const os = require("os");
const path = require("path");
const test = require("node:test");
const { ensurePythonEnvironment, pythonExecutable } = require("../python-environment");

test("reuses the shared environment when the pinned pytest version is installed", async (t) => {
  const storage = fs.mkdtempSync(path.join(os.tmpdir(), "debug-gym-python-"));
  t.after(() => fs.rmSync(storage, { recursive: true, force: true }));
  const environment = path.join(storage, "python-env");
  const python = pythonExecutable(environment);
  fs.mkdirSync(path.dirname(python), { recursive: true });
  fs.writeFileSync(python, "");
  const calls = [];

  const result = await ensurePythonEnvironment(environment, {
    async runCommand(executable, args) {
      calls.push({ executable, args });
      return { stdout: "pytest 8.4.2\n", stderr: "" };
    },
    async findPythonCandidate() {
      assert.fail("A valid shared environment must not create another environment.");
    },
  });

  assert.equal(result, python);
  assert.deepEqual(calls, [{ executable: python, args: ["-m", "pytest", "--version"] }]);
});
