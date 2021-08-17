""" Handle non-attack Actions """
import dice
from constants import ActionType
from constants import Condition
from constants import DamageType


##############################################################################
##############################################################################
##############################################################################
class Action:
    """generic action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        self.name = name
        self.available = True
        self.type = ActionType.UNKNOWN
        self.side_effect = kwargs.get("side_effect", self.no_side_effect)
        self.dmg = kwargs.get("dmg", "")
        self.dmg_type = kwargs.get("dmg_type", DamageType.PIERCING)

    ########################################################################
    def modifier(self, attacker):
        """Modifier to the action dice roll"""
        raise NotImplementedError(f"{__class__.__name__} hasn't implemented modifier()")

    ########################################################################
    def no_side_effect(self, source):
        """No side_effect"""

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to do the action to"""
        print(f"{self.__class__.__name__}.pick_target({doer=}) - needs to be replaced")

    ########################################################################
    def heuristic(self, doer):  # pylint: disable=unused-argument, no-self-use
        """How good is this action for doer this turn
        0 - don't do
        1 - whatevs
        ..
        5 - zOMG!
        """
        return 1

    ########################################################################
    def range(self):  # pylint: disable=no-self-use
        """Return the range (good, max) of the action"""
        return 0, 0

    ##########################################################################
    def is_available(self, owner):  # pylint: disable=unused-argument, no-self-use
        """Is this action currently available to the creature"""
        return True

    ########################################################################
    def perform_action(self, source):  # pylint: disable=unused-argument
        """Perform the action"""

    ########################################################################
    def __repr__(self):
        return self.name

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
            msg_0 = " with disadvantage"
        elif balance > 0:
            to_hit_roll = max(int(dice.roll("d20")), int(dice.roll("d20")))
            msg_0 = " with advantage"
        else:
            to_hit_roll = int(dice.roll("d20"))
            msg_0 = ""
        msg = f"{source} rolled {to_hit_roll}{msg_0}"

        if to_hit_roll == 20:
            crit_hit = True
        if to_hit_roll == 1:
            crit_miss = True
        modifier = self.modifier(source)
        msg += f" +{self.modifier(source)}"
        to_hit = to_hit_roll + modifier
        for name, eff in source.effects.items():
            mod = eff.hook_attack_to_hit(target, rnge)["bonus"]
            to_hit += mod
            msg += f" +{mod} from {name}"
        if crit_hit:
            msg += " (critical hit)"
        elif crit_miss:
            msg += " (critical miss)"
        else:
            msg += f" = {to_hit}"
        print(msg)
        return int(to_hit), crit_hit, crit_miss

    ########################################################################
    def do_attack(self, source):
        """Do the attack from {source}"""
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
            self.side_effect(source)
            source.statistics.append((self.name, dmg, self.dmg_type, crit_hit))
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
    def max_dmg(self, victim):
        """What is the most damage this attack can do"""
        dmg = int(dice.roll_max(self.dmg[0])) + self.dmg[1]
        if self.dmg_type in victim.vulnerable:
            dmg *= 2
        if self.dmg_type in victim.immunity:
            dmg = 0
        return dmg

    ########################################################################
    def has_disadvantage(
        self, source, target, rnge
    ):  # pylint: disable=unused-argument, no-self-use
        """Does this attack have disadvantage at this range"""
        if source.has_condition(Condition.POISONED):
            return True
        return False

    ########################################################################
    def has_advantage(
        self, source, target, rnge
    ):  # pylint: disable=unused-argument, no-self-use
        """Does this attack have advantage at this range"""
        if target.has_condition(Condition.UNCONSCIOUS) and rnge <= 1:
            return True
        return False


# EOF
