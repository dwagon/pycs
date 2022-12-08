""" https://www.dndbeyond.com/magic-items/potion-of-healing """
from typing import Any
from pycs.equipment import HealingPotion


##############################################################################
##############################################################################
##############################################################################
class PotionHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["cure_dice"] = "2d4"
        kwargs["cure_bonus"] = 2
        super().__init__("Potion of Healing", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class PotionGreaterHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["cure_dice"] = "4d4"
        kwargs["cure_bonus"] = 4
        super().__init__("Potion of Greater Healing", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class PotionSuperiorHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["cure_dice"] = "8d4"
        kwargs["cure_bonus"] = 8
        super().__init__("Potion of Superior Healing", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class PotionSupremeHealing(HealingPotion):
    """Liquid Band Aids"""

    def __init__(self, **kwargs: Any):
        kwargs["cure_dice"] = "10d4"
        kwargs["cure_bonus"] = 20
        super().__init__("Potion of Supreme Healing", **kwargs)


# EOF
