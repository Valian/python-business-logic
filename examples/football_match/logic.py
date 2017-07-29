from business_logic import validator, validated_by


@validator
def can_shoot_goal(person, match):
    pass


@validator
def can_start_match(person, match):
    pass


@validator
def can_finish_match(person, match):
    pass


@validated_by(can_shoot_goal)
def shoot_goal(person, match):
    pass


@validated_by(can_start_match)
def start_match(person, match):
    pass


@validated_by(can_finish_match)
def finish_match(person, match):
    pass

