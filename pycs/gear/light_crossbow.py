""" A Mace """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class LightCrossbow(RangedWeapon):
    """Fire sticks at speed"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 80
        kwargs["l_range"] = 320
        kwargs["dmgroll"] = DamageRoll("1d8", 0, DamageType.PIERCING)

        super().__init__("Light Crossbow", **kwargs)


# EOF
