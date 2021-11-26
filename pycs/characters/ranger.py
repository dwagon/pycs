""" https://www.dndbeyond.com/classes/ranger """
import unittest
from collections import namedtuple
from unittest.mock import patch
import colors
import dice
from pycs.arena import Arena
from pycs.attack import RangedAttack
from pycs.character import Character
from pycs.constant import ActionType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.gear import Shortbow
from pycs.gear import Shortsword
from pycs.monsters import Skeleton
from pycs.spells import CureWounds
from pycs.spells import HuntersMark
from pycs.spells import LesserRestoration


##############################################################################
##############################################################################
##############################################################################
class Ranger(Character):
    """Ranger class"""

    def __init__(self, **kwargs):
        self.spell_slots = {}
        kwargs.update(
            {
                "str": 12,
                "dex": 17,
                "con": 13,
                "int": 8,
                "wis": 14,
                "cha": 11,
                "stat_prof": [Stat.STR, Stat.DEX],
                "speed": 25,
                "actions": [],
                "effects": [],
                "spellcast_bonus_stat": Stat.WIS,
                "action_preference": {
                    ActionType.RANGED: 5,
                    SpellType.HEALING: 3,
                    ActionType.MELEE: 2,
                },
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            kwargs["hp"] = 11
        if level >= 2:
            kwargs["hp"] = 18
            self.spell_slots = {1: 2}
            kwargs["effects"].append(ArcheryFightingStyle())
            kwargs["actions"].append(CureWounds())
            kwargs["actions"].append(HuntersMark())
        if level >= 3:
            kwargs["hp"] = 25
            # Ranger Archetype: Hunter
            kwargs["effects"].append(ColossusSlayer())
            # self.add_action(Absorb_Elements())
            self.spell_slots = {1: 3}
        if level >= 4:
            kwargs["hp"] = 36
            kwargs["dex"] = 18
            kwargs["con"] = 14
        if level >= 5:
            self.spell_slots = {1: 4, 2: 2}
            kwargs["hp"] = 44
            kwargs["attacks_per_action"] = 2
            kwargs["actions"].append(LesserRestoration())

        super().__init__(**kwargs)

    ##########################################################################
    def pick_target(self, action):
        """Override default targetting - pick the fewest hp"""
        s_range = action.range()[0]
        result = namedtuple("result", "hp id creature")
        combs = [
            result(_.hp, id(_), _)
            for _ in self.arena.pick_alive()
            if _.side != self.side and self.distance(_) < s_range
        ]
        if not combs:
            return None
        combs.sort()
        target = combs[0].creature
        print(f"Picking on {target} as has fewest hp")
        return target

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
    def shortrepr(self):  # pragma: no cover
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
    def heuristic(self):
        """Should we perform this attack - no if adjacent, yes if in range,
        middling if at long range"""
        enemies = self.owner.pick_closest_enemy()
        if not enemies:
            return 0
        if not self.available:
            return 0
        hmark = [_ for _ in enemies if _.has_effect("Hunters Mark")]
        dist = self.owner.distance(enemies[0])
        if dist <= 1:
            return 0
        return self.max_dmg() + len(hmark)

    ########################################################################
    def pick_target(self):
        """Who are we doing this to - the target with hunters mark or the
        closest"""
        enemies = self.owner.pick_closest_enemy()
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
            eff += 2
        return eff


##############################################################################
##############################################################################
##############################################################################
class TestArcheryStyle(unittest.TestCase):
    """Test ArcheryStyle"""

    ########################################################################
    def setUp(self):
        self.arena = Arena()
        self.ranger = Ranger(
            name="Ryan", side="a", level=2, gear=[Shortbow(), Shortsword()]
        )
        self.arena.add_combatant(self.ranger, coords=(1, 1))
        self.skel = Skeleton(side="b")
        self.arena.add_combatant(self.skel, coords=(3, 3))

    ########################################################################
    def test_archery_ranged(self):
        """Test Effect with ranged"""
        self.assertTrue(self.ranger.has_effect("Archery Fighting Style"))
        act = self.ranger.pick_action_by_name("Shortbow")
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 10
            to_hit, _, _ = act.roll_to_hit(self.skel)
        # 10 to hit, 2 prof, 3 stat, 2 archery style
        self.assertEqual(to_hit, 10 + 2 + 3 + 2)

    ########################################################################
    def test_archery_melee(self):
        """Test Effect with melee - should not apply"""
        self.assertTrue(self.ranger.has_effect("Archery Fighting Style"))
        act = self.ranger.pick_action_by_name("Shortsword")
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 10
            to_hit, _, _ = act.roll_to_hit(self.skel)
        # 10 to hit, 2 prof, 3 stat
        self.assertEqual(to_hit, 10 + 2 + 3)


##############################################################################
##############################################################################
##############################################################################
class TestColussusSlayer(unittest.TestCase):
    """Test ColussusSlayer"""

    ########################################################################
    def setUp(self):
        self.arena = Arena()
        self.ranger = Ranger(name="Ryan", side="a", level=4, gear=[Shortbow()])
        self.arena.add_combatant(self.ranger, coords=(1, 1))
        self.skel = Skeleton(side="b", hp=10)
        self.arena.add_combatant(self.skel, coords=(3, 3))

    ########################################################################
    def test_colossus(self):
        """Test Effect with ranged"""
        self.assertTrue(self.ranger.has_effect("Colossus Slayer"))
        act = self.ranger.pick_action_by_name("Shortbow")
        with patch.object(dice, "roll") as mock:
            mock.return_value = 2
            act.buff_attack_damage(self.skel)
        self.assertEqual(self.skel.hp, self.skel.max_hp - 2)
        # Shouldn't happen twice in a turn
        with patch.object(dice, "roll") as mock:
            mock.return_value = 2
            act.buff_attack_damage(self.skel)
        self.assertEqual(self.skel.hp, self.skel.max_hp - 2)


# EOF
