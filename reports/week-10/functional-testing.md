# Local v2 functional checks

**Date:** 2026-11-28.
**Baseline:** `dbb4854247a07947883b7f5287b4faae79582d2c`, with local fixes.
**Environment:** macOS, Django development server, SQLite, Docker Desktop,
and the OpenCode Chromium browser. This is not staging or Customer UAT.

## Observed browser checks

Synthetic demo accounts and a specifically created Functional QA exercise,
assignment and student were used in this separate checkout.
No original learner volume was reset.

| Scenario | Observed result |
| --- | --- |
| Demo sign-in and sign-out for all three roles | Expected role dashboard and return to login |
| Administrator creates and searches for a student | Account created and search returns the account |
| Administrator deactivates selected student | Confirmation shown; account becomes inactive |
| Professor imports a two-file Python ZIP | Exercise created with its source and tests |
| Professor publishes and assigns it to a group | Exercise published; assignment appears for the student |
| Student starts browser VS Code | Workspace opens with `main.py`, tests and the extension |
| Extension Test on original code | One failed and one passed |
| Extension Submit on unchanged code | Rejected as unchanged |
| Test after fixing the disposable exercise file | Two passed |
| Extension Submit on corrected code | Server verification reports 2/2; attempt saved |
| Website result refresh | Submitted status, 2/2 and own source appear without reload |
| Student requests administrator/professor pages | HTTP 403 |
| Student requests nonexistent assignment | HTTP 404 |
| Professor closes the test assignment | Results become visible, including 2/2 |
| Professor exports CSV | HTTP 200; correct counts and students with no submissions |
| Extension submits after closure | Submission rejected |

The exercise-file correction was applied to the disposable QA workspace on
disk, not typed through Monaco. Some browser form submissions used the DOM
form API after pointer-coordinate failures in the browser tooling; those
checks establish the form/server flow, not reliable pointer interaction on
every control.

Docker CLI worked initially, but Python's Docker SDK required `DOCKER_HOST`
to point at the active Docker Desktop socket. The development process was
restarted with that environment setting and explicit locally built IDE images.
No `.env` or credential file was changed.

## Regressions addressed

- Own private practice was visible on the website but rejected by the scoped
  pairing API. Access now includes the owning student, not other students.
- Scoped workspace tokens bypassed the website's graded-attempt lock.
  Authorization now uses the same best-attempt ranking as the website and
  rechecks the lock after verification.
- The older student callback also accepted a submission if grading occurred
  during verification. Its transaction now rechecks grading and assignment
  withdrawal, exercise identity and membership.
- Manual closure incorrectly produced a deadline-expired explanation.
  The message now distinguishes manual closure from deadline expiry.
- An existing progress test contradicted the live own-source preview.
  Its replacement checks own-source visibility and other-student isolation.

## Automated verification

Run from `app/v2/debug_gym`:

```sh
python manage.py test --noinput
```

The baseline discovered 248 tests: one failed and one was skipped.
The final run discovered **254 tests: 253 passed, one skipped**.
The skipped Linux relay check requires `127.0.0.2`, unavailable on this Mac.
Changed Markdown passed markdownlint (three files); `git diff --check` passed.

Root `python -m pytest -q`: **11 passed**.
The first grading/private-pairing regression tests failed before their fixes.
The grading-during-verification regression on the older callback also failed
before its fix.

## Limits and follow-up

- External AI requests, email delivery, university deployment, SSH and real
  local-desktop VS Code interaction were not verified.
- No live provider API key was used; agent-related automated tests use mocks.
- A full security audit, load test and cross-browser matrix were not performed.
- The root Compose launcher still starts the old catalog. This is an existing
  setup mismatch, not a launch path for v2; a unified v2 launcher remains a
  follow-up candidate.
- The student page loads two progress pollers. Consolidating them remains a
  resource-efficiency candidate, not part of the authorization fixes.
- [Task #211](https://github.com/team-ok-ITPD/team-OK-itpd/issues/211) and branch
  `211-v2-functional-fixes` carry the fixes for team review. Approval and merge
  remain pending.
