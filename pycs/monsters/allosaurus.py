""" Allosaurus MM p79"""
from typing import Any
import unittest
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import MonsterType
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.monster import Monster


##############################################################################
class Allosaurus(Monster):
    """Allosaurus"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "6d10+18",
                "speed": 60,
                "type": MonsterType.BEAST,
                "ac": 13,
                "str": 19,
                "dex": 13,
                "con": 17,
                "int": 2,
                "wis": 12,
                "cha": 5,
                "actions": [
                    MeleeAttack("Bite", reach=5, dmgroll=DamageRoll("2d10", 0, DamageType.PIERCING)),
                    MeleeAttack("Claw", reach=5, dmgroll=DamageRoll("1d8", 0, DamageType.SLASHING)),
                ],
            }
        )
        # TO DO : Pounce
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:
        """What a allosaurus looks like on the arena"""
        if self.is_alive():
            return colors.blue("A")
        return colors.blue("A", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestAllosaurus(unittest.TestCase):
    """Test Allosaurus"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Allosaurus(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC exists"""
        self.assertEqual(self.beast.ac, 13)


# EOF
