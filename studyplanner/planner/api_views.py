from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, Subject, StudySession, Note
from .serializers import (
    TaskSerializer,
    SubjectSerializer,
    StudySessionSerializer,
    NoteSerializer,
)


# ---------------- Function-Based Views with DRF decorators (>=2) ----------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def task_list_create(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "GET":
        return Response(TaskSerializer(task).data)

    if request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- Class-Based Views using APIView (>=2) ----------------

class SubjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subjects = Subject.objects.filter(user=request.user)
        return Response(SubjectSerializer(subjects, many=True).data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Subject, pk=pk, user=user)

    def get(self, request, pk):
        subject = self.get_object(pk, request.user)
        return Response(SubjectSerializer(subject).data)

    def put(self, request, pk):
        subject = self.get_object(pk, request.user)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        subject = self.get_object(pk, request.user)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudySessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = StudySession.objects.filter(task__user=request.user)
        return Response(StudySessionSerializer(sessions, many=True).data)

    def post(self, request):
        serializer = StudySessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoteListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        return Response(NoteSerializer(notes, many=True).data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
