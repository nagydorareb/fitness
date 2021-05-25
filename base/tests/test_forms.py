from django.test import TestCase, Client
from base.forms import *
from datetime import date
from base.models import *

class TestForms(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Jelszo123')
        self.user.save()

        self.client.login(username='testuser', password='Jelszo123')

        self.exercise1 = Exercise.objects.create(user=self.user, name='Squat', focus=Exercise.Focus.LEGS)

    def test_workout_form(self):
        self.assertEqual(list(WorkoutForm.base_fields), ['title', 'workout_day', 'training_type', 'body_focus', 'public'])

        form = WorkoutForm(data={
            'title': 'Workout Form',
            'workout_day': date.today(), 
            'training_type': Workout.TrainingType.STRENGTH, 
            'body_focus': Workout.BodyFocus.LOWER_BODY, 
            'public': True
        })

        self.assertTrue(form.is_valid())

    def test_simple_set_form(self):
        self.assertEqual(list(SimpleSetForm.base_fields), ['exercise'])

        form = SimpleSetForm(data={
            'exercise': self.exercise1
        })

        self.assertTrue(form.is_valid())

    def test_set_form(self):
        self.assertEqual(list(SetForm.base_fields), ['exercise', 'set_num', 'rep_num', 'rep_type', 'weight_num', 'weight_type', 'rest_time'])

        form = SetForm(data={
            'exercise': self.exercise1,
            'set_num': 4, 
            'rep_num': 12, 
            'rep_type': ExerciseSet.REP, 
            'weight_num': 20, 
            'weight_type': ExerciseSet.KG, 
            'rest_time': 60
        })

        self.assertTrue(form.is_valid())

    def test_simple_set_update_form(self):
        self.assertEqual(list(SimpleSetUpdateForm.base_fields), ['exercise'])

        form = SimpleSetUpdateForm(data={
            'exercise': self.exercise1
        })

        self.assertTrue(form.is_valid())

    def test_set_update_form(self):
        self.assertEqual(list(SetUpdateForm.base_fields), ['exercise', 'set_num', 'rep_num', 'rep_type', 'weight_num', 'weight_type', 'rest_time'])

        form = SetUpdateForm(data={
            'exercise': self.exercise1,
            'set_num': 4, 
            'rep_num': 12, 
            'rep_type': ExerciseSet.REP, 
            'weight_num': 20, 
            'weight_type': ExerciseSet.KG, 
            'rest_time': 60
        })

        self.assertTrue(form.is_valid())

    def test_ordering(self):
        self.assertEqual(list(OrderingForm.base_fields), ['ordering'])

        form = OrderingForm(data={
            'ordering': '[2,3,1]'
        })

        self.assertTrue(form.is_valid())