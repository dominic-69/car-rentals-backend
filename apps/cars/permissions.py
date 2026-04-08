from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "seller"