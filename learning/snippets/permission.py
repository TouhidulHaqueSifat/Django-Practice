from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated

class Danger(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        raise NotAuthenticated(detail="Authentication is required to access this resource.")
        