// Read pytest's JUnit XML report into one plain result per test.

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'" };

function unescapeXml(text) {
  return text.replace(/&(#x[0-9a-f]+|#\d+|\w+);/gi, (match, code) => {
    if (code[0] === "#") {
      const number = code[1].toLowerCase() === "x" ? parseInt(code.slice(2), 16) : parseInt(code.slice(1), 10);
      return String.fromCodePoint(number);
    }
    return ENTITIES[code] ?? match;
  });
}

function attributes(tag) {
  const result = {};
  for (const match of tag.matchAll(/([\w:-]+)="([^"]*)"/g)) {
    result[match[1]] = unescapeXml(match[2]);
  }
  return result;
}

// Returns [{ name, file, line, status: "passed" | "failed" | "skipped", message, details }].
function parseJUnit(xml) {
  const results = [];
  const testcase = /<testcase\b([^>]*?)(?:\/>|>([\s\S]*?)<\/testcase>)/g;
  for (const match of xml.matchAll(testcase)) {
    const attrs = attributes(match[1]);
    const body = match[2] || "";
    const problem = body.match(/<(failure|error)\b([^>]*?)(?:\/>|>([\s\S]*?)<\/\1>)/);
    const skipped = /<skipped\b/.test(body);
    let status = "passed";
    let message = "";
    let details = "";
    if (problem) {
      status = "failed";
      message = attributes(problem[2]).message || problem[1];
      details = unescapeXml(problem[3] || "").trim();
    } else if (skipped) {
      status = "skipped";
    }
    results.push({
      name: attrs.name,
      file: attrs.file || "",
      line: attrs.line === undefined ? null : Number(attrs.line),
      status,
      message,
      details,
    });
  }
  return results;
}

module.exports = { parseJUnit };
