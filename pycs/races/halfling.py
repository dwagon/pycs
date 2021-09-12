"""https://www.dndbeyond.com/races/halfling"""
import dice
from pycs.constant import Condition
from pycs.race import Race
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class Halfling(Race):
    """Breakfast?"""

    def __init__(self, **kwargs):
        kwargs["effects"] = [Brave(), Lucky()]
        super().__init__("Halfling", **kwargs)


##############################################################################
##############################################################################
##############################################################################
class Lucky(Effect):
    """When you roll a 1 on the d20 for an attack roll, ability check,
    or saving throw, you can reroll the die and must use the new roll."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Lucky", **kwargs)

    ########################################################################
    def hook_d20(self, val, reason):
        """Reroll ones"""
        if reason in ("attack", "ability", "save"):
            if val == 1:
                val = int(dice.roll("d20"))
                print(f"Lucky - reroll 1 to {val}")
        return val


##############################################################################
##############################################################################
##############################################################################
class Brave(Effect):
    """You have advantage on saving throws against being frightened."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Brave", **kwargs)

    ########################################################################
    def hook_saving_throw(self, stat, **kwargs):
        """Advantage Frightened"""
        eff = super().hook_saving_throw(stat, **kwargs)
        if kwargs.get("effect") == Condition.FRIGHTENED:
            eff["advantage"] = True
        return eff


# EOF
