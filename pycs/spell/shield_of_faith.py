"""https://www.dndbeyond.com/spells/shield-of-faith"""

from effect import Effect
import spells
from constants import SpellType


##############################################################################
class Shield_Of_Faith(spells.SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    ###########################################################################
    def __init__(self, **kwargs):
        name = "Shield of Faith"
        kwargs.update(
            {
                "casting": "bonus",
                "concentration": True,
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
        print(f"{caster} casts Shield of Faith on {friend}")
        friend.add_effect(Shield_Of_Faith_Effect(cause=caster))
        return True

    ###########################################################################
    def pick_target(self, doer):
        """Who gets the spell - person with the lowest AC"""
        targets = []
        for friend in doer.arena.my_side(doer.side):
            if friend.has_effect("Shield of Faith"):
                continue
            targets.append((friend.ac, id(friend), friend))
        targets.sort()
        if not targets:
            return None
        return targets[0][-1]

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if self.pick_target(doer):
            return 1
        return 0


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
        eff.update({"bonus": 2})
        return eff


# EOF
