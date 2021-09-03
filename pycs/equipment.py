""" All sorts of equipment """
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import Stat


##############################################################################
##############################################################################
##############################################################################
class Equipment:
    """Generic class"""

    ##########################################################################
    def __init__(self, name, **kwargs):  # pylint: disable=unused-argument
        """init"""
        self.name = name
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
                ammo=kwargs.get("ammo"),
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


# EOF
