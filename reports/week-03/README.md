# Week 3 MUP Verification

## Scope and provenance

- Task: [#57](https://github.com/team-ok-ITPD/team-OK-itpd/issues/57).
- Verification date: 2026-10-17.
- Initial audit baseline: `62da3c55e50d0b8ccaea3b3d430a79bb78ab22a7` on `main`.
- The initial audit used a separate clone, Python 3.13, pytest 8.4.2, and Docker Desktop.
- The initial audit and the subsequent manual rehearsal are reported separately so that earlier findings are not confused with later verification.
- These results document team verification. They do not constitute Customer acceptance or automatically close user stories.

## Initial automated and source-level audit

The initial audit executed:

```powershell
python -m pip install -r requirements.lock
python -m pytest -q
docker compose -p itpd-artem-audit config --quiet
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