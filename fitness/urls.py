"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from workouts import views as workouts_views
from workouts.views import WorkoutPlanListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    
    path('profile/', user_views.profile, name='profile'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('', include('exercises.urls')),

    path('workouts/', workouts_views.workouts_filter, name='workouts-filter'),
    path('programs/', WorkoutPlanListView.as_view(), name='workout-programs'),
    path('programs/<int:pk>', workouts_views.workoutplan_detail, name='workout-program-detail'),
    path('programs/<int:pk>/unfollow', workouts_views.unfollow_workoutplan, name='workout-program-unfollow'),
    path('programs/<int:pk>/follow', workouts_views.follow_workoutplan, name='workout-program-follow'),
    # path('programs/<int:pk>/follow', FollowWorkoutPlan.as_view(), name='workout-program-follow'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)