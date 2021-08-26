""" Cleric """
import colors
from pycs.attacks import MeleeAttack
from pycs.actions import Action
from pycs.effect import Effect
from pycs.spell.aid import Aid
from pycs.spell.beacon_of_hope import Beacon_Of_Hope
from pycs.spell.bless import Bless
from pycs.spell.cure_wounds import Cure_Wounds
from pycs.spell.enhance_ability import Enhance_Ability
from pycs.spell.guiding_bolt import Guiding_Bolt
from pycs.spell.healing_word import Healing_Word
from pycs.spell.hold_person import Hold_Person
from pycs.spell.lesser_restoration import Lesser_Restoration
from pycs.spell.mass_healing_word import Mass_Healing_Word
from pycs.spell.sacred_flame import Sacred_Flame
from pycs.spell.shield_of_faith import Shield_Of_Faith
from pycs.spell.spirit_guardians import Spirit_Guardians
from pycs.spell.spiritual_weapon import Spiritual_Weapon
from pycs.constants import DamageType
from pycs.constants import MonsterType
from pycs.constants import SpellType
from pycs.constants import Stat
from pycs.constants import ActionType
from pycs.characters import Character


##############################################################################
##############################################################################
##############################################################################
class Cleric(Character):
    """Cleric class"""

    ##########################################################################
    def __init__(self, level=1, **kwargs):
        self.level = level
        kwargs.update(
            {
                "str": 14,
                "dex": 9,
                "con": 15,
                "int": 11,
                "wis": 16,
                "cha": 13,
                "ac": 18,
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
            }
        )
        if level == 1:
            self.spell_slots = {1: 2}
            kwargs["hp"] = 10
        elif level == 2:
            self.spell_slots = {1: 3}
            kwargs["hp"] = 17
        elif level == 3:
            self.spell_slots = {1: 4, 2: 2}
            kwargs["hp"] = 24
        elif level == 4:
            kwargs["hp"] = 31
            self.spell_slots = {1: 4, 2: 3}
        elif level == 5:
            kwargs["hp"] = 38
            self.spell_slots = {1: 4, 2: 3, 3: 2}
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Mace",
                reach=5,
                dmg=("1d6", 0),
                dmg_type=DamageType.BLUDGEONING,
            )
        )
        self.add_action(Bless())  # Life Domain freebie
        self.add_action(Cure_Wounds())  # Life Domain freebie
        self.add_action(Sacred_Flame())
        self.add_action(Guiding_Bolt())
        self.add_bonus_action(Healing_Word())
        self.add_bonus_action(Shield_Of_Faith())
        if level >= 2:
            self.add_action(TurnUndead())
        if level >= 3:
            self.add_action(Aid())
            self.add_action(Lesser_Restoration())  # Life Domain freebie
            self.add_action(Enhance_Ability())
            self.add_bonus_action(Spiritual_Weapon())  # Life Domain freebie
            self.add_action(Hold_Person())
        if level >= 4:
            self.stats[Stat.WIS] = 18
        if level >= 5:
            self.add_action(Beacon_Of_Hope())  # Life Domain freebie
            self.add_bonus_action(Mass_Healing_Word())
            self.add_action(Spirit_Guardians())

    ##########################################################################
    def report(self):
        """Character report"""
        super().report()
        print(f"| Spells: {self.spell_slots}")

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
    def shortrepr(self):
        """What a cleric looks like in the arena"""
        if self.is_alive():
            return colors.blue("C", bg="green")
        else:
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
        name = "Turn Undead"
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do this"""
        return 0  # Not finished yet

    ##########################################################################
    def perform_action(self, source):
        """Do the action"""
        undead = [
            _
            for _ in source.arena.combatants
            if _.side != source.side and _.is_type(MonsterType.UNDEAD)
        ]
        for und in undead:
            if source.arena.distance(source, und) < 30 / 5:
                if und.saving_throw(Stat.WIS, 10 + source.spellcast_modifier):
                    print(f"{und} has been turned by {source}")
                    und.add_effect(TurnedUndeadEffect())

    ##########################################################################
    def recover(self, undead):  # pylint: disable=unused-argument
        """Did we recover from being turned"""
        return False


##############################################################################
##############################################################################
##############################################################################
class TurnedUndeadEffect(Effect):
    """Still to do"""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Turned", **kwargs)


# EOF
