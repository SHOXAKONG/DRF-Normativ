from django.utils import timezone
from rest_framework import serializers
from .models import Task, Projects, Tag, TaskAssignment, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['name', 'description', 'owner', 'members']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Title is too short')
        return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'project']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate(self, data):
        if data['due_data'] and data['due_data'] < timezone.now().date():
            raise serializers.ValidationError("Due Data Cannot be in the past")
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'name'


class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = ['task', 'user', 'assign_at']

    def validate(self, data):
        if data['assign_at'] and data['assign_at'] < timezone.now().date():
            raise serializers.ValidationError("Assign Data Cannot be in the past")
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['task', 'user', 'content']
