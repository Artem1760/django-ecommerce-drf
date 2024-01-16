from django.test import TestCase
from django.contrib.auth import get_user_model

from ..forms import AddressForm
from checkout.models import DeliveryOptions


class AddressFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                                                username='testuser',
                                                email='testuser@example.com',
                                                password='password')
        self.delivery_option = DeliveryOptions.objects.create(
            delivery_name='Express',
            delivery_price=10,
            is_active=True
        )

    def test_address_form_save(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'email': 'john.doe@example.com',
            'postcode': '12345',
            'country': 'US',
            'street_address': '123 Main St',
            'town_city': 'Anytown',
            'country_state': 'CA',
            'delivery_instructions': 'Leave at the doorstep.',
        }

        form = AddressForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Save the form to create an Address instance
        address = form.save(commit=False)
        address.user = self.user
        address.delivery_option = self.delivery_option
        address.save()

        # Check whether the Address instance is saved correctly
        self.assertEqual(address.first_name, 'John')
        self.assertEqual(address.last_name, 'Doe')
        self.assertEqual(address.phone, '1234567890')
        self.assertEqual(address.email, 'john.doe@example.com')
        self.assertEqual(address.postcode, '12345')
        self.assertEqual(address.country, 'US')
        self.assertEqual(address.street_address, '123 Main St')
        self.assertEqual(address.town_city, 'Anytown')
        self.assertEqual(address.country_state, 'CA')
        self.assertEqual(address.delivery_instructions,
                         'Leave at the doorstep.')
