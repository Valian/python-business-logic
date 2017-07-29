from business_logic import LogicErrors
from business_logic.exceptions import InvalidOperationException, NotPermittedException


class MatchErrors(LogicErrors):
    CANT_FINISH_NOT_STARTED = InvalidOperationException(u'Only started match can be finished')
    CANT_FINISH_NOT_REFEREE = NotPermittedException(u'Only referee can finish match')

    CANT_START_NOT_EVEN_TEAMS = InvalidOperationException(u'Teams are not even')
    CANT_START_ALREADY_STARTED = InvalidOperationException(u'Match already started')
    CANT_START_NOT_REFEREE = NotPermittedException(u'Only referee can start match')
