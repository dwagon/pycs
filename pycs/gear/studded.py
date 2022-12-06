""" Studded"""
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Studded(Armour):
    """Dead Cow with spikes"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 12
        kwargs["dex_bonus"] = True
        super().__init__("Studded", **kwargs)


# EOF
