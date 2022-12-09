""" A Mace """
from typing import Any
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Mace(MeleeWeapon):
    """Long and pointy"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.BLUDGEONING

        super().__init__("Mace", **kwargs)


# EOF
