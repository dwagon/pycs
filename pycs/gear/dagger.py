""" A dagger """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Dagger(MeleeWeapon):
    """Very short and pointy"""

    def __init__(self, **kwargs: Any):
        kwargs["reach"] = 5
        kwargs["finesse"] = True
        kwargs["dmgroll"] = DamageRoll("1d4", 0, DamageType.PIERCING)

        super().__init__("Dagger", **kwargs)


# EOF
