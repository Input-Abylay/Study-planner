from django import template
from django.utils import timezone

register = template.Library()


@register.inclusion_tag("planner/_overdue_badge.html")
def overdue_count(tasks):
    """Custom inclusion tag: counts overdue, not-done tasks from a list/queryset
    and renders a small badge partial. Usage: {% overdue_count tasks %}"""
    now = timezone.now()
    count = sum(1 for t in tasks if not t.is_done and t.due_date < now)
    return {"count": count}


@register.filter
def priority_badge_class(priority):
    """Maps a task priority string to a Bootstrap-like CSS class."""
    return {
        "low": "badge-low",
        "medium": "badge-medium",
        "high": "badge-high",
    }.get(priority, "badge-medium")
