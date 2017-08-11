from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    User can only view oneself.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
