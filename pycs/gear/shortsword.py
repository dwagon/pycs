""" A short sword """
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Shortsword(MeleeWeapon):
    """Short and pointy"""

    def __init__(self, **kwargs):
        kwargs["reach"] = 5
        kwargs["finesse"] = True
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Shortsword", **kwargs)


# EOF
