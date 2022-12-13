""" A Longbox """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Longbow(RangedWeapon):
    """Fire sticks at speed"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 150
        kwargs["l_range"] = 600
        kwargs["dmgroll"] = DamageRoll("1d8", 0, DamageType.PIERCING)

        super().__init__("Longbow", **kwargs)


# EOF
