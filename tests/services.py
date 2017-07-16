from django_application_logic.core import validation_func, validator


@validation_func
def can_remove_user(by_user, user):
    return True


@validator(can_remove_user)
def remove_user(by_user, user):
    user.delete()
