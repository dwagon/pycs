""" https://www.dndbeyond.com/classes/ranger """
import colors
import dice
from pycs.attack import RangedAttack
from pycs.character import Character
from pycs.constant import ActionType
from pycs.constant import Condition
from pycs.constant import Race
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.gear import Leather
from pycs.gear import Longbow
from pycs.gear import Shortsword

# from pycs.spells import Absorb_Elements
from pycs.spells import Cure_Wounds
from pycs.spells import Hunters_Mark
from pycs.spells import Lesser_Restoration


##############################################################################
##############################################################################
##############################################################################
class Ranger(Character):
    """Ranger class"""

    def __init__(self, level=1, **kwargs):
        self.level = level
        self.spell_slots = {}
        kwargs.update(
            {
                "race": Race.HALFLING,
                "str": 12,
                "dex": 17,
                "con": 13,
                "int": 8,
                "wis": 14,
                "cha": 11,
                "speed": 25,
                "spellcast_bonus_stat": Stat.WIS,
                "action_preference": {
                    ActionType.RANGED: 5,
                    SpellType.HEALING: 3,
                    ActionType.MELEE: 2,
                },
            }
        )
        if level >= 1:
            kwargs["hp"] = 11
        if level >= 2:
            kwargs["hp"] = 18
            self.spell_slots = {1: 2}
        if level >= 3:
            kwargs["hp"] = 25
            # Ranger Archetype: Hunter
            # Hunter's Prey: Colossus Slayer
            self.spell_slots = {1: 3}
        if level >= 4:
            kwargs["hp"] = 36
            kwargs["dex"] = 18
            kwargs["con"] = 14
        if level >= 5:
            self.spell_slots = {1: 4, 2: 2}
            kwargs["hp"] = 44
            kwargs["attacks_per_action"] = 2

        super().__init__(**kwargs)

        self.add_effect(Brave())
        self.add_effect(Lucky())
        if level >= 2:
            self.add_effect(ArcheryFightingStyle())
            self.add_action(Cure_Wounds())
            self.add_action(Hunters_Mark())
        if level >= 3:
            self.add_effect(ColossusSlayer())
            # self.add_action(Absorb_Elements())
        if level >= 5:
            self.add_action(Lesser_Restoration())

        self.add_gear(Shortsword())
        self.add_gear(Longbow())
        self.add_gear(Leather())

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
    def report(self):
        """Character report"""
        super().report()
        print(f"|  Spells: {self.spell_slots}")

    ##########################################################################
    def shortrepr(self):
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("R", bg="green")
        return colors.blue("R", bg="red")


##############################################################################
##############################################################################
##############################################################################
class RangersRangedAttack(RangedAttack):
    """Prioritise the creature with a hunters mark"""

    ########################################################################
    def heuristic(self, doer):
        """Should we perform this attack - no if adjacent, yes if in range,
        middling if at long range"""
        enemies = doer.pick_closest_enemy()
        if not enemies:
            return 0
        if not self.available:
            return 0
        hmark = [_ for _ in enemies if _.has_effect("Hunters Mark")]
        dist = doer.distance(enemies[0])
        if dist <= 1:
            return 0
        return self.max_dmg(doer) + len(hmark)

    ########################################################################
    def pick_target(self, doer):
        """Who are we doing this to - the target with hunters mark or the
        closest"""
        enemies = doer.pick_closest_enemy()
        if not enemies:
            return 0
        if not self.available:
            return 0
        hmark = [_ for _ in enemies if _.has_effect("Hunters Mark")]
        if hmark:
            return hmark[0]
        return enemies[0]


##############################################################################
##############################################################################
##############################################################################
class ColossusSlayer(Effect):
    """Your tenacity can wear down the most potent foes. When you hit
    a creature with a weapon attack, the creature takes an extra 1d8
    damage if it’s below its hit point maximum. You can deal this extra
    damage only once per turn."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        self.used = False
        super().__init__("Colossus Slayer", **kwargs)

    ########################################################################
    def hook_start_turn(self):
        """Reset"""
        self.used = False

    ########################################################################
    def hook_source_additional_damage(self, attack, source, target):
        """+1d8 damage"""
        if not self.used:
            self.used = True
            return ("1d8", 0, None)
        return ("", 0, None)


##############################################################################
##############################################################################
##############################################################################
class ArcheryFightingStyle(Effect):
    """You gain a +2 bonus to attack rolls you make with ranged weapons."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Archery Fighting Style", **kwargs)

    ########################################################################
    def hook_attack_to_hit(self, **kwargs):
        """+2 to hit"""
        eff = super().hook_attack_to_hit(**kwargs)
        if issubclass(kwargs["action"].__class__, RangedAttack):
            eff.update({"bonus": 2})
        return eff


##############################################################################
##############################################################################
##############################################################################
class Brave(Effect):
    """You have advantage on saving throws against being frightened."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Brave", **kwargs)

    ########################################################################
    def hook_saving_throw(self, stat, **kwargs):
        """Advantage Frightened"""
        eff = super().hook_saving_throw(stat, **kwargs)
        if kwargs.get("effect") == Condition.FRIGHTENED:
            eff["advantage"] = True
        return eff


##############################################################################
##############################################################################
##############################################################################
class Lucky(Effect):
    """When you roll a 1 on the d20 for an attack roll, ability check,
    or saving throw, you can reroll the die and must use the new roll."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Lucky", **kwargs)

    ########################################################################
    def hook_d20(self, val, reason):
        """Reroll ones"""
        if reason in ("attack", "ability", "save"):
            if val == 1:
                val = int(dice.roll("d20"))
                print(f"Lucky - reroll 1 to {val}")
        return val


# EOF
