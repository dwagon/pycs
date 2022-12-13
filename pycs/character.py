""" Base Player character """
from typing import Any
from pycs.creature import Creature
from pycs.spell import SpellAction
from pycs.damage import Damage
from pycs.races import Human
from pycs.util import check_args
from pycs.constant import Condition


##############################################################################
class Character(Creature):
    """Base character class"""

    def __init__(self, **kwargs: Any):
        check_args(self._valid_args(), self.__class__.__name__, kwargs)
        self.level = kwargs.get("level", 1)
        self.race = kwargs.get("race", Human)()
        self.race.owner = self
        if "prof_bonus" not in kwargs:
            profb = int((kwargs.get("level", 1) - 1) / 4) + 2
            kwargs.update({"prof_bonus": profb})
        super().__init__(**kwargs)

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"level", "race"}

    ##########################################################################
    def shortrepr(self) -> str:
        """Arena repr"""
        return "?"

    ##########################################################################
    def spell_actions(self) -> list[SpellAction]:
        """Return a list of actions that are spells"""
        return [_ for _ in self.actions if issubclass(_.__class__, SpellAction)]

    ##########################################################################
    def creature_fallen_unconscious(self, dmg: Damage, critical: bool) -> None:
        """Character has fallen unconscious"""
        self.hp = 0
        if self.has_condition(Condition.UNCONSCIOUS):
            return
        self.remove_concentration()
        self.add_condition(Condition.UNCONSCIOUS)
        self.remove_condition(Condition.OK)


# EOF
