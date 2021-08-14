"""https://www.dndbeyond.com/spells/lesser-restoration"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Lesser_Restoration(SpellAction):
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


# EOF
