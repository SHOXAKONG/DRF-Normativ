from django.db import models
from django.utils import timezone

from common.models import BaseModel
from users.models import Users


class Tag(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tag'


class Projects(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='project_owner')
    members = models.ManyToManyField(Users)

    class Meta:
        db_table = 'project'



class Task(BaseModel):

    PRIORITY_CHOICES = (
        ('low', "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH")
    )

    STATUS_CHOICES = (
        ("to do", "TODO"),
        ("in_progress", "IN_PROGRESS"),
        ("done", "DONE")
    )

    title = models.CharField(max_length=200)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='task_project')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES)
    description = models.TextField()
    due_date = models.DateTimeField(default=timezone.now)
    tag = models.ManyToManyField(Tag)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task'

class TaskAssignment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_assignment')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='assignment_user')
    assign_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'task_assignment'

class Comment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comment')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comment_user')
    content = models.TextField()
