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

The Docker host needs these tools. The learner uses the prepared browser
workspace and does not install Python or VS Code locally. This is a local,
single-learner prototype: the workspace has no login and its published ports
are bound to loopback. Keep it on your own machine.

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

## Start and check readiness

From the repository root:

```sh
docker compose -p debug-gym-local config --quiet
docker compose -p debug-gym-local up --build -d
docker compose -p debug-gym-local ps
docker compose -p debug-gym-local logs --tail 100
```

The initial build downloads a code-server image, Python dependencies, and
debugger extensions; it can take several minutes. A successful catalog request
does not prove that VS Code is ready. Open both health URLs in the browser:

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
4. Prepare the debugger manually. The baseline does not track the named launch
    configuration mentioned in the exercise README. In VS Code's Explorer,
    create `.vscode/launch.json` inside `/home/coder/project` with:

    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "name": "Debug reproduction tests",
          "type": "debugpy",
          "request": "launch",
          "python": "/opt/debug-gym/bin/python",
          "module": "pytest",
          "args": ["-q", "-s", "tests/test_remove_negatives.py"],
          "cwd": "${workspaceFolder}",
          "console": "integratedTerminal",
          "justMyCode": true
        }
      ]
    }
    ```

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

This manual debugger setup is a workaround, not evidence that all user-story
acceptance criteria are met. This version offers browser VS Code, not SSH;
invalid-access rejection and automatic workspace provisioning are not provided.

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
| Image or extension download fails | Check network access and inspect build output; retry `docker compose -p debug-gym-local build`. |
| A port is already allocated | Stop the conflicting process. For workspace port changes, update both workspace variables in `.env`. |
| Catalog works but VS Code does not | Check workspace health and Compose logs. The catalog currently does not detect workspace readiness. |
| `pytest` is missing or imports fail | Use `/opt/debug-gym/bin/python -m pytest -q` from `/home/coder/project` in the container. |
| No debugger launch configuration exists | Follow the manual `.vscode/launch.json` step above. |
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

Shell scripts use LF through `.gitattributes` so a Windows checkout does not
break the Linux container entry point.