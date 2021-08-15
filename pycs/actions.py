""" Handle non-attack Actions """
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


# EOF
