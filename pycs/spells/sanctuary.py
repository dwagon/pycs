"""https://www.dndbeyond.com/spells/sanctuary"""

from typing import Any
from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.spell import SpellAction


##############################################################################
class Sanctuary(SpellAction):
    """Spell"""

    def __init__(self, **kwargs: Any):
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

    def cast(self) -> bool:
        """Do the spell"""
        return False


# EOF
