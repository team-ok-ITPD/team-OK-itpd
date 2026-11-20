# [Backend Dev] Provider calls and encrypted personal credentials
import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.views.decorators.debug import sensitive_variables

from .models import AgentCredential


class AgentError(ValueError):
    pass


def cipher():
    path = settings.DEBUG_GYM_KEY_FILE
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        pass
    else:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(Fernet.generate_key())
    return Fernet(path.read_bytes())


@sensitive_variables()
def save_key(user, key):
    if key:
        AgentCredential.objects.update_or_create(
            user=user, defaults={"encrypted_key": cipher().encrypt(key.encode()).decode()},
        )
    else:
        AgentCredential.objects.filter(user=user).delete()


def api_key(user):
    record = AgentCredential.objects.filter(user=user).first()
    if record and record.encrypted_key:
        try:
            return cipher().decrypt(record.encrypted_key.encode()).decode()
        except (InvalidToken, ValueError):
            raise AgentError("Your stored API key cannot be read. Save it again in Settings.")
    if not settings.DEBUG_GYM_AGENT_KEY:
        raise AgentError("Add your API key in Settings or ask the administrator to configure the platform key.")
    return settings.DEBUG_GYM_AGENT_KEY


@sensitive_variables()
def ask_agent(user, instruction, data):
    key = api_key(user)
    payload = {
        "model": settings.DEBUG_GYM_AGENT_MODEL,
        "messages": [
            {"role": "system", "content": instruction + " Return a JSON object only."},
            {"role": "user", "content": json.dumps(data)},
        ],
        "response_format": {"type": "json_object"},
    }
    request = Request(
        settings.DEBUG_GYM_AGENT_URL, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=90) as response:
            raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise AgentError("The provider response exceeded the size limit.")
        result = json.loads(json.loads(raw)["choices"][0]["message"]["content"])
        if not isinstance(result, dict):
            raise ValueError()
        return result
    except (URLError, TimeoutError, OSError, ValueError, KeyError, IndexError, TypeError):
        # Provider errors may contain a token or submitted code.
        raise AgentError("The agent could not complete the request. Check your key and try again.")
