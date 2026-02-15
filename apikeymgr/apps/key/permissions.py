"""custom permission classes"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrSuperUserForDelete(BasePermission):
    """
    1. checks if all the following fields are True of the current user:
      is_staff
      is_superuser
    because superusers should be able to directly make DELETE request

    2. checks if the API key is owned by the current user
    even if a user is signed in, they must have no access to any API key
      they do not own
    """

    def has_permission(self, request, view):
        """only signed in user can make http requests"""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            # only superuser/staff can DELETE
            return request.user.is_superuser and request.user.is_staff

        if request.method in SAFE_METHODS:
            # only the owner can read/get
            return request.user == obj.user

        if request.method in ["PUT", "PATCH"]:
            # only the owner can update
            return request.user == obj.user

        return False
