""" All sorts of equipment """
import dice
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Stat
from pycs.util import check_args


##############################################################################
##############################################################################
##############################################################################
class Equipment:  # pylint: disable=too-few-public-methods
    """Generic class"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        self.name = name
        self.owner = None  # Set by add_gear()
        self.actions = []

    ##########################################################################
    def __repr__(self):
        return f"{self.name}"

    ##########################################################################
    def _valid_args(self):
        """What is valid in this class for kwargs"""
        return set()


##############################################################################
##############################################################################
##############################################################################
class Weapon(Equipment):
    """Attitude adjusters"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.magic_bonus = kwargs.get("magic_bonus", 0)
        self.side_effect = kwargs.get("side_effect")
        self.actions = kwargs.get("actions", [])

    ##########################################################################
    def _valid_args(self):
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"magic_bonus", "side_effect", "actions"}

    ##########################################################################
    def hook_attack_to_hit(self, target):  # pylint: disable=unused-argument
        """Any modifier to hit"""
        return self.magic_bonus

    ##########################################################################
    def hook_source_additional_damage(self):
        """Additional damage"""
        return self.magic_bonus


##############################################################################
##############################################################################
##############################################################################
class MeleeWeapon(Weapon):
    """Up close and personal"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.finesse = kwargs.get("finesse", False)
        self.reach = kwargs.get("reach")
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
    def range(self):
        """Range of weapon"""
        return self.reach, self.reach

    ##########################################################################
    @property
    def use_stat(self):
        """Stat to use for weapon"""
        if self.finesse:
            if self.owner.stats[Stat.STR] < self.owner.stats[Stat.DEX]:
                return Stat.DEX
        return Stat.STR

    ##########################################################################
    def _valid_args(self):
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
    def __init__(self, name, **kwargs):
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
        self.l_range = kwargs.get("l_range")
        self.s_range = kwargs.get("s_range")

    ##########################################################################
    def _valid_args(self):
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
    def range(self):
        """Range of weapon"""
        return self.s_range, self.l_range

    ##########################################################################
    @property
    def use_stat(self):
        """Stat to use for weapon"""
        return Stat.DEX


##############################################################################
##############################################################################
##############################################################################
class Armour(Equipment):  # pylint: disable=too-few-public-methods
    """Stop taking damage"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.ac = kwargs.get("ac", 0)  # pylint: disable=invalid-name
        self.ac_bonus = kwargs.get("ac_bonus", 0)
        self.dex_bonus = kwargs.get("dex_bonus", False)
        self.max_dex_bonus = kwargs.get("max_dex_bonus", 999)
        self.magic_bonus = kwargs.get("magic_bonus", 0)

    ##########################################################################
    def _valid_args(self):
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
    def __init__(self, name, **kwargs):  # pylint: disable=useless-super-delegation
        """init"""
        check_args(self._valid_args(), name, kwargs)
        super().__init__(name, **kwargs)
        self.act = DrinkPotion(f"Drink {name}")
        self.act.heuristic = kwargs.get("heuristic", self.heuristic)
        self.act.perform_action = kwargs.get("perform_action", self.perform_action)
        self.act.category = ActionCategory.BONUS
        self.act.ammo = kwargs.get("ammo")
        self.actions = [self.act]

    ##########################################################################
    def _valid_args(self):
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"heuristic", "perform_action", "ammo"}

    ##########################################################################
    def perform_action(self):
        """Drink the potion"""
        raise NotImplementedError

    ##########################################################################
    def heuristic(self):
        """Should we drink the potion"""
        raise NotImplementedError


##############################################################################
##############################################################################
##############################################################################
class HealingPotion(Potion):
    """Boozing on the job for health"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        self.curing = kwargs.get("curing")
        super().__init__(name, **kwargs)
        self.act.type = ActionType.HEALING

    ##########################################################################
    def perform_action(self):
        """Drink the healing potion"""
        self.owner.heal(*self.curing)

    ##########################################################################
    def heuristic(self):
        """Should we drink the potion"""
        maxcure = int(dice.roll_max(self.curing[0])) + self.curing[1]
        return min(self.owner.max_hp - self.owner.hp, maxcure)

    ##########################################################################
    def _valid_args(self):
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
    def __init__(self, name, **kwargs):  # pylint: disable=useless-super-delegation
        super().__init__(name, **kwargs)

    ##########################################################################
    def pick_target(self):
        """Who do we do it do"""
        return self.owner

    ##########################################################################
    def perform_action(self):
        raise NotImplementedError


# EOF
