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

// Destructive membership changes need an explicit user acknowledgement.
document.addEventListener("submit", (event) => {
  const form = event.target.closest("form[data-confirm]");
  if (form && !window.confirm(form.dataset.confirm)) {
    event.preventDefault();
  }

  const activeField = event.target.querySelector('[name="is_active"]');
  if (
    event.target.dataset.deactivateConfirm &&
    activeField &&
    !activeField.checked &&
    !window.confirm(event.target.dataset.deactivateConfirm)
  ) {
    event.preventDefault();
  }
});
