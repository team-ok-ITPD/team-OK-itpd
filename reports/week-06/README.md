# Week 06 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 6, Product Analytics, Observability And The Week 6 Release
- **Release:** `REL-06` has not been cut at the time of writing.

## Summary

The product now records an analytics event for each core-task step and exposes a request-duration signal for the catalog search. [The analytics plan](../../docs/analytics.md) names the focus metric, solved exercises per active learner per week, with its counter-metric, inputs and event table. [FR-014](../../docs/functional-requirements/fr/FR-014.md) and [ADR-006](../../docs/architecture/adr/ADR-006.md) specify the events; [FR-013](../../docs/functional-requirements/fr/FR-013.md), [ADR-005](../../docs/architecture/adr/ADR-005.md) and [QR-06](../../docs/quality-requirements/qr/QR-06.md) specify the operating signal and its diagnosability test.

The focus metric has no value yet. It needs an analytics backend that receives the events, and learners outside the team using the product. The [workspace open rate](../../docs/analytics.md#workspace-open-rate) is defined to be computed by its query rather than by hand, but it has no measured value because no backend is deployed. The events were checked by sending them from a development machine to a temporary HTTPS request catcher.

Nothing in this report claims a deployed backend, a dashboard, a staging or production deployment, or a passed `QR-06 QRT-01`. The work that remains is in [Deviations](#deviations).

## Threshold Review

| Goal | Current measure | New data can settle it | Proposal |
| --- | --- | --- | --- |
| [TOS-01](../../docs/threshold-of-success.md#tos-01) | Three dated pilot records of a learner passing the exercise in 20 minutes or less. | Yes, in part: `exercise_opened` and `solution_verified` provide the elapsed time after a backend is running. | — |
| [TOS-02](../../docs/threshold-of-success.md#tos-02) | A validation run over ten sampled exercises. | No: the measure is about exercise content, not use. | — |
| [TOS-03](../../docs/threshold-of-success.md#tos-03) | A linked Customer acceptance decision and four positive answers from five pilot learners. | No: it needs the Customer's decision and a survey. | — |

[TOS-01](../../docs/threshold-of-success.md#tos-01) is `Open`.
[TOS-02](../../docs/threshold-of-success.md#tos-02) is `Open`.
[TOS-03](../../docs/threshold-of-success.md#tos-03) is `Open`.

This report records no proposal for an analytics-measured goal, and the Customer has made no decision on one, so no `DEC-nnn` changes a goal.

## Dashboards

The four dashboards, an analytics and an observability dashboard in each of staging and production, do not exist yet, so this report has no dashboard screenshots. The queries they will run are recorded in [the analytics plan](../../docs/analytics.md) and in [SLI-01](../../docs/observability.md#sli-01).

## Customer Meeting Outcome

The Week 6 meeting was held on 2026-11-06, before the telemetry was built, so it did not show the analytics, the observability signals or the `QR-06` test. Its outcome is in the [meeting report](meeting-report.md) and the [meeting notes](meeting-notes.md). The report has no meeting script for this week.

No telemetry story received a Customer acceptance or rejection verdict. The
meeting refined the university workflow and produced `DEC-032` through
`DEC-038`; it cannot be treated as validation of the later telemetry increment.

## Minimum Usable Product Candidate

The latest released candidate remains
[`v0.3.0`](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.3.0).
The Week 6 sharing, analytics and observability changes remain unreleased because
there is no final production deployment or passed deployed QRT.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and new stories | [docs/project-plan.md#sprint-06](../../docs/project-plan.md#sprint-06); the two required internal-user stories were not created and are declared as a deviation |
| Analytics plan | [docs/analytics.md](../../docs/analytics.md), with the metric tree and a section per metric |
| Events and instrumentation | [docs/analytics.md#the-events](../../docs/analytics.md#the-events), `app/adel_b/config/analytics.py` and `scripts/send_smoke_event.py` |
| Analytics dashboards | Not produced: OpenPanel and the university VM were unavailable |
| Observability plan and `SLI`s | [docs/observability.md](../../docs/observability.md) |
| Observability dashboards | Not produced: OpenObserve and the university VM were unavailable |
| Feature documentation | [docs/features.md](../../docs/features.md) |
| Functional requirements | [docs/functional-requirements/README.md](../../docs/functional-requirements/README.md), [FR-013](../../docs/functional-requirements/fr/FR-013.md) and [FR-014](../../docs/functional-requirements/fr/FR-014.md) |
| ADRs and container view | [docs/architecture/README.md#architectural-decisions](../../docs/architecture/README.md#architectural-decisions) and [docs/architecture/README.md#container-view](../../docs/architecture/README.md#container-view) |
| Observability requirement | [docs/quality-requirements/qr/QR-06.md](../../docs/quality-requirements/qr/QR-06.md) and [QRT-01](../../docs/quality-requirements/qr/QR-06.md#qrt-01) |
| Runtime test re-run | [docs/project-plan.md#quality-requirement-testing-plan](../../docs/project-plan.md#quality-requirement-testing-plan); no runtime test was re-run |
| Threshold review | [reports/week-06/README.md#threshold-review](#threshold-review) |
| Week 5 action points | [reports/week-06/meeting-report.md#previous-action-points](meeting-report.md#previous-action-points) |
| Week 5 open questions | [reports/week-06/meeting-report.md#previous-open-questions](meeting-report.md#previous-open-questions) |
| Meeting script | Not produced: the meeting preceded the telemetry implementation and was not the required telemetry Sprint Review |
| Customer validation | [reports/week-06/meeting-report.md](meeting-report.md); it does not validate the telemetry increment |
| `REL-06` | Not released: no final production deployment or passed deployed QRT exists |
| Sprint retrospective | [reports/week-06/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-06/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@adelazzi](https://github.com/adelazzi) | Approved the analytics and observability records in [PR #151](https://github.com/team-ok-ITPD/team-OK-itpd/pull/151) and [PR #153](https://github.com/team-ok-ITPD/team-OK-itpd/pull/153). |
| [@Danashi11](https://github.com/Danashi11) | Implemented the role-based sharing increment and approved the final observability records in [PR #153](https://github.com/team-ok-ITPD/team-OK-itpd/pull/153). |
| [@qwxiae](https://github.com/qwxiae) | Authored the merged analytics and observability work in [PR #151](https://github.com/team-ok-ITPD/team-OK-itpd/pull/151) and [PR #153](https://github.com/team-ok-ITPD/team-OK-itpd/pull/153). |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | Contributed the group-assignment and isolated-verification work recorded in the sprint backlog. |

## Quality Evidence

`QR-06 QRT-01` is **Not verified**: it runs against a staging deployment and a staging observability organization, and neither exists. `QR-02 QRT-01` is **Not verified** and moved to `SPRINT-07`, because the product does not yet provision five isolated learner workspaces. The [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan) holds both rows.

The Django tests for the analytics emitter, the four event call sites and the smoke script passed on a development machine. The full Django suite has two failures that occur on Windows only: one test opens `/dev/null` and one asserts a file mode of `0o600`.

## Repository Evidence

The telemetry records and implementation were merged through
[PR #151](https://github.com/team-ok-ITPD/team-OK-itpd/pull/151) and
[PR #153](https://github.com/team-ok-ITPD/team-OK-itpd/pull/153). On the latest
public `main` commit before this report correction, the
[product checks](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/42500884685),
[link check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/42500884377),
[Markdown check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/42500884517),
[actionlint](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/42500884633)
and [documentation build](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/42500884338)
all passed. The submission snapshot must use the merged report-correction commit
and its own green checks.

## Deviations

- The university VM and the two telemetry backends are not available to the team, so no backend, no dashboard, no staging or production deployment and no `QR-06 QRT-01` run exist.
- The team has not run `QR-06 QRT-01`, so its [script](../../scripts/check_sli.py) is untested against an observability backend.
- No analytics metric has a measured value, and no staging smoke event reached a backend.
- `REL-06` is not cut because there is no final production deployment or passed deployed QRT.
- The two required product-analyst and system-operator stories were not created;
  telemetry work was tracked as tasks, so actual velocity is zero.
- The Customer meeting preceded the telemetry, so there is no meeting script, no `DEC-nnn` for a threshold proposal and no demonstration of the telemetry.
- `QR-02 QRT-01`, planned for `SPRINT-06`, moved to `SPRINT-07`, as above.

## Privacy

No private-only material was committed to this repository.
