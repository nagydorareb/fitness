import django_filters
from base.models import Exercise
from django.db import models

class ExerciseFilter(django_filters.FilterSet):

    ARMS = 'AR'
    LEGS = 'LG'
    CORE = 'CR'
    BACK = 'BK'
    CHEST = 'CH'
    SHOULDERS = 'SH'
    FULLBODY = 'FB'
    CARDIO = 'CA'
    YOGAPOSE = 'YP'

    FOCUS = [
        (ARMS, 'Arms'),
        (LEGS, 'Legs'),
        (CORE, 'Core'),
        (BACK, 'Back'),
        (CHEST, 'Chest'),
        (SHOULDERS, 'Shoulders'),
        (FULLBODY, 'Full Body'),
        (CARDIO, 'Cardio'),
        (YOGAPOSE, 'Yoga Pose'),
    ]

    focus = django_filters.ChoiceFilter(choices=FOCUS, empty_label="All")

    class Meta:
        model = Exercise
        fields = ['focus']