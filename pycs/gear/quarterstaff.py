""" A Quarterstaff """
from typing import Any
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Quarterstaff(MeleeWeapon):
    """Long and blunt"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.BLUDGEONING

        super().__init__("Quarterstaff", **kwargs)


# EOF
