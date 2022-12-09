""" Ring Mail"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Ringmail(Armour):
    """Clinky Precious"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 14
        super().__init__("Ring mail", **kwargs)


# EOF
