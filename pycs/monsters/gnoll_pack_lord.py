""" https://www.dndbeyond.com/monsters/gnoll"""
from typing import Any
import unittest
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.gear import ChainShirt
from pycs.gear import Longbow
from pycs.gear import Glaive
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class GnollPackLord(Monster):
    """Gnoll Pack Lord"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "9d8+9",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 16,
                "dex": 14,
                "con": 13,
                "int": 8,
                "wis": 11,
                "cha": 9,
                "gear": [ChainShirt(), Glaive(), Longbow()],
                "actions": [MeleeAttack("Bite", reach=5, dmgroll=("1d4", 0, DamageType.PIERCING))],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a gnoll looks like on the arena"""
        if self.is_alive():
            return colors.blue("P")
        return colors.green("P", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestGnoll(unittest.TestCase):
    """Test GnollPackLord"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = GnollPackLord(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b")
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 15)


# EOF
