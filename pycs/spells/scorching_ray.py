"""https://www.dndbeyond.com/spells/scorching-ray"""

from typing import Any, Optional
from unittest.mock import patch
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.damageroll import DamageRoll
from pycs.constant import SpellType
from pycs.creature import Creature
from pycs.spell import AttackSpell
from .spelltest import SpellTest


##############################################################################
class ScorchingRay(AttackSpell):
    """You create three rays of fire and hurl them at targets within
    range. You can hurl them at one target or several.

    Make a ranged spell attack for each ray. On a hit, the target takes
    2d6 fire damage.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, you create one additional ray for each slot
    level above 2nd."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Scorching Ray"
        kwargs.update(
            {
                "category": ActionCategory.ACTION,
                "reach": 120,
                "level": 2,
                "dmgroll": DamageRoll("2d6", 0, DamageType.FIRE),
                "style": SpellType.TOHIT,
                "type": SpellType.RANGED,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def cast(self) -> bool:
        """Do the spell - reevaluate targets each ray in case the ray
        has already killed the target"""
        for _ in range(3):
            targets = []
            for enemy in self.owner.pick_closest_enemy():
                if self.owner.distance(enemy) < self.range()[0]:
                    targets.append(enemy)
            if not targets:
                return False
            target = targets[0]
            print(f"Targeting {target} with Scorching Ray")
            to_hit, crit_hit, crit_miss = self.roll_to_hit(target)
            if to_hit >= target.ac and not crit_miss:
                dmg = self.roll_dmg(self.owner, target)
                target.hit(dmg, self.owner, crit_hit, self.name)
            else:
                print(f"Scorching Ray missed {target} (Rolled {to_hit} < AC: {target.ac})")
        return True

    ##########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we do the spell to"""
        for enemy in self.owner.pick_closest_enemy():
            if self.owner.distance(enemy) < self.range()[0]:
                return enemy
        return None

    ##########################################################################
    def heuristic(self) -> int:
        """Should we do the spell"""
        targets = 0
        for enemy in self.owner.pick_closest_enemy():
            if self.owner.distance(enemy) < self.range()[0]:
                targets += 1
        return min(3, targets) * 12


##############################################################################
##############################################################################
##############################################################################
class TestScorchingRay(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self) -> None:
        """setup tests"""
        super().setUp()
        self.caster.add_action(ScorchingRay())

    ##########################################################################
    def test_cast_miss(self) -> None:
        """test casting where misses victim"""
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 2
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        self.assertEqual(self.enemy.damage_this_turn, [])

    ##########################################################################
    def test_cast_hit(self) -> None:
        """test casting where victim fails saving throw"""
        self.enemy.max_hp = 100  # Need enough hp to survive 3 rays
        self.enemy.hp = 100
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        self.assertEqual(self.enemy.damage_this_turn, [])
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertLess(self.enemy.hp, self.enemy.max_hp)
        print(f"{self.enemy.damage_this_turn=}")
        self.assertEqual(len(self.enemy.damage_this_turn), 3)
        for obj in self.enemy.damage_this_turn:
            self.assertEqual(obj.type, DamageType.FIRE)


# EOF
