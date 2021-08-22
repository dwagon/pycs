"""https://www.dndbeyond.com/spells/healing-word"""

import spells
from constants import SpellType


##############################################################################
class Healing_Word(spells.SpellAction):
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
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def cast(self, caster):
        """Do the spell"""
        caster.target.heal("1d4", self.modifier(caster))
        return True

    ########################################################################
    def pick_target(self, doer):
        """Who should we target"""
        return spells.pick_heal_target(doer)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        if not doer.spell_available(self):
            return 0
        return spells.healing_heuristic(doer, self)


# EOF
