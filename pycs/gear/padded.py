""" Padded """
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Padded(Armour):
    """Puffy"""

    def __init__(self, **kwargs):

        kwargs["ac"] = 11
        kwargs["dex_bonus"] = True
        super().__init__("Padded", **kwargs)


# EOF
