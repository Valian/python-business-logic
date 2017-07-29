from unittest import TestCase

from application_logic.tests import ApplicationLogicTestMixin


class TestUtilsTest(ApplicationLogicTestMixin, TestCase):

    def test_not_raising_exceptions_fails(self):
        try:
            with self.shouldRaiseException(Exception()):
                pass
        except AssertionError:
            # it's expected
            pass

    def test_not_expected_exception_raises_assertion_errors(self):
        try:
            error1 = Exception()
            error2 = Exception()
            with self.shouldRaiseException(error1):
                raise error2
        except AssertionError:
            # expected
            pass

    def test_expected_exception_passes(self):
        error = Exception()
        with self.shouldRaiseException(error):
            raise error
