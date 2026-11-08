# Week 06 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 6, Product Analytics, Observability And The Week 6 Release
- **Release:** `REL-06` has not been cut at the time of writing.

## Summary

The product now records an analytics event for each core-task step and exposes a request-duration signal for the catalog search. [The analytics plan](../../docs/analytics.md) names the focus metric, solved exercises per active learner per week, with its counter-metric, inputs and event table. [FR-014](../../docs/functional-requirements/fr/FR-014.md) and [ADR-006](../../docs/architecture/adr/ADR-006.md) specify the events; [FR-013](../../docs/functional-requirements/fr/FR-013.md), [ADR-005](../../docs/architecture/adr/ADR-005.md) and [QR-06](../../docs/quality-requirements/qr/QR-06.md) specify the operating signal and its diagnosability test.

The focus metric has no value yet. It needs an analytics backend that receives the events, and learners outside the team using the product. No metric has been computed by its query, because no backend is deployed. The events were checked by sending them from a development machine to a temporary HTTPS request catcher.

Nothing in this report claims a deployed backend, a dashboard, a staging or production deployment, or a passed `QR-06 QRT-01`. The work that remains is in [Deviations](#deviations).

## Threshold Review

| Goal | Current measure | Can the new data settle it? | Proposal |
| --- | --- | --- | --- |
| [TOS-01](../../docs/threshold-of-success.md#tos-01) | Three dated pilot records of a learner passing the exercise in 20 minutes or less. | In part: the timestamps of `exercise_opened` and `solution_verified` give the time to a passing run, but only for traffic after a backend is running. | None recorded. |
| [TOS-02](../../docs/threshold-of-success.md#tos-02) | A validation run over ten sampled exercises. | No: the measure is about exercise content, not use. | None recorded. |
| [TOS-03](../../docs/threshold-of-success.md#tos-03) | A linked Customer acceptance decision and four positive answers from five pilot learners. | No: it needs the Customer's decision and a survey. | None recorded. |

[TOS-01](../../docs/threshold-of-success.md#tos-01) stays `Open`: no pilot records are linked from this report, and the analytics cannot yet supply the time to a passing run. [TOS-02](../../docs/threshold-of-success.md#tos-02) stays `Open` and is due in Week 7. [TOS-03](../../docs/threshold-of-success.md#tos-03) stays `Open` and is due in Week 9.

This report records no proposal for an analytics-measured goal, and the Customer has made no decision on one, so no `DEC-nnn` changes a goal.

## Dashboards

The four dashboards, an analytics and an observability dashboard in each of staging and production, do not exist yet, so this report has no dashboard screenshots. The queries they will run are recorded in [the analytics plan](../../docs/analytics.md) and in [SLI-01](../../docs/observability.md#sli-01).

## Customer Meeting Outcome

The Week 6 meeting was held on 2026-11-06, before the telemetry was built, so it did not show the analytics, the observability signals or the `QR-06` test. Its outcome is in the [meeting report](meeting-report.md) and the [meeting notes](meeting-notes.md). The report has no meeting script for this week.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Analytics plan | [Analytics plan](../../docs/analytics.md), with the metric tree and a section per metric |
| Events and instrumentation | [The events](../../docs/analytics.md#the-events), `app/adel_b/config/analytics.py` and `scripts/send_smoke_event.py` |
| Observability plan and `SLI`s | [Observability plan](../../docs/observability.md) |
| Feature documentation | [Feature documentation](../../docs/features.md) |
| Functional requirements | [Functional requirements](../../docs/functional-requirements/README.md), with [FR-013](../../docs/functional-requirements/fr/FR-013.md) and [FR-014](../../docs/functional-requirements/fr/FR-014.md) |
| ADRs and container view | [ADR index](../../docs/architecture/README.md#architectural-decisions) and [container view](../../docs/architecture/README.md#container-view) |
| Observability requirement | [QR-06](../../docs/quality-requirements/qr/QR-06.md) and its [QRT-01](../../docs/quality-requirements/qr/QR-06.md#qrt-01) |
| Deployment procedure | [Telemetry pipelines](../../docs/deployment.md#telemetry-pipelines) |
| Threshold review | [Threshold review](#threshold-review) |
| Week 5 action points and open questions | [Meeting report](meeting-report.md) |
| AI usage | [Week 6 AI usage](ai-usage.md) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@adelazzi](https://github.com/adelazzi) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aadelazzi) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aadelazzi) |
| [@Danashi11](https://github.com/Danashi11) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3ADanashi11) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3ADanashi11) |
| [@qwxiae](https://github.com/qwxiae) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aqwxiae) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aqwxiae) |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3AUTKANOS-RIBA) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3AUTKANOS-RIBA) |

## Quality Evidence

`QR-06 QRT-01` is **Not verified**: it runs against a staging deployment and a staging observability organization, and neither exists. `QR-02 QRT-01` is **Not verified** and moved to `SPRINT-07`, because the product does not yet provision five isolated learner workspaces. The [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan) holds both rows.

The Django tests for the analytics emitter, the four event call sites and the smoke script passed on a development machine. The full Django suite has two failures that occur on Windows only: one test opens `/dev/null` and one asserts a file mode of `0o600`.

## Deviations

- The university VM and the two telemetry backends are not available to the team, so no backend, no dashboard, no staging or production deployment and no `QR-06 QRT-01` run exist.
- The team has not run `QR-06 QRT-01`, so its [script](../../scripts/check_sli.py) is untested against an observability backend.
- No analytics metric is computed by its query, and no staging smoke event reached a backend.
- `REL-06` is not cut, the plan's `REL-06` block and `SPRINT-06`'s actual velocity are not set, and there is no sprint retrospective in this report.
- The Customer meeting preceded the telemetry, so there is no meeting script, no `DEC-nnn` for a threshold proposal and no demonstration of the telemetry.
- `QR-02 QRT-01`, planned for `SPRINT-06`, moved to `SPRINT-07`, as above.

## Privacy

No private VM address, credential, API key or private-only meeting material is included in the repository.
