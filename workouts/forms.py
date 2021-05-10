from django import forms
from base.models import Workout
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'

class StartingDateForm(ModelForm): 
    """
    Form for setting a starting date for workout program
    """  
    class Meta:
        model = Workout
        fields = ['workout_day']
        widgets = {'workout_day' : DateInput()}
        labels = {
            "workout_day": ""
        }