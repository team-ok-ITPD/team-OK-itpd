// Debug GYM front end: a "New challenge" screen and a "Practice" screen,
// switched with hash routes (#/new and #/practice/<exercise-id>).

// The catalog (titles, code, tests) comes from the Django API at /api/bugs/.
let EXERCISES = [];

// The browser cannot run Python, so each exercise's buggy function is mirrored
// in JavaScript to compute the preview test results.
const RUNNERS = {
  "remove-negatives"(input) {
    // Mirrors Python: list.remove() while a for loop walks the same list.
    const numbers = [...input];
    for (let i = 0; i < numbers.length; i += 1) {
      if (numbers[i] < 0) {
        numbers.splice(numbers.indexOf(numbers[i]), 1);
      }
    }
    return numbers;
  },
  "total-starts-late"(input) {
    let total = 0;
    for (let i = 1; i < input.length; i += 1) {
      total += input[i];
    }
    return total;
  },
  "duplicated-result"(input) {
    const seen = [];
    const result = [];
    for (const item of input) {
      if (!seen.includes(item)) {
        result.push(item);
      }
    }
    return result;
  },
  "missing-last-element"(input) {
    let total = 0;
    for (let i = 0; i < input.length - 1; i += 1) {
      if (input[i] > 0) {
        total += input[i];
      }
    }
    return total;
  },
  "count-words"(input) {
    const counts = {};
    for (const word of input) {
      const key = word.trim();
      counts[key] = (counts[key] || 0) + 1;
    }
    return counts;
  },
};

function fromApi(bug) {
  return {
    ...bug,
    code: bug.buggyCode,
    run: RUNNERS[bug.id] || (() => null),
  };
}

async function loadExercises() {
  const response = await apiFetch("/api/bugs/");
  if (!response.ok) {
    throw new Error(`The catalog answered with HTTP ${response.status}.`);
  }
  const payload = await response.json();
  EXERCISES = payload.bugs.map(fromApi);
}

const STATUS_ICONS = {
  solved: { icon: "i-check", label: "Solved", badge: "success" },
  progress: { icon: "i-clock", label: "In progress", badge: "warning" },
  failed: { icon: "i-x-circle", label: "Not solved", badge: "danger" },
};

const PY_KEYWORDS = new Set([
  "and", "as", "break", "class", "continue", "def", "elif", "else", "except",
  "False", "for", "from", "if", "import", "in", "is", "lambda", "None", "not",
  "or", "pass", "raise", "return", "True", "try", "while", "with",
]);
const PY_BUILTINS = new Set([
  "dict", "enumerate", "int", "len", "list", "print", "range", "set", "str", "sum",
]);

const state = {
  selectedId: "remove-negatives",
  source: "prepared",
  search: "",
  instructions: "",
  practiceId: null,
  lastPracticeId: "remove-negatives",
  results: {},
  selectedTest: {},
  workspaceUrl: null,
  drafts: {},
  history: { items: [], activity: [] },
  user: null,
  afterLogin: "#/new",
  tests: {},
  editingTest: null,
  busy: false,
};

const $ = (selector) => document.querySelector(selector);

/* Server calls */

function csrfToken() {
  const cookie = document.cookie.split("; ").find((item) => item.startsWith("csrftoken="));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
}

