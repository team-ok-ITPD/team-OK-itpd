# [Backend Dev] Isolated test execution and shared browser VS Code launcher
import hashlib
import json
import tempfile
import threading
import shlex
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from xml.etree import ElementTree

import docker
from requests.exceptions import RequestException
from django.conf import settings

from app.adel_b.bugs.ide import IdeError, start_ide
from app.adel_b.bugs.verification import VerificationGate
from .projects import entry_path, project_files, python_test_files, validate_project

gate = VerificationGate(concurrency=2, queue_size=8, wait_timeout=10)
workspace_lock = threading.Lock()


class RuntimeError(ValueError):
    pass


def verify(bug, code):
    language = bug.language.lower()
    if language not in ("python", "python3", "python 3", "javascript"):
        raise RuntimeError("Automatic verification supports Python and JavaScript projects.")
    files = dict(project_files(bug))
    entry = entry_path(bug)
    files[entry] = code
    validate_project(files, entry)
    if language == "javascript":
        test_files = [name for name in files if name.endswith((".test.js", ".test.mjs", ".test.cjs"))]
        entrypoint = ["/usr/lib/code-server/lib/node"]
        command = ["--test", "--test-reporter=junit", "--test-reporter-destination=/tmp/report.xml"]
    else:
        test_files = python_test_files(files)
        entrypoint = ["/opt/debug-gym/bin/python"]
        command = ["-m", "pytest", "-q", "-p", "no:cacheprovider", "--junitxml=/tmp/report.xml"]
    if not test_files:
        raise RuntimeError("Add test files to this exercise before submitting solutions.")
    with gate.slot(), tempfile.TemporaryDirectory(prefix="debug-gym-v2-tests-") as directory:
        root = Path(directory)
        root.chmod(0o755)
        for name, source in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
        container = None
        try:
            client = docker.from_env()
            container = client.containers.run(
                settings.DEBUG_GYM_IDE_IMAGE,
                entrypoint=["/bin/sh", "-c"],
                command=[
                    shlex.join(entrypoint + command)
                    + " > /tmp/test-output 2>&1; result=$?; cat /tmp/report.xml; exit $result",
                ],
                working_dir=str(PurePosixPath("/work") / PurePosixPath(entry).parent),
                environment={"PYTHONDONTWRITEBYTECODE": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
                volumes={str(root): {"bind": "/work", "mode": "ro"}},
                detach=True, network_disabled=True, read_only=True,
                mem_limit="256m", nano_cpus=500_000_000, pids_limit=64,
                security_opt=["no-new-privileges:true"], cap_drop=["ALL"],
                tmpfs={"/tmp": "rw,noexec,nosuid,size=32m"},
            )
            outcome = container.wait(timeout=35)
            if outcome.get("StatusCode") not in (0, 1):
                raise RuntimeError("Tests could not be collected or executed. Check the exercise test files.")
            report = bytearray()
            for chunk in container.logs(stream=True, stdout=True, stderr=False):
                report.extend(chunk)
                if len(report) > 2_000_000:
                    raise RuntimeError("The test report exceeded the size limit.")
            tree = ElementTree.fromstring(report)
            cases = list(tree.iter("testcase"))
            total = len(cases)
            if not total:
                raise RuntimeError("The exercise did not run any tests.")
            passed = sum(not any(case.find(kind) is not None for kind in ("failure", "error", "skipped")) for case in cases)
            return passed, total
        except (docker.errors.DockerException, RequestException, OSError, ElementTree.ParseError, KeyError):
            raise RuntimeError("Verification is unavailable. Check Docker and the Debug GYM workspace image.")
        finally:
            if container is not None:
                try:
                    container.remove(force=True)
                except docker.errors.NotFound:
                    pass


def open_workspace(session, token):
    bug = session.bug
    folder = settings.DEBUG_GYM_WORKSPACES_DIR / str(session.pk)
    files = project_files(bug)
    validate_project(files, entry_path(bug))
    with workspace_lock:
        folder.mkdir(parents=True, exist_ok=True)
        for name, source in files.items():
            target = folder / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text(source, encoding="utf-8")
        if not session.authoring:
            latest = bug.submissions.filter(
                student=session.user, assignment=session.assignment,
            ).first()
            if latest and not (folder / ".debug-gym/config.json").exists():
                (folder / entry_path(bug)).write_text(latest.submitted_code, encoding="utf-8")
        config = {
            "server": settings.DEBUG_GYM_IDE_SERVER_URL,
            "site": settings.DEBUG_GYM_SITE_URL + (
                f"/professor/bugs/{bug.pk}/" if session.authoring else
                f"/student/assignments/{session.assignment_id}/" if session.assignment_id else "/student/results/"
            ),
            "bug": bug.pk, "file": entry_path(bug), "token": token,
            "mode": "author" if session.authoring else "student", "protocol": 2,
            "testRoot": str(PurePosixPath(entry_path(bug)).parent),
            "revision": session.revision,
            "language": bug.language.lower(),
        }
        (folder / ".debug-gym").mkdir(exist_ok=True)
        (folder / ".debug-gym/config.json").write_text(json.dumps(config), encoding="utf-8")
        (folder / ".vscode").mkdir(exist_ok=True)
        (folder / ".vscode/settings.json").write_text(json.dumps({
            "python.defaultInterpreterPath": "/opt/debug-gym/bin/python",
        }), encoding="utf-8")
        mode = "author" if session.authoring else "student"
        namespace = hashlib.sha256(str(settings.DEBUG_GYM_WORKSPACES_DIR).encode()).hexdigest()[:8]
        port = start_ide(SimpleNamespace(id=f"v2-{namespace}-{session.user_id}-{mode}"), folder)
    return f"http://localhost:{port}/?folder=/home/coder/project"
