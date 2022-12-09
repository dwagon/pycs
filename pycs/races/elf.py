"""https://www.dndbeyond.com/races/elf"""
from typing import Any
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class Elf(Race):
    """Pointy Ears"""

    def __init__(self, **kwargs: Any):
        super().__init__("Elf", **kwargs)


# EOF
