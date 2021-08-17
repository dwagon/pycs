""" Cleric """
import colors
from attacks import MeleeAttack
from actions import Action
from spell.aid import Aid
from spell.bless import Bless
from spell.cure_wounds import Cure_Wounds
from spell.guiding_bolt import Guiding_Bolt
from spell.healing_word import Healing_Word
from spell.lesser_restoration import Lesser_Restoration
from spell.enhance_ability import Enhance_Ability
from spell.sacred_flame import Sacred_Flame
from spell.shield_of_faith import Shield_Of_Faith
from spell.spiritual_weapon import Spiritual_Weapon
from constants import DamageType
from constants import MonsterType
from constants import SpellType
from constants import Stat
from constants import ActionType
from .character import Character


##############################################################################
##############################################################################
##############################################################################
class Cleric(Character):
    """Cleric class"""

    ##########################################################################
    def __init__(self, level=1, **kwargs):
        kwargs.update(
            {
                "str": 14,
                "dex": 9,
                "con": 15,
                "int": 11,
                "wis": 16,
                "cha": 13,
                "ac": 18,
                "spellcast_bonus": Stat.WIS,
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
            self.spell_slots = {1: 4, 2: 3}
        elif level == 5:
            self.spell_slots = {1: 4, 2: 3, 3: 2}
        elif level == 6:
            self.spell_slots = {1: 4, 2: 3, 3: 3}
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Mace",
                reach=5,
                dmg=("1d6", 2),
                dmg_type=DamageType.BLUDGEONING,
            )
        )
        self.add_action(Bless())  # Life Domain freebie
        self.add_action(Cure_Wounds())  # Life Domain freebie
        self.add_action(Sacred_Flame())
        self.add_action(Guiding_Bolt())
        self.add_action(Healing_Word())
        self.add_action(Shield_Of_Faith())
        if level >= 2:
            self.add_action(TurnUndead())
        if level >= 3:
            self.add_action(Aid())
            self.add_action(Lesser_Restoration())
            self.add_action(Enhance_Ability())
            self.add_action(Spiritual_Weapon())

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
            return
        self.spell_slots[spell.level] -= 1

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
    can use the Dodge action"""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Turn Undead"
        super().__init__(name, **kwargs)

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
                    und.add_effect("turned", self.recover)

    ##########################################################################
    def recover(self, undead):  # pylint: disable=unused-argument
        """Did we recover from being turned"""
        return False


# EOF
