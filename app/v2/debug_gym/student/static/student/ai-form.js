// [Student Dev] AI bug form: show that generation is running and block double submits

document.querySelectorAll("[data-ai-form]").forEach((form) => {
  form.addEventListener("submit", () => {
    const button = form.querySelector("[data-busy-label]");
    if (!button) {
      return;
    }
    // Disable after the browser has collected the form, so the request still goes out.
    setTimeout(() => {
      button.disabled = true;
      button.textContent = button.dataset.busyLabel;
      button.setAttribute("aria-busy", "true");
    });
  });
});
