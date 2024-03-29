"""https://www.dndbeyond.com/spells/healing-word"""

from typing import Any, Optional
from pycs.creature import Creature
from pycs.spell import SpellAction
from pycs.spell import pick_heal_target
from pycs.spell import healing_heuristic
from pycs.constant import SpellType
from pycs.constant import ActionCategory
from pycs.spells.spelltest import SpellTest


##############################################################################
class HealingWord(SpellAction):
    """A creature of your choice that you can see within range regains
    hit points equal to 1d4 + your spellcasting ability modifier. This
    spell has no effect on undead or constructs.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, the healing increases by 1d4 for each slot
    level above 1st."""

    def __init__(self, **kwargs: Any):
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
    def cast(self) -> bool:
        """Do the spell"""
        self.owner.target.heal("1d4", self.spell_modifier(self.owner))
        return True

    ########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we target"""
        return pick_heal_target(self.owner)

    ########################################################################
    def heuristic(self) -> int:
        """Should we cast this"""
        return healing_heuristic(self.owner, self)


##############################################################################
##############################################################################
##############################################################################
class TestHealingWord(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self) -> None:
        super().setUp()
        self.caster.add_action(HealingWord())

    ##########################################################################
    def test_cast(self) -> None:
        """See what this spell does"""
        self.friend.hp = 5
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertGreater(self.friend.hp, 5)


# EOF
