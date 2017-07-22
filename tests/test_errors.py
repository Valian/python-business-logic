import mock
from django.test import TestCase

from application_logic import errors, exceptions


class TestErrors(errors.ServicesErrors):
    INVALID_ACTION = exceptions.InvalidOperationException(
        "This action is permitted by business logic")
    NO_PERMISSION = exceptions.NotPermittedException(
        "This action is permitted because not sufficient permissions")
    generic_error = exceptions.ServiceException(
        "This action is permitted just because :)")


class TestErrorsAPI(TestCase):

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
