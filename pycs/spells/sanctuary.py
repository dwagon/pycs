"""https://www.dndbeyond.com/spells/sanctuary"""

from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.spell import SpellAction


##############################################################################
class Sanctuary(SpellAction):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Sanctuary"
        kwargs.update(
            {
                "category": ActionCategory.BONUS,
                "reach": 30,
                "level": 1,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def cast(self):
        """Do the spell"""


# EOF
