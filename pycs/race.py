""" Races """
from typing import Any


##############################################################################
##############################################################################
##############################################################################
class Race:
    """Racial profiling at its best"""

    def __init__(self, name: str, **kwargs: Any):
        self.name = name
        self.owner = None
        self.effects = kwargs.get("effects", [])


# EOF
