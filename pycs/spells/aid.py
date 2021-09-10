"""https://www.dndbeyond.com/spells/aid"""

from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.effect import Effect
from pycs.spell import SpellAction
from .spelltest import SpellTest


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
        kwargs.update({"reach": 30, "level": 2, "type": SpellType.BUFF})
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        close = 0
        for targ in self.owner.arena.my_side(self.owner.side):
            if self.owner.distance(targ) <= 30 / 5:
                if targ.has_effect("Aid"):
                    continue
                close += 5
        return close

    ##########################################################################
    def pick_target(self):
        """Who should we do the spell to"""
        # Pick three people near where we are
        # TO DO - better this to move to where we can get 3 peeps
        return self.owner

    ##########################################################################
    def cast(self):
        """Do the spell"""
        targets = 3
        for targ in self.owner.arena.my_side(self.owner.side):
            if self.owner.distance(targ) <= 30 / 5:
                if not targ.has_effect("Aid"):
                    print(f"{self.owner} casts Aid on {targ}")
                    targ.add_effect(AidEffect(cause=self.owner))
                    targets -= 1
        return True


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


##############################################################################
##############################################################################
##############################################################################
class TestAid(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        """Set up test"""
        super().setUp()
        self.caster.add_action(Aid())

    ##########################################################################
    def test_cast(self):
        """See what this spell does"""
        self.friend.hp = 5
        self.assertFalse(self.friend.has_effect("Aid"))
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        if self.caster.distance(self.friend) <= 30 / 5:
            self.assertTrue(self.friend.has_effect("Aid"))
            self.assertEqual(self.friend.hp, 10)
            self.assertEqual(self.friend.max_hp, 35)
        else:
            self.assertFalse(self.friend.has_effect("Aid"))
            self.assertEqual(self.friend.hp, 5)
            self.assertEqual(self.friend.max_hp, 30)
        self.assertTrue(self.caster.has_effect("Aid"))
        self.assertEqual(self.caster.max_hp, 35)


# EOF
