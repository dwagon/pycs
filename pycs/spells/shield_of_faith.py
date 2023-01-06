"""https://www.dndbeyond.com/spells/shield-of-faith"""

from typing import Any, Optional
from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.spell import SpellAction

from pycs.spells.spelltest import SpellTest


##############################################################################
class ShieldOfFaith(SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    ###########################################################################
    def __init__(self, **kwargs: Any):
        name = "Shield of Faith"
        self._target: Optional[Creature]
        kwargs.update(
            {
                "category": ActionCategory.BONUS,
                "concentration": SpellType.CONCENTRATION,
                "reach": 60,
                "level": 1,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def cast(self) -> bool:
        """Do the spell"""
        friend = self.pick_target()
        if friend is None:
            return False
        if self.owner.distance(friend) > self.range()[0]:
            return False
        friend.add_effect(ShieldOfFaithEffect(cause=self.owner))
        self._target = friend
        return True

    ###########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who gets the spell - person with the lowest AC"""
        targets = []
        for friend in self.owner.arena.my_side(self.owner.side):
            if friend.has_effect(self.name):
                continue
            if self.owner.distance(friend) > self.range()[0]:
                continue
            targets.append((friend.ac, id(friend), friend))
        targets.sort()
        if not targets:
            return None
        return targets[0][-1]

    ###########################################################################
    def heuristic(self) -> int:
        """Should we do the spell"""
        if self.pick_target():
            return 5
        return 0

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""
        if self._target is None:
            return
        self._target.remove_effect("Shield of Faith")


##############################################################################
##############################################################################
##############################################################################
class ShieldOfFaithEffect(Effect):
    """Effect of the Shield of Faith spell"""

    ###########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Shield of Faith", **kwargs)

    ###########################################################################
    def hook_ac_modifier(self) -> int:
        return 2


##############################################################################
##############################################################################
##############################################################################
class TestShieldOfFaith(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self) -> None:
        """Test setup"""
        super().setUp()
        self.caster.options_this_turn = [ActionCategory.BONUS]
        self.caster.add_action(ShieldOfFaith())
        self.caster._ac = 19  # pylint: disable=protected-access
        self.caster.speed = 90  # Ensure we can get to friend

    ##########################################################################
    def test_cast(self) -> None:
        """See what this spell does"""
        self.assertEqual(self.friend.ac, 10)
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=True)
        self.assertTrue(self.friend.has_effect("Shield of Faith"))
        self.assertEqual(self.friend.ac, 12)

    ##########################################################################
    def test_concentration(self) -> None:
        """What happens when we lose concentration"""
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=True)
        self.assertTrue(self.friend.has_effect("Shield of Faith"))
        self.caster.remove_concentration()
        self.assertFalse(self.friend.has_effect("Shield of Faith"))
        self.assertEqual(self.friend.ac, 10)


# EOF
