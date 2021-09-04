"""https://www.dndbeyond.com/spells/shield-of-faith"""

from pycs.effect import Effect
from pycs.spell import SpellAction
from pycs.constant import SpellType


##############################################################################
class Shield_Of_Faith(SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    ###########################################################################
    def __init__(self, **kwargs):
        name = "Shield of Faith"
        kwargs.update(
            {
                "casting": "bonus",
                "concentration": SpellType.CONCENTRATION,
                "reach": 60,
                "level": 1,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def cast(self, caster):
        """Do the spell"""
        friend = self.pick_target(caster)
        if caster.distance(friend) > self.range()[0]:
            return False
        friend.add_effect(Shield_Of_Faith_Effect(cause=caster))
        self.target = friend
        return True

    ###########################################################################
    def pick_target(self, doer):
        """Who gets the spell - person with the lowest AC"""
        targets = []
        for friend in doer.arena.my_side(doer.side):
            if friend.has_effect(self.name):
                continue
            if doer.distance(friend) > self.range()[0]:
                continue
            targets.append((friend.ac, id(friend), friend))
        targets.sort()
        if not targets:
            return None
        return targets[0][-1]

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        if self.pick_target(doer):
            return 5
        return 0

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""
        self.target.remove_effect("Shield of Faith")


##############################################################################
##############################################################################
##############################################################################
class Shield_Of_Faith_Effect(Effect):
    """Effect of the Shield of Faith spell"""

    ###########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Shield of Faith", **kwargs)

    ###########################################################################
    def hook_ac_modifier(self, target):
        eff = super().hook_ac_modifier(target)
        eff += 2
        return eff


# EOF
