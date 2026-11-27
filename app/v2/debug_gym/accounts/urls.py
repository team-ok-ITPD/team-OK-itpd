# [Backend Dev] URL routes for the accounts app, mounted at /accounts/
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.SignInView.as_view(), name="login"),
    path("logout/", views.SignOutView.as_view(), name="logout"),
    path("set-password/<uidb64>/<token>/", views.SetAccountPasswordView.as_view(), name="set-password"),
]
