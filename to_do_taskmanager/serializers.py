from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'task_text', 'status', 'author', 'assigned_to', 'created_at', 'edited_at')
