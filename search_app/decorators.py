from django.core.exceptions import PermissionDenied


#decorator function for admin access only
def admin_user_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.admin:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
