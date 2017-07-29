from business_logic import LogicErrors
from business_logic.exceptions import InvalidOperationException, NotPermittedException


class MatchErrors(LogicErrors):
    CANT_SHOOT_GOAL_NOT_IN_TEAMS = InvalidOperationException(u'Player is not taking part in match')
    CANT_SHOOT_GOAL_MATCH_NOT_STARTED = InvalidOperationException(u'Match not started yet!')
    CANT_SHOOT_GOAL_NOT_PLAYER = NotPermittedException(u'Only player can shoot goals')

    CANT_FINISH_NOT_STARTED = InvalidOperationException(u'Only started match can be finished')
    CANT_FINISH_NOT_REFEREE = NotPermittedException(u'Only referee can finish match')

    CANT_START_NOT_EVEN_TEAMS = InvalidOperationException(u'Teams are not even')
    CANT_START_ALREADY_STARTED = InvalidOperationException(u'Match already started')
    CANT_START_NOT_REFEREE = NotPermittedException(u'Only referee can start match')
