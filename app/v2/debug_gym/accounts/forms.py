# [Backend Dev] Forms for login, registration, profile editing and password reset
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Email and password login (the User model logs in by email)."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "autofocus": True, "placeholder": "you@university.edu"}
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Your password"}),
    )

    error_messages = {
        "invalid_login": "That email and password do not match. Check both and try again.",
        "inactive": "This account is deactivated. Contact your administrator.",
    }
