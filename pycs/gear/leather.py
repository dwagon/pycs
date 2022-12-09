""" Leather"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Leather(Armour):
    """Dead Cow"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 11
        kwargs["dex_bonus"] = True
        super().__init__("Leather", **kwargs)


# EOF
