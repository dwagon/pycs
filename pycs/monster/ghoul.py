""" Ghoul Monster Class """
import colors
from pycs.effect import Effect
from pycs.attacks import MeleeAttack
from pycs.constants import DamageType
from pycs.constants import Condition
from pycs.constants import Stat
from pycs.constants import MonsterType
from pycs.monsters import Monster


##############################################################################
##############################################################################
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
                dmg=("2d6", 0),
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_action(
            MeleeAttack(
                "Claw",
                reach=5,
                dmg=("2d4", 0),
                heuristic=self.ghoul_claw,
                dmg_type=DamageType.SLASHING,
                side_effect=self.se_ghoul_claws,
            )
        )

    ##########################################################################
    def se_ghoul_claws(self, source, target, dmg):  # pylint: disable=unused-argument
        """Implement Side Effect of Ghoul Claws"""
        svth = target.saving_throw(Stat.CON, 10)
        if not svth:
            print(f"{target} got paralysed by {source}")
            target.add_effect(GhoulClawEffect())
        else:
            print(f"{target} resisted Ghoul claws")

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
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("G", style="bold")
        return colors.green("G", bg="red", style="bold")


##############################################################################
##############################################################################
##############################################################################
class GhoulClawEffect(Effect):
    """If the target is a creature other than an elf or undead, it must
    succeed on a DC 10 Constitution saving throw or be paralyzed for 1
    minute. The target can repeat the saving throw at the end of each
    of its turns, ending the effect on itself on a success."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Ghoul Claws", **kwargs)

    ##########################################################################
    def initial(self, target):
        """First effect"""
        target.add_condition(Condition.PARALYZED)

    ##########################################################################
    def removal_end_of_its_turn(self, victim):
        """Do we rmove the effect"""
        svth = victim.saving_throw(Stat.CON, 10)
        if svth:
            print(f"{victim} resisted Ghoul claws")
            return True
        return False


# EOF
