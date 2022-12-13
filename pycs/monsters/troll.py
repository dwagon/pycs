""" Troll Monster Class """
from typing import Any
import unittest
import colors
from pycs.action import Action
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterSize
from pycs.constant import MonsterType
from pycs.damage import Damage
from pycs.damageroll import DamageRoll
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Troll(Monster):
    """Troll - https://www.dndbeyond.com/monsters/troll"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        self._regen = 5
        kwargs.update(
            {
                "hitdice": "8d10+40",
                "ac": 15,
                "size": MonsterSize.LARGE,
                "speed": 30,
                "type": MonsterType.GIANT,
                "str": 18,
                "dex": 13,
                "con": 20,
                "int": 7,
                "wis": 9,
                "cha": 7,
                "prof_bonus": 3,
                "actions": [TrollMultiAttack()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def hook_start_turn(self) -> None:
        """Regeneration. The troll regains 10 hit points at the start of
        its turn. If the troll takes acid or fire damage, this trait doesn't
        function at the start of the troll's next turn. The troll dies only
        if it starts its turn with 0 hit points and doesn't regenerate."""
        for hit in self.damage_last_turn:
            if hit.type in (DamageType.ACID, DamageType.FIRE):
                print(f"Not regenerating as took {hit.type.value} damage last turn")
                return
        # Don't come back from unconsciousness forever - can lead to loops
        if self.hp <= 0:
            self._regen -= 1
        if self._regen <= 0:
            print("Not regening as getting ridiculous")
            return
        print(f"{self._regen} regens left")
        if self.hp < self.max_hp:
            self.heal("", 10)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a skeleton looks like on the arena"""
        if self.is_alive():
            return colors.green("T")
        return colors.green("T", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TrollMultiAttack(Action):
    """Handle a multi attack of Bite, Claw, Claw"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the action"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 1
        return 0

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the attack"""
        bite = MeleeAttack("Bite", dmgroll=DamageRoll("1d6", 0, DamageType.PIERCING), owner=self.owner)
        claw1 = MeleeAttack("Claw", dmgroll=DamageRoll("2d6", 0, DamageType.SLASHING), owner=self.owner)
        claw2 = MeleeAttack("Claw", dmgroll=DamageRoll("2d6", 0, DamageType.SLASHING), owner=self.owner)
        bite.do_attack()
        claw1.do_attack()
        claw2.do_attack()
        return True


##############################################################################
##############################################################################
##############################################################################
class TestTroll(unittest.TestCase):
    """Test Troll"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the bridge"""
        self.arena = Arena()
        self.troll = Troll(side="a")
        self.arena.add_combatant(self.troll)

    ##########################################################################
    def test_regen(self) -> None:
        """Test the regeneration"""
        self.troll.hp = 20
        self.troll.start_turn()
        self.assertEqual(self.troll.hp, 30)

    ##########################################################################
    def test_noregen(self) -> None:
        """Test the regeneration with acid attak"""
        self.troll.hp = 20
        self.troll.damage_this_turn.append(Damage(1, DamageType.FIRE))
        self.troll.start_turn()
        self.assertEqual(self.troll.hp, 20)


# EOF
