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
