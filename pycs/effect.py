""" Handle Temporary effects """


##############################################################################
##############################################################################
##############################################################################
class Effect:
    """Temporary effects"""

    ##########################################################################
    def __init__(self, name, **kwargs):
        self.name = name
        self.cause = kwargs.get("cause")

    ##########################################################################
    def hook_attack_to_hit(self, target, rnge):  # pylint: disable=unused-argument
        """Modify the roll to hit on attacks"""
        return {"bonus": 0}

    ##########################################################################
    def hook_saving_throw(self, stat):  # pylint: disable=unused-argument
        """Modify the saving throw roll"""
        return {"bonus": 0}

    ##########################################################################
    def initial(self, target):
        """Initial effects on target"""

    ##########################################################################
    def removal_end_of_its_turn(self, victim):  # pylint: disable=unused-argument
        """Do we remove this effect and the end of the victims turn"""
        return False

    ##########################################################################
    def hook_ac_modifier(self, target):  # pylint: disable=unused-argument
        """Modifications to {target}'s armour class"""
        return {"bonus": 0}


# EOF
