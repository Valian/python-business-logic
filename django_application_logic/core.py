import functools

from django_application_logic.exceptions import ServiceException


class PermissionResult(object):

    def __init__(self, success, error=None):
        self.success = success
        self.error = error

    @property
    def errors(self):
        return self.error.errors if self.error else None

    @property
    def error_code(self):
        return self.error.error_code if self.error else None

    def __nonzero__(self):
        return self.success
    __bool__ = __nonzero__

    def __eq__(self, other):
        if isinstance(other, (bool, PermissionResult)):
            return bool(self) == bool(other)
        return False

    def __repr__(self):
        return u'<PermissionResult success={} error={}>'.format(self.success, self.error)


def validated_by(validation_func):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            validate = kwargs.pop('validate', True)
            if validate:
                validation_func(raise_exception=True, *args, **kwargs)
            return f(*args, **kwargs)
        wrapper._validator = validation_func
        return wrapper
    return decorator


def validator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        raise_exception = kwargs.pop('raise_exception', True)
        try:
            result = f(*args, **kwargs)
            return PermissionResult(True if result is None else bool(result), None)
        except ServiceException as e:
            if raise_exception:
                raise
            return PermissionResult(False, e)
    return wrapper
