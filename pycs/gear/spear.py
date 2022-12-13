""" A spear """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Spear(RangedWeapon):
    """Long and Pointy"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 20
        kwargs["l_range"] = 60
        kwargs["dmgroll"] = DamageRoll("1d6", 0, DamageType.PIERCING)

        super().__init__("Spear", **kwargs)


# EOF
