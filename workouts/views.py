from django.shortcuts import render
from base.models import Workout
from .filter import WorkoutFilter

def workouts_filter(request):
    f = WorkoutFilter(request.GET, queryset=Workout.objects.all())
    return render(request, 'workouts/workout_filter.html', {'filter': f})