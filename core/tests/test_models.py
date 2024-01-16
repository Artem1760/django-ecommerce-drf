from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models import ContactInformation, WorkDays, ContactUs


class ModelTestsMixin:
    def create_contact_information(self):
        return ContactInformation.objects.create(
            email='test@store.com',
            phone='1234567890',
            address='123 Main St',
        )

    def create_work_day(self, contact_information, workday='Monday',
                        work_hour='9:00 AM - 5:00 PM'):
        return WorkDays.objects.create(
            contact_information=contact_information,
            workday=workday,
            work_hour=work_hour,
        )

    def create_contact_us(self, user=None):
        return ContactUs.objects.create(
            user=user,
            name='John Doe',
            email='john.doe@example.com',
            phone='1234567890',
            subject='Inquiry',
            message='Hello, I have a question.',
            created_date=timezone.now(),
        )


class ContactInformationModelTest(ModelTestsMixin, TestCase):
    def test_contact_information_str(self):
        contact_info = self.create_contact_information()
        self.assertEqual(str(contact_info), 'Store Contact')


class WorkDaysModelTest(ModelTestsMixin, TestCase):
    def test_work_days_str(self):
        contact_info = self.create_contact_information()
        work_day = self.create_work_day(contact_info)
        self.assertEqual(str(work_day), 'Monday')


class ContactUsModelTest(ModelTestsMixin, TestCase):
    def test_contact_us_str(self):
        contact_us = self.create_contact_us()
        self.assertEqual(str(contact_us), 'John Doe - Message')

    def test_contact_us_with_user(self):
        user = get_user_model().objects.create_user(username='testuser',
                                                    email='testuser@example.com',
                                                    password='password')
        contact_us = self.create_contact_us(user=user)
        self.assertEqual(contact_us.user, user)
