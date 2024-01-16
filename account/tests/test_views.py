from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.registration_url = reverse('account:register')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

    def test_registration_view_get(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/registration/register.html')

    def test_registration_view_post(self):
        response = self.client.post(self.registration_url, data=self.user_data)
        self.assertEqual(response.status_code,
                         200)  # Check that the form is invalid due to email activation
        self.assertTemplateUsed(response,
                                'account/registration/register_email_confirm.html')

        # Check that the user is created and inactive
        self.assertTrue(get_user_model().objects.filter(username='testuser',
                                                        is_active=False).exists())


class DashboardViewTest(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_dashboard_view_authenticated(self):
        # Replace with your actual dashboard view URL
        url = reverse('account:dashboard')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_unauthenticated(self):
        # Replace with your actual dashboard view URL
        url = reverse('account:dashboard')

        response = self.client.get(url)
        # Assuming the view is protected by login_required decorator
        self.assertRedirects(response, f'/account/login/?next={url}')


class OrdersViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpass')

    def test_user_orders_authenticated(self):
        response = self.client.get(reverse('account:user-orders'))
        self.assertEqual(response.status_code, 302)


class WishlistViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpass')

    def test_wishlist_authenticated(self):
        response = self.client.get(reverse('account:wishlist'))
        self.assertEqual(response.status_code, 302)
