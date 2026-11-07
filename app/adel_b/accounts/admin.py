from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = "Debug GYM role"
    # Exactly one role per user: no "Add another" button, no empty second form.
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_editable = ("role",)
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")


# Show and change the role on each user's admin page.
admin.site.unregister(User)


@admin.register(User)
class DebugGymUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = (*UserAdmin.list_display, "role")

    @admin.display(description="Role")
    def role(self, user):
        return user.profile.get_role_display() if hasattr(user, "profile") else "Student"
