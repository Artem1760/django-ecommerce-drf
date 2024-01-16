from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import ContactUsForm


class ContactUsFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                                                username='testuser',
                                                email='testuser@example.com',
                                                password='password'
                                                )

    def test_contact_us_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'subject': 'Inquiry',
            'message': 'Hello, I have a question.',
        }
        form = ContactUsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_us_form_invalid_missing_fields(self):
        form_data = {}
        form = ContactUsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['name'])
        self.assertIn('This field is required.', form.errors['email'])
        self.assertIn('This field is required.', form.errors['message'])

    def test_contact_us_form_with_user(self):
        form_data = {
            'user': self.user.id,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'subject': 'Inquiry',
            'message': 'Hello, I have a question.',
        }
        form = ContactUsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_us_form_invalid_email(self):
        form_data = {
            'name': 'John Doe',
            'email': 'invalidemail',  # Invalid email address
            'phone': '1234567890',
            'subject': 'Inquiry',
            'message': 'Hello, I have a question.',
        }
        form = ContactUsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])
