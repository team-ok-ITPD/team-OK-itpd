# Week 8 customer meeting report

## Metadata

- **Date:** 2026-11-20
- **Attendees:** Customer and Team 02
- **Presented:** Group and assignment workflows; teacher assignment and results views; exercise creation and catalogue; student assignment and history pages; VS Code extension workflow; submission and test behavior; CSV export; AI-assisted exercise generation and submission review
- **Script:** [meeting-script.md](../week-08/meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [Week 7 report](../week-07/meeting-report.md#action-points): Update the role, group-assignment and teacher-results stories and requirements to reflect DEC-039 and DEC-040; add the corresponding traceability links. | The meeting revisited group assignment, teacher results and student assignment views. The customer clarified that course management remains external and that the course name should be visible in the group context. The transcript does not confirm that all related stories and traceability links were updated. | [DEC-044](../../docs/decisions.md#dec-044), [DEC-045](../../docs/decisions.md#dec-045) |
| [Week 7 report](../week-07/meeting-report.md#action-points): Specify the post-deadline suspicious-submission review scenario, including initiation, flagged-result review and false-positive handling, without assuming an unapproved provider or cost model. | AI-assisted review and API configuration were revisited. The customer discussed provider-specific endpoints and offering a token. The provider, credential handling, failure behavior and final review process were not settled. | None |
| [Week 7 report](../week-07/meeting-report.md#action-points): Propose the teacher-facing configuration for tools in the student container and identify the container changes it requires. | The meeting discussed exercise creation and container configuration. For a single task container, the customer preferred a Dockerfile rather than Docker Compose. The complete teacher-facing tool-configuration mechanism remains open. | [DEC-051](../../docs/decisions.md#dec-051) |
| [Week 7 report](../week-07/meeting-report.md#action-points): Define a first CSV export schema for assignment results and check its suitability for the intended grading workflow. | CSV export was discussed again. The customer agreed that the export should include the grade. The application does not calculate the grade; the exact CSV schema and downstream workflow remain to be specified. | [DEC-049](../../docs/decisions.md#dec-049) |
| [Week 7 report](../week-07/meeting-report.md#action-points): Present the UT-01 design and agree the session plan and results date. | The supplied Week 8 transcript does not establish that the UT-01 design was presented or that a session plan and results date were agreed. Carry forward. | None |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [Week 7 report](../week-07/meeting-report.md#open-questions): What exact fields and drill-downs should the professor see in the group-results view? | The teacher workflow was discussed, including closing an assignment to open its results. CSV export should include the grade. The complete results-table fields and drill-down behavior were not fully specified. | [DEC-047](../../docs/decisions.md#dec-047), [DEC-049](../../docs/decisions.md#dec-049) |
| [Week 7 report](../week-07/meeting-report.md#open-questions): What is the final exercise-creation flow across the website and VS Code? | Manual exercise creation and AI-assisted generation should be separate tabs. The customer also discussed uploading a project ZIP and configuring a single task container with a Dockerfile. | [DEC-051](../../docs/decisions.md#dec-051), [DEC-052](../../docs/decisions.md#dec-052) |
| [Week 7 report](../week-07/meeting-report.md#open-questions): How will AI assistance be provided in the VS Code container, and whose API key and quota will be used? | API keys and provider-specific endpoints were discussed. The customer offered to provide a token, but the final credential and provider configuration was not agreed. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): How does the professor configure the tools available to students? | Dockerfile configuration was preferred over Docker Compose for a single task container. The full teacher-facing configuration and available tools remain open. | [DEC-051](../../docs/decisions.md#dec-051) |
| [Week 7 report](../week-07/meeting-report.md#open-questions): Which malicious-code checks are required, separately from unfair-solution detection? | No complete malicious-code scanning or security-check design was agreed in the supplied transcript. Remains open. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): What model, trigger, resource limits and false-positive process apply to post-deadline analysis? | AI-agent review and provider configuration were discussed, but the trigger, provider, limits, failure handling and false-positive process were not settled. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): What columns and semantics should the results CSV contain, and what Moodle workflow is expected? | The customer agreed that the CSV should include the grade. The exact columns and Moodle import or use process remain open. | [DEC-049](../../docs/decisions.md#dec-049) |
| [Week 7 report](../week-07/meeting-report.md#open-questions): What happens to submissions after the deadline? | The meeting confirmed that missed-deadline assignments should remain visible in the student's all-assignments/history view. The rules for accepting late submissions and grading them were not settled. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): How are group membership changes and assignment notifications shown to students? | Student assignment and history views were discussed. Notification behavior and group-membership change handling were not settled. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): Can a group have multiple professors, and how are university accounts verified? | Not established in the supplied Week 8 transcript. Both questions remain open. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): What upload size, file count, folder depth and supplementary formats does the MVP allow? | Project ZIP upload was discussed, but no limits or complete permitted-format policy were agreed. | None |
| [Week 7 report](../week-07/meeting-report.md#open-questions): How are hidden tests protected, and what are the concurrent-container and queue limits? | Not settled in the supplied Week 8 transcript. | None |

## Summary

- Course management remains outside Debug GYM. The customer wants the course name clearly visible in the group context, so it should appear first in the group description, followed by other useful information.
- Professors need to manage assignments for individual groups, including group-specific deadlines. They should also be able to unassign an exercise from a group.
- Closing an assignment is treated as final and opens the results view. Whether a professor can inspect submissions before closing the assignment was not settled.
- Submissions should be accepted even when automated tests fail. A failed test must not prevent a student from submitting their work.
- The customer agreed that CSV exports should include grades, while grade calculation remains outside the application.
- Manual exercise creation and AI-assisted generation should be presented as separate tabs. For a single task container, the customer preferred a Dockerfile over Docker Compose.
- Student-created exercises remain private and cannot be published to the public gallery.
- Students need to see pending assignments and retain access to all assignments, including missed-deadline assignments, in their history.
- The VS Code extension's test and submit controls were not sufficiently discoverable during the customer test. Clearer instructions or a dedicated usage page are needed.
- AI-provider configuration, credentials, agent failure handling, upload validation and container resource limits remain unresolved.

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
| Update group and assignment requirements to include the course name in the group description, group-specific deadlines and the ability to unassign an exercise. | Team | Next review |
| Clarify whether professors can inspect submissions before closing an assignment and whether closure requires confirmation. | Team and Customer | Next review |
| Implement and verify submission acceptance when automated tests fail; investigate the reported debug-server connectivity problem. | Team | Next review |
| Prepare a sample CSV export containing assignment results and grades; confirm the exact columns and downstream grading workflow. | Team and Customer | Next review |
| Improve discoverability of the VS Code extension's test and submit controls through clearer instructions or a dedicated usage page. | Team | Next review |
| Specify the project ZIP upload validation rules and the Dockerfile configuration expected for a task container. | Team | Next review |
| Confirm the AI provider, endpoint configuration, credential handling and behavior when the agent cannot complete a request. | Team and Customer | Next review |
| Confirm the student assignment/history presentation, including how missed-deadline assignments and grades are displayed. | Team and Customer | Next review |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Can a professor inspect submissions before closing an assignment? | Assignment lifecycle, teacher workflow and results access. | Confirm whether pre-close inspection is required. |
| Should closing an assignment require a confirmation step, given that closure is final? | Assignment controls and prevention of accidental closure. | Show the close-assignment interaction and confirm expected behavior. |
| What happens to submissions and results when an exercise is unassigned from a group? | Assignment history, student visibility and preservation of submitted work. | Specify the expected behavior before implementation. |
| What exact fields should appear in the teacher results table and CSV export? | Teacher results UI and export format. | Bring a sample table and CSV for customer review. |
| How should grades be represented in the CSV, and what is the intended Moodle workflow? | Export implementation and downstream grading. | Confirm column names, grade semantics and import process. |
| Which AI provider and endpoint should be supported, and how should API credentials be stored and supplied? | Agent integration, secrets management, provider compatibility and cost. | Agree the provider and credential-handling design. |
| What should happen when AI-assisted generation or review fails? | Error handling, user experience and manual fallback. | Confirm whether users can continue manually and how failures are reported. |
| What ZIP file limits, project structure and validation rules should apply to uploaded exercises? | Exercise upload, storage and security. | Propose file-size, file-count and structure limits. |
| What resource limits and execution settings apply to Dockerfile-based task containers? | Container isolation, reliability and infrastructure cost. | Propose and validate container limits. |
| How should students discover the VS Code extension's test and submit controls? | Extension usability and onboarding documentation. | Provide a clearer guide or dedicated extension-use page. |
| How should missed-deadline assignments appear, and what late-submission behavior is expected? | Student history, assignment eligibility and grading. | Confirm whether late submissions are accepted and how they are marked. |
| How should student assignment details and grades be shown without redundant grade information? | Student dashboard and assignment-history UI. | Review a revised student assignment and history page. |
| How should students browse their private exercises and remove an exercise? | Student exercise catalogue, filtering and confirmation interactions. | Confirm the private-exercise list and removal confirmation behavior. |
| What are the final rules for suspicious-submission review, including provider, trigger, false positives and manual review? | Academic-integrity workflow, agent execution and review UI. | Agree the review process without assuming an unconfirmed provider or automation policy. |
| How are group membership changes and assignment notifications communicated to students? | Student dashboard and notification requirements. | Confirm notification expectations. |
| Can a group have multiple professors, and how are university accounts verified? | Group permissions and authentication. | Carry forward for customer confirmation. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| The team had a submission workflow in which automated tests provide feedback on submitted work. | During the customer test, the debug server could not be reached. The customer and team agreed that submissions should be accepted even when tests fail. | Submission acceptance must not depend on successful test execution. The connectivity issue still needs investigation. |
| The team discussed the exercise and course context through the existing group model. | The customer explained that courses are managed externally and asked for the course name to be clearly visible in the group context. | Keep the existing group model and put the course name first in the group description; do not introduce a new course-management model. |
| The team demonstrated the VS Code extension's test and submit workflow. | The customer found the controls difficult to discover. | Improve extension instructions or provide a dedicated page explaining how to use the extension. |
| The team discussed AI-assisted generation and review with provider and API-key configuration. | The customer highlighted that provider-specific endpoints matter and offered to provide a token. | Record the provider and credential configuration as unresolved; do not treat the provider, key-handling approach or fallback behavior as finalized. |