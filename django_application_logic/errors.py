from django_application_logic import exceptions
from six import with_metaclass

errors_registry = type('Errors', (), {})  # we setattr here all found errors


class ErrorBase(object):
    exception_class = None

    def __init__(self, message):
        self.message = message


class NotPermitted(ErrorBase):
    exception_class = exceptions.OperationNotPermittedException


class InvalidOperation(ErrorBase):
    exception_class = exceptions.InvalidOperationException


class ServicesErrorsMetaclass(type):
    def __init__(cls, name, bases, dict):
        super(ServicesErrorsMetaclass, cls).__init__(name, bases, dict)
        for attr_name, attr in dict.items():
            if isinstance(attr, ErrorBase):
                exception = attr.exception_class(attr.message, attr_name.lower(), cls)
                setattr(errors_registry, attr_name, exception)
                setattr(cls, attr_name, exception)


class ServicesErrors(with_metaclass(ServicesErrorsMetaclass)):
    pass
