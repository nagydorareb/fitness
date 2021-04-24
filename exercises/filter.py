import django_filters
from base.models import Exercise
from django.db import models

class ExerciseFilter(django_filters.FilterSet):
    focus = django_filters.ChoiceFilter(choices=Exercise.FOCUS, empty_label="All")

    class Meta:
        model = Exercise
        fields = ['focus']