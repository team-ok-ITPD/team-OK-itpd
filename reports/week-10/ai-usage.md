# Week 10 AI usage

## 2026-11-28 functional verification

OpenCode (GPT-6.1 Sol) inspected the v2 application, ran automated tests,
performed local browser checks with synthetic demo data, and prepared fixes
and regression tests. The user requested functional testing and bug fixes.

The work corrected private-practice pairing and graded-assignment callback
authorization, including grading during verification on both callback paths.
It also corrected the explanation for manually closed assignments.
An outdated progress test was updated to check that the student's own code
is returned without exposing another student's code. The initial hypothesis
that returning any source was a defect was rejected after inspecting the
student update script; that API behavior was preserved.

The agent used a separate checkout based on `dbb4854`, without modifying the
original checkout's uncommitted usability materials. Changes are prepared for
[task #211](https://github.com/team-ok-ITPD/team-OK-itpd/issues/211) on
`211-v2-functional-fixes` for team review. No review approval, merge or
Customer acceptance is claimed.

See [the functional check record](functional-testing.md) for evidence and
limitations. These agent-driven checks are not human usability sessions,
Customer UAT, or proof that every requirement is met.

## 2026-11-28 local email configuration

At the user's request, OpenCode connected the local development process to
Gmail SMTP using an owner-created, Git-ignored credential file. STARTTLS and
SMTP authentication succeeded without sending a message. The web process
was restarted with account email enabled and the service mailbox as sender;
the login endpoint returned HTTP 200. No secret was printed or committed.
Inbox delivery is not yet verified. Account links currently use the local
development origin and are not a deployed handoff configuration.

At the user's request, OpenCode subsequently prepared plain-text account
invitation and access-link templates, with distinct subjects, role and login
details, expiry guidance and unexpected-message instructions. Creation can
include the administrator-supplied initial password; resend never does.
All 45 administrator tests passed, including template-content assertions.
Three clearly marked test previews were accepted by Gmail SMTP for the
user-designated recipient. They contained no real credentials or usable reset
token, and did not create or change an account. Inbox receipt is not confirmed.
The local web process was restarted to use the templates.

OpenCode later exercised email and CSV workflows with a disposable database
and in-memory mail capture, added regression tests, and corrected the template
selection for CSV password updates of existing accounts. No separate testing
report was created, as requested by the user.

At the user's request, the email/template changes are prepared separately on
`215-account-email-templates` under
[task #215](https://github.com/team-ok-ITPD/team-OK-itpd/issues/215) for
independent team review. SMTP credentials and local environment files are
excluded from the commit; no review approval or deployment is inferred.
