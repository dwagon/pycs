#!/usr/bin/env python

"""Tests for `equipment`"""


import unittest
from unittest.mock import Mock
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.gear import Dagger
from pycs.gear import Javelin
from pycs.gear import Leather
from pycs.gear import PotionHealing
from pycs.gear import Shield
from pycs.gear import Splint


##############################################################################
##############################################################################
##############################################################################
class TestEquipment(unittest.TestCase):
    """Tests for `equipment` package."""

    ########################################################################
    def setUp(self) -> None:
        """Set up test fixtures, if any."""
        self.arena = Mock(max_x=21, max_y=21)
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 13,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "side": "a",
            "hp": 30,
            "type": MonsterType.UNDEAD,
            "spellcast_bonus_stat": Stat.WIS,
        }
        self.creat = Creature(**kwargs)

    ########################################################################
    def tearDown(self) -> None:
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_weapon(self) -> None:
        """Test adding weapons"""
        self.assertEqual(len(self.creat.actions), 0)
        self.creat.add_gear(Javelin(ammo=3))
        self.assertEqual(len(self.creat.actions), 1)
        jav_action = self.creat.actions[0]
        self.assertEqual(jav_action.name, "Javelin")
        self.assertEqual(jav_action.ammo, 3)

    ########################################################################
    def test_finesse_weapon(self) -> None:
        """Test weapons with finesse"""
        self.creat.add_gear(Dagger())
        att = self.creat.pick_action_by_name("Dagger")
        assert att is not None
        self.creat.stats[Stat.STR] = 9
        self.creat.stats[Stat.DEX] = 19
        self.assertEqual(att.use_stat, Stat.DEX)
        self.creat.stats[Stat.STR] = 19
        self.creat.stats[Stat.DEX] = 9
        self.assertEqual(att.use_stat, Stat.STR)

    ########################################################################
    def test_potion(self) -> None:
        """Test adding potion"""
        self.assertEqual(len(self.creat.bonus_actions), 0)
        self.creat.add_gear(PotionHealing(ammo=1))
        self.assertEqual(len(self.creat.bonus_actions), 1)
        hp_action = self.creat.bonus_actions[0]
        self.assertEqual(hp_action.name, "Drink Potion of Healing")
        self.assertEqual(hp_action.ammo, 1)
        self.creat.hp = 10
        self.creat.target = self.creat
        self.creat.do_action(hp_action)
        self.assertEqual(hp_action.ammo, 0)
        self.assertGreater(self.creat.hp, 10)

    ########################################################################
    def test_armour(self) -> None:
        """Test adding armour"""
        self.assertEqual(self.creat.ac, 11)
        self.creat.add_gear(Leather())
        self.assertEqual(self.creat.ac, 12)

    ########################################################################
    def test_heavy_armour(self) -> None:
        """Test adding heavy armour"""
        self.assertEqual(self.creat.ac, 11)
        self.creat.add_gear(Splint())
        self.assertEqual(self.creat.ac, 17)

    ########################################################################
    def test_armour_shield(self) -> None:
        """Test armour and shield combo"""
        self.assertEqual(self.creat.ac, 11)
        self.creat.add_gear(Leather())
        self.assertEqual(self.creat.ac, 12)
        self.creat.add_gear(Shield())
        self.assertEqual(self.creat.ac, 14)

    ########################################################################
    def test_magic_armour_shield(self) -> None:
        """Test magic armour and shield combo"""
        self.assertEqual(self.creat.ac, 11)
        self.creat.add_gear(Leather(magic_bonus=1))
        self.assertEqual(self.creat.ac, 13)
        self.creat.add_gear(Shield(magic_bonus=2))
        self.assertEqual(self.creat.ac, 17)


# EOF