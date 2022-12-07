""" All sorts of equipment """
from typing import Any, TYPE_CHECKING
import dice
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Stat
from pycs.util import check_args

if TYPE_CHECKING:
    from pycs.creature import Creature



##############################################################################
##############################################################################
##############################################################################
class Equipment:  # pylint: disable=too-few-public-methods
    """Generic class"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        self.name = name
        self.owner: "Creature"  # Set by add_gear()
        self.actions: list[Action] = []

    ##########################################################################
    def __repr__(self) -> str:
        return f"{self.name}"

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return set()


##############################################################################
##############################################################################
##############################################################################
class Weapon(Equipment):
    """Attitude adjusters"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.magic_bonus = kwargs.get("magic_bonus", 0)
        self.side_effect = kwargs.get("side_effect")
        self.actions = kwargs.get("actions", [])

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"magic_bonus", "side_effect", "actions"}

    ##########################################################################
    def hook_attack_to_hit(self, target: "Creature") -> int:  # pylint: disable=unused-argument
        """Any modifier to hit"""
        return self.magic_bonus

    ##########################################################################
    def hook_source_additional_damage(self) -> int:
        """Additional damage"""
        return self.magic_bonus


##############################################################################
##############################################################################
##############################################################################
class MeleeWeapon(Weapon):
    """Up close and personal"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.finesse = kwargs.get("finesse", False)
        self.reach: int = kwargs.get("reach")
        self.actions.append(
            MeleeAttack(
                name,
                dmg=kwargs.get("dmg"),
                dmg_type=kwargs.get("dmg_type"),
                reach=kwargs.get("reach"),
                side_effect=kwargs.get("side_effect"),
            )
        )

    ##########################################################################
    def range(self) -> tuple[int, int]:
        """Range of weapon"""
        return self.reach, self.reach

    ##########################################################################
    @property
    def use_stat(self) -> Stat:
        """Stat to use for weapon"""
        if self.finesse:
            if self.owner.stats[Stat.STR] < self.owner.stats[Stat.DEX]:
                return Stat.DEX
        return Stat.STR

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {
            "dmg",
            "dmg_type",
            "finesse",
            "magic_bonus",
            "reach",
            "side_effect",
        }


##############################################################################
##############################################################################
##############################################################################
class RangedWeapon(Weapon):
    """Combat from a distance"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.actions.append(
            RangedAttack(
                name,
                ammo=kwargs.get("ammo"),
                dmg=kwargs.get("dmg"),
                dmg_type=kwargs.get("dmg_type"),
                l_range=kwargs.get("l_range"),
                side_effect=kwargs.get("side_effect"),
                s_range=kwargs.get("s_range"),
            )
        )
        self.l_range: int = kwargs.get("l_range", -1)
        self.s_range: int = kwargs.get("s_range", -1)

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {
            "ammo",
            "magic_bonus",
            "dmg",
            "dmg_type",
            "l_range",
            "s_range",
            "side_effect",
        }

    ##########################################################################
    def range(self) -> tuple[int, int]:
        """Range of weapon"""
        return self.s_range, self.l_range

    ##########################################################################
    @property
    def use_stat(self) -> Stat:
        """Stat to use for weapon"""
        return Stat.DEX


##############################################################################
##############################################################################
##############################################################################
class Armour(Equipment):  # pylint: disable=too-few-public-methods
    """Stop taking damage"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.ac = kwargs.get("ac", 0)  # pylint: disable=invalid-name
        self.ac_bonus = kwargs.get("ac_bonus", 0)
        self.dex_bonus = kwargs.get("dex_bonus", False)
        self.max_dex_bonus = kwargs.get("max_dex_bonus", 999)
        self.magic_bonus = kwargs.get("magic_bonus", 0)

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {
            "ac",
            "magic_bonus",
            "ac_bonus",
            "dex_bonus",
            "max_dex_bonus",
        }


##############################################################################
##############################################################################
##############################################################################
class Potion(Equipment):
    """Boozing on the job"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):  # pylint: disable=useless-super-delegation
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.act = DrinkPotion(f"Drink {name}")
        self.act.heuristic = kwargs.get("heuristic", self.heuristic)    # type: ignore
        self.act.perform_action = kwargs.get("perform_action", self.perform_action) # type: ignore
        self.act.category = ActionCategory.BONUS
        self.act.ammo = kwargs.get("ammo")
        self.actions = [self.act]

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"heuristic", "perform_action", "ammo"}

    ##########################################################################
    def perform_action(self) -> None:
        """Drink the potion"""
        raise NotImplementedError

    ##########################################################################
    def heuristic(self) -> int:
        """Should we drink the potion"""
        raise NotImplementedError


##############################################################################
##############################################################################
##############################################################################
class HealingPotion(Potion):
    """Boozing on the job for health"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        """init"""
        self.curing = kwargs.get("curing")
        super().__init__(name, **kwargs)
        self.act.type = ActionType.HEALING

    ##########################################################################
    def perform_action(self) -> None:
        """Drink the healing potion"""
        self.owner.heal(*self.curing)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we drink the potion"""
        maxcure = int(dice.roll_max(self.curing[0])) + self.curing[1]
        return min(self.owner.max_hp - self.owner.hp, maxcure)

    ##########################################################################
    def _valid_args(self) -> set[str]:
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {
            "curing",
        }


##############################################################################
##############################################################################
##############################################################################
class DrinkPotion(Action):
    """Drinking a potion"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):  # pylint: disable=useless-super-delegation
        super().__init__(name, **kwargs)

    ##########################################################################
    def pick_target(self) -> "Creature":
        """Who do we do it do"""
        return self.owner

    ##########################################################################
    def perform_action(self) -> bool:
        raise NotImplementedError


# EOF
