// [Shared] Main JavaScript for shared site behavior

// Show / hide password: <button data-toggle-password="<input id>">Show</button>
document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-toggle-password]");
  if (!button) {
    return;
  }
  const input = document.getElementById(button.dataset.togglePassword);
  const showing = input.type === "text";
  input.type = showing ? "password" : "text";
  button.textContent = showing ? "Show" : "Hide";
  button.setAttribute("aria-pressed", String(!showing));
  input.focus();
});

// Selection persists within this tab/account across filters and pagination.
// Clearing an applied student search immediately restores unsearched results.
const studentSearchForm = document.querySelector(".admin-toolbar-filters");
if (studentSearchForm) {
  const search = studentSearchForm.elements.q;
  const appliedQuery = new URL(window.location.href).searchParams.get("q") || "";
  let resettingSearch = false;
  const resetSearch = () => {
    if (!resettingSearch && appliedQuery && !search.value.trim()) {
      resettingSearch = true;
      studentSearchForm.requestSubmit();
    }
  };
  search.addEventListener("input", resetSearch);
  search.addEventListener("search", resetSearch);
}

const selectionForm = document.getElementById("student-batch");
if (selectionForm) {
  const key = selectionForm.dataset.selectionKey;
  const selected = new Set();
  const boxes = [...document.querySelectorAll('input[name="students"][form="student-batch"]')];
  const selectPage = document.querySelector("[data-select-students]");
  const clear = document.querySelector("[data-clear-student-selection]");
  let storageAvailable = true;
  const restore = () => {
    try {
      const saved = JSON.parse(sessionStorage.getItem(key) || "[]");
      selected.clear();
      if (Array.isArray(saved)) saved.forEach((id) => {
        if (typeof id === "string" && /^\d+$/.test(id)) selected.add(id);
      });
    } catch {
      storageAvailable = false;
    }
  };
  const sync = () => {
    boxes.forEach((box) => { box.checked = selected.has(box.value); });
    const onPage = boxes.filter((box) => box.checked).length;
    if (selectPage) {
      selectPage.checked = boxes.length > 0 && onPage === boxes.length;
      selectPage.indeterminate = onPage > 0 && onPage < boxes.length;
    }
    // Hidden fields carry only off-page selections; visible checkboxes submit themselves.
    selectionForm.querySelectorAll("[data-persisted-student]").forEach((input) => input.remove());
    const visible = new Set(boxes.map((box) => box.value));
    selected.forEach((id) => {
      if (visible.has(id)) return;
      const input = document.createElement("input");
      input.type = "hidden";
      input.name = "students";
      input.value = id;
      input.dataset.persistedStudent = "";
      selectionForm.append(input);
    });
    document.querySelector("[data-selection-summary]").textContent =
      `${selected.size} selected` +
      (storageAvailable ? "" : " · Browser storage unavailable; selection cannot persist across pages.");
    clear.disabled = selected.size === 0;
    selectionForm.dataset.selectionCount = String(selected.size);
    try {
      sessionStorage.setItem(key, JSON.stringify([...selected]));
    } catch {
      storageAvailable = false;
    }
  };
  restore();
  if (selectionForm.dataset.resetSelection === "true") selected.clear();
  sync();
  boxes.forEach((box) => box.addEventListener("change", () => {
    if (box.checked) selected.add(box.value);
    else selected.delete(box.value);
    sync();
  }));
  selectPage?.addEventListener("change", () => {
    boxes.forEach((box) => {
      if (selectPage.checked) selected.add(box.value);
      else selected.delete(box.value);
    });
    sync();
  });
  clear.addEventListener("click", () => { selected.clear(); sync(); });
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) { restore(); sync(); }
  });
}

