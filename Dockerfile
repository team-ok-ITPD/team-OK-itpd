FROM ghcr.io/coder/code-server:4.144.0

USER root

RUN apt-get update \
    && apt-get install --yes --no-install-recommends python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/debug-gym \
    && mkdir -p /opt/debug-gym/extensions

COPY requirements.lock /tmp/requirements.lock
RUN /opt/debug-gym/bin/pip install --no-cache-dir --requirement /tmp/requirements.lock \
    && code-server --extensions-dir /opt/debug-gym/extensions --install-extension ms-python.python \
    && code-server --extensions-dir /opt/debug-gym/extensions --install-extension ms-python.debugpy

COPY app/adel_b/vscode-extension /tmp/debug-gym-extension
RUN python3 /tmp/debug-gym-extension/package_vsix.py /tmp/debug-gym.vsix \
    && code-server --extensions-dir /opt/debug-gym/extensions --install-extension /tmp/debug-gym.vsix \
    && rm -rf /tmp/debug-gym-extension /tmp/debug-gym.vsix

COPY --chown=coder:coder app /opt/debug-gym/app
COPY --chown=coder:coder exercise /home/coder/project
COPY --chown=coder:coder scripts/start.sh /usr/local/bin/debug-gym-start

RUN printf '\nexport PATH="/opt/debug-gym/bin:$PATH"\n' | tee -a /home/coder/.bashrc /home/coder/.profile > /dev/null \
    && chown coder:coder /home/coder/.bashrc /home/coder/.profile

USER coder
WORKDIR /home/coder/project

EXPOSE 3000 8080

ENTRYPOINT ["debug-gym-start"]
