from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#4287f5")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskManager(models.Manager):
    def pending(self):
        return self.filter(is_done=False)

    def overdue(self):
        return self.filter(is_done=False, due_date__lt=timezone.now())


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TaskManager()

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return self.title


class StudySession(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="sessions")
    started_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.task.title} - {self.duration_minutes}min"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note on {self.subject.name}"
