""" Ghast Monster Class """
import colors
from attacks import MeleeAttack
from constants import Condition
from constants import DamageType
from constants import MonsterType
from constants import Stat
from effect import Effect
from .monster import Monster


##############################################################################
##############################################################################
##############################################################################
class Ghast(Monster):
    """Ghast - https://www.dndbeyond.com/monsters/ghast"""

    ##########################################################################
    def __init__(self, **kwargs):
        self.hitdice = "8d8"
        kwargs.update(
            {
                "ac": 13,
                "speed": 30,
                "type": MonsterType.UNDEAD,
                "str": 16,
                "dex": 17,
                "con": 10,
                "int": 11,
                "wis": 10,
                "cha": 8,
                "resistant": [DamageType.NECROTIC],
                "immunity": [DamageType.POISON],
                "cond_immunity": [
                    Condition.CHARMED,
                    Condition.EXHAUSTION,
                    Condition.POISONED,
                ],
            }
        )
        super().__init__(**kwargs)
        self.add_action(
            MeleeAttack(
                "Bite",
                reach=5,
                bonus=3,
                dmg=("2d8", 3),
                dmg_type=DamageType.PIERCING,
            )
        )
        self.add_action(
            MeleeAttack(
                "Claw",
                reach=5,
                bonus=5,
                dmg=("2d6", 3),
                dmg_type=DamageType.SLASHING,
                side_effect=self.ghast_claws,
            )
        )

    ##########################################################################
    def start_others_turn(self, creat):
        """Creature creat is starting a turn"""
        # Stench. Any creature that starts its turn within 5 feet of the
        # ghast must succeed on a DC 10 Constitution saving throw or be
        # poisoned until the start of its next turn. On a successful saving
        # throw, the creature is immune to the ghast's Stench for 24 hours."
        dist = self.arena.distance(self, creat)
        if dist <= 1:
            svth = creat.saving_throw(Stat.CON, 10)
            if not svth:
                creat.add_condition(Condition.POISONED, self)
            else:
                print(f"{creat} resists Ghast's poisonous stench")

    ##########################################################################
    def ghast_claws(self, source):  # pylint: disable=unused-argument
        """If the target is a creature other than an undead, it must
        succeed on a DC 10 Constitution saving throw or be paralyzed for 1
        minute. The target can repeat the saving throw at the end of each
        of its turns, ending the effect on itself on a success."""
        target = self.target
        svth = target.saving_throw(Stat.CON, 10)
        if not svth:
            print(f"{target} got paralysed by {self}")
            target.add_effect(GhastClawEffect(cause=self))
        else:
            print(f"{target} resisted Ghast claws")

    ##########################################################################
    def pick_best_attack(self):
        """Pick the claw attack more often than damage would indicate"""
        if self.target.has_condition(Condition.PARALYZED):
            return self.pick_attack_by_name("Bite")
        else:
            return self.pick_attack_by_name("Claw")

    ##########################################################################
    def shortrepr(self):
        """What it looks like on the arena"""
        if self.is_alive():
            return colors.red("G", bg="green", style="bold")
        return colors.green("G", bg="red")


##############################################################################
##############################################################################
##############################################################################
class GhastClawEffect(Effect):
    """Effect of Ghast Claws"""

    ##########################################################################
    def __init__(self, **kwargs):
        super().__init__("Ghast Claws", **kwargs)

    ##########################################################################
    def initial(self, target):
        target.add_condition(Condition.PARALYZED)

    ##########################################################################
    def removal_end_of_its_turn(self, victim):
        """Check to see if victim can recover from claws"""
        svth = victim.saving_throw(Stat.CON, 10)
        if svth:
            print(f"{victim} no longer paralyzed")
            victim.remove_condition(Condition.PARALYZED)
            return True
        return False


# EOF
