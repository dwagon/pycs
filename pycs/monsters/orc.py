""" https://www.dndbeyond.com/monsters/orc"""
import unittest
import colors
from pycs.arena import Arena
from pycs.gear import Javelin
from pycs.gear import Hide
from pycs.gear import Greataxe
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Orc(Monster):
    """Orc"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "2d8+6",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 16,
                "dex": 12,
                "con": 16,
                "int": 7,
                "wis": 11,
                "cha": 10,
                "gear": [Javelin(ammo=4), Greataxe(), Hide()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What an Orc looks like on the arena"""
        if self.is_alive():
            return colors.green("O")
        return colors.green("O", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestOrc(unittest.TestCase):
    """Test Orc"""

    ##########################################################################
    def setUp(self):
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Orc(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))

    ##########################################################################
    def test_ac(self):
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 13)


# EOF
