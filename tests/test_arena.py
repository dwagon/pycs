#!/usr/bin/env python

"""Tests for `arena`"""


import unittest
from unittest.mock import Mock
from pycs.arena import Arena


##############################################################################
##############################################################################
class TestArena(unittest.TestCase):
    """Tests for `arena` package."""

    ########################################################################
    def setUp(self):
        """Set up test fixtures, if any."""
        self.arena = Arena(max_x=21, max_y=21)
        self.critter1 = Mock()
        self.critter2 = Mock()
        self.critter3 = Mock()
        self.critter4 = Mock()

    ########################################################################
    def tearDown(self):
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_distance(self):
        """Test distance and grid placement."""
        self.assertEqual(self.arena.max_x, 21)
        self.assertIsNone(self.arena[(0, 0)])
        self.arena.add_combatant(self.critter1, (0, 0))
        self.arena.add_combatant(self.critter2, (9, 0))
        self.assertEqual(self.critter1.coords, (0, 0))
        self.assertEqual(self.critter2.coords, (9, 0))
        self.assertIsNotNone(self.arena[(0, 0)])
        self.assertEqual(self.arena[(9, 0)], self.critter2)

        dist = self.arena.distance(self.critter1, self.critter2)
        self.assertEqual(dist, 9)

    ########################################################################
    def test_closest_friend(self):
        """Test pick_closest_friends()"""
        self.arena.add_combatant(self.critter1, (0, 0))
        self.arena.add_combatant(self.critter2, (1, 1))
        self.arena.add_combatant(self.critter3, (2, 2))
        self.arena.add_combatant(self.critter4, (3, 3))
        self.critter1.side = "a"
        self.critter2.side = "b"
        self.critter3.side = "a"
        self.critter4.side = "a"
        friends = self.arena.pick_closest_friends(self.critter1)
        self.assertEqual(friends, [self.critter3, self.critter4])

    ########################################################################
    def test_closest_enemy(self):
        """Test pick_closest_enemy()"""
        self.arena.add_combatant(self.critter1, (0, 0))
        self.arena.add_combatant(self.critter2, (1, 1))
        self.arena.add_combatant(self.critter3, (2, 2))
        self.arena.add_combatant(self.critter4, (3, 3))
        self.critter1.side = "a"
        self.critter2.side = "b"
        self.critter3.side = "b"
        self.critter4.side = "a"
        enemy = self.arena.pick_closest_enemy(self.critter1)
        self.assertEqual(enemy, [self.critter2, self.critter3])


# EOF
