# [Student Dev] VS Code in the browser (code-server) for solving Debug Gym v2 bugs.
# Build from this folder:  docker build --network host -t debug-gym-v2-ide app/v2/ide
# (--network host avoids slow downloads on networks with a small MTU, such as Tailscale.)
FROM ghcr.io/coder/code-server:4.141.0

USER root

# Python with pytest runs the bugs' tests; the Python extensions give the debugger.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/debug-gym \
    && /opt/debug-gym/bin/pip install --no-cache-dir "pytest>=8,<9" \
    && mkdir -p /opt/debug-gym/extensions \
    && code-server --extensions-dir /opt/debug-gym/extensions --install-extension ms-python.python \
    && code-server --extensions-dir /opt/debug-gym/extensions --install-extension ms-python.debugpy

# The Debug Gym extension: Test and Submit buttons.
COPY vscode-extension /tmp/debug-gym-extension
RUN python3 /tmp/debug-gym-extension/package_vsix.py /tmp/debug-gym.vsix \
    && code-server --extensions-dir /opt/debug-gym/extensions --install-extension /tmp/debug-gym.vsix \
    && rm -rf /tmp/debug-gym-extension /tmp/debug-gym.vsix \
    && chown -R coder:coder /opt/debug-gym

# code-server builds the environment from the login shell, so put the venv on PATH there too:
# then `python` and `pytest` work in VS Code's terminal.
RUN printf '\nexport PATH="/opt/debug-gym/bin:$PATH"\n' | tee -a /home/coder/.bashrc /home/coder/.profile > /dev/null \
    && chown coder:coder /home/coder/.bashrc /home/coder/.profile

USER coder
WORKDIR /home/coder/project
