from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Workout, ExerciseSet, Exercise

class SetForm(ModelForm):
    # exercise = ModelChoiceField(queryset=Exercise.objects.all(), label=('Exercise'), empty_label="Choose an exercise...")

    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'set_num', 'rep_num', 'rep_type', 'weight_num', 'weight_type']
        exclude = ('workout',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['exercise'].queryset = Exercise.objects.none()

        if 'exercise' in self.data:
            self.fields['exercise'].queryset = Exercise.objects.all()

class SetUpdateForm(ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'set_num', 'rep_num', 'rep_type', 'weight_num', 'weight_type']
        exclude = ('workout',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise'].queryset = Exercise.objects.none()

        if 'exercise' in self.data:
            self.fields['exercise'].queryset = Exercise.objects.all()

        # for exercise set updates:
        elif self.instance.pk:
            self.fields['exercise'].queryset = Exercise.objects.all().filter(pk=self.instance.exercise.pk)

class DateInput(forms.DateInput):
    input_type = 'date'

class WorkoutForm(ModelForm):
    blank_choice_training = [('', 'Choose a training type...')] 
    training_type = forms.ChoiceField(choices=blank_choice_training + Workout.TRAINING)

    blank_choice = [('', 'Choose a body focus...')] 
    body_focus = forms.ChoiceField(choices=blank_choice + Workout.BODYFOCUS)
    
    class Meta:
        model = Workout
        fields = ['title', 'workout_day', 'training_type', 'body_focus']
        widgets = {'workout_day' : DateInput()}


