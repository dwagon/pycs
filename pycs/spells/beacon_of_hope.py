"""https://www.dndbeyond.com/spells/beacon-of-hope"""

from typing import Any, Optional
from pycs.constant import SpellType
from pycs.creature import Creature
from pycs.spell import SpellAction


##############################################################################
##############################################################################
##############################################################################
class BeaconOfHope(SpellAction):
    """This spell bestows hope and vitality. Choose any number of
    creatures within range. For the duration, each target has advantage
    on Wisdom saving throws and death saving throws, and regains the
    maximum number of hit points possible from any healing."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Beacon of Hope"
        kwargs.update(
            {
                "reach": 30,
                "level": 3,
                "type": SpellType.BUFF,
                "concentration": SpellType.CONCENTRATION,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the spell
        the more people it can effect the more we should do it"""
        if not self.owner.spell_available(self):
            return 0
        return 0

    ##########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we do the spell to"""
        return self.owner

    ##########################################################################
    def cast(self) -> bool:
        """Do the spell"""
        return True

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""


# EOF
