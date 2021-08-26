"""https://www.dndbeyond.com/spells/bless"""

import dice
from pycs.constants import SpellType
from pycs.effect import Effect
from pycs.spells import SpellAction


##############################################################################
##############################################################################
##############################################################################
class Bless(SpellAction):
    """You bless up to three creatures of your choice within range.
    Whenever a target makes an attack roll or a saving throw before the
    spell ends, the target can roll a d4 and add the number rolled to
    the attack roll or saving throw.

    At Higher Levels. When you cast this spell using a spell slot of
    2nd level or higher, you can target one additional creature for
    each slot level above 1st."""

    ##########################################################################
    def __init__(self, **kwargs):
        name = "Bless"
        kwargs.update(
            {
                "reach": 30,
                "level": 1,
                "type": SpellType.BUFF,
                "concentration": True,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        # The more applicable targets the more likely we should do it
        if not doer.spell_available(self):
            return 0
        close = 0
        for targ in doer.arena.my_side(doer.side):
            if doer.distance(targ) <= self.range()[0]:
                if doer.has_effect("Bless"):
                    continue
                close += 1
        return close

    ###########################################################################
    def pick_target(self, doer):
        """Who should we do the spell to"""
        # Improve this
        return doer

    ###########################################################################
    def cast(self, caster):
        """Do the spell"""
        targets = 3
        for friend in caster.arena.my_side(caster.side):
            if friend.has_effect("Bless"):
                continue
            targets -= 1
            print(f"{friend} is now Blessed")
            friend.add_effect(BlessEffect(cause=caster))
            if targets <= 0:
                break
        return True

    ###########################################################################
    def bless_result(self):
        """What does the bless do"""
        return int(dice.roll("d4"))


##############################################################################
##############################################################################
##############################################################################
class BlessEffect(Effect):
    """The Effect of the bless spell"""

    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Bless", **kwargs)

    def hook_attack_to_hit(self, target, rnge):
        """Mod attack roll"""
        eff = super().hook_attack_to_hit(target, rnge)
        eff.update({"bonus": int(dice.roll("d4"))})
        return eff

    def hook_saving_throw(self, stat):
        """Mod saving throw"""
        eff = super().hook_saving_throw(stat)
        eff.update({"bonus": int(dice.roll("d4"))})
        print(f"Bless adds {eff['bonus']} to saving throw")
        return eff


# EOF
