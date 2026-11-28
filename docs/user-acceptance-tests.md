# User acceptance tests

## The Tests

**Record status:** Retrospective draft from the Sprint 9 recording, not evidence
that these definitions or identifiers were agreed before the review.
No earlier UAT record was found in the inspected checkout. The team must recover
the original definitions/numbering if they exist elsewhere and reconcile this
draft before submission.

The observations below are sourced to the
[Sprint 9 report](../reports/week-09/meeting-report.md#user-acceptance-tests)
and [sanitized evidence notes](../reports/week-09/meeting-notes.md#acceptance-tests-and-deployment).
Reviewed build, runner attribution and member-verified DEC entries remain
incomplete. Current `main` is not substituted for the unknown reviewed build.

| Test | Journey | Status | SPRINT-09 | SPRINT-10 |
| --- | --- | --- | --- | --- |
| [UAT-01](#uat-01) | Administrator creates a professor account that can sign in. | Active | Observed success; formal result pending original-test/build/DEC verification. | Not run yet. |
| [UAT-02](#uat-02) | Student generates, fixes and submits a debugging exercise. | Active | Explicit Pass statement; formal record pending original-test/build/DEC verification. | Not run yet. |
| [UAT-03](#uat-03) | Professor assigns an exercise, student submits, professor exports results. | Active | Observed assignment failure; complete fresh run not established. | Not run yet. |

Access details, provider credentials and deployment addresses belong in the
private Moodle wrapper, not this record.

## UAT-01

An administrator creates a professor account and the professor signs in.

**Status:** Active

**Start state:** Synthetic administrator access on `<production-url>`, a fresh
test email controlled by the team, and an agreed account invitation/credential
flow. This is a retrospective candidate start state, not a claim of recorded
pre-review preparation.

**Steps:**

1. Sign in as the administrator and create the professor account.
2. Complete the agreed invitation or initial-credential step.
3. Sign out and sign in as that professor.

**Expected result:** The account has the professor role and can access its own
professor dashboard. It does not acquire administrator permissions.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| --- | --- | --- | --- | --- | --- | --- |
| SPRINT-09 | 2026-11-28 | Team | Not established | Observed successful creation/sign-in; formal classification pending. Cross-role denial was not shown in this final check. | [Review](../reports/week-09/meeting-report.md#user-acceptance-tests), 01:22:59–01:24:42 | Member verification pending. |

If the original administrator UAT also required student/group creation, retain
those criteria and verify coverage rather than narrowing the test after the run.
The final invitation preference differs from the initial-password demonstration.

## UAT-02

A student generates a private debugging exercise, corrects it and submits a
solution with a recorded result.

**Status:** Active

**Start state:** Synthetic student access on `<production-url>`, a privately
configured working generation provider, and a supported VS Code connection.
The exact original start state still requires team confirmation.

**Steps:**

1. Generate a private exercise from a suitable prompt.
2. Open the exercise in VS Code and reproduce its failing behavior.
3. Correct the code, run tests and submit the attempt.
4. Return to the website and inspect the saved attempt/result.

**Expected result:** The generated exercise is available only to the student,
the correction can be submitted, and the result appears on the website.
If the original test requires a particular return button or hidden-test
guarantee, preserve and check that requirement separately.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| --- | --- | --- | --- | --- | --- | --- |
| SPRINT-09 | 2026-11-28 | Team | Not established | Customer calls the demonstrated UAT a Pass; formal record pending original-test mapping. | [Review](../reports/week-09/meeting-report.md#user-acceptance-tests), demonstration 01:10:27–01:19:38; judgment 01:22:37–01:22:58 | Member verification pending. |

The return-to-site button was reported to fail with an authentication/403 issue
at 01:17:29–01:18:03. Do not remove that defect from the record or claim it was
fixed because later navigation succeeded. Local/browser submission demonstrations
also occur at 00:39:39–00:49:39, but do not prove SSH acceptance.

## UAT-03

A professor creates an exercise, assigns it to a group, a student submits, and
the professor exports the group's result.

**Status:** Active

**Start state:** Synthetic professor/student accounts on `<production-url>`,
administrator-managed membership in the professor's test group, and a fresh
exercise. Confirm whether the original test specifically requires AI generation.

**Steps:**

1. Create the exercise by the originally agreed method.
2. Assign it to the test group and confirm student visibility.
3. Submit an attempt as a member of that group.
4. Close the assignment or wait until the agreed results boundary.
5. Inspect results and download the CSV as the group's professor.

**Expected result:** A fresh assignment reaches the correct students and the
professor can obtain the resulting submission/test information without relying
on pre-existing demo results.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| --- | --- | --- | --- | --- | --- | --- |
| SPRINT-09 | 2026-11-28 | Team | Not established | Assignment step failed; fresh end-to-end run incomplete. Formal Fail/Not run mapping requires the original definition. | [Review](../reports/week-09/meeting-report.md#user-acceptance-tests), failed attempt 01:02:32–01:05:28; scope/results discussion 01:24:44–01:26:25 | Member verification pending. |

Student AI generation does not establish professor generation. Exporting an
older seeded assignment does not substitute for this fresh run. Preserve the
failed attempt and distinguish any unexecuted generation step from an observed
provider failure. Re-run the complete agreed journey at handoff.
