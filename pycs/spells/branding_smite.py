"""https://www.dndbeyond.com/spells/branding-smite"""

from typing import Any, Optional
from pycs.action import Action
from pycs.creature import Creature
from pycs.spell import SpellAction
from pycs.constant import SpellType
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class BrandingSmite(SpellAction):
    """The next time you hit a creature with a weapon attack before
    this spell ends, the weapon gleams with astral radiance as you
    strike. The attack deals an extra 2d6 radiant damage to the target,
    which becomes visible if it is invisible, and the target sheds dim
    light in a 5-foot radius and can’t become invisible until the spell
    ends."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        name = "Branding Smite"
        kwargs.update(
            {
                "category": ActionCategory.BONUS,
                "reach": 0,
                "level": 2,
                "type": SpellType.BUFF,
                "concentration": SpellType.CONCENTRATION,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def cast(self) -> bool:
        """Do the spell"""
        self.owner.add_effect(BrandingSmiteEffect(cause=self.owner))
        return True

    ########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we do the spell to"""
        return self.owner

    ########################################################################
    def heuristic(self) -> int:
        """Should we do the spell"""
        if not self.owner.spell_available(self):
            return 0
        if self.owner.has_effect("Branding Smite"):
            return 0
        return 12  # 2d6

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""
        self.owner.remove_effect("Branding Smite")


##############################################################################
##############################################################################
##############################################################################
class BrandingSmiteEffect(Effect):
    """Branding Smite"""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Branding Smite", **kwargs)

    ########################################################################
    def hook_source_additional_damage(
        self, attack: Action, source: Creature, target: Creature
    ) -> tuple[str, int, Optional[DamageType]]:
        """More damage"""
        return "2d6", 0, DamageType.RADIANT


# EOF
