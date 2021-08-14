"""https://www.dndbeyond.com/spells/bless"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Bless(SpellAction):
    """You bless up to three creatures of your choice within range.
    Whenever a target makes an attack roll or a saving throw before the
    spell ends, the target can roll a d4 and add the number rolled to
    the attack roll or saving throw.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, you can target one additional creature for
    each slot level above 1st."""

    def __init__(self, **kwargs):
        name = "Bless"
        kwargs.update(
            {"reach": 30, "level": 1, "side_effect": self.bless, "type": SpellType.BUFF}
        )
        super().__init__(name, **kwargs)

    def bless(self, caster):
        """Do the spell"""


# EOF
