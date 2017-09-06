class LogicException(Exception):
    def __init__(self, message=None, error_code=None, errors=None):
        super(LogicException, self).__init__(message)
        self.errors = errors
        self.error_code = error_code


class InvalidOperationException(LogicException):
    pass


class NotPermittedException(LogicException):
    pass
