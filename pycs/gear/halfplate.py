"""Half Plate"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class HalfPlate(Armour):
    """Budget Tank"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 15
        kwargs["dex_bonus"] = True
        kwargs["max_dex_bonus"] = 2
        super().__init__("Half Plate", **kwargs)


# EOF
