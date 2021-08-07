""" Fighter """
import colors
from attacks import MeleeAttack
from .character import Character


##############################################################################
class Fighter(Character):
    """Fighter class"""

    def __init__(self, **kwargs):
        self.hp = 10
        kwargs.update(
            {"str": 16, "dex": 14, "con": 15, "int": 11, "wis": 13, "cha": 9, "ac": 18}
        )
        super().__init__(**kwargs)
        self.add_action(MeleeAttack("longsword", reach=5, bonus="+5", dmg="1d8+3"))

    def shortrepr(self):
        """What a fighter looks like in the arena"""
        return colors.red("F")


# EOF
