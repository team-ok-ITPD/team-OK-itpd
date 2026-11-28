// [Student Dev] Refresh only the workspace result fields after a VS Code submission.
(() => {
  const status = document.querySelector("[data-progress-url]");
  if (!status) return;

  const statusLabel = document.querySelector("[data-submission-status]");
  const testCount = document.querySelector("[data-test-count]");
  const submittedAt = document.querySelector("[data-submitted-at]");
  const latestCard = document.querySelector("[data-latest-submission]");
  const latestAt = document.querySelector("[data-latest-submitted-at]");
  const latestCode = document.querySelector("[data-latest-submitted-code]");
  const hasTests = status.dataset.hasTests === "true";
  let lastSubmissionId = null;
  let requestPending = false;

  function formatDate(value) {
    if (!value) return "Never";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? "Just now" : date.toLocaleString();
  }

  async function refresh() {
    if (requestPending || document.hidden) return;
    requestPending = true;
    try {
      const response = await fetch(status.dataset.progressUrl, {
        cache: "no-store",
        headers: { Accept: "application/json" },
      });
      if (!response.ok) return;
      const result = await response.json();

      if (!result.id) {
        status.textContent = "No submission yet. Submit your solution in VS Code to see the result here.";
        return;
      }

      if (result.id === lastSubmissionId) return;
      lastSubmissionId = result.id;

      if (statusLabel) {
        statusLabel.textContent = result.status || "Submitted";
        statusLabel.classList.toggle("success", result.status === "Graded");
        statusLabel.classList.toggle("warning", result.status !== "Graded");
      }
      if (testCount) {
        testCount.textContent = result.total === null
          ? (hasTests ? "Not recorded for this attempt" : "No automated tests for this exercise")
          : `${result.passed} / ${result.total}`;
      }
      if (submittedAt) submittedAt.textContent = formatDate(result.submitted);
      if (latestAt) latestAt.textContent = formatDate(result.submitted);
      if (latestCode) latestCode.textContent = result.submitted_code || "";
      if (latestCard) latestCard.hidden = false;

      status.classList.toggle("success", result.total !== null && result.passed === result.total);
      status.classList.toggle("warning", result.total !== null && result.passed !== result.total);
      status.textContent = result.total === null
        ? "Your submission was saved. No automated test result is available for this exercise."
        : `${result.passed} / ${result.total} tests passed. Your latest submission is now shown below.`;
    } catch {
      // A temporary connection failure is harmless; the next poll retries.
    } finally {
      requestPending = false;
    }
  }

  refresh();
  window.setInterval(refresh, 3000);
  document.addEventListener("visibilitychange", refresh);
})();
