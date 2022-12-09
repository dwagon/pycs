#!/usr/bin/env python

"""Tests for `actions`"""


from typing import Any, Optional
import unittest
from unittest.mock import patch, call
from pycs.action import Action
from pycs.arena import Arena
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.equipment import Equipment


##############################################################################
##############################################################################
##############################################################################
class TestAction(unittest.TestCase):
    """Tests for `actions` package."""

    ########################################################################
    def setUp(self) -> None:
        """Set up test fixtures, if any."""
        self.arena = Arena(max_x=21, max_y=21)
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
        self.alpha = Creature(**kwargs)
        self.arena.add_combatant(self.alpha)
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
        self.beta = Creature(**kwargs)
        self.arena.add_combatant(self.beta)

    ########################################################################
    def tearDown(self) -> None:
        """Tear down test fixtures, if any."""

    ########################################################################
    def test_check_criticals(self) -> None:
        """Test check_criticals"""
        act = DummyAction()
        self.beta.add_action(act)
        self.assertEqual(act.check_criticals(10), (False, False))
        self.assertEqual(act.check_criticals(1), (False, True))
        self.assertEqual(act.check_criticals(20), (True, False))

    ########################################################################
    def test_roll_to_hit(self) -> None:
        """test roll_to_hit()"""
        act = DummyAction()
        self.beta.add_action(act)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 18
            to_hit, crit_hit, crit_miss = act.roll_to_hit(self.alpha)
        # 5 for DummyAction atk_bonus, 2 for prof bonus
        self.assertEqual(to_hit, 18 + 5 + 2)
        self.assertFalse(crit_hit)
        self.assertFalse(crit_miss)

    ########################################################################
    def test_calculate_to_hit(self) -> None:
        """Test calculate_to_hit()"""
        self.beta.add_effect(DummyEffect())
        act = DummyAction()
        self.beta.add_action(act)
        to_hit, msg = act.calculate_to_hit(10, self.alpha)
        # 5 for DummyAction atk_bonus, 2 for prof bonus, 3 for dummy effect
        self.assertEqual(to_hit, 10 + 5 + 2 + 3)
        self.assertEqual(msg, "+5 (modifier), +2 (prof bonus), +3 from Dummy Effect")

    ########################################################################
    def test_buff_attack_damage(self) -> None:
        """Test buff_attack_damage()"""
        act = DummyAction()
        self.beta.add_action(act)
        with patch.object(Creature, "hit") as mock:
            self.beta.add_effect(DummyEffect())
            self.beta.add_action(act)
            self.alpha.add_effect(DummyEffect())
            act.buff_attack_damage(self.alpha)

            self.assertEqual(
                mock.call_args_list[0],
                call(
                    2,
                    DamageType.FIRE,
                    self.beta,
                    critical=False,
                    atkname="Dummy Effect",
                ),
            )
            self.assertEqual(
                mock.call_args_list[1],
                call(
                    4,
                    DamageType.ACID,
                    self.beta,
                    critical=False,
                    atkname="Dummy Effect",
                ),
            )


############################################################################
class DummyEffect(Effect):
    """Test effect"""

    def __init__(self, **kwargs: Any):
        super().__init__("Dummy Effect", **kwargs)

    def hook_source_additional_damage(
        self, attack: Action, source: Creature, target: Creature
    ) -> tuple[str, int, Optional[DamageType]]:
        return ("", 2, DamageType.FIRE)

    def hook_target_additional_damage(
        self, attack: Action, source: Creature, target: Creature
    ) -> tuple[str, int, Optional[DamageType]]:
        return ("", 4, DamageType.ACID)

    def hook_attack_to_hit(self, **kwargs: Any) -> int:
        return 3


############################################################################
############################################################################
############################################################################
class DummyAction(Action):
    """Test action"""

    def __init__(self, **kwargs: Any):
        super().__init__("Dummy Action", **kwargs)

    def perform_action(self) -> bool:
        """Required"""
        return False

    def atk_modifier(self, _: Any) -> int:
        return 5

    def heuristic(self) -> int:
        return 1


############################################################################
class DummyGear(Equipment):
    """Test gear"""

    def __init__(self, **kwargs: Any):
        super().__init__("Dummy Gear", **kwargs)


# EOF
