# [Student Dev] Values the student sidebar needs on every page
def student_nav(request):
    """The number of assignments a student still has to do, for the sidebar badge."""
    user = getattr(request, "user", None)
    if not (user and user.is_authenticated and getattr(user, "is_student", False)):
        return {}
    if not request.resolver_match or request.resolver_match.app_name != "student":
        return {}
    from .views import attach_status, my_assignments

    todo = sum(1 for a in attach_status(my_assignments(user), user) if a.my_status == "todo")
    return {"student_todo_count": todo}
