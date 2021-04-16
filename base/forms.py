from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import ExerciseSet, Exercise

class SetForm(ModelForm):
    exercise = ModelChoiceField(queryset=Exercise.objects.all(), label=('Exercise'), empty_label="Choose an exercise...")

    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'set_num', 'rep_num', 'rep_type', 'weight_num', 'weight_type']
        exclude = ('workout',)

class SetUpdateForm(ModelForm):
    exercise = ModelChoiceField(queryset=Exercise.objects.all(), label=('Exercise'))

    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'set_num', 'rep_num', 'rep_type', 'weight_num', 'weight_type']
        exclude = ('workout',)