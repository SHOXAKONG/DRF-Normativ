from django.urls import path

from app import views

urlpatterns = [
    path('hello/', views.HelloAPIView.as_view(), name='hello')
]