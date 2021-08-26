"""https://www.dndbeyond.com/spells/cure-wounds"""

from pycs.spell import SpellAction
from pycs.spell import pick_heal_target
from pycs.spell import healing_heuristic
from pycs.constant import SpellType


##############################################################################
class Cure_Wounds(SpellAction):
    """A creature you touch regains a number of hit points equal to 1d8
    + your spellcasting ability modifier. This spell has no effect on
    undead or constructs."""

    ########################################################################
    def __init__(self, **kwargs):
        name = "Cure Wounds"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 5,
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def cast(self, caster):
        """Do the spell"""
        caster.target.heal("1d8", self.modifier(caster))
        return True

    ########################################################################
    def pick_target(self, doer):
        """Who should we target"""
        return pick_heal_target(doer)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        if not doer.spell_available(self):
            return 0
        return healing_heuristic(doer, self)


# EOF
