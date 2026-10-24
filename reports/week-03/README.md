# Week 03 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 3, Planning and the Minimum Usable Product
- **Release:** `REL-03`, published as
  [v0.1.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.1.0)
  on 2026-10-18.

## Summary

The team planned seven sprints, defined a draft threshold of success and risk
register, established the contribution workflow, selected the Docker,
code-server, Python, and pytest stack, and delivered one runnable debugging
exercise. A clean environment can open the catalog and browser-based VS Code,
reproduce the Python list-mutation defect, inspect it with the debugger, apply a
fix, and pass the tests.

No story moved out of the Week 2 candidate. The Week 3 Customer meeting was
intentionally used to validate the Figma prototype and product direction. The
running application was completed and verified by the team afterwards; its
Customer demonstration and story verdicts carry into the next assignment.

## Customer Meeting Outcome

The team showed the Figma prototype rather than running software. The Customer
settled the exercise structure, VS Code workflow, preview content, language
selector, and test-output direction in
[`DEC-006` through `DEC-010`](../../docs/decisions.md#dec-006).

`US-01` through `US-05` received no accepted or rejected verdict because the
running application was not shown. They remain open, and this report does not
claim Customer acceptance from team verification.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Threshold of success | [docs/threshold-of-success.md](../../docs/threshold-of-success.md) |
| Project plan | [docs/project-plan.md](../../docs/project-plan.md) |
| Risk register | [docs/risks.md](../../docs/risks.md) |
| Stack decision | [`DEC-005`](../../docs/decisions.md#dec-005) |
| Definition of Done | [docs/definition-of-done.md](../../docs/definition-of-done.md) |
| Contributing guide | [CONTRIBUTING.md](../../CONTRIBUTING.md) |
| Sprint milestones and issue fields | [`SPRINT-03`](https://github.com/team-ok-ITPD/team-OK-itpd/milestone/2) and its scheduled issues in the [sprint table](https://github.com/orgs/team-ok-ITPD/projects/1) |
| GitHub project | [Debug GYM delivery](https://github.com/orgs/team-ok-ITPD/projects/1) |
| Minimum usable product | Candidate stories [`US-01` through `US-05`](https://github.com/team-ok-ITPD/team-OK-itpd/issues?q=milestone%3A%22SPRINT-03%3A+MUP+and+planning%22+label%3Auser-story), implementation [PR #55](https://github.com/team-ok-ITPD/team-OK-itpd/pull/55), and [verification evidence](mup-verification.md) |
| Changelog and first release | [CHANGELOG.md](../../CHANGELOG.md) and [v0.1.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.1.0) |
| Documentation site | [published documentation](https://team-ok-itpd.github.io/team-OK-itpd/) |
| Setup and run instructions | [docs/setup.md](../../docs/setup.md) |
| Week 2 action points | [previous meeting reports and action points](meeting-report.md#2-previous-meeting-reports-and-action-points) |
| Week 2 open questions | [open questions carried by the Week 3 meeting](meeting-report.md#6-open-questions) |
| Meeting script | [meeting-script.md](meeting-script.md) |
| Customer validation | [meeting-report.md](meeting-report.md) and [meeting-transcript.md](meeting-transcript.md) |
| AI usage | [ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@Danashi11](https://github.com/Danashi11) | Planning and workflow [PR #53](https://github.com/team-ok-ITPD/team-OK-itpd/pull/53), MUP implementation [PR #55](https://github.com/team-ok-ITPD/team-OK-itpd/pull/55), GitHub milestones, project, issue fields, and release. |
| [@qwxiae](https://github.com/qwxiae) | Week 3 meeting artifacts and decisions in [PR #51](https://github.com/team-ok-ITPD/team-OK-itpd/pull/51). |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | Clean-checkout and acceptance-criteria audit in [PR #58](https://github.com/team-ok-ITPD/team-OK-itpd/pull/58). |
| [@adelazzi](https://github.com/adelazzi) | Setup and documentation review, MUP follow-up implementation, manual verification, and Week 3 evidence in [PR #60](https://github.com/team-ok-ITPD/team-OK-itpd/pull/60). |

## Repository Evidence

- [PR #55](https://github.com/team-ok-ITPD/team-OK-itpd/pull/55) implemented
  the working slice and closed task issue
  [#54](https://github.com/team-ok-ITPD/team-OK-itpd/issues/54).
- The latest `main` [link check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/39145619745),
  [Markdown check](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/39145619851),
  [product checks](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/39145619770),
  and [documentation workflow](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/39145619832)
  are green.

## Deviations

- The Week 3 meeting validated the Figma prototype and product direction, not
  the running MUP. Customer demonstration and story verdicts are carried into
  the next assignment; no acceptance is inferred from team verification.
- The threshold is a measurable team draft pending Customer review.
- The delivered environment uses browser-based code-server. The original SSH
  and invalid-access criteria remain open rather than being silently rewritten.
- Task acceptance criteria were not consistently ticked before earlier Week 3
  pull requests merged. This report preserves that history instead of editing
  completed reviews retroactively.

## Privacy

No private-only material was committed. The Customer permitted recording and
publication of the sanitized transcript.

## MUP Verification Detail

- Task: [#57](https://github.com/team-ok-ITPD/team-OK-itpd/issues/57).
- Verification date: 2026-10-17.
- Initial audit baseline: `62da3c55e50d0b8ccaea3b3d430a79bb78ab22a7`
  on `main`.
- The initial audit used a separate clone, Python 3.13, pytest 8.4.2, and Docker
  Desktop.
- The initial audit and the subsequent manual rehearsal are reported separately
  so that earlier findings are not confused with later verification.
- These results document team verification. They do not constitute Customer
  acceptance or automatically close user stories.

## Initial automated and source-level audit

The initial audit executed:

```powershell
python -m pip install -r requirements.lock
python -m pytest -q
docker compose -p itpd-debug-gym-audit config --quiet
```

The recorded results were:

- Product tests: **7 passed**.
- Docker Compose configuration validation passed.
- The exercise reproduced its intended defect when run with `python -m pytest -q`.
- The reference solution passed the exercise tests in the product test workflow.
- The supported catalog request returned the `remove-negatives` exercise and a workspace URL.
- An unsupported concurrency request returned HTTP 404.
- `git diff --check` passed.

The initial audit also found that the documented `pytest -q` command failed collection with `ModuleNotFoundError: remove_negatives` in the audit environment. Confirm that this discrepancy is resolved in the current workspace before claiming that the documented terminal workflow is fully verified.

The initial Docker image build was cancelled after approximately five minutes of slow base-image downloads. This was an incomplete build attempt, not a demonstrated build failure.

## Manual MUP verification

The team subsequently started the MUP successfully in an isolated Docker Compose project and performed the following manual checks.

### Catalog and workspace

- [x] Docker Compose started successfully.
- [x] Catalog health endpoint responded.
- [x] Workspace health endpoint responded.
- [x] A supported exercise request returned the live workspace URL.
- [x] The exercise workspace opened successfully.

### Reproduction, fix, and reset

- [x] The original exercise reproduced the expected test failures.
- [x] The buggy implementation was replaced with the reference solution.
- [x] All three exercise tests passed after applying the reference solution.
- [x] Resetting the isolated workspace restored the original buggy exercise.

### Browser-based debugging

- [x] Browser-based debugging was verified manually in code-server.
- [x] Breakpoints worked.
- [x] Stepping through execution worked.
- [x] Variable inspection worked.

These results supersede the initial audit's pending status for the checks explicitly listed above. They do not establish that every story acceptance criterion is satisfied.

## Acceptance-criterion matrix

This matrix records the available evidence. Story closure remains subject to the complete acceptance criteria in GitHub.

| Story | Criterion | Current evidence and status |
|---|---|---|
| [US-01 / #28](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28) | AC-01 | Supported exercise request returned the exercise and workspace URL. Verified manually. |
| US-01 / #28 | AC-02 | Unsupported request returned the expected no-match response in the initial audit. Retain the evidence and confirm the criterion is satisfied. |
| [US-02 / #29](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29) | AC-01 | Docker Compose and workspace startup were verified manually. |
| US-02 / #29 | AC-02 | Workspace health was verified, but the separate error-handling and access requirements must be checked against the issue's exact wording. |
| [US-03 / #30](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30) | AC-01 | The exercise reproduced the expected failures manually. Confirm the documented command works in the current container. |
| US-03 / #30 | AC-02 | Repeatable buggy behavior was checked in the initial product tests; the manual reset restored the original buggy exercise. |
| [US-04 / #31](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31) | AC-01 | The reference solution passed all three exercise tests after manual application. |
| US-04 / #31 | AC-02 | The initial bug and successful reference solution were verified. Check the exact story criteria before marking the issue complete. |
| [US-05 / #32](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32) | AC-01 | Browser-based breakpoint debugging, stepping, and variable inspection were verified. The SSH requirement remains unresolved. |
| US-05 / #32 | AC-02 | Browser-based debugging works, but the current workspace uses unauthenticated code-server. The access-control requirement remains unresolved. |

**Important:** Update the checkboxes in GitHub issues #28–#32 individually. This report does not replace the required acceptance-criteria review.

## Outstanding issues and follow-up

### SSH and workspace access control

The current workspace uses browser-based code-server with authentication disabled (`--auth none`). The original US-05 criteria require SSH and access control.

Browser debugging working successfully does not resolve this mismatch.

Track the decision and follow-up in the separate SSH/access-control issue. Document whether SSH is mandatory or whether browser-only access is acceptable, implement the agreed requirements, and verify the resulting access controls before claiming US-05 is fully satisfied.

### Python test command

The initial audit recorded an import failure with the documented `pytest -q` command, while `python -m pytest -q` reproduced the intended exercise defect.

Verify both commands in the current container using the documented Python environment. Update the setup instructions if the commands behave differently.

### Configurable catalog port

The initial source audit identified a possible mismatch between `DEBUG_GYM_CATALOG_PORT` and the Compose port mapping. Verify a non-default port against the current implementation before treating this as resolved.

### Setup documentation

The initial audit was conducted before `docs/setup.md` was available. The setup documentation has since been added. A separate clean-checkout run following those instructions is still needed if that procedure has not already been verified.

## AI assistance

Codex assisted with repository inspection, test analysis, and drafting the initial audit. The team subsequently performed the manual MUP verification described in this report.

The reported manual results are distinct from the initial audit and do not constitute Customer acceptance. Review the outstanding criteria and record the Customer/team decision before closing the affected stories.
