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
