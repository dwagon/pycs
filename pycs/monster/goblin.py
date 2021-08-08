""" Gobline Monster Class """
import colors
from attacks import MeleeAttack
from attacks import RangedAttack
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
                "str": 8,
                "dex": 14,
                "con": 10,
                "int": 10,
                "wis": 8,
                "cha": 8,
            }
        )
        super().__init__(**kwargs)
        self.add_action(MeleeAttack("scimitar", reach=5, bonus=4, dmg=("1d6", 2)))

        self.add_action(
            RangedAttack("shortbow", bonus=4, s_range=80, l_range=320, dmg=("1d6", 2))
        )

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("G")
        else:
            return colors.green("G", bg="red")


# EOF
