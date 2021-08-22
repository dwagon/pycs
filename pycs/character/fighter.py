""" Fighter """
import colors
from actions import Action
from effect import Effect
from attacks import MeleeAttack
from constants import DamageType
from constants import ActionType
from .character import Character


##############################################################################
##############################################################################
##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, level=1, **kwargs):
        self.level = level
        self.second_wind = 1
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
                "ac": 18,
            }
        )
        if level == 1:
            kwargs["hp"] = 12
            # Fighting Style: Dueling
        elif level == 2:
            # Action Surge
            kwargs["hp"] = 20
        elif level == 3:
            kwargs["hp"] = 28
            # Martial Archetype: Champion
        elif level == 4:
            kwargs["hp"] = 36
            kwargs["str"] = 18
        elif level == 5:
            kwargs["str"] = 18
            kwargs["hp"] = 44
            kwargs["attacks_per_action"] = 2
        if level >= 3:
            # Critical on 19 or 20
            kwargs["critical"] = 19
        super().__init__(**kwargs)

        self.add_action(
            MeleeAttack(
                "Longsword",
                reach=5,
                dmg=("1d8", 0),
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_bonus_action(SecondWind())
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
        if doer.max_hp - doer.hp > 10:
            return 1
        return 0

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
    def hook_source_additional_melee_damage(self):
        """2 more damage"""
        return ("", 2, None)


# EOF
