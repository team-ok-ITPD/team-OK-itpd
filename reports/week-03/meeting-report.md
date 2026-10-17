# Week 3 Customer Validation Meeting Report

## 1. Metadata

- **Date:** 2026-10-16
- **Duration:** Approximately 23 minutes
- **Attendees:** @adelazzi, @Danashi11, Customer
- **Presented:** Figma prototype of the New Challenge screen and Practice workspace.
- **Recording:** Permitted
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## 2. Previous Meeting Reports and Action Points

### 2.1 Meeting Report 1 — Week 1 Kickoff (2 October 2026)

**Reference:** [Week 1 kickoff meeting report](../week-01/meeting-report.md)

| Previous action point | Outcome during Week 3 validation |
|---|---|
| Define the initial Python bug categories and prepare at least one example for each category. | The prototype included the Arrays & loops topic and three prepared exercises. Completion of the full bug-category task was not confirmed. |
| Clarify the first-version priorities for scoring, leaderboard, attempt tracking, gallery, and categories. | The prototype displayed attempt history and a practice streak, but no leaderboard or gallery. The customer did not discuss feature priorities during this meeting. |
| Specify the permitted AI assistance levels: explanation, hints, or revealing the fix. | The prototype included optional hints and a hidden solution reveal. The customer did not confirm the final assistance policy. |
| Check the infrastructure assumption for one 16 GB VPS versus several configured servers. | The infrastructure question remained unresolved. The customer raised the question of where learner code should execute. |

### 2.2 Meeting Report 2 — Internal Project Planning (9 October 2026)

**Reference:** [Week 2 internal project planning report](../week-02/meeting-report.md)

| Previous action point | Outcome during Week 3 validation |
|---|---|
| Finalize the prototype flow based on the completed Figma design. | A Figma prototype was presented to the customer for validation. Feedback identified changes needed to the language selector, exercise preview, and test output. |
| Document the architecture and supporting reference examples. | Completion was not verified during the customer validation meeting. |
| Define workstreams, responsibilities, and dependencies. | Completion was not discussed during the customer validation meeting. |
| Prepare the client-facing architecture summary and recommendation. | Completion was not verified during the customer validation meeting. |

## 3. Meeting Summary

The purpose of the meeting was to validate the proposed debugging-practice product and gather feedback on the structure and usability of the Figma prototype.

The main findings were:

- **Language selection:** The programming-language selector was not immediately discoverable. It should be placed prominently in the central area of the challenge creation form.
- **Exercise preview:** Displaying source code and output in a small preview is unsuitable for large or multi-file exercises. The preview should show only the problem statement.
- **Real debugging:** The customer expects a real debugger with breakpoints and step-by-step execution. VS Code should be the primary environment for solving and submitting exercises.
- **Exercise generation:** Each exercise should contain a correct program, a buggy program, and pytest tests that pass on the correct program and reproduce the intended bug on the buggy program.
- **Test results:** The interface should display complete test output, including long output, rather than limiting results to a single row.
- **Technical implementation:** The team has not yet decided whether VS Code will be standalone, browser-based, or supported through a custom extension. The execution environment for learner code also remains undecided.

## 4. Decisions

The following decisions were recorded as outcomes of the customer validation meeting:

- [DEC-006: Generate each exercise as a correct program, a buggy program, and pytest tests](../../docs/decisions.md#dec-006)
- [DEC-007: Debug and submit in VS Code with a real debugger, not in a web editor](../../docs/decisions.md#dec-007)
- [DEC-008: Show only a problem statement in the exercise preview](../../docs/decisions.md#dec-008)
- [DEC-009: Put the language choice in the centre of the request form](../../docs/decisions.md#dec-009)
- [DEC-010: Show the full output of the tests, not one row](../../docs/decisions.md#dec-010)

## 5. Action Points

The following follow-up actions were proposed based on the meeting decisions. Owners and deadlines were not assigned in the transcript.

| Action | Owner | Due |
|---|---|---|
| Update the prototype to make language selection prominent, simplify the exercise preview, and display full test output. | — | — |
| Update user stories and acceptance criteria for exercise generation, verification, and debugging, referencing DEC-006 and DEC-007. | — | — |
| Investigate whether a VS Code extension can submit multi-file solutions and retrieve test results. | — | — |
| Evaluate where learner code should execute and present the available options to the customer. | — | — |

## 6. Open Questions

| Question | Impact | Follow-up |
|---|---|---|
| Should learner code run in a sandboxed server-side container or on the learner's own computer? | Infrastructure, execution safety, and cost per learner. | — |
| Will learners see and edit all tests, or only a selected subset? | Test-result presentation and exercise generation requirements. | — |
| Will VS Code be standalone, browser-based, or supported through a custom extension? | Exercise setup, submission workflow, and learner onboarding. | — |
| How can the team verify that a generated exercise contains the specific intended bug, beyond checking whether tests fail? | Exercise-generation validation and acceptance criteria. | — |

## 7. Disagreements and Resolutions

| Initial team approach | Customer feedback | Outcome |
|---|---|---|
| Use a web editor with a Run Tests button and paste solutions from VS Code when necessary. | The customer needs a real debugger, breakpoints, and support for multi-file exercises. | VS Code becomes the primary debugging and submission environment. The delivery mechanism remains open. |
| Generate JSON input/output files and compare results using a Python script. | The customer expects executable pytest tests and a way to verify the intended bug. | Each exercise should include a correct program, a buggy program, and pytest tests. |
| Display buggy code and its output in the exercise preview. | The customer explained that this approach does not scale to large or multi-file exercises. | The preview will contain only the problem statement. |
| Display test results in a single row and limit the number of tests to three. | The customer emphasized that test output can be very long and needs to be inspected in full. | The interface will show complete test output. The number and visibility of tests remain open questions. |

## 8. Conclusion

The Week 3 customer validation meeting clarified the product's direction and identified changes needed to the prototype and project requirements.

The meeting established five decisions concerning exercise generation, VS Code debugging and submission, exercise preview content, language selection, and test output.

These outcomes build on the initial product direction established during the Week 1 kickoff and the prototype preparation discussed during the Week 2 internal planning meeting. The next step is to update the relevant documentation and investigate the remaining technical questions before implementation decisions are finalized.
