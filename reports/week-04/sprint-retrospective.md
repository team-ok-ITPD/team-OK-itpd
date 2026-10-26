# Sprint 04 retrospective

## What Went Well

| What went well |
| --- |
| The team merged the quality requirements, functional requirements, architectural decision records, glossary and `AGENTS.md` through a reviewed pull request ([PR #84](https://github.com/team-ok-ITPD/team-OK-itpd/pull/84)) instead of leaving them as separate drafts. |
| `SPRINT-04` carries a goal and a planned velocity of `22SP` in [the plan](../../docs/project-plan.md#sprint-04), so the sprint had a target the team could compare with. |
| The Customer meeting produced five decisions, [`DEC-011` through `DEC-015`](../../docs/decisions.md#dec-011), and seven action points due inside Week 5. |
| The issue-conversion script was previewed and reviewed before it touched live issues, and its defect was corrected in [PR #85](https://github.com/team-ok-ITPD/team-OK-itpd/pull/85). |

## What Did Not

| Problem | Root cause |
| --- | --- |
| `US-01` through `US-05` received no Customer verdict, so no story closed and no points count as completed. | The meeting showed the web prototype of the learner flow, not the containerized workspace, so no `AC-nn` was shown and the Customer had nothing to accept or reject. |
| `REL-04` (`v0.2.0`) was cut on 2026-10-25, a day before the Customer meeting, so the release does not carry the meeting's decisions. | The meeting was scheduled for 2026-10-26, after the sprint's due date of 2026-10-24, and the team released before it rather than waiting for the rework the meeting could cause. |
| The first functional-requirements pull request ([PR #80](https://github.com/team-ok-ITPD/team-OK-itpd/pull/80)) was closed and redone, and [PR #87](https://github.com/team-ok-ITPD/team-OK-itpd/pull/87) was still awaiting review at the close. | Ownership of the task moved to another member after work had started, and a review was not requested from a second member while the author was still working. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Show the containerized workspace against `US-01` through `US-05`, one `AC-nn` at a time, and record a verdict for each as a `DEC-nnn`. | adelazzi | High | No story closed because the meeting showed the prototype and not the workspace. | Yes |
| Hold the Customer meeting before the sprint's due date, and cut the release only after it. | Danashi11 | High | `REL-04` was cut before the meeting and the meeting's decisions are not in it. | Yes |
| Name one author and one reviewer on a task when it is opened, and hand the branch over in the issue when the owner changes. | qwxiae | Medium | PR #80 was closed and redone when ownership moved. | No |
| Request the second member's review as soon as a pull request is opened. | UTKANOS-RIBA | Medium | PR #87 was still awaiting review at the close. | No |

## Carried Actions

None: `SPRINT-04` is the first sprint with a retrospective, so there is no previous retrospective to carry actions from.