""" Ghoul Monster Class """
import colors
from attacks import MeleeAttack
from constants import DamageType
from constants import Condition
from constants import Stat
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
        self.add_action(
            MeleeAttack(
                "Bite",
                reach=5,
                bonus=2,
                dmg=("2d6", 2),
                dmg_type=DamageType.PIERCING,
            )
        )
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
    def pick_best_attack(self):
        """Pick the claw attack more often than damage would indicate"""
        if self.target.has_condition(Condition.PARALYZED):
            return self.pick_attack_by_name("Bite")
        else:
            return self.pick_attack_by_name("Claw")

    ##########################################################################
    def ghoul_claws(self, target):
        """Side effect of ghoul claws"""
        svth = target.saving_throw(Stat.CON, 10)
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
