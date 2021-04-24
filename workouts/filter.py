import django_filters
from base.models import Workout
from django.db import models
from django import forms

class WorkoutFilter(django_filters.FilterSet):
    training_type = django_filters.ChoiceFilter(choices=Workout.TRAINING, empty_label="All")
    body_focus = django_filters.ChoiceFilter(choices=Workout.BODYFOCUS, empty_label="All")

    class Meta:
        model = Workout
        fields = ['training_type', 'body_focus']
