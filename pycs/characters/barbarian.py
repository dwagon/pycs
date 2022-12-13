""" Barbarian """
import unittest
from typing import Any
from unittest.mock import patch
import colors
import dice
from pycs.action import Action
from pycs.arena import Arena
from pycs.damageroll import DamageRoll
from pycs.damage import Damage
from pycs.attack import MeleeAttack
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import DamageType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.gear import Greataxe
from pycs.monsters import Orc


##############################################################################
##############################################################################
##############################################################################
class Barbarian(Character):
    """Barbarian class"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
                "stat_prof": [Stat.STR, Stat.CON],
                "actions": [BarbarianRage()],
                "effects": [],
                "action_preference": {
                    BarbarianRage: 9,
                    ActionType.MELEE: 8,
                    ActionType.RANGED: 4,
                },
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            kwargs["hp"] = 14
        if level >= 2:
            kwargs["hp"] = 23
            kwargs["effects"].append(BarbarianDangerSenseEffect())
        if level >= 3:
            kwargs["hp"] = 32
        if level >= 4:
            kwargs["hp"] = 41
            kwargs["str"] = 18
        if level >= 5:
            kwargs["hp"] = 50
            kwargs["speed"] = 40
            kwargs["attacks_per_action"] = 2
        super().__init__(**kwargs)

    ##########################################################################
    def report(self) -> None:
        """Character Report"""
        super().report()
        javs = self.pick_action_by_name("Javelin")
        assert javs is not None
        print(f"|  Javelins: {javs.ammo}")

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("B", bg="green")
        return colors.blue("B", bg="red")


##############################################################################
##############################################################################
##############################################################################
class BarbarianRage(Action):
    """Shield biting stuff"""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Barbarian Rage", **kwargs)
        self.type = ActionType.BUFF
        self.category = ActionCategory.BONUS

    ########################################################################
    def pick_target(self) -> Creature:
        """Who do we do it to"""
        return self.owner

    ########################################################################
    def heuristic(self) -> int:
        """Should we do it"""
        if self.owner.has_effect("Rage"):
            return 0
        return 10

    ########################################################################
    def perform_action(self) -> bool:
        """Do the action"""
        self.owner.add_effect(BarbarianRageEffect())
        return True


##############################################################################
##############################################################################
##############################################################################
class BarbarianFrenziedRageEffect(Effect):
    """While raging, you can choose to frenzy. You can make a single
    melee weapon attack as a bonus action on each of your turns after
    this one. When your rage ends, you suffer one level of exhaustion."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Frenzied Rage", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class BarbarianRageEffect(Effect):
    """You gain advantage on STR checks and saving throws (not attacks),
    +2 melee damage with STR weapons, resistance to bludgeoning, piercing,
    slashing damage. You can't cast or concentrate on spells while
    raging."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Rage", **kwargs)

    ########################################################################
    def hook_being_hit(self, dmg: Damage) -> Damage:
        """Mod damage"""
        if dmg.type in (
            DamageType.BLUDGEONING,
            DamageType.PIERCING,
            DamageType.SLASHING,
        ):
            dmg //= 2
        return dmg

    ########################################################################
    def hook_source_additional_damage(self, attack: Action, source: Creature, target: Creature) -> DamageRoll:
        """Rage causes dangerous things"""
        if issubclass(attack.__class__, MeleeAttack):
            return DamageRoll("", 2)
        return DamageRoll("", 0)

    ########################################################################
    def hook_saving_throw(self, stat: Stat, **kwargs: Any) -> dict:
        """Advantage on strength"""
        eff = super().hook_saving_throw(stat, **kwargs)
        if stat == Stat.STR:
            eff.update({"advantage": True})
        return eff


##############################################################################
##############################################################################
##############################################################################
class BarbarianDangerSenseEffect(Effect):
    """You have advantage on DEX saving throws against effects that you
    can see while not blinded, deafened, or incapacitated."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Danger Sense", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class BarbarianRecklessAttack(Effect):
    """When you make your first attack on your turn, you can decide to
    attack recklessly, giving you advantage on melee weapon attack rolls
    using STR during this turn, but attack rolls against you have
    advantage until your next turn."""

    ########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Reckless Attack", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class TestBarbarianRage(unittest.TestCase):
    """Test Rage"""

    ########################################################################
    def setUp(self) -> None:
        self.arena = Arena()
        self.barb = Barbarian(name="Babs", side="a", level=2, gear=[Greataxe()])
        self.arena.add_combatant(self.barb, coords=(1, 1))
        self.orc = Orc(side="b", hp=20)
        self.arena.add_combatant(self.orc, coords=(2, 2))

    ########################################################################
    def test_rage(self) -> None:
        """Lets get angry"""
        self.assertFalse(self.barb.has_effect("Rage"))
        rage = self.barb.pick_action_by_name("Barbarian Rage")
        assert rage is not None
        rage.perform_action()
        self.assertTrue(self.barb.has_effect("Rage"))
        self.barb.hit(Damage(10, DamageType.PIERCING), self.orc, False, "Test")
        # Take half damage from piercing etc.
        self.assertEqual(self.barb.hp, self.barb.max_hp - 5)

        self.barb.hit(Damage(10, DamageType.NECROTIC), self.orc, False, "Test")
        # Take full damage from non-piercing etc.
        self.assertEqual(self.barb.hp, self.barb.max_hp - 5 - 10)

        axe = self.barb.pick_action_by_name("Greataxe")
        assert axe is not None
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19  # Hit target
            with patch.object(dice, "roll") as mock_dice:
                mock_dice.return_value = 3
                self.barb.target = self.orc
                axe.perform_action()
        # Dmg = 3 from axe, 3 from prof, 2 from rage
        self.assertEqual(self.orc.hp, self.orc.max_hp - 3 - 3 - 2)


# EOF
