// Helpers for materializing an exercise pulled into a learner's local VS Code.

const fs = require("fs");
const path = require("path");

const RESERVED_PARTS = new Set([
  ".debug-gym",
  ".env",
  ".git",
  ".venv",
  ".vscode",
  "__pycache__",
  "node_modules",
]);

function normalizePairingCode(value) {
  const code = String(value || "").replace(/[\s-]/g, "").toUpperCase();
  if (!/^[0-9A-F]{24}$/.test(code)) {
    throw new Error("Enter the 24-character pairing code shown on the exercise page.");
  }
  return code;
}

function validateBundle(bundle) {
  if (
    !bundle || typeof bundle !== "object"
    || typeof bundle.token !== "string" || !bundle.token
    || !bundle.exercise || typeof bundle.exercise !== "object"
    || bundle.exercise.language !== "python"
    || typeof bundle.exercise.title !== "string"
    || !["number", "string"].includes(typeof bundle.exercise.id)
    || typeof bundle.exercise.entryFile !== "string"
    || !bundle.files || typeof bundle.files !== "object" || Array.isArray(bundle.files)
  ) {
    throw new Error("The server returned an invalid Python exercise bundle.");
  }

  const names = Object.keys(bundle.files);
  if (names.length < 1 || names.length > 100) {
    throw new Error("The exercise must contain between 1 and 100 files.");
  }
  let totalBytes = 0;
  for (const [name, contents] of Object.entries(bundle.files)) {
    const parts = name.split("/");
    if (
      !name || name.length > 255 || name.startsWith("/")
      || name.includes("\\") || name.includes(":")
      || parts.some((part) =>
        !part || part === "." || part === ".." || RESERVED_PARTS.has(part.toLowerCase())
        || /[. ]$/.test(part)
        || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$/i.test(part)
      )
      || typeof contents !== "string"
    ) {
      throw new Error("The exercise contains an unsafe or invalid file path.");
    }
    totalBytes += Buffer.byteLength(contents, "utf8");
  }
  if (totalBytes > 5_000_000) {
    throw new Error("The exercise bundle exceeds the 5 MB limit.");
  }
  if (!Object.hasOwn(bundle.files, bundle.exercise.entryFile)) {
    throw new Error("The exercise bundle does not contain its entry file.");
  }
  if (typeof bundle.exercise.tests !== "boolean" || typeof bundle.site !== "string") {
    throw new Error("The server returned incomplete exercise details.");
  }
  try {
    const site = new URL(bundle.site);
    if (!["http:", "https:"].includes(site.protocol)) throw new Error();
  } catch {
    throw new Error("The server returned an invalid exercise website URL.");
  }
  return bundle;
}

function workspaceName(title) {
  const name = title
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 60);
  return name || "debug-gym-exercise";
}

function appendGitignore(folder) {
  const filename = path.join(folder, ".gitignore");
  const existing = fs.existsSync(filename) ? fs.readFileSync(filename, "utf8") : "";
  const required = [".debug-gym/", ".venv/", "__pycache__/", ".pytest_cache/"];
  const additions = required.filter((entry) => !existing.split(/\r?\n/).includes(entry));
  if (additions.length) {
    const separator = existing && !existing.endsWith("\n") ? "\n" : "";
    fs.appendFileSync(filename, `${separator}${additions.join("\n")}\n`, "utf8");
  }
}

function writeWorkspace(parent, bundle, serverUrl, connectionId, python) {
  validateBundle(bundle);
  if (typeof python !== "string" || !path.isAbsolute(python)) {
    throw new Error("The shared Python environment path must be absolute.");
  }
  const base = workspaceName(bundle.exercise.title);
  let folder;
  for (let suffix = 1; suffix <= 100; suffix += 1) {
    const candidate = path.join(parent, suffix === 1 ? base : `${base}-${suffix}`);
    try {
      fs.mkdirSync(candidate);
      folder = candidate;
      break;
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
    }
  }
  if (!folder) {
    throw new Error("Could not find an unused folder name for this exercise.");
  }

  try {
    for (const [name, contents] of Object.entries(bundle.files)) {
      const target = path.resolve(folder, ...name.split("/"));
      const relative = path.relative(folder, target);
      if (relative.startsWith("..") || path.isAbsolute(relative)) {
        throw new Error("The exercise contains a file path outside its workspace.");
      }
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, contents, { encoding: "utf8", flag: "wx" });
    }

    fs.mkdirSync(path.join(folder, ".debug-gym"));
    fs.mkdirSync(path.join(folder, ".vscode"));
    appendGitignore(folder);
    const config = {
      server: serverUrl,
      site: bundle.site,
      bug: bundle.exercise.id,
      file: bundle.exercise.entryFile,
      tests: bundle.exercise.tests,
      testRoot: bundle.exercise.testRoot || ".",
      language: bundle.exercise.language,
      revision: bundle.exercise.revision,
      protocol: 3,
      connectionId,
      python,
    };
    fs.writeFileSync(
      path.join(folder, ".debug-gym", "config.json"),
      `${JSON.stringify(config, null, 2)}\n`,
      { encoding: "utf8", flag: "wx" },
    );
    const launch = bundle.exercise.tests
      ? {
        name: "Debug exercise tests",
        type: "debugpy",
        request: "launch",
        module: "pytest",
        args: ["-q"],
        cwd: "${workspaceFolder}",
        python,
      }
      : {
        name: "Debug exercise",
        type: "debugpy",
        request: "launch",
        program: `\${workspaceFolder}/${bundle.exercise.entryFile}`,
        cwd: "${workspaceFolder}",
        python,
      };
    fs.writeFileSync(
      path.join(folder, ".vscode", "launch.json"),
      `${JSON.stringify({ version: "0.2.0", configurations: [launch] }, null, 2)}\n`,
      { encoding: "utf8", flag: "wx" },
    );
    fs.writeFileSync(
      path.join(folder, ".vscode", "settings.json"),
      `${JSON.stringify({ "python.defaultInterpreterPath": python }, null, 2)}\n`,
      { encoding: "utf8", flag: "wx" },
    );
    return { folder, python };
  } catch (error) {
    fs.rmSync(folder, { recursive: true, force: true });
    throw error;
  }
}

module.exports = { normalizePairingCode, validateBundle, workspaceName, writeWorkspace };
