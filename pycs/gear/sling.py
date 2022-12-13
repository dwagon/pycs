""" A Sling """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Sling(RangedWeapon):
    """Piff rocks"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 30
        kwargs["l_range"] = 120
        kwargs["dmgroll"] = DamageRoll("1d4", 0, DamageType.BLUDGEONING)

        super().__init__("Sling", **kwargs)


# EOF
