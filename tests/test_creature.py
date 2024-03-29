#!/usr/bin/env python

"""Tests for `creature`"""


import unittest
from unittest.mock import Mock, patch
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.constant import Condition
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.creature import DamageType
from pycs.damage import Damage
from pycs.effect import Effect
from pycs.gear import Scimitar


##############################################################################
##############################################################################
##############################################################################
class TestCreature(unittest.TestCase):
    """Tests for `creature` package."""

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
            "type": MonsterType.UNDEAD,
            "spellcast_bonus_stat": Stat.WIS,
        }
        self.arena = Arena()
        self.creat = Creature(**kwargs)
        self.arena.add_combatant(self.creat)

    ########################################################################
    def tearDown(self) -> None:
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_stat(self) -> None:  # NFI why this doesn't work
        """Test stats"""
        self.assertEqual(self.creat.stats[Stat.CON], 11)
        self.assertEqual(self.creat.stat_bonus(Stat.STR), -2)

    ########################################################################
    def test_condition(self) -> None:
        """Test conditions"""
        self.assertFalse(self.creat.has_condition(Condition.PRONE, Condition.BLINDED))
        self.creat.add_condition(Condition.PRONE)
        self.assertTrue(self.creat.has_condition(Condition.PRONE))
        self.creat.remove_condition(Condition.PRONE)
        self.assertFalse(self.creat.has_condition(Condition.PRONE))

    ######################################################################
    def test_type(self) -> None:
        """Test monster type"""
        self.assertTrue(self.creat.is_type(MonsterType.UNDEAD))
        self.assertFalse(self.creat.is_type(MonsterType.HUMANOID))

    ########################################################################
    def test_spellcast_details(self) -> None:
        """Spell cast details"""
        self.assertEqual(self.creat.spellcast_bonus_stat, Stat.WIS)
        self.assertEqual(self.creat.spellcast_save, 14)

    ########################################################################
    def test_pick_action_by_name(self) -> None:
        """Test pick_action_by_name()"""
        alpha = MeleeAttack("alpha")
        beta = RangedAttack("beta")
        self.creat.add_action(alpha)
        self.creat.add_action(beta)
        atk = self.creat.pick_action_by_name("alpha")
        self.assertEqual(atk, alpha)
        atk2 = self.creat.pick_action_by_name("beta")
        self.assertEqual(atk2, beta)
        atk3 = self.creat.pick_action_by_name("gamma")
        self.assertIsNone(atk3)

    ########################################################################
    def test_add_gear(self) -> None:
        """Test add_gear()"""
        self.assertEqual(self.creat.gear, [])
        self.assertEqual(self.creat.actions, [])
        self.creat.add_gear(Scimitar())
        self.assertEqual(self.creat.gear[0].name, "Scimitar")
        self.assertEqual(self.creat.gear[0].owner, self.creat)
        self.assertEqual(self.creat.actions[0].name, "Scimitar")

    ########################################################################
    def test_ac(self) -> None:
        """Test AC calculations"""
        self.assertEqual(self.creat.ac, 11)
        eff = MockACEffect("AC Effect")
        self.creat.add_effect(eff)
        self.assertTrue(self.creat.has_effect("AC Effect"))
        self.assertEqual(self.creat.ac, 9)
        self.creat.remove_effect(eff)
        self.assertFalse(self.creat.has_effect("AC Effect"))

    ########################################################################
    def test_heal(self) -> None:
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
    def test_add_action(self) -> None:
        """test add_action"""
        self.creat.add_action(MeleeAttack("alpha"))
        self.creat.add_action(MeleeAttack("beta"))
        act = self.creat.pick_action_by_name("alpha")
        assert act is not None
        self.assertEqual(act.name, "alpha")
        act = self.creat.pick_action_by_name("foo")
        self.assertIsNone(act)

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
    def test_grapple(self) -> None:
        """Test grappling"""
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
            "type": MonsterType.UNDEAD,
            "spellcast_bonus_stat": Stat.WIS,
        }
        victim = Creature(**kwargs)
        self.arena.add_combatant(victim)
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [19, 1]
            self.creat.grapple(victim, 9)
        self.assertTrue(victim.has_condition(Condition.GRAPPLED))
        self.assertEqual(self.creat.has_grappled, victim)
        self.assertEqual(victim.grappled_by, self.creat)
        self.assertEqual(victim.escape_grapple_dc, 9)

    ########################################################################
    def test_roll_initiative(self) -> None:
        """Test rolling initiative"""
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 10
            init = self.creat.roll_initiative()
            self.assertEqual(init, 9)  # Dex -1

    ########################################################################
    def test_hit(self) -> None:
        """Test creature hurting"""
        self.creat.hp = 30
        self.creat.hit(Damage(5, DamageType.ACID), source=Mock(), critical=False, atkname="attack")
        self.assertEqual(self.creat.hp, 25)
        # Vulnerable = twice damaage
        self.creat.vulnerable.append(DamageType.PIERCING)
        self.creat.hit(
            Damage(5, DamageType.PIERCING),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 15)
        # Immunity = no damage
        self.creat.immunity.append(DamageType.FIRE)
        self.creat.hit(
            Damage(5, DamageType.FIRE),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 15)
        # Resistant = half damage
        self.creat.resistant.append(DamageType.NECROTIC)
        self.creat.hit(
            Damage(10, DamageType.NECROTIC),
            source=Mock(),
            critical=False,
            atkname="attack",
        )
        self.assertEqual(self.creat.hp, 10)


############################################################################
class MockACEffect(Effect):
    """Test AC modification"""

    def hook_ac_modifier(self) -> int:
        return -2


# EOF
