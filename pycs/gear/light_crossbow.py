""" A Mace """
from pycs.constant import DamageType
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Light_Crossbow(RangedWeapon):
    """Fire sticks at speed"""

    def __init__(self, **kwargs):
        kwargs["s_range"] = 80
        kwargs["l_range"] = 320
        kwargs["dmg"] = ("1d8", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Light Crossbow", **kwargs)


# EOF
