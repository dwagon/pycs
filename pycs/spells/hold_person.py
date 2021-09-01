"""https://www.dndbeyond.com/spells/hold-person"""

from pycs.constant import Condition
from pycs.constant import MonsterType
from pycs.constant import SpellType
from pycs.constant import Stat
from pycs.effect import Effect
from pycs.spell import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Hold_Person(SpellAction):
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

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        if not doer.spell_available(self):
            return 0
        for enemy in doer.pick_closest_enemy():
            if not enemy.is_type(MonsterType.HUMANOID):
                continue
            if doer.distance(enemy) > self.range()[0]:
                continue
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
        if svth:
            caster.target.add_effect(HoldPersonEffect(caster=caster))
        self.target = caster.target
        return True

    ##########################################################################
    def end_concentration(self):
        """What happens when we stop concentrating"""
        print(f"Removing Hold Person form {self.target}")
        self.target.remove_effect("Hold Person")


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
    def removal_end_of_its_turn(self, victim):
        """Do we save"""
        svth = victim.saving_throw(
            Stat.WIS, self.caster.spellcast_save, effect=Condition.PARALYZED
        )
        if svth:
            victim.remove_condition(Condition.PARALYZED)
            return True
        return False


# EOF
