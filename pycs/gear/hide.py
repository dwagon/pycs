"""Hide"""
from pycs.equipment import Armour


##############################################################################
##############################################################################
##############################################################################
class Hide(Armour):
    """Tough Dead Cow"""

    def __init__(self, **kwargs):

        kwargs["ac"] = 12
        kwargs["dex_bonus"] = True
        kwargs["max_dex_bonus"] = 2
        super().__init__("Hide", **kwargs)


# EOF
