from django.urls import path, include
from . import views
from .views import WorkoutPlanListView

urlpatterns = [
    path('', views.workouts_filter, name='workouts-filter'),

    path('programs/', include([
        path('', WorkoutPlanListView.as_view(), name='workout-programs'),
        path('<int:pk>/', views.workoutplan_detail, name='workout-program-detail'),
        path('<int:pk>/unfollow/', views.unfollow_workoutplan, name='workout-program-unfollow'),
        path('<int:pk>/follow/', views.follow_workoutplan, name='workout-program-follow'),
    ])),
]