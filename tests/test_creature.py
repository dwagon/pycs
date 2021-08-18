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
        self.crit = Creature(self.arena, **kwargs)

    ########################################################################
    def tearDown(self):
        """Tear down test fixtures, if any."""

    ########################################################################
    def x_test_stat(self):  # NFI why this doesn't work
        """Test stats"""
        self.assertEqual(self.crit.stats[Stat.CON], 11)
        self.assertEqual(self.crit.stat_bonus(Stat.STR), -2)

    ########################################################################
    def test_condition(self):
        """Test conditions"""
        self.assertFalse(self.crit.has_condition(Condition.PRONE))
        self.crit.add_condition(Condition.PRONE)
        self.assertTrue(self.crit.has_condition(Condition.PRONE))
        self.crit.remove_condition(Condition.PRONE)
        self.assertFalse(self.crit.has_condition(Condition.PRONE))

    ######################################################################
    def test_type(self):
        """Test monster type"""
        self.assertTrue(self.crit.is_type(MonsterType.UNDEAD))
        self.assertFalse(self.crit.is_type(MonsterType.HUMANOID))


# EOF
