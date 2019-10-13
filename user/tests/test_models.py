from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_username_successful(self):
        """Test creating a new user with an email is successful"""
        username = 'admins'
        password = 'admins'
        user = get_user_model().objects.create_user(
			username = username,
			password=password
		)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    
    def test_new_user_invalid_username(self):
        """Test creating user with no username raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_user_invalid_password(self):
        """Test creating user with no username raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test', None)

    