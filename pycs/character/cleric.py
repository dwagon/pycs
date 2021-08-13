""" Cleric """
import colors
from attacks import MeleeAttack
from spells.sacred_flame import Sacred_Flame
from spells.guiding_bolt import Guiding_Bolt
from spells.cure_wounds import Cure_Wounds
from spells.healing_word import Healing_Word
from constants import DamageType
from constants import SpellType
from .character import Character


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
            }
        )
        if level == 1:
            self.spell_slots = {1: 2}
            self.spell_modifier = 3
            kwargs["hp"] = 10
        elif level == 2:
            self.spell_slots = {1: 3}
            self.spell_modifier = 3
            kwargs["hp"] = 17
        elif level == 3:
            self.spell_slots = {1: 4, 2: 1}
            kwargs["hp"] = 24
        elif level == 4:
            pass
        elif level == 5:
            pass
        elif level == 6:
            pass

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
        self.add_action(Sacred_Flame())
        self.add_action(Guiding_Bolt())
        self.add_action(Cure_Wounds())
        self.add_action(Healing_Word())

    ##########################################################################
    def report(self):
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
        heal_spells = [_ for _ in self.spell_actions() if _.is_type(SpellType.HEALING)]
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
            for actn in self.spell_actions():
                if actn.is_type(SpellType.HEALING):
                    # Sort by amount it can cure, then lowest spell level, then enforce no collision
                    heals.append((actn.max_cure(self, self.target), 10-actn.level, id(actn), actn))
            heals.sort(reverse=True)
            return heals[0][-1]
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