// fetch() plus Django's CSRF header on changes, and a sign-out when the session ends.
async function apiFetch(url, options = {}) {
  const method = (options.method || "GET").toUpperCase();
  const headers = { ...options.headers };
  if (method !== "GET") {
    headers["X-CSRFToken"] = csrfToken();
  }
  const response = await fetch(url, { ...options, headers, credentials: "same-origin" });
  if (response.status === 401 && state.user) {
    signedOut();
  }
  return response;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function icon(id, extraClass = "") {
  return `<svg class="icon ${extraClass}" aria-hidden="true"><use href="#${id}"/></svg>`;
}

function findExercise(id) {
  return EXERCISES.find((exercise) => exercise.id === id) || null;
}

// Python-style repr so values read like the learner's own code.
function pyRepr(value) {
  if (Array.isArray(value)) {
    return `[${value.map(pyRepr).join(", ")}]`;
  }
  if (value === null) {
    return "None";
  }
  if (typeof value === "string") {
    return `'${value.replaceAll("\\", "\\\\").replaceAll("'", "\\'").replaceAll("\n", "\\n")}'`;
  }
  if (typeof value === "boolean") {
    return value ? "True" : "False";
  }
  if (typeof value === "object") {
    const entries = Object.entries(value).map(([key, item]) => `${pyRepr(key)}: ${pyRepr(item)}`);
    return `{${entries.join(", ")}}`;
  }
  return String(value);
}

function canonical(value) {
  if (Array.isArray(value)) {
    return `[${value.map(canonical).join(",")}]`;
  }
  if (value && typeof value === "object") {
    const keys = Object.keys(value).sort();
    return `{${keys.map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function currentTests(exercise) {
  return state.tests[exercise.id] || exercise.tests;
}

function isTestEdited(exercise, index) {
  const test = currentTests(exercise)[index];
  const original = exercise.tests[index];
  return canonical([test.input, test.expected]) !== canonical([original.input, original.expected]);
}

function hasEditedTests(exercise) {
  return exercise.tests.some((_, index) => isTestEdited(exercise, index));
}

function runTests(exercise) {
  return currentTests(exercise).map((test) => {
    const actual = exercise.run(structuredClone(test.input));
    return { ...test, actual, passed: canonical(actual) === canonical(test.expected) };
  });
}

function actualText(result) {
  return result.error ?? result.actualRepr ?? pyRepr(result.actual);
}

function testFunctionName(test) {
  return `test_${test.name.toLowerCase().replace(/[^a-z0-9]+/g, "_")}`;
}

function highlightPython(source) {
  const token = /(#.*$)|("""[\s\S]*?"""|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+|.)/g;
  return source
    .split("\n")
    .map((line) => {
      let html = "";
      let afterDef = false;
      for (const match of line.matchAll(token)) {
        const [text, comment, string, number, name] = match;
        const safe = escapeHtml(text);
        if (comment) {
          html += `<span class="tok-comment">${safe}</span>`;
        } else if (string) {
          html += `<span class="tok-string">${safe}</span>`;
        } else if (number) {
          html += `<span class="tok-number">${safe}</span>`;
        } else if (name) {
          if (afterDef) {
            html += `<span class="tok-function">${safe}</span>`;
            afterDef = false;
          } else if (PY_KEYWORDS.has(name)) {
            html += `<span class="tok-keyword">${safe}</span>`;
            afterDef = name === "def";
          } else if (PY_BUILTINS.has(name)) {
            html += `<span class="tok-builtin">${safe}</span>`;
          } else {
            html += safe;
          }
        } else {
          html += safe;
        }
      }
      return `<span class="line">${html || " "}</span>`;
    })
    .join("");
}

let toastTimer;
function toast(message) {
  const element = $("#toast");
  element.textContent = message;
  element.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    element.hidden = true;
  }, 3800);
}

/* Sidebar */

const DAY_MS = 24 * 60 * 60 * 1000;

function startOfDay(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime();
}

function dayGroup(isoTime) {
  const days = Math.round((startOfDay(new Date()) - startOfDay(new Date(isoTime))) / DAY_MS);
  if (days <= 0) {
    return "Today";
  }
  if (days === 1) {
    return "Yesterday";
  }
  return days <= 7 ? "Previous 7 days" : "Older";
}

function historyStatus(id) {
  return state.history.items.find((item) => item.bugId === id)?.status || null;
}

async function loadHistory() {
  try {
    const response = await apiFetch("/api/history/");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    state.history = await response.json();
  } catch {
    return;
  }
  if (!state.practiceId && state.history.items.length > 0) {
    state.lastPracticeId = state.history.items[0].bugId;
    $("#back-to-practice").href = `#/practice/${state.lastPracticeId}`;
  }
  renderHistory();
  renderStreak();
  if (state.practiceId) {
    renderStatus(state.practiceId);
  } else if (!$("#view-new").hidden) {
    renderExerciseList();
  }
}

function renderHistory() {
  const query = state.search.trim().toLowerCase();
  const items = state.history.items.filter((item) => item.title.toLowerCase().includes(query));

  if (items.length === 0) {
    $("#history").innerHTML = query
      ? `<p class="history-empty">No challenges match “${escapeHtml(state.search)}”.</p>`
      : `<p class="history-empty">No challenges yet. Pick an exercise to start.</p>`;
    return;
  }

  const groups = [];
  for (const item of items) {
    const label = dayGroup(item.lastActivity);
    let group = groups.find((existing) => existing.label === label);
    if (!group) {
      group = { label, items: [] };
      groups.push(group);
    }
    group.items.push(item);
  }

  $("#history").innerHTML = groups
    .map(
      (group) => `
        <section>
          <h2>${escapeHtml(group.label)}</h2>
          <ul>
            ${group.items
              .map((item) => {
                const status = STATUS_ICONS[item.status];
                const current = item.bugId === state.practiceId ? ' aria-current="page"' : "";
                return `
                  <li>
                    <button class="history-item" type="button" data-id="${escapeHtml(item.bugId)}"${current}>
                      <span class="status-${item.status}" title="${status.label}">
                        ${icon(status.icon)}
                        <span class="visually-hidden">${status.label}:</span>
                      </span>
                      <span>${escapeHtml(item.title)}</span>
                    </button>
                  </li>`;
              })
              .join("")}
          </ul>
        </section>`,
    )
    .join("");
}

// Consecutive days, ending today or yesterday, with at least one submission.
function renderStreak() {
  const days = new Set(state.history.activity.map((time) => startOfDay(new Date(time))));
  let day = startOfDay(new Date());
  if (!days.has(day)) {
    day = startOfDay(new Date(day - DAY_MS / 2));
  }
  let streak = 0;
  while (days.has(day)) {
    streak += 1;
    day = startOfDay(new Date(day - DAY_MS / 2));
  }
  $("#streak-text").innerHTML = streak
    ? `<strong>${streak}-day</strong> practice streak`
    : "Submit a solution to start a streak";
}

function renderStatus(id) {
  const status = STATUS_ICONS[historyStatus(id)] || { icon: "i-clock", label: "Pending", badge: "warning" };
  const badge = $("#badge-status");
  badge.className = `badge ${status.badge}`;
  badge.innerHTML = `${icon(status.icon)} ${status.label}`;
}

function setSidebar(open) {
  $("#sidebar").classList.toggle("is-open", open);
  $("#scrim").hidden = !open;
  $("#menu-open").setAttribute("aria-expanded", String(open));
}

/* New challenge screen */

function visibleExercises() {
  const topic = $("#filter-topic").value;
  const difficulty = $("#filter-difficulty").value;
  const language = $("#filter-language").value;
  const query = state.search.trim().toLowerCase();
  return EXERCISES.filter(
    (exercise) =>
      (topic === "all" || exercise.topic === topic) &&
      (difficulty === "all" || exercise.difficulty === difficulty) &&
      exercise.language === language &&
      (!query || exercise.title.toLowerCase().includes(query)),
  );
}

function renderExerciseList() {
  const list = $("#exercise-list");

  if (state.source === "ai") {
    list.innerHTML = `
      <div class="empty">
        <strong>AI-generated challenges are not available yet.</strong>
        <span>Describe the bug you want above, and Debug GYM will match it to a prepared exercise.</span>
      </div>`;
    return;
  }

  const exercises = visibleExercises();
  if (exercises.length === 0) {
    list.innerHTML = `
      <div class="empty">
        <strong>No exercises match these filters.</strong>
        <span>Try another topic or difficulty.</span>
      </div>`;
    return;
  }

  if (!exercises.some((exercise) => exercise.id === state.selectedId)) {
    state.selectedId = exercises[0].id;
  }

  list.innerHTML = exercises
    .map((exercise) => {
      const checked = exercise.id === state.selectedId ? " checked" : "";
      const status = STATUS_ICONS[historyStatus(exercise.id)];
      return `
        <label class="exercise-card">
          <input type="radio" name="exercise" value="${exercise.id}"${checked}>
          <span class="exercise-text">
            <strong>${escapeHtml(exercise.title)}</strong>
            <small>${escapeHtml(exercise.summary)}</small>
          </span>
          <span class="exercise-meta">
            ${status ? `<span class="badge ${status.badge} small">${status.label}</span>` : ""}
            <span class="badge">${escapeHtml(exercise.difficulty)}</span>
            <span class="badge">${escapeHtml(exercise.duration)}</span>
          </span>
        </label>`;
    })
    .join("");
}

function renderPreview() {
  const preview = $("#preview");
  const exercise = state.source === "prepared" ? findExercise(state.selectedId) : null;
  const visible = exercise && visibleExercises().includes(exercise);

  if (!visible) {
    preview.innerHTML = `
      <div class="empty">
        <strong>No exercise selected</strong>
        <span>Pick a prepared exercise to see what it involves.</span>
      </div>`;
    return;
  }

  preview.innerHTML = `
    <div>
      <p class="eyebrow">${escapeHtml(exercise.topicLabel)}</p>
      <h2>${escapeHtml(exercise.title)}</h2>
    </div>
    <div class="preview-meta">
      <span class="badge">${escapeHtml(exercise.difficulty)}</span>
      <span class="badge">${escapeHtml(exercise.language)}</span>
      <span class="badge">${icon("i-clock")} ${escapeHtml(exercise.duration)}</span>
    </div>
    <p class="preview-description">${escapeHtml(exercise.description)}</p>
    <div>
      <h3>What you'll do</h3>
      <ul class="steps">
        <li>
          <span class="source-icon">${icon("i-search")}</span>
          <span>
            <strong>Investigate, fix, and test</strong>
            <small>Reproduce the failure, trace it with the debugger, then prove your fix with the tests.</small>
          </span>
        </li>
        <li>
          <span class="source-icon">${icon("i-eye-off")}</span>
          <span>
            <strong>Keep the solution hidden</strong>
            <small>The reference fix stays out of sight. Hints only appear when you ask.</small>
          </span>
        </li>
      </ul>
    </div>
    <div class="preview-actions">
      <button class="button ghost" type="button" data-action="cancel">Cancel</button>
      <button class="button primary" type="button" data-action="start">
        ${icon("i-play")}
        Start practice
      </button>
    </div>`;
}

function renderNewChallenge() {
  renderExerciseList();
  renderPreview();
}

async function askForExercise(query) {
  const response = await apiFetch("/api/exercises", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`The catalog answered with HTTP ${response.status}.`);
  }
  if (!response.ok) {
    throw new Error(payload.error || `The catalog answered with HTTP ${response.status}.`);
  }
  return payload.exercise;
}

