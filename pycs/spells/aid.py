"""https://www.dndbeyond.com/spells/aid"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Aid(SpellAction):
    """Your spell bolsters your allies with toughness and resolve.
    Choose up to three creatures within range. Each target's hit
    point maximum and current hit points increase by 5 for the
    duration.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, a target's hit points increase by an additional
    5 for each slot level above 2nd."""

    def __init__(self, **kwargs):
        name = "Aid"
        kwargs.update(
            {"reach": 30, "level": 2, "side_effect": self.aid, "type": SpellType.BUFF}
        )
        super().__init__(name, **kwargs)

    def aid(self, caster, target):
        """Do the spell"""


# EOF
