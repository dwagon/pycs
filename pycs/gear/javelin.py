""" A Javelin """
from typing import Any
from pycs.constant import DamageType
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Javelin(RangedWeapon):
    """Long pointy sticks"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 30
        kwargs["l_range"] = 120
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Javelin", **kwargs)


# EOF
