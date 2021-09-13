""" https://www.dndbeyond.com/monsters/hobgoblin"""
import colors
from pycs.effect import Effect
from pycs.gear import Longbow
from pycs.gear import Longsword
from pycs.gear import Chainmail
from pycs.gear import Shield
from pycs.constant import MonsterType
from pycs.monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Hobgoblin(Monster):
    """Hobgoblin"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "2d8+2"
        kwargs.update(
            {
                "speed": 30,
                "type": MonsterType.HUMANOID,
                "str": 13,
                "dex": 12,
                "con": 12,
                "int": 10,
                "wis": 10,
                "cha": 9,
                "gear": [Longsword(), Longbow(), Chainmail(), Shield()],
                "effects": [MartialAdvantage()],
            }
        )
        super().__init__(**kwargs)

    ##########################################################################
    def shortrepr(self):
        """What a hobgoblin looks like on the arena"""
        if self.is_alive():
            return colors.green("h")
        return colors.green("h", bg="red")


##############################################################################
##############################################################################
##############################################################################
class MartialAdvantage(Effect):
    """Martial Advantage. Once per turn, the hobgoblin can deal an
    extra 7 (2d6) damage to a creature it hits with a weapon attack if
    that creature is within 5 feet of an ally of the hobgoblin that
    isn't incapacitated."""

    ##########################################################################
    def __init__(self, **kwargs):
        self.used_this_turn = False
        super().__init__("Martial Advantage", **kwargs)

    ##########################################################################
    def hook_start_turn(self):
        """Start turn effects"""
        self.used_this_turn = False

    ##########################################################################
    def hook_source_additional_damage(self, attack, source, target):
        """Additional damage?"""
        if self.used_this_turn:
            return ("", 0, None)
        allies = [
            _
            for _ in target.pick_closest_friends()
            if _ != source and _.distance(target) <= 1
        ]
        if allies:
            self.used_this_turn = True
            return ("2d6", 0, None)
        return ("", 0, None)


# EOF
