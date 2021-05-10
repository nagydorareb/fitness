from django.urls import path
from . import views
from .views import (
    WorkoutAddView, 
    WorkoutUpdateView, 
    WorkoutDeleteView
)

urlpatterns = [
    # The landing page
    path('', views.home, name='home'),
    path('workout/add/', WorkoutAddView.as_view(), name='add'),
    path('workout/<int:pk>/fav/', views.fav_add, name='fav_add'),
    path('workout/favorites', views.workout_favorites, name='workout_favorites'),

    # Workout exercise sets
    path('workout/<int:pk>/', views.view, name='workout_detail'),
    path('workout/<int:pk>/order/', views.save_new_ordering, name='ordering'),
    path('workout/<int:pk>/update/', WorkoutUpdateView.as_view(), name='update'),
    path('workout/<int:pk>/delete/', WorkoutDeleteView.as_view(), name='delete'),

    # Add, edit, delete exercise set
    path('workout/<int:workout_pk>/add/', views.add_exercise, name='add_exercise'),
    path('workout/<int:workout_pk>/<int:exercise_pk>/add/', views.add_exercise, name='add_exercise'),
    path('workout/<int:workout_pk>/<int:exercise_set_pk>/update/', views.exercise_set_update, name='exercise_update'),
    path('workout/<int:workout_pk>/<int:exercise_set_pk>/delete/', views.exercise_set_delete, name='exercise_delete'),

    # Calendar view
    path('calendar/', views.workout_calendar, name='workout-calendar'),
    path('calendar/<int:year>/<int:month>/', views.workout_calendar, name='workout-calendar'),
]