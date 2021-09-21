"""https://www.dndbeyond.com/spells/spirit-guardians"""

from pycs.constant import SpellType
from pycs.spell import AttackSpell


##############################################################################
##############################################################################
##############################################################################
class Spirit_Guardians(AttackSpell):
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
        kwargs.update(
            {
                "reach": 15,
                "level": 3,
                "style": SpellType.SAVE_HALF,
                "type": SpellType.RANGED,
                "concentration": SpellType.CONCENTRATION,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        if not self.owner.spell_available(self):
            return 0
        return 0

    ##########################################################################
    def pick_target(self):
        """Who should we do the spell to"""
        return self.owner

    ##########################################################################
    def cast(self):
        """Do the spell"""
        return True

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""


# EOF
