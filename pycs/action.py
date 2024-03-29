""" Handle non-attack Actions """
from typing import Any, Optional, TYPE_CHECKING, cast
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import DamageType
from pycs.constant import Condition
from pycs.damage import Damage
from pycs.constant import Stat
from pycs.util import check_args
from pycs.damageroll import DamageRoll

if TYPE_CHECKING:
    from pycs.creature import Creature
    from pycs.equipment import Equipment


##############################################################################
##############################################################################
##############################################################################
class Action:  # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """generic action"""

    ########################################################################
    def __init__(self, name: str, **kwargs: Any):
        check_args(self._valid_args(), name, kwargs)
        self.name = name
        self.available = True
        self.type = ActionType.UNKNOWN
        self.category = kwargs.get("category", ActionCategory.ACTION)
        self.side_effect = kwargs.get("side_effect")
        self.attacks_per_action = kwargs.get("attacks_per_action", 1)
        self.action_cost = kwargs.get("action_cost", 1)
        self.finesse = kwargs.get("finesse", False)
        self.dmgroll: DamageRoll = cast(DamageRoll, kwargs.get("dmgroll"))
        self.attack_modifier = kwargs.get("attack_modifier", None)
        self.damage_modifier = kwargs.get("damage_modifier", None)
        self.heuristic = kwargs.get("heuristic", self.heuristic)  # type: ignore
        self.ammo = kwargs.get("ammo", None)
        self.gear: Optional["Equipment"] = None  # Gear that induced the action (set when added)
        # Creature owning the action (set when added) or sometimes explicitly
        self.owner = kwargs.get("owner", None)
        self.preferred_stat: Stat = Stat.STR

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return {
            "action_cost",
            "ammo",
            "attack_modifier",
            "attacks_per_action",
            "category",
            "damage_modifier",
            "dmgroll",
            "heuristic",
            "owner",
            "side_effect",
        }

    ########################################################################
    @property
    def use_stat(self) -> Stat:
        """What stat to use"""
        # Set from the equipment
        if self.gear and hasattr(self.gear, "use_stat"):
            return self.gear.use_stat
        # Default for attack type
        if self.finesse:
            if self.owner.stats[Stat.STR] < self.owner.stats[Stat.DEX]:
                return Stat.DEX
        return self.preferred_stat

    ########################################################################
    def atk_modifier(self, attacker: "Creature") -> int:  # pylint: disable=unused-argument
        """Modifier to the attack dice roll"""
        # Don't use NotImplementedError as isn't required for every action
        print(f"{self.__class__.__name__} hasn't implemented atk_modifier()")
        return 0

    ########################################################################
    def dmg_modifier(self, attacker: "Creature") -> Damage:  # pylint: disable=unused-argument
        """Modifier to the damage bonus"""
        # Don't use NotImplementedError as isn't required for every action
        print(f"{self.__class__.__name__} hasn't implemented dmg_modifier()")
        return Damage(0, DamageType.NONE)

    ########################################################################
    def pick_target(self) -> Optional["Creature"]:
        """Who are we going to do the action to - generally overwritten"""
        if hasattr(self.owner, "pick_target"):
            return self.owner.pick_target(self)
        enemy = self.owner.pick_closest_enemy()
        if enemy:
            return enemy[0]
        return None

    ########################################################################
    def hook_postdmg(self) -> None:
        """Should be overwritten"""

    ########################################################################
    def hook_predmg(self, dmg: Damage, source: "Creature", critical: bool) -> Damage:  # pylint: disable=unused-argument
        """Should be overwritten"""
        return Damage()

    ########################################################################
    def get_heuristic(self) -> int:
        """How much we should do this action"""
        heur: int = 0
        heur += self.owner.effects.hook_heuristic_mod(self, self.owner)
        heur += self.heuristic()
        return heur

    ########################################################################
    def heuristic(self) -> int:  # pylint: disable=method-hidden
        """Should we do this thing"""
        raise NotImplementedError(f"{self.name} {self.__class__.__name__}.heuristic() not implemented")

    ########################################################################
    def range(self) -> tuple[int, int]:
        """Return the range (good, max) of the action"""
        return 0, 0

    ##########################################################################
    def is_available(self) -> bool:
        """Is this action currently available to the creature"""
        if self.ammo is not None and not self.ammo:
            return False
        return True

    ########################################################################
    def perform_action(self) -> bool:
        """Perform the action"""
        raise NotImplementedError

    ########################################################################
    def ammo_usage(self) -> None:
        """Use up ammo if that is a thing"""
        if self.ammo is not None:
            self.ammo -= 1
            if self.ammo <= 0:
                self.available = False

    ########################################################################
    def __repr__(self) -> str:
        return self.name

    ##########################################################################
    def check_criticals(self, to_hit_roll: int) -> tuple[bool, bool]:
        """Did we critical hit or miss"""
        crit_hit = False
        crit_miss = False
        if to_hit_roll >= self.owner.critical:
            crit_hit = True
        if to_hit_roll == 1:
            crit_miss = True
        return crit_hit, crit_miss

    ##########################################################################
    def roll_to_hit(self, target: "Creature") -> tuple[int, bool, bool]:
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
    def calculate_to_hit(self, to_hit_roll: int, target: "Creature") -> tuple[int, str]:
        """Calculate the to_hit"""
        msg = []
        rnge = self.owner.distance(target)
        modifier = self.atk_modifier(self.owner)
        msg.append(f"+{modifier} (stat modifier)")
        profbon = self.owner.prof_bonus
        msg.append(f"+{profbon} (prof bonus)")
        to_hit = to_hit_roll + modifier + profbon
        to_hit_mod, msg_mod = self.owner.effects.hook_attack_to_hit(target=target, range_=rnge, action=self)
        to_hit += to_hit_mod
        msg.extend(msg_mod)
        if self.gear:
            if hasattr(self.gear, "hook_attack_to_hit"):
                mod = self.gear.hook_attack_to_hit(target=target)
                if mod:
                    to_hit += mod
                    msg.append(f"+{mod} from {self.gear}")
        return to_hit, ", ".join(msg)

    ########################################################################
    def buff_attack_damage(self, target: "Creature") -> None:
        """Calculate the attack damage from buffs"""
        self.owner.effects.hook_source_additional_damage(attack=self, source=self.owner, target=target)
        target.effects.hook_target_additional_damage(attack=self, source=self.owner, target=target)

    ########################################################################
    def did_we_hit(self, target: "Creature") -> tuple[bool, bool]:
        """Did we actually hit the target"""
        to_hit, crit_hit, crit_miss = self.roll_to_hit(target)

        hit = to_hit >= target.ac and not crit_miss
        return hit, crit_hit

    ########################################################################
    def do_attack(self) -> bool:
        """Do the attack - return wether we did the attack"""
        assert self.owner is not None
        target = self.pick_target()
        if target is None:
            return False
        rnge = self.owner.distance(target)
        if rnge > self.range()[1]:
            print(f"{target} is out of range")
            return False
        print(f"{self.owner} attacking {target} with {self}")

        did_hit, crit_hit = self.did_we_hit(target)
        if did_hit:
            dmg = self.roll_dmg(target, crit_hit)
            if not dmg:
                return True
            target.hit(dmg=dmg, source=self.owner, critical=crit_hit, atkname=self.name)
            if self.side_effect:
                self.side_effect(source=self.owner, target=target, dmg=dmg)

            # If the target or source of the damage has a buff
            self.buff_attack_damage(target)
            print(f"{self.owner} hit {target} (AC: {target.ac})" f" with {self} for {dmg} damage")
        else:
            target.miss(source=self.owner, atkname=self.name)
            print(f"{self.owner} missed {target} (AC: {target.ac}) with {self}")
        target.effects.removal_after_being_attacked()
        return True

    ########################################################################
    def max_dmg(self) -> Damage:
        """Return the max possible damage of the attack - used to calculate desirable action"""
        dmg = self.dmgroll.roll_max()
        dmg += self.dmg_modifier(self.owner)
        return dmg

    ########################################################################
    def dmg_bonus(self) -> list[tuple[Damage, str]]:
        """All the damage bonuses - using the relevant stat and the gear"""
        bonus = []
        if self.damage_modifier is not None:
            bonus.append((Damage(self.damage_modifier), "DmgMod"))
        elif self.use_stat:
            dmg_bon = self.dmg_modifier(self.owner)
            if dmg_bon:
                bonus.append((dmg_bon, f"{self.use_stat.value[:3]}"))
        if self.gear:
            if hasattr(self.gear, "hook_source_additional_damage"):
                dmg_bon = self.gear.hook_source_additional_damage()
                if dmg_bon:
                    bonus.append((dmg_bon, self.gear.name))
        return bonus

    ########################################################################
    def roll_dmg(self, _: Any, critical: bool = False) -> Damage:
        """Roll the damage of the attack"""
        msg = ""
        if critical:
            dmg_roll = self.dmgroll.roll_max() + self.dmgroll.roll()
        else:
            dmg_roll = self.dmgroll.roll()
        dmg = dmg_roll.copy()
        dmg_bon = self.dmg_bonus()
        for bonus, cause in dmg_bon:
            if isinstance(bonus, DamageRoll):
                bonus_roll = bonus.roll()
            else:
                bonus_roll = bonus.copy()
            dmg += bonus_roll
            msg += f"+{bonus_roll.hp} ({cause}); "
        print(f"{self.owner} inflicted {dmg} damage (Rolled {dmg_roll.hp} on {self.dmgroll}; {msg.strip()})")
        return dmg

    ########################################################################
    def has_disadvantage(self, target: "Creature", rnge: int) -> bool:
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
        if target.effects.hook_gives_disadvantage_against():
            return True
        if self.owner.effects.hook_gives_disadvantage(target):
            return True
        return False

    ########################################################################
    def has_advantage(self, target: "Creature", rnge: int) -> bool:
        """Does this attack have advantage at this range"""
        if target.has_condition(Condition.BLINDED) or target.has_condition(Condition.RESTRAINED):
            return True
        if target.has_condition(Condition.UNCONSCIOUS) and rnge <= 1:
            return True
        if target.has_condition(Condition.PRONE) and rnge <= 1:
            return True
        if target.effects.hook_gives_advantage_against():
            return True
        if self.owner.effects.hook_gives_advantage(target):
            return True
        return False


# EOF
