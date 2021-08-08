""" Handle Attacks """
import dice


##############################################################################
##############################################################################
##############################################################################
class Attack:
    """generic attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        self.name = name
        self.dmg = kwargs.get("dmg", "")
        self.bonus = kwargs.get("bonus", "")

    ########################################################################
    def range(self):
        """Return the range (good, max) of the attack"""
        return 0, 0

    ##########################################################################
    def is_available(self, owner):  # pylint: disable=unused-argument
        """Is this attack currently available to the creature"""
        return True

    ##########################################################################
    def post_attack_hook(self, source, target):
        """Post attack hook"""

    ##########################################################################
    def roll_to_hit(self, rnge):
        """Roll to hit with the attack"""
        crit = False
        if self.has_disadvantage(rnge):
            to_hit_roll = min(int(dice.roll("d20")), int(dice.roll("d20")))
        else:
            to_hit_roll = int(dice.roll("d20"))
        if to_hit_roll == 20:
            crit = True
        to_hit = to_hit_roll + self.bonus
        print(f"{self} rolled {to_hit_roll} (critical: {crit}): {to_hit}")
        return int(to_hit), crit

    ########################################################################
    def max_dmg(self):
        """What is the most damage this attack can do"""
        return int(dice.roll_max(self.dmg[0])) + self.dmg[1]

    ########################################################################
    def perform_attack(self, source, target, rnge):
        """Do the attack"""
        to_hit, crit = self.roll_to_hit(rnge)
        if to_hit > target.ac:
            dmg = self.roll_dmg(target, crit)
            print(f"{source} hit {target} with {self} for {dmg} hp damage")
            target.hit(dmg, source)
        else:
            print(f"{source} missed {target} with {self}")
        self.post_attack_hook(source, target)

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
        return dmg

    ########################################################################
    def __repr__(self):
        return f"{self.__class__.__name__} {self.name}"

    ########################################################################
    def has_disadvantage(self, rnge):  # pylint: disable=unused-argument
        """Does this attack have disadvantage at this range"""
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

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.s_range, self.l_range

    ########################################################################
    def has_disadvantage(self, rnge):
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
        else:
            saved = victim.saving_throw(stat=self.save[0], dc=self.save[1])
            dmg = int(dice.roll(self.dmg[0])) + self.dmg[1]
            if saved:
                dmg = int(dmg / 2)
            return dmg

    ########################################################################
    def roll_to_hit(self, rnge):
        """Special spell attack"""
        assert self.style in ("tohit", "save")
        if self.style == "tohit":
            return super().roll_to_hit(rnge)
        else:
            return 999, False

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
        return owner.spell_available(self)


# EOF
