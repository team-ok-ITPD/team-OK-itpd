# Week 5 customer meeting report

## Metadata

- **Date:** 2026-10-31
- **Duration:** Approximately 46 minutes (2 min 45 s in the English section, 43 min 44 s in the Russian section)
- **Attendees:** @UTKANOS-RIBA, @Danashi11, @qwxiae, Customer
- **Presented:** The web prototype with the VS Code button in the workspace, the dynamically updating test panel, the AI-Generated tab with its request form, the Prepared exercises list with search, and the left navigation panel.
- **Recording:** Permitted
- **Transcript publication:** Permitted, see [the transcript](meeting-transcript.md)
- **Private sharing with instructors:** Not needed, because publication was permitted
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Try both routes to VS Code, desktop VS Code over SSH and VS Code in the browser embedded in the site, and report which one can submit a multi-file solution and return the test results." | Partly shown. The workspace now has a VS Code button, an extension to test and upload, and the files live on the server, not on the learner's device. A comparison of the two routes was not presented. | None |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Build one complete scenario, preferably two exercises: log in, choose an exercise, open it in VS Code, solve it and submit from VS Code." | Partly carried out. The VS Code button and upload exist and the test panel updates after a run. Some links are still unfixed and the team said the rest was left for later. | None |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Keep the default tests read-only and add a separate set that learners can edit, per DEC-011." | Not discussed in this meeting. | None |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Rework the search: prepared exercises only, the input just above the list, every match listed, the first match selected, and no preview when there are no results, per DEC-015." | Partly carried out. Search moved into Prepared exercises. The Customer noted that the "Describe the bug you want to practice" box is only a title search, so its label misleads. | [DEC-023](../../docs/decisions.md#dec-023) |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Update the stories for DEC-012 and DEC-013, and cite the decisions in each story's change comment." | Not discussed in this meeting. | None |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Present the options for where learner code runs, with their cost per learner, to the customer." | Not presented. The Customer asked where files are stored, and the team answered that they stay on the server and nothing is kept on the device. | None |
| [reports/week-04/meeting-report.md#action-points](../week-04/meeting-report.md#action-points): "Show the containerized workspace against the acceptance criteria of US-01 to US-05 and ask for a verdict on each." | Not done. No story was shown against its acceptance criteria. | None |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [reports/week-04/meeting-report.md#open-questions](../week-04/meeting-report.md#open-questions): "Should learner code run in a sandboxed server-side container or on the learner's own computer?" | Answered in part. The team stated that files are kept on the server. Options and cost per learner were not presented, and it reappears below. | None |
| [reports/week-04/meeting-report.md#open-questions](../week-04/meeting-report.md#open-questions): "Should learners see every default test?" | Not asked. | None |
| [reports/week-04/meeting-report.md#open-questions](../week-04/meeting-report.md#open-questions): "Does the customer accept US-01 to US-05 against their acceptance criteria?" | Not asked. | None |
| [reports/week-04/meeting-report.md#open-questions](../week-04/meeting-report.md#open-questions): "How can the team verify that an exercise contains the specific intended bug?" | Not asked. | None |
| [reports/week-04/meeting-report.md#open-questions](../week-04/meeting-report.md#open-questions): "Will the team ship desktop VS Code over SSH or VS Code in the browser embedded in the site?" | Not answered. The Customer questioned the in-page preview and agreed to drop it, see DEC-016. | [DEC-016](../../docs/decisions.md#dec-016) |

## Summary

- The workspace drops the code preview and the debug control and keeps only the tests, because multi-file stubs of about 300 lines each do not fit a browser preview. The test panel must update dynamically after each run.
- The product needs three roles, admin, teacher and student. Only teachers publish to the public gallery, because a student could upload malicious code that others then run.
- Everyone except the admin can generate exercises and use their own API key. The admin uploads a key that only teachers can use.
- The Customer wants teachers to form named groups, assign exercises to them, set deadlines and download the group's results as a CSV. None of this was in the requirements before.
- Prepared exercises becomes the single list for all exercises, with the access levels private, public and shared with a group.
- The Customer wants a first version for Innopolis students and teachers, in the manner of Moodle. The team had understood the target as an open training service for any beginner.

## Decisions

- [DEC-016: Remove the code preview and the debug control from the workspace, show only the tests, and update them dynamically.](../../docs/decisions.md#dec-016)
- [DEC-017: Use three roles, admin, teacher and student, and let only teachers publish to the public gallery.](../../docs/decisions.md#dec-017)
- [DEC-018: Let everyone except the admin generate exercises and use their own API key, and let the admin's key serve teachers.](../../docs/decisions.md#dec-018)
- [DEC-019: Require authorization with a university email, with no public access for now.](../../docs/decisions.md#dec-019)
- [DEC-020: Put all exercises in Prepared exercises with the access levels private, public and group, and filters My, Public, Group and All.](../../docs/decisions.md#dec-020)
- [DEC-021: Let teachers form named groups, with one teacher per group, and download each group's results as a CSV without grades.](../../docs/decisions.md#dec-021)
- [DEC-022: Set a deadline per group and exercise, and count the best submission.](../../docs/decisions.md#dec-022)
- [DEC-023: Keep the title search in Prepared exercises and rename its label so that it no longer reads as a bug description.](../../docs/decisions.md#dec-023)
- [DEC-024: Keep Custom instructions, difficulty and language in the request form, drop topic, and give Custom instructions priority on conflict.](../../docs/decisions.md#dec-024)
- [DEC-025: Keep the left panel for started, unfinished exercises with tests passed and a delete option, and remove the New Challenge button and the Back to practice button.](../../docs/decisions.md#dec-025)
- [DEC-026: Build for the university first, with no paid features and no Moodle integration.](../../docs/decisions.md#dec-026)

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Remove the preview and the debug control, make the test panel update dynamically, and fix the remaining links. | UTKANOS-RIBA | 2026-11-05 (Week 6) |
| Add the admin, teacher and student roles with the access levels private, public and group. | qwxiae | 2026-11-06 (Week 6) |
| Add groups, deadlines per group and exercise, best-submission scoring and the CSV export of results. | UTKANOS-RIBA | 2026-11-06 (Week 6) |
| Change the request form per DEC-024 and the search label per DEC-023. | Danashi11 | 2026-11-05 (Week 6) |
| Rework the left panel per DEC-025. | Danashi11 | 2026-11-05 (Week 6) |
| Update the user stories, acceptance criteria and functional requirements for roles, groups, deadlines and CSV export, and cite DEC-017 to DEC-022. | Danashi11 | 2026-11-05 (Week 6) |
| Analyse whether free-text Custom instructions are usable for a learner who has never met the bug, as the team proposed. | Danashi11 | 2026-11-06 (Week 6) |
| Decide how a student sees their groups, and show it in a quick Figma iteration or explain it in words at the next meeting. | Danashi11 | 2026-11-05 (Week 6) |
| Set up a mailbox for verification codes, for example a new shared account. | qwxiae | 2026-11-05 (Week 6) |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Should learner code run in a sandboxed server-side container or on the learner's own computer? | Infrastructure, safety and the cost per learner, see [QR-02](../../docs/quality-requirements/qr/QR-02.md) and ADR-003. | Present the options at the next meeting. |
| Are free-text Custom instructions usable for someone who has never seen the bug? | The request form and the prompt the generator builds. | The usability analysis in the action points. |
| How does a student see their groups: a list of groups at the top left, a filter in Prepared exercises, or a feed with deadline, group and author? | The student's home screen and the work to build it. | A quick prototype or a discussion at the next meeting. |
| Is a student notified when an exercise is assigned to their group? | Whether the product needs notifications or an export to a tool such as Outlook or Moodle. | Ask at the next meeting. |
| What happens to an exercise after its deadline: is editing blocked, and is anything submitted automatically? | The deadline logic and the stored results. | Ask at the next meeting. |
| Can a group have more than one teacher? | The group model. | Ask at the next meeting. |
| How are verification codes sent: a new shared mailbox, or the university's single sign-on? | Registration and the effort of the sign-in. | The mailbox action point. |
| Should someone outside the university, such as a school pupil, be able to use the product later? | The access model, the interface and the business requirements. | Ask when the first university version is stable. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| The key is stored in the backend, and a user has no reason to enter their own. | Teachers may need a stronger model than the admin's key, and 250 students cannot all share a key with a limit of $10. Students should be able to use their own. | Everyone except the admin may enter their own key, per DEC-018. |
| Free-text Custom instructions may be of little use, and the form should offer presets instead. | A learner may have heard of a bug such as a concurrency bug and ask for it. | We kept Custom instructions with difficulty and language, and we will analyse their usability, per DEC-024. |
| Groups could be shown as a list at the top left, like projects in ChatGPT (@Danashi11), or as a filter in Prepared exercises (another team member). | A feed of assigned exercises with deadline, group and author would do, so the student clicks the earliest one. | Not settled. The first open question carries it. |
| The left panel is overhead and could be removed. | Back to practice matters, because a learner may leave an exercise unfinished and return later. | The panel stays and lists the started exercises, per DEC-025. |
| The product was understood as an open training service for beginners, like CodeForces, with a different interface for a paid version. | Start with a Moodle-like version for students and teachers, to test whether learning on bugs works, and add no paid features now. | We build for the university first, per DEC-026. |
