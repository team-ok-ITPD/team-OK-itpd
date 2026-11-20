# Week 8 AI Usage

## Tools

- Codex implemented and tested the local v2 professor group, catalog,
  assignment, result export and project import workflows, browser VS Code
  authoring, server verification, generation integration, encrypted personal
  keys and one-time scheduled submission review.
- Codex refreshed the professor interface using the shared design tokens.
  A disposable Docker rehearsal checked author saves, student submission,
  result refresh and CSV. Provider responses were mocked because a live API
  key is not configured; visual browser inspection was unavailable.
- Codex added owner-only unpublication and independent private copies when
  assigning another author's public exercise, with source links and regression
  checks for ownership, copied project contents and transaction rollback.
- OpenCode reviewed the v2 administrator workflows, the role-access record and
  the course rule router before making changes.
- OpenCode implemented and tested administrator account, membership and
  read-only assignment-view improvements, including inactive-account access
  enforcement and form accessibility fixes.

## Review And Use

OpenCode aligned the group teacher and student-enrollment cards in two equal
columns with matching heights and bottom-aligned compact actions, stacking them
on narrow screens, following the user's layout feedback.

OpenCode corrected stretching on the group-membership page after a user
screenshot: the teacher/student controls align to their content, action buttons
use their natural width, and the roster occupies a separate full-width row.

At the user's follow-up request, OpenCode made all five administrator dashboard
card actions use the shared primary button style instead of highlighting only
teacher management.

OpenCode expanded administrator functional coverage to 23 tests and recorded
browser and automated evidence in
[Administrator Functional Testing](admin-functional-testing.md). It created
task #189 and prepared the corresponding PR for independent team review.
The complete v2 suite still has two professor/student integration failures;
mobile visual inspection remains incomplete. Neither limitation is represented
as a passed check.

OpenCode adjusted the administrator dashboard after the user reported touching
cards: page-scoped section gaps, wider responsive action cards, wrapping
navigation and bottom-aligned buttons use existing design tokens.

OpenCode updated the checkout to `f8e4d91` and implemented the user's requested
administrator provisioning of students, administrators and groups, plus teacher
assignment. It preserved the one-teacher-per-group model and existing student
membership operations. The server fixes roles per creation route and rejects
non-admin access, duplicate emails ignoring case, invalid passwords, and
non-teacher or inactive group teachers.

Verification: all 17 administrator tests passed, migration-drift detection
reported no changes, and the full Django suite passed 160 of 162 tests. The
remaining professor tests fail when expecting student submissions to be
created (`test_fake_student_test_counts_are_not_saved` and
`test_student_can_submit_without_deadline_until_manual_closure`).
In the browser, OpenCode signed in as the demo administrator, created
`UI Smoke Student` and `UI Smoke Group`, assigned the demo professor and
enrolled the new student. These synthetic records are in the separate local
`startup-demo.sqlite3`; the original database was not reset. The updated demo
database migrated successfully, including the independent exercise-test branch.
This is implementation/testing evidence, not Customer acceptance.

OpenCode diagnosed overlapping v2 migrations after updating the local checkout.
It ordered the test-result migration before the project-fields migration,
removed duplicate field creation and reconciled the constraint name. Verification
results: local migration application and migration-drift checks passed. The
Django suite ran 126 tests, with two errors for a missing `test_result` property
and two failures in student test-result handling; those are outside this
migration fix. No Customer decision was made.

The team must review the generated implementation before merge. This assistance
did not make Customer decisions; unresolved administrator permissions remain
open until the Customer confirms them.
