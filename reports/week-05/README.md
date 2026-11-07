# Week 05 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 5, MVP Workflow, Testing And Deployment Preparation
- **Release:** `REL-05`, published as `v0.3.0` on 2026-10-31.

## Summary

The team integrated the multi-user Django application and browser-based VS Code
extension, then added the missing root CI coverage for the catalog, exercise,
Django application, extension and product container. A signed-in learner can
choose a prepared exercise, keep a separate draft and attempt history, open its
workspace, run tests and submit from VS Code. The Customer accepted `US-01`
through `US-05`; `US-08` completed the title-search clarification.

`SPRINT-05` planned and completed `23SP`: `US-01` (3), `US-02` (5), `US-03`
(3), `US-04` (3), `US-05` (8) and `US-08` (1). `US-09` remains an estimated,
unscheduled product-backlog item. The newly requested roles, groups, deadlines
and result export are future increments and are not part of `REL-05`.

## Customer Meeting Outcome

The 2026-10-31 review accepted the five core learner stories and produced
[`DEC-016` through `DEC-031`](../../docs/decisions.md). The university-specific
roles, access levels, groups, deadlines and CSV export extend the accepted
baseline rather than reopening it. The full outcome and follow-up questions are
in the [meeting report](meeting-report.md).

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan, velocity and milestones | [Project plan](../../docs/project-plan.md#sprint-05) |
| Customer validation | [Meeting report](meeting-report.md), [transcript](meeting-transcript.md) and [`DEC-027` to `DEC-031`](../../docs/decisions.md#dec-027) |
| Product checks | [Workflow](../../.github/workflows/product.yml) and [successful `main` run](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/41228949546) |
| Quality tests and evidence | [Testing plan](../../docs/project-plan.md#quality-requirement-testing-plan), [QR-01](../../docs/quality-requirements/qr/QR-01.md#qrt-01), [QR-02](../../docs/quality-requirements/qr/QR-02.md#qrt-01) and [QR-03](../../docs/quality-requirements/qr/QR-03.md#qrt-01) |
| Current product behavior | [Feature documentation](../../docs/features.md) |
| Environment and deployment procedure | [Deployment runbook](../../docs/deployment.md) |
| Sprint retrospective | [Sprint 05 retrospective](sprint-retrospective.md) |
| AI usage | [Week 5 AI usage](ai-usage.md) |
| Release | `REL-05` / `v0.3.0` and [changelog](../../CHANGELOG.md) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@adelazzi](https://github.com/adelazzi) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aadelazzi) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aadelazzi) |
| [@Danashi11](https://github.com/Danashi11) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3ADanashi11) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3ADanashi11) |
| [@qwxiae](https://github.com/qwxiae) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3Aqwxiae) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3Aqwxiae) |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | [Pull requests](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+author%3AUTKANOS-RIBA) and [reviews](https://github.com/team-ok-ITPD/team-OK-itpd/pulls?q=is%3Apr+reviewed-by%3AUTKANOS-RIBA) |

## Quality Evidence

The merged `main` Product checks run passed the catalog and exercise contract,
Django application, VS Code extension and product-container jobs. This verifies
`QR-01 QRT-01` and `QR-03 QRT-01`. `QR-02 QRT-01` remains **Not verified**:
the product does not yet provision five isolated learner workspaces with the
specified resource limits, and the unavailable university VM cannot substitute
for that test.

## Deviations And Limitations

- The university VM was unavailable. No staging or production deployment was
  performed, and `REL-05` has no deployed QRT evidence.
- The release has one curated exercise, not the ten-exercise library target in
  `QR-01`.
- Roles, university-email verification, exercise access levels, groups,
  deadlines, best-submission scoring and CSV export are not implemented.
- The test panel updates after a test run, but there is no realtime
  synchronization between an already open website page and VS Code.

## Privacy

No private VM address, credential, API key or private-only meeting material is
included in the repository.
