"""Verify untrusted learner code in a fresh, short-lived Docker container."""

import json
import tempfile
import threading
from contextlib import contextmanager
from pathlib import Path

import docker
from django.conf import settings


class VerificationError(RuntimeError):
    pass


class VerificationBusy(VerificationError):
    pass


class VerificationGate:
    """Bound running verifications and the requests waiting for a runner."""

    def __init__(self, concurrency, queue_size, wait_timeout):
        if concurrency < 1 or queue_size < 0 or wait_timeout < 0:
            raise ValueError("Verification concurrency must be positive; queue limits cannot be negative.")
        self.capacity = threading.BoundedSemaphore(concurrency + queue_size)
        self.runners = threading.BoundedSemaphore(concurrency)
        self.wait_timeout = wait_timeout

    @contextmanager
    def slot(self):
        if not self.capacity.acquire(blocking=False):
            raise VerificationBusy("Submission verification is busy. Try again shortly.")
        running = False
        try:
            running = self.runners.acquire(timeout=self.wait_timeout)
            if not running:
                raise VerificationBusy("Submission verification is busy. Try again shortly.")
            yield
        finally:
            if running:
                self.runners.release()
            self.capacity.release()


_gate = None
_gate_settings = None
_gate_lock = threading.Lock()


def _verification_gate():
    global _gate, _gate_settings
    values = (
        settings.DEBUG_GYM_VERIFICATION_CONCURRENCY,
        settings.DEBUG_GYM_VERIFICATION_QUEUE_SIZE,
        settings.DEBUG_GYM_VERIFICATION_QUEUE_TIMEOUT,
    )
    with _gate_lock:
        if _gate is None or _gate_settings != values:
            _gate = VerificationGate(*values)
            _gate_settings = values
        return _gate


HARNESS = """\
import copy
import contextlib
import io
import json

payload = json.loads(open('/verification/input.json', encoding='utf-8').read())
dump_result = json.dumps
write_result = print
test_count = len(payload['tests'])
namespace = {'__name__': 'submission'}
passed = 0
try:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        exec(compile(payload['code'], 'submission.py', 'exec'), namespace)
        function = namespace.get(payload['function'])
        if callable(function):
            for test in payload['tests']:
                try:
                    actual = function(copy.deepcopy(test['input']))
                    passed += actual == test['expected']
                except BaseException:
                    pass
except BaseException:
    pass
write_result(dump_result({'passed': passed, 'total': test_count}))
"""


def verify_submission(bug, code):
    """Return trusted passed/total counts from an isolated one-use container."""
    with _verification_gate().slot():
        return _run_verification(bug, code)


def _run_verification(bug, code):
    payload = {"code": code, "function": bug.function_name, "tests": bug.tests}
    with tempfile.TemporaryDirectory(prefix="debug-gym-verification-") as directory:
        path = Path(directory)
        path.chmod(0o755)
        (path / "verify.py").write_text(HARNESS, encoding="utf-8")
        (path / "input.json").write_text(json.dumps(payload), encoding="utf-8")
        try:
            client = docker.from_env()
            client.ping()
            container = client.containers.run(
                settings.DEBUG_GYM_VERIFICATION_IMAGE,
                entrypoint=["python3", "-I", "/verification/verify.py"],
                detach=True,
                init=True,
                network_disabled=True,
                read_only=True,
                mem_limit=settings.DEBUG_GYM_VERIFICATION_MEMORY,
                nano_cpus=settings.DEBUG_GYM_VERIFICATION_NANO_CPUS,
                pids_limit=settings.DEBUG_GYM_VERIFICATION_PIDS,
                security_opt=["no-new-privileges:true"],
                tmpfs={"/tmp": "rw,noexec,nosuid,size=16m"},
                volumes={str(path): {"bind": "/verification", "mode": "ro"}},
            )
            try:
                result = container.wait(timeout=settings.DEBUG_GYM_VERIFICATION_TIMEOUT)
                output = container.logs(stdout=True, stderr=False).decode().strip()
            finally:
                container.remove(force=True)
        except docker.errors.ImageNotFound as error:
            raise VerificationError("The submission verification image is not available.") from error
        except (docker.errors.DockerException, ValueError, json.JSONDecodeError) as error:
            raise VerificationError("The submission could not be verified. Try again.") from error

    if result.get("StatusCode") != 0:
        raise VerificationError("The submission could not be verified. Try again.")
    try:
        counts = json.loads(output)
        passed, total = counts["passed"], counts["total"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise VerificationError("The submission returned an invalid verification result.") from error
    if type(passed) is not int or type(total) is not int or total != len(bug.tests) or not 0 <= passed <= total:
        raise VerificationError("The submission returned an invalid verification result.")
    return passed, total
