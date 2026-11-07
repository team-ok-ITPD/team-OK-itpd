from functools import wraps

from django.http import JsonResponse

from .models import is_professor


def professor_required_json(view):
    """Allow only logged-in professors: 401 when logged out, 403 for students."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Log in to continue."}, status=401)
        if not is_professor(request.user):
            return JsonResponse({"error": "Only professors can do this."}, status=403)
        return view(request, *args, **kwargs)

    return wrapper
