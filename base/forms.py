from django import forms
from django.forms import ModelForm
from .models import Workout, ExerciseSet, SimpleExerciseSet, Exercise
from .helpers import setform_helper, simplesetform_helper

class SimpleSetForm(ModelForm): 
    """
    Form for adding exercises to workouts without sets/reps
    """
    class Meta:
        model = SimpleExerciseSet
        fields = ['exercise']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = simplesetform_helper()

        if 'exercise' in self.data:
            self.fields['exercise'].queryset = Exercise.objects.all()

class SimpleSetUpdateForm(ModelForm):
    """
    Form for updating exercises in workouts without sets/reps
    """
    class Meta:
        model = SimpleExerciseSet
        fields = ['exercise']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = simplesetform_helper()
        self.fields['exercise'].queryset = Exercise.objects.none()

        if 'exercise' in self.data:
            self.fields['exercise'].queryset = Exercise.objects.all()
        elif self.instance.pk:
            self.fields['exercise'].queryset = Exercise.objects.all().filter(pk=self.instance.exercise.pk)

class SetForm(ModelForm):
    """
    Form for adding exercises to workouts with sets/reps
    """
    class Meta:
        model = ExerciseSet
        exclude = ('workout', 'order')
        help_texts = {
            'weight_num': 'For body-weight exercise leave weight set to <em>0</em>',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = setform_helper()

        if 'exercise' in self.data:
            self.fields['exercise'].queryset = Exercise.objects.all()

class SetUpdateForm(ModelForm):
    """
    Form for updating exercises in workouts with sets/reps
    """
    class Meta:
        model = ExerciseSet
        exclude = ('workout', 'order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = setform_helper()

        self.fields['exercise'].queryset = Exercise.objects.none()

        if 'exercise' in self.data:
            self.fields['exercise'].queryset = Exercise.objects.all()

        # for exercise set updates:
        elif self.instance.pk:
            self.fields['exercise'].queryset = Exercise.objects.all().filter(pk=self.instance.exercise.pk)

class DateInput(forms.DateInput):
    input_type = 'date'

class WorkoutForm(ModelForm):
    """
    Form for creating workouts
    """
    blank_choice_training = [('', 'Choose a training type...')] 
    training_type = forms.ChoiceField(choices=blank_choice_training + Workout.TrainingType.choices)

    blank_choice = [('', 'Choose a body focus...')] 
    body_focus = forms.ChoiceField(choices=blank_choice + Workout.BodyFocus.choices)
    
    class Meta:
        model = Workout
        fields = ['title', 'workout_day', 'training_type', 'body_focus', 'public']
        widgets = {
            'workout_day' : DateInput(),
            'public': forms.RadioSelect
        }
        labels = {
            'public': ''
        }

class OrderingForm(forms.Form):
    """
    Form for ordering exercises inside workouts
    """
    ordering = forms.CharField()
