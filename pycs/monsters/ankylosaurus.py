""" Ankylosaurus  MM p79 """
from typing import Any
import unittest
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import MonsterType, DamageType, Condition, Stat
from pycs.creature import Creature
from pycs.damageroll import DamageRoll
from pycs.monster import Monster


##############################################################################
class Ankylosaurus(Monster):
    """Ankylosaurus"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "8d12+16",
                "speed": 30,
                "type": MonsterType.BEAST,
                "ac": 15,
                "str": 19,
                "dex": 11,
                "con": 15,
                "int": 2,
                "wis": 12,
                "cha": 5,
                "actions": [
                    MeleeAttack(
                        "Tail",
                        reach=10,
                        dmgroll=DamageRoll("4d6", 0, DamageType.BLUDGEONING),
                        side_effect=self.anktail,
                    ),
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def anktail(self, source: Creature, target: Creature, dmg: DamageType) -> None:  # pylint: disable=unused-argument
        """Ank Tail - must succeed at a DC14 strength save or be knocked prone"""
        svth = target.saving_throw(Stat.STR, 14)
        if not svth:
            target.add_condition(Condition.PRONE)

    ##########################################################################
    def shortrepr(self) -> str:
        """What a allosaurus looks like on the arena"""
        if self.is_alive():
            return colors.blue("K")
        return colors.blue("K", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestAllosaurus(unittest.TestCase):
    """Test Ankylosaurus"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = Ankylosaurus(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC exists"""
        self.assertEqual(self.beast.ac, 15)


# EOF
