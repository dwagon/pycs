#!/usr/bin/env python

"""Tests for `monster`"""


import unittest
from unittest.mock import Mock
from pycs.arena import Arena
from pycs.constant import Condition, Stat
from pycs.damage import Damage
from pycs.monster import Monster
from pycs.creature import DamageType


##############################################################################
##############################################################################
##############################################################################
class TestMonster(unittest.TestCase):
    """Tests for `monster` class."""

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
        self.creat = Monster(**kwargs)
        self.arena.add_combatant(self.creat)

    ########################################################################
    def tearDown(self) -> None:
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_is_alive(self) -> None:
        """is_alive testing"""
        self.creat.hp = 10
        self.assertTrue(self.creat.is_alive())
        self.creat.hit(
            Damage(15, DamageType.ACID),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertFalse(self.creat.is_alive())

    ########################################################################
    def test_dieing(self) -> None:
        """Test death"""
        self.creat.hp = 10
        self.creat.hit(
            Damage(15, DamageType.ACID),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertTrue(self.creat.has_condition(Condition.DEAD))
        self.assertFalse(self.creat.has_condition(Condition.OK))


# EOF
