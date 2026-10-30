"""Start a learner's code-server (VS Code in the browser) container."""

import hashlib
import json
import time
from urllib.error import URLError
from urllib.request import urlopen

import docker
from django.conf import settings

PROJECT_DIR = "/home/coder/project"
CONTAINER_PORT = "8080/tcp"
FOLDER_LABEL = "debug-gym.folder"
SETTINGS_LABEL = "debug-gym.settings"
READY_TIMEOUT_SECONDS = 30
# The image's start script puts the Debug GYM venv first; we skip that script, so set it here.
CONTAINER_PATH = "/opt/debug-gym/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


class IdeError(RuntimeError):
    pass


def container_name(user):
    return f"debug-gym-ide-{user.id}"


def _client():
    try:
        client = docker.from_env()
        client.ping()
    except docker.errors.DockerException as error:
        raise IdeError("Docker is not running on the server, so VS Code cannot start.") from error
    return client


def _host_port(container):
    container.reload()
    bindings = (container.ports or {}).get(CONTAINER_PORT) or []
    if not bindings:
        raise IdeError("The VS Code container has no published port.")
    return int(bindings[0]["HostPort"])


def _image_id(client):
    try:
        return client.images.get(settings.DEBUG_GYM_IDE_IMAGE).id
    except docker.errors.ImageNotFound:
        return None


def _remove(container):
    try:
        container.remove(force=True)
    except docker.errors.NotFound:
        pass


CODE_SERVER_ARGS = [
    "--auth", "none",
    "--bind-addr", "0.0.0.0:8080",
    "--disable-telemetry",
    # The folder only holds the learner's own exercise; Restricted Mode would block
    # the Python debugger and the Debug GYM extension.
    "--disable-workspace-trust",
    # No /proxy/<port> routes: they would expose ports inside the container and turn the
    # extension's localhost link back to the website into a proxy URL.
    "--disable-proxy",
    "--extensions-dir", "/opt/debug-gym/extensions",
    PROJECT_DIR,
]
CONTAINER_ENV = {"PATH": CONTAINER_PATH}


def settings_label():
    """A short fingerprint of how containers are started, to replace outdated ones."""
    text = json.dumps({"args": CODE_SERVER_ARGS, "env": CONTAINER_ENV}, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _start(client, name, folder):
    return client.containers.run(
        settings.DEBUG_GYM_IDE_IMAGE,
        entrypoint=["code-server"],
        command=CODE_SERVER_ARGS,
        name=name,
        detach=True,
        init=True,
        environment=CONTAINER_ENV,
        # Lets the Debug GYM extension reach the Django server on the host.
        extra_hosts={"host.docker.internal": "host-gateway"},
        labels={FOLDER_LABEL: str(folder), SETTINGS_LABEL: settings_label()},
        volumes={str(folder): {"bind": PROJECT_DIR, "mode": "rw"}},
        ports={CONTAINER_PORT: ("127.0.0.1", None)},
        mem_limit="512m",
        security_opt=["no-new-privileges:true"],
        tmpfs={"/tmp": "", "/home/coder/.cache": ""},
    )


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


def start_ide(user, folder):
    """Start or reuse the user's container with this folder open; return its local port."""
    client = _client()
    name = container_name(user)
    try:
        container = client.containers.get(name)
    except docker.errors.NotFound:
        container = None

    # Reuse only a running container with this bug's folder, the current image and settings.
    if container is not None:
        if (
            container.status == "running"
            and container.labels.get(FOLDER_LABEL) == str(folder)
            and container.labels.get(SETTINGS_LABEL) == settings_label()
            and container.image.id == _image_id(client)
        ):
            port = _host_port(container)
            _wait_until_ready(port)
            return port
        _remove(container)

    try:
        container = _start(client, name, folder)
    except docker.errors.ImageNotFound as error:
        raise IdeError(
            f"The VS Code image {settings.DEBUG_GYM_IDE_IMAGE!r} is not built on the server."
        ) from error
    except docker.errors.APIError as error:
        raise IdeError(f"Docker could not start VS Code: {error.explanation or error}") from error
    port = _host_port(container)
    _wait_until_ready(port)
    return port
