from django.test import TestCase
from django.db.models.signals import post_save
from ..models import CustomerUser, CustomerProfile
from ..signals import create_or_update_user_profile, update_customer_user
from django.test import override_settings


class SignalsTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

    @override_settings(DEBUG=True)  # To ensure signals are connected in testing
    def test_create_or_update_user_profile_signal(self):
        # Connect the signal to the post_save signal
        post_save.connect(create_or_update_user_profile, sender=CustomerUser)

        # Create a new user triggering the signal
        user = CustomerUser.objects.create_user(**self.user_data)

        # Retrieve the associated profile
        profile = user.profile

        # Assert that the profile is created or updated correctly
        self.assertEqual(profile.email, self.user_data['email'])
        self.assertEqual(profile.username, self.user_data['username'])
        self.assertEqual(profile.first_name, self.user_data['first_name'])
        self.assertEqual(profile.last_name, self.user_data['last_name'])
        self.assertFalse(profile.is_active)

    @override_settings(DEBUG=True)
    def test_update_customer_user_signal(self):
        # Connect the signal to the post_save signal
        post_save.connect(update_customer_user, sender=CustomerProfile)

        # Create a new user and profile
        user = CustomerUser.objects.create_user(**self.user_data)
        profile = user.profile

        # Update the profile triggering the signal
        updated_data = {
            'email': 'updated@example.com',
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'phone': '1234567890',
            'is_active': True,
        }
        for key, value in updated_data.items():
            setattr(profile, key, value)

        # Save the profile to trigger the signal
        profile.save()

        # Retrieve the updated user
        updated_user = CustomerUser.objects.get(pk=user.pk)

        # Assert that the user is updated correctly
        self.assertEqual(updated_user.email, updated_data['email'])
        self.assertEqual(updated_user.username, updated_data['username'])
        self.assertEqual(updated_user.first_name, updated_data['first_name'])
        self.assertEqual(updated_user.last_name, updated_data['last_name'])
        self.assertEqual(updated_user.phone, updated_data['phone'])
        self.assertTrue(updated_user.is_active)

        # Disconnect the signals to avoid interference with other tests
        post_save.disconnect(update_customer_user, sender=CustomerProfile)
