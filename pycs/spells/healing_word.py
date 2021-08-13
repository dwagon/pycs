"""https://www.dndbeyond.com/spells/healing-word"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Healing_Word(SpellAction):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Healing Word"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 60,
                "cure_hp": ("1d4", 3),
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)


# EOF
