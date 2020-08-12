from rest_framework import permissions


class IsBoardOwnerOrBoardUserReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it and board's users to retrieve one.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == user or user in obj.users.all()

        return obj.owner == user


class IsSectionUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.board.owner == user or user in obj.board.users.all()


class IsCardUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.section.board.owner == user or user in obj.section.board.users.all()
