import django_filters
from django import forms
from base.models import Workout
from django.db import models

class WorkoutDateFilter(django_filters.FilterSet):
    workout_day = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Workout
        fields = ['workout_day']