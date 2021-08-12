""" Handle non-attack Actions """
import dice


##############################################################################
##############################################################################
##############################################################################
class Action:
    """generic action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        self.name = name
        self.side_effect = kwargs.get("side_effect", self.no_side_effect)

    ########################################################################
    def no_side_effect(self, source, target):
        """No side_effect"""

    ########################################################################
    def range(self):
        """Return the range (good, max) of the action"""
        return 0, 0

    ##########################################################################
    def is_available(self, owner):  # pylint: disable=unused-argument
        """Is this action currently available to the creature"""
        return True

    ########################################################################
    def perform_action(self, source, target):  # pylint: disable=unused-argument
        """Perform the action"""

    ########################################################################
    def __repr__(self):
        return self.name


##############################################################################
##############################################################################
##############################################################################
class SpellHealing(Action):
    """Healing action"""

    ########################################################################
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.cure = kwargs.get("cure")
        self.level = kwargs.get("level")

    ########################################################################
    def max_cure(self, source):
        """What is the most effective cure"""
        mhp = int(dice.roll_max(self.cure[0])) + self.cure[1] + source.spell_modifier
        return mhp

    ########################################################################
    def perform_action(self, source, target, rnge):  # pylint: disable=unused-argument
        """Cure the target"""
        chp = int(dice.roll(self.cure[0])) + self.cure[1] + source.spell_modifier
        target.hp += chp
        target.hp = min(target.max_hp, target.hp)
        print(f"{source} cured {target} of {chp} hp")


# EOF
