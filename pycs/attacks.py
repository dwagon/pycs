""" Handle Attacks """


##############################################################################
class Attack:
    """generic attack"""

    def __init__(self, name, **kwargs):
        self.name = name


##############################################################################
class MeleeAttack(Attack):
    """A melee attack"""

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


##############################################################################
class RangedAttack(Attack):
    """A ranged attack"""

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


# EOF
