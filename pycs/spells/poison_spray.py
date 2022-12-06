"""https://www.dndbeyond.com/spells/poison-spray"""

from typing import Any
from unittest.mock import patch

from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.spell import AttackSpell
from pycs.spells.spelltest import SpellTest


##############################################################################
class PoisonSpray(AttackSpell):
    """You extend your hand toward a creature you can see within
    range and project a puff of noxious gas from your palm. The
    creature must succeed on a Constitution saving throw or take
    1d12 poison damage.

    This spell's damage increases by 1d12 when you reach 5th level
    (2d12), 11th level (3d12), and 17th level (4d12)."""

    ##########################################################################
    def __init__(self, **kwargs: Any):
        name = "Poison Spray"
        kwargs.update(
            {
                "reach": 10,
                "level": 0,
                "dmg": ("1d12", 0),
                "dmg_type": DamageType.POISON,
                "style": SpellType.SAVE_NONE,
                "type": SpellType.RANGED,
                "save_stat": Stat.CON,
            }
        )
        super().__init__(name, **kwargs)


##############################################################################
##############################################################################
##############################################################################
class TestPoisonSpray(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self) -> None:
        super().setUp()
        self.caster.add_action(PoisonSpray())

    ##########################################################################
    def test_cast_saves(self) -> None:
        """test casting where victim makes save"""
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        self.assertEqual(self.enemy.damage_this_turn, [])

    ##########################################################################
    def test_cast_fails(self) -> None:
        """test casting where victim fails saving throw"""
        self.caster.moves = 90
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        self.caster.target = self.enemy
        self.assertEqual(self.enemy.damage_this_turn, [])
        self.caster.move_to_target(self.enemy, 1)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertLess(self.enemy.hp, self.enemy.max_hp)
        self.assertEqual(len(self.enemy.damage_this_turn), 1)
        for obj in self.enemy.damage_this_turn:
            self.assertEqual(obj.type, DamageType.POISON)


# EOF
