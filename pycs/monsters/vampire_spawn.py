""" Vampire Spawn Monster Class """
from typing import Any
import unittest
from unittest.mock import patch
import colors
import dice
from pycs.attack import Action
from pycs.arena import Arena
from pycs.attack import MeleeAttack
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.creature import Creature
from pycs.monster import Monster


##############################################################################
class VampireSpawn(Monster):
    """Wraith - https://www.dndbeyond.com/monsters/vampire-spawn"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        self._regen = 5
        kwargs.update(
            {
                "hitdice": "11d8+33",
                "ac": 15,
                "speed": 30,
                "challenge": 5,
                "type": MonsterType.UNDEAD,
                "str": 16,
                "dex": 16,
                "con": 16,
                "int": 11,
                "wis": 10,
                "cha": 12,
                "prof_bonus": 2,
                "resistant": [
                    DamageType.NECROTIC,
                    DamageType.BLUDGEONING,
                    DamageType.PIERCING,
                    DamageType.SLASHING,
                ],
                "actions": [VSMultiAttack()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def hook_start_turn(self) -> None:
        """Regeneration. The vampire regains 10 hit points at the
        start of its turn if it has at least 1 hit point and isn't
        in sunlight or running water. If the vampire takes radiant
        damage or damage from holy water, this trait doesn't function
        at the start of the vampire's next turn."""
        for hit in self.damage_last_turn:
            if hit.type == DamageType.RADIANT:
                print(f"Not regenerating as took {hit.type.value} damage last turn")
                return
        # Don't come back from unconsciousness forever - can lead to loops
        if self.hp <= 0:
            self._regen -= 1
        if self._regen <= 0:
            print("Not regening as getting ridiculous")
            return
        if self.hp < self.max_hp:
            self.heal("", 10)

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a vampire spawn looks like on the arena"""
        if self.is_alive():
            return colors.red("V")
        return colors.green("V", bg="red")


##############################################################################
##############################################################################
##############################################################################
class VSMultiAttack(Action):
    """Vampire Spawn Multi Attack
    The vampire makes two attacks, only one of which can be a bite attack.
    """

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Multiattack", **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the attack"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 1
        return 0

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the attack"""
        bite = BiteAttack(owner=self.owner)
        claw = ClawAttack(owner=self.owner)
        claw.do_attack()
        if self.owner.has_grappled:
            bite.do_attack()
        else:
            claw.do_attack()
        return True


##############################################################################
##############################################################################
##############################################################################
class BiteAttack(MeleeAttack):
    """Vampire Spawn Bite Attack
    Bite. Melee Weapon Attack: +6 to hit, reach 5 ft., one willing
    creature, or a creature that is grappled by the vampire,
    incapacitated, or restrained. Hit: 6 (1d6 + 3) piercing damage
    plus 7 (2d6) necrotic damage. The target's hit point maximum
    is reduced by an amount equal to the necrotic damage taken, and
    the vampire regains hit points equal to that amount. The reduction
    lasts until the target finishes a long rest. The target dies
    if this effect reduces its hit point maximum to 0."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__(
            "Bite",
            dmg=("1d6", 0),
            dmg_type=DamageType.PIERCING,
            side_effect=self.bite_side_effect,
            **kwargs,
        )

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the attack"""
        if self.owner.has_grappled:
            return 5
        return 0

    ##########################################################################
    def bite_side_effect(
        self, source: Creature, target: Creature, dmg: int
    ) -> None:  # pylint: disable=unused-argument
        """Do the side_effect"""
        necro_dmg = int(dice.roll("2d6"))
        target.hit(necro_dmg, DamageType.NECROTIC, source, False, "Vampire Spawn Bite")
        print(f"Inflicted {necro_dmg} from the bite")
        source.heal("", necro_dmg)
        target.max_hp -= necro_dmg
        if target.max_hp <= 0:
            target.died()


##############################################################################
##############################################################################
##############################################################################
class ClawAttack(MeleeAttack):
    """Vampire Spawn Claw Attack
    Claws. Melee Weapon Attack: +6 to hit, reach 5 ft., one creature.
    Hit: 8 (2d4 + 3) slashing damage. Instead of dealing damage,
    the vampire can grapple the target (escape DC 13)."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Claws", dmg=("2d4", 0), dmg_type=DamageType.SLASHING, **kwargs)

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the attack"""
        enemy = self.owner.pick_closest_enemy()
        if enemy and self.owner.distance(enemy[0]) <= 1:
            return 1
        return 0

    ##########################################################################
    def do_attack(self) -> bool:
        """Do the attack"""
        if self.owner.has_grappled:
            super().do_attack()
        else:
            targ = self.pick_target()
            if targ and self.did_we_hit(targ):
                self.owner.grapple(targ, escape_dc=13)
        return True


##############################################################################
##############################################################################
##############################################################################
class TestVampireSpawn(unittest.TestCase):
    """Test VampireSpawn"""

    ##########################################################################
    def setUp(self) -> None:
        """Set up the crypt"""
        self.vict_max_hp = 50
        self.arena = Arena()
        self.beast = VampireSpawn(side="a")
        self.arena.add_combatant(self.beast, coords=(1, 1))
        self.victim = Monster(
            str=11,
            int=11,
            dex=11,
            wis=11,
            con=11,
            cha=11,
            hp=self.vict_max_hp,
            side="b",
        )
        self.arena.add_combatant(self.victim, coords=(1, 2))

    ##########################################################################
    def test_grapple_attack(self) -> None:
        """Test attack with grapple"""
        multiatt = self.beast.pick_action_by_name("Multiattack")
        assert multiatt is not None
        self.beast.target = self.victim
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [
                18,  # Claw to hit
                20,  # Grapple attack
                1,  # Save by victim
                1,  # Bite to hit
            ]
            multiatt.perform_action()
        self.assertTrue(self.victim.has_condition(Condition.GRAPPLED))
        self.assertEqual(self.victim.damage_this_turn, [])

    ##########################################################################
    def test_already_grapple_attack(self) -> None:
        """Test attack with grapple already in place"""
        self.beast.hp = 10
        multiatt = self.beast.pick_action_by_name("Multiattack")
        assert multiatt is not None
        self.beast.target = self.victim
        self.victim.add_condition(Condition.GRAPPLED)
        self.beast.has_grappled = self.victim
        with patch.object(Creature, "rolld20") as mock:
            mock.side_effect = [
                18,  # Claw to hit
                17,  # Bite to hit
            ]
            multiatt.perform_action()
        found_claw = False
        found_bite = False
        found_suck = False
        for dmg in self.victim.damage_this_turn:
            if dmg.type == DamageType.SLASHING:
                found_claw = True
            if dmg.type == DamageType.PIERCING:
                found_bite = True
            if dmg.type == DamageType.NECROTIC:
                found_suck = True
                suck_dmg = dmg.hp
        self.assertTrue(found_claw)
        self.assertTrue(found_bite)
        self.assertTrue(found_suck)
        self.assertEqual(self.beast.hp, 10 + suck_dmg)
        self.assertEqual(self.victim.max_hp, self.vict_max_hp - suck_dmg)


# EOF
