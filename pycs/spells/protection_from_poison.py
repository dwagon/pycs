"""https://www.dndbeyond.com/spells/protection-from-poison"""

from typing import Any
from pycs.spell import SpellAction
from pycs.constant import SpellType


##############################################################################
class ProtectionFromPoison(SpellAction):
    """Spell"""

    def __init__(self, **kwargs: Any):
        name = "Protection From Poison"
        kwargs.update(
            {
                "reach": 5,
                "level": 2,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def cast(self) -> bool:
        """Not implemented yet"""
        return False


# EOF
