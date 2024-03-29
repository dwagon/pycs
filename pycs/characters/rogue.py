""" https://www.dndbeyond.com/classes/rogue """
from typing import Any
import unittest
from unittest.mock import patch
import colors
import dice
from pycs.action import Action
from pycs.arena import Arena
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.damageroll import DamageRoll
from pycs.damage import Damage
from pycs.constant import Condition
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.gear import Shortsword
from pycs.monsters import Orc


##############################################################################
##############################################################################
##############################################################################
class Rogue(Character):
    """Rogue class"""

    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "str": 12,
                "dex": 17,
                "con": 13,
                "int": 9,
                "wis": 14,
                "cha": 10,
                "stat_prof": [Stat.DEX, Stat.INT],
                "speed": 35,
                "actions": [],
                "effects": [],
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            kwargs["hp"] = 9
            self.sneak_attack_dmg = "1d6"
        if level >= 2:
            kwargs["hp"] = 15
            kwargs["effects"].append(SneakAttack())
        if level >= 3:
            self.sneak_attack_dmg = "2d6"
            kwargs["actions"].append(CunningAction())
            kwargs["hp"] = 21
        if level >= 4:
            kwargs["hp"] = 31
            kwargs["dex"] = 18
            kwargs["con"] = 14
        if level >= 5:
            kwargs["hp"] = 38
            self.sneak_attack_dmg = "3d6"
            kwargs["actions"].append(UncannyDodge())

        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a rogue looks like in the arena"""
        if self.is_alive():
            return colors.black("R", bg="green")
        return colors.blue("R", bg="red")


##############################################################################
##############################################################################
##############################################################################
class UncannyDodge(Action):
    """When an attacker that you can see hits you with an attack,
    you can use your reaction to halve the attack’s damage against
    you."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Uncanny Dodge", **kwargs)
        self.category = ActionCategory.REACTION

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this - prob could be smarter, but at the moment
        just do it for the first attack"""
        return 1

    ##########################################################################
    def hook_predmg(self, dmg: Damage, source: Creature, critical: bool) -> Damage:
        """Half damage"""
        print("Using uncanny dodge to reduce damage")
        dmg //= 2
        return dmg

    ##########################################################################
    def perform_action(self) -> bool:
        """Need to define but nothing to do"""
        return False


##############################################################################
##############################################################################
##############################################################################
class CunningAction(Action):
    """You can take a bonus action on each of your turns to take the
    Dash, Disengage, or Hide action."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Cunning Action", **kwargs)
        self.category = ActionCategory.BONUS

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this"""
        return 0
        # Don't know how to implement this yet

    ##########################################################################
    def perform_action(self) -> bool:
        """Not implemented yet"""
        return False


##############################################################################
##############################################################################
##############################################################################
class SneakAttack(Effect):
    """Beginning at 1st level, you know how to strike subtly and exploit
    a foe's distraction. Once per turn, you can deal an extra 1d6 damage
    to one creature you hit with an attack if you have advantage on the
    attack roll. The attack must use a finesse or a ranged weapon.

    You don't need advantage on the attack roll if another enemy of the
    target is within 5 feet of it, that enemy isn't incapacitated, and
    you don't have disadvantage on the attack roll.

    The amount of the extra damage increases as you gain levels in this
    class, as shown in the Sneak Attack column of the Rogue table."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Sneak Attack", **kwargs)
        self._used_this_turn = False

    ########################################################################
    def hook_start_turn(self) -> None:
        """Start the turn"""
        self._used_this_turn = False

    ########################################################################
    def hook_source_additional_damage(self, attack: Action, source: Creature, target: Creature) -> DamageRoll:
        """Do the sneak attack"""
        if self._used_this_turn:
            return DamageRoll()

        if not target.has_condition(Condition.OK):
            return DamageRoll()

        allies_adjacent = False
        allies = [_ for _ in target.pick_closest_enemy() if _ != source]
        if allies:
            if allies[0].distance(target) <= 1:
                allies_adjacent = True
                print(f"Ally {allies[0]} adjacent to {target}")

        rnge = source.distance(target)
        if allies_adjacent and attack.has_disadvantage(target, rnge):
            print("but it doesn't matter as we have disadvantage")
            allies_adjacent = False

        if not allies_adjacent:
            if not attack.has_advantage(target, rnge):
                return DamageRoll()
            print("We have advantage on attack")
        self._used_this_turn = True
        return DamageRoll(self.owner.sneak_attack_dmg, 0)  # type: ignore


##############################################################################
##############################################################################
##############################################################################
class TestSneakAttack(unittest.TestCase):
    """Test SneakAttack"""

    ########################################################################
    def setUp(self) -> None:
        self.arena = Arena()
        self.rogue = Rogue(name="Rufus", side="a", level=2, gear=[Shortsword()])
        self.arena.add_combatant(self.rogue, coords=(1, 1))
        self.orc = Orc(side="b", hp=20)
        self.arena.add_combatant(self.orc, coords=(2, 2))

    ########################################################################
    def test_no_sneak(self) -> None:
        """Make sure not everything is a sneak attack"""
        self.assertTrue(self.rogue.has_effect("Sneak Attack"))
        act = self.rogue.pick_action_by_name("Shortsword")
        assert act is not None
        self.rogue.target = self.orc
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19  # Hit target
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 3
                act.perform_action()
        self.assertEqual(self.orc.hp, self.orc.max_hp - 6)  # 3 for dmg, 3 for stat

    ########################################################################
    def test_sneak(self) -> None:
        """Do a sneak attack"""
        self.assertTrue(self.rogue.has_effect("Sneak Attack"))
        act = self.rogue.pick_action_by_name("Shortsword")
        assert act is not None
        friend = Orc(side="a")
        self.arena.add_combatant(friend, coords=(2, 3))
        self.rogue.target = self.orc
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19  # Hit target
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 3
                act.perform_action()
        self.assertEqual(self.orc.hp, self.orc.max_hp - 6 - 3)  # Additional 3 dmg

        # Attack again - should not be another sneak
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19  # Hit target
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 3
                act.perform_action()
        self.assertEqual(self.orc.hp, self.orc.max_hp - 6 - 3 - 6)


# EOF
