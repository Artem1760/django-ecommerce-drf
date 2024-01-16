from django.urls import reverse
from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin():
    """Mixin for combining admin user and staff editor permissions."""
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


class UserQuerySetMixin():
    """Mixin for custom access to the queryset based on the user."""
    user_field = 'user'
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        # Display full available data for the admin user
        if user.is_superuser:
            return qs
        # Display empty qs for the all users except admin 
        if self.allow_staff_view and user.is_staff:
            return qs
        # Display filtered to the specific staff user qs
        return qs.filter(**lookup_data)


class RelatedURLsMixin:
    """
    Mixin for generating related URLs based on predefined mappings.
    """
    RELATED_FIELDS = {
        'publisher': 'api:publisher-list-create',
        'author': 'api:author-list-create',
        'book_type': 'api:type-list-create',
        'languages': 'api:language-list-create',
        'category': 'api:category-list-create',
    }

    def get_related_url(self, obj, field_name):
        """
        Get the related URL for a specific field based on the predefined mappings.

        Args:
            obj: The instance of the object.
            field_name: The name of the related field.

        Returns:
            str: The related URL or None if not found.
        """
        request = self.context.get('request')
        if request is None:
            return None

        view_name = self.RELATED_FIELDS.get(field_name)
        if view_name:
            return request.build_absolute_uri(reverse(view_name))
        return None

    def get_publisher_url(self, obj):
        return self.get_related_url(obj, 'publisher')

    def get_author_url(self, obj):
        return self.get_related_url(obj, 'author')

    def get_book_type_url(self, obj):
        return self.get_related_url(obj, 'book_type')

    def get_languages_url(self, obj):
        return self.get_related_url(obj, 'languages')

    def get_category_url(self, obj):
        return self.get_related_url(obj, 'category')
