"""https://www.dndbeyond.com/monsters/ghoul"""
import unittest
from unittest.mock import patch
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Ghoul(Monster):
    """Ghoul Monster Class"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "5d8",
                "ac": 12,
                "challenge": 1,
                "speed": 30,
                "type": MonsterType.UNDEAD,
                "str": 13,
                "dex": 15,
                "con": 10,
                "int": 7,
                "wis": 10,
                "cha": 6,
                "immunity": [DamageType.POISON],
                "actions": [
                    MeleeAttack(
                        "Bite",
                        reach=5,
                        heuristic=self.heuristic_ghoul_bite,
                        dmg=("2d6", 0),
                        dmg_type=DamageType.PIERCING,
                    ),
                    MeleeAttack(
                        "Claw",
                        reach=5,
                        dmg=("2d4", 0),
                        heuristic=self.heuristic_ghoul_claw,
                        dmg_type=DamageType.SLASHING,
                        side_effect=self.se_ghoul_claws,
                    ),
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def se_ghoul_claws(self, source, target, dmg):
        """Implement Side Effect of Ghoul Claws"""
        svth = target.saving_throw(Stat.CON, 10, effect=Condition.PARALYZED)
        if not svth:
            print(f"{target} got paralysed by {source} (+{dmg} dmg)")
            target.add_effect(GhoulClawEffect())
        else:
            print(f"{target} resisted Ghoul claws")

    ##########################################################################
    def heuristic_ghoul_bite(self):
        """When is Ghoul bite good"""
        if self.target and self.target.has_condition(Condition.PARALYZED):
            return 2
        return 1

    ##########################################################################
    def heuristic_ghoul_claw(self):
        """When is Ghoul claw good"""
        if self.target and not self.target.has_condition(Condition.PARALYZED):
            return 2
        return 1

    ##########################################################################
    def shortrepr(self):  # pragma: no cover
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("G", style="bold")
        return colors.green("G", bg="red", style="bold")


##############################################################################
##############################################################################
##############################################################################
class GhoulClawEffect(Effect):
    """If the target is a creature other than an elf or undead, it must
    succeed on a DC 10 Constitution saving throw or be paralyzed for 1
    minute. The target can repeat the saving throw at the end of each
    of its turns, ending the effect on itself on a success."""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Ghoul Claws", **kwargs)

    ##########################################################################
    def initial(self, target):
        """First effect"""
        target.add_condition(Condition.PARALYZED)

    ##########################################################################
    def removal_end_of_its_turn(self, victim):
        """Do we rmove the effect"""
        svth = victim.saving_throw(Stat.CON, 10, effect=Condition.PARALYZED)
        if svth:
            print(f"{victim} resisted Ghoul claws")
            victim.remove_condition(Condition.PARALYZED)
            return True
        return False


##############################################################################
##############################################################################
##############################################################################
class TestGhoul(unittest.TestCase):
    """Test Ghoul"""

    ##########################################################################
    def setUp(self):
        """Set up the crypt"""
        self.arena = Arena()
        self.beast = Ghoul(side="a")
        self.arena.add_combatant(self.beast, coords=(1, 1))
        self.victim = Monster(
            str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b"
        )
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_claws(self):
        """Test claws"""
        claws = self.beast.pick_action_by_name("Claw")
        self.beast.target = self.victim
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [20, 1]
            claws.perform_action()
            self.assertTrue(self.victim.has_effect("Ghoul Claws"))
            self.assertTrue(self.victim.has_condition(Condition.PARALYZED))
        # Keep the effect on a failed save
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 2
            self.victim.end_turn()
            self.assertTrue(self.victim.has_condition(Condition.PARALYZED))
        # Remove the effect on a good save
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.victim.end_turn()
            self.assertFalse(self.victim.has_condition(Condition.PARALYZED))


# EOF
