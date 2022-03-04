from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdminRole(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.is_admin)


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AuthorAdminModerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_admin:
            return True
        if request.user.is_moderator:
            return True
        if obj.author == request.user:
            return True
