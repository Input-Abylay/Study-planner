from .models import Task


def pending_task_count(request):
    """Injects the number of pending (not done) tasks for the logged-in user
    into every template's context, so the nav bar badge can show it anywhere."""
    if request.user.is_authenticated:
        count = Task.objects.filter(user=request.user, is_done=False).count()
    else:
        count = 0
    return {"pending_task_count": count}
