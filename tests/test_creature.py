#!/usr/bin/env python

"""Tests for `creature`"""


import unittest
from unittest.mock import Mock, patch
from pycs.constant import Condition
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.attack import MeleeAttack
from pycs.creature import DamageType
from pycs.effect import Effect


##############################################################################
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
            "wis": 18,
            "con": 11,
            "cha": 15,
            "side": "a",
            "hp": 30,
            "ac": 11,
            "type": MonsterType.UNDEAD,
            "spellcast_bonus_stat": Stat.WIS,
        }
        self.creat = Creature(self.arena, **kwargs)

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
        self.assertFalse(self.creat.has_condition(Condition.PRONE, Condition.BLINDED))
        self.creat.add_condition(Condition.PRONE)
        self.assertTrue(self.creat.has_condition(Condition.PRONE))
        self.creat.remove_condition(Condition.PRONE)
        self.assertFalse(self.creat.has_condition(Condition.PRONE))

    ######################################################################
    def test_type(self):
        """Test monster type"""
        self.assertTrue(self.creat.is_type(MonsterType.UNDEAD))
        self.assertFalse(self.creat.is_type(MonsterType.HUMANOID))

    ########################################################################
    def test_spellcast_details(self):
        """Spell cast details"""
        self.assertEqual(self.creat.spellcast_bonus_stat, Stat.WIS)
        self.assertEqual(self.creat.spellcast_save, 14)

    ########################################################################
    def test_ac(self):
        """Test AC calculations"""
        self.assertEqual(self.creat.ac, 11)
        self.creat.add_effect(MockACEffect("AC Effect"))
        self.assertTrue(self.creat.has_effect("AC Effect"))
        self.assertEqual(self.creat.ac, 9)
        self.creat.remove_effect("AC Effect")
        self.assertFalse(self.creat.has_effect("AC Effect"))

    ########################################################################
    def test_heal(self):
        """Test creature healing"""
        self.assertEqual(self.creat.max_hp, 30)
        self.assertEqual(self.creat.hp, 30)
        self.creat.hp = 10
        healed = self.creat.heal("", 9)
        self.assertEqual(healed, 9)
        self.assertEqual(self.creat.hp, 19)
        healed = self.creat.heal("d4", 0)
        self.assertLessEqual(healed, 4)
        self.assertGreaterEqual(healed, 1)
        self.assertEqual(self.creat.hp, 19 + healed)
        healed = self.creat.heal("d4", 99)
        self.assertEqual(self.creat.hp, self.creat.max_hp)

    ########################################################################
    def test_add_action(self):
        """test add_action"""
        self.creat.add_action(MeleeAttack("alpha"))
        self.creat.add_action(MeleeAttack("beta"))
        act = self.creat.pick_attack_by_name("alpha")
        self.assertEqual(act.name, "alpha")
        act = self.creat.pick_attack_by_name("foo")
        self.assertIsNone(act)

    ########################################################################
    def test_is_alive(self):
        """is_alive testing"""
        self.creat.hp = 10
        self.assertTrue(self.creat.is_alive())
        self.creat.hp = 0
        self.assertFalse(self.creat.is_alive())

    ########################################################################
    def test_saving_throw(self):
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

    ########################################################################
    def test_roll_initiative(self):
        """Test rolling initiative"""
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 10
            init = self.creat.roll_initiative()
            self.assertEqual(init, 9)  # Dex -1

    ########################################################################
    def test_hit(self):
        """Test creature hurting"""
        self.creat.hp = 30
        self.creat.hit(
            5, dmg_type=DamageType.ACID, source=Mock(), critical=False, atkname="attack"
        )
        self.assertEqual(self.creat.hp, 25)
        # Vulnerable = twice damaage
        self.creat.vulnerable.append(DamageType.PIERCING)
        self.creat.hit(
            5,
            dmg_type=DamageType.PIERCING,
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 15)
        # Immunity = no damage
        self.creat.immunity.append(DamageType.FIRE)
        self.creat.hit(
            5,
            dmg_type=DamageType.FIRE,
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 15)
        # Resistant = half damage
        self.creat.resistant.append(DamageType.NECROTIC)
        self.creat.hit(
            10,
            dmg_type=DamageType.NECROTIC,
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 10)
        self.creat.hit(
            25,
            dmg_type=DamageType.ACID,
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.state, "UNCONSCIOUS")
        self.assertEqual(self.creat.hp, 0)


############################################################################
class MockACEffect(Effect):
    """Test AC modification"""

    def hook_ac_modifier(self, target):
        return -2


# EOF
