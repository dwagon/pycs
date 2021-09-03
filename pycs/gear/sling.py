""" A Sling """
from pycs.constant import DamageType
from pycs.equipment import RangedWeapon


##############################################################################
##############################################################################
##############################################################################
class Sling(RangedWeapon):
    """Piff rocks"""

    def __init__(self, **kwargs):
        kwargs["s_range"] = 30
        kwargs["l_range"] = 120
        kwargs["dmg"] = ("1d4", 0)
        kwargs["dmg_type"] = DamageType.BLUDGEONING

        super().__init__("Sling", **kwargs)


# EOF
