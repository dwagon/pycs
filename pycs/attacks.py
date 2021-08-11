""" Handle Attacks """
import dice
from constants import DamageType
from constants import Condition
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
        self.available = True
        self.dmg_type = kwargs.get("dmg_type", DamageType.PIERCING)

    ##########################################################################
    def post_attack_hook(self, source, target):  # pylint: disable=unused-argument
        """Post attack hook"""
        if self.side_effect is not None:
            self.side_effect(target)

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
        elif balance > 0:
            to_hit_roll = max(int(dice.roll("d20")), int(dice.roll("d20")))
        else:
            to_hit_roll = int(dice.roll("d20"))

        if to_hit_roll == 20:
            crit_hit = True
        if to_hit_roll == 1:
            crit_miss = True
        to_hit = to_hit_roll + self.bonus
        msg = f"{self} rolled {to_hit_roll} = {to_hit}"
        if crit_hit:
            msg += " (critical hit)"
        if crit_miss:
            msg += " (critical miss)"
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
    def perform_action(self, source, target, rnge):
        """Do the attack"""
        to_hit, crit_hit, crit_miss = self.roll_to_hit(source, target, rnge)
        if to_hit > target.ac and not crit_miss:
            dmg = self.roll_dmg(target, crit_hit)
            print(
                f"{source} hit {target} with {self} for {dmg} hp {self.dmg_type.value} damage"
            )
            target.hit(dmg, self.dmg_type, source, crit_hit)
            source.statistics.append((self.name, dmg, self.dmg_type, crit_hit))
            self.post_attack_hook(source, target)
        else:
            source.statistics.append((self.name, 0, False, False))
            print(f"{source} missed {target} with {self}")

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

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return self.available


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
        self.ammo = kwargs.get("ammo", None)

    ########################################################################
    def perform_action(self, source, target, rnge):
        """Fire the weapon"""
        if self.ammo is not None:
            self.ammo -= 1
            if self.ammo == 0:
                print(f"{source} {self} has run out of ammo")
                self.available = False

        super().perform_action(source, target, rnge)

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
    def post_attack_hook(self, source, target):
        """Tell the caster they have cast the spell"""
        source.cast(self)

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return owner.spell_available(self)


# EOF
