from rest_framework import permissions


class IsUserAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAppAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated applications.
    """

    def has_permission(self, request, view):
        if request.auth is not None:
            application = request.auth.application
            user = request.user
            return not user.is_authenticated and application is not None
        return False
