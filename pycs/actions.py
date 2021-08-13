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
    def perform_action(self, source, target):  # pylint: disable=unused-argument
        self.side_effect(source, target)


# EOF
