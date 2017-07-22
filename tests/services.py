from application_logic.core import validator, validated_by


@validator
def can_remove_user(by_user, user):
    return True


@validated_by(can_remove_user)
def remove_user(by_user, user):
    user.delete()
