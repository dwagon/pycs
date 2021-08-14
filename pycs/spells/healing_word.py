"""https://www.dndbeyond.com/spells/healing-word"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Healing_Word(SpellAction):
    """A creature of your choice that you can see within range regains
    hit points equal to 1d4 + your spellcasting ability modifier. This
    spell has no effect on undead or constructs.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, the healing increases by 1d4 for each slot
    level above 1st."""

    def __init__(self, **kwargs):
        name = "Healing Word"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 60,
                "cure_hp": ("1d4", 3),
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
            if doer.distance(_) <= 60 / 5
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
