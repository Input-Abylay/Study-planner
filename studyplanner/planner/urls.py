from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("subjects/", views.subject_list_view, name="subject_list"),
    path("tasks/create/", views.task_create_view, name="task_create"),
    path("tasks/<int:pk>/toggle/", views.task_toggle_done_view, name="task_toggle"),
    path("tasks/<int:pk>/delete/", views.task_delete_view, name="task_delete"),
    path("notes/", views.note_create_view, name="note_list"),

    # Auth (Django built-in + custom register)
    path("login/", auth_views.LoginView.as_view(template_name="planner/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
]
