""" Cleric """
import colors
from attacks import MeleeAttack
from attacks import SpellAttack
from actions import SpellHealing
from constants import DamageType
from constants import Stat
from .character import Character


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
                "ac": 18,
                "hp": 10,
            }
        )
        self.spell_slots = {1: 2}
        self.spell_modifier = 3
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Mace",
                reach=5,
                bonus=4,
                dmg=("1d6", 2),
                dmg_type=DamageType.BLUDGEONING,
            )
        )
        self.add_action(
            SpellAttack(
                "Sacred Flame",
                reach=60,
                style="save",
                save=(Stat.DEX, 13),
                dmg=("1d8", 0),
                dmg_type=DamageType.RADIANT,
                level=0,
            )
        )
        self.add_action(
            SpellAttack(
                "Guiding Bolt",
                reach=120,
                bonus=5,
                dmg=("4d6", 5),
                dmg_type=DamageType.RADIANT,
                level=1,
            )
        )
        self.add_action(
            SpellHealing(
                "Cure Wounds",
                reach=5,
                cure=("1d8", 3),
                level=1,
            )
        )
        self.add_action(
            SpellHealing(
                "Healing Word",
                reach=60,
                cure=("1d4", 3),
                level=1,
            )
        )

    ##########################################################################
    def spell_available(self, spell):
        """Do we have enough slots to cast a spell"""
        if spell.level == 0:
            return True
        if self.spell_slots[spell.level] > 0:
            return True
        return False

    ##########################################################################
    def find_most_hurt(self):
        """Find who is the most hurt on our side"""
        target = None
        pct_hurt = 0.0
        for person in self.arena.remaining_participants()[self.side]:
            hurt = 1 - person.hp / person.max_hp
            if hurt > pct_hurt:
                pct_hurt = hurt
                target = person
        if pct_hurt < 0.5:  # No one is too hurt
            target = None
        return target

    ##########################################################################
    def pick_target(self):
        """See if anyone needs healing"""
        heal_spells = [_ for _ in self.actions if isinstance(_, SpellHealing)]
        for spell in heal_spells:
            if self.spell_slots[spell.level] > 0:  # Spells healing available
                self.target = self.find_most_hurt()
                if self.target:
                    return
        super().pick_target()

    ##########################################################################
    def choose_action(self):
        """Try and heal first then attack"""
        if self.target and self.target.side == self.side:
            heals = []
            for actn in self.actions:
                if issubclass(actn.__class__, SpellHealing):
                    heals.append((actn.max_cure(self), actn))
            heals.sort(reverse=True)
            return heals[0][1]
        else:
            return super().choose_action()

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


# EOF
