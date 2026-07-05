from django.urls import path
from . import api_views, auth_views

urlpatterns = [
    # Auth
    path("auth/login/", auth_views.api_login, name="api_login"),
    path("auth/logout/", auth_views.api_logout, name="api_logout"),

    # Tasks (FBV, full CRUD)
    path("tasks/", api_views.task_list_create, name="api_task_list_create"),
    path("tasks/<int:pk>/", api_views.task_detail, name="api_task_detail"),

    # Subjects (CBV)
    path("subjects/", api_views.SubjectListCreateView.as_view(), name="api_subject_list_create"),
    path("subjects/<int:pk>/", api_views.SubjectDetailView.as_view(), name="api_subject_detail"),

    # Study sessions (CBV)
    path("sessions/", api_views.StudySessionView.as_view(), name="api_session_list_create"),

    # Notes (CBV)
    path("notes/", api_views.NoteListCreateView.as_view(), name="api_note_list_create"),
]
