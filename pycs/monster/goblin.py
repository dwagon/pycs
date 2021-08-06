""" Gobline Monster Class """
from .monster import Monster


##############################################################################
class Goblin(Monster):
    """Goblin"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """ What a goblin looks like on the arena """
        return "G"


# EOF
