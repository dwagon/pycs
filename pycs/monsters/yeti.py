""" Yeti Monster Class """
from typing import Any, Optional
import unittest
from collections import namedtuple
import colors
import dice
from pycs.action import Action
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
class Yeti(Monster):
    """Yeti - https://www.dndbeyond.com/monsters/yeti"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "6d10+18",
                "ac": 12,
                "speed": 40,
                "challenge": 3,
                "type": MonsterType.MONSTROSITY,
                "str": 18,
                "dex": 13,
                "con": 16,
                "int": 8,
                "wis": 12,
                "cha": 7,
                "immunity": [DamageType.COLD],
                "actions": [YetiMultiAttack()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a yeti looks like on the arena"""
        if self.is_alive():
            return colors.blue("Y")
        return colors.blue("Y", bg="red")


##############################################################################
##############################################################################
##############################################################################
class YetiMultiAttack(Action):
    """Multiattack. The yeti can use its Chilling Gaze and makes two claw attacks."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the attack"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 6:
            return 1
        return 0

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the attack"""
        claw = MeleeAttack(
            "Claw",
            reach=5,
            dmg=("1d6", 0),
            dmg_type=DamageType.SLASHING,
            side_effect=self.cold_claw,
            owner=self.owner,
        )
        claw.do_attack()
        claw.do_attack()
        self.chill_glaze()
        return True

    ##########################################################################
    def cold_claw(
        self, source: Creature, target: Creature, dmg: int
    ) -> None:  # pylint: disable=unused-argument
        """Additional 1d6 Cold damage to claw"""
        cold_dmg = int(dice.roll("1d6"))
        target.hit(cold_dmg, DamageType.COLD, source, False, "Yeti Cold Claws")

    ##########################################################################
    def chill_glaze(self) -> None:
        """Chilling Gaze. The yeti targets one creature it can see
        within 30 feet of it. If the target can see the yeti, the target
        must succeed on a DC 13 Constitution saving throw against this
        magic or take 10 (3d6) cold damage and then be paralyzed for 1
        minute, unless it is immune to cold damage. The target can
        repeat the saving throw at the end of each of its turns, ending
        the effect on itself on a success. If the target’s saving throw
        is successful, or if the effect ends on it, the target is immune
        to the Chilling Gaze of all yetis (but not abominable yetis)
        for 1 hour."""
        target = self.pick_chill_target()
        if not target:
            return
        dmg = int(dice.roll("3d6"))
        svth = target.saving_throw(Stat.CON, 13)
        if not svth:
            print(f"{self.owner} doing Chilling Glaze at {target}")
            target.add_effect(ChillGlazeEffect(cause=self))
            target.hit(dmg, DamageType.COLD, self.owner, False, "Chilling Glaze")
        else:
            print(f"{target} saved against Chilling Glaze - no effect")

    ##########################################################################
    def pick_chill_target(self) -> Optional[Creature]:
        """Who to attack"""
        result = namedtuple("result", "health id target")
        targets = [
            result(_.hp, id(_), _)
            for _ in self.owner.pick_closest_enemy()
            if self.owner.distance(_) <= 30 / 5 and DamageType.COLD not in _.immunity
        ]
        if not targets:
            return None
        targets.sort()
        print(f"Yeti chill glazes {targets=}")
        return targets[-1].target


##############################################################################
##############################################################################
##############################################################################
class ChillGlazeEffect(Effect):
    """Effect of Chill Glaze"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Yeti Chill Glaze", **kwargs)

    ##########################################################################
    def initial(self, target: Creature) -> None:
        target.add_condition(Condition.PARALYZED)

    ##########################################################################
    def removal_end_of_its_turn(self, victim: Creature) -> bool:
        """Do we recover from paralysis"""
        svth = victim.saving_throw(Stat.CON, 13)
        if svth:
            print(f"{victim} no longer paralyzed from Yeti's Chill Touch")
            victim.remove_condition(Condition.PARALYZED)
            return True
        return False


##############################################################################
##############################################################################
##############################################################################
class TestYeti(unittest.TestCase):
    """Test Yeti"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the glacier"""
        self.arena = Arena()
        self.beast = Yeti(side="a")
        self.arena.add_combatant(self.beast)


# EOF
