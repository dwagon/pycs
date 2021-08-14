""" Utility functions for spell """
from collections import namedtuple


##############################################################################
def health_level_of_peers(doer):
    """Return the health levels of peers"""
    result = namedtuple("Result", "health id target")
    peers = [
        result(1 - _.hp / _.max_hp, id(_), _)
        for _ in doer.arena.my_side(doer.side)
        if doer.distance(_) <= 1
    ]
    peers.sort(reverse=True)
    return peers[0]


##############################################################################
def healing_heuristic(doer, spell):
    """Should we cast this"""
    if not doer.spell_available(spell):
        return 0
    peers = health_level_of_peers(doer)
    if peers[0] < 0.25:  # No one is less than 25% wounded
        return 0
    elif peers[0] < 0.5:
        return 2
    elif peers[0] < 0.7:
        return 3
    else:
        return 5


##############################################################################
def pick_target(doer):
    """Who to heal"""
    return health_level_of_peers(doer).target


# EOF
