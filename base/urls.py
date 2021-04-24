from django.urls import path
from . import views
from .views import WorkoutAddView, WorkoutUpdateView, WorkoutDeleteView

urlpatterns = [

    # The landing page
    path('', views.index, name='index'),
    path('workout/', views.home, name='home'),

    path('workout/<int:pk>/', views.view, name='workout_detail'),
    path('workout/add/', WorkoutAddView.as_view(), name='add'),

    path('workout/<int:pk>/update/', WorkoutUpdateView.as_view(), name='update'),
    path('workout/<int:pk>/delete/', WorkoutDeleteView.as_view(), name='delete'),

    # Add exercise set to workout
    path('workout/<int:workout_pk>/add/', views.add_exercise, name='add_exercise'),
    path('workout/<int:workout_pk>/<int:pk>/', views.exercise_set_view, name='exercise_set_detail'),
    path('workout/<int:workout_pk>/<int:pk>/update/', views.exercise_set_update, name='exercise_update'),
    path('workout/<int:workout_pk>/<int:pk>/delete/', views.exercise_set_delete, name='exercise_delete'),

    path('calendar/', views.workout_calendar, name='workout-calendar'),
    path('calendar/<int:year>/<int:month>/', views.workout_calendar, name='workout-calendar'),
]