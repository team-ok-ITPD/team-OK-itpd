# Contributing

## Issues and planning

All work starts in an issue. A story describes a user outcome; implementation
is split into task issues, and one pull request closes exactly one task. Assign
the issue to its sprint milestone and to the same two members named by its
`Responsible` and `Accountable` fields.

The team uses the public GitHub Projects table linked from the
[organization's projects page](https://github.com/orgs/team-ok-ITPD/projects) to
see ownership and status across the repository. The table is grouped by
milestone so sprint scope and unscheduled work are visible together. Sprint
backlogs remain visible in the repository's
[milestones](https://github.com/team-ok-ITPD/team-OK-itpd/milestones).

## Branches and commits

Name a branch `<issue-number>-<short-lowercase-description>`, for example
`52-week-03-planning`.

Use Conventional Commits in the form `type: short imperative description`.
Common types are `feat`, `fix`, `docs`, `test`, `ci`, and `chore`. Keep each
commit focused on one coherent change.

## Pull requests

A pull request must target `main`, link exactly one task with `Closes #nn`,
explain what changed and why, state how it was checked, and direct the reviewer
to the risky or requirement-sensitive parts. It also states whether the change
is user-visible and updates `[Unreleased]` when it is.

The accountable reviewer checks the task criteria, scope, tests, documentation,
privacy, and repository checks. They tick every task criterion before approving.
A member other than the author must approve, and the branch merges only through
its pull request after all checks are green.

The complete standard for stories, tasks, and pull requests is the
[Definition of Done](docs/definition-of-done.md).
