""" https://www.dndbeyond.com/spells/sacred-flame"""

from typing import Any
from pycs.damageroll import DamageRoll
from pycs.spell import AttackSpell
from pycs.constant import DamageType
from pycs.constant import Stat
from pycs.constant import SpellType


##############################################################################
class SacredFlame(AttackSpell):
    """Flame-like radiance descends on a creature that you can see
    within range. The target must succeed on a Dexterity saving throw
    or take 1d8 radiant damage. The target gains no benefit from cover
    for this saving throw.

    The spell's damage increases by 1d8 when you reach 5th level (2d8),
    11th level (3d8), and 17th level (4d8)."""

    ###########################################################################
    def __init__(self, **kwargs: Any):
        name = "Sacred Flame"
        kwargs.update(
            {
                "type": SpellType.RANGED,
                "reach": 60,
                "style": SpellType.SAVE_NONE,
                "save_stat": Stat.DEX,
                "dmgroll": DamageRoll("1d8", 0, DamageType.RADIANT),
                "level": 0,
            }
        )
        super().__init__(name, **kwargs)


# EOF
