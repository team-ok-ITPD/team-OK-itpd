# Setup and run

Debug GYM currently provides one prepared Python list-mutation exercise.
Run the catalog and browser-based VS Code together on your own computer.
The documentation site describes the product; it does not host the exercise.

## Prerequisites

- Git.
- Docker Desktop with the Linux engine running, or Docker Engine with Compose v2
  on Linux. Check `docker version` and `docker compose version` first.
- A modern browser, an internet connection for the first image build, and free
  host ports 3000 and 8080.

The manual Docker Compose path needs only those tools. The optional launchers
under `runners/` also need host Python 3 and `curl` on `PATH`. The learner does
not install Python or VS Code for use inside the prepared workspace.

This is a local, single-learner prototype: the workspace has no login and its
published ports are bound to loopback. Keep it on your own machine. It does not
provide the remote SSH or invalid-access rejection required by
[FR-005](functional-requirements/fr/FR-005.md).

## Install and configure

Clone a fresh copy and enter its directory:

```sh
git clone https://github.com/team-ok-ITPD/team-OK-itpd.git
cd team-OK-itpd
```

Create `.env` from the tracked [`.env.example`](../.env.example).
In PowerShell:

```powershell
Copy-Item .env.example .env
```

On macOS or Linux:

```sh
cp .env.example .env
```

The current configuration is:

| Variable | Default | Meaning |
| --- | --- | --- |
| `DEBUG_GYM_CATALOG_PORT` | `3000` | Catalog port. Keep this at 3000: the current Compose mapping has a fixed internal target of 3000. |
| `DEBUG_GYM_WORKSPACE_PORT` | `8080` | Host port for browser VS Code. |
| `DEBUG_GYM_WORKSPACE_URL` | `http://localhost:8080` | Link the catalog presents to the learner. Update it if the workspace host port changes. |

No API key is required for the prepared exercise. Keep `.env` local; it is
ignored by Git. If port 3000 is occupied, stop the conflicting service before
starting this version rather than changing its catalog port.

## Optional launchers

The launchers create `.env` from `.env.example` when it is absent, run Docker
Compose with project name `debug-gym-local`, wait for both health endpoints and
open the catalog.

On Windows, from the repository root:

```bat
runners\run_debug_gym.bat
```

On macOS or Linux, from the repository root:

```sh
bash runners/run_debug_gym.command
```

The tracked macOS file is not currently executable, so invoking it directly as
`./runners/run_debug_gym.command` fails. The launchers also check fixed URLs on
ports 3000 and 8080. Use the manual Compose path below when using a different
workspace host port. These are known launcher limitations, not evidence that
Docker or the product failed to start.

## Start and check readiness

From the repository root:

```sh
docker compose -p debug-gym-local config --quiet
docker compose -p debug-gym-local up --build -d
docker compose -p debug-gym-local ps
docker compose -p debug-gym-local logs --tail 100
```

The initial build downloads a code-server image, Python dependencies, and
debugger extensions; it can take several minutes. The catalog checks workspace
health before returning a supported exercise, but the two endpoints can also be
checked independently:

- Catalog: `http://localhost:3000/health`, expected `{"status": "ok"}`.
- Workspace: `http://localhost:8080/healthz`, expected an HTTP success response.

Open `http://localhost:3000` once both are ready.

## Complete the learner task

1. Submit `A Python list mutation bug with negative numbers`. The catalog shows
    **The surviving negative**. An unsupported request such as
    `A Python concurrency race condition` should show a no-match message.
2. Choose **Open prepared workspace**. Browser VS Code opens the exercise at
    `/home/coder/project`. Open `README.md` and `remove_negatives.py`.
3. Open **Terminal > New Terminal** and reproduce the bug twice:

    ```sh
    cd /home/coder/project
    /opt/debug-gym/bin/python -m pytest -q
    /opt/debug-gym/bin/python -m pytest -q
    ```

    Both runs should report `test_mixed_numbers` and
    `test_consecutive_negatives` failing, with one test passing. The absolute
    interpreter path uses the installed pytest environment; do not rely on a
    bare `pytest` command being available in the terminal.
4. Open **Run and Debug**. A fresh workspace contains the tracked
    [`Debug reproduction tests`](../exercise/.vscode/launch.json)
    configuration. Docker preserves an existing named volume across image
    rebuilds, so a workspace created by an older version may not receive this
    file. Do not reset the volume merely to repair the configuration: save the
    learner's edits first, then copy the tracked configuration into the
    workspace or recreate it through VS Code.

5. Set a breakpoint inside the loop in `remove_negatives.py`. Open **Run and
    Debug**, select **Debug reproduction tests**, and press F5. Inspect the
    list and step through iterations to see why adjacent negative values survive.
    If a workspace-trust prompt appears, review the checked-out code before
    choosing whether to trust this local exercise.
6. Edit and save `remove_negatives.py` so the function removes every negative
    number, including consecutive negative numbers. The learner performs the
    investigation and fix; the product does not apply it automatically.
