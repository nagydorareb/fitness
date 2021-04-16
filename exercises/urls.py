from django.urls import path
from . import views

urlpatterns = [
    path('exercises/bank/filter', views.exercise_filter, name='exercise-filter'),
    path('exercises/add', views.exercise_create, name='exercise-create'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise-detail'),
]