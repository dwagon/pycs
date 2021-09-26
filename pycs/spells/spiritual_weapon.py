"""https://www.dndbeyond.com/spells/spiritual-weapon"""

from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.spell import SpellAction


##############################################################################
class SpiritualWeapon(SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    def __init__(self, **kwargs):
        name = "Spiritual Weapon"
        kwargs.update(
            {
                "category": ActionCategory.BONUS,
                "reach": 60,
                "level": 1,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def cast(self):
        """Do the spell"""
        return True

    ###########################################################################
    def heuristic(self):
        """Should we do the spell"""
        if not self.owner.spell_available(self):
            return 0
        return 0


# EOF
