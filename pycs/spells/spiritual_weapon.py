"""https://www.dndbeyond.com/spells/spiritual-weapon"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Spiritual_Weapon(SpellAction):
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
                "side_effect": self.spiritual_weap,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def spiritual_weap(self, caster, target):
        """Do the spell"""


# EOF
