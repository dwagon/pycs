"""https://www.dndbeyond.com/races/elf"""
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class Elf(Race):
    """Pointy Ears"""

    def __init__(self, **kwargs):
        super().__init__("Elf", **kwargs)


# EOF
