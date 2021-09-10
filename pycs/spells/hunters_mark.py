"""https://www.dndbeyond.com/spells/hunters-mark"""

from unittest.mock import patch
import dice
from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.gear import Shortbow
from pycs.spell import SpellAction
from .spelltest import SpellTest


##############################################################################
##############################################################################
##############################################################################
class HuntersMark(SpellAction):
    """You choose a creature you can see within range and mystically
    mark it as your quarry. Until the spell ends, you deal an extra 1d6
    damage to the target whenever you hit it with a weapon attack, and
    you have advantage on any Wisdom (Perception) or Wisdom (Survival)
    check you make to find it. If the target drops to 0 hit points
    before this spell ends, you can use a bonus action on a subsequent
    turn of yours to mark a new creature.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd or 4th level, you can maintain your concentration on the spell
    for up to 8 hours. When you use a spell slot of 5th level or higher,
    you can maintain your concentration on the spell for up to 24
    hours."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Hunters Mark"
        kwargs.update(
            {
                "category": ActionCategory.BONUS,
                "concentration": SpellType.CONCENTRATION,
                "level": 1,
                "reach": 90,
                "type": SpellType.BUFF,
            }
        )
        super().__init__(name, **kwargs)
        self._victim = None

    ##########################################################################
    def heuristic(self):
        """Should we do the spell"""
        for enemy in self.owner.pick_closest_enemy():
            if self.owner.distance(enemy) > self.range()[0]:
                continue
            if enemy.has_effect("Hunters Mark"):
                return 0
            return 6
        print("No enemy in range")
        return 0

    ##########################################################################
    def pick_target(self):
        """Who should we do the spell to"""
        for enemy in self.owner.pick_closest_enemy():
            if self.owner.distance(enemy) > self.range()[0]:
                continue
            self.target = enemy
            return enemy
        return None

    ##########################################################################
    def cast(self):
        """Do the spell"""
        self.target.add_effect(HuntersMarkEffect(caster=self.owner))
        self._victim = self.target

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""
        if self._victim:
            print(f"Removing Hunters Mark from {self._victim}")
            self._victim.remove_effect("Hunters Mark")
            self._victim = None


##############################################################################
##############################################################################
##############################################################################
class HuntersMarkEffect(Effect):
    """Hunters Mark Effect"""

    ##########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Hunters Mark", **kwargs)

    ##########################################################################
    def hook_target_additional_damage(self, _, source, target):
        """More damage"""
        if source == self.caster:
            return ("1d6", 0, None)
        return ("", 0, None)


##############################################################################
##############################################################################
##############################################################################
class TestHuntersMark(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        """test setup"""
        super().setUp()
        self.caster.add_action(HuntersMark())

    ##########################################################################
    def test_cast(self):
        """test casting"""
        self.caster.options_this_turn = [ActionCategory.BONUS]
        self.assertFalse(self.enemy.has_effect("Hunters Mark"))
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=False)
        self.assertTrue(self.enemy.has_effect("Hunters Mark"))

    ##########################################################################
    def test_effect(self):
        """Test the effect of casting the spell"""
        self.caster.moves = 99
        self.caster.options_this_turn = [ActionCategory.BONUS, ActionCategory.ACTION]
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=True)
        self.caster.add_gear(Shortbow())
        self.assertEqual(len(self.enemy.damage_this_turn), 0)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 18
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 5
                self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertEqual(len(self.enemy.damage_this_turn), 2)

    ##########################################################################
    def test_removal(self):
        """Test the effect gets removed"""
        self.caster.options_this_turn = [ActionCategory.BONUS]
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=False)
        self.assertTrue(self.enemy.has_effect("Hunters Mark"))
        self.caster.remove_concentration()
        self.assertFalse(self.enemy.has_effect("Hunters Mark"))


# EOF
