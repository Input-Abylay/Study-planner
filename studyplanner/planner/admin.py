from django.contrib import admin
from .models import Subject, Task, StudySession, Note


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color", "created_at")
    list_filter = ("user",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "user", "priority", "due_date", "is_done")
    list_filter = ("priority", "is_done", "subject")
    search_fields = ("title", "description")
    date_hierarchy = "due_date"


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("task", "started_at", "duration_minutes")
    list_filter = ("task__subject",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "created_at")
    search_fields = ("content",)
