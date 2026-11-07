from django.contrib import admin

from accounts.models import Profile

from .models import Attempt, Bug, Draft, GroupMembership, TeachingGroup


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "difficulty", "topic")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ("bug", "user", "updated_at")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("bug", "user", "passed_count", "total_count", "created_at")


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0
    autocomplete_fields = ("student",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(
                profile__role=Profile.STUDENT, is_active=True, is_staff=False
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TeachingGroup)
class TeachingGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "member_count")
    search_fields = ("name", "teacher__username")
    autocomplete_fields = ("teacher",)
    inlines = (GroupMembershipInline,)

    @admin.display(description="Members")
    def member_count(self, group):
        return group.memberships.count()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(profile__role=Profile.PROFESSOR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
