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

    ########################################################################
    def max_dmg(self):
        """What is the most damage this attack can do"""
        return dice.roll_max(self.dmg)

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
        self.s_range = int(kwargs.get("range", 999) / 5)

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.range, self.range


# EOF
