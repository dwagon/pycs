""" https://www.dndbeyond.com/monsters/goblin"""
import unittest
import colors
from pycs.arena import Arena
from pycs.gear import Shortbow
from pycs.gear import Scimitar
from pycs.gear import Leather
from pycs.gear import Shield
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
class Goblin(Monster):
    """Goblin"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "2d6",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 8,
                "dex": 14,
                "con": 10,
                "int": 10,
                "wis": 8,
                "cha": 8,
                "gear": [Scimitar(), Shortbow(), Leather(), Shield()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("g")
        return colors.green("g", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestGoblin(unittest.TestCase):
    """Test oblin"""

    ##########################################################################
    def setUp(self):
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Goblin(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))

    ##########################################################################
    def test_ac(self):
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 15)


# EOF
