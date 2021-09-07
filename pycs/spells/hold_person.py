"""https://www.dndbeyond.com/spells/hold-person"""

from unittest.mock import patch
from pycs.constant import ActionCategory
from pycs.creature import Creature
from pycs.constant import Condition
from pycs.constant import MonsterType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.spell import SpellAction
from .spelltest import SpellTest


##############################################################################
##############################################################################
##############################################################################
class HoldPerson(SpellAction):
    """Choose a humanoid that you can see within range. The target must
    succeed on a Wisdom saving throw or be paralyzed for the duration.
    At the end of each of its turns, the target can make another Wisdom
    saving throw. On a success, the spell ends on the target."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Hold Person"
        kwargs.update(
            {
                "reach": 60,
                "level": 2,
                "type": SpellType.RANGED,
                "concentration": SpellType.CONCENTRATION,
            }
        )
        super().__init__(name, **kwargs)
        self._victim = None

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        target = self.pick_target(doer)
        if target:
            return 10
        return 0

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        for enemy in doer.pick_closest_enemy():
            if not enemy.is_type(MonsterType.HUMANOID):
                continue
            if doer.distance(enemy) > self.range()[0]:
                continue
            return enemy
        return None

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        svth = caster.target.saving_throw(
            Stat.WIS, caster.spellcast_save, effect=Condition.PARALYZED
        )
        if not svth:
            caster.target.add_effect(HoldPersonEffect(caster=caster))
            self._victim = caster.target
        return True

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""
        # They could have saved in the meantime
        if self._victim.has_effect("Hold Person"):
            print(f"Removing Hold Person from {self._victim}")
            self._victim.remove_effect("Hold Person")
        self._victim = None


##############################################################################
##############################################################################
##############################################################################
class HoldPersonEffect(Effect):
    """Hold Person Effect"""

    ###########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Hold Person", **kwargs)

    ###########################################################################
    def initial(self, target):
        """Initial effects of Hold Person"""
        target.add_condition(Condition.PARALYZED)

    ###########################################################################
    def finish(self, victim):
        """When the effect is over"""
        victim.remove_condition(Condition.PARALYZED)

    ###########################################################################
    def removal_end_of_its_turn(self, victim):
        """Do we save"""
        svth = victim.saving_throw(
            Stat.WIS, self.caster.spellcast_save, effect=Condition.PARALYZED
        )
        if svth:
            victim.remove_condition(Condition.PARALYZED)
            return True
        return False


##############################################################################
##############################################################################
##############################################################################
class TestHoldPerson(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        super().setUp()
        self.caster.add_action(HoldPerson())

    ##########################################################################
    def test_cast_save(self):
        """test casting with creature making save"""
        self.assertFalse(self.enemy.has_condition(Condition.PARALYZED))
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertFalse(self.enemy.has_effect("Hold Person"))

    ##########################################################################
    def test_cast_fails(self):
        """test casting with creature failing save"""
        self.assertFalse(self.enemy.has_condition(Condition.PARALYZED))
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertTrue(self.enemy.has_effect("Hold Person"))

    ##########################################################################
    def test_end_turn(self):
        """Test the effect gets removed at the end of a turn"""
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertTrue(self.enemy.has_condition(Condition.PARALYZED))
        self.assertTrue(self.enemy.has_effect("Hold Person"))
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.enemy.end_turn(draw=False)
        self.assertFalse(self.enemy.has_effect("Hold Person"))
        self.assertFalse(self.enemy.has_condition(Condition.PARALYZED))

    ##########################################################################
    def test_removal(self):
        """Test the effect gets removed on concentration failure"""
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=False)
        self.assertTrue(self.enemy.has_condition(Condition.PARALYZED))
        self.assertTrue(self.enemy.has_effect("Hold Person"))
        self.caster.remove_concentration()
        self.assertFalse(self.enemy.has_effect("Hold Person"))
        self.assertFalse(self.enemy.has_condition(Condition.PARALYZED))


# EOF
