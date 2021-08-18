""" Handle Attacks """
from actions import Action
from constants import ActionType
from constants import Stat


##############################################################################
##############################################################################
##############################################################################
class Attack(Action):
    """generic attack"""

    ########################################################################
    def perform_action(self, source):
        """Do the attack"""
        return self.do_attack(source)

    ########################################################################
    def modifier(self, attacker):
        raise NotImplementedError(f"Attack.{__class__.__name__} needs modifier()")


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
    def modifier(self, attacker):  # pylint: disable=no-self-use
        """The melee attack modifier"""
        return attacker.prof_bonus + attacker.stat_bonus(Stat.STR)

    ########################################################################
    def dmg_bonus(self, attacker):  # pylint: disable=no-self-use
        """The melee damage bonus modifier"""
        return attacker.stat_bonus(Stat.STR)

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return self.available

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to hit"""
        enemy = doer.pick_closest_enemy()[0]
        return enemy

    ########################################################################
    def heuristic(self, doer):
        """Should we perform this attack - yes if adjacent"""
        enemy = doer.pick_closest_enemy()
        if not enemy:
            return 0
        if doer.distance(enemy[0]) <= 1:
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
            if self.ammo <= 0:
                print(f"{source} {self} has run out of ammo")
                self.available = False

        return super().perform_action(source)

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to hit"""
        enemy = doer.pick_closest_enemy()[0]
        return enemy

    ########################################################################
    def heuristic(self, doer):
        """Should we perform this attack - no if adjacent,
        yes if in range, middling if at long range"""
        enemy = doer.pick_closest_enemy()
        if not enemy:
            return 0
        if not self.available:
            return 0
        dist = doer.distance(enemy[0])
        if dist <= 1:
            return 0
        if dist < self.l_range:
            return 1
        if dist < self.s_range:
            return 2
        return 0

    ########################################################################
    def modifier(self, attacker):  # pylint: disable=no-self-use
        """The melee attack modifier"""
        return attacker.prof_bonus + attacker.stat_bonus(Stat.DEX)

    ########################################################################
    def dmg_bonus(self, attacker):  # pylint: disable=no-self-use
        """The melee damage bonus modifier"""
        return attacker.stat_bonus(Stat.DEX)

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


# EOF
