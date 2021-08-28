""" Wraith Monster Class """
import colors
from pycs.attack import MeleeAttack
from pycs.constant import DamageType
from pycs.constant import MonsterType
from pycs.constant import Condition
from pycs.constant import Stat
from pycs.monster import Monster


##############################################################################
class Wraith(Monster):
    """Wraith - https://www.dndbeyond.com/monsters/wraith"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "9d8+27"
        kwargs.update(
            {
                "ac": 13,
                "speed": 60,
                "type": MonsterType.UNDEAD,
                "str": 6,
                "dex": 16,
                "con": 16,
                "int": 12,
                "wis": 14,
                "cha": 15,
                "prof_bonus": 3,
                "immunity": [DamageType.POISON, DamageType.NECROTIC],
                "resistant": [
                    DamageType.ACID,
                    DamageType.COLD,
                    DamageType.FIRE,
                    DamageType.LIGHTNING,
                    DamageType.THUNDER,
                    DamageType.BLUDGEONING,
                    DamageType.PIERCING,
                    DamageType.SLASHING,
                ],
                "cond_immunity": [
                    Condition.CHARMED,
                    Condition.EXHAUSTION,
                    Condition.GRAPPLED,
                    Condition.PARALYZED,
                    Condition.PETRIFIED,
                    Condition.POISONED,
                    Condition.PRONE,
                    Condition.RESTRAINED,
                ],
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Life Drain",
                use_stat=Stat.DEX,
                reach=5,
                dmg=("4d8", 0),
                dmg_type=DamageType.NECROTIC,
                side_effect=self.life_drain,
            )
        )

    ##########################################################################
    def life_drain(self, source, target, dmg):  # pylint: disable=unused-argument
        """The target must succeed on a DC 14 Constitution saving throw
        or its hit point maximum is reduced by an amount equal to the damage
        taken. This reduction lasts until the target finishes a long rest.
        The target dies if this effect reduces its hit point maximum to 0."""
        svth = target.saving_throw(Stat.CON, 14)
        if svth:
            print(f"{target} resisted Wraith life drain")
        else:
            print(f"Wraith life drain's {target} of {dmg} hit points")
            target.max_hp -= dmg

    ##########################################################################
    def shortrepr(self):
        """What a wraith looks like on the arena"""
        if self.is_alive():
            return colors.red("W")
        return colors.green("W", bg="red")


# EOF
