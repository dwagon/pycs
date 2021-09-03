""" A Great Axe """
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Greataxe(MeleeWeapon):
    """Long and sharp"""

    def __init__(self, **kwargs):
        kwargs["reach"] = 5
        kwargs["dmg"] = ("1d12", 0)
        kwargs["dmg_type"] = DamageType.SLASHING

        super().__init__("Greataxe", **kwargs)


# EOF
