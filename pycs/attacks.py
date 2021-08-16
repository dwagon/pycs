""" Handle Attacks """
import dice
from constants import ActionType
from actions import Action


##############################################################################
##############################################################################
##############################################################################
class Attack(Action):
    """generic attack"""

    ##########################################################################
    def post_attack_hook(self, source):
        """Post attack hook"""
        if self.side_effect is not None:
            self.side_effect(source)

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


# EOF
