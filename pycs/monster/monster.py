""" Base Monster Class """
from creature import Creature


##############################################################################
class Monster(Creature):
    """Base monster class"""

    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""
        pass


# EOF
