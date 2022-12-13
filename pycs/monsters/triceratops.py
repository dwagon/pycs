""" Triceratops MM p80"""
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
class Triceratops(Monster):
    """Triceratops"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "10d12+30",
                "speed": 50,
                "type": MonsterType.BEAST,
                "ac": 13,
                "str": 22,
                "dex": 9,
                "con": 17,
                "int": 2,
                "wis": 11,
                "cha": 5,
                "actions": [
                    MeleeAttack("Gore", reach=5, dmgroll=DamageRoll("4d8", 0, DamageType.PIERCING)),
                    MeleeAttack(
                        "Stomp",
                        reach=5,
                        dmgroll=DamageRoll("3d10", 0, DamageType.BLUDGEONING),
                    ),
                ],
            }
        )
        # TO DO : Trampling Charge
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:
        """What a triceratop looks like on the arena"""
        if self.is_alive():
            return colors.blue("T")
        return colors.blue("T", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestTriceratops(unittest.TestCase):
    """Test Triceratops"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Triceratops(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC exists"""
        self.assertEqual(self.beast.ac, 13)


# EOF
