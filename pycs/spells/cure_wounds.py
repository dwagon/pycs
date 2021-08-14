"""https://www.dndbeyond.com/spells/cure-wounds"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Cure_Wounds(SpellAction):
    """Spell"""

    ########################################################################
    def __init__(self, **kwargs):
        name = "Cure Wounds"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 5,
                "cure_hp": ("1d8", 3),
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        if not doer.spell_available(self):
            return 0
        peers = [
            (1 - _.hp / _.max_hp, id(_), _)
            for _ in doer.arena.my_side(doer.side)
            if doer.distance(_) <= 1
        ]
        peers.sort(reverse=True)
        if peers[0][0] < 0.25:  # No one is less than 25% wounded
            return 0
        elif peers[0][0] < 0.5:
            return 2
        elif peers[0][0] < 0.7:
            return 3
        else:
            return 5


# EOF
