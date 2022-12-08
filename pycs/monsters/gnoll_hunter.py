""" VGTM p154 : Gnoll Hunter"""
from typing import Any
import unittest
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import MonsterType, DamageType
from pycs.gear import Leather, Spear, Longbow
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class GnollHunter(Monster):
    """Gnoll Hunter"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "4d8+4",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 14,
                "dex": 14,
                "con": 12,
                "int": 8,
                "wis": 12,
                "cha": 8,
                "actions": [MeleeAttack("Bite", reach=5, dmg=("1d4", 0), dmg_type=DamageType.PIERCING)],
                "gear": [Leather(), Spear(), Longbow()],
                "challenge": 0.5,
                "attacks_per_action": 2,
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a gnoll looks like on the arena"""
        if self.is_alive():
            return colors.blue("h")
        return colors.green("h", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestGnollHunter(unittest.TestCase):
    """Test Gnoll Hunter"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = GnollHunter(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b")
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC exists"""
        self.assertEqual(self.beast.ac, 13)


# EOF
