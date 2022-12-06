""" Wraith Monster Class """
from typing import Any
import unittest
from unittest.mock import patch
import colors
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Condition
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.monster import Monster


##############################################################################
class Wraith(Monster):
    """Wraith - https://www.dndbeyond.com/monsters/wraith"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        kwargs.update(
            {
                "hitdice": "9d8+27",
                "ac": 13,
                "speed": 60,
                "challenge": 5,
                "type": MonsterType.UNDEAD,
                "str": 6,
                "dex": 16,
                "con": 16,
                "int": 12,
                "wis": 14,
                "cha": 15,
                "prof_bonus": 3,
                "immunity": [DamageType.POISON, DamageType.NECROTIC],
                "resistant": [
                    DamageType.ACID,
                    DamageType.COLD,
                    DamageType.FIRE,
                    DamageType.LIGHTNING,
                    DamageType.THUNDER,
                    DamageType.BLUDGEONING,
                    DamageType.PIERCING,
                    DamageType.SLASHING,
                ],
                "cond_immunity": [
                    Condition.CHARMED,
                    Condition.EXHAUSTION,
                    Condition.GRAPPLED,
                    Condition.PARALYZED,
                    Condition.PETRIFIED,
                    Condition.POISONED,
                    Condition.PRONE,
                    Condition.RESTRAINED,
                ],
                "actions": [
                    MeleeAttack(
                        "Life Drain",
                        finesse=True,
                        reach=5,
                        dmg=("4d8", 0),
                        dmg_type=DamageType.NECROTIC,
                        side_effect=self.life_drain,
                    )
                ],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def life_drain(
        self, source: Creature, target: Creature, dmg: int
    ) -> None:  # pylint: disable=unused-argument
        """The target must succeed on a DC 14 Constitution saving throw
        or its hit point maximum is reduced by an amount equal to the damage
        taken. This reduction lasts until the target finishes a long rest.
        The target dies if this effect reduces its hit point maximum to 0."""
        svth = target.saving_throw(Stat.CON, 14)
        if svth:
            print(f"{target} resisted Wraith life drain")
        else:
            print(f"Wraith life drain's {target} of {dmg} hit points")
            target.max_hp = max(target.max_hp - dmg, 0)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a wraith looks like on the arena"""
        if self.is_alive():
            return colors.red("W")
        return colors.green("W", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TestWraith(unittest.TestCase):
    """Test Wraith"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the crypt"""
        self.arena = Arena()
        self.beast = Wraith(side="a")
        self.arena.add_combatant(self.beast, coords=(1, 1))
        self.victim = Monster(str=11, int=11, dex=11, wis=11, con=11, cha=11, hp=50, side="b")
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_drain(self) -> None:
        """Test life drain"""
        lfdr = self.beast.pick_action_by_name("Life Drain")
        assert lfdr is not None
        self.beast.target = self.victim

        # Ensure we hit
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [19, 19]
            lfdr.perform_action()
            self.assertLess(self.victim.hp, 50)

            # Victim saves
            self.assertEqual(self.victim.max_hp, 50)

        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [19, 1]
            lfdr.perform_action()
            self.assertLess(self.victim.hp, 50)

            # Victim fails to save
            self.assertLess(self.victim.max_hp, 50)


# EOF
