""" Chain Mail"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Chainmail(Armour):
    """Clinky"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 16
        super().__init__("Chain mail", **kwargs)


# EOF
