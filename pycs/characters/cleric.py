""" https://www.dndbeyond.com/classes/cleric """
import colors
from pycs.action import Action
from pycs.character import Character
from pycs.constant import ActionType
from pycs.constant import MonsterType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.spells import Aid
from pycs.spells import Beacon_Of_Hope
from pycs.spells import Bless
from pycs.spells import CureWounds
from pycs.spells import Enhance_Ability
from pycs.spells import Guiding_Bolt
from pycs.spells import HealingWord
from pycs.spells import HoldPerson
from pycs.spells import LesserRestoration
from pycs.spells import MassHealingWord
from pycs.spells import Sacred_Flame
from pycs.spells import ShieldOfFaith
from pycs.spells import SpiritGuardians
from pycs.spells import Spiritual_Weapon


##############################################################################
##############################################################################
##############################################################################
class Cleric(Character):
    """Cleric class"""

    ##########################################################################
    def __init__(self, **kwargs):
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
                    TurnUndead: 4,
                    SpellType.BUFF: 3,
                    SpellType.RANGED: 2,
                    ActionType.RANGED: 2,
                    SpellType.MELEE: 1,
                    ActionType.MELEE: 1,
                },
                "actions": [
                    Bless(),  # Life Domain freebie
                    CureWounds(),  # Life Domain freebie
                    Sacred_Flame(),
                    Guiding_Bolt(),
                    HealingWord(),
                    ShieldOfFaith(),
                ],
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            self.destroy_undead = 0
            self.spell_slots = {1: 2}
            kwargs["hp"] = 10
        if level >= 2:
            self.spell_slots = {1: 3}
            kwargs["hp"] = 17
            kwargs["actions"].append(TurnUndead())
        if level >= 3:
            self.spell_slots = {1: 4, 2: 2}
            kwargs["hp"] = 24
            kwargs["actions"].append(Aid())
            kwargs["actions"].append(LesserRestoration())  # Life Domain freebie
            kwargs["actions"].append(Enhance_Ability())
            kwargs["actions"].append(Spiritual_Weapon())  # Life Domain freebie
            kwargs["actions"].append(HoldPerson())
        if level >= 4:
            kwargs["hp"] = 31
            self.spell_slots = {1: 4, 2: 3}
            kwargs["wis"] = 18
        if level >= 5:
            self.destroy_undead = 0.5
            kwargs["hp"] = 38
            self.spell_slots = {1: 4, 2: 3, 3: 2}
            kwargs["actions"].append(Beacon_Of_Hope())  # Life Domain freebie
            kwargs["actions"].append(MassHealingWord())
            kwargs["actions"].append(SpiritGuardians())
        super().__init__(**kwargs)

    ##########################################################################
    def report(self):
        """Character report"""
        super().report()
        print(f"|  Spells: {self.spell_slots}")

    ##########################################################################
    def spell_available(self, spell):
        """Do we have enough slots to cast a spell"""
        if spell.level == 0:
            return True
        if self.spell_slots[spell.level] > 0:
            return True
        return False

    ##########################################################################
    def cast(self, spell):
        """Cast a spell"""
        if spell.level == 0:
            return True
        if not self.spell_available(spell):
            return False
        self.spell_slots[spell.level] -= 1
        return True

    ##########################################################################
    def shortrepr(self):  # pragma: no cover
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
    def __init__(self, **kwargs):
        super().__init__("Turn Undead", **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do this"""
        heur = 0
        undead = self.owner.arena.remaining_type(self.owner, MonsterType.UNDEAD)
        for und in undead:
            heur += und.hp
        return heur

    ##########################################################################
    def perform_action(self):
        """Do the action"""
        undead = self.owner.arena.remaining_type(self.owner, MonsterType.UNDEAD)
        for und in undead:
            if self.owner.arena.distance(self.owner, und) <= 30 / 5:
                if not und.saving_throw(Stat.WIS, self.owner.spellcast_save):
                    if und.challenge <= self.owner.destroy_undead:
                        print(f"{und} has been destroyed by {self.owner}")
                        und.state = "UNCONSCIOUS"  # Make dead
                        und.hp = 0
                    else:
                        print(f"{und} has been turned by {self.owner}")
                        und.add_effect(TurnedUndeadEffect(cause=self.owner))


##############################################################################
##############################################################################
##############################################################################
class TurnedUndeadEffect(Effect):
    """A turned creature must spend its turns trying to move as far away
    from you as it can, and it can’t willingly move to a space within
    30 feet of you. It also can’t take reactions. For its action, it
    can use only the Dash action or try to escape from an effect that
    prevents it from moving. If there’s nowhere to move, the creature
    can use the Dodge action"""

    ########################################################################
    def __init__(self, cause, **kwargs):
        """Initialise"""
        self.cause = cause  # Cleric who is doing the turning
        super().__init__("Turned", **kwargs)

    ########################################################################
    def flee(self):
        return self.cause


# EOF
