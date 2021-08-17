"""https://www.dndbeyond.com/spells/protection-from-poison"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Protection_From_Poison(SpellAction):
    def __init__(self, **kwargs):
        name = "Protection From Poison"
        kwargs.update(
            {
                "reach": 5,
                "level": 2,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)


# EOF
