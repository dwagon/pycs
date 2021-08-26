""" Base Monster Class """
from pycs.creature import Creature


##############################################################################
class Monster(Creature):
    """Base monster class"""

    def __init__(self, **kwargs):  # pylint: disable=useless-super-delegation
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""
        pass


# EOF