// Native selects are the no-JavaScript fallback; search lives inside the popup.
document.querySelectorAll("select[data-searchable-select]").forEach((select, index) => {
  const label = select.labels[0];
  const labelText = label
    ? Array.from(label.childNodes).filter((node) => node.nodeType === Node.TEXT_NODE)
      .map((node) => node.textContent.trim()).join(" ").trim()
    : select.dataset.searchableSelect;
  const id = select.id || `searchable-select-${index}`;
  const required = select.required;
  const wrapper = document.createElement("div");
  wrapper.className = "searchable-select";
  const trigger = document.createElement("button");
  trigger.type = "button";
  trigger.className = "searchable-select-trigger";
  trigger.setAttribute("aria-haspopup", "dialog");
  trigger.setAttribute("aria-expanded", "false");
  trigger.setAttribute("aria-controls", `${id}-popup`);
  const value = document.createElement("span");
  value.className = "searchable-select-value";
  trigger.append(value);
  const popup = document.createElement("div");
  popup.id = `${id}-popup`;
  popup.className = "searchable-select-popup";
  popup.hidden = true;
  popup.setAttribute("role", "dialog");
  popup.setAttribute("aria-label", select.dataset.searchableSelect);
  const search = document.createElement("input");
  search.type = "search";
  search.autocomplete = "off";
  search.placeholder = select.dataset.searchableSelect;
  search.setAttribute("aria-label", select.dataset.searchableSelect);
  search.setAttribute("role", "combobox");
  search.setAttribute("aria-autocomplete", "list");
  search.setAttribute("aria-controls", `${id}-options`);
  search.setAttribute("aria-expanded", "false");
  const list = document.createElement("div");
  list.id = `${id}-options`;
  list.className = "searchable-select-options";
  list.setAttribute("role", "listbox");
  list.setAttribute("aria-label", labelText);
  const empty = document.createElement("p");
  empty.className = "searchable-select-empty";
  empty.textContent = "No matches";
  empty.setAttribute("role", "status");
  const error = document.createElement("span");
  error.className = "field-error";
  error.textContent = "Choose an option.";
  error.hidden = true;
  popup.append(search, list, empty);
  wrapper.append(trigger, popup, error);
  select.after(wrapper);
  select.hidden = true;
  // Validate through the visible control instead of an unfocusable hidden select.
  select.required = false;

  const sync = () => {
    value.textContent = select.selectedOptions[0]?.label ||
      (select.dataset.emptyPlaceholder ?? "Choose an option");
    trigger.setAttribute("aria-label", `${labelText}: ${value.textContent}`);
    trigger.disabled = select.disabled;
  };
  const close = (restoreFocus = false) => {
    popup.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
    search.setAttribute("aria-expanded", "false");
    if (restoreFocus) trigger.focus();
  };
  const render = () => {
    const query = search.value.trim().toLocaleLowerCase();
    list.replaceChildren();
    Array.from(select.options).forEach((option, optionIndex) => {
      if (!option.value && select.hasAttribute("data-empty-placeholder")) return;
      if (option.hidden || (query && !option.label.toLocaleLowerCase().includes(query))) return;
      const item = document.createElement("button");
      item.type = "button";
      item.className = "searchable-select-option";
      item.id = `${id}-option-${optionIndex}`;
      item.textContent = option.label;
      item.disabled = option.disabled;
      item.tabIndex = -1;
      item.setAttribute("role", "option");
      item.setAttribute("aria-selected", String(option.selected));
      item.addEventListener("click", (event) => {
        event.preventDefault();
        select.value = option.value;
        error.hidden = true;
        trigger.removeAttribute("aria-invalid");
        select.dispatchEvent(new Event("change", { bubbles: true }));
        close(true);
      });
      list.append(item);
    });
    empty.hidden = list.children.length !== 0;
  };
  const open = () => {
    if (select.disabled) return;
    search.value = "";
    render();
    popup.hidden = false;
    trigger.setAttribute("aria-expanded", "true");
    search.setAttribute("aria-expanded", "true");
    search.focus();
  };
  const options = () => Array.from(list.querySelectorAll("button:not(:disabled)"));
  trigger.addEventListener("click", (event) => {
    event.preventDefault();
    if (popup.hidden) open();
    else close();
  });
  trigger.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      open();
    }
  });
  search.addEventListener("input", render);
  search.addEventListener("keydown", (event) => {
    const items = options();
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      (event.key === "ArrowDown" ? items[0] : items.at(-1))?.focus();
    } else if (event.key === "Enter") {
      event.preventDefault();
      const selected = items.find((item) => item.getAttribute("aria-selected") === "true");
      (selected || items[0])?.click();
    }
  });
  list.addEventListener("keydown", (event) => {
    const items = options();
    const current = items.indexOf(document.activeElement);
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      items[(current + (event.key === "ArrowDown" ? 1 : items.length - 1)) % items.length]?.focus();
    } else if (event.key === "Home" || event.key === "End") {
      event.preventDefault();
      (event.key === "Home" ? items[0] : items.at(-1))?.focus();
    }
  });
  wrapper.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      close(true);
    }
  });
  document.addEventListener("click", (event) => {
    if (!wrapper.contains(event.target)) close();
  });
  document.addEventListener("focusin", (event) => {
    if (!wrapper.contains(event.target)) close();
  });
  select.addEventListener("change", () => {
    sync();
    if (!popup.hidden) render();
  });
  select.form?.addEventListener("submit", (event) => {
    if (required && !select.disabled && !select.value) {
      event.preventDefault();
      error.hidden = false;
      trigger.setAttribute("aria-invalid", "true");
      open();
    }
  });
  select.form?.addEventListener("reset", () => queueMicrotask(() => {
    sync();
    close();
    error.hidden = true;
  }));
  sync();
});

