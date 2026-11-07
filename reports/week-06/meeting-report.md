# Week 6 customer meeting report

## Metadata

- **Date:** 2026-11-06
- **Duration:** Approximately 41 minutes across two recording parts
- **Attendees:** Customer and Team 02; the automatic transcript does not
  reliably identify individual speakers
- **Presented:** The updated learner flow, the removal of the browser editor,
  live test-result updates, the draft role split, and teacher-side interface
  concepts for groups, assignments, deadlines and results
- **Recording:** A recording and automatic transcript were provided to the team
- **Public record:** Sanitized, decision-focused
  [meeting notes](meeting-notes.md); no verbatim transcript or recording is
  published

The source transcript occasionally assigns a reply to the wrong speaker. This
report therefore attributes statements only to the Customer or the team when
the context makes that role clear. It records an outcome as a decision only
when the discussion reached an explicit agreement.

## Previous Action Points

| Week 5 action | Outcome | Decision |
| --- | --- | --- |
| Remove the preview and debug control, make the test panel update dynamically, and fix remaining links. | Partly done. The team reported the dynamic update as fixed. The browser editor removal existed but was missing from the demonstrated branch because it had been merged to the wrong base; the team corrected this after the meeting. Link fixes were not reviewed. | [DEC-038](../../docs/decisions.md#dec-038) confirms that the page retains tests, not the browser editor. |
| Add admin, teacher and student roles with private, public and group access. | The role split was presented as the direction, but complete role and audience enforcement was not demonstrated. | No new decision; [DEC-017](../../docs/decisions.md#dec-017) to [DEC-020](../../docs/decisions.md#dec-020) remain active. |
| Add groups, group/exercise deadlines, best-submission scoring and CSV export. | Not implemented. The meeting refined assignment to group-only, put membership management on the administrator side and kept dashboard/export details open. | [DEC-032](../../docs/decisions.md#dec-032), [DEC-033](../../docs/decisions.md#dec-033), [DEC-036](../../docs/decisions.md#dec-036) |
| Change the request form and title-search label. | Not reviewed in this meeting. | None |
| Rework the left panel. | Not reviewed in this meeting. | None |
| Update stories, acceptance criteria and functional requirements for the university workflow. | The role/access constraints were documented, but the separate group, assignment, deadline, result and execution-safety stories still need refinement. | None |
| Analyse whether free-text Custom instructions are usable for a new learner. | Not reviewed; carried forward. | None |
| Decide how a student sees groups. | Not settled. The meeting concentrated on a teacher group-first dashboard and deliberately chose to validate the exact UI through a prototype. | None |
| Set up a mailbox for verification codes. | Not reviewed; carried forward. | None |

## Previous Open Questions

| Week 5 question | Outcome | Decision |
| --- | --- | --- |
| Should learner code run in a server-side sandbox or on the learner's computer? | Closed for the current direction: submissions run server-side in fresh, temporary containers. | [DEC-037](../../docs/decisions.md#dec-037) |
| Are Custom instructions usable for someone who has never met the bug? | Not answered; carried forward. | None |
| How does a student see their groups? | Not answered. The teacher dashboard was discussed, but the student presentation was not settled. | None |
| Is a student notified when an exercise is assigned? | Not answered; carried forward. | None |
| What happens after an assignment deadline? | Not answered. The deadline's location was clarified, but late editing and automatic submission remain open. | [DEC-035](../../docs/decisions.md#dec-035) covers only where the deadline belongs. |
| Can a group have more than one teacher? | Not answered; carried forward. | None |
| How are verification codes sent? | Not answered; carried forward. | None |
| Should people outside the university use the product later? | Not discussed; the university-first scope remains unchanged. | None |

## Summary

- A student has three practice routes: complete an exercise assigned to a
  group, choose a teacher-published exercise from the university gallery, or
  generate a private exercise for personal practice.
- Teachers assign an existing exercise to one or more groups, not directly to
  individual students. Administrators manage group membership.
- Exercises have selected visible tests for reproduction and additional hidden
  tests for verification. Hidden tests must not be readable by submitted code.
- Estimated duration is removed. A deadline belongs to each group/exercise
  assignment; behavior after the deadline remains open.
- Legal-excuse handling stays outside Debug GYM and remains in Moodle.
- Each submission runs in a fresh temporary container. Concurrency and queue
  sizes are bounded, but their numeric limits remain to be chosen.
- The teacher dashboard's exact result fields and layout will be validated with
  a prototype rather than settled from the verbal discussion.

## Decisions

- [DEC-032: Give students assigned, gallery and private-generation practice routes.](../../docs/decisions.md#dec-032)
- [DEC-033: Assign exercises to groups and manage group membership as an administrator operation.](../../docs/decisions.md#dec-033)
- [DEC-034: Use visible reproduction tests and hidden verification tests.](../../docs/decisions.md#dec-034)
- [DEC-035: Remove estimated duration and put the deadline on the group/exercise assignment.](../../docs/decisions.md#dec-035)
- [DEC-036: Keep legal-excuse handling outside Debug GYM.](../../docs/decisions.md#dec-036)
- [DEC-037: Verify every submission in a fresh temporary container with bounded concurrency and queueing.](../../docs/decisions.md#dec-037)
- [DEC-038: Keep test and reproduction information on the learner page after removing its browser editor.](../../docs/decisions.md#dec-038)

## Action Points

| Action | Owner | Due |
| --- | --- | --- |
| Refine separate stories and requirements for group membership, group assignment, deadlines, teacher results and isolated submission execution. | Team 02 | 2026-11-13 (Week 7) |
| Build a teacher group-first dashboard prototype: groups, members, assigned exercises and result drill-down; validate its layout at the next review. | Team 02 | 2026-11-13 (Week 7) |
| Define and test the fresh submission-container lifecycle, concurrency limit, bounded queue and waiting response. | Team 02 | 2026-11-13 (Week 7) |
| Propose an MVP total upload-size limit and permitted supplementary file types, with evidence for the chosen values. | Team 02 | 2026-11-13 (Week 7) |

## Open Questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| What total upload size, file count and folder depth does the MVP allow? | Validation, storage and denial-of-service controls. | Measure representative exercises and propose limits. |
| Which supplementary formats are allowed besides source code? | Upload validation and exercise packaging. | Decide whether CSV and text-like data are required; do not infer a policy from the transcript. |
| Which external or built-in security checks supplement container isolation? | Submission acceptance, cost and false-positive handling. | Compare options; no provider or AI scanner was selected. |
| How are hidden tests mounted so submitted code cannot read or modify them? | The execution architecture and submission integrity. | Specify this with the fresh-container implementation. |
| What are the concurrent-container and queue limits? | Capacity, waiting behavior and resource cost. | Load-test before choosing numeric limits. |
| What does the teacher dashboard show: pass/fail, passed count, failed test, source, or a drill-down combination? | Teacher workflow, privacy and CSV schema. | Validate the group-first prototype with the Customer. |
| What happens after a deadline, and how are late submissions treated? | Submission eligibility and best-result calculation. | Ask explicitly at the next review. |
| How does a student see group assignments and notifications? | Student home screen and notification scope. | Carry forward from Week 5. |
| How are university emails verified, and can a group have multiple teachers? | Identity and group model. | Carry forward from Week 5. |

## Discussion Not Recorded As A Decision

The meeting explored AI scanning, third-party security APIs, Cloudflare, exact
file and line limits, accepted attachment types, rankings, detailed CSV fields
and manual review through external messaging. None reached a sufficiently clear
agreement, so they remain proposals or open questions rather than requirements.

## Privacy

The report contains no private infrastructure address, credential or personal
data. It uses role names instead of attempting to reconstruct unreliable
speaker identities.
