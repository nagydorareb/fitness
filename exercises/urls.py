from django.urls import path
from . import views

urlpatterns = [
    path('bank/', views.exercise_filter, name='exercise-filter'),
    path('add/', views.exercise_create, name='exercise-create'),
    path('<int:pk>/', views.exercise_detail, name='exercise-detail'),
]