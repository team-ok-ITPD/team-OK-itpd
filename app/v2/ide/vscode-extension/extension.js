// Debug Gym (v2) for VS Code: run the bug's tests, show each result, and submit the fix.

const { execFile } = require("child_process");
const { randomUUID } = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const vscode = require("vscode");
const { parseJUnit } = require("./junit");
const { normalizePairingCode, validateBundle, writeWorkspace } = require("./local-workspace");
const { siteLink } = require("./links");
const { ensurePythonEnvironment, pythonExecutable } = require("./python-environment");

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
      const testRoot = readConfig(folder)?.testRoot || ".";
      item.command = {
        command: "vscode.open",
        title: "Open test",
        arguments: [
          vscode.Uri.file(path.join(folder, testRoot, result.file)),
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

function pairingServerUrl() {
  const server = String(vscode.workspace.getConfiguration("debugGym").get("serverUrl", "") || "").trim();
  if (!server) return null;
  try {
    const url = new URL(server);
    if (!["http:", "https:"].includes(url.protocol) || url.username || url.password) {
      return null;
    }
    return url.toString().replace(/\/+$/, "");
  } catch {
    return null;
  }
}

async function getPairingServerUrl() {
  const configured = pairingServerUrl();
  if (configured) return configured;
  const value = await vscode.window.showInputBox({
    prompt: "Enter the Debug Gym website address (saved in your VS Code user settings)",
    placeHolder: "https://debug-gym.example.edu",
    ignoreFocusOut: true,
  });
  if (!value) return null;
  let server;
  try {
    const url = new URL(value.trim());
    if (!["http:", "https:"].includes(url.protocol) || url.username || url.password) {
      throw new Error();
    }
    server = url.toString().replace(/\/+$/, "");
  } catch {
    vscode.window.showErrorMessage("Enter a valid Debug Gym website URL using http or https.");
    return null;
  }
  await vscode.workspace.getConfiguration("debugGym").update(
    "serverUrl",
    server,
    vscode.ConfigurationTarget.Global,
  );
  return server;
}

async function pullExercise(context) {
  const server = await getPairingServerUrl();
  if (!server) return;
  const codeInput = await vscode.window.showInputBox({
    prompt: "Enter the one-time pairing code from the exercise page",
    placeHolder: "ABCD-EF01-2345-6789-ABCD-EF01",
    ignoreFocusOut: true,
    validateInput(value) {
      try {
        normalizePairingCode(value);
        return undefined;
      } catch (error) {
        return error.message;
      }
    },
  });
  if (!codeInput) return;
  const code = normalizePairingCode(codeInput);
  const folders = await vscode.window.showOpenDialog({
    canSelectFiles: false,
    canSelectFolders: true,
    canSelectMany: false,
    openLabel: "Choose workspace parent folder",
  });
  if (!folders?.length) return;
  const confirmation = await vscode.window.showWarningMessage(
    "The exercise code and tests will run on this computer. Debug Gym will create or reuse one Python virtual environment in VS Code storage and install pytest 8.4.2 from PyPI. Continue only for an exercise source you trust.",
    { modal: true },
    "Pull and set up",
  );
  if (confirmation !== "Pull and set up") return;

  let bundle;
  try {
    bundle = await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: "Pulling exercise from Debug Gym" },
      async () => {
        const response = await fetch(`${server}/api/ide/pair/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code }),
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(payload.error || `The server answered with HTTP ${response.status}.`);
        }
        return validateBundle(payload);
      },
    );
  } catch (error) {
    vscode.window.showErrorMessage(`The exercise was not pulled: ${error.message}`);
    return;
  }

  const connectionId = randomUUID();
  const environmentDirectory = path.join(context.globalStorageUri.fsPath, "python-env");
  const python = pythonExecutable(environmentDirectory);
  let workspace;
  try {
    workspace = writeWorkspace(folders[0].fsPath, bundle, server, connectionId, python);
    await context.secrets.store(`debugGym.session.${connectionId}`, bundle.token);
  } catch (error) {
    if (workspace?.folder && fs.existsSync(workspace.folder)) {
      fs.rmSync(workspace.folder, { recursive: true, force: true });
    }
    vscode.window.showErrorMessage(`The exercise could not be saved locally: ${error.message}`);
    return;
  }

  try {
    await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: "Setting up the Python environment" },
      () => ensurePythonEnvironment(environmentDirectory),
    );
  } catch (error) {
    const action = await vscode.window.showErrorMessage(
      `The exercise was downloaded to ${workspace.folder}, but Python setup failed: ${error.message}`,
      "Open workspace",
    );
    if (action === "Open workspace") {
      await vscode.commands.executeCommand("vscode.openFolder", vscode.Uri.file(workspace.folder), true);
    }
    return;
  }

  await vscode.commands.executeCommand("vscode.openFolder", vscode.Uri.file(workspace.folder), true);
}

async function workspaceToken(context, config) {
  if (config.token) return config.token;
  if (!config.connectionId) return null;
  return context.secrets.get(`debugGym.session.${config.connectionId}`);
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
        () => runPytest(path.join(folder, readConfig(folder)?.testRoot || "."), targets),
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
      const action = await vscode.window.showInformationMessage(
        "This bug has no tests. Use the debugger to check your fix, then submit it.",
        "Submit",
      );
      if (action === "Submit") {
        await submit();
      }
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
    submitButton.text = "$(sync~spin) Submitting...";
    try {
      const token = await workspaceToken(context, config);
      if (!token) {
        vscode.window.showWarningMessage("This local workspace is disconnected. Pull the exercise again from its website page.");
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

      const code = fs.readFileSync(path.join(folder, config.file), "utf8");
      const sessionProtocol = Number(config.protocol) >= 2;
      const endpoint = sessionProtocol ? "/api/ide/submit/" : "/student/ide/submit/";
      const response = await fetch(`${config.server}${endpoint}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify(sessionProtocol ? { bug: config.bug, code } : { code }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.error || `The server answered with HTTP ${response.status}.`);
      }
      const message = payload.attempt
        ? Number.isInteger(payload.attempt.total)
          ? `Submitted: ${payload.attempt.passed} / ${payload.attempt.total} tests pass.`
          : "Submitted. This exercise has no automated tests."
        : payload.message || "Submitted.";
      await backToWebsite(config, message, sessionProtocol ? "" : testSummary);
    } catch (error) {
      const reason = error.cause?.code === "ECONNREFUSED" ? "the Debug Gym server could not be reached" : error.message;
      output.appendLine(`Submission failed: ${error.stack || error.message}`);
      output.show(true);
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
    vscode.commands.registerCommand("debugGym.pullExercise", () => pullExercise(context)),
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
