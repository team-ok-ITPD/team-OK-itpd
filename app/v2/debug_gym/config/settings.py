# [Backend Dev] Project settings: installed apps, database, templates, static files, auth
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Share the existing browser VS Code launcher with the original application.
sys.path.insert(0, str(BASE_DIR.parents[2]))

# --- Security -------------------------------------------------------------
# Set DJANGO_SECRET_KEY / DJANGO_DEBUG / DJANGO_ALLOWED_HOSTS in the environment
# for anything other than local development.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
# host.docker.internal: the VS Code containers submit fixes through this name.
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,host.docker.internal").split(",")
# One-click demo sign-in buttons on the login page (needs `manage.py seed_demo`).
# On by default only while DEBUG is on; never enable it on a public server.
DEMO_LOGIN = os.environ.get("DJANGO_DEMO_LOGIN", "1" if DEBUG else "0") == "1"

# --- Applications ---------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Debug Gym apps
    "core",
    "accounts",
    "admin_panel",
    "professor",
    "student",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Templates ------------------------------------------------------------
# Shared layout lives in BASE_DIR/templates; each app keeps its own templates/<app>/.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "student.context_processors.student_nav",
            ],
        },
    },
]

# --- Database -------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Schema uses INT primary keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# --- Authentication -------------------------------------------------------
AUTH_USER_MODEL = "core.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Account mail is opt-in. Access links are never printed by the application.
ACCOUNT_EMAIL_ENABLED = os.environ.get("DJANGO_ACCOUNT_EMAIL_ENABLED", "0") == "1"
ACCOUNT_PUBLIC_URL = os.environ.get("DJANGO_ACCOUNT_PUBLIC_URL", "")
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "noreply@example.com")

# --- Internationalization -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files ---------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- VS Code (code-server) --------------------------------------------------
# One folder tree for all VS Code workspaces; DEBUG_GYM_WORKSPACES_DIR overrides it.
WORKSPACES_DIR = Path(os.environ.get("DEBUG_GYM_WORKSPACES_DIR", BASE_DIR / "workspaces")).resolve()
# Image for professor authoring and server-side test verification (root Dockerfile).
DEBUG_GYM_IDE_IMAGE = os.environ.get("DEBUG_GYM_IDE_IMAGE", "debug-gym-ide")
# Image students solve bugs in (app/v2/ide/Dockerfile).
DEBUG_GYM_STUDENT_IDE_IMAGE = os.environ.get("DEBUG_GYM_STUDENT_IDE_IMAGE", "debug-gym-v2-ide")
# How VS Code containers reach this Django server. In development the request's own
# port is used instead unless this is set (core/bridge.py).
DEBUG_GYM_IDE_SERVER_URL = os.environ.get("DEBUG_GYM_IDE_SERVER_URL", "http://host.docker.internal:8002")
DEBUG_GYM_SITE_URL = os.getenv("DEBUG_GYM_SITE_URL", "http://localhost:8002")
DEBUG_GYM_WORKSPACES_DIR = WORKSPACES_DIR
# Student folders live apart from the professors' authoring sessions.
STUDENT_WORKSPACES_DIR = WORKSPACES_DIR / "students"
DEBUG_GYM_AGENT_URL = os.getenv("DEBUG_GYM_AGENT_URL", "https://api.openai.com/v1/chat/completions")
DEBUG_GYM_AGENT_MODEL = os.getenv("DEBUG_GYM_AGENT_MODEL", "gpt-4.1-mini")
DEBUG_GYM_AGENT_KEY = os.getenv("DEBUG_GYM_AGENT_KEY", "")
DEBUG_GYM_KEY_FILE = BASE_DIR / ".agent-encryption-key"
DATA_UPLOAD_MAX_MEMORY_SIZE = 6_000_000
