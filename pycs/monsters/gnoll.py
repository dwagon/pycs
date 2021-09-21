""" https://www.dndbeyond.com/monsters/gnoll"""
import unittest
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
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
    def __init__(self, **kwargs):
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
                "actions": [
                    MeleeAttack(
                        "Bite", reach=5, dmg=("1d4", 0), dmg_type=DamageType.PIERCING
                    )
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):  # pragma: no cover
        """What a gnoll looks like on the arena"""
        if self.is_alive():
            return colors.green("G")
        return colors.green("G", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestGnoll(unittest.TestCase):
    """Test Gnoll"""

    ##########################################################################
    def setUp(self):
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Gnoll(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(
            str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b"
        )
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_ac(self):
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 15)


# EOF
