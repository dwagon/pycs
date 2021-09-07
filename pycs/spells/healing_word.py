"""https://www.dndbeyond.com/spells/healing-word"""

from pycs.spell import SpellAction
from pycs.spell import pick_heal_target
from pycs.spell import healing_heuristic
from pycs.constant import SpellType
from pycs.constant import ActionCategory
from .spelltest import SpellTest


##############################################################################
class HealingWord(SpellAction):
    """A creature of your choice that you can see within range regains
    hit points equal to 1d4 + your spellcasting ability modifier. This
    spell has no effect on undead or constructs.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, the healing increases by 1d4 for each slot
    level above 1st."""

    def __init__(self, **kwargs):
        name = "Healing Word"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 60,
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def cast(self, caster):
        """Do the spell"""
        caster.target.heal("1d4", self.modifier(caster))
        return True

    ########################################################################
    def pick_target(self, doer):
        """Who should we target"""
        return pick_heal_target(doer)

    ########################################################################
    def heuristic(self, doer):
        """Should we cast this"""
        return healing_heuristic(doer, self)


##############################################################################
##############################################################################
##############################################################################
class Test_HealingWord(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        super().setUp()
        self.caster.add_action(HealingWord())

    ##########################################################################
    def test_cast(self):
        """See what this spell does"""
        self.friend.hp = 5
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertGreater(self.friend.hp, 5)


# EOF
