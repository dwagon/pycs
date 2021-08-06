""" Fighter """
from .character import Character


##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shortrepr(self):
        """What a fighter looks like in the arena"""
        return "F"


# EOF
