#!/usr/bin/env python
""" Tests for damage class"""
import unittest
from pycs.constant import DamageType

from pycs.damage import Damage

##############################################################################
class TestDamage(unittest.TestCase):
    """Tests for `damage` class."""

    def test_equal(self) -> None:
        d1 = Damage(10, DamageType.RADIANT)
        d2 = Damage(10, DamageType.RADIANT)
        self.assertEqual(d1, d2)

        d3 = Damage(11, DamageType.RADIANT)
        self.assertNotEqual(d1, d3)

        d4 = Damage(10, DamageType.FIRE)
        self.assertNotEqual(d1, d4)

        self.assertNotEqual(d1, 33)

    def test_divide(self) -> None:
        d1 = Damage(10, DamageType.FIRE)
        d1 //= 2
        self.assertEqual(d1.hp, 5)

    def test_boolean(self) -> None:
        d1 = Damage(10, DamageType.ACID)
        self.assertTrue(d1)
        d2 = Damage(0, DamageType.ACID)
        self.assertFalse(d2)

    def test_sub(self) -> None:
        d1 = Damage(12, DamageType.PSYCHIC)
        d1 -= 5
        self.assertEqual(d1, Damage(12 - 5, DamageType.PSYCHIC))


# EOF
