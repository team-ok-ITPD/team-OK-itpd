# Meeting Notes

**Meeting:** Week 2 Internal Team Discussion — Project Scope and Prototype Architecture

**Date:** 09.10.2026

**Attendees:** @adelazzi, @UTKANOS-RIBA, @Danashi11, @qwxiae

## Notes

The team discussed the project structure, client feedback, and the scope of the first prototype. The discussion focused on the proposed ChatGPT-style interface, where users describe what they want to practice and are directed to a ready-to-use debugging environment with minimal steps.

The team discussed the client's acceptance of this interaction style and reviewed the design direction using the existing mockups and [Figma prototype](https://www.figma.com/design/29kS3KyEPkdidEwrBsmNwO/ITPD?node-id=1-2&t=3J8dqgqCYNouOkZA-1).

For the first prototype, the team agreed to focus on **Python as the initial programming language** and **web-based coding and debugging**. Users should be able to access prepared code, investigate bugs, and test their fixes directly in the browser. VS Code integration through SSH may be added later, once the core web experience is functional.

The team also discussed separating responsibilities across frontend and UX, backend orchestration, environment provisioning, task generation, validation, and AI assistance. The priority is to validate the complete user journey before implementing optional features.

## Decided

- Use a ChatGPT-style, prompt-first interface, subject to client confirmation.
- Start with Python as the first supported language.
- Focus on browser-based coding and debugging for the initial prototype.
- Keep the workflow simple, with minimal steps between the prompt and the coding environment.
- Consider VS Code integration through SSH as a future enhancement.
- Prioritize the core debugging workflow before adding optional features.

## Left Open

- The final level of AI assistance during exercises.
- The technical implementation of Python environment provisioning and task validation.
- The scope and timing of VS Code integration.
- Future features such as scoring, leaderboards, and attempt tracking.

## Next Steps

- Finalize the prototype's user flow and architecture.
- Divide implementation tasks among team members.
- Present the proposed direction to the client for validation.