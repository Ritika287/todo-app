from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_email_success(self):
        """Test creating a user with email"""
        email = 'riti2874@gmail.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for a new user is normalized."""
        email = 'riti2874@GMAIL.COM'
        password = 'Testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_invalid_email(self):
        """Test creating s user with no email gives error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'riti2874@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
