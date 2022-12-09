""" https://www.dndbeyond.com/monsters/hobgoblin"""
from typing import Any, Optional
import unittest
from unittest.mock import patch
import colors
import dice
from pycs.action import Action
from pycs.arena import Arena
from pycs.effect import Effect
from pycs.gear import Longbow
from pycs.gear import Longsword
from pycs.gear import Chainmail
from pycs.gear import Shield
from pycs.constant import DamageType, MonsterType
from pycs.creature import Creature
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Hobgoblin(Monster):
    """Hobgoblin"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "2d8+2",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 13,
                "dex": 12,
                "con": 12,
                "int": 10,
                "wis": 10,
                "cha": 9,
                "gear": [Longsword(), Longbow(), Chainmail(), Shield()],
                "effects": [MartialAdvantage()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a hobgoblin looks like on the arena"""
        if self.is_alive():
            return colors.green("h")
        return colors.green("h", bg="red")


##############################################################################
##############################################################################
##############################################################################
class MartialAdvantage(Effect):
    """Martial Advantage. Once per turn, the hobgoblin can deal an
    extra 7 (2d6) damage to a creature it hits with a weapon attack if
    that creature is within 5 feet of an ally of the hobgoblin that
    isn't incapacitated."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        self.used_this_turn = False
        super().__init__("Martial Advantage", **kwargs)

    ##########################################################################
    def hook_start_turn(self) -> None:
        """Start turn effects"""
        self.used_this_turn = False

    ##########################################################################
    def hook_source_additional_damage(
        self, attack: Action, source: Creature, target: Creature
    ) -> tuple[str, int, Optional[DamageType]]:
        """Additional damage?"""
        if self.used_this_turn:
            return ("", 0, None)
        allies = [_ for _ in source.pick_closest_friends() if _ != source and _.distance(target) <= 1]
        if allies:
            self.used_this_turn = True
            return ("2d6", 0, None)
        return ("", 0, None)


##############################################################################
##############################################################################
##############################################################################
class TestHobgoblin(unittest.TestCase):
    """Test Hobgoblin"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Hobgoblin(side="a")
        self.arena.add_combatant(self.beast, coords=(1, 1))
        self.victim = Monster(str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b")
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_martial(self) -> None:
        """Test Martial Advantage"""
        friend = Hobgoblin(side="a")
        self.arena.add_combatant(friend, coords=(1, 3))
        sword = self.beast.pick_action_by_name("Longsword")
        assert sword is not None
        self.beast.target = self.victim
        self.assertFalse(self.beast.effects["Martial Advantage"].used_this_turn)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 1  # Sword and MartAdv damage
                sword.perform_action()
                self.assertEqual(self.victim.hp, 47)  # 2 for sword, 1 for MA
                self.assertTrue(self.beast.effects["Martial Advantage"].used_this_turn)
                sword.perform_action()
                self.assertEqual(self.victim.hp, 45)  # No martial advantage

    ##########################################################################
    def test_martial_miss(self) -> None:
        """Test Martial Advantage not applying"""
        sword = self.beast.pick_action_by_name("Longsword")
        assert sword is not None
        self.beast.target = self.victim
        self.assertFalse(self.beast.effects["Martial Advantage"].used_this_turn)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 1  # Sword and MartAdv damage
                sword.perform_action()
                self.assertEqual(self.victim.hp, 48)  # 2 for sword
                self.assertFalse(self.beast.effects["Martial Advantage"].used_this_turn)

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 18)


# EOF
