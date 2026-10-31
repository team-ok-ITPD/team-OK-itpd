# Week 5 AI Usage

## OpenCode

The team used OpenCode to inspect the repository and GitHub state, compare the
work against Assignment 5, and decompose the remaining work into reviewed pull
requests. It helped draft the CI changes, quality-requirement tests, testing
plan, sprint plan, deployment runbook, feature documentation, retrospective
and weekly-report structure.

The team retained changes only after checking them against the course rules and
the repository. It rejected the suggestion to reopen `US-01` through `US-05`
because the Customer had reviewed the implementation and the team records the
stories as completed. It also rejected implementing all new roles, groups and
deadline requirements in Week 5; those outcomes became new backlog work.

OpenCode ran the existing Python and Node.js tests where the local environment
supported them, Markdown linting and `git diff --check`. The Django suite was
left to the Python 3.12 CI environment because the available local Python 3.9
cannot install Django 5.2. AI output was not treated as evidence of a CI run,
Customer decision, deployment or release.

## Review And Use

Every retained change was put in a task-specific pull request and the other
three team members were requested as reviewers. At least one teammate must
approve before merge. Generated text was edited to avoid claiming a university
VM deployment or a passing isolation test that had not occurred.

## Codex Roles And Access Documentation

On 2026-10-31 Codex compared DEC-017 through DEC-022 and DEC-026 with the current Django implementation, drafted the role profiles, capability matrix and access constraints, and linked them into maintained documentation. Proposed enforcement and unresolved policy are labelled separately from confirmed decisions. This contribution does not implement role/group management or change Customer verdicts. The requester also asked Codex to start the current local application.
