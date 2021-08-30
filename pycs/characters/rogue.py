""" https://www.dndbeyond.com/classes/rogue """
import colors
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import Race
from pycs.constant import Stat


##############################################################################
##############################################################################
##############################################################################
class Rogue(Character):
    """Rogue class"""

    def __init__(self, level=1, **kwargs):
        self.level = level
        kwargs.update(
            {
                "race": Race.ELF,
                "str": 12,
                "dex": 17,
                "con": 13,
                "int": 9,
                "wis": 14,
                "cha": 10,
                "ac": 14,
                "speed": 35,
            }
        )
        if level >= 1:
            kwargs["hp"] = 9
        if level >= 2:
            kwargs["hp"] = 15
        if level >= 3:
            kwargs["hp"] = 21
        if level >= 4:
            kwargs["hp"] = 31
            kwargs["dex"] = 18
            kwargs["con"] = 14
        if level >= 5:
            kwargs["hp"] = 38

        super().__init__(**kwargs)

        if level >= 2:
            pass
            # Sneak Attack
        if level >= 3:
            # Cunning Action
            # Rogueish Archetype
            pass
        if level >= 4:
            pass
        if level >= 5:
            self.add_action(UncannyDodge())
            pass

        self.add_action(
            MeleeAttack(
                "Shortsword",
                reach=5,
                dmg=("1d6", 0),
                use_stat=Stat.DEX,
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_action(
            RangedAttack(
                "Longbow",
                s_range=150,
                l_range=600,
                dmg=("1d8", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def shortrepr(self):
        """What a rogue looks like in the arena"""
        if self.is_alive():
            return colors.black("R", bg="green")
        return colors.blue("R", bg="red")


##############################################################################
##############################################################################
##############################################################################
class UncannyDodge(Action):
    """When an attacker that you can see hits you with an attack,
    you can use your reaction to halve the attack’s damage against
    you."""

    ##########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Uncanny Dodge", **kwargs)
        self.category = ActionCategory.REACTION

    ##########################################################################
    def hook_predmg(self, **kwargs):
        """Half damage"""
        print("Using uncanny dodge to reduce damage")
        return int(kwargs.get("dmg") / 2)


# EOF
