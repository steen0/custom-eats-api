from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        test_emails = [
            ['TEST@Example.com', 'TEST@example.com'],
            ['teSt2@example.cOm', 'teSt2@example.com'],
            ['test3@example.COM', 'test3@example.com'],
            ['tEst@EXAMPLE.COM', 'tEst@example.com']
        ]
        password = 'testpass123'
        for e in test_emails:
            user = get_user_model().objects.create_user(
                email=e[0],
                password=password
            )
            self.assertEqual(user.email, e[1])

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='zerd')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='password',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_upgrade_user_successful(self):
        user = get_user_model().objects.create_user(
            email='testUpgrade@example.com',
            )
        user = get_user_model().objects.upgrade_user(
            email='testUpgrade@example.com',
            )
        self.assertTrue(user.is_superuser)

    def test_upgrade_user_does_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.upgrade_user(
                    email='testUpgrade@example.com',
                )
