from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import DeliveryOptions 


class CheckoutViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@user.com',
            password='testpassword'
        )
        # Create delivery option for testing
        self.delivery_option = DeliveryOptions.objects.create(
            delivery_name='Test Delivery',
            delivery_price=10,
            is_active=True
        )

        self.client = Client()
        # Log in the user
        self.client.force_login(self.user)

    def test_checkout_view(self):
        response = self.client.get(reverse('checkout:checkout'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_view_post(self):
        self.client.force_login(self.user)
        address_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'email': 'john.doe@example.com',
            'postcode': '12345',
            'country': 'US',
            'street_address': '123 Main St',
            'town_city': 'City',
            'country_state': 'State',
            'delivery_instructions': 'Leave at the door'
        }

        response = self.client.post(reverse('checkout:checkout'),
                                    data=address_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_cart_update_delivery(self):
        response = self.client.post(reverse('checkout:cart-update-delivery'),
                                    {'action': 'POST',
                                     'delivery_option': self.delivery_option.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('delivery_price', data)

    def test_payment_selection_view(self):
        url = reverse('checkout:payment-selection')
        response = self.client.get(url)

        # Check if the view returns a successful response
        self.assertEqual(response.status_code, 302)
