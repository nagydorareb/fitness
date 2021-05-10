from django.urls import path
from . import views
from .views import WorkoutPlanListView

urlpatterns = [
    path('workouts/', views.workouts_filter, name='workouts-filter'),
    
    path('programs/', WorkoutPlanListView.as_view(), name='workout-programs'),
    path('programs/<int:pk>', views.workoutplan_detail, name='workout-program-detail'),
    path('programs/<int:pk>/unfollow', views.unfollow_workoutplan, name='workout-program-unfollow'),
    path('programs/<int:pk>/follow', views.follow_workoutplan, name='workout-program-follow'),
]