"""https://www.dndbeyond.com/spells/spirit-guardians"""

from constants import SpellType
from spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Spirit_Guardians(SpellAction):
    """You call forth spirits to protect you. They flit around you to
    a distance of 15 feet for the duration. If you are good or neutral,
    their spectral form appears angelic or fey (your choice). If you
    are evil, they appear fiendish.

    When you cast this spell, you can designate any number of creatures
    you can see to be unaffected by it. An affected creature's speed
    is halved in the area, and when the creature enters the area for
    the first time on a turn or starts its turn there, it must make a
    Wisdom saving throw. On a failed save, the creature takes 3d8 radiant
    damage (if you are good or neutral) or 3d8 necrotic damage (if you
    are evil). On a successful save, the creature takes half as much
    damage."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Spirit Guardians"
        kwargs.update({"reach": 15, "level": 3, "type": SpellType.RANGED})
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
