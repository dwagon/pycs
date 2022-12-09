"""https://www.dndbeyond.com/spells/hunters-mark"""

from typing import Any, Optional
from unittest.mock import patch
import dice
from pycs.action import Action
from pycs.constant import ActionCategory, DamageType
from pycs.constant import SpellType
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.gear import Shortbow
from pycs.spell import SpellAction
from pycs.spells.spelltest import SpellTest


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
    def __init__(self, **kwargs: Any):
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

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the spell"""
        if self.pick_target():
            return 6
        print("No enemy in range")
        return 0

    ##########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we do the spell to"""
        for enemy in self.owner.pick_closest_enemy():
            if self.owner.distance(enemy) > self.range()[0]:
                continue
            if enemy.has_effect("Hunters Mark"):
                continue
            return enemy
        return None

    ##########################################################################
    def cast(self) -> bool:
        """Do the spell"""
        self.owner.target.add_effect(HuntersMarkEffect(caster=self.owner))
        print(f"Cast Hunters Mark on {self.owner.target}")
        return True

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""
        if self.owner.target:
            print(f"Removing Hunters Mark from {self.owner.target}")
            self.owner.target.remove_effect("Hunters Mark")
            self.owner.target = None


##############################################################################
##############################################################################
##############################################################################
class HuntersMarkEffect(Effect):
    """Hunters Mark Effect"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Hunters Mark", **kwargs)

    ##########################################################################
    def hook_target_additional_damage(
        self, attack: Action, source: Creature, target: Creature
    ) -> tuple[str, int, Optional[DamageType]]:
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
    def setUp(self) -> None:
        """test setup"""
        super().setUp()
        self.caster.add_action(HuntersMark())

    ##########################################################################
    def test_cast(self) -> None:
        """test casting"""
        self.caster.options_this_turn = [ActionCategory.BONUS]
        self.assertFalse(self.enemy.has_effect("Hunters Mark"))
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=False)
        self.assertTrue(self.enemy.has_effect("Hunters Mark"))

    ##########################################################################
    def test_effect(self) -> None:
        """Test the effect of casting the spell"""
        print(self.caster.arena)
        self.caster.moves = 99
        self.caster.options_this_turn = [ActionCategory.BONUS, ActionCategory.ACTION]
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=True)
        self.assertTrue(self.enemy.has_effect("Hunters Mark"))
        self.caster.add_gear(Shortbow())
        self.assertEqual(len(self.enemy.damage_this_turn), 0)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 18
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 5
                self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        print(f"{self.enemy.damage_this_turn=}")
        self.assertEqual(len(self.enemy.damage_this_turn), 2)

    ##########################################################################
    def test_removal(self) -> None:
        """Test the effect gets removed"""
        self.caster.options_this_turn = [ActionCategory.BONUS]
        self.caster.do_stuff(categ=ActionCategory.BONUS, moveto=False)
        self.assertTrue(self.enemy.has_effect("Hunters Mark"))
        self.caster.remove_concentration()
        self.assertFalse(self.enemy.has_effect("Hunters Mark"))


# EOF
