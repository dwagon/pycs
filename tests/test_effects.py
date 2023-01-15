#!/usr/bin/env python
""" Tests for damage class"""
import unittest
from pycs.arena import Arena
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.effects import Effects
from pycs.constant import DamageType
from pycs.damage import Damage

##############################################################################
##############################################################################
##############################################################################
class TestEffects(unittest.TestCase):
    """Tests for `effects` class."""

    def setUp(self) -> None:
        self.kwargs = {"str": 6, "int": 7, "dex": 8, "wis": 18, "con": 11, "cha": 15, "side": "a", "hp": 30, "ac": 11}
        self.arena = Arena()
        self.owner = Creature(**self.kwargs)
        self.arena.add_combatant(self.owner, (0, 0))
        self.eff = Effects(owner=self.owner)

    def test_add_effect(self) -> None:
        """Test that adding an effect works"""
        eff = FauxEffect(name="faux")
        someone = Creature(**self.kwargs)

        self.eff.add_effect(source=someone, effect=eff)
        self.assertTrue(self.eff.has_effect("faux"))

        neweff = self.eff["faux"]
        self.assertEqual(neweff, eff)

    def test_hook_being_hit(self) -> None:
        """Test that being hit hook"""
        attacker = Creature(**self.kwargs)
        eff = FauxEffect(name="faux")
        self.owner.add_effect(effect=eff)

        self.owner.hit(Damage(5, DamageType.FIRE), source=attacker, critical=False, atkname="Demo")
        self.assertEqual(self.owner.damage_this_turn[0], Damage(1, DamageType.ACID))


##############################################################################
##############################################################################
##############################################################################
class FauxEffect(Effect):
    """Fake effect for testing"""

    def hook_being_hit(self, dmg: Damage) -> Damage:
        return Damage(1, DamageType.ACID)
