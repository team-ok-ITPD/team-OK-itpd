# [Backend Dev] Project validation shared by import, generation and author saves
from pathlib import PurePosixPath


class ProjectError(ValueError):
    pass


def validate_project(files, entry_file):
    if not isinstance(files, dict) or not 1 <= len(files) <= 100:
        raise ProjectError("A project must contain between 1 and 100 text files.")
    total = 0
    for name, content in files.items():
        if not isinstance(name, str) or not isinstance(content, str):
            raise ProjectError("Project paths and file contents must be text.")
        path = PurePosixPath(name)
        if (
            not name or len(name) > 255 or str(path) != name
            or path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name
            or any(part in (".git", ".debug-gym", ".env", "node_modules", "__pycache__") for part in path.parts)
        ):
            raise ProjectError("Use regular relative project paths without secrets or generated files.")
        total += len(content.encode("utf-8"))
    if total > 5_000_000:
        raise ProjectError("The project exceeds 5 MB.")
    if entry_file not in files:
        raise ProjectError("The source entry file is missing from the project.")
    return files


def entry_path(bug):
    if bug.entry_file:
        return bug.entry_file
    matches = [name for name, source in bug.project_files.items() if source == bug.buggy_code]
    return matches[0] if matches else "main.py"


def project_files(bug):
    files = dict(bug.project_files or {entry_path(bug): bug.buggy_code})
    if bug.tests_code and not any(
        name.endswith(".py") and PurePosixPath(name).name.startswith("test_")
        for name in files
    ):
        files["test_main.py"] = bug.tests_code
    return files


def python_test_files(files):
    return [
        name for name in files
        if name.endswith(".py") and PurePosixPath(name).name.startswith("test_")
    ]
