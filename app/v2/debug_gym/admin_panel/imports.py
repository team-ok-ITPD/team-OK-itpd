# [Admin Dev] Atomic, role-safe and repeatable student CSV import
import csv
import io

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from core.models import GroupStudent, StudyGroup, User
from .access import revoke_access


COLUMNS = {
    "name", "email", "is_active", "password", "group", "group_number", "teacher_email", "course",
}


@transaction.atomic
def import_students(upload):
    try:
        text = upload.read(1_000_001).decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValidationError("Use a UTF-8 encoded CSV file.") from None
    if len(text.encode("utf-8")) > 1_000_000:
        raise ValidationError("The CSV must be at most 1 MB.")
    reader = csv.DictReader(io.StringIO(text), strict=True)
    try:
        headers = reader.fieldnames or []
    except csv.Error:
        raise ValidationError("Malformed CSV headers. No rows were applied.") from None
    if (
        not {"name", "email"}.issubset(headers)
        or not set(headers).issubset(COLUMNS)
        or len(headers) != len(set(headers))
    ):
        raise ValidationError("Use unique headers: name,email,is_active,password,course,group_number,teacher_email (legacy group also accepted). Name and email are required.")
    seen = {}
    result = {"created": 0, "updated": 0, "memberships": 0, "groups": 0}
    notify = {}
    rows = 0
    try:
        for line, row in enumerate(reader, 2):
            rows += 1
            if rows > 5000:
                raise ValidationError("At most 5000 student/group rows are allowed.")
            if None in row or any(value is None for value in row.values()):
                raise ValidationError(f"Row {line}: the number of cells does not match the headers.")
            name = row["name"].strip()
            email = row["email"].strip().lower()
            password = row.get("password", "")
            active = row.get("is_active", "").strip().lower()
            if not name or len(name) > 100 or len(email) > 150:
                raise ValidationError(f"Row {line}: supply a name (up to 100 characters) and email (up to 150).")
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(f"Row {line}: invalid email.") from None
            if active not in ("", "true", "false", "1", "0"):
                raise ValidationError(f"Row {line}: is_active must be true or false.")
            if password and len(password) < 8:
                raise ValidationError(f"Row {line}: passwords must have at least 8 characters.")
            signature = (name, active, password)
            if email in seen and seen[email] != signature:
                raise ValidationError(f"Row {line}: repeated student rows must have identical account data.")
            first = email not in seen
            seen[email] = signature
            matches = User.objects.select_for_update().filter(email__iexact=email)
            if matches.count() > 1:
                raise ValidationError(f"Row {line}: email matches multiple accounts.")
            user = matches.first()
            if user and user.role != User.Role.STUDENT:
                raise ValidationError(f"Row {line}: cannot update a non-student account.")
            changed_password = False
            if user is None:
                if not password and not settings.ACCOUNT_EMAIL_ENABLED:
                    raise ValidationError(f"Row {line}: new students need a password while email delivery is disabled.")
                user = User(email=email, name=name, role=User.Role.STUDENT)
                user.set_password(password or None)
                user.is_active = active not in ("false", "0")
                user.save()
                result["created"] += 1
                notify[user.pk] = (user, password or None, True)
            elif first:
                changed = user.name != name
                user.name = name
                if active:
                    next_active = active in ("true", "1")
                    changed = changed or user.is_active != next_active
                    user.is_active = next_active
                if password and not user.check_password(password):
                    user.set_password(password)
                    changed = changed_password = True
                if changed:
                    user.save()
                    result["updated"] += 1
                    if not user.is_active:
                        revoke_access([user])
                if changed_password:
                    notify[user.pk] = (user, None, False)
            legacy_group = row.get("group", "").strip()
            course = row.get("course", "").strip()
            group_name = legacy_group or course
            group_number = row.get("group_number", "").strip()
            legacy_description = course if legacy_group else ""
            teacher_email = row.get("teacher_email", "").strip()
            if not group_name:
                if teacher_email or group_number:
                    raise ValidationError(f"Row {line}: supply a course when specifying a group number or teacher.")
                continue
            if len(group_name) > 100 or len(group_number) > 50:
                raise ValidationError(f"Row {line}: course names must be at most 100 characters and group numbers at most 50.")
            groups = StudyGroup.objects.select_for_update().filter(name__iexact=group_name)
            if group_number:
                groups = groups.filter(group_number__iexact=group_number)
            if groups.count() > 1:
                raise ValidationError(f"Row {line}: course matches multiple groups; supply group_number.")
            group = groups.first()
            teacher = None
            if teacher_email:
                teachers = User.objects.filter(
                    email__iexact=teacher_email, role=User.Role.PROFESSOR, is_active=True
                )
                if teachers.count() != 1:
                    raise ValidationError(f"Row {line}: teacher_email must identify one active teacher.")
                teacher = teachers.get()
            if group is None:
                if teacher is None or not group_number:
                    raise ValidationError(f"Row {line}: new groups require teacher_email and group_number.")
                group = StudyGroup.objects.create(
                    name=group_name, group_number=group_number,
                    professor=teacher, description=legacy_description,
                )
                result["groups"] += 1
            else:
                if teacher and group.professor_id != teacher.pk:
                    raise ValidationError(f"Row {line}: use Edit group to change its teacher.")
                if legacy_description and (group.description or "").splitlines()[:1] != [legacy_description]:
                    raise ValidationError(f"Row {line}: legacy course/description conflicts with the existing group.")
            _, created = GroupStudent.objects.get_or_create(group=group, student=user)
            result["memberships"] += int(created)
    except csv.Error:
        raise ValidationError("Malformed CSV. No rows were applied.") from None
    if not rows:
        raise ValidationError("The CSV has no student rows.")
    return result, list(notify.values())
