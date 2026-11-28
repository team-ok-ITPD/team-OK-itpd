# [Student Dev] Start a student's VS Code (code-server) container (ported from app/adel_b)
import hashlib
import json
import time
from urllib.error import URLError
from urllib.request import urlopen

from django.conf import settings

PROJECT_DIR = "/home/coder/project"
CONTAINER_PORT = "8080/tcp"
FOLDER_LABEL = "debug-gym.folder"
SETTINGS_LABEL = "debug-gym.settings"
READY_TIMEOUT_SECONDS = 30
CONTAINER_ENV = {
    # Put the image's Python venv (with pytest) first.
    "PATH": "/opt/debug-gym/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}
CODE_SERVER_ARGS = [
    "--auth", "none",
    "--bind-addr", "0.0.0.0:8080",
    "--disable-telemetry",
    # The folder only holds the student's own bug; Restricted Mode would block the
    # Python debugger and the Debug Gym extension.
    "--disable-workspace-trust",
    # No /proxy/<port> routes: they would expose ports inside the container.
    "--disable-proxy",
    "--extensions-dir", "/opt/debug-gym/extensions",
    PROJECT_DIR,
]


class IdeError(RuntimeError):
    """A problem the student can read on the page."""


def container_name(student):
    return f"debug-gym-v2-ide-{student.pk}"


def settings_label():
    """A short fingerprint of how containers are started, to replace outdated ones."""
    text = json.dumps({"args": CODE_SERVER_ARGS, "env": CONTAINER_ENV}, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _docker():
    # Imported here so the rest of the site works where the docker package is missing.
    try:
        import docker
    except ImportError as error:
        raise IdeError("VS Code is not available: the server has no Docker support installed.") from error
    try:
        client = docker.from_env()
        client.ping()
    except docker.errors.DockerException as error:
        raise IdeError("VS Code is not available: Docker is not running on the server.") from error
    return docker, client


def _host_port(container):
    container.reload()
    bindings = (container.ports or {}).get(CONTAINER_PORT) or []
    if not bindings:
        raise IdeError("The VS Code container has no published port.")
    return int(bindings[0]["HostPort"])


def _wait_until_ready(port):
    deadline = time.monotonic() + READY_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            with urlopen(f"http://127.0.0.1:{port}/healthz", timeout=2) as response:
                if response.status == 200:
                    return
        except (URLError, ConnectionError, TimeoutError):
            pass
        time.sleep(0.5)
    raise IdeError("VS Code did not start in time. Try again in a moment.")


def start_ide(student, folder):
    """Start or reuse the student's container with `folder` open; return its local URL."""
    docker, client = _docker()
    name = container_name(student)
    try:
        image_id = client.images.get(settings.DEBUG_GYM_STUDENT_IDE_IMAGE).id
    except docker.errors.ImageNotFound:
        raise IdeError(
            f"VS Code is not available: the image {settings.DEBUG_GYM_STUDENT_IDE_IMAGE!r} is not built on the server."
        ) from None

    try:
        container = client.containers.get(name)
    except docker.errors.NotFound:
        container = None
    # Reuse only a running container with this folder, the current image and settings.
    # Do not access container.image.id here: Docker SDK resolves that property by
    # inspecting the image, which raises ImageNotFound if the old image was pruned
    # after an IDE image rebuild. The container inspection data retains its image ID.
    if container is not None:
        container.reload()
        if (
            container.status == "running"
            and container.labels.get(FOLDER_LABEL) == str(folder)
            and container.labels.get(SETTINGS_LABEL) == settings_label()
            and container.attrs.get("Image") == image_id
        ):
            port = _host_port(container)
            _wait_until_ready(port)
            return _url(port)
        # A stale container may reference an image that no longer exists.
        container.remove(force=True)

    try:
        container = client.containers.run(
            settings.DEBUG_GYM_STUDENT_IDE_IMAGE,
            entrypoint=["code-server"],
            command=CODE_SERVER_ARGS,
            name=name,
            detach=True,
            init=True,
            environment=CONTAINER_ENV,
            # Lets the extension reach this Django server on the host.
            extra_hosts={"host.docker.internal": "host-gateway"},
            labels={FOLDER_LABEL: str(folder), SETTINGS_LABEL: settings_label()},
            volumes={str(folder): {"bind": PROJECT_DIR, "mode": "rw"}},
            ports={CONTAINER_PORT: ("127.0.0.1", None)},
            mem_limit="512m",
            security_opt=["no-new-privileges:true"],
            tmpfs={"/tmp": "", "/home/coder/.cache": ""},
        )
    except docker.errors.APIError as error:
        raise IdeError(f"Docker could not start VS Code: {error.explanation or error}") from error
    port = _host_port(container)
    _wait_until_ready(port)
    return _url(port)


def _url(port):
    return f"http://localhost:{port}/?folder={PROJECT_DIR}"
