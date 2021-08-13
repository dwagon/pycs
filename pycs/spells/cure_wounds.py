"""https://www.dndbeyond.com/spells/cure-wounds"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Cure_Wounds(SpellAction):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Cure Wounds"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 5,
                "cure_hp": ("1d8", 3),
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)


# EOF
