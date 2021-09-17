""" Fighter """
import colors
from pycs.action import Action
from pycs.attack import MeleeAttack
from pycs.character import Character
from pycs.constant import ActionCategory
from pycs.constant import ActionType
from pycs.constant import Stat
from pycs.effect import Effect


##############################################################################
##############################################################################
##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, **kwargs):
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
                "stat_prof": [Stat.STR, Stat.CON],
                "actions": [SecondWind()],
                "effects": [DuelingFightingStyle()],
            }
        )
        level = kwargs.get("level", 1)
        if level >= 1:
            kwargs["hp"] = 12
            # Fighting Style: Dueling
        if level >= 2:
            kwargs["hp"] = 20
            kwargs["actions"].append(ActionSurge())
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

    ##########################################################################
    def shortrepr(self):  # pragma: no cover
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
    def perform_action(self):
        """Do the action"""
        self.owner.second_wind = 0
        self.owner.heal("d10", self.owner.level)

    ##########################################################################
    def heuristic(self):
        """Should we do this"""
        if not self.owner.second_wind:
            return 0
        return self.owner.max_hp - self.owner.hp

    ##########################################################################
    def pick_target(self):
        """Only applies to self"""
        return self.owner


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
    def perform_action(self):
        """Do the action"""
        self.owner.action_surge = 0
        self.owner.options_this_turn.append(ActionCategory.ACTION)

    ##########################################################################
    def heuristic(self):
        """Should we do this"""
        if not self.owner.action_surge:
            return 0
        return 0  # Doesn't work yet

    ##########################################################################
    def pick_target(self):
        """Only applies to self"""
        return self.owner


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
