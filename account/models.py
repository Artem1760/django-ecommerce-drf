from django.core.mail import send_mail
import os
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def user_upload_directory(instance, filename):
    """Generates the file path for user avatars based on user profile ID."""
    return os.path.join('user_avatar', str(instance.user.profile.id), filename)


class CustomerUserManager(BaseUserManager):
    """
    Custom manager for the User model with additional functionality.
    """

    def validateEmail(self, email):
        validate_email(email)

    def create_superuser(self, email, username, password, **other_fields):
        """
        Creates and returns a superuser with the given email,
        username, and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get('is_staff') or not other_fields.get(
                'is_superuser'):
            raise ValueError(
                'Superuser must be assigned to is_staff=True '
                'and is_superuser=True')

        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError(
                _('Superuser Account: You must provide an email address'))

        return self.create_user(email, password, username, **other_fields)

    def create_user(self, email, password, username, **other_fields):
        """
        Creates and returns a regular user with the given email,
        username, and password.
        """
        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError(
                _('Customer Account: You must provide an email address'))

        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    id = ShortUUIDField(primary_key=True, unique=True, length=10,
                        editable=False, alphabet='1234567890')
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def __str__(self):
        return self.username

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'molla@bk.com',
            [self.email],
            fail_silently=False,
        )


class CustomerProfile(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, length=10,
                        editable=False, alphabet='1234567890')
    user = models.OneToOneField('CustomerUser', on_delete=models.CASCADE,
                                related_name='profile')
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_upload_directory,
                               default='default_avatar.png')

    class Meta:
        verbose_name = _('Customer profile')
        verbose_name_plural = _('Customer profiles')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def image_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
