from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from django.contrib.auth.models import User


class TestRegister(APITestCase):

    url = reverse_lazy('auth-signup')

    def test_register(self):
        self.assertFalse(User.objects.exists())

        response = self.client.post(self.url, data={
            'username': 'toto',
            'password': 'MyP@$$w0rd',
            'password2': 'MyP@$$w0rd',
            'email': 'toto@toto.fr',
            'first_name': 'toto',
            'last_name': 'tata'}
                                    )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(User.objects.exists())

    def test_name_already_exist(self):
        User.objects.create(
            username='toto',
            password='MyP@$$w0rd',
            email='toto@toto.fr',
            first_name='toto',
            last_name='tata'
        )
        response = self.client.post(self.url, data={
            'username': 'toto',
            'password': 'MyP@$$w0rd',
            'password2': 'MyP@$$w0rd',
            'email': 'toto@toto.fr',
            'first_name': 'toto',
            'last_name': 'tata'}
                                    )

        self.assertEqual(response.status_code, 400)

    def test_error_password(self):
        response = self.client.post(self.url, data={
            'username': 'titi',
            'password': 'MyP@$$w0rd',
            'password2': 'MyP@$$w0rds',
            'email': 'titi@titi.fr',
            'first_name': 'titi',
            'last_name': 'tutu'}
                                    )

        self.assertEqual(response.status_code, 400)

    def test_email_not_unique(self):
        User.objects.create(
            username='toto',
            password='MyP@$$w0rd',
            email='toto@toto.fr',
            first_name='toto',
            last_name='tata'
        )
        response = self.client.post(self.url, data={
            'username': 'tata',
            'password': 'MyP@$$w0rd',
            'password2': 'MyP@$$w0rd',
            'email': 'toto@toto.fr',
            'first_name': 'tata',
            'last_name': 'titi'}
                                    )

        self.assertEqual(response.status_code, 400)


class TestLogin(APITestCase):

    url = reverse_lazy('token_obtain_pair')

    def test_obtain_token(self):
        user = User.objects.create_user(
            username='toto',
            password='MyP@$$w0rd',
            email='toto@toto.fr',
            first_name='toto',
            last_name='tata'
        )
        user.save()

        response = self.client.post(self.url,
                                    {'username': 'toto',
                                     'password': 'MyP@$$w0rd'
                                     },
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        token = response.data['access']
        print(token)
