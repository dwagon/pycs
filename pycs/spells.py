""" Handle non-attack Actions """
from collections import namedtuple
from actions import Action


##############################################################################
##############################################################################
##############################################################################
class SpellAction(Action):
    """Spell action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.type = kwargs.get("type")
        self.cure_hp = kwargs.get("cure_hp")
        self.level = kwargs.get("level")
        self.concentration = kwargs.get("concentration")

    ########################################################################
    def is_type(self, *types):
        """Is this spell of the specified types"""
        return self.type in types

    ########################################################################
    def perform_action(self, source):
        """Cast the spell"""
        print(f"{source} is casting {self.name}")
        source.cast(self)
        self.side_effect(source)

    ########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 1


##############################################################################
def health_level_of_peers(doer):
    """Return the health levels of peers as percentage"""
    result = namedtuple("Result", "health id target")
    peers = [
        result(100 * _.hp / _.max_hp, id(_), _) for _ in doer.arena.my_side(doer.side)
    ]
    peers.sort()
    return peers[0]


##############################################################################
def healing_heuristic(doer, spell):
    """Should we cast this"""
    if not doer.spell_available(spell):
        return 0
    peers = health_level_of_peers(doer)
    # print(f"health of peers = {peers}")
    if peers.health < 20:  # No one is less than 20% wounded
        return 5
    elif peers.health < 40:
        return 4
    elif peers.health < 60:
        return 2
    elif peers.health < 80:
        return 1
    else:
        return 0


##############################################################################
def pick_heal_target(doer):
    """Who to heal"""
    return health_level_of_peers(doer).target


# EOF
