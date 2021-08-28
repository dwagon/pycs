"""https://www.dndbeyond.com/spells/branding-smite"""

from pycs.spell import SpellAction
from pycs.constant import SpellType
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class Branding_Smite(SpellAction):
    """The next time you hit a creature with a weapon attack before
    this spell ends, the weapon gleams with astral radiance as you
    strike. The attack deals an extra 2d6 radiant damage to the target,
    which becomes visible if it is invisible, and the target sheds dim
    light in a 5-foot radius and can’t become invisible until the spell
    ends."""

    ########################################################################
    def __init__(self, **kwargs):
        name = "Branding Smite"
        kwargs.update(
            {
                "category": ActionCategory.BONUS,
                "concentration": True,
                "reach": 0,
                "level": 2,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def cast(self, caster):
        """Do the spell"""
        caster.add_effect(BrandingSmiteEffect(cause=caster))
        return True

    ########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        return doer

    ########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        if doer.has_effect("Branding Smite"):
            return 0
        return 1


##############################################################################
##############################################################################
##############################################################################
class BrandingSmiteEffect(Effect):
    """Branding Smite"""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Branding Smite", **kwargs)

    ########################################################################
    def hook_source_additional_melee_damage(self):
        """More damage"""
        return ("2d6", 0, DamageType.RADIANT)


# EOF
