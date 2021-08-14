"""https://www.dndbeyond.com/spells/enhance-ability"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Enhance_Ability(SpellAction):
    """Up to six creatures of your choice that you can see within range
    each regain hit points equal to 2d8 + your spellcasting ability
    modifier. This spell has no effect on undead or constructs.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, the healing increases by 1d8 for each slot
    level above 2nd.
    """

    def __init__(self, **kwargs):
        name = "Enhance Ability"
        kwargs.update(
            {
                "reach": 5,
                "level": 2,
                "side_effect": self.enhance_ability,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def enhance_ability(self, caster, target):
        """Do the spell"""


# EOF