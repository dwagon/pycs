"""https://www.dndbeyond.com/spells/protection-from-poison"""

from pycs.spells import SpellAction
from pycs.constants import SpellType


##############################################################################
class Protection_From_Poison(SpellAction):
    """Spell"""

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
