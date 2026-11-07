from django.contrib import admin

from .models import Assignment, Attempt, Bug, Draft


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


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("bug", "student", "assigned_by", "due_date")
    list_filter = ("bug",)
