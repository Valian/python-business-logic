from business_logic import validator, validated_by

from errors import MatchErrors


@validator
def can_shoot_goal(person, match):
    pass


@validator
def can_start_match(person, match):
    if not person.is_referee:
        raise MatchErrors.CANT_START_NOT_REFEREE
    if match.status != match.BEFORE_START:
        raise MatchErrors.CANT_START_ALREADY_STARTED
    if len(match.first_team.players) != len(match.second_team.players):
        raise MatchErrors.CANT_START_NOT_EVEN_TEAMS


@validator
def can_finish_match(person, match):
    pass


@validated_by(can_shoot_goal)
def shoot_goal(person, match):
    pass


@validated_by(can_start_match)
def start_match(person, match):
    # side effect, like sending emails, logging etc should live here
    print(u"{} started match!".format(person.name))
    match.status = match.STARTED


@validated_by(can_finish_match)
def finish_match(person, match):
    pass

