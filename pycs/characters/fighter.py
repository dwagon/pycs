""" Fighter """
import colors
from pycs.action import Action
from pycs.effect import Effect
from pycs.attack import MeleeAttack
from pycs.gear import Longsword
from pycs.gear import Plate
from pycs.constant import ActionType
from pycs.constant import ActionCategory
from pycs.character import Character


##############################################################################
##############################################################################
##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, level=1, **kwargs):
        self.level = level
        self.second_wind = 1
        self.action_surge = 1
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
            }
        )
        if level >= 1:
            kwargs["hp"] = 12
            # Fighting Style: Dueling
        if level >= 2:
            kwargs["hp"] = 20
        if level >= 3:
            kwargs["hp"] = 28
            # Martial Archetype: Champion
            # Critical on 19 or 20
            kwargs["critical"] = 19
        if level >= 4:
            kwargs["hp"] = 36
            kwargs["str"] = 18
        if level >= 5:
            kwargs["str"] = 18
            kwargs["hp"] = 44
            kwargs["attacks_per_action"] = 2

        super().__init__(**kwargs)

        if level >= 2:
            self.add_action(ActionSurge())

        self.add_gear(Longsword())
        self.add_gear(Plate())

        self.add_action(SecondWind())
        self.add_effect(DuelingFightingStyle())

    ##########################################################################
    def shortrepr(self):
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("F", bg="green")
        return colors.blue("F", bg="red")


##############################################################################
##############################################################################
##############################################################################
class SecondWind(Action):
    """You have a limited well of stamina that you can draw on to protect
    yourself from harm. On your turn, you can use a bonus action to
    regain hit points equal to 1d10 + your fighter level. Once you use
    this feature, you must finish a short or long rest before you can
    use it again."""

    ##########################################################################
    def __init__(self, **kwargs):
        """initialise"""
        super().__init__("Second Wind", **kwargs)
        self.type = ActionType.HEALING

    ##########################################################################
    def perform_action(self, source):
        """Do the action"""
        source.second_wind = 0
        source.heal("d10", source.level)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do this"""
        if not doer.second_wind:
            return 0
        return doer.max_hp - doer.hp

    ##########################################################################
    def pick_target(self, doer):
        """Only applies to self"""
        return doer


##############################################################################
##############################################################################
##############################################################################
class ActionSurge(Action):
    """Starting at 2nd level, you can push yourself beyond your normal
    limits for a moment. On your turn, you can take one additional
    action on top of your regular action and a possible bonus action."""

    ##########################################################################
    def __init__(self, **kwargs):
        """initialise"""
        kwargs["action_cost"] = 0
        super().__init__("Action Surge", **kwargs)
        self.type = ActionType.BUFF

    ##########################################################################
    def perform_action(self, source):
        """Do the action"""
        source.action_surge = 0
        source.options_this_turn.append(ActionCategory.ACTION)

    ##########################################################################
    def heuristic(self, doer):
        """Should we do this"""
        if not doer.action_surge:
            return 0
        return 0  # Doesn't work yet

    ##########################################################################
    def pick_target(self, doer):
        """Only applies to self"""
        return doer


##############################################################################
##############################################################################
##############################################################################
class DuelingFightingStyle(Effect):
    """When you are wielding a melee weapon in one hand and no other
    weapons, you gain a +2 bonus to damage rolls with that weapon."""

    ########################################################################
    def __init__(self, **kwargs):
        """Initialise"""
        super().__init__("Dueling Fighting Style", **kwargs)

    ########################################################################
    def hook_source_additional_damage(self, attack, source, target):
        """2 more damage"""
        if issubclass(attack.__class__, MeleeAttack):
            return ("", 2, None)
        return ("", 0, None)


# EOF
