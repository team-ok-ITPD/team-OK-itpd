// Debug Gym (v2) for VS Code: run the bug's tests, show each result, and submit the fix.

const { execFile } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const vscode = require("vscode");
const { parseJUnit } = require("./junit");
const { siteLink } = require("./links");

const TEST_TIMEOUT_MS = 60_000;
// Written by the Debug Gym server when it opens this folder.
const CONFIG_FILE = path.join(".debug-gym", "config.json");

const ICONS = {
  passed: new vscode.ThemeIcon("pass", new vscode.ThemeColor("testing.iconPassed")),
  failed: new vscode.ThemeIcon("error", new vscode.ThemeColor("testing.iconFailed")),
  skipped: new vscode.ThemeIcon("circle-slash", new vscode.ThemeColor("testing.iconSkipped")),
};

class ResultsProvider {
  constructor() {
    this.results = [];
    this.changed = new vscode.EventEmitter();
    this.onDidChangeTreeData = this.changed.event;
  }

  update(results) {
    this.results = results;
    this.changed.fire();
  }

  // Replace the results of the tests that ran, keep the others.
  merge(results) {
    const byName = new Map(results.map((result) => [result.name, result]));
    const merged = this.results.map((result) => byName.get(result.name) || result);
    for (const result of results) {
      if (!this.results.some((existing) => existing.name === result.name)) {
        merged.push(result);
      }
    }
    this.update(merged);
  }

  getChildren() {
    return this.results;
  }

  getTreeItem(result) {
    const item = new vscode.TreeItem(result.name);
    item.iconPath = ICONS[result.status];
    item.description = result.status === "failed" ? result.message.split("\n")[0] : result.status;
    item.tooltip = new vscode.MarkdownString().appendCodeblock(result.details || result.message || result.status, "text");
    item.contextValue = "debugGymTest";
    const folder = workspaceFolder();
    if (folder && result.file) {
      item.command = {
        command: "vscode.open",
        title: "Open test",
        arguments: [
          vscode.Uri.file(path.join(folder, result.file)),
          { selection: new vscode.Range(result.line ?? 0, 0, result.line ?? 0, 0) },
        ],
      };
    }
    return item;
  }
}

function workspaceFolder() {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
}

function summarize(results) {
  const counts = { passed: 0, failed: 0, skipped: 0 };
  for (const result of results) {
    counts[result.status] += 1;
  }
  return ["failed", "passed", "skipped"]
    .filter((status) => counts[status])
    .map((status) => `${counts[status]} ${status}`)
    .join(", ");
}

// Runs pytest in the workspace and resolves with the parsed results and the console output.
// The server writes the image's Python into the config: code-server resets PATH for extensions.
function runPytest(folder, targets) {
  const python = readConfig(folder)?.python || "python";
  const report = path.join(os.tmpdir(), `debug-gym-${process.pid}-${Date.now()}.xml`);
  const args = ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "junit_family=xunit1", `--junitxml=${report}`, ...targets];
  return new Promise((resolve, reject) => {
    // No __pycache__ folders in the learner's files.
    const env = { ...process.env, PYTHONDONTWRITEBYTECODE: "1" };
    execFile(python, args, { cwd: folder, env, timeout: TEST_TIMEOUT_MS }, (error, stdout, stderr) => {
      const output = `${stdout}${stderr}`;
      let xml = "";
      try {
        xml = fs.readFileSync(report, "utf8");
        fs.rmSync(report, { force: true });
      } catch {
        // No report: pytest did not get as far as running tests.
      }
      if (error?.killed) {
        reject(new Error(`The tests ran for more than ${TEST_TIMEOUT_MS / 1000} seconds and were stopped. Look for a loop that never ends.`));
      } else if (!xml) {
        reject(new Error(error ? `pytest could not run: ${error.message}` : "pytest wrote no report."));
      } else {
        resolve({ results: parseJUnit(xml), output, exitCode: error ? error.code : 0 });
      }
    });
  });
}

function readConfig(folder) {
  try {
    return JSON.parse(fs.readFileSync(path.join(folder, CONFIG_FILE), "utf8"));
  } catch {
    return null;
  }
}

// Report the submission, with a button back to the bug's page on the Debug Gym website.
async function backToWebsite(config, message, testSummary) {
  const text = testSummary ? `${message} (tests: ${testSummary})` : message;
  const buttons = config.site ? ["Back to Debug Gym"] : [];
  if ((await vscode.window.showInformationMessage(text, ...buttons)) === "Back to Debug Gym") {
    await vscode.env.openExternal(vscode.Uri.parse(siteLink(config.site)));
  }
}


