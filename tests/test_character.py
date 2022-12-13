#!/usr/bin/env python

"""Tests for `character`"""


import unittest
from unittest.mock import Mock, patch
import dice
from pycs.arena import Arena
from pycs.constant import Condition
from pycs.constant import Stat
from pycs.character import Character
from pycs.creature import Creature
from pycs.creature import DamageType
from pycs.damage import Damage


##############################################################################
##############################################################################
##############################################################################
class TestCharacter(unittest.TestCase):
    """Tests for `character` package."""

    ########################################################################
    def setUp(self) -> None:
        """Set up test fixtures, if any."""
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 8,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "side": "a",
            "hp": 30,
            "ac": 11,
            "stat_prof": [Stat.CHA],
            "spellcast_bonus_stat": Stat.WIS,
        }
        self.arena = Arena()
        self.creat = Character(**kwargs)
        self.arena.add_combatant(self.creat)

    ########################################################################
    def tearDown(self) -> None:
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_saving_throw(self) -> None:
        """Test saving_throw"""
        # If unconscious - auto fail STR saves
        self.creat.add_condition(Condition.UNCONSCIOUS)
        res = self.creat.saving_throw(Stat.STR, 1)
        self.assertFalse(res)
        self.creat.remove_condition(Condition.UNCONSCIOUS)

        # Test succeeding save
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            res = self.creat.saving_throw(Stat.WIS, 20)
            self.assertTrue(res)

        # Test failing save
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            res = self.creat.saving_throw(Stat.WIS, 20)
            self.assertFalse(res)

        # Test stat proficiency
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 10
            res = self.creat.saving_throw(Stat.CHA, 11)
            self.assertTrue(res)

    ########################################################################
    def test_death_saving(self) -> None:
        """Test death saving throws"""
        self.creat.hp = 10
        self.creat.hit(
            Damage(15, DamageType.ACID),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertTrue(self.creat.has_condition(Condition.UNCONSCIOUS))
        self.assertFalse(self.creat.has_condition(Condition.OK))
        self.assertEqual(self.creat.death_saves, 0)
        # Does the creature come back after a 20?
        with patch.object(dice, "roll") as mock:
            mock.return_value = 20
            self.creat.start_turn()
            self.assertEqual(self.creat.hp, 1)
        self.assertFalse(self.creat.has_condition(Condition.UNCONSCIOUS))
        self.assertTrue(self.creat.has_condition(Condition.OK))

        self.creat.hit(
            Damage(15, DamageType.ACID),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 0)

        with patch.object(dice, "roll") as mock:
            mock.return_value = 2
            self.creat.start_turn()
            self.assertEqual(self.creat.death_saves, 1)
        # Test death
        with patch.object(dice, "roll") as mock:
            mock.return_value = 1
            self.creat.start_turn()
            self.assertEqual(self.creat.death_saves, 3)
            self.assertTrue(self.creat.has_condition(Condition.DEAD))


# EOF
