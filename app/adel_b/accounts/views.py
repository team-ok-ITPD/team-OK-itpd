import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

User = get_user_model()


def user_dict(user):
    return {"username": user.username, "email": user.email}


def _read_json(request):
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _text(payload, name):
    value = payload.get(name, "")
    return value.strip() if isinstance(value, str) and name != "password" else value


@require_http_methods(["POST"])
def register(request):
    payload = _read_json(request)
    if payload is None:
        return JsonResponse({"error": "Send a JSON object."}, status=400)
    username, email, password = (_text(payload, name) for name in ("username", "email", "password"))
    if not all(isinstance(value, str) and value for value in (username, email, password)):
        return JsonResponse({"error": "Enter a username, an email and a password."}, status=400)

    errors = {}
    try:
        UnicodeUsernameValidator()(username)
        if len(username) > 150:
            raise ValidationError("Use 150 characters or fewer.")
    except ValidationError as error:
        errors["username"] = " ".join(error.messages)
    if "username" not in errors and User.objects.filter(username__iexact=username).exists():
        errors["username"] = "That username is taken."
    try:
        validate_email(email)
    except ValidationError:
        errors["email"] = "Enter a valid email address."
    if "email" not in errors and User.objects.filter(email__iexact=email).exists():
        errors["email"] = "An account with that email already exists."
    try:
        validate_password(password, User(username=username, email=email))
    except ValidationError as error:
        errors["password"] = " ".join(error.messages)
    if errors:
        return JsonResponse({"error": "Please fix the highlighted fields.", "fields": errors}, status=400)

    user = User.objects.create_user(username=username, email=email.lower(), password=password)
    login(request, user)
    return JsonResponse({"user": user_dict(user)}, status=201)


@require_http_methods(["POST"])
def login_view(request):
    payload = _read_json(request)
    if payload is None:
        return JsonResponse({"error": "Send a JSON object."}, status=400)
    identifier, password = _text(payload, "login"), _text(payload, "password")
    if not isinstance(identifier, str) or not isinstance(password, str) or not identifier or not password:
        return JsonResponse({"error": "Enter your username or email and your password."}, status=400)

    # People can sign in with either their username or their email. An unknown
    # name still goes through authenticate() so it takes as long as a bad password.
    lookup = {"email__iexact": identifier} if "@" in identifier else {"username__iexact": identifier}
    account = User.objects.filter(**lookup).first()
    user = authenticate(request, username=account.username if account else identifier, password=password)
    if user is None:
        return JsonResponse({"error": "That username/email and password do not match."}, status=400)
    login(request, user)
    return JsonResponse({"user": user_dict(user)})


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"user": None})


@require_http_methods(["GET"])
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"user": None})
    return JsonResponse({"user": user_dict(request.user)})
