from rest_framework import permissions


class IsBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsBoardGuestReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == user or user in obj.users.all()

        return False


class IsSectionUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.board.owner == user or user in obj.board.users.all()


class IsCardUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.section.board.owner == user or user in obj.section.board.users.all()
