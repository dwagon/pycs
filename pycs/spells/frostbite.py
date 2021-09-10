"""https://www.dndbeyond.com/spells/frostbite"""

from unittest.mock import patch
from pycs.constant import ActionCategory
from pycs.constant import DamageType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.creature import Creature
from pycs.effect import Effect
from pycs.spell import AttackSpell
from .spelltest import SpellTest


##############################################################################
##############################################################################
##############################################################################
class Frostbite(AttackSpell):
    """You cause numbing frost to form on one creature that you can see
    within range. The target must make a Constitution saving throw. On
    a failed save, the target takes 1d6 cold damage, and it has
    disadvantage on the next weapon attack roll it makes before the end
    of its next turn.

    The spell’s damage increases by 1d6 when you reach 5th level (2d6),
    11th level (3d6), and 17th level (4d6)."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Frostbite"
        self._target = None
        kwargs.update(
            {
                "reach": 60,
                "level": 0,
                "style": SpellType.SAVE_NONE,
                "type": SpellType.RANGED,
                "save_stat": Stat.CON,
                "dmg": ("1d6", 0),
                "dmg_type": DamageType.COLD,
            }
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self):
        """Slightly better than the damage itself would indicate"""
        return super().heuristic() + 2

    ##########################################################################
    def pick_target(self):
        """Who should we target"""
        self._target = super().pick_target()
        return self._target

    ##########################################################################
    def failed_save(self, source, target, dmg):
        """What to when we target fails save"""
        self._target.add_effect(FrostbiteEffect(cause=source))


##############################################################################
##############################################################################
##############################################################################
class FrostbiteEffect(Effect):
    """Effect of the Frostbite"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Frostbite", **kwargs)

    ##########################################################################
    def initial(self, target):
        """Initial effects of Frostbite"""

    ##########################################################################
    def hook_gives_disadvantage(self, target):
        return True

    ##########################################################################
    def removal_end_of_its_turn(self, victim):
        return True


##############################################################################
##############################################################################
##############################################################################
class TestFrostbite(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        """Test Setup"""
        super().setUp()
        self.caster.add_action(Frostbite())

    ##########################################################################
    def test_cast_miss(self):
        """test casting where victim makes saving throw"""
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 19
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        self.assertFalse(self.enemy.has_effect("Frostbite"))

    ##########################################################################
    def test_cast_hit(self):
        """test casting where victim fails saving throw"""
        self.assertEqual(self.enemy.hp, self.enemy.max_hp)
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertLess(self.enemy.hp, self.enemy.max_hp)
        self.assertTrue(self.enemy.has_effect("Frostbite"))

    ##########################################################################
    def test_effect(self):
        """Test the effect of casting the spell"""
        act = self.enemy.pick_attack_by_name("Longsword")
        self.assertFalse(act.has_disadvantage(self.friend, 1))
        self.enemy.add_effect(FrostbiteEffect())
        self.assertTrue(act.has_disadvantage(self.friend, 1))

    ##########################################################################
    def test_removal(self):
        """Test the effect gets removed"""
        self.enemy.add_effect(FrostbiteEffect())
        self.assertTrue(self.enemy.has_effect("Frostbite"))
        self.enemy.end_turn(draw=False)
        self.assertFalse(self.enemy.has_effect("Frostbite"))


# EOF
