""" A dagger """
from pycs.constant import DamageType
from pycs.equipment import MeleeWeapon


##############################################################################
##############################################################################
##############################################################################
class Dagger(MeleeWeapon):
    """Very short and pointy"""

    def __init__(self, **kwargs):
        kwargs["reach"] = 5
        kwargs["dmg"] = ("1d4", 0)
        kwargs["dmg_type"] = DamageType.PIERCING

        super().__init__("Dagger", **kwargs)


# EOF
