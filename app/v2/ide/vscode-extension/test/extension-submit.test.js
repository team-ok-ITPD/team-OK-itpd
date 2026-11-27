const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const Module = require("node:module");
const test = require("node:test");

test("the no-tests notice can submit the exercise", async (t) => {
  const folder = fs.mkdtempSync(path.join(os.tmpdir(), "debug-gym-submit-"));
  t.after(() => fs.rmSync(folder, { recursive: true, force: true }));
  fs.mkdirSync(path.join(folder, ".debug-gym"));
  fs.writeFileSync(path.join(folder, "main.py"), "fixed = True\n");
  fs.writeFileSync(
    path.join(folder, ".debug-gym", "config.json"),
    JSON.stringify({
      server: "https://debug-gym.example",
      bug: 99,
      file: "main.py",
      tests: false,
      protocol: 3,
      token: "session-token",
    }),
  );

  const commands = new Map();
  const messages = [];
  let submittedRequest;
  const vscode = {
    EventEmitter: class {
      event() {}
      fire() {}
    },
    StatusBarAlignment: { Left: 1 },
    ThemeColor: class {},
    ThemeIcon: class {},
    commands: {
      registerCommand(name, callback) {
        commands.set(name, callback);
        return { dispose() {} };
      },
    },
    window: {
      createTreeView() {
        return { dispose() {} };
      },
      createOutputChannel() {
        return { appendLine() {}, show() {}, dispose() {} };
      },
      createStatusBarItem() {
        return { show() {}, dispose() {} };
      },
      async showInformationMessage(...args) {
        messages.push(args);
        return messages.length === 1 ? "Submit" : undefined;
      },
      showWarningMessage() {},
    },
    workspace: {
      workspaceFolders: [{ uri: { fsPath: folder } }],
      async saveAll() {
        return true;
      },
    },
  };
  const originalLoad = Module._load;
  const originalFetch = global.fetch;
  Module._load = function load(request, parent, isMain) {
    return request === "vscode" ? vscode : originalLoad.call(this, request, parent, isMain);
  };
  global.fetch = async (url, options) => {
    submittedRequest = { url, options };
    return {
      ok: true,
      async json() {
        return { attempt: { id: 1, verified: false } };
      },
    };
  };

  try {
    const extension = require("../extension");
    extension.activate({ subscriptions: [], secrets: { async get() { return null; } } });
    await commands.get("debugGym.runTests")();
  } finally {
    Module._load = originalLoad;
    global.fetch = originalFetch;
  }

  assert.equal(messages[0][0], "This bug has no tests. Use the debugger to check your fix, then submit it.");
  assert.deepEqual(messages[0].slice(1), ["Submit"]);
  assert.equal(submittedRequest.url, "https://debug-gym.example/api/ide/submit/");
  assert.deepEqual(JSON.parse(submittedRequest.options.body), { bug: 99, code: "fixed = True\n" });
  assert.equal(messages[1][0], "Submitted. This exercise has no automated tests.");
});
