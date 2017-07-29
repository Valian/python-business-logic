from unittest import TestCase

from business_logic.tests import BusinessLogicTestMixin

import factories
import models
import logic
from errors import MatchErrors


class TestFactories(TestCase):

    def test_person_factory(self):
        person = factories.PersonFactory()
        self.assertIsNotNone(person.name)
        self.assertIsInstance(person, models.Person)

    def test_referee_factory(self):
        referee = factories.RefereeFactory()
        self.assertIsNotNone(referee.name)
        self.assertIsInstance(referee, models.Referee)

    def test_player_factory(self):
        player = factories.PlayerFactory()
        self.assertIsNotNone(player.name)
        self.assertIsInstance(player, models.Player)

    def test_team_factory(self):
        team = factories.TeamFactory(players__count=5)
        self.assertIsNotNone(team)
        self.assertEqual(len(team.players), 5)
        self.assertTrue(all(isinstance(p, models.Player) for p in team.players))


class StartMatchLogicTests(BusinessLogicTestMixin, TestCase):

    def test_not_referee_cant_start_match(self):
        person = factories.PersonFactory()
        match = factories.MatchFactory()
        with self.shouldRaiseException(MatchErrors.CANT_START_NOT_REFEREE):
            logic.can_start_match(person, match)

    def test_cant_start_match_if_already_started(self):
        referee = factories.RefereeFactory()
        match = factories.MatchFactory(status=models.Match.STARTED)
        with self.shouldRaiseException(MatchErrors.CANT_START_ALREADY_STARTED):
            logic.can_start_match(referee, match)

    def test_cant_start_match_if_teams_have_different_number_of_players(self):
        referee = factories.RefereeFactory()
        match = factories.MatchFactory(
            first_team__players__count=3,
            second_team__players__count=5)
        with self.shouldRaiseException(MatchErrors.CANT_START_NOT_EVEN_TEAMS):
            logic.can_start_match(referee, match)

    def test_start_match(self):
        referee = factories.RefereeFactory()
        match = factories.MatchFactory(status=models.Match.BEFORE_START)
        logic.start_match(referee, match)
        self.assertEqual(match.status, match.STARTED)


class FinishMatchLogicTests(BusinessLogicTestMixin, TestCase):

    def test_not_referee_cant_finish_match(self):
        person = factories.PersonFactory()
        match = factories.MatchFactory(status=models.Match.STARTED)
        with self.shouldRaiseException(MatchErrors.CANT_FINISH_NOT_REFEREE):
            logic.can_finish_match(person, match)

    def test_cant_finish_match_if_not_started(self):
        referee = factories.RefereeFactory()
        match = factories.MatchFactory(status=models.Match.BEFORE_START)
        with self.shouldRaiseException(MatchErrors.CANT_FINISH_NOT_STARTED):
            logic.can_finish_match(referee, match)

    def test_cant_finish_match_if_already_finished(self):
        referee = factories.RefereeFactory()
        match = factories.MatchFactory(status=models.Match.FINISHED)
        with self.shouldRaiseException(MatchErrors.CANT_FINISH_NOT_STARTED):
            logic.can_finish_match(referee, match)

    def test_finish_match_gives_reward_to_winning_team(self):
        referee = factories.RefereeFactory()
        reward = 1000
        match = factories.MatchFactory(
            first_team__goals=1,
            second_team__goals=0,
            status=models.Match.STARTED,
            reward=reward)
        logic.finish_match(referee, match)
        self.assertEqual(match.status, match.FINISHED)
        # referee takes 50% of winning players reward as salary
        self.assertEqual(referee.cash, 0.5 * reward)
        for player in match.first_team.players:
            self.assertEqual(player.cash, reward)
        for player in match.second_team.players:
            self.assertEqual(player.cash, 0)

    def test_draw_divides_reward_between_players(self):
        referee = factories.RefereeFactory()
        reward = 1000
        match = factories.MatchFactory(
            first_team__goals=3,
            second_team__goals=3,
            status=models.Match.STARTED,
            reward=reward)
        logic.finish_match(referee, match)
        self.assertEqual(match.status, match.FINISHED)
        self.assertEqual(referee.cash, 0.5 * reward)
        for player in match.first_team.players:
            self.assertEqual(player.cash, reward / 2)
        for player in match.second_team.players:
            self.assertEqual(player.cash, reward / 2)
