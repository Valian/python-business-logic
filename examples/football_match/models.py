class Person(object):
    def __init__(self, name, cash=0):
        self.name = name
        self.cash = cash

    @property
    def is_referee(self):
        return False

    def __str__(self):
        return 'Person <name: "{}" cash: {} >'.format(self.name, self.cash)


class Referee(Person):

    @property
    def is_referee(self):
        return True

    def __str__(self):
        return 'Referee <name: "{}" cash: {} >'.format(self.name, self.cash)


class Player(Person):
    def __init__(self, name, cash=0, total_goals=0):
        super(Player, self).__init__(name, cash)
        self.total_goals = total_goals

    def __str__(self):
        return 'Player <name: "{}" cash: {} goals: {}>'.format(self.name, self.cash, self.total_goals)


class Team(object):
    def __init__(self, name, players=None, goals=0):
        self.name = name.upper()
        self.players = players or []
        self.goals = goals

    def __str__(self):
        return 'Team <name: "{}" goals: {} players_count: {} >'.format(self.name, self.goals, len(self.players))


class Match(object):

    BEFORE_START, STARTED, FINISHED = range(3)
    AVAILABLE_STATUSES = {
        BEFORE_START: 'Before start',
        STARTED: 'Started',
        FINISHED: 'Finished'
    }

    def __init__(self, first_team, second_team, reward, status=BEFORE_START):
        self.first_team = first_team
        self.second_team = second_team
        self.reward = reward
        self.winner = None
        self.status = status

    def get_status_display(self):
        return self.AVAILABLE_STATUSES[self.status]

    def __str__(self):
        return 'Match "{} vs {}" <status: {}, reward: {}, winner: {}>'.format(
            self.first_team.name, self.second_team.name, self.get_status_display(),
            self.reward, self.winner and self.winner.name
        )
