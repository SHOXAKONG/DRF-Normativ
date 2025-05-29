from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('tasks', views.TaskViewSet, basename='task')
router.register('tasks_assignment', views.TaskAssignmentViewSet, basename='tasks_assignment')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('tag', views.TagViewSet, basename='tag')

urlpatterns = [
    path('hello/', views.HelloAPIView.as_view(), name='hello'),
    path('', include(router.urls))
]
