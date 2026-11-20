// [Student Dev] Bug workspace editor: line numbers, Tab indent, reset, unsaved-changes guard

const INDENT = "    ";

function setupWorkspace(form) {
  const input = form.querySelector(".editor-input");
  const gutter = form.querySelector("[data-editor-gutter]");
  const state = form.querySelector("[data-editor-state]");
  const resetButton = form.querySelector("[data-reset-code]");
  const buggyCode = JSON.parse(document.getElementById("buggy-code").textContent);
  let saved = input.value;
  let submitting = false;

  function renderGutter() {
    const lines = input.value.split("\n").length;
    gutter.textContent = Array.from({ length: lines }, (_, i) => i + 1).join("\n");
    gutter.scrollTop = input.scrollTop;
  }

  function markChanged() {
    if (state) {
      state.textContent = input.value === saved ? "No unsaved changes." : "Unsaved changes.";
    }
  }

  input.addEventListener("input", () => {
    renderGutter();
    markChanged();
  });
  input.addEventListener("scroll", () => {
    gutter.scrollTop = input.scrollTop;
  });

  // Tab inserts spaces instead of leaving the editor; Shift+Tab removes one indent.
  // Escape then Tab still moves focus out, so keyboard users are not trapped.
  let escaped = false;
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      escaped = true;
      return;
    }
    if (event.key !== "Tab" || escaped || input.readOnly) {
      escaped = false;
      return;
    }
    event.preventDefault();
    const { selectionStart: start, selectionEnd: end, value } = input;
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;
    if (event.shiftKey) {
      if (value.startsWith(INDENT, lineStart)) {
        input.setRangeText("", lineStart, lineStart + INDENT.length, "preserve");
        input.setSelectionRange(Math.max(start - INDENT.length, lineStart), Math.max(end - INDENT.length, lineStart));
      }
    } else {
      input.setRangeText(INDENT, start, end, "end");
    }
    input.dispatchEvent(new Event("input"));
  });

  if (resetButton) {
    resetButton.addEventListener("click", () => {
      if (input.value !== buggyCode && !window.confirm("Replace your code with the original buggy code?")) {
        return;
      }
      input.value = buggyCode;
      input.dispatchEvent(new Event("input"));
      input.focus();
    });
  }

  form.addEventListener("submit", () => {
    submitting = true;
  });
  window.addEventListener("beforeunload", (event) => {
    if (!submitting && input.value !== saved) {
      event.preventDefault();
    }
  });

  renderGutter();
  // A page re-shown with a validation error holds the typed code, which is not saved yet.
  if (input.getAttribute("aria-invalid") === "true") {
    saved = null;
  }
}

document.querySelectorAll("[data-workspace]").forEach(setupWorkspace);
