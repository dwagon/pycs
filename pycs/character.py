""" Base Player character """
from pycs.creature import Creature
from pycs.spell import SpellAction
from pycs.races import Human


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):
        self.level = kwargs.get("level", 1)
        self.race = kwargs.get("race", Human)()
        self.race.owner = self
        if "prof_bonus" not in kwargs:
            profb = int((kwargs.get("level", 1) - 1) / 4) + 2
            kwargs.update({"prof_bonus": profb})
        kwargs["effects"] = self.race.effects
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""

    ##########################################################################
    def spell_actions(self):
        """Return a list of actions that are spells"""
        return [_ for _ in self.actions if issubclass(_.__class__, SpellAction)]


# EOF
