""" Base Player character """
from creature import Creature
from spells import SpellAction
from constants import Race


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):
        self.race = kwargs.get("race", Race.HUMAN)
        if "prof_bonus" not in kwargs:
            profb = int((kwargs.get("level", 1) - 1) / 4) + 2
            kwargs.update({"prof_bonus": profb})
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""

    ##########################################################################
    def spell_actions(self):
        """Return a list of actions that are spells"""
        return [_ for _ in self.actions if issubclass(_.__class__, SpellAction)]


# EOF
