""" Base Monster Class """
import dice
from pycs.creature import Creature
from pycs.util import check_args


##############################################################################
class Monster(Creature):
    """Base monster class"""

    def __init__(self, **kwargs):
        check_args(self._valid_args(), self.__class__.__name__, kwargs)
        self.challenge = kwargs.get("challenge")
        hitdice = kwargs.get("hitdice")
        hp = kwargs.get("hp")
        if hp is None and hitdice is not None:
            kwargs["hp"] = max(1, int(dice.roll(hitdice)))

        super().__init__(**kwargs)

    ##########################################################################
    def _valid_args(self):
        """What is valid in this class for kwargs"""
        return super()._valid_args() | {"hitdice", "challenge"}

    ##########################################################################
    def shortrepr(self):
        """Arena repr"""
        return "?"


# EOF
