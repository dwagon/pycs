"""https://www.dndbeyond.com/races/half-orc"""
from pycs.race import Race
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class HalfOrc(Race):
    """Grunt"""

    def __init__(self, **kwargs):
        kwargs["effects"] = [RelentlessEndurance()]
        super().__init__("Half Orc", **kwargs)

    # TO DO - Savage Attack


##############################################################################
##############################################################################
##############################################################################
class RelentlessEndurance(Effect):
    """Relentless Endurance - When you are reduced to 0 HP but not
    killed, you can drop to 1 HP instead once per long rest."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Relentless Endurance", **kwargs)
        self._relentless_used = False

    ########################################################################
    def hook_fallen_unconscious(self, dmg, dmg_type, critical):
        """Engage Relentless Attack"""
        if self._relentless_used:
            return True
        print(f"{self.owner}'s Relentless Endurance kicks in")
        self.owner.hp = 1
        self._relentless_used = True
        return False


# EOF
