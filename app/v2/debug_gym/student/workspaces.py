# [Student Dev] Write a student's VS Code folder for one bug (ported from app/adel_b)
"""One folder per student and bug (or assignment), built from the bug's project files
(core.projects, shared with the professor pages):

    <entry file>             the code to fix; written once, then the student's edits are kept
    test_*.py, *.test.js     the bug's test files; refreshed on every open
    other project files      written once
    .vscode/launch.json      debugger setup (Python)
    .vscode/settings.json    Python interpreter of the VS Code image
    .debug-gym/config.json   where and as whom the extension submits (private token)
"""
import json
from pathlib import Path, PurePosixPath

from django.conf import settings

from core.projects import entry_path, project_files, validate_project

from .ide import IdeError
from .models import IdeToken

# The Python venv inside the student VS Code image (app/v2/ide/Dockerfile).
VENV_PYTHON = "/opt/debug-gym/bin/python"


EXTENSIONS = {
    "python": "py", "javascript": "js", "typescript": "ts", "dart": "dart",
    "java": "java", "c": "c", "cpp": "cpp", "c++": "cpp", "go": "go", "kotlin": "kt",
}
TESTS_FILE = "test_main.py"


def code_file_name(bug):
    return entry_path(bug)


def default_entry(language):
    return f"main.{EXTENSIONS.get(language.lower(), 'txt')}"


def build_project(language, buggy_code, tests_code="", base=None):
    """Project files and entry file for a one-file bug plus optional Python tests.

    `base` is the bug's current project_files: other files in it are kept.
    Returns (project_files, entry_file).
    """
    files = dict(base or {})
    entry = default_entry(language)
    for name in list(files):
        if name.startswith("main.") and name != entry:
            del files[name]  # the language changed
    files[entry] = buggy_code
    if tests_code.strip() and language.lower() in ("python", "python3", "python 3"):
        files[TESTS_FILE] = tests_code
    else:
        files.pop(TESTS_FILE, None)
    return files, entry


def bug_tests_code(bug):
    """The text of a one-file bug's test file, for the edit form."""
    return (bug.project_files or {}).get(TESTS_FILE, "")


def is_test_file(name):
    file = PurePosixPath(name).name
    return (file.startswith("test_") and file.endswith(".py")) or file.endswith((".test.js", ".test.mjs", ".test.cjs"))


def project_has_tests(bug):
    """Whether the server can verify submissions (core.runtime.verify needs test files)."""
    return any(is_test_file(name) for name in project_files(bug))


def has_tests(bug):
    """Whether the Test button works in VS Code: the student image has Python and pytest only."""
    return bug.language.lower() in ("python", "python3", "python 3") and any(
        PurePosixPath(name).name.startswith("test_") for name in project_files(bug) if is_test_file(name)
    )


def workspace_dir(student, bug, assignment=None):
    work = f"assignment-{assignment.pk}" if assignment else f"practice-{bug.pk}"
    return Path(settings.STUDENT_WORKSPACES_DIR) / str(student.pk) / work


def write_workspace(student, bug, *, assignment=None, start_code, site_url, server_url=None):
    """Prepare the folder and return it. `start_code` fills the entry file the first time only."""
    files = project_files(bug)
    entry = entry_path(bug)
    try:
        validate_project(files, entry)
    except ValueError as error:
        raise IdeError(f"This bug's project files are not valid: {error}") from error

    folder = workspace_dir(student, bug, assignment)
    (folder / ".vscode").mkdir(parents=True, exist_ok=True)
    (folder / ".debug-gym").mkdir(exist_ok=True)
    for name, source in files.items():
        path = folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if name == entry:
            text = start_code
        elif is_test_file(name):
            text = source  # always the current tests: a professor may have improved them
        elif path.exists():
            continue
        else:
            text = source
        if name == entry and path.exists():
            continue  # keep the student's work in progress
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")

    # Remove test files we wrote earlier that the bug no longer has. Only ours:
    # a student may have written test files of their own.
    record = folder / ".debug-gym" / "managed-tests.json"
    try:
        previous = set(json.loads(record.read_text()))
    except (OSError, ValueError):
        previous = set()
    current = {name for name in files if is_test_file(name)}
    for name in previous - current:
        stale = folder / name
        if stale.is_file() and stale.resolve().is_relative_to(folder.resolve()):
            stale.unlink()
    record.write_text(json.dumps(sorted(current)))

    _write_vscode_config(folder, bug)
    _write_extension_config(folder, student, bug, assignment, site_url, server_url)
    return folder


def _write_vscode_config(folder, bug):
    if has_tests(bug):
        configuration = {
            "name": "Debug the tests", "type": "debugpy", "request": "launch",
            "module": "pytest", "args": ["-q"], "cwd": "${workspaceFolder}", "python": VENV_PYTHON,
        }
    else:
        configuration = {
            "name": f"Run {entry_path(bug)}", "type": "debugpy", "request": "launch",
            "program": "${workspaceFolder}/" + entry_path(bug), "cwd": "${workspaceFolder}", "python": VENV_PYTHON,
        }
    python = bug.language.lower() in ("python", "python3", "python 3")
    launch = {"version": "0.2.0", "configurations": [configuration] if python else []}
    (folder / ".vscode" / "launch.json").write_text(json.dumps(launch, indent=2) + "\n")
    workspace_settings = {"python.defaultInterpreterPath": VENV_PYTHON, "files.exclude": {".debug-gym": True}}
    (folder / ".vscode" / "settings.json").write_text(json.dumps(workspace_settings, indent=2) + "\n")


def _write_extension_config(folder, student, bug, assignment, site_url, server_url=None):
    """Tell the extension where and as whom to submit; replaces any older token."""
    config = {
        "server": server_url or settings.DEBUG_GYM_IDE_SERVER_URL,
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
