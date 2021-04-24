from django import forms
from base.models import Exercise
from django.forms import ModelForm, ModelChoiceField

class ExerciseCreateForm(forms.ModelForm):
    # focus = ModelChoiceField(queryset=Exercise.FOCUS, empty_label="Choose a focus...")
    # focus = forms.ChoiceField(choices=Exercise.FOCUS, placeholder="Choose a focus...", required=True)
    blank_choice = [('', 'Choose a focus...')] 
    focus = forms.ChoiceField(choices=blank_choice + Exercise.FOCUS)
    class Meta:
        model = Exercise
        fields = [
            "name", 
            "image", 
            "description",
            "focus"
        ]