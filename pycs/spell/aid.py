"""https://www.dndbeyond.com/spells/aid"""

from spells import SpellAction
from constants import SpellType


##############################################################################
class Aid(SpellAction):
    """Your spell bolsters your allies with toughness and resolve.
    Choose up to three creatures within range. Each target's hit
    point maximum and current hit points increase by 5 for the
    duration.

    At Higher Levels. When you cast this spell using a spell slot of
    3rd level or higher, a target's hit points increase by an additional
    5 for each slot level above 2nd."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Aid"
        kwargs.update(
            {"reach": 30, "level": 2, "side_effect": self.aid, "type": SpellType.BUFF}
        )
        super().__init__(name, **kwargs)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do the spell
        the more people it can effect the more we should do it"""
        if not doer.spell_available(self):
            return 0
        close = 0
        for targ in doer.pick_closest_friend(3):
            if doer.distance(targ) <= 30 / 6:
                if doer.has_temp_effect("Aid"):
                    continue
                close += 1
        return close

    ##########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        # Pick three people near where we are
        # TO DO - better this to move to where we can get 3 peeps
        return doer

    ##########################################################################
    def aid_person(self, person):
        """Add the aid benefits to {person}"""
        if person.has_temp_effect("Aid"):
            return 0
        else:
            print(f"Aid: {person} increasing HPs by 5")
            person.hp += 5
            person.max_hp += 5
            person.add_temp_effect("Aid", None)
            return 1

    ##########################################################################
    def aid(self, caster):
        """Do the spell"""
        targets = 3
        for targ in caster.arena.my_side(caster.side):
            if caster.distance(targ) <= 30 / 6:
                targets -= self.aid_person(targ)
        if targets < 3:
            self.aid_person(caster)


# EOF
