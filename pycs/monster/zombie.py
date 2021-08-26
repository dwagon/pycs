""" Zombie Monster Class """
import colors
from pycs.attacks import MeleeAttack
from pycs.constants import DamageType
from pycs.constants import Stat
from pycs.constants import MonsterType
from pycs.monsters import Monster


##############################################################################
class Zombie(Monster):
    """Zombie - https://www.dndbeyond.com/monsters/zombie"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "3d8+9"
        kwargs.update(
            {
                "ac": 8,
                "speed": 20,
                "type": MonsterType.UNDEAD,
                "str": 13,
                "dex": 6,
                "con": 16,
                "int": 3,
                "wis": 6,
                "cha": 5,
                "immunity": [DamageType.POISON],
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Slam",
                reach=5,
                dmg=("1d6", 0),
                dmg_type=DamageType.BLUDGEONING,
            )
        )

    ##########################################################################
    def fallen_unconscious(self, dmg, dmg_type, critical):
        """Undead Fortitude. If damage reduces the zombie to 0 hit points,
        it must make a Constitution saving throw with a DC of 5 + the damage
        taken, unless the damage is radiant or from a critical hit.
        On a success, the zombie drops to 1 hit point instead."""
        if not critical and dmg_type != DamageType.RADIANT:
            save = self.saving_throw(Stat.CON, 5 + dmg)
            if save:
                self.hp = 1
                print(f"{self} uses Undead Fortitude and stays conscious")
                return
        super().fallen_unconscious(dmg, dmg_type, critical)

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.red("Z", bg="green")
        return colors.green("Z", bg="red")


# EOF
