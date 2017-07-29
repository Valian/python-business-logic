class Person(object):
    def __init__(self, name, cash=0):
        self.name = name
        self.cash = cash

    @property
    def is_referee(self):
        return False


class Referee(Person):

    @property
    def is_referee(self):
        return True


class Player(Person):
    def __init__(self, name, cash=0, total_goals=0):
        super(Player, self).__init__(name, cash)
        self.total_goals = total_goals


class Team(object):
    def __init__(self, name, players=None, goals=0):
        self.name = name
        self.players = players or []
        self.goals = goals


class Match(object):

    BEFORE_START, STARTED, FINISHED = range(3)
    AVAILABLE_STATUSES = {BEFORE_START, STARTED, FINISHED}

    def __init__(self, first_team, second_team, reward, status=BEFORE_START):
        self.first_team = first_team
        self.second_team = second_team
        self.reward = reward
        self.winner = None
        self.status = status
