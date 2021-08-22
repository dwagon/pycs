"""https://www.dndbeyond.com/spells/spiritual-weapon"""

import spells
from constants import SpellType


##############################################################################
class Spiritual_Weapon(spells.SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    def __init__(self, **kwargs):
        name = "Spiritual Weapon"
        kwargs.update(
            {
                "casting": "bonus",
                "reach": 60,
                "level": 1,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def cast(self, caster):
        """Do the spell"""
        return True

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 0


# EOF
