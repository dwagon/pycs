""" Warlock """
import colors
from attacks import MeleeAttack
from attacks import RangedAttack
from spells import AttackSpell
from constants import ActionType
from constants import DamageType
from constants import SpellType
from constants import Stat
from .character import Character


##############################################################################
class Warlock(Character):
    """Warlock class"""

    def __init__(self, level, **kwargs):
        self.level = level
        kwargs.update(
            {
                "str": 9,
                "dex": 14,
                "con": 15,
                "int": 13,
                "wis": 11,
                "cha": 16,
                "ac": 13,
                "hp": 10,
                "spellcast_bonus": Stat.CHA,
                "action_preference": {
                    SpellType.RANGED: 5,
                    SpellType.MELEE: 3,
                    ActionType.RANGED: 2,
                    ActionType.MELEE: 1,
                },
            }
        )
        self.spell_slots = 1
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Mace",
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
        self.add_action(
            AttackSpell(
                "Eldritch Blast",
                reach=120,
                dmg=("1d10", 0),
                level=0,
                dmg_type=DamageType.FORCE,
            )
        )
        self.add_action(
            AttackSpell(
                "Burning Hands",
                style="save",
                reach=15,
                save=(Stat.DEX, 13),
                dmg=("1d6", 0),
                level=1,
                dmg_type=DamageType.FIRE,
            )
        )
        self.add_reaction(
            AttackSpell(
                "Hellish Rebuke",
                reach=60,
                dmg=("2d10", 0),
                level=1,
                dmg_type=DamageType.FIRE,
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
