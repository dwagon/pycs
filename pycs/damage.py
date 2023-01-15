""" Damage"""
from typing import Self, Union
from pycs.constant import DamageType


class Damage:
    """Represents damage"""

    def __init__(self, hp: int = 0, type_: DamageType = DamageType.NONE):
        self.hp = hp
        self.type = type_

    def __str__(self) -> str:
        return f"{self.hp} damage ({self.type.value})"

    def __repr__(self) -> str:
        return f"Damage: {self.hp} of {self.type.value}"

    def __add__(self, other: Union[int, "Damage"]) -> "Damage":
        if isinstance(other, int):
            self.hp += other
        elif isinstance(other, self.__class__):
            self.hp += other.hp
        self.hp = max(self.hp, 0)
        return self

    def copy(self) -> Self:
        """Copy a damage"""
        newdmg = Damage(hp=self.hp, type_=self.type)
        return newdmg

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Damage):
            return self.hp == other.hp and self.type == other.type
        return False

    def __int__(self) -> int:
        return self.hp

    def __ifloordiv__(self, denom: int) -> "Damage":
        self.hp //= denom
        return self

    def __sub__(self, amount: int) -> "Damage":
        self.hp -= amount
        return self

    def __bool__(self) -> bool:
        return self.hp != 0


# EOF
