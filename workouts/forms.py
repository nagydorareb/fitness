from django import forms
import datetime
from base.models import Workout
from django.forms import ModelForm
# from bootstrap_modal_forms.forms import BSModalModelForm

class DateInput(forms.DateInput):
    input_type = 'date'

class StartingDateForm(ModelForm):   
    class Meta:
        model = Workout
        fields = ['workout_day']
        widgets = {'workout_day' : DateInput()}
        labels = {
            "workout_day": ""
        }

""" class StartingDateForm(BSModalModelForm):   
    class Meta:
        model = Workout
        fields = ['workout_day']
        widgets = {'workout_day' : DateInput()}
        labels = {
            "workout_day": "Start date of workout program"
        } """