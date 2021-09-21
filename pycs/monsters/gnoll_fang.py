""" https://www.dndbeyond.com/monsters/gnoll"""
import unittest
import colors
import dice
from pycs.action import Action
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Stat
from pycs.gear import Hide
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class GnollFangOfYeenoghu(Monster):
    """Gnoll Fang Of Yeenoghu"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "10d8+20",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 17,
                "dex": 15,
                "con": 15,
                "int": 10,
                "wis": 11,
                "cha": 13,
                "gear": [Hide()],
                "actions": [FangMultiAttack()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):  # pragma: no cover
        """What a gnoll looks like on the arena"""
        if self.is_alive():
            return colors.blue("F")
        return colors.green("F", bg="red")


##############################################################################
##############################################################################
##############################################################################
class FangMultiAttack(Action):
    """Handle a multi-attack: bite, claw, claw"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def perform_action(self):
        """Do the attack"""
        bite = MeleeAttack(
            "Bite",
            reach=5,
            dmg=("1d6", 0),
            dmg_type=DamageType.PIERCING,
            side_effect=self.gnoll_bite,
            owner=self.owner,
        )
        claw = MeleeAttack(
            "Claw",
            reach=5,
            dmg=("1d8", 0),
            dmg_type=DamageType.SLASHING,
            owner=self.owner,
        )
        bite.do_attack()
        claw.do_attack()
        claw.do_attack()

    ##########################################################################
    def heuristic(self):
        """Should we do the attack"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 1
        return 0

    ##########################################################################
    def gnoll_bite(
        self, source, target, dmg
    ):  # pylint: disable=unused-argument, no-self-use
        """Gnoll bites can be pretty nasty"""
        svth = target.saving_throw(Stat.CON, 12)
        if not svth:
            dmg = int(dice.roll("2d6"))
            target.hit(dmg, DamageType.POISON, source, False, "Gnoll Fang Bite Poison")


##############################################################################
##############################################################################
##############################################################################
class TestGnoll(unittest.TestCase):
    """Test GnollFangOfYeenoghu"""

    ##########################################################################
    def setUp(self):
        """Set up the lair"""
        self.arena = Arena()
        self.beast = GnollFangOfYeenoghu(side="a")
        self.arena.add_combatant(self.beast, coords=(5, 5))
        self.victim = Monster(
            str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b"
        )
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_ac(self):
        """Test that the AC matches equipment"""
        self.assertEqual(self.beast.ac, 14)


# EOF
