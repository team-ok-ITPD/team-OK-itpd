#!/usr/bin/env python3
"""Start Debug GYM from the repo root and open the catalog."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = REPO_ROOT / ".env"
ENV_EXAMPLE = REPO_ROOT / ".env.example"
CATALOG_URL = "http://localhost:3000"
WORKSPACE_URL = "http://localhost:8080"

def ensure_env() -> None:
    if ENV_FILE.exists():
        return
    if not ENV_EXAMPLE.exists():
        raise FileNotFoundError(f"Missing .env.example at {ENV_EXAMPLE}")
    shutil.copy2(ENV_EXAMPLE, ENV_FILE)
    print("Created .env from .env.example")

def ensure_docker() -> None:
    if shutil.which("docker") is None:
        raise RuntimeError("Docker is not installed or not on PATH.")
    result = subprocess.run(["docker", "info"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Docker is not running. Start Docker Desktop or Docker Engine first.")

def run_compose() -> None:
    print("Starting Debug GYM...")
    subprocess.run(
        ["docker", "compose", "-p", "debug-gym-local", "up", "--build", "-d"],
        cwd=str(REPO_ROOT),
        check=True,
    )

def wait_until_ready(timeout_seconds: int = 180) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        catalog_ok = subprocess.run(
            ["curl", "-fsS", f"{CATALOG_URL}/health"],
            capture_output=True,
            text=True,
        ).returncode == 0
        workspace_ok = subprocess.run(
            ["curl", "-fsS", f"{WORKSPACE_URL}/healthz"],
            capture_output=True,
            text=True,
        ).returncode == 0
        if catalog_ok and workspace_ok:
            return True
        time.sleep(2)
    return False

def main() -> int:
    try:
        ensure_env()
        ensure_docker()
        run_compose()
        print("Waiting for services to be ready...")
        if not wait_until_ready():
            print("Startup timed out. Check:")
            print("docker compose -p debug-gym-local logs --tail 100")
            return 1

        try:
            webbrowser.open(CATALOG_URL, new=2)
        except Exception:
            pass

        print("\nDebug GYM is ready.")
        print(f"Catalog: {CATALOG_URL}")
        print(f"Workspace: {WORKSPACE_URL}")
        print("Stop later with: docker compose -p debug-gym-local down")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("\nTroubleshooting:")
        print("1. Docker is not running.")
        print("2. Docker is not on PATH.")
        print("3. Run: docker compose -p debug-gym-local logs --tail 100")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())