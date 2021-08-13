"""https://www.dndbeyond.com/spells/shield-of-faith"""

from actions import SpellAction
from constants import SpellType


##############################################################################
class Shield_Of_Faith(SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    def __init__(self, **kwargs):
        name = "Shield of Faith"
        kwargs.update(
            {
                "casting": "bonus",
                "reach": 60,
                "level": 1,
                "side_effect": self.shieldfaith,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    def shieldfaith(self, caster, target):
        """Do the spell"""


# EOF
