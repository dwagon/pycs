"""https://www.dndbeyond.com/spells/fireball"""

from collections import defaultdict
from unittest.mock import patch
import dice
from pycs.spell import AttackSpell
from pycs.creature import Creature
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.constant import Stat
from .spelltest import SpellTest


##############################################################################
class Fireball(AttackSpell):
    """A bright streak flashes from your pointing finger to a point you
    choose within range and then blossoms with a low roar into an
    explosion of flame. Each creature in a 20-foot-radius sphere centered
    on that point must make a Dexterity saving throw. A target takes
    8d6 fire damage on a failed save, or half as much damage on a
    successful one.

    The fire spreads around corners. It ignites flammable objects in
    the area that aren't being worn or carried.

    At Higher Levels. When you cast this spell using a spell slot of
    4th level or higher, the damage increases by 1d6 for each slot level
    above 3rd."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Fireball"
        kwargs.update(
            {
                "reach": 150,
                "level": 3,
                "style": SpellType.SAVE_HALF,
                "type": SpellType.RANGED,
                "save_stat": Stat.DEX,
                "dmg": ("8d6", 0),
                "dmg_type": DamageType.FIRE,
            }
        )
        super().__init__(name, **kwargs)
        self._num_enemy = 0
        self._num_friend = 0

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        for per in caster.arena.combatants:
            if per.distance(self.target) < 20 / 5:
                print(f"Attacking {per} with fireball")
                dmg = self.roll_dmg(caster, per)
                per.hit(dmg, self.dmg_type, caster, False, self.name)

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        targets = []
        for enemy in doer.pick_closest_enemy():
            if doer.distance(enemy) > self.range()[0]:
                continue
            sides = defaultdict(int)

            for per in doer.arena.combatants:
                if per.distance(enemy) < 20 / 5:
                    sides[per.side] += 1
            targets.append(
                (sides[enemy.side], 999 - sides[doer.side], id(enemy), enemy)
            )
        # We want the most enemy and the least friends in the blast
        if targets:
            self._num_enemy = targets[0][0]
            self._num_friend = -targets[0][1] + 999
            self.target = targets[0][-1]
            targets.sort()
            return targets[0][-1]
        return None

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if self.pick_target(doer):
            val = (
                int(dice.roll_max("8d6")) * self._num_enemy
                - int(1.5 * int(dice.roll_max("8d6"))) * self._num_friend
            )
            return val
        return 0


##############################################################################
##############################################################################
##############################################################################
class TestFireball(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        super().setUp()
        self.caster.add_action(Fireball())

    ##########################################################################
    def test_cast_saved(self):
        """test casting where victim makes saving throw"""
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        with patch.object(dice, "roll") as mock_dice:
            mock_dice.return_value = 20
            with patch.object(Creature, "rolld20") as mock:
                mock.return_value = 19
                self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        # Damage should be half of (20 + 4(prof_bonus))
        self.assertEqual(self.enemy.hp, self.enemy.max_hp - 12)

    ##########################################################################
    def test_cast_hit(self):
        """test casting where victim fails saving throw"""
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        with patch.object(dice, "roll") as mock_dice:
            mock_dice.return_value = 20
            with patch.object(Creature, "rolld20") as mock:
                mock.return_value = 1
                self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertEqual(self.enemy.hp, self.enemy.max_hp - 24)


# EOF
