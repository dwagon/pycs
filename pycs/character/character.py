""" Base Player character """
from creature import Creature
from actions import SpellAction


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):  # pylint: disable=useless-super-delegation
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""

    ##########################################################################
    def spell_actions(self):
        """ Return a list of actions that are spells """
        return [_ for _ in self.actions if issubclass(_.__class__, SpellAction)]


# EOF
