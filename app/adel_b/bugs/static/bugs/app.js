// Debug GYM front end: a "New challenge" screen and a "Practice" screen,
// switched with hash routes (#/new and #/practice/<exercise-id>).

// The catalog (titles, code, tests) comes from the Django API at /api/bugs/.
let EXERCISES = [];

// Prepared buggy functions supply an initial preview; saved solutions are run
// in the Python worker before their actual test results are displayed.
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
    run: RUNNERS[bug.id] || null,
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

const state = {
  selectedId: "remove-negatives",
  // The last "Describe the bug" search: { query, ids } with the best match first, or null.
  matches: null,
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
  teach: { editing: null, assigning: null, groups: [], total: 0 },
  assignments: [],
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
  const user = state.user;
  const response = await fetch(url, { ...options, headers, credentials: "same-origin" });
  if (response.status === 401 && user && state.user === user) {
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
  if (!exercise.run) {
    return currentTests(exercise).map((test) => ({ ...test, notRun: true, passed: false }));
  }
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
  loadAssignments();
  try {
    const response = await apiFetch("/api/history/");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const history = await response.json();
    if (state.user !== user) return;
    state.history = history;
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
  // After a search, list only its matches, best match first.
  const pool = state.matches ? state.matches.ids.map(findExercise).filter(Boolean) : EXERCISES;
  const titleMatches = (exercise) => !query || exercise.title.toLowerCase().includes(query);
  const filtered = pool.filter(
    (exercise) =>
      (topic === "all" || exercise.topic === topic) &&
      (difficulty === "all" || exercise.difficulty === difficulty) &&
      exercise.language === language &&
      titleMatches(exercise),
  );
  if (state.matches) {
    return filtered;
  }
  // Assigned exercises lead the list even when the filters would hide them.
  const assigned = state.assignments.map((item) => findExercise(item.bugId)).filter(Boolean).filter(titleMatches);
  const assignedIds = new Set(assigned.map((exercise) => exercise.id));
  return [...assigned, ...filtered.filter((exercise) => !assignedIds.has(exercise.id))];
}

function matchBar() {
  if (!state.matches) {
    return "";
  }
  const count = state.matches.ids.length;
  if (count === 0) {
    return `
    <div class="match-bar">
      <span>No exercises match “${escapeHtml(state.matches.query)}”.</span>
      <button class="button ghost small" type="button" data-action="clear-matches">Show all exercises</button>
    </div>`;
  }
  return `
    <div class="match-bar">
      <span>${count === 1 ? "1 exercise matches" : `${count} exercises match`} “${escapeHtml(state.matches.query)}”${count === 1 ? "." : ", best match first."}</span>
      <button class="button ghost small" type="button" data-action="clear-matches">Show all exercises</button>
    </div>`;
}

function clearMatches() {
  state.matches = null;
  $("#ask-result").hidden = true;
  renderNewChallenge();
}

function renderExerciseList() {
  const list = $("#exercise-list");

  if (state.source === "ai") {
    list.innerHTML = `
      <div class="empty">
        <strong>AI-generated challenges are not available yet.</strong>
        <span>Describe the bug you want below, and Debug GYM will match it to prepared exercises.</span>
      </div>`;
    return;
  }

  const exercises = visibleExercises();
  if (exercises.length === 0) {
    const searched = state.matches && state.matches.ids.length === 0;
    list.innerHTML = `
      ${matchBar()}
      <div class="empty">
        <strong>${searched ? "No exercises match your search." : "No exercises match these filters."}</strong>
        <span>${searched ? "Try other words, or show all exercises." : "Try another topic or difficulty."}</span>
      </div>`;
    return;
  }

  if (!exercises.some((exercise) => exercise.id === state.selectedId)) {
    state.selectedId = exercises[0].id;
  }

  list.innerHTML = matchBar() + exercises
    .map((exercise, index) => {
      const checked = exercise.id === state.selectedId ? " checked" : "";
      const status = STATUS_ICONS[historyStatus(exercise.id)];
      const best = state.matches && index === 0 ? '<span class="badge accent small">Best match</span>' : "";
      const assignment = assignmentFor(exercise.id);
      const assignedBadge = assignment
        ? `<span class="badge accent small">${assignment.deadline ? `Assigned · due ${escapeHtml(shortDate(assignment.deadline))}` : "Assigned"}</span>`
        : "";
      return `
        <label class="exercise-card">
          <input type="radio" name="exercise" value="${exercise.id}"${checked}>
          <span class="exercise-text">
            <strong>${escapeHtml(exercise.title)}</strong>
            <small>${escapeHtml(exercise.summary)}</small>
          </span>
          <span class="exercise-meta">
            ${best}
            ${assignedBadge}
            ${status ? `<span class="badge ${status.badge} small">${status.label}</span>` : ""}
            <span class="badge">${escapeHtml(exercise.difficulty)}</span>
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
  if (response.status === 404) {
    return { exercises: [], matchedBy: null };
  }
  if (!response.ok) {
    throw new Error(payload.error || `The catalog answered with HTTP ${response.status}.`);
  }
  return { exercises: payload.exercises || [payload.exercise], matchedBy: payload.matchedBy || "title" };
}

function showAskResult(kind, message) {
  const result = $("#ask-result");
  result.hidden = false;
  result.className = `ask-result ${kind}`;
  result.textContent = message;
}

async function handleAsk(event) {
  event.preventDefault();
  const query = String(new FormData(event.target).get("query") || "").trim();
  showAskResult("pending", "Finding related exercises...");

  try {
    const found = await askForExercise(query);
    const matches = found.exercises.filter((match) => findExercise(match.id));
    if (matches.length === 0) {
      // An empty result empties the list too, instead of keeping the previous search.
      state.matches = { query, ids: [] };
      renderNewChallenge();
      showAskResult("error", `No exercise matches “${query}”. Try words from a title, like “negative” or “duplicate”.`);
      return;
    }

    // Show every related exercise: clear the filters that could hide some of them.
    state.matches = { query, ids: matches.map((match) => match.id) };
    state.source = "prepared";
    state.selectedId = matches[0].id;
    document.querySelector('input[name="source"][value="prepared"]').checked = true;
    $("#filter-topic").value = "all";
    $("#filter-difficulty").value = "all";
    renderNewChallenge();
    const count = matches.length;
    const where = found.matchedBy === "title" ? "" : " No titles matched, so these come from the descriptions.";
    showAskResult(
      "success",
      (count === 1
        ? `Found 1 exercise: “${matches[0].title}”.`
        : `Found ${count} exercises. The best match, “${matches[0].title}”, is selected.`) + where,
    );
    $("#exercise-list").scrollIntoView({ behavior: "smooth", block: "nearest" });
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
              <button class="button ghost small" type="button" data-test-action="edit" data-index="${index}" aria-label="Edit test ${index + 1}"${state.busy || index === editing ? " disabled" : ""}>
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
    <p>Edit your code in VS Code. Press F5 to debug, then use Test or Submit in VS Code. The page uses your latest saved solution.</p>
    <p class="workspace-error" id="workspace-error" role="alert" hidden></p>`;
}

function consolePrint(html) {
  const output = $("#console-output");
  output.insertAdjacentHTML("beforeend", `${html}\n`);
  output.scrollTop = output.scrollHeight;
}

function resetConsole(exercise) {
  $("#console-output").innerHTML = "";
  consolePrint("Edit your code in VS Code, then run the tests or submit your saved solution.");
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

function renderPractice(id) {
  const exercise = findExercise(id);
  if (!exercise) {
    location.hash = "#/new";
    return;
  }

  if (state.practiceId !== exercise.id) {
    state.editingTest = null;
    state.practiceId = exercise.id;
    resetConsole(exercise);
  }
  state.lastPracticeId = exercise.id;

  $("#practice-crumb").textContent = `Practice / ${exercise.topicLabel}`;
  renderAssignedNote(exercise.id);
  $("#practice-title").textContent = exercise.title;
  $("#badge-difficulty").textContent = exercise.difficulty;
  $("#badge-language").textContent = exercise.language;
  $("#symptom").textContent = exercise.symptom;
  $("#explanation").textContent = exercise.explanation;

  const notes = $("#your-notes");
  notes.hidden = !state.instructions.trim();
  notes.textContent = `Your instructions: ${state.instructions.trim()}`;

  renderTests(exercise);
  renderWorkspace(exercise);
  renderStatus(exercise.id);
  document.title = `Debug GYM | ${exercise.title}`;
  startSubmissionSync(exercise);
}

/* Live submissions: stop on route/account changes and never overlap reads/runs. */

let practiceEpoch = 0;
let submissionSync = null;

function stopSubmissionSync() {
  practiceEpoch += 1;
  submissionSync?.stop();
  submissionSync = null;
}

function startSubmissionSync(exercise) {
  if (submissionSync) return;
  const user = state.user;
  const epoch = practiceEpoch;
  const current = () => state.user === user && state.practiceId === exercise.id && practiceEpoch === epoch;
  let lastSnapshot = null;
  let lastMessage = "Watching for VS Code submissions...";
  const status = (message) => { if (current()) $("#sync-state").textContent = message; };
  status(lastMessage);
  submissionSync = DebugGymSubmissionSync.createSubmissionSync({
    isActive: () => current() && !document.hidden && !state.busy && !state.editingTest,
    read: async (signal) => {
      const response = await apiFetch(`/api/bugs/${encodeURIComponent(exercise.id)}/progress/`, { signal });
      const snapshot = await response.json();
      if (!response.ok) throw new Error(snapshot.error || `HTTP ${response.status}`);
      return snapshot;
    },
    apply: async (snapshot) => {
      if (!current()) return;
      const fingerprint = canonical([snapshot.draft, snapshot.attempt?.id ?? null]);
      if (fingerprint === lastSnapshot) { status(lastMessage); return; }
      lastSnapshot = fingerprint;
      applyDraft(exercise, snapshot.draft);
      status(snapshot.attempt ? "Submission received. Running tests..." : "Running tests on your saved solution...");
      setBusy(true, $("#run-tests"), "Running...");
      try {
        const results = await runInPython(exercise, currentCode(exercise), currentTests(exercise), "python -m pytest -q");
        if (!current()) return;
        if (results) {
          state.results[exercise.id] = results;
          delete state.selectedTest[exercise.id];
          showTestList(exercise);
          lastMessage = snapshot.attempt ? "Submission received. Tests updated automatically." : "Tests up to date. Watching for VS Code submissions...";
        } else {
          lastMessage = "Automatic tests could not run. Use Run Tests to retry.";
        }
        await loadHistory();
        status(lastMessage);
      } finally {
        setBusy(false);
      }
    },
    onError: () => status("Connection interrupted. Retrying automatically..."),
  });
  void submissionSync.refresh();
}

/* Saved code: source editing belongs in VS Code. */

function draftUrl(exercise) {
  return `/api/bugs/${encodeURIComponent(exercise.id)}/draft/`;
}

function currentCode(exercise) {
  return state.drafts[exercise.id] ?? exercise.code;
}

function applyDraft(exercise, draft) {
  const previousCode = currentCode(exercise);
  const previousTests = canonical(state.tests[exercise.id] || null);
  if (draft) {
    state.drafts[exercise.id] = draft.code;
  } else {
    delete state.drafts[exercise.id];
  }
  if (draft?.tests) {
    state.tests[exercise.id] = draft.tests;
  } else {
    delete state.tests[exercise.id];
  }
  const changed = previousCode !== currentCode(exercise) || previousTests !== canonical(state.tests[exercise.id] || null);
  if (changed) {
    state.results[exercise.id] = currentTests(exercise).map((test) => ({ ...test, notRun: true, passed: false }));
    renderTests(exercise);
  }
  return changed;
}

async function loadDraft(exercise) {
  const user = state.user;
  try {
    const response = await apiFetch(draftUrl(exercise));
    const payload = await response.json();
    if (state.user !== user || state.practiceId !== exercise.id) {
      return false;
    }
    if (!response.ok) {
      throw new Error(payload.error || `HTTP ${response.status}`);
    }
    applyDraft(exercise, payload.draft);
    return true;
  } catch (error) {
    if (state.user === user && state.practiceId === exercise.id) {
      toast(`Saved code could not be loaded: ${error instanceof TypeError ? "the server could not be reached" : error.message}`);
    }
    return false;
  }
}

/* Python runner (Pyodide in a web worker) */

const WORKER_URL = new URL(`python-worker.js${new URL(document.currentScript.src).search}`, document.currentScript.src);
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

async function runPython(exercise, code, tests, { literal = false } = {}) {
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
      literal,
    });
  });
}

// Runs code against the given tests and returns one result per test (or null on failure).
async function runInPython(exercise, code, tests, command) {
  const user = state.user;
  const epoch = practiceEpoch;
  const current = () => state.user === user && state.practiceId === exercise.id && practiceEpoch === epoch;
  consolePrint(`<span class="cmd">${escapeHtml(exercise.id)} $ ${escapeHtml(command)}</span>`);
  try {
    const output = await runPython(exercise, code, tests);
    if (!current()) return null;
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
    if (current()) consolePrint(`<span class="fail">${escapeHtml(error.message)}</span>`);
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
  document.querySelectorAll('[data-test-action="run"], [data-test-action="edit"]').forEach((element) => {
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
  if (state.busy || !exercise) return;
  setBusy(true, $("#run-tests"), "Running...");
  try {
    if (!(await loadDraft(exercise))) return;
    const results = await runInPython(exercise, currentCode(exercise), currentTests(exercise), "python -m pytest -q");
    if (results) {
      state.results[exercise.id] = results;
      delete state.selectedTest[exercise.id];
      showTestList(exercise);
    }
  } finally {
    setBusy(false);
  }
}

async function handleRunOne(index) {
  const exercise = findExercise(state.practiceId);
  if (state.busy) {
    return;
  }
  const button = document.querySelector(`[data-test-action="run"][data-index="${index}"]`);
  setBusy(true, button, "Running");
  if (!(await loadDraft(exercise))) {
    setBusy(false);
    return;
  }
  const test = currentTests(exercise)[index];
  const command = `python -m pytest -q tests/test_${exercise.functionName}.py::${testFunctionName(test)}`;
  const results = await runInPython(exercise, currentCode(exercise), [test], command);
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
  if (state.busy || !exercise) return;
  setBusy(true, $("#submit"), "Submitting...");
  try {
    if (!(await loadDraft(exercise))) return;
    const code = currentCode(exercise);
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
      .writeText(currentCode(exercise))
      .then(() => toast("Code copied to the clipboard."))
      .catch(() => toast("Copying is not available here. Open the code in VS Code instead."));
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
    const role = user.role === "professor" ? "Professor" : "Student";
    $("#profile-email").textContent = `${role} · ${user.email}`;
    document.body.dataset.role = user.role || "student";
    $("#nav-teach").hidden = user.role !== "professor";
    $("#nav-assignments").hidden = user.role === "professor";
    $("#profile-avatar").textContent = user.username.slice(0, 2).toUpperCase();
  }
}

function resetUserState() {
  clearTimeout(saveTimer);
  // Nothing from the previous account stays in the page, even hidden.
  for (const selector of ["#assignment-list", "#teach-list", "#results", "#student-list", "#history"]) {
    $(selector).innerHTML = "";
  }
  $("#assignments-count").hidden = true;
  Object.assign(state, {
    drafts: {},
    results: {},
    selectedTest: {},
    tests: {},
    editingTest: null,
    history: { items: [], activity: [] },
    assignments: [],
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
  goTo(state.afterLogin === "#/new" && user.role === "professor" ? "#/teach" : state.afterLogin);
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
  form.querySelectorAll("[aria-invalid]").forEach((input) => input.removeAttribute("aria-invalid"));
}

function showAuthError(form, name, message) {
  const element = form.querySelector(`[data-error="${name}"]`);
  if (!element) {
    return;
  }
  element.textContent = message;
  element.hidden = false;
  form.querySelector(`[name="${name}"]`)?.setAttribute("aria-invalid", "true");
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

/* Teaching (professor pages) */

const STUDENT_STATUS = {
  "not-started": { label: "Not started", badge: "" },
  progress: { label: "In progress", badge: "warning" },
  failed: { label: "Not solved", badge: "danger" },
  solved: { label: "Solved", badge: "success" },
};
const EMPTY_TEST = { name: "", input: "", expected: "" };

function isProfessor() {
  return state.user?.role === "professor";
}

async function teachFetch(url, options = {}) {
  const response = await apiFetch(url, {
    ...options,
    headers: options.body ? { "Content-Type": "application/json" } : undefined,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(payload.error || `The server answered with HTTP ${response.status}.`);
    error.fields = payload.fields || {};
    error.status = response.status;
    throw error;
  }
  return payload;
}

function failureText(error) {
  return error instanceof TypeError ? "The server could not be reached." : error.message;
}

/* My exercises */

async function renderTeachList() {
  document.title = "Debug GYM | Teaching";
  const list = $("#teach-list");
  list.innerHTML = '<div class="empty"><span>Loading your exercises...</span></div>';
  try {
    const { exercises } = await teachFetch("/api/teach/exercises/");
    if (exercises.length === 0) {
      list.innerHTML = `
        <div class="empty">
          <strong>No exercises yet.</strong>
          <span>Create your first one: buggy code and the tests it should pass.</span>
        </div>`;
      return;
    }
    list.innerHTML = exercises
      .map(
        (exercise) => `
          <article class="teach-row">
            <div>
              <h2>${escapeHtml(exercise.title)}</h2>
              <p>${escapeHtml(exercise.summary || exercise.description)}</p>
              <div class="badges">
                <span class="badge small">${escapeHtml(exercise.difficulty)}</span>
                <span class="badge small">${escapeHtml(exercise.topicLabel)}</span>
                <span class="badge small">${exercise.tests.length} ${exercise.tests.length === 1 ? "test" : "tests"}</span>
              </div>
            </div>
            <div class="teach-stats">
              <span><strong>${exercise.assigned}</strong> ${exercise.assigned === 1 ? "group" : "groups"} · ${exercise.assignedStudents} students</span>
              <span><strong>${exercise.solved}</strong> solved</span>
            </div>
            <div class="row-actions">
              <a class="button ghost small" href="#/teach/${encodeURIComponent(exercise.id)}/edit">Edit</a>
              <a class="button primary small" href="#/teach/${encodeURIComponent(exercise.id)}">Assign &amp; results</a>
            </div>
          </article>`,
      )
      .join("");
  } catch (error) {
    list.innerHTML = `<div class="empty"><strong>Your exercises could not be loaded.</strong><span>${escapeHtml(failureText(error))}</span></div>`;
  }
}

/* Exercise editor */

function testRowHtml(test, index) {
  const field = (name, label, placeholder) => `
    <label>
      <span>${label}</span>
      <input name="tests.${index}.${name}" value="${escapeHtml(test[name])}" placeholder="${placeholder}" spellcheck="false" autocomplete="off">
      <small class="field-error" data-error="tests.${index}.${name}" hidden></small>
    </label>`;
  return `
    <div class="test-row" data-index="${index}">
      <span class="test-number">${index + 1}</span>
      ${field("name", "Name", "Empty list")}
      ${field("input", "Input", "[0, 1, 0]")}
      ${field("expected", "Expected", "2")}
      <button class="icon-button" type="button" data-remove-test="${index}" aria-label="Remove test ${index + 1}">
        ${icon("i-x")}
      </button>
    </div>`;
}

function readTests() {
  return [...document.querySelectorAll("#test-rows .test-row")].map((row) => {
    const index = row.dataset.index;
    const value = (name) => row.querySelector(`[name="tests.${index}.${name}"]`).value;
    return { name: value("name").trim(), input: value("input").trim(), expected: value("expected").trim() };
  });
}

function renderTestRows(tests) {
  $("#test-rows").innerHTML = tests.map(testRowHtml).join("");
  // Keep at least one row so there is always somewhere to type.
  $("#test-rows").querySelectorAll("[data-remove-test]").forEach((button) => {
    button.disabled = tests.length === 1;
  });
}

function fillExerciseForm(exercise) {
  const form = $("#exercise-form");
  form.reset();
  clearAuthErrors(form);
  $("#check-result").hidden = true;
  const values = exercise || {};
  for (const name of ["title", "summary", "description", "functionName", "file", "buggyCode", "symptom", "explanation"]) {
    form.elements[name].value = values[name] || "";
  }
  form.elements.difficulty.value = values.difficulty || "Easy";
  form.elements.topic.value = values.topic || "arrays";
  renderTestRows(values.editTests?.length ? values.editTests : [{ ...EMPTY_TEST }]);
}

function readExerciseForm() {
  const form = $("#exercise-form");
  const value = (name) => form.elements[name].value;
  return {
    title: value("title"),
    summary: value("summary"),
    description: value("description"),
    difficulty: value("difficulty"),
    topic: value("topic"),
    functionName: value("functionName").trim(),
    file: value("file").trim(),
    buggyCode: value("buggyCode"),
    symptom: value("symptom"),
    explanation: value("explanation"),
    tests: readTests(),
  };
}

async function renderTeachEditor(slug) {
  state.teach.editing = slug || null;
  const isNew = !slug;
  $("#edit-title").textContent = isNew ? "New exercise" : "Edit exercise";
  $("#edit-crumb").textContent = isNew ? "New exercise" : "Edit";
  $("#delete-exercise").hidden = isNew;
  $("#edit-assign-link").hidden = isNew;
  document.title = `Debug GYM | ${isNew ? "New exercise" : "Edit exercise"}`;
  fillExerciseForm(null);
  if (isNew) {
    $("#exercise-form").elements.title.focus();
    return;
  }
  $("#edit-assign-link").href = `#/teach/${encodeURIComponent(slug)}`;
  try {
    const { exercise } = await teachFetch(`/api/teach/exercises/${encodeURIComponent(slug)}/`);
    if (state.teach.editing !== slug) {
      return;
    }
    fillExerciseForm(exercise);
    $("#edit-title").textContent = exercise.title;
  } catch (error) {
    toast(error.status === 404 ? "That exercise was not found." : failureText(error));
    goTo("#/teach");
  }
}

async function saveExercise(event) {
  event.preventDefault();
  const form = $("#exercise-form");
  const button = $("#save-exercise");
  clearAuthErrors(form);
  button.disabled = true;
  const slug = state.teach.editing;
  try {
    const { exercise } = await teachFetch(slug ? `/api/teach/exercises/${encodeURIComponent(slug)}/` : "/api/teach/exercises/", {
      method: slug ? "PUT" : "POST",
      body: JSON.stringify(readExerciseForm()),
    });
    // The catalog on the other pages now includes this exercise.
    await loadExercises();
    toast(slug ? "Exercise saved." : "Exercise created. Now assign it to students.");
    goTo(`#/teach/${encodeURIComponent(exercise.id)}`);
  } catch (error) {
    showAuthError(form, "form", error.message);
    for (const [name, message] of Object.entries(error.fields || {})) {
      showAuthError(form, name, message);
    }
    form.querySelector('[aria-invalid="true"]')?.focus();
  } finally {
    button.disabled = false;
  }
}

async function deleteExercise() {
  const slug = state.teach.editing;
  const title = $("#exercise-form").elements.title.value;
  if (!slug || !window.confirm(`Delete “${title}”? Students lose it, with their code and submissions.`)) {
    return;
  }
  try {
    await teachFetch(`/api/teach/exercises/${encodeURIComponent(slug)}/`, { method: "DELETE" });
    await loadExercises();
    toast("Exercise deleted.");
    goTo("#/teach");
  } catch (error) {
    toast(failureText(error));
  }
}

// Run the buggy code against the tests in the browser: a good exercise fails at least one.
async function checkExercise() {
  const data = readExerciseForm();
  const result = $("#check-result");
  const button = $("#check-exercise");
  const show = (kind, html) => {
    result.hidden = false;
    result.className = `check-result wide ${kind}`;
    result.innerHTML = html;
  };
  if (!data.functionName || !data.buggyCode.trim() || data.tests.some((test) => !test.input || !test.expected)) {
    show("bad", "Fill in the function name, the code, and every test's input and expected value first.");
    return;
  }
  button.disabled = true;
  show("", "Running the buggy code in your browser (the first run downloads Python, about 10 MB)...");
  try {
    const output = await runPython({ functionName: data.functionName }, data.buggyCode, data.tests, { literal: true });
    if (output.error) {
      show("bad", `The code could not run: ${escapeHtml(output.error)}`);
      return;
    }
    const lines = output.results.map((outcome, index) => {
      const name = escapeHtml(data.tests[index].name || `Test ${index + 1}`);
      const verdict = outcome.passed ? "passes" : `fails (got ${escapeHtml(outcome.error || outcome.actualRepr)})`;
      return `<li>${name}: ${verdict}</li>`;
    });
    const failed = output.results.filter((outcome) => !outcome.passed).length;
    if (failed === 0) {
      show("warn", `<strong>Every test passes on the buggy code.</strong> Add a test that shows the bug, or students have nothing to find.<ul>${lines.join("")}</ul>`);
    } else {
      show("good", `<strong>${failed} of ${output.results.length} tests fail on the buggy code.</strong> Students have a bug to find.<ul>${lines.join("")}</ul>`);
    }
  } catch (error) {
    show("bad", escapeHtml(error.message));
  } finally {
    button.disabled = false;
  }
}

/* Assign & results */

function dueText(date) {
  return date ? new Date(`${date}T00:00:00`).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }) : "—";
}

function renderResults(rows, total) {
  const results = $("#results");
  if (rows.length === 0) {
    results.innerHTML = '<div class="empty"><strong>Not assigned yet.</strong><span>Pick groups on the left and press Assign.</span></div>';
    return;
  }
  const today = new Date().toISOString().slice(0, 10);
  results.innerHTML = rows
    .map((assignment) => `
      <section class="assignment-results">
        <div class="card-head">
          <h3>${escapeHtml(assignment.groupName)}</h3>
          <span>${assignment.deadline ? `Deadline ${escapeHtml(dueText(assignment.deadline))}` : "No deadline"}</span>
          <button class="button ghost small" type="button" data-unassign="${assignment.assignmentId}">Unassign group</button>
        </div>
        ${assignment.members.length ? `<table class="results-table">
          <thead><tr><th>Student</th><th>Status</th><th>Best</th><th>Submissions</th><th>Deadline</th></tr></thead>
          <tbody>${assignment.members.map((row) => {
            const status = STUDENT_STATUS[row.status];
            const overdue = assignment.deadline && assignment.deadline < today && row.status !== "solved";
            const last = row.lastActivity ? new Date(row.lastActivity).toLocaleString() : "No activity yet";
            return `
              <tr>
                <td>${escapeHtml(row.username)}<small>${escapeHtml(row.email)}</small></td>
                <td><span class="badge small ${status.badge}">${status.label}</span><small>${escapeHtml(last)}</small></td>
                <td>${row.bestPassed === null ? "—" : `${row.bestPassed} / ${total}`}</td>
                <td>${row.attempts}</td>
                <td class="${overdue ? "overdue" : ""}">${dueText(assignment.deadline)}${overdue ? "<small>Overdue</small>" : ""}</td>
              </tr>`;
          }).join("")}</tbody>
        </table>` : '<p class="field-hint">This group has no students.</p>'}
      </section>`)
    .join("");
}

function renderGroupChoices(groups, rows) {
  const assigned = new Set(rows.map((row) => row.groupId));
  $("#student-list").innerHTML = groups.length
    ? groups
        .map(
          (group) => `
            <label class="student-option">
              <input type="checkbox" name="groups" value="${group.id}">
              ${escapeHtml(group.name)}
              <small>${group.memberCount} ${group.memberCount === 1 ? "student" : "students"}${assigned.has(group.id) ? " · Assigned" : ""}</small>
            </label>`,
        )
        .join("")
    : '<p class="field-hint">No groups yet. Ask an administrator to create a group and maintain its membership.</p>';
}

async function renderTeachAssign(slug) {
  state.teach.assigning = slug;
  $("#assign-title").textContent = "Loading...";
  $("#assign-edit-link").href = `#/teach/${encodeURIComponent(slug)}/edit`;
  $("#assign-try-link").href = `#/practice/${encodeURIComponent(slug)}`;
  $("#assign-message").hidden = true;
  $("#assign-form").reset();
  $("#results").innerHTML = "";
  try {
    const base = `/api/teach/exercises/${encodeURIComponent(slug)}/`;
    const [{ exercise }, { assignments }, { groups }] = await Promise.all([
      teachFetch(base),
      teachFetch(`${base}assignments/`),
      teachFetch("/api/teach/groups/"),
    ]);
    if (state.teach.assigning !== slug) {
      return;
    }
    state.teach.total = exercise.tests.length;
    state.teach.groups = groups;
    $("#assign-title").textContent = exercise.title;
    document.title = `Debug GYM | ${exercise.title}`;
    renderGroupChoices(groups, assignments);
    renderResults(assignments, exercise.tests.length);
  } catch (error) {
    toast(error.status === 404 ? "That exercise was not found." : failureText(error));
    goTo("#/teach");
  }
}

function showAssignMessage(kind, text) {
  const message = $("#assign-message");
  message.hidden = false;
  message.className = `ask-result ${kind}`;
  message.textContent = text;
}

async function assignGroups(event) {
  event.preventDefault();
  const form = event.target;
  const ids = [...form.querySelectorAll('input[name="groups"]:checked')].map((input) => Number(input.value));
  if (ids.length === 0) {
    showAssignMessage("error", "Choose at least one group.");
    return;
  }
  const slug = state.teach.assigning;
  try {
    const { assignments } = await teachFetch(`/api/teach/exercises/${encodeURIComponent(slug)}/assignments/`, {
      method: "POST",
      body: JSON.stringify({ groups: ids, deadline: form.elements.deadline.value || null }),
    });
    renderGroupChoices(state.teach.groups, assignments);
    renderResults(assignments, state.teach.total);
    showAssignMessage("success", `Assigned to ${ids.length} ${ids.length === 1 ? "group" : "groups"}.`);
  } catch (error) {
    showAssignMessage("error", failureText(error));
  }
}

async function unassignGroup(assignmentId) {
  const slug = state.teach.assigning;
  try {
    const { assignments } = await teachFetch(
      `/api/teach/exercises/${encodeURIComponent(slug)}/assignments/${assignmentId}/`,
      { method: "DELETE" },
    );
    renderGroupChoices(state.teach.groups, assignments);
    renderResults(assignments, state.teach.total);
  } catch (error) {
    toast(failureText(error));
  }
}

/* My assignments (students) */

function assignmentFor(id) {
  return state.assignments.find((item) => item.bugId === id) || null;
}

function assignmentsFor(id) {
  return state.assignments.filter((item) => item.bugId === id);
}

function shortDate(date) {
  return new Date(`${date}T00:00:00`).toLocaleDateString(undefined, { day: "numeric", month: "short" });
}

// Open work first, then the earliest deadline; no deadline last.
function sortAssignments(items) {
  const rank = (item) => [item.status === "solved" ? 1 : 0, item.deadline || "9999-12-31", item.title];
  return [...items].sort((a, b) => {
    const [x, y] = [rank(a), rank(b)];
    return x[0] - y[0] || x[1].localeCompare(y[1]) || x[2].localeCompare(y[2]);
  });
}

async function loadAssignments() {
  if (isProfessor()) {
    return;
  }
  try {
    const { assignments } = await teachFetch("/api/assignments/");
    state.assignments = sortAssignments(assignments);
  } catch {
    return;
  }
  const open = state.assignments.filter((item) => item.status !== "solved").length;
  const count = $("#assignments-count");
  count.hidden = open === 0;
  count.textContent = open;
  if (!$("#view-assignments").hidden) {
    renderAssignments();
  } else if (!$("#view-new").hidden) {
    renderExerciseList();
  } else if (state.practiceId) {
    renderAssignedNote(state.practiceId);
  }
}

function renderAssignedNote(id) {
  const note = $("#practice-assigned");
  const assignments = assignmentsFor(id);
  const assignment = assignments[0];
  note.hidden = assignments.length === 0;
  if (!assignment) {
    return;
  }
  const parts = [`Assigned to ${assignments.map((item) => item.groupName).join(", ")}`];
  if (assignment.assignedBy) parts.push(`by ${assignment.assignedBy}`);
  if (assignment.deadline) {
    parts.push(`due ${dueText(assignment.deadline)}`);
  }
  note.textContent = parts.join(" · ");
  note.classList.toggle("overdue", assignment.overdue);
  if (assignment.overdue) {
    note.textContent += " · overdue";
  }
  if (assignments.length > 1) {
    note.textContent += " · earliest deadline shown";
  }
}

function renderAssignments() {
  document.title = "Debug GYM | My assignments";
  const list = $("#assignment-list");
  if (state.assignments.length === 0) {
    list.innerHTML = `
      <div class="empty">
        <strong>No assignments yet.</strong>
        <span>When a professor assigns you an exercise, it shows up here. Meanwhile, browse all exercises.</span>
      </div>`;
    return;
  }
  list.innerHTML = state.assignments
    .map((item) => {
      const status = STUDENT_STATUS[item.status];
      const due = item.deadline
        ? `<span class="${item.overdue ? "overdue" : ""}">Due ${escapeHtml(dueText(item.deadline))}${item.overdue ? " · overdue" : ""}</span>`
        : "<span>No deadline</span>";
      const score = item.bestPassed === null ? "" : `<span>Best ${item.bestPassed} / ${item.total}</span>`;
      const action = item.status === "solved" ? "Review" : item.status === "not-started" ? "Start" : "Continue";
      return `
        <article class="teach-row">
          <div>
            <h2>${escapeHtml(item.title)}</h2>
            <p>${escapeHtml(item.summary)}</p>
            <div class="badges">
              <span class="badge small ${status.badge}">${status.label}</span>
              <span class="badge small">${escapeHtml(item.difficulty)}</span>
              <span class="badge small">${escapeHtml(item.groupName)}</span>
            </div>
          </div>
          <div class="teach-stats">
            ${due}
            ${score}
            ${item.assignedBy ? `<span>From ${escapeHtml(item.assignedBy)}</span>` : ""}
          </div>
          <div class="row-actions">
            <a class="button ${item.status === "solved" ? "ghost" : "primary"} small" href="#/practice/${encodeURIComponent(item.bugId)}">${action}</a>
          </div>
        </article>`;
    })
    .join("");
}

/* Routing */

function route() {
  stopSubmissionSync();
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
    goTo(isProfessor() ? "#/teach" : "#/new");
    return;
  }
  if ((view === "teach" && !isProfessor()) || (view === "assignments" && isProfessor())) {
    goTo(isProfessor() ? "#/teach" : "#/new");
    return;
  }
  $("#auth").hidden = true;

  const practice = view === "practice";
  const action = location.hash.split("/")[3];
  let shown = practice ? "view-practice" : view === "assignments" ? "view-assignments" : "view-new";
  if (view === "teach") {
    shown = !id ? "view-teach" : id === "new" || action === "edit" ? "view-teach-edit" : "view-teach-assign";
  }
  document.querySelectorAll("main > .view").forEach((section) => {
    section.hidden = section.id !== shown;
  });
  for (const [link, current] of [["#nav-teach", view === "teach"], ["#nav-assignments", view === "assignments"]]) {
    if (current) {
      $(link).setAttribute("aria-current", "page");
    } else {
      $(link).removeAttribute("aria-current");
    }
  }
  setSidebar(false);
  setMenu(false);

  if (view === "teach") {
    state.practiceId = null;
    if (shown === "view-teach") {
      renderTeachList();
    } else if (shown === "view-teach-edit") {
      renderTeachEditor(id === "new" ? null : decodeURIComponent(id));
    } else {
      renderTeachAssign(decodeURIComponent(id));
    }
  } else if (view === "assignments") {
    state.practiceId = null;
    renderAssignments();
  } else if (practice) {
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
$("#exercise-form").addEventListener("submit", saveExercise);
$("#check-exercise").addEventListener("click", checkExercise);
$("#delete-exercise").addEventListener("click", deleteExercise);
$("#add-test").addEventListener("click", () => {
  const tests = [...readTests(), { ...EMPTY_TEST }];
  renderTestRows(tests);
  $(`[name="tests.${tests.length - 1}.name"]`).focus();
});
$("#test-rows").addEventListener("click", (event) => {
  const button = event.target.closest("[data-remove-test]");
  if (button) {
    const tests = readTests();
    tests.splice(Number(button.dataset.removeTest), 1);
    renderTestRows(tests);
  }
});
$("#assign-form").addEventListener("submit", assignGroups);
$("#results").addEventListener("click", (event) => {
  const button = event.target.closest("[data-unassign]");
  if (button) {
    unassignGroup(Number(button.dataset.unassign));
  }
});
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

$("#exercise-list").addEventListener("click", (event) => {
  if (event.target.closest('[data-action="clear-matches"]')) {
    clearMatches();
  }
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
window.addEventListener("focus", () => { void submissionSync?.refresh(); });
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) void submissionSync?.refresh();
});
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
