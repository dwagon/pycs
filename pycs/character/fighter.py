""" Fighter """
import colors
from attacks import MeleeAttack
from constants import DamageType
from .character import Character


##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, level=1, **kwargs):
        self.level = level
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
                "ac": 18,
                "hp": 10,
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Longsword",
                reach=5,
                bonus=5,
                dmg=("1d8", 3),
                dmg_type=DamageType.PIERCING,
            )
        )

    def shortrepr(self):
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("F")
        else:
            return colors.blue("F", bg="red")


# EOF
