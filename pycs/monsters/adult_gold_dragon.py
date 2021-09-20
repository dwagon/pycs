""" https://www.dndbeyond.com/monsters/adult-gold-dragon"""
from collections import namedtuple
import colors
import dice
from pycs.action import Action
from pycs.attack import Attack
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import Condition
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.monster import Monster


##############################################################################
class AdultGoldDragon(Monster):
    """Adult Gold Dragon"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.immune_fp = set()
        self.breath = True
        kwargs.update(
            {
                "hitdice": "19d12+133",
                "prof_bonus": 6,
                "ac": 19,
                "stat_prof": [Stat.DEX, Stat.CON, Stat.WIS, Stat.CHA],
                "speed": 40,
                "type": MonsterType.UNDEAD,
                "str": 27,
                "dex": 14,
                "con": 25,
                "int": 16,
                "wis": 15,
                "cha": 24,
                "immunity": [DamageType.FIRE],
                "actions": [DragonMultiAttack(), DragonFireBreath()],
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
class FrightfulPresenceAttack(Attack):
    """Use Fightful Presence"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Frightful Presence", **kwargs)

    ##########################################################################
    def heuristic(self):
        """Do the attack"""
        return 1

    ##########################################################################
    def modifier(self, _):
        """Attack modifier"""
        return 0

    ##########################################################################
    def perform_action(self):
        """Do the action"""
        for enemy in self.owner.pick_closest_enemy():
            if enemy in self.owner.immune_fp:
                continue
            if self.owner.distance(enemy) < 120 / 5:
                continue
            self.owner.immune_fp.add(enemy)
            svth = enemy.saving_throw(Stat.WIS, 21)
            if not svth:
                enemy.add_effect(FrightfulPresenceEffect())


##############################################################################
##############################################################################
##############################################################################
class FrightfulPresenceEffect(Effect):
    """Each creature of the dragon's choice that is within 120 feet of the
    dragon and aware of it must succeed on a DC 21 Wisdom saving throw
    or become frightened for 1 minute. A creature can repeat the saving
    throw at the end of each of its turns, ending the effect on itself
    on a success. If a creature's saving throw is successful or the
    effect ends for it, the creature is immune to the dragon's Frightful
    Presence for the next 24 hours."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Frightful Presence", **kwargs)

    ##########################################################################
    def initial(self, target):
        """Have the effect"""
        target.add_condition(Condition.FRIGHTENED)

    ##########################################################################
    def finish(self, victim):
        """Remove the effect"""
        victim.remove_condition(Condition.FRIGHTENED)

    ##########################################################################
    def removal_end_of_its_turn(self, victim):
        """Does the victim save"""
        svth = victim.saving_throw(Stat.WIS, 21)
        if svth:
            return True
        return False


##############################################################################
##############################################################################
##############################################################################
class DragonFireBreath(Attack):
    """The dragon exhales fire in a 60-foot cone. Each creature in that
    area must make a DC 21 Dexterity saving throw, taking 66 (12d10)
    fire damage on a failed save, or half as much damage on a successful
    one."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Fire Breath", **kwargs)

    ##########################################################################
    def atk_modifier(self, attacker):
        return 0

    ##########################################################################
    def heuristic(self):
        """Should we do this attack"""
        target = self.pick_target()
        if not target:
            return 0
        return min(target.hp, 66)

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
        dmg = int(dice.roll("12d10"))
        svth = target.saving_throw(Stat.DEX, 21)
        if not svth:
            target.hit(dmg, DamageType.FIRE, self.owner, False, "Fire Breath")
        else:
            target.hit(dmg / 2, DamageType.FIRE, self.owner, False, "Fire Breath")
        self.owner.breath = False


##############################################################################
##############################################################################
##############################################################################
class DragonMultiAttack(Action):
    """The dragon can use its Frightful Presence. It then makes
    three attacks: one with its bite and two with its claws."""

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
        fright = FrightfulPresenceAttack(owner=self.owner)
        fright.perform_action()
        bite.do_attack()
        claw.do_attack()
        claw.do_attack()


# EOF
