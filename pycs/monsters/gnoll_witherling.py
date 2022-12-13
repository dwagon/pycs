""" VGTM p155 : Gnoll Witherling"""
from typing import Any
import unittest
import colors
from pycs.action import Action
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import ActionCategory
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.creature import Creature
from pycs.damageroll import DamageRoll
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class GnollWitherling(Monster):
    """Gnoll Witherling"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "2d8+2",
                "ac": 12,
                "speed": 30,
                "type": MonsterType.UNDEAD,
                "str": 14,
                "dex": 8,
                "con": 12,
                "int": 5,
                "wis": 5,
                "cha": 5,
                "actions": [WitherlingMultiAttack(), VengefulStrike()],
                "immunity": [DamageType.POISON],
                "cond_immunity": [Condition.EXHAUSTION, Condition.POISONED],
                "challenge": 0.25,
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a gnoll looks like on the arena"""
        if self.is_alive():
            return colors.blue("w")
        return colors.green("w", bg="red")

    ##########################################################################
    def hook_see_someone_die(self, creat: Creature) -> None:
        """We get to react if a fellow gnoll dies nearby"""
        if self.distance(creat) > 30 / 5:
            return
        if not creat.__class__.__name__.startswith("Gnoll"):
            return
        if ActionCategory.REACTION not in self.options_this_turn:
            return
        print(f"{self} saw {creat} die so doing Vengeful Strike")
        act = self.pick_action_by_name("Vengeful Strike")
        assert act is not None
        if not self.target:
            self.target = act.pick_target()
        if self.target:
            act.perform_action()
            self.options_this_turn.remove(ActionCategory.REACTION)
        else:
            print(f"{self} doesn't have a target")


##############################################################################
##############################################################################
##############################################################################
class VengefulStrike(Action):
    """React to another gnoll being killed within 30' by doing a melee attack"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Vengeful Strike", **kwargs)
        self.category = ActionCategory.REACTION

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this"""
        return 0  # Triggered by hook in creature

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the action"""
        bite = MeleeAttack(
            "Bite",
            reach=5,
            dmgroll=DamageRoll("1d4", 0, DamageType.PIERCING),
            owner=self.owner,
        )
        bite.do_attack()
        return True


##############################################################################
##############################################################################
##############################################################################
class WitherlingMultiAttack(Action):
    """Handle a multi-attack: bite, club"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the attack"""
        bite = MeleeAttack(
            "Bite",
            reach=5,
            dmgroll=DamageRoll("1d4", 0, DamageType.PIERCING),
            owner=self.owner,
        )
        club = MeleeAttack(
            "Club",
            reach=5,
            dmgroll=DamageRoll("1d4", 0, DamageType.BLUDGEONING),
            owner=self.owner,
        )
        bite.do_attack()
        club.do_attack()
        return True

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the attack"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 1
        return 0


##############################################################################
##############################################################################
##############################################################################
class TestGnoll(unittest.TestCase):
    """Test GnollWitherling"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the lair"""
        self.arena = Arena()
        self.beast = GnollWitherling(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b")
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_ac(self) -> None:
        """Test that the AC exists"""
        self.assertEqual(self.beast.ac, 12)


# EOF
