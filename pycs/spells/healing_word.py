"""https://www.dndbeyond.com/spells/healing-word"""

from actions import SpellAction
from constants import SpellType
import spells


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
    def pick_target(self, doer):
        """Who should we target"""
        return spells.pick_target(doer)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        return spells.healing_heuristic(doer, self)


# EOF
