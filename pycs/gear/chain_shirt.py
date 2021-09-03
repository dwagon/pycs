"""Chain Shirt"""
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class ChainShirt(Armour):
    """Half-Clinky"""

    def __init__(self, **kwargs):

        kwargs["ac"] = 13
        kwargs["dex_bonus"] = True
        kwargs["max_dex_bonus"] = 2
        super().__init__("Chain Shirt", **kwargs)


# EOF
