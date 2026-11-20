// Capture regular text project files for author saves, excluding session credentials.
const fs = require("fs");
const path = require("path");

function projectSnapshot(folder) {
  const files = {};
  let size = 0;
  const ignored = new Set([".debug-gym", ".git", "__pycache__", ".pytest_cache", "node_modules"]);
  function visit(directory, prefix) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (ignored.has(entry.name) || entry.name === ".env") continue;
      if (entry.isSymbolicLink()) throw new Error("Remove symbolic links before saving the project.");
      const relative = prefix ? prefix + "/" + entry.name : entry.name;
      const target = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        visit(target, relative);
      } else if (entry.isFile()) {
        const buffer = fs.readFileSync(target);
        size += buffer.length;
        if (size > 5_000_000 || Object.keys(files).length >= 100) {
          throw new Error("Project limit: 100 files and 5 MB.");
        }
        const source = buffer.toString("utf8");
        if (!Buffer.from(source).equals(buffer)) throw new Error("Project files must use UTF-8 text.");
        files[relative] = source;
      }
    }
  }
  visit(folder, "");
  return files;
}

module.exports = { projectSnapshot };
