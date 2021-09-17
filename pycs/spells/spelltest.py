""" Parent Test for Spell """

import unittest
from unittest.mock import Mock
from pycs.arena import Arena
from pycs.creature import Creature
from pycs.gear import Longsword
from pycs.constant import ActionCategory
from pycs.constant import Stat


##############################################################################
##############################################################################
##############################################################################
class SpellTest(unittest.TestCase):
    """Test Framework for Spell"""

    def setUp(self):
        self.arena = Arena(max_x=10, max_y=10)
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
        }
        self.caster = Creature(name="caster", side="a", **kwargs)
        self.arena.add_combatant(self.caster)
        self.caster.spell_available = Mock(return_value=True)
        self.caster.cast = Mock(return_value=True)

        self.friend = Creature(name="friend", side="a", **kwargs)
        self.arena.add_combatant(self.friend)
        self.friend.add_gear(Longsword())

        self.enemy = Creature(name="enemy", side="b", **kwargs)
        self.arena.add_combatant(self.enemy)
        self.enemy.add_gear(Longsword())

        self.caster.options_this_turn = [ActionCategory.ACTION]


# EOF
