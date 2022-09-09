from functools import wraps
from flask import g, abort, current_app


def is_admin(api_method):
    @wraps(api_method)
    def check_is_admin(*args, **kwargs):
        if g.user and (g.user.is_admin() or g.user.is_superadmin()):
            return api_method(*args, **kwargs)
        else:
            current_app.logger.info('User is not admin')
            abort(401)

    return check_is_admin


def is_super_admin(api_method):
    @wraps(api_method)
    def check_is_super_admin(*args, **kwargs):
        if g.user and g.user.is_superadmin():
            return api_method(*args, **kwargs)
        else:
            abort(401)

    return check_is_super_admin
