"""https://www.dndbeyond.com/spells/shield-of-faith"""

from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.effect import Effect
from pycs.spell import SpellAction

from .spelltest import SpellTest


##############################################################################
class ShieldOfFaith(SpellAction):
    """A shimmering field appears and surrounds a creature of your
    choice within range, granting it a +2 bonus to AC for the duration.
    """

    ###########################################################################
    def __init__(self, **kwargs):
        name = "Shield of Faith"
        self._target = None
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
        friend.add_effect(ShieldOfFaithEffect(cause=caster))
        self._target = friend
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
        return targets[0][-1]

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if self.pick_target(doer):
            return 5
        return 0

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""
        self._target.remove_effect("Shield of Faith")


##############################################################################
##############################################################################
##############################################################################
class ShieldOfFaithEffect(Effect):
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


##############################################################################
##############################################################################
##############################################################################
class TestShieldOfFaith(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        super().setUp()
        self.caster.add_action(ShieldOfFaith())
        self.caster._ac = 19
        self.caster.speed = 90  # Ensure we can get to friend

    ##########################################################################
    def test_cast(self):
        """See what this spell does"""
        self.assertEqual(self.friend.ac, 10)
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertTrue(self.friend.has_effect("Shield of Faith"))
        self.assertEqual(self.friend.ac, 12)

    ##########################################################################
    def test_concentration(self):
        """What happens when we lose concentration"""
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertTrue(self.friend.has_effect("Shield of Faith"))
        self.caster.remove_concentration()
        self.assertFalse(self.friend.has_effect("Shield of Faith"))
        self.assertEqual(self.friend.ac, 10)


# EOF
