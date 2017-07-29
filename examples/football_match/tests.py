from unittest import TestCase

import factories, models


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
