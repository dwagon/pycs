""" Base Monster Class """
from creature import Creature


##############################################################################
class Monster(Creature):
    """ Base monster class """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    ##########################################################################
    def turn(self):
        """ Have a turn """


# EOF
