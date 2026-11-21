# Week 8 customer meeting report

## Metadata

- **Date:** 2026-11-20
- **Attended:** @adelazzi, @Danashi11, @qwxiae, @UTKANOS-RIBA, Customer
- **Presented:** Group and assignment workflows; teacher assignment and results views; exercise creation and catalogue; student assignment and history pages; VS Code extension workflow; submission and test behavior; CSV export; AI-assisted exercise generation and submission review
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#action-points): "Update the role, group-assignment and teacher-results stories and requirements to reflect DEC-039 and DEC-040; add the corresponding traceability links." | Not confirmed as carried out. The meeting revisited group assignment, teacher results and student assignment views, and the Customer clarified that course management stays external and that the course name must be visible in the group context. The requirements still need the update, now for [DEC-044](../../docs/decisions.md#dec-044), [DEC-045](../../docs/decisions.md#dec-045) and [DEC-046](../../docs/decisions.md#dec-046) as well; it reappears in the action points below. | [DEC-044](../../docs/decisions.md#dec-044), [DEC-045](../../docs/decisions.md#dec-045) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#action-points): "Specify the post-deadline suspicious-submission review scenario, including initiation, flagged-result review and false-positive handling, without assuming an unapproved provider or cost model." | Not settled. AI-assisted review and API configuration were revisited, and the Customer discussed provider-specific endpoints and offered a token. The provider, credential handling, failure behavior and final review process were not agreed; the provider and failure-behavior confirmation reappears in the action points below. | None |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#action-points): "Propose the teacher-facing configuration for tools in the student container and identify the container changes it requires." | Partly carried out. For a single task container the Customer preferred a Dockerfile rather than Docker Compose. The complete teacher-facing tool-configuration mechanism remains open and reappears in the action points below. | [DEC-051](../../docs/decisions.md#dec-051) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#action-points): "Define a first CSV export schema for assignment results and check its suitability for the intended grading workflow." | Partly carried out. The Customer agreed that the export includes the grade, which the application does not calculate. The exact schema and downstream workflow remain to be specified; this action is due in Week 9 and reappears below as a sample export. | [DEC-049](../../docs/decisions.md#dec-049) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#action-points): "Team action added after the meeting: present the `UT-01` design (record, surveys, tasks, instrumentation, consent, private repository, recordings folder, session plan and `QR-07`) to the Customer, check that its main task still matches the core workflow of `DEC-040`, and agree the session plan and the results date." | Not established. The meeting covered the product workflows rather than the `UT-01` design, so no session plan or results date was agreed with the Customer. The team shows the `UT-01` results and the product response at the next review instead; this reappears in the action points below. | None |
| [`reports/week-06/meeting-report.md`](../week-06/meeting-report.md#action-points): "Define and test the fresh submission-container lifecycle, concurrency limit, bounded queue and waiting response." | Not addressed at this meeting, and not re-listed by the Week 7 report. Carried forward through the container-limit question and the task-container action below. | None |
| [`reports/week-06/meeting-report.md`](../week-06/meeting-report.md#action-points): "Propose an MVP total upload-size limit and permitted supplementary file types, with evidence for the chosen values." | Not addressed at this meeting, and not re-listed by the Week 7 report. Carried forward in the project ZIP validation action below. | None |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "What exact fields and drill-downs should the professor see in the group-results view?" | The teacher workflow was discussed, including closing an assignment to open its results, and the CSV export includes the grade. The complete results-table fields and drill-down behavior were not specified; the question reappears below. | [DEC-047](../../docs/decisions.md#dec-047), [DEC-049](../../docs/decisions.md#dec-049) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "What is the final exercise-creation flow across the website and VS Code?" | Manual creation and AI-assisted generation are separate tabs. The Customer also discussed uploading a project ZIP and configuring a single task container with a Dockerfile. The ZIP and container details are carried by the open questions below. | [DEC-051](../../docs/decisions.md#dec-051), [DEC-052](../../docs/decisions.md#dec-052) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "How will AI assistance be provided in the VS Code container, and whose API key and quota will be used?" | Not answered. API keys and provider-specific endpoints were discussed and the Customer offered a token, but the credential and provider configuration was not agreed; the question reappears below. | None |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "How does the professor configure the tools available to students?" | Partly answered: a Dockerfile is preferred over Docker Compose for a single task container. The teacher-facing configuration and the available tools remain open. | [DEC-051](../../docs/decisions.md#dec-051) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "Which malicious-code checks are required, separately from unfair-solution detection?" | Not answered. No malicious-code scanning or security-check design was agreed. | None |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "What model, trigger, resource limits and false-positive process apply to post-deadline analysis?" | Not answered. AI-agent review and provider configuration were discussed, but the trigger, provider, limits, failure handling and false-positive process were not settled; the question reappears below. | None |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "What columns and semantics should the results CSV contain, and what Moodle workflow is expected?" | Partly answered: the CSV includes the grade. The exact columns and the Moodle process remain open; the question reappears below. | [DEC-049](../../docs/decisions.md#dec-049) |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "What happens to submissions after the deadline?" | Partly answered: a missed-deadline assignment stays visible in the student's all-assignments and history view. Whether late submissions are accepted and how they are graded was not settled; the question reappears below. | None |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "How are group membership changes and assignment notifications shown to students?" | Not answered. The student assignment and history views were discussed, but notification behavior and group-membership change handling were not settled. | None |
| [`reports/week-07/meeting-report.md`](../week-07/meeting-report.md#open-questions): "Can a group have multiple professors, and how are university accounts verified?" | Not answered. Neither point was established at this meeting. | None |
| [`reports/week-06/meeting-report.md`](../week-06/meeting-report.md#open-questions): "What total upload size, file count and folder depth does the MVP allow?" | Not answered. Project ZIP upload was discussed, but no limits were agreed; the question reappears below. | None |
| [`reports/week-06/meeting-report.md`](../week-06/meeting-report.md#open-questions): "Which supplementary formats are allowed besides source code?" | Not answered. No permitted-format policy was agreed. | None |
| [`reports/week-06/meeting-report.md`](../week-06/meeting-report.md#open-questions): "How are hidden tests mounted so submitted code cannot read or modify them?" | Not answered at this meeting. | None |
| [`reports/week-06/meeting-report.md`](../week-06/meeting-report.md#open-questions): "What are the concurrent-container and queue limits?" | Not answered at this meeting; the container-limit question below carries it. | None |

## Summary

- Course management stays outside Debug GYM: the course name appears first in the group description, and professors manage assignments and deadlines per group and can unassign an exercise.
- Closing an assignment is final and opens its results view, and a student's submission is accepted even when the automated tests fail.
- The CSV export includes the grade, which the application does not calculate.
- Manual exercise creation and AI-assisted generation are separate tabs, a single task container uses a Dockerfile, and student-created exercises stay private.
- The VS Code test and submit controls were hard to discover during the Customer's test, and the AI provider, credentials, upload validation and container limits remain unresolved.

## Decisions

- [DEC-044: Keep course management outside Debug GYM and put the course name first in the group description.](../../docs/decisions.md#dec-044)
- [DEC-045: Support group-specific exercise assignments and deadlines.](../../docs/decisions.md#dec-045)
- [DEC-046: Allow a professor to unassign an exercise from a group.](../../docs/decisions.md#dec-046)
- [DEC-047: Treat assignment closure as final and use it to open the results view.](../../docs/decisions.md#dec-047)
- [DEC-048: Accept student submissions regardless of whether automated tests pass.](../../docs/decisions.md#dec-048)
- [DEC-049: Include grades in assignment-result CSV exports without calculating grades in the application.](../../docs/decisions.md#dec-049)
- [DEC-050: Keep student-created exercises private and prevent students from publishing them to the public gallery.](../../docs/decisions.md#dec-050)
- [DEC-051: Use a Dockerfile rather than Docker Compose for a single task container.](../../docs/decisions.md#dec-051)
- [DEC-052: Separate manual exercise creation and AI-assisted exercise generation into different tabs.](../../docs/decisions.md#dec-052)

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Update the group and assignment requirements and stories for the course name in the group description, group-specific deadlines and unassigning an exercise, and add the traceability links to `DEC-039` through `DEC-046`. | adelazzi | End of Week 9 |
| Clarify with the Customer whether a professor can inspect submissions before closing an assignment and whether closing needs a confirmation step. | adelazzi | End of Week 9 |
| Show the `UT-01` results, the findings and the product response to the Customer, and record the Customer's decision on the fixes. | adelazzi | End of Week 9 |
| Implement and verify that a submission is accepted when the automated tests fail, and investigate the debug-server connectivity problem the Customer met. | qwxiae | End of Week 9 |
| Specify the project ZIP upload validation rules and the Dockerfile configuration expected for a task container, including its resource limits. | qwxiae | End of Week 9 |
| Prepare a sample CSV export with assignment results and grades, and confirm the exact columns and the downstream grading workflow with the Customer. | Danashi11 | End of Week 9 |
| Confirm with the Customer how the student assignment and history views show missed-deadline assignments and grades, and what late-submission behavior is expected. | Danashi11 | End of Week 9 |
| Make the VS Code extension's test and submit controls easier to find, through clearer instructions or a dedicated usage page. | UTKANOS-RIBA | End of Week 9 |
| Confirm the AI provider, endpoint configuration, credential handling and behavior when the agent cannot complete a request, without assuming an unconfirmed provider. | UTKANOS-RIBA | End of Week 9 |

## Open questions

| Question                                                                                                                   | What it would change                                                       | Follow-up                                                                               |
| -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Can a professor inspect submissions before closing an assignment?                                                          | Assignment lifecycle, teacher workflow and results access.                 | Confirm whether pre-close inspection is required.                                       |
| Should closing an assignment require a confirmation step, given that closure is final?                                     | Assignment controls and prevention of accidental closure.                  | Show the close-assignment interaction and confirm expected behavior.                    |
| What happens to submissions and results when an exercise is unassigned from a group?                                       | Assignment history, student visibility and preservation of submitted work. | Specify the expected behavior before implementation.                                    |
| What exact fields should appear in the teacher results table and CSV export?                                               | Teacher results UI and export format.                                      | Bring a sample table and CSV for customer review.                                       |
| How should grades be represented in the CSV, and what is the intended Moodle workflow?                                     | Export implementation and downstream grading.                              | Confirm column names, grade semantics and import process.                               |
| Which AI provider and endpoint should be supported, and how should API credentials be stored and supplied?                 | Agent integration, secrets management, provider compatibility and cost.    | Agree the provider and credential-handling design.                                      |
| What should happen when AI-assisted generation or review fails?                                                            | Error handling, user experience and manual fallback.                       | Confirm whether users can continue manually and how failures are reported.              |
| What ZIP file limits, project structure and validation rules should apply to uploaded exercises?                           | Exercise upload, storage and security.                                     | Propose file-size, file-count and structure limits.                                     |
| What resource limits and execution settings apply to Dockerfile-based task containers?                                     | Container isolation, reliability and infrastructure cost.                  | Propose and validate container limits.                                                  |
| How should students discover the VS Code extension's test and submit controls?                                             | Extension usability and onboarding documentation.                          | Provide a clearer guide or dedicated extension-use page.                                |
| How should missed-deadline assignments appear, and what late-submission behavior is expected?                              | Student history, assignment eligibility and grading.                       | Confirm whether late submissions are accepted and how they are marked.                  |
| How should student assignment details and grades be shown without redundant grade information?                             | Student dashboard and assignment-history UI.                               | Review a revised student assignment and history page.                                   |
| How should students browse their private exercises and remove an exercise?                                                 | Student exercise catalogue, filtering and confirmation interactions.       | Confirm the private-exercise list and removal confirmation behavior.                    |
| What are the final rules for suspicious-submission review, including provider, trigger, false positives and manual review? | Academic-integrity workflow, agent execution and review UI.                | Agree the review process without assuming an unconfirmed provider or automation policy. |
| How are group membership changes and assignment notifications communicated to students?                                    | Student dashboard and notification requirements.                           | Confirm notification expectations.                                                      |
| Can a group have multiple professors, and how are university accounts verified?                                            | Group permissions and authentication.                                      | Carry forward for customer confirmation.                                                |
| Which malicious-code checks are required, separately from unfair-solution detection? | Submission security, execution policy and false-positive handling. | Specify the threat cases and compare feasible checks; do not assume a scanner or provider. |
| How are hidden tests mounted so that submitted code cannot read or modify them? | Execution architecture and submission integrity. | Specify this together with the Dockerfile-based task container. |

## Disagreements

| Your position                                                                                   | Customer's position                                                                                                                                     | What you changed                                                                                                                                    |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| The team had a submission workflow in which automated tests provide feedback on submitted work. | During the customer test, the debug server could not be reached. The customer and team agreed that submissions should be accepted even when tests fail. | Submission acceptance must not depend on successful test execution. The connectivity issue still needs investigation.                               |
| The team discussed the exercise and course context through the existing group model.            | The customer explained that courses are managed externally and asked for the course name to be clearly visible in the group context.                    | Keep the existing group model and put the course name first in the group description; do not introduce a new course-management model.               |
| The team demonstrated the VS Code extension's test and submit workflow.                         | The customer found the controls difficult to discover.                                                                                                  | Improve extension instructions or provide a dedicated page explaining how to use the extension.                                                     |
| The team discussed AI-assisted generation and review with provider and API-key configuration.   | The customer highlighted that provider-specific endpoints matter and offered to provide a token.                                                        | Record the provider and credential configuration as unresolved; do not treat the provider, key-handling approach or fallback behavior as finalized. |
