from django.test import SimpleTestCase
from django.urls import reverse, resolve

from base.views import *

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_add_url_resolves(self):
        url = reverse('add')
        self.assertEquals(resolve(url).func.view_class, WorkoutAddView)

    def test_favadd_url_resolves(self):
        url = reverse('fav_add', args=[1])
        self.assertEquals(resolve(url).func, fav_add)

    def test_workout_favorites_url_resolves(self):
        url = reverse('workout_favorites')
        self.assertEquals(resolve(url).func, workout_favorites)

    def test_workout_detail_url_resolves(self):
        url = reverse('workout_detail', args=[1])
        self.assertEquals(resolve(url).func, view)

    def test_ordering_url_resolves(self):
        url = reverse('ordering', args=[1])
        self.assertEquals(resolve(url).func, save_new_ordering)

    def test_workout_update_url_resolves(self):
        url = reverse('update', args=[1])
        self.assertEquals(resolve(url).func.view_class, WorkoutUpdateView)

    def test_workout_delete_url_resolves(self):
        url = reverse('delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, WorkoutDeleteView)

    def test_add_exercise_url_resolves(self):
        url = reverse('add_exercise', args=[1])
        self.assertEquals(resolve(url).func, add_exercise)

    def test_add_exercise_from_bank_url_resolves(self):
        url = reverse('add_exercise', args=[1,2])
        self.assertEquals(resolve(url).func, add_exercise)

    def test_exercise_set_update_url_resolves(self):
        url = reverse('exercise_update', args=[1,2])
        self.assertEquals(resolve(url).func, exercise_set_update)

    def test_exercise_set_delete_url_resolves(self):
        url = reverse('exercise_delete', args=[1,2])
        self.assertEquals(resolve(url).func, exercise_set_delete)

    def test_calendar_url_resolves(self):
        url = reverse('workout-calendar')
        self.assertEquals(resolve(url).func, workout_calendar)

    def test_calendar_with_args_url_resolves(self):
        url = reverse('workout-calendar', args=[2021,5])
        self.assertEquals(resolve(url).func, workout_calendar)