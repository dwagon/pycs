"""https://www.dndbeyond.com/spells/hellish-rebuke"""

from pycs.spell import AttackSpell
from pycs.constant import SpellType
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import Stat


##############################################################################
class Hellish_Rebuke(AttackSpell):
    """You point your finger, and the creature that damaged you is
    momentarily surrounded by hellish flames. The creature must make a
    Dexterity saving throw. It takes 2d10 fire damage on a failed save,
    or half as much damage on a successful one.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, the damage increases by 1d10 for each slot
    level above 1st."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Hellish Rebuke"
        kwargs.update(
            {
                "category": ActionCategory.REACTION,
                "reach": 60,
                "level": 1,
                "dmg": ("2d10", 0),
                "dmg_type": DamageType.FIRE,
                "save_stat": Stat.DEX,
                "style": SpellType.SAVE_HALF,
                "type": SpellType.RANGED,
            }
        )
        super().__init__(name, **kwargs)


# EOF
