""" Ghoul Monster Class """
import colors
from attacks import MeleeAttack
from constants import DamageType
from constants import Condition
from .monster import Monster


##############################################################################
class Ghoul(Monster):
    """Ghoul - https://www.dndbeyond.com/monsters/ghoul"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "5d8"
        kwargs.update(
            {
                "ac": 12,
                "speed": 30,
                "str": 13,
                "dex": 15,
                "con": 10,
                "int": 7,
                "wis": 10,
                "cha": 6,
                "immunity": [DamageType.POISON],
            }
        )
        super().__init__(**kwargs)
        #        self.add_action(
        #            MeleeAttack(
        #                "Bite",
        #                reach=5,
        #                bonus=2,
        #                dmg=("2d6", 2),
        #                dmg_type=DamageType.PIERCING,
        #            )
        #        )
        self.add_action(
            MeleeAttack(
                "Claw",
                reach=5,
                bonus=4,
                dmg=("2d4", 2),
                dmg_type=DamageType.SLASHING,
                side_effect=self.ghoul_claws,
            )
        )

    ##########################################################################
    def ghoul_claws(self, target):
        """Side effect of ghoul claws"""
        svth = target.saving_throw("con", 10)
        if not svth:
            print(f"{target} got paralysed by {self}")
            target.add_condition(Condition.PARALYZED)

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("G", style="bold")
        else:
            return colors.green("G", bg="red", style="bold")


# EOF
