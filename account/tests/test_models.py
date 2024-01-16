from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from ..models import CustomerUser, CustomerProfile


class BaseCustomerModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def create_customer_user(self, is_superuser=False, is_active=False,
                             **kwargs):
        user_data = self.user_data.copy()
        user_data.update(kwargs)
        user = CustomerUser.objects.create_user(**user_data)
        if is_superuser:
            user.is_superuser = True
            user.is_staff = True
        user.is_active = is_active
        user.save()
        return user

    def create_customer_profile(self, user=None, is_active=False):
        if user is None:
            user = self.create_customer_user()
        profile = CustomerProfile.objects.get(user=user)
        profile.is_active = is_active
        profile.save()
        return profile


class CustomerUserModelTest(BaseCustomerModelTest):
    def test_user_creation(self):
        user = self.create_customer_user()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)

    def test_create_superuser(self):
        admin_user = self.create_customer_user(is_superuser=True,
                                               is_active=True)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_customer_user_str_method(self):
        user = self.create_customer_user()
        self.assertEqual(str(user), 'testuser')

    def test_user_email_validation(self):
        with self.assertRaises(ValidationError):
            self.create_customer_user(email='invalidemail',
                                      username='testuser',
                                      password='testpassword')


class CustomerProfileModelTest(BaseCustomerModelTest):
    def test_customer_profile_creation(self):
        user = self.create_customer_user()
        profile = self.create_customer_profile(user=user)
        self.assertEqual(profile.email, self.user_data['email'])
        self.assertEqual(profile.username, self.user_data['username'])
        self.assertEqual(profile.first_name, self.user_data['first_name'])
        self.assertEqual(profile.last_name, self.user_data['last_name'])
        self.assertFalse(profile.is_active)

    def test_user_upload_directory(self):
        user = self.create_customer_user()
        image = SimpleUploadedFile("avatar.jpg", b"file_content",
                                   content_type="image/jpeg")
        user.profile.avatar = image
        user.profile.save()
        self.assertIsNotNone(user.profile.avatar)

    def test_customer_profile_str_method(self):
        user = self.create_customer_user()
        profile = self.create_customer_profile(user=user)
        self.assertEqual(str(profile), 'Test User')
