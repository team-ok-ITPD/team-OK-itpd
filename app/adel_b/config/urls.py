from django.contrib import admin
from django.urls import include, path

from .observability import metrics

urlpatterns = [
    path("admin/", admin.site.urls),
    path("metrics", metrics, name="metrics"),
    path("", include("accounts.urls")),
    path("", include("bugs.urls")),
]
