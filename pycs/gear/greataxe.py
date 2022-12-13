""" A Great Axe """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Greataxe(MeleeWeapon):
    """Long and sharp"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["dmgroll"] = DamageRoll("1d12", 0, DamageType.SLASHING)

        super().__init__("Greataxe", **kwargs)


# EOF
