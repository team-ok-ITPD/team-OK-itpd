# [Admin Dev] Optional initial credentials and password-setup link delivery
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_access_link(user, *, initial_password=None):
    if not settings.ACCOUNT_EMAIL_ENABLED or not user.is_active:
        return False
    # Never trust the incoming Host header and never print access tokens to logs.
    if not settings.ACCOUNT_PUBLIC_URL or settings.EMAIL_BACKEND.endswith(
        (".console.EmailBackend", ".filebased.EmailBackend", ".dummy.EmailBackend")
    ):
        return False
    path = reverse("accounts:set-password", kwargs={
        "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    })
    origin = settings.ACCOUNT_PUBLIC_URL.rstrip("/")
    lines = [
        "An administrator created or updated your Debug Gym account.",
        f"Email: {user.email}",
    ]
    if initial_password:
        # Available only from the successful creation request, never recovered
        # from the stored hash or retained for subsequent resend requests.
        lines.extend([
            f"Initial password: {initial_password}",
            f"Sign in: {origin}{reverse('accounts:login')}",
            "You can use the link below to choose your own password.",
        ])
    lines.extend([
        f"Set your password here:\n{origin}{path}",
        "If this was unexpected, contact your administrator.",
    ])
    try:
        return send_mail(
            "Your Debug Gym account",
            "\n\n".join(lines),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        ) == 1
    except Exception:
        # Provider errors can contain credentials; do not echo them to the UI/logs.
        return False
