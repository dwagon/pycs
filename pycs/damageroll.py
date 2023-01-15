""" Damage Roll"""

import dice
from pycs.constant import DamageType
from pycs.damage import Damage


class DamageRoll:
    """Basic Damage Roll"""

    def __init__(self, roll: str = "", bonus: int = 0, type_: DamageType = DamageType.NONE):
        self.diceroll: str = roll
        self.bonus: int = bonus
        self.type: DamageType = type_

    def __repr__(self) -> str:
        return f"<DamageRoll {self.diceroll}+{self.bonus} of {self.type}>"

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
        if self.bonus:
            return f"{self.diceroll}+{self.bonus}"
        return f"{self.diceroll}"

    def __bool__(self) -> bool:
        """Boolean repr of damage roll"""
        if self.diceroll == "" and self.bonus == 0:
            return False
        return True


# EOF
