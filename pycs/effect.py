""" Handle Effects """
from typing import Any, Optional, TYPE_CHECKING
from pycs.action import Action
from pycs.damage import Damage
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.constant import Stat

if TYPE_CHECKING:
    from pycs.creature import Creature


##############################################################################
##############################################################################
##############################################################################
class Effect:
    """A single effect"""

    ##########################################################################
    def __init__(self, name: str, **kwargs: Any):
        self.name = name
        self.cause = kwargs.get("cause")
        self.owner: Optional[Creature]  # Set when added to a creature

    ##########################################################################
    def hook_heuristic_mod(self, action: Action, actor: "Creature") -> int:  # pylint: disable=unused-argument
        """Modification to the actions {action} heuristic"""
        return 0

    ##########################################################################
    def hook_attack_to_hit(self, **kwargs: Any) -> int:  # pylint: disable=unused-argument
        """Modify the roll to hit on attacks"""
        return 0

    ##########################################################################
    def hook_being_hit(self, dmg: Damage) -> Damage:  # pylint: disable=unused-argument
        """We've been hit by an attack; return the new dmg"""
        return dmg

    ##########################################################################
    def hook_saving_throw(self, stat: Stat, **kwargs: Any) -> dict:  # pylint: disable=unused-argument
        """Modify the saving throw roll"""
        return {"bonus": 0, "advantage": False, "disadvantage": False}

    ##########################################################################
    def initial(self, target: "Creature") -> None:
        """Initial effects on target"""

    ##########################################################################
    def finish(self, victim: "Creature") -> None:
        """When the effect finishes"""

    ##########################################################################
    def hook_start_turn(self) -> None:
        """We start the turn with an effect"""

    ##########################################################################
    def removal_end_of_its_turn(self, victim: "Creature") -> bool:  # pylint: disable=unused-argument
        """Do we remove this effect and the end of the victims turn"""
        return False

    ##########################################################################
    def hook_ac_modifier(self) -> int:
        """Modifications to armour class"""
        return 0

    ##########################################################################
    def hook_gives_advantage_against(self) -> bool:  # pylint: disable=unused-argument
        """Gives advantage against creature who has effect"""
        return False

    ##########################################################################
    def hook_gives_disadvantage_against(self) -> bool:  # pylint: disable=unused-argument
        """Gives disadvantage for creature who has the effect"""
        return False

    ##########################################################################
    def hook_gives_advantage(self, target: "Creature") -> bool:  # pylint: disable=unused-argument
        """Gives advantage for creature doing the attack"""
        return False

    ##########################################################################
    def hook_gives_disadvantage(self, target: "Creature") -> bool:  # pylint: disable=unused-argument
        """Gives disadvantage for creature doing the attack"""
        return False

    ##########################################################################
    def removal_after_being_attacked(self) -> bool:  # pylint: disable=unused-argument
        """Do we remove the effect after being turned"""
        return False

    ##########################################################################
    def hook_d20(self, val: int, reason: str) -> int:  # pylint: disable=unused-argument
        """We have rolled {val} on a d20 for {reason}"""
        return val

    ##########################################################################
    def hook_source_additional_damage(
        self,
        attack: Action,  # pylint: disable=unused-argument
        source: "Creature",  # pylint: disable=unused-argument
        target: "Creature",  # pylint: disable=unused-argument
    ) -> DamageRoll:
        """Addition damage from melee weapons based on the owner of the effect"""
        return DamageRoll("", 0, DamageType.NONE)

    ##########################################################################
    def hook_start_in_range(self, creat: "Creature") -> None:  # pylint: disable=unused-argument
        """Did we start our turn in range of any effect"""
        return

    ##########################################################################
    def hook_target_additional_damage(
        self,
        attack: Action,  # pylint: disable=unused-argument
        source: "Creature",  # pylint: disable=unused-argument
        target: "Creature",  # pylint: disable=unused-argument
    ) -> DamageRoll:
        """Addition damage from melee weapons based on the target of the effect"""
        return DamageRoll("", 0, DamageType.NONE)

    ##########################################################################
    def hook_fallen_unconscious(self, dmg: Damage, critical: bool) -> bool:  # pylint: disable=unused-argument
        """The owner of the effect has fallen unconscious
        Return True is creature still falls unconscious after hook
        """
        return True

    ##########################################################################
    def flee(self) -> None:
        """Run awaaay - from what?"""
        return None


# EOF
