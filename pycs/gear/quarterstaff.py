""" A Quarterstaff """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Quarterstaff(MeleeWeapon):
    """Long and blunt"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["dmgroll"] = DamageRoll("1d6", 0, DamageType.BLUDGEONING)

        super().__init__("Quarterstaff", **kwargs)


# EOF
