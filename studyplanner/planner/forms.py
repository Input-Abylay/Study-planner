from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subject, Task, Note


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "color"]
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["subject", "title", "description", "priority", "due_date"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["subject"].queryset = Subject.objects.filter(user=user)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["subject"].queryset = Subject.objects.filter(user=user)
