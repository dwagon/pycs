""" Base Player character """
from creature import Creature


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = kwargs.get("level", 1)

    ##########################################################################
    def turn(self):
        """Have a turn"""

    ##########################################################################
    def shortrepr(self):
        """Arena repr """


# EOF
