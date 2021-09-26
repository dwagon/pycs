""" Handle Effects """
from typing import Tuple, Optional
from pycs.constant import DamageType


##############################################################################
##############################################################################
##############################################################################
class Effect:
    """Effects"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        self.name = name
        self.cause = kwargs.get("cause")
        self.caster = kwargs.get("caster")
        self.owner = None  # Set when added to a creature

    ##########################################################################
    def hook_heuristic_mod(self, action, actor):  # pylint: disable=unused-argument
        """Modification to the actions {action} heuristic"""
        return 0

    ##########################################################################
    def hook_attack_to_hit(self, **kwargs) -> dict:  # pylint: disable=unused-argument
        """Modify the roll to hit on attacks"""
        return 0

    ##########################################################################
    def hook_being_hit(self, dmg, dmgtype) -> int:  # pylint: disable=unused-argument
        """We've been hit by an attack; return the new dmg"""
        return dmg

    ##########################################################################
    def hook_saving_throw(
        self, stat, **kwargs  # pylint: disable=unused-argument
    ) -> dict:
        """Modify the saving throw roll"""
        return {"bonus": 0, "advantage": False, "disadvantage": False}

    ##########################################################################
    def initial(self, target):
        """Initial effects on target"""

    ##########################################################################
    def finish(self, victim):
        """When the effect finishes"""

    ##########################################################################
    def hook_start_turn(self):
        """We start the turn with an effect"""

    ##########################################################################
    def removal_end_of_its_turn(self, victim):  # pylint: disable=unused-argument
        """Do we remove this effect and the end of the victims turn"""
        return False

    ##########################################################################
    def hook_ac_modifier(self, target):  # pylint: disable=unused-argument
        """Modifications to {target}'s armour class"""
        return 0

    ##########################################################################
    def hook_gives_advantage_against(
        self,
    ):  # pylint: disable=unused-argument
        """Gives advantage against creature who has effect"""
        return False

    ##########################################################################
    def hook_gives_disadvantage_against(self):  # pylint: disable=unused-argument
        """Gives disadvantage for creature who has the effect"""
        return False

    ##########################################################################
    def hook_gives_advantage(self, target):  # pylint: disable=unused-argument
        """Gives advantage for creature doing the attack"""
        return False

    ##########################################################################
    def hook_gives_disadvantage(self, target):  # pylint: disable=unused-argument
        """Gives disadvantage for creature doing the attack"""
        return False

    ##########################################################################
    def removal_after_being_attacked(
        self,
    ):  # pylint: disable=unused-argument
        """Do we remove the effect after being turned"""
        return False

    ##########################################################################
    def hook_d20(self, val, reason):  # pylint: disable=unused-argument
        """We have rolled {val} on a d20 for {reason}"""
        return val

    ##########################################################################
    def hook_source_additional_damage(
        self, attack, source, target  # pylint: disable=unused-argument
    ) -> Optional[Tuple[str, int, Optional[DamageType]]]:
        """Addition damage from melee weapons based on the owner of the effect
        Return:
        * Dice Damage
        * Damage Bonus
        * Damage Type. If DamageType is None, use the existing damage type of the attack
        """
        return ("", 0, None)

    ##########################################################################
    def hook_start_in_range(self, creat):  # pylint: disable=unused-argument
        """Did we start our turn in range of any effect"""
        return

    ##########################################################################
    def hook_target_additional_damage(
        self, attack, source, target  # pylint: disable=unused-argument
    ) -> Optional[Tuple[str, int, Optional[DamageType]]]:
        """Addition damage from melee weapons based on the target of the effect
        Return:
        * Dice Damage
        * Damage Bonus
        * Damage Type. If DamageType is None, use the existing damage type of the attack
        """
        return ("", 0, None)

    ##########################################################################
    def hook_fallen_unconscious(
        self, dmg: int, dmg_type, critical: bool  # pylint: disable=unused-argument
    ) -> bool:
        """The owner of the effect has fallen unconscious
        Return True is creature still falls unconscious after hook
        """
        return True

    ##########################################################################
    def flee(self):
        """Run awaaay - from what?"""
        return None


# EOF
