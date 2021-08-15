""" Handle Attacks """
import dice
from constants import DamageType
from constants import Condition
from constants import ActionType
from actions import Action


##############################################################################
##############################################################################
##############################################################################
class Attack(Action):
    """generic attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.dmg = kwargs.get("dmg", "")
        self.bonus = kwargs.get("bonus", "")
        self.dmg_type = kwargs.get("dmg_type", DamageType.PIERCING)

    ##########################################################################
    def post_attack_hook(self, source):
        """Post attack hook"""
        if self.side_effect is not None:
            self.side_effect(source)

    ##########################################################################
    def roll_to_hit(self, source, target, rnge):
        """Roll to hit with the attack"""
        crit_hit = False
        crit_miss = False
        balance = 0
        if self.has_disadvantage(source, target, rnge):
            balance -= 1
        elif self.has_advantage(source, target, rnge):
            balance += 1

        if balance < 0:
            to_hit_roll = min(int(dice.roll("d20")), int(dice.roll("d20")))
            msg_0 = "with disadvantage"
        elif balance > 0:
            to_hit_roll = max(int(dice.roll("d20")), int(dice.roll("d20")))
            msg_0 = "with advantage"
        else:
            to_hit_roll = int(dice.roll("d20"))
            msg_0 = ""

        if to_hit_roll == 20:
            crit_hit = True
        if to_hit_roll == 1:
            crit_miss = True
        to_hit = to_hit_roll + self.bonus
        for eff in source.effects.values():
            to_hit += eff.hook_attack_to_hit(target, rnge)['bonus']
        msg = f"{source} rolled {to_hit_roll} {msg_0}"
        if crit_hit:
            msg += " (critical hit)"
        elif crit_miss:
            msg += " (critical miss)"
        else:
            msg += f" = {to_hit}"
        print(msg)
        return int(to_hit), crit_hit, crit_miss

    ########################################################################
    def max_dmg(self, victim):
        """What is the most damage this attack can do"""
        dmg = int(dice.roll_max(self.dmg[0])) + self.dmg[1]
        if self.dmg_type in victim.vulnerable:
            dmg *= 2
        if self.dmg_type in victim.immunity:
            dmg = 0
        return dmg

    ########################################################################
    def perform_action(self, source):
        """Do the attack"""
        target = source.target
        rnge = source.distance(target)
        if rnge > self.range()[1]:
            print(f"{target} is out of range")
            return False
        to_hit, crit_hit, crit_miss = self.roll_to_hit(source, target, rnge)
        print(
            f"{source} attacking {target} @ {target.coords} with {self} (Range: {rnge})"
        )
        if to_hit > target.ac and not crit_miss:
            dmg = self.roll_dmg(target, crit_hit)
            print(
                f"{source} hit {target} with {self} for {dmg} hp {self.dmg_type.value} damage"
            )
            target.hit(dmg, self.dmg_type, source, crit_hit)
            source.statistics.append((self.name, dmg, self.dmg_type, crit_hit))
            self.post_attack_hook(source)
        else:
            source.statistics.append((self.name, 0, False, False))
            print(f"{source} missed {target} with {self}")
        return True

    ########################################################################
    def roll_dmg(self, victim, critical=False):  # pylint: disable=unused-argument
        """Roll the damage of the attack"""
        if critical:
            dmg = (
                int(dice.roll_max(self.dmg[0]))
                + int(dice.roll(self.dmg[0]))
                + self.dmg[1]
            )
        else:
            dmg = int(dice.roll(self.dmg[0])) + self.dmg[1]
        if self.dmg_type in victim.vulnerable:
            print(f"{self} is vulnerable to {self.dmg_type.value}")
            dmg *= 2
        if self.dmg_type in victim.immunity:
            print(f"{self} is immune to {self.dmg_type.value}")
            dmg = 0
        return dmg

    ########################################################################
    def has_disadvantage(self, source, target, rnge):  # pylint: disable=unused-argument
        """Does this attack have disadvantage at this range"""
        if source.has_condition(Condition.POISONED):
            return True
        return False

    ########################################################################
    def has_advantage(self, source, target, rnge):  # pylint: disable=unused-argument
        """Does this attack have advantage at this range"""
        if target.has_condition(Condition.UNCONSCIOUS) and rnge <= 1:
            return True
        return False


##############################################################################
##############################################################################
##############################################################################
class MeleeAttack(Attack):
    """A melee attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.reach = int(kwargs.get("reach", 5) / 5)
        self.type = ActionType.MELEE

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return self.available

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to hit"""
        enemy = doer.pick_closest_enemy()
        return enemy

    ########################################################################
    def heuristic(self, doer):
        """Should we perform this attack - yes if adjacent"""
        enemy = doer.pick_closest_enemy()
        if not enemy:
            return 0
        if doer.distance(enemy) <= 1:
            return 2
        return 0


##############################################################################
##############################################################################
##############################################################################
class RangedAttack(Attack):
    """A ranged attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.s_range = int(kwargs.get("s_range", 999) / 5)
        self.l_range = int(kwargs.get("l_range", 999) / 5)
        self.type = ActionType.RANGED
        self.ammo = kwargs.get("ammo", None)

    ########################################################################
    def perform_action(self, source):
        """Fire the weapon"""
        if self.ammo is not None:
            self.ammo -= 1
            if self.ammo == 0:
                print(f"{source} {self} has run out of ammo")
                self.available = False

        return super().perform_action(source)

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to hit"""
        enemy = doer.pick_closest_enemy()
        return enemy

    ########################################################################
    def heuristic(self, doer):
        """Should we perform this attack - no if adjacent,
        yes if in range, middling if at long range"""
        enemy = doer.pick_closest_enemy()
        if not enemy:
            return 0
        dist = doer.distance(enemy)
        if dist <= 1:
            return 0
        if dist < self.l_range:
            return 1
        if dist < self.s_range:
            return 2
        return 0

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.s_range, self.l_range

    ########################################################################
    def has_disadvantage(self, source, target, rnge):
        """Does this attack have disadvantage at this range"""
        if rnge == 1:
            return True
        if rnge > self.s_range:
            return True
        return False


##############################################################################
##############################################################################
##############################################################################
class SpellAttack(Attack):
    """A spell attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.reach = int(kwargs.get("reach", 5) / 5)
        self.level = kwargs.get("level", 99)
        # Style is tohit or save;
        #   "tohit" you need to roll to hit,
        #   "save" you hit automatically but save on damage
        self.style = kwargs.get("style", "tohit")
        self.type = kwargs.get("type")
        self.save = kwargs.get("save", ("none", 999))

    ########################################################################
    def roll_dmg(self, victim, critical=False):
        """Special spell damage"""
        if self.style == "tohit":
            return super().roll_dmg(victim, critical)
        saved = victim.saving_throw(stat=self.save[0], dc=self.save[1])
        dmg = int(dice.roll(self.dmg[0])) + self.dmg[1]
        if saved:
            dmg = int(dmg / 2)
        return dmg

    ########################################################################
    def pick_target(self, doer):
        """Who should we target"""
        return doer.pick_closest_enemy()

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        if not doer.spell_available(self):
            return 0
        return 2

    ########################################################################
    def roll_to_hit(self, source, target, rnge):
        """Special spell attack"""
        assert self.style in ("tohit", "save")
        if self.style == "tohit":
            return super().roll_to_hit(source, target, rnge)
        return 999, False, False

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def post_attack_hook(self, source):
        """Tell the caster they have cast the spell"""
        pass

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return owner.spell_available(self)


# EOF
