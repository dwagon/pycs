""" A Short Bow """
from typing import Any
from pycs.constant import DamageType
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Shortbow(RangedWeapon):
    """Fire sticks at speed"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 80
        kwargs["l_range"] = 320
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Shortbow", **kwargs)


# EOF
