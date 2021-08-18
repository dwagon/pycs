"""https://www.dndbeyond.com/spells/branding-smite"""

from spells import SpellAction
from constants import SpellType


##############################################################################
class Branding_Smite(SpellAction):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Branding Smite"
        kwargs.update(
            {
                "casting": "bonus",
                "concentration": True,
                "reach": 5,
                "level": 2,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def cast(self, caster):
        """Do the spell"""


# EOF
