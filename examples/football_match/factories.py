import factory

import models


class PersonFactory(factory.Factory):

    class Meta:
        model = models.Person

    name = factory.Faker('name')


class RefereeFactory(PersonFactory):

    class Meta:
        model = models.Referee


class PlayerFactory(PersonFactory):

    class Meta:
        model = models.Player

    total_goals = 0


class TeamFactory(factory.Factory):

    class Meta:
        model = models.Team

    name = factory.Faker('word')

    @factory.post_generation
    def players(self, create, extracted, count=0, **kwargs):
        if not extracted and count > 0:
            self.players = [PlayerFactory(**kwargs) for _ in range(count)]


class MatchFactory(factory.Factory):

    class Meta:
        model = models.Match

    first_team = factory.SubFactory(TeamFactory, players__count=5)
    second_team = factory.SubFactory(TeamFactory, players__count=5)
    reward = 0
