# Sprint 05 retrospective

## What Went Well

| What went well |
| --- |
| The team merged the multi-user Django application, browser-based VS Code launch and submission extension through [PR #103](https://github.com/team-ok-ITPD/team-OK-itpd/pull/103). |
| The Customer reviewed the current workflow and confirmed its direction while providing eleven recorded decisions for the next university-specific increments. |
| `US-01` through `US-05` closed as the completed core learner workflow, and the title-search clarification became the small completed `US-08`. |
| The meeting report carried every Week 4 action and open question forward rather than silently dropping unfinished work. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| Staging and production were not available for the review, so the team could not run a deployed QRT or show the Customer the university VM. | The university VM was unavailable during the sprint, and GitHub-hosted CI cannot reach the university network. |
| The first CI run after the Django merge still exercised only the original product suite. | The application arrived as a large feature branch late in the sprint, while its separate Django and extension suites were not added to the root workflow in the same pull request. |
| Most Assignment 5 planning and release records remained until the sprint's final day. | The team prioritized the working learner flow and meeting preparation before decomposing the required testing, deployment and reporting artifacts. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Require every product-code pull request to add its suite to the root product workflow before merge. | Danashi11 | High | The Django and extension suites initially existed without CI execution. | Yes |
| Prepare staging at the start of the first sprint in which the university VM is available. | qwxiae | High | Week 5 could not produce deployed evidence or a production demonstration. | Yes |
| Split the university roles, exercise access, groups and deadlines into independently reviewable stories before implementation. | UTKANOS-RIBA | High | The Customer added a large university-specific scope that should not become one feature branch. | No |
| Open the sprint-closing documentation tasks during planning rather than on the deadline day. | adelazzi | Medium | Planning, testing and release records accumulated at the end of SPRINT-05. | No |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-04/sprint-retrospective.md](../week-04/sprint-retrospective.md#actions): "Show the containerized workspace against `US-01` through `US-05`, one `AC-nn` at a time, and record a verdict for each as a `DEC-nnn`." | `Done`: the team showed the current learner workflow, the Customer was satisfied with the completed core increment, and the stories closed; the meeting also produced the next product requirements. |
| [reports/week-04/sprint-retrospective.md](../week-04/sprint-retrospective.md#actions): "Hold the Customer meeting before the sprint's due date, and cut the release only after it." | `Done`: the meeting was held on the 2026-10-31 sprint due date, before `REL-05` is cut. |
