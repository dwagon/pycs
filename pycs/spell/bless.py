"""https://www.dndbeyond.com/spells/bless"""

import dice
from spells import SpellAction
from constants import SpellType


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
                "side_effect": self.bless,
                "type": SpellType.BUFF,
                "concentration": True,
            }
        )
        super().__init__(name, **kwargs)

    ###########################################################################
    def heuristic(self, doer):
        """Should we do the spell"""
        return 0

    ###########################################################################
    def bless(self, caster):
        """Do the spell"""
        friends = caster.pick_closest_friend(3)
        for friend in friends:
            friend.add_hook("attack_to_hit", self.bless_result)
            friend.add_hook("saving_throw", self.bless_result)

    ###########################################################################
    def bless_result(self):
        """What does the bless do"""
        return int(dice.roll("d4"))


# EOF
