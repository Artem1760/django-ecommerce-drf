from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

CustomerUser = settings.AUTH_USER_MODEL


class ContactInformation(models.Model):
    """Store's Contact data"""
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return 'Store Contact'


class WorkDays(models.Model):
    """Store working schedule: days and hours"""
    contact_information = models.ForeignKey(ContactInformation,
                                            on_delete=models.CASCADE,
                                            related_name='workdays')
    workday = models.CharField(max_length=155)
    work_hour = models.CharField(max_length=155)

    def __str__(self):
        return self.workday


class ContactUs(models.Model):
    """Data for collecting queries from customers"""
    id = ShortUUIDField(primary_key=True, unique=True, length=10,
                        editable=False, alphabet='1234567890')
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, null=True,
                             blank=True)
    name = models.CharField(max_length=160)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=14, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    created_date = models.DateField(default=timezone.now, editable=False,
                                    verbose_name='Date')

    class Meta:
        verbose_name = _("User's message")
        verbose_name_plural = _("User's messages")

    def __str__(self):
        return f'{self.name} - Message'
