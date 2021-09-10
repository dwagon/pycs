"""https://www.dndbeyond.com/spells/cure-wounds"""

from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.spell import SpellAction
from pycs.spell import healing_heuristic
from pycs.spell import pick_heal_target
from .spelltest import SpellTest


##############################################################################
class CureWounds(SpellAction):
    """A creature you touch regains a number of hit points equal to 1d8
    + your spellcasting ability modifier. This spell has no effect on
    undead or constructs."""

    ########################################################################
    def __init__(self, **kwargs):
        name = "Cure Wounds"
        kwargs.update(
            {
                "type": SpellType.HEALING,
                "reach": 5,
                "level": 1,
            }
        )
        super().__init__(name, **kwargs)

    ########################################################################
    def cast(self):
        """Do the spell"""
        self.owner.target.heal("1d8", self.modifier(self.owner))
        return True

    ########################################################################
    def pick_target(self):
        """Who should we target"""
        return pick_heal_target(self.owner)

    ########################################################################
    def heuristic(self):
        """Should we cast this"""
        return healing_heuristic(self.owner, self)


##############################################################################
##############################################################################
##############################################################################
class TestCureWounds(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        """setup tests"""
        super().setUp()
        self.caster.add_action(CureWounds())

    ##########################################################################
    def test_cast(self):
        """See what this spell does"""
        self.friend.hp = 5
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertGreater(self.friend.hp, 5)


# EOF
