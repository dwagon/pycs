""" Handle Attacks """
import dice
from pycs.action import Action
from pycs.constant import ActionType
from pycs.constant import Stat


##############################################################################
##############################################################################
##############################################################################
class Attack(Action):
    """generic attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        self.use_stat = None
        super().__init__(name, **kwargs)

    ########################################################################
    def perform_action(self, source):
        """Do the attack"""
        response = False
        apa = source.attacks_per_action
        if isinstance(self.attacks_per_action, tuple):
            apa *= (
                int(dice.roll(self.attacks_per_action[0])) + self.attacks_per_action[1]
            )
        elif isinstance(self.attacks_per_action, int):
            apa = source.attacks_per_action
        if apa != 1:
            print(f"Doing {apa} attacks")
        for _ in range(apa):
            success = self.do_attack(source)
            if success:
                response = True
        return response

    ########################################################################
    def modifier(self, attacker):
        raise NotImplementedError(f"Attack.{__class__.__name__} needs modifier()")

    ########################################################################
    def stat_dmg_bonus(self, attacker):  # pylint: disable=no-self-use
        """The damage bonus modifier"""
        if self.damage_modifier:
            return self.damage_modifier
        bonus = 0
        if self.gear:
            bonus = self.gear.magic_bonus
        bonus += attacker.stat_bonus(self.use_stat)
        return bonus


##############################################################################
##############################################################################
##############################################################################
class MeleeAttack(Attack):
    """A melee attack"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.reach = int(kwargs.get("reach", 5) / 5)
        self.use_stat = kwargs.get("use_stat", Stat.STR)
        self.type = ActionType.MELEE

    ########################################################################
    def range(self):
        """Return the range of the attack"""
        return self.reach, self.reach

    ########################################################################
    def modifier(self, attacker):  # pylint: disable=no-self-use
        """The melee attack modifier"""
        if self.attack_modifier:
            return self.attack_modifier
        return attacker.prof_bonus + attacker.stat_bonus(self.use_stat)

    ########################################################################
    def is_available(self, owner):
        """Is this action available?"""
        return self.available

    ########################################################################
    def heuristic(self, doer):
        """Should we perform this attack - yes if adjacent"""
        enemy = doer.pick_closest_enemy()
        if not enemy:
            return 0
        if doer.distance(enemy[0]) <= 1:
            return self.max_dmg(doer)
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
        self.use_stat = kwargs.get("use_stat", Stat.DEX)
        self.type = ActionType.RANGED

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
        return self.max_dmg(doer)

    ########################################################################
    def modifier(self, attacker):  # pylint: disable=no-self-use
        """The ranged attack modifier"""
        if self.attack_modifier:
            return self.attack_modifier
        return attacker.prof_bonus + attacker.stat_bonus(self.use_stat)

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
