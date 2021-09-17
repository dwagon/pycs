""" Zombie Monster Class """
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
class Zombie(Monster):
    """Zombie - https://www.dndbeyond.com/monsters/zombie"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "3d8+9"
        kwargs.update(
            {
                "ac": 8,
                "speed": 20,
                "type": MonsterType.UNDEAD,
                "str": 13,
                "dex": 6,
                "con": 16,
                "int": 3,
                "wis": 6,
                "cha": 5,
                "immunity": [DamageType.POISON],
                "actions": [
                    MeleeAttack(
                        "Slam",
                        reach=5,
                        dmg=("1d6", 0),
                        dmg_type=DamageType.BLUDGEONING,
                    )
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def fallen_unconscious(self, dmg, dmg_type, critical):
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
    def shortrepr(self):  # pragma: no cover
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.red("Z", bg="green")
        return colors.green("Z", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestZombie(unittest.TestCase):
    """Test Zombie"""

    ##########################################################################
    def setUp(self):
        """Set up the graveyard"""
        self.arena = Arena()
        self.beast = Zombie(side="a")
        self.arena.add_combatant(self.beast)

    ##########################################################################
    def test_zombie_fortitude(self):
        """Test being hit unconscious and recovering"""
        self.beast.hp = 1
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.beast.hit(6, DamageType.PIERCING, Mock(), False, "DummyAttack")
            self.assertEqual(self.beast.hp, 1)

    ##########################################################################
    def test_zombie_no_fort(self):
        """Test being hit unconscious"""
        self.beast.hp = 1
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.beast.hit(6, DamageType.RADIANT, Mock(), False, "DummyAttack")
            self.assertEqual(self.beast.hp, 0)
            self.assertTrue(self.beast.has_condition(Condition.UNCONSCIOUS))


# EOF
