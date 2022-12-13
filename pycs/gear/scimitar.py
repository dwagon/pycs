""" A scimitar """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Scimitar(MeleeWeapon):
    """Short and curvy"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["finesse"] = True
        kwargs["dmgroll"] = DamageRoll("1d6", 0, DamageType.SLASHING)

        super().__init__("Scimitar", **kwargs)


# EOF
