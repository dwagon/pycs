"""https://www.dndbeyond.com/spells/burning-hands"""

from typing import Any
from pycs.damageroll import DamageRoll
from pycs.spell import AttackSpell
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.constant import Stat


##############################################################################
class BurningHands(AttackSpell):
    """As you hold your hands with thumbs touching and fingers spread,
    a thin sheet of flames shoots forth from your outstretched fingertips.
    Each creature in a 15-foot cone must make a Dexterity saving throw.
    A creature takes 3d6 fire damage on a failed save, or half as much
    damage on a successful one.

    The fire ignites any flammable objects in the area that aren't being
    worn or carried.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, the damage increases by 1d6 for each slot level
    above 1st."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Burning Hands"
        kwargs.update(
            {
                "reach": 15,
                "level": 1,
                "dmgroll": DamageRoll("3d6", 0, DamageType.FIRE),
                "style": SpellType.SAVE_HALF,
                "type": SpellType.RANGED,
                "save_stat": Stat.DEX,
            }
        )
        super().__init__(name, **kwargs)


# EOF
