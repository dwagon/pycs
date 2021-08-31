""" Warlock """
import colors
from pycs.attack import MeleeAttack
from pycs.attack import RangedAttack
from pycs.character import Character
from pycs.constant import ActionType
from pycs.constant import DamageType
from pycs.constant import Race
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.spells import Burning_Hands

# from pycs.spells import Command
from pycs.spells import Eldritch_Blast
from pycs.spells import Fireball

# from pycs.spells import Frostbite
from pycs.spells import Hellish_Rebuke

# from pycs.spells import Poison_Spray
from pycs.spells import Scorching_Ray
from pycs.spells import Shatter
from pycs.spells import Thunderclap


##############################################################################
class Warlock(Character):
    """Warlock class"""

    def __init__(self, level, **kwargs):
        self.level = level
        kwargs.update(
            {
                "str": 8,
                "dex": 14,
                "con": 14,
                "int": 12,
                "wis": 11,
                "cha": 17,
                "ac": 13,
                "race": Race.HALFELF,
                "spellcast_bonus_stat": Stat.CHA,
                "action_preference": {
                    SpellType.RANGED: 5,
                    SpellType.MELEE: 3,
                    ActionType.RANGED: 2,
                    ActionType.MELEE: 1,
                },
            }
        )
        if level == 1:
            kwargs["hp"] = 10
        if level == 2:
            kwargs["hp"] = 17
        if level == 3:
            kwargs["hp"] = 24
        if level == 4:
            kwargs["hp"] = 31
        if level == 5:
            kwargs["hp"] = 38

        super().__init__(**kwargs)

        if level >= 1:
            self.spell_slots = 1
            self.add_action(Eldritch_Blast())
            # self.add_action(Frostbite())
            # self.add_action(Poison_Spray())
            self.add_action(Burning_Hands())
            self.add_action(Hellish_Rebuke())
        if level >= 2:
            self.spell_slots = 2
            # self.add_action(Command())
            # Agonizing Blast
            # When you cast eldritch blast, add your Charisma modifier to the
            # damage it deals on a hit.
            # Armor of Shadows
            # You can cast mage armor on yourself at will, without expending
            # a spell slot or material components.
        if level >= 3:
            self.add_action(Scorching_Ray())
            # Pact Boon: Pact of the Blades
            # Summon magical weapon
        if level >= 4:
            self.add_action(Shatter())
            self.add_action(Thunderclap())
            self.stats[Stat.CHA] = 19
        if level >= 5:
            self.add_action(Fireball())

        self.add_action(
            MeleeAttack(
                "Quarterstaff",
                reach=5,
                dmg=("1d6", 0),
                dmg_type=DamageType.BLUDGEONING,
            )
        )
        self.add_action(
            RangedAttack(
                "Light Crossbow",
                s_range=80,
                l_range=320,
                dmg=("1d8", 0),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def report(self):
        super().report()
        print(f"| Spells: {self.spell_slots}")

    ########################################################################
    def spell_available(self, spell):
        """Do we have enough slots to cast a spell"""
        if spell.level == 0:
            return True
        if self.spell_slots > 0:
            return True
        return False

    ########################################################################
    def cast(self, spell):
        """Cast a spell"""
        if spell.level == 0:  # Cantrip
            return
        self.spell_slots -= 1

    ########################################################################
    def shortrepr(self):
        """What a warlock looks like in the arena"""
        if self.is_alive():
            return colors.blue("W", bg="green")
        return colors.blue("W", bg="red")


# EOF
