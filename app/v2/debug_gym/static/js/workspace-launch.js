// [Shared] Open connected VS Code sessions and refresh own verified results
document.querySelectorAll("[data-launch-workspace]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector("button");
    const error = form.querySelector("[data-workspace-error]");
    const popup = window.open("about:blank", "_blank");
    if (popup) popup.document.body.textContent = "Starting your Debug GYM workspace…";
    button.disabled = true;
    error.hidden = true;
    try {
      const response = await fetch(form.action, { method: "POST", body: new FormData(form) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "The workspace could not be opened.");
      if (popup) popup.location.href = payload.url;
      else window.location.href = payload.url;
    } catch (failure) {
      if (popup) popup.close();
      error.textContent = failure.message;
      error.hidden = false;
    } finally {
      button.disabled = false;
    }
  });
});

const progress = document.querySelector("[data-progress-url]");
if (progress) {
  let busy = false;
  async function refresh() {
    if (busy || document.hidden) return;
    busy = true;
    try {
      const response = await fetch(progress.dataset.progressUrl, { cache: "no-store" });
      if (!response.ok) return;
      const result = await response.json();
      progress.textContent = result.total === null
        ? "No verified submission yet."
        : result.passed + " / " + result.total + " tests passed · " + result.submitted;
    } catch {
      // A temporary connection failure is retried on the next poll.
    } finally {
      busy = false;
    }
  }
  window.setInterval(refresh, 3000);
  document.addEventListener("visibilitychange", refresh);
  refresh();
}
