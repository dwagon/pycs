""" A scimitar """
from typing import Any
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Scimitar(MeleeWeapon):
    """Short and curvy"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["finesse"] = True
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.SLASHING

        super().__init__("Scimitar", **kwargs)


# EOF
