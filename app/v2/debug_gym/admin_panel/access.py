# [Admin Dev] Revoke existing web sessions and IDE tokens on deactivation
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session
from django.utils import timezone

from core.models import WorkspaceSession
from student.models import IdeToken


def revoke_access(users):
    user_ids = {str(user.pk) for user in users}
    session_keys = [
        session.session_key
        for session in Session.objects.filter(expire_date__gt=timezone.now()).iterator()
        if session.get_decoded().get(SESSION_KEY) in user_ids
    ]
    Session.objects.filter(session_key__in=session_keys).delete()
    WorkspaceSession.objects.filter(user_id__in=user_ids).delete()
    IdeToken.objects.filter(student_id__in=user_ids).delete()
