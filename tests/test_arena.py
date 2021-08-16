#!/usr/bin/env python

"""Tests for `arena`"""


import unittest
from unittest.mock import Mock
from pycs.arena import Arena


##############################################################################
##############################################################################
class TestArena(unittest.TestCase):
    """Tests for `arena` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.arena = Arena(max_x=21, max_y=21)
        self.critter1 = Mock()
        self.critter2 = Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        self.assertEqual(self.arena.max_x, 21)
        self.arena.add_combatant(self.critter1, (0, 0))
        self.arena.add_combatant(self.critter2, (9, 0))
        self.assertEqual(self.critter1.coords, (0, 0))
        self.assertEqual(self.critter2.coords, (9, 0))
        dist = self.arena.distance(self.critter1, self.critter2)
        self.assertEqual(dist, 9)


# EOF
