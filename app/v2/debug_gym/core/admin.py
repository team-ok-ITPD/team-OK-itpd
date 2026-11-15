# [Backend Dev] Django admin registration for the shared core models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from .models import Assignment, AssignmentGroup, Bug, GroupStudent, StudyGroup, Submission, User

# Access comes from User.role, not Django permission groups; hide them so they
# are not confused with study groups.
admin.site.unregister(Group)


class UserCreateForm(BaseUserCreationForm):
    """Create a user by email, name and role; the password is stored hashed."""

    class Meta:
        model = User
        fields = ("email", "name", "role")


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Django's UserAdmin expects a username, staff flags and permission groups;
    # our User has email login and a single role instead.
    add_form = UserCreateForm
    form = UserEditForm
    list_display = ("email", "name", "role", "is_active", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("email", "name")
    ordering = ("email",)
    filter_horizontal = ()
    readonly_fields = ("last_login", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("name", "role", "avatar_url", "is_active")}),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "name", "role", "password1", "password2")}),
    )


class GroupStudentInline(admin.TabularInline):
    model = GroupStudent
    extra = 0
    autocomplete_fields = ("student",)


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "professor", "created_at")
    list_filter = ("professor",)
    search_fields = ("name",)
    inlines = (GroupStudentInline,)


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "difficulty", "visibility", "created_by", "created_at")
    list_filter = ("visibility", "difficulty", "language")
    search_fields = ("title", "description")


class AssignmentGroupInline(admin.TabularInline):
    model = AssignmentGroup
    extra = 0


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "bug", "professor", "deadline", "status")
    list_filter = ("status", "professor")
    search_fields = ("title",)
    inlines = (AssignmentGroupInline,)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "bug", "assignment", "status", "grade", "submitted_at")
    list_filter = ("status",)
    search_fields = ("student__email", "student__name", "bug__title")
