"""https://www.dndbeyond.com/spells/beacon-of-hope"""

from pycs.constant import SpellType
from pycs.spell import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Beacon_Of_Hope(SpellAction):
    """This spell bestows hope and vitality. Choose any number of
    creatures within range. For the duration, each target has advantage
    on Wisdom saving throws and death saving throws, and regains the
    maximum number of hit points possible from any healing."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Beacon of Hope"
        kwargs.update({"reach": 30, "level": 3, "type": SpellType.BUFF})
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        if not doer.spell_available(self):
            return 0
        return 0

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        return doer

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        return True


# EOF
