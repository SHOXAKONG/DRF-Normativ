from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Projects, Task, Tag, TaskAssignment, Comment
from .pagination import PaginationPage
from .serializers import TaskSerializer, TagSerializer, ProjectSerializer, TaskAssignmentSerializer, CommentSerializer


class HelloAPIView(APIView):
    def get(self, request):
        data = {"message": "Hello World"}
        return Response(data=data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationPage
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['-id']


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'project']
    search_fields = ['title']
    ordering_fields = ['title', 'due_date', 'priority', 'created_at']
    ordering = ['-due_date']
    pagination_class = PaginationPage

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.owner != self.request.user:
            raise PermissionDenied("Only Owner Can create task")
        serializer.save()

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue_tasks(self, request):
        now = timezone.now().date()
        overdue = self.queryset.filter(due_date__lt=now)
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_done(self, request, pk=None):
        task = self.get_object()
        task.status = 'DONE'
        task.save()
        return Response({"status" : "Task Marked Done"})

class TagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='today')
    def today_assignment(self, request):
        today = timezone.now().date()
        assignments = self.queryset.filter(assign_at=today)
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
