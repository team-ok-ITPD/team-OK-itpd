# Week 08 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 8, The Usability Results And The Project Configuration Review

## What we did

We held the Week 8 Sprint Review with the Customer on 2026-11-20, closed the Week 7 action points and open questions in [the meeting report](meeting-report.md), and recorded the nine decisions the meeting made, [DEC-044](../../docs/decisions.md#dec-044) through [DEC-052](../../docs/decisions.md#dec-052).
The Customer kept course management outside Debug GYM, accepted group-specific assignments and deadlines, asked that a submission be accepted even when its tests fail, agreed that the CSV export carries the grade, and found the VS Code test and submit controls hard to discover.
We wrote [the configuration plan](../../docs/configuration-plan.md), which inventories eight `Active` items in the five groups and one `Dropped` item, and [the configuration evaluation](cm-evaluation.md) of the three local goals our artifacts serve.
The evaluation keeps the separate checks, the public environment shape and the nested v2 instructions, adds a v2 test job, merges the two root dependency files and pins the v2 requirements, and replaces the stale layout lines in the root `AGENTS.md`; its first change is the dependency merge, whose tradeoff is more Dependabot pull requests and a rename that touches the Dockerfile, the workflow and the setup guides.
We added the configuration terms to [the glossary](../../docs/glossary.md) and the four configuration risks, [RISK-09](../../docs/risks.md#risk-09) through [RISK-12](../../docs/risks.md#risk-12), to [the risk register](../../docs/risks.md), and planned `SPRINT-08` and `SPRINT-09` in [the project plan](../../docs/project-plan.md#sprint-08).
The focus metric, [solved exercises per active learner per week](../../docs/analytics.md), still has no value, because the deployed analytics backend has no traffic from learners outside the team; no test or smoke traffic is presented as a value.

## Configuration management

The configuration plan is [docs/configuration-plan.md](../../docs/configuration-plan.md), and it inventories eight `Active` items across the five groups, each with its purpose, owner, location, connections and the rule it must meet, plus one `Dropped` item kept in place.
The evaluation judged the configuration at [v0.4.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.4.0), and it is [reports/week-08/cm-evaluation.md](cm-evaluation.md).

The three local goals are catching a regression before a release, reproducing the product safely, and keeping the project context findable.
The team keeps the separate checks and the public environment shape, adds a v2 test job, merges the two root dependency files and pins the v2 requirements, and replaces the root `AGENTS.md` layout and checks lines.

The first change is the dependency merge: one exactly pinned root file, pinned v2 requirements and the v2 directory under Dependabot, whose main tradeoff is more Dependabot pull requests and a rename that touches the Dockerfile, the workflow and the setup guides.
The pinned container build, the separate workflows and the public `.env.example` are kept.
The evaluation also records what the team could not judge, the university VM's backup policy and the GitHub protection settings, with the risk each carries.

No configuration change from the evaluation was enacted this week, and the goal sections and the first change are the review's recommendation rather than scheduled work.

## Week 9 handoff

The Week 9 deck cites [the configuration plan](../../docs/configuration-plan.md) rather than repeating it.
The evaluation's goal sections and its first change are the review's recommendation and schedule no work for Week 9.
The private usability-data repository and the recordings folder stay open until the course is graded, and the final repository state is the `main` commit that the Week 9 submission takes its permalink from.
The Week 9 deck also reflects on the work the Customer set for the next review in [the meeting report](meeting-report.md#action-points): the group and assignment requirements, the submission acceptance fix, the CSV export sample, the extension usage guide, the project ZIP and Dockerfile rules, and the AI provider confirmation.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan | [docs/project-plan.md](../../docs/project-plan.md#sprint-08) |
| Configuration management | [the configuration management section](#configuration-management) |
| Glossary | [docs/glossary.md](../../docs/glossary.md) |
| Risk register | [docs/risks.md](../../docs/risks.md) |
| AI usage | [reports/week-08/ai-usage.md](ai-usage.md) |
| Week 7 action points | [reports/week-08/meeting-report.md](meeting-report.md#previous-action-points) |
| Week 7 open questions | [reports/week-08/meeting-report.md](meeting-report.md#previous-open-questions) |
| Sprint Review | [reports/week-08/meeting-report.md](meeting-report.md) |
| Meeting script | [reports/week-08/meeting-script.md](meeting-script.md) |
| Week 9 handoff | [reports/week-08/README.md#week-9-handoff](#week-9-handoff) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@adelazzi](https://github.com/adelazzi) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aadelazzi), [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aadelazzi), and the moderator of the Week 8 Sprint Review in [the script](meeting-script.md#roles). |
| [@Danashi11](https://github.com/Danashi11) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3ADanashi11), [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3ADanashi11), and the note taker of the Week 8 Sprint Review in [the script](meeting-script.md#roles). |
| [@qwxiae](https://github.com/qwxiae) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aqwxiae), [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aqwxiae), and the observer of the Week 8 Sprint Review in [the script](meeting-script.md#roles). |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3AUTKANOS-RIBA), [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3AUTKANOS-RIBA), and the technical presenter of the Week 8 Sprint Review in [the script](meeting-script.md#roles). |

## Repository evidence

The latest runs on `main` are listed for the [product checks](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/product.yml?query=branch%3Amain), the [link check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/lychee.yml?query=branch%3Amain), the [Markdown check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/markdown.yml?query=branch%3Amain), [actionlint](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/actionlint.yml?query=branch%3Amain) and the [documentation build](https://github.com/team-ok-ITPD/team-OK-itpd/actions/workflows/pages.yml?query=branch%3Amain).

The link check excludes only the private usability-data repository, because opening it needs authenticated course access; the exclusion and its reason are in `.lycheeignore`.

## Deviations

- The Week 8 Sprint Review on 2026-11-20 presented the product workflows and did not present sanitized usability results or a `QR/QRT` result, and it did not establish that the `UT-01` design or a session plan was agreed. [The meeting report](meeting-report.md#previous-action-points) carries that action point into Week 9.
- [The meeting script](meeting-script.md) was written as a `UT-01` design and execution review, but the meeting covered the product workflows, so the script's agenda and the report's `Presented` line differ.
- Two Week 6 action points, on the submission-container lifecycle and the upload limit, were not re-listed by the Week 7 report; [the meeting report](meeting-report.md#previous-action-points) closes them here and carries them forward.
- No configuration change from the evaluation was enacted this week.

## Privacy

No private-only material was committed to this repository, and no participant identity was committed to it.
