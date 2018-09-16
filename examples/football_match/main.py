import random

from business_logic import LogicException
from examples.football_match import logic, factories, models


def main():
    """
    This example shows how easily business logic can be used.
    To understand this sample properly, check `logic.py`, `errors.py` and `tests.py`
    """
    # lets create out models, two teams 2 players each, and match with 500$ as reward
    first_team = factories.TeamFactory(players__count=2)
    second_team = factories.TeamFactory(players__count=2)
    match = factories.MatchFactory(
        first_team=first_team, second_team=second_team,
        status=models.Match.BEFORE_START, reward=500)

    print(u"Welcome to the football match between '{}' and '{}'!".format(
        first_team.name, second_team.name))
    print(u'\n--------\n')

    # normal person, not player, who is really enthusiastic about match
    observer = factories.PersonFactory()
    referee = factories.RefereeFactory()
    start_match(match, observer, referee)

    print(u'\n--------\n')

    # we add observer to shooters, he want to shoot goals, but our logic won't allow him to do so
    potential_shooters = first_team.players + second_team.players + [observer]
    simulate_match(match, potential_shooters)
    print(u'\n--------\n')

    # only referee can finish match, it's validated by default
    # logic.finish_match(observer, match) will raise exception
    logic.finish_match(referee, match)
    print(u'\nMatch finished!')
    if match.winner:
        print(u'Winner: "{}"!'.format(match.winner.name))
    else:
        print(u'Draw, no winner!')

    # our logic disallows finishing match second time, but let's check that
    print(u"\nCan't finish match, reason: {}".format(
        logic.can_finish_match(referee, match, raise_exception=False))
    )


def start_match(match, observer, referee):
    # here is example how you can check certain validator without raising exception
    observer_can_start_match = logic.can_start_match(observer, match, raise_exception=False)

    # observer_can_start_match is a `ValidationResult` object.
    # It contains information about success and error.

    # Due to logic, I know that observer_can_start_match will be false, but let's check
    if not observer_can_start_match:
        print(u"{} can't start match, reason: {}".format(observer, str(observer_can_start_match)))

    # This will pass without exception, it's valid case
    logic.start_match(referee, match, validate=True)


def simulate_match(match, potential_shooters):
    # time for some randomness
    number_of_goals = random.randint(5, 10)
    while number_of_goals > 0:
        # we select one of players
        selected = random.choice(potential_shooters)
        try:
            # selected player shoots goal!
            # validation is on by default, so if it fails, exception is raised
            logic.shoot_goal(selected, match)
            number_of_goals -= 1
        except LogicException as e:
            print(u"{} can't shoot goals, reason: {}".format(selected.name, str(e)))

    print(u"\nFinal score:")
    print(u"{:15} - {}".format(match.first_team.name, match.first_team.goals))
    print(u"{:15} - {}".format(match.second_team.name, match.second_team.goals))


if __name__ == '__main__':
    main()
