// Reuse one extension-managed Python environment across pulled exercises.

const { execFile } = require("child_process");
const fs = require("fs");
const path = require("path");

const PYTEST_VERSION = "8.4.2";
const PROCESS_TIMEOUT_MS = 180_000;

function run(executable, args, options = {}) {
  return new Promise((resolve, reject) => {
    execFile(
      executable,
      args,
      { timeout: PROCESS_TIMEOUT_MS, maxBuffer: 1_000_000, ...options },
      (error, stdout, stderr) => {
        if (error) {
          const output = `${stderr || ""}${stdout || ""}`.trim();
          reject(new Error(output || error.message, { cause: error }));
        } else {
          resolve({ stdout, stderr });
        }
      },
    );
  });
}

async function findPython() {
  const candidates = process.platform === "win32"
    ? [{ executable: "py", prefix: ["-3"] }, { executable: "python", prefix: [] }]
    : [{ executable: "python3", prefix: [] }, { executable: "python", prefix: [] }];

  for (const candidate of candidates) {
    try {
      const { stdout, stderr } = await run(candidate.executable, [...candidate.prefix, "--version"]);
      const match = /Python\s+(\d+)\.(\d+)/.exec(`${stdout}${stderr}`);
      if (match && (Number(match[1]) > 3 || (Number(match[1]) === 3 && Number(match[2]) >= 10))) {
        return candidate;
      }
    } catch {
      // Try the next standard Python launcher.
    }
  }
  throw new Error("Python 3.10 or newer is required. Install Python, then pull the exercise again.");
}

function pythonExecutable(environmentDirectory) {
  return path.join(
    environmentDirectory,
    process.platform === "win32" ? "Scripts" : "bin",
    process.platform === "win32" ? "python.exe" : "python",
  );
}

async function ensurePythonEnvironment(environmentDirectory, dependencies = {}) {
  const execute = dependencies.runCommand || run;
  const locatePython = dependencies.findPythonCandidate || findPython;
  const python = pythonExecutable(environmentDirectory);
  if (fs.existsSync(python)) {
    try {
      const { stdout, stderr } = await execute(python, ["-m", "pytest", "--version"]);
      if (`${stdout}${stderr}`.includes(`pytest ${PYTEST_VERSION}`)) {
        return python;
      }
    } catch {
      // Rebuild an incomplete or outdated managed environment.
    }
  }

  fs.rmSync(environmentDirectory, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(environmentDirectory), { recursive: true });
  const basePython = await locatePython();
  await execute(basePython.executable, [...basePython.prefix, "-m", "venv", environmentDirectory]);
  await execute(python, [
    "-m", "pip", "install", "--disable-pip-version-check", `pytest==${PYTEST_VERSION}`,
  ]);
  return python;
}

module.exports = { ensurePythonEnvironment, pythonExecutable };
