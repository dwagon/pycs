""" Plate Mail"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Plate(Armour):
    """Very Clinky"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 18
        super().__init__("Plate", **kwargs)


# EOF
