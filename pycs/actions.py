""" Handle non-attack Actions """
import dice
from constants import ActionType


##############################################################################
##############################################################################
##############################################################################
class Action:
    """generic action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        self.name = name
        self.available = True
        self.type = ActionType.UNKNOWN
        self.side_effect = kwargs.get("side_effect", self.no_side_effect)

    ########################################################################
    def no_side_effect(self, source):
        """No side_effect"""

    ########################################################################
    def pick_target(self, doer):
        """Who are we going to do the action to"""
        print(f"{self.__class__.__name__}.pick_target({doer=}) - needs to be replaced")

    ########################################################################
    def heuristic(self, doer):  # pylint: disable=unused-argument
        """How good is this action for doer this turn
        0 - don't do
        1 - whatevs
        ..
        5 - zOMG!
        """
        return 1

    ########################################################################
    def range(self):
        """Return the range (good, max) of the action"""
        return 0, 0

    ##########################################################################
    def is_available(self, owner):  # pylint: disable=unused-argument
        """Is this action currently available to the creature"""
        return True

    ########################################################################
    def perform_action(self, source):  # pylint: disable=unused-argument
        """Perform the action"""

    ########################################################################
    def __repr__(self):
        return self.name


##############################################################################
##############################################################################
##############################################################################
class SpellAction(Action):
    """Spell action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.type = kwargs.get("type")
        self.cure_hp = kwargs.get("cure_hp")
        self.level = kwargs.get("level")

    ########################################################################
    def max_cure(self, source, target):
        """What is the most effective cure"""
        mhp = (
            int(dice.roll_max(self.cure_hp[0]))
            + self.cure_hp[1]
            + source.spell_modifier
        )
        thp = target.max_hp - target.hp
        return min(mhp, thp)

    ########################################################################
    def cure(self, source, target):
        """Cure the target"""
        chp = int(dice.roll(self.cure_hp[0])) + self.cure_hp[1] + source.spell_modifier
        target.hp += chp
        target.hp = min(target.max_hp, target.hp)
        print(f"{source} cured {target} of {chp} hp")

    ########################################################################
    def is_type(self, *types):
        """Is this spell of the specified types"""
        return self.type in types

    ########################################################################
    def perform_action(self, source):  # pylint: disable=unused-argument
        self.side_effect(source)


# EOF
