# Project plan

## Milestones

### MLS-03

- **Due:** 2026-10-17
- **Sprints:** [SPRINT-03](#sprint-03)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01)

A learner can choose a prepared Python bug, open a ready VS Code environment,
reproduce the failure, debug it, and verify the fix. The increment includes one
curated exercise and the setup evidence needed to run the flow from a clean
checkout.

### MLS-05

- **Due:** 2026-10-31
- **Sprints:** [SPRINT-04](#sprint-04), [SPRINT-05](#sprint-05)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01), [TOS-03](threshold-of-success.md#tos-03)

A signed-in learner completes the prepared debugging workflow from choosing an
exercise through submitting the tested fix from browser-based VS Code. The
increment also keeps each learner's drafts and attempts separate and records
the Customer's validation of the workflow.

### MLS-06

- **Due:** 2026-11-07
- **Sprints:** [SPRINT-06](#sprint-06)
- **Advances:** [TOS-03](threshold-of-success.md#tos-03)

Teachers and students have the first university-specific sharing increment:
roles determine who may publish an exercise and which prepared exercises each
learner may open. Group assignment, deadlines and result export build on this
access model in later increments.

## Sprints

### SPRINT-03

A clean checkout provides one complete prepared Python debugging exercise through a browser-based VS Code environment.

- **Due:** 2026-10-17
- **Sprint Backlog:** [the issues scheduled into SPRINT-03](https://github.com/team-ok-ITPD/team-OK-itpd/milestone/2)

#### REL-03

Released as [v0.1.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.1.0) on 2026-10-18.

### SPRINT-04

The product has documented quality requirements and architecture, and the team has validated and selected a safe execution architecture for multi-file learner submissions.

- **Due:** 2026-10-24
- **Sprint Backlog:** [the issues scheduled into SPRINT-04](https://github.com/team-ok-ITPD/team-OK-itpd/milestone/5)
- **Planned Velocity:** 22
- **Actual Velocity:** 0; `US-01` through `US-05` received no Customer verdict at the 2026-10-26 review and moved to `SPRINT-05`.

#### REL-04

Released as [v0.2.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.2.0) on 2026-10-25 as a pre-meeting validation candidate. It
adds the documented
requirements and architecture package, improves local setup and terminal use,
and prevents known false-positive exercise matches. It remains a learner-local,
browser-based flow with one prepared exercise; Customer acceptance,
SSH/authentication, multi-user isolation, agent assistance (US-06), and category
browsing (US-07) are not included.

### SPRINT-05

A signed-in learner can choose a prepared exercise, work on it in browser-based VS Code, run its tests and submit the result in the validated end-to-end workflow.

- **Due:** 2026-10-31
- **Sprint Backlog:** [the issues scheduled into SPRINT-05](https://github.com/team-ok-ITPD/team-OK-itpd/milestone/7)
- **Planned Velocity:** 23
- **Actual Velocity:** 23; `US-01` through `US-05` and `US-08` completed, while the refined `US-09` remains unscheduled for `SPRINT-06` planning.

#### REL-05

Released as [v0.3.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.3.0)
on 2026-10-31. It adds the signed-in, multi-user Django learner flow, persistent
drafts and attempts, browser-based VS Code launch, in-editor test results and
submission, and the prepared-exercise title search. The university VM was not
available, so this release has CI and local-container evidence but no staging or
production deployment evidence.

### SPRINT-06

Provisional: learners can request bounded assistance without the product applying the fix for them.

- **Due:** 2026-11-07

#### REL-06

### SPRINT-07

Provisional: learners can choose from a small verified library of Python bug categories.

- **Due:** 2026-11-14

#### REL-07

### SPRINT-08

Provisional: the core workflow is reliable, safe, and supported by pilot evidence.

- **Due:** 2026-11-21

#### REL-08

### SPRINT-09

Provisional: the release candidate meets the agreed threshold measures available by code freeze.

- **Due:** 2026-11-28

#### REL-09

## Quality Requirement Testing Plan

| QR                                        | QRT                                                     | Status       | Checked | Planned for sprint      | Evidence |
| ----------------------------------------- | ------------------------------------------------------- | ------------ | ------- | ----------------------- | -------- |
| [QR-01](quality-requirements/qr/QR-01.md) | [QR-01 QRT-01](quality-requirements/qr/QR-01.md#qrt-01) | Passes      | 2026-10-31 | [SPRINT-05](#sprint-05) | [Product checks](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/41228949546) |
| [QR-02](quality-requirements/qr/QR-02.md) | [QR-02 QRT-01](quality-requirements/qr/QR-02.md#qrt-01) | Not verified | None    | [SPRINT-06](#sprint-06) | None     |
| [QR-03](quality-requirements/qr/QR-03.md) | [QR-03 QRT-01](quality-requirements/qr/QR-03.md#qrt-01) | Passes      | 2026-10-31 | [SPRINT-05](#sprint-05) | [Product checks](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/41228949546) |

## Progress Monitoring

- **Review:** the team reviews
  [threshold-of-success.md](threshold-of-success.md) and
  [risks.md](risks.md), including every testing-plan row that is not `Passes`,
  every Friday before the weekly submission.
- **Checked by:** all four team members walk the sprint goal, scheduled issues,
  threshold measures, and risk triggers; each accountable member reports the
  state of their issues.
- **Visible at:** the public
  [GitHub Projects sprint table](https://github.com/orgs/team-ok-ITPD/projects/1)
  and the [sprints' GitHub milestones](https://github.com/team-ok-ITPD/team-OK-itpd/milestones).
