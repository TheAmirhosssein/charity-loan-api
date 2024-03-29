from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_admin_user:
                return True
            else:
                return False
        return False


class IsAdminOrAuthorNested(permissions.BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        if request.user.is_admin_user:
            return True

        user = getattr(view.get_parent_object(), view.user_field)
        return user == request.user
