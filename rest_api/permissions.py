from rest_framework import permissions


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    """
    It allows staff users to view and edit data of other staff users 
    and simple users, but not to delete and update superusers nor update 
    delete staff users.        
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # Superusers have all permissions
        if request.user.is_superuser:
            return True

        # Staff users can view and edit data of other staff users and simple users
        if request.user.is_staff:
            return request.method in permissions.SAFE_METHODS or request.method in [
                'PUT', 'POST', 'PATCH']

        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action
        on a specific object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # Superusers can perform any action
        if request.user.is_superuser:
            return True

        # Staff users can view and edit data of staff users and simple users,
        # but not delete superusers
        if request.user.is_staff and not obj.is_superuser:
            return request.method in permissions.SAFE_METHODS or request.method in [
                'PUT', 'POST', 'PATCH']

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    This custom permission class allows admins to perform any action 
    and non-admins to perform safe methods (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action.

        Args:
            request (Request): The incoming HTTP request.
            view: The view requesting the permission.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)
