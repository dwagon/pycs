""" https://www.dndbeyond.com/spells/guiding-bolt"""

from pycs.spell import AttackSpell
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class Guiding_Bolt(AttackSpell):
    """A flash of light streaks toward a creature of your choice within
    range. Make a ranged spell attack against the target. On a hit, the
    target takes 4d6 radiant damage, and the next attack roll made
    against this target before the end of your next turn has advantage,
    thanks to the mystical dim light glittering on the target until
    then."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Guiding Bolt"
        kwargs.update(
            {
                "type": SpellType.RANGED,
                "reach": 120,
                "dmg": ("4d6", 0),
                "dmg_type": DamageType.RADIANT,
                "style": SpellType.TOHIT,
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        caster.target.add_effect(GuidingBoltEffect(cause=caster))
        return True

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 0


##############################################################################
##############################################################################
##############################################################################
class GuidingBoltEffect(Effect):
    """Spell"""

    ##########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Guiding Bolt", **kwargs)

    ##########################################################################
    def hook_gives_advantage_against(self):
        """Gives advantage against creature who has effect"""
        print(f"{self.name} gives you advantage")
        return True

    ##########################################################################
    def removal_after_being_attacked(self):
        """Do we remove the effect after being turned"""
        return True


# EOF
