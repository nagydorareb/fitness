import django_filters
from base.models import Exercise
from django.db import models
from django import forms

class ExerciseFilter(django_filters.FilterSet):
    """
    Filter exercises by body focus (chest, back, legs, ...)
    """
    focus = django_filters.MultipleChoiceFilter(choices=Exercise.Focus.choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Exercise
        fields = ['focus']