""" Troll Monster Class """
import colors
from actions import Action
from attacks import MeleeAttack
from constants import DamageType
from constants import MonsterSize
from constants import MonsterType
from .monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Troll(Monster):
    """Troll - https://www.dndbeyond.com/monsters/troll"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "8d10+40"
        kwargs.update(
            {
                "ac": 15,
                "size": MonsterSize.LARGE,
                "speed": 30,
                "type": MonsterType.GIANT,
                "str": 18,
                "dex": 13,
                "con": 20,
                "int": 7,
                "wis": 9,
                "cha": 7,
                "prof_bonus": 3,
            }
        )
        super().__init__(**kwargs)
        self.add_action(TrollMultiAttack())

    ##########################################################################
    def hook_start_turn(self):
        """Regeneration. The troll regains 10 hit points at the start of
        its turn. If the troll takes acid or fire damage, this trait doesn't
        function at the start of the troll's next turn. The troll dies only
        if it starts its turn with 0 hit points and doesn't regenerate."""
        if self.hp < self.max_hp:
            self.heal("", 10)

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("T")
        return colors.green("T", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TrollMultiAttack(Action):
    """Handle a multi attack of Bite, Claw, Claw"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the action"""
        enemy = doer.pick_closest_enemy()
        if enemy and doer.distance(enemy[0]) <= 1:
            return 1
        return 0

    ##########################################################################
    def perform_action(self, source):
        """Do the attack"""
        bite = MeleeAttack("Bite", dmg=("1d6", 0), dmg_type=DamageType.PIERCING)
        claw1 = MeleeAttack("Claw", dmg=("2d6", 0), dmg_type=DamageType.SLASHING)
        claw2 = MeleeAttack("Claw", dmg=("2d6", 0), dmg_type=DamageType.SLASHING)
        bite.do_attack(source)
        claw1.do_attack(source)
        claw2.do_attack(source)


# EOF
