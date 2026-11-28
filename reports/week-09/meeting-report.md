# Sprint 9 Customer meeting report

## Metadata

- **Status:** Retrospective draft for team verification; not a completed acceptance record.
- **Date:** 2026-11-28, confirmed by the team.
- **Duration:** Approximately 1 hour 29 minutes 34 seconds.
- **Format:** Recorded screen-based review; the required in-person format is not established from the supplied evidence.
- **Presented:** Administrator accounts/email/import/groups; student assignments, practice and results; browser/local VS Code; professor catalog, creation, provider settings and assignment; UATs and handoff expectations.
- **Build:** The owner confirms main as of 2026-11-28 at 13:30. The [candidate reviewed baseline](../../docs/user-acceptance-tests.md#review-baseline) is `43de5255488ddd6f98e254c05da50c7a1d8f4edf` assuming UTC+03:00; timezone and per-run deployment identity still need confirmation.
- **Deployment:** The administrator presenter states a local launch at 00:03:13–00:03:18; a university-VM deployment is reported at 01:07:43–01:08:02. Which environment each scenario used needs verification.
- **Recording:** Permission confirmed by the team; the recording must remain private and is not included in this PR.
- **Transcript publication:** Not established. No full transcript is included.
- **Transcript shared privately:** Permission and instructor access require confirmation.
- **Evidence:** [Sanitized, timestamped notes](meeting-notes.md); raw automatic transcripts and recording stay outside the repository.
- **Script:** None supplied or found for Week 9. Recover the actual pre-meeting script if it exists; do not backdate a reconstruction.

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [Week 8](../week-08/meeting-report.md#action-points): "Update the group and assignment requirements and stories for the course name in the group description, group-specific deadlines and unassigning an exercise, and add the traceability links to `DEC-039` through `DEC-046`." | Group identity is reconsidered at 00:11:07–00:13:49. Removal of the separate group number is read back; requirement/story updates are not established. Carry forward. | Member-verified new decision pending. |
| [Week 8](../week-08/meeting-report.md#action-points): "Clarify with the Customer whether a professor can inspect submissions before closing an assignment and whether closing needs a confirmation step." | Closure appears near 01:26:19, but no complete pre-close inspection/confirmation policy is recovered. Carry forward. | None established. |
| [Week 8](../week-08/meeting-report.md#action-points): "Show the `UT-01` results, the findings and the product response to the Customer, and record the Customer's decision on the fixes." | No identifiable UT-01 results/instrumentation/QR-07 presentation was recovered. The [qualitative record](../../docs/usability-tests/ut-01/results.md) exists, but that does not prove it was reviewed here. Carry forward unless the team supplies another source. | None established. |
| [Week 8](../week-08/meeting-report.md#action-points): "Implement and verify that a submission is accepted when the automated tests fail, and investigate the debug-server connectivity problem the Customer met." | Browser submission updates status at 00:39:39–00:40:41; a local-extension submission with zero passing tests is described at 00:46:19–00:46:55. Exact build/counts need verification. A return-navigation authentication problem remains. | New acceptance/defect decisions pending. |
| [Week 8](../week-08/meeting-report.md#action-points): "Specify the project ZIP upload validation rules and the Dockerfile configuration expected for a task container, including its resource limits." | ZIP/Dockerfile/entry-file configuration is discussed at 00:57:15–00:59:57. Visible/hidden test separation needs clarification; resource-limit acceptance is not established. Carry forward. | None established. |
| [Week 8](../week-08/meeting-report.md#action-points): "Prepare a sample CSV export with assignment results and grades, and confirm the exact columns and the downstream grading workflow with the Customer." | Export is discussed at 01:25:42–01:26:25 for existing data; the schema and grade semantics are not confirmed. Carry forward. | None established. |
| [Week 8](../week-08/meeting-report.md#action-points): "Confirm with the Customer how the student assignment and history views show missed-deadline assignments and grades, and what late-submission behavior is expected." | Status tabs are reviewed; To do should be the default and the cross-course grade average should be removed. Historical multi-file viewing is future work. Late-submission rules remain unresolved. | Member-verified UI/deferral decisions pending. |
| [Week 8](../week-08/meeting-report.md#action-points): "Make the VS Code extension's test and submit controls easier to find, through clearer instructions or a dedicated usage page." | Local-editor support is positively received. Clearer instructions, copy-code and completion feedback are requested. Not closed; carry forward the remaining polish. | Member-verified feedback pending. |
| [Week 8](../week-08/meeting-report.md#action-points): "Confirm the AI provider, endpoint configuration, credential handling and behavior when the agent cannot complete a request, without assuming an unconfirmed provider." | OpenRouter is discussed/configured privately and student generation is demonstrated. Professor settings/generation and failure behavior are not established. Carry forward those parts. | Provider-direction decision pending verification; credentials remain private. |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [Week 8](../week-08/meeting-report.md#open-questions): "Can a professor inspect submissions before closing an assignment?" | Not explicitly settled; retain as open. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "Should closing an assignment require a confirmation step, given that closure is final?" | A closure demonstration is not an explicit policy answer; retain as open. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "What happens to submissions and results when an exercise is unassigned from a group?" | Historical access is discussed for group lifecycle, not a complete unassignment policy. Retain as open. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "What exact fields should appear in the teacher results table and CSV export?" | Result download is discussed; final columns are not agreed in the recovered dialogue. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How should grades be represented in the CSV, and what is the intended Moodle workflow?" | Not settled. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "Which AI provider and endpoint should be supported, and how should API credentials be stored and supplied?" | OpenRouter is used in the student demonstration; exact model, final credential policy and professor configuration still need confirmation. | New source-verified decision pending. |
| [Week 8](../week-08/meeting-report.md#open-questions): "What should happen when AI-assisted generation or review fails?" | Initial generation postponement is followed by a successful student demonstration. No general failure policy is established. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "What ZIP file limits, project structure and validation rules should apply to uploaded exercises?" | Configuration is discussed, without a verified final limit policy. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "What resource limits and execution settings apply to Dockerfile-based task containers?" | Not settled. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How should students discover the VS Code extension's test and submit controls?" | Improve instructions, add copy-code and clearer completion feedback. | New source-verified feedback decision pending. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How should missed-deadline assignments appear, and what late-submission behavior is expected?" | Prefer To do initially; a precise late-work policy is not settled. | New UI decision pending; late policy open. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How should student assignment details and grades be shown without redundant grade information?" | Make the dashboard compact and remove the cross-course average. | New source-verified decision pending. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How should students browse their private exercises and remove an exercise?" | All/My/Public filtering is requested; removal policy is not established. | New filtering decision pending; removal open. |
| [Week 8](../week-08/meeting-report.md#open-questions): "What are the final rules for suspicious-submission review, including provider, trigger, false positives and manual review?" | No complete policy is established. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How are group membership changes and assignment notifications communicated to students?" | Account email is shown; this does not establish membership/assignment notifications. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "Can a group have multiple professors, and how are university accounts verified?" | Any email is allowed under administrator responsibility at 00:02:15–00:02:37. Multiple-professor policy is not answered. | New email-policy decision pending. |
| [Week 8](../week-08/meeting-report.md#open-questions): "Which malicious-code checks are required, separately from unfair-solution detection?" | Not settled. | None. |
| [Week 8](../week-08/meeting-report.md#open-questions): "How are hidden tests mounted so that submitted code cannot read or modify them?" | The entry-file explanation is challenged; no isolation verification is shown. | None. |

## Summary

- Administrator provisioning, email/import and membership workflows were demonstrated. Simplify group identity, clear filtered-out selections and add individual membership editing.
- Prefer owner-selected passwords through emailed setup links; do not display or retain existing plaintext passwords. Any email domain is permitted under administrator responsibility.
- Student generation, correction and submission were demonstrated, and the reviewer called that UAT a pass. Creating and signing in to a professor account also worked.
- Professor group assignment remained blocked. Student UI and local-editor instructions/navigation need polish; full historical submissions and student forks are future work.
- Before handoff, fix the blocker and make the README useful to real users. Formal UAT identities, reviewed build, permissions and DEC entries still need verification.

## User acceptance tests

The [UAT record](../../docs/user-acceptance-tests.md) is a retrospective draft.
Its numbering must be reconciled with any original pre-review definitions.
The evidence does not establish that three tests were documented beforehand.

**Build tested:** Owner-reported main at 13:30, with the
[candidate commit](../../docs/user-acceptance-tests.md#review-baseline) qualified
by timezone. Administrator demonstration includes local execution; a VM
deployment is reported later. Confirm each run's environment.

| Test/journey | Runner | Result | Observation and evidence | Decision |
| --- | --- | --- | --- | --- |
| [UAT-01](../../docs/user-acceptance-tests.md#uat-01), provisional identity: account provisioning/sign-in | Team attribution to confirm | Observed successful check; formal classification pending. | A created professor signs in with the same initial credentials; reviewer confirms it works, 01:22:59–01:24:42. Broader administrator criteria need original-test verification. | Separate DEC entry pending member verification. |
| [UAT-02](../../docs/user-acceptance-tests.md#uat-02), provisional identity: student generation/fix/submission | Team attribution to confirm | Explicit Pass statement; formal record incomplete. | Generated matrix-mean task is corrected/submitted, 01:10:27–01:19:38. Reviewer calls this UAT passing at 01:22:37–01:22:58. Return-button defect remains documented. | Separate DEC entry pending member verification. |
| [UAT-03](../../docs/user-acceptance-tests.md#uat-03), provisional identity: professor/student/results cycle | Team attribution to confirm | Assignment failed; fresh complete journey not established. | Failed assignment attempt, 01:02:32–01:05:28. Desired cross-role cycle clarified at 01:24:44–01:26:25. Existing demo-data export does not complete it. | Separate Fail/Not run classification and DEC pending original-test verification. |

There is no claim that all three UATs passed. Student generation does not prove
professor generation. Do not convert an unexecuted AI step into an observed
provider failure or silently replace the failed fresh-assignment step.

## Decisions

Member verification and new entries in `docs/decisions.md` are pending.
The agent has not edited that protected record or invented DEC identifiers.
[Timestamped candidate decisions](meeting-notes.md#candidate-decisions-requiring-member-verification)
cover email policy, group identity, password invitations, filtered selection,
student UI, deferred features, the three acceptance outcomes and handoff scope.
No story is newly closed or accepted without its `US-nn`/criteria mapping.

## Action points

Owners and dates below are intentionally unassigned: the recording does not
establish them. A team member must replace each pending value with a verified
GitHub username and due date inside a named week before final submission.

| Action | Owner | Due |
| --- | --- | --- |
| Reproduce/fix professor group assignment and re-run the complete fresh professor/student/export journey. | Pending team assignment. | Before handoff; exact Week 10 date pending. |
| Complete professor provider settings and verify its generation independently of the student flow. | Pending team assignment. | Before the Week 10 UAT rerun. |
| Update requirements/stories for the reviewed group identity and implement removal of the separate number input with safe data migration. | Pending team assignment. | Week 10 date pending. |
| Prefer account creation without an administrator-chosen password and send an owner password-setup link. | Pending team assignment. | Week 10 date pending. |
| Clear hidden selections after filtering and keep the counter aligned with the intended checked rows. | Pending team assignment. | Week 10 date pending. |
| Add individual student group-membership editing alongside bulk operations. | Pending team assignment. | Week 10 date pending. |
| Compact the student dashboard, default to To do and remove the cross-course grade average. | Pending team assignment. | Week 10 date pending. |
| Improve ownership/public filters, search-match clarity and latest-submission placement. | Pending team assignment. | Week 10 prioritization pending. |
| Add copy-code, clearer local-editor guidance and meaningful successful-completion feedback. | Pending team assignment. | Week 10 prioritization pending. |
| Diagnose/fix return-to-site authentication without exposing IDE credentials or weakening browser access controls. | Pending team assignment. | Before handoff; exact date pending. |
| Clarify visible/hidden test configuration, ZIP validation and container limits; verify actual isolation. | Pending team assignment. | Before claiming these capabilities; Week 10 date pending. |
| Supply a result CSV sample and settle columns/grade semantics, pre-close access, unassignment and late-work policy. | Pending team assignment. | Week 10 review date pending. |
| Present the UT-01 findings/product response if not already reviewed; retain its protocol limitations. | Pending team assignment. | Week 10 review date pending. |
| Complete the suspicious-review provider/failure/false-positive policy rather than infer it from generation. | Pending team assignment. | Week 10 review date pending. |
| Rewrite the root README for users and link deployment/product instructions; schedule handoff before demo day. | Pending team assignment. | Before handoff/demo day; exact appointment pending. |
| Record historical multi-file viewing and public-bug forks as future work; confirm group deactivation scope without deleting history. | Pending team assignment. | Week 10 refinement date pending. |
| Recover original script/UAT identities, reviewed builds, permissions and actual runners; verify and record decisions. | Pending team assignment. | Before Assignment 9 submission. |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Was permission granted to publish a sanitized transcript or share one privately with instructors? | Permitted transcript handling, separate from confirmed recording permission. | Team verifies these two distinct permission answers; the recording remains private. |
| Which commit/tag and environment were used in each UAT, and who operated it? | Traceable acceptance results. | Supply deployment/build and runner evidence. |
| Where are the original pre-review script and three UAT definitions? | Advance-preparation compliance and correct test numbering/results. | Recover existing sources or declare the omission. |
| Does the third UAT specifically require professor AI generation? | Correct Fail versus Not run classification and rerun scope. | Preserve the original expected result, not a retrospective narrower substitute. |
| Is group deactivation scheduled or deferred, and what happens on unassignment? | Lifecycle behavior and historical student access. | Confirm the changing discussion at 00:07:21–00:11:07 and carry forward the separate unassignment question. |
| What exact CSV/grade, late-work and pre-close inspection rules apply? | Teaching workflow and acceptance criteria. | Bring explicit examples to the next review. |
| What final provider/failure/false-positive and malicious-code policies apply? | Safe generation/review and execution behavior. | Carry forward the unresolved Week 8 questions. |
| Which upload, hidden-test and resource-limit rules are accepted? | Validated container/test configuration. | Present the implementation and its evidence, not only the entry-file UI. |
| How are membership/assignment notifications and student exercise removal handled; can a group have several professors? | Notification, lifecycle and role scopes. | Carry forward the unresolved Week 8 questions. |
| Were quality/threshold results and UT-01 findings discussed outside the recovered recording? | Correct quality-plan/threshold evidence and earlier-action closure. | Team supplies the missing evidence; no success inferred. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| Separate group name, course and group number were shown. | Group number duplicates identity that the name can carry. | Removal is read back; no implementation is claimed in this report. |
| Selection persisted across filters, including hidden rows. | Hidden selections should not remain or reappear. | Record a required correction rather than call the old persistence design accepted. |
| Initial credentials could be entered/emailed during account creation. | Owner-selected passwords via setup link are preferred after discussing storage/email risks. | Record the new preference; do not recover or expose stored plaintext passwords. |
| Student results included a cross-course grade average. | Different weights make that average unhelpful. | Removal requested, not yet verified. |
| Only the latest/limited submission preview is available. | Full historical multi-file viewing is useful but new features should be deferred. | Record as future work, not a new immediate commitment. |
| Entry-file configuration was used to explain hidden-test visibility. | One path is not enough to specify hidden files. | Clarify the model and verify isolation. |
| The professor flow was described as supporting group assignment. | The actual attempt failed. | Retain the blocker; exporting older demo results does not make the fresh journey pass. |
