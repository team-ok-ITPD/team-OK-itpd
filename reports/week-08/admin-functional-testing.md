# Administrator Functional Testing

## Scope And Environment

- Date: 2026-11-20.
- Task: [#189](https://github.com/team-ok-ITPD/team-OK-itpd/issues/189).
- Base: `f8e4d91`; implementation branch: `189-admin-provisioning`.
- Local macOS, Python 3.12, Django 5.2.19, SQLite; OpenCode browser.
- Browser data: synthetic `UI Smoke` accounts and group in the separate local
  `startup-demo.sqlite3`. The original `db.sqlite3` was not reset.
- This is developer functional evidence, not Customer acceptance or a UT-01
  participant session. No production service was modified.

## Observed Results

| Scenario | Method | Result |
| --- | --- | --- |
| Create teacher, student and administrator accounts | Django tests; browser form submissions for all three roles | Passed |
| Passwords are hashed; submitted role cannot override route role | Django tests | Passed |
| Teacher edit retains role and unchanged password | Django tests | Passed |
| Teacher deactivation blocks subsequent authenticated access | Django tests | Passed |
| Invalid email, duplicate email ignoring case, short/mismatched passwords | Django tests; mismatched administrator passwords also in browser | Passed; visible form errors |
| Create a group with one active teacher | Django tests; browser | Passed |
| Reassign a group's teacher | Django tests; browser | Passed; browser showed the newly created teacher |
| Preserve membership and assignment/exercise ownership on teacher change | Django tests | Passed |
| Add and remove a student | Django tests; browser, including removal confirmation | Passed |
| Reject duplicate/inactive students and non-student members | Django tests | Passed |
| Reject inactive/non-teacher group teachers | Django tests | Passed |
| Group-scoped removal and POST-only membership changes | Django tests | Passed |
| Anonymous and non-admin direct-page/mutation access | Django tests | Passed |
| CSRF protection on account/group creation | Django client with CSRF checks enabled | Passed |
| Role-scoped account search and 20-item pagination | Django tests | Passed |
| Group/teacher/assignment search and no-match states | Django tests | Passed |
| Assignment list/detail remain read-only | Django tests | Passed |
| Dashboard sections do not touch | Browser computed geometry | Passed; 22.5px gaps between successive sections |
| Dashboard action buttons and wider card layout | CSS inspection and desktop browser | Page-scoped flex cards with bottom-aligned actions |
| Mobile-width visual layout | Not completed | Embedded-page probe was blocked by browser security; no security settings were changed |
| Browser console after membership removal | Browser error log | No errors |

## Automated Checks

From `app/v2/debug_gym/`:

```sh
.venv/bin/python manage.py test admin_panel accounts core
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python manage.py test
```

- Focused administrator/accounts/core suite: 62 tests passed, including
  23 administrator tests.
- Migration drift: no changes detected.
- Full v2 suite: 168 tests, 166 passed, one failure and one error:
  - `professor.tests.TeachingWorkflowTests.test_fake_student_test_counts_are_not_saved`:
    expected submission does not exist.
  - `professor.tests.TeachingWorkflowTests.test_student_can_submit_without_deadline_until_manual_closure`:
    expected one submission, found zero.
- The full suite creates and migrates a fresh test database successfully.
  The separate browser demo database also migrated successfully.
- Repository `python -m pytest -q` using the v2 virtual environment:
  11 product tests passed.
- Repository-wide Markdown lint: four errors in unchanged `README.md`
  lines 101–103 (blank lines, trailing space and heading spacing).
  Lint on changed Markdown files is checked separately.
- `git diff --check`: passed.

## Review Limits And Follow-up

### Account Editing Follow-up

The user subsequently requested student and administrator editing. The expanded
`admin_panel accounts core` suite passes 67 tests, including 28 administrator
tests. Added coverage verifies list edit links, role-scoped GET/POST access,
name/email changes, password replacement and preservation, deactivation,
duplicate emails, password mismatch, role-injection rejection, CSRF protection,
self-deactivation rejection and retaining the current session after an
administrator changes their own password. The earlier full-suite counts above
remain the earlier run, not a claim that the expanded full suite was rerun.
Browser follow-up also saved name changes for the synthetic student and
administrator accounts, observed both success messages, and verified the
administrator list's Edit link opens the matching account form.

- Do not merge based only on the focused suite: the full-suite failures need
  team triage, and mobile visual testing is still outstanding.
- The older local database has a schema mismatch involving `groups.is_archived`.
  It was preserved, not repaired or replaced by the test run.
- The migration fix changes a dependency of an existing migration to eliminate
  duplicate fields. A deployment that already applied the project-fields
  migration without the test-results migration needs a migration-history audit
  before applying this branch. No production-history repair was attempted.
- FR-008/FR-010 describe related older-catalog boundaries, not a complete v2
  administrator specification. New permissions follow the explicit development
  request, not an invented Customer decision.
- Independent review is requested; acceptance boxes in #189 remain for the
  reviewer to verify and tick.
