""" A spear """
from pycs.constant import DamageType
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Spear(RangedWeapon):
    """Long and Pointy"""

    def __init__(self, **kwargs):
        kwargs["s_range"] = 20
        kwargs["l_range"] = 60
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Spear", **kwargs)


# EOF
