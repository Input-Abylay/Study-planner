from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, SubjectForm, TaskForm, NoteForm
from .models import Subject, Task, Note


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Welcome to Study Planner.")
            return redirect("dashboard")
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "planner/register.html", {"form": form})


@login_required
def dashboard_view(request):
    subject_id = request.GET.get("subject")  # event handler: filter dropdown
    tasks = Task.objects.filter(user=request.user)
    if subject_id:
        tasks = tasks.filter(subject_id=subject_id)

    subjects = Subject.objects.filter(user=request.user)
    context = {
        "tasks": tasks,
        "subjects": subjects,
        "selected_subject": int(subject_id) if subject_id else None,
    }
    return render(request, "planner/dashboard.html", context)


@login_required
def subject_list_view(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, f"Subject '{subject.name}' created.")
            return redirect("subject_list")
        messages.error(request, "Could not create subject. Check the form.")
    else:
        form = SubjectForm()

    subjects = Subject.objects.filter(user=request.user)
    return render(request, "planner/subject_list.html", {"subjects": subjects, "form": form})


@login_required
def task_create_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added.")
            return redirect("dashboard")
        messages.error(request, "Could not add task. Check the form.")
    else:
        form = TaskForm(user=request.user)
    return render(request, "planner/task_form.html", {"form": form})


@login_required
def task_toggle_done_view(request, pk):
    # event handler: submit button that toggles completion
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect("dashboard")


@login_required
def task_delete_view(request, pk):
    # event handler: delete link
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("dashboard")


@login_required
def note_create_view(request):
    if request.method == "POST":
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note saved.")
            return redirect("note_list")
        messages.error(request, "Could not save note.")
    else:
        form = NoteForm(user=request.user)

    notes = Note.objects.filter(user=request.user)
    return render(request, "planner/note_list.html", {"form": form, "notes": notes})
