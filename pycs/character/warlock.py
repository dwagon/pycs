""" Warlock """
import colors
from attacks import MeleeAttack
from attacks import RangedAttack
from attacks import SpellAttack
from .character import Character


##############################################################################
class Warlock(Character):
    """Warlock class"""

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "str": 9,
                "dex": 14,
                "con": 15,
                "int": 13,
                "wis": 11,
                "cha": 16,
                "ac": 13,
                "hp": 10,
            }
        )
        self.spell_slots = 1
        super().__init__(**kwargs)
        self.add_action(MeleeAttack("mace", reach=5, bonus=1, dmg=("1d6", -1)))
        self.add_action(
            RangedAttack(
                "light crossbow", s_range=80, l_range=320, bonus=4, dmg=("1d8", 2)
            )
        )
        self.add_action(
            SpellAttack("eldritch blast", reach=120, bonus=5, dmg=("1d10", 0), level=0)
        )
        self.add_reaction(
            SpellAttack(
                "hellish rebuke",
                reach=60,
                bonus=5,
                dmg=("2d10", 0),
                reaction=True,
                level=1,
            )
        )

    def shortrepr(self):
        """What a warlock looks like in the arena"""
        if self.is_alive():
            return colors.blue("W")
        else:
            return colors.blue("W", bg="red")


# EOF
