from django import forms
from base.models import Exercise
from django.forms import ModelForm

class ExerciseCreateForm(forms.ModelForm):
    """
    Form for creating exercise
    """
    blank_choice = [('', 'Choose a focus...')] 
    focus = forms.ChoiceField(choices=blank_choice + Exercise.Focus.choices)
    class Meta:
        model = Exercise
        fields = [
            "name", 
            "image", 
            "description",
            "focus"
        ]