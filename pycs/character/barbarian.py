""" Barbarian """
import colors
from attacks import MeleeAttack
from attacks import RangedAttack
from constants import DamageType
from .character import Character


##############################################################################
class Barbarian(Character):
    """Barbarian class"""

    ##########################################################################
    def __init__(self, level, **kwargs):
        self.level = level
        kwargs.update(
            {
                "str": 16,
                "dex": 14,
                "con": 15,
                "int": 11,
                "wis": 13,
                "cha": 9,
                "ac": 16,
                "hp": 14,
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Greataxe",
                reach=5,
                dmg=("1d12", 3),
                dmg_type=DamageType.SLASHING,
            )
        )
        self.add_action(
            RangedAttack(
                "Javelin",
                reach=5,
                ammo=3,
                dmg=("1d6", 3),
                dmg_type=DamageType.PIERCING,
            )
        )

    ##########################################################################
    def report(self):
        """Character Report"""
        super().report()
        javs = self.pick_attack_by_name("Javelin")
        print(f"| Javelins: {javs.ammo}")

    ##########################################################################
    def shortrepr(self):
        """What a fighter looks like in the arena"""
        if self.is_alive():
            return colors.blue("B", bg="green")
        return colors.blue("B", bg="red")


# EOF
