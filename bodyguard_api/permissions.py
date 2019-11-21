from rest_framework import permissions
from .models import Role

RETRIEVE_METHOD = "retrieve"
DELETE_METHOD = "destroy"
UPDATE_METHOD = "update"
PATCH_METHOD = "partial_update"
CREATE_METHOD = "create"
LIST_METHOD = "list"


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.customer == request.user


class HasPermissionForUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj or user.is_superuser or view.action == RETRIEVE_METHOD:
            return True
        else:
            return False


class HasPermissionForJob(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action == LIST_METHOD or user.profile.role.id == Role.CUSTOMER or user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action in [UPDATE_METHOD, PATCH_METHOD] and obj.orders.exists() == True:
            return False
        elif user.is_superuser or user == obj.customer or view.action == RETRIEVE_METHOD:
            return True
        else:
            return False


class HasPermissionForGuardFirm(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action == LIST_METHOD or user.profile.role.id == Role.FIRM or user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user == obj.owner or view.action == RETRIEVE_METHOD:
            return True
        else:
            return False


class HasPermissionForOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action == LIST_METHOD or user.profile.role.id == Role.FIRM or user.is_superuser\
                or (user.profile.role.id == Role.CUSTOMER and view.action != CREATE_METHOD):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user == obj.firm.owner or view.action == RETRIEVE_METHOD \
                or (user == obj.job.customer and view.action in [UPDATE_METHOD, PATCH_METHOD]):
            if user == obj.firm.owner and view.action in [UPDATE_METHOD, PATCH_METHOD, DELETE_METHOD] \
                    and obj.approved == True:
                return False
            return True
        else:
            return False


class HasPermissionForFirmFeedback(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if view.action == LIST_METHOD or user.profile.role.id == Role.CUSTOMER or user.is_superuser:
            return True
        else:
            return False