"""https://www.dndbeyond.com/spells/enhance-ability"""

from constants import SpellType
from spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Enhance_Ability(SpellAction):
    """You touch a creature and bestow upon it a magical enhancement.
    Choose one of the following effects; the target gains that effect
    until the spell ends.

    Bear's Endurance. The target has advantage on Constitution checks.
    It also gains 2d6 temporary hit points, which are lost when the
    spell ends.

    Bull's Strength. The target has advantage on Strength checks, and
    his or her carrying capacity doubles.

    Cat's Grace. The target has advantage on Dexterity checks. It also
    doesn't take damage from falling 20 feet or less if it isn't
    incapacitated.

    Eagle's Splendor. The target has advantage on Charisma checks.

    Fox's Cunning. The target has advantage on Intelligence checks.

    Owl's Wisdom. The target has advantage on Wisdom checks.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, you can target one additional creature for
    each slot level above 2nd."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Enhance Ability"
        kwargs.update({"reach": 0, "level": 2, "type": SpellType.BUFF})
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 0

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        return doer

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        return True


# EOF