function showAskResult(kind, message) {
  const result = $("#ask-result");
  result.hidden = false;
  result.className = `ask-result ${kind}`;
  result.textContent = message;
}

async function handleAsk(event) {
  event.preventDefault();
  const query = String(new FormData(event.target).get("query") || "");
  showAskResult("pending", "Matching your request...");

  try {
    const match = await askForExercise(query);
    state.workspaceUrl = match.workspaceUrl;
    const exercise = findExercise(match.id);
    if (!exercise) {
      showAskResult("success", `Matched “${match.title}”, but this page doesn't know that exercise yet.`);
      return;
    }

    state.source = "prepared";
    state.selectedId = exercise.id;
    document.querySelector('input[name="source"][value="prepared"]').checked = true;
    $("#filter-topic").value = exercise.topic;
    $("#filter-difficulty").value = exercise.difficulty;
    renderNewChallenge();
    showAskResult("success", `Matched “${exercise.title}”. Its workspace is ready. Review it, then start practice.`);
    $("#preview").scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (error) {
    const message = error instanceof TypeError ? `The catalog could not be reached: ${error.message}` : error.message;
    showAskResult("error", message);
  }
}

/* Practice screen */

function testEditForm(exercise, test, index) {
  const restore = isTestEdited(exercise, index)
    ? '<button class="button ghost small" type="button" data-test-action="restore">Restore original</button>'
    : "";
  return `
    <form class="test-edit" data-index="${index}" novalidate>
      <label>
        Input
        <input name="input" value="${escapeHtml(pyRepr(test.input))}" spellcheck="false" autocomplete="off">
        <small class="field-error" data-error="input" hidden></small>
      </label>
      <label>
        Expected
        <input name="expected" value="${escapeHtml(pyRepr(test.expected))}" spellcheck="false" autocomplete="off">
        <small class="field-error" data-error="expected" hidden></small>
      </label>
      <small class="field-hint">Write Python values, for example [4, -3, 5] or {'apple': 2}.</small>
      <p class="ask-result error" data-error="form" hidden></p>
      <div class="test-edit-actions">
        <button class="button primary small" type="submit">Save test</button>
        <button class="button ghost small" type="button" data-test-action="cancel">Cancel</button>
        ${restore}
      </div>
    </form>`;
}

function renderTests(exercise) {
  const results = state.results[exercise.id] || runTests(exercise);
  state.results[exercise.id] = results;
  const passed = results.filter((result) => result.passed).length;
  const selected = state.selectedTest[exercise.id] ?? results.findIndex((result) => !result.passed);
  const editing = state.editingTest?.id === exercise.id ? state.editingTest.index : null;

  const score = $("#tests-score");
  score.textContent = `${passed} / ${results.length} checks passed`;
  score.className = `tests-score ${passed === results.length ? "pass" : "fail"}`;

  $("#test-list").innerHTML = results
    .map((result, index) => {
      let status = `<span class="status-failed">${icon("i-x-circle")}</span>`;
      let badge = '<span class="badge danger small">Failed</span>';
      if (result.notRun) {
        status = `<span class="status-progress">${icon("i-clock")}</span>`;
        badge = '<span class="badge small">Not run</span>';
      } else if (result.passed) {
        status = `<span class="status-solved">${icon("i-check")}</span>`;
        badge = '<span class="badge success small">Passed</span>';
      }
      const edited = isTestEdited(exercise, index) ? '<span class="badge warning small">Edited</span>' : "";
      const body =
        index === editing
          ? testEditForm(exercise, result, index)
          : `
            <span class="test-values">
              <span><b>Input</b> ${escapeHtml(pyRepr(result.input))}</span>
              <span><b>Expected</b> ${escapeHtml(pyRepr(result.expected))}</span>
              <span class="${result.passed || result.notRun ? "" : "mismatch"}"><b>Actual</b> ${escapeHtml(result.notRun ? "—" : actualText(result))}</span>
            </span>`;
      return `
        <li class="test-item${index === selected ? " is-selected" : ""}">
          <div class="test-top">
            <button class="test-row" type="button" data-index="${index}" aria-pressed="${index === selected}">
              <span class="test-head">
                ${status}
                Test ${index + 1} · ${escapeHtml(result.name)}
                ${edited}
                ${badge}
              </span>
            </button>
            <span class="test-actions">
              <button class="button ghost small" type="button" data-test-action="run" data-index="${index}" aria-label="Run test ${index + 1}"${state.busy ? " disabled" : ""}>
                ${icon("i-play")} Run
              </button>
              <button class="button ghost small" type="button" data-test-action="edit" data-index="${index}" aria-label="Edit test ${index + 1}"${index === editing ? " disabled" : ""}>
                Edit
              </button>
            </span>
          </div>
          ${body}
        </li>`;
    })
    .join("");

  renderReproduce(exercise, results[Math.max(selected, 0)]);
}

function renderReproduce(exercise, test) {
  const call = `${exercise.functionName}(${pyRepr(test.input)})`;
  if (test.notRun) {
    $("#reproduce-text").innerHTML = `This test changed. Press <b>Run</b> on it to see what <code>${escapeHtml(call)}</code> returns.`;
    $("#reproduce-code").textContent = `>>> ${call}`;
    return;
  }
  $("#reproduce-text").innerHTML = test.passed
    ? `This case passes: <code>${escapeHtml(call)}</code> returns the expected value. Pick a failing test to reproduce the bug.`
    : `Call the function with <code>${escapeHtml(pyRepr(test.input))}</code>. You should get <code>${escapeHtml(pyRepr(test.expected))}</code>, but the code returns <code>${escapeHtml(actualText(test))}</code>.`;
  $("#reproduce-code").textContent =
    `>>> from ${exercise.file.replace(".py", "")} import ${exercise.functionName}\n` +
    `>>> ${call}\n${actualText(test)}`;
}

function renderWorkspace() {
  $("#workspace").innerHTML = `
    <button class="button secondary" type="button" id="open-workspace">
      ${icon("i-external")}
      Open in VS Code online
    </button>
    <p>Your code and the tests open in VS Code. Press F5 to debug the tests with breakpoints.</p>
    <p class="workspace-error" id="workspace-error" role="alert" hidden></p>`;
}

function consolePrint(html) {
  const output = $("#console-output");
  output.insertAdjacentHTML("beforeend", `${html}\n`);
  output.scrollTop = output.scrollHeight;
}

function resetConsole(exercise) {
  $("#console-output").innerHTML = "";
  $("#console-prompt").textContent = `${exercise.id} $`;
  consolePrint(`Debug GYM console. Type <span class="cmd">help</span> for commands.`);
}

function pytestReport(exercise, results) {
  const dots = results.map((result) => (result.passed ? "." : "F")).join("");
  const failures = results
    .filter((result) => !result.passed)
    .map(
      (result) =>
        `<span class="fail">FAILED tests/test_${escapeHtml(exercise.functionName)}.py::${testFunctionName(result)}` +
        (result.error
          ? ` - ${escapeHtml(result.error)}</span>`
          : ` - assert ${escapeHtml(actualText(result))} == ${escapeHtml(pyRepr(result.expected))}</span>`),
    );
  const passed = results.filter((result) => result.passed).length;
  const failed = results.length - passed;
  const summary = [failed && `${failed} failed`, passed && `${passed} passed`].filter(Boolean).join(", ");
  return [dots, ...failures, `<span class="${failed ? "fail" : "pass"}">${summary}</span>`].join("\n");
}

function handleConsole(event) {
  event.preventDefault();
  const exercise = findExercise(state.practiceId);
  const input = $("#console-command");
  const command = input.value.trim();
  input.value = "";
  if (!exercise || !command) {
    return;
  }

  consolePrint(`<span class="cmd">${escapeHtml(exercise.id)} $ ${escapeHtml(command)}</span>`);
  if (command === "help") {
    consolePrint("pytest     run the exercise tests\nrepro      run the selected test input\nclear      clear the console");
  } else if (command === "clear") {
    $("#console-output").innerHTML = "";
  } else if (command === "pytest" || command === "python -m pytest" || command === "python -m pytest -q") {
    handleRunTests();
  } else if (command === "repro") {
    const results = state.results[exercise.id] || runTests(exercise);
    const test = results[Math.max(state.selectedTest[exercise.id] ?? results.findIndex((r) => !r.passed), 0)];
    consolePrint(`${escapeHtml(exercise.functionName)}(${escapeHtml(pyRepr(test.input))}) -> ${escapeHtml(actualText(test))}`);
  } else {
    consolePrint(`${escapeHtml(command.split(" ")[0])}: not available in this preview console. Use the VS Code workspace terminal for a full shell.`);
  }
}

function renderPractice(id) {
  const exercise = findExercise(id);
  if (!exercise) {
    location.hash = "#/new";
    return;
  }

  if (state.practiceId !== exercise.id) {
    state.practiceId = exercise.id;
    resetConsole(exercise);
    loadDraft(exercise);
  }
  state.lastPracticeId = exercise.id;

  $("#practice-crumb").textContent = `Practice / ${exercise.topicLabel}`;
  $("#practice-title").textContent = exercise.title;
  $("#badge-difficulty").textContent = exercise.difficulty;
  $("#badge-language").textContent = exercise.language;
  $("#file-name").textContent = exercise.file;
  $("#symptom").textContent = exercise.symptom;
  $("#explanation").textContent = exercise.explanation;

  const notes = $("#your-notes");
  notes.hidden = !state.instructions.trim();
  notes.textContent = `Your instructions: ${state.instructions.trim()}`;

  renderTests(exercise);
  renderWorkspace(exercise);
  renderStatus(exercise.id);
  document.title = `Debug GYM | ${exercise.title}`;
}

/* Code editor */

const SAVE_DELAY_MS = 600;
let saveTimer;

function draftUrl(exercise) {
  return `/api/bugs/${encodeURIComponent(exercise.id)}/draft/`;
}

function setSaveState(text) {
  $("#save-state").textContent = text;
}

function renderEditor(exercise) {
  const code = $("#code-input").value;
  $("#code").innerHTML = highlightPython(code);
  const edited = code !== exercise.code;
  const badge = $("#code-state");
  badge.textContent = edited ? "Edited" : "Buggy";
  badge.className = `badge ${edited ? "warning" : "danger"} small`;
  $("#reset-code").hidden = !edited;
}

function setEditorCode(exercise, code) {
  $("#code-input").value = code;
  renderEditor(exercise);
}

async function loadDraft(exercise) {
  clearTimeout(saveTimer);
  const shown = state.drafts[exercise.id] ?? exercise.code;
  setEditorCode(exercise, shown);
  setSaveState("Python 3.12");
  try {
    const response = await apiFetch(draftUrl(exercise));
    const payload = await response.json();
    if (state.practiceId !== exercise.id) {
      return;
    }
    const savedTests = payload.draft?.tests || null;
    if (canonical(savedTests) !== canonical(state.tests[exercise.id] || null)) {
      if (savedTests) {
        state.tests[exercise.id] = savedTests;
      } else {
        delete state.tests[exercise.id];
      }
      delete state.results[exercise.id];
      renderTests(exercise);
    }
    // Skip stale code: the learner already started typing.
    if ($("#code-input").value !== shown) {
      return;
    }
    if (payload.draft) {
      state.drafts[exercise.id] = payload.draft.code;
      setEditorCode(exercise, payload.draft.code);
      setSaveState("Saved");
    }
  } catch {
    setSaveState("Saved code unavailable");
  }
}

async function saveDraft(exercise, code) {
  setSaveState("Saving...");
  try {
    const response = await apiFetch(draftUrl(exercise), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || `HTTP ${response.status}`);
    }
    const firstSave = !(exercise.id in state.drafts);
    state.drafts[exercise.id] = code;
    if (state.practiceId === exercise.id) {
      setSaveState("Saved");
    }
    if (firstSave) {
      loadHistory();
    }
  } catch (error) {
    setSaveState("Not saved");
    toast(`Your code could not be saved: ${error.message}`);
  }
}

function handleCodeInput() {
  const exercise = findExercise(state.practiceId);
  renderEditor(exercise);
  setSaveState("Editing...");
  clearTimeout(saveTimer);
  const code = $("#code-input").value;
  saveTimer = setTimeout(() => saveDraft(exercise, code), SAVE_DELAY_MS);
}

function handleCodeKeydown(event) {
  if (event.key !== "Tab" || event.shiftKey || event.metaKey || event.ctrlKey || event.altKey) {
    return;
  }
  // Indent with four spaces, as Python code expects, instead of leaving the editor.
  event.preventDefault();
  event.target.setRangeText("    ", event.target.selectionStart, event.target.selectionEnd, "end");
  handleCodeInput();
}

async function resetCode() {
  const exercise = findExercise(state.practiceId);
  clearTimeout(saveTimer);
  setEditorCode(exercise, exercise.code);
  delete state.drafts[exercise.id];
  try {
    await apiFetch(draftUrl(exercise), { method: "DELETE" });
    setSaveState("Reset to the original code");
    loadHistory();
  } catch {
    setSaveState("Not saved");
  }
  $("#code-input").focus();
}

/* Python runner (Pyodide in a web worker) */

const WORKER_URL = new URL("python-worker.js", document.currentScript.src);
const RUN_TIMEOUT_MS = 5000;
const python = { worker: null, ready: false, loading: null, nextId: 1 };

