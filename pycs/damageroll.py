""" Damage Roll"""

from typing import Optional
import dice
from pycs.constant import DamageType
from pycs.damage import Damage


class DamageRoll:
    """Basic Damage Roll"""

    def __init__(self, roll: str = "", bonus: int = 0, type_: DamageType = DamageType.NONE):
        self.diceroll: str = roll
        self.bonus: int = bonus
        self.type: DamageType = type_

    def roll(self) -> Damage:
        """Roll for damage"""
        dmg: int = 0
        if self.diceroll:
            dmg += int(dice.roll(self.diceroll))
        dmg += self.bonus
        return Damage(dmg, self.type)

    def roll_max(self) -> Damage:
        """Maximum damage"""
        dmg: int = 0
        if self.diceroll:
            dmg += int(dice.roll_max(self.diceroll))
        dmg += self.bonus
        return Damage(dmg, self.type)

    def __str__(self) -> str:
        return f"{self.diceroll} + {self.bonus}"
