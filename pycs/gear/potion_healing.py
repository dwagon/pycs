""" https://www.dndbeyond.com/magic-items/potion-of-healing """
from pycs.equipment import HealingPotion


##############################################################################
##############################################################################
##############################################################################
class Potion_Healing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs):
        kwargs["curing"] = ("2d4", 2)
        super().__init__("Potion of Healing", **kwargs)


# EOF
