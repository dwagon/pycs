"""Scale"""
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Scale(Armour):
    """Toucgh Lizard"""

    def __init__(self, **kwargs):

        kwargs["ac"] = 14
        kwargs["dex_bonus"] = True
        kwargs["max_dex_bonus"] = 2
        super().__init__("Scale mail", **kwargs)


# EOF
