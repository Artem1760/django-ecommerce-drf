from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


class CoreViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         email='test@user.com',
                                                         password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_view(self):
        response = self.client.get(reverse('core:about-us'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_get(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_contact_view_post_valid_form(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]),
                         'Your message has been sent successfully!')
        self.assertEqual(str(messages[1]), 'Please correct the errors below.')

    def test_contact_view_post_invalid_form(self):
        response = self.client.post(reverse('core:contact'), {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name',
                             'This field is required.')

    def test_contact_view_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_error_404_view(self):
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')
