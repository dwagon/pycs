""" Shield"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Shield(Armour):
    """Clinky"""

    def __init__(self, **kwargs: Any):

        kwargs["ac_bonus"] = 2
        kwargs["dex_bonus"] = True
        super().__init__("Shield", **kwargs)


# EOF
