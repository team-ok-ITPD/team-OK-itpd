# Week 04 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 4, Quality, Requirements, Architecture, And The Fourth Release
- **Release:** `REL-04`, published as
  [v0.2.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.2.0)
  on 2026-10-25.

Our problem-space sentence: a developer who wants to practise debugging needs
one place where a realistic, multi-file exercise is generated, run with real
debugging tools, and checked against the intended bug, and no product carries
all three in one flow.

## Summary

The team wrote five quality requirements and seven functional requirements,
drew the container view, recorded three accepted architectural decisions, and
linked the drivers to them in one architecture document. It also wrote the
glossary and the team's `AGENTS.md`, brought the Week 2 and Week 3 issues to the
Week 4 shape, and released `REL-04` as `v0.2.0`.

`SPRINT-04` planned `22SP` (`US-01` 3, `US-02` 5, `US-03` 3, `US-04` 3, `US-05` 8)
and completed `0SP`: no story closed, so `US-01` through `US-05` moved to
`SPRINT-05`. `US-06` (8) and `US-07` (5) are estimated and wait in the product
backlog. The testability requirement
[QR-03](../../docs/quality-requirements/qr/QR-03.md) and the stack decision
[ADR-001](../../docs/architecture/adr/ADR-001.md) are what the rest of the
architecture rests on. The requirements still carry proposed targets that the
Customer has not reviewed, and remote SSH, invalid-access refusal, shared-service
isolation, assistance and category browsing remain required but unimplemented.

## Customer Meeting Outcome

The meeting on 2026-10-26 showed the web prototype of the learner flow, not the
containerized workspace. No story was shown against its `AC-nn`, so the Customer
neither accepted nor rejected `US-01` through `US-05`; all five stay open and no
acceptance is inferred from team verification. No candidate story moved out of
the minimum usable product.

The Customer changed the product in five decisions: the default tests are
read-only ([`DEC-011`](../../docs/decisions.md#dec-011)), the product is for
desktop users ([`DEC-012`](../../docs/decisions.md#dec-012)), opening an exercise
in VS Code is a Must Have ([`DEC-013`](../../docs/decisions.md#dec-013)),
solutions are submitted from VS Code
([`DEC-014`](../../docs/decisions.md#dec-014)), and search covers prepared
exercises only ([`DEC-015`](../../docs/decisions.md#dec-015)).

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and estimates | [docs/project-plan.md](../../docs/project-plan.md#sprint-04) |
| Product backlog refinement | [the project's table view](https://github.com/orgs/team-ok-ITPD/projects/1) grouped by `Milestone`; its group with no milestone is the product backlog |
| Issue catch-up | [issues of the `User Story` type](https://github.com/team-ok-ITPD/team-OK-itpd/issues?q=type%3A%22User+Story%22) and [issues of the `Task` type](https://github.com/team-ok-ITPD/team-OK-itpd/issues?q=type%3ATask) |
| Quality requirements | [docs/quality-requirements/qr/](../../docs/quality-requirements/qr/), with [docs/quality-requirements/README.md](../../docs/quality-requirements/README.md) as the priority matrix |
| Functional requirements | [docs/functional-requirements/](../../docs/functional-requirements/), with [README.md](../../docs/functional-requirements/README.md) as the index and [fr/](../../docs/functional-requirements/fr/) for the records |
| Container view | [docs/architecture/README.md#container-view](../../docs/architecture/README.md#container-view), its image [container.svg](../../docs/architecture/container.svg) and source [container.mmd](../../docs/architecture/container.mmd), and [#container-responsibilities](../../docs/architecture/README.md#container-responsibilities) |
| Architecture and drivers | [docs/architecture/README.md](../../docs/architecture/README.md), with [its drivers](../../docs/architecture/README.md#drivers) and [the ADR index](../../docs/architecture/README.md#architectural-decisions) |
| Architectural decisions | [docs/architecture/adr/](../../docs/architecture/adr/) and [the ADR index](../../docs/architecture/README.md#architectural-decisions) |
| Glossary | [docs/glossary.md](../../docs/glossary.md) |
| Team `AGENTS.md` | [AGENTS.md](../../AGENTS.md) |
| Issue fields in the project view | [the project's table view](https://github.com/orgs/team-ok-ITPD/projects/1) with `Responsible`, `Accountable`, `MoSCoW`, `Story Points`, and `Priority` beside the `Assignees` and `Milestone` columns |
| Documentation site | [the published site](https://team-ok-itpd.github.io/team-OK-itpd/) |
| Week 3 action points | [reports/week-04/meeting-report.md#previous-action-points](meeting-report.md#previous-action-points) |
| Week 3 open questions | [reports/week-04/meeting-report.md#previous-open-questions](meeting-report.md#previous-open-questions) |
| Meeting script | [reports/week-04/meeting-script.md](meeting-script.md) |
| Customer validation | [reports/week-04/meeting-report.md](meeting-report.md), [reports/week-04/meeting-transcript.md](meeting-transcript.md), and no story verdict, because no story was shown |
| `REL-04` | [v0.2.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.2.0), [the changelog's released section](../../CHANGELOG.md), and [the plan's `REL-04` line](../../docs/project-plan.md#rel-04) |
| Sprint retrospective | [reports/week-04/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-04/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@adelazzi](https://github.com/adelazzi) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aadelazzi), [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aadelazzi), and the questions asked at the Customer meeting, see [the transcript](meeting-transcript.md). |
| [@Danashi11](https://github.com/Danashi11) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3ADanashi11), [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3ADanashi11), the [v0.2.0 release](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.2.0), and the notes at the Customer meeting. |
| [@qwxiae](https://github.com/qwxiae) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aqwxiae) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aqwxiae). |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3AUTKANOS-RIBA) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3AUTKANOS-RIBA). |

The specification package is [PR #84](https://github.com/team-ok-ITPD/team-OK-itpd/pull/84), with a correction in [PR #85](https://github.com/team-ok-ITPD/team-OK-itpd/pull/85) and the setup update in [PR #87](https://github.com/team-ok-ITPD/team-OK-itpd/pull/87).

## Repository Evidence

- [PR #84](https://github.com/team-ok-ITPD/team-OK-itpd/pull/84) merged the specification package, and the functional-requirements task it served is [issue #74](https://github.com/team-ok-ITPD/team-OK-itpd/issues/74).
- The latest `main` runs of the [link check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/lychee.yml?query=branch%3Amain) and the [Markdown check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/markdown.yml?query=branch%3Amain) are green.

## Deviations

- The Customer meeting was held on 2026-10-26, after the sprint's due date of
  2026-10-24, and `REL-04` was cut on 2026-10-25, before it, and GitHub marks
  `v0.2.0` as a pre-release. The release does not carry the meeting's decisions,
  which are recorded for `SPRINT-05`.
- The Customer was shown the web prototype and not the containerized workspace,
  so no story has a verdict and no `DEC-nnn` records one. The action to show the
  workspace against `US-01` through `US-05` is in
  [the meeting report](meeting-report.md#action-points).
- `Actual Velocity` is `0SP` because no story closed; the team's verification of
  the five stories is not Customer acceptance.
- [PR #87](https://github.com/team-ok-ITPD/team-OK-itpd/pull/87) was still
  awaiting review when this report was written.

## Privacy

No private-only material was committed to this repository.