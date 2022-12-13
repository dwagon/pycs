""" A long sword """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Longsword(MeleeWeapon):
    """Long and pointy"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["dmgroll"] = DamageRoll("1d8", 0, DamageType.PIERCING)

        super().__init__("Longsword", **kwargs)


# EOF
