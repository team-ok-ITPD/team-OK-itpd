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

## Codex Exercise Page

On 2026-10-31 Codex removed the browser source editor and interactive preview console, retained test output and actions, and changed manual runs/submissions to read the current server draft. It checked page contracts and saved-code behavior; editing remains in VS Code.

## Codex Live Submission Results

On 2026-10-31 Codex added an authenticated progress snapshot, atomic IDE submission/draft updates and serial page synchronization with automatic test runs. It added backend isolation/rollback checks and frontend lifecycle tests, and rehearsed a submission on an isolated local fixture rather than changing the requester's solution.
