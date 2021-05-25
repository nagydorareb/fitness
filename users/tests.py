from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import authenticate
from .forms import UserUpdateForm

class RegistrationTestCase(TestCase):
    """
    Tests registering a new user
    """
    def test_register(self):
        # Fetch the registration page
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Fill in the registration form
        registration_data = {'username': 'myusername',
                             'password1': 'Jelszo123',
                             'password2': 'Jelszo123',
                             'email': 'not an email', }
        count_before = User.objects.count()

        # Wrong email
        response = self.client.post(reverse('register'), registration_data)
        self.assertFalse(response.context['form'].is_valid())
        self.client.logout()

        # Correct email
        registration_data['email'] = 'my.email@example.com'
        response = self.client.post(reverse('register'), registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before + 1, count_after)
        self.client.logout()

        # Passwords don't match
        registration_data['password2'] = 'Jelszo12'
        response = self.client.post(reverse('register'), registration_data)
        self.assertFalse(response.context['form'].is_valid())
        self.client.logout()

class LoginTest(TestCase):
    """
    Tests the sign in process
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Jelszo123', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='testuser', password='Jelszo123')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='Jelszo123')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='testuser', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

class UpdateUserTestCase(TestCase):
    """
    Tests updating profile information by logged in user
    """
    def test_profile_update(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)

        form_data = {'username': 'NewUsername',
                     'email': 'myusername@email.com', }

        response = self.client.post(reverse('profile'), form_data)
        self.assertEqual(response.status_code, 302)