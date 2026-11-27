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
def save_key(user, key, provider=AgentCredential.Provider.PLATFORM):
    if provider not in AgentCredential.Provider.values:
        raise AgentError("Choose a supported provider.")
    if key:
        AgentCredential.objects.update_or_create(
            user=user, defaults={"encrypted_key": cipher().encrypt(key.encode()).decode(), "provider": provider},
        )
    else:
        AgentCredential.objects.filter(user=user).delete()


@sensitive_variables()
def api_credentials(user):
    record = AgentCredential.objects.filter(user=user).first()
    if record and record.encrypted_key:
        try:
            return cipher().decrypt(record.encrypted_key.encode()).decode(), record.provider
        except (InvalidToken, ValueError):
            raise AgentError("Your stored API key cannot be read. Save it again in Settings.")
    if not settings.DEBUG_GYM_AGENT_KEY:
        raise AgentError("Add your API key in Settings or ask the administrator to configure the platform key.")
    return settings.DEBUG_GYM_AGENT_KEY, AgentCredential.Provider.PLATFORM


def api_key(user):
    return api_credentials(user)[0]


@sensitive_variables()
def ask_agent(user, instruction, data):
    key, provider = api_credentials(user)
    endpoint, model = settings.DEBUG_GYM_AGENT_URL, settings.DEBUG_GYM_AGENT_MODEL
    if provider == AgentCredential.Provider.OPENAI:
        endpoint = "https://api.openai.com/v1/chat/completions"
    elif provider == AgentCredential.Provider.OPENROUTER:
        endpoint = "https://openrouter.ai/api/v1/chat/completions"
        model = model if "/" in model else "openai/" + model
    elif provider != AgentCredential.Provider.PLATFORM:
        raise AgentError("Choose a supported provider in Settings.")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": instruction + " Return a JSON object only."},
            {"role": "user", "content": json.dumps(data)},
        ],
        "response_format": {"type": "json_object"},
    }
    request = Request(
        endpoint, data=json.dumps(payload).encode(),
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
