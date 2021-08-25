"""https://www.dndbeyond.com/spells/hold-person"""

from constants import SpellType
from spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Hold_Person(SpellAction):
    """Choose a humanoid that you can see within range. The target must
    succeed on a Wisdom saving throw or be paralyzed for the duration.
    At the end of each of its turns, the target can make another Wisdom
    saving throw. On a success, the spell ends on the target."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Hold Person"
        kwargs.update({"reach": 60, "level": 2, "type": SpellType.CONTROL})
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        return 0

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        # Pick three people near where we are
        # TO DO - better this to move to where we can get 3 peeps
        return doer

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        return True


# EOF
