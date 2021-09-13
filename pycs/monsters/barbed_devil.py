""" https://www.dndbeyond.com/monsters/barbed-devil"""
# TO DO: Implement Magic Reistance
# TO DO: Implement Barbed Hide
import colors
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
class BarbedDevil(Monster):
    """Barbed Devil"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "13d8+52"
        kwargs.update(
            {
                "ac": 15,
                "speed": 30,
                "type": MonsterType.FIEND,
                "str": 16,
                "dex": 17,
                "con": 18,
                "int": 12,
                "wis": 14,
                "cha": 14,
                "prof_bonus": 3,
                "resistant": [
                    DamageType.COLD,
                    DamageType.BLUDGEONING,
                    DamageType.PIERCING,
                    DamageType.SLASHING,
                ],
                "immunity": [DamageType.FIRE, DamageType.POISON],
                "cond_immunity": [Condition.POISONED],
                "actions": [BDMeleeAttack(), BDRangedAttack()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("D")
        return colors.green("D", bg="red")


##############################################################################
##############################################################################
##############################################################################
class BDMeleeAttack(MeleeAttack):
    """Handle a multi attack of Tail, Claw, Claw"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Tail / Claw combo", **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the action"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 10
        return 0

    ##########################################################################
    def pick_target(self):
        """Who we should do the action against"""
        enemy = self.owner.pick_closest_enemy()
        if not enemy:
            return None
        return enemy[0]

    ##########################################################################
    def perform_action(self):
        """Do the attack"""
        tail = MeleeAttack(
            "Tail", dmg=("2d6", 0), dmg_type=DamageType.PIERCING, owner=self.owner
        )
        claw1 = MeleeAttack(
            "Claw", dmg=("1d6", 0), dmg_type=DamageType.PIERCING, owner=self.owner
        )
        claw2 = MeleeAttack(
            "Claw", dmg=("1d6", 0), dmg_type=DamageType.PIERCING, owner=self.owner
        )
        tail.do_attack()
        claw1.do_attack()
        claw2.do_attack()


##############################################################################
##############################################################################
##############################################################################
class BDRangedAttack(RangedAttack):
    """Handle a multi attack of hurl flame twice"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Hurl Flame", **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the action"""
        enemy = self.owner.pick_closest_enemy()
        if not enemy:
            return 0
        if self.owner.distance(enemy[0]) <= 1:
            return 0
        return 10

    ##########################################################################
    def pick_target(self):
        """Who we should attack"""
        enemy = self.owner.pick_closest_enemy()
        if not enemy:
            return None
        return enemy[0]

    ##########################################################################
    def perform_action(self):
        """Do the attack"""
        flame = RangedAttack(
            "Hurl Flame",
            dmg=("3d6", 0),
            s_range=150,
            l_range=150,
            dmg_type=DamageType.FIRE,
            owner=self.owner,
        )
        flame.do_attack()
        flame.do_attack()


# EOF
