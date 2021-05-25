from django.test import TestCase, Client
from django.contrib.auth.models import User
from base.models import Workout, Exercise, MainExerciseSet, ExerciseSet, SimpleExerciseSet
from django.urls import reverse

class WorkoutModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Jelszo123')
        self.user.save()
        self.workout1 = Workout.objects.create(title='Test Workout 1',
                                                training_type=Workout.TrainingType.STRENGTH,
                                                body_focus=Workout.BodyFocus.LOWER_BODY,
                                                public=True,
                                                user=self.user, )
        self.workout1.save()

        self.workout2 = Workout.objects.create(title='Test Workout 2',
                                                training_type=Workout.TrainingType.YOGA,
                                                body_focus=Workout.BodyFocus.LOWER_BODY,
                                                public=True,
                                                user=self.user, )
        self.workout2.save()

    def test_created_properly(self):
        self.assertEqual(Workout.objects.count(), 2)
        self.workout3 = Workout.objects.create(title='Test Workout 3',
                                                training_type=Workout.TrainingType.CARDIO,
                                                body_focus=Workout.BodyFocus.CORE,
                                                public=True,
                                                user=self.user, )
        self.workout3.save()
        self.assertEqual(Workout.objects.count(), 3)

        self.assertEqual(self.workout1.title, 'Test Workout 1')
        self.assertEqual(self.workout1.public, True)
    
    def test_absolute_url(self):
        self.assertEqual(self.workout1.get_absolute_url(), reverse('workout_detail', args=[str(self.workout1.id)]))

    def test_is_simple_workout(self):
        self.assertEqual(True, self.workout2.training_type in {Workout.TrainingType.YOGA})

class ExerciseModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Jelszo123')
        self.user.save()

        self.exercise1 = Exercise.objects.create(name='Exercise 1',
                                                image='tests/push_up.jpg',
                                                focus=Exercise.Focus.LEGS,
                                                user=self.user, )
        self.exercise1.save()

    def test_created_properly(self):
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(self.exercise1.name, 'Exercise 1')

class MainExerciseSetModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Jelszo123')
        self.user.save()

        self.workout1 = Workout.objects.create(title='Test Workout 1',
                                                training_type=Workout.TrainingType.STRENGTH,
                                                body_focus=Workout.BodyFocus.LOWER_BODY,
                                                public=True,
                                                user=self.user, )
        self.workout1.save()

        self.exercise1 = Exercise.objects.create(name='Exercise 1',
                                                image='tests/push_up.jpg',
                                                focus=Exercise.Focus.LEGS,
                                                user=self.user, )
        self.exercise1.save()

    def test_created_properly(self):
        self.assertEqual(MainExerciseSet.objects.count(), 0)

        self.mainexerciseset1 = MainExerciseSet.objects.create(workout=self.workout1,
                                                                exercise=self.exercise1,
                                                                order=1, )
        self.mainexerciseset1.save()

        self.assertEqual(MainExerciseSet.objects.count(), 1)

class ExerciseSetModelTestCase(MainExerciseSetModelTestCase):

    def test_exercise_set_created_properly(self):
        self.assertEqual(ExerciseSet.objects.count(), 0)
        self.exerciseset1 = ExerciseSet.objects.create(workout=self.workout1,
                                                        exercise=self.exercise1,
                                                        order=2,
                                                        rep_num=12,)
        self.exerciseset1.save()
        self.assertEqual(ExerciseSet.objects.count(), 1)