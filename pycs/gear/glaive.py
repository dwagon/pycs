""" A glaive """
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Glaive(MeleeWeapon):
    """Long and slashy"""

    def __init__(self, **kwargs):
        kwargs["reach"] = 10
        kwargs["dmg"] = ("1d10", 0)
        kwargs["dmg_type"] = DamageType.SLASHING

        super().__init__("Glaive", **kwargs)


# EOF
