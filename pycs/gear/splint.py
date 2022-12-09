""" Splint Mail"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Splint(Armour):
    """Clinky"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 17
        super().__init__("Splint", **kwargs)


# EOF
