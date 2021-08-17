""" Gobline Monster Class """
import colors
from attacks import MeleeAttack
from attacks import RangedAttack
from constants import DamageType
from constants import MonsterType
from .monster import Monster


##############################################################################
class Goblin(Monster):
    """Goblin"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d6"
        kwargs.update(
            {
                "ac": 15,
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 8,
                "dex": 14,
                "con": 10,
                "int": 10,
                "wis": 8,
                "cha": 8,
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "scimitar",
                reach=5,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

        self.add_action(
            RangedAttack(
                "shortbow",
                s_range=80,
                l_range=320,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("g")
        return colors.green("g", bg="red")


# EOF
