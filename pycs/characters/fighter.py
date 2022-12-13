""" Fighter """
from typing import Any, Optional
import unittest
from unittest.mock import patch
import colors
import dice
from pycs.action import Action
from pycs.arena import Arena
from pycs.damageroll import DamageRoll
from pycs.attack import MeleeAttack
from pycs.character import Character
from pycs.constant import ActionCategory, DamageType
from pycs.constant import ActionType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.gear import LightCrossbow
from pycs.gear import Mace
from pycs.monsters import Orc


##############################################################################
##############################################################################
##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, **kwargs: Any):
        self.second_wind = 1
        self.action_surge = 1
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
                "stat_prof": [Stat.STR, Stat.CON],
                "actions": [SecondWind()],
                "effects": [DuelingFightingStyle()],
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            kwargs["hp"] = 12
            # Fighting Style: Dueling
        if level >= 2:
            kwargs["hp"] = 20
            kwargs["actions"].append(ActionSurge())
        if level >= 3:
            kwargs["hp"] = 28
            # Martial Archetype: Champion
            # Critical on 19 or 20
            kwargs["critical"] = 19
        if level >= 4:
            kwargs["hp"] = 36
            kwargs["str"] = 18
        if level >= 5:
            kwargs["str"] = 18
            kwargs["hp"] = 44
            kwargs["attacks_per_action"] = 2

        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("F", bg="green")
        return colors.blue("F", bg="red")


##############################################################################
##############################################################################
##############################################################################
class SecondWind(Action):
    """You have a limited well of stamina that you can draw on to protect
    yourself from harm. On your turn, you can use a bonus action to
    regain hit points equal to 1d10 + your fighter level. Once you use
    this feature, you must finish a short or long rest before you can
    use it again."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        """initialise"""
        super().__init__("Second Wind", **kwargs)
        self.type = ActionType.HEALING

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the action"""
        self.owner.second_wind = 0
        self.owner.heal("d10", self.owner.level)
        return True

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this"""
        if not self.owner.second_wind:
            return 0
        return self.owner.max_hp - self.owner.hp

    ##########################################################################
    def pick_target(self) -> Creature:
        """Only applies to self"""
        return self.owner


##############################################################################
##############################################################################
##############################################################################
class ActionSurge(Action):
    """Starting at 2nd level, you can push yourself beyond your normal
    limits for a moment. On your turn, you can take one additional
    action on top of your regular action and a possible bonus action."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        """initialise"""
        kwargs["action_cost"] = 0
        super().__init__("Action Surge", **kwargs)
        self.type = ActionType.BUFF

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the action"""
        self.owner.action_surge = 0
        self.owner.options_this_turn.append(ActionCategory.ACTION)
        return True

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this"""
        if not self.owner.action_surge:
            return 0
        return 0  # Doesn't work yet

    ##########################################################################
    def pick_target(self) -> Creature:
        """Only applies to self"""
        return self.owner


##############################################################################
##############################################################################
##############################################################################
class DuelingFightingStyle(Effect):
    """When you are wielding a melee weapon in one hand and no other
    weapons, you gain a +2 bonus to damage rolls with that weapon."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Dueling Fighting Style", **kwargs)

    ########################################################################
    def hook_source_additional_damage(self, attack: Action, source: Creature, target: Creature) -> DamageRoll:
        """2 more damage"""
        if issubclass(attack.__class__, MeleeAttack):
            return DamageRoll("", 2)
        return DamageRoll("", 0)


##############################################################################
##############################################################################
##############################################################################
class TestDuelingFightingStyle(unittest.TestCase):
    """Test DuelingFightingStyle"""

    ########################################################################
    def setUp(self) -> None:
        self.arena = Arena()
        self.fighter = Fighter(name="Freya", side="a", level=2, gear=[Mace(), LightCrossbow()])
        self.arena.add_combatant(self.fighter, coords=(1, 1))
        self.orc = Orc(side="b", hp=20)
        self.arena.add_combatant(self.orc, coords=(2, 2))

    ########################################################################
    def test_dfs_melee(self) -> None:
        """Test damage bonus"""
        self.assertTrue(self.fighter.has_effect("Dueling Fighting Style"))
        act = self.fighter.pick_action_by_name("Mace")
        assert act is not None
        self.fighter.target = self.orc
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19
            with patch.object(dice, "roll") as mock_dice:  # damage roll
                mock_dice.return_value = 1
                act.perform_action()
        # 1 for mace, 3 for str, 2 for fighting style
        self.assertEqual(self.orc.hp, self.orc.max_hp - 1 - 3 - 2)

    ########################################################################
    def test_dfs_ranged(self) -> None:
        """Test damage bonus doesn't apply to ranged"""
        self.assertTrue(self.fighter.has_effect("Dueling Fighting Style"))
        act = self.fighter.pick_action_by_name("Light Crossbow")
        assert act is not None
        self.fighter.target = self.orc
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19
            with patch.object(dice, "roll") as mock_dice:  # damage roll
                mock_dice.return_value = 1
                act.perform_action()
        # 1 for weap, 2 for dex
        self.assertEqual(self.orc.hp, self.orc.max_hp - 1 - 2)


##############################################################################
##############################################################################
##############################################################################
class TestSecondWind(unittest.TestCase):
    """Test SecondWind"""

    ########################################################################
    def setUp(self) -> None:
        self.arena = Arena()
        self.fighter = Fighter(name="Freya", side="a", level=5)
        self.arena.add_combatant(self.fighter, coords=(1, 1))

    ########################################################################
    def test_second_wind(self) -> None:
        """Test Second Wind"""
        act = self.fighter.pick_action_by_name("Second Wind")
        assert act is not None
        self.assertTrue(act is not None)
        self.assertEqual(act.pick_target(), self.fighter)
        before = act.heuristic()
        self.assertEqual(before, 0)
        self.fighter.hp = 10
        after = act.heuristic()
        self.assertGreater(after, 0)
        with patch.object(dice, "roll") as mock_dice:  # healing roll
            mock_dice.return_value = 4
            act.perform_action()
        # Original 10 + 4 for healing + 5 for level
        self.assertEqual(self.fighter.hp, 10 + 4 + 5)


# EOF
