"""custom permission classes"""

from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    checks if all the following fields are True of the current user:
      is_staff
      is_superuser
      is_active
    because superusers should be able to directly make DELETE request
    """

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        pass


class IsOwner(BasePermission):
    """checks if the API key is owned by the current user"""

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        pass
