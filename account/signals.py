from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile, CustomerUser


@receiver(post_save, sender=CustomerUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update CustomerProfile when CustomerUser
    is created or updated.
    """
    if created:
        # If a new CustomerUser is created, create a new CustomerProfile instance
        CustomerProfile.objects.get_or_create(
            user=instance,
            email=instance.email,
            username=instance.username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            phone=instance.phone,
            is_active=instance.is_active
        )
    else:
        # Check if the related CustomerProfile exists before updating
        if hasattr(instance, 'profile'):
            profile = instance.profile
            changed_fields = []
            if profile.email != instance.email:
                profile.email = instance.email
                changed_fields.append('email')
            if profile.username != instance.username:
                profile.username = instance.username
                changed_fields.append('username')
            if profile.first_name != instance.first_name:
                profile.first_name = instance.first_name
                changed_fields.append('first_name')
            if profile.last_name != instance.last_name:
                profile.last_name = instance.last_name
                changed_fields.append('last_name')
            if profile.phone != instance.phone:
                profile.phone = instance.phone
                changed_fields.append('phone')
            if profile.is_active != instance.is_active:
                profile.is_active = instance.is_active
                changed_fields.append('is_active')

            if changed_fields:
                profile.save(update_fields=changed_fields)


@receiver(post_save, sender=CustomerProfile)
def update_customer_user(sender, instance, **kwargs):
    """
    Signal to update the related CustomerUser when a CustomerProfile is updated.
    """
    user = instance.user
    changed_fields = []
    if user.email != instance.email:
        user.email = instance.email
        changed_fields.append('email')
    if user.username != instance.username:
        user.username = instance.username
        changed_fields.append('username')
    if user.first_name != instance.first_name:
        user.first_name = instance.first_name
        changed_fields.append('first_name')
    if user.last_name != instance.last_name:
        user.last_name = instance.last_name
        changed_fields.append('last_name')
    if user.phone != instance.phone:
        user.phone = instance.phone
        changed_fields.append('phone')
    if user.is_active != instance.is_active:
        user.is_active = instance.is_active
        changed_fields.append('is_active')

    if changed_fields:
        user.save(update_fields=changed_fields)
