import re
from copy import copy


class LogicException(Exception):

    PARAMETERS_REGEX = re.compile(r'{\w+}')

    def __init__(self, message=None, error_code=None, errors=None):
        super(LogicException, self).__init__(message)
        self.errors = errors
        self.error_code = error_code

    @property
    def required_params(self):
        return set(self.PARAMETERS_REGEX.findall(str(self)))

    def format(self, **params):
        """Use to create exception with formatted message."""
        message = str(self).format(**params)
        formatted_exception = copy(self)
        formatted_exception.args = (message,) + self.args[1:]
        return formatted_exception

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.error_code is not None:
                return self.error_code == other.error_code
            else:
                return str(self) == str(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        cls_name = self.__class__.__name__
        exc_args = ', '.join(repr(a) for a in self.args)
        code = repr(self.error_code)
        return u'{}({}, error_code={})'.format(cls_name, exc_args, code)


class InvalidOperationException(LogicException):
    pass


class NotPermittedException(LogicException):
    pass
