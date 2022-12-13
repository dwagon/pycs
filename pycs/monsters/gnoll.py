""" https://www.dndbeyond.com/monsters/gnoll"""
from typing import Any
import unittest
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.damageroll import DamageRoll
from pycs.gear import Hide
from pycs.gear import Longbow
from pycs.gear import Shield
from pycs.gear import Spear
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Gnoll(Monster):
    """Gnoll"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "5d8",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 14,
                "dex": 12,
                "con": 11,
                "int": 6,
                "wis": 10,
                "cha": 7,
                "gear": [Spear(), Longbow(), Hide(), Shield()],
                "actions": [MeleeAttack("Bite", reach=5, dmgroll=DamageRoll("1d4", 0, DamageType.PIERCING))],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a gnoll looks like on the arena"""
        if self.is_alive():
            return colors.blue("G")
        return colors.blue("G", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestGnoll(unittest.TestCase):
    """Test Gnoll"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Gnoll(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b")
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 15)


# EOF
