""" Skeleton Monster Class """
import colors
from pycs.gear import Shortsword
from pycs.gear import Shortbow
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.monster import Monster


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
        self.add_gear(Shortsword())
        self.add_gear(Shortbow())

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("S")
        return colors.green("S", bg="red")


# EOF
