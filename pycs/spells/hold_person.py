"""https://www.dndbeyond.com/spells/hold-person"""

from typing import Any, Optional
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
    def __init__(self, **kwargs: Any):
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
    def heuristic(self) -> int:
        """Should we do the spell"""
        target = self.pick_target()
        if target:
            return 10
        return 0

    ##########################################################################
    def pick_target(self) -> Optional[Creature]:
        """Who should we do the spell to"""
        for enemy in self.owner.pick_closest_enemy():
            if not enemy.is_type(MonsterType.HUMANOID):
                continue
            if self.owner.distance(enemy) > self.range()[0]:
                continue
            return enemy
        return None

    ##########################################################################
    def cast(self) -> bool:
        """Do the spell"""
        svth = self.owner.target.saving_throw(Stat.WIS, self.owner.spellcast_save, effect=Condition.PARALYZED)
        # TO DO: If the saving throw is made the spell should end
        if not svth:
            self.owner.target.add_effect(HoldPersonEffect(caster=self.owner))
            self._victim = self.owner.target
        return True

    ##########################################################################
    def end_concentration(self) -> None:
        """What happens when we stop concentrating"""
        # They could have saved in the meantime
        if self._victim and self._victim.has_effect("Hold Person"):
            print(f"Removing Hold Person from {self._victim}")
            self._victim.remove_effect("Hold Person")
        self._victim = None


##############################################################################
##############################################################################
##############################################################################
class HoldPersonEffect(Effect):
    """Hold Person Effect"""

    ###########################################################################
    def __init__(self, **kwargs: Any):
        """Initialise"""
        super().__init__("Hold Person", **kwargs)

    ###########################################################################
    def initial(self, target: Creature) -> None:
        """Initial effects of Hold Person"""
        target.add_condition(Condition.PARALYZED)

    ###########################################################################
    def finish(self, victim: Creature) -> None:
        """When the effect is over"""
        victim.remove_condition(Condition.PARALYZED)

    ###########################################################################
    def removal_end_of_its_turn(self, victim: Creature) -> bool:
        """Do we save"""
        assert self.caster is not None
        svth = victim.saving_throw(Stat.WIS, self.caster.spellcast_save, effect=Condition.PARALYZED)
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
    def setUp(self) -> None:
        """Setup tests"""
        super().setUp()
        self.caster.add_action(HoldPerson())

    ##########################################################################
    def test_cast_save(self) -> None:
        """test casting with creature making save"""
        self.assertFalse(self.enemy.has_condition(Condition.PARALYZED))
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 20
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertFalse(self.enemy.has_effect("Hold Person"))

    ##########################################################################
    def test_cast_fails(self) -> None:
        """test casting with creature failing save"""
        self.assertFalse(self.enemy.has_condition(Condition.PARALYZED))
        with patch.object(Creature, "rolld20") as mock:
            mock.return_value = 1
            self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertTrue(self.enemy.has_effect("Hold Person"))

    ##########################################################################
    def test_end_turn(self) -> None:
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
    def test_removal(self) -> None:
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
