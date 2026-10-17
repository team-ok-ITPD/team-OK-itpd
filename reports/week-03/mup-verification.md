# Week 3 MUP verification

## Scope and provenance

- Task: [#57](https://github.com/team-ok-ITPD/team-OK-itpd/issues/57).
- Date: 2026-10-17.
- Baseline: `62da3c55e50d0b8ccaea3b3d430a79bb78ab22a7` on `main`.
- Environment: Windows, Python 3.13, pytest 8.4.2, Docker Desktop engine 29.5.2.
- A separate clone was created with `git clone --no-hardlinks`; dependencies
  were installed into a separate virtual environment from `requirements.lock`.
- Results below are team verification, not Customer acceptance. No story is
  closed and no acceptance criterion is changed by this report.

## Executed checks

From the repository root, with the audit virtual environment active:

```powershell
python -m pip install -r requirements.lock
python -m pytest -q
docker compose -p itpd-artem-audit config --quiet
```

Product tests: **7 passed in 2.83 seconds**. Compose configuration validated.
The product tests run the buggy exercise, check the names of failing tests,
and copy the reference solution into a temporary workspace where all exercise
tests must pass. The learner's source is not overwritten.

From `exercise/`, `python -m pytest -q` produced **2 failed, 1 passed**:

```text
test_mixed_numbers: [4, -2, 5] != [4, 5]
test_consecutive_negatives: [-2] != []
```

The documented `pytest -q` entry point, using the same virtual environment,
instead failed collection with `ModuleNotFoundError: remove_negatives`.
This local result needs a corresponding check inside the container.

The catalog was also opened in the in-app browser on a separate local port. The supported request displayed the exercise card; the unsupported concurrency request displayed the expected no-match message. These checks did not open a working debugger workspace.

An actual HTTP server using `CatalogHandler` was started on a temporary local
port and queried with JSON requests:

| Request | Result |
| --- | --- |
| `I want a Python list mutation bug` | HTTP 200, exercise `remove-negatives`, workspace URL returned |
| `A Python concurrency race condition` | HTTP 404, no matching prepared exercise |

The first response was returned without a running workspace container. This
demonstrates that catalog success does not prove workspace readiness.

## Acceptance-criterion matrix

Pass below refers only to the stated automated or source-level evidence.
The complete learner journey still requires the browser rehearsal below.

| Story | AC | Result | Evidence and remaining work |
| --- | --- | --- | --- |
| [US-01 / #28](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28) | AC-01 | Pass at API level | Supported Python list request returns the curated exercise; the browser form also displayed its card and workspace link. |
| US-01 | AC-02 | Pass at API level | Unsupported request returns HTTP 404 and a visible browser error. The handler has no environment-creation operation. |
| [US-02 / #29](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29) | AC-01 | Unverified | Docker is required on the host; clarify the operator/learner boundary and verify the prepared browser environment. |
| US-02 | AC-02 | Gap found | API returns a workspace link even when the workspace is unavailable. It does not check readiness or implement creation-failure cleanup. |
| [US-03 / #30](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30) | AC-01 | Command gap | `python -m pytest -q` shows the intended defect; documented `pytest -q` fails import locally. Container reproduction is unverified. |
| US-03 | AC-02 | Pass at contract level | Product tests check repeatable buggy behavior; the full documented terminal path remains unverified. |
| [US-04 / #31](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31) | AC-01 | Pass at contract level | Reference solution passes the copied exercise tests in a temporary workspace. Manual learner editing remains unverified. |
| US-04 | AC-02 | Pass at contract level | Buggy solution fails named tests; the full documented terminal path remains unverified. |
| [US-05 / #32](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32) | AC-01 | Implementation mismatch | AC requires remote SSH. The shipped start script runs browser code-server, without an SSH service. No named debugger launch configuration is tracked. |
| US-05 | AC-02 | Implementation mismatch | AC requires invalid access to be refused. `scripts/start.sh` explicitly sets `--auth none`. Loopback port binding limits exposure but does not implement authentication. |

## Defects and proposed follow-up

### Missing debugger configuration

`exercise/README.md` tells the learner to select **Debug reproduction tests**.
`git ls-files exercise` contains only the README, source, and tests. The global
`.vscode/` ignore rule excludes exercise-specific settings.

Track `exercise/.vscode/launch.json` and any required interpreter settings using
a narrow ignore exception. Verify a breakpoint, variable inspection, and step
execution in a fresh browser workspace. Installing the debugger extension alone
does not supply the named launch configuration.

### Reproduction command and Python environment

Use `python -m pytest` with the intended Python interpreter, or configure import
paths so the documented entry point behaves consistently. The Dockerfile
installs pytest into `/opt/debug-gym`, but neither it nor the start script adds
that virtual environment to `PATH`; verify what the learner terminal resolves
for both `python` and `pytest` before claiming a working run path.

### Workspace availability

Start the catalog while the workspace is stopped, submit a supported request,
and observe the successful response containing the unavailable workspace URL.
Add a readiness/error path, or agree revised environment-provisioning criteria
with the Customer. A network error for the catalog itself is not evidence of
handling a workspace creation error.

### Configurable catalog port

`compose.yaml` passes `DEBUG_GYM_CATALOG_PORT` to the server, while mapping the
host port to a fixed container port of `3000`. For example, setting the variable
to `3100` makes the server listen on container port `3100` while forwarding to
`3000`. This follows from configuration inspection; it has not been reproduced
in a running container. Keep the internal listening port fixed, or update the
mapping and verify a non-default port.

### Story scope and acceptance

The browser environment and unauthenticated local access differ from US-05's
SSH and access-control criteria. Implement the existing criteria or obtain a
Customer decision before editing them. Do not mark the story accepted based
on the Week 3 Figma feedback.

## Container build attempt

Docker Desktop was started and the baseline image build was attempted. The build was cancelled after approximately five minutes while still downloading base-image layers slowly. No image build or running-container result is claimed from this machine; this was not a demonstrated build failure. The missing debugger configuration and setup page already prevent signing off the documented end-to-end workflow. The existing remote CI build is supporting evidence, not a substitute for the pending browser rehearsal.

## Remaining manual rehearsal

These steps are pending and must not be reported as completed:

1. Build and start the isolated Compose project from a clean clone.
2. Open the catalog, submit the supported and unsupported requests, and open
   the prepared workspace.
3. Check the terminal's interpreter and pytest availability, then run the
   documented reproduction command twice and compare symptoms.
4. Set a breakpoint, inspect the list and loop position, and step execution.
5. Fix `remove_negatives.py` manually and confirm all three tests pass.
6. Reset only the disposable audit workspace volume, restart it, and confirm
   the original broken exercise is restored. Reset deletes learner edits.
7. Stop the workspace and verify the user's error path; test invalid access
   against the agreed criteria.
8. Repeat using `docs/setup.md` after task
   [#56](https://github.com/team-ok-ITPD/team-OK-itpd/issues/56) merges.

At the audited baseline, `docs/setup.md` does not exist. The clean-checkout
instruction requirement therefore cannot be signed off yet.

## AI assistance

Codex inspected the repository and public GitHub evidence, executed the
reported local checks, and drafted this report. This artifact does not claim
that its author manually completed the browser workflow or obtained Customer
acceptance. The team should review the commands, evidence, and proposed
follow-up before using them in the weekly report.
