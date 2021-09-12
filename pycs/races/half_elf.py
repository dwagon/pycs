"""https://www.dndbeyond.com/races/half-elf"""
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class HalfElf(Race):
    """Pointy Ears and beards"""

    def __init__(self, **kwargs):
        super().__init__("Half Elf", **kwargs)


# EOF
