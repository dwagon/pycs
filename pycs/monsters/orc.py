""" https://www.dndbeyond.com/monsters/orc"""
import colors
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
class Orc(Monster):
    """Orc"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d8+6"
        kwargs.update(
            {
                "ac": 13,
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 16,
                "dex": 12,
                "con": 16,
                "int": 7,
                "wis": 11,
                "cha": 10,
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Greataxe",
                reach=5,
                dmg=("1d12", 0),
                dmg_type=DamageType.SLASHING,
            )
        )

        self.add_action(
            RangedAttack(
                "Javelin",
                ammo=2,
                s_range=30,
                l_range=120,
                dmg=("1d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def shortrepr(self):
        """What an Orc looks like on the arena"""
        if self.is_alive():
            return colors.green("O")
        return colors.green("O", bg="red")


# EOF
