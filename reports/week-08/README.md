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

## Usability test

**Late supplement, 2026-11-27:** After the 2026-11-21 deadline, the team
provided notes from three real local sessions: P-01/P-02 on 26 November
and P-03 on 27 November. Participation consent was obtained. The team reports
that the instructor personally approved a recording-requirement exception.
Staging execution and prior instrumentation verification remain outstanding;
UT-01 stays `Planned` and
[QR-07 QRT-01](../../docs/quality-requirements/qr/QR-07.md#qrt-01)
stays `Not verified`. It moves to SPRINT-09 with the reason in
[the testing plan](../../docs/project-plan.md#quality-requirement-testing-plan).

The [qualitative record](../../docs/usability-tests/ut-01/results.md) links
[P-01](../../docs/usability-tests/ut-01/sessions/P-01.md),
[P-02](../../docs/usability-tests/ut-01/sessions/P-02.md) and
[P-03](../../docs/usability-tests/ut-01/sessions/P-03.md).
Practice discovery was understandable, but local editor startup, missing-test
feedback, rejected submissions and return navigation caused friction.
Individual SEQ and calculated SUS scores are in the notes; no completion,
time, SEQ or SUS aggregates are claimed under the shortfall rule.
Without an export, telemetry cannot corroborate the described actions.

The [findings and triage](../../docs/usability-tests/ut-01/results.md#findings)
record provisional recommendations; no issues or fixes have been scheduled
by this supplement. No REL-08 fix or Customer review of these late observations
is claimed. The
[private usability-data repository](https://github.com/team-ok-ITPD/team-OK-itpd-usability-data)
is the designated private store; this update does not verify its contents/access.

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
The private usability-data repository remains the designated private store.
The final repository state is the
`main` commit that the Week 9 submission takes its permalink from.
The handoff includes the [qualitative UT-01 record](../../docs/usability-tests/ut-01/results.md),
its unscheduled candidate fixes and the outstanding verified staging execution.
The Week 9 deck also reflects on the work the Customer set for the next review in [the meeting report](meeting-report.md#action-points): the group and assignment requirements, the submission acceptance fix, the CSV export sample, the extension usage guide, the project ZIP and Dockerfile rules, and the AI provider confirmation.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan | [docs/project-plan.md](../../docs/project-plan.md#sprint-08) |
| Usability results and findings | [Late qualitative record](../../docs/usability-tests/ut-01/results.md) |
| Sanitized session notes | [Session index](../../docs/usability-tests/ut-01/sessions/README.md#late-exploratory-notes) |
| QR-07 and its test | [QR-07 QRT-01](../../docs/quality-requirements/qr/QR-07.md#qrt-01) |
| Threshold review | [Threshold review](#threshold-review) |
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

- The 2026-11-27 usability supplement is late. Three real local sessions
  ran on 26–27 November. The team reports instructor approval of a
  recording-requirement exception. Staging execution, prior instrumentation
  verification, telemetry comparison
  and significant-finding issue scheduling remain outstanding.
- The sessions did not run against university staging. Timing is missing or
  partial, exercises and verification paths differ, and sanitized notes were
  prepared retrospectively. No aggregates or completed-study verdict are claimed.
- QR-07 QRT-01 moves to SPRINT-09, still `Not verified`, because the available
  local sessions do not establish the remaining protocol conditions. No late fix is attributed
  to REL-08.

- The Week 8 Sprint Review on 2026-11-20 presented the product workflows and did not present sanitized usability results or a `QR/QRT` result, and it did not establish that the `UT-01` design or a session plan was agreed. [The meeting report](meeting-report.md#previous-action-points) carries that action point into Week 9.
- [The meeting script](meeting-script.md) was written as a `UT-01` design and execution review, but the meeting covered the product workflows, so the script's agenda and the report's `Presented` line differ.
- Two Week 6 action points, on the submission-container lifecycle and the upload limit, were not re-listed by the Week 7 report; [the meeting report](meeting-report.md#previous-action-points) closes them here and carries them forward.
- No configuration change from the evaluation was enacted this week.

## Threshold review

The late UT-01 observations do not settle
[TOS-01 or TOS-03](../../docs/threshold-of-success.md): the former requires
timely debugger evidence and the latter five usefulness responses and Customer
acceptance. Those measures were not collected here. Their existing `Open`
proposal status is preserved; no Customer decision is invented.

## Privacy

No private-only material was committed to this repository, and no participant identity was committed to it.
