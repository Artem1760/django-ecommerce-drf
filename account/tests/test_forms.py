from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import RegistrationForm, UserEditForm, UserAddressForm
from ..models import CustomerUser


class RegistrationFormTest(TestCase):
    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_username(self):
        # Test with an existing username
        existing_user = CustomerUser.objects.create_user(
            username='existinguser', email='existing@example.com',
            password='testpassword')
        form_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Username already exists', form.errors['username'])

    def test_registration_form_invalid_email(self):
        # Test with an existing email
        existing_user = CustomerUser.objects.create_user(
            username='newuser', email='existing@example.com',
            password='testpassword')
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please use another Email, that is already taken',
                      form.errors['email'])

    def test_registration_form_invalid_password_mismatch(self):
        # Test with mismatched passwords
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'mismatchedpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match.', form.errors['password2'])


class UserEditFormTest(TestCase):
    def setUp(self):
        self.user = CustomerUser.objects.create_user(
            username='testuser', email='testuser@example.com',
            password='testpassword')

    def test_user_edit_form_valid(self):
        form_data = {
            'email': 'newemail@example.com',
            'username': 'testuser',
            'first_name': 'New',
            'last_name': 'Name',
            'phone': '1234567890',
            'avatar': SimpleUploadedFile("avatar.jpg", b"file_content",
                                         content_type="image/jpeg"),
        }
        form = UserEditForm(data=form_data, instance=self.user.profile)
        self.assertTrue(form.is_valid())

    def test_user_edit_form_invalid(self):
        # Test with invalid email and required fields missing
        form_data = {
            'email': 'invalidemail',
            'username': 'testuser',
            'first_name': 'New',
            'last_name': 'Name',
        }
        form = UserEditForm(data=form_data, instance=self.user.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])
        self.assertIn('This field is required.', form.errors['phone'])


class UserAddressFormTest(TestCase):
    def test_user_address_form_valid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'country': 'US',
            'country_state': 'CA',
            'postcode': '12345',
            'street_address': '123 Main St',
            'town_city': 'Anytown',
            'phone': '1234567890',
            'default': True,
        }
        form = UserAddressForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_address_form_invalid(self):
        # Test with required field missing: email
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'country': 'US',
            'country_state': 'CA',
            'postcode': '12345',
            'street_address': '123 Main St',
            'town_city': 'Anytown',
            'phone': '1234567890',
            'default': True,
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid())
