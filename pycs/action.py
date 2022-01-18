""" Handle non-attack Actions """
from typing import Tuple
import dice
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import Stat
from pycs.constant import Statistics
from pycs.util import check_args


##############################################################################
##############################################################################
##############################################################################
class Action:  # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """generic action"""

    ########################################################################
    def __init__(self, name: str, **kwargs):
        check_args(self._valid_args(), name, kwargs)
        self.name = name
        self.available = True
        self.type = ActionType.UNKNOWN
        self.category = kwargs.get("category", ActionCategory.ACTION)
        self.side_effect = kwargs.get("side_effect")
        self.attacks_per_action = kwargs.get("attacks_per_action", 1)
        self.action_cost = kwargs.get("action_cost", 1)
        self.finesse = kwargs.get("finesse", False)
        self.dmg = kwargs.get("dmg", "")
        self.dmg_type = kwargs.get("dmg_type", DamageType.PIERCING)
        self.attack_modifier = kwargs.get("attack_modifier", None)
        self.damage_modifier = kwargs.get("damage_modifier", None)
        self.heuristic = kwargs.get("heuristic", self.heuristic)
        self.ammo = kwargs.get("ammo", None)
        self.gear = None  # Gear that induced the action (set when added)
        # Creature owning the action (set when added) or sometimes explicitly
        self.owner = kwargs.get("owner", None)
        if not hasattr(self, "preferred_stat"):
            self.preferred_stat = None

    ##########################################################################
    def _valid_args(self):
        """What is valid in this class for kwargs"""
        return {
            "action_cost",
            "ammo",
            "attack_modifier",
            "attacks_per_action",
            "category",
            "damage_modifier",
            "dmg",
            "dmg_type",
            "heuristic",
            "owner",
            "side_effect",
        }

    ########################################################################
    @property
    def use_stat(self):
        """What stat to use"""
        # Set from the equipment
        if self.gear:
            return self.gear.use_stat
        # Default for attack type
        if self.finesse:
            if self.owner.stats[Stat.STR] < self.owner.stats[Stat.DEX]:
                return Stat.DEX
        return self.preferred_stat

    ########################################################################
    def atk_modifier(self, attacker):  # pylint: disable=unused-argument
        """Modifier to the attack dice roll"""
        # Don't use NotImplementedError as isn't required for every action
        print(f"{__class__.__name__} hasn't implemented atk_modifier()")
        return 0

    ########################################################################
    def dmg_modifier(self, attacker):  # pylint: disable=unused-argument
        """Modifier to the damage bonus"""
        # Don't use NotImplementedError as isn't required for every action
        print(f"{__class__.__name__} hasn't implemented dmg_modifier()")
        return 0

    ########################################################################
    def pick_target(self):
        """Who are we going to do the action to - generally overwritten"""
        if hasattr(self.owner, "pick_target"):
            print(f"DEBUG action.pick_target: {self.owner=}")
            return self.owner.pick_target(self)
        enemy = self.owner.pick_closest_enemy()
        if enemy:
            return enemy[0]
        return None

    ########################################################################
    def get_heuristic(self):
        """How much we should do this action"""
        heur = 0
        for _, eff in self.owner.effects.items():
            heur += eff.hook_heuristic_mod(self, self.owner)
        heur += self.heuristic()
        return heur

    ########################################################################
    def heuristic(self):  # pylint: disable=method-hidden
        """Should we do this thing"""
        raise NotImplementedError(
            f"{self.name} {__class__.__name__}.heuristic() not implemented"
        )

    ########################################################################
    def range(self):
        """Return the range (good, max) of the action"""
        return 0, 0

    ##########################################################################
    def is_available(self):
        """Is this action currently available to the creature"""
        if self.ammo is not None and not self.ammo:
            return False
        return True

    ########################################################################
    def perform_action(self):
        """Perform the action"""
        raise NotImplementedError

    ########################################################################
    def ammo_usage(self):
        """Use up ammo if that is a thing"""
        if self.ammo is not None:
            self.ammo -= 1
            if self.ammo <= 0:
                self.available = False

    ########################################################################
    def __repr__(self):
        return self.name

    ##########################################################################
    def check_criticals(self, to_hit_roll: int) -> Tuple[bool, bool]:
        """Did we critical hit or miss"""
        crit_hit = False
        crit_miss = False
        if to_hit_roll >= self.owner.critical:
            crit_hit = True
        if to_hit_roll == 1:
            crit_miss = True
        return crit_hit, crit_miss

    ##########################################################################
    def roll_to_hit(self, target) -> Tuple[int, bool, bool]:
        """Roll to hit with the attack"""
        msg = ""
        rnge = self.owner.distance(target)
        balance = 0
        if self.has_disadvantage(target, rnge):
            balance -= 1
        elif self.has_advantage(target, rnge):
            balance += 1

        if balance < 0:
            roll1 = self.owner.rolld20("attack")
            roll2 = self.owner.rolld20("attack")
            to_hit_roll = min(roll1, roll2)
            msg += f"Rolled {to_hit_roll}; [{roll1}, {roll2}] with disadvantage"
        elif balance > 0:
            roll1 = self.owner.rolld20("attack")
            roll2 = self.owner.rolld20("attack")
            to_hit_roll = max(roll1, roll2)
            msg += f"Rolled {to_hit_roll}; [{roll1}, {roll2}] with advantage"
        else:
            to_hit_roll = self.owner.rolld20("attack")
            msg += f"Rolled {to_hit_roll};"

        crit_hit, crit_miss = self.check_criticals(to_hit_roll)
        to_hit, msg1 = self.calculate_to_hit(to_hit_roll, target=target)
        if crit_hit:
            msg += " (critical hit)"
        elif crit_miss:
            msg += " (critical miss)"
            msg1 = ""
        print(f"{self.owner} got {to_hit} to hit ({msg} {msg1})")
        return int(to_hit), crit_hit, crit_miss

    ########################################################################
    def calculate_to_hit(self, to_hit_roll, target):
        """Calculate the to_hit"""
        msg = []
        rnge = self.owner.distance(target)
        modifier = self.atk_modifier(self.owner)
        msg.append(f"+{modifier} (modifier)")
        profbon = self.owner.prof_bonus
        msg.append(f"+{profbon} (prof bonus)")
        to_hit = to_hit_roll + modifier + profbon
        for name, eff in self.owner.effects.items():
            mod = eff.hook_attack_to_hit(target=target, range=rnge, action=self)
            if mod:
                to_hit += mod
                msg.append(f"+{mod} from {name}")
        if self.gear:
            mod = self.gear.hook_attack_to_hit(target=target)
            if mod:
                to_hit += mod
                msg.append(f"+{mod} from {self.gear}")
        return to_hit, ", ".join(msg)

    ########################################################################
    def buff_attack_damage(self, target) -> None:
        """Calculate the attack damage from buffs"""
        for atkname, eff in self.owner.effects.copy().items():
            dice_dmg, dmg, dmg_type = eff.hook_source_additional_damage(
                self, self.owner, target
            )
            if dmg_type is None:
                dmg_type = self.dmg_type
            if dice_dmg:
                dmg += int(dice.roll(dice_dmg))
            if dmg:
                target.hit(dmg, dmg_type, self.owner, critical=False, atkname=atkname)

        # If the target of the damage has a buff
        for atkname, eff in target.effects.copy().items():
            dice_dmg, dmg, dmg_type = eff.hook_target_additional_damage(
                self, self.owner, target
            )
            if dmg_type is None:
                dmg_type = self.dmg_type
            if dice_dmg:
                dmg += int(dice.roll(dice_dmg))
            if dmg:
                target.hit(dmg, dmg_type, self.owner, critical=False, atkname=atkname)

    ########################################################################
    def did_we_hit(self, target):
        """Did we actually hit the target"""
        to_hit, crit_hit, crit_miss = self.roll_to_hit(target)

        hit = to_hit >= target.ac and not crit_miss
        return hit, crit_hit

    ########################################################################
    def do_attack(self) -> bool:
        """Do the attack"""
        assert self.owner is not None
        target = self.owner.target
        rnge = self.owner.distance(target)
        if rnge > self.range()[1]:
            print(f"{target} is out of range")
            return False
        print(f"{self.owner} attacking {target} with {self}")

        did_hit, crit_hit = self.did_we_hit(target)
        if did_hit:
            dmg = self.roll_dmg(target, crit_hit)
            if dmg == 0:
                return True
            target.hit(dmg, self.dmg_type, self.owner, crit_hit, self.name)
            if self.side_effect:
                self.side_effect(source=self.owner, target=target, dmg=dmg)

            # If the target or source of the damage has a buff
            self.buff_attack_damage(target)

            print(
                f"{self.owner} hit {target} (AC: {target.ac})"
                f" with {self} for {dmg} hp {self.dmg_type.value} damage"
            )
        else:
            self.owner.statistics.append(Statistics(self.name, 0, None, False))
            print(f"{self.owner} missed {target} (AC: {target.ac}) with {self}")
        for name, eff in target.effects.copy().items():
            if eff.removal_after_being_attacked():
                print(f"{name} removed from {target}")
                target.remove_effect(name)
        return True

    ########################################################################
    def max_dmg(self) -> int:
        """Return the max possible damage of the attack - used to calculate desirable action"""
        dmg = int(dice.roll_max(self.dmg[0]))
        if self.dmg[1]:
            dmg += self.dmg[1]
        dmg_bon = self.dmg_modifier(self.owner)
        if dmg_bon:
            dmg += dmg_bon
        return max(dmg, 0)

    ########################################################################
    def dmg_bonus(self) -> list:
        """All the damage bonuses"""
        bonus = []
        if self.damage_modifier is not None:
            bonus.append((self.damage_modifier, "DmgMod"))
        elif self.use_stat:
            dmg_bon = self.dmg_modifier(self.owner)
            if dmg_bon:
                bonus.append((dmg_bon, f"{self.use_stat.value[:3]}"))
        if self.gear:
            dmg_bon = self.gear.hook_source_additional_damage()
            if dmg_bon:
                bonus.append((dmg_bon, self.gear.name))
        return bonus

    ########################################################################
    def roll_dmg(self, _, critical=False) -> int:
        """Roll the damage of the attack"""
        msg = ""
        if critical:
            dmg = int(dice.roll_max(self.dmg[0])) + int(dice.roll(self.dmg[0]))
        else:
            dmg = int(dice.roll(self.dmg[0]))
        rolled = dmg
        if self.dmg[1]:
            dmg += self.dmg[1]
            msg += f"{self.dmg[1]} "
        dmg_bon = self.dmg_bonus()
        for bonus, cause in dmg_bon:
            dmg += bonus
            msg += f"+{bonus} ({cause}) "
        dmg = max(dmg, 0)
        print(
            f"{self.owner} got {dmg} damage (Rolled {rolled} on {self.dmg[0]}; {msg.strip()})"
        )
        return dmg

    ########################################################################
    def has_disadvantage(self, target, rnge: int) -> bool:
        """Does this attack have disadvantage"""
        # Needs to change to be related to the source of the fright
        if (
            self.owner.has_condition(Condition.POISONED)
            or self.owner.has_condition(Condition.FRIGHTENED)
            or self.owner.has_condition(Condition.PRONE)
        ):
            return True
        if target.has_condition(Condition.PRONE) and rnge > 1:
            return True
        for _, eff in target.effects.items():
            if eff.hook_gives_disadvantage_against():
                return True
        for _, eff in self.owner.effects.items():
            if eff.hook_gives_disadvantage(target):
                return True
        return False

    ########################################################################
    def has_advantage(self, target, rnge: int) -> bool:
        """Does this attack have advantage at this range"""
        if target.has_condition(Condition.UNCONSCIOUS) and rnge <= 1:
            return True
        if target.has_condition(Condition.PRONE) and rnge <= 1:
            return True
        for _, eff in target.effects.items():
            if eff.hook_gives_advantage_against():
                return True
        for _, eff in self.owner.effects.items():
            if eff.hook_gives_advantage(target):
                return True
        return False


# EOF
