""" Padded """
from typing import Any
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Padded(Armour):
    """Puffy"""

    def __init__(self, **kwargs: Any):

        kwargs["ac"] = 11
        kwargs["dex_bonus"] = True
        super().__init__("Padded", **kwargs)


# EOF
