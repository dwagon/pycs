""" Paladin """
import colors
import dice
from pycs.action import Action
from pycs.character import Character
from pycs.constant import ActionType
from pycs.constant import Condition
from pycs.constant import DamageType
from pycs.constant import Race
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.gear import Chainmail
from pycs.gear import Javelin
from pycs.gear import Longsword
from pycs.gear import Potion_Healing
from pycs.gear import Shield
from pycs.spells import Bless
from pycs.spells import BrandingSmite
from pycs.spells import CureWounds
from pycs.spells import LesserRestoration
from pycs.spells import Sanctuary
from pycs.spells import ShieldOfFaith

# from pycs.spells.protection_from_poison import Protection_From_Poison


##############################################################################
##############################################################################
##############################################################################
class Paladin(Character):
    """Paladin class"""

    ########################################################################
    def __init__(self, level, **kwargs):
        self.level = level
        self.channel_divinity = 0
        self.lay_on_hands = 0
        kwargs.update(
            {
                "str": 17,
                "dex": 10,
                "con": 14,
                "int": 8,
                "wis": 12,
                "cha": 14,
                "stat_prof": [Stat.WIS, Stat.CHA],
                "spellcast_bonus_stat": Stat.CHA,
                "race": Race.HALFORC,
                "action_preference": {
                    LayOnHands: 2,
                    SpellType.HEALING: 2,
                    SpellType.BUFF: 2,
                    BrandingSmite: 9,
                    ActionType.RANGED: 4,
                    ActionType.MELEE: 6,
                }
                # "immunity": DISEASE
            }
        )
        if level >= 1:
            kwargs["hp"] = 14
            self.spell_slots = {}
        if level >= 2:
            kwargs["hp"] = 20
            kwargs["ac"] = 19  # Defense fighting style
            self.spell_slots = {1: 2}
        if level >= 3:
            kwargs["hp"] = 28
            self.spell_slots = {1: 3}
            self.lay_on_hands = 15
            self.channel_divinity = 1
        if level >= 4:
            kwargs["hp"] = 36
            kwargs["str"] = 19
            self.lay_on_hands = 20
        if level >= 5:
            # Prof Bonus = 3
            kwargs["attacks_per_action"] = 2
            kwargs["hp"] = 44
            kwargs["str"] = 19
            self.spell_slots = {1: 4, 2: 2}
            self.lay_on_hands = 25

        super().__init__(**kwargs)
        if level >= 2:
            self.lay_on_hands = 5
            self.add_action(CureWounds())
            self.add_action(Bless())
            self.add_action(ShieldOfFaith())
            # Divine Smite
            # Starting at 2nd level, when you hit a creature with a melee weapon
            # attack, you can expend one spell slot to deal radiant damage to the
            # target, in addition to the weapon’s damage. The extra damage is 2d8
            # for a 1st-level spell slot, plus 1d8 for each spell level higher
            # than 1st, to a maximum of 5d8. The damage increases by 1d8 if the
            # target is an undead or a fiend, to a maximum of 6d8.
            self.add_action(LayOnHands())
        if level >= 3:
            self.add_action(Sanctuary())
            # Add Action Channel Divinity : Sacred Weapon
            # Add Action Channel Divinity : Turn the Unholy
        if level >= 5:
            self.add_action(BrandingSmite())
            self.add_action(LesserRestoration())
        #            self.add_action(Protection_From_Poison())
        self.add_gear(Chainmail(magic_bonus=1))
        self.add_gear(Shield(magic_bonus=1))
        self.add_gear(Potion_Healing(ammo=1))
        self.add_gear(Longsword(side_effect=self.flaming_sword))
        self.add_gear(Javelin(ammo=3))

    ########################################################################
    def flaming_sword(self, source, target, dmg):
        """Add some extra spice"""
        dmg = int(dice.roll("1d6"))
        target.hit(dmg, DamageType.FIRE, source, False, "Flaming Sword")

    ########################################################################
    def fallen_unconscious(self, dmg, dmg_type, critical):
        if self.has_effect("Relentless Endurance"):
            super().fallen_unconscious(dmg, dmg_type, critical)
        else:
            self.add_effect(RelentlessEndurance())

    ########################################################################
    def spell_available(self, spell):
        """Do we have enough slots to cast a spell"""
        if self.spell_slots[spell.level] > 0:
            return True
        return False

    ########################################################################
    def cast(self, spell):
        """Cast a spell"""
        if not self.spell_available(spell):
            return False
        self.spell_slots[spell.level] -= 1
        return True

    ########################################################################
    def report(self):
        """Character report"""
        super().report()
        print(f"|  Lay On Hands: {self.lay_on_hands}")
        print(f"|  Spells: {self.spell_slots}")

    ########################################################################
    def shortrepr(self):
        """What we look like in the arena"""
        if self.is_alive():
            return colors.blue("P", bg="green")
        return colors.blue("P", bg="red")


##############################################################################
##############################################################################
##############################################################################
class LayOnHands(Action):
    """You have a pool of healing power that can restore 5 HP per long
    rest. As an action, you can touch a creature to restore any number
    of HP remaining in the pool, or 5 HP to either cure a disease or
    neutralize a poison affecting the creature."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Lay on Hands", **kwargs)

    ########################################################################
    def perform_action(self, source):
        """Do the action"""
        if source.lay_on_hands >= 5 and source.target.has_condition(Condition.POISONED):
            print(f"{source} lays on hands to {source.target} and cures them of poison")
            source.lay_on_hands -= 5
            source.target.remove_condition(Condition.POISONED)
        print(f"{source} lays on hands to {source.target} to heal them")
        chp = min(source.lay_on_hands, source.target.max_hp - source.target.hp)
        source.target.heal("", chp)
        source.lay_on_hands -= source.target.heal(0, chp)

    ########################################################################
    def heuristic(self, doer):
        """Should we do this action"""
        if doer.lay_on_hands == 0:
            return 0
        friends = doer.pick_closest_friends()
        if not friends:
            return 0
        friend = friends[0]
        if friend.has_condition(Condition.POISONED):
            return 10
        return friend.max_hp - friend.hp

    ########################################################################
    def pick_target(self, doer):
        """Who are we doing the action to"""
        friends = doer.pick_closest_friends()
        if friends:
            return friends[0]
        return None


##############################################################################
##############################################################################
##############################################################################
class RelentlessEndurance(Effect):
    """Relentless Endurance - When you are reduced to 0 HP but not
    killed, you can drop to 1 HP instead once per long rest."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Relentless Endurance", **kwargs)

    ########################################################################
    def initial(self, target):
        print(f"{target}'s Relentless Endurance kicks in")
        target.hp = 1


# EOF
