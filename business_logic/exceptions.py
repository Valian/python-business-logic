class ServiceException(Exception):
    def __init__(self, message=None, error_code=None, errors=None):
        super(ServiceException, self).__init__(message)
        self.errors = errors
        self.error_code = error_code


class InvalidOperationException(ServiceException):
    pass


class NotPermittedException(ServiceException):
    pass
