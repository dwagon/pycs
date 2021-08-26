#!/usr/bin/env python

"""Tests for `arena`"""


import unittest
from unittest.mock import Mock
from pycs.creature import Creature
from pycs.constants import Stat
from pycs.constants import Condition
from pycs.constants import MonsterType


##############################################################################
##############################################################################
class TestCreature(unittest.TestCase):
    """Tests for `creature` package."""

    ########################################################################
    def setUp(self):
        """Set up test fixtures, if any."""
        self.arena = Mock(max_x=21, max_y=21)
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 8,
            "wis": 9,
            "con": 11,
            "cha": 15,
            "side": "a",
            "hp": 3,
            "type": MonsterType.UNDEAD,
        }
        self.creat = Creature(self.arena, **kwargs)
        print(self.creat.stats)

    ########################################################################
    def tearDown(self):
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_stat(self):  # NFI why this doesn't work
        """Test stats"""
        self.assertEqual(self.creat.stats[Stat.CON], 11)
        self.assertEqual(self.creat.stat_bonus(Stat.STR), -2)

    ########################################################################
    def test_condition(self):
        """Test conditions"""
        self.assertFalse(self.creat.has_condition(Condition.PRONE))
        self.creat.add_condition(Condition.PRONE)
        self.assertTrue(self.creat.has_condition(Condition.PRONE))
        self.creat.remove_condition(Condition.PRONE)
        self.assertFalse(self.creat.has_condition(Condition.PRONE))

    ######################################################################
    def test_type(self):
        """Test monster type"""
        self.assertTrue(self.creat.is_type(MonsterType.UNDEAD))
        self.assertFalse(self.creat.is_type(MonsterType.HUMANOID))


##############################################################################
##############################################################################
class TestSpellCaster(unittest.TestCase):
    """Tests for spell caster"""

    ########################################################################
    def setUp(self):
        """Set up test fixtures, if any."""
        self.arena = Mock(max_x=21, max_y=21)
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 8,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "side": "a",
            "hp": 3,
            "spellcast_bonus_stat": Stat.WIS,
        }
        self.cleric = Creature(self.arena, **kwargs)

    ########################################################################
    def tearDown(self):
        """Tear down test fixtures, if any."""

    ########################################################################
    def xtest_stuff(self):
        """test"""
        assert isinstance(self.cleric.stats, dict)
        assert len(self.cleric.stats), 6

    ########################################################################
    def xtest_spellcast_details(self):
        """Spell cast details"""
        self.assertEqual(self.cleric.spellcast_bonus_stat, Stat.WIS)
        self.assertEqual(self.cleric.spellcast_save, 14)


# EOF
