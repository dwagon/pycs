"""https://www.dndbeyond.com/spells/aid"""

from constants import SpellType
from effect import Effect
from spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Aid(SpellAction):
    """Your spell bolsters your allies with toughness and resolve.
    Choose up to three creatures within range. Each target's hit
    point maximum and current hit points increase by 5 for the
    duration.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, a target's hit points increase by an additional
    5 for each slot level above 2nd."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Aid"
        kwargs.update(
            {"reach": 30, "level": 2, "side_effect": self.aid, "type": SpellType.BUFF}
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        close = 0
        for targ in doer.arena.my_side(doer.side):
            if doer.distance(targ) <= 30 / 5:
                if doer.has_effect("Aid"):
                    continue
                close += 1
        return close

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        # Pick three people near where we are
        # TO DO - better this to move to where we can get 3 peeps
        return doer

    ##########################################################################
    def aid(self, caster):
        """Do the spell"""
        targets = 3
        for targ in caster.arena.my_side(caster.side):
            if caster.distance(targ) <= 30 / 6:
                if not targ.has_effect("Aid"):
                    targ.add_effect(AidEffect(cause=caster))
                    targets -= 1
        if targets < 3:
            caster.add_effect(AidEffect(cause=caster))


##############################################################################
##############################################################################
##############################################################################
class AidEffect(Effect):
    """Effect of the aid spell"""

    def __init__(self, **kwargs):
        super().__init__("Aid", **kwargs)

    def initial(self, target):
        """Initial effects of Aid"""
        target.hp += 5
        target.max_hp += 5


# EOF
