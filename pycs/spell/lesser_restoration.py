"""https://www.dndbeyond.com/spells/lesser-restoration"""

import spells
from constants import SpellType


##############################################################################
class Lesser_Restoration(spells.SpellAction):
    """You touch a creature and can end either one disease or one
    condition afflicting it. The condition can be blinded, deafened,
    paralyzed, or poisoned."""

    def __init__(self, **kwargs):
        name = "Lesser Restoration"
        kwargs.update(
            {
                "reach": 5,
                "level": 2,
                "side_effect": self.lesser_restoration,
                "type": SpellType.HEALING,
            }
        )
        super().__init__(name, **kwargs)

    def lesser_restoration(self, caster, target):
        """Do the spell"""

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        return 0


# EOF
