from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test the user API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating using with a valid payload is successful"""
        payload = {
            'email': 'riti2468@gmail.com',
            'password': 'testpass',
            'name': 'Riti',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_already_present(self):
        """Test creatring a user that already exists"""
        payload = {
            'email': 'riti2864@gmail.com',
            'password': 'Test1234',
            'name': 'Riti'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """Test that password must be more then 8 characters"""
        payload = {
            'email': 'riti2468@gmail.com',
            'password': 'Test',
            'name': 'Riti'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists, False)

    def test_creating_token_for_user(self):
        """Test token is created for the user"""
        payload = {
            'email': 'ritika2367@gmail.com',
            'password': 'Testpass'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_inavlid_cred(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='riti23456@gmail.com', password='Test12345')
        payload = {'email': 'riti23456@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'riti2456@gmail.com',
            'password': 'Test@1233'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_fieldmissing(self):
            """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'NA', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
