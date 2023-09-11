from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsWriterorReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.writer:
                return True
            return False
        else:
            return False