function activate(context) {
  const provider = new ResultsProvider();
  const view = vscode.window.createTreeView("debugGym.results", { treeDataProvider: provider });
  const output = vscode.window.createOutputChannel("Debug Gym");
  let busy = false;

  const testButton = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  testButton.text = "$(beaker) Test";
  testButton.tooltip = "Run the bug's tests";
  testButton.command = "debugGym.runTests";
  const submitButton = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 99);
  submitButton.text = "$(cloud-upload) Submit";
  submitButton.tooltip = "Submit your fix to Debug Gym";
  submitButton.command = "debugGym.submit";
  const startConfig = workspaceFolder() && readConfig(workspaceFolder());
  // Bugs without tests (or in languages the image cannot test) only get Submit.
  if (startConfig?.tests) {
    testButton.show();
  }
  if (startConfig) {
    submitButton.show();
  }

  async function run(targets, label) {
    const folder = workspaceFolder();
    if (!folder) {
      vscode.window.showWarningMessage("Open the bug folder to run its tests.");
      return null;
    }
    if (busy) {
      vscode.window.showInformationMessage("Debug Gym is already running the tests.");
      return null;
    }
    busy = true;
    testButton.text = "$(sync~spin) Testing...";
    try {
      await vscode.workspace.saveAll(false);
      output.appendLine(`$ python -m pytest -q ${targets.join(" ")}`.trim());
      const outcome = await vscode.window.withProgress(
        { location: { viewId: "debugGym.results" }, title: label },
        () => runPytest(folder, targets),
      );
      output.appendLine(outcome.output.trimEnd());
      output.appendLine("");
      return outcome;
    } catch (error) {
      output.appendLine(error.message);
      output.show(true);
      vscode.window.showErrorMessage(error.message);
      return null;
    } finally {
      busy = false;
      testButton.text = "$(beaker) Test";
    }
  }

  function show(results) {
    view.description = summarize(provider.results);
    const failed = results.filter((result) => result.status === "failed").length;
    const message = `Tests: ${summarize(results)}`;
    if (failed) {
      vscode.window.showWarningMessage(message);
    } else {
      vscode.window.showInformationMessage(message);
    }
  }

  async function runTests() {
    const config = workspaceFolder() && readConfig(workspaceFolder());
    if (!config?.tests) {
      vscode.window.showInformationMessage("This bug has no tests. Use the debugger to check your fix, then Submit.");
      return null;
    }
    const outcome = await run([], "Running tests");
    if (outcome) {
      provider.update(outcome.results);
      show(outcome.results);
    }
    return outcome;
  }

  async function runTest(result) {
    if (!result?.file) {
      return;
    }
    const outcome = await run([`${result.file}::${result.name}`], `Running ${result.name}`);
    if (outcome) {
      provider.merge(outcome.results);
      show(outcome.results);
    }
  }

  async function submit() {
    const folder = workspaceFolder();
    const config = folder && readConfig(folder);
    if (!config) {
      vscode.window.showWarningMessage(
        "This folder is not connected to Debug Gym. Open it with the website's Open in VS Code button.",
      );
      return;
    }
    // Run the tests first so the student sees how the fix does; the professor still grades it.
    let testSummary = "";
    if (config.tests) {
      const outcome = await runTests();
      if (outcome) {
        testSummary = summarize(outcome.results);
      }
    } else {
      await vscode.workspace.saveAll(false);
    }
    submitButton.text = "$(sync~spin) Submitting...";
    try {
      const code = fs.readFileSync(path.join(folder, config.file), "utf8");
      const response = await fetch(`${config.server}/student/ide/submit/`, {
        method: "POST",
        headers: { Authorization: `Bearer ${config.token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.error || `The server answered with HTTP ${response.status}.`);
      }
      backToWebsite(config, payload.message || "Submitted.", testSummary);
    } catch (error) {
      const reason = error.cause?.code === "ECONNREFUSED" ? "the Debug Gym server could not be reached" : error.message;
      vscode.window.showErrorMessage(`Your fix was not submitted: ${reason}`);
    } finally {
      submitButton.text = "$(cloud-upload) Submit";
    }
  }

  context.subscriptions.push(
    view,
    output,
    testButton,
    submitButton,
    vscode.commands.registerCommand("debugGym.runTests", runTests),
    vscode.commands.registerCommand("debugGym.runTest", runTest),
    vscode.commands.registerCommand("debugGym.submit", submit),
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
