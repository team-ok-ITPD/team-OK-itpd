# Sprint 06 Retrospective

## What Went Well

| What went well |
| --- |
| The team delivered server-enforced exercise audiences, administrator-managed groups, group deadlines and isolated submission verification through independently reviewed pull requests. |
| The catalog now emits privacy-preserving analytics events and structured operating signals, with automated coverage for their schemas and call sites. |
| The analytics, observability, architecture, functional-requirement and diagnosability records were merged into maintained documentation rather than left on feature branches. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| The four telemetry dashboards, deployed QRT and production release were not completed. | The university VM and telemetry backends were unavailable, and no substitute environment could provide the required university-network evidence. |
| The product-analyst and system-operator stories were not created during sprint planning. | Telemetry work was decomposed directly into implementation tasks, so the internal users, story points and acceptance criteria were omitted. |
| Sprint-closing records again accumulated near the deadline. | Product implementation and corrective documentation were prioritized before the retrospective and release readiness review. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Obtain university VM access before scheduling dashboard and deployed-QRT work, then deploy staging before production. | qwxiae | High | A second sprint ended without deployable university infrastructure. | Yes |
| Create the product-analyst and system-operator stories before rescheduling the telemetry deployment. | Danashi11 | High | The sprint had tasks but no required internal-user stories or countable velocity. | No |
| Run `QR-06 QRT-01` against staging and retain the sanitized log, P95 and dashboard evidence before cutting `REL-06`. | UTKANOS-RIBA | High | Local tests cannot establish deployed diagnosability. | Yes |
| Open the report, retrospective and release-readiness tasks during sprint planning. | adelazzi | Medium | Closing evidence should develop with the increment rather than after it. | Yes |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-05/sprint-retrospective.md](../week-05/sprint-retrospective.md#actions): "Require every product-code pull request to add its suite to the root product workflow before merge." | `Done`: product checks now run the Django, product, frontend and container checks for the merged Week 6 changes. |
| [reports/week-05/sprint-retrospective.md](../week-05/sprint-retrospective.md#actions): "Prepare staging at the start of the first sprint in which the university VM is available." | `Not done`: the university VM remained unavailable, so this action is carried into the next sprint. |