7. Run `/opt/debug-gym/bin/python -m pytest -q` again. Completion means
    **3 passed**. Inspect the full terminal output if a test still fails.

The debugger demonstration is not evidence that all user-story acceptance
criteria are met. This version offers browser VS Code, not SSH; invalid-access
rejection and automatic per-learner workspace provisioning are not provided.
Agent assistance and category browsing are specified by FR-006 and FR-007 but
are not implemented by this MUP.

## Stop and reset

Stop the local project while preserving learner edits:

```sh
docker compose -p debug-gym-local down
```

To start the same saved exercise again, run
`docker compose -p debug-gym-local up -d`.

To discard learner edits and restore the original broken exercise, first copy
out anything you need. The following removes the **debug-gym-local** project's
exercise volume, including the manually created debugger configuration:

```sh
docker compose -p debug-gym-local down --volumes
docker compose -p debug-gym-local up --build -d
```

Reopen VS Code and repeat reproduction. Expect the original two failing tests.
Rebuilding an image alone does not reset an existing named workspace volume.

## Product checks

For contributors, install local Python 3.12 or newer and create a virtual
environment from the repository root:

```sh
python -m venv .venv
```

Activate it in PowerShell with `.venv\Scripts\Activate.ps1`, or on macOS/Linux
with `source .venv/bin/activate`. If activation is unavailable, invoke the
virtual environment's Python executable directly.

```sh
python -m pip install -r requirements.lock
python -m pytest -q
```

The product suite should pass. The exercise's intentional failures are checked
by the suite and do not mean the product suite should fail.

Markdown and repository links are checked on every pull request by the
**Markdown check** and **Check Links** GitHub Actions workflows. Contributors
with Node.js can also run the same Markdown checker locally:

```sh
npx --yes markdownlint-cli2@0.20.0 "**/*.md"
```

## Build and preview the documentation

In the activated contributor environment:

```sh
python -m pip install -r requirements-docs.txt
python -m mkdocs build --strict
python -m mkdocs serve
```

Open the local address printed by MkDocs. The site is mounted under
`/team-OK-itpd/`. `site/` is generated output and must not be committed.

The **Documentation site** workflow builds on pull requests and deploys only
from `main` or a manual run on `main`. A repository administrator must select
**Settings > Pages > Build and deployment > Source: GitHub Actions** before
the first deployment. The workflow uses the `github-pages` environment.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Docker daemon is unavailable | Start Docker Desktop and select its Linux engine, then retry `docker version`. |
| A launcher reports that Docker is unavailable | Run `docker info` and `docker compose version` directly; the current launcher groups several Docker and dependency failures under the same troubleshooting text. |
| `run_debug_gym.command` is not executable | Run `bash runners/run_debug_gym.command`; direct execution is a known limitation of the tracked file mode. |
| A launcher times out after changing ports | Use the manual Compose path and open the URLs configured in `.env`; launcher health checks currently use ports 3000 and 8080. |
| Image or extension download fails | Check network access and inspect build output; retry `docker compose -p debug-gym-local build`. |
| A port is already allocated | Stop the conflicting process. For workspace port changes, update both workspace variables in `.env`. |
| Compose fails with `all predefined address pools have been fully subnetted` | Docker has run out of networks. Run `docker network prune`, which removes every unused Docker network on the machine, then repeat `docker compose -p debug-gym-local up --build -d`. |
| A supported catalog request reports an unavailable workspace | Open the workspace health URL and inspect Compose logs; the catalog checks readiness before returning the exercise. |
| `pytest` is missing or imports fail | Use `/opt/debug-gym/bin/python -m pytest -q` from `/home/coder/project` in the container. |
| No debugger launch configuration exists | Preserve learner edits and copy the tracked `exercise/.vscode/launch.json` into the workspace; an older named volume can hide files added to a newer image. |
| Old edited exercise survives a rebuild | Reset the named volume only after saving the learner's work. |

## Verification record

On 2026-10-17, the setup rehearsal on Windows with Docker Desktop confirmed:

- The image built and both catalog and workspace health endpoints responded.
- The container's exercise tests failed twice with the same two named failures.
- The installed debugpy adapter stopped at a breakpoint, exposed `number` and
  `numbers`, and completed a step-over through the Debug Adapter Protocol.
- Copying the reference solution into the disposable workspace produced
  `3 passed`; removing only that project's volume restored the original
  `2 failed, 1 passed` state.
- Browser VS Code loaded. The complete manual F5 interaction remains a reviewer
  check; adapter verification is not a claim of Customer acceptance.

On 2026-10-24, a clean macOS 26.6.2 ARM checkout built and opened the catalog
and workspace through `bash runners/run_debug_gym.command`; both health
endpoints, the catalog match and the expected `2 failed, 1 passed` exercise
result were verified. Direct macOS execution remained blocked by the tracked
non-executable file mode. The team marked Windows and Linux as verified in
issue #82, but the repository does not contain their command-level platform
logs. These checks are not Customer acceptance.

Shell scripts use LF through `.gitattributes` so a Windows checkout does not
break the Linux container entry point.
