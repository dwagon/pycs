"""https://www.dndbeyond.com/spells/lesser-restoration"""

from pycs.spell import SpellAction
from pycs.constant import SpellType
from pycs.constant import Condition


##############################################################################
class Lesser_Restoration(SpellAction):
    """You touch a creature and can end either one disease or one
    condition afflicting it. The condition can be blinded, deafened,
    paralyzed, or poisoned."""

    ###########################################################################
    def __init__(self, **kwargs):
        name = "Lesser Restoration"
        kwargs.update(
            {
                "reach": 5,
                "level": 2,
                "type": SpellType.HEALING,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def cast(self, caster):
        """Do the spell"""
        if not caster.target:
            return False
        for cond in (
            Condition.PARALYZED,
            Condition.BLINDED,
            Condition.POISONED,
            Condition.DEAFENED,
        ):
            if caster.target.has_condition(cond):
                caster.target.remove_condition(cond)
                print(f"{caster} cured {caster.target} of {cond.value}")
                break
        return True

    ###########################################################################
    def pick_target(self, doer):
        """Who are we going to cast it on"""
        friends = doer.pick_closest_friends()
        for friend in friends:
            if doer.distance(friend) < doer.moves:
                if friend.has_condition(
                    Condition.BLINDED,
                    Condition.DEAFENED,
                    Condition.PARALYZED,
                    Condition.POISONED,
                ):
                    return friend
        return None

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        if self.pick_target(doer) is None:
            return 0
        return 2


# EOF
