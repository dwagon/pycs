""" A Mace """
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Mace(MeleeWeapon):
    """Long and pointy"""

    def __init__(self, **kwargs):
        kwargs["reach"] = 5
        kwargs["dmg"] = ("1d6", 0)
        kwargs["dmg_type"] = DamageType.BLUDGEONING

        super().__init__("Mace", **kwargs)


# EOF
