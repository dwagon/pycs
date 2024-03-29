"""https://www.dndbeyond.com/races/half-orc"""
from typing import Any
import unittest
from unittest.mock import Mock

from pycs.arena import Arena
from pycs.constant import DamageType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.damage import Damage
from pycs.effect import Effect
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class HalfOrc(Race):
    """Grunt"""

    def __init__(self, **kwargs: Any):
        kwargs["effects"] = [RelentlessEndurance()]
        super().__init__("Half Orc", **kwargs)

    # TO DO - Savage Attack


##############################################################################
##############################################################################
##############################################################################
class RelentlessEndurance(Effect):
    """Relentless Endurance - When you are reduced to 0 HP but not
    killed, you can drop to 1 HP instead once per long rest."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Relentless Endurance", **kwargs)
        self._relentless_used = False

    ########################################################################
    def hook_fallen_unconscious(self, dmg: Damage, critical: bool) -> bool:
        """Engage Relentless Attack"""
        if self._relentless_used:
            return True
        print(f"{self.owner}'s Relentless Endurance kicks in")
        assert self.owner is not None
        self.owner.hp = 1
        self._relentless_used = True
        return False


##############################################################################
##############################################################################
##############################################################################
class TestRelentlessEndurance(unittest.TestCase):
    """Test Relentless Endurance"""

    def setUp(self) -> None:
        kwargs = {
            "str": 6,
            "int": 7,
            "dex": 8,
            "wis": 18,
            "con": 11,
            "cha": 15,
            "hp": 30,
            "ac": 10,
            "spellcast_bonus_stat": Stat.WIS,
            "name": "Half Orc",
            "side": "a",
        }
        self.orc = Creature(**kwargs)
        self.orc.add_effect(RelentlessEndurance())
        self.arena = Arena()
        self.arena.add_combatant(self.orc)
        self.orc.creature_fallen_unconscious = Mock()  # type:ignore

    ########################################################################
    def test_go_uncon(self) -> None:
        """Test what happens when we go uncon"""
        self.assertTrue(self.orc.has_effect("Relentless Endurance"))
        self.orc.hit(Damage(40, DamageType.FIRE), self.orc, False, "test")
        self.assertEqual(self.orc.hp, 1)
        self.orc.hit(Damage(40, DamageType.FIRE), self.orc, False, "test")
        self.assertEqual(self.orc.hp, 0)


# EOF
