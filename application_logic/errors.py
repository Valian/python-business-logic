from application_logic import exceptions
from six import with_metaclass


class ServicesErrorsMetaclass(type):
    """
    Metaclass automatically creating errors registry and setting error code to attribute name.
    You should subclass this and set all possible application logic exceptions.
    """
    def __init__(cls, name, bases, dict):
        super(ServicesErrorsMetaclass, cls).__init__(name, bases, dict)
        # dictionary containing all errors by error code
        cls._errors = {}
        for attr_name, attr in dict.items():
            if isinstance(attr, exceptions.ServiceException):
                # attribute name becomes exception `error_code`
                attr.error_code = attr_name
                attr.errors = cls._errors
                cls._errors[attr_name] = attr


class ServicesErrors(with_metaclass(ServicesErrorsMetaclass)):
    pass
