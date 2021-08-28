""" Handle non-attack Actions """
from typing import Tuple
import dice
from pycs.constant import ActionType
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import Statistics


##############################################################################
##############################################################################
##############################################################################
class Action:
    """generic action"""

    ########################################################################
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.available = True
        self.type = ActionType.UNKNOWN
        self.side_effect = kwargs.get("side_effect")
        self.attacks_per_action = kwargs.get("attacks_per_action", 1)
        self.action_cost = kwargs.get("action_cost", 1)
        self.dmg = kwargs.get("dmg", "")
        self.dmg_type = kwargs.get("dmg_type", DamageType.PIERCING)
        self.attack_modifier = kwargs.get("attack_modifier", None)
        self.damage_modifier = kwargs.get("damage_modifier", None)

    ########################################################################
    def modifier(self, attacker):  # pylint: disable=unused-argument
        """Modifier to the action dice roll"""
        # Don't use NotImplementedError as isn't required for every action
        print(f"{__class__.__name__} hasn't implemented modifier()")
        return 0

    ########################################################################
    def dmg_bonus(self, attacker):  # pylint: disable=unused-argument
        """Modifier to the damage bonus"""
        # Don't use NotImplementedError as isn't required for every action
        print(f"{__class__.__name__} hasn't implemented dmg_bonus()")
        return 0

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to do the action to"""
        enemy = doer.pick_closest_enemy()
        if enemy:
            return enemy[0]
        return None

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
    def roll_to_hit(self, source, target, rnge: int) -> Tuple[int, bool, bool]:
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

        if to_hit_roll >= source.critical:
            crit_hit = True
        if to_hit_roll == 1:
            crit_miss = True
        modifier = self.modifier(source)
        msg += f" +{self.modifier(source)}"
        to_hit = to_hit_roll + modifier
        for name, eff in source.effects.items():
            mod = eff.hook_attack_to_hit(target, rnge)["bonus"]
            if mod:
                to_hit += mod
                msg += f" (+{mod} from {name})"
        if crit_hit:
            msg += " (critical hit)"
        elif crit_miss:
            msg += " (critical miss)"
        else:
            msg += f" = {to_hit}"
        print(msg)
        return int(to_hit), crit_hit, crit_miss

    ########################################################################
    def buff_attack_damage(self, source, target) -> None:
        """Calculate the attack damage from buffs"""
        for atkname, eff in source.effects.copy().items():
            if self.type == ActionType.MELEE:
                dice_dmg, dmg, dmg_type = eff.hook_source_additional_melee_damage()
                if dmg_type is None:
                    dmg_type = self.dmg_type
                if dice_dmg:
                    dmg += int(dice.roll(dice_dmg))
                if dmg:
                    target.hit(dmg, dmg_type, source, critical=False, atkname=atkname)

    ########################################################################
    def do_attack(self, source) -> bool:
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
            dmg = self.roll_dmg(source, target, crit_hit)
            target.hit(dmg, self.dmg_type, source, crit_hit, self.name)
            if self.side_effect:
                self.side_effect(source=source, target=target, dmg=dmg)

            # If the source of the damage has a buff
            self.buff_attack_damage(source, target)
            print(
                f"{source} hit {target} (AC: {target.ac})"
                f" with {self} for {dmg} hp {self.dmg_type.value} damage"
            )
        else:
            source.statistics.append(Statistics(self.name, 0, None, False))
            print(f"{source} missed {target} (AC: {target.ac}) with {self}")
        for name, eff in target.effects.copy().items():
            if eff.removal_after_being_attacked():
                print(f"{name} removed from {target}")
                target.remove_effect(name)
        return True

    ########################################################################
    def roll_dmg(self, source, _, critical=False) -> int:
        """Roll the damage of the attack"""
        if critical:
            dmg = (
                int(dice.roll_max(self.dmg[0]))
                + int(dice.roll(self.dmg[0]))
                + self.dmg[1]
            )
        else:
            dmg = int(dice.roll(self.dmg[0]))
            print(f"{source} rolled {dmg} on {self.dmg[0]} for damage")
            if self.dmg[1]:
                dmg += self.dmg[1]
                print(f"Adding bonus of {self.dmg[1]} -> {dmg}")
        dmg_bon = self.dmg_bonus(source)
        if dmg_bon:
            dmg += dmg_bon
            print(f"Adding stat bonus of {dmg_bon} -> {dmg}")
        return max(dmg, 0)

    ########################################################################
    def has_disadvantage(
        self, source, target, rnge: int  # pylint: disable=unused-argument, no-self-use
    ) -> bool:
        """Does this attack have disadvantage at this range"""
        if source.has_condition(Condition.POISONED):
            return True
        return False

    ########################################################################
    def has_advantage(
        self, source, target, rnge: int  # pylint: disable=unused-argument, no-self-use
    ) -> bool:
        """Does this attack have advantage at this range"""
        if target.has_condition(Condition.UNCONSCIOUS) and rnge <= 1:
            return True
        for _, eff in target.effects.items():
            if eff.hook_gives_advantage_against():
                return True
        return False


# EOF
