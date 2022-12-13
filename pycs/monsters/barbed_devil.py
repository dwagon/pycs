""" https://www.dndbeyond.com/monsters/barbed-devil"""
# TO DO: Implement Magic Reistance
# TO DO: Implement Barbed Hide
from typing import Any, Optional
import colors
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.creature import Creature
from pycs.damageroll import DamageRoll
from pycs.monster import Monster


##############################################################################
class BarbedDevil(Monster):
    """Barbed Devil"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "13d8+52",
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
    def shortrepr(self) -> str:
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
    def __init__(self, **kwargs: Any):
        super().__init__("Tail / Claw combo", **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the action"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 10
        return 0

    ##########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who we should do the action against"""
        enemy = self.owner.pick_closest_enemy()
        if not enemy:
            return None
        return enemy[0]

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the attack"""
        tail = MeleeAttack("Tail", dmgroll=DamageRoll("2d6", 0, DamageType.PIERCING), owner=self.owner)
        claw1 = MeleeAttack("Claw", dmgroll=DamageRoll("1d6", 0, DamageType.PIERCING), owner=self.owner)
        claw2 = MeleeAttack("Claw", dmgroll=DamageRoll("1d6", 0, DamageType.PIERCING), owner=self.owner)
        tail.do_attack()
        claw1.do_attack()
        claw2.do_attack()
        return True


##############################################################################
##############################################################################
##############################################################################
class BDRangedAttack(RangedAttack):
    """Handle a multi attack of hurl flame twice"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Hurl Flame", **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the action"""
        enemy = self.owner.pick_closest_enemy()
        if not enemy:
            return 0
        if self.owner.distance(enemy[0]) <= 1:
            return 0
        return 10

    ##########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who we should attack"""
        enemy = self.owner.pick_closest_enemy()
        if not enemy:
            return None
        return enemy[0]

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the attack"""
        flame = RangedAttack(
            "Hurl Flame",
            dmgroll=DamageRoll("3d6", 0, DamageType.FIRE),
            s_range=150,
            l_range=150,
            owner=self.owner,
        )
        flame.do_attack()
        flame.do_attack()
        return True


# EOF
