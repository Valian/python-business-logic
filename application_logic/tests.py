from application_logic.exceptions import ServiceException


class shouldRaiseErrorCode(object):
    def __init__(self, error):
        self.error = error

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError(u"Exception has not been raised")
        if not issubclass(exc_type, ServiceException):
            raise AssertionError(u"Raised {} exception type where {} was expected.\nMore info:\n{}".format(
                exc_type, ServiceException, self.get_traceback(exc_tb)))
        if exc_val != self.error:
            raise AssertionError(u'Expected error code "{}", but received "{}"'.format(self.error, exc_val))
        return True

    def get_traceback(self, exc_tb):
        try:
            return exc_tb.format_exc()
        except AttributeError:
            # python3 fix
            import traceback
            traceback.format_exc()


class ApplicationLogicTestMixin(object):

    shouldRaiseErrorCode = shouldRaiseErrorCode
