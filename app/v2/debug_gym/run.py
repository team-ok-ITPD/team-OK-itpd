#!/usr/bin/env python3
# [Shared] One-command launcher for Debug Gym v2 on Windows, macOS and Linux
"""Set up and start Debug Gym v2 from any folder.

    python run.py            # create .venv, install, migrate, start, open browser
    python run.py --demo     # also create demo accounts and sample data
    python run.py --test     # run the Django test suite instead of the server

On Windows use `py run.py` if `python` is not on PATH; on macOS or Linux use
`python3 run.py`. Only the Python standard library is needed to start it.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import venv
import webbrowser
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_DIR = PROJECT_DIR / ".venv"
REQUIREMENTS = PROJECT_DIR / "requirements.txt"
STAMP = VENV_DIR / ".requirements.sha256"
MIN_PYTHON = (3, 10)  # Django 5.2 needs Python 3.10 or newer
DEMO_PASSWORD = "debug-gym-pass"

# Runs inside the project through `manage.py shell -c`; safe to repeat.
DEMO_SEED = f'''
from datetime import timedelta

from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, User

PASSWORD = "{DEMO_PASSWORD}"


def account(email, name, role):
    user = User.objects.filter(email__iexact=email).first()
    if user is None:
        user = User.objects.create_user(email, name, PASSWORD, role=role)
    return user


admin = account("admin@example.com", "Demo Admin", User.Role.ADMIN)
prof = account("prof@example.com", "Demo Professor", User.Role.PROFESSOR)
ali = account("ali@example.com", "Ali", User.Role.STUDENT)
omar = account("omar@example.com", "Omar", User.Role.STUDENT)

group, _ = StudyGroup.objects.get_or_create(name="Demo Group", defaults={{"professor": prof}})
group.students.add(ali, omar)

private_bug, _ = Bug.objects.get_or_create(
    title="Off by one",
    defaults=dict(
        description="The loop skips the last item. Fix it so every item is processed.",
        buggy_code="def total(xs):\\n    t = 0\\n    for i in range(len(xs) - 1):\\n        t += xs[i]\\n    return t\\n",
        language="python",
        difficulty=Bug.Difficulty.EASY,
        visibility=Bug.Visibility.PRIVATE,
        created_by=prof,
    ),
)
Bug.objects.get_or_create(
    title="Mutable default argument",
    defaults=dict(
        description="Calls share one list. Make each call start with its own empty list.",
        buggy_code="def add(x, items=[]):\\n    items.append(x)\\n    return items\\n",
        language="python",
        difficulty=Bug.Difficulty.MEDIUM,
        visibility=Bug.Visibility.PUBLIC,
        created_by=prof,
    ),
)

assignment, created = Assignment.objects.get_or_create(
    title="Demo assignment: off by one",
    defaults=dict(
        bug=private_bug,
        professor=prof,
        instructions="Find the bug and submit your fix.",
        deadline=timezone.now() + timedelta(days=7),
    ),
)
assignment.groups.add(group)
print("Demo data ready.")
'''


def say(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> "None":
    say(f"\nError: {message}")
    sys.exit(1)


def venv_python() -> Path:
    folder = "Scripts" if os.name == "nt" else "bin"
    name = "python.exe" if os.name == "nt" else "python"
    return VENV_DIR / folder / name


def check_python() -> None:
    if sys.version_info < MIN_PYTHON:
        found = ".".join(str(n) for n in sys.version_info[:3])
        need = ".".join(str(n) for n in MIN_PYTHON)
        fail(f"Python {need} or newer is required (this is {found}). Install it from python.org.")


def ensure_venv() -> Path:
    python = venv_python()
    if not python.exists():
        say("Creating the virtual environment (.venv)...")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    if not python.exists():
        fail("The virtual environment was created but its Python is missing. Delete .venv and retry.")
    return python


def ensure_requirements(python: Path) -> None:
    digest = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
    if STAMP.exists() and STAMP.read_text().strip() == digest:
        return
    say("Installing dependencies (needs an internet connection the first time)...")
    result = subprocess.run(
        [str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(REQUIREMENTS)],
        cwd=PROJECT_DIR,
    )
    if result.returncode != 0:
        fail("pip could not install the dependencies. Check your network and retry.")
    STAMP.write_text(digest)


def manage(python: Path, *args: str, check: bool = True) -> int:
    result = subprocess.run([str(python), "manage.py", *args], cwd=PROJECT_DIR)
    if check and result.returncode != 0:
        fail(f"`manage.py {' '.join(args)}` failed (exit code {result.returncode}).")
    return result.returncode


def port_is_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) != 0


def wait_then_open(url: str, probe: str, open_browser: bool, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(probe, timeout=2).close()
        except urllib.error.HTTPError:
            break  # any HTTP answer means the server is up
        except OSError:
            time.sleep(0.5)
            continue
        else:
            break
    else:
        return
    say(f"\nDebug Gym is running at {url}  (press Ctrl+C to stop)")
    if open_browser:
        webbrowser.open(url)


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up and run Debug Gym v2.")
    parser.add_argument("--port", type=int, default=8000, help="port for the dev server (default 8000)")
    parser.add_argument("--demo", action="store_true", help="create demo accounts and sample data")
    parser.add_argument("--test", action="store_true", help="run the Django tests and exit")
    parser.add_argument("--no-browser", action="store_true", help="do not open the browser")
    args = parser.parse_args()

    check_python()
    python = ensure_venv()
    ensure_requirements(python)

    if args.test:
        return manage(python, "test", check=False)

    manage(python, "migrate", "--noinput")

    if args.demo:
        if os.environ.get("DJANGO_DEBUG", "1") != "1":
            fail("--demo only runs with DJANGO_DEBUG=1 because it creates accounts with a known password.")
        manage(python, "shell", "-c", DEMO_SEED)
        say(f"\nDemo accounts (password: {DEMO_PASSWORD})")
        say("  admin@example.com   admin")
        say("  prof@example.com    professor")
        say("  ali@example.com     student")
        say("  omar@example.com    student")
    else:
        count = subprocess.run(
            [str(python), "manage.py", "shell", "-c",
             "from core.models import User; print(User.objects.count())"],
            cwd=PROJECT_DIR, capture_output=True, text=True,
        )
        if count.returncode == 0 and count.stdout.strip() == "0":
            say("\nNo accounts exist yet. Re-run with --demo, or create an admin with:")
            say("  python manage.py createsuperuser   (from the activated .venv)")

    host = "127.0.0.1"
    if not port_is_free(host, args.port):
        fail(f"Port {args.port} is already in use. Stop that program or pass --port <number>.")

    url = f"http://{host}:{args.port}/"
    threading.Thread(
        target=wait_then_open,
        args=(url, url + "accounts/login/", not args.no_browser),
        daemon=True,
    ).start()
    try:
        return subprocess.run(
            [str(python), "manage.py", "runserver", f"{host}:{args.port}"], cwd=PROJECT_DIR
        ).returncode
    except KeyboardInterrupt:
        say("\nStopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
