"""Scale"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Scale(Armour):
    """Toucgh Lizard"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 14
        kwargs["dex_bonus"] = True
        kwargs["max_dex_bonus"] = 2
        super().__init__("Scale mail", **kwargs)


# EOF
