# Week 8 AI Usage

## Tools

- On 2026-11-28, the team reconfirmed that P-01, P-02 and P-03 were real
  human sessions. OpenCode corrected its mistaken conflation of P-03 with a
  [separate technical rehearsal](../week-10/technical-rehearsal.md).
  AI assistance prepared and checked the documentation; it did not replace
  any participant in those sessions. The publication is prepared under
  [task #213](https://github.com/team-ok-ITPD/team-OK-itpd/issues/213);
  review and acceptance remain pending.

- On 2026-11-27, OpenCode (GPT-6.1 Sol) prepared a late usability supplement
  from three team-supplied session-result files and the team's clarification
  of dates and consent. These inputs contained participant
  background details; they were not pre-sanitized public notes. No raw recording
  was supplied to the agent. The agent removed demographic combinations, quotations,
  addresses and raw survey answers from the public summaries, recalculated
  individual SUS scores and documented the shortfall without aggregates.
  UT-01 remains Planned and QR-07 Not verified. No private repository access,
  recording, telemetry, Customer acceptance or product fix was verified.
  The team must review publication consent and remove private input copies
  from tools under the course retention policy. AI helped structure the record;
  it did not conduct the human sessions or supply missing measurements.
  In a follow-up, the team reported personal instructor approval of a
  recording-requirement exception. OpenCode removed recording-based exclusion
  claims while retaining the independently documented protocol limitations.

- OpenCode prepared the #193 commit and pull request at the user's request,
  updated task scope and sprint/project metadata, and requested independent
  review from the three non-author repository collaborators. Review requests
  do not constitute approval or Customer acceptance.
- OpenCode fetched `origin/main` on 2026-11-22 and verified that both it and the
  working branch were based on `41c9dd87b04ee37d9a8b08f5a0aae45ebd3a5a7d`;
  no merge or stash operation was needed and existing local work was preserved.
  Two professor tests still posted code to the IDE-launch page; they now use
  the actual token-authenticated submission endpoints, retaining closure and
  trusted-verification assertions. Added cross-role regressions for admin-created
  accounts, teacher assignments, student submissions, deadline-gated teacher
  results, membership removal/re-enrollment and revocation of web sessions and
  both IDE token types. External verification is mocked, not live evidence.
  Removed duplicated IDE image configuration while preserving its effective
  default and made both launchers honor the configured workspace root.
  Docker was unavailable, so real container launch, live AI and SMTP delivery
  remain unverified. No standalone testing report was created.
  Final checks passed: 190 Django tests, 11 root product tests, migration-drift
  check, strict MkDocs build, repository Markdown lint and `git diff --check`.
  Git reported no unmerged files.
- OpenCode simplified the selection counter to the total selected only, keeping
  off-page selections included in that total and in bulk actions.
- OpenCode verified the counters end to end using a disposable 45-student
  database: three selected on page one plus student 45 on page two yielded
  `4 selected / 1 outside` on page one and `4 selected / 3 outside` when
  searching for student 45. A confirmed test deactivation affected all four,
  then reset selection to zero. The working demo database was not modified.
  Added a regression test for 45 total students, 30/15 pagination and off-page
  bulk processing.
- OpenCode added automatic student-search reset when an applied query is
  cleared; the explicit group filter and persisted student selection remain.
- OpenCode changed student pagination to 30 per page at the user's request;
  pagination for other account roles remains unchanged.
- OpenCode retained 20-account pagination and implemented tab/account-scoped
  student selection across search, filters and pagination, with an off-page
  counter, explicit clear, confirmation count and reset after successful actions.
  Search remains explicit; large-dataset performance has not been benchmarked.
  Browser checks verified selection across two searches, restoration, submitted
  off-page IDs, confirmation count and clear; the action was cancelled.
  The administrator/accounts/core suite passed 80 tests.
- OpenCode made the bulk-action target group initially empty and reset after
  submission, without displaying a blank dropdown item. Group membership
  actions still require an explicit group selection.
- OpenCode removed the empty bulk-action group option and hid/disabled the
  target group for activation/deactivation. Server validation ignores submitted
  groups for these actions; regression tests cover status and membership safety.
- OpenCode versioned the shared CSS and JavaScript URLs to refresh stale
  browser assets. Browser checks on the actual student bulk-action and account
  deletion pages verified the styled dialog and equal button vertical positions;
  the confirmation was cancelled and no account was deleted.
- OpenCode removed automatic target-group filtering after student bulk actions,
  retained explicit list filters, aligned deletion actions horizontally and
  replaced browser confirmations with a keyboard-accessible native dialog.
- OpenCode restyled the CSV import confirmation as an inline, clickable
  checkbox row with token-based checked and keyboard-focus states.
- OpenCode prepared a synthetic 10-student import CSV and verified the exact
  file in a disposable database: creation, password checks, repeat-import
  idempotency and rollback on invalid input. The administrator suite passed
  all 37 tests; the running demo database was not changed by these checks.
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

OpenCode removed the empty teacher option from existing-group edit forms at the
user's request, retaining required-field validation for tampered empty requests.

On 2026-11-22 the user clarified that the existing Name field represents the
course and a separate group number is needed. OpenCode added a text group-number
field, a non-destructive migration, form/database duplicate checks, combined
display labels and course/number-aware CSV enrollment. Existing names and
descriptions were preserved and legacy numbers were left blank, not fabricated.
Historical Customer decisions were not edited.
The migration preserved all three pre-existing groups in the local demo database.
Browser checks created and edited a synthetic numbered group, retaining leading
zeroes. The focused administrator/accounts/core suite passed 76 tests. The full
suite passed 180 of 182; the same two previously recorded professor submission
failures remain outside this change.

OpenCode synchronized merged PR #195 while preserving the local administrator
work. It made group rows clickable, replaced separate teacher-search input with
a keyboard-accessible searchable dropdown, and combined student filters and
batch actions in a compact responsive toolbar with inset select arrows. The
user's group-number/course-field wording needs clarification before schema
changes; technical implementation notes were removed from the group form.

At the user's explicit follow-up request, OpenCode added the administrator-set
initial password to enabled account-creation emails for all three roles and
CSV-created students. Original password text is passed only from the creation
request; only hashes are stored. Link-only creation without a password,
manual resend and password-update messages retain their earlier behavior.
Regression coverage checks delivery content, login with the initial password,
disabled/inactive/invalid accounts, generic delivery-failure warnings, refusal
to print credentials and no duplicate email on repeated CSV imports.

OpenCode removed the student-list explanatory paragraph, retaining a compact
count badge, and made Cancel right-aligned with the same secondary style as
access email. The password edit field is explicitly labelled New password;
stored passwords remain irreversible hashes and are not displayed.

OpenCode made newly entered administrator-managed passwords visible by default,
without redisplaying saved hashes or submitted passwords. It grouped edit actions
beside Save/Cancel while retaining a separate CSRF-protected form for access
email, and aligned account filters and student batch controls in responsive grids.

On 2026-11-21, OpenCode implemented task #193 using the merged Week 8 transcript:
central student membership/batch management, atomic student/group CSV import,
removal of administrator assignment/group-member pages, teacher lookup,
single-field password entry and guarded account deletion. It added optional
one-time access-link email, keeping passwords hashed and refusing token logging,
and revoked web/IDE credentials on deactivation. DEC-044 storage was preserved;
separate-course-field and data-retention policy need confirmation. Actual SMTP
delivery requires owner configuration and is not claimed as verified.

OpenCode inspected PR #190's failed CI logs and corrected README whitespace.
It replaced three administrator template URL interpolations with Django's
named URL tag so the static link checker no longer treats runtime values as
missing files. Link-check exclusions and required-check policies were not weakened.

OpenCode removed the Exercise column from the administrator assignment list at
the user's request, retaining exercise information in assignment details and
adding regression assertions for both views.

OpenCode removed the dashboard's introductory provisioning sentence at the
user's request.

OpenCode added student/administrator editing at the user's request, including
role-scoped URLs, list actions, password preservation/reset, self-deactivation
protection and session refresh after changing one's own administrator password.
Regression tests cover editing, role injection, invalid data, authorization,
CSRF and self-account handling.

OpenCode added the shared stack layout between assignment-detail sections after
the user reported that the instructions card touched the context cards.

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
