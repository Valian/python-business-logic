from business_logic import validator, validated_by

from examples.football_match import models
from examples.football_match.errors import MatchErrors


@validator
def can_shoot_goal(person, match):
    if not isinstance(person, models.Player):
        raise MatchErrors.CANT_SHOOT_GOAL_NOT_PLAYER
    if not match.status == match.STARTED:
        raise MatchErrors.CANT_SHOOT_GOAL_MATCH_NOT_STARTED
    if person not in match.first_team.players + match.second_team.players:
        raise MatchErrors.CANT_SHOOT_GOAL_NOT_IN_TEAMS


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
    if match.status != match.STARTED:
        raise MatchErrors.CANT_FINISH_NOT_STARTED
    if not person.is_referee:
        raise MatchErrors.CANT_FINISH_NOT_REFEREE


@validated_by(can_shoot_goal)
def shoot_goal(person, match):
    person.total_goals += 1
    if person in match.first_team.players:
        match.first_team.goals += 1
    else:
        match.second_team.goals += 1
    print(u"Goal was shoot by {}!".format(person.name))


@validated_by(can_start_match)
def start_match(person, match):
    match.status = match.STARTED
    # side effect, like sending emails, logging etc should live here
    print(u"{} started match!".format(person.name))


@validated_by(can_finish_match)
def finish_match(person, match):
    """
    A bit more complicated function calculating rewards, but I wanted
    to show that such cases are still perfectly valid
    """
    match.status = match.FINISHED
    print(u"{} finished match!\n".format(person.name))
    first_score = match.first_team.goals
    second_score = match.second_team.goals
    if first_score == second_score:
        first_team_reward = match.reward / 2
        second_team_reward = match.reward / 2
    else:
        first_team_won = first_score > second_score
        first_team_reward = match.reward if first_team_won else 0
        second_team_reward = match.reward if not first_team_won else 0
        match.winner = match.first_team if first_team_won else match.second_team

    for player in match.first_team.players:
        player.cash += first_team_reward
        print(u"{:24} - first team player  - earned {} cash!".format(player.name, first_team_reward))

    for player in match.second_team.players:
        player.cash += second_team_reward
        print(u"{:24} - second team player - earned {} cash!".format(player.name, second_team_reward))

    referee_salary = int(0.5 * match.reward)
    person.cash += referee_salary
    print(u"{:24} - referee            - earned {} cash as salary".format(person.name, referee_salary))
