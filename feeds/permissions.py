from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import ParseError


class IsWriterorReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.writer or request.user.is_superuser:
                return True
            return False
        else:
            return False


class OnlyoneReview(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            print(obj.reviews.filter(writer=request.user))
            if obj.reviews.filter(writer=request.user).exists():
                raise ParseError("이미 리뷰를 작성하셨습니다.")
            elif request.user == obj.writer or request.user.is_superuser:
                return True
            else:
                return True
