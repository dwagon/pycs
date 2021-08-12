"""https://www.dndbeyond.com/spells/healing-word"""

from actions import SpellHealing


##############################################################################
class Healing_Word(SpellHealing):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Healing Word"
        kwargs.update(
            {
                "reach": 60,
                "cure": ("1d4", 3),
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)


# EOF
