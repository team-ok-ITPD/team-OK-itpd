# Sprint 07 Retrospective

## What Went Well

| What went well |
| --- |
| The `UT-01` design is complete and consistent across its record, surveys, consent template, session template, results stub, `QR-07` and testing-plan row, with a recruitment target, an analysis plan and an evidence map written before any session. |
| The staging-only `source=usability-test` marking was implemented with automated tests, so the test's events can be excluded from product metrics without a new event. |
| The Customer meeting settled the three-role model and the group-first teaching workflow, and recorded `DEC-039` through `DEC-043` with owners and due weeks for the follow-up work. |
| The recruitment, consent, data-access and schedule risks were written with a fallback for each failure mode before the first session is arranged. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| The `UT-01` design was not shown to the Customer, so no `DEC-nnn` records feedback on it and the Week 8 plan and results date were not agreed. | The meeting script was built from the open product questions rather than from Assignment 7's design-review agenda. |
| The instrumentation verification, the dry run and the deployed `QR-02` and `QR-06` runs could not happen. | The university VM and staging were again unavailable, so nothing could be verified on the university network. |
| The report, the retrospective and the release records were again written on the last day. | Their tasks were not opened at sprint planning, and design and product work took priority. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Obtain university VM access, deploy staging, then run the `UT-01` instrumentation verification and the dry run before the first counted session. | qwxiae | High | Staging has been unavailable since Week 5 and blocks every deployed check. | Yes |
| Run `QR-06 QRT-01` and `QR-02 QRT-01` against staging and keep the sanitized evidence. | UTKANOS-RIBA | High | Local tests cannot establish deployed diagnosability or isolation. | Yes |
| Open the report, retrospective and release-readiness tasks during sprint planning, each with an owner. | adelazzi | Medium | Closing evidence should develop with the increment, not after it. | Yes |
| Write the Week 8 meeting script from the assignment's design-review agenda, and show `UT-01` and agree the session plan and the results date. | Danashi11 | High | The Week 7 meeting did not review the test design. | No |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-06/sprint-retrospective.md](../week-06/sprint-retrospective.md#actions): "Obtain university VM access before scheduling dashboard and deployed-QRT work, then deploy staging before production." | `Not done`: staging was not available during the sprint, so the action is re-listed above. |
| [reports/week-06/sprint-retrospective.md](../week-06/sprint-retrospective.md#actions): "Run `QR-06 QRT-01` against staging and retain the sanitized log, P95 and dashboard evidence before cutting `REL-06`." | `Not done`: no staging organization existed, so the run moves to `SPRINT-08` and the action is re-listed above. |
| [reports/week-06/sprint-retrospective.md](../week-06/sprint-retrospective.md#actions): "Open the report, retrospective and release-readiness tasks during sprint planning." | `Not done`: the closing records were again completed at the end of the sprint, so the action is re-listed above. |
