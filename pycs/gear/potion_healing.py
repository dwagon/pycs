""" https://www.dndbeyond.com/magic-items/potion-of-healing """
from typing import Any
from pycs.equipment import HealingPotion


##############################################################################
##############################################################################
##############################################################################
class PotionHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["curing"] = ("2d4", 2)
        super().__init__("Potion of Healing", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class PotionGreaterHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["curing"] = ("4d4", 4)
        super().__init__("Potion of Greater Healing", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class PotionSuperiorHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["curing"] = ("8d4", 8)
        super().__init__("Potion of Superior Healing", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class PotionSupremeHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["curing"] = ("10d4", 20)
        super().__init__("Potion of Supreme Healing", **kwargs)


# EOF
