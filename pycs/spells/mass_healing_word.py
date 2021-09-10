"""https://www.dndbeyond.com/spells/mass-healing-word"""

from pycs.constant import ActionCategory
from pycs.constant import SpellType
from pycs.spell import SpellAction
from .spelltest import SpellTest


##############################################################################
##############################################################################
##############################################################################
class MassHealingWord(SpellAction):
    """As you call out words of restoration, up to six creatures of
    your choice that you can see within range regain hit points equal
    to 1d4 + your spellcasting ability modifier. This spell has no
    effect on undead or constructs."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Mass Healing Word"
        kwargs.update({"reach": 60, "level": 3, "type": SpellType.HEALING})
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        suitable = 0
        for creat in self.owner.pick_closest_friends():
            if creat.hp < creat.max_hp:
                suitable += creat.max_hp - creat.hp
        return suitable

    ##########################################################################
    def pick_target(self):
        """Who should we do the spell to"""
        return self.owner

    ##########################################################################
    def cast(self):
        """Do the spell"""
        cured = 0
        for creat in self.owner.pick_closest_friends():
            if creat.hp < creat.max_hp:
                cured += 1
                creat.heal("1d4", self.modifier(self.owner))
            if cured >= 6:
                break
        if cured <= 6 and self.owner.hp < self.owner.max_hp:
            self.owner.heal("1d4", self.modifier(self.owner))
        return True


##############################################################################
##############################################################################
##############################################################################
class Test_MassHealingWord(SpellTest):
    """Test Spell"""

    ##########################################################################
    def setUp(self):
        super().setUp()
        self.caster.add_action(MassHealingWord())

    ##########################################################################
    def test_cast(self):
        """See what this spell does"""
        self.friend.hp = 5
        self.caster.hp = 5
        self.caster.do_stuff(categ=ActionCategory.ACTION, moveto=True)
        self.assertGreater(self.friend.hp, 5)
        self.assertGreater(self.caster.hp, 5)


# EOF
