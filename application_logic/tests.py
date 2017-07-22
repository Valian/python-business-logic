from application_logic.exceptions import InvalidOperationException, OperationNotPermittedException


class shouldRaiseErrorCode(object):
    def __init__(self, error):
        self.error = error

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError(u"Exception has not been raised")
        desired_exceptions = (InvalidOperationException, OperationNotPermittedException)
        if exc_type not in desired_exceptions:
            raise AssertionError(u"Raised {} exception type where {} was expected.\nMore info:\n{}".format(
                exc_type, desired_exceptions, exc_tb.format_exc()))
        if exc_val != self.error:
            raise AssertionError(u'Expected error code "{}", but received "{}"'.format(self.error, exc_val))
        return True


class ApplicationLogicTestMixin(object):

    shouldRaiseErrorCode = shouldRaiseErrorCode
