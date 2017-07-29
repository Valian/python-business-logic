class Person(object):
    def __init__(self, name):
        self.name = name

    @property
    def is_referee(self):
        return False


class Referee(Person):

    @property
    def is_referee(self):
        return True


class Player(Person):
    def __init__(self, name, total_goals):
        super(Player, self).__init__(name)
        self.total_goals = total_goals


class Team(object):
    def __init__(self, players):
        self.players = players
        self.goals = 0


class Match(object):

    BEFORE_START, STARTED, FINISHED = range(3)
    AVAILABLE_STATUSES = {BEFORE_START, STARTED, FINISHED}

    def __init__(self, first_team, second_team, reward, status=BEFORE_START):
        self.first_team = first_team
        self.second_team = second_team
        self.reward = reward
        self.winner = None
        self.status = status
