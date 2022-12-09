"""https://www.dndbeyond.com/spells/shatter"""

from typing import Any
from pycs.spell import AttackSpell
from pycs.constant import SpellType
from pycs.constant import DamageType
from pycs.constant import Stat


##############################################################################
class Shatter(AttackSpell):
    """A sudden loud ringing noise, painfully intense, erupts from a
    point of your choice within range. Each creature in a 10-foot-radius
    sphere centered on that point must make a Constitution saving throw.
    A creature takes 3d8 thunder damage on a failed save, or half as
    much damage on a successful one. A creature made of inorganic
    material such as stone, crystal, or metal has disadvantage on this
    saving throw."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Shatter"
        kwargs.update(
            {
                "reach": 60,
                "level": 2,
                "style": SpellType.SAVE_HALF,
                "dmg": ("3d8", 0),
                "dmg_type": DamageType.THUNDER,
                "save_stat": Stat.CON,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)


# EOF
