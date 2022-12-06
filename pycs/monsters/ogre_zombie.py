""" Ogre Zombie Monster Class """
from typing import Any
import unittest
from unittest.mock import patch, Mock
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.monster import Monster


##############################################################################
class OgreZombie(Monster):
    """Ogre Zombie - https://www.dndbeyond.com/monsters/ogre-zombie"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "9d10+36",
                "ac": 8,
                "speed": 30,
                "challenge": 2,
                "type": MonsterType.UNDEAD,
                "str": 19,
                "dex": 6,
                "con": 18,
                "int": 3,
                "wis": 6,
                "cha": 5,
                "immunity": [DamageType.POISON],
                "actions": [
                    MeleeAttack(
                        "Morning Star",
                        reach=5,
                        dmg=("2d8", 0),
                        dmg_type=DamageType.BLUDGEONING,
                    )
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def fallen_unconscious(self, dmg: int, dmg_type: DamageType, critical: bool) -> None:
        """Undead Fortitude. If damage reduces the zombie to 0 hit points,
        it must make a Constitution saving throw with a DC of 5 + the damage
        taken, unless the damage is radiant or from a critical hit.
        On a success, the zombie drops to 1 hit point instead."""
        if not critical and dmg_type != DamageType.RADIANT:
            save = self.saving_throw(Stat.CON, 5 + dmg)
            if save:
                self.hp = 1
                print(f"{self} uses Undead Fortitude and stays conscious")
                return
        super().fallen_unconscious(dmg, dmg_type, critical)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("O")
        return colors.green("O", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestOgreZombie(unittest.TestCase):
    """Test Ogre Zombie"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the graveyard"""
        self.arena = Arena()
        self.beast = OgreZombie(side="a")
        self.arena.add_combatant(self.beast)

    ##########################################################################
    def test_zombie_fortitude(self) -> None:
        """Test being hit unconscious and recovering"""
        self.beast.hp = 1
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.beast.hit(6, DamageType.PIERCING, Mock(), False, "DummyAttack")
            self.assertEqual(self.beast.hp, 1)

    ##########################################################################
    def test_zombie_no_fort(self) -> None:
        """Test being hit unconscious"""
        self.beast.hp = 1
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.beast.hit(6, DamageType.RADIANT, Mock(), False, "DummyAttack")
            self.assertTrue(self.beast.has_condition(Condition.DEAD))


# EOF
