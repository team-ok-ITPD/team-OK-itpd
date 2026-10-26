# Week 4 customer meeting report

## Metadata

- **Date:** 2026-10-26
- **Duration:** Approximately 36 minutes
- **Attendees:** @adelazzi, Customer
- **Presented:** The web prototype of the learner flow: login, the challenge request form with language, difficulty and topic, the code and test workspace, the prepared exercise list, and a worked example of fixing a failing test.
- **Recording:** Permitted
- **Transcript publication:** Permitted, see [the transcript](meeting-transcript.md)
- **Private sharing with instructors:** Not needed, because publication was permitted
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [reports/week-03/meeting-report.md#5-action-points](../week-03/meeting-report.md#5-action-points): "Update the prototype to make language selection prominent, simplify the exercise preview, and display full test output." | Partly carried out. The prototype shown in this meeting moves the language choice into the request form, next to difficulty and topic. The customer still found the exercise preview and the search box confusing, and full test output was not shown, so the rest reappears in the action points below. | None |
| [reports/week-03/meeting-report.md#5-action-points](../week-03/meeting-report.md#5-action-points): "Update user stories and acceptance criteria for exercise generation, verification, and debugging, referencing DEC-006 and DEC-007." | Carried out. The functional requirements cite both decisions: [FR-003](../../docs/functional-requirements/fr/FR-003.md), [FR-004](../../docs/functional-requirements/fr/FR-004.md) and [FR-005](../../docs/functional-requirements/fr/FR-005.md), written in [task #74](https://github.com/team-ok-ITPD/team-OK-itpd/issues/74). | None |
| [reports/week-03/meeting-report.md#5-action-points](../week-03/meeting-report.md#5-action-points): "Investigate whether a VS Code extension can submit multi-file solutions and retrieve test results." | Partly carried out. The team packaged VS Code in the browser with the exercise and a debugger configuration, see [ADR-001](../../docs/architecture/adr/ADR-001.md) and [the MUP verification](../week-03/mup-verification.md). Submitting multi-file solutions and retrieving test results was not investigated, and it reappears below. | [DEC-014](../../docs/decisions.md#dec-014) |
| [reports/week-03/meeting-report.md#5-action-points](../week-03/meeting-report.md#5-action-points): "Evaluate where learner code should execute and present the available options to the customer." | Partly carried out. [ADR-003](../../docs/architecture/adr/ADR-003.md) keeps the prototype on the learner's own computer for now. The options for a shared server were not presented, and it reappears below. | None |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [reports/week-03/meeting-report.md#6-open-questions](../week-03/meeting-report.md#6-open-questions): "Should learner code run in a sandboxed server-side container or on the learner's own computer?" | Not answered. The meeting did not reach it. It reappears in the open questions below. | None |
| [reports/week-03/meeting-report.md#6-open-questions](../week-03/meeting-report.md#6-open-questions): "Will learners see and edit all tests, or only a selected subset?" | Answered in part. The customer said the default tests are the source of truth and must not be editable, while learners may add tests of their own. Whether every default test is visible was not asked, and it reappears below. | [DEC-011](../../docs/decisions.md#dec-011) |
| [reports/week-03/meeting-report.md#6-open-questions](../week-03/meeting-report.md#6-open-questions): "Will VS Code be standalone, browser-based, or supported through a custom extension?" | Answered in part. The customer accepted desktop VS Code or VS Code in the browser, either connected over SSH to a server that holds the exercise and tests, and required submission from VS Code. Which of the two the team ships is not chosen, and it reappears below. | [DEC-013](../../docs/decisions.md#dec-013), [DEC-014](../../docs/decisions.md#dec-014) |
| [reports/week-03/meeting-report.md#6-open-questions](../week-03/meeting-report.md#6-open-questions): "How can the team verify that a generated exercise contains the specific intended bug, beyond checking whether tests fail?" | Not asked in this meeting. [ADR-002](../../docs/architecture/adr/ADR-002.md) validates exercises with a buggy program and an oracle, but the customer has not seen it, and it reappears below. | None |

## Summary

- The default tests stay read-only as the source of truth, and learners add tests of their own beside them.
- The product is for desktop users, so mobile support is dropped, and opening an exercise in VS Code becomes a Must Have instead of a delighter.
- Learners submit from VS Code and not from a button on the site, and the customer accepts either desktop VS Code or VS Code in the browser connected over SSH.
- Search covers only prepared exercises, sits just above the exercise list, and shows every match, with the first match selected and nothing shown when there are none.
- The customer expects the next meeting to show one complete scenario, preferably two: log in, choose an exercise, open it in VS Code, solve it and submit.

## Decisions

- [DEC-011: Keep the default tests read-only and let learners add tests of their own.](../../docs/decisions.md#dec-011)
- [DEC-012: Design for desktop users and do not build for mobile.](../../docs/decisions.md#dec-012)
- [DEC-013: Make opening an exercise in VS Code a Must Have.](../../docs/decisions.md#dec-013)
- [DEC-014: Submit the solution from VS Code, not from a button on the site.](../../docs/decisions.md#dec-014)
- [DEC-015: Search only the prepared exercises and list every match below the filters.](../../docs/decisions.md#dec-015)

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Try both routes to VS Code, desktop VS Code over SSH and VS Code in the browser embedded in the site, and report which one can submit a multi-file solution and return the test results. | qwxiae | 2026-10-29 (Week 5) |
| Build one complete scenario, preferably two exercises: log in, choose an exercise, open it in VS Code, solve it and submit from VS Code. | adelazzi | 2026-10-30 (Week 5) |
| Keep the default tests read-only and add a separate set that learners can edit, per DEC-011. | UTKANOS-RIBA | 2026-10-30 (Week 5) |
| Rework the search: prepared exercises only, the input just above the list, every match listed, the first match selected, and no preview when there are no results, per DEC-015. | Danashi11 | 2026-10-29 (Week 5) |
| Update the stories for DEC-012 and DEC-013, and cite the decisions in each story's change comment. | Danashi11 | 2026-10-29 (Week 5) |
| Present the options for where learner code runs, with their cost per learner, to the customer. | qwxiae | 2026-10-30 (Week 5) |
| Show the containerized workspace against the acceptance criteria of US-01 to US-05 and ask for a verdict on each. | adelazzi | 2026-10-30 (Week 5) |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Should learner code run in a sandboxed server-side container or on the learner's own computer? | Infrastructure, safety and the cost per learner, see [QR-02](../../docs/quality-requirements/qr/QR-02.md) and ADR-003. | Present the options at the next meeting. |
| Should learners see every default test? | What the test output shows and how exercises are generated. | Ask at the next meeting. |
| Does the customer accept US-01 to US-05 against their acceptance criteria? | Whether the stories close, and what the next sprint contains. | Show the containerized workspace at the next meeting. |
| How can the team verify that an exercise contains the specific intended bug? | The exercise checks in [QR-01](../../docs/quality-requirements/qr/QR-01.md) and ADR-002. | Show the customer the buggy program and oracle approach. |
| Will the team ship desktop VS Code over SSH or VS Code in the browser embedded in the site? | Setup effort, onboarding and the design of US-05. | The experiment in the first action point. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| Learners may edit every test, as on LeetCode. | The default tests are the source of truth and must stay read-only, though learners may add tests. | The default tests become read-only and learners add their own, per DEC-011. |
| Mobile use belongs in the documents as a delighter, with a button to open the online IDE for light users. | The product serves desktop users, so mobile is not worth the time and opening an exercise in VS Code is a Must Have. | Mobile is dropped and VS Code becomes a Must Have, per DEC-012 and DEC-013. |
| The in-page editor already gives the learner the functions of VS Code. | It does not: it lacks go to definition, debugging, a language server and linting, and VS Code should be part of the product. | We kept our position that both routes need testing, and the first action point compares them. |
| Search finds one exercise and shows it in a preview, even for AI-generated exercises. | Search must offer several matches and apply only to prepared exercises, and the preview should appear only after a selection. | Search is reworked per DEC-015. |
