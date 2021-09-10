""" All sorts of equipment """
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Stat


##############################################################################
##############################################################################
##############################################################################
class Equipment:  # pylint: disable=too-few-public-methods
    """Generic class"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        self.name = name
        self.owner = None  # Set by add_gear()
        self.ammo = kwargs.get("ammo")
        self.actions = []

    ##########################################################################
    def __repr__(self):
        return f"{self.name}"


##############################################################################
##############################################################################
##############################################################################
class Weapon(Equipment):
    """Attitude adjusters"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        self.magic_bonus = kwargs.get("magic_bonus", 0)
        self.side_effect = kwargs.get("side_effect")
        super().__init__(name, **kwargs)

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
        super().__init__(name, **kwargs)
        self.actions = [
            MeleeAttack(
                name,
                magic_bonus=kwargs.get("magic_bonus"),
                dmg=kwargs.get("dmg"),
                dmg_type=kwargs.get("dmg_type"),
                reach=kwargs.get("reach"),
                side_effect=kwargs.get("side_effect"),
                use_stat=kwargs.get("use_stat", Stat.STR),
            )
        ]


##############################################################################
##############################################################################
##############################################################################
class RangedWeapon(Weapon):
    """Combat from a distance"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        super().__init__(name, **kwargs)
        self.actions = [
            RangedAttack(
                name,
                magic_bonus=kwargs.get("magic_bonus"),
                ammo=self.ammo,
                dmg=kwargs.get("dmg"),
                dmg_type=kwargs.get("dmg_type"),
                l_range=kwargs.get("l_range"),
                s_range=kwargs.get("s_range"),
                use_stat=kwargs.get("use_stat", Stat.DEX),
            )
        ]


##############################################################################
##############################################################################
##############################################################################
class Armour(Equipment):  # pylint: disable=too-few-public-methods
    """Stop taking damage"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        self.ac = kwargs.get("ac", 0)  # pylint: disable=invalid-name
        self.ac_bonus = kwargs.get("ac_bonus", 0)
        self.dex_bonus = kwargs.get("dex_bonus", False)
        self.max_dex_bonus = kwargs.get("max_dex_bonus", 999)
        self.magic_bonus = kwargs.get("magic_bonus", 0)
        super().__init__(name, **kwargs)


##############################################################################
##############################################################################
##############################################################################
class Potion(Equipment):
    """Boozing on the job"""

    ##########################################################################
    def __init__(self, name, **kwargs):  # pylint: disable=useless-super-delegation
        """init"""
        super().__init__(name, **kwargs)
        self.act = DrinkPotion(f"Drink {name}")
        self.act.heuristic = kwargs.get("heuristic", self.heuristic)
        self.act.perform_action = kwargs.get("perform_action", self.perform_action)
        self.act.category = ActionCategory.BONUS
        self.act.ammo = self.ammo
        self.actions = [self.act]

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
        return self.owner.max_hp - self.owner.hp


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
