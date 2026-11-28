# [Admin Dev] Optional initial credentials and password-setup link delivery
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_access_link(user, *, initial_password=None, account_created=False):
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
    created = account_created or bool(initial_password)
    template = "account_created" if created else "access_link"
    subject = "Welcome to Debug Gym — your account is ready" if created else "Debug Gym — your password setup link"
    body = render_to_string(f"admin_panel/email/{template}.txt", {
        "name": user.name,
        "email": user.email,
        "role": user.get_role_display(),
        "login_url": f"{origin}{reverse('accounts:login')}",
        "access_url": f"{origin}{path}",
        "expiry_hours": settings.PASSWORD_RESET_TIMEOUT / 3600,
    }).strip()
    try:
        return send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        ) == 1
    except Exception:
        # Provider errors can contain credentials; do not echo them to the UI/logs.
        return False
