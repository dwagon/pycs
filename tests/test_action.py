#!/usr/bin/env python

"""Tests for `actions`"""


import unittest
from unittest.mock import Mock, patch, call
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.constant import DamageType
from pycs.creature import Creature
from pycs.action import Action
from pycs.effect import Effect
from pycs.equipment import Equipment


##############################################################################
##############################################################################
##############################################################################
class TestAction(unittest.TestCase):
    """Tests for `actions` package."""

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
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 8,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "side": "b",
            "hp": 10,
        }
        self.source = Creature(self.arena, **kwargs)

    ########################################################################
    def tearDown(self):
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_check_criticals(self):
        """Test check_criticals"""
        act = DummyAction()
        self.source.add_action(act)
        self.assertEqual(act.check_criticals(10), (False, False))
        self.assertEqual(act.check_criticals(1), (False, True))
        self.assertEqual(act.check_criticals(20), (True, False))

    ########################################################################
    def test_roll_to_hit(self):
        """test roll_to_hit()"""
        act = DummyAction()
        self.source.add_action(act)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 18
            to_hit, crit_hit, crit_miss = act.roll_to_hit(self.creat)
        self.assertEqual(to_hit, 18 + 5)
        self.assertFalse(crit_hit)
        self.assertFalse(crit_miss)

    ########################################################################
    def test_calculate_to_hit(self):
        """Test calculate_to_hit()"""
        self.source.add_effect(DummyEffect())
        act = DummyAction()
        self.source.add_action(act)
        to_hit, msg = act.calculate_to_hit("msg_0", 10, self.creat)
        self.assertEqual(to_hit, 10 + 5 + 3)
        self.assertEqual(msg, "Creature rolled 10msg_0 +5 (+3 from Dummy Effect)")

    ########################################################################
    def test_buff_attack_damage(self):
        """Test buff_attack_damage()"""
        act = DummyAction()
        self.source.add_action(act)
        with patch.object(Creature, "hit") as mock:
            self.source.add_effect(DummyEffect())
            self.source.add_action(act)
            self.creat.add_effect(DummyEffect())
            act.buff_attack_damage(self.creat)

            self.assertEqual(
                mock.call_args_list[0],
                call(
                    2,
                    DamageType.FIRE,
                    self.source,
                    critical=False,
                    atkname="Dummy Effect",
                ),
            )
            self.assertEqual(
                mock.call_args_list[1],
                call(
                    4,
                    DamageType.ACID,
                    self.source,
                    critical=False,
                    atkname="Dummy Effect",
                ),
            )


############################################################################
class DummyEffect(Effect):
    """Test effect"""

    def __init__(self, **kwargs):
        super().__init__("Dummy Effect", **kwargs)

    def hook_source_additional_damage(self, attack, source, target):
        return ("", 2, DamageType.FIRE)

    def hook_target_additional_damage(self, attack, source, target):
        return ("", 4, DamageType.ACID)

    def hook_attack_to_hit(self, **kwargs):
        return 3


############################################################################
############################################################################
############################################################################
class DummyAction(Action):
    """Test action"""

    def __init__(self, **kwargs):
        super().__init__("Dummy Action", **kwargs)

    def perform_action(self):
        """Required"""

    def modifier(self, _):
        return 5

    def heuristic(self):
        return 1


############################################################################
class DummyGear(Equipment):
    """Test gear"""

    def __init__(self, **kwargs):
        super().__init__("Dummy Gear", **kwargs)


# EOF
