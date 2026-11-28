# [Shared] Let VS Code containers (students and professors) reach the development server
"""Development only (DEBUG on).

The Debug Gym extension inside a VS Code container (student or professor) submits to
http://host.docker.internal:<port>. On Linux that name points at Docker's bridge
address (usually 172.17.0.1), but `manage.py runserver` and `run.py` listen on
127.0.0.1 only, so the container cannot connect and Submit fails.

This module opens a small TCP relay on the bridge address that forwards to the
server on 127.0.0.1. The bridge address is reachable only from containers on this
machine, not from the network. On Docker Desktop (Windows, macOS) the bridge
address is not local and host.docker.internal already reaches 127.0.0.1, so the
relay simply does not start there.
"""
import os
import socket
import threading
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings

_lock = threading.Lock()
_listening = set()  # (address, port) relays started by this process
DEFAULT_BRIDGE = "172.17.0.1"


def ide_server_url(port):
    """Return an address reachable from the code-server container.

    A loopback URL refers to the code-server container itself, not the Django
    host. Rewrite it to Docker's host gateway; ensure_ide_relay() below makes
    that gateway:port forward to a localhost-bound Django dev server on Linux.
    """
    configured = os.environ.get("DEBUG_GYM_IDE_SERVER_URL")
    url = configured or f"http://host.docker.internal:{port}"
    parsed = urlsplit(url)
    if parsed.hostname in ("localhost", "127.0.0.1", "::1"):
        host = "host.docker.internal"
        netloc = f"{host}:{parsed.port}" if parsed.port else host
        url = urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))
    return url


def ensure_ide_relay(port):
    """Relay the actual configured IDE API port, not necessarily Django's request port."""
    parsed = urlsplit(ide_server_url(port))
    if parsed.hostname != "host.docker.internal":
        return False  # A public/reverse-proxy URL is already reachable directly.
    return ensure_relay(parsed.port or (443 if parsed.scheme == "https" else 80))


def site_url(request):
    """The website address for "Back to Debug Gym" links: an explicit setting wins, else this request's."""
    if os.environ.get("DEBUG_GYM_SITE_URL"):
        return settings.DEBUG_GYM_SITE_URL.rstrip("/")
    return request.build_absolute_uri("/").rstrip("/")


LOCAL_ADDRESSES = ("127.0.0.1", "localhost", "::1", "[::1]")


def runserver_address(argv):
    """(address, port) from `manage.py runserver [addr:]port`; Django's default is 127.0.0.1:8000."""
    args = [a for a in argv[argv.index("runserver") + 1:] if not a.startswith("-")]
    if not args:
        return "127.0.0.1", 8000
    address, _, port = args[0].rpartition(":")
    return address or "127.0.0.1", int(port) if port.isdigit() else None


def runserver_port(argv):
    """The port from `manage.py runserver [addr:]port`, or Django's default 8000."""
    return runserver_address(argv)[1]


def start_with_runserver(argv):
    """Called from CoreConfig.ready(): start the relay in the process that serves requests."""
    if "runserver" not in argv:
        return
    if os.environ.get("RUN_MAIN") != "true" and "--noreload" not in argv:
        return
    address, port = runserver_address(argv)
    # Only a server on localhost needs the relay. On 0.0.0.0 (or the bridge address)
    # containers already reach it, and a relay on the same port would make the
    # server's own bind fail with "That port is already in use".
    if port and address in LOCAL_ADDRESSES:
        threading.Thread(target=ensure_relay, args=(port,), daemon=True).start()


def bridge_address():
    """Docker's bridge gateway address, or the usual default when Docker cannot be asked."""
    try:
        import docker

        config = docker.from_env().networks.get("bridge").attrs["IPAM"]["Config"]
        return config[0]["Gateway"]
    except Exception:
        return DEFAULT_BRIDGE


def ensure_relay(port, address=None):
    """Start forwarding address:port to 127.0.0.1:port once per process. Returns True if a relay runs."""
    if not settings.DEBUG:
        return False
    address = address or bridge_address()
    with _lock:
        if (address, port) in _listening:
            return True
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((address, port))
        except OSError:
            # Address not on this machine (Docker Desktop) or already served there
            # (for example Django itself also listens on the bridge address).
            server.close()
            return False
        server.listen(32)
        _listening.add((address, port))
    threading.Thread(target=_accept, args=(server, port), daemon=True, name=f"ide-relay-{port}").start()
    return True


def _accept(server, port):
    while True:
        try:
            client, _ = server.accept()
        except OSError:
            return
        threading.Thread(target=_connect, args=(client, port), daemon=True).start()


def _connect(client, port):
    try:
        upstream = socket.create_connection(("127.0.0.1", port), timeout=10)
    except OSError:
        client.close()
        return
    upstream.settimeout(None)
    back = threading.Thread(target=_pipe, args=(upstream, client), daemon=True)
    back.start()
    _pipe(client, upstream)
    back.join()
    client.close()
    upstream.close()


def _pipe(source, target):
    """Copy one direction; at its end tell the other side no more data is coming."""
    try:
        while data := source.recv(65536):
            target.sendall(data)
    except OSError:
        pass
    try:
        target.shutdown(socket.SHUT_WR)
    except OSError:
        pass
