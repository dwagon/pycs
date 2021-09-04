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
class Equipment:
    """Generic class"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        self.name = name
        self.ammo = kwargs.get("ammo")
        self.actions = []


##############################################################################
##############################################################################
##############################################################################
class Weapon(Equipment):
    """Attitude adjusters"""

    ##########################################################################
    def __init__(self, name, **kwargs):  # pylint: disable=useless-super-delegation
        """init"""
        super().__init__(name, **kwargs)


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
class Armour(Equipment):
    """Stop taking damage"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        """init"""
        self.ac = kwargs.get("ac", 0)
        self.ac_bonus = kwargs.get("ac_bonus", 0)
        self.dex_bonus = kwargs.get("dex_bonus", False)
        self.max_dex_bonus = kwargs.get("max_dex_bonus", 999)
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
    def perform_action(self, source):
        """Drink the potion"""
        raise NotImplementedError

    ##########################################################################
    def heuristic(self, source):
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
    def perform_action(self, source):
        """Drink the healing potion"""
        source.heal(*self.curing)

    ##########################################################################
    def heuristic(self, source):
        """Should we drink the potion"""
        return source.max_hp - source.hp


##############################################################################
##############################################################################
##############################################################################
class DrinkPotion(Action):
    """Drinking a potion"""

    ##########################################################################
    def __init__(self, name, **kwargs):  # pylint: disable=useless-super-delegation
        super().__init__(name, **kwargs)

    ##########################################################################
    def pick_target(self, doer):
        """Who do we do it do"""
        return doer

    ##########################################################################
    def perform_action(self, source):
        raise NotImplementedError


# EOF
