""" https://www.dndbeyond.com/monsters/violet-fungus """
import colors
from attacks import MeleeAttack
from constants import DamageType
from constants import MonsterType
from constants import Condition
from .monster import Monster


##############################################################################
class VioletFungus(Monster):
    """Violet Fungus"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "4d8"
        kwargs.update(
            {
                "ac": 5,
                "speed": 5,
                "type": MonsterType.PLANT,
                "str": 3,
                "dex": 1,
                "con": 10,
                "int": 1,
                "wis": 3,
                "cha": 1,
                "cond_immunity": [
                    Condition.BLINDED,
                    Condition.DEAFENED,
                    Condition.FRIGHTENED,
                ],
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "rotting touch",
                attacks_per_action=("1d4", 0),
                reach=10,
                dmg=("1d8", 0),
                dmg_type=DamageType.NECROTIC,
                attack_modifier=2,
                damage_modifier=0,
            )
        )

    ##########################################################################
    def shortrepr(self):
        """What a violet fungus looks like on the arena"""
        if self.is_alive():
            return colors.magenta("v")
        return colors.green("v", bg="red")


# EOF
