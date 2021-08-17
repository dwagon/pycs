"""https://www.dndbeyond.com/spells/sanctuary"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Sanctuary(SpellAction):
    def __init__(self, **kwargs):
        name = "Sanctuary"
        kwargs.update(
            {
                "casting": "bonus",
                "reach": 30,
                "level": 1,
                "style": "save",
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def cast(self, caster):
        """Do the spell"""


# EOF
