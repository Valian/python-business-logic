from business_logic import exceptions
from six import with_metaclass


class _LogicErrorsMetaclass(type):
    """
    Metaclass automatically creating errors registry and setting error code to attribute name.
    You should subclass this and set all possible business logic exceptions.
    """
    def __init__(cls, name, bases, dict):
        super(_LogicErrorsMetaclass, cls).__init__(name, bases, dict)
        # dictionary containing all errors by error code
        cls._errors = {}
        for attr_name, attr in dict.items():
            if isinstance(attr, exceptions.LogicException):
                # attribute name becomes exception `error_code`
                attr.error_code = attr_name
                attr.errors = cls._errors
                cls._errors[attr_name] = attr


class LogicErrors(with_metaclass(_LogicErrorsMetaclass)):
    pass
