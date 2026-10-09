# Internal Project Planning Report

**Status:** Draft — Week 2 internal discussion, documenting the project direction and prototype preparation before the next client review.

## 1. Meeting Details

- **Date:** 09.10.2026
- **Location:** Internal team meeting / workspace discussion
- **Recording:** Not recorded
- **Board:** Not used

## 2. Attendance and Roles

- **Attendees:** @adelazzi, @UTKANOS-RIBA, @Danashi11, @qwxiae
- **Facilitator:** @adelazzi
- **Note-taker:** @qwxiae
- **Timekeeper:** @Danashi11

## 3. Discussion Summary

- **Project split:** The team discussed dividing the project into workstreams covering frontend and UX, backend orchestration, environment provisioning, exercise generation, validation, and AI assistance.
- **Figma design:** The team completed the Figma design for the proposed user flow and interface, establishing the visual direction for the prototype.
- **ChatGPT-style UX:** The team discussed the client's acceptance of the prompt-first interaction model, where users describe their learning goal and proceed directly to a debugging exercise.
- **Prototype scope:** The first prototype will focus on Python and browser-based coding and debugging, allowing users to inspect code, investigate bugs, and test fixes directly in the web application.
- **Future integration:** VS Code support through SSH may be added in a later phase after the core web-based experience is functional.
- **Architecture:** The team agreed to prioritize a modular architecture and validate the complete user journey before adding optional features.

## 4. Decisions

- **Confirmed:** The project will be divided into workstreams with clear responsibilities.
- **Completed:** The initial Figma design has been finished.
- **Agreed direction:** The prototype will use a ChatGPT-style, prompt-first workflow.
- **Agreed scope:** Python will be the first supported language, with coding and debugging performed in the browser.
- **Future enhancement:** VS Code integration through SSH will be considered after the initial prototype.
- **Next step:** Present the prototype direction and architecture to the client for validation.

## 5. Action Points

| Action | Owner | Due |
|---|---|---|
| Finalize the prototype flow based on the completed Figma design. | @adelazzi | Week 3: 2026-10-16 |
| Document the architecture and supporting reference examples. | @UTKANOS-RIBA | Week 3: 2026-10-16 |
| Define workstreams, responsibilities, and dependencies. | @Danashi11 | Week 3: 2026-10-16 |
| Prepare the client-facing architecture summary and recommendation. | @qwxiae | Week 3: 2026-10-16 |

## 6. Disagreements

No major disagreements were reported. The team aligned on simplifying the user experience, starting with a browser-based Python debugging prototype, and validating the architecture with the client before proceeding with deeper implementation.