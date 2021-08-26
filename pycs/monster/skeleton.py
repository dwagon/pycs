""" Skeleton Monster Class """
import colors
from pycs.attacks import MeleeAttack
from pycs.attacks import RangedAttack
from pycs.constants import DamageType
from pycs.constants import MonsterType
from pycs.monsters import Monster


##############################################################################
class Skeleton(Monster):
    """Skeleton - https://www.dndbeyond.com/monsters/skeleton"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d8+4"
        kwargs.update(
            {
                "ac": 13,
                "speed": 30,
                "type": MonsterType.UNDEAD,
                "str": 10,
                "dex": 14,
                "con": 15,
                "int": 6,
                "wis": 8,
                "cha": 5,
                "vulnerable": [DamageType.BLUDGEONING],
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Shortsword",
                reach=5,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

        self.add_action(
            RangedAttack(
                "Shortbow",
                s_range=80,
                l_range=320,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("S")
        return colors.green("S", bg="red")


# EOF
