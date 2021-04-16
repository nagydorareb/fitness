import django_filters
from base.models import Workout
from django.db import models
from django import forms

class WorkoutFilter(django_filters.FilterSet):
    HIIT = 'HI'
    STRENGTH = 'ST'
    YOGA = 'YO'
    CARDIO = 'CA'

    TRAINING = [
        (HIIT, 'HIIT'),
        (STRENGTH, 'Strength Training'),
        (YOGA, 'Yoga'),
        (CARDIO, 'Cardio'),
    ]

    UPPER = 'UP'
    LOWER = 'LW'
    CORE = 'CR'
    TOTAL = 'TL'

    BODYFOCUS = [
        (UPPER, 'Upper Body'), 
        (LOWER, 'Lower Body'),
        (CORE, 'Core'),
        (TOTAL, 'Total Body'),
    ]

    training_type = django_filters.ChoiceFilter(choices=TRAINING, empty_label="All")
    body_focus = django_filters.ChoiceFilter(choices=BODYFOCUS, empty_label="All")

    class Meta:
        model = Workout
        fields = ['training_type', 'body_focus']
