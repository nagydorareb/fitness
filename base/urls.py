from django.urls import path, include
from . import views
from .views import (
    WorkoutAddView, 
    WorkoutUpdateView, 
    WorkoutDeleteView
)

urlpatterns = [
    # The landing page
    path('', views.home, name='home'),

    path('workout/', include([
        # Create and save workouts
        path('add/', WorkoutAddView.as_view(), name='add'),
        path('<int:pk>/fav/', views.fav_add, name='fav_add'),
        path('favorites/', views.workout_favorites, name='workout_favorites'),

        # Workout exercise sets
        path('<int:pk>/', views.view, name='workout_detail'),
        path('<int:pk>/order/', views.save_new_ordering, name='ordering'),
        path('<int:pk>/update/', WorkoutUpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', WorkoutDeleteView.as_view(), name='delete'),

        # Add, edit, delete exercise set
        path('<int:workout_pk>/add/', views.add_exercise, name='add_exercise'),
        path('<int:workout_pk>/<int:exercise_pk>/add/', views.add_exercise, name='add_exercise'),
        path('<int:workout_pk>/<int:exercise_set_pk>/update/', views.exercise_set_update, name='exercise_update'),
        path('<int:workout_pk>/<int:exercise_set_pk>/delete/', views.exercise_set_delete, name='exercise_delete'),
    ])),

    # Calendar view
    path('calendar/', views.workout_calendar, name='workout-calendar'),
    path('calendar/<int:year>/<int:month>/', views.workout_calendar, name='workout-calendar'),
]