"""https://www.dndbeyond.com/spells/mass-healing-word"""

from pycs.constants import SpellType
from pycs.spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Mass_Healing_Word(SpellAction):
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
    def heuristic(self, doer):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        if not doer.spell_available(self):
            return 0
        suitable = 0
        for creat in doer.pick_closest_friends():
            if creat.hp < creat.max_hp:
                suitable += 1
        return int(suitable / 2)

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        return doer

    ##########################################################################
    def cast(self, caster):
        """Do the spell"""
        cured = 6
        for creat in caster.pick_closest_friends():
            if creat.hp < creat.max_hp:
                cured -= 1
                creat.heal("1d4", self.modifier(caster))
            if cured <= 0:
                break
        return True


# EOF
