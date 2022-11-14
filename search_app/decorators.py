from django.core.exceptions import PermissionDenied


def admin_user_required(function):
    """
    Decorator function for admin access
    """
    def wrap(request, *args, **kwargs):
        if request.user.admin:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
