""" https://www.dndbeyond.com/monsters/kobold"""
import unittest
import colors
from pycs.arena import Arena
from pycs.gear import Dagger
from pycs.gear import Sling
from pycs.effect import Effect
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Kobold(Monster):
    """Kobold"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "2d6-2",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 7,
                "dex": 15,
                "con": 9,
                "int": 8,
                "wis": 7,
                "cha": 8,
                "gear": [Dagger(), Sling()],
                "effects": [PackTactics()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):  # pragma: no cover
        """What a kobold looks like on the arena"""
        if self.is_alive():
            return colors.green("k")
        return colors.green("k", bg="red")


##############################################################################
##############################################################################
##############################################################################
class PackTactics(Effect):
    """Pack Tactics. The kobold has advantage on an attack roll against
    a creature if at least one of the kobold's allies is within 5 feet
    of the creature and the ally isn't incapacitated"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Pack Tactics", **kwargs)

    ##########################################################################
    def hook_gives_advantage(self, target):
        """Do pack tactics apply?"""
        allies = [_ for _ in target.pick_closest_enemy() if _ != self.owner]
        if allies:
            if allies[0].distance(target) <= 1:
                return True
        return False


##############################################################################
##############################################################################
##############################################################################
class TestKobold(unittest.TestCase):
    """Test Kobold"""

    ##########################################################################
    def setUp(self):
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Kobold(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(
            str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b"
        )
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_pack(self):
        """Test pack tactics"""
        sling = self.beast.pick_attack_by_name("Sling")
        self.assertFalse(sling.has_advantage(self.victim, 3))
        friend = Kobold(side="a")
        self.arena.add_combatant(friend, coords=(1, 3))
        self.assertTrue(sling.has_advantage(self.victim, 3))

    ##########################################################################
    def test_ac(self):
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 12)


# EOF
