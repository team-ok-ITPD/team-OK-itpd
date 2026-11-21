# [Backend Dev] Scoped IDE sessions, verified submissions and author snapshots
from datetime import timedelta
import hashlib
import json
import secrets

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.debug import sensitive_variables
from django.conf import settings

from .models import Assignment, Bug, Submission, User, WorkspaceSession
from .bridge import ensure_relay, ide_server_url, site_url
from .projects import ProjectError, entry_path, validate_project
from .runtime import IdeError, RuntimeError, open_workspace, verify
from app.adel_b.bugs.verification import VerificationBusy


def session_allowed(session):
    user, bug = session.user, session.bug
    if not user.is_active or session.expires_at <= timezone.now():
        return False
    if session.authoring:
        return user.role == User.Role.PROFESSOR and bug.created_by_id == user.pk
    if user.role != User.Role.STUDENT:
        return False
    if session.assignment_id:
        assignment = session.assignment
        return (
            assignment.bug_id == bug.pk
            and assignment.groups.filter(students=user).exists()
            and assignment.status == Assignment.Status.ACTIVE
            and (assignment.deadline is None or assignment.deadline >= timezone.now())
        )
    return bug.visibility == Bug.Visibility.PUBLIC


@login_required
@require_POST
@sensitive_variables()
def launch(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    authoring = request.POST.get("mode") == "author"
    assignment = None
    if request.POST.get("assignment"):
        raw_pk = request.POST["assignment"]
        if not raw_pk.isdecimal() or len(raw_pk) > 18:
            return JsonResponse({"error": "Invalid assignment."}, status=400)
        assignment = get_object_or_404(Assignment, pk=raw_pk, bug=bug)
    session = WorkspaceSession(
        user=request.user, bug=bug, assignment=assignment, authoring=authoring,
        revision=bug.revision, expires_at=timezone.now() + timedelta(hours=8),
    )
    if not session_allowed(session):
        return JsonResponse({"error": "This workspace is not available to your account."}, status=403)
    token = secrets.token_urlsafe(32)
    previous = WorkspaceSession.objects.filter(
        user=request.user, bug=bug, assignment=assignment,
        authoring=authoring, revision=bug.revision, expires_at__gt=timezone.now(),
    ).order_by("-pk").first()
    if previous:
        try:
            config = json.loads(
                (settings.DEBUG_GYM_WORKSPACES_DIR / str(previous.pk) / ".debug-gym/config.json").read_text(),
            )
            previous_token = config["token"]
            if hashlib.sha256(previous_token.encode()).hexdigest() == previous.token_digest:
                session, token = previous, previous_token
        except (OSError, ValueError, KeyError, TypeError):
            pass
    session.token_digest = hashlib.sha256(token.encode()).hexdigest()
    session.save()
    port = int(request.get_port())
    try:
        url = open_workspace(session, token, server_url=ide_server_url(port), site_url=site_url(request))
        # Development on Linux: let the container reach this server (see core/bridge.py).
        ensure_relay(port)
    except (IdeError, ProjectError, OSError) as error:
        session.delete()
        return JsonResponse({"error": str(error)}, status=503)
    return JsonResponse({"url": url})


@csrf_exempt
@require_POST
@sensitive_variables()
def submit(request):
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return JsonResponse({"error": "A workspace token is required."}, status=401)
    token = authorization[7:]
    session = WorkspaceSession.objects.select_related("user", "bug", "assignment").filter(
        token_digest=hashlib.sha256(token.encode()).hexdigest(), expires_at__gt=timezone.now(),
    ).first()
    if session is None or not session_allowed(session):
        return JsonResponse({"error": "Workspace access expired or the assignment is closed."}, status=403)
    try:
        if len(request.body) > 6_000_000:
            raise ProjectError("The workspace snapshot exceeds the upload limit.")
        data = json.loads(request.body)
        code = data["code"]
        if not isinstance(code, str) or len(code.encode()) > 500_000:
            raise ProjectError("The source file exceeds the size limit.")
        if str(data.get("bug")) != str(session.bug_id):
            raise ProjectError("This token belongs to a different exercise.")
        digest = hashlib.sha256(request.body).hexdigest()
        if digest == session.last_request:
            return JsonResponse(session.last_response)
        if session.authoring:
            files = validate_project(data["files"], entry_path(session.bug))
            if files[entry_path(session.bug)] != code:
                raise ProjectError("The source and project snapshot do not match.")
            passed, total = 0, 0
        else:
            passed, total = verify(session.bug, code)
        with transaction.atomic():
            # Serialized tokens make retries idempotent; recheck deadlines after tests.
            session = WorkspaceSession.objects.select_for_update().select_related(
                "user", "assignment",
            ).get(pk=session.pk)
            bug = Bug.objects.select_for_update().get(pk=session.bug_id)
            session.bug = bug
            if digest == session.last_request:
                return JsonResponse(session.last_response)
            if not session_allowed(session):
                return JsonResponse({"error": "The assignment closed while the tests ran."}, status=403)
            if session.revision != bug.revision:
                return JsonResponse({"error": "The exercise changed. Reopen it from the website."}, status=409)
            if session.authoring:
                bug.project_files = files
                bug.buggy_code = code
                bug.revision += 1
                bug.save(update_fields=("project_files", "buggy_code", "revision", "updated_at"))
                session.revision = bug.revision
                result = {"saved": True, "revision": bug.revision}
            else:
                submission = Submission.objects.create(
                    student=session.user, assignment=session.assignment, bug=bug,
                    submitted_code=code, tests_passed=passed, tests_total=total,
                )
                result = {"attempt": {
                    "id": submission.pk, "passed": passed, "total": total, "solved": passed == total,
                }}
            session.last_request = digest
            session.last_response = result
            session.save(update_fields=("last_request", "last_response", "revision"))
        return JsonResponse(result)
    except (ValueError, KeyError, TypeError) as error:
        message = str(error) if isinstance(error, (ProjectError, RuntimeError)) else "Invalid workspace snapshot."
        return JsonResponse({"error": message}, status=400)
    except VerificationBusy as error:
        return JsonResponse({"error": str(error)}, status=503)