function startPython() {
  python.worker = new Worker(WORKER_URL);
  python.ready = false;
  python.loading = new Promise((resolve, reject) => {
    python.worker.addEventListener("message", function onReady(event) {
      if (event.data.type === "ready") {
        python.ready = true;
        python.worker.removeEventListener("message", onReady);
        resolve();
      } else if (event.data.type === "load-failed") {
        reject(new Error(event.data.failure));
      }
    });
    python.worker.addEventListener("error", (event) => reject(new Error(event.message || "Python could not start.")));
  });
}

function stopPython() {
  python.worker?.terminate();
  python.worker = null;
}

async function runPython(exercise, code, tests) {
  if (!python.worker) {
    startPython();
  }
  if (!python.ready) {
    consolePrint("Loading Python in your browser (the first run downloads about 10 MB)...");
  }
  try {
    await python.loading;
  } catch (error) {
    stopPython();
    throw error;
  }

  const id = python.nextId++;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      // A run that never finishes is usually an infinite loop: restart Python.
      python.worker.removeEventListener("message", onMessage);
      stopPython();
      reject(new Error(`Your code ran for more than ${RUN_TIMEOUT_MS / 1000} seconds and was stopped. Look for a loop that never ends.`));
    }, RUN_TIMEOUT_MS);

    function onMessage(event) {
      if (event.data.id !== id) {
        return;
      }
      clearTimeout(timer);
      python.worker.removeEventListener("message", onMessage);
      if (event.data.failure) {
        reject(new Error(event.data.failure));
      } else {
        resolve(event.data);
      }
    }

    python.worker.addEventListener("message", onMessage);
    python.worker.postMessage({
      id,
      code,
      functionName: exercise.functionName,
      tests: tests.map(({ input, expected }) => ({ input, expected })),
    });
  });
}

