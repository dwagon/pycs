"""https://www.dndbeyond.com/spells/frostbite"""

from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.spell import AttackSpell


##############################################################################
##############################################################################
##############################################################################
class Frostbite(AttackSpell):
    """You cause numbing frost to form on one creature that you can see
    within range. The target must make a Constitution saving throw. On
    a failed save, the target takes 1d6 cold damage, and it has
    disadvantage on the next weapon attack roll it makes before the end
    of its next turn.

    The spell’s damage increases by 1d6 when you reach 5th level (2d6),
    11th level (3d6), and 17th level (4d6)."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Frostbite"
        self._target = None
        kwargs.update(
            {
                "reach": 60,
                "level": 0,
                "style": SpellType.SAVE_NONE,
                "type": SpellType.RANGED,
                "save_stat": Stat.CON,
                "dmg": ("1d6", 0),
                "dmg_type": DamageType.COLD,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Slightly better than the damage itself would indicate"""
        return super().heuristic(doer) + 2

    ##########################################################################
    def pick_target(self, doer):
        """Who should we target"""
        self._target = super().pick_target(doer)
        return self._target

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        self._target.add_effect(FrostbiteEffect(cause=caster))
        return super().cast(caster)


##############################################################################
##############################################################################
##############################################################################
class FrostbiteEffect(Effect):
    """Effect of the Frostbite"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Frostbite", **kwargs)

    ##########################################################################
    def initial(self, target):
        """Initial effects of Frostbite"""

    ##########################################################################
    def hook_gives_disadvantage(self, target):
        return True

    ##########################################################################
    def removal_end_of_its_turn(self, victim):
        return True


# EOF
