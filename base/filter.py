import django_filters
from django import forms
from base.models import Workout

class WorkoutDateFilter(django_filters.FilterSet):
    """
    Filter workouts by date on home page
    """
    workout_day = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), label='')

    class Meta:
        model = Workout
        fields = ['workout_day']