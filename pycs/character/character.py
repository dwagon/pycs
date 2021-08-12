""" Base Player character """
from creature import Creature


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):  # pylint: disable=useless-super-delegation
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""


# EOF
