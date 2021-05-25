from django.test import TestCase, Client
from django.urls import reverse
from base.models import *
import json
from base.filter import WorkoutDateFilter
from django.db.models import Q
from django.utils import timezone

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Jelszo123')
        self.user.save()

        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com')
        self.user2.set_password('Jelszo123')
        self.user2.save()

        self.client.login(username='testuser', password='Jelszo123')

        self.workout1 = Workout.objects.create(title='Test Workout 1',
                                                training_type=Workout.TrainingType.STRENGTH,
                                                body_focus=Workout.BodyFocus.LOWER_BODY,
                                                public=True,
                                                user=self.user, )
        self.workout1.save()

        self.exercise1 = Exercise.objects.create(user=self.user, name='Squat', focus=Exercise.Focus.LEGS)
        self.exercise2 = Exercise.objects.create(user=self.user, name='Push Up', focus=Exercise.Focus.CHEST)
        self.exercise3 = Exercise.objects.create(user=self.user, name='Plank', focus=Exercise.Focus.CORE)

        self.exercise_set1 = MainExerciseSet.objects.create(workout=self.workout1, exercise=self.exercise1)
        self.exercise_set2 = MainExerciseSet.objects.create(workout=self.workout1, exercise=self.exercise2)
        self.exercise_set3 = MainExerciseSet.objects.create(workout=self.workout1, exercise=self.exercise3)

        self.exercise_set_delete = SimpleExerciseSet.objects.create(workout=self.workout1, exercise=self.exercise1)
        self.exercise_set_delete.save()

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

        self.client.logout()

        # Tests the home page for not logged in users
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/index.html')

    def test_view(self):
        response = self.client.get(reverse('workout_detail', args=[self.workout1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/detail.html')

        # Ensure a non-existant pk throws a Not Found.
        response = self.client.get(reverse('workout_detail', args=[333]))
        self.assertEqual(response.status_code, 404)

    def test_fav_add(self):
        response = self.client.get(reverse('fav_add', args=[self.workout1.id]), HTTP_REFERER='http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 302)

        # Checks if workout was added to favorites
        workout_in_favorites = self.workout1.favorites.filter(id=self.user.id).exists()
        self.assertTrue(workout_in_favorites)

    def test_workout_favorites(self):
        response = self.client.get(reverse('workout_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/favorites.html')

    def test_save_new_ordering(self):
        data = {'ordering': ['2,1,3']}

        response = self.client.post(reverse('ordering', args=[self.workout1.id]), data)
        self.assertEqual(response.status_code, 302)

        self.exercise_set2.refresh_from_db()
        self.assertEqual(self.exercise_set2.order, 1)

    def test_workout_calendar(self):
        response = self.client.get(reverse('workout-calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/workout_calendar.html')

    def test_workout_calendar_args(self):
        response = self.client.get(reverse('workout-calendar', args=[2021,5]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/workout_calendar.html')

    def test_add_workout(self):
        count_before = Workout.objects.count()
        data = {
            'title': 'New Workout', 
            'workout_day': date.today(), 
            'training_type': Workout.TrainingType.STRENGTH, 
            'body_focus': Workout.BodyFocus.LOWER_BODY, 
            'public': True
        }

        response = self.client.post(reverse('add'), data)
        self.assertEqual(response.status_code, 302)

        # Checks if workout was created
        count_after = Workout.objects.count()
        self.assertEqual(count_before + 1, count_after)

    def test_update_workout(self):
        data = {
            'title': 'Workout Update', 
            'workout_day': date.today(), 
            'training_type': Workout.TrainingType.STRENGTH, 
            'body_focus': Workout.BodyFocus.LOWER_BODY, 
            'public': True,
        }

        response = self.client.get(reverse('update', args=[self.workout1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/workout_update.html')

        response = self.client.post(reverse('update', kwargs={'pk': self.workout1.id}), data)
        self.assertEqual(response.status_code, 302)

        self.workout1.refresh_from_db()
        self.assertEqual(self.workout1.title, 'Workout Update')

    def test_delete_workout(self):
        self.workout_d = Workout.objects.create(title='Workout to delete',
                                                training_type=Workout.TrainingType.STRENGTH,
                                                body_focus=Workout.BodyFocus.LOWER_BODY,
                                                public=True,
                                                user=self.user, )
        self.workout_d.save()
        count_before = Workout.objects.count()

        data = {
            'title': self.workout_d.title
        }

        response = self.client.post(reverse('delete', kwargs={'pk': self.workout_d.id}), data)
        self.assertEqual(response.status_code, 302)

        # Checks if workout was deleted
        count_after = Workout.objects.count()
        self.assertEqual(count_before - 1, count_after)

    def test_exercise_set_delete(self):
        self.workout6 = Workout.objects.create(title='Test Workout 1',
                                                training_type=Workout.TrainingType.YOGA,
                                                body_focus=Workout.BodyFocus.CORE,
                                                public=True,
                                                user=self.user, )
        self.workout6.save()

        self.exercise1 = Exercise.objects.create(user=self.user, name='Squat', focus=Exercise.Focus.LEGS)

        self.exercise_set_delete = SimpleExerciseSet.objects.create(workout=self.workout6, exercise=self.exercise1)
        self.exercise_set_delete.save()

        count_before = SimpleExerciseSet.objects.count()

        response = self.client.post(reverse("exercise_delete", args=[self.workout6.id, self.exercise_set_delete.id]))
        self.assertEqual(response.status_code, 302)

        # Checks if workout was deleted
        count_after = SimpleExerciseSet.objects.count()
        self.assertEqual(count_before - 1, count_after)