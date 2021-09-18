""" https://www.dndbeyond.com/monsters/goblin"""
import colors
from pycs.gear import Shortbow
from pycs.gear import Scimitar
from pycs.gear import Leather
from pycs.gear import Shield
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
class Goblin(Monster):
    """Goblin"""

    ##########################################################################
    def __init__(self, **kwargs):
        kwargs.update(
            {
                "hitdice": "2d6",
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 8,
                "dex": 14,
                "con": 10,
                "int": 10,
                "wis": 8,
                "cha": 8,
                "gear": [Scimitar(), Shortbow(), Leather(), Shield()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("g")
        return colors.green("g", bg="red")


# EOF
