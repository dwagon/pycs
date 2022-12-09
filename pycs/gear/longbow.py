""" A Longbox """
from typing import Any
from pycs.constant import DamageType
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Longbow(RangedWeapon):
    """Fire sticks at speed"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 150
        kwargs["l_range"] = 600
        kwargs["dmg"] = ("1d8", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Longbow", **kwargs)


# EOF
