"""https://www.dndbeyond.com/races/human"""
from typing import Any
from pycs.race import Race


##############################################################################
##############################################################################
##############################################################################
class Human(Race):
    """Beige"""

    def __init__(self, **kwargs: Any):
        super().__init__("Human", **kwargs)


# EOF
