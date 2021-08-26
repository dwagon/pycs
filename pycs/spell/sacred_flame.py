""" https://www.dndbeyond.com/spells/sacred-flame"""

from pycs.spells import AttackSpell
from pycs.constants import DamageType
from pycs.constants import Stat
from pycs.constants import SpellType


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
