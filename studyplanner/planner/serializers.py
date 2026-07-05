from rest_framework import serializers
from .models import Subject, Task, StudySession, Note


# ---------- ModelSerializer-based (>=2) ----------

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "color", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "subject", "subject_name", "title", "description",
            "priority", "due_date", "is_done", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


# ---------- Plain Serializer-based (>=2) ----------

class StudySessionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    started_at = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True, default="")

    def create(self, validated_data):
        return StudySession.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.subject = validated_data.get("subject", instance.subject)
        instance.save()
        return instance
