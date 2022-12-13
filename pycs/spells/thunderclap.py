"""https://www.dndbeyond.com/spells/thunderclap"""

from typing import Any
from pycs.damageroll import DamageRoll
from pycs.spell import AttackSpell
from pycs.constant import DamageType, SpellType
from pycs.constant import Stat


##############################################################################
class Thunderclap(AttackSpell):
    """You create a burst of thunderous sound that can be heard up to
    100 feet away. Each creature within range, other than you, must
    succeed on a Constitution saving throw or take 1d6 thunder damage.

    The spell's damage increases by 1d6 when you reach 5th level (2d6),
    11th level (3d6), and 17th level (4d6)."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Thunderclap"
        kwargs.update(
            {
                "reach": 5,
                "level": 0,
                "style": SpellType.SAVE_NONE,
                "save_stat": Stat.CON,
                "dmgroll": DamageRoll("1d6", 0, DamageType.THUNDER),
                "type": SpellType.MELEE,
            }
        )
        super().__init__(name, **kwargs)


# EOF
