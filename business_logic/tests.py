class shouldRaiseException(object):
    def __init__(self, error):
        self.error = error

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError(u"Exception has not been raised")
        if exc_val != self.error:
            raise AssertionError(u'Expected error code "{}", but received "{}"'.format(self.error, exc_val))
        return True


class BusinessLogicTestMixin(object):

    shouldRaiseException = shouldRaiseException
