""" Giant Frog Monster Class """
from typing import Any, Optional
import unittest
from unittest.mock import patch
import colors
import dice
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.monster import Monster


##############################################################################
class GiantFrog(Monster):
    """Giant Frog - https://www.dndbeyond.com/monsters/giant-frog"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "4d8",
                "ac": 11,
                "speed": 30,
                "type": MonsterType.BEAST,
                "str": 12,
                "dex": 13,
                "con": 11,
                "int": 2,
                "wis": 10,
                "cha": 3,
                "actions": [
                    MeleeAttack(
                        "Bite",
                        reach=5,
                        dmg=("1d6", 0),
                        dmg_type=DamageType.PIERCING,
                        heuristic=self.frog_bite,
                        side_effect=self.bite_swallow,
                    )
                ],
            }
        )
        super().__init__(**kwargs)
        self._swallowed: Optional[Creature] = None

    ##########################################################################
    def bite_swallow(self, source: Creature, target: Creature, dmg: int) -> None:  # pylint: disable=unused-argument
        """Swallow. The frog makes one bite attack against a Small or smaller target
        it is grappling. If the attack hits, the target is swallowed, and the grapple
        ends. The swallowed target is blinded and restrained, it has total cover
        against attacks and other effects outside the frog, and it takes 5 (2d4) acid
        damage at the start of each of the frog's turns.  The frog can have only
        one target swallowed at a time. If the frog dies, a swallowed creature is
        no longer restrained by it and can escape from the corpse using 5 feet
        of movement, exiting prone."""
        if self.has_grappled == target and self._swallowed is None:
            print(f"{self} swallowed {target}")
            target.add_effect(GiantFrogSwallowEffect(source=self))
            self.ungrapple()
            self._swallowed = target
            return

        self.grapple(target, escape_dc=11)

    ##########################################################################
    def report(self) -> None:
        """Additional reporting"""
        super().report()
        if self._swallowed:
            print(f"| Swallowed: {self._swallowed}")

    ##########################################################################
    def frog_bite(self) -> int:
        """When is it good to bite"""
        return 1

    ##########################################################################
    def fallen_unconscious(self, dmg: int, dmg_type: DamageType, critical: bool) -> None:
        """Frog has died"""
        if self._swallowed:
            self._swallowed.remove_condition(Condition.RESTRAINED)
            self._swallowed.remove_condition(Condition.BLINDED)
            self._swallowed.remove_effect("Giant Frog Swallow")
            print(f"{self._swallowed} escapes from being swallowed by {self.name}")
            self._swallowed = None
        super().fallen_unconscious(dmg, dmg_type, critical)

    ##########################################################################
    def shortrepr(self) -> str:
        """What it looks like on the arena"""
        if self.is_alive():
            return colors.green("F")
        return colors.green("F", bg="red")


##############################################################################
##############################################################################
##############################################################################
class GiantFrogSwallowEffect(Effect):
    """Swallow. The frog makes one bite attack against a Small or smaller
    target it is grappling. If the attack hits, the target is swallowed,
    and the grapple ends. The swallowed target is blinded and restrained,
    it has total cover against attacks and other effects outside the
    frog, and it takes 5 (2d4) acid damage at the start of each of the
    frog's turns. The frog can have only one target swallowed at a time.
    If the frog dies, a swallowed creature is no longer restrained by
    it and can escape from the corpse using 5 feet of movement, exiting
    prone."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Giant Frog Swallow", **kwargs)
        self.target = None

    ##########################################################################
    def initial(self, target: Creature) -> None:
        """Initial effect"""
        target.add_condition(Condition.RESTRAINED)
        target.add_condition(Condition.BLINDED)

    ##########################################################################
    def hook_start_turn(self) -> None:
        dmg = int(dice.roll("2d4"))
        assert self.target is not None
        self.target.hit(
            dmg=dmg,
            dmg_type=DamageType.ACID,
            source=self.owner,
            critical=False,
            atkname="Frog Acid",
        )
        print(f"{self.target} hurt by {dmg} acid from being swallowed by Giant Frog")


##############################################################################
##############################################################################
##############################################################################
class TestGiantFrog(unittest.TestCase):
    """Test Giant Frog"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the swamp"""
        self.arena = Arena()
        self.beast = GiantFrog(side="a")
        self.arena.add_combatant(self.beast, coords=(1, 1))
        self.victim = Monster(
            name="Victim",
            str=11,
            int=11,
            dex=11,
            wis=11,
            con=11,
            cha=11,
            hp=20,
            side="b",
        )
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_bite(self) -> None:
        """Test a frog nibble"""
        att = self.beast.pick_action_by_name("Bite")
        assert att is not None
        self.beast.target = self.victim
        # Bite the victim to grapple
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [19, 18, 2]  # To hit, To grapple, To avoid grapple
            att.perform_action()
        self.assertEqual(self.beast.has_grappled, self.victim)

        # Bite again to swallow
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [17, 16]  # To hit
            att.perform_action()
        self.assertEqual(self.beast._swallowed, self.victim)  # pylint: disable=protected-access
        self.assertTrue(self.victim.has_effect("Giant Frog Swallow"))
        self.assertIsNone(self.beast.has_grappled)
        self.assertFalse(self.victim.has_condition(Condition.GRAPPLED))
        self.assertTrue(self.victim.has_condition(Condition.RESTRAINED))
        self.assertTrue(self.victim.has_condition(Condition.BLINDED))


# EOF
