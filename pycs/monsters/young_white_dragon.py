""" https://www.dndbeyond.com/monsters/young-white-dragon"""
from collections import namedtuple
import colors
import dice
from pycs.action import Action
from pycs.attack import Attack
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.monster import Monster


##############################################################################
class YoungWhiteDragon(Monster):
    """Young White Dragon"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.immune_fp = set()
        self.breath = True
        kwargs.update(
            {
                "hitdice": "14d10+56",
                "prof_bonus": 3,
                "ac": 17,
                "stat_prof": [Stat.DEX, Stat.CON, Stat.WIS, Stat.CHA],
                "speed": 40,
                "type": MonsterType.DRAGON,
                "str": 18,
                "dex": 10,
                "con": 18,
                "int": 6,
                "wis": 11,
                "cha": 12,
                "immunity": [DamageType.COLD],
                "actions": [DragonMultiAttack(), DragonBreath()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def hook_start_turn(self):
        """Recharge breath weapon on 5/6"""
        if not self.breath:
            if int(dice.roll("d6")) in (5, 6):
                print(f"{self} regains breath weapon")
                self.breath = True

    ##########################################################################
    def report(self):
        """Creature Report"""
        super().report()
        print(f"|  Breath Weapon: {self.breath}")

    ##########################################################################
    def shortrepr(self):
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.blue("D", bg="yellow")
        return colors.blue("D", bg="red")


##############################################################################
##############################################################################
##############################################################################
class DragonBreath(Attack):
    """Cold Breath (Recharge 5–6). The dragon exhales an icy blast
    in a 30-foot cone. Each creature in that area must make a DC
    15 Constitution saving throw, taking 45 (10d8) cold damage on
    a failed save, or half as much damage on a successful one."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Cold Breath", **kwargs)

    ##########################################################################
    def atk_modifier(self, attacker):
        return 0

    ##########################################################################
    def heuristic(self):
        """Should we do this attack"""
        target = self.pick_target()
        if not target:
            return 0
        return min(target.hp, 45)

    ##########################################################################
    def is_available(self):
        """Is breath weapon available"""
        return self.owner.breath

    ##########################################################################
    def pick_target(self):
        """Pick on the strongest enemy"""
        result = namedtuple("Result", "health id target")
        targets = [
            result(_.hp, id(_), _)
            for _ in self.owner.pick_closest_enemy()
            if self.owner.distance(_) < 60 / 5 and DamageType.FIRE not in _.immunity
        ]
        if not targets:
            return None
        targets.sort()
        return targets[-1].target

    ##########################################################################
    def perform_action(self):
        """Do the breath weapon - need to do cone"""
        target = self.pick_target()
        dmg = int(dice.roll("10d8"))
        svth = target.saving_throw(Stat.CON, 15)
        if not svth:
            target.hit(dmg, DamageType.COLD, self.owner, False, "Cold Breath")
        else:
            target.hit(dmg / 2, DamageType.COLD, self.owner, False, "Cold Breath")
        self.owner.breath = False


##############################################################################
##############################################################################
##############################################################################
class DragonMultiAttack(Action):
    """Multiattack. The dragon makes three attacks: one with its
    bite and two with its claws."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the attack"""
        return 1

    ##########################################################################
    def perform_action(self):
        """Do the attack"""
        bite = MeleeAttack(
            "Bite",
            reach=10,
            dmg=("2d10", 0),
            dmg_type=DamageType.PIERCING,
            owner=self.owner,
        )
        claw = MeleeAttack(
            "Claw",
            reach=10,
            dmg=("2d6", 0),
            dmg_type=DamageType.PIERCING,
            owner=self.owner,
        )
        bite.do_attack()
        claw.do_attack()
        claw.do_attack()


# EOF
