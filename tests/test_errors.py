
from unittest import TestCase

from business_logic import errors, exceptions
from business_logic.tests import BusinessLogicTestMixin


class TestErrors(errors.LogicErrors):
    INVALID_ACTION = exceptions.InvalidOperationException(
        "This action is permitted by business logic")
    NO_PERMISSION = exceptions.NotPermittedException(
        "This action is permitted because not sufficient permissions")
    generic_error = exceptions.LogicException(
        "This action is permitted just because :)")


class TestLogicException(TestCase):

    def test_exception_repr_is_working_correctly(self):
        exc = exceptions.LogicException('Test', error_code='TEST')
        self.assertEqual(repr(exc), "LogicException('Test', error_code='TEST')")

    def test_exception_is_hashable(self):
        exc = exceptions.LogicException('Test')
        self.assertIsInstance(hash(exc), int)

    def test_exceptions_with_same_error_codes_are_equal(self):
        exc1 = exceptions.LogicException('Test', error_code='TEST')
        exc2 = exceptions.LogicException('Test', error_code='TEST')
        self.assertEqual(exc1, exc2)

    def test_exceptions_without_error_codes_are_equal_only_if_messages_are_equal(self):
        exc1 = exceptions.LogicException('Test')
        exc2 = exceptions.LogicException('Test')
        exc3 = exceptions.LogicException('Not Test')
        self.assertEqual(exc1, exc2)
        self.assertNotEqual(exc1, exc3)


class TestErrorsAPI(BusinessLogicTestMixin, TestCase):

    def test_service_errors_magically_receives_error_codes(self):
        self.assertEqual(TestErrors.generic_error.error_code, 'generic_error')
        self.assertEqual(TestErrors.NO_PERMISSION.error_code, 'NO_PERMISSION')
        self.assertEqual(TestErrors.INVALID_ACTION.error_code, 'INVALID_ACTION')

    def test_each_errors_receives_other_errors_in_registry(self):
        self.assertEqual(TestErrors._errors, TestErrors.generic_error.errors)
        self.assertEqual(TestErrors._errors, TestErrors.NO_PERMISSION.errors)
        self.assertEqual(TestErrors._errors, TestErrors.INVALID_ACTION.errors)

    def test_registry_contains_all_errors(self):
        self.assertEqual(
            TestErrors._errors,
            {
                'NO_PERMISSION': TestErrors.NO_PERMISSION,
                'INVALID_ACTION': TestErrors.INVALID_ACTION,
                'generic_error': TestErrors.generic_error,
            }
        )

    def test_raising_exception_works_as_intended(self):
        with self.shouldRaiseException(TestErrors.INVALID_ACTION):
            raise TestErrors.INVALID_ACTION

    def test_formatting_returns_copy_with_formatted_message(self):
        parametrizable = exceptions.LogicException(
            message='{user} has been {behaviour}!',
            error_code='BEHAVIOUR',
            errors={'BEHAVIOUR': 'test'})
        formatted = parametrizable.format(
            user='Marian', behaviour='naughty')
        self.assertEqual(str(formatted), 'Marian has been naughty!')
        self.assertIs(type(parametrizable), type(formatted))
        self.assertEqual(parametrizable.errors, formatted.errors)
        self.assertEqual(parametrizable.error_code, formatted.error_code)
        self.assertEqual(parametrizable, formatted)
        self.assertIsNot(parametrizable, formatted)

    def test_formatting_message_with_invalid_parameters_raises_error(self):
        exc = exceptions.LogicException('Test {person}?')
        with self.assertRaises(KeyError):
            exc.format(pearson='me')
