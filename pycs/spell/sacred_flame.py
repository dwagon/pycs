""" https://www.dndbeyond.com/spells/sacred-flame"""

from spells import AttackSpell
from constants import DamageType
from constants import Stat
from constants import SpellType


##############################################################################
class Sacred_Flame(AttackSpell):
    """Spell"""

    ###########################################################################
    def __init__(self, **kwargs):
        name = "Sacred Flame"
        kwargs.update(
            {
                "type": SpellType.RANGED,
                "reach": 60,
                "style": "save",
                "save": (Stat.DEX, 13),
                "dmg": ("1d8", 0),
                "dmg_type": DamageType.RADIANT,
                "level": 0,
            }
        )
        super().__init__(name, **kwargs)


# EOF