// Runs code against the given tests and returns one result per test (or null on failure).
async function runInPython(exercise, code, tests, command) {
  consolePrint(`<span class="cmd">${escapeHtml(exercise.id)} $ ${escapeHtml(command)}</span>`);
  try {
    const output = await runPython(exercise, code, tests);
    if (output.stdout) {
      consolePrint(escapeHtml(output.stdout.replace(/\n$/, "")));
    }
    // A file that does not even load fails every test with the same error.
    const results = tests.map((test, index) => ({
      ...test,
      ...(output.error ? { error: output.error, passed: false } : output.results[index]),
    }));
    consolePrint(pytestReport(exercise, results));
    return results;
  } catch (error) {
    consolePrint(`<span class="fail">${escapeHtml(error.message)}</span>`);
    return null;
  }
}

function showTestList(exercise) {
  renderTests(exercise);
  $("#tests-toggle").setAttribute("aria-expanded", "true");
  $("#test-list").hidden = false;
}

function setBusy(busy, button, label) {
  state.busy = busy;
  $("#run-tests").disabled = busy;
  $("#submit").disabled = busy;
  document.querySelectorAll('[data-test-action="run"]').forEach((element) => {
    element.disabled = busy;
  });
  if (busy) {
    button.innerHTML = `${icon("i-loader", "spin")} ${label}`;
  } else {
    $("#run-tests").innerHTML = `${icon("i-play")} Run Tests`;
    $("#submit").innerHTML = `${icon("i-send")} Submit Solution`;
    const exercise = findExercise(state.practiceId);
    if (exercise) {
      renderTests(exercise);
    }
  }
}

async function handleRunTests() {
  const exercise = findExercise(state.practiceId);
  if ($("#run-tests").disabled) {
    return;
  }
  setBusy(true, $("#run-tests"), "Running...");
  const results = await runInPython(exercise, $("#code-input").value, currentTests(exercise), "python -m pytest -q");
  if (results) {
    state.results[exercise.id] = results;
    delete state.selectedTest[exercise.id];
    showTestList(exercise);
  }
  setBusy(false);
}

async function handleRunOne(index) {
  const exercise = findExercise(state.practiceId);
  if (state.busy) {
    return;
  }
  const test = currentTests(exercise)[index];
  const button = document.querySelector(`[data-test-action="run"][data-index="${index}"]`);
  setBusy(true, button, "Running");
  const command = `python -m pytest -q tests/test_${exercise.functionName}.py::${testFunctionName(test)}`;
  const results = await runInPython(exercise, $("#code-input").value, [test], command);
  if (results) {
    const all = state.results[exercise.id] || runTests(exercise);
    all[index] = results[0];
    state.results[exercise.id] = all;
    state.selectedTest[exercise.id] = index;
    showTestList(exercise);
  }
  setBusy(false);
}

/* Editing one test */

function testUrl(exercise, index) {
  return `/api/bugs/${encodeURIComponent(exercise.id)}/tests/${index}/`;
}

function startEditingTest(index) {
  const exercise = findExercise(state.practiceId);
  state.editingTest = { id: exercise.id, index };
  state.selectedTest[exercise.id] = index;
  renderTests(exercise);
  document.querySelector(`.test-edit[data-index="${index}"] input`)?.focus();
}

function stopEditingTest() {
  state.editingTest = null;
  renderTests(findExercise(state.practiceId));
}

// Store the learner's tests from the server and mark a changed test as not run yet.
function applyTests(exercise, payload, index) {
  if (payload.edited) {
    state.tests[exercise.id] = payload.tests;
  } else {
    delete state.tests[exercise.id];
  }
  const all = state.results[exercise.id] || runTests(exercise);
  all[index] = { ...currentTests(exercise)[index], notRun: true, passed: false };
  state.results[exercise.id] = all;
  state.editingTest = null;
  renderTests(exercise);
  loadHistory();
}

