# [Student Dev] Write a student's VS Code folder for one bug (ported from app/adel_b)
"""One folder per student and bug (or assignment):

    main.<ext>               the code; written once, then the student's own edits are kept
    test_main.py             the bug's tests (Python bugs with tests only)
    .vscode/launch.json      debugger setup
    .vscode/settings.json    Python interpreter of the VS Code image
    .debug-gym/config.json   where and as whom the extension submits (private token)
"""
import json
from pathlib import Path

from django.conf import settings

from .models import IdeToken

# The Python venv inside the VS Code image (app/v2/ide/Dockerfile).
VENV_PYTHON = "/opt/debug-gym/bin/python"
TESTS_FILE = "test_main.py"
EXTENSIONS = {
    "python": "py", "javascript": "js", "typescript": "ts", "dart": "dart",
    "java": "java", "c": "c", "cpp": "cpp", "c++": "cpp", "go": "go", "kotlin": "kt",
}


def code_file_name(bug):
    return f"main.{EXTENSIONS.get(bug.language.lower(), 'txt')}"


def has_tests(bug):
    """Tests run only for Python bugs: the VS Code image has Python and pytest only."""
    return bug.language.lower() == "python" and bool(bug.tests_code.strip())


def workspace_dir(student, bug, assignment=None):
    work = f"assignment-{assignment.pk}" if assignment else f"practice-{bug.pk}"
    return Path(settings.WORKSPACES_DIR) / str(student.pk) / work


def write_workspace(student, bug, *, assignment=None, start_code, site_url):
    """Prepare the folder and return it. `start_code` fills main.* the first time only."""
    folder = workspace_dir(student, bug, assignment)
    (folder / ".vscode").mkdir(parents=True, exist_ok=True)
    (folder / ".debug-gym").mkdir(exist_ok=True)

    code_path = folder / code_file_name(bug)
    if not code_path.exists():
        code_path.write_text(start_code if start_code.endswith("\n") else start_code + "\n")

    tests_path = folder / TESTS_FILE
    if has_tests(bug):
        # Always the current tests: a professor may have improved them.
        tests_path.write_text(bug.tests_code if bug.tests_code.endswith("\n") else bug.tests_code + "\n")
    elif tests_path.exists():
        tests_path.unlink()

    _write_vscode_config(folder, bug)
    _write_extension_config(folder, student, bug, assignment, site_url)
    return folder


def _write_vscode_config(folder, bug):
    if has_tests(bug):
        configuration = {
            "name": "Debug the tests", "type": "debugpy", "request": "launch",
            "module": "pytest", "args": ["-q"], "cwd": "${workspaceFolder}", "python": VENV_PYTHON,
        }
    else:
        configuration = {
            "name": "Run main.py", "type": "debugpy", "request": "launch",
            "program": "${workspaceFolder}/main.py", "cwd": "${workspaceFolder}", "python": VENV_PYTHON,
        }
    launch = {"version": "0.2.0", "configurations": [configuration] if bug.language.lower() == "python" else []}
    (folder / ".vscode" / "launch.json").write_text(json.dumps(launch, indent=2) + "\n")
    workspace_settings = {"python.defaultInterpreterPath": VENV_PYTHON, "files.exclude": {".debug-gym": True}}
    (folder / ".vscode" / "settings.json").write_text(json.dumps(workspace_settings, indent=2) + "\n")


def _write_extension_config(folder, student, bug, assignment, site_url):
    """Tell the extension where and as whom to submit; replaces any older token."""
    config = {
        "server": settings.DEBUG_GYM_IDE_SERVER_URL,
        "site": site_url,
        "title": assignment.title if assignment else bug.title,
        "file": code_file_name(bug),
        "tests": has_tests(bug),
        # code-server resets PATH for extensions, so name the image's Python exactly.
        "python": VENV_PYTHON,
        "token": IdeToken.issue(student, bug, assignment),
    }
    path = folder / ".debug-gym" / "config.json"
    path.write_text(json.dumps(config, indent=2) + "\n")
    path.chmod(0o600)
