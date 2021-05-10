import django_filters
from base.models import Workout
from django.db import models
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class WorkoutFilter(django_filters.FilterSet):
    """
    Filter workouts by training type (e.g. HIIT, Strength...) and/or body focus (e.g. Upper, Lower body...)
    """
    training_type = django_filters.MultipleChoiceFilter(choices=Workout.TrainingType.choices, widget=forms.CheckboxSelectMultiple)
    body_focus = django_filters.MultipleChoiceFilter(choices=Workout.BodyFocus.choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Workout
        fields = ['training_type', 'body_focus']