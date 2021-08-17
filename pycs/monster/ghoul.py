""" Ghoul Monster Class """
import colors
from attacks import MeleeAttack
from constants import DamageType
from constants import Condition
from constants import Stat
from constants import MonsterType
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
                "type": MonsterType.UNDEAD,
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
                heuristic=self.ghoul_bite,
                dmg=("2d6", 2),
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_action(
            MeleeAttack(
                "Claw",
                reach=5,
                dmg=("2d4", 2),
                heuristic=self.ghoul_claw,
                dmg_type=DamageType.SLASHING,
                side_effect=self.se_ghoul_claws,
            )
        )

    ##########################################################################
    def ghoul_bite(self, actor):  # pylint: disable=unused-argument
        """When is Ghoul bite good"""
        if self.target.has_condition(Condition.PARALYZED):
            return 2
        return 1

    ##########################################################################
    def ghoul_claw(self, actor):  # pylint: disable=unused-argument
        """When is Ghoul claw good"""
        if not self.target.has_condition(Condition.PARALYZED):
            return 2
        return 1

    ##########################################################################
    def se_ghoul_claws(self, source):  # pylint: disable=unused-argument
        """Side effect of ghoul claws"""
        target = self.target
        svth = target.saving_throw(Stat.CON, 10)
        if not svth:
            print(f"{target} got paralysed by {self}")
            target.add_condition(Condition.PARALYZED)
        else:
            print(f"{target} resisted Ghoul claws")

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("G", style="bold")
        return colors.green("G", bg="red", style="bold")


# EOF
