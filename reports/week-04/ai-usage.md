# Week 4 AI Usage

## Scope

The team used OpenCode and Codex during Week 4. AI output was treated as a draft or review aid, not as evidence that a test, Customer meeting or acceptance decision had occurred.

## OpenCode

OpenCode was used to inspect the repository and GitHub project, compare the current state with the Assignment 4 requirements, and help prepare planning, quality-requirement, container-view, functional-requirement and architecture changes. It also supported pull-request review, Project field verification, macOS launcher verification and the maintained setup update in [PR #87](https://github.com/team-ok-ITPD/team-OK-itpd/pull/87).

The team did not retain every generated change. The first functional-requirement contribution in [PR #80](https://github.com/team-ok-ITPD/team-OK-itpd/pull/80) was closed when ownership moved to another member. A separate ADR branch was not merged; the reviewed specification package in [PR #84](https://github.com/team-ok-ITPD/team-OK-itpd/pull/84) became the repository evidence instead. When a status request was initially interpreted as permission to change files, that work was stopped and subsequent stages were confirmed explicitly.

For macOS verification, OpenCode used a clean checkout and recorded observed results rather than inferring them from CI. The product built and ran through the documented Bash workaround, while direct execution of the non-executable `.command` file failed. The repository therefore records both the working product flow and the launcher limitation.

## Codex

Codex inspected the stories, decisions, implementation and course requirements and consolidated the team's requirements and architecture drafts in PR #84. It helped draft the glossary, repository agent instructions, navigation and the previewable issue-conversion tool used before the live Week 4 issue migration. The team reviewed the resulting files and migration behavior before merge and applied a separate correction through [PR #85](https://github.com/team-ok-ITPD/team-OK-itpd/pull/85).

Codex output preserved unresolved requirements rather than treating the current MUP as complete. In particular, remote SSH, invalid-access refusal, shared-service isolation, agent assistance and category browsing remain requirements or planned behavior, not verified current capabilities.

## Review And Verification

AI-assisted changes retained on `main` were reviewed through pull requests by a member other than the author. PR #87 is still awaiting that review, and the closed PR #80 is not treated as accepted evidence. Depending on the affected files, the team used product tests, Docker image and health checks, strict MkDocs builds, Markdown linting, repository link checks and `git diff --check`.

Generated claims were corrected or rejected when they exceeded available evidence. Accepted ADRs describe architectural decisions but do not prove implementation. A checked platform criterion is not presented as command-level evidence when the commands were not recorded. The meeting script is not treated as a held Customer meeting, and no Customer verdict, Week 4 release or sprint velocity is claimed before those events occur.
