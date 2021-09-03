""" A long sword """
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Longsword(MeleeWeapon):
    """Long and pointy"""

    def __init__(self, **kwargs):
        kwargs["reach"] = 5
        kwargs["dmg"] = ("1d8", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Longsword", **kwargs)


# EOF
