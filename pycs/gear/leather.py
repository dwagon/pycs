""" Leather"""
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Leather(Armour):
    """Dead Cow"""

    def __init__(self, **kwargs):

        kwargs["ac"] = 11
        kwargs["dex_bonus"] = True
        super().__init__("Leather", **kwargs)


# EOF
