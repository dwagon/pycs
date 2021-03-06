""" Base Player character """
from pycs.creature import Creature
from pycs.spell import SpellAction
from pycs.races import Human
from pycs.util import check_args
from pycs.constant import Condition
from pycs.constant import DamageType


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs):
        check_args(self._valid_args(), self.__class__.__name__, kwargs)
        self.level = kwargs.get("level", 1)
        self.race = kwargs.get("race", Human)()
        self.race.owner = self
        if "prof_bonus" not in kwargs:
            profb = int((kwargs.get("level", 1) - 1) / 4) + 2
            kwargs.update({"prof_bonus": profb})
        super().__init__(**kwargs)

    ##########################################################################
    def _valid_args(self):
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"level", "race"}

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""

    ##########################################################################
    def spell_actions(self):
        """Return a list of actions that are spells"""
        return [_ for _ in self.actions if issubclass(_.__class__, SpellAction)]

    ##########################################################################
    def creature_fallen_unconscious(
        self, dmg: int, dmg_type: DamageType, critical: bool
    ) -> None:
        """Character has fallen unconscious"""
        self.hp = 0
        if self.has_condition(Condition.UNCONSCIOUS):
            return
        self.remove_concentration()
        self.add_condition(Condition.UNCONSCIOUS)
        self.remove_condition(Condition.OK)


# EOF
