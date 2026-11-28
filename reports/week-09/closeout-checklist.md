# Assignment 9 closeout preparation

Working checklist as of 2026-11-28, after the review. It is not the final
weekly report, submission wrapper, release approval or retrospective.
Reference: [Assignment 9](https://github.com/inno-itpd/itpd/blob/33e889a8617d04a1c31c4ab395c75cf15224ad4e/assignments/assignment-9.md).

## Prepared

- [x] [Meeting report](meeting-report.md) and [sanitized notes](meeting-notes.md)
  merged through [#218](https://github.com/team-ok-ITPD/team-OK-itpd/pull/218).
- [x] Date confirmed as 28 November; recording permission confirmed and the
  recording kept private. Do not publish a participant list.
- [x] [Retrospective UAT evidence draft](../../docs/user-acceptance-tests.md)
  distinguishes the student passing statement and failed professor assignment.
- [x] Sprint 9 platform deadline corrected to 29 November; provisional
  [Sprint 10](https://github.com/team-ok-ITPD/team-OK-itpd/milestone/8) created
  with a 6 December deadline.
- [x] [Handoff preparation](handoff-preparation.md) separates observed readiness,
  pending verification and explicitly deferred features.

## Evidence Confirmation — Team Required

- [ ] Identify the actual reviewed commit/tag and environment for each run.
  The explicitly local administrator demo and later VM-deployment statement
  do not prove every UAT ran on production.
- [ ] Recover original UAT definitions/numbering and any actual advance script.
  If unavailable, declare missing advance preparation; do not backdate files.
- [ ] Reconcile Pass/Fail/Not run against those definitions with runner `Team`
  where the team controlled the live demo. Do not choose an individual arbitrarily.
- [ ] A member verifies each real UAT judgment and records its separate DEC
  entry, then links it from the UAT and meeting records.
- [ ] Confirm sanitized-transcript publication/private instructor-sharing
  permission separately. Recording permission is not publication permission.
- [ ] Supply real action owners and dates, and confirm any story-level verdicts.
- [ ] Supply the actual team retrospective discussion and agreed improvements.
  A preparation scaffold is not a completed retrospective.

## Quality And Threshold Gates

- [ ] Reconcile every row in the
  [quality testing plan](../../docs/project-plan.md#quality-requirement-testing-plan)
  against its actual QRT protocol. Functional tests do not replace quality tests.
- [ ] Resolve the overdue Week 5/7 TOS-01/02 verdicts against dated evidence;
  lack of evidence in this recording does not establish what happened earlier.
  Do not silently keep expired goals open or move their dates.
- [ ] For TOS-03, check the full acceptance decision and five comparable
  learner usefulness responses by the end of Week 9, not merely positive remarks.
- [ ] Confirm the goal measures' Customer review: the maintained threshold file
  still identifies them as draft proposals. Do not invent approval or lower bars.
- [ ] Retain UT-01's real participant sessions and protocol limitations.
  Do not replace human sessions with agent rehearsals or claim QR-07 passed.

## Release And Sprint Close — Not Yet Authorized As Complete

- [ ] Independent review and merge of the product work selected for REL-09,
  including [#220](https://github.com/team-ok-ITPD/team-OK-itpd/pull/220) if selected.
- [ ] Release owner identifies the final product commit and cuts the protected
  SemVer tag; keep reviewed and released builds distinct.
- [ ] Merge the released changelog section before publishing the release body.
- [ ] Fill REL-09 with Released, Checked QRs, the testing-plan link and Checked
  UATs, without calling a failed/not-run test passing.
- [ ] Recover planned story points and record actual completed story points;
  task counts and merged PR counts are not velocity.
- [ ] Team triages unfinished issues, preserving priorities; close Sprint 9
  only after review, release and triage.

## Owner-Held Submission Gates

Final report, PDF and ZIP remain on hold at the owner's request. Once authorized,
merge the evidence/report, verify CI on that exact main commit, and use that
same commit for the report permalink and submission snapshot.
Private customer/instructor access and the usability-data deletion plan belong
in the private wrapper, not in public repository files.
