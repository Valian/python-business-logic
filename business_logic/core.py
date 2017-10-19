import functools

import six

from business_logic.exceptions import LogicException


def validated_by(validation_func):
    """
    Decorator ensuring that 'validation_func' passes before actually calling decorated func.
    Check can be controlled using 'validate' named parameter  - True by default.
    `validation_func` should accept the same parameters as decorated function + 'raise_exception'.
    `validation_func` called with `raise_exception=True` must raise Exception to indicate
    that business rules forbids performing action.

    :param validation_func: function accepting same args as decorated function + 'raise_exception'
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # when not specified, checks are performed
            validate = kwargs.pop('validate', True)
            if validate:
                # we just pass exception and let it be handled by calling code
                validation_func(raise_exception=True, *args, **kwargs)
            # validation passed or skipped, we can run original func
            return f(*args, **kwargs)
        wrapper._validator = validation_func
        return wrapper
    return decorator


def validator(f):
    """
    Decorator changing underlying function to validator. Now it returns `PermissionResult`.
    Decorated function should raise exception or return False in case of
    validation failure. Automatically handles `raise_exception` parameter.
    :param f: Function to be decorated
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # consume `raise_exception` parameter, True if not defined
        raise_exception = kwargs.pop('raise_exception', True)
        try:
            # let's get original function result
            result = f(*args, **kwargs)
            # if exception is not raised, check return value.
            # if it's False, raise generic exception and handle it as usual
            if result is False:
                raise LogicException("Validation failed!")
            else:  # in other cases, return success
                return ValidationResult(True, error=None)
        except LogicException as e:
            # validation failed, if `raise_exception` is True, we re-raise exception
            if raise_exception:
                raise
            # otherwise, we create PermissionResult with error
            return ValidationResult(False, error=e)
    return wrapper


@six.python_2_unicode_compatible
class ValidationResult(object):
    """
    Class for storing result of validation function.
    If exception was passed, it provides some utility methods for getting useful data
    """

    def __init__(self, success, error=None):
        self.success = success
        self.error = error

    @property
    def errors(self):
        try:
            return self.error.errors
        except AttributeError:
            return None

    @property
    def error_code(self):
        try:
            return self.error.error_code
        except AttributeError:
            return None

    def __nonzero__(self):
        return self.success
    __bool__ = __nonzero__

    def __eq__(self, other):
        if isinstance(other, (bool, ValidationResult)):
            return bool(self) == bool(other)
        return False

    def __repr__(self):
        return u'<PermissionResult success={} error={}>'.format(self.success, self.error)

    def __str__(self):
        return six.text_type(self.error) if self.error else u''
