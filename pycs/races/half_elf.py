"""https://www.dndbeyond.com/races/half-elf"""
from typing import Any
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class HalfElf(Race):
    """Pointy Ears and beards"""

    def __init__(self, **kwargs: Any):
        super().__init__("Half Elf", **kwargs)


# EOF
