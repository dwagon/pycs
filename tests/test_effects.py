#!/usr/bin/env python
""" Tests for damage class"""
import unittest
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.effects import Effects

##############################################################################
##############################################################################
##############################################################################
class TestEffects(unittest.TestCase):
    """Tests for `effects` class."""
    def setUp(self) -> None:
        self.kwargs = {
            "str": 6,
            "int": 7,
            "dex": 8,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "side": "a",
            "hp": 30,
            "ac": 11}
        owner = Creature(**self.kwargs)
        self.eff = Effects(owner=owner)

    def test_add_effect(self) -> None:
        eff = FauxEffect(name="faux")
        someone = Creature(**self.kwargs)

        self.eff.add_effect(source=someone, effect=eff)
        self.assertTrue(self.eff.has_effect("faux"))

        neweff = self.eff["faux"]
        self.assertEqual(neweff, eff)


##############################################################################
##############################################################################
##############################################################################
class FauxEffect(Effect):
    pass