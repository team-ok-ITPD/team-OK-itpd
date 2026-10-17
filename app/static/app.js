const form = document.querySelector("#request-form");
const result = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.hidden = false;
  result.className = "result";
  result.textContent = "Matching your request...";

  try {
    const response = await fetch("/api/exercises", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: new FormData(form).get("query") }),
    });
    const payload = await response.json();

    if (!response.ok) {
      result.classList.add("error");
      result.textContent = payload.error;
      return;
    }

    const exercise = payload.exercise;
    result.innerHTML = `
      <span class="eyebrow">Prepared exercise</span>
      <h2>${exercise.title}</h2>
      <p>${exercise.description}</p>
      <div class="meta">
        <span class="tag">${exercise.difficulty}</span>
        <span class="tag">${exercise.language}</span>
        <span class="tag">${exercise.duration}</span>
        <span class="tag">${exercise.topic}</span>
      </div>
      <a class="start" href="${exercise.workspaceUrl}" target="_blank" rel="noopener">
        Open prepared workspace
      </a>
    `;
  } catch (error) {
    result.classList.add("error");
    result.textContent = `The catalog could not be reached: ${error.message}`;
  }
});
