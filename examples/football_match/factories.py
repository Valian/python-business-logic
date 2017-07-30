import factory

import models


class PersonFactory(factory.Factory):
    name = factory.Faker('name')
    cash = 0

    class Meta:
        model = models.Person


class RefereeFactory(PersonFactory):

    class Meta:
        model = models.Referee


class PlayerFactory(PersonFactory):
    total_goals = 0

    class Meta:
        model = models.Player


class TeamFactory(factory.Factory):
    name = factory.Faker('word')
    goals = 0

    class Meta:
        model = models.Team

    @factory.post_generation
    def players(self, create, extracted, count=4, **kwargs):
        if not extracted and count > 0:
            self.players = [PlayerFactory(**kwargs) for _ in range(count)]


class MatchFactory(factory.Factory):
    first_team = factory.SubFactory(TeamFactory, players__count=5)
    second_team = factory.SubFactory(TeamFactory, players__count=5)
    reward = 0

    class Meta:
        model = models.Match
