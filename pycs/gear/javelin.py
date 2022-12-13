""" A Javelin """
from typing import Any
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Javelin(RangedWeapon):
    """Long pointy sticks"""

    def __init__(self, **kwargs: Any):
        kwargs["s_range"] = 30
        kwargs["l_range"] = 120
        kwargs["dmgroll"] = DamageRoll("1d6", 0, DamageType.SLASHING)

        super().__init__("Javelin", **kwargs)


# EOF