// The original group-name link remains available without JavaScript.
const followGroupRow = (event) => {
  const row = event.target.closest("tr[data-row-link]");
  if (!row || event.target.closest("a, button, input, select, textarea, label")) return;
  if (window.getSelection()?.toString()) return;
  if (event.button === 1 || event.ctrlKey || event.metaKey || event.shiftKey) {
    event.preventDefault();
    window.open(row.dataset.rowLink, "_blank", "noopener");
  } else if (event.button === 0) {
    window.location.assign(row.dataset.rowLink);
  }
};
document.addEventListener("click", followGroupRow);
document.addEventListener("auxclick", (event) => {
  if (event.button === 1) followGroupRow(event);
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && event.target.matches("tr[data-row-link]")) {
    event.preventDefault();
    window.location.assign(event.target.dataset.rowLink);
  }
});

// Account activation is independent of group membership.
const studentBatchForm = document.getElementById("student-batch");
if (studentBatchForm) {
  const action = studentBatchForm.elements.action;
  const group = studentBatchForm.elements.group;
  const groupField = studentBatchForm.querySelector("[data-batch-group]");
  const syncGroupVisibility = () => {
    const needsGroup = ["add", "remove"].includes(action.value);
    groupField.hidden = !needsGroup;
    group.disabled = !needsGroup;
    group.dispatchEvent(new Event("change", { bubbles: true }));
    studentBatchForm.closest(".admin-student-toolbar").classList.toggle("status-action", !needsGroup);
  };
  action.addEventListener("change", syncGroupVisibility);
  syncGroupVisibility();
}

// Keep confirmations within the application, with native dialog focus handling.
const confirmationDialog = document.getElementById("action-confirmation");
let pendingConfirmation = null;
confirmationDialog?.addEventListener("close", () => {
  const pending = pendingConfirmation;
  pendingConfirmation = null;
  if (confirmationDialog.returnValue === "confirm" && pending) {
    pending.form.dataset.confirmed = "true";
    if (pending.submitter) pending.form.requestSubmit(pending.submitter);
    else pending.form.requestSubmit();
    delete pending.form.dataset.confirmed;
  }
});
document.addEventListener("submit", (event) => {
  const form = event.target;
  if (form.dataset.confirmed || form.closest("#action-confirmation")) return;
  const activeField = form.querySelector('[name="is_active"]');
  const message = form.dataset.confirm ||
    (activeField && !activeField.checked ? form.dataset.deactivateConfirm : "");
  if (!message || !confirmationDialog) return;
  event.preventDefault();
  if (pendingConfirmation) return;
  pendingConfirmation = { form, submitter: event.submitter };
  confirmationDialog.querySelector("#action-confirmation-description").textContent =
    form.id === "student-batch"
      ? `Apply "${form.elements.action.selectedOptions[0].textContent}" to all ${form.dataset.selectionCount} selected students, including those outside this page?`
      : message;
  confirmationDialog.returnValue = "";
  confirmationDialog.showModal();
});
