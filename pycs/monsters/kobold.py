""" https://www.dndbeyond.com/monsters/kobold"""
import colors
from pycs.effect import Effect
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Kobold(Monster):
    """Kobold"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d6-2"
        kwargs.update(
            {
                "ac": 12,
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 7,
                "dex": 15,
                "con": 9,
                "int": 8,
                "wis": 7,
                "cha": 8,
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Dagger",
                reach=5,
                dmg=("1d4", 0),
                use_stat=Stat.DEX,
                dmg_type=DamageType.PIERCING,
            )
        )

        self.add_action(
            RangedAttack(
                "Sling",
                s_range=30,
                l_range=120,
                dmg=("1d4", 0),
                use_stat=Stat.DEX,
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_effect(PackTactics())

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("k")
        return colors.green("k", bg="red")


##############################################################################
##############################################################################
##############################################################################
class PackTactics(Effect):
    """Pack Tactics. The kobold has advantage on an attack roll against
    a creature if at least one of the kobold's allies is within 5 feet
    of the creature and the ally isn't incapacitated"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Pack Tactics", **kwargs)

    ##########################################################################
    def hook_gives_advantage(self, target):
        """Do pack tactics apply?"""
        allies = [_ for _ in target.pick_closest_enemy() if _ != self.source]
        if allies:
            if allies[0].distance(target) <= 1:
                return True
        return False


# EOF