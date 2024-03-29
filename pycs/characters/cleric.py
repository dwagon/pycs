""" https://www.dndbeyond.com/classes/cleric """
from typing import Any
import unittest
from unittest.mock import patch
import colors
from pycs.action import Action
from pycs.arena import Arena
from pycs.character import Character
from pycs.constant import ActionType, DamageType, MonsterType, SpellType, Stat
from pycs.creature import Creature
from pycs.damage import Damage
from pycs.effect import Effect
from pycs.monsters import Skeleton
from pycs.spell import SpellAction
from pycs.spells import Aid
from pycs.spells import BeaconOfHope
from pycs.spells import Bless
from pycs.spells import CureWounds
from pycs.spells import EnhanceAbility
from pycs.spells import GuidingBolt
from pycs.spells import HealingWord
from pycs.spells import HoldPerson
from pycs.spells import LesserRestoration
from pycs.spells import MassHealingWord
from pycs.spells import SacredFlame
from pycs.spells import ShieldOfFaith
from pycs.spells import SpiritGuardians
from pycs.spells import SpiritualWeapon


##############################################################################
##############################################################################
##############################################################################
class Cleric(Character):
    """Cleric class"""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        self.channel_divinity = 0
        kwargs.update(
            {
                "str": 14,
                "dex": 9,
                "con": 15,
                "int": 11,
                "wis": 16,
                "cha": 13,
                "stat_prof": [Stat.WIS, Stat.CHA],
                "spellcast_bonus_stat": Stat.WIS,
                "action_preference": {
                    SpellType.HEALING: 5,
                    TurnUndead: 3,
                    SpellType.BUFF: 3,
                    SpellType.RANGED: 2,
                    ActionType.RANGED: 2,
                    SpellType.MELEE: 1,
                    ActionType.MELEE: 1,
                },
                "actions": [
                    Bless(),  # Life Domain freebie
                    CureWounds(),  # Life Domain freebie
                    SacredFlame(),
                    GuidingBolt(),
                    HealingWord(),
                    ShieldOfFaith(),
                ],
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            self.destroy_undead = 0.0
            self.spell_slots = {1: 2}
            kwargs["hp"] = 10
        if level >= 2:
            self.channel_divinity = 1
            self.spell_slots = {1: 3}
            kwargs["hp"] = 17
            kwargs["actions"].append(TurnUndead())
        if level >= 3:
            self.spell_slots = {1: 4, 2: 2}
            kwargs["hp"] = 24
            kwargs["actions"].append(Aid())
            kwargs["actions"].append(LesserRestoration())  # Life Domain freebie
            kwargs["actions"].append(EnhanceAbility())
            kwargs["actions"].append(SpiritualWeapon())  # Life Domain freebie
            kwargs["actions"].append(HoldPerson())
        if level >= 4:
            kwargs["hp"] = 31
            self.spell_slots = {1: 4, 2: 3}
            kwargs["wis"] = 18
        if level >= 5:
            self.destroy_undead = 0.5
            kwargs["hp"] = 38
            self.spell_slots = {1: 4, 2: 3, 3: 2}
            kwargs["actions"].append(BeaconOfHope())  # Life Domain freebie
            kwargs["actions"].append(MassHealingWord())
            kwargs["actions"].append(SpiritGuardians())
        super().__init__(**kwargs)

    ##########################################################################
    def report(self) -> None:
        """Character report"""
        super().report()
        print(f"|  Spells: {self.spell_slots}")

    ##########################################################################
    def spell_available(self, spell: SpellAction) -> bool:
        """Do we have enough slots to cast a spell"""
        if spell.level == 0:
            return True
        if self.spell_slots[spell.level] > 0:
            return True
        return False

    ##########################################################################
    def cast(self, spell: SpellAction) -> bool:
        """Cast a spell"""
        if spell.level == 0:
            return True
        if not self.spell_available(spell):
            return False
        self.spell_slots[spell.level] -= 1
        return True

    ##########################################################################
    def shortrepr(self) -> str:  # pragma: no cover
        """What a cleric looks like in the arena"""
        if self.is_alive():
            return colors.blue("C", bg="green")
        return colors.blue("C", bg="red")


##############################################################################
##############################################################################
##############################################################################
class TurnUndead(Action):
    """As an action, you present your holy symbol and speak a prayer
    censuring the undead. Each undead that can see or hear you within
    30 feet of you must make a Wisdom saving throw. If the creature
    fails its saving throw, it is turned for 1 minute or until it takes
    any damage.

    A turned creature must spend its turns trying to move as far away
    from you as it can, and it can’t willingly move to a space within
    30 feet of you. It also can’t take reactions. For its action, it
    can use only the Dash action or try to escape from an effect that
    prevents it from moving. If there’s nowhere to move, the creature
    can use the Dodge action

    Starting at 5th level, when an undead fails its saving throw against
    your Turn Undead feature, the creature is instantly destroyed if
    its challenge rating is at or below a certain threshold, as shown
    in the Destroy Undead table."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        super().__init__("Turn Undead", **kwargs)

    ##########################################################################
    def is_available(self) -> bool:
        return self.owner.channel_divinity >= 1

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do this"""
        heur = 0
        undead = self.owner.arena.remaining_type(self.owner, MonsterType.UNDEAD)
        for und in undead:
            if self.owner.arena.distance(self.owner, und) <= 30 / 5:
                heur += und.hp
        return heur

    ##########################################################################
    def perform_action(self) -> bool:
        """Do the action"""
        undead = self.owner.arena.remaining_type(self.owner, MonsterType.UNDEAD)
        self.owner.channel_divinity -= 1
        for und in undead:
            if self.owner.arena.distance(self.owner, und) <= 30 / 5:
                if not und.saving_throw(Stat.WIS, self.owner.spellcast_save):
                    if und.challenge is None:
                        print(f"ERROR: Need to specify challenge rating of {und}")
                        continue
                    if und.challenge <= self.owner.destroy_undead:
                        print(f"{und} has been destroyed by {self.owner}")
                        und.hit(Damage(und.hp, DamageType.RADIANT), self.owner, False, "Turn Undead")
                    else:
                        print(f"{und} has been turned by {self.owner}")
                        und.add_effect(TurnedUndeadEffect(cause=self.owner))
        return True


##############################################################################
##############################################################################
##############################################################################
class TurnedUndeadEffect(Effect):
    """A turned creature must spend its turns trying to move as far away
    from you as it can, and it can't willingly move to a space within
    30 feet of you. It also can't take reactions. For its action, it
    can use only the Dash action or try to escape from an effect that
    prevents it from moving. If there's nowhere to move, the creature
    can use the Dodge action"""

    ########################################################################
    def __init__(self, cause: Creature, **kwargs: Any):
        """Initialise"""
        kwargs["cause"] = cause  # Cleric who is doing the turning
        super().__init__("Turned", **kwargs)

    ########################################################################
    def flee(self) -> None:
        raise NotImplementedError


##############################################################################
##############################################################################
##############################################################################
class TestTurnUndead(unittest.TestCase):
    """Test Turning"""

    ########################################################################
    def setUp(self) -> None:
        self.arena = Arena()
        self.cleric = Cleric(name="Cyril", side="a", level=2)
        self.arena.add_combatant(self.cleric, coords=(1, 1))
        self.skel = Skeleton(side="b")
        self.arena.add_combatant(self.skel, coords=(2, 2))

    ########################################################################
    def test_turn_fail(self) -> None:
        """Test inflicting the turn and failing the save"""
        self.assertTrue(self.skel.is_alive())
        act = self.cleric.pick_action_by_name("Turn Undead")
        assert act is not None
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            act.perform_action()
            self.skel.report()
        self.assertTrue(self.skel.is_alive())
        self.assertTrue(self.skel.has_effect("Turned"))

    ########################################################################
    def test_turn_save(self) -> None:
        """Test inflicting the turn and making the save"""
        self.assertTrue(self.skel.is_alive())
        act = self.cleric.pick_action_by_name("Turn Undead")
        assert act is not None
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            act.perform_action()
        self.assertTrue(self.skel.is_alive())
        self.assertFalse(self.skel.has_effect("Turned"))

    ########################################################################
    def test_destroy(self) -> None:
        """Test inflicting the turn with senior cleric"""
        self.assertTrue(self.skel.is_alive())
        self.cleric = Cleric(name="St Cyril", side="a", level=5)
        self.arena.add_combatant(self.cleric, coords=(1, 1))
        act = self.cleric.pick_action_by_name("Turn Undead")
        assert act is not None
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            act.perform_action()
        self.assertFalse(self.skel.is_alive())


# EOF
