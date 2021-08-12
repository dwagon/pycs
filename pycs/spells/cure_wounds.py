"""https://www.dndbeyond.com/spells/cure-wounds"""

from actions import SpellHealing


##############################################################################
class Cure_Wounds(SpellHealing):
    """Spell"""

    def __init__(self, **kwargs):
        name = "Cure Wounds"
        kwargs.update(
            {
                "reach": 5,
                "cure": ("1d8", 3),
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)


# EOF
