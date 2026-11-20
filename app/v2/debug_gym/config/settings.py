# [Backend Dev] Project settings: installed apps, database, templates, static files, auth
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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

# Password reset emails are printed to the console during development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Internationalization -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files ---------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- VS Code (code-server) for solving bugs -------------------------------
# Image built from app/v2/ide/Dockerfile.
DEBUG_GYM_IDE_IMAGE = os.environ.get("DEBUG_GYM_IDE_IMAGE", "debug-gym-v2-ide")
# One folder per student and bug; mounted into the student's VS Code container.
WORKSPACES_DIR = Path(os.environ.get("DEBUG_GYM_WORKSPACES_DIR", BASE_DIR / "workspaces")).resolve()
# How the VS Code container reaches this Django server to submit. Django must also
# listen on Docker's bridge address (172.17.0.1) for this to work.
DEBUG_GYM_IDE_SERVER_URL = os.environ.get("DEBUG_GYM_IDE_SERVER_URL", "http://host.docker.internal:8002")
