""" A Mace """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Mace(MeleeWeapon):
    """Long and pointy"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["dmgroll"] = DamageRoll("1d6", 0, DamageType.BLUDGEONING)

        super().__init__("Mace", **kwargs)


# EOF
