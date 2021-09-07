"""https://www.dndbeyond.com/spells/lesser-restoration"""

from pycs.spell import SpellAction
from pycs.constant import SpellType
from pycs.constant import Condition
from pycs.constant import ActionCategory
from .spelltest import SpellTest


##############################################################################
class LesserRestoration(SpellAction):
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
        if self.pick_target(doer) is None:
            return 0
        return 20


##############################################################################
##############################################################################
##############################################################################
class TestLesserRestoration(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        super().setUp()
        self.caster.add_action(LesserRestoration())

    ##########################################################################
    def test_cast(self):
        """See what this spell does"""
        self.caster.moves = 90  # Make sure we can get there
        self.friend.add_condition(Condition.BLINDED)
        self.assertTrue(self.friend.has_condition(Condition.BLINDED))
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertFalse(self.friend.has_condition(Condition.BLINDED))


# EOF