async function saveTestEdit(form) {
  const exercise = findExercise(state.practiceId);
  const index = Number(form.dataset.index);
  clearAuthErrors(form);
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  try {
    const response = await apiFetch(testUrl(exercise, index), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    const payload = await response.json();
    if (!response.ok) {
      showAuthError(form, "form", payload.error || `The server answered with HTTP ${response.status}.`);
      for (const [name, message] of Object.entries(payload.fields || {})) {
        showAuthError(form, name, message);
      }
      return;
    }
    applyTests(exercise, payload, index);
    toast(`Test ${index + 1} saved. Press Run to try it.`);
  } catch {
    showAuthError(form, "form", "The server could not be reached. Try again in a moment.");
  } finally {
    button.disabled = false;
  }
}

async function restoreTest(index) {
  const exercise = findExercise(state.practiceId);
  try {
    const response = await apiFetch(testUrl(exercise, index), { method: "DELETE" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || `HTTP ${response.status}`);
    }
    applyTests(exercise, payload, index);
    toast(`Test ${index + 1} is back to the original.`);
  } catch (error) {
    toast(`The test could not be restored: ${error instanceof TypeError ? "the server could not be reached" : error.message}`);
  }
}

async function handleSubmit() {
  const exercise = findExercise(state.practiceId);
  const code = $("#code-input").value;
  setBusy(true, $("#submit"), "Submitting...");
  try {
    // Submissions are graded on the original tests, never on the learner's edits.
    const edited = hasEditedTests(exercise);
    if (edited) {
      consolePrint("Submitting checks your code against the original tests, not your edited ones.");
    }
    const results = await runInPython(exercise, code, exercise.tests, "python -m pytest -q");
    if (results && !edited) {
      state.results[exercise.id] = results;
      delete state.selectedTest[exercise.id];
      showTestList(exercise);
    }
    if (!results) {
      toast("Your solution was not submitted because the tests could not run.");
      return;
    }
    const passed = results.filter((result) => result.passed).length;
    const response = await apiFetch(`/api/bugs/${encodeURIComponent(exercise.id)}/attempts/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, passed, total: results.length }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || `HTTP ${response.status}`);
    }
    toast(
      payload.attempt.solved
        ? "Solved! Every test passes. Your solution is saved."
        : `Submitted: ${passed} / ${results.length} tests pass. Keep going.`,
    );
    await loadHistory();
  } catch (error) {
    toast(`Your solution could not be submitted: ${error instanceof TypeError ? "the server could not be reached" : error.message}`);
  } finally {
    setBusy(false);
  }
}

async function openWorkspace() {
  const exercise = findExercise(state.practiceId);
  const button = $("#open-workspace");
  const error = $("#workspace-error");
  if (button.disabled) {
    return;
  }
  // Open the tab now, while the click still counts, so the browser does not block it.
  const tab = window.open("", "_blank");
  if (tab) {
    tab.document.title = "Starting VS Code...";
    tab.document.body.textContent = "Starting VS Code for this exercise...";
  }
  button.disabled = true;
  button.innerHTML = `${icon("i-loader", "spin")} Starting VS Code...`;
  error.hidden = true;
  try {
    // VS Code gets the saved code, so save the latest edits first.
    const code = $("#code-input").value;
    if (code !== (state.drafts[exercise.id] ?? exercise.code)) {
      clearTimeout(saveTimer);
      await saveDraft(exercise, code);
    }
    const response = await apiFetch(`/api/bugs/${encodeURIComponent(exercise.id)}/vscode/`, { method: "POST" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || `The server answered with HTTP ${response.status}.`);
    }
    if (tab) {
      tab.opener = null;
      tab.location = payload.url;
    } else {
      window.location.href = payload.url;
    }
  } catch (failure) {
    tab?.close();
    error.textContent = failure instanceof TypeError ? "The server could not be reached." : failure.message;
    error.hidden = false;
  } finally {
    button.disabled = false;
    button.innerHTML = `${icon("i-external")} Open in VS Code online`;
  }
}

function setMenu(open) {
  $("#options-menu").hidden = !open;
  $("#options-button").setAttribute("aria-expanded", String(open));
  if (open) {
    $("#options-menu button").focus();
  }
}

function handleMenu(action) {
  const exercise = findExercise(state.practiceId);
  setMenu(false);
  if (action === "restart") {
    delete state.results[exercise.id];
    delete state.selectedTest[exercise.id];
    resetConsole(exercise);
    renderTests(exercise);
    toast("Exercise view restarted.");
  } else if (action === "copy") {
    navigator.clipboard
      .writeText(exercise.code)
      .then(() => toast("Code copied to the clipboard."))
      .catch(() => toast("Copying isn't allowed here. Select the code instead."));
  } else if (action === "challenges") {
    location.hash = "#/new";
  }
}

/* Accounts */

function setUser(user) {
  state.user = user;
  document.body.classList.toggle("signed-out", !user);
  if (user) {
    $("#profile-name").textContent = user.username;
    $("#profile-email").textContent = user.email;
    $("#profile-avatar").textContent = user.username.slice(0, 2).toUpperCase();
  }
}

function resetUserState() {
  clearTimeout(saveTimer);
  Object.assign(state, {
    drafts: {},
    results: {},
    selectedTest: {},
    tests: {},
    editingTest: null,
    history: { items: [], activity: [] },
    practiceId: null,
    lastPracticeId: "remove-negatives",
    instructions: "",
  });
}

function goTo(hash) {
  if (location.hash === hash) {
    route();
  } else {
    location.hash = hash;
  }
}

function signedIn(user) {
  resetUserState();
  setUser(user);
  for (const form of document.querySelectorAll(".auth-form")) {
    form.reset();
  }
  goTo(state.afterLogin);
  state.afterLogin = "#/new";
  loadHistory();
}

function signedOut() {
  resetUserState();
  setUser(null);
  goTo("#/login");
}

function showAuth(mode) {
  $("#auth").hidden = false;
  $("#login-form").hidden = mode !== "login";
  $("#register-form").hidden = mode !== "register";
  document.title = mode === "login" ? "Debug GYM | Log in" : "Debug GYM | Create account";
  $(`#${mode}-form input`).focus();
}

function clearAuthErrors(form) {
  form.querySelectorAll("[data-error]").forEach((element) => {
    element.hidden = true;
    element.textContent = "";
  });
  form.querySelectorAll("input").forEach((input) => input.removeAttribute("aria-invalid"));
}

function showAuthError(form, name, message) {
  const element = form.querySelector(`[data-error="${name}"]`);
  element.textContent = message;
  element.hidden = false;
  form.querySelector(`input[name="${name}"]`)?.setAttribute("aria-invalid", "true");
}

async function handleAuthSubmit(event, url) {
  event.preventDefault();
  const form = event.target;
  const button = form.querySelector('button[type="submit"]');
  clearAuthErrors(form);
  button.disabled = true;
  try {
    const response = await apiFetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    const payload = await response.json();
    if (!response.ok) {
      showAuthError(form, "form", payload.error || `The server answered with HTTP ${response.status}.`);
      for (const [name, message] of Object.entries(payload.fields || {})) {
        showAuthError(form, name, message);
      }
      return;
    }
    signedIn(payload.user);
  } catch {
    showAuthError(form, "form", "The server could not be reached. Try again in a moment.");
  } finally {
    button.disabled = false;
  }
}

async function handleLogout() {
  try {
    await apiFetch("/api/auth/logout/", { method: "POST" });
  } finally {
    signedOut();
  }
}

/* Routing */

function route() {
  const [, view, id] = location.hash.split("/");
  const authView = view === "login" || view === "register";
  if (!state.user) {
    if (!authView) {
      // Come back to the page they asked for once they log in.
      state.afterLogin = location.hash || "#/new";
      history.replaceState(null, "", "#/login");
    }
    showAuth(view === "register" ? "register" : "login");
    return;
  }
  if (authView) {
    goTo("#/new");
    return;
  }
  $("#auth").hidden = true;

  const practice = view === "practice";
  $("#view-new").hidden = practice;
  $("#view-practice").hidden = !practice;
  setSidebar(false);
  setMenu(false);

  if (practice) {
    renderPractice(id || state.lastPracticeId);
  } else {
    state.practiceId = null;
    document.title = "Debug GYM | New challenge";
    renderNewChallenge();
  }
  $("#back-to-practice").href = `#/practice/${state.lastPracticeId}`;
  renderHistory();
  window.scrollTo(0, 0);
}

/* Events */

$("#request-form").addEventListener("submit", handleAsk);
$("#login-form").addEventListener("submit", (event) => handleAuthSubmit(event, "/api/auth/login/"));
$("#register-form").addEventListener("submit", (event) => handleAuthSubmit(event, "/api/auth/register/"));
$("#logout").addEventListener("click", handleLogout);

document.querySelectorAll('input[name="source"]').forEach((input) => {
  input.addEventListener("change", () => {
    state.source = input.value;
    renderNewChallenge();
  });
});

["#filter-topic", "#filter-difficulty", "#filter-language"].forEach((selector) => {
  $(selector).addEventListener("change", renderNewChallenge);
});

$("#exercise-list").addEventListener("change", (event) => {
  if (event.target.name === "exercise") {
    state.selectedId = event.target.value;
    renderPreview();
  }
});

$("#instructions").addEventListener("input", (event) => {
  state.instructions = event.target.value;
});

$("#preview").addEventListener("click", (event) => {
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action === "start") {
    location.hash = `#/practice/${state.selectedId}`;
  } else if (action === "cancel") {
    location.hash = `#/practice/${state.lastPracticeId}`;
  }
});

$("#history").addEventListener("click", (event) => {
  const item = event.target.closest(".history-item");
  if (!item) {
    return;
  }
  if (item.dataset.id) {
    location.hash = `#/practice/${item.dataset.id}`;
  } else {
    toast("That challenge isn't available in this prototype yet.");
  }
});

$("#search").addEventListener("input", (event) => {
  state.search = event.target.value;
  renderHistory();
  if (!$("#view-new").hidden) {
    renderNewChallenge();
  }
});

$("#test-list").addEventListener("click", (event) => {
  const action = event.target.closest("[data-test-action]");
  if (action) {
    const index = Number(action.dataset.index ?? action.closest(".test-edit")?.dataset.index);
    if (action.dataset.testAction === "run") {
      handleRunOne(index);
    } else if (action.dataset.testAction === "edit") {
      startEditingTest(index);
    } else if (action.dataset.testAction === "cancel") {
      stopEditingTest();
    } else if (action.dataset.testAction === "restore") {
      restoreTest(index);
    }
    return;
  }
  const row = event.target.closest(".test-row");
  if (row) {
    state.selectedTest[state.practiceId] = Number(row.dataset.index);
    renderTests(findExercise(state.practiceId));
  }
});

$("#test-list").addEventListener("submit", (event) => {
  event.preventDefault();
  saveTestEdit(event.target);
});

$("#test-list").addEventListener("keydown", (event) => {
  if (event.key === "Escape" && event.target.closest(".test-edit")) {
    event.stopPropagation();
    stopEditingTest();
  }
});

$("#tests-toggle").addEventListener("click", (event) => {
  const expanded = event.currentTarget.getAttribute("aria-expanded") === "true";
  event.currentTarget.setAttribute("aria-expanded", String(!expanded));
  $("#test-list").hidden = expanded;
});

$("#console-form").addEventListener("submit", handleConsole);
$("#code-input").addEventListener("input", handleCodeInput);
$("#code-input").addEventListener("keydown", handleCodeKeydown);
$("#reset-code").addEventListener("click", resetCode);
$("#run-tests").addEventListener("click", handleRunTests);
$("#submit").addEventListener("click", handleSubmit);
$("#workspace").addEventListener("click", (event) => {
  if (event.target.closest("#open-workspace")) {
    openWorkspace();
  }
});

$("#options-button").addEventListener("click", () => setMenu($("#options-menu").hidden));
$("#options-menu").addEventListener("click", (event) => {
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action) {
    handleMenu(action);
  }
});

$("#menu-open").addEventListener("click", () => setSidebar(true));
$("#menu-close").addEventListener("click", () => setSidebar(false));
$("#scrim").addEventListener("click", () => setSidebar(false));

document.addEventListener("click", (event) => {
  if (!event.target.closest(".menu")) {
    setMenu(false);
  }
});

document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    if (window.matchMedia("(max-width: 860px)").matches) {
      setSidebar(true);
    }
    $("#search").focus();
  } else if (event.key === "Escape") {
    if (!$("#options-menu").hidden) {
      setMenu(false);
      $("#options-button").focus();
    }
    setSidebar(false);
  }
});

if (!/Mac|iPhone|iPad/.test(navigator.platform)) {
  $("#search-shortcut").textContent = "Ctrl K";
}

window.addEventListener("hashchange", route);
if (!location.hash) {
  history.replaceState(null, "", "#/new");
}
async function start() {
  try {
    const response = await apiFetch("/api/auth/me/");
    setUser((await response.json()).user);
    await loadExercises();
  } catch (error) {
    toast(error instanceof TypeError ? "The catalog could not be reached." : error.message);
  }
  route();
  if (state.user) {
    loadHistory();
  }
}

start();
