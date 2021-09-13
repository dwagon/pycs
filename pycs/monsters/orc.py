""" https://www.dndbeyond.com/monsters/orc"""
import colors
from pycs.gear import Javelin
from pycs.gear import Hide
from pycs.gear import Greataxe
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
class Orc(Monster):
    """Orc"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d8+6"
        kwargs.update(
            {
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 16,
                "dex": 12,
                "con": 16,
                "int": 7,
                "wis": 11,
                "cha": 10,
                "gear": [Javelin(ammo=4), Greataxe(), Hide()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What an Orc looks like on the arena"""
        if self.is_alive():
            return colors.green("O")
        return colors.green("O", bg="red")


# EOF
