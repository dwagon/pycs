""" Minotaur Skeleton Monster Class """
import colors
from pycs.attack import MeleeAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
class MinotaurSkeleton(Monster):
    """Minotaur Skeleton - https://www.dndbeyond.com/monsters/minotaur-skeleton"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "9d10+18",
                "ac": 12,
                "challenge": 2,
                "speed": 40,
                "type": MonsterType.UNDEAD,
                "str": 18,
                "dex": 11,
                "con": 15,
                "int": 6,
                "wis": 8,
                "cha": 5,
                "vulnerable": [DamageType.BLUDGEONING],
                "immunity": [DamageType.POISON],
                "cond_immunity": [Condition.EXHAUSTION, Condition.POISONED],
                "actions": [
                    MeleeAttack(
                        "Greataxe",
                        reach=5,
                        dmg=("2d12", 0),
                        dmg_type=DamageType.SLASHING,
                    ),
                    MeleeAttack(
                        "Gore", reach=5, dmg=("2d8", 0), dmg_type=DamageType.PIERCING
                    ),
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What a minotaur skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("M")
        return colors.green("M", bg="red")


# EOF
