""" https://www.dndbeyond.com/monsters/kobold"""
import colors
from pycs.gear import Dagger
from pycs.gear import Sling
from pycs.effect import Effect
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Kobold(Monster):
    """Kobold"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d6-2"
        kwargs.update(
            {
                "ac": 12,
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 7,
                "dex": 15,
                "con": 9,
                "int": 8,
                "wis": 7,
                "cha": 8,
            }
        )
        super().__init__(**kwargs)
        self.add_gear(Dagger())
        self.add_gear(Sling())
        self.add_effect(PackTactics())

    ##########################################################################
    def shortrepr(self):
        """What a goblin looks like on the arena"""
        if self.is_alive():
            return colors.green("k")
        return colors.green("k", bg="red")


##############################################################################
##############################################################################
##############################################################################
class PackTactics(Effect):
    """Pack Tactics. The kobold has advantage on an attack roll against
    a creature if at least one of the kobold's allies is within 5 feet
    of the creature and the ally isn't incapacitated"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Pack Tactics", **kwargs)

    ##########################################################################
    def hook_gives_advantage(self, target):
        """Do pack tactics apply?"""
        allies = [_ for _ in target.pick_closest_enemy() if _ != self.source]
        if allies:
            if allies[0].distance(target) <= 1:
                return True
        return False


# EOF
