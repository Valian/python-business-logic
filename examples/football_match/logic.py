from business_logic import validator, validated_by

import models
from errors import MatchErrors


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


@validated_by(can_start_match)
def start_match(person, match):
    match.status = match.STARTED
    # side effect, like sending emails, logging etc should live here
    print(u"{} started match!".format(person.name))


@validated_by(can_finish_match)
def finish_match(person, match):
    match.status = match.FINISHED
    first_score = match.first_team.goals
    second_score = match.second_team.goals
    if first_score == second_score:
        first_team_reward = match.reward / 2
        second_team_reward = match.reward / 2
    else:
        first_team_won = first_score > second_score
        first_team_reward = match.reward if first_team_won else 0
        second_team_reward = match.reward if not first_team_won else 0

    for player in match.first_team.players:
        player.cash += first_team_reward

    for player in match.second_team.players:
        player.cash += second_team_reward

    referee_salary = 0.5 * match.reward
    person.cash += referee_salary
