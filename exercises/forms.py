from django import forms
from base.models import Exercise
from django.forms import ModelForm, ModelChoiceField

class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            "name", 
            "image", 
            "description", 
            "focus"
        ]