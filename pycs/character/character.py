""" Base Player character """
from creature import Creature
from actions import SpellAction


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):
        if "prof_bonus" not in kwargs:
            pb = int((kwargs.get("level", 1) - 1) / 4) + 2
            kwargs.update({"prof_bonus": pb})
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""

    ##########################################################################
    def spell_actions(self):
        """Return a list of actions that are spells"""
        return [_ for _ in self.actions if issubclass(_.__class__, SpellAction)]


# EOF
