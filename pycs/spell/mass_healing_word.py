"""https://www.dndbeyond.com/spells/mass-healing-word"""

from constants import SpellType
from spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Mass_Healing_Word(SpellAction):
    """As you call out words of restoration, up to six creatures of
    your choice that you can see within range regain hit points equal
    to 1d4 + your spellcasting ability modifier. This spell has no
    effect on undead or constructs."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Mass Healing Word"
        kwargs.update({"reach": 60, "level": 3, "type": SpellType.HEALING})
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
        # Pick three people near where we are
        # TO DO - better this to move to where we can get 3 peeps
        return doer

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        return True


# EOF
