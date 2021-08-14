"""https://www.dndbeyond.com/spells/cure-wounds"""

from actions import SpellAction
from constants import SpellType
import spells


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
    def pick_target(self, doer):
        """Who should we target"""
        return spells.pick_target(doer)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        return spells.healing_heuristic(doer, self)


# EOF
