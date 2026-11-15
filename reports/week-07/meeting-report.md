# Week 7 customer meeting report

## Metadata

- **Date:** 2026-11-13
- **Attendees:** Customer and Team 02
- **Presented:** Administrator, professor and student pages; group and
  assignment management; bug creation and selection; the VS Code workflow;
  student dashboards; submission review and result concepts
- **Script:** [meeting-script.md](../week-07/meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [Week 6 report](../week-06/meeting-report.md#action-points): "Refine separate stories and requirements for group membership, group assignment, deadlines, teacher results and isolated submission execution." | Partly discussed. The meeting reviewed group assignment, role separation and teacher results, but the transcript does not establish that the corresponding stories and requirements were updated. Carry the unverified documentation work forward. | [DEC-039](../../docs/decisions.md#dec-039), [DEC-040](../../docs/decisions.md#dec-040) |
| [Week 6 report](../week-06/meeting-report.md#action-points): "Build a teacher group-first dashboard prototype: groups, members, assigned exercises and result drill-down; validate its layout at the next review." | A teacher interface and related administrator/student pages were demonstrated. Group assignments and group-level review were discussed. The exact result drill-down and final layout were not fully settled. | [DEC-040](../../docs/decisions.md#dec-040) |
| [Week 6 report](../week-06/meeting-report.md#action-points): "Define and test the fresh submission-container lifecycle, concurrency limit, bounded queue and waiting response." | Not addressed in the supplied transcript. The discussion covered VS Code containers and AI-agent execution, not the per-submission verification lifecycle or queue limits. Carry forward. | None |
| [Week 6 report](../week-06/meeting-report.md#action-points): "Propose an MVP total upload-size limit and permitted supplementary file types, with evidence for the chosen values." | Not addressed in the supplied transcript. Carry forward. | None |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "What total upload size, file count and folder depth does the MVP allow?" | Not discussed. Remains open. | None |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "Which supplementary formats are allowed besides source code?" | Not discussed. Remains open. | None |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "Which external or built-in security checks supplement container isolation?" | Malicious-code scanning and AI-assisted suspicious-solution analysis were discussed. No scanner, provider or complete security design was selected. The question remains open. | None |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "How are hidden tests mounted so submitted code cannot read or modify them?" | Not discussed. Remains open. | None |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "What are the concurrent-container and queue limits?" | Not discussed. Remains open. | None |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "What does the teacher dashboard show: pass/fail, passed count, failed test, source, or a drill-down combination?" | The professor should see group results, submitted code and test outcomes, including passed-test counts. The exact dashboard fields and drill-down remain open. | [DEC-040](../../docs/decisions.md#dec-040) |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "What happens after a deadline, and how are late submissions treated?" | The deadline was mentioned as an assignment property, but late-submission behavior was not discussed. Remains open. | None |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "How does a student see group assignments and notifications?" | The student dashboard was discussed and students may belong to multiple groups. Notification behavior was not discussed. | [DEC-040](../../docs/decisions.md#dec-040) |
| [Week 6 report](../week-06/meeting-report.md#open-questions): "How are university emails verified, and can a group have more than one teacher?" | Not discussed. Both questions remain open. | None |

## Summary

- Assignment management belongs to professors, while administrators manage
  users and group membership; administrators may need assignment visibility
  without taking over the professor's teaching workflow.
- The central workflow is to select or create an exercise, assign it to a
  group, let students solve and submit it, and let the professor review group
  results, test outcomes and submitted code.
- Professors need a way to configure the development tools available in the
  student environment, although the configuration mechanism is unresolved.
- The participants discussed professor-initiated, system-supported analysis
  of all submissions after the deadline, with suspicious results reviewed by
  the professor; cost, execution and false-positive controls remain open.
- CSV export was identified as useful for downstream grading, but its schema
  and Moodle workflow were not settled.

## Decisions

- [DEC-039: Keep assignment creation and editing in the professor workflow; administrators may view assignments but do not manage them.](../../docs/decisions.md#dec-039)
- [DEC-040: Make group assignment, student submission and professor review of code and test results the core workflow.](../../docs/decisions.md#dec-040)
- [DEC-041: Let professors specify which development tools are available to students for an exercise.](../../docs/decisions.md#dec-041)
- [DEC-042: Let a professor initiate system-supported suspicious-solution analysis across an assignment's submissions after its deadline.](../../docs/decisions.md#dec-042)
- [DEC-043: Provide professors with an export of assignment submission and test results.](../../docs/decisions.md#dec-043)

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Update the role, group-assignment and teacher-results stories and requirements to reflect DEC-039 and DEC-040; add the corresponding traceability links. | [Assign GitHub username] | End of Week 8 |
| Specify the post-deadline suspicious-submission review scenario, including initiation, flagged-result review and false-positive handling, without assuming an unapproved provider or cost model. | [Assign GitHub username] | End of Week 8 |
| Propose the teacher-facing configuration for tools in the student container and identify the container changes it requires. | [Assign GitHub username] | End of Week 8 |
| Define a first CSV export schema for assignment results and check its suitability for the intended grading workflow. | [Assign GitHub username] | End of Week 9 |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| What exact fields and drill-downs should the professor see in the group-results view? | Teacher dashboard, result pages and acceptance criteria. | Show a concrete result-page proposal at the next review. |
| What is the final exercise-creation flow across the website and VS Code? | Page structure, source selection, save, private/public visibility and assignment flow. | Demonstrate the gallery, own-bug and AI-generation paths end to end. |
| How will AI assistance be provided in the VS Code container, and whose API key and quota will be used? | Container image, secrets, access control, operating cost and limits. | Present an architecture and cost options before implementation. |
| How does the professor configure the tools available to students? | Exercise configuration, container build and reproducibility. | Propose a teacher-facing configuration and its technical contract. |
| Which malicious-code checks are required, separately from unfair-solution detection? | Submission security, execution policy and false-positive handling. | Specify threat cases and compare feasible checks. |
| What model, trigger, resource limits and false-positive process apply to post-deadline analysis? | Agent orchestration, infrastructure cost, review UI and academic-integrity workflow. | Produce a bounded design and confirm who initiates each run. |
| What columns and semantics should the results CSV contain, and what Moodle workflow is expected? | Export implementation and grading integration. | Bring a sample CSV and a concrete import/use scenario. |
| What happens to submissions after the deadline? | Assignment eligibility, resubmission and scoring behavior. | Ask the customer to choose the expected late-submission behavior. |
| How are group membership changes and assignment notifications shown to students? | Student dashboard and notification requirements. | Demonstrate the student view and ask about notification expectations. |
| Can a group have multiple professors, and how are university accounts verified? | Group model, permissions and authentication. | Confirm both constraints with the customer. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| The team proposed finishing the basic pages first and postponing complicated agent integration. | The customer argued that the team must first define the complete scenarios and architecture, and that agent-assisted editing and suspicious-submission review cannot simply disappear from the core requirements. | The meeting did not settle the implementation sequence. The backlog should retain the scenarios and architectural requirements while scheduling implementation incrementally; do not treat the agent work as rejected or fully specified. |
